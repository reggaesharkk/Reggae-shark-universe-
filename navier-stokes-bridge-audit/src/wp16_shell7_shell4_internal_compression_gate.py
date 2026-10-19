"""Internal compression audit for dominant old-core shells 7 and 4.

Taxonomies:
  * abs_orbit: sorted absolute coordinate triple
  * parity: coordinate-wise |k_i| mod 2
  * sign_pattern: signs of coordinates (-1,0,+1)

For each taxonomy, evaluate each class restricted to shells 7 and 4, then rank
classes by endpoint log-C gain and add cumulatively. Finite N=11 diagnostic.
"""

import argparse, json
from pathlib import Path
import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


def wrapped(x):
    return np.angle(np.exp(1j*x))


def build(payload):
    rows={int(r["N"]):r for r in payload["rows"]}
    r10,r11=rows[10],rows[11]
    system=System(N=11,nu=NU)
    base=base_state(system,float(r11["amplitude"]),float(r11["anchor_time"]))
    pairs=active_pairs(system,base)
    if [list(k) for _,_,k in pairs] != r11["support_vectors"]:
        raise AssertionError("support mismatch")

    p10={tuple(k):float(phi) for k,phi in zip(r10["support_vectors"],r10["best_phases"])}
    inherited=np.zeros(len(pairs))
    old=np.zeros(len(pairs),dtype=bool)
    shells=np.zeros(len(pairs),dtype=int)
    ks=[]

    for j,(_,_,k) in enumerate(pairs):
        ks.append(tuple(int(x) for x in k))
        shells[j]=int(np.ceil(np.linalg.norm(k)-1e-12))
        if tuple(k) in p10:
            inherited[j]=p10[tuple(k)]
            old[j]=True

    final=np.asarray(r11["best_phases"],float)
    delta=wrapped(final-inherited)
    target=old & np.isin(shells,[7,4])
    return system,base,pairs,inherited,delta,target,ks,shells


def key_for(k,tax):
    if tax=="abs_orbit":
        return tuple(sorted(abs(x) for x in k))
    if tax=="parity":
        return tuple(abs(x)%2 for x in k)
    if tax=="sign_pattern":
        return tuple(0 if x==0 else (1 if x>0 else -1) for x in k)
    raise ValueError(tax)


def qeval(system,base,pairs,ph,grid):
    return evaluate(system,phase_rotate(base,pairs,ph),grid=grid)


def metrics(q,q0):
    return {
      "C":q["C_infinity_stretch"],
      "N_high":q["H2_high_transfer"],
      "P_plus":q["H1_positive_stretching"],
      "C_gain_pct":100*(q["C_infinity_stretch"]/q0["C_infinity_stretch"]-1),
      "N_change_pct":100*(q["H2_high_transfer"]/q0["H2_high_transfer"]-1),
      "P_plus_change_pct":100*(q["H1_positive_stretching"]/q0["H1_positive_stretching"]-1),
      "log_C_gain":float(np.log(q["C_infinity_stretch"]/q0["C_infinity_stretch"]))
    }


def audit_taxonomy(tax,system,base,pairs,inh,delta,target,ks,grid):
    groups={}
    for i,k in enumerate(ks):
        if target[i]:
            groups.setdefault(key_for(k,tax),[]).append(i)

    q0=qeval(system,base,pairs,inh,grid)
    rows=[]
    for key,inds in groups.items():
        mask=np.zeros(len(pairs),dtype=bool); mask[inds]=True
        q=qeval(system,base,pairs,inh+delta*mask,grid)
        rows.append({
          "class":list(key),
          "pair_count":len(inds),
          "mean_abs_delta":float(np.mean(np.abs(delta[inds]))),
          **metrics(q,q0)
        })

    ranked=sorted(rows,key=lambda r:r["log_C_gain"],reverse=True)
    cumulative=[]
    mask=np.zeros(len(pairs),dtype=bool)
    for rank,row in enumerate(ranked,1):
        key=tuple(row["class"])
        for i,k in enumerate(ks):
            if target[i] and key_for(k,tax)==key:
                mask[i]=True
        q=qeval(system,base,pairs,inh+delta*mask,grid)
        cumulative.append({
          "rank":rank,
          "added_class":row["class"],
          "pair_count":int(mask.sum()),
          **metrics(q,q0)
        })
    return {"classes":rows,"ranked_cumulative":cumulative}


def run(path,grid):
    payload=json.loads(path.read_text())
    system,base,pairs,inh,delta,target,ks,shells=build(payload)
    q0=qeval(system,base,pairs,inh,grid)
    qall=qeval(system,base,pairs,inh+delta*target,grid)
    return {
      "status":"executed shell7-shell4 internal compression audit",
      "source":str(path),
      "grid":grid,
      "target_pair_count":int(target.sum()),
      "target_shells":[7,4],
      "baseline":metrics(q0,q0),
      "full_target":metrics(qall,q0),
      "taxonomies":{
        tax:audit_taxonomy(tax,system,base,pairs,inh,delta,target,ks,grid)
        for tax in ["abs_orbit","parity","sign_pattern"]
      },
      "interpretation_rule":"Finite structured-class compression audit on shells 7 and 4 only."
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("continuation_json",type=Path)
    p.add_argument("--grid",type=int,default=48)
    p.add_argument("--output",type=Path,default=Path("/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/wp16_shell7_shell4_internal_compression_results.json"))
    a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    r=run(a.continuation_json,a.grid)
    a.output.write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps(r,indent=2))
