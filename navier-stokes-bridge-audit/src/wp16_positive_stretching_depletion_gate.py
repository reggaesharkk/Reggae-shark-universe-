"""Physical-space positive-stretching depletion audit for the N=11 continuation.

Compares the inherited N=10 phase map embedded in the N=11 support against the
final optimized N=11 phase map. Modal magnitudes and polarizations are fixed;
only phases differ.

Primary object:
    F(x) = omega(x) · S(x) omega(x)
    P_plus = mean(max(F,0))

The audit asks whether optimization reduces P_plus by suppressing a small
extreme positive set or by broad depression of positive stretching.

Finite Galerkin diagnostic only.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate
from strain_alignment_trajectory import spatial_fields


def local_stretch(system, state, grid):
    grad, omega, _, imag = spatial_fields(system, state, grid)
    if imag > 1e-10:
        raise AssertionError(f"imaginary field error {imag}")
    strain = (grad + np.swapaxes(grad, -1, -2)) / 2
    F = np.einsum("...i,...ij,...j->...", omega, strain, omega)
    return F


def top_share(F, frac):
    pos = np.maximum(F.ravel(), 0.0)
    total = float(np.sum(pos))
    if total <= 0:
        return 0.0
    n = max(1, int(np.ceil(frac * len(pos))))
    idx = np.argpartition(pos, -n)[-n:]
    return float(np.sum(pos[idx]) / total)


def top_mask(F, frac):
    flat = np.maximum(F.ravel(), 0.0)
    n = max(1, int(np.ceil(frac * len(flat))))
    idx = np.argpartition(flat, -n)[-n:]
    mask = np.zeros(len(flat), dtype=bool)
    mask[idx] = True
    return mask.reshape(F.shape)


def jaccard(a, b):
    union = np.logical_or(a, b)
    if not np.any(union):
        return 1.0
    return float(np.logical_and(a, b).sum() / union.sum())


def summarize_field(F):
    pos = np.maximum(F, 0.0)
    positive = F > 0
    return {
        "P_plus": float(np.mean(pos)),
        "signed_mean": float(np.mean(F)),
        "positive_volume_fraction": float(np.mean(positive)),
        "max_positive": float(np.max(pos)),
        "q90_positive_allpoints": float(np.quantile(pos, 0.90)),
        "q95_positive_allpoints": float(np.quantile(pos, 0.95)),
        "q99_positive_allpoints": float(np.quantile(pos, 0.99)),
        "top_1pct_contribution": top_share(F, 0.01),
        "top_5pct_contribution": top_share(F, 0.05),
        "top_10pct_contribution": top_share(F, 0.10),
    }


def inherited_bins(F_inh, F_opt):
    mask = F_inh > 0
    vals = F_inh[mask]
    if len(vals) == 0:
        return []

    qs = [0.0, 0.50, 0.90, 0.95, 0.99, 1.0]
    edges = np.quantile(vals, qs)
    out = []

    for lo_q, hi_q, lo, hi in zip(qs[:-1], qs[1:], edges[:-1], edges[1:]):
        if hi_q == 1.0:
            sel = mask & (F_inh >= lo) & (F_inh <= hi)
        else:
            sel = mask & (F_inh >= lo) & (F_inh < hi)

        count = int(sel.sum())
        if not count:
            continue

        inherited_sum = float(np.sum(np.maximum(F_inh[sel], 0.0)))
        optimized_sum = float(np.sum(np.maximum(F_opt[sel], 0.0)))

        out.append({
            "quantile_range": [lo_q, hi_q],
            "count": count,
            "fraction_of_grid": float(count / F_inh.size),
            "inherited_mean_F": float(np.mean(F_inh[sel])),
            "optimized_mean_F_same_points": float(np.mean(F_opt[sel])),
            "inherited_positive_sum": inherited_sum,
            "optimized_positive_sum_same_points": optimized_sum,
            "positive_sum_ratio_opt_over_inherited": (
                optimized_sum / inherited_sum if inherited_sum > 0 else None
            ),
        })

    return out


def build_states(payload):
    rows = {int(r["N"]): r for r in payload["rows"]}
    r10 = rows[10]
    r11 = rows[11]

    system = System(N=11, nu=NU)
    base = base_state(system, float(r11["amplitude"]), float(r11["anchor_time"]))
    pairs = active_pairs(system, base)

    support11 = [list(k) for _, _, k in pairs]
    if support11 != r11["support_vectors"]:
        raise AssertionError("reconstructed N11 support mismatch")

    phase10 = {
        tuple(k): float(phi)
        for k, phi in zip(r10["support_vectors"], r10["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    for j, (_, _, k) in enumerate(pairs):
        inherited[j] = phase10.get(tuple(k), 0.0)

    optimized = np.asarray(r11["best_phases"], dtype=float)

    a_inh = phase_rotate(base, pairs, inherited)
    a_opt = phase_rotate(base, pairs, optimized)
    return system, a_inh, a_opt


def run(path, grids):
    payload = json.loads(path.read_text(encoding="utf-8"))
    system, a_inh, a_opt = build_states(payload)

    rows = []
    for grid in grids:
        F_inh = local_stretch(system, a_inh, grid)
        F_opt = local_stretch(system, a_opt, grid)

        sin = summarize_field(F_inh)
        sop = summarize_field(F_opt)

        pos_inh = F_inh > 0
        pos_opt = F_opt > 0

        row = {
            "grid": grid,
            "inherited": sin,
            "optimized": sop,
            "P_plus_ratio_opt_over_inherited": (
                sop["P_plus"] / sin["P_plus"] if sin["P_plus"] > 0 else None
            ),
            "P_plus_change_pct": 100 * (
                sop["P_plus"] / sin["P_plus"] - 1
            ),
            "positive_volume_change_pct": 100 * (
                sop["positive_volume_fraction"] / sin["positive_volume_fraction"] - 1
            ),
            "positive_set_jaccard": jaccard(pos_inh, pos_opt),
            "top_1pct_jaccard": jaccard(top_mask(F_inh, 0.01), top_mask(F_opt, 0.01)),
            "top_5pct_jaccard": jaccard(top_mask(F_inh, 0.05), top_mask(F_opt, 0.05)),
            "inherited_positive_quantile_bins": inherited_bins(F_inh, F_opt),
        }
        rows.append(row)

    return {
        "status": "executed N11 positive-stretching depletion audit",
        "source": str(path),
        "comparison": "N11 inherited N10 phase map vs final optimized N11 phase map",
        "grids": list(grids),
        "rows": rows,
        "interpretation_rule": (
            "This is a finite physical-space diagnostic. It identifies how the "
            "optimized phase perturbation changes positive stretching at fixed "
            "modal magnitudes; it is not an asymptotic or regularity theorem."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("continuation_json", type=Path)
    p.add_argument("--grids", nargs="+", type=int, default=[48, 64, 96])
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/"
            "wp16_positive_stretching_depletion_results.json"
        ),
    )
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(args.continuation_json, args.grids)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
