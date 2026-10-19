#!/usr/bin/env python3
"""WP19 v0.26 -- signed-C500 numerator Hermite goal-adjoint design gate.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

Floating/pre-interval verification only. The endpoint objective is the single
fixed smooth polynomial obtained after freezing the prospective N13 K36 sign
chart and the portable C500 rank/orbit/sign coalition. The script:
  * verifies both frozen identities fail-closed;
  * verifies the floating endpoint polynomial against the exact-rational
    v0.25b nominal signed-numerator certificates;
  * checks that all 36 endpoint K36 signs match the frozen chart;
  * propagates the terminal polynomial gradient with the v0.23 analytic
    dealiased VJP and half-step RK4 along the lower cubic-Hermite path;
  * pairs the adjoint with the full Hermite reconstruction residual by Simpson;
  * measures endpoint/dynamic remainders and a conservative quadratic
    nonlinear-radius envelope;
  * reports every transfer budget against the rigorous negative numerator
    margin already certified by v0.25b.

This is not an interval adjoint certificate and proves no all-N theorem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

H = 0.000025
NU = 0.1
STEPS = 120
P = (3, 2, 2)
Q = (3, -2, 1)
K = (6, 0, 3)
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36 = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART = "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC = "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def c500_semantic_sha(path: Path):
    obj = json.loads(path.read_text())
    rows = obj["keys"]
    semantic = {
        "schema": "wp19-c500-semantic-identity-v1",
        "coalition_size": int(obj["coalition_size"]),
        "keys": [
            {
                "rank": int(r["rank_from_N11_endpoint"]),
                "left_orbit": [int(x) for x in r["left_orbit"]],
                "right_orbit": [int(x) for x in r["right_orbit"]],
                "fixed_linear_sign": int(r["fixed_linear_sign"]),
            }
            for r in rows
        ],
    }
    payload = (json.dumps(semantic, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(payload).hexdigest()


def load_coefficients(sign_chart: Path, c500_path: Path):
    if sha256(sign_chart) != EXPECTED_SIGN_CHART:
        raise ValueError("frozen K36 sign-chart SHA mismatch")
    s = json.loads(sign_chart.read_text())
    if s.get("K36_sha256") != EXPECTED_K36 or len(s.get("keys", [])) != 36:
        raise ValueError("frozen K36 sign-chart identity mismatch")

    sem = c500_semantic_sha(c500_path)
    c = json.loads(c500_path.read_text())
    if sem != EXPECTED_C500_SEMANTIC or int(c.get("coalition_size", -1)) != 500:
        raise ValueError("portable C500 semantic identity mismatch")

    coeff = {}
    k36_signs = {}
    for r in s["keys"]:
        key = (tuple(r["left_orbit"]), tuple(r["right_orbit"]))
        sig = int(r["fixed_numerator_sign"])
        if sig not in (-1, 1) or key in coeff:
            raise ValueError("invalid frozen K36 sign chart")
        coeff[key] = sig
        k36_signs[key] = sig

    c500_signs = {}
    for r in c["keys"]:
        key = (tuple(r["left_orbit"]), tuple(r["right_orbit"]))
        tau = int(r["fixed_linear_sign"])
        if tau not in (-1, 1) or key in coeff:
            raise ValueError("invalid/disjoint C500 coalition")
        coeff[key] = -9 * tau
        c500_signs[key] = tau

    return coeff, k36_signs, c500_signs, sem


def numpy_signed_numerator(system, a, coeff):
    a = np.asarray(a, dtype=np.complex128)
    pi, qi, ki = (system.index[x] for x in (P, Q, K))
    Pk = system.projectors[ki]
    weight = float(system.square[ki] ** 2)
    B = Pk @ (1j * np.dot(np.asarray(Q, float), a[pi]) * a[qi])
    z = -weight * np.vdot(a[ki], B)

    groups = {}
    wanted = set(coeff)
    for li0, ri0 in zip(system.left, system.right):
        li = int(li0)
        ri = int(ri0)
        key = (orbit(system.modes[li]), orbit(system.modes[ri]))
        if key not in wanted:
            continue
        raw = 1j * np.dot(system.waves[ri], a[li]) * a[ri]
        d = -(Pk @ raw)
        groups[key] = groups.get(key, np.zeros(3, dtype=np.complex128)) + d

    if set(groups) != wanted:
        missing = wanted - set(groups)
        raise ValueError(f"objective support missing {len(missing)} frozen groups")

    nvals = {}
    J = 0.0
    for key, c in coeff.items():
        w = -weight * np.vdot(groups[key], B)
        n = float(np.imag(w * np.conj(z)))
        nvals[key] = n
        J += float(c) * n
    return float(J), nvals


def torch_terminal_gradient(system, a_np, coeff, tangent_project):
    import torch

    torch.set_default_dtype(torch.float64)
    a = torch.tensor(np.asarray(a_np), dtype=torch.complex128, requires_grad=True)
    Pk = torch.tensor(
        system.projectors[system.index[K]], dtype=torch.float64
    ).to(torch.complex128)
    qwave = torch.tensor(Q, dtype=torch.float64).to(torch.complex128)
    pi, qi, ki = (system.index[x] for x in (P, Q, K))
    weight = float(system.square[ki] ** 2)

    B = Pk @ (1j * torch.sum(qwave * a[pi]) * a[qi])
    z = -weight * torch.vdot(a[ki], B)

    groups = {}
    wanted = set(coeff)
    for li0, ri0 in zip(system.left, system.right):
        li = int(li0)
        ri = int(ri0)
        key = (orbit(system.modes[li]), orbit(system.modes[ri]))
        if key not in wanted:
            continue
        wave = torch.tensor(system.waves[ri], dtype=torch.float64).to(torch.complex128)
        raw = 1j * torch.sum(wave * a[li]) * a[ri]
        d = -(Pk @ raw)
        groups[key] = groups.get(key, 0.0) + d

    if set(groups) != wanted:
        raise ValueError("torch objective support mismatch")

    J = None
    for key, c in coeff.items():
        w = -weight * torch.vdot(groups[key], B)
        n = torch.imag(w * torch.conj(z))
        term = float(c) * n
        J = term if J is None else J + term
    if J is None:
        raise ValueError("empty objective")
    J.backward()
    g = a.grad.detach().cpu().numpy()
    return float(J.detach().cpu().numpy()), tangent_project(system, g)


def hermite_derivative(a0, a1, f0, f1, theta):
    t = float(theta)
    dh00 = 6 * t * t - 6 * t
    dh10 = 3 * t * t - 4 * t + 1
    dh01 = -6 * t * t + 6 * t
    dh11 = 3 * t * t - 2 * t
    return (dh00 * a0 + dh01 * a1) / H + dh10 * f0 + dh11 * f1


def segment_value(v23, nodes, rhs, j, theta):
    return v23.hermite(
        np.asarray(nodes[j]), np.asarray(nodes[j + 1]),
        np.asarray(rhs[j]), np.asarray(rhs[j + 1]), theta
    )


def halfgrid_error_schedule(directory: Path):
    node = np.zeros(STEPS + 1, dtype=np.float64)
    half = np.zeros(2 * STEPS + 1, dtype=np.float64)
    sqrt2 = math.sqrt(2.0)
    half[0] = 0.0
    for j in range(STEPS):
        row = json.loads((directory / f"{j:03d}.json").read_text())
        R = float(row["residual_L2_upper_decimal"])
        M = float(row["gradient_Fourier_l1_upper_decimal"])
        S = M / sqrt2
        tau = H / 2
        half[2 * j] = node[j]
        half[2 * j + 1] = math.exp(S * tau) * (node[j] + tau * R)
        node[j + 1] = math.exp(S * H) * (node[j] + H * R)
        half[2 * j + 2] = node[j + 1]
    return half


def simpson(values):
    values = np.asarray(values, dtype=np.float64)
    if len(values) != 2 * STEPS + 1:
        raise ValueError("Simpson grid length mismatch")
    return float(
        (H / 6.0)
        * sum(
            values[2 * j] + 4 * values[2 * j + 1] + values[2 * j + 2]
            for j in range(STEPS)
        )
    )


def grad_fourier_l1(system, lam):
    per = np.linalg.norm(np.asarray(lam), axis=1)
    return float(np.sum(np.sqrt(system.square.astype(np.float64)) * per))


def sign_map(nvals, keys):
    return {key: (1 if nvals[key] > 0 else -1 if nvals[key] < 0 else 0) for key in keys}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--lower-dir", type=Path, required=True)
    ap.add_argument("--higher-dir", type=Path, required=True)
    ap.add_argument("--sign-chart", type=Path, required=True)
    ap.add_argument("--c500", type=Path, required=True)
    ap.add_argument("--lower-cert", type=Path, required=True)
    ap.add_argument("--higher-cert", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    sys.path.insert(0, str((args.repo / "src").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    M = args.M
    low = DealiasedSystem(M, nu=NU)
    high = DealiasedSystem(M + 1, nu=NU)
    fixed = DealiasedSystem(11, nu=NU)
    coeff, k36_signs, _, c500_sem = load_coefficients(args.sign_chart, args.c500)

    for directory, N in ((args.lower_dir, M), (args.higher_dir, M + 1)):
        meta = json.loads((directory / "metadata.json").read_text())
        if (
            meta["N"] != N
            or meta["witness_sha256"] != EXPECTED_WITNESS
            or meta["K36_keys_sha256"] != EXPECTED_K36
        ):
            raise ValueError("predictor metadata mismatch")

    lo_cert = json.loads(args.lower_cert.read_text())
    hi_cert = json.loads(args.higher_cert.read_text())
    for cert, N in ((lo_cert, M), (hi_cert, M + 1)):
        if cert.get("N") != N or cert.get("status") != "PASS":
            raise ValueError("v0.25b endpoint certificate mismatch")
        if cert.get("C500_semantic_sha256") != EXPECTED_C500_SEMANTIC:
            raise ValueError("v0.25b C500 semantic mismatch")
        if cert.get("K36_sign_locked_count") != 36:
            raise ValueError("v0.25b K36 sign lock missing")
        if not cert.get("certified_signed_numerator_negative"):
            raise ValueError("v0.25b negative numerator certificate missing")

    lo_nodes = np.load(args.lower_dir / "nodes.npy", mmap_mode="r")
    lo_rhs = np.load(args.lower_dir / "rhs.npy", mmap_mode="r")
    hi_nodes = np.load(args.higher_dir / "nodes.npy", mmap_mode="r")
    hi_rhs = np.load(args.higher_dir / "rhs.npy", mmap_mode="r")
    if len(lo_nodes) != STEPS + 1 or len(hi_nodes) != STEPS + 1:
        raise ValueError("unexpected node count")

    idx11_low = np.asarray([low.index[k] for k in fixed.modes], dtype=np.int64)
    idx11_high = np.asarray([high.index[k] for k in fixed.modes], dtype=np.int64)
    base11 = v23.physical_project(fixed, np.asarray(lo_nodes[-1, idx11_low]))
    target11 = v23.physical_project(fixed, np.asarray(hi_nodes[-1, idx11_high]))

    base_J, base_n = numpy_signed_numerator(fixed, base11, coeff)
    target_J, target_n = numpy_signed_numerator(fixed, target11, coeff)
    base_ref = float(lo_cert["nominal_signed_numerator_decimal"])
    target_ref = float(hi_cert["nominal_signed_numerator_decimal"])
    base_ref_rel = abs(base_J - base_ref) / max(1.0, abs(base_ref))
    target_ref_rel = abs(target_J - target_ref) / max(1.0, abs(target_ref))
    if max(base_ref_rel, target_ref_rel) > 5e-11:
        raise ValueError(("floating/exact nominal signed-numerator mismatch", base_ref_rel, target_ref_rel))

    base_signs = sign_map(base_n, k36_signs)
    target_signs = sign_map(target_n, k36_signs)
    if base_signs != k36_signs or target_signs != k36_signs:
        raise ValueError("endpoint K36 sign differs from frozen prospective chart")

    torch_J, grad11 = torch_terminal_gradient(
        fixed, base11, coeff, v23.tangent_project
    )
    torch_rel = abs(torch_J - base_J) / max(1.0, abs(base_J))
    if torch_rel > 5e-12:
        raise ValueError(("torch/numpy signed numerator mismatch", torch_J, base_J))

    delta11 = target11 - base11
    endpoint_linear = float(np.real(np.vdot(grad11.ravel(), delta11.ravel())))
    actual = float(target_J - base_J)
    endpoint_remainder = float(actual - endpoint_linear)
    eT = float(np.linalg.norm(delta11.ravel()))
    observed_directional_curvature = (
        2.0 * abs(endpoint_remainder) / (eT * eT) if eT > 0 else 0.0
    )

    dn = eT
    if dn == 0:
        raise ValueError("zero endpoint direction")
    direction = delta11 / dn
    eps = 1e-7
    fp, _ = numpy_signed_numerator(
        fixed, v23.physical_project(fixed, base11 + eps * direction), coeff
    )
    fm, _ = numpy_signed_numerator(
        fixed, v23.physical_project(fixed, base11 - eps * direction), coeff
    )
    fd = (fp - fm) / (2 * eps)
    ad = float(np.real(np.vdot(grad11.ravel(), direction.ravel())))
    grad_check_rel = abs(fd - ad) / max(1.0, abs(fd), abs(ad))
    if grad_check_rel > 2e-5:
        raise ValueError(("signed numerator gradient directional check failed", fd, ad, grad_check_rel))

    high_idx11 = np.asarray([high.index[k] for k in fixed.modes], dtype=np.int64)
    lam = np.zeros((len(high.modes), 3), dtype=np.complex128)
    lam[high_idx11] = grad11
    lambdas = [None] * (2 * STEPS + 1)
    lambdas[-1] = lam.copy()

    def x_at(j, theta):
        return v23.embed(low, high, segment_value(v23, lo_nodes, lo_rhs, j, theta))

    dt = -H / 2.0
    for j in range(STEPS - 1, -1, -1):
        for sub in (1, 0):
            theta1 = (sub + 1) / 2.0
            theta0 = sub / 2.0
            thetam = 0.5 * (theta0 + theta1)
            u1 = x_at(j, theta1)
            um = x_at(j, thetam)
            u0 = x_at(j, theta0)
            k1 = v23.adjoint_rhs(high, u1, lam)
            k2 = v23.adjoint_rhs(high, um, lam + 0.5 * dt * k1)
            k3 = v23.adjoint_rhs(high, um, lam + 0.5 * dt * k2)
            k4 = v23.adjoint_rhs(high, u0, lam + dt * k3)
            lam = lam + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            lam = v23.physical_project(high, lam)
            lambdas[2 * j + sub] = lam.copy()
        if j % 20 == 0:
            print("M", M, "signed-numerator half-step adjoint segment", j, flush=True)

    err_low = halfgrid_error_schedule(args.lower_dir)
    err_high = halfgrid_error_schedule(args.higher_dir)

    dual_pair = np.empty(2 * STEPS + 1, dtype=np.float64)
    residual_norm = np.empty_like(dual_pair)
    lambda_grad_l1 = np.empty_like(dual_pair)
    e_nom = np.empty_like(dual_pair)
    e_upper_scout = np.empty_like(dual_pair)

    for n in range(2 * STEPS + 1):
        if n == 2 * STEPS:
            j = STEPS - 1
            theta = 1.0
        else:
            j = n // 2
            theta = 0.0 if n % 2 == 0 else 0.5

        lo = segment_value(v23, lo_nodes, lo_rhs, j, theta)
        lodot = hermite_derivative(
            np.asarray(lo_nodes[j]), np.asarray(lo_nodes[j + 1]),
            np.asarray(lo_rhs[j]), np.asarray(lo_rhs[j + 1]), theta
        )
        hi = segment_value(v23, hi_nodes, hi_rhs, j, theta)

        x = v23.embed(low, high, lo)
        xdot = v23.embed(low, high, lodot)
        r = high.rhs(x) - xdot
        y = np.asarray(hi)
        e = y - x

        residual_norm[n] = float(np.linalg.norm(r.ravel()))
        dual_pair[n] = float(np.real(np.vdot(lambdas[n].ravel(), r.ravel())))
        lambda_grad_l1[n] = grad_fourier_l1(high, lambdas[n])
        e_nom[n] = float(np.linalg.norm(e.ravel()))
        e_upper_scout[n] = e_nom[n] + err_low[n] + err_high[n]

    eta = simpson(dual_pair)
    nonlinear_bound_nominal = simpson(lambda_grad_l1 * e_nom * e_nom)
    nonlinear_bound_radius = simpson(lambda_grad_l1 * e_upper_scout * e_upper_scout)
    dynamic_observed = float(endpoint_linear - eta)

    base_cert_upper = float(lo_cert["true_signed_numerator_upper_decimal"])
    target_cert_upper = float(hi_cert["true_signed_numerator_upper_decimal"])
    if base_cert_upper >= 0 or target_cert_upper >= 0:
        raise ValueError("rigorous negative numerator margin missing")
    base_margin = -base_cert_upper
    target_margin = -target_cert_upper

    total_remainder = float(actual - eta)
    scout_total_budget = abs(eta) + nonlinear_bound_radius + abs(endpoint_remainder)
    out = {
        "schema": "wp19-v0.26-signed-c500-numerator-hermite-goal-adjoint-v1",
        "copyright": "Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "status": "NON-RIGOROUS SIGNED-NUMERATOR GOAL-ADJOINT / PRE-INTERVAL DESIGN GATE",
        "transition": f"{M}->{M+1}",
        "M": M,
        "objective": "fixed polynomial signed C500 numerator with prospective N13 K36 sign chart",
        "frozen": {
            "witness_sha256": EXPECTED_WITNESS,
            "K36_sha256": EXPECTED_K36,
            "K36_sign_chart_sha256": EXPECTED_SIGN_CHART,
            "C500_portable_semantic_sha256": c500_sem,
            "K36_sign_count": 36,
            "C500_count": 500,
        },
        "endpoint_identity": {
            "base_floating_J": base_J,
            "base_v0_25b_nominal_J": base_ref,
            "base_reference_relative_error": base_ref_rel,
            "target_floating_J": target_J,
            "target_v0_25b_nominal_J": target_ref,
            "target_reference_relative_error": target_ref_rel,
            "torch_vs_numpy_relative_error": torch_rel,
            "frozen_K36_signs_match_base": True,
            "frozen_K36_signs_match_target": True,
        },
        "actual_delta_signed_numerator": actual,
        "endpoint_gradient_linear_prediction": endpoint_linear,
        "endpoint_taylor_remainder_observed": endpoint_remainder,
        "endpoint_nominal_difference_L2": eT,
        "observed_directional_curvature_2R_over_e2": observed_directional_curvature,
        "objective_gradient_directional_check_relative_error": grad_check_rel,
        "hermite_simpson_dual_prediction": eta,
        "total_remainder_actual_minus_dual": total_remainder,
        "total_remainder_over_base_certified_margin": abs(total_remainder) / base_margin,
        "actual_transfer_over_base_certified_margin": abs(actual) / base_margin,
        "positive_actual_transfer_over_base_certified_margin": max(actual, 0.0) / base_margin,
        "full_reconstruction_residual_max_L2": float(residual_norm.max()),
        "adjoint": {
            "terminal_L2": float(np.linalg.norm(lambdas[-1].ravel())),
            "initial_L2": float(np.linalg.norm(lambdas[0].ravel())),
            "gradient_Fourier_l1_max": float(lambda_grad_l1.max()),
            "gradient_Fourier_l1_simpson_integral": simpson(lambda_grad_l1),
        },
        "state_difference": {
            "nominal_max_halfgrid_L2": float(e_nom.max()),
            "radius_augmented_max_halfgrid_L2_scout": float(e_upper_scout.max()),
            "nominal_endpoint_L2": float(e_nom[-1]),
            "radius_augmented_endpoint_L2_scout": float(e_upper_scout[-1]),
        },
        "nonlinear_dynamic_remainder_candidate": {
            "identity_bound": "|<lambda,B(e,e)>| <= ||grad lambda||_infty ||e||_2^2 <= (sum_k |k||lambda_k||_2)||e||_2^2",
            "nominal_simpson_bound": nonlinear_bound_nominal,
            "radius_augmented_simpson_bound_scout": nonlinear_bound_radius,
            "observed_abs_dynamic_remainder": abs(dynamic_observed),
            "radius_bound_over_observed": nonlinear_bound_radius / max(abs(dynamic_observed), 1e-30),
            "radius_bound_over_base_certified_margin": nonlinear_bound_radius / base_margin,
        },
        "margin": {
            "base_v0_25b_true_signed_numerator_upper": base_cert_upper,
            "base_rigorous_negative_margin": base_margin,
            "target_v0_25b_true_signed_numerator_upper": target_cert_upper,
            "target_rigorous_negative_margin": target_margin,
            "scout_total_abs_dual_plus_nonlinear_plus_observed_endpoint_remainder": scout_total_budget,
            "scout_total_budget_over_base_certified_margin": scout_total_budget / base_margin,
        },
        "method": "Fixed-sign/fixed-C500 P11 polynomial terminal objective; complex128 PyTorch reverse-mode terminal gradient cross-checked against NumPy and a centered directional derivative; half-step RK4 continuous adjoint along the lower cubic-Hermite reconstruction; full reconstruction residual f_high(E ubar)-E ubar_dot; per-segment Simpson dual quadrature; certified trajectory-radius decimals replayed in binary64 only for scout budgeting.",
        "claim_boundary": "Floating pre-interval design result only. Adjoint propagation, Simpson quadrature, midpoint radius replay, gradient-l1 envelope, and endpoint Taylor control are not interval-enclosed. No all-N or continuum theorem.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "transition": out["transition"],
        "base_J": base_J,
        "target_J": target_J,
        "actual_delta_J": actual,
        "dual": eta,
        "remainder_over_margin": out["total_remainder_over_base_certified_margin"],
        "nonlinear_radius_over_margin": out["nonlinear_dynamic_remainder_candidate"]["radius_bound_over_base_certified_margin"],
        "scout_total_budget_over_margin": out["margin"]["scout_total_budget_over_base_certified_margin"],
        "gradient_check_rel": grad_check_rel,
    }, indent=2))


if __name__ == "__main__":
    main()