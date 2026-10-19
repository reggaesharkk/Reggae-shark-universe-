"""WP16 [0,3,6] output partner-triad decomposition.

For the target orbit [0,3,6], decompose only exact finite-Galerkin H2
high-advector triads where the target mode is the OUTPUT mode.

For each continuation step:
  N8 -> N9
  N9 -> N10
  N10 -> N11

bucket those output triads by the absolute-coordinate orbit classes of:
  - the advector/left partner
  - the advected/right partner

Rank partner-orbit pairs by signed transfer change caused by the registered
[0,3,6] phase correction.

Finite diagnostic only.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs


TARGET = (0, 3, 6)


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
        raise AssertionError(f"N={N} support mismatch")

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    old = np.zeros(len(pairs), dtype=bool)
    target_pair_indices = []

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            old[j] = True
            if orbit_key(kt) == TARGET:
                target_pair_indices.append(j)

    if int(old.sum()) != int(curr["inherited_pairs"]):
        raise AssertionError(f"N={N} inherited mismatch")

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = wrapped(final - inherited)

    return system, base, pairs, inherited, delta, target_pair_indices


def signed_mode_phases(system, pairs, pair_phases):
    psi = np.zeros(len(system.modes), dtype=float)
    for (i, j, _), phi in zip(pairs, pair_phases):
        psi[i] = phi
        psi[j] = -phi
    return psi


def empty_bucket():
    return {"count": 0, "A": 0.0, "N_before": 0.0, "N_after": 0.0}


def add(bucket, z0, th0, th1):
    if len(z0) == 0:
        return
    bucket["count"] += int(len(z0))
    bucket["A"] += float(np.sum(np.abs(z0)))
    bucket["N_before"] += float(np.sum(np.real(z0 * np.exp(1j * th0))))
    bucket["N_after"] += float(np.sum(np.real(z0 * np.exp(1j * th1))))


def finish(bucket):
    out = dict(bucket)
    out["delta_N"] = out["N_after"] - out["N_before"]
    out["chi_before"] = out["N_before"] / out["A"] if out["A"] else 0.0
    out["chi_after"] = out["N_after"] / out["A"] if out["A"] else 0.0
    return out


def analyze_step(prev, curr, chunk_size, top_k):
    system, base, pairs, inherited, delta, target_pair_indices = reconstruct(prev, curr)

    if not target_pair_indices:
        return {
            "N": int(curr["N"]),
            "present": False,
            "reason": "target orbit not in inherited support",
        }

    mask = np.zeros(len(pairs), dtype=bool)
    mask[target_pair_indices] = True
    target_phases = inherited + delta * mask

    psi0 = signed_mode_phases(system, pairs, inherited)
    psi1 = signed_mode_phases(system, pairs, target_phases)

    target_modes = np.zeros(len(system.modes), dtype=bool)
    for idx in target_pair_indices:
        i, j, _ = pairs[idx]
        target_modes[i] = True
        target_modes[j] = True

    mode_orbits = [orbit_key(k) for k in system.modes]
    weights = system.square.astype(float) ** 2.0

    total_output = empty_bucket()
    buckets = defaultdict(empty_bucket)

    pair_count = len(system.out)
    for start in range(0, pair_count, chunk_size):
        stop = min(pair_count, start + chunk_size)
        out = system.out[start:stop]
        left = system.left[start:stop]
        right = system.right[start:stop]

        high = system.square[left] > 4
        is_target_output = target_modes[out]
        keep = high & is_target_output
        if not np.any(keep):
            continue

        out = out[keep]
        left = left[keep]
        right = right[keep]

        qdot = np.einsum("ij,ij->i", system.waves[right], base[left])
        raw = 1j * qdot[:, None] * base[right]
        projected = np.einsum("kij,kj->ki", system.projectors[out], raw)
        z0 = -weights[out] * np.einsum("ij,ij->i", np.conj(base[out]), projected)

        th0 = psi0[left] + psi0[right] - psi0[out]
        th1 = psi1[left] + psi1[right] - psi1[out]

        add(total_output, z0, th0, th1)

        # Group by ordered partner orbit classes. Orientation matters because
        # left is the high-advector slot and right is the advected slot.
        local = defaultdict(list)
        for idx_local, (li, ri) in enumerate(zip(left, right)):
            key = (mode_orbits[int(li)], mode_orbits[int(ri)])
            local[key].append(idx_local)

        for key, inds in local.items():
            inds = np.asarray(inds, dtype=int)
            add(buckets[key], z0[inds], th0[inds], th1[inds])

    total_output = finish(total_output)

    rows = []
    for key, bucket in buckets.items():
        r = finish(bucket)
        r.update({
            "advector_orbit": list(key[0]),
            "advected_orbit": list(key[1]),
            "A_fraction_of_target_output": (
                r["A"] / total_output["A"] if total_output["A"] else 0.0
            ),
            "delta_N_fraction_of_target_output": (
                r["delta_N"] / total_output["delta_N"]
                if total_output["delta_N"] else 0.0
            ),
        })
        rows.append(r)

    by_positive_delta = sorted(rows, key=lambda r: r["delta_N"], reverse=True)
    by_abs_delta = sorted(rows, key=lambda r: abs(r["delta_N"]), reverse=True)
    by_A = sorted(rows, key=lambda r: r["A"], reverse=True)

    return {
        "N": int(curr["N"]),
        "present": True,
        "target_pair_count": len(target_pair_indices),
        "target_output_total": total_output,
        "partner_pair_count": len(rows),
        "top_positive_delta_N": by_positive_delta[:top_k],
        "top_absolute_delta_N": by_abs_delta[:top_k],
        "top_coefficient_envelope": by_A[:top_k],
        "all_partner_pairs": rows,
    }


def run(prior_path, current_path, chunk_size, top_k):
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    current = json.loads(current_path.read_text(encoding="utf-8"))

    r8 = get_row(prior, 8)
    r9 = get_row(prior, 9)
    r10 = get_row(current, 10)
    r11 = get_row(current, 11)

    steps = {
        "N9_from_N8": analyze_step(r8, r9, chunk_size, top_k),
        "N10_from_N9": analyze_step(r9, r10, chunk_size, top_k),
        "N11_from_N10": analyze_step(r10, r11, chunk_size, top_k),
    }

    # Persistent partner motifs: exact ordered partner-orbit pair present
    # among top positive-delta lists in multiple steps.
    memberships = defaultdict(list)
    for step_name, step in steps.items():
        if not step["present"]:
            continue
        for rank, row in enumerate(step["top_positive_delta_N"], 1):
            key = (tuple(row["advector_orbit"]), tuple(row["advected_orbit"]))
            memberships[key].append({
                "step": step_name,
                "rank": rank,
                "delta_N": row["delta_N"],
                "A": row["A"],
                "chi_before": row["chi_before"],
                "chi_after": row["chi_after"],
            })

    persistent = []
    for key, vals in memberships.items():
        if len(vals) >= 2:
            persistent.append({
                "advector_orbit": list(key[0]),
                "advected_orbit": list(key[1]),
                "step_count": len(vals),
                "steps": vals,
                "mean_rank": float(np.mean([v["rank"] for v in vals])),
            })
    persistent.sort(key=lambda r: (-r["step_count"], r["mean_rank"]))

    return {
        "status": "executed [0,3,6] output partner-triad decomposition",
        "target": list(TARGET),
        "steps": steps,
        "persistent_top_positive_partner_pairs": persistent,
        "interpretation_rule": (
            "Partner-orbit buckets are exact finite-Galerkin decompositions of "
            "the target-as-output H2 high-advector contribution. Persistence "
            "across three finite cutoffs does not establish an all-N resonance law."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prior-json", type=Path, required=True)
    p.add_argument("--current-json", type=Path, required=True)
    p.add_argument("--chunk-size", type=int, default=250000)
    p.add_argument("--top-k", type=int, default=20)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.prior_json, a.current_json, a.chunk_size, a.top_k)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 88)
    print("[0,3,6] OUTPUT PARTNER-TRIAD DECOMPOSITION")
    print("=" * 88)

    for step_name, step in result["steps"].items():
        print("\n", step_name)
        if not step["present"]:
            print(" target unavailable")
            continue
        print("target output total:", step["target_output_total"])
        print("top positive partner pairs:")
        for rank, row in enumerate(step["top_positive_delta_N"][:10], 1):
            print(
                rank,
                "L=", row["advector_orbit"],
                "R=", row["advected_orbit"],
                "deltaN=", row["delta_N"],
                "A=", row["A"],
                "chi", row["chi_before"], "->", row["chi_after"],
            )

    print("\nPERSISTENT TOP-POSITIVE PARTNER PAIRS")
    for row in result["persistent_top_positive_partner_pairs"][:20]:
        print(row)

    print("\nSAVED:", a.output)
