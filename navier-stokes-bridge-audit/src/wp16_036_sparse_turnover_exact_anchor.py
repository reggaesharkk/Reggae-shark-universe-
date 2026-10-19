"""Exact rational initial K36 margin for the post-hoc 112-pair N11 witness.

The finite decimal JSON entries are interpreted as rationals, then projected
exactly onto the transverse plane. This certifies only the t=0 sign for the
slightly adjusted rational field; it says nothing about its later trajectory.
"""

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

P, Q, K = (3, 2, 2), (3, -2, 1), (6, 0, 3)
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def conj(x):
    return x[0], -x[1]


def scale(x, r):
    return x[0] * r, x[1] * r


def dot_real(k, a):
    out = ZERO
    for ki, ai in zip(k, a):
        out = add(out, scale(ai, ki))
    return out


def vdot(a, b):
    out = ZERO
    for ai, bi in zip(a, b):
        out = add(out, mul(conj(ai), bi))
    return out


def project(k, a):
    kk = sum(x * x for x in k)
    ak = dot_real(k, a)
    return tuple(add(ai, scale(ak, F(-ki, kk))) for ki, ai in zip(k, a))


def orbit(k):
    return tuple(sorted(abs(x) for x in k))


def fraction_decimal(x):
    return F(str(x))


def input_state(path):
    raw = path.read_bytes()
    obj = json.loads(raw, parse_float=Decimal)
    a = {}
    projection = F(0)
    for row in obj["pairs"]:
        k = tuple(row["wavevector"])
        if k <= tuple(-x for x in k) or k in a:
            raise ValueError("noncanonical or duplicate representative")
        original = tuple((fraction_decimal(r), fraction_decimal(i))
                         for r, i in row["coefficient"])
        transverse = project(k, original)
        projection = max(projection, *(abs(x-y) for old, new in zip(original, transverse)
                          for x, y in zip(old, new)))
        a[k] = transverse
        a[tuple(-x for x in k)] = tuple(conj(x) for x in transverse)
        assert dot_real(k, transverse) == ZERO
    assert len(obj["pairs"]) == 112 and len(a) == 224
    return a, projection, hashlib.sha256(raw).hexdigest()


def source(a, left, right):
    qdot = dot_real(right, a[left])
    raw = tuple(mul(mul((F(0), F(1)), qdot), v) for v in a[right])
    return tuple(scale(v, -1) for v in project(K, raw))


def signed(w, z):
    denom = z[0] * z[0] + z[1] * z[1]
    return (w[1] * z[0] - w[0] * z[1]) / denom


def certified_decimal(x, digits=10):
    unit = 10 ** digits
    lo = x.numerator * unit // x.denominator
    hi = -((-x.numerator * unit) // x.denominator)
    with localcontext() as ctx:
        ctx.prec = 40
        return [str(Decimal(lo) / unit), str(Decimal(hi) / unit)]


def compute(witness, keys_path):
    a, projection, witness_sha = input_state(witness)
    if witness_sha != EXPECTED_WITNESS:
        raise ValueError("witness SHA-256 mismatch")
    keys_raw = keys_path.read_bytes()
    keys_sha = hashlib.sha256(keys_raw).hexdigest()
    if keys_sha != "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47":
        raise ValueError("K36 key file hash mismatch")
    obj = json.loads(keys_raw)
    keys = {(tuple(row["left_orbit"]), tuple(row["right_orbit"])) for row in obj["keys"]}
    if len(keys) != 36 or any(x not in a for x in (P, Q, K)):
        raise ValueError("missing keys or anchor")
    weight = sum(x*x for x in K) ** 2
    b = project(K, tuple(mul(mul((F(0), F(1)), dot_real(Q, a[P])), v)
                         for v in a[Q]))
    z = scale(vdot(a[K], b), -weight)
    if z == ZERO:
        raise ValueError("zero normalizer")
    groups = defaultdict(lambda: ZERO)
    for left in a:
        right = tuple(K[i] - left[i] for i in range(3))
        if right not in a:
            continue
        da = source(a, left, right)
        w = scale(vdot(da, b), -weight)
        key = (orbit(left), orbit(right))
        groups[key] = add(groups[key], w)
    I = sum((abs(signed(w, z)) for k, w in groups.items() if k in keys), F(0))
    O = sum((abs(signed(w, z)) for k, w in groups.items() if k not in keys), F(0))
    margin = I - 9*O
    return {"status": "exact rational initial margin for projected finite decimal data",
            "witness_sha256": witness_sha, "K36_keys_sha256": keys_sha,
            "conjugate_pairs": 112, "nonzero_ordered_group_count": len(groups),
            "max_coefficient_projection_change_upper_decimal": certified_decimal(projection, 20)[1],
            "normalizer_squared_positive": z[0]*z[0]+z[1]*z[1] > 0,
            "I_interval_decimal": certified_decimal(I),
            "O_interval_decimal": certified_decimal(O),
            "F0_interval_decimal": certified_decimal(margin),
            "exact_F0_positive": margin > 0,
            "interpretation": "only the initial Galerkin algebra is certified; no validated trajectory or continuum claim"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--witness", type=Path, required=True)
    p.add_argument("--keys", type=Path, required=True)
    p.add_argument("--result", type=Path, required=True)
    args = p.parse_args()
    result = compute(args.witness, args.keys)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2) + "\n")
    print("exact_F0_positive", result["exact_F0_positive"],
          "F0", result["F0_interval_decimal"],
          "projection", result["max_coefficient_projection_change_upper_decimal"])
    if not result["exact_F0_positive"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
