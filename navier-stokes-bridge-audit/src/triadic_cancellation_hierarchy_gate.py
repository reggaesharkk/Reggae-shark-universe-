"""Resolve triadic cancellation into within-output-mode and across-mode levels.

For ordered triad contributions Z_{k,p,q}, define
  A = sum_{k,p,q} |Z|,
  C_k = sum_{p+q=k} Z,
  B = sum_k |C_k|,
  T = Re sum_k C_k.
Then |T| <= B <= A exactly.

Uses the deterministic G=1 dense fields from triadic_envelope_growth_gate.py.
Finite seeded evidence only; no universal bound is inferred.
"""

import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from triadic_envelope_growth_gate import CUTOFFS, SEEDS, dense_field

HERE = Path(__file__).resolve().parent


def hierarchy(sys, a):
    qdot = np.einsum("ij,ij->i", sys.qwaves, a[sys.left])
    raw = 1j*qdot[:, None]*a[sys.right]
    projected = np.einsum("kij,kj->ki", sys.projectors[sys.out], raw)
    z = -sys.square[sys.out]*np.einsum(
        "ij,ij->i", np.conj(a[sys.out]), projected)

    A = float(np.sum(np.abs(z)))
    grouped = np.zeros(len(sys.modes), dtype=complex)
    np.add.at(grouped, sys.out, z)
    B = float(np.sum(np.abs(grouped)))
    T = float(np.real(np.sum(grouped)))

    assert abs(T) <= B + 1e-12
    assert B <= A + 1e-12

    n = sys.nonlinear(a)
    direct = -float(np.real(np.einsum(
        "i,ij,ij->", sys.square, np.conj(a), n)))
    err = abs(T-direct)
    assert err < 1e-8*max(1.0, abs(T))

    return dict(
        A=A,
        B=B,
        T=T,
        within_ratio_B_over_A=B/A if A else 0.0,
        across_ratio_absT_over_B=abs(T)/B if B else 0.0,
        abs_chi=abs(T)/A if A else 0.0,
        decomposition_error=err,
    )


def run():
    rows = []
    for family in ("ball", "outer_half"):
        for N in CUTOFFS:
            sys = System(N=N, nu=NU)
            samples = [
                hierarchy(sys, dense_field(sys, seed, family))
                for seed in SEEDS
            ]
            rows.append(dict(
                family=family,
                N=N,
                median_B_over_G32=float(np.median(
                    [x["B"] for x in samples])),
                median_B_over_A=float(np.median(
                    [x["within_ratio_B_over_A"] for x in samples])),
                median_absT_over_B=float(np.median(
                    [x["across_ratio_absT_over_B"] for x in samples])),
                median_abs_chi=float(np.median(
                    [x["abs_chi"] for x in samples])),
                samples=samples,
            ))

    return dict(
        normalization="G=1 exactly up to floating point",
        identity=(
            "|T| <= B=sum_k |sum_{p+q=k} Z_kpq| "
            "<= A=sum_{k,p,q}|Z_kpq|"
        ),
        warning=(
            "Finite deterministic random fields only. Near-stability of "
            "B/G^(3/2) on these samples does not imply a universal bound. "
            "Because B>=|T|, the existing fixed-energy concentration "
            "obstruction rules out an energy-only cutoff-uniform "
            "B<=C(E0)G^(3/2) estimate."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "triadic_cancellation_hierarchy_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
