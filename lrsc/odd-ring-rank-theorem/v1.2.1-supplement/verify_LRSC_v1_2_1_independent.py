#!/usr/bin/env python3
"""Independent finite checks accompanying LRSC v1.2.1.

This is a numerical cross-check, not a proof. It does not import or call the
v1.2 verifier. It starts from the local-minimum definition, uses NumPy's DFT,
evaluates the finite cosine sum directly, and constructs the stated channels.
"""

from __future__ import annotations

import math
import numpy as np


AMPLITUDE = 0.5
RANK_RINGS = (9, 11, 13, 17, 25)
MAX_M = 401
ABS_TOL = 2e-14
RANK_RTOL = 1e-10


def direct_shedding(M: int) -> np.ndarray:
    """Evaluate j_t = X_t - min(X_{t-1}, X_t, X_{t+1}) literally."""
    i = np.arange(M)
    k = (M - 1) // 2
    X = 1.0 + AMPLITUDE * np.cos(2.0 * np.pi * k * i / M)
    return X - np.minimum.reduce((np.roll(X, 1), X, np.roll(X, -1)))


def compact_coefficient(M: int, r: int) -> float:
    """Evaluate the v1.2 residue formula using ordinary double precision."""
    alpha = math.pi / M
    denominator = math.sin((2 * r - 1) * alpha) * math.sin((2 * r + 1) * alpha)
    parity_cos = (-1.0 if r % 2 else 1.0) * math.cos(r * alpha)
    if M % 4 == 3:
        B = -math.sin(2 * alpha) * (parity_cos + math.sin(alpha / 2)) / (2 * denominator)
    else:
        B = -math.sin(alpha) * (
            parity_cos * math.cos(2 * r * alpha)
            + math.cos(alpha) * math.sin(alpha / 2)
        ) / denominator
    return 2 * AMPLITUDE * math.cos(alpha / 2) * B / M


def finite_sum_coefficient(j: np.ndarray, M: int, r: int) -> float:
    """Evaluate the finite Fourier sum from the spatial samples directly."""
    L = (M - 1) // 4
    return float(
        (j[0] + 2 * sum(j[2 * u] * math.cos(4 * math.pi * r * u / M)
                         for u in range(1, L + 1))) / M
    )


def numerical_rank(A: np.ndarray) -> int:
    """SVD rank after column normalization, with the stated relative tolerance."""
    norms = np.linalg.norm(A, axis=0)
    safe = np.where(norms > 0, norms, 1.0)
    singular_values = np.linalg.svd(A / safe, compute_uv=False)
    if singular_values.size == 0 or singular_values[0] == 0:
        return 0
    return int(np.sum(singular_values > RANK_RTOL * singular_values[0]))


def rank_checks() -> tuple[int, int]:
    cases = 0
    passes = 0
    for M in RANK_RINGS:
        k = (M - 1) // 2
        i = np.arange(M)
        jhat = np.fft.fft(direct_shedding(M)) / M
        q = np.arange(M)
        multiplier = np.cos(2 * np.pi * q / M) - 1.0

        for p in range(1, k + 1):
            mask = np.zeros(M, dtype=float)
            representatives = np.arange(p)
            mask[representatives] = 1.0
            mask[(-representatives) % M] = 1.0

            W = np.zeros((M, k + 1), dtype=float)
            W[:, 0] = mask * jhat[0].real
            for r in range(1, k + 1):
                W[:, r] = 2 * mask * jhat[r].real * np.cos(2 * np.pi * r * i / M)

            SW = np.fft.ifft(
                multiplier[:, None] * np.fft.fft(W, axis=0), axis=0
            ).real
            ok = numerical_rank(W) == p and numerical_rank(SW) == p
            cases += 1
            passes += int(ok)
    return cases, passes


def main() -> None:
    max_spatial = 0.0
    max_fft = 0.0
    max_finite_sum = 0.0
    coefficient_count = 0

    for M in range(9, MAX_M + 1, 2):
        alpha = math.pi / M
        k = (M - 1) // 2
        j = direct_shedding(M)

        # Compare the literal local-minimum result with the closed spatial form.
        t = np.arange(M)
        centered = np.where(t <= k, t, t - M)
        u = np.abs(centered)
        closed = np.zeros(M, dtype=float)
        closed[u == 0] = AMPLITUDE * (1 + math.cos(alpha))
        even_nonzero = (u > 0) & (u % 2 == 0)
        closed[even_nonzero] = AMPLITUDE * (
            np.cos(u[even_nonzero] * alpha)
            + np.cos((u[even_nonzero] - 1) * alpha)
        )
        max_spatial = max(max_spatial, float(np.max(np.abs(j - closed))))

        dft = np.fft.fft(j) / M
        for r in range(k):
            compact = compact_coefficient(M, r)
            direct_sum = finite_sum_coefficient(j, M, r)
            max_fft = max(max_fft, abs(float(dft[r].real) - compact))
            max_finite_sum = max(max_finite_sum, abs(direct_sum - compact))
            coefficient_count += 1

    rank_cases, rank_passes = rank_checks()
    print(f"rings_checked={((MAX_M - 9) // 2) + 1}")
    print(f"coefficients_checked={coefficient_count}")
    print(f"max_spatial_formula_abs_error={max_spatial:.17e}")
    print(f"max_direct_DFT_abs_error={max_fft:.17e}")
    print(f"max_direct_finite_sum_abs_error={max_finite_sum:.17e}")
    print(f"rank_cases={rank_cases}; rank_cases_passing={rank_passes}")
    print(f"rank_rings={list(RANK_RINGS)}; rank_relative_tolerance={RANK_RTOL:g}")
    print(f"coefficient_absolute_tolerance={ABS_TOL:g}")

    if max_fft >= ABS_TOL or max_finite_sum >= ABS_TOL:
        raise SystemExit("FAIL: Fourier cross-check exceeded stated tolerance")
    if rank_cases != 35 or rank_passes != rank_cases:
        raise SystemExit("FAIL: one or more finite rank checks failed")
    print("STATUS=PASS (finite corroboration only; not a proof)")


if __name__ == "__main__":
    main()
