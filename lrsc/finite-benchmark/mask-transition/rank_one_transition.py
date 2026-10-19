#!/usr/bin/env python3
"""Exact-form, high-precision mask transition identity for M=99.

This is a post-certificate mechanism diagnostic; it performs no subset search.
"""
from pathlib import Path
import runpy

import mpmath as mp

src = Path(__file__).resolve().parents[2] / "odd-ring-rank-theorem" / "v1.2.2-supplement" / "source" / "part2_build.py"
g = runpy.run_path(str(src))
M, J, jh, cosT, stencil = (g[x] for x in ("M", "J", "jh", "cosT", "stencil"))
build = g["build"]
sq = g["sq"]
mp.mp.dps = 50


def inner(x, y):
    return mp.fsum(a * b for a, b in zip(x, y)) / M


def residual(E, V, subset):
    return [E[t] - mp.fsum(V[i][t] for i in subset) for t in range(M)]


def main():
    old_m, old_E, old_V = build(mp.mpf("0.08"))
    new_m, new_E, new_V = build(mp.mpf("0.07"))
    added = [t for t in range(M) if new_m[t] and not old_m[t]]
    assert added == [41, 58]
    assert all(J[t] == 0 for t in added)
    assert new_E == old_E

    delta = [int(t in added) for t in range(M)]
    h = stencil(delta)
    assert h == stencil([new_m[t] - old_m[t] for t in range(M)])
    beta = [jh[0]] + [2 * jh[r] * cosT[r][41] for r in range(1, 50)]
    # Reflection symmetry ensures the two added sites share every w_r value.
    for r in range(1, 50):
        assert abs(cosT[r][41] - cosT[r][58]) < mp.mpf("1e-45")
    discrepancy = max(abs(new_V[r][t] - old_V[r][t] - beta[r] * h[t])
                      for r in range(50) for t in range(M))
    assert discrepancy < mp.mpf("1e-45")

    print("transition: theta 0.08 -> 0.07, M=99, added sites 41 and 58")
    print("target E unchanged:", new_E == old_E)
    print("max |V07 - V08 - h beta^T|:", mp.nstr(discrepancy, 5))
    print("||h||^2:", mp.nstr(sq(h), 18))
    print("||E||^2:", mp.nstr(sq(old_E), 18))
    old_witness = (0, 1, 3, 42, 43, 44, 45, 46, 47, 48, 49)
    new_witness = (0, 1, 2, 4, 5, 6, 42, 43, 44, 45, 46, 47, 48, 49)
    for name, subset in (("0.08 K11 witness", old_witness),
                         ("0.07 K14 witness", new_witness)):
        r0 = residual(old_E, old_V, subset)
        r1 = residual(new_E, new_V, subset)
        B = mp.fsum(beta[i] for i in subset)
        predicted = sq(r0) - 2 * B * inner(r0, h) + B * B * sq(h)
        assert abs(predicted - sq(r1)) < mp.mpf("1e-45")
        print(name)
        print("  sum beta:", mp.nstr(B, 18))
        print("  old relative residual:", mp.nstr(mp.sqrt(sq(r0) / sq(old_E)), 18))
        print("  new relative residual:", mp.nstr(mp.sqrt(sq(r1) / sq(new_E)), 18))
        print("  quadratic identity error:", mp.nstr(abs(predicted - sq(r1)), 5))


if __name__ == "__main__":
    main()
