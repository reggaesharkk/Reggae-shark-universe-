"""Verify exact finite-Galerkin Gevrey commutator and shell expansion.

Only algebra is checked. This does not establish a cutoff-uniform bound.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import NU
from smooth_commutator_gate import multipliers
from smooth_gevrey_identity_audit import schedule_persistence, schedule_smoothing


def audit(sys, a, s, sigma):
    r = np.sqrt(sys.square.astype(float))
    m = np.zeros_like(r)
    positive = r > 0
    m[positive] = np.exp(sigma*r[positive]) * r[positive]**s
    psi = multipliers(sys)
    partition_error = float(np.max(np.abs(
        np.sum(psi[:, positive]**2, axis=0) - 1.0)))

    # P_k acts on the conjugate output coefficient by self-adjointness.
    projected_conj = np.einsum('kij,kj->ki', sys.projectors, np.conj(a))
    qdot = np.einsum('ij,ij->i', sys.qwaves, a[sys.left])
    inner = np.einsum('ij,ij->i', projected_conj[sys.out], a[sys.right])
    base = 1j * qdot * inner
    nonlinear = sys.nonlinear(a)
    direct = -float(np.real(np.einsum(
        'k,kj,kj->', m*m, np.conj(a), nonlinear)))
    unweighted_pairs = -float(np.real(np.sum(
        m[sys.out]**2 * base)))
    commutator = -float(np.real(np.sum(
        m[sys.out]*(m[sys.out]-m[sys.right])*base)))
    transport = -float(np.real(np.sum(
        m[sys.out]*m[sys.right]*base)))

    shells = []
    for j, pj in enumerate(psi):
        mj = m*pj
        shell_direct = -float(np.real(np.einsum(
            'k,kj,kj->', mj*mj, np.conj(a), nonlinear)))
        shell_commutator = -float(np.real(np.sum(
            mj[sys.out]*(mj[sys.out]-mj[sys.right])*base)))
        shell_transport = -float(np.real(np.sum(
            mj[sys.out]*mj[sys.right]*base)))
        shells.append(dict(level=j, direct=shell_direct,
                           commutator=shell_commutator,
                           transport=shell_transport))

    values = [direct, unweighted_pairs, commutator,
              sum(x['direct'] for x in shells),
              sum(x['commutator'] for x in shells)]
    relative_error = max(abs(x-direct) for x in values) / max(1., abs(direct))
    transport_relative_error = max(
        [abs(transport)] + [abs(x['transport']) for x in shells]
    ) / max(1., abs(direct))
    shell_relative_error = max(
        abs(x['direct']-x['commutator']) for x in shells
    ) / max(1., abs(direct))
    if max(relative_error, transport_relative_error,
           shell_relative_error, partition_error) > 1e-10:
        raise AssertionError('Gevrey commutator identity did not close')
    return dict(sigma=sigma, nonlinear=direct,
                pair_sum=unweighted_pairs, commutator=commutator,
                transport=transport, shells=shells,
                relative_error=relative_error,
                transport_relative_error=transport_relative_error,
                shell_relative_error=shell_relative_error,
                partition_error=partition_error)


def run(cutoffs=(4,7), scenarios=('reference',
            'combined_double_quarter_high'), s=2., dt=.0005,
        t_end=.005):
    steps = round(t_end/dt)
    if s <= 1.5 or steps < 1 or not math.isclose(
            steps*dt, t_end, abs_tol=1e-14):
        raise ValueError('Need s>3/2 and positive integral number of steps')
    rows = []
    for name in scenarios:
        for N in cutoffs:
            sys = System(N=N, nu=NU)
            a = make_initial(sys, *SCENARIOS[name])
            for step in range(steps+1):
                if step in (0, steps):
                    t=step*dt
                    weights = {'zero_radius': 0.,
                               'persistence': schedule_persistence(t)[0],
                               'smoothing': schedule_smoothing(t)[0]}
                    rows.append(dict(N=N, scenario=name, time=t,
                                     weights={label:audit(sys,a,s,sigma)
                                              for label,sigma in weights.items()}))
                if step < steps:
                    a = sys.rk4(a,dt)
    return dict(s=s, nu=NU, dt=dt, interval=[0.,t_end], rows=rows,
                scope='Exact finite Galerkin algebra only; no inequality or analyticity radius.')


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cutoffs',type=int,nargs='+',default=[4,7])
    p.add_argument('--scenarios',nargs='+',choices=list(SCENARIOS),
                   default=['reference','combined_double_quarter_high'])
    p.add_argument('--dt',type=float,default=.0005)
    p.add_argument('--t-end',type=float,default=.005)
    p.add_argument('--s',type=float,default=2.)
    p.add_argument('--output',type=Path,default=Path(__file__).with_name(
        'gevrey_commutator_identity_results.json'))
    args=p.parse_args()
    result=run(args.cutoffs,args.scenarios,args.s,args.dt,args.t_end)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('Wrote',args.output)
    print('max relative identity error',max(
        v['relative_error'] for row in result['rows']
        for v in row['weights'].values()))
