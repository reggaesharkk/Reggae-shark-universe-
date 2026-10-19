"""Exact phase-condition audit for persistent [223]+[123]->[036] motif.

For every exact signed triad in the single symmetry class:
    z0 = -|k|^4 i (q·a_p)(conj(a_k)·a_q)
and the signed contribution is
    Re[z0 exp(i theta)] = |z0| cos(alpha),
where
    alpha = arg(z0) + theta.

The pointwise maximizing phase condition is alpha = 0 mod 2pi.

This gate tests whether the registered [0,3,6] phase correction moves the
weighted motif toward that exact maximizing condition across:
    N8 -> N9
    N9 -> N10
    N10 -> N11

Finite diagnostic only.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs


TARGET = (0, 3, 6)
LEFT = (2, 2, 3)
RIGHT = (1, 2, 3)


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


def wrapped(x):
    return np.angle(np.exp(1j * x))


def get_row(payload, N):
    return {int(r["N"]): r for r in payload["rows"]}[N]


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

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    target_idx = []

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            if orbit(kt) == TARGET:
                target_idx.append(j)

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = wrapped(final - inherited)
    mask = np.zeros(len(pairs), dtype=bool)
    mask[target_idx] = True
    target_only = inherited + delta * mask

    return system, base, pairs, inherited, target_only


def weighted_stats(alpha, amp):
    total = float(np.sum(amp))
    if total <= 0:
        raise AssertionError("zero motif envelope")

    abs_a = np.abs(alpha)
    cos_a = np.cos(alpha)
    vec = np.sum(amp * np.exp(1j * alpha))

    return {
        "weighted_mean_abs_phase_error": float(np.sum(amp * abs_a) / total),
        "weighted_rms_phase_error": float(np.sqrt(np.sum(amp * alpha**2) / total)),
        "weighted_cosine_mean_chi": float(np.sum(amp * cos_a) / total),
        "weighted_resultant": float(abs(vec) / total),
        "weighted_mean_angle": float(np.angle(vec)),
        "A_fraction_within_0p10": float(np.sum(amp[abs_a <= 0.10]) / total),
        "A_fraction_within_0p25": float(np.sum(amp[abs_a <= 0.25]) / total),
        "A_fraction_within_0p50": float(np.sum(amp[abs_a <= 0.50]) / total),
        "A_fraction_positive_cosine": float(np.sum(amp[cos_a > 0]) / total),
    }


def analyze_step(prev, curr):
    system, base, pairs, ph0, ph1 = reconstruct(prev, curr)
    psi0 = signed_mode_phases(system, pairs, ph0)
    psi1 = signed_mode_phases(system, pairs, ph1)

    weights = system.square.astype(float) ** 2

    rows = []
    for oi, li, ri in zip(system.out, system.left, system.right):
        if system.square[li] <= 4:
            continue
        if orbit(system.modes[oi]) != TARGET:
            continue
        if orbit(system.modes[li]) != LEFT:
            continue
        if orbit(system.modes[ri]) != RIGHT:
            continue

        qdot = np.dot(system.waves[ri], base[li])
        raw = 1j * qdot * base[ri]
        projected = system.projectors[oi] @ raw
        z0 = -weights[oi] * np.vdot(base[oi], projected)

        th0 = float(psi0[li] + psi0[ri] - psi0[oi])
        th1 = float(psi1[li] + psi1[ri] - psi1[oi])
        beta = float(np.angle(z0))
        a0 = float(wrapped(beta + th0))
        a1 = float(wrapped(beta + th1))
        amp = float(abs(z0))

        rows.append({
            "p": [int(x) for x in system.modes[li]],
            "q": [int(x) for x in system.modes[ri]],
            "k": [int(x) for x in system.modes[oi]],
            "A": amp,
            "arg_z0": beta,
            "theta_before": th0,
            "theta_after": th1,
            "alpha_before": a0,
            "alpha_after": a1,
            "phase_error_reduction": abs(a0) - abs(a1),
            "N_before": float(amp * np.cos(a0)),
            "N_after": float(amp * np.cos(a1)),
        })

    if len(rows) != 48:
        raise AssertionError(f"expected 48 exact motif triads, found {len(rows)}")

    amp = np.asarray([r["A"] for r in rows], dtype=float)
    a0 = np.asarray([r["alpha_before"] for r in rows], dtype=float)
    a1 = np.asarray([r["alpha_after"] for r in rows], dtype=float)

    before = weighted_stats(a0, amp)
    after = weighted_stats(a1, amp)

    # Rank by coefficient envelope so we can see whether the dominant exact
    # representatives move toward alpha=0.
    dominant = sorted(rows, key=lambda r: r["A"], reverse=True)[:12]

    return {
        "N": int(curr["N"]),
        "exact_triad_count": len(rows),
        "maximizing_condition": "alpha = arg(z0) + theta = 0 mod 2pi",
        "before": before,
        "after": after,
        "changes": {
            "weighted_mean_abs_phase_error": (
                after["weighted_mean_abs_phase_error"]
                - before["weighted_mean_abs_phase_error"]
            ),
            "weighted_rms_phase_error": (
                after["weighted_rms_phase_error"]
                - before["weighted_rms_phase_error"]
            ),
            "chi": after["weighted_cosine_mean_chi"] - before["weighted_cosine_mean_chi"],
            "A_fraction_within_0p25": (
                after["A_fraction_within_0p25"]
                - before["A_fraction_within_0p25"]
            ),
            "A_fraction_positive_cosine": (
                after["A_fraction_positive_cosine"]
                - before["A_fraction_positive_cosine"]
            ),
        },
        "dominant_by_A": dominant,
        "all_exact_triads": rows,
    }


def run(prior_path, current_path):
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    current = json.loads(current_path.read_text(encoding="utf-8"))

    r8 = get_row(prior, 8)
    r9 = get_row(prior, 9)
    r10 = get_row(current, 10)
    r11 = get_row(current, 11)

    steps = {
        "N9_from_N8": analyze_step(r8, r9),
        "N10_from_N9": analyze_step(r9, r10),
        "N11_from_N10": analyze_step(r10, r11),
    }

    all_toward = all(
        s["after"]["weighted_mean_abs_phase_error"]
        < s["before"]["weighted_mean_abs_phase_error"]
        for s in steps.values()
    )
    all_chi_up = all(
        s["after"]["weighted_cosine_mean_chi"]
        > s["before"]["weighted_cosine_mean_chi"]
        for s in steps.values()
    )

    return {
        "status": "executed exact phase-condition audit for [223]+[123]->[036]",
        "target_output_orbit": list(TARGET),
        "advector_orbit": list(LEFT),
        "advected_orbit": list(RIGHT),
        "exact_phase_condition": "arg(z0) + theta = 0 mod 2pi",
        "steps": steps,
        "all_three_steps_reduce_weighted_phase_error": all_toward,
        "all_three_steps_increase_weighted_chi": all_chi_up,
        "interpretation_rule": (
            "The pointwise phase maximizer is exact for each finite triad term. "
            "Observed movement toward it under the registered phase correction "
            "is a finite-state mechanism diagnostic, not a theorem that the "
            "full Navier-Stokes dynamics enforces this condition."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prior-json", type=Path, required=True)
    p.add_argument("--current-json", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.prior_json, a.current_json)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 88)
    print("EXACT [223]+[123]->[036] PHASE-CONDITION AUDIT")
    print("=" * 88)

    for name, s in result["steps"].items():
        print("\n", name)
        print(" exact triads:", s["exact_triad_count"])
        print(
            " weighted mean |alpha|:",
            s["before"]["weighted_mean_abs_phase_error"],
            "->",
            s["after"]["weighted_mean_abs_phase_error"],
        )
        print(
            " weighted RMS |alpha|:",
            s["before"]["weighted_rms_phase_error"],
            "->",
            s["after"]["weighted_rms_phase_error"],
        )
        print(
            " chi:",
            s["before"]["weighted_cosine_mean_chi"],
            "->",
            s["after"]["weighted_cosine_mean_chi"],
        )
        print(
            " A within 0.25 rad:",
            s["before"]["A_fraction_within_0p25"],
            "->",
            s["after"]["A_fraction_within_0p25"],
        )
        print(
            " A with cos(alpha)>0:",
            s["before"]["A_fraction_positive_cosine"],
            "->",
            s["after"]["A_fraction_positive_cosine"],
        )

    print(
        "\nall three reduce weighted phase error:",
        result["all_three_steps_reduce_weighted_phase_error"],
    )
    print(
        "all three increase weighted chi:",
        result["all_three_steps_increase_weighted_chi"],
    )
    print("\nSAVED:", a.output)
