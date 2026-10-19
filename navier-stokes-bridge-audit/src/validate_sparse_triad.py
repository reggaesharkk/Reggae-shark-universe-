"""Independent seeded sparse-triad checks of the Fourier energy budget."""

import json
import math
import numpy as np

from galerkin import (leray, nonlinear, rhs, energy, flux, dissipation,
                      energy_derivative)

SEED = 20260923
P = (1, 0, 0)
Q = (0, 1, 1)
R = (1, 1, 1)  # P + Q = R; squared lengths are 1, 2, 3.
N = 2
K = 1.2
NU = 0.07
TOL = 1e-10


def neg(k):
    return tuple(-x for x in k)


def make_field(seed=SEED):
    rng = np.random.default_rng(seed)
    u = {}
    for k in (P, Q, R):
        raw = rng.normal(size=3) + 1j*rng.normal(size=3)
        a = leray(k) @ raw
        u[k], u[neg(k)] = a, np.conjugate(a)
    return u


def check():
    u = make_field()
    n = nonlinear(u, N)
    du = rhs(u, N, NU)

    hermitian_error = max(np.linalg.norm(u[neg(k)] - np.conjugate(a))
                          for k, a in u.items())
    divergence_error = max(abs(np.dot(k, a)) for k, a in u.items())
    projected_error = max(abs(np.dot(k, a)) for k, a in n.items())
    total_flux = flux(u, n, N)
    low_flux = flux(u, n, K)
    # Independent two-pair enumeration for output P. Only (R,-Q) and
    # (-Q,R) contribute to this coefficient in the selected six-mode field.
    direct_p = 1j * leray(P) @ (
        np.dot(neg(Q), u[R]) * u[neg(Q)]
        + np.dot(R, u[neg(Q)]) * u[R])
    direct_triad_error = np.linalg.norm(n[P] - direct_p)
    low_budget_error = abs(energy_derivative(u, du, K)
                           + NU*dissipation(u, K) + low_flux)
    full_budget_error = abs(energy_derivative(u, du, N)
                            + NU*dissipation(u, N))
    high_flux = total_flux - low_flux

    # A deliberately overstrong estimate: |Pi_K| <= C * E_total, with C
    # independent of field amplitude. Pi scales cubically, E quadratically.
    # For a nonzero flux, scaling must eventually falsify every finite C.
    scale = 100.0
    scaled = {k: scale*a for k, a in u.items()}
    scaled_n = nonlinear(scaled, N)
    cubic_error = abs(flux(scaled, scaled_n, K) - scale**3*low_flux)
    e = energy(u, N)
    threshold_for_C1 = e / abs(low_flux) if low_flux else math.inf

    results = {
        "seed": SEED, "N": N, "K": K, "viscosity": NU,
        "triad": [P, Q, R], "hermitian_error": hermitian_error,
        "input_divergence_error": divergence_error,
        "projected_divergence_error": projected_error,
        "total_flux_should_be_zero": total_flux,
        "low_flux": low_flux, "high_flux": high_flux,
        "direct_triad_coefficient_error": direct_triad_error,
        "low_budget_error": low_budget_error,
        "full_budget_error": full_budget_error,
        "scaled_cubic_error": cubic_error,
        "energy_total": e,
        "C_equals_1_fails_for_amplitude_scale_above": threshold_for_C1,
        "at_scale_100_flux_over_total_energy":
            abs(flux(scaled, scaled_n, K))/energy(scaled, N),
    }
    assert hermitian_error < TOL and divergence_error < TOL
    assert projected_error < TOL and abs(total_flux) < TOL
    assert abs(low_flux) > 1e-6, "Chosen triad did not transfer energy"
    assert direct_triad_error < TOL
    assert abs(low_flux + high_flux) < TOL
    assert low_budget_error < TOL and full_budget_error < TOL
    assert cubic_error < 1e-6
    assert results["at_scale_100_flux_over_total_energy"] > 1
    return results


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
