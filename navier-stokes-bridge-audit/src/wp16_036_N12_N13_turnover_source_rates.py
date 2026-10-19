"""Post-hoc source-resolved N12/N13 K36 turnover audit.

Reconstructs the frozen N12/N13 finite-Galerkin states, samples t=0 and
t=0.001, differentiates each ordered source-orbit absolute contribution
along the exact finite-dimensional RHS, and attributes

    F = I - 9 O,    F' = I' - 9 O'.

This is mechanism analysis after the prospective holdouts. It never searches,
retunes K36, or changes any archived prospective result.
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
    "n10_n11": "34a10cf119ab6614c46d29540c4d4701eab082229582fb0a8189add0cd8f96a5",
    "n12": "ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855",
    "n13": "13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd",
    "source": "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e",
}
DT = 1e-4
H = 1e-8
SAMPLE_STEPS = (0, 10)
STABILITY_H = (5e-9, 1e-8, 2e-8)
N16_RECURRENT = ((3, 3, 4), (0, 2, 3))


def read_checked(path, kind):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED[kind]:
        raise ValueError(f"{kind} byte hash mismatch: {actual}")
    return json.loads(raw)


def grouped(system, a):
    pi, qi, ki = (system.index[x] for x in (hold.P, hold.Q, hold.K))
    q = np.asarray(hold.Q, float)
    projector = system.projectors[ki]
    weight = float(system.square[ki] ** 2)
    b = projector @ (1j * np.dot(q, a[pi]) * a[qi])
    z = -weight * np.vdot(a[ki], b)
    if abs(z) < 1e-30:
        raise ValueError("tracked complex normalizer vanished")

    groups = defaultdict(float)
    for li, ri, dak in hold.source_terms_for_output(system, a, ki):
        dz = -weight * np.vdot(dak, b)
        value = float(np.imag(dz / z))
        key = (hold.orbit(system.modes[li]), hold.orbit(system.modes[ri]))
        groups[key] += value
    return dict(groups), z


def source_rates(system, a, keys, h):
    velocity = system.rhs(a)
    gm, _ = grouped(system, a - h * velocity)
    g0, z0 = grouped(system, a)
    gp, _ = grouped(system, a + h * velocity)

    rows = []
    for key in sorted(set(gm) | set(g0) | set(gp)):
        vm = abs(gm.get(key, 0.0))
        v0 = abs(g0.get(key, 0.0))
        vp = abs(gp.get(key, 0.0))
        rows.append({
            "left": list(key[0]),
            "right": list(key[1]),
            "in_K36": key in keys,
            "value": float(g0.get(key, 0.0)),
            "abs_mass": float(v0),
            "rate": float((vp - vm) / (2 * h)),
        })

    inside = [r for r in rows if r["in_K36"]]
    outside = [r for r in rows if not r["in_K36"]]
    I = sum(r["abs_mass"] for r in inside)
    O = sum(r["abs_mass"] for r in outside)
    I_rate = sum(r["rate"] for r in inside)
    O_rate = sum(r["rate"] for r in outside)
    return rows, {
        "I": I,
        "O": O,
        "F": I - 9 * O,
        "I_rate": I_rate,
        "O_rate": O_rate,
        "F_rate": I_rate - 9 * O_rate,
        "z": [float(z0.real), float(z0.imag)],
    }


def advance(system, a, steps):
    out = a.copy()
    for _ in range(steps):
        out = system.rk4(out, DT)
    return out


def recurrent_record(rows):
    for r in rows:
        if (tuple(r["left"]), tuple(r["right"])) == N16_RECURRENT:
            return r
    raise AssertionError("recurrent N16 orbit missing")


def run(args):
    j11 = read_checked(args.n10_n11, "n10_n11")
    j12 = read_checked(args.n12, "n12")
    j13 = read_checked(args.n13, "n13")
    source = read_checked(args.source, "source")
    keys = set(hold.frozen_keys(source))
    if len(keys) != 36:
        raise AssertionError("frozen K36 size changed")

    hold.System = DealiasedSystem
    result = {
        "status": "post-hoc finite N12/N13 source-resolved K36 turnover audit; no retuning",
        "inputs_sha256": EXPECTED,
        "dt": DT,
        "directional_difference_h": H,
        "rate_definition": (
            "central directional difference of each ordered source-orbit absolute "
            "normalized contribution along the exact finite Galerkin RHS; I_rate "
            "and O_rate sum group rates; F_rate=I_rate-9*O_rate"
        ),
        "snapshots": {},
    }

    top10_frequency = defaultdict(int)
    top10_rate_sum = defaultdict(float)

    for N, prev, curr in (
        (12, hold.get_row(j11, 11), hold.get_row(j12, 12)),
        (13, hold.get_row(j12, 12), hold.get_row(j13, 13)),
    ):
        system, states = hold.reconstruct(prev, curr)
        for name, a0 in states.items():
            for step in SAMPLE_STEPS:
                a = advance(system, a0, step)
                rows, aggregate = source_rates(system, a, keys, H)
                outside = sorted(
                    (r for r in rows if not r["in_K36"]),
                    key=lambda r: r["rate"],
                    reverse=True,
                )
                recurrent = recurrent_record(rows)
                tag = f"N{N}/{name}/t={step*DT:.4f}"
                result["snapshots"][tag] = {
                    **aggregate,
                    "top5_outside_growth": outside[:5],
                    "recurrent_N16_orbit": recurrent,
                }
                for r in outside[:10]:
                    key = (tuple(r["left"]), tuple(r["right"]))
                    top10_frequency[key] += 1
                    top10_rate_sum[key] += r["rate"]
                print(tag, "F'", aggregate["F_rate"], "I'", aggregate["I_rate"],
                      "O'", aggregate["O_rate"], flush=True)

    # Three-step finite-difference stability check requested before formalization.
    sys13, states13 = hold.reconstruct(hold.get_row(j12, 12), hold.get_row(j13, 13))
    stability = {}
    for h in STABILITY_H:
        _, aggregate = source_rates(sys13, states13["inherited"], keys, h)
        stability[str(h)] = aggregate
    result["stability_check_N13_inherited_t0"] = stability

    freq_rows = [
        {
            "left": list(k[0]),
            "right": list(k[1]),
            "top10_count": count,
            "summed_rate_when_top10": top10_rate_sum[k],
        }
        for k, count in top10_frequency.items()
    ]
    freq_rows.sort(key=lambda r: (-r["top10_count"], -r["summed_rate_when_top10"]))
    result["cross_snapshot_top10_frequency"] = freq_rows[:15]
    result["recurrent_N16_attribution_orbit"] = {
        "left": list(N16_RECURRENT[0]),
        "right": list(N16_RECURRENT[1]),
        "N16_context": (
            "same ordered orbit is the largest outside-mass decrease in the "
            "post-hoc N16 full_final-minus-inherited comparison at t=0.0023; "
            "that comparison is a state-difference attribution, not a time derivative"
        ),
    }
    result["interpretation_rule"] = (
        "post-hoc finite-cutoff mechanism diagnostic only; frozen K36 is unchanged; "
        "repeated orbit identity is descriptive and does not establish a uniform "
        "source law or continuum bound"
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_name(args.output.name + ".tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    tmp.replace(args.output)


def main():
    p = argparse.ArgumentParser()
    for name in ("n10-n11", "n12", "n13", "source", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    run(p.parse_args())


if __name__ == "__main__":
    main()
