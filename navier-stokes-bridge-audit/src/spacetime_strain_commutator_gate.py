"""Exact cross-shell strain commutator and short-time Galerkin budget.

Run beside archived src modules. The time integral is numerical, and no
cutoff-uniform estimate is inferred from this finite-dimensional experiment.
"""

import json
from pathlib import Path

import numpy as np

from phase_cascade_trajectory import DT, NU, System, initial
from smooth_commutator_gate import multipliers
from strain_alignment_trajectory import spatial_fields


def terms(sys, a, grid=32):
    psi = multipliers(sys)
    grad, omega, shells, imag = spatial_fields(sys, a, grid, psi)
    S = (grad + np.swapaxes(grad, -1, -2)) * 0.5
    Somega = np.einsum('...ij,...j->...i', S, omega)
    Tgrid = float(np.mean(np.sum(omega * Somega, axis=-1)))
    S_hat = np.fft.fftn(Somega, axes=(0, 1, 2)) / grid**3
    idx = tuple((sys.waves % grid).T)
    S_modes = S_hat[idx]
    omega_hat = 1j * np.cross(sys.waves, a)
    shell_terms = []
    for j, w in enumerate(shells):
        Q = float(np.mean(np.sum(w * np.einsum('...ij,...j->...i', S, w), axis=-1)))
        P2 = float(np.real(np.einsum('i,ij,ij->', psi[j]**2,
                                      omega_hat.conj(), S_modes)))
        shell_terms.append(dict(level=j, Q=Q, commutator=P2-Q,
                                projected_full_stretching=P2))
    nonlinear = sys.nonlinear(a)
    Tfourier = -float(np.real(np.einsum('i,ij,ij->', sys.square, a.conj(), nonlinear)))
    G = float(np.sum(sys.square[:, None] * abs(a)**2))
    D = float(np.sum(sys.square[:, None]**2 * abs(a)**2))
    Qsum = sum(s['Q'] for s in shell_terms)
    Rsum = sum(s['commutator'] for s in shell_terms)
    assert abs(Tfourier-Tgrid) < 1e-8
    assert abs(Tfourier-Qsum-Rsum) < 1e-8
    assert imag < 1e-10
    return dict(G=G, D=D, T=Tfourier, Qsum=Qsum, Rsum=Rsum,
                shell_terms=shell_terms, identity_error=Tfourier-Qsum-Rsum)


def composite_simpson(values, step):
    assert len(values) % 2 == 1
    return step/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+2*sum(values[2:-1:2]))


def run():
    runs = []
    for N in (4, 5):
        sys = System(N=N, nu=NU)
        a = initial(sys, 0)
        rows = []
        for step in range(41):
            row = terms(sys, a)
            row['time'] = step * DT
            rows.append(row)
            if step < 40:
                a = sys.rk4(a, DT)
        fine = {key: composite_simpson([row[key] for row in rows], DT)
                for key in ('T','Qsum','Rsum','D')}
        coarse = {key: composite_simpson([row[key] for row in rows[::2]], 2*DT)
                  for key in ('T','Qsum','Rsum','D')}
        halfG_change = (rows[-1]['G']-rows[0]['G'])/2
        budget_residual = halfG_change-fine['T']+NU*fine['D']
        assert abs(fine['T']-fine['Qsum']-fine['Rsum']) < 1e-9
        assert abs(budget_residual) < 1e-4
        runs.append(dict(N=N, initial=rows[0], final=rows[-1],
                         integral_simpson_dt_0_0005=fine,
                         integral_simpson_dt_0_001=coarse,
                         integration_resolution_differences={key:fine[key]-coarse[key]
                             for key in fine},
                         half_G_change=halfG_change,
                         integrated_budget_residual=budget_residual,
                         max_instantaneous_commutator_identity_error=max(abs(row['identity_error']) for row in rows)))
    return dict(interval=[0, .02], dt=DT, nu=NU,
                identity='T=Q+R; Q=sum_j <P_j omega,S P_j omega>; R=sum_j <P_j omega,[P_j,S]omega>; P_j real self-adjoint, sum_j P_j^2=I on nonzero modes',
                limitation='Finite-cutoff RK4 trajectories only; Simpson comparisons show quadrature refinement, not a rigorous continuum or cutoff-uniform bound.',
                runs=runs)


if __name__ == '__main__':
    result = run()
    path = Path(__file__).with_name('spacetime_strain_commutator_results.json')
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('Wrote',path)
    for r in result['runs']:
        print('N',r['N'], 'final T,Q,R',*[round(r['final'][k],6) for k in ('T','Qsum','Rsum')])
        print('integrals',r['integral_simpson_dt_0_0005'])
        print('resolution differences',r['integration_resolution_differences'])
        print('integrated budget residual',r['integrated_budget_residual'])
