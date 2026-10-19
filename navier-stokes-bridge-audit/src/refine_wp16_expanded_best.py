"""Refine the fixed best state from a completed WP16 expanded search.

Usage:
    python src/refine_wp16_expanded_best.py /path/to/wp16_expanded_phase_search_results.json

The script does not re-optimize phases. It reconstructs the registered evolved
anchor, applies the stored best phase vector, and reevaluates the same state on
finer physical grids.

Finite-family diagnostic only.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from wp16_expanded_phase_search import (
    active_pairs,
    base_state,
    evaluate,
    phase_rotate,
)
from phase_cascade_trajectory import NU


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def select_best(payload):
    return max(
        payload["rows"],
        key=lambda r: r["best"]["C_infinity_stretch"],
    )


def run(path, grids=(24, 32, 48, 64, 96, 128)):
    payload = json.loads(path.read_text(encoding="utf-8"))
    row = select_best(payload)

    N = int(row["N"])
    anchor_time = float(row["anchor_time"])
    amplitude = float(row["amplitude"])
    phases = np.asarray(row["best_phases"], float)

    system = System(N=N, nu=NU)
    base = base_state(system, amplitude, anchor_time)
    pairs = active_pairs(system, base)

    if len(pairs) != len(phases):
        raise AssertionError(
            f"active pair count mismatch: {len(pairs)} != {len(phases)}"
        )

    state = phase_rotate(base, pairs, phases)

    refinement = []
    for grid in grids:
        q = evaluate(system, state, grid=grid)
        refinement.append(dict(grid=int(grid), **q))

    return {
        "status": "fixed-state WP16 expanded phase-only grid refinement",
        "source_file": path.name,
        "source_sha256": sha256(path),
        "selected_case": {
            "N": N,
            "anchor_time": anchor_time,
            "seed": int(row["seed"]),
            "active_conjugate_pairs": int(row["active_conjugate_pairs"]),
            "search_grid": int(row["search"]["grid"]),
            "search_best": float(row["best"]["C_infinity_stretch"]),
        },
        "refinement": refinement,
        "warning": (
            "No phase re-optimization is performed. This is a fixed-state "
            "physical-grid refinement of one finite optimized state only."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("results_json", type=Path)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("wp16_expanded_refinement_results.json"),
    )
    a = p.parse_args()

    result = run(a.results_json)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
