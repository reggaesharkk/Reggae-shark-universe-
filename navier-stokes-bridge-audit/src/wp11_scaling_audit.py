"""Exact Navier–Stokes dilation check for the WP11 phase diagnostics.

On the torus integer lambda maps k -> lambda*k, a_k -> lambda*a_k,
t -> t/lambda**2, and N,K -> lambda*N,lambda*K. The image lattice is
invariant under convolution. Represent it using the original compact
Galerkin index rather than allocating the entire larger Fourier ball.

Run: python3 src/wp11_scaling_audit.py --output /tmp/wp11_scaling.json
This validates scaling of finite equations, not regularity as N tends to infinity.
"""

import argparse
import json

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from wp11_phase_rate_audit import snapshot


def dilated_system(base, lam):
    """Image of the invariant Galerkin sublattice lambda*Z^3."""
    scaled = object.__new__(System)
    scaled.__dict__.update(base.__dict__)
    scaled.N = lam*base.N
    scaled.modes = [tuple(lam*x for x in p) for p in base.modes]
    scaled.index = {p:i for i,p in enumerate(scaled.modes)}
    scaled.waves = lam*base.waves
    scaled.square = lam*lam*base.square
    scaled.qwaves = lam*base.qwaves
    # Leray projectors and triad indices are unchanged because
    # P_(lambda*k)=P_k and k=p+q iff lambda*k=lambda*p+lambda*q.
    return scaled


def discrepancy(actual, expected):
    return abs(actual-expected)/max(1.0, abs(actual), abs(expected))


def audit(N, lam, s=2.0, K=2, dt=0.0005, steps=10):
    base = System(N=N, nu=0.1)
    scaled = dilated_system(base, lam)
    a = make_initial(base, *SCENARIOS['combined_double_quarter_high'])
    a_scaled = lam*a.copy()
    value_power = 2*s+4
    derivative_power = value_power+2
    value_keys = ('high_transfer', 'total_transfer', 'high_absolute_mass',
                  'high_complex_mass', 'active_mass')
    derivative_keys = ('high_transfer_derivative', 'phase_derivative_sum',
                       'amplitude_derivative_sum', 'inactive_derivative_sum',
                       'active_mass_derivative')
    rate_keys = ('weighted_abs_phase_rate',
                 'covariance_cos_phase_abs_rate',
                 'covariance_cos_phase_amplitude_growth',
                 'weighted_mean_sin_phase_rate')
    invariant_keys = ('active_mean_cos_phase', 'active_weight_fraction')
    largest = {k:0.0 for k in (*value_keys, *derivative_keys,
                                 *rate_keys, *invariant_keys, 'field', 'rhs')}
    traces = [[], []]
    for step in range(steps+1):
        ra = snapshot(base, a, s, K)
        rb = snapshot(scaled, a_scaled, s, lam*K)
        for k in value_keys:
            largest[k] = max(largest[k], discrepancy(rb[k], lam**value_power*ra[k]))
        for k in derivative_keys:
            largest[k] = max(largest[k], discrepancy(rb[k], lam**derivative_power*ra[k]))
        for k in rate_keys:
            largest[k] = max(largest[k], discrepancy(rb[k], lam**2*ra[k]))
        for k in invariant_keys:
            largest[k] = max(largest[k], discrepancy(rb[k], ra[k]))
        largest['field'] = max(largest['field'],
                               discrepancy(float(np.max(abs(a_scaled-lam*a))), 0))
        rhs_error = np.max(abs(scaled.rhs(a_scaled)-lam**3*base.rhs(a)))
        rhs_norm = max(1.0, float(np.max(abs(scaled.rhs(a_scaled)))))
        largest['rhs'] = max(largest['rhs'], float(rhs_error)/rhs_norm)
        traces[0].append(ra['high_transfer'])
        traces[1].append(rb['high_transfer'])
        if step < steps:
            a = base.rk4(a, dt)
            a_scaled = scaled.rk4(a_scaled, dt/lam**2)
    first = float(np.trapezoid(traces[0], dx=dt))
    second = float(np.trapezoid(traces[1], dx=dt/lam**2))
    integral_error = discrepancy(second, lam**(2*s+2)*first)
    assert max(*largest.values(), integral_error) < 2e-9
    return dict(base_cutoff=N, scaled_cutoff=lam*N,
                base_threshold=K, scaled_threshold=lam*K,
                lambda_factor=lam, base_time_end=steps*dt,
                scaled_time_end=steps*dt/lam**2,
                base_signed_integral=first, scaled_signed_integral=second,
                predicted_integral=lam**(2*s+2)*first,
                integrated_scaling_error=integral_error,
                maximum_relative_errors=largest,
                representation='invariant scaled image lattice; no full ball allocation')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='/tmp/wp11_scaling.json')
    parser.add_argument('--lambda-factor', type=int, default=2)
    args = parser.parse_args()
    if args.lambda_factor < 2:
        raise ValueError('lambda-factor must be an integer >= 2')
    result = [audit(N, args.lambda_factor) for N in (4,7)]
    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=2)
    for item in result:
        print('N', item['base_cutoff'], '->', item['scaled_cutoff'],
              'integrated scaling residual', item['integrated_scaling_error'],
              'maximum check residual', max(item['maximum_relative_errors'].values()))
