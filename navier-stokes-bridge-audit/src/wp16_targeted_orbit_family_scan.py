"""Targeted three-step orbit-family scan for WP16.

Primary preregistered family:
    [0,3,m]

Matched nearby control families:
    [0,2,m], [0,4,m], [1,3,m]

Steps:
    N8 -> N9
    N9 -> N10
    N10 -> N11

For each family member that belongs to the inherited support at a step, apply
epsilon times its registered wrapped old-core phase correction and measure
    dlogN, -dlogPplus, dlogC.

Also evaluate the full registered orbit correction at that step.

The purpose is to test whether [0,3,m] forms a coherent recurring family and,
in particular, whether [0,3,9] becomes favorable when it first becomes
available in the inherited N10 support for the N10->N11 step.

Finite diagnostic only.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict
import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


FAMILIES = {
    "0_3_m": lambda m: tuple(sorted((0, 3, m))),
    "0_2_m": lambda m: tuple(sorted((0, 2, m))),
    "0_4_m": lambda m: tuple(sorted((0, 4, m))),
    "1_3_m": lambda m: tuple(sorted((1, 3, m))),
}


def wrapped(x):
    return np.angle(np.exp(1j * x))


def orbit_key(k):
    return tuple(sorted(abs(int(x)) for x in k))


def get_row(payload, N):
    rows = {int(r["N"]): r for r in payload["rows"]}
    return rows[N]


def reconstruct(prev, curr):
    N = int(curr["N"])
    system = System(N=N, nu=NU)
    base = base_state(system, float(curr["amplitude"]), float(curr["anchor_time"]))
    pairs = active_pairs(system, base)

    if [list(k) for _, _, k in pairs] != curr["support_vectors"]:
        raise AssertionError(f"N={N}: support mismatch")

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    old = np.zeros(len(pairs), dtype=bool)
    keys = []

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        keys.append(orbit_key(kt))
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            old[j] = True

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = wrapped(final - inherited)

    if int(old.sum()) != int(curr["inherited_pairs"]):
        raise AssertionError(f"N={N}: inherited count mismatch")

    groups = defaultdict(list)
    for i, key in enumerate(keys):
        if old[i]:
            groups[key].append(i)

    return system, base, pairs, inherited, delta, groups


def qeval(system, base, pairs, phases, grid):
    return evaluate(system, phase_rotate(base, pairs, phases), grid=grid)


def orbit_response(system, base, pairs, inherited, delta, inds, q0, eps, grid):
    mask = np.zeros(len(pairs), dtype=bool)
    mask[inds] = True

    qe = qeval(system, base, pairs, inherited + eps * delta * mask, grid)
    q1 = qeval(system, base, pairs, inherited + delta * mask, grid)

    dlogN = float(np.log(qe["H2_high_transfer"] / q0["H2_high_transfer"]) / eps)
    mdlogP = float(-np.log(
        qe["H1_positive_stretching"] / q0["H1_positive_stretching"]
    ) / eps)

    return {
        "pair_count": len(inds),
        "mean_abs_delta": float(np.mean(np.abs(delta[inds]))),
        "directional_per_unit_lambda": {
            "dlogN": dlogN,
            "minus_dlogPplus": mdlogP,
            "dlogC": dlogN + mdlogP,
        },
        "endpoint": {
            "C_gain_pct": 100.0 * (
                q1["C_infinity_stretch"] / q0["C_infinity_stretch"] - 1.0
            ),
            "N_change_pct": 100.0 * (
                q1["H2_high_transfer"] / q0["H2_high_transfer"] - 1.0
            ),
            "P_plus_change_pct": 100.0 * (
                q1["H1_positive_stretching"] / q0["H1_positive_stretching"] - 1.0
            ),
        },
    }


def analyze_step(prev, curr, grid, eps, m_values):
    N = int(curr["N"])
    system, base, pairs, inherited, delta, groups = reconstruct(prev, curr)
    q0 = qeval(system, base, pairs, inherited, grid)

    families = {}
    for name, builder in FAMILIES.items():
        rows = []
        seen = set()
        for m in m_values:
            key = builder(m)
            if key in seen:
                continue
            seen.add(key)
            inds = groups.get(key, [])
            rows.append({
                "m": int(m),
                "orbit": list(key),
                "present": bool(inds),
                "response": (
                    orbit_response(
                        system, base, pairs, inherited, delta, inds, q0, eps, grid
                    )
                    if inds else None
                ),
            })
        families[name] = rows

    return {
        "N": N,
        "inherited_support_cutoff": N - 1,
        "families": families,
    }


def run(prior_path, current_path, grid, eps, m_values):
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    current = json.loads(current_path.read_text(encoding="utf-8"))

    r8 = get_row(prior, 8)
    r9 = get_row(prior, 9)
    r10 = get_row(current, 10)
    r11 = get_row(current, 11)

    steps = {
        "N9_from_N8": analyze_step(r8, r9, grid, eps, m_values),
        "N10_from_N9": analyze_step(r9, r10, grid, eps, m_values),
        "N11_from_N10": analyze_step(r10, r11, grid, eps, m_values),
    }

    # Collect the primary family longitudinally.
    longitudinal = []
    for m in m_values:
        row = {"m": int(m), "orbit": list(tuple(sorted((0, 3, m))))}
        vals = []
        for step_name, step in steps.items():
            match = None
            for x in step["families"]["0_3_m"]:
                if x["m"] == m:
                    match = x
                    break
            if match is None or not match["present"]:
                row[step_name] = None
            else:
                resp = match["response"]["directional_per_unit_lambda"]
                row[step_name] = resp
                vals.append(resp["dlogC"])
        row["positive_all_available_steps"] = bool(vals) and all(v > 0 for v in vals)
        row["available_step_count"] = len(vals)
        row["geometric_mean_positive_dlogC"] = (
            float(np.prod(vals) ** (1.0 / len(vals)))
            if vals and all(v > 0 for v in vals)
            else 0.0
        )
        longitudinal.append(row)

    longitudinal.sort(
        key=lambda r: (
            r["available_step_count"],
            r["geometric_mean_positive_dlogC"]
        ),
        reverse=True,
    )

    return {
        "status": "executed targeted orbit-family scan",
        "grid": grid,
        "epsilon": eps,
        "m_values": list(m_values),
        "primary_family": "[0,3,m]",
        "control_families": ["[0,2,m]", "[0,4,m]", "[1,3,m]"],
        "steps": steps,
        "primary_family_longitudinal": longitudinal,
        "interpretation_rule": (
            "This is a finite targeted family diagnostic. The primary family was "
            "motivated after observing [0,3,6], so matched nearby controls are "
            "included to reduce post-hoc pattern risk. Favorable finite responses "
            "do not establish an all-N law."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prior-json", type=Path, required=True)
    p.add_argument("--current-json", type=Path, required=True)
    p.add_argument("--grid", type=int, default=48)
    p.add_argument("--epsilon", type=float, default=0.1)
    p.add_argument("--m-min", type=int, default=3)
    p.add_argument("--m-max", type=int, default=10)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    m_values = list(range(a.m_min, a.m_max + 1))
    r = run(a.prior_json, a.current_json, a.grid, a.epsilon, m_values)

    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 84)
    print("TARGETED ORBIT FAMILY SCAN")
    print("=" * 84)

    print("\nPRIMARY FAMILY [0,3,m]")
    for row in r["primary_family_longitudinal"]:
        print(row)

    print("\nSTEPWISE CONTROLS")
    for step_name, step in r["steps"].items():
        print("\n", step_name)
        for fam_name, rows in step["families"].items():
            print(" ", fam_name)
            for x in rows:
                if x["present"]:
                    d = x["response"]["directional_per_unit_lambda"]
                    print(
                        "   m=", x["m"],
                        "orbit=", x["orbit"],
                        "dlogC=", d["dlogC"],
                        "dlogN=", d["dlogN"],
                        "-dlogP=", d["minus_dlogPplus"],
                    )

    print("\nSAVED:", a.output)
