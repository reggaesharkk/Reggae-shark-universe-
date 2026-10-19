"""Cutoff and time-step audit of the signed total enstrophy transfer.

Run from the repository root: python src/cutoff_spacetime_gate.py
The exact finite Galerkin convolution uses the aligned two-scale initial field
from phase_cascade_trajectory.py. This is a diagnostic, not a PDE estimate.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU, T_END, initial


def observables(sys, a):
    powers = np.sum(abs(a)**2, axis=1)
    n = sys.nonlinear(a)
    return dict(E=.5*float(np.sum(powers)),
                G=float(np.dot(sys.square, powers)),
                D=float(np.dot(sys.square**2, powers)),
                T=-float(np.real(np.einsum('i,ij,ij->', sys.square, a.conj(), n))),
                high_G_fraction=float(np.dot(sys.square[sys.square > (.75*sys.N)**2],
                                             powers[sys.square > (.75*sys.N)**2]) /
                                      np.dot(sys.square, powers)),
                reality_error=float(np.max(np.linalg.norm(a[sys.neg]-a.conj(), axis=1))),
                divergence_error=float(np.max(abs(np.einsum('ij,ij->i',sys.waves,a)))))


def simpson(values, dt):
    assert len(values) % 2 == 1
    return dt/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+
                 2*sum(values[2:-1:2]))


def run_one(sys, dt):
    steps = round(T_END/dt)
    assert steps % 2 == 0 and math.isclose(steps*dt,T_END,abs_tol=1e-14)
    a = initial(sys, 0.)
    rows = []
    for step in range(steps+1):
        row = observables(sys, a)
        rows.append(row)
        assert row['reality_error'] < 1e-9 and row['divergence_error'] < 1e-9
        if step < steps:
            a = sys.rk4(a,dt)
    integral = {key:simpson([r[key] for r in rows],dt)
                for key in ('G','D','T')}
    integral['positive_T'] = simpson([max(0.,r['T']) for r in rows],dt)
    integral['positive_growth'] = simpson([max(0.,r['T']-NU*r['D']) for r in rows],dt)
    energy_budget = rows[-1]['E']-rows[0]['E']+NU*integral['G']
    enstrophy_budget = .5*(rows[-1]['G']-rows[0]['G'])-integral['T']+NU*integral['D']
    return dict(dt=dt,steps=steps,initial=rows[0],final=rows[-1],
                max_G=max(r['G'] for r in rows),
                max_T=max(r['T'] for r in rows),
                max_high_G_fraction=max(r['high_G_fraction'] for r in rows),
                integral=integral,energy_budget_residual=energy_budget,
                enstrophy_budget_residual=enstrophy_budget),a


def run(cutoffs=(4,5,6,7),dt=.0005):
    runs=[]
    finals={}
    for N in cutoffs:
        sys=System(N=N,nu=NU)
        coarse,ac=run_one(sys,dt)
        fine,af=run_one(sys,dt/2)
        refinement=dict(final_state_l2_difference=float(np.linalg.norm(ac-af)),
                        integral_differences={key:fine['integral'][key]-coarse['integral'][key]
                                              for key in fine['integral']},
                        final_T_difference=fine['final']['T']-coarse['final']['T'],
                        final_G_difference=fine['final']['G']-coarse['final']['G'])
        assert abs(fine['energy_budget_residual'])<1e-5
        assert abs(fine['enstrophy_budget_residual'])<1e-4
        runs.append(dict(N=N,modes=len(sys.modes),ordered_pairs=len(sys.out),
                         coarse=coarse,refined=fine,refinement=refinement))
        finals[N]=(sys,af)
        print(f'N={N}: intT={fine["integral"]["T"]:.9f}, '
              f'intT+={fine["integral"]["positive_T"]:.9f}, '
              f'finalT={fine["final"]["T"]:.6f}',flush=True)
    comparisons=[]
    for low,high in zip(cutoffs,cutoffs[1:]):
        lo,al=finals[low]
        hi,ah=finals[high]
        projected=ah[[hi.index[k] for k in lo.modes]]
        comparisons.append(dict(low=low,high=high,
                                final_shared_mode_l2_difference=float(np.linalg.norm(al-projected)),
                                integrated_T_difference=runs[cutoffs.index(high)]['refined']['integral']['T']-
                                                        runs[cutoffs.index(low)]['refined']['integral']['T'],
                                integrated_positive_T_difference=runs[cutoffs.index(high)]['refined']['integral']['positive_T']-
                                                                 runs[cutoffs.index(low)]['refined']['integral']['positive_T']))
    return dict(interval=[0.,T_END],nu=NU,cutoffs=list(cutoffs),
                initial_field='Same aligned two-scale field from phase_cascade_trajectory.initial; embedded unchanged in every Fourier ball.',
                transfer='T=-Re sum_k |k|^2 conjugate(a_k) dot P_k[(u dot grad)u]_k = <omega dot S omega> at each cutoff.',
                interpretation='Short finite-cutoff evidence only. No uniform-in-cutoff estimate, continuum convergence rate, global regularity, or long-time claim.',
                runs=runs,comparisons=comparisons)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cutoffs',type=int,nargs='+',default=[4,5,6,7])
    parser.add_argument('--dt',type=float,default=.0005)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('cutoff_spacetime_results.json'))
    args=parser.parse_args()
    result=run(args.cutoffs,args.dt)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {args.output}',flush=True)
