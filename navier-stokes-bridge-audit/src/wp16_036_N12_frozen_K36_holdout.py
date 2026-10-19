"""Prospective N12 holdout for frozen N11 k-channel K=36 coalition.

Inputs:
- N10/N11 continuation JSON
- newly generated N12 continuation JSON
- prior q/k RHS source JSON containing the frozen N11 target-only ranking

The exact first 36 ordered source-orbit keys from the N11 target-only
k-channel are frozen before inspecting N12.

Evaluate at N12:
  inherited
  target_only [036]
  full_final

Prospective consistency criteria:
  same sign as full k-channel
  absolute mass fraction >= 0.90
  signed share in [0.80, 1.20]

Finite holdout diagnostic only.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate


P=(3,2,2)
Q=(3,-2,1)
K=(6,0,3)
TARGET_ORBIT=(0,3,6)
PREFIX=36


def orbit(v):
    return tuple(sorted(abs(int(x)) for x in v))


def get_row(payload,N):
    rows={int(r["N"]):r for r in payload["rows"]}
    if N not in rows:
        raise KeyError(f"missing N={N}")
    return rows[N]


def reconstruct(prev,curr):
    N=int(curr["N"])
    system=System(N=N,nu=NU)
    base=base_state(system,float(curr["amplitude"]),float(curr["anchor_time"]))
    pairs=active_pairs(system,base)

    if [list(k) for _,_,k in pairs] != curr["support_vectors"]:
        raise AssertionError("support mismatch")

    prev_map={
        tuple(k):float(phi)
        for k,phi in zip(prev["support_vectors"],prev["best_phases"])
    }

    inherited=np.zeros(len(pairs),float)
    mask=np.zeros(len(pairs),bool)

    for j,(_,_,kk) in enumerate(pairs):
        kt=tuple(int(x) for x in kk)
        if kt in prev_map:
            inherited[j]=prev_map[kt]
            if orbit(kt)==TARGET_ORBIT:
                mask[j]=True

    final=np.asarray(curr["best_phases"],float)
    delta=np.angle(np.exp(1j*(final-inherited)))
    target_only=inherited+delta*mask

    return system,{
        "inherited":phase_rotate(base,pairs,inherited),
        "target_only":phase_rotate(base,pairs,target_only),
        "full_final":phase_rotate(base,pairs,final),
    }


def source_terms_for_output(system,a,out_index):
    rows=[]
    mask=np.nonzero(system.out==out_index)[0]
    Pout=system.projectors[out_index]
    for idx in mask:
        li=int(system.left[idx]); ri=int(system.right[idx])
        qdot=np.dot(system.waves[ri],a[li])
        raw=1j*qdot*a[ri]
        da_term=-(Pout@raw)
        rows.append((li,ri,da_term))
    return rows


def k_channel_grouped(system,a):
    pi=system.index[P]
    qi=system.index[Q]
    ki=system.index[K]

    ap=a[pi]; aq=a[qi]; ak=a[ki]
    qwave=np.asarray(Q,float)
    Pk=system.projectors[ki]
    weight=float(system.square[ki]**2)

    s=np.dot(qwave,ap)
    B=Pk@(1j*s*aq)
    z=-weight*np.vdot(ak,B)
    if abs(z)<1e-30:
        raise AssertionError("tracked z vanished")

    groups=defaultdict(float)

    for li,ri,dak_term in source_terms_for_output(system,a,ki):
        dz=-weight*np.vdot(dak_term,B)
        adot=float(np.imag(dz/z))
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]+=adot

    total_signed=sum(groups.values())
    total_abs=sum(abs(v) for v in groups.values())
    return groups,float(total_signed),float(total_abs)


def frozen_keys(source_payload):
    rows=source_payload["steps"]["N11_from_N10"]["states"]["target_only"]["k_grouped_by_ordered_orbit_pair"]
    rows=sorted(rows,key=lambda r:abs(float(r["alpha_dot_contribution"])),reverse=True)
    return [
        (tuple(r["left_orbit"]),tuple(r["right_orbit"]))
        for r in rows[:PREFIX]
    ]


def evaluate_state(system,a,keys):
    groups,total_signed,total_abs=k_channel_grouped(system,a)
    vals=[groups.get(x,0.0) for x in keys]
    signed=sum(vals)
    abs_mass=sum(abs(v) for v in vals)

    signed_share=signed/total_signed if abs(total_signed)>1e-30 else None
    abs_fraction=abs_mass/total_abs if total_abs>0 else None
    same_sign=(
        signed*total_signed>0
        if abs(signed)>1e-30 and abs(total_signed)>1e-30
        else None
    )

    passes=(
        same_sign is True
        and abs_fraction is not None and abs_fraction>=0.90
        and signed_share is not None and 0.80<=signed_share<=1.20
    )

    return {
        "k_channel_total_signed":total_signed,
        "k_channel_total_abs_group_contribution":total_abs,
        "frozen_K36_signed_contribution":signed,
        "signed_share_of_channel_total":signed_share,
        "absolute_mass_captured":abs_mass,
        "absolute_mass_fraction":abs_fraction,
        "same_sign_as_channel_total":same_sign,
        "passes_preregistered_consistency_criteria":passes,
        "present_key_count":sum(1 for x in keys if x in groups),
    }


def run(current_path,n12_path,source_path):
    current=json.loads(current_path.read_text(encoding="utf-8"))
    n12=json.loads(n12_path.read_text(encoding="utf-8"))
    source=json.loads(source_path.read_text(encoding="utf-8"))

    r11=get_row(current,11)
    r12=get_row(n12,12)
    system,states=reconstruct(r11,r12)
    keys=frozen_keys(source)

    out_states={
        name:evaluate_state(system,a,keys)
        for name,a in states.items()
    }

    return {
        "status":"executed prospective N12 frozen K36 k-channel holdout",
        "reference":"N11_from_N10 target_only k-channel first 36 absolute-ranked source-orbit groups",
        "N":12,
        "frozen_prefix_size":PREFIX,
        "criteria":{
            "same_sign":True,
            "minimum_absolute_mass_fraction":0.90,
            "signed_share_interval":[0.80,1.20],
        },
        "states":out_states,
        "all_three_states_pass":all(
            s["passes_preregistered_consistency_criteria"]
            for s in out_states.values()
        ),
        "interpretation_rule":(
            "This is one new finite-cutoff holdout of a source set frozen from "
            "N11. Passing does not establish all-N persistence or continuum "
            "phase dynamics; failure is retained without retuning K36."
        ),
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--current-json",type=Path,required=True)
    p.add_argument("--n12-json",type=Path,required=True)
    p.add_argument("--source-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    r=run(a.current_json,a.n12_json,a.source_json)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")

    print("\nN12 FROZEN K36 HOLDOUT")
    print("="*72)
    for name,s in r["states"].items():
        print(
            name,
            "signed_share=",s["signed_share_of_channel_total"],
            "abs_fraction=",s["absolute_mass_fraction"],
            "same_sign=",s["same_sign_as_channel_total"],
            "PASS=",s["passes_preregistered_consistency_criteria"],
        )
    print("\nALL THREE PASS:",r["all_three_states_pass"])
    print("SAVED:",a.output)
