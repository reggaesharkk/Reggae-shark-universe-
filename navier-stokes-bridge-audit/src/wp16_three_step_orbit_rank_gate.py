"""Three-step cross-cutoff orbit persistence / independent-response rank audit.

Uses:
  N8 -> N9   from prior escalation JSON
  N9 -> N10  bridging prior to current JSON
  N10 -> N11 from current JSON

Orbit = sort(|k1|,|k2|,|k3|).

For each shared orbit, estimate independent directional responses
  dlogN, -dlogPplus
at epsilon=0.1 for each step.

The response matrix therefore has 6 independent coordinates:
  [N9 dlogN, N9 -dlogP,
   N10 dlogN, N10 -dlogP,
   N11 dlogN, N11 -dlogP]

dlogC is reported but excluded from SVD because
  dlogC = dlogN + (-dlogPplus)
exactly at fixed phase-invariant factors.
"""

import argparse, json
from pathlib import Path
from collections import defaultdict
import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate

DOMINANT = [(0,3,6),(0,2,3),(1,4,5),(0,1,3),(0,1,6),(1,1,3)]

def wrapped(x): return np.angle(np.exp(1j*x))
def orbit_key(k): return tuple(sorted(abs(int(x)) for x in k))

def get_row(payload,N):
    rows={int(r["N"]):r for r in payload["rows"]}
    return rows[N]

def reconstruct(prev,curr):
    N=int(curr["N"])
    system=System(N=N,nu=NU)
    base=base_state(system,float(curr["amplitude"]),float(curr["anchor_time"]))
    pairs=active_pairs(system,base)
    if [list(k) for _,_,k in pairs] != curr["support_vectors"]:
        raise AssertionError(f"N={N} support mismatch")
    pm={tuple(k):float(phi) for k,phi in zip(prev["support_vectors"],prev["best_phases"])}
    inh=np.zeros(len(pairs)); old=np.zeros(len(pairs),bool); keys=[]
    for j,(_,_,k) in enumerate(pairs):
        kt=tuple(int(x) for x in k); keys.append(orbit_key(kt))
        if kt in pm:
            inh[j]=pm[kt]; old[j]=True
    final=np.asarray(curr["best_phases"],float)
    delta=wrapped(final-inh)
    if int(old.sum()) != int(curr["inherited_pairs"]):
        raise AssertionError(f"N={N} inherited mismatch")
    return system,base,pairs,inh,delta,old,keys

def qeval(system,base,pairs,ph,grid):
    return evaluate(system,phase_rotate(base,pairs,ph),grid=grid)

def responses(prev,curr,grid,eps):
    system,base,pairs,inh,delta,old,keys=reconstruct(prev,curr)
    q0=qeval(system,base,pairs,inh,grid)
    groups=defaultdict(list)
    for i,k in enumerate(keys):
        if old[i]: groups[k].append(i)
    out={}
    for key,inds in groups.items():
        mask=np.zeros(len(pairs),bool); mask[inds]=True
        qe=qeval(system,base,pairs,inh+eps*delta*mask,grid)
        dN=float(np.log(qe["H2_high_transfer"]/q0["H2_high_transfer"])/eps)
        dP=float(-np.log(qe["H1_positive_stretching"]/q0["H1_positive_stretching"])/eps)
        out[key]={
            "pair_count":len(inds),
            "dlogN":dN,
            "minus_dlogPplus":dP,
            "dlogC":dN+dP,
        }
    qfull=qeval(system,base,pairs,inh+delta*old,grid)
    full={
      "C_gain_pct":100*(qfull["C_infinity_stretch"]/q0["C_infinity_stretch"]-1),
      "N_change_pct":100*(qfull["H2_high_transfer"]/q0["H2_high_transfer"]-1),
      "P_plus_change_pct":100*(qfull["H1_positive_stretching"]/q0["H1_positive_stretching"]-1),
      "old_core_pair_count":int(old.sum())
    }
    return out,full

def svd_summary(M):
    s=np.linalg.svd(M,full_matrices=False,compute_uv=False)
    e=s*s; frac=e/e.sum(); cum=np.cumsum(frac)
    return {
      "shape":list(M.shape),
      "singular_values":[float(x) for x in s],
      "energy_fraction":[float(x) for x in frac],
      "cumulative_energy_fraction":[float(x) for x in cum],
      "effective_rank_95pct":int(np.searchsorted(cum,0.95)+1),
      "effective_rank_99pct":int(np.searchsorted(cum,0.99)+1),
    }

def run(prior_path,current_path,grid,eps):
    prior=json.loads(prior_path.read_text())
    current=json.loads(current_path.read_text())
    r8=get_row(prior,8); r9=get_row(prior,9)
    r10=get_row(current,10); r11=get_row(current,11)

    a9,f9=responses(r8,r9,grid,eps)
    a10,f10=responses(r9,r10,grid,eps)
    a11,f11=responses(r10,r11,grid,eps)

    shared=sorted(set(a9)&set(a10)&set(a11))
    rows=[]; M=[]
    for key in shared:
        v=[a9[key]["dlogN"],a9[key]["minus_dlogPplus"],
           a10[key]["dlogN"],a10[key]["minus_dlogPplus"],
           a11[key]["dlogN"],a11[key]["minus_dlogPplus"]]
        M.append(v)
        rows.append({
          "orbit":list(key),
          "N9":a9[key],
          "N10":a10[key],
          "N11":a11[key],
          "dlogC_positive_all_three":bool(a9[key]["dlogC"]>0 and a10[key]["dlogC"]>0 and a11[key]["dlogC"]>0),
        })
    M=np.asarray(M,float)
    scale=np.std(M,axis=0); scale[scale==0]=1.0
    dom=[]
    for key in DOMINANT:
        dom.append({
          "orbit":list(key),
          "present_all_three":key in a9 and key in a10 and key in a11,
          "N9":a9.get(key),
          "N10":a10.get(key),
          "N11":a11.get(key),
          "positive_dlogC_all_three":(
              a9.get(key,{}).get("dlogC",0)>0 and
              a10.get(key,{}).get("dlogC",0)>0 and
              a11.get(key,{}).get("dlogC",0)>0
          ) if key in a9 and key in a10 and key in a11 else None
        })
    pers=[]
    for row in rows:
        vals=[max(0,row[x]["dlogC"]) for x in ["N9","N10","N11"]]
        score=float((vals[0]*vals[1]*vals[2])**(1/3)) if all(v>0 for v in vals) else 0.0
        pers.append({"orbit":row["orbit"],"score":score,
                     "N9_dlogC":row["N9"]["dlogC"],
                     "N10_dlogC":row["N10"]["dlogC"],
                     "N11_dlogC":row["N11"]["dlogC"]})
    pers.sort(key=lambda x:x["score"],reverse=True)
    return {
      "status":"executed three-step orbit persistence / independent-response rank audit",
      "grid":grid,"epsilon":eps,
      "full_old_core_steps":{"N9_from_N8":f9,"N10_from_N9":f10,"N11_from_N10":f11},
      "shared_orbit_count":len(shared),
      "dominant_orbits":dom,
      "persistent_positive_ranking":pers,
      "independent_response_svd_raw":svd_summary(M),
      "independent_response_svd_standardized":svd_summary(M/scale),
      "shared_orbit_rows":rows,
      "interpretation_rule":"Finite three-step diagnostic only; persistence does not establish an all-N orbit law."
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--prior-json",type=Path,required=True)
    p.add_argument("--current-json",type=Path,required=True)
    p.add_argument("--grid",type=int,default=48)
    p.add_argument("--epsilon",type=float,default=0.1)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    r=run(a.prior_json,a.current_json,a.grid,a.epsilon)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n")
    print("shared orbits:",r["shared_orbit_count"])
    print("\nDOMINANT")
    for x in r["dominant_orbits"]: print(x)
    print("\nTOP PERSISTENT")
    for x in r["persistent_positive_ranking"][:20]: print(x)
    print("\nRAW",json.dumps(r["independent_response_svd_raw"],indent=2))
    print("\nSTANDARDIZED",json.dumps(r["independent_response_svd_standardized"],indent=2))
    print("\nFULL STEPS",json.dumps(r["full_old_core_steps"],indent=2))
    print("\nSAVED",a.output)
