#!/usr/bin/env python3
"""WP19 v0.25 wrapper for exact signed-C500 endpoint composition.

The v0.10 arithmetic is reused unchanged. Before invoking it, this wrapper
checks the portable semantic identity of the C500 rank/orbit/sign coalition.
It then binds v0.10's historical byte-hash guard to the actually reconstructed
file bytes for this run. No coalition retuning is permitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_C500_SEMANTIC_SHA="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"
HISTORICAL_C500_BYTE_SHA="79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216"

def semantic_sha(path: Path):
    obj=json.loads(path.read_text())
    rows=obj["keys"]
    semantic={
        "schema":"wp19-c500-semantic-identity-v1",
        "coalition_size":int(obj["coalition_size"]),
        "keys":[{
            "rank":int(r["rank_from_N11_endpoint"]),
            "left_orbit":[int(x) for x in r["left_orbit"]],
            "right_orbit":[int(x) for x in r["right_orbit"]],
            "fixed_linear_sign":int(r["fixed_linear_sign"]),
        } for r in rows],
    }
    payload=(json.dumps(semantic,sort_keys=True,separators=(",",":"))+"\n").encode()
    return hashlib.sha256(payload).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,required=True)
    ap.add_argument("--nodes",required=True)
    ap.add_argument("--k36",required=True)
    ap.add_argument("--c500",required=True)
    ap.add_argument("--E",required=True)
    ap.add_argument("--repo-src",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()

    c500_path=Path(a.c500)
    sem=semantic_sha(c500_path)
    if sem!=EXPECTED_C500_SEMANTIC_SHA:
        raise SystemExit(f"C500 semantic identity mismatch: {sem}")

    byte_sha=hashlib.sha256(c500_path.read_bytes()).hexdigest()

    sys.path.insert(0,str(Path(a.repo_src).resolve()))
    import wp19_v0_10_signed_numerator_exact as exact

    # v0.10's historical byte guard protected identity. v0.25 has already
    # verified that identity using the portable rank/orbit/sign digest above.
    exact.EXPECTED_C500=byte_sha
    exact.run(
        a.N,a.nodes,a.k36,a.c500,a.E,a.repo_src,a.out
    )

    out=Path(a.out)
    res=json.loads(out.read_text())
    res["schema"]="wp19-v0.25-signed-c500-numerator-certificate-v1"
    res["C500_input_byte_sha256"]=byte_sha
    res["C500_historical_byte_sha256"]=HISTORICAL_C500_BYTE_SHA
    res["C500_historical_byte_hash_matches"]=(byte_sha==HISTORICAL_C500_BYTE_SHA)
    res["C500_semantic_sha256"]=sem
    res["C500_identity_mode"]="portable rank/orbit/sign semantic identity"
    res["C500_retuned"]=False
    out.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "N":res["N"],
        "status":res["status"],
        "C500_input_byte_sha256":byte_sha,
        "C500_historical_byte_hash_matches":res["C500_historical_byte_hash_matches"],
        "C500_semantic_sha256":sem,
        "K36_sign_locked_count":res["K36_sign_locked_count"],
        "true_signed_numerator_upper_decimal":res["true_signed_numerator_upper_decimal"],
        "certified_G_upper_decimal":res["certified_G_upper_decimal"],
        "normalizer_true_lower_bound_decimal":res["normalizer_true_lower_bound_decimal"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
