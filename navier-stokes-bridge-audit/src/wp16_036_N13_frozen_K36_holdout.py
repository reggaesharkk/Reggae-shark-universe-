"""Prospective N13 test of the unchanged N11-derived K36 k-channel coalition.

The inputs and pass criteria were frozen before N13 was generated. This is a
finite-cutoff descriptive holdout, not a continuum or all-N result.
"""

import argparse
import hashlib
import json
from pathlib import Path

from wp16_036_N12_frozen_K36_holdout import (
    PREFIX,
    evaluate_state,
    frozen_keys,
    get_row,
    reconstruct,
)


N12_SHA256 = "ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855"
SOURCE_SHA256 = "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e"


def checked_json(path, expected_sha256=None):
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if expected_sha256 is not None and actual != expected_sha256:
        raise ValueError(f"SHA-256 mismatch for {path}: {actual}")
    return json.loads(data), actual


def run(n12_path, n13_path, source_path):
    n12, n12_hash = checked_json(n12_path, N12_SHA256)
    n13, n13_hash = checked_json(n13_path)
    source, source_hash = checked_json(source_path, SOURCE_SHA256)

    r12 = get_row(n12, 12)
    r13 = get_row(n13, 13)
    if n13.get("resume_from_N") != 12 or n13.get("cutoffs") != [13]:
        raise ValueError("N13 JSON must be the single-step continuation from N12")

    keys = frozen_keys(source)
    if len(keys) != PREFIX or len(set(keys)) != PREFIX:
        raise ValueError("frozen N11 ranking did not yield 36 unique keys")

    system, states = reconstruct(r12, r13)
    evaluated = {
        name: evaluate_state(system, state, keys)
        for name, state in states.items()
    }
    if set(evaluated) != {"inherited", "target_only", "full_final"}:
        raise AssertionError("unexpected N13 state set")

    return {
        "status": "executed prospective N13 frozen K36 k-channel holdout",
        "N": 13,
        "source_coalition": "N11_from_N10 target_only first 36 absolute-ranked ordered source-orbit groups",
        "frozen_prefix_size": PREFIX,
        "input_sha256": {
            "n12_continuation": n12_hash,
            "n13_continuation": n13_hash,
            "n11_source_ranking": source_hash,
        },
        "criteria": {
            "same_sign": True,
            "minimum_absolute_mass_fraction": 0.90,
            "signed_share_interval": [0.80, 1.20],
        },
        "states": evaluated,
        "all_three_states_pass": all(
            result["passes_preregistered_consistency_criteria"]
            for result in evaluated.values()
        ),
        "interpretation_rule": (
            "One additional finite-cutoff holdout of a coalition frozen at N11. "
            "Passing does not establish all-N persistence or continuum phase dynamics; "
            "failure is retained without retuning K36 or its thresholds."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n12-json", type=Path, required=True)
    p.add_argument("--n13-json", type=Path, required=True)
    p.add_argument("--source-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.n12_json, a.n13_json, a.source_json)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\nN13 FROZEN K36 HOLDOUT")
    print("=" * 72)
    for name, row in result["states"].items():
        print(
            name,
            "signed_share=", row["signed_share_of_channel_total"],
            "abs_fraction=", row["absolute_mass_fraction"],
            "same_sign=", row["same_sign_as_channel_total"],
            "PASS=", row["passes_preregistered_consistency_criteria"],
        )
    print("ALL THREE PASS:", result["all_three_states_pass"])
    print("SAVED:", a.output)
