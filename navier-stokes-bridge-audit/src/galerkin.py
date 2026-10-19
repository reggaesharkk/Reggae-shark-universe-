"""Finite Fourier-Galerkin operator for periodic 3D incompressible flow.

Fourier convention: u(x) = sum_k a[k] exp(i k.x) on [0, 2*pi)^3.
The volume-normalized L2 energy is 1/2 sum_k |a[k]|^2.
Only explicitly supplied modes enter the exact (non-aliased) convolution.
"""

from __future__ import annotations

from typing import Dict, Tuple
import numpy as np

Wave = Tuple[int, int, int]
Field = Dict[Wave, np.ndarray]


def leray(k: Wave) -> np.ndarray:
    """Orthogonal projection onto k-perpendicular vectors; P_0 = identity."""
    x = np.asarray(k, dtype=float)
    d = float(x @ x)
    return np.eye(3) if d == 0 else np.eye(3) - np.outer(x, x) / d


def modes_in_ball(N: int) -> list[Wave]:
    """Integer wavevectors with |k| <= N, including the zero mode."""
    return [(i, j, k) for i in range(-N, N + 1)
            for j in range(-N, N + 1) for k in range(-N, N + 1)
            if i * i + j * j + k * k <= N * N]


def nonlinear(u: Field, N: int) -> Field:
    """N_k = P_k [(u.grad)u]_k; no FFT wraparound or grid aliasing."""
    keys = modes_in_ball(N)
    out: Field = {}
    for k in keys:
        total = np.zeros(3, dtype=complex)
        for p, ap in u.items():
            q = tuple(k[d] - p[d] for d in range(3))
            aq = u.get(q)
            if aq is not None:
                total += 1j * np.dot(q, ap) * aq
        out[k] = leray(k) @ total
    return out


def nonlinear_on_support(u: Field) -> Field:
    """Compute quadratic coefficients only at occupied modes.

    Sufficient for instantaneous energy flux, because its inner product is
    weighted by a_k, and absent modes have a_k=0. It is NOT the full RHS:
    absent modes may acquire nonzero time derivatives.
    """
    out: Field = {}
    for k in u:
        total = np.zeros(3, dtype=complex)
        for p, ap in u.items():
            q = tuple(k[d] - p[d] for d in range(3))
            aq = u.get(q)
            if aq is not None:
                total += 1j * np.dot(q, ap) * aq
        out[k] = leray(k) @ total
    return out


def rhs(u: Field, N: int, nu: float) -> Field:
    n = nonlinear(u, N)
    return {k: -n[k] - nu * sum(x*x for x in k) * u.get(k, np.zeros(3, complex))
            for k in n}


def energy(u: Field, K: float) -> float:
    return 0.5 * sum(float(np.vdot(a, a).real) for k, a in u.items()
                     if sum(x*x for x in k) <= K*K)


def flux(u: Field, n: Field, K: float) -> float:
    """Pi_K = Re sum_{|k|<=K} conj(a_k).N_k; positive means outflow."""
    return sum(float(np.vdot(a, n[k]).real) for k, a in u.items()
               if sum(x*x for x in k) <= K*K)


def shell_transfer(u: Field, n: Field, K1: float, K2: float) -> float:
    """Signed nonlinear contribution to shell energy, K1 < |k| <= K2."""
    if not 0 <= K1 < K2:
        raise ValueError("Require 0 <= K1 < K2")
    return flux(u, n, K1) - flux(u, n, K2)


def dissipation(u: Field, K: float) -> float:
    return sum(sum(x*x for x in k) * float(np.vdot(a, a).real)
               for k, a in u.items() if sum(x*x for x in k) <= K*K)


def energy_derivative(u: Field, du: Field, K: float) -> float:
    return sum(float(np.vdot(a, du[k]).real) for k, a in u.items()
               if sum(x*x for x in k) <= K*K)


def sobolev_norm(u: Field, s: float) -> float:
    """Inhomogeneous periodic H^s norm for a real s (including fractional)."""
    return sum((1 + sum(x*x for x in k))**s * float(np.vdot(a, a).real)
               for k, a in u.items())**0.5


def gradient_norm(u: Field) -> float:
    return sum(sum(x*x for x in k) * float(np.vdot(a, a).real)
               for k, a in u.items())**0.5
