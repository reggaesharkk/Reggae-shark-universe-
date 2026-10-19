"""Conjugate-triad-pair reduction for the dominant k=(6,0,3) angle.

Consumes the exact phase-condition result and isolates the four exact ordered
motif terms belonging to the target conjugate output pair k=±(6,0,3).

The four terms are grouped into conjugate pairs:
    (p,q,k) ~ (-p,-q,-k)

For each step, report coefficient envelope and signed-transfer gain by conjugate
pair and test whether one conjugate pair dominates.

No new PDE simulation is run.
"""

import argparse
import json
from pathlib import Path


TARGET_K = (6, 0, 3)


def neg(v):
    return tuple(-int(x) for x in v)


def triple_key(row):
    p = tuple(int(x) for x in row["p"])
    q = tuple(int(x) for x in row["q"])
    k = tuple(int(x) for x in row["k"])
    a = p + q + k
    b = neg(p) + neg(q) + neg(k)
    return min(a, b)


def is_target_k(k):
    k = tuple(int(x) for x in k)
    return k == TARGET_K or k == neg(TARGET_K)


def run(path):
    payload = json.loads(path.read_text(encoding="utf-8"))

    result = {
        "status": "executed dominant conjugate-triad-pair reduction",
        "target_k_pair": [list(TARGET_K), list(neg(TARGET_K))],
        "steps": {},
    }

    all_two_classes = True
    all_dominant_A_gt_099999 = True

    for step_name, step in payload["steps"].items():
        rows = [r for r in step["all_exact_triads"] if is_target_k(r["k"])]
        if len(rows) != 4:
            raise AssertionError(
                f"{step_name}: expected 4 exact terms for ±{TARGET_K}, got {len(rows)}"
            )

        groups = {}
        for row in rows:
            key = triple_key(row)
            g = groups.setdefault(
                key,
                {
                    "canonical_flat": list(key),
                    "count": 0,
                    "A": 0.0,
                    "N_before": 0.0,
                    "N_after": 0.0,
                    "terms": [],
                },
            )
            g["count"] += 1
            g["A"] += float(row["A"])
            g["N_before"] += float(row["N_before"])
            g["N_after"] += float(row["N_after"])
            g["terms"].append(row)

        classes = []
        total_A = sum(g["A"] for g in groups.values())
        total_before = sum(g["N_before"] for g in groups.values())
        total_after = sum(g["N_after"] for g in groups.values())
        total_gain = total_after - total_before

        for g in groups.values():
            g["delta_N"] = g["N_after"] - g["N_before"]
            g["A_share"] = g["A"] / total_A if total_A else 0.0
            g["gain_share"] = (
                g["delta_N"] / total_gain if abs(total_gain) > 1e-30 else None
            )
            classes.append(g)

        classes.sort(key=lambda g: g["A"], reverse=True)
        dominant = classes[0]

        result["steps"][step_name] = {
            "exact_term_count": len(rows),
            "conjugate_pair_class_count": len(classes),
            "total": {
                "A": total_A,
                "N_before": total_before,
                "N_after": total_after,
                "delta_N": total_gain,
            },
            "classes": classes,
            "dominant_class": dominant,
            "dominant_A_share": dominant["A_share"],
            "dominant_gain_share": dominant["gain_share"],
        }

        all_two_classes &= len(classes) == 2
        all_dominant_A_gt_099999 &= dominant["A_share"] > 0.99999

    result["all_three_have_two_conjugate_pair_classes"] = all_two_classes
    result["all_three_dominant_A_share_gt_99p999pct"] = all_dominant_A_gt_099999
    result["interpretation_rule"] = (
        "This is exact accounting within the isolated finite motif and one "
        "target conjugate phase pair. Dominance does not imply an all-cutoff "
        "or continuum one-triad reduction."
    )
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--phase-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.phase_json)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\nDOMINANT CONJUGATE-TRIAD-PAIR REDUCTION")
    print("=" * 78)
    for name, step in result["steps"].items():
        print("\n", name)
        print("exact terms:", step["exact_term_count"])
        print("conjugate-pair classes:", step["conjugate_pair_class_count"])
        for i, c in enumerate(step["classes"], 1):
            print(
                i,
                "count=", c["count"],
                "A=", c["A"],
                "Ashare=", c["A_share"],
                "deltaN=", c["delta_N"],
                "gainshare=", c["gain_share"],
                "canon=", c["canonical_flat"],
            )
    print(
        "\nall three dominant A shares >99.999%:",
        result["all_three_dominant_A_share_gt_99p999pct"],
    )
    print("\nSAVED:", a.output)
