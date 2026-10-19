#!/usr/bin/env python3
"""WP19 v0.25 portable reconstruction of the frozen C500 coalition.

The historical v0.6 JSON byte hash included full-precision floating diagnostic
fields, so it is not portable across floating-point environments. This script
reconstructs the mathematical coalition from the byte-identical historical
N11 predictor and verifies an environment-independent semantic identity:
rank + left orbit + right orbit + fixed sign.

It does not retune the coalition.
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
HISTORICAL_C500_BYTE_SHA="79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216"
EXPECTED_C500_SEMANTIC_SHA="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"
EXPECTED_CAPTURE=0.9994122170697335
EXPECTED_BASE_G=-47.8162782412821
EXPECTED_PAIRS=1048
EXPECTED_MODES=1159

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def projection(k,v):
    k=np.asarray(k,float)
    v=np.asarray(v,complex)
    return v-k*np.dot(k,v)/np.dot(k,k)

def semantic_payload(rows):
    obj={
        "schema":"wp19-c500-semantic-identity-v1",
        "coalition_size":500,
        "keys":[{
            "rank":int(r["rank_from_N11_endpoint"]),
            "left_orbit":[int(x) for x in r["left_orbit"]],
            "right_orbit":[int(x) for x in r["right_orbit"]],
            "fixed_linear_sign":int(r["fixed_linear_sign"]),
        } for r in rows],
    }
    return (json.dumps(obj,sort_keys=True,separators=(",",":"))+"\n").encode()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--n11-nodes",type=Path,required=True)
    ap.add_argument("--k36",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    a=ap.parse_args()

    raw=a.k36.read_bytes()
    k36_sha=hashlib.sha256(raw).hexdigest()
    if k36_sha!=EXPECTED_K36:
        raise SystemExit(f"K36 SHA mismatch: {k36_sha}")

    sys.path.insert(0,str((a.repo/"src").resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    k36_obj=json.loads(raw)
    k36={(tuple(r["left_orbit"]),tuple(r["right_orbit"])) for r in k36_obj["keys"]}

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
            "fixed_linear_sign":1 if signed>=0 else -1,
        })

    sem_sha=hashlib.sha256(semantic_payload(rows)).hexdigest()
    if sem_sha!=EXPECTED_C500_SEMANTIC_SHA:
        raise SystemExit(f"C500 semantic identity mismatch: {sem_sha}")

    c500={(tuple(r["left_orbit"]),tuple(r["right_orbit"])):int(r["fixed_linear_sign"]) for r in rows}
    inside=sum(abs(values[k]) for k in k36)
    signed_out=sum(tau*values[k] for k,tau in c500.items())
    base_G=inside-9.0*signed_out
    outside_total=sum(abs(v) for k,v in values.items() if k not in k36)
    capture=sum(abs(values[k]) for k in c500)/outside_total

    chosen=set(k36)|set(c500)
    pairs=0
    modes={P,Q,K}
    for li,ri in zip(s.left,s.right):
        key=(orbit(s.modes[li]),orbit(s.modes[ri]))
        if key in chosen:
            pairs+=1
            modes.add(s.modes[li])
            modes.add(s.modes[ri])

    if abs(base_G-EXPECTED_BASE_G)>1e-10:
        raise SystemExit(f"historical G invariant mismatch: {base_G}")
    if abs(capture-EXPECTED_CAPTURE)>1e-14:
        raise SystemExit(f"historical capture invariant mismatch: {capture}")
    if pairs!=EXPECTED_PAIRS or len(modes)!=EXPECTED_MODES:
        raise SystemExit(f"support invariant mismatch: pairs={pairs}, modes={len(modes)}")

    obj={
        "schema":"wp19-frozen-c500-outside-orbit-coalition-v1",
        "selection_rule":"Post-hoc at the saved N11 same-datum endpoint: rank every outside-K36 ordered orbit-pair group by absolute normalized contribution and retain ranks 1..500. Freeze for all subsequent use.",
        "K36_key_sha256":EXPECTED_K36,
        "coalition_size":500,
        "keys":rows,
    }
    payload=(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
    byte_sha=hashlib.sha256(payload).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(payload)

    report={
        "schema":"wp19-v0.25-c500-portable-reconstruction-v1",
        "status":"PASS",
        "historical_C500_byte_sha256":HISTORICAL_C500_BYTE_SHA,
        "reproduced_C500_byte_sha256":byte_sha,
        "historical_byte_hash_matches":byte_sha==HISTORICAL_C500_BYTE_SHA,
        "portable_semantic_sha256":sem_sha,
        "portable_semantic_hash_matches":True,
        "N11_base_G_C500":base_G,
        "N11_outside_mass_capture_fraction":capture,
        "ordered_source_pairs":pairs,
        "unique_fourier_modes":len(modes),
        "meaning":"The rank/orbit/sign coalition matches the frozen mathematical selection. Full JSON bytes may differ because the file also stores platform-sensitive full-precision floating diagnostics.",
        "retuned":False,
    }
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
