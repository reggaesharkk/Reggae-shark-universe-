"""Exact ordered-source rate envelope for the frozen K36 mass margin."""

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


def audit(system, a, keys):
    v = system.rhs(a)
    pi, qi, ki = (system.index[x] for x in (hold.P, hold.Q, hold.K))
    pk = system.projectors[ki]
    weight = float(system.square[ki]**2)
    q = np.asarray(hold.Q, float)
    b = pk @ (1j*np.dot(q, a[pi])*a[qi])
    db = pk @ (1j*(np.dot(q, v[pi])*a[qi]+np.dot(q, a[pi])*v[qi]))
    z = -weight*np.vdot(a[ki], b)
    dz = -weight*(np.vdot(v[ki], b)+np.vdot(a[ki], db))
    assert abs(z)>1e-30

    group_value = defaultdict(float)
    group_rate = defaultdict(float)
    group_envelope = defaultdict(float)
    for li, ri in zip(system.left, system.right):
        li, ri = int(li), int(ri)
        rwave = system.waves[ri]
        left, right = a[li], a[ri]
        dl, dr = v[li], v[ri]
        dak = -pk @ (1j*np.dot(rwave, left)*right)
        ddak = -pk @ (1j*(np.dot(rwave, dl)*right+np.dot(rwave, left)*dr))
        c = -weight*np.vdot(dak, b)
        dc = -weight*(np.vdot(ddak, b)+np.vdot(dak, db))
        x = c/z
        dx = dc/z-c*dz/(z*z)
        key = (hold.orbit(system.modes[li]), hold.orbit(system.modes[ri]))
        group_value[key] += float(np.imag(x))
        group_rate[key] += float(np.imag(dx))
        group_envelope[key] += float(abs(dx))
    ki_set = set(keys)
    inside = sum(abs(x) for k, x in group_value.items() if k in ki_set)
    outside = sum(abs(x) for k, x in group_value.items() if k not in ki_set)
    ei = sum(x for k, x in group_envelope.items() if k in ki_set)
    eo = sum(x for k, x in group_envelope.items() if k not in ki_set)
    a_l2 = float(np.linalg.norm(a))
    v_l2 = float(np.linalg.norm(v))
    grad_a = float(np.sqrt(np.sum(system.square[:,None]*abs(a)**2)))
    grad_v = float(np.sqrt(np.sum(system.square[:,None]*abs(v)**2)))
    s0_bound = a_l2*grad_a
    s1_bound = v_l2*grad_a+a_l2*grad_v
    b_norm, db_norm = float(np.linalg.norm(b)), float(np.linalg.norm(db))
    full_rate_sobolev_bound = 9*weight/abs(z)*(
        b_norm*s1_bound+(db_norm+b_norm*abs(dz)/abs(z))*s0_bound)
    grouped_rate = sum(
        (1 if x>0 else -1 if x<0 else 0)*group_rate[k] *
        (1 if k in ki_set else -9)
        for k, x in group_value.items()
    )
    return {
        'margin': inside-9*outside,
        'mass_fraction': inside/(inside+outside),
        'ordered_source_rate_envelope_inside': ei,
        'ordered_source_rate_envelope_outside': eo,
        'margin_rate_lower_bound': -ei-9*eo,
        'grouped_margin_rate_away_from_zero_kinks': grouped_rate,
        'instantaneous_margin_over_rate_envelope': (inside-9*outside)/(ei+9*eo),
        'conditional_H1_rate_lower_bound': -float(full_rate_sobolev_bound),
        'instantaneous_margin_over_H1_bound': (inside-9*outside)/full_rate_sobolev_bound,
        'norm_a_L2': a_l2, 'norm_a_H1_seminorm': grad_a,
        'norm_rhs_L2': v_l2, 'norm_rhs_H1_seminorm': grad_v,
        'tracked_z_abs': float(abs(z)),
    }


def main():
    p=argparse.ArgumentParser()
    for name in ('n11-json','n12-json','n13-json','source-json','output'):
        p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args()
    j11,j12,j13,source=[
        json.loads(getattr(args,name.replace('-','_')).read_text())
        for name in ('n11-json','n12-json','n13-json','source-json')]
    hold.System=DealiasedSystem
    keys=hold.frozen_keys(source)
    out={'status':'post-hoc exact instantaneous ordered-source rate envelope',
         'N':{}}
    for N,prev,curr in ((12,hold.get_row(j11,11),hold.get_row(j12,12)),
                        (13,hold.get_row(j12,12),hold.get_row(j13,13))):
        system,states=hold.reconstruct(prev,curr)
        out['N'][str(N)]={}
        for name,a in states.items():
            out['N'][str(N)][name]=audit(system,a,keys)
            print('DONE',N,name,flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__': main()
