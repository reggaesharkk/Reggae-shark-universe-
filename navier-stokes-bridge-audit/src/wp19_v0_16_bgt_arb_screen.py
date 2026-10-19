#!/usr/bin/env python3
"""WP19 v0.16: Arb screen of the Brunk--Giesselmann--Tscherpel criterion.

This script evaluates the exact cubic-Hermite N14 reconstruction used by the
validated same-datum certificate. It does two things:

1. proves a LOWER bound on the BGT criterion's left-hand side using only the
   first Hermite segment and one omitted Fourier mode k=(12,5,6); if this lower
   bound already exceeds one, the published sufficient criterion cannot certify
   this reconstruction;
2. computes conservative WHOLE-PATH Arb upper envelopes for the residual in
   W^{-1,2} and W^{-1,3}, using the certified low-mode Hermite-residual bound and
   Fourier inequalities for the omitted high-frequency residual.

Failure of the sufficient criterion is NOT evidence of blowup or singularity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from math import comb

import numpy as np
from flint import acb, arb, ctx

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
N14TOOLS = ROOT / "next-work" / "n14_same_datum" / "tools"
WITNESS = ROOT / "results" / "wp16_n17_holdout" / "wp16_036_sparse_turnover_112_pairs.json"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(N14TOOLS))

import wp16_036_sparse_turnover_exact_anchor as exact
from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import arb_segment_n14 as seg

EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_NODES = "e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0"
EXPECTED_RHS = "f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253"
EXPECTED_N14_ARTIFACT_SHA = "b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698"
CERTIFIED_LOW_RESIDUAL_MAX = "0.000216927907"
TARGET_K = (12, 5, 6)
NU = "0.1"
H = "0.000025"
T = "0.003"
STEPS = 120
CPI1 = 14
CPI2 = 35
CE1 = 24
CE2 = 22


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def au(x):
    return arb(x.abs_upper())


def al(x):
    return arb(x.abs_lower())


def vector_norm_upper(row):
    s = arb(0)
    for z in row:
        q = au(z)
        s += q * q
    return s.sqrt().upper()


def vector_norm_lower(row):
    s = arb(0)
    for z in row:
        q = al(z)
        s += q * q
    return s.sqrt().lower()


def state_l2_upper(state):
    s = arb(0)
    for row in state:
        q = arb(vector_norm_upper(row))
        s += q * q
    return s.sqrt().upper()


def state_l2_lower(state):
    s = arb(0)
    for row in state:
        for z in row:
            q = al(z)
            s += q * q
    return s.sqrt().lower()


def state_hdot1_upper(state, square):
    s = arb(0)
    for row, kk in zip(state, square):
        rr = arb(0)
        for z in row:
            q = au(z)
            rr += q * q
        s += int(kk) * rr
    return s.sqrt().upper()


def state_coeff_l1_upper(state):
    s = arb(0)
    for row in state:
        s += arb(vector_norm_upper(row))
    return s.upper()


def state_sub(a, b, scale=1):
    return [[scale * (a[i][j] - b[i][j]) for j in range(3)] for i in range(len(a))]


def state_add_scaled(a, b, scale):
    return [[a[i][j] + scale * b[i][j] for j in range(3)] for i in range(len(a))]


def hermite_bernstein_controls(system, a, b, f, g, h, exact_initial=None):
    A = seg.solenoidal_reality_projection(system, a)
    B = seg.solenoidal_reality_projection(system, b)
    F = seg.solenoidal_reality_projection(system, f)
    G = seg.solenoidal_reality_projection(system, g)
    if exact_initial is not None:
        A = seg.exact_rational_state(system, exact_initial)
    hh = arb(str(h))
    one_third = arb(1) / 3
    return [
        A,
        state_add_scaled(A, F, hh * one_third),
        state_add_scaled(B, G, -hh * one_third),
        B,
    ]


def target_bilinear(system, x, y, target):
    out = [acb(0), acb(0), acb(0)]
    k = tuple(int(v) for v in target)
    for pi, p in enumerate(system.modes):
        q = tuple(k[d] - int(p[d]) for d in range(3))
        qi = system.index.get(q)
        if qi is None:
            continue
        qdot = sum((x[pi][j] * int(q[j]) for j in range(3)), acb(0))
        for c in range(3):
            out[c] += acb(0, 1) * qdot * y[qi][c]
    kk = sum(v * v for v in k)
    kd = sum((out[j] * k[j] for j in range(3)), acb(0))
    return [out[j] - kd * k[j] / kk for j in range(3)]


def quadratic_bernstein_target(system, controls, target):
    pair = {}
    for i in range(4):
        for j in range(4):
            pair[i, j] = target_bilinear(system, controls[i], controls[j], target)
    out = []
    for r in range(7):
        row = [acb(0), acb(0), acb(0)]
        for i in range(4):
            j = r - i
            if not 0 <= j < 4:
                continue
            w = arb(comb(3, i) * comb(3, j)) / comb(6, r)
            for c in range(3):
                row[c] += w * pair[i, j][c]
        out.append(row)
    return out


def decimal_upper(x, places=12):
    return str(arb(x).upper())


def decimal_lower(x, places=12):
    return str(arb(x).lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    ctx.prec = 160
    artifact = args.artifact_dir.resolve()
    nodes_path = artifact / "nodes.npy"
    rhs_path = artifact / "rhs.npy"
    if sha(nodes_path) != EXPECTED_NODES:
        raise SystemExit("nodes.npy hash mismatch")
    if sha(rhs_path) != EXPECTED_RHS:
        raise SystemExit("rhs.npy hash mismatch")
    if sha(WITNESS) != EXPECTED_WITNESS:
        raise SystemExit("witness hash mismatch")

    nodes = np.load(nodes_path, mmap_mode="r")
    rhs = np.load(rhs_path, mmap_mode="r")
    if nodes.shape[0] != STEPS + 1 or rhs.shape != nodes.shape:
        raise SystemExit("unexpected predictor shape")

    system = DealiasedSystem(14, nu=float(NU))
    if nodes.shape[1] != len(system.modes):
        raise SystemExit("mode count mismatch")
    field, _, witness_sha = exact.input_state(WITNESS)
    if witness_sha != EXPECTED_WITNESS:
        raise SystemExit("exact witness parser mismatch")

    pi = arb.pi()
    lam = 2 * pi
    h = arb(H)
    t_final = arb(T)
    h_unit = h / (lam * lam)
    T_unit = t_final / (lam * lam)
    nu = arb(NU)

    controls0 = hermite_bernstein_controls(
        system, nodes[0], nodes[1], rhs[0], rhs[1], H, exact_initial=field
    )

    u0_l2_lower = arb(state_l2_lower(controls0[0]))
    dcontrols = [state_sub(controls0[j + 1], controls0[j], scale=3) for j in range(3)]
    dtheta_l2_upper = max((arb(state_l2_upper(x)) for x in dcontrols), key=float)
    first_segment_l2_lower = (u0_l2_lower - dtheta_l2_upper).lower()
    if not first_segment_l2_lower > 0:
        raise SystemExit("failed to prove positive first-segment L2 lower bound")

    qbern = quadratic_bernstein_target(system, controls0, TARGET_K)
    g0_lower = arb(vector_norm_lower(qbern[0]))
    dgbern = [
        [6 * (qbern[j + 1][c] - qbern[j][c]) for c in range(3)]
        for j in range(6)
    ]
    dg_upper = max((arb(vector_norm_upper(x)) for x in dgbern), key=float)
    target_coeff_lower = (g0_lower - dg_upper).lower()
    if not target_coeff_lower > 0:
        raise SystemExit("target coefficient lower bound did not remain positive on segment 0")

    k2 = sum(v * v for v in TARGET_K)
    target_wm12_lower = (
        lam**3 * target_coeff_lower / (1 + lam**2 * k2).sqrt()
    ).lower()

    A_lower = (
        h_unit * (arb(1) / 2 + 1 / nu) * target_wm12_lower**2
    ).lower()

    U_l2_lower = (lam * first_segment_l2_lower).lower()
    quartic_coeff = arb(4) * (3**3) * (CE1**2) / (nu**3)
    logM_lower = (h_unit * quartic_coeff * U_l2_lower**4).lower()

    logB1 = (
        (arb(8) / 3) * arb(3).log()
        - (2 * nu).log()
        + 2 * arb(CPI1).log()
        + 2 * arb(CE1).log()
        + (1 + 2 / nu).log()
    )
    log_lhs_lower = (
        (8 * (1 + T_unit)).log()
        + logB1
        + (arb(2) / 3) * ((8 * A_lower).log() + logM_lower)
    ).lower()
    criterion_proven_false_for_reconstruction = bool(log_lhs_lower > 0)

    Rlow = arb(CERTIFIED_LOW_RESIDUAL_MAX)
    wm12_sq_integral_upper = arb(0)
    wm13_cube_integral_upper = arb(0)
    alpha_integral_upper = arb(0)
    max_w12_unit = arb(0)
    max_l2_unit = arb(0)
    max_l1_unit = arb(0)
    max_wm12 = arb(0)
    max_wm13 = arb(0)

    for step in range(STEPS):
        controls = hermite_bernstein_controls(
            system, nodes[step], nodes[step + 1], rhs[step], rhs[step + 1], H,
            exact_initial=field if step == 0 else None,
        )
        seg_l2 = arb(0)
        seg_w12 = arb(0)
        seg_l1 = arb(0)
        for st in controls:
            l2 = arb(state_l2_upper(st))
            h1 = arb(state_hdot1_upper(st, system.square))
            w12_unit = lam * (l2*l2 + lam*lam*h1*h1).sqrt()
            l2_unit = lam * l2
            l1_unit = lam * arb(state_coeff_l1_upper(st))
            seg_l2 = seg_l2.max(l2_unit)
            seg_w12 = seg_w12.max(w12_unit)
            seg_l1 = seg_l1.max(l1_unit)

        L6 = CE1 * seg_w12
        low_unit_l2 = lam**3 * Rlow
        tail_wm12 = seg_l2.sqrt() * L6 * L6.sqrt()
        g2 = low_unit_l2 + tail_wm12
        g3 = CE2 * low_unit_l2 + seg_l1**2

        alpha = (
            4 + nu / 3
            + (4 * CE1 / nu) * L6**2
            + (4 * (3**3) * (CE1**2) / (nu**3)) * L6**4
        )
        wm12_sq_integral_upper += h_unit * g2**2
        wm13_cube_integral_upper += h_unit * g3**3
        alpha_integral_upper += h_unit * alpha
        max_w12_unit = max_w12_unit.max(seg_w12)
        max_l2_unit = max_l2_unit.max(seg_l2)
        max_l1_unit = max_l1_unit.max(seg_l1)
        max_wm12 = max_wm12.max(g2)
        max_wm13 = max_wm13.max(g3)

        if step % 20 == 0:
            print("segment", step, "whole-path envelope", flush=True)

    A_upper = (
        (arb(CPI2)**3 / 3) * (1 + arb(2)**4 / (nu * nu.sqrt())) * wm13_cube_integral_upper
        + (arb(1)/2 + 1/nu) * wm12_sq_integral_upper
    )

    logB2 = (
        (arb(7) / 3) * arb(3).log()
        - (2 * nu).log()
        + 2 * arb(CPI1).log()
        + 4 * arb(CE1).log()
        + (1 + 2 / nu).log()
        + 2 * max_w12_unit.log()
    )
    log8AM_upper = (8 * A_upper).log() + alpha_integral_upper
    logterm1 = logB1 + (arb(2)/3) * log8AM_upper
    logterm2 = logB2 + (arb(1)/3) * log8AM_upper
    log_sum_upper = logterm1.max(logterm2) + arb(2).log()
    log_lhs_upper = (8 * (1 + T_unit)).log() + log_sum_upper

    result = {
        "schema": "wp19-v0.16-bgt-arb-screen-v1",
        "status": "ARBITRARY-PRECISION WHOLE-SEGMENT SCREEN",
        "source_theorem": {
            "paper": "Brunk-Giesselmann-Tscherpel, A posteriori existence of strong solutions to the Navier-Stokes equations in 3D, arXiv:2509.25105",
            "constants_used": {"cPi1": CPI1, "cPi2": CPI2, "ce1": CE1, "ce2": CE2},
            "domain_conversion": "U(y,s)=2*pi*u(2*pi*y,4*pi^2*s), preserving nu=0.1",
        },
        "provenance": {
            "witness_sha256": EXPECTED_WITNESS,
            "nodes_sha256": EXPECTED_NODES,
            "rhs_sha256": EXPECTED_RHS,
            "N14_workflow_artifact_sha256": EXPECTED_N14_ARTIFACT_SHA,
            "certified_low_mode_residual_L2_max": CERTIFIED_LOW_RESIDUAL_MAX,
        },
        "first_segment_rigorous_lower_gate": {
            "target_high_mode": list(TARGET_K),
            "target_squared_norm": k2,
            "initial_original_L2_lower": decimal_lower(u0_l2_lower),
            "first_segment_state_variation_L2_upper": decimal_upper(dtheta_l2_upper),
            "first_segment_original_L2_lower": decimal_lower(first_segment_l2_lower),
            "target_tail_coeff_at_theta0_L2_lower": decimal_lower(g0_lower),
            "target_tail_coeff_theta_derivative_L2_upper": decimal_upper(dg_upper),
            "target_tail_coeff_whole_segment_L2_lower": decimal_lower(target_coeff_lower),
            "target_unit_Wminus1_2_whole_segment_lower": decimal_lower(target_wm12_lower),
            "A_lower_from_single_mode_first_segment": decimal_lower(A_lower),
            "logM_lower_from_first_segment_L2_only": decimal_lower(logM_lower),
            "log_BGT_condition_LHS_lower": decimal_lower(log_lhs_lower),
            "criterion_condition_42_proven_false_for_this_reconstruction": criterion_proven_false_for_reconstruction,
        },
        "whole_path_rigorous_upper_envelope": {
            "unit_torus_T": decimal_upper(T_unit),
            "max_U_L2_upper": decimal_upper(max_l2_unit),
            "max_U_W1_2_upper": decimal_upper(max_w12_unit),
            "max_U_fourier_l1_upper": decimal_upper(max_l1_unit),
            "max_full_residual_Wminus1_2_upper": decimal_upper(max_wm12),
            "max_full_residual_Wminus1_3_upper": decimal_upper(max_wm13),
            "integral_residual_Wminus1_2_squared_upper": decimal_upper(wm12_sq_integral_upper),
            "integral_residual_Wminus1_3_cubed_upper": decimal_upper(wm13_cube_integral_upper),
            "A_upper": decimal_upper(A_upper),
            "logM_upper": decimal_upper(alpha_integral_upper),
            "log_BGT_condition_LHS_upper": decimal_upper(log_lhs_upper),
        },
        "decision": (
            "PUBLISHED_BGT_SUFFICIENT_CRITERION RIGOROUSLY FAILS FOR THIS PARTICULAR "
            "N14 HERMITE RECONSTRUCTION" if criterion_proven_false_for_reconstruction
            else "LOWER SCREEN INCONCLUSIVE"
        ),
        "claim_boundary": (
            "Failure of this sufficient a-posteriori criterion does not imply blowup, singularity, "
            "or failure of continuum strong existence. It only rules out certification by this "
            "specific reconstruction and the stated published constants/criterion."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
