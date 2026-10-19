"""Post-hoc stress tests of frozen K36 states; no coalition retuning."""

import argparse
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem
from wp16_expanded_phase_search import canonical_half


def stress(system, a, keys, rng, draws):
    pairs = [(i, system.index[tuple(-v for v in k)])
             for i,k in enumerate(system.modes) if canonical_half(k)]
    result = {}
    for kind, levels in (('phase_radians',(0.04,0.08,0.20)),
                         ('relative_amplitude',(0.02,0.05,0.10))):
        for level in levels:
            rows=[]
            for _ in range(draws):
                b=a.copy()
                changes=rng.uniform(-level,level,len(pairs))
                for (i,j),d in zip(pairs,changes):
                    b[i] *= np.exp(1j*d) if kind=='phase_radians' else (1+d)
                    b[j] = np.conj(b[i])
                row=hold.evaluate_state(system,b,keys)
                rows.append({'mass_fraction':row['absolute_mass_fraction'],
                             'signed_share':row['signed_share_of_channel_total'],
                             'pass':row['passes_preregistered_consistency_criteria']})
            result[f'{kind}_{level}']={
                'draws':draws,'pass_count':sum(x['pass'] for x in rows),
                'min_mass_fraction':min(x['mass_fraction'] for x in rows),
                'max_mass_fraction':max(x['mass_fraction'] for x in rows),
                'min_signed_share':min(x['signed_share'] for x in rows),
                'max_signed_share':max(x['signed_share'] for x in rows)}
    return result


def grid_stress(system,a):
    out={}
    base=system.rhs(a)
    original_L=system.L
    original_slots=system.slots
    for L in (3*system.N+1,4*system.N+1,5*system.N+1):
        system.L=L
        system.slots=tuple(system.waves[:,j] % L for j in range(3))
        rhs=system.rhs(a)
        out[str(L)]={'max_abs_rhs_difference_from_4N_plus_1':float(np.max(abs(rhs-base)))}
    system.L=original_L
    system.slots=original_slots
    return out


def targeted(system,a,keys,envelope):
    ranked=envelope['outside_group_envelopes_ranked']
    cases={}
    for count in (1,5,10):
        orbit_set={tuple(row[side]) for row in ranked[:count]
                   for side in ('left_orbit','right_orbit')}
        mask=np.asarray([hold.orbit(k) in orbit_set for k in system.modes])
        for factor in (1.1,1.25,1.5,2.0,3.0,4.0):
            b=a.copy();b[mask]*=factor
            row=hold.evaluate_state(system,b,keys)
            cases[f'top{count}_outside_orbits_x{factor}']={
                'orbit_count':len(orbit_set),'mode_count':int(mask.sum()),
                'mass_fraction':row['absolute_mass_fraction'],
                'signed_share':row['signed_share_of_channel_total'],
                'pass':row['passes_preregistered_consistency_criteria']}
    for gamma in (0.1,0.25,0.5,1.0,2.0):
        b=a*np.exp(gamma*system.square[:,None]/system.N**2)
        row=hold.evaluate_state(system,b,keys)
        cases[f'radial_exp_{gamma}']={
            'max_amplitude_factor':float(np.exp(gamma)),
            'mass_fraction':row['absolute_mass_fraction'],
            'signed_share':row['signed_share_of_channel_total'],
            'pass':row['passes_preregistered_consistency_criteria']}
    return cases


def main():
    p=argparse.ArgumentParser()
    for name in ('n11-json','n12-json','n13-json','source-json','envelope','output'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--draws',type=int,default=32)
    args=p.parse_args()
    j11,j12,j13,source=[json.loads(getattr(args,n.replace('-','_')).read_text())
                         for n in ('n11-json','n12-json','n13-json','source-json')]
    hold.System=DealiasedSystem
    keys=hold.frozen_keys(source)
    rng=np.random.default_rng(20260926)
    envelopes=json.loads(args.envelope.read_text())['N']
    out={'status':'post-hoc exploratory stress, frozen K36 unchanged','seed':20260926,
         'draws_per_setting':args.draws,'N':{}}
    for N,prev,curr in ((12,hold.get_row(j11,11),hold.get_row(j12,12)),
                        (13,hold.get_row(j12,12),hold.get_row(j13,13))):
        system,states=hold.reconstruct(prev,curr)
        a=states['full_final']
        out['N'][str(N)]={'grid':grid_stress(system,a),
                          'baseline':hold.evaluate_state(system,a,keys),
                          'random':stress(system,a,keys,rng,args.draws),
                          'targeted':targeted(system,a,keys,envelopes[str(N)])}
        print('COMPLETE',N,flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
