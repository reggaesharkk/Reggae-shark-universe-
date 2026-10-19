"""One-angle reduction audit for exact [223]+[123]->[036] separable motif.

Consumes wp16_036_exact_separable_variational_results.json and quantifies how
much of the isolated motif objective is carried by the dominant target pair
k=(6,0,3).

No new PDE simulation is run.
"""

import argparse
import json
from pathlib import Path

TARGET_K = (6, 0, 3)


def get_pair(step):
    for row in step["pairs"]:
        if tuple(row["representative_k"]) == TARGET_K:
            return row
    raise KeyError(f"target pair {TARGET_K} not found")


def run(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    out = {
        "status": "executed one-angle reduction audit",
        "target_pair_k": list(TARGET_K),
        "steps": {},
    }

    all_coeff_gt_099 = True
    all_available_gt_099 = True

    for name, step in payload["steps"].items():
        s = step["summary"]
        p = get_pair(step)

        coeff_share = p["C_abs"] / s["motif_F_exact_separable_optimum"]
        available_share = p["available_gain"] / s["available_motif_gain"]
        registered_gain_share = p["registered_gain"] / s["registered_motif_gain"]
        residual_registered_gain = s["registered_motif_gain"] - p["registered_gain"]

        row = {
            "dominant_pair": p,
            "coefficient_share_of_exact_motif_optimum": coeff_share,
            "available_gain_share": available_share,
            "registered_gain_share": registered_gain_share,
            "residual_11_pair_registered_gain": residual_registered_gain,
            "residual_opposes_dominant_gain": residual_registered_gain < 0,
        }
        out["steps"][name] = row

        all_coeff_gt_099 &= coeff_share > 0.99
        all_available_gt_099 &= available_share > 0.99

    out["all_three_coefficient_share_gt_99pct"] = all_coeff_gt_099
    out["all_three_available_gain_share_gt_99pct"] = all_available_gt_099
    out["interpretation_rule"] = (
        "This is an exact accounting identity within the isolated separable "
        "[223]+[123]->[036] motif. It does not imply one-angle reduction of "
        "the full phase objective or continuum dynamics."
    )
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--separable-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.separable_json)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\nONE-ANGLE REDUCTION AUDIT")
    print("=" * 72)
    for name, row in result["steps"].items():
        p = row["dominant_pair"]
        print("\n", name)
        print("k:", p["representative_k"])
        print("coefficient share:", row["coefficient_share_of_exact_motif_optimum"])
        print("available-gain share:", row["available_gain_share"])
        print("registered-gain share:", row["registered_gain_share"])
        print("residual 11-pair registered gain:", row["residual_11_pair_registered_gain"])
        print("distance:", p["distance_inherited_to_opt"], "->", p["distance_registered_to_opt"])
        print("pair gain captured:", p["fraction_available_gain_captured"])
    print("\nall coefficient shares >99%:", result["all_three_coefficient_share_gt_99pct"])
    print("all available-gain shares >99%:", result["all_three_available_gain_share_gt_99pct"])
    print("\nSAVED:", a.output)
