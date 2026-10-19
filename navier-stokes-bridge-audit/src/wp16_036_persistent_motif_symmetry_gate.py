"""Exact symmetry decomposition of persistent [223]+[123]->[036] motif."""

import argparse, itertools, json
from pathlib import Path
from collections import defaultdict
import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs

TARGET=(0,3,6); LEFT=(2,2,3); RIGHT=(1,2,3)

def orbit(k): return tuple(sorted(abs(int(x)) for x in k))
def wrapped(x): return np.angle(np.exp(1j*x))

def get_row(payload,N): return {int(r["N"]):r for r in payload["rows"]}[N]

def signed_phases(system,pairs,pair_phases):
    psi=np.zeros(len(system.modes))
    for (i,j,_),phi in zip(pairs,pair_phases):
        psi[i]=phi; psi[j]=-phi
    return psi

def canon(p,q,k):
    reps=[]
    perms=list(itertools.permutations(range(3)))
    signs=list(itertools.product((-1,1),repeat=3))
    p=np.array(p,int); q=np.array(q,int); k=np.array(k,int)
    for perm in perms:
        for s in signs:
            s=np.array(s,int)
            P=tuple((p[list(perm)]*s).tolist())
            Q=tuple((q[list(perm)]*s).tolist())
            K=tuple((k[list(perm)]*s).tolist())
            reps.append(P+Q+K)
    return min(reps)

def reconstruct(prev,curr):
    N=int(curr["N"]); system=System(N=N,nu=NU)
    base=base_state(system,float(curr["amplitude"]),float(curr["anchor_time"]))
    pairs=active_pairs(system,base)
    prevmap={tuple(k):float(phi) for k,phi in zip(prev["support_vectors"],prev["best_phases"])}
    inh=np.zeros(len(pairs)); target_idx=[]
    for j,(_,_,k) in enumerate(pairs):
        kt=tuple(int(x) for x in k)
        if kt in prevmap: inh[j]=prevmap[kt]
        if kt in prevmap and orbit(kt)==TARGET: target_idx.append(j)
    final=np.asarray(curr["best_phases"],float)
    delta=wrapped(final-inh)
    mask=np.zeros(len(pairs),bool); mask[target_idx]=True
    ph1=inh+delta*mask
    return system,base,pairs,inh,ph1

def run_step(prev,curr):
    system,base,pairs,ph0,ph1=reconstruct(prev,curr)
    psi0=signed_phases(system,pairs,ph0); psi1=signed_phases(system,pairs,ph1)
    w=system.square.astype(float)**2
    groups=defaultdict(lambda:{"count":0,"A":0.0,"N_before":0.0,"N_after":0.0,"rows":[]})
    total={"count":0,"A":0.0,"N_before":0.0,"N_after":0.0}
    for oi,li,ri in zip(system.out,system.left,system.right):
        if system.square[li] <= 4: continue
        if orbit(system.modes[oi])!=TARGET: continue
        if orbit(system.modes[li])!=LEFT or orbit(system.modes[ri])!=RIGHT: continue
        p=system.modes[li]; q=system.modes[ri]; k=system.modes[oi]
        qdot=np.dot(system.waves[ri],base[li])
        raw=1j*qdot*base[ri]
        proj=system.projectors[oi]@raw
        z0=-w[oi]*np.vdot(base[oi],proj)
        t0=float(psi0[li]+psi0[ri]-psi0[oi]); t1=float(psi1[li]+psi1[ri]-psi1[oi])
        nb=float(np.real(z0*np.exp(1j*t0))); na=float(np.real(z0*np.exp(1j*t1)))
        A=float(abs(z0))
        key=canon(p,q,k); g=groups[key]
        g["count"]+=1; g["A"]+=A; g["N_before"]+=nb; g["N_after"]+=na
        g["rows"].append({"p":list(map(int,p)),"q":list(map(int,q)),"k":list(map(int,k)),
                          "A":A,"N_before":nb,"N_after":na,
                          "theta_before":t0,"theta_after":t1})
        total["count"]+=1; total["A"]+=A; total["N_before"]+=nb; total["N_after"]+=na
    out=[]
    for key,g in groups.items():
        g["delta_N"]=g["N_after"]-g["N_before"]
        g["chi_before"]=g["N_before"]/g["A"] if g["A"] else 0.0
        g["chi_after"]=g["N_after"]/g["A"] if g["A"] else 0.0
        g["canonical_flat"]=list(key)
        out.append(g)
    out.sort(key=lambda x:abs(x["delta_N"]),reverse=True)
    total["delta_N"]=total["N_after"]-total["N_before"]
    total["chi_before"]=total["N_before"]/total["A"] if total["A"] else 0.0
    total["chi_after"]=total["N_after"]/total["A"] if total["A"] else 0.0
    return {"N":int(curr["N"]),"exact_triad_count":total["count"],
            "symmetry_class_count":len(out),"total":total,"classes":out}

def run(prior_path,current_path):
    prior=json.loads(prior_path.read_text()); cur=json.loads(current_path.read_text())
    r8=get_row(prior,8); r9=get_row(prior,9); r10=get_row(cur,10); r11=get_row(cur,11)
    return {"status":"executed exact symmetry decomposition of persistent [223]+[123]->[036] motif",
            "steps":{"N9_from_N8":run_step(r8,r9),
                     "N10_from_N9":run_step(r9,r10),
                     "N11_from_N10":run_step(r10,r11)},
            "interpretation_rule":"Finite exact-triad symmetry decomposition only."}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--prior-json",type=Path,required=True)
    p.add_argument("--current-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(); r=run(a.prior_json,a.current_json)
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(r,indent=2)+"\n")
    for name,s in r["steps"].items():
        print("\n",name,"triads=",s["exact_triad_count"],"classes=",s["symmetry_class_count"])
        print("total",s["total"])
        for i,c in enumerate(s["classes"][:10],1):
            print(i,"count=",c["count"],"deltaN=",c["delta_N"],"chi",c["chi_before"],"->",c["chi_after"],"canon=",c["canonical_flat"])
    print("\nSAVED",a.output)
