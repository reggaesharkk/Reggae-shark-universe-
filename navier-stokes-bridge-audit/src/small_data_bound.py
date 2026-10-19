"""Cutoff-independent sufficient H1 small-data condition on T^3.

The universal constant comes from an analytic lattice-series upper bound.
Numerical values below illustrate the theorem; they do not establish it.
"""

import json
import math
import numpy as np

from galerkin import nonlinear_on_support
from validate_sparse_triad import make_field
from validate_enstrophy import h1_nonlinear_growth, h2_square

# Sum_{k != 0} |k|^-4 <= sum_{n >= 1} (24 n^2+2)/n^4
# = 24*zeta(2) + 2*zeta(4) = 4*pi^2 + pi^4/45.
LATTICE_C_UPPER = math.sqrt(4*math.pi**2 + math.pi**4/45)


def gradient_square(u):
    return sum(sum(x*x for x in k) * float(np.vdot(a, a).real)
               for k, a in u.items())


def finite_lattice_constant(N):
    """Diagnostic finite-frequency L-infinity estimate constant."""
    return math.sqrt(sum(1/(i*i+j*j+k*k)**2
                         for i in range(-N, N+1)
                         for j in range(-N, N+1)
                         for k in range(-N, N+1)
                         if 0 < i*i+j*j+k*k <= N*N))


def check():
    nu = .1
    original = make_field()
    sign = -1 if h1_nonlinear_growth(
        original, nonlinear_on_support(original)) < 0 else 1
    u = {k: sign*a for k, a in original.items()}
    g_base = gradient_square(u)
    smallness_amplitude = nu/(LATTICE_C_UPPER*math.sqrt(g_base))
    rows = []
    for amplitude in (.001, .002, .01, 1, 5):
        v = {k: amplitude*a for k, a in u.items()}
        g = gradient_square(v)
        d = h2_square(v)
        t = h1_nonlinear_growth(v, nonlinear_on_support(v))
        envelope = LATTICE_C_UPPER*math.sqrt(g)*d
        criterion = LATTICE_C_UPPER*math.sqrt(g) < nu
        derivative = t - nu*d
        assert abs(t) <= envelope*(1+1e-12)
        if criterion:
            assert derivative < 0
        rows.append({"amplitude": amplitude,
                     "criterion_satisfied": criterion,
                     "upper_bound_on_abs_nonlinearity": envelope,
                     "actual_nonlinearity": t,
                     "viscous_damping": nu*d,
                     "instantaneous_H1_derivative": derivative})
    assert finite_lattice_constant(2) < LATTICE_C_UPPER
    assert rows[0]["criterion_satisfied"]
    assert not rows[-1]["criterion_satisfied"]
    return {"universal_constant_upper": LATTICE_C_UPPER,
            "viscosity": nu,
            "base_gradient_square": g_base,
            "sufficient_amplitude_strictly_below": smallness_amplitude,
            "finite_N2_constant_for_diagnostic_only": finite_lattice_constant(2),
            "rows": rows,
            "scope": "Small-data sufficient condition; failure of criterion implies nothing about blowup."}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
