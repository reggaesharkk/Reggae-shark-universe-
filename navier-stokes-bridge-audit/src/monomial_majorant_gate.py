"""Analytic scaling certificate plus descriptive screening of stored traces.

The calculation classifies T <= nu D/2 + C(E0,nu) G^(1+p).
Observed constants are never treated as universal bounds.
"""

import json
from pathlib import Path

from phase_cascade_trajectory import NU


HERE=Path(__file__).resolve().parent
EXPONENTS=(0.,.5,1.,1.25)


def load_runs():
    runs=[]
    for name in ('candidate_inequality_results.json',
                 'candidate_inequality_N7_results.json'):
        payload=json.loads((HERE/name).read_text(encoding='utf-8'))
        cols=payload['sample_columns']
        assert len(cols)==7
        for run in payload['runs']:
            records=[dict(zip(cols,row)) for row in run['samples']]
            assert len(records)==round(.02/payload['dt'])+1
            runs.append((run,records))
    return runs


def certificate(p):
    # Under fixed-energy concentration: G ~ lambda^2, D ~ lambda^4,
    # T ~ lambda^(9/2). The viscosity term has exponent 4.
    residual_exponent=2*(1+p)
    return dict(p=p,transfer_exponent=4.5,dissipation_exponent=4.,
                residual_exponent=residual_exponent,
                fixed_energy_concentration=(
                    'refuted for all smooth data' if residual_exponent<4.5
                    else 'not excluded by this scaling test'),
                coefficient_integral_from_energy=(
                    'bounded by energy identity on finite intervals' if p<=1
                    else 'not bounded by the energy identity alone'))


def run():
    rows=[]
    for entry,records in load_runs():
        factors={f'p={p:g}':max(max(0.,r['T']-NU*r['D']/2)/r['G']**(1+p)
                              for r in records) for p in EXPONENTS}
        standard=max(abs(r['T'])/(r['G']**.75*r['D']**.75)
                     for r in records)
        assert abs(factors['p=0.5']-entry['max_required_C'])<1e-11
        rows.append(dict(scenario=entry['scenario'],N=entry['N'],
                         necessary_sampled_constants=factors,
                         standard_G_3_4_D_3_4_ratio=standard))
    return dict(trial='T <= nu D/2 + C(E0,nu) G^(1+p)',
                scope='Fixed-energy spatial concentration excludes every p<5/4 for a coefficient depending only on E0 and nu. p>=5/4 is not excluded by this scaling, but its G^p time integral is not controlled by the energy identity.',
                standard_estimate='|T| <= C G^(3/4) D^(3/4); Young gives nu D/2 + C_nu G^3, whose Gronwall coefficient is proportional to G^2; energy supplies only integral G.',
                warning='Empirical ratios are maxima over finitely sampled Galerkin trajectories; they do not prove any inequality.',
                analytic_certificates=[certificate(p) for p in EXPONENTS],
                runs=rows)


if __name__=='__main__':
    result=run()
    destination=HERE/'monomial_majorant_results.json'
    destination.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {destination.name}; {len(result["runs"])} trajectory records')
    for x in result['runs']:
        if x['scenario'] in ('reference','high_frequency_25pct_G',
                             'combined_double_quarter_high'):
            print(x['scenario'],x['N'],x['necessary_sampled_constants'],
                  x['standard_G_3_4_D_3_4_ratio'])
