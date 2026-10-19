"""Finite-sub-lattice scaling and H^s energy-budget check for WP11.

Run: python3 src/wp11_regularized_energy_scaling_audit.py --output /tmp/wp11_energy_scaling.json
The scaled image lattice is not the full enlarged Fourier ball.
"""

import argparse
import json

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from wp11_phase_rate_audit import triad_values
from wp11_regularized_phase_audit import decompose
from wp11_scaling_audit import dilated_system, discrepancy


def snapshot(system, a, s, K, relative_epsilon):
    m2 = system.square.astype(float)**s
    da = system.rhs(a)
    X = float(np.sum(m2[:, None]*abs(a)**2))
    Y = float(np.sum((m2*system.square)[:, None]*abs(a)**2))
    half_X_dot = float(np.real(np.einsum('k,kj,kj->', m2, np.conj(a), da)))
    transfer = -float(np.real(np.einsum(
        'k,kj,kj->', m2, np.conj(a), system.nonlinear(a))))
    high = system.square[system.left] > K*K
    z, dz, _ = triad_values(system, a, s, high)
    # The absolute epsilon must transform with z under dilation.
    epsilon = relative_epsilon*max(float(np.max(abs(z))), 1e-300)
    radial, angular, activation = decompose(z, dz, epsilon)
    terms = dict(radial=float(np.sum(radial)), angular=float(np.sum(angular)),
                 activation=float(np.sum(activation)))
    high_value = float(np.sum(z.real))
    high_dot = float(np.sum(dz.real))
    budget_error = abs(half_X_dot+system.nu*Y-transfer) / max(
        1.0, abs(half_X_dot), abs(system.nu*Y), abs(transfer))
    decomposition_error = float(np.sum(abs(radial+angular+activation-dz.real))
                                / max(1.0, float(np.sum(abs(dz.real)))))
    assert budget_error < 2e-12 and decomposition_error < 2e-12
    return dict(X=X, Y=Y, half_X_dot=half_X_dot, transfer=transfer,
                high_transfer=high_value, high_dot=high_dot,
                epsilon=epsilon, terms=terms,
                budget_error=budget_error, decomposition_error=decomposition_error)


def run(N, lam=2, s=2.0, K=2, dt=0.0005, steps=10):
    base = System(N=N, nu=0.1)
    scaled = dilated_system(base, lam)
    a = make_initial(base, *SCENARIOS['combined_double_quarter_high'])
    b = lam*a.copy()
    value_power = 2*s+4
    derivative_power = value_power+2
    check_times = {0, steps//2, steps}
    rows = []
    maximum = 0.0
    for step in range(steps+1):
        if step in check_times:
            for relative_epsilon in (1e-3, 1e-6):
                x = snapshot(base, a, s, K, relative_epsilon)
                y = snapshot(scaled, b, s, lam*K, relative_epsilon)
                errors = [discrepancy(y['X'], lam**(2*s+2)*x['X']),
                          discrepancy(y['epsilon'], lam**value_power*x['epsilon'])]
                errors.extend(discrepancy(y[key], lam**value_power*x[key])
                              for key in ('Y', 'half_X_dot', 'transfer',
                                          'high_transfer'))
                errors.append(discrepancy(y['high_dot'],
                                          lam**derivative_power*x['high_dot']))
                errors.extend(discrepancy(y['terms'][key],
                                          lam**derivative_power*x['terms'][key])
                              for key in x['terms'])
                maximum = max(maximum, *errors, x['budget_error'],
                              y['budget_error'], x['decomposition_error'],
                              y['decomposition_error'])
                rows.append(dict(time=step*dt, scaled_time=step*dt/lam**2,
                                 relative_epsilon=relative_epsilon,
                                 base=x, scaled=y, largest_scaling_error=max(errors)))
        if step < steps:
            a = base.rk4(a, dt)
            b = scaled.rk4(b, dt/lam**2)
    assert maximum < 2e-9
    return dict(N=N, scaled_image_cutoff=lam*N, K=K, scaled_K=lam*K,
                lambda_factor=lam, maximum_error=maximum, rows=rows,
                scope='Finite Galerkin image-sublattice scaling, not full-ball convergence')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='/tmp/wp11_energy_scaling.json')
    args = parser.parse_args()
    result = [run(N) for N in (4, 7)]
    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=2)
    for branch in result:
        print('N', branch['N'], '->', branch['scaled_image_cutoff'],
              'maximum normalized error', branch['maximum_error'])
        for row in branch['rows']:
            if row['relative_epsilon'] == 1e-6:
                print(' t=', row['time'], 'high=', row['base']['high_transfer'],
                      'radial=', row['base']['terms']['radial'],
                      'angular=', row['base']['terms']['angular'],
                      'activation=', row['base']['terms']['activation'])
