"""Decompose q- and k-channel phase velocity into exact nonlinear RHS sources.

Dominant tracked triad:
    p=(3,2,2), q=(3,-2,1), k=(6,0,3)

For the q-channel and k-channel in dz, decompose da_q and da_k into the
ordered Fourier convolution pairs that generate those mode derivatives.

Each exact source contribution is propagated through dz/z to obtain its
instantaneous alpha_dot contribution.

Results are grouped by ordered absolute-coordinate orbit pair and also ranked
at exact source-triad level.

Finite instantaneous diagnostic only.
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


def orbit(v):
    return tuple(sorted(abs(int(x)) for x in v))


def get_row(payload,N):
    return {int(r["N"]):r for r in payload["rows"]}[N]


def reconstruct(prev,curr):
    N=int(curr["N"])
    system=System(N=N,nu=NU)
    base=base_state(system,float(curr["amplitude"]),float(curr["anchor_time"]))
    pairs=active_pairs(system,base)

    prev_map={tuple(k):float(phi) for k,phi in zip(prev["support_vectors"],prev["best_phases"])}
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
    """Return exact ordered nonlinear RHS contributions to one output mode."""
    rows=[]
    mask=np.nonzero(system.out==out_index)[0]
    Pout=system.projectors[out_index]

    for idx in mask:
        li=int(system.left[idx]); ri=int(system.right[idx])
        qdot=np.dot(system.waves[ri],a[li])
        raw=1j*qdot*a[ri]
        # nonlinear RHS contribution is minus projected nonlinear term
        da_term=-(Pout@raw)
        rows.append((li,ri,da_term))
    return rows


def decompose_state(system,a):
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

    exact_rows=[]

    # q-channel source decomposition
    for li,ri,daq_term in source_terms_for_output(system,a,qi):
        dz=-weight*np.vdot(ak,Pk@(1j*s*daq_term))
        adot=float(np.imag(dz/z))
        exact_rows.append({
            "channel":"q_channel",
            "left_mode":[int(x) for x in system.modes[li]],
            "right_mode":[int(x) for x in system.modes[ri]],
            "output_mode":list(Q),
            "left_orbit":list(orbit(system.modes[li])),
            "right_orbit":list(orbit(system.modes[ri])),
            "alpha_dot_contribution":adot,
            "dz_abs":float(abs(dz)),
        })

    # k-channel source decomposition
    for li,ri,dak_term in source_terms_for_output(system,a,ki):
        dz=-weight*np.vdot(dak_term,B)
        adot=float(np.imag(dz/z))
        exact_rows.append({
            "channel":"k_channel",
            "left_mode":[int(x) for x in system.modes[li]],
            "right_mode":[int(x) for x in system.modes[ri]],
            "output_mode":list(K),
            "left_orbit":list(orbit(system.modes[li])),
            "right_orbit":list(orbit(system.modes[ri])),
            "alpha_dot_contribution":adot,
            "dz_abs":float(abs(dz)),
        })

    # Direct channel totals from source sums.
    q_total=sum(r["alpha_dot_contribution"] for r in exact_rows if r["channel"]=="q_channel")
    k_total=sum(r["alpha_dot_contribution"] for r in exact_rows if r["channel"]=="k_channel")

    # Group by ordered source-orbit pair within each derivative channel.
    grouped=defaultdict(lambda:{
        "count":0,
        "alpha_dot_contribution":0.0,
        "sum_abs_alpha_dot_contribution":0.0,
        "sum_dz_abs":0.0,
    })

    for r in exact_rows:
        key=(
            r["channel"],
            tuple(r["left_orbit"]),
            tuple(r["right_orbit"]),
        )
        g=grouped[key]
        g["count"]+=1
        g["alpha_dot_contribution"]+=r["alpha_dot_contribution"]
        g["sum_abs_alpha_dot_contribution"]+=abs(r["alpha_dot_contribution"])
        g["sum_dz_abs"]+=r["dz_abs"]

    group_rows=[]
    for (channel,left_o,right_o),g in grouped.items():
        row=dict(g)
        row.update({
            "channel":channel,
            "left_orbit":list(left_o),
            "right_orbit":list(right_o),
        })
        group_rows.append(row)

    q_groups=sorted(
        [r for r in group_rows if r["channel"]=="q_channel"],
        key=lambda r:abs(r["alpha_dot_contribution"]),
        reverse=True,
    )
    k_groups=sorted(
        [r for r in group_rows if r["channel"]=="k_channel"],
        key=lambda r:abs(r["alpha_dot_contribution"]),
        reverse=True,
    )

    q_exact=sorted(
        [r for r in exact_rows if r["channel"]=="q_channel"],
        key=lambda r:abs(r["alpha_dot_contribution"]),
        reverse=True,
    )
    k_exact=sorted(
        [r for r in exact_rows if r["channel"]=="k_channel"],
        key=lambda r:abs(r["alpha_dot_contribution"]),
        reverse=True,
    )

    return {
        "alpha":float(np.angle(z)),
        "q_channel_total_alpha_dot":float(q_total),
        "k_channel_total_alpha_dot":float(k_total),
        "q_channel_source_count":len(q_exact),
        "k_channel_source_count":len(k_exact),
        "q_grouped_by_ordered_orbit_pair":q_groups,
        "k_grouped_by_ordered_orbit_pair":k_groups,
        "q_exact_sources_ranked":q_exact,
        "k_exact_sources_ranked":k_exact,
    }


def analyze(prev,curr):
    system,states=reconstruct(prev,curr)
    return {
        "N":int(curr["N"]),
        "states":{name:decompose_state(system,a) for name,a in states.items()}
    }


def run(prior_path,current_path):
    prior=json.loads(prior_path.read_text())
    current=json.loads(current_path.read_text())
    r8=get_row(prior,8); r9=get_row(prior,9)
    r10=get_row(current,10); r11=get_row(current,11)

    steps={
        "N9_from_N8":analyze(r8,r9),
        "N10_from_N9":analyze(r9,r10),
        "N11_from_N10":analyze(r10,r11),
    }

    return {
        "status":"executed q/k nonlinear RHS source decomposition for dominant triad phase velocity",
        "tracked_triad":{"p":list(P),"q":list(Q),"k":list(K)},
        "steps":steps,
        "interpretation_rule":(
            "Each source is an exact ordered convolution contribution to da_q "
            "or da_k under the finite nonlinear Galerkin RHS, propagated into "
            "instantaneous alpha_dot. Source dominance is finite and state-specific."
        )
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--prior-json",type=Path,required=True)
    p.add_argument("--current-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--top-k",type=int,default=12)
    a=p.parse_args()

    r=run(a.prior_json,a.current_json)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n")

    print("\nQ/K NONLINEAR RHS SOURCE DECOMPOSITION")
    print("="*88)
    for step_name,step in r["steps"].items():
        print("\n",step_name)
        for state_name,s in step["states"].items():
            print("\n ",state_name,"alpha=",s["alpha"])
            print("  q total=",s["q_channel_total_alpha_dot"])
            for row in s["q_grouped_by_ordered_orbit_pair"][:a.top_k]:
                print("   Q",row["left_orbit"],"+",row["right_orbit"],
                      "count=",row["count"],"alpha_dot=",row["alpha_dot_contribution"])
            print("  k total=",s["k_channel_total_alpha_dot"])
            for row in s["k_grouped_by_ordered_orbit_pair"][:a.top_k]:
                print("   K",row["left_orbit"],"+",row["right_orbit"],
                      "count=",row["count"],"alpha_dot=",row["alpha_dot_contribution"])

    print("\nSAVED:",a.output)
