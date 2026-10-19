"""Post-hoc, algebraic accounting of the frozen N16 K36 mass exit.

Consumes the original time-gate JSON; does not reconstruct states or optimize.
Every reported rate is a sample-to-sample secant, not a PDE derivative.
"""

import argparse
import hashlib
import json
from pathlib import Path


SOURCE_SHA256 = "111eb0407c60cb60c24c57e3c471ece05a9e1b94b88628a688d015a4249decf7"
STATES = ("inherited", "target_only", "full_final")


def mass(row):
    inside = row["absolute_mass_captured"]
    outside = row["k_channel_total_abs_group_contribution"] - inside
    return inside, outside, inside - 9 * outside


def checked_rows(data):
    assert data["dt"] == 0.0001 and data["steps"] == 30
    assert data["criteria"]["minimum_absolute_mass_fraction"] == 0.9
    result = {}
    for name in STATES:
        state = data["states"][name]
        rows = state["samples"]
        assert len(rows) == 31
        for i, row in enumerate(rows):
            inside, outside, margin = mass(row)
            assert inside > 0 and outside > 0
            assert abs(row["time_after_anchor"] - i * data["dt"]) < 1e-12
            assert abs(margin - row["K36_mass_margin"]) < 1e-8
            assert abs(inside / (inside + outside) - row["absolute_mass_fraction"]) < 1e-12
            assert (margin >= -1e-10) == row["mass_gate_pass"]
        assert state["first_mass_failure_index"] == next(
            (i for i, row in enumerate(rows) if not row["mass_gate_pass"]), None
        )
        result[name] = rows
    return result


def summarize(data):
    rows = checked_rows(data)
    out = {
        "status": "post-hoc descriptive N16 exit accounting; frozen result unmodified",
        "input_sha256": SOURCE_SHA256,
        "identity": "F=I-9O; 90% gate iff F>=0",
        "states": {},
    }
    for name, samples in rows.items():
        values = [mass(row) for row in samples]
        peak = max(range(len(values)), key=lambda i: values[i][2])
        first_negative_secant = next(
            i for i in range(1, len(values)) if values[i][2] - values[i-1][2] < 0
        )
        exit_index = data["states"][name]["first_mass_failure_index"]
        i0, o0, f0 = values[0]
        ie, oe, fe = values[exit_index]
        out["states"][name] = {
            "peak_margin_index": peak,
            "peak_margin": values[peak][2],
            "first_negative_margin_secant_interval_indices": [first_negative_secant-1, first_negative_secant],
            "exit_index": exit_index,
            "anchor": {"I": i0, "O": o0, "F": f0},
            "exit": {"I": ie, "O": oe, "F": fe},
            "anchor_to_exit_change": {"delta_I": ie-i0, "delta_O": oe-o0, "delta_F": fe-f0},
            "last_passing_F": values[exit_index-1][2],
            "exit_step_change": {
                "delta_I": ie-values[exit_index-1][0],
                "delta_O": oe-values[exit_index-1][1],
                "delta_F": fe-values[exit_index-1][2],
            },
        }

    reference = [mass(r) for r in rows["inherited"]]
    final = [mass(r) for r in rows["full_final"]]
    contrasts = []
    for index, (base, optimized) in enumerate(zip(reference, final)):
        di = optimized[0]-base[0]
        do = optimized[1]-base[1]
        df = optimized[2]-base[2]
        assert abs(df - (di-9*do)) < 1e-8
        contrasts.append((di, do, df))
    first_o_advantage = next(i for i, (_, do, _) in enumerate(contrasts) if do < 0)
    first_f_advantage = next(i for i, (_, _, df) in enumerate(contrasts) if df > 0)
    out["full_final_minus_inherited"] = {
        "first_outside_mass_advantage_index": first_o_advantage,
        "first_margin_advantage_index": first_f_advantage,
        "selected_indices": {},
    }
    for index in (0, 10, 11, 15, 20, 22, 23, 24, 30):
        di, do, df = contrasts[index]
        out["full_final_minus_inherited"]["selected_indices"][str(index)] = {
            "delta_I": di, "delta_O": do, "outside_suppression_gain": -9*do,
            "delta_F": df,
            "full_final_F": final[index][2],
            "inherited_F": reference[index][2],
        }
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--time-gate", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    raw = args.time_gate.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("N16 frozen time-gate byte hash mismatch")
    result = summarize(json.loads(raw))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
