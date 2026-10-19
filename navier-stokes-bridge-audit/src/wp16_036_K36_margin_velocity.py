"""Directional finite-time derivative attribution for frozen K36 mass margin."""

import argparse
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


def margin(system, a, keys):
    row = hold.evaluate_state(system, a, keys)
    inside = row['absolute_mass_captured']
    outside = row['k_channel_total_abs_group_contribution'] - inside
    return inside-9*outside, row['absolute_mass_fraction']


def components(system, a):
    nonlinear = -system.nonlinear(a)
    viscous = -system.nu*system.square[:, None]*a
    velocity = nonlinear+viscous
    power = np.sum(abs(a)**2, axis=1)
    radial_coeff = np.real(np.einsum('ij,ij->i', np.conj(a), velocity))/power
    phase_coeff = np.imag(np.einsum('ij,ij->i', np.conj(a), velocity))/power
    radial = radial_coeff[:, None]*a
    scalar_phase = 1j*phase_coeff[:, None]*a
    polarization = velocity-radial-scalar_phase
    assert np.max(abs(radial+scalar_phase+polarization-velocity))<1e-10
    return {'full':velocity, 'nonlinear':nonlinear, 'viscous':viscous,
            'radial_magnitude':radial, 'scalar_phase':scalar_phase,
            'vector_polarization':polarization}


def audit(system, a, keys):
    initial, initial_fraction = margin(system, a, keys)
    terms = components(system, a)
    result={'margin':initial,'mass_fraction':initial_fraction,'rates':{}}
    for h in (1e-8, 2e-8):
        rates={}
        for name, v in terms.items():
            plus, plus_fraction=margin(system,a+h*v,keys)
            minus,minus_fraction=margin(system,a-h*v,keys)
            rates[name]={'margin_central':(plus-minus)/(2*h),
                         'fraction_central':(plus_fraction-minus_fraction)/(2*h),
                         'margin_forward':(plus-initial)/h}
        result['rates'][str(h)]=rates
        result.setdefault('additivity_residual',{})[str(h)]=(
            rates['full']['margin_central']-
            sum(rates[k]['margin_central'] for k in
                ('radial_magnitude','scalar_phase','vector_polarization')))
    result['max_component_speed']=float(max(np.max(abs(v)) for v in terms.values()))
    return result


def main():
    p=argparse.ArgumentParser()
    for name in ('n11-json','n12-json','n13-json','source-json','crossings-json','output'):
        p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args()
    names=('n11-json','n12-json','n13-json','source-json','crossings-json')
    j11,j12,j13,source,crossings=[
        json.loads(getattr(args,name.replace('-','_')).read_text()) for name in names]
    hold.System=DealiasedSystem
    keys=hold.frozen_keys(source)
    out={'status':'post-hoc local directional derivative; grouped absolute masses have kinks',
         'N':{}}
    for N,prev,curr in ((12,hold.get_row(j11,11),hold.get_row(j12,12)),
                        (13,hold.get_row(j12,12),hold.get_row(j13,13))):
        system,states=hold.reconstruct(prev,curr)
        out['N'][str(N)]={}
        for name,a in states.items():
            t=crossings['states'][str(N)][name]['coarse_first_fail_time']
            at_anchor=audit(system,a,keys)
            b=a.copy()
            for _ in range(round(t/.0001)):
                b=system.rk4(b,.0001)
            at_exit=audit(system,b,keys)
            out['N'][str(N)][name]={'exit_sample_time':t,'anchor':at_anchor,'exit':at_exit}
            print('DONE',N,name,flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
