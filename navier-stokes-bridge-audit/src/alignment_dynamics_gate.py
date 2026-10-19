"""Reconcile strain-envelope alignment with the exact log-enstrophy budget.

Uses deterministic sampled states from the local scanner and the dense
Galerkin E/G/D/T traces. No temporal or continuum bound is inferred.
"""

import json
import math
from pathlib import Path

from phase_cascade_trajectory import NU

HERE=Path(__file__).resolve().parent


def simpson(values,dt):
    assert len(values)%2==1
    return dt/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+
                 2*sum(values[2:-1:2]))


def read_dense():
    output={}
    for name in ('candidate_inequality_results.json',
                 'candidate_inequality_N7_results.json'):
        data=json.loads((HERE/name).read_text(encoding='utf-8'))
        columns=data['sample_columns']
        for run in data['runs']:
            output[(run['scenario'],run['N'])]=[
                dict(zip(columns,row)) for row in run['samples']]
    return output


def run():
    local=json.loads((HERE/'local_strain_majorant_results.json').read_text(encoding='utf-8'))
    dense=read_dense()
    rows=[]
    for item in local['dynamic_trajectories']:
        scenario,N=item['scenario'],item['N']
        records=dense[(scenario,N)]
        assert len(records)==41 and len(item['snapshots'])==5
        assert all(abs(row['time']-.0005*i)<1e-12 for i,row in enumerate(records))
        samples=[]
        for j,geometry in enumerate(item['snapshots']):
            scalar=records[10*j]
            assert abs(geometry['time']-scalar['time'])<1e-12
            assert abs(geometry['G']-scalar['G'])<1e-8*max(1,scalar['G'])
            assert abs(geometry['T']-scalar['T'])<1e-8*max(1,abs(scalar['T']))
            M=geometry['max_eigenvalue_envelope']
            b=M/geometry['G']
            alpha=geometry['T']/M
            q=NU*scalar['D']/scalar['G']
            samples.append(dict(time=scalar['time'],alignment=alpha,
                                max_strain_per_enstrophy=b,
                                transfer_per_enstrophy=alpha*b,
                                viscous_rate=q,
                                half_log_G_rate=alpha*b-q))
        bint=simpson([x['max_strain_per_enstrophy'] for x in samples],.005)
        c5=simpson([x['transfer_per_enstrophy'] for x in samples],.005)
        visc5=simpson([x['viscous_rate'] for x in samples],.005)
        c41=simpson([x['T']/x['G'] for x in records],.0005)
        visc41=simpson([NU*x['D']/x['G'] for x in records],.0005)
        positive41=simpson([max(x['T'],0)/x['G'] for x in records],.0005)
        log_change=.5*math.log(records[-1]['G']/records[0]['G'])
        assert abs(log_change-c41+visc41)<1e-6
        rows.append(dict(scenario=scenario,N=N,samples=samples,
                         five_point_integral_M_over_G=bint,
                         five_point_integral_T_over_G=c5,
                         five_point_integral_nuD_over_G=visc5,
                         envelope_weighted_signed_alignment=c5/bint,
                         dense_integral_T_over_G=c41,
                         dense_integral_positive_T_over_G=positive41,
                         dense_integral_nuD_over_G=visc41,
                         five_minus_dense_T_over_G=c5-c41,
                         half_log_G_change=log_change,
                         dense_log_budget_residual=log_change-c41+visc41))
    return dict(identity='(log G)/2 derivative = (T/M)(M/G) - nu D/G when G,M>0',
                limitations='The five local alignment samples and 41 scalar samples cover only [0,0.02] for selected finite cutoffs; monotonicity between snapshots, long-time cancellation, and cutoff-uniform control are not established.',
                rows=rows)


if __name__=='__main__':
    result=run()
    path=HERE/'alignment_dynamics_results.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for r in result['rows']:
        print(r['scenario'],r['N'],'alignment endpoints',
              r['samples'][0]['alignment'],r['samples'][-1]['alignment'],
              'weighted avg',r['envelope_weighted_signed_alignment'],flush=True)
    print('Wrote',path)
