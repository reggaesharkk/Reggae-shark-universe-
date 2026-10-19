"""Instantaneous H1/enstrophy budget and viscous threshold on a sparse triad."""

import json
import math
import numpy as np

from galerkin import nonlinear_on_support, rhs, flux
from validate_sparse_triad import make_field, N
from validate_shells_and_dilation import dilate_modes


def h1_energy(u):
    return 0.5 * sum(sum(x*x for x in k) * float(np.vdot(a, a).real)
                     for k, a in u.items())


def h2_square(u):
    return sum(sum(x*x for x in k)**2 * float(np.vdot(a, a).real)
               for k, a in u.items())


def h1_nonlinear_growth(u, n):
    return -sum(sum(x*x for x in k) * float(np.vdot(a, n[k]).real)
                for k, a in u.items())


def h1_derivative(u, du):
    return sum(sum(x*x for x in k) * float(np.vdot(a, du[k]).real)
               for k, a in u.items())


def physical_space_growth(u, grid_size=16):
    """Independent torus quadrature of -∫(∂j ui)(∂i ul)(∂j ul).

    At the base triad the integrand's frequencies are at most three per
    coordinate, so a 16-point trapezoidal grid resolves its mean exactly
    apart from floating-point roundoff. Do not use for dilated modes.
    """
    coords = 2*np.pi*np.arange(grid_size)/grid_size
    x, y, z = np.meshgrid(coords, coords, coords, indexing='ij')
    grad = np.zeros((grid_size,)*3 + (3, 3), dtype=complex)
    for k, a in u.items():
        phase = np.exp(1j*(k[0]*x + k[1]*y + k[2]*z))
        grad += phase[..., None, None] * (1j*np.outer(k, a))
    value = -np.einsum('...ji,...il,...jl->...', grad, grad, grad)
    return float(value.real.mean())


def check():
    # Reversing every amplitude reverses cubic enstrophy transfer but leaves
    # quadratic energy and dissipation unchanged. Pick the sign with growth.
    initial = make_field()
    base = h1_nonlinear_growth(initial, nonlinear_on_support(initial))
    assert abs(base) > 1e-6
    u = {k: (-1 if base < 0 else 1)*a for k, a in initial.items()}
    physical_growth = physical_space_growth(u)
    spectral_growth = h1_nonlinear_growth(u, nonlinear_on_support(u))
    assert abs(physical_growth - spectral_growth) < 1e-10
    rows = []
    for amplitude, m, nu in [(1, 1, .01), (1, 1, .1),
                             (5, 1, .1), (1, 2, .1), (1, 4, .1),
                             (5, 4, .1)]:
        v = {k: amplitude*a for k, a in dilate_modes(u, m).items()}
        n = nonlinear_on_support(v)
        growth = h1_nonlinear_growth(v, n)
        d2 = h2_square(v)
        viscous = nu*d2
        du = rhs(v, N*m, nu)
        budget_error = abs(h1_derivative(v, du) - (growth-viscous))
        assert budget_error < 1e-9 * max(1, abs(growth), viscous)
        assert abs(flux(v, n, N*m)) < 1e-9 * max(1, amplitude**3*m)
        rows.append({"amplitude": amplitude, "frequency_multiplier": m,
                     "viscosity": nu, "enstrophy": h1_energy(v),
                     "nonlinear_enstrophy_growth": growth,
                     "viscous_enstrophy_damping": viscous,
                     "instantaneous_enstrophy_derivative": growth-viscous,
                     "viscosity_threshold_nu_star": growth/d2,
                     "budget_error": budget_error})
    nu_star_base = rows[0]["viscosity_threshold_nu_star"]
    for row in rows:
        expected = nu_star_base * row["amplitude"]/row["frequency_multiplier"]
        assert math.isclose(row["viscosity_threshold_nu_star"], expected,
                            rel_tol=1e-12)
    return {"threshold_formula": "nu_star = positive nonlinear H1 growth / sum |k|^4 |a_k|^2",
            "scaling": "Under u(x)->A u(mx), nu_star scales as A/m",
            "independent_physical_space_growth": physical_growth,
            "physical_vs_fourier_error": abs(physical_growth-spectral_growth),
            "rows": rows,
            "limit": "An instantaneous positive derivative is not a finite-time singularity."}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
