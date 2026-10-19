"""WP16 [0,3,6] resonance-mechanism audit.

Compare target orbit [0,3,6] against:
  [0,2,4], [0,4,8], [0,3,5], [0,3,7]

Across available continuation steps:
  N8 -> N9
  N9 -> N10
  N10 -> N11

For each orbit:
1. reconstruct the inherited phase state and registered old-core phase correction;
2. evaluate endpoint and epsilon directional changes in C, H2 high transfer, P_plus;
3. decompose the exact finite-Galerkin ordered H2 high-advector triads;
4. quantify coefficient envelope and signed-transfer participation of triads touching
   the orbit, including target-as-advector / target-as-advected / target-as-output;
5. compare before/after signed triad transfer on the touched triad set.

Finite diagnostic only. No resonance theorem or continuum claim.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


TARGETS = [
    (0, 3, 6),
    (0, 2, 4),
    (0, 4, 8),
    (0, 3, 5),
    (0, 3, 7),
]


def wrapped(x):
    return np.angle(np.exp(1j * x))


def orbit_key(k):
    return tuple(sorted(abs(int(x)) for x in k))


def get_row(payload, N):
    rows = {int(r["N"]): r for r in payload["rows"]}
    if N not in rows:
        raise KeyError(f"missing N={N}")
    return rows[N]


def signed_mode_phases(system, pairs, pair_phases):
    psi = np.zeros(len(system.modes), dtype=float)
    for (i, j, _), phi in zip(pairs, pair_phases):
        psi[i] = phi
        psi[j] = -phi
    return psi


def reconstruct(prev, curr):
    N = int(curr["N"])
    system = System(N=N, nu=NU)
    base = base_state(system, float(curr["amplitude"]), float(curr["anchor_time"]))
    pairs = active_pairs(system, base)

    support = [list(k) for _, _, k in pairs]
    if support != curr["support_vectors"]:
        raise AssertionError(f"N={N}: support mismatch")

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    old = np.zeros(len(pairs), dtype=bool)
    groups = defaultdict(list)

    for idx, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        if kt in prev_map:
            inherited[idx] = prev_map[kt]
            old[idx] = True
            groups[orbit_key(kt)].append(idx)

    if int(old.sum()) != int(curr["inherited_pairs"]):
        raise AssertionError(
            f"N={N}: inherited count {int(old.sum())} != {curr['inherited_pairs']}"
        )

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = wrapped(final - inherited)

    return system, base, pairs, inherited, delta, groups


def qeval(system, base, pairs, phases, grid):
    return evaluate(system, phase_rotate(base, pairs, phases), grid=grid)


def qchanges(q, q0):
    return {
        "C_gain_pct": 100.0 * (
            q["C_infinity_stretch"] / q0["C_infinity_stretch"] - 1.0
        ),
        "N_change_pct": 100.0 * (
            q["H2_high_transfer"] / q0["H2_high_transfer"] - 1.0
        ),
        "P_plus_change_pct": 100.0 * (
            q["H1_positive_stretching"] / q0["H1_positive_stretching"] - 1.0
        ),
    }


def empty_bucket():
    return {
        "count": 0,
        "A": 0.0,
        "N_before": 0.0,
        "N_after": 0.0,
    }


def add_bucket(bucket, z0, theta0, theta1):
    if len(z0) == 0:
        return
    bucket["count"] += int(len(z0))
    bucket["A"] += float(np.sum(np.abs(z0)))
    bucket["N_before"] += float(np.sum(np.real(z0 * np.exp(1j * theta0))))
    bucket["N_after"] += float(np.sum(np.real(z0 * np.exp(1j * theta1))))


def finalize_bucket(bucket, total):
    out = dict(bucket)
    out["delta_N"] = out["N_after"] - out["N_before"]
    out["A_fraction_of_total"] = (
        out["A"] / total["A"] if total["A"] else 0.0
    )
    out["N_before_fraction_of_total"] = (
        out["N_before"] / total["N_before"] if total["N_before"] else 0.0
    )
    out["delta_N_fraction_of_total_before"] = (
        out["delta_N"] / total["N_before"] if total["N_before"] else 0.0
    )
    out["chi_before"] = out["N_before"] / out["A"] if out["A"] else 0.0
    out["chi_after"] = out["N_after"] / out["A"] if out["A"] else 0.0
    return out


def triad_audit(
    system,
    base,
    pairs,
    inherited,
    target_phases,
    target_pair_indices,
    chunk_size,
    Kcut=2,
):
    psi0 = signed_mode_phases(system, pairs, inherited)
    psi1 = signed_mode_phases(system, pairs, target_phases)

    target_modes = np.zeros(len(system.modes), dtype=bool)
    for idx in target_pair_indices:
        i, j, _ = pairs[idx]
        target_modes[i] = True
        target_modes[j] = True

    weights = system.square.astype(float) ** 2.0
    buckets = {
        "total": empty_bucket(),
        "touches_target": empty_bucket(),
        "target_as_advector": empty_bucket(),
        "target_as_advected": empty_bucket(),
        "target_as_output": empty_bucket(),
        "target_exactly_one_role": empty_bucket(),
        "target_multiple_roles": empty_bucket(),
    }

    pair_count = len(system.out)
    for start in range(0, pair_count, chunk_size):
        stop = min(pair_count, start + chunk_size)
        out = system.out[start:stop]
        left = system.left[start:stop]
        right = system.right[start:stop]

        high = system.square[left] > Kcut * Kcut
        if not np.any(high):
            continue

        out = out[high]
        left = left[high]
        right = right[high]

        qdot = np.einsum(
            "ij,ij->i",
            system.waves[right],
            base[left],
        )
        raw = 1j * qdot[:, None] * base[right]
        projected = np.einsum(
            "kij,kj->ki",
            system.projectors[out],
            raw,
        )
        z0 = -weights[out] * np.einsum(
            "ij,ij->i",
            np.conj(base[out]),
            projected,
        )

        th0 = psi0[left] + psi0[right] - psi0[out]
        th1 = psi1[left] + psi1[right] - psi1[out]

        add_bucket(buckets["total"], z0, th0, th1)

        mL = target_modes[left]
        mR = target_modes[right]
        mO = target_modes[out]
        touches = mL | mR | mO
        role_count = mL.astype(int) + mR.astype(int) + mO.astype(int)

        add_bucket(buckets["touches_target"], z0[touches], th0[touches], th1[touches])
        add_bucket(buckets["target_as_advector"], z0[mL], th0[mL], th1[mL])
        add_bucket(buckets["target_as_advected"], z0[mR], th0[mR], th1[mR])
        add_bucket(buckets["target_as_output"], z0[mO], th0[mO], th1[mO])

        one = role_count == 1
        multi = role_count >= 2
        add_bucket(buckets["target_exactly_one_role"], z0[one], th0[one], th1[one])
        add_bucket(buckets["target_multiple_roles"], z0[multi], th0[multi], th1[multi])

    total = buckets["total"]
    if total["A"] <= 0:
        raise AssertionError("empty total triad envelope")

    finalized = {"total": finalize_bucket(total, total)}
    for name, bucket in buckets.items():
        if name == "total":
            continue
        finalized[name] = finalize_bucket(bucket, total)

    return finalized


def analyze_orbit(
    system,
    base,
    pairs,
    inherited,
    delta,
    inds,
    grid,
    eps,
    chunk_size,
):
    mask = np.zeros(len(pairs), dtype=bool)
    mask[inds] = True

    q0 = qeval(system, base, pairs, inherited, grid)
    qe = qeval(system, base, pairs, inherited + eps * delta * mask, grid)
    q1 = qeval(system, base, pairs, inherited + delta * mask, grid)

    dlogN = float(np.log(qe["H2_high_transfer"] / q0["H2_high_transfer"]) / eps)
    mdlogP = float(-np.log(
        qe["H1_positive_stretching"] / q0["H1_positive_stretching"]
    ) / eps)

    phases1 = inherited + delta * mask
    triads = triad_audit(
        system,
        base,
        pairs,
        inherited,
        phases1,
        inds,
        chunk_size,
    )

    # Exact finite-state consistency: total triad N_before/after should match
    # evaluate() high-tail transfer for the corresponding phase states.
    rel0 = abs(triads["total"]["N_before"] - q0["H2_high_transfer"]) / max(
        1.0, abs(q0["H2_high_transfer"])
    )
    rel1 = abs(triads["total"]["N_after"] - q1["H2_high_transfer"]) / max(
        1.0, abs(q1["H2_high_transfer"])
    )
    if rel0 > 2e-11 or rel1 > 2e-11:
        raise AssertionError(
            f"triad reconstruction mismatch before={rel0} after={rel1}"
        )

    return {
        "pair_count": len(inds),
        "mean_abs_phase_delta": float(np.mean(np.abs(delta[inds]))),
        "directional_per_unit_lambda": {
            "dlogN": dlogN,
            "minus_dlogPplus": mdlogP,
            "dlogC": dlogN + mdlogP,
        },
        "endpoint": qchanges(q1, q0),
        "triad_participation": triads,
        "triad_reconstruction_relative_error": {
            "before": rel0,
            "after": rel1,
        },
    }


def analyze_step(prev, curr, grid, eps, chunk_size):
    system, base, pairs, inherited, delta, groups = reconstruct(prev, curr)

    rows = []
    for key in TARGETS:
        inds = groups.get(key, [])
        row = {
            "orbit": list(key),
            "present": bool(inds),
        }
        if inds:
            row["result"] = analyze_orbit(
                system,
                base,
                pairs,
                inherited,
                delta,
                inds,
                grid,
                eps,
                chunk_size,
            )
        else:
            row["result"] = None
        rows.append(row)

    return {
        "N": int(curr["N"]),
        "inherited_support_cutoff": int(curr["N"]) - 1,
        "orbits": rows,
    }


def run(prior_path, current_path, grid, eps, chunk_size):
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    current = json.loads(current_path.read_text(encoding="utf-8"))

    r8 = get_row(prior, 8)
    r9 = get_row(prior, 9)
    r10 = get_row(current, 10)
    r11 = get_row(current, 11)

    steps = {
        "N9_from_N8": analyze_step(r8, r9, grid, eps, chunk_size),
        "N10_from_N9": analyze_step(r9, r10, grid, eps, chunk_size),
        "N11_from_N10": analyze_step(r10, r11, grid, eps, chunk_size),
    }

    # Compact longitudinal comparison.
    longitudinal = []
    for key in TARGETS:
        item = {"orbit": list(key), "steps": {}}
        for name, step in steps.items():
            found = next(x for x in step["orbits"] if tuple(x["orbit"]) == key)
            if found["present"]:
                r = found["result"]
                item["steps"][name] = {
                    "dlogC": r["directional_per_unit_lambda"]["dlogC"],
                    "dlogN": r["directional_per_unit_lambda"]["dlogN"],
                    "minus_dlogPplus": r["directional_per_unit_lambda"]["minus_dlogPplus"],
                    "endpoint_C_gain_pct": r["endpoint"]["C_gain_pct"],
                    "endpoint_N_change_pct": r["endpoint"]["N_change_pct"],
                    "endpoint_P_plus_change_pct": r["endpoint"]["P_plus_change_pct"],
                    "touched_A_fraction": r["triad_participation"]["touches_target"]["A_fraction_of_total"],
                    "touched_N_before_fraction": r["triad_participation"]["touches_target"]["N_before_fraction_of_total"],
                    "touched_delta_N_fraction_of_total_before": r["triad_participation"]["touches_target"]["delta_N_fraction_of_total_before"],
                    "advector_A_fraction": r["triad_participation"]["target_as_advector"]["A_fraction_of_total"],
                    "advected_A_fraction": r["triad_participation"]["target_as_advected"]["A_fraction_of_total"],
                    "output_A_fraction": r["triad_participation"]["target_as_output"]["A_fraction_of_total"],
                }
            else:
                item["steps"][name] = None
        longitudinal.append(item)

    return {
        "status": "executed [0,3,6] resonance-mechanism audit",
        "grid": grid,
        "epsilon": eps,
        "targets": [list(x) for x in TARGETS],
        "steps": steps,
        "longitudinal_summary": longitudinal,
        "interpretation_rule": (
            "This audit decomposes exact finite-Galerkin H2 high-advector triads "
            "and finite phase-response effects. Large triad participation or "
            "response does not by itself establish a resonance theorem or "
            "cutoff-uniform Navier-Stokes estimate."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prior-json", type=Path, required=True)
    p.add_argument("--current-json", type=Path, required=True)
    p.add_argument("--grid", type=int, default=48)
    p.add_argument("--epsilon", type=float, default=0.1)
    p.add_argument("--chunk-size", type=int, default=250000)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(
        a.prior_json,
        a.current_json,
        a.grid,
        a.epsilon,
        a.chunk_size,
    )

    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 88)
    print("[0,3,6] RESONANCE-MECHANISM AUDIT")
    print("=" * 88)

    for item in result["longitudinal_summary"]:
        print("\nORBIT", item["orbit"])
        for step, r in item["steps"].items():
            if r is None:
                print(" ", step, "NOT AVAILABLE")
                continue
            print(
                " ", step,
                "dlogC=", r["dlogC"],
                "dlogN=", r["dlogN"],
                "-dlogP=", r["minus_dlogPplus"],
                "Cgain%=", r["endpoint_C_gain_pct"],
                "Nchange%=", r["endpoint_N_change_pct"],
                "Pchange%=", r["endpoint_P_plus_change_pct"],
                "touchA=", r["touched_A_fraction"],
                "touchN=", r["touched_N_before_fraction"],
                "deltaN/totalN=", r["touched_delta_N_fraction_of_total_before"],
                "roles(A)=",
                (r["advector_A_fraction"], r["advected_A_fraction"], r["output_A_fraction"]),
            )

    print("\nSAVED:", a.output)
