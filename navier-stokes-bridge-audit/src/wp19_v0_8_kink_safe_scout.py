#!/usr/bin/env python3
"""WP19 v0.8 floating endpoint scout for the kink-safe quadratic envelope."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
def orbit(k): return tuple(sorted(abs(int(x)) for x in k))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--lower-N",type=int,required=True)
    p.add_argument("--lower-nodes",type=Path,required=True)
    p.add_argument("--higher-nodes",type=Path,required=True)
    p.add_argument("--k36",type=Path,required=True)
    p.add_argument("--c500",type=Path,required=True)
    a=p.parse_args()
    sys.path.insert(0,str(a.repo/"src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    k36={(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
         for r in json.loads(a.k36.read_text())["keys"]}
    cobj=json.loads(a.c500.read_text())
    tau={(tuple(r["left_orbit"]),tuple(r["right_orbit"])):
         int(r["fixed_linear_sign"]) for r in cobj["keys"]}

    def proj(v):
        k=np.asarray(K,float)
        return v-k*np.dot(k,v)/np.dot(k,k)

    def values(system,field):
        pidx,qidx,kidx=(system.index[x] for x in (P,Q,K))
        b=proj(1j*np.dot(Q,field[pidx])*field[qidx])
        W=system.square[kidx]**2
        z=-W*np.vdot(field[kidx],b)
        groups={}
        for li,ri in zip(system.left,system.right):
            d=-proj(1j*np.dot(system.waves[ri],field[li])*field[ri])
            key=(orbit(system.modes[li]),orbit(system.modes[ri]))
            groups[key]=groups.get(key,0j)-W*np.vdot(d,b)
        return {key:float((w/z).imag) for key,w in groups.items()}

    low=DealiasedSystem(a.lower_N)
    high=DealiasedSystem(a.lower_N+1)
    x0=np.asarray(np.load(a.lower_nodes,mmap_mode="r")[-1])
    xh=np.asarray(np.load(a.higher_nodes,mmap_mode="r")[-1])
    idx=np.asarray([high.index[k] for k in low.modes],dtype=np.int64)
    x1=xh[idx]
    y0=values(low,x0); y1=values(low,x1)
    sigma={g:(1 if y0[g]>=0 else -1) for g in k36}

    def G(y):
        return sum(abs(y[g]) for g in k36)-9*sum(tau[g]*y[g] for g in tau)
    def L(y):
        return sum(sigma[g]*y[g] for g in k36)-9*sum(tau[g]*y[g] for g in tau)

    Qcorr=sum((y1[g]-y0[g])**2/(2*abs(y0[g])) for g in k36)
    flips=[g for g in k36 if np.sign(y0[g])!=np.sign(y1[g])]
    H=sum(1/(2*abs(y0[g])) for g in k36)
    out={
      "lower_N":a.lower_N,
      "upper_N":a.lower_N+1,
      "base_G":G(y0),
      "target_G":G(y1),
      "delta_L":L(y1)-L(y0),
      "quadratic_kink_correction":Qcorr,
      "quadratic_envelope_target_upper":G(y0)+L(y1)-L(y0)+Qcorr,
      "K36_sign_flip_count":len(flips),
      "H_half_inverse_abs_base":H,
      "max_K36_ratio_change":max(abs(y1[g]-y0[g]) for g in k36)
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
