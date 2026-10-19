"""N=11 phase-path and old/new block decomposition.

Compare the inherited N=10 phase map embedded at N=11 with the final optimized
N=11 phase map. Decompose the wrapped phase displacement into:

  * old-core corrections on inherited modes,
  * new-shell phases on newly activated modes,
  * both together.

Evaluate a linear wrapped phase path for each block and refine the four endpoint
states on a higher physical grid.

Finite Galerkin diagnostic only.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


def wrapped(x):
    return np.angle(np.exp(1j * x))


def build_phase_vectors(payload):
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
    old_mask = np.zeros(len(pairs), dtype=bool)

    for j, (_, _, k) in enumerate(pairs):
        if tuple(k) in phase10:
            inherited[j] = phase10[tuple(k)]
            old_mask[j] = True

    final = np.asarray(r11["best_phases"], dtype=float)
    delta = wrapped(final - inherited)

    return system, base, pairs, inherited, final, delta, old_mask


def eval_phases(system, base, pairs, phases, grid):
    return evaluate(system, phase_rotate(base, pairs, phases), grid=grid)


def path(system, base, pairs, inherited, delta, mask, lambdas, grid):
    rows = []
    for lam in lambdas:
        phases = inherited + lam * (delta * mask)
        q = eval_phases(system, base, pairs, phases, grid)
        rows.append({
            "lambda": float(lam),
            **q,
        })
    return rows


def endpoint(name, phases, system, base, pairs, grid):
    q = eval_phases(system, base, pairs, phases, grid)
    return {"name": name, **q}


def run(path_in, path_grid, refine_grid, nsteps):
    payload = json.loads(path_in.read_text(encoding="utf-8"))
    system, base, pairs, inherited, final, delta, old_mask = build_phase_vectors(payload)

    new_mask = ~old_mask
    full_mask = np.ones(len(pairs), dtype=bool)
    lambdas = np.linspace(0.0, 1.0, nsteps)

    paths = {
        "old_core_only": path(
            system, base, pairs, inherited, delta, old_mask, lambdas, path_grid
        ),
        "new_shell_only": path(
            system, base, pairs, inherited, delta, new_mask, lambdas, path_grid
        ),
        "full": path(
            system, base, pairs, inherited, delta, full_mask, lambdas, path_grid
        ),
    }

    old_only = inherited + delta * old_mask
    new_only = inherited + delta * new_mask
    both = inherited + delta

    endpoints = {
        "inherited": endpoint(
            "inherited", inherited, system, base, pairs, refine_grid
        ),
        "old_core_only": endpoint(
            "old_core_only", old_only, system, base, pairs, refine_grid
        ),
        "new_shell_only": endpoint(
            "new_shell_only", new_only, system, base, pairs, refine_grid
        ),
        "full": endpoint(
            "full", both, system, base, pairs, refine_grid
        ),
    }

    base_q = endpoints["inherited"]

    for q in endpoints.values():
        q["C_gain_vs_inherited_pct"] = 100 * (
            q["C_infinity_stretch"] / base_q["C_infinity_stretch"] - 1
        )
        q["N_high_change_vs_inherited_pct"] = 100 * (
            q["H2_high_transfer"] / base_q["H2_high_transfer"] - 1
        )
        q["P_plus_change_vs_inherited_pct"] = 100 * (
            q["H1_positive_stretching"] / base_q["H1_positive_stretching"] - 1
        )

    logC0 = np.log(base_q["C_infinity_stretch"])
    gain_old = np.log(endpoints["old_core_only"]["C_infinity_stretch"]) - logC0
    gain_new = np.log(endpoints["new_shell_only"]["C_infinity_stretch"]) - logC0
    gain_full = np.log(endpoints["full"]["C_infinity_stretch"]) - logC0

    synergy = {
        "log_gain_old": float(gain_old),
        "log_gain_new": float(gain_new),
        "log_gain_full": float(gain_full),
        "log_interaction": float(gain_full - gain_old - gain_new),
    }

    return {
        "status": "executed N11 phase-path and block-decomposition audit",
        "source": str(path_in),
        "active_pairs": len(pairs),
        "old_core_pairs": int(old_mask.sum()),
        "new_shell_pairs": int(new_mask.sum()),
        "path_grid": int(path_grid),
        "refine_grid": int(refine_grid),
        "lambdas": [float(x) for x in lambdas],
        "phase_delta": {
            "mean_abs_old_core": float(np.mean(np.abs(delta[old_mask]))),
            "mean_abs_new_shell": float(np.mean(np.abs(delta[new_mask]))),
            "median_abs_old_core": float(np.median(np.abs(delta[old_mask]))),
            "median_abs_new_shell": float(np.median(np.abs(delta[new_mask]))),
        },
        "paths": paths,
        "refined_endpoints": endpoints,
        "log_gain_decomposition": synergy,
        "interpretation_rule": (
            "Block and path effects are finite-state diagnostics. They do not "
            "establish a general variational law or asymptotic theorem."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("continuation_json", type=Path)
    p.add_argument("--path-grid", type=int, default=48)
    p.add_argument("--refine-grid", type=int, default=96)
    p.add_argument("--nsteps", type=int, default=11)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/"
            "wp16_phase_path_block_decomposition_results.json"
        ),
    )
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        args.continuation_json,
        args.path_grid,
        args.refine_grid,
        args.nsteps,
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
