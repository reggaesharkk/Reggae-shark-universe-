#!/usr/bin/env python3
"""WP19 exact K36 cutoff-monotonicity support checker.

Checks the finite combinatorial premise used in the v0.4 theorem:
every orbit appearing in the frozen K36 selected key set has norm < 10.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path

EXPECTED = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
P,Q,K=(3,2,2),(3,-2,1),(6,0,3)

def n2(v):
    return sum(int(x)*int(x) for x in v)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--keys",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    raw=args.keys.read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    if sha != EXPECTED:
        raise SystemExit("K36 key SHA mismatch")

    obj=json.loads(raw)
    vals=[]
    for row in obj["keys"]:
        vals.append(n2(row["left_orbit"]))
        vals.append(n2(row["right_orbit"]))

    result={
        "status":"exact finite combinatorial support check",
        "keys_sha256":sha,
        "selected_key_count":len(obj["keys"]),
        "max_selected_orbit_squared_norm":max(vals),
        "max_selected_orbit_norm":math.sqrt(max(vals)),
        "all_selected_orbits_strictly_below_10":max(vals)<100,
        "anchor_squared_norms":{"P":n2(P),"Q":n2(Q),"K":n2(K)},
        "safe_integer_base_cutoff":10
    }
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
