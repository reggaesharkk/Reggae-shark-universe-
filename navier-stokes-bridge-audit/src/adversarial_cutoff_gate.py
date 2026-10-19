"""Finite Galerkin amplitude, phase, and high-frequency stress tests.

Execute from the repository root. Keeps the same initial modes inside every
tested cutoff. Numerical observations cannot establish a uniform PDE bound.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from cutoff_spacetime_gate import observables, simpson
from evolve_galerkin import System
from phase_cascade_trajectory import NU, T_END, initial


SCENARIOS = {
    'reference': (1., 0., 0.),
    'half_amplitude': (.5, 0., 0.),
    'double_amplitude': (2., 0., 0.),
    'quarter_phase': (1., math.pi/2, 0.),
    'opposite_phase': (1., math.pi, 0.),
    'high_frequency_25pct_G': (1., 0., .25),
    'combined_double_quarter_high': (2., math.pi/2, .25),
}


def make_initial(sys, scale, phase_offset, high_fraction):
    if sys.N < 4:
        raise ValueError('N>=4 required for shared high-frequency modes')
    state = scale*initial(sys, phase_offset)
    initial_G = float(np.sum(sys.square[:,None]*abs(state)**2))
    if high_fraction:
        # Two exact |k|^2=13 pairs, all present already in the N=4 ball.
        # Their transverse polarizations are deterministic and conjugate-real.
        wavevectors = ((3,2,0),(2,-3,0))
        coefficient = math.sqrt(high_fraction/(1-high_fraction)*initial_G/(4*13))
        for k in wavevectors:
            v = np.asarray((-k[1],k[0],0),float)/math.sqrt(13)
            w = np.array((0.,0.,1.))
            polarization = (v+1j*w)/math.sqrt(2)
            state[sys.index[k]] = coefficient*polarization
            state[sys.index[tuple(-x for x in k)]] = coefficient*polarization.conj()
        full_G = float(np.sum(sys.square[:,None]*abs(state)**2))
        actual = (full_G-initial_G)/full_G
        assert abs(actual-high_fraction)<1e-12
    return state


def evolve(sys, scenario, dt):
    scale, phase, high_fraction = SCENARIOS[scenario]
    steps = round(T_END/dt)
    assert steps%2==0 and math.isclose(steps*dt,T_END,abs_tol=1e-14)
    state=make_initial(sys,scale,phase,high_fraction)
    values={key:[] for key in ('E','G','D','T','high_G_fraction')}
    for j in range(steps+1):
        row=observables(sys,state)
        for key in values: values[key].append(row[key])
        assert row['reality_error']<1e-9 and row['divergence_error']<1e-9
        if j<steps: state=sys.rk4(state,dt)
    integrals={key:simpson(values[key],dt) for key in ('G','D','T')}
    integrals['positive_T']=simpson([max(t,0.) for t in values['T']],dt)
    integrals['positive_growth']=simpson([max(t-NU*d,0.) for t,d in zip(values['T'],values['D'])],dt)
    # This fitted coefficient is explicitly descriptive, not a proof bound.
    integrals['required_coefficient']=simpson(
        [max(0.,t-NU*d/2)/g for t,d,g in zip(values['T'],values['D'],values['G'])],dt)
    energy_error=values['E'][-1]-values['E'][0]+NU*integrals['G']
    enstrophy_error=.5*(values['G'][-1]-values['G'][0])-integrals['T']+NU*integrals['D']
    return dict(dt=dt, initial={k:values[k][0] for k in values},
                final={k:values[k][-1] for k in values},
                min_T=min(values['T']),max_T=max(values['T']),
                max_G=max(values['G']),
                max_high_G_fraction=max(values['high_G_fraction']),
                integrals=integrals,
                energy_budget_residual=energy_error,
                enstrophy_budget_residual=enstrophy_error),state


def run(cutoffs,scenarios,dt,refine):
    rows=[]
    for scenario in scenarios:
        for N in cutoffs:
            sys=System(N=N,nu=NU)
            coarse,ac=evolve(sys,scenario,dt)
            fine,af=evolve(sys,scenario,dt/2) if scenario in refine else (None,None)
            if fine:
                coarse['dt_refinement']={
                    'integral_T_difference':fine['integrals']['T']-coarse['integrals']['T'],
                    'integral_positive_T_difference':fine['integrals']['positive_T']-coarse['integrals']['positive_T'],
                    'final_state_l2_difference':float(np.linalg.norm(af-ac)),
                    'refined_energy_budget_residual':fine['energy_budget_residual'],
                    'refined_enstrophy_budget_residual':fine['enstrophy_budget_residual']}
            assert abs(coarse['energy_budget_residual'])<1e-4
            assert abs(coarse['enstrophy_budget_residual'])<1e-3
            rows.append(dict(scenario=scenario,N=N,modes=len(sys.modes),
                             ordered_pairs=len(sys.out),trajectory=coarse))
            print(f'{scenario} N={N} intT={coarse["integrals"]["T"]:.8f} '
                  f'intT+={coarse["integrals"]["positive_T"]:.8f}',flush=True)
    return dict(interval=[0.,T_END],nu=NU,dt=dt,
                high_modes=[[3,2,0],[2,-3,0]],
                initial_high_G_fraction_when_enabled=.25,
                scenario_parameters={x:dict(amplitude_factor=SCENARIOS[x][0],
                                            R_phase_offset_radians=SCENARIOS[x][1],
                                            initial_extra_high_G_fraction=SCENARIOS[x][2])
                                     for x in scenarios},
                warning='The required_coefficient integral uses the unknown transfer and is tautological. Do not treat it as an a priori bound. Finite cutoffs and short time do not establish PDE regularity or continuum convergence.',
                runs=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cutoffs',nargs='+',type=int,default=[4,5,6])
    p.add_argument('--scenarios',nargs='+',choices=list(SCENARIOS),default=list(SCENARIOS))
    p.add_argument('--refine',nargs='+',choices=list(SCENARIOS),default=['reference','double_amplitude','high_frequency_25pct_G','combined_double_quarter_high'])
    p.add_argument('--dt',type=float,default=.0005)
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('adversarial_cutoff_results.json'))
    x=p.parse_args()
    result=run(x.cutoffs,x.scenarios,x.dt,x.refine)
    x.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {x.output}',flush=True)
