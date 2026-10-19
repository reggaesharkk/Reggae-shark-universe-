"""Resume the fixed N13 continuation after a Colab disconnect.

Replays RNG draws through the last processed trial without rescoring them,
then continues the original deterministic proposal sequence from the saved
best phase vector. Does not alter the objective, search settings, or K36 gate.
"""

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import active_pairs, base_state, evaluate, phase_rotate
from wp16_phase_cutoff_escalation import inherited_phases, normalized_angle


N12_SHA256 = "ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855"
SEED = 20260938
SEARCH_GRID = 40
NEW_GLOBAL_DRAWS = 16
NEW_BLOCK_ROUNDS = 3
FULL_BLOCK_ROUNDS = 4
BLOCK_TRIALS = 72
BLOCK_SIZE = 40
INITIAL_STEP = 0.30
TOTAL_TRIALS = NEW_GLOBAL_DRAWS + (NEW_BLOCK_ROUNDS + FULL_BLOCK_ROUNDS) * BLOCK_TRIALS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finest(row):
    if not row.get("refined"):
        return float(row["best_search_grid"]["C_infinity_stretch"])
    grid = max(map(int, row["refined"]))
    return float(row["refined"][str(grid)]["C_infinity_stretch"])


def consume_rng_through(rng, last_trial, new_idx, all_idx):
    """Advance the exact original draw stream without objective evaluations."""
    trial = 0
    for _ in range(NEW_GLOBAL_DRAWS):
        trial += 1
        rng.uniform(-math.pi, math.pi, size=len(new_idx))
        if trial == last_trial:
            return
    new_size = min(BLOCK_SIZE, len(new_idx))
    step = INITIAL_STEP
    for round_index in range(NEW_BLOCK_ROUNDS):
        for _ in range(BLOCK_TRIALS):
            trial += 1
            rng.choice(new_idx, size=new_size, replace=False)
            rng.normal(scale=step, size=new_size)
            if trial == last_trial:
                return
        step *= 0.6
    full_size = min(BLOCK_SIZE, len(all_idx))
    step = INITIAL_STEP
    for round_index in range(FULL_BLOCK_ROUNDS):
        for _ in range(BLOCK_TRIALS):
            trial += 1
            rng.choice(all_idx, size=full_size, replace=False)
            rng.normal(scale=step, size=full_size)
            if trial == last_trial:
                return
        step *= 0.6
    if last_trial != TOTAL_TRIALS:
        raise ValueError(f"last trial {last_trial} is outside the frozen schedule")


def run(n12_path, checkpoint_path, output_checkpoint_path, output_path):
    if digest(n12_path) != N12_SHA256:
        raise ValueError("N12 input SHA-256 differs from the frozen N13 gate")
    n12 = json.loads(n12_path.read_text(encoding="utf-8"))
    cp = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    checkpoint_sha256 = digest(checkpoint_path)
    if n12.get("cutoffs") != [12] or n12.get("resume_from_N") != 11:
        raise ValueError("N12 continuation structure changed")
    prev = n12["rows"][0]
    if int(prev["N"]) != 12:
        raise ValueError("N12 row missing")
    if cp.get("N") != 13 or cp.get("seed") != SEED or cp.get("search_grid") != SEARCH_GRID:
        raise ValueError("checkpoint configuration differs from the frozen N13 run")

    records = cp["records"]
    last_trial = int(cp.get("last_processed_trial", max(int(r["trial"]) for r in records)))
    if not (NEW_GLOBAL_DRAWS <= last_trial <= TOTAL_TRIALS):
        raise ValueError("checkpoint trial outside fixed N13 schedule")
    if max(int(r["trial"]) for r in records) > last_trial:
        raise ValueError("checkpoint records run beyond last processed trial")

    started = time.time()
    system = System(N=13, nu=NU)
    base = base_state(system, float(prev["amplitude"]), float(prev["anchor_time"]))
    pairs = active_pairs(system, base)
    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }
    phases0, inherited = inherited_phases(pairs, prev_map)
    new_idx = np.flatnonzero(~inherited)
    all_idx = np.arange(len(pairs))
    if (
        len(pairs) != cp["active_conjugate_pairs"]
        or int(inherited.sum()) != cp["inherited_pairs"]
        or len(new_idx) != cp["new_pairs"]
    ):
        raise ValueError("reconstructed support differs from checkpoint")

    best = cp["best"]
    best_phases = np.asarray(cp["best_phases"], dtype=float)
    if len(best_phases) != len(pairs):
        raise ValueError("checkpoint phase vector has wrong length")
    if float(best["C_infinity_stretch"]) != max(
        float(r["C_infinity_stretch"]) for r in records
    ):
        raise ValueError("checkpoint best disagrees with accepted records")

    rng = np.random.default_rng(SEED)
    consume_rng_through(rng, last_trial, new_idx, all_idx)
    print(f"RECOVERED: N=13, last trial={last_trial}/{TOTAL_TRIALS}, best C={best['C_infinity_stretch']:.9f}", flush=True)

    def save_checkpoint(trial):
        payload = {
            "N": 13,
            "seed": SEED,
            "active_conjugate_pairs": len(pairs),
            "inherited_pairs": int(inherited.sum()),
            "new_pairs": len(new_idx),
            "search_grid": SEARCH_GRID,
            "best": best,
            "best_phases": best_phases.tolist(),
            "records": records,
            "last_processed_trial": trial,
            "elapsed_seconds": float(cp["elapsed_seconds"]) + time.time() - started,
            "recovery_input_sha256": checkpoint_sha256,
        }
        temporary = output_checkpoint_path.with_name(output_checkpoint_path.name + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output_checkpoint_path)

    def score(proposal):
        return evaluate(system, phase_rotate(base, pairs, proposal), grid=SEARCH_GRID)

    trial = last_trial
    if trial < NEW_GLOBAL_DRAWS:
        raise ValueError("global draw checkpoint unsupported")
    # The original checkpoint is at trial 200, inside the third new-mode round.
    # Support later recovery checkpoints in either block stage as well.
    step = INITIAL_STEP
    for round_index in range(NEW_BLOCK_ROUNDS):
        for j in range(BLOCK_TRIALS):
            scheduled = NEW_GLOBAL_DRAWS + round_index * BLOCK_TRIALS + j + 1
            if scheduled <= trial:
                continue
            idx = rng.choice(new_idx, size=min(BLOCK_SIZE, len(new_idx)), replace=False)
            proposal = best_phases.copy()
            proposal[idx] = normalized_angle(proposal[idx] + rng.normal(scale=step, size=len(idx)))
            q = score(proposal)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best, best_phases = q, proposal.copy()
                records.append(dict(kind="new_modes_block_best", trial=scheduled, round=round_index, step=step, **q))
            trial = scheduled
            if trial % 8 == 0:
                save_checkpoint(trial)
        if trial == NEW_GLOBAL_DRAWS + (round_index + 1) * BLOCK_TRIALS:
            print(f"N=13 new-round={round_index+1}/{NEW_BLOCK_ROUNDS} C={best['C_infinity_stretch']:.9f}", flush=True)
            save_checkpoint(trial)
        step *= 0.6

    step = INITIAL_STEP
    for round_index in range(FULL_BLOCK_ROUNDS):
        for j in range(BLOCK_TRIALS):
            scheduled = NEW_GLOBAL_DRAWS + NEW_BLOCK_ROUNDS * BLOCK_TRIALS + round_index * BLOCK_TRIALS + j + 1
            if scheduled <= trial:
                continue
            idx = rng.choice(all_idx, size=min(BLOCK_SIZE, len(all_idx)), replace=False)
            proposal = best_phases.copy()
            proposal[idx] = normalized_angle(proposal[idx] + rng.normal(scale=step, size=len(idx)))
            q = score(proposal)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best, best_phases = q, proposal.copy()
                records.append(dict(kind="full_block_best", trial=scheduled, round=round_index, step=step, **q))
            trial = scheduled
            if trial % 8 == 0:
                save_checkpoint(trial)
        if trial == NEW_GLOBAL_DRAWS + NEW_BLOCK_ROUNDS * BLOCK_TRIALS + (round_index + 1) * BLOCK_TRIALS:
            print(f"N=13 full-round={round_index+1}/{FULL_BLOCK_ROUNDS} C={best['C_infinity_stretch']:.9f}", flush=True)
            save_checkpoint(trial)
        step *= 0.6

    if trial != TOTAL_TRIALS:
        raise AssertionError("not all frozen candidate trials completed")

    baseline = evaluate(system, base, grid=SEARCH_GRID)
    continuation = score(phases0)
    for stored, computed in zip(records[:2], (baseline, continuation)):
        for key, value in computed.items():
            if not math.isclose(float(stored[key]), float(value), rel_tol=1e-12, abs_tol=1e-12):
                raise AssertionError(f"baseline / inheritance changed: {key}")

    refined = {}
    for grid in (32, 40, 48, 64, 96):
        if grid <= 3 * 13:
            continue
        refined[str(grid)] = evaluate(system, phase_rotate(base, pairs, best_phases), grid=grid)
        print(f"N=13 refine {grid}^3 C={refined[str(grid)]['C_infinity_stretch']:.9f}", flush=True)

    row = {
        "N": 13,
        "anchor_time": float(prev["anchor_time"]),
        "amplitude": float(prev["amplitude"]),
        "seed": SEED,
        "active_conjugate_pairs": len(pairs),
        "support_vectors": [list(k) for _, _, k in pairs],
        "inherited_pairs": int(inherited.sum()),
        "new_pairs": len(new_idx),
        "unrotated_baseline": baseline,
        "inherited_continuation": continuation,
        "best_search_grid": best,
        "best_phases": best_phases.tolist(),
        "refined": refined,
        "search": {
            "search_grid": SEARCH_GRID,
            "new_global_draws": NEW_GLOBAL_DRAWS,
            "new_block_rounds": NEW_BLOCK_ROUNDS,
            "full_block_rounds": FULL_BLOCK_ROUNDS,
            "block_trials": BLOCK_TRIALS,
            "block_size": BLOCK_SIZE,
            "initial_step": INITIAL_STEP,
        },
        "records": records,
        "elapsed_seconds": float(cp["elapsed_seconds"]) + time.time() - started,
        "recovery": {
            "method": "checkpoint best state plus deterministic RNG draw replay",
            "input_checkpoint_sha256": checkpoint_sha256,
            "initial_last_processed_trial": last_trial,
        },
    }
    result = {
        "status": "completed resumed WP16 phase-only cutoff escalation",
        "resume_source": str(n12_path),
        "resume_from_N": 12,
        "resume_from_refined_C": finest(prev),
        "cutoffs": [13],
        "anchor_time": row["anchor_time"],
        "rows": [row],
        "best_refined_case": {"N": 13, "C": finest(row)},
        "interpretation_rule": "Finite cutoff continuation only; this recovered run uses the unchanged deterministic proposal schedule.",
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    save_checkpoint(trial)
    print("N13 COMPLETE:", result["best_refined_case"], flush=True)
    print("SAVED:", output_path, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n12-json", type=Path, required=True)
    p.add_argument("--resume-checkpoint", type=Path, required=True)
    p.add_argument("--output-checkpoint", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise FileExistsError(a.output)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    run(a.n12_json, a.resume_checkpoint, a.output_checkpoint, a.output)
