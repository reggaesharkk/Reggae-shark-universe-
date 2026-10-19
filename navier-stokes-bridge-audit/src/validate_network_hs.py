"""Seeded growing-mode check of a cutoff-independent H^2 flux bound."""

import json
import math
import numpy as np

from galerkin import (energy, flux, gradient_norm, leray,
                      nonlinear_on_support, sobolev_norm)

C0 = math.sqrt(4*math.pi**2 + math.pi**4/45)
C2 = math.sqrt(1 + C0*C0)  # Bound for the full Z^3 H^2 embedding sum.


def embedding_constant(s, N):
    return math.sqrt(sum((1+i*i+j*j+k*k)**(-s)
                         for i in range(-N, N+1)
                         for j in range(-N, N+1)
                         for k in range(-N, N+1)
                         if i*i+j*j+k*k <= N*N))


def negative(k):
    return tuple(-x for x in k)


def network(L, seed):
    """Conjugate-symmetric divergence-free cube of growing occupied modes."""
    rng = np.random.default_rng(seed)
    u = {}
    for i in range(-L, L+1):
        for j in range(-L, L+1):
            for k in range(-L, L+1):
                wave = (i, j, k)
                if wave == (0, 0, 0) or wave < negative(wave):
                    continue
                raw = rng.normal(size=3) + 1j*rng.normal(size=3)
                vector = (leray(wave) @ raw)/(1+sum(x*x for x in wave))**0.9
                u[wave] = vector
                u[negative(wave)] = np.conjugate(vector)
    # Fix E_total=1 across different network sizes.
    full_cutoff = math.sqrt(3)*L + 1e-9
    scale = math.sqrt(1/energy(u, full_cutoff))
    return {k: scale*a for k, a in u.items()}


def run():
    rows = []
    for L in (1, 2, 3):
        for seed in (20260923, 20260924, 20260925):
            u = network(L, seed)
            n = nonlinear_on_support(u)
            K = float(L)
            actual = abs(flux(u, n, K))
            bound = (math.sqrt(2*energy(u, K)) * C2
                     * sobolev_norm(u, 2) * gradient_norm(u))
            total = flux(u, n, math.sqrt(3)*L + 1e-9)
            assert bound > 0 and actual <= bound * (1+1e-11)
            assert abs(total) < 1e-9
            assert abs(energy(u, math.sqrt(3)*L + 1e-9)-1) < 1e-11
            rows.append({"cube_radius": L, "occupied_modes": len(u),
                         "seed": seed, "K": K, "absolute_low_flux": actual,
                         "H2": sobolev_norm(u, 2),
                         "bound": bound, "actual_over_bound": actual/bound,
                         "total_nonlinear_flux_error": abs(total)})
    return {"inequality": "|Pi_K| <= sqrt(2 E_low) * C2 * ||u||_H2 * ||grad u||_2",
            "cutoff_independent_C2_upper": C2,
            "finite_embedding_constants": {
                str(s): {str(N): embedding_constant(s, N)
                         for N in (2, 4, 8, 16)} for s in (1, 1.5, 2)},
            "rows": rows,
            "scope": "Numerical checks of a proven embedding bound, not evidence of global regularity."}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
