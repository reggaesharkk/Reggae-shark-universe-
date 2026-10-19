"""WP16 phase-only cutoff escalation by deterministic continuation.

Purpose
-------
Test whether the refined WP16 evolved-spectrum phase-only quotient continues
to rise beyond N=7.  The N=7 optimized phases from the completed expanded
search are transferred mode-by-mode into N=8 and N=9. Newly active Fourier
pairs start at zero phase and are optimized first; the full phase torus is
then relaxed by deterministic block proposals.

This is a finite falsification search. It does not prove asymptotic growth,
a global optimum, or any Navier-Stokes regularity statement.
"""

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import (
    active_pairs,
    base_state,
    evaluate,
    phase_rotate,
)

DEFAULT_SOURCE = Path(
    "/content/drive/MyDrive/WP16_EXPANDED_RESULTS/"
    "wp16_expanded_phase_search_results.json"
)


def best_source_row(payload):
    rows = [
        r for r in payload["rows"]
        if int(r["N"]) == 7 and math.isclose(float(r["anchor_time"]), 0.005)
    ]
    if not rows:
        raise ValueError("source JSON has no N=7, t=0.005 row")
    return max(rows, key=lambda r: r["best"]["C_infinity_stretch"])


def source_phase_map(source_row):
    system = System(N=7, nu=NU)
    base = base_state(system, float(source_row["amplitude"]), 0.005)
    pairs = active_pairs(system, base)
    phases = np.asarray(source_row["best_phases"], float)
    if len(pairs) != len(phases):
        raise AssertionError("source active-pair/phase length mismatch")
    return {tuple(k): float(phi) for (_, _, k), phi in zip(pairs, phases)}


def inherited_phases(pairs, phase_map):
    phases = np.zeros(len(pairs), float)
    inherited = np.zeros(len(pairs), dtype=bool)
    for j, (_, _, k) in enumerate(pairs):
        if tuple(k) in phase_map:
            phases[j] = phase_map[tuple(k)]
            inherited[j] = True
    return phases, inherited


def normalized_angle(x):
    return np.angle(np.exp(1j * x))


def optimize_continuation(
    N,
    phase_map,
    amplitude,
    anchor_time,
    seed,
    search_grid,
    new_global_draws,
    new_block_rounds,
    full_block_rounds,
    block_trials,
    block_size,
    initial_step,
    checkpoint=None,
):
    t0 = time.time()
    system = System(N=N, nu=NU)
    base = base_state(system, amplitude, anchor_time)
    pairs = active_pairs(system, base)
    phases0, inherited = inherited_phases(pairs, phase_map)
    new_idx = np.flatnonzero(~inherited)
    all_idx = np.arange(len(pairs))
    rng = np.random.default_rng(seed)

    def score(phases):
        return evaluate(
            system,
            phase_rotate(base, pairs, phases),
            grid=search_grid,
        )

    baseline = evaluate(system, base, grid=search_grid)
    continuation = score(phases0)
    best = dict(continuation)
    best_phases = phases0.copy()
    records = [
        dict(kind="unrotated_baseline", trial=0, **baseline),
        dict(kind="inherited_continuation", trial=0, **continuation),
    ]
    trial = 0

    def maybe_save():
        if checkpoint is None:
            return
        payload = {
            "N": N,
            "seed": seed,
            "active_conjugate_pairs": len(pairs),
            "inherited_pairs": int(inherited.sum()),
            "new_pairs": int((~inherited).sum()),
            "search_grid": search_grid,
            "best": best,
            "best_phases": best_phases.tolist(),
            "records": records,
            "elapsed_seconds": time.time() - t0,
        }
        checkpoint.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    # Stage A: randomize only phases that are genuinely new at this cutoff.
    if len(new_idx):
        for draw in range(new_global_draws):
            trial += 1
            proposal = phases0.copy()
            proposal[new_idx] = rng.uniform(-math.pi, math.pi, size=len(new_idx))
            q = score(proposal)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_phases = proposal.copy()
                records.append(dict(kind="new_modes_global_best", trial=trial, **q))
                maybe_save()
                print(
                    f"N={N} new-global {draw+1}/{new_global_draws} "
                    f"C={best['C_infinity_stretch']:.9f}",
                    flush=True,
                )

    # Stage B: block-coordinate relaxation, new modes first.
    step = initial_step
    effective_new_block = max(1, min(block_size, len(new_idx))) if len(new_idx) else 0
    for round_index in range(new_block_rounds):
        if not len(new_idx):
            break
        improved = False
        for _ in range(block_trials):
            trial += 1
            proposal = best_phases.copy()
            idx = rng.choice(new_idx, size=effective_new_block, replace=False)
            proposal[idx] = normalized_angle(
                proposal[idx] + rng.normal(scale=step, size=len(idx))
            )
            q = score(proposal)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_phases = proposal.copy()
                improved = True
                records.append(dict(
                    kind="new_modes_block_best",
                    trial=trial,
                    round=round_index,
                    step=step,
                    **q,
                ))
                maybe_save()
        print(
            f"N={N} new-round={round_index+1}/{new_block_rounds} "
            f"step={step:.4f} C={best['C_infinity_stretch']:.9f}",
            flush=True,
        )
        step *= 0.6

    # Stage C: relax the entire active phase torus.
    step = initial_step
    effective_full_block = max(1, min(block_size, len(all_idx)))
    for round_index in range(full_block_rounds):
        for _ in range(block_trials):
            trial += 1
            proposal = best_phases.copy()
            idx = rng.choice(all_idx, size=effective_full_block, replace=False)
            proposal[idx] = normalized_angle(
                proposal[idx] + rng.normal(scale=step, size=len(idx))
            )
            q = score(proposal)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_phases = proposal.copy()
                records.append(dict(
                    kind="full_block_best",
                    trial=trial,
                    round=round_index,
                    step=step,
                    **q,
                ))
                maybe_save()
        print(
            f"N={N} full-round={round_index+1}/{full_block_rounds} "
            f"step={step:.4f} C={best['C_infinity_stretch']:.9f}",
            flush=True,
        )
        step *= 0.6

    refinements = {}
    for grid in (32, 40, 48, 64, 96):
        if grid <= 3 * N:
            continue
        refinements[str(grid)] = evaluate(
            system,
            phase_rotate(base, pairs, best_phases),
            grid=grid,
        )
        print(
            f"N={N} refine {grid}^3 "
            f"C={refinements[str(grid)]['C_infinity_stretch']:.9f}",
            flush=True,
        )

    result = {
        "N": N,
        "anchor_time": anchor_time,
        "amplitude": amplitude,
        "seed": seed,
        "active_conjugate_pairs": len(pairs),
        "support_vectors": [list(k) for _, _, k in pairs],
        "inherited_pairs": int(inherited.sum()),
        "new_pairs": int((~inherited).sum()),
        "unrotated_baseline": baseline,
        "inherited_continuation": continuation,
        "best_search_grid": best,
        "best_phases": best_phases.tolist(),
        "refined": refinements,
        "search": {
            "search_grid": search_grid,
            "new_global_draws": new_global_draws,
            "new_block_rounds": new_block_rounds,
            "full_block_rounds": full_block_rounds,
            "block_trials": block_trials,
            "block_size": block_size,
            "initial_step": initial_step,
        },
        "records": records,
        "elapsed_seconds": time.time() - t0,
    }
    maybe_save()
    return result


def run(args):
    source = json.loads(args.source_json.read_text(encoding="utf-8"))
    src = best_source_row(source)
    phase_map = source_phase_map(src)

    source_refined = 3.744126696758515
    rows = []
    for N in args.cutoffs:
        checkpoint = args.output.parent / f"wp16_cutoff_escalation_N{N}_checkpoint.json"
        row = optimize_continuation(
            N=N,
            phase_map=phase_map,
            amplitude=float(src["amplitude"]),
            anchor_time=0.005,
            seed=args.seed + N,
            search_grid=args.search_grid,
            new_global_draws=args.new_global_draws,
            new_block_rounds=args.new_block_rounds,
            full_block_rounds=args.full_block_rounds,
            block_trials=args.block_trials,
            block_size=args.block_size,
            initial_step=args.initial_step,
            checkpoint=checkpoint,
        )
        rows.append(row)
        # True continuation: the next cutoff inherits the optimized phases
        # from this cutoff mode-by-mode wherever the active support overlaps.
        phase_map = {
            tuple(k): float(phi)
            for k, phi in zip(row["support_vectors"], row["best_phases"])
        }

    def finest(row):
        if not row["refined"]:
            return row["best_search_grid"]["C_infinity_stretch"]
        g = max(map(int, row["refined"]))
        return row["refined"][str(g)]["C_infinity_stretch"]

    best_row = max(rows, key=finest)
    return {
        "status": "completed WP16 phase-only cutoff escalation",
        "source": {
            "path": str(args.source_json),
            "N7_search_best": float(src["best"]["C_infinity_stretch"]),
            "N7_refined_128": source_refined,
        },
        "cutoffs": list(args.cutoffs),
        "anchor_time": 0.005,
        "rows": rows,
        "best_refined_case": {
            "N": int(best_row["N"]),
            "C": float(finest(best_row)),
        },
        "interpretation_rule": (
            "Finite cutoff escalation only. Increasing values motivate further "
            "analytic/cutoff tests; saturation does not prove a universal bound."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source-json", type=Path, default=DEFAULT_SOURCE)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/"
                     "wp16_phase_cutoff_escalation_results.json"),
    )
    p.add_argument("--cutoffs", nargs="+", type=int, default=[8, 9])
    p.add_argument("--seed", type=int, default=20260925)
    p.add_argument("--search-grid", type=int, default=32)
    p.add_argument("--new-global-draws", type=int, default=24)
    p.add_argument("--new-block-rounds", type=int, default=3)
    p.add_argument("--full-block-rounds", type=int, default=4)
    p.add_argument("--block-trials", type=int, default=96)
    p.add_argument("--block-size", type=int, default=32)
    p.add_argument("--initial-step", type=float, default=0.35)
    args = p.parse_args()

    if args.search_grid <= 3 * max(args.cutoffs):
        raise ValueError("search grid must exceed 3*max(cutoffs)")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(args)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("\nFINAL", json.dumps({
        "best_refined_case": result["best_refined_case"],
        "output": str(args.output),
    }, indent=2))
