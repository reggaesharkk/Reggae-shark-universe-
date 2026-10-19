#!/usr/bin/env python3
"""Build and verify the frozen WP19 v0.6 C500 outside coalition."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_C500="79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216"

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def projection(k,v):
    k=np.asarray(k,float); v=np.asarray(v,complex)
    return v-k*np.dot(k,v)/np.dot(k,k)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--n11-nodes",type=Path,required=True)
    p.add_argument("--k36",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    raw=a.k36.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_K36:
        raise SystemExit("K36 SHA mismatch")

    sys.path.insert(0,str(a.repo/"src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    k36_obj=json.loads(raw)
    k36={(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
         for r in k36_obj["keys"]}

    s=DealiasedSystem(11)
    field=np.asarray(np.load(a.n11_nodes,mmap_mode="r")[-1])
    pidx,qidx,kidx=(s.index[x] for x in (P,Q,K))
    b=projection(K,1j*np.dot(Q,field[pidx])*field[qidx])
    weight=float(s.square[kidx]**2)
    z=-weight*np.vdot(field[kidx],b)

    groups={}
    for li,ri in zip(s.left,s.right):
        d=-projection(K,1j*np.dot(s.waves[ri],field[li])*field[ri])
        key=(orbit(s.modes[li]),orbit(s.modes[ri]))
        groups[key]=groups.get(key,0j)-weight*np.vdot(d,b)

    values={key:float((w/z).imag) for key,w in groups.items()}
    ranked=sorted(
        [(abs(v),key,v) for key,v in values.items() if key not in k36],
        reverse=True
    )

    rows=[]
    for rank,(mass,key,signed) in enumerate(ranked[:500],1):
        rows.append({
            "rank_from_N11_endpoint":rank,
            "left_orbit":list(key[0]),
            "right_orbit":list(key[1]),
            "N11_endpoint_absolute_mass":mass,
            "N11_endpoint_signed_value":signed,
            "fixed_linear_sign":1 if signed>=0 else -1
        })

    obj={
        "schema":"wp19-frozen-c500-outside-orbit-coalition-v1",
        "selection_rule":"Post-hoc at the saved N11 same-datum endpoint: rank every outside-K36 ordered orbit-pair group by absolute normalized contribution and retain ranks 1..500. Freeze for all subsequent use.",
        "K36_key_sha256":EXPECTED_K36,
        "coalition_size":500,
        "keys":rows
    }

    payload=(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
    sha=hashlib.sha256(payload).hexdigest()
    if sha!=EXPECTED_C500:
        raise SystemExit(f"C500 SHA mismatch: {sha}")
    a.output.write_bytes(payload)

    c500={(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in rows}
    chosen=k36|c500
    max_sq=max(sum(x*x for x in orb) for pair in chosen for orb in pair)
    counts={}
    for N in (11,12,13,14,17):
        ss=DealiasedSystem(N)
        modes={P,Q,K}; pairs=0
        for li,ri in zip(ss.left,ss.right):
            key=(orbit(ss.modes[li]),orbit(ss.modes[ri]))
            if key in chosen:
                pairs+=1
                modes.add(ss.modes[li]); modes.add(ss.modes[ri])
        counts[str(N)]={"ordered_source_pairs":pairs,
                        "unique_fourier_modes":len(modes)}

    print(json.dumps({
        "K36_sha256":EXPECTED_K36,
        "C500_sha256":sha,
        "max_selected_orbit_squared_norm":max_sq,
        "support_counts":counts,
        "cutoff_invariant_support":
            len({(v["ordered_source_pairs"],v["unique_fourier_modes"])
                 for v in counts.values()})==1
    },indent=2))

if __name__=="__main__":
    main()
