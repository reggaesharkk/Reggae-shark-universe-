"""Finite-cutoff review checks for the WP11 signed-transfer identity and L1.

Run from the repository root: python3 src/wp11_review_audit.py
This checks an exact finite-dimensional identity and samples an already
proved low-advector inequality. It does not test the open high-tail lemma.
"""

import json
import math

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System


def check(sys, a, s, sigma, low_cutoff):
    lengths = np.sqrt(sys.square)
    multiplier = lengths**s * np.exp(sigma * lengths)
    weights = multiplier**2
    qdot = np.einsum('ij,ij->i', sys.qwaves, a[sys.left])
    products = 1j * qdot * np.einsum(
        'ij,ij->i', np.conj(a[sys.out]), a[sys.right])
    direct = -float(np.real(np.einsum(
        'k,kj,kj->', weights, np.conj(a), sys.nonlinear(a))))
    sym = -0.5 * float(np.real(np.sum(
        (weights[sys.out] - weights[sys.right]) * products)))

    low = sys.square[sys.left] <= low_cutoff**2
    direct_low = -float(np.real(np.sum(
        weights[sys.out[low]] * products[low])))
    sym_low = -0.5 * float(np.real(np.sum(
        (weights[sys.out[low]] - weights[sys.right[low]])
        * products[low])))
    scale = max(1.0, abs(direct), abs(sym))
    low_scale = max(1.0, abs(direct_low), abs(sym_low))
    assert abs(direct - sym) <= 2e-12 * scale
    assert abs(direct_low - sym_low) <= 2e-12 * low_scale

    result = dict(cutoff=sys.N, s=s, sigma=sigma, K=low_cutoff,
                  direct=direct, sym=sym,
                  relative_identity_error=abs(direct - sym) / scale,
                  direct_low=direct_low, sym_low=sym_low,
                  relative_low_identity_error=(
                      abs(direct_low - sym_low) / low_scale))
    if sigma == 0:
        # Independently evaluate the unsymmetrized single-symbol commutator.
        comm_low = -float(np.real(np.sum(
            (multiplier[sys.out[low]]
             * (multiplier[sys.out[low]] - multiplier[sys.right[low]]))
            * products[low])))
        assert abs(direct_low - comm_low) <= 2e-12 * low_scale
        mode_count = int(np.count_nonzero(
            (sys.square > 0) & (sys.square <= low_cutoff**2)))
        # Count all lattice points in the fixed band, even if N < K.
        if sys.N < low_cutoff:
            mode_count = sum(
                0 < i*i+j*j+k*k <= low_cutoff**2
                for i in range(-low_cutoff, low_cutoff+1)
                for j in range(-low_cutoff, low_cutoff+1)
                for k in range(-low_cutoff, low_cutoff+1))
        constant = s * low_cutoff * (1 + low_cutoff)**(s-1) * math.sqrt(mode_count)
        energy_norm = math.sqrt(float(np.sum(abs(a)**2)))
        X = float(np.sum(weights[:, None] * abs(a)**2))
        bound = constant * energy_norm * X
        assert abs(direct_low) <= bound + 2e-12 * max(1.0, bound)
        result.update(comm_low=comm_low, C_s_K=constant,
                      L1_bound=bound, L1_fraction=(abs(direct_low) / bound
                                                     if bound else 0.0))
    return result


def main():
    results = []
    for N in (4, 7):
        sys = System(N=N, nu=0.1)
        a = make_initial(sys, *SCENARIOS['combined_double_quarter_high'])
        for t in (0.0, 0.0025):
            if t:
                for _ in range(5):
                    a = sys.rk4(a, 0.0005)
            for sigma in (0.0, 0.2):
                for K in (1, 2):
                    entry = check(sys, a, s=2.0, sigma=sigma, low_cutoff=K)
                    entry['time'] = t
                    results.append(entry)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
