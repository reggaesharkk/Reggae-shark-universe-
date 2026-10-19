"""Post-hoc N16 source-orbit attribution of the extra sampled K36 step.

Reconstructs two original finite-Galerkin states; never searches or retunes.
The two-factor swap is algebraic counterfactual bookkeeping, not a PDE flow.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

EXPECTED = {
    "n15": "c0bd97f554df3e8561d75e1ba62356d04200fbe4986f573e3305a98932ccb225",
    "n16": "53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca",
    "time_gate": "111eb0407c60cb60c24c57e3c471ece05a9e1b94b88628a688d015a4249decf7",
    "frozen_keys": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
}
TIMES = (0, 10, 11, 20, 22, 23, 24)


def read_checked(path, kind):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED[kind]:
        raise ValueError(f"{kind} byte hash mismatch: {actual}")
    return json.loads(raw)


def keys_from_freeze(path):
    source = read_checked(path, "frozen_keys")
    assert source["source_original_sha256"] == "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e"
    keys = [(tuple(row["left_orbit"]), tuple(row["right_orbit"])) for row in source["keys"]]
    assert len(keys) == len(set(keys)) == 36
    return set(keys)


def complex_groups(system, a):
    pi, qi, ki = (system.index[x] for x in (hold.P, hold.Q, hold.K))
    q = np.asarray(hold.Q, float)
    projector = system.projectors[ki]
    weight = float(system.square[ki] ** 2)
    b = projector @ (1j * np.dot(q, a[pi]) * a[qi])
    z = -weight * np.vdot(a[ki], b)
    if abs(z) < 1e-30:
        raise ValueError("tracked normalizer vanished")
    grouped = defaultdict(complex)
    for li, ri, dak in hold.source_terms_for_output(system, a, ki):
        key = (hold.orbit(system.modes[li]), hold.orbit(system.modes[ri]))
        grouped[key] += -weight * np.vdot(dak, b)
    return dict(grouped), z


def signed_mass(c, z):
    return float(np.imag(c / z))


def snapshot(system, a, keys, archived):
    groups, z = complex_groups(system, a)
    inside = sum(abs(signed_mass(c, z)) for k, c in groups.items() if k in keys)
    outside = sum(abs(signed_mass(c, z)) for k, c in groups.items() if k not in keys)
    signed = sum(signed_mass(c, z) for c in groups.values())
    for actual, target in (
        (inside, archived["absolute_mass_captured"]),
        (inside + outside, archived["k_channel_total_abs_group_contribution"]),
        (signed, archived["k_channel_total_signed"]),
    ):
        if abs(actual - target) > 2e-7:
            raise AssertionError((actual, target, actual-target))
    return groups, z, inside, outside


def contributions(h, f, keys):
    gh, zh, ih, oh = h
    gf, zf, iff, of = f
    rows = []
    for key in sorted(set(gh) | set(gf)):
        ch, cf = gh.get(key, 0j), gf.get(key, 0j)
        aa = abs(signed_mass(ch, zh))
        bb = abs(signed_mass(cf, zh))
        cc = abs(signed_mass(ch, zf))
        dd = abs(signed_mass(cf, zf))
        numerator = ((bb-aa)+(dd-cc))/2
        normalizer = ((cc-aa)+(dd-bb))/2
        delta = dd-aa
        assert abs(delta-numerator-normalizer) < 1e-11
        rows.append({
            "left_orbit": list(key[0]), "right_orbit": list(key[1]),
            "in_K36": key in keys,
            "inherited_value": signed_mass(ch, zh),
            "full_final_value": signed_mass(cf, zf),
            "delta_absolute_mass": delta,
            "complex_numerator_swap": numerator,
            "tracked_normalizer_swap": normalizer,
        })
    in_rows = [r for r in rows if r["in_K36"]]
    out_rows = [r for r in rows if not r["in_K36"]]
    assert abs(sum(r["delta_absolute_mass"] for r in in_rows)-(iff-ih)) < 1e-7
    assert abs(sum(r["delta_absolute_mass"] for r in out_rows)-(of-oh)) < 1e-7
    out_rows.sort(key=lambda r: r["delta_absolute_mass"])
    return {
        "inherited_z": [float(zh.real), float(zh.imag)],
        "full_final_z": [float(zf.real), float(zf.imag)],
        "normalizer_magnitude_ratio_full_over_inherited": float(abs(zf)/abs(zh)),
        "normalizer_relative_phase_radians": float(np.angle(zf/zh)),
        "inherited_I": ih, "inherited_O": oh,
        "full_final_I": iff, "full_final_O": of,
        "delta_I": iff-ih, "delta_O": of-oh,
        "inside_complex_numerator_swap": sum(r["complex_numerator_swap"] for r in in_rows),
        "inside_tracked_normalizer_swap": sum(r["tracked_normalizer_swap"] for r in in_rows),
        "outside_complex_numerator_swap": sum(r["complex_numerator_swap"] for r in out_rows),
        "outside_tracked_normalizer_swap": sum(r["tracked_normalizer_swap"] for r in out_rows),
        "outside_group_count": len(out_rows),
        "largest_outside_decreases": out_rows[:12],
        "largest_outside_increases": list(reversed(out_rows[-12:])),
        "top_12_decrease_sum": sum(r["delta_absolute_mass"] for r in out_rows[:12]),
        "remaining_outside_sum": sum(r["delta_absolute_mass"] for r in out_rows[12:]),
    }


def run(args):
    j15 = read_checked(args.n15, "n15")
    j16 = read_checked(args.n16, "n16")
    archived = read_checked(args.time_gate, "time_gate")
    keys = keys_from_freeze(args.frozen_keys)
    hold.System = DealiasedSystem
    system, states = hold.reconstruct(hold.get_row(j15, 15), hold.get_row(j16, 16))
    current = {name: states[name] for name in ("inherited", "full_final")}
    result = {
        "status": "post-hoc finite N16 source-orbit attribution; no prospective retuning",
        "sha256": EXPECTED,
        "key_source_original_sha256": "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e",
        "N": 16, "dt": archived["dt"], "samples": {},
        "swap_interpretation": "symmetric two-factor attribution of group absolute mass changes to complex group numerator versus tracked complex normalizer; algebraic counterfactual, not a causal flow",
    }
    for step in range(max(TIMES)+1):
        observed = {}
        for name in current:
            observed[name] = snapshot(system, current[name], keys, archived["states"][name]["samples"][step])
        if step in TIMES:
            result["samples"][str(step)] = contributions(observed["inherited"], observed["full_final"], keys)
            print("CHECKED", step, "delta_O", result["samples"][str(step)]["delta_O"], flush=True)
        if step < max(TIMES):
            for name in current:
                current[name] = system.rk4(current[name], archived["dt"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_name(args.output.name+".tmp")
    temp.write_text(json.dumps(result, indent=2)+"\n")
    temp.replace(args.output)


def main():
    p = argparse.ArgumentParser()
    for name in ("n15", "n16", "time-gate", "frozen-keys", "output"):
        p.add_argument("--"+name, type=Path, required=True)
    run(p.parse_args())


if __name__ == "__main__":
    main()
