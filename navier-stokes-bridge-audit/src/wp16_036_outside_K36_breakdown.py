"""Descriptive per-key k-channel source breakdown for completed N12/N13 states."""

import argparse
import hashlib
import json
from pathlib import Path

from wp16_036_N12_frozen_K36_holdout import (
    frozen_keys, get_row, k_channel_grouped, reconstruct,
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_for_state(system, state, keys, stored):
    groups, total, absolute = k_channel_grouped(system, state)
    inside = sum(groups.get(k, 0.0) for k in keys)
    inside_abs = sum(abs(groups.get(k, 0.0)) for k in keys)
    assert abs(total - stored["k_channel_total_signed"]) < 1e-9
    assert abs(absolute - stored["k_channel_total_abs_group_contribution"]) < 1e-9
    assert abs(inside - stored["frozen_K36_signed_contribution"]) < 1e-9
    assert abs(inside_abs - stored["absolute_mass_captured"]) < 1e-9

    outside = sorted(
        ((k, v) for k, v in groups.items() if k not in keys),
        key=lambda kv: (-abs(kv[1]), kv[0]),
    )
    rows = [
        {"left_orbit": list(k[0]), "right_orbit": list(k[1]), "alpha_dot_contribution": v}
        for k, v in outside
    ]
    pos = sum(v for _, v in outside if v > 0)
    neg = sum(v for _, v in outside if v < 0)
    outside_abs = sum(abs(v) for _, v in outside)
    return {
        "group_count_total": len(groups),
        "group_count_outside": len(outside),
        "total_signed": total,
        "K36_signed": inside,
        "outside_signed": total - inside,
        "outside_positive_sum": pos,
        "outside_negative_sum": neg,
        "outside_absolute_mass": outside_abs,
        "top_5_outside_absolute_fraction": sum(abs(v) for _, v in outside[:5]) / outside_abs,
        "top_10_outside_absolute_fraction": sum(abs(v) for _, v in outside[:10]) / outside_abs,
        "outside_groups_ranked_by_absolute_contribution": rows,
    }


def main():
    p = argparse.ArgumentParser()
    for name in ("n11-json", "n12-json", "n13-json", "source-json", "n12-holdout-json", "n13-holdout-json", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    n11 = json.loads(a.n11_json.read_text())
    n12 = json.loads(a.n12_json.read_text())
    n13 = json.loads(a.n13_json.read_text())
    src = json.loads(a.source_json.read_text())
    holdouts = {
        12: json.loads(a.n12_holdout_json.read_text()),
        13: json.loads(a.n13_holdout_json.read_text()),
    }
    keys = frozen_keys(src)
    result = {
        "status": "post-hoc descriptive outside-K36 breakdown; no change to frozen gate",
        "input_sha256": {name: sha(getattr(a, name.replace('-', '_'))) for name in
                         ("n11-json", "n12-json", "n13-json", "source-json", "n12-holdout-json", "n13-holdout-json")},
        "N": {},
    }
    for N, prev, curr in ((12, get_row(n11, 11), get_row(n12, 12)),
                          (13, get_row(n12, 12), get_row(n13, 13))):
        print("RECONSTRUCT", N, flush=True)
        system, states = reconstruct(prev, curr)
        result["N"][str(N)] = {}
        for name, state in states.items():
            print("GROUP", N, name, flush=True)
            result["N"][str(N)][name] = rows_for_state(system, state, set(keys), holdouts[N]["states"][name])
            print("OUTSIDE", N, name, result["N"][str(N)][name]["outside_signed"], flush=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print("SAVED", a.output, flush=True)


if __name__ == "__main__":
    main()
