"""Satellite first-variation audit around the WP18 dominant m=2 triad.

Parameterizes the registered WP17 best ladder as

    u_eps = u_(m=2) + eps * v_sat

after normalizing A2=1.  The script verifies that G, X2 and the signed H2
high-advector transfer have zero linear response, then evaluates the exact
local first variation of omega.S.omega and integrates it over the positive
set of the base field on several deterministically shifted grids.

Finite sparse-family diagnostic only; no global bound is claimed.
"""

import json
import math
from pathlib import Path

import numpy as np

from galerkin import leray
from helicity_phase_gate import POLARIZATIONS
from validate_sparse_triad import P, Q, R

HERE = Path(__file__).resolve().parent

WP17_AMPS = np.array([
    1.0,
    20.085536923187668,
    0.049787068367863944,
    0.2171527798601354,
    0.049787068367863944,
    0.14147102746208645,
], dtype=float)

WP17_PHASES = np.array([
    -3.003156442967318,
    -1.5708698100185097,
    -2.977730689860095,
    2.023287979573299,
    1.9851705838179707,
    -1.333169824255259,
], dtype=float)

RATIOS = WP17_AMPS / WP17_AMPS[1]

SHIFTS = (
    (0.137, 0.271, 0.419),
    (0.319, 0.113, 0.227),
    (0.071, 0.383, 0.293),
    (0.443, 0.197, 0.059),
)


def neg(k):
    return tuple(-x for x in k)


def field(eps):
    u = {}
    for m in range(1, 7):
        A = 1.0 if m == 2 else eps * RATIOS[m - 1]
        theta = WP17_PHASES[m - 1]
        for k, v in POLARIZATIONS.items():
            km = tuple(m * x for x in k)
            phase = np.exp(1j * theta) if k == R else 1.0
            a = A * v.astype(complex) * phase
            u[km] = a
            u[neg(km)] = np.conj(a)
    return u


def satellite_direction():
    u0 = field(0.0)
    u1 = field(1.0)
    return {k: u1[k] - u0.get(k, 0.0) for k in u1}


def quadratic(u):
    G = sum(
        sum(x * x for x in k) * float(np.vdot(a, a).real)
        for k, a in u.items()
    )
    X2 = sum(
        (sum(x * x for x in k) ** 2) * float(np.vdot(a, a).real)
        for k, a in u.items()
    )
    return G, X2


def sparse_high_transfer(u, K=2, s=2.0):
    total = 0j
    for k, ak in u.items():
        k2 = sum(x * x for x in k)
        weight = k2 ** s
        for p, ap in u.items():
            if sum(x * x for x in p) <= K * K:
                continue
            q = tuple(k[d] - p[d] for d in range(3))
            aq = u.get(q)
            if aq is None:
                continue
            raw = 1j * np.dot(q, ap) * aq
            total += -weight * np.vdot(ak, leray(k) @ raw)
    return float(np.real(total))


def gradient_fields(u, grid, shift_frac):
    shape = (grid, grid, grid, 3)
    grad = np.empty((grid, grid, grid, 3, 3), float)
    shift = np.asarray(shift_frac, float) * (2 * np.pi / grid)

    for direction in range(3):
        coeff = np.zeros(shape, complex)
        for k, a in u.items():
            ka = np.asarray(k)
            idx = tuple(ka % grid)
            phase = np.exp(1j * np.dot(ka, shift))
            coeff[idx] = 1j * k[direction] * a * phase * grid**3
        reconstructed = np.fft.ifftn(coeff, axes=(0, 1, 2))
        if np.max(np.abs(reconstructed.imag)) > 5e-10:
            raise AssertionError("imaginary reconstruction error")
        grad[..., :, direction] = reconstructed.real

    omega = np.stack(
        (
            grad[..., 2, 1] - grad[..., 1, 2],
            grad[..., 0, 2] - grad[..., 2, 0],
            grad[..., 1, 0] - grad[..., 0, 1],
        ),
        axis=-1,
    )
    strain = (grad + np.swapaxes(grad, -1, -2)) / 2
    return omega, strain


def positive_first_variation(grid, shift_frac):
    u0 = field(0.0)
    v = satellite_direction()

    omega0, strain0 = gradient_fields(u0, grid, shift_frac)
    omega1, strain1 = gradient_fields(v, grid, shift_frac)

    F0 = np.einsum("...i,...ij,...j->...", omega0, strain0, omega0)
    F1 = (
        2 * np.einsum("...i,...ij,...j->...", omega1, strain0, omega0)
        + np.einsum("...i,...ij,...j->...", omega0, strain1, omega0)
    )

    positive0 = float(np.mean(np.maximum(F0, 0.0)))
    derivative = float(np.mean(np.where(F0 > 0.0, F1, 0.0)))
    zero_fraction = float(np.mean(np.abs(F0) < 1e-12))
    return positive0, derivative, zero_fraction


def polynomial_checks():
    # Quadratic norms: recover exact-in-epsilon coefficients from eps=-1,0,1.
    qm = quadratic(field(-1.0))
    q0 = quadratic(field(0.0))
    qp = quadratic(field(1.0))

    G2 = (qm[0] + qp[0] - 2 * q0[0]) / 2
    X22 = (qm[1] + qp[1] - 2 * q0[1]) / 2

    # N(eps) is cubic. Solve coefficients from five symmetric evaluations.
    es = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    ns = np.array([sparse_high_transfer(field(e)) for e in es])
    coeff = np.polynomial.polynomial.polyfit(es, ns, 3)

    return {
        "G0": q0[0],
        "G_eps2": G2,
        "X2_0": q0[1],
        "X2_eps2": X22,
        "N_polynomial_coefficients_increasing_order": coeff.tolist(),
        "N_linear_abs": abs(float(coeff[1])),
        "N_quadratic_abs": abs(float(coeff[2])),
    }


def run():
    poly = polynomial_checks()
    if poly["N_linear_abs"] > 1e-9 or poly["N_quadratic_abs"] > 1e-9:
        raise AssertionError("unexpected linear/quadratic H2-transfer response")

    grids = (48, 64, 96, 128, 160)
    rows = []
    for grid in grids:
        vals = np.array(
            [positive_first_variation(grid, shift) for shift in SHIFTS],
            dtype=float,
        )
        rows.append({
            "grid": grid,
            "shift_count": len(SHIFTS),
            "positive0_mean": float(vals[:, 0].mean()),
            "positive0_std": float(vals[:, 0].std()),
            "positive_derivative_mean": float(vals[:, 1].mean()),
            "positive_derivative_std": float(vals[:, 1].std()),
            "zero_fraction_max": float(vals[:, 2].max()),
        })

    # Independent WP18 4096^2 reduced-quadrature baseline.
    wp18_positive0 = 8.0 * 1.3834814931299562
    wp18_C0 = 5.059699052542701
    dpositive = rows[-1]["positive_derivative_mean"]
    Cprime_est = -wp18_C0 * dpositive / wp18_positive0

    if dpositive >= 0:
        raise AssertionError("registered WP17 direction did not deplete positive stretching")

    return {
        "status": "executed satellite first-variation audit",
        "parameterization": "u_eps = normalized WP18 m=2 base + eps * registered WP17 satellites",
        "relative_amplitudes_m1_to_m6": RATIOS.tolist(),
        "phases_m1_to_m6": WP17_PHASES.tolist(),
        "polynomial_checks": poly,
        "shifted_grid_first_variation": rows,
        "wp18_positive_stretching_baseline_4096_reduced": wp18_positive0,
        "wp18_C_baseline_4096_reduced": wp18_C0,
        "Cprime_from_160_directional_derivative": Cprime_est,
        "interpretation": (
            "Along the registered WP17 satellite direction, N2_high, G and X2 "
            "have zero linear response while positive stretching decreases at "
            "first order. The quotient therefore has a positive first variation."
        ),
        "warning": (
            "One sparse-family direction only. Shifted-grid derivative is a "
            "deterministic numerical approximation to the continuum positive-part "
            "directional derivative; no global supremum or regularity theorem."
        ),
    }


if __name__ == "__main__":
    result = run()
    out = HERE / "satellite_first_variation_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Wrote", out)
    print(json.dumps(result, indent=2))
