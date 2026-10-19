"""Compress the N=11 inherited-core phase correction by radial shell.

Uses the verified N=10 -> N=11 continuation.  The full old-core wrapped phase
correction is split by shell s = ceil(|k|).  Each shell block is evaluated
alone, then shell blocks are ranked by their endpoint log-C gain and added
cumulatively.

This is a finite diagnostic on the registered N=11 state.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


def wrapped(x):
    return np.angle(np.exp(1j * x))


def build(payload):
    rows={int(r["N"]):r for r in payload["rows"]}
    r10,r11=rows[10],rows[11]
    system=System(N=11,nu=NU)
    base=base_state(system,float(r11["amplitude"]),float(r11["anchor_time"]))
    pairs=active_pairs(system,base)
    support=[list(k) for _,_,k in pairs]
    if support != r11["support_vectors"]:
        raise AssertionError("support mismatch")

    p10={tuple(k):float(phi) for k,phi in zip(r10["support_vectors"],r10["best_phases"])}
    inherited=np.zeros(len(pairs))
    old=np.zeros(len(pairs),dtype=bool)
    shells=np.zeros(len(pairs),dtype=int)

    for j,(_,_,k) in enumerate(pairs):
        shells[j]=int(np.ceil(np.linalg.norm(k)-1e-12))
        if tuple(k) in p10:
            inherited[j]=p10[tuple(k)]
            old[j]=True

    final=np.asarray(r11["best_phases"],float)
    delta=wrapped(final-inherited)
    return system,base,pairs,inherited,delta,old,shells


def qeval(system,base,pairs,phases,grid):
    return evaluate(system,phase_rotate(base,pairs,phases),grid=grid)


def metrics(q,q0):
    return {
        "C":q["C_infinity_stretch"],
        "N_high":q["H2_high_transfer"],
        "P_plus":q["H1_positive_stretching"],
        "C_gain_pct":100*(q["C_infinity_stretch"]/q0["C_infinity_stretch"]-1),
        "N_change_pct":100*(q["H2_high_transfer"]/q0["H2_high_transfer"]-1),
        "P_plus_change_pct":100*(q["H1_positive_stretching"]/q0["H1_positive_stretching"]-1),
        "log_C_gain":float(np.log(q["C_infinity_stretch"]/q0["C_infinity_stretch"])),
    }


def run(path,grid,eps):
    payload=json.loads(path.read_text())
    system,base,pairs,inh,delta,old,shells=build(payload)
    q0=qeval(system,base,pairs,inh,grid)

    shell_rows=[]
    for s in sorted(set(shells[old])):
        mask=old & (shells==s)
        ph=inh + delta*mask
        q=qeval(system,base,pairs,ph,grid)

        ph_eps=inh + eps*delta*mask
        qe=qeval(system,base,pairs,ph_eps,grid)

        shell_rows.append({
            "shell":int(s),
            "pair_count":int(mask.sum()),
            "mean_abs_delta":float(np.mean(abs(delta[mask]))),
            "endpoint":metrics(q,q0),
            "directional_per_unit_lambda":{
                "dlogC":float(np.log(qe["C_infinity_stretch"]/q0["C_infinity_stretch"])/eps),
                "dlogN":float(np.log(qe["H2_high_transfer"]/q0["H2_high_transfer"])/eps),
                "dlogPplus":float(np.log(qe["H1_positive_stretching"]/q0["H1_positive_stretching"])/eps),
            }
        })

    ranked=sorted(shell_rows,key=lambda x:x["endpoint"]["log_C_gain"],reverse=True)
    cumulative=[]
    mask=np.zeros(len(pairs),dtype=bool)
    for rank,row in enumerate(ranked,1):
        mask |= old & (shells==row["shell"])
        q=qeval(system,base,pairs,inh+delta*mask,grid)
        cumulative.append({
            "rank":rank,
            "added_shell":row["shell"],
            "included_shells":[x["shell"] for x in ranked[:rank]],
            "pair_count":int(mask.sum()),
            **metrics(q,q0)
        })

    q_old=qeval(system,base,pairs,inh+delta*old,grid)

    return {
        "status":"executed N11 old-core shell-compression audit",
        "source":str(path),
        "grid":grid,
        "epsilon":eps,
        "old_core_pair_count":int(old.sum()),
        "inherited":metrics(q0,q0),
        "full_old_core":metrics(q_old,q0),
        "shell_blocks":shell_rows,
        "ranked_cumulative":cumulative,
        "interpretation_rule":"Finite shell decomposition of the registered N11 old-core correction only; not a general variational theorem."
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("continuation_json",type=Path)
    p.add_argument("--grid",type=int,default=48)
    p.add_argument("--epsilon",type=float,default=0.1)
    p.add_argument("--output",type=Path,default=Path("/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/wp16_old_core_shell_compression_results.json"))
    a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    result=run(a.continuation_json,a.grid,a.epsilon)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
