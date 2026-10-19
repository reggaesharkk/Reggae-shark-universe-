"""Reverse-engineer phase structure in the completed N=10/N=11 continuation.

This diagnostic deliberately separates three questions:

1. Are the optimized *mode phases* themselves globally coherent?
2. How much does the inherited N=10 phase core move when continued to N=11,
   modulo the physically irrelevant spatial-translation gauge phi_k -> phi_k+k.x0?
3. Are unweighted triad-relative phases phi_p+phi_q-phi_k globally coherent?

The last quantity is gauge invariant under spatial translation.  A near-uniform
unweighted distribution does not imply the dynamically weighted triad
contributions are unstructured; it motivates the next coefficient-weighted
triad-phase gate.

Finite diagnostic only.
"""

import argparse
import json
from pathlib import Path

import numpy as np


def wrapped(x):
    return np.angle(np.exp(1j * x))


def resultant(x):
    return float(abs(np.mean(np.exp(1j * x))))


def translation_align(K, delta, max_iter=20):
    """Deterministic Newton alignment for phi-differences modulo k.x0."""
    x = np.zeros(3, dtype=float)

    def objective(xx):
        return 1.0 - float(np.mean(np.cos(delta - K @ xx)))

    for _ in range(max_iter):
        r = delta - K @ x
        grad = -np.mean(np.sin(r)[:, None] * K, axis=0)
        hess = np.einsum("n,ni,nj->ij", np.cos(r), K, K) / len(K)

        try:
            step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            break

        if np.linalg.norm(step) < 1e-13:
            break

        old = objective(x)
        scale = 1.0
        while scale > 1e-6:
            trial = x - scale * step
            if objective(trial) <= old:
                x = trial
                break
            scale *= 0.5
        else:
            break

    residual = wrapped(delta - K @ x)
    return x, residual


def full_phase_map(row):
    phase = {(0, 0, 0): 0.0}
    for k, phi in zip(row["support_vectors"], row["best_phases"]):
        k = tuple(k)
        phase[k] = float(phi)
        phase[tuple(-x for x in k)] = -float(phi)
    return phase


def triad_phase_sample(row, samples=250_000, seed=20260925):
    """Uniform mode-pair sample of the unweighted relative phase."""
    N = int(row["N"])
    phase_map = full_phase_map(row)
    modes = np.asarray(list(phase_map), dtype=int)
    phases = np.asarray([phase_map[tuple(k)] for k in modes], dtype=float)
    index = {tuple(k): i for i, k in enumerate(modes)}
    rng = np.random.default_rng(seed + N)

    values = []
    while len(values) < samples:
        remaining = samples - len(values)
        batch = min(400_000, max(50_000, 2 * remaining))
        pi = rng.integers(0, len(modes), batch)
        qi = rng.integers(0, len(modes), batch)
        K = modes[pi] + modes[qi]
        good = np.flatnonzero(np.sum(K * K, axis=1) <= N * N)

        for j in good:
            ki = index.get(tuple(K[j]))
            if ki is None:
                continue
            values.append(phases[pi[j]] + phases[qi[j]] - phases[ki])
            if len(values) >= samples:
                break

    theta = np.asarray(values[:samples])
    return {
        "samples": samples,
        "R1": resultant(theta),
        "R2": resultant(2 * theta),
        "mean_cos": float(np.mean(np.cos(theta))),
    }


def stage_summary(row):
    records = row["records"]
    order = (
        "inherited_continuation",
        "new_modes_global_best",
        "new_modes_block_best",
        "full_block_best",
    )
    selected = []
    for kind in order:
        matches = [r for r in records if r["kind"] == kind]
        if matches:
            selected.append((kind, matches[-1]))

    stages = []
    previous = None
    for kind, q in selected:
        entry = {
            "kind": kind,
            "C": q["C_infinity_stretch"],
            "N_high": q["H2_high_transfer"],
            "P_positive": q["H1_positive_stretching"],
        }
        if previous is not None:
            entry["C_gain_pct"] = 100 * (
                q["C_infinity_stretch"]
                / previous["C_infinity_stretch"] - 1
            )
            entry["N_high_change_pct"] = 100 * (
                q["H2_high_transfer"]
                / previous["H2_high_transfer"] - 1
            )
            entry["P_positive_change_pct"] = 100 * (
                q["H1_positive_stretching"]
                / previous["H1_positive_stretching"] - 1
            )
        stages.append(entry)
        previous = q
    return stages


def run(path, samples=250_000):
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = {int(row["N"]): row for row in payload["rows"]}
    r10 = rows[10]
    r11 = rows[11]

    phase11 = {
        tuple(k): float(phi)
        for k, phi in zip(r11["support_vectors"], r11["best_phases"])
    }

    K10 = np.asarray(r10["support_vectors"], dtype=float)
    p10 = np.asarray(r10["best_phases"], dtype=float)
    p11_overlap = np.asarray(
        [phase11[tuple(map(int, k))] for k in K10],
        dtype=float,
    )

    delta = wrapped(p11_overlap - p10)
    translation, residual = translation_align(K10, delta)

    stability = {
        "overlap_modes": len(K10),
        "translation_gauge": translation.tolist(),
        "raw_resultant": resultant(delta),
        "aligned_resultant": resultant(residual),
        "mean_abs_residual": float(np.mean(abs(residual))),
        "median_abs_residual": float(np.median(abs(residual))),
        "q90_abs_residual": float(np.quantile(abs(residual), 0.9)),
        "frac_abs_lt_0_25": float(np.mean(abs(residual) < 0.25)),
        "frac_abs_lt_0_5": float(np.mean(abs(residual) < 0.5)),
    }

    one_point = {}
    for row in (r10, r11):
        phi = np.asarray(row["best_phases"], dtype=float)
        one_point[str(row["N"])] = {
            "phase_resultant": resultant(phi),
            "phase_mean_abs_to_zero": float(np.mean(abs(wrapped(phi)))),
        }

    return {
        "status": "phase-structure reverse-engineering diagnostic",
        "stability_N10_to_N11": stability,
        "one_point_phase_coherence": one_point,
        "unweighted_triad_phase_sample": {
            str(row["N"]): triad_phase_sample(
                row, samples=samples
            )
            for row in (r10, r11)
        },
        "optimization_stages": {
            str(row["N"]): stage_summary(row)
            for row in (r10, r11)
        },
        "interpretation": (
            "Mode phases are globally incoherent, while the inherited core "
            "is stable across continuation. Unweighted triad-relative phases "
            "are also nearly uniform, so the next object should be "
            "coefficient-weighted gauge-invariant triad phases rather than "
            "a raw shell/radial phase law."
        ),
        "warning": (
            "The triad-phase sample is unweighted. It does not test the "
            "correlation between relative phase and the complex base triad "
            "coefficient that actually determines nonlinear transfer."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("continuation_json", type=Path)
    parser.add_argument("--samples", type=int, default=250_000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("wp16_phase_structure_results.json"),
    )
    args = parser.parse_args()

    result = run(args.continuation_json, samples=args.samples)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
