"""Time-resolved screen of a trial enstrophy-transfer inequality.

Tests the necessary constant for T <= nu D/2 + C G^(3/2) on specified
finite Galerkin trajectories. A finite sample cannot verify universality.
"""

import argparse
import json
import math
from pathlib import Path

from adversarial_cutoff_gate import SCENARIOS, make_initial
from cutoff_spacetime_gate import observables, simpson
from evolve_galerkin import System
from phase_cascade_trajectory import NU, T_END


def trace(sys, scenario, dt):
    steps=round(T_END/dt)
    assert steps%2==0 and math.isclose(steps*dt,T_END,abs_tol=1e-14)
    state=make_initial(sys,*SCENARIOS[scenario])
    samples=[]
    packed=[]
    for j in range(steps+1):
        row=observables(sys,state)
        g,d,t=row['G'],row['D'],row['T']
        assert g>0 and row['reality_error']<1e-9 and row['divergence_error']<1e-9
        row.update(time=j*dt,
                   positive_transfer=max(0.,t),
                   net_enstrophy_growth=t-NU*d,
                   required_C=max(0.,t-NU*d/2)/g**1.5)
        samples.append(row)
        packed.append([float(f'{row[k]:.12g}') for k in
                       ('time','E','G','D','T','high_G_fraction','required_C')])
        if j<steps: state=sys.rk4(state,dt)
    integrals={key:simpson([r[key] for r in samples],dt)
               for key in ('T','D','G','positive_transfer','required_C')}
    integrals['sqrt_G']=simpson([math.sqrt(r['G']) for r in samples],dt)
    energy_budget=samples[-1]['E']-samples[0]['E']+NU*integrals['G']
    enstrophy_budget=(samples[-1]['G']-samples[0]['G'])/2-integrals['T']+NU*integrals['D']
    assert abs(energy_budget)<1e-4 and abs(enstrophy_budget)<1e-3
    return dict(scenario=scenario,N=sys.N,dt=dt,
                initial_G=samples[0]['G'],initial_E=samples[0]['E'],
                max_required_C=max(r['required_C'] for r in samples),
                time_at_max_required_C=samples[max(range(len(samples)),key=lambda i:samples[i]['required_C'])]['time'],
                integrals=integrals,
                energy_budget_residual=energy_budget,
                enstrophy_budget_residual=enstrophy_budget,
                samples=packed)


def run(scenarios,cutoffs,dt):
    runs=[]
    for scenario in scenarios:
        for N in cutoffs:
            entry=trace(System(N=N,nu=NU),scenario,dt)
            runs.append(entry)
            print(f'{scenario} N={N} C_required={entry["max_required_C"]:.8g} '
                  f'intT={entry["integrals"]["T"]:.8f}',flush=True)
    return dict(candidate='T_N <= nu D_N/2 + C G_N^(3/2)',
                required_C='(T_N - nu D_N/2)_+ / G_N^(3/2)',
                rationale='If a single C held for all smooth fields and cutoffs, a_N=C sqrt(G_N) would be time-integrable via the energy identity; this file only tests finitely many fields and cannot establish such a C.',
                limitation='C inferred from T is descriptive and may grow without bound outside these samples. Finite RK4 sampling can miss a between-sample peak.',
                interval=[0.,T_END],nu=NU,dt=dt,
                scenario_parameters={x:dict(amplitude_factor=SCENARIOS[x][0],
                                            R_phase_offset_radians=SCENARIOS[x][1],
                                            extra_initial_high_G_fraction=SCENARIOS[x][2])
                                     for x in scenarios},
                sample_columns=['time','E','G','D','T','high_G_fraction','required_C'],
                runs=runs)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cutoffs',nargs='+',type=int,default=[4,5,6])
    p.add_argument('--scenarios',nargs='+',choices=list(SCENARIOS),default=list(SCENARIOS))
    p.add_argument('--dt',type=float,default=.0005)
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('candidate_inequality_results.json'))
    x=p.parse_args()
    result=run(x.scenarios,x.cutoffs,x.dt)
    x.output.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
    print(f'Wrote {x.output}',flush=True)
