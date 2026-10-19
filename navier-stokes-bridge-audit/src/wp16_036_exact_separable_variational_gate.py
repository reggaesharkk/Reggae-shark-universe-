"""Exact separable variational audit for the persistent [223]+[123]->[036] motif.

Because the target orbit [036] appears only in the OUTPUT slot of this motif,
varying only the 12 [036] conjugate-pair phases makes the motif functional
separable by target pair.

For one target pair phase phi_r, every motif term has
    A_j cos(c_j - s_j phi_r),  s_j in {+1,-1}.
Therefore
    F_r(phi) = Re[C_r exp(-i phi)]
with
    C_r = sum_{s=+1} A_j exp(i c_j)
          + conj(sum_{s=-1} A_j exp(i c_j)).

Hence the exact motif-only maximizing phase is
    phi_r^* = arg(C_r) mod 2pi
and the exact pair maximum is |C_r|.

This gate compares inherited, registered [036]-only, and exact motif-optimal
phases across N8->N9, N9->N10, and N10->N11.

Finite variational statement only.
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
    return float(np.angle(np.exp(1j * x)))


def get_row(payload, N):
    return {int(r["N"]): r for r in payload["rows"]}[N]


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
    target_idx = []

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            if orbit(kt) == TARGET:
                target_idx.append(j)

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = np.angle(np.exp(1j * (final - inherited)))
    registered = inherited.copy()
    registered[target_idx] += delta[target_idx]

    return system, base, pairs, inherited, registered, target_idx


def signed_mode_phases(system, pairs, pair_phases):
    psi = np.zeros(len(system.modes), dtype=float)
    for (i, j, _), phi in zip(pairs, pair_phases):
        psi[i] = phi
        psi[j] = -phi
    return psi


def analyze_step(prev, curr):
    system, base, pairs, inherited, registered, target_idx = reconstruct(prev, curr)

    if len(target_idx) != 12:
        raise AssertionError(f"expected 12 target pairs, got {len(target_idx)}")

    psi_fixed = signed_mode_phases(system, pairs, inherited)
    weights = system.square.astype(float) ** 2

    # Map target output mode -> (pair index in target_idx list, sign in psi).
    out_map = {}
    pair_meta = []
    for local_r, pair_index in enumerate(target_idx):
        i, j, krep = pairs[pair_index]
        out_map[int(i)] = (local_r, +1)
        out_map[int(j)] = (local_r, -1)
        pair_meta.append({
            "local_index": local_r,
            "pair_index": int(pair_index),
            "representative_k": [int(x) for x in krep],
            "phi_inherited": float(inherited[pair_index]),
            "phi_registered": float(registered[pair_index]),
            "Bplus_real": 0.0,
            "Bplus_imag": 0.0,
            "Bminus_real": 0.0,
            "Bminus_imag": 0.0,
            "term_count": 0,
            "A_sum": 0.0,
        })

    exact_count = 0
    for oi, li, ri in zip(system.out, system.left, system.right):
        if int(oi) not in out_map:
            continue
        if system.square[li] <= 4:
            continue
        if orbit(system.modes[li]) != LEFT:
            continue
        if orbit(system.modes[ri]) != RIGHT:
            continue

        local_r, sign = out_map[int(oi)]

        qdot = np.dot(system.waves[ri], base[li])
        raw = 1j * qdot * base[ri]
        projected = system.projectors[oi] @ raw
        z0 = -weights[oi] * np.vdot(base[oi], projected)

        A = float(abs(z0))
        beta = float(np.angle(z0))
        c = beta + float(psi_fixed[li]) + float(psi_fixed[ri])
        ph = A * np.exp(1j * c)

        if sign == +1:
            pair_meta[local_r]["Bplus_real"] += float(np.real(ph))
            pair_meta[local_r]["Bplus_imag"] += float(np.imag(ph))
        else:
            pair_meta[local_r]["Bminus_real"] += float(np.real(ph))
            pair_meta[local_r]["Bminus_imag"] += float(np.imag(ph))

        pair_meta[local_r]["term_count"] += 1
        pair_meta[local_r]["A_sum"] += A
        exact_count += 1

    if exact_count != 48:
        raise AssertionError(f"expected 48 exact motif triads, got {exact_count}")

    total_before = 0.0
    total_after = 0.0
    total_opt = 0.0
    weighted_dist_before_num = 0.0
    weighted_dist_after_num = 0.0
    weight_sum = 0.0

    for m in pair_meta:
        Bp = complex(m.pop("Bplus_real"), m.pop("Bplus_imag"))
        Bm = complex(m.pop("Bminus_real"), m.pop("Bminus_imag"))
        C = Bp + np.conj(Bm)

        phi_star = float(np.angle(C))
        amp = float(abs(C))
        phi0 = m["phi_inherited"]
        phi1 = m["phi_registered"]

        F0 = float(np.real(C * np.exp(-1j * phi0)))
        F1 = float(np.real(C * np.exp(-1j * phi1)))
        Fopt = amp

        d0 = abs(wrapped(phi0 - phi_star))
        d1 = abs(wrapped(phi1 - phi_star))

        possible_gain = Fopt - F0
        captured = (
            (F1 - F0) / possible_gain
            if possible_gain > 1e-14
            else None
        )

        m.update({
            "C_real": float(np.real(C)),
            "C_imag": float(np.imag(C)),
            "C_abs": amp,
            "phi_exact_opt": phi_star,
            "distance_inherited_to_opt": d0,
            "distance_registered_to_opt": d1,
            "moves_toward_opt": bool(d1 < d0),
            "F_inherited": F0,
            "F_registered": F1,
            "F_exact_opt": Fopt,
            "registered_gain": F1 - F0,
            "available_gain": possible_gain,
            "fraction_available_gain_captured": captured,
        })

        total_before += F0
        total_after += F1
        total_opt += Fopt
        weighted_dist_before_num += amp * d0
        weighted_dist_after_num += amp * d1
        weight_sum += amp

    if weight_sum <= 0:
        raise AssertionError("zero total separable phasor weight")

    total_available = total_opt - total_before
    total_captured = total_after - total_before

    return {
        "N": int(curr["N"]),
        "exact_triad_count": exact_count,
        "target_pair_count": len(pair_meta),
        "exact_separable_form": "F(phi_1,...,phi_12)=sum_r Re[C_r exp(-i phi_r)]",
        "exact_pair_maximizer": "phi_r^*=arg(C_r) mod 2pi",
        "pairs": pair_meta,
        "summary": {
            "pairs_moving_toward_exact_optimum": int(sum(m["moves_toward_opt"] for m in pair_meta)),
            "weighted_mean_distance_to_opt_inherited": weighted_dist_before_num / weight_sum,
            "weighted_mean_distance_to_opt_registered": weighted_dist_after_num / weight_sum,
            "motif_F_inherited": total_before,
            "motif_F_registered": total_after,
            "motif_F_exact_separable_optimum": total_opt,
            "registered_motif_gain": total_captured,
            "available_motif_gain": total_available,
            "fraction_available_gain_captured": (
                total_captured / total_available
                if total_available > 1e-14 else None
            ),
        },
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

    return {
        "status": "executed exact separable motif variational audit",
        "target_output_orbit": list(TARGET),
        "advector_orbit": list(LEFT),
        "advected_orbit": list(RIGHT),
        "steps": steps,
        "all_three_reduce_weighted_distance_to_exact_pair_optima": all(
            s["summary"]["weighted_mean_distance_to_opt_registered"]
            < s["summary"]["weighted_mean_distance_to_opt_inherited"]
            for s in steps.values()
        ),
        "interpretation_rule": (
            "The separable cosine form and phi_r^*=arg(C_r) are exact for the "
            "finite motif when only [036] output phases vary and all inputs are "
            "held fixed. This is not a variational characterization of the full "
            "Navier-Stokes dynamics or full phase objective."
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

    print("\n" + "=" * 92)
    print("EXACT SEPARABLE VARIATIONAL AUDIT — [223]+[123]->[036]")
    print("=" * 92)

    for name, step in result["steps"].items():
        s = step["summary"]
        print("\n", name)
        print(" exact triads:", step["exact_triad_count"])
        print(" target phase pairs:", step["target_pair_count"])
        print(" pairs moving toward exact optimum:", s["pairs_moving_toward_exact_optimum"], "/ 12")
        print(
            " weighted mean distance:",
            s["weighted_mean_distance_to_opt_inherited"],
            "->",
            s["weighted_mean_distance_to_opt_registered"],
        )
        print(
            " motif F:",
            s["motif_F_inherited"],
            "->",
            s["motif_F_registered"],
            "exact separable optimum=",
            s["motif_F_exact_separable_optimum"],
        )
        print(
            " fraction available motif gain captured:",
            s["fraction_available_gain_captured"],
        )

    print(
        "\nall three reduce weighted distance:",
        result["all_three_reduce_weighted_distance_to_exact_pair_optima"],
    )
    print("\nSAVED:", a.output)
