"""Instantaneous phase-dynamics audit for the dominant conjugate triad pair.

Representative positive triad:
    p=(3,2,2)
    q=(3,-2,1)
    k=(6,0,3)=p+q

For the exact H2 triad coefficient
    z = -|k|^4 <a_k, P_k i(q·a_p)a_q>,
define alpha = arg(z).

Along the full finite Galerkin Navier-Stokes ODE:
    alpha_dot = Im(z_dot / z)

with z_dot obtained analytically by the product rule using the full RHS for
a_p, a_q, and a_k.

The gate evaluates three states at each cutoff step:
  inherited, target_only, full_final.

It also verifies that viscosity contributes zero phase velocity up to floating
point error, as expected because the linear viscous factors are real.

Finite instantaneous diagnostic only.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate


P = (3, 2, 2)
Q = (3, -2, 1)
K = (6, 0, 3)
TARGET_ORBIT = (0, 3, 6)


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

    if [list(k) for _, _, k in pairs] != curr["support_vectors"]:
        raise AssertionError(f"N={N}: support mismatch")

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev["support_vectors"], prev["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    target_mask = np.zeros(len(pairs), dtype=bool)

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            if orbit(kt) == TARGET_ORBIT:
                target_mask[j] = True

    final = np.asarray(curr["best_phases"], dtype=float)
    delta = np.angle(np.exp(1j * (final - inherited)))
    target_only = inherited + delta * target_mask

    states = {
        "inherited": phase_rotate(base, pairs, inherited),
        "target_only": phase_rotate(base, pairs, target_only),
        "full_final": phase_rotate(base, pairs, final),
    }
    return system, states


def z_and_zdot(system, a, da):
    pi = system.index[P]
    qi = system.index[Q]
    ki = system.index[K]

    qwave = np.asarray(Q, dtype=float)
    Pk = system.projectors[ki]
    weight = float(system.square[ki] ** 2)

    ap = a[pi]
    aq = a[qi]
    ak = a[ki]

    dap = da[pi]
    daq = da[qi]
    dak = da[ki]

    s = np.dot(qwave, ap)
    ds = np.dot(qwave, dap)

    B = Pk @ (1j * s * aq)
    dB = Pk @ (1j * (ds * aq + s * daq))

    z = -weight * np.vdot(ak, B)
    dz = -weight * (np.vdot(dak, B) + np.vdot(ak, dB))

    return z, dz


def inspect_state(system, a):
    da_full = system.rhs(a)
    da_nl = -system.nonlinear(a)
    da_visc = -system.nu * system.square[:, None] * a

    z, dz_full = z_and_zdot(system, a, da_full)
    z2, dz_nl = z_and_zdot(system, a, da_nl)
    z3, dz_visc = z_and_zdot(system, a, da_visc)

    if abs(z-z2) > 1e-10 * max(1.0, abs(z)):
        raise AssertionError("z mismatch nonlinear path")
    if abs(z-z3) > 1e-10 * max(1.0, abs(z)):
        raise AssertionError("z mismatch viscous path")
    if abs(z) < 1e-30:
        raise AssertionError("dominant triad coefficient vanished")

    alpha = wrapped(np.angle(z))
    adot_full = float(np.imag(dz_full / z))
    adot_nl = float(np.imag(dz_nl / z))
    adot_visc = float(np.imag(dz_visc / z))

    dabs = (
        float(np.sign(alpha) * adot_full)
        if abs(alpha) > 1e-14 else 0.0
    )
    dcos = float(-np.sin(alpha) * adot_full)

    return {
        "z_real": float(np.real(z)),
        "z_imag": float(np.imag(z)),
        "z_abs": float(abs(z)),
        "alpha": alpha,
        "alpha_dot_full": adot_full,
        "alpha_dot_nonlinear": adot_nl,
        "alpha_dot_viscous": adot_visc,
        "full_minus_nonlinear_phase_velocity": adot_full - adot_nl,
        "d_abs_alpha_dt_local": dabs,
        "d_cos_alpha_dt_local": dcos,
        "instantaneously_toward_alpha_zero": bool(dabs < 0.0),
        "instantaneously_increasing_phase_cosine": bool(dcos > 0.0),
    }


def analyze_step(prev, curr):
    system, states = reconstruct(prev, curr)
    out = {
        "N": int(curr["N"]),
        "representative": {"p": list(P), "q": list(Q), "k": list(K)},
        "states": {},
    }

    for name, a in states.items():
        out["states"][name] = inspect_state(system, a)

    out["viscosity_phase_neutral_max_abs"] = max(
        abs(s["alpha_dot_viscous"]) for s in out["states"].values()
    )
    return out


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
        "status": "executed dominant-triad instantaneous phase-dynamics audit",
        "representative": {"p": list(P), "q": list(Q), "k": list(K)},
        "exact_identity": "alpha_dot = Im(z_dot/z)",
        "steps": steps,
        "target_only_toward_zero_all_three": all(
            s["states"]["target_only"]["instantaneously_toward_alpha_zero"]
            for s in steps.values()
        ),
        "full_final_toward_zero_all_three": all(
            s["states"]["full_final"]["instantaneously_toward_alpha_zero"]
            for s in steps.values()
        ),
        "interpretation_rule": (
            "This tests only the instantaneous phase velocity of one explicit "
            "triad coefficient under the full finite Galerkin RHS. A negative "
            "local d|alpha|/dt is not a stability theorem, long-time locking "
            "result, cutoff-uniform estimate, or continuum regularity claim."
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

    print("\nDOMINANT TRIAD INSTANTANEOUS PHASE-DYNAMICS AUDIT")
    print("=" * 84)
    for step_name, step in result["steps"].items():
        print("\n", step_name)
        for state_name, s in step["states"].items():
            print(
                " ",
                state_name,
                "alpha=", s["alpha"],
                "alpha_dot=", s["alpha_dot_full"],
                "d|alpha|/dt=", s["d_abs_alpha_dt_local"],
                "dcos/dt=", s["d_cos_alpha_dt_local"],
                "toward0=", s["instantaneously_toward_alpha_zero"],
            )
        print(
            " viscosity phase-neutral max abs:",
            step["viscosity_phase_neutral_max_abs"],
        )

    print(
        "\ntarget-only toward zero all three:",
        result["target_only_toward_zero_all_three"],
    )
    print(
        "full-final toward zero all three:",
        result["full_final_toward_zero_all_three"],
    )
    print("\nSAVED:", a.output)
