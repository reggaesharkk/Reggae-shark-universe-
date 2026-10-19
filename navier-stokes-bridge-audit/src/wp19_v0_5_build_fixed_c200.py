#!/usr/bin/env python3
"""Build and verify the frozen WP19 v0.5 C200 outside coalition.

The coalition is selected from the saved N11 same-datum endpoint by one
deterministic rule: rank all outside-K36 ordered orbit-pair groups by absolute
normalized contribution and retain the first 200.

The expected output SHA-256 freezes the resulting key set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_C200="4fb5531fcc6c4490aa7826992ff843f27fefdbc1427c7587ac0544027420e698"

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def projection(k,v):
    k=np.asarray(k,float)
    v=np.asarray(v,complex)
    return v-k*np.dot(k,v)/np.dot(k,k)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--n11-nodes",type=Path,required=True)
    ap.add_argument("--k36",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    raw=args.k36.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_K36:
        raise SystemExit("K36 SHA mismatch")

    sys.path.insert(0,str(args.repo/"src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    k36_obj=json.loads(raw)
    k36={(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in k36_obj["keys"]}

    s=DealiasedSystem(11)
    a=np.asarray(np.load(args.n11_nodes,mmap_mode="r")[-1])
    p,q,k=(s.index[x] for x in (P,Q,K))
    b=projection(K,1j*np.dot(Q,a[p])*a[q])
    weight=float(s.square[k]**2)
    z=-weight*np.vdot(a[k],b)

    groups={}
    for li,ri in zip(s.left,s.right):
        d=-projection(K,1j*np.dot(s.waves[ri],a[li])*a[ri])
        key=(orbit(s.modes[li]),orbit(s.modes[ri]))
        groups[key]=groups.get(key,0j)-weight*np.vdot(d,b)

    vals={key:float((w/z).imag) for key,w in groups.items()}
    ranked=sorted(
        [(abs(v),key,v) for key,v in vals.items() if key not in k36],
        reverse=True
    )

    rows=[]
    for rank,(mass,key,signed) in enumerate(ranked[:200],1):
        rows.append({
            "rank_from_N11_endpoint":rank,
            "left_orbit":list(key[0]),
            "right_orbit":list(key[1]),
            "N11_endpoint_signed_value":signed,
            "N11_endpoint_absolute_mass":mass,
        })

    obj={
        "schema":"wp19-fixed-outside-coalition-v0.5",
        "status":"post-hoc N11-derived coalition; frozen for later cutoff tests",
        "source_cutoff":11,
        "selection_rule":"top 200 outside-K36 ordered orbit-pair groups by absolute normalized contribution at the saved N11 same-datum endpoint",
        "K36_key_sha256":EXPECTED_K36,
        "coalition_size":200,
        "keys":rows,
    }

    payload=(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
    sha=hashlib.sha256(payload).hexdigest()
    if sha!=EXPECTED_C200:
        raise SystemExit(f"C200 SHA mismatch: {sha}")

    args.output.write_bytes(payload)

    c200={(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in rows}
    chosen=k36|c200
    max_sq=max(sum(x*x for x in orb) for pair in chosen for orb in pair)

    support={}
    for N in [11,12,13,14,17]:
        ss=DealiasedSystem(N)
        modes={P,Q,K}
        pairs=0
        for li,ri in zip(ss.left,ss.right):
            key=(orbit(ss.modes[li]),orbit(ss.modes[ri]))
            if key in chosen:
                pairs+=1
                modes.add(ss.modes[li])
                modes.add(ss.modes[ri])
        support[str(N)]={"ordered_source_pairs":pairs,"unique_fourier_modes":len(modes)}

    print(json.dumps({
        "K36_sha256":EXPECTED_K36,
        "C200_sha256":sha,
        "max_selected_orbit_squared_norm":max_sq,
        "support_counts":support,
        "cutoff_invariant_support":len({(x["ordered_source_pairs"],x["unique_fourier_modes"]) for x in support.values()})==1,
    },indent=2))

if __name__=="__main__":
    main()
