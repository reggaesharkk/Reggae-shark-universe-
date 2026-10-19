"""Retained-shell occupancy versus omitted nonlinear boundary response.

Provides an exact two-shell-only non-identifiability witness at initial time
and short finite-Galerkin trajectories for four selected cases.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU

HERE=Path(__file__).resolve().parent


def simpson(values,dt):
    assert len(values)%2==1
    return dt/3*(values[0]+values[-1]+
                 4*sum(values[1:-1:2])+2*sum(values[2:-1:2]))


def bands(sys,a,nonlinear=None):
    if nonlinear is None:
        nonlinear=sys.nonlinear(a)
    output=[]
    for upper in (sys.N-1,sys.N):
        support=(sys.square>(upper-1)**2)&(sys.square<=upper**2)
        w=sys.square[support]
        x=a[support]
        nl=nonlinear[support]
        energy=float(.5*np.sum(abs(x)**2))
        G=float(np.sum(w[:,None]*abs(x)**2))
        D=float(np.sum(w[:,None]**2*abs(x)**2))
        transfer=-float(np.real(np.einsum('i,ij,ij->',w,x.conj(),nl)))
        Gdot=2*(transfer-NU*D)
        return_entry=dict(radial_band=(upper-1,upper),energy=energy,
                          G=G,D=D,T=transfer,Gdot=Gdot)
        output.append(return_entry)
    return output


def run():
    old=json.loads((HERE/'projection_shell_results.json').read_text(encoding='utf-8'))
    dense={}
    for filename in ('candidate_inequality_results.json','candidate_inequality_N7_results.json'):
        data=json.loads((HERE/filename).read_text(encoding='utf-8'))
        for item in data['runs']:
            dense[(item['scenario'],item['N'])]=item['samples']
    initial_cases=[]
    temporal=[]
    zero_field_comparison=None
    for existing in old['rows']:
        name,N=existing['scenario'],existing['N']
        sys=System(N=N,nu=NU)
        a=make_initial(sys,*SCENARIOS[name])
        band0=bands(sys,a)
        observed=existing['samples'][0]
        first=observed['shells'][0]
        initial_cases.append(dict(scenario=name,N=N,retained_top_two=band0,
                                  first_omitted_R_l2=first['R_l2'],
                                  first_omitted_J=first['total'],
                                  full_J=observed['projection_response']))
        if name=='combined_double_quarter_high' and N==6:
            assert all(x['G']==0 and x['energy']==0 for x in band0)
            assert first['R_l2']>1 and abs(observed['projection_response'])>1
            zero_field_comparison=dict(N=6,top_two_coefficients='identically zero for both',
                zero_field_R_l2=0.,zero_field_J=0.,
                nonzero_field_first_R_l2=first['R_l2'],
                nonzero_field_J=observed['projection_response'])
        if (name,N) not in {('reference',4),('reference',7),
                            ('combined_double_quarter_high',4),
                            ('combined_double_quarter_high',7)}:
            continue
        records=[]
        for step in range(41):
            nonlin=sys.nonlinear(a)
            current=bands(sys,a,nonlin)
            row=dict(time=step*DT,retained_top_two=current)
            if step%10==0:
                stored=dense[(name,N)][step]
                full_G=float(np.sum(sys.square[:,None]*abs(a)**2))
                full_T=-float(np.real(np.einsum(
                    'i,ij,ij->',sys.square,a.conj(),nonlin)))
                assert abs(full_G-stored[2])<1e-8*max(1,abs(full_G))
                assert abs(full_T-stored[4])<1e-8*max(1,abs(full_T))
            if step%10==0:
                snap=existing['samples'][step//10]
                assert abs(snap['time']-row['time'])<1e-12
                row['first_omitted_R_l2']=snap['shells'][0]['R_l2']
                row['first_omitted_J']=snap['shells'][0]['total']
                row['full_J']=snap['projection_response']
            records.append(row)
            if step<40:
                # Avoid recalculating the first RK stage, while preserving
                # exactly the same classical RK4 formula as sys.rk4.
                k1=-nonlin-NU*sys.square[:,None]*a
                k2=sys.rhs(a+DT*k1/2)
                k3=sys.rhs(a+DT*k2/2)
                k4=sys.rhs(a+DT*k3)
                a=a+DT*(k1+2*k2+2*k3+k4)/6
        checks=[]
        for i in range(2):
            G=[row['retained_top_two'][i]['G'] for row in records]
            T=[row['retained_top_two'][i]['T'] for row in records]
            D=[row['retained_top_two'][i]['D'] for row in records]
            error=(G[-1]-G[0])/2-simpson(T,DT)+NU*simpson(D,DT)
            assert abs(error)<1e-3*max(1,abs(G[-1]),abs(G[0]))
            checks.append(error)
        temporal.append(dict(scenario=name,N=N,band_budget_residuals=checks,
                             samples=records))
        print(name,N,'high G',round(records[0]['retained_top_two'][1]['G'],6),
              round(records[-1]['retained_top_two'][1]['G'],6),
              'R',round(records[0]['first_omitted_R_l2'],6),
              round(records[-1]['first_omitted_R_l2'],6),flush=True)
    assert len(initial_cases)==24 and len(temporal)==4
    return dict(analytic_witness='Top two retained shells cannot determine R or J: the zero field and the N=6 combined initial field agree exactly on both upper shells while R and J differ.',
                limitation='The trajectories run only to .02 and shell occupancy is not a proxy for the full quadratic convolution; no predictive PDE closure or cutoff-uniform bound is established.',
                zero_field_comparison=zero_field_comparison,
                initial_cases=initial_cases,temporal=temporal)


if __name__=='__main__':
    result=run()
    target=HERE/'boundary_capacity_results.json'
    target.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
    print('Wrote',target)
