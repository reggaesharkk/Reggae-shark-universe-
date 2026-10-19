#!/usr/bin/env python3
"""WP19 v0.22 recursive state/backreaction drift scout.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

This is deliberately a NON-RIGOROUS scout. It combines:
  * exact fixed-output Lipschitz algebra from WP19 v0.14/v0.19;
  * independently certified scalar trajectory-error radii from the Arb runs;
  * floating nodewise predictor differences between consecutive cutoffs.

The point is to falsify or support the simple state-drift route before
spending time on an interval/adjoint implementation. No all-N or continuum
claim follows from this file.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

C11 = math.sqrt(404724.0)
H = 0.000025
STEPS = 120
NU = 0.1
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_KEYS = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"


def load_meta(directory: Path) -> dict:
    return json.loads((directory / "metadata.json").read_text())


def certified_node_error_schedule(directory: Path) -> np.ndarray:
    """Replay the same scalar error recurrence used by the Arb certificates.

    The segment R/M values are outward-rounded certificate data. The recurrence
    itself is evaluated in binary64 here, so this array is used as a scouting
    input rather than promoted to a new interval certificate.
    """
    e = np.zeros(STEPS + 1, dtype=np.float64)
    sqrt2 = math.sqrt(2.0)
    for step in range(STEPS):
        row = json.loads((directory / f"{step:03d}.json").read_text())
        residual = float(row["residual_L2_upper_decimal"])
        grad_l1 = float(row["gradient_Fourier_l1_upper_decimal"])
        strain = grad_l1 / sqrt2
        e[step + 1] = math.exp(strain * H) * (e[step] + H * residual)
    return e


def trapezoid(values: np.ndarray) -> float:
    return H * (0.5 * values[0] + float(values[1:-1].sum()) + 0.5 * values[-1])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--lower-dir", type=Path, required=True)
    ap.add_argument("--higher-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    M = args.M
    if M < 12:
        ap.error("M must be >= 12")

    sys.path.insert(0, str((args.repo / "src").resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    lower_meta = load_meta(args.lower_dir)
    higher_meta = load_meta(args.higher_dir)
    if lower_meta["N"] != M or higher_meta["N"] != M + 1:
        raise ValueError("cutoff metadata mismatch")
    for meta in (lower_meta, higher_meta):
        if meta["witness_sha256"] != EXPECTED_WITNESS:
            raise ValueError("witness hash mismatch")
        if meta["K36_keys_sha256"] != EXPECTED_KEYS:
            raise ValueError("K36 hash mismatch")

    low = DealiasedSystem(M, nu=NU)
    high = DealiasedSystem(M + 1, nu=NU)
    low_nodes = np.load(args.lower_dir / "nodes.npy", mmap_mode="r")
    high_nodes = np.load(args.higher_dir / "nodes.npy", mmap_mode="r")
    if len(low_nodes) != STEPS + 1 or len(high_nodes) != STEPS + 1:
        raise ValueError("unexpected predictor length")

    high_index = np.asarray([high.index[k] for k in low.modes], dtype=np.int64)

    nominal = np.empty(STEPS + 1, dtype=np.float64)
    for j in range(STEPS + 1):
        delta = np.asarray(high_nodes[j, high_index]) - np.asarray(low_nodes[j])
        nominal[j] = float(np.linalg.norm(delta.ravel()))

    e_low = certified_node_error_schedule(args.lower_dir)
    e_high = certified_node_error_schedule(args.higher_dir)
    state_upper_scout = nominal + e_low + e_high

    initial_l2 = float(np.linalg.norm(np.asarray(low_nodes[0]).ravel()))
    nominal_l1 = trapezoid(nominal)
    state_upper_l1_scout = trapezoid(state_upper_scout)

    # Exact algebraic inequality for exact states x=P_M u_{M+1}, y=u_M:
    #
    # Gamma_M(u) = -P11[B(u,u)-B(P11u,P11u)]
    #
    # ||Gamma_M(x)-Gamma_M(y)||_2
    # <= 2*C11*(||x||_2+||y||_2)*||x-y||_2
    # <= 4*C11*||u0||_2*||x-y||_2
    #
    # The inequality is exact; only the nodewise/integrated state-drift input
    # below is a floating scout.
    recursive_gamma_l1_scout = 4.0 * C11 * initial_l2 * state_upper_l1_scout
    recursive_gamma_l1_nominal = 4.0 * C11 * initial_l2 * nominal_l1

    # Exact v0.19 theorem-form direct shell bound for this transition M->M+1.
    direct_shell_theorem_bound = (
        C11
        * initial_l2**2
        / (2.0 * NU)
        * (1.0 / (M * (M - 11.0)) + 1.0 / (M * M))
    )

    out = {
        "schema": "wp19-v0.22-recursive-drift-lipschitz-scout-v1",
        "copyright": "Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "status": "NON-RIGOROUS FLOATING SCOUT WITH CERTIFIED SEGMENT-RADIUS INPUTS",
        "transition": f"{M}->{M+1}",
        "M": M,
        "C11": C11,
        "nu": NU,
        "h": H,
        "steps": STEPS,
        "witness_sha256": EXPECTED_WITNESS,
        "K36_keys_sha256": EXPECTED_KEYS,
        "initial_predictor_L2": initial_l2,
        "nominal_state_drift": {
            "endpoint_L2": float(nominal[-1]),
            "maximum_node_L2": float(nominal.max()),
            "node_trapezoid_L1_t_L2": nominal_l1,
        },
        "trajectory_error_replay": {
            "lower_terminal": float(e_low[-1]),
            "higher_terminal": float(e_high[-1]),
        },
        "state_difference_upper_scout": {
            "endpoint_L2": float(state_upper_scout[-1]),
            "maximum_node_L2": float(state_upper_scout.max()),
            "node_trapezoid_L1_t_L2": state_upper_l1_scout,
        },
        "recursive_gamma_lipschitz": {
            "exact_inequality": "||Gamma_M(x)-Gamma_M(y)||_2 <= 4*C11*||u0||_2*||x-y||_2",
            "nominal_node_trapezoid_L1_bound": recursive_gamma_l1_nominal,
            "radius_augmented_node_trapezoid_L1_scout": recursive_gamma_l1_scout,
        },
        "direct_shell_v0_19": {
            "exact_theorem_form": "C11*||u0||_2^2/(2*nu)*[1/(M(M-11))+1/M^2]",
            "L1_t_L2_bound": direct_shell_theorem_bound,
        },
        "combined_simple_route_scout": {
            "direct_plus_recursive": direct_shell_theorem_bound + recursive_gamma_l1_scout,
            "interpretation": "If this is grossly too large, the simple full-state Lipschitz route should be abandoned in favor of the goal-oriented adjoint."
        },
        "claim_boundary": (
            "The fixed-output Lipschitz inequality and v0.19 direct-shell formula are analytic. "
            "The nodewise predictor norms, binary64 replay of the scalar radii, and trapezoid integration "
            "are scouting quantities only; this JSON is not a new interval certificate and makes no all-N "
            "or continuum Navier-Stokes claim."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "transition": out["transition"],
        "endpoint_nominal_drift": nominal[-1],
        "state_L1_scout": state_upper_l1_scout,
        "recursive_gamma_L1_scout": recursive_gamma_l1_scout,
        "direct_shell_bound": direct_shell_theorem_bound,
        "combined": direct_shell_theorem_bound + recursive_gamma_l1_scout,
    }, indent=2))


if __name__ == "__main__":
    main()
