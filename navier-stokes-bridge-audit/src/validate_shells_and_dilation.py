"""Disjoint-shell budget and a resolution-scaling counterexample."""

import json
import math
import numpy as np

from galerkin import (energy, flux, nonlinear_on_support, shell_transfer)
from validate_sparse_triad import make_field, N, K


def dilate_modes(u, m):
    """u(mx) on the torus: wavevectors times m, amplitudes fixed."""
    return {tuple(m*x for x in k): a.copy() for k, a in u.items()}


def check():
    u = make_field()
    n = nonlinear_on_support(u)
    full_flux = flux(u, n, N)
    shells = [(-flux(u, n, 1.2)),
              shell_transfer(u, n, 1.2, 1.5),
              shell_transfer(u, n, 1.5, 2.0)]
    # dE_shell/dt = nonlinear contribution - viscous dissipation.
    assert abs(sum(shells)) < 1e-10
    assert abs(full_flux) < 1e-10
    assert abs(shells[0]) > 1e-6

    e = energy(u, N)
    base_flux = abs(flux(u, n, K))
    rows = []
    for m in (1, 2, 4, 8, 16):
        um = dilate_modes(u, m)
        nm = nonlinear_on_support(um)
        f = abs(flux(um, nm, K*m))
        em = energy(um, N*m)
        rows.append({"frequency_multiplier": m,
                     "energy": em, "low_flux_abs": f,
                     "flux_over_energy_3_over_2": f / em**1.5})
        assert math.isclose(em, e, rel_tol=1e-12)
        assert math.isclose(f, m*base_flux, rel_tol=1e-12)
        assert abs(flux(um, nm, N*m)) < 1e-9
    assert rows[-1]["flux_over_energy_3_over_2"] > 1

    return {"initial_shells": {
        "abs_k_le_1_2": shells[0],
        "1_2_lt_abs_k_le_1_5": shells[1],
        "1_5_lt_abs_k_le_2": shells[2]},
        "candidate": "|Pi_K| <= C E_total^(3/2), with C independent of cutoff",
        "dilation": rows,
        "conclusion": "Any finite universal C fails as m grows; E fixed and flux linear in m."
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
