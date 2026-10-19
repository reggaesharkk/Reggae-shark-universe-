#!/usr/bin/env python3
"""Independent audit of the WP19 v0.25b aggregate artifact (stdlib only).

Usage:
  python tools/verify_wp19_v025b.py <wp19-v0-25b-signed-c500-n11-n18.zip>

Checks:
  1. SHA256SUMS.txt matches every payload file in the ZIP.
     Historical artifacts accidentally listed SHA256SUMS.txt itself; that
     impossible self-hash entry is skipped explicitly.
     GitHub artifact downloads may flatten the uploaded top-level final/
     directory, so exactly that prefix normalization is accepted.
  2. Summary claims: all PASS, negative signed numerator, K36 count=36,
     negative certified G upper bound and positive normalizer lower bound.
  3. For rows with an explicit numerator, checks the necessary consistency
     implied_norm=sqrt(numerator/G_upper) >= normalizer_lower.
  4. Dumps relevant per-N numeric fields and cross-checks summary values.
"""
import hashlib
import json
import math
import re
import sys
import zipfile
from decimal import Decimal, getcontext

getcontext().prec = 50

def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj

def as_dec(x):
    try:
        return Decimal(str(x))
    except Exception:
        return None

def main(zpath):
    ok = True
    z = zipfile.ZipFile(zpath)
    names = z.namelist()
    print("files:", names)

    sums = [n for n in names if n.upper().startswith("SHA256SUMS")]
    if sums:
        manifest = sums[0]
        for line in z.read(manifest).decode().splitlines():
            m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line.strip())
            if not m:
                continue
            want, fn = m.group(1).lower(), m.group(2).strip()
            zfn = fn
            if zfn not in names and zfn.startswith("final/") and zfn[6:] in names:
                zfn = zfn[6:]
            if zfn not in names:
                print("  MISSING", fn)
                ok = False
                continue
            if zfn == manifest or zfn.endswith("/" + manifest):
                print(f"  [skip-self] {fn}")
                continue
            got = hashlib.sha256(z.read(zfn)).hexdigest()
            flag = "ok " if got == want else "BAD"
            ok &= got == want
            print(f"  [{flag}] {fn}")
    else:
        print("  no SHA256SUMS file found")
        ok = False

    summ_name = next(n for n in names if "SUMMARY" in n.upper())
    summ = json.loads(z.read(summ_name))
    print("\nsummary status:", summ.get("status"), "| retuned:", summ.get("C500_retuned"))
    rows = {r["N"]: r for r in summ["rows"]}
    for N, r in sorted(rows.items()):
        G = as_dec(r["certified_G_upper_decimal"])
        nlo = as_dec(r["normalizer_true_lower_bound_decimal"])
        good = (r["status"] == "PASS" and r["K36_sign_locked_count"] == 36
                and r["certified_signed_numerator_negative"] and G < 0 and nlo > 0)
        line = f"N={N:2d} G_upper={G:.6f} norm_lo={nlo:.3f}"
        num = r.get("true_signed_numerator_upper_decimal")
        if num is not None:
            num = as_dec(num)
            implied = (num / G).sqrt()
            good &= num < 0 and implied >= nlo
            line += (f" num={num:.4e} implied_norm={implied:.3f} "
                     f"(gap {implied - nlo:.3f}, rel {((implied - nlo) / nlo):.2e})")
        print(("  [ok ] " if good else "  [BAD] ") + line)
        ok &= good

    print("\nper-N file contents (relevant numeric fields):")
    for n in sorted(names):
        m = re.match(r"N(\d+)_signed_C500\.json$", n)
        if not m:
            continue
        N = int(m.group(1))
        data = json.loads(z.read(n))
        print(f"\n{n}: top-level keys = {list(data)[:12] if isinstance(data, dict) else type(data)}")
        hits = [(p, v) for p, v in walk(data)
                if re.search(r"normaliz|numerat|k36|sign_lock|certified_G|G_upper", p, re.I)
                and not isinstance(v, (dict, list))]
        for p, v in hits[:25]:
            print(f"    {p} = {v}")
        if len(hits) > 25:
            print(f"    ... {len(hits) - 25} more")
        r = rows.get(N)
        if r:
            for p, v in walk(data):
                if p.endswith("certified_G_upper_decimal") and as_dec(v) != as_dec(r["certified_G_upper_decimal"]):
                    print("    MISMATCH G_upper vs summary:", v, r["certified_G_upper_decimal"])
                    ok = False
                if p.endswith("normalizer_true_lower_bound_decimal") and as_dec(v) != as_dec(r["normalizer_true_lower_bound_decimal"]):
                    print("    MISMATCH normalizer vs summary:", v)
                    ok = False

    print("\nOVERALL:", "PASS" if ok else "CHECK FAILURES ABOVE")
    return 0 if ok else 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
