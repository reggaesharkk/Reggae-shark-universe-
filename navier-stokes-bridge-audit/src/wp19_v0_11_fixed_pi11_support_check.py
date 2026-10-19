#!/usr/bin/env python3
"""Verify the fixed-Pi11 support premise for the frozen K36+C500 objective."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path

EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_C500="79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216"
P,Q,K=(3,2,2),(3,-2,1),(6,0,3)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def n2(v):
    return sum(int(x)*int(x) for x in v)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--k36",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()

    if sha(a.k36)!=EXPECTED_K36:
        raise SystemExit("K36 SHA mismatch")
    if sha(a.c500)!=EXPECTED_C500:
        raise SystemExit("C500 SHA mismatch")

    k36=json.loads(a.k36.read_text())["keys"]
    c500=json.loads(a.c500.read_text())["keys"]
    rows=k36+c500
    orbits={tuple(r[s]) for r in rows for s in ("left_orbit","right_orbit")}
    max_sq=max(n2(o) for o in orbits)
    max_component=max(max(o) for o in orbits)
    max_orbits=sorted([list(o) for o in orbits if n2(o)==max_sq])

    result={
        "K36_sha256":EXPECTED_K36,
        "C500_sha256":EXPECTED_C500,
        "K36_count":len(k36),
        "C500_count":len(c500),
        "unique_orbit_count":len(orbits),
        "max_selected_orbit_squared_norm":max_sq,
        "max_selected_orbit_norm":math.sqrt(max_sq),
        "max_selected_orbit_component":max_component,
        "max_norm_orbits":max_orbits,
        "anchor_squared_norms":{"P":n2(P),"Q":n2(Q),"K":n2(K)},
        "fixed_Pi11_support":max_sq<=121 and max(n2(P),n2(Q),n2(K))<=121,
        "exact_consequence":"For any cutoff M>=11, the frozen C500 numerator depends only on Pi_11 a; when the normalizer is nonzero, G_C500(a)=G_C500(Pi_11 a)."
    }
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.write_text(payload)
    print(payload,end="")

if __name__=="__main__":
    main()
