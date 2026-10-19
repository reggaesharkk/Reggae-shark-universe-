"""Cutoff-growth stress test for the absolute triadic envelope.

Constructs deterministic dense real divergence-free Fourier fields, normalizes
each to G=||grad u||_2^2=1, and measures A/G^(3/2), T/G^(3/2), and chi=T/A.
Finite seeded evidence only; it is not an asymptotic theorem.
"""

import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from triadic_coherence_suite import snapshot

HERE = Path(__file__).resolve().parent
SEEDS = (20260924, 20260925, 20260926)
CUTOFFS = range(2, 8)


def canonical_half(k):
    """Select exactly one member of each nonzero +/-k pair."""
    for x in k:
        if x > 0:
            return True
        if x < 0:
            return False
    return False


def dense_field(sys, seed, family):
    rng = np.random.default_rng(seed)
    a = np.zeros((len(sys.modes), 3), dtype=complex)

    for i, k in enumerate(sys.modes):
        if k == (0, 0, 0) or not canonical_half(k):
            continue
        radius = float(np.sqrt(sys.square[i]))
        if family == "outer_half" and not (sys.N/2 < radius <= sys.N):
            continue
        if family not in {"ball", "outer_half"}:
            raise ValueError(f"Unknown family {family}")

        raw = rng.normal(size=3) + 1j*rng.normal(size=3)
        value = sys.projectors[i] @ raw
        j = sys.index[tuple(-x for x in k)]
        a[i] = value
        a[j] = value.conj()

    G = float(np.sum(sys.square[:, None] * abs(a)**2))
    assert G > 0
    a /= np.sqrt(G)

    reality = float(np.max(np.linalg.norm(a[sys.neg]-np.conj(a), axis=1)))
    divergence = float(np.max(abs(np.einsum("ij,ij->i", sys.waves, a))))
    normalized_G = float(np.sum(sys.square[:, None] * abs(a)**2))
    assert reality < 1e-12
    assert divergence < 1e-12
    assert abs(normalized_G-1.0) < 1e-12
    return a


def run():
    rows = []
    for family in ("ball", "outer_half"):
        for N in CUTOFFS:
            sys = System(N=N, nu=NU)
            samples = []
            for seed in SEEDS:
                a = dense_field(sys, seed, family)
                d = snapshot(sys, a)
                samples.append(dict(
                    seed=seed,
                    A_over_G32=d["A"],
                    T_over_G32=d["T"],
                    chi=d["chi"],
                    decomposition_error=d["decomposition_error"],
                ))

            rows.append(dict(
                family=family,
                N=N,
                samples=samples,
                median_A_over_G32=float(np.median(
                    [x["A_over_G32"] for x in samples])),
                median_abs_T_over_G32=float(np.median(
                    [abs(x["T_over_G32"]) for x in samples])),
                median_abs_chi=float(np.median(
                    [abs(x["chi"]) for x in samples])),
            ))

    return dict(
        normalization="G=1 exactly up to floating point",
        seeds=list(SEEDS),
        families={
            "ball": "all nonzero modes with |k|<=N",
            "outer_half": "modes with N/2<|k|<=N",
        },
        warning=(
            "Only N=2,...,7 and three deterministic random seeds are tested. "
            "Growth of A/G^(3/2) in these samples does not prove divergence "
            "as N->infinity; small chi values do not prove a cancellation theorem."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "triadic_envelope_growth_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
