"""Threshold-free ordered-triad transfer derivative audit for WP11.

Run: python3 src/wp11_regularized_phase_audit.py
The regularization is an exact identity, not a signed transfer estimate.
"""

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from wp11_phase_rate_audit import triad_values


def decompose(z, dz, epsilon):
    """Return amplitude, angular, and zero-activation terms in d Re(z)/dt.

    epsilon is a strictly positive absolute scale in the units of z.
    """
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError('epsilon must be positive and finite')
    denom = np.abs(z)**2 + epsilon**2
    radial = (np.real(np.conj(z)*dz) / denom) * np.real(z)
    angular = -(np.imag(np.conj(z)*dz) / denom) * np.imag(z)
    activation = (epsilon**2 / denom) * np.real(dz)
    return radial, angular, activation


def run():
    rows = []
    for N in (4, 7):
        system = System(N=N, nu=0.1)
        a = make_initial(system, *SCENARIOS['combined_double_quarter_high'])
        for time in (0.0, 0.0025):
            if time:
                for _ in range(5):
                    a = system.rk4(a, 0.0005)
            high = system.square[system.left] > 4
            z, dz, _ = triad_values(system, a, 2.0, high)
            scale = max(1.0, float(np.max(np.abs(z))))
            for relative_epsilon in (1e-3, 1e-6):
                radial, angular, activation = decompose(
                    z, dz, relative_epsilon*scale)
                error = float(np.sum(np.abs(radial+angular+activation-dz.real))
                              / max(1.0, float(np.sum(np.abs(dz.real)))))
                zeros = np.abs(z) == 0
                zero_error = (float(np.max(np.abs(activation[zeros]-dz.real[zeros])))
                              if np.any(zeros) else 0.0)
                assert error < 2e-12 and zero_error < 2e-12
                rows.append((N, time, relative_epsilon, error,
                             int(np.sum(zeros)), float(np.sum(activation))))
    return rows


if __name__ == '__main__':
    for N, t, eps, error, zeros, activation in run():
        print(f'N={N} t={t:.4f} relative_epsilon={eps:g} '
              f'residual={error:.3g} zero_triads={zeros} '
              f'activation_sum={activation:.8g}')
