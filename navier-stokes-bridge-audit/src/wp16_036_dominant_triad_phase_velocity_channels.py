"""Channel decomposition of dominant-triad phase velocity.

Representative:
    p=(3,2,2), q=(3,-2,1), k=(6,0,3)

For
    z = -|k|^4 <a_k, P_k i(q·a_p)a_q>,
the product rule gives three nonlinear channels:
    dz_p : derivative acting on a_p through q·a_p
    dz_q : derivative acting on a_q
    dz_k : derivative acting on conjugate a_k

The phase-velocity contribution of each channel is
    Im(dz_channel / z).

Evaluated at inherited, target_only, and full_final states for N9/N10/N11.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate


P=(3,2,2)
Q=(3,-2,1)
K=(6,0,3)
TARGET_ORBIT=(0,3,6)


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


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
    for j,(_,_,k) in enumerate(pairs):
        kt=tuple(int(x) for x in k)
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


def channels(system,a):
    pi=system.index[P]
    qi=system.index[Q]
    ki=system.index[K]

    ap=a[pi]; aq=a[qi]; ak=a[ki]
    da=-system.nonlinear(a)
    dap=da[pi]; daq=da[qi]; dak=da[ki]

    qwave=np.asarray(Q,float)
    Pk=system.projectors[ki]
    weight=float(system.square[ki]**2)

    s=np.dot(qwave,ap)
    ds=np.dot(qwave,dap)

    B=Pk@(1j*s*aq)

    z=-weight*np.vdot(ak,B)

    dz_p=-weight*np.vdot(ak,Pk@(1j*ds*aq))
    dz_q=-weight*np.vdot(ak,Pk@(1j*s*daq))
    dz_k=-weight*np.vdot(dak,B)

    dz_sum=dz_p+dz_q+dz_k

    full_phase=float(np.imag(dz_sum/z))
    cp=float(np.imag(dz_p/z))
    cq=float(np.imag(dz_q/z))
    ck=float(np.imag(dz_k/z))

    vals={"p_channel":cp,"q_channel":cq,"k_channel":ck}
    ranked=sorted(vals.items(),key=lambda kv:abs(kv[1]),reverse=True)

    return {
        "alpha":float(np.angle(z)),
        "alpha_dot_nonlinear":full_phase,
        "p_channel_alpha_dot":cp,
        "q_channel_alpha_dot":cq,
        "k_channel_alpha_dot":ck,
        "channel_sum_error":float(full_phase-(cp+cq+ck)),
        "dominant_channel":ranked[0][0],
        "ranked_channels":[{"channel":k,"alpha_dot":v} for k,v in ranked],
        "channel_fraction_of_alpha_dot":{
            "p_channel": cp/full_phase if abs(full_phase)>1e-30 else None,
            "q_channel": cq/full_phase if abs(full_phase)>1e-30 else None,
            "k_channel": ck/full_phase if abs(full_phase)>1e-30 else None,
        },
    }


def analyze(prev,curr):
    system,states=reconstruct(prev,curr)
    return {
        "N":int(curr["N"]),
        "states":{name:channels(system,a) for name,a in states.items()}
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
        "status":"executed dominant-triad phase-velocity channel decomposition",
        "representative":{"p":list(P),"q":list(Q),"k":list(K)},
        "steps":steps,
        "interpretation_rule":(
            "These are instantaneous product-rule contributions to the phase "
            "velocity of one finite triad coefficient under the nonlinear "
            "Galerkin RHS. Channel dominance is not a continuum theorem."
        )
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--prior-json",type=Path,required=True)
    p.add_argument("--current-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    r=run(a.prior_json,a.current_json)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n")

    print("\nDOMINANT TRIAD PHASE-VELOCITY CHANNEL DECOMPOSITION")
    print("="*84)
    for step_name,step in r["steps"].items():
        print("\n",step_name)
        for state_name,s in step["states"].items():
            print(
                state_name,
                "alpha=",s["alpha"],
                "alpha_dot=",s["alpha_dot_nonlinear"],
                "p=",s["p_channel_alpha_dot"],
                "q=",s["q_channel_alpha_dot"],
                "k=",s["k_channel_alpha_dot"],
                "dominant=",s["dominant_channel"],
            )
    print("\nSAVED:",a.output)
