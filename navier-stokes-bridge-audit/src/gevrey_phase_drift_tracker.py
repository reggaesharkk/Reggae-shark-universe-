"""Finite-Galerkin Gevrey triad phase diagnostics; no continuum claim.

Run from any directory. The two weight schedules evaluate the *same* states.
An angular rate is reported only where its complex triad amplitude is nonzero.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import NU
from smooth_gevrey_identity_audit import (
    functionals, schedule_persistence, schedule_smoothing,
)


def triads(sys, a, adot=None):
    """Ordered k=p+q scalar triads, with P_k acting on the output pairing."""
    out, left, right = sys.out, sys.left, sys.right
    projected_conj = np.einsum('kij,kj->ki', sys.projectors, np.conj(a))
    qdot = np.einsum('ij,ij->i', sys.qwaves, a[left])
    inner = np.einsum('ij,ij->i', projected_conj[out], a[right])
    z = qdot * inner
    if adot is None:
        return z
    projected_conj_dot = np.einsum(
        'kij,kj->ki', sys.projectors, np.conj(adot))
    qdot_dot = np.einsum('ij,ij->i', sys.qwaves, adot[left])
    inner_dot = (
        np.einsum('ij,ij->i', projected_conj_dot[out], a[right])
        + np.einsum('ij,ij->i', projected_conj[out], adot[right])
    )
    return z, qdot_dot * inner + qdot * inner_dot


def snapshot(sys, a, s, sigma, relative_floor=1e-9, top_k=5):
    if s <= 1.5 or sigma < 0 or relative_floor < 0:
        raise ValueError('Need s>3/2, sigma>=0, relative_floor>=0')
    adot = sys.rhs(a)
    z, zdot = triads(sys, a, adot)
    X, Y, Z, nonlinear, weights = functionals(sys, a, s, sigma)
    w = weights[sys.out]
    reconstructed = float(np.sum(w * np.imag(z)))
    absolute_sum = float(np.sum(w * np.abs(z)))
    residual = reconstructed - nonlinear
    scale = max(1.0, abs(reconstructed), abs(nonlinear))
    if abs(residual) / scale > 1e-11:
        raise AssertionError(f'Triad reconstruction failed: {residual}')
    threshold = relative_floor * float(np.max(np.abs(z)))
    valid = (np.abs(z) > 0) & (np.abs(z) >= threshold) & (w > 0)
    phase_rate = np.full(len(z), np.nan)
    phase_rate[valid] = (
        np.imag(np.conj(z[valid]) * zdot[valid]) / np.abs(z[valid])**2
    )
    candidates = np.flatnonzero(valid)
    best = candidates[np.argsort(-(w[candidates] * np.abs(z[candidates])))[:top_k]]
    examples = [dict(
        k=list(map(int, sys.waves[sys.out[i]])),
        p=list(map(int, sys.waves[sys.left[i]])),
        q=list(map(int, sys.waves[sys.right[i]])),
        z_real=float(np.real(z[i])), z_imag=float(np.imag(z[i])),
        zdot_real=float(np.real(zdot[i])), zdot_imag=float(np.imag(zdot[i])),
        phase_rate=float(phase_rate[i]),
        weighted_signed_transfer=float(w[i] * np.imag(z[i])),
    ) for i in best]
    return dict(
        X=X, Y=Y, Z=Z, nonlinear=nonlinear,
        reconstructed_nonlinear=reconstructed,
        reconstruction_relative_error=abs(residual)/scale,
        absolute_triad_envelope=absolute_sum,
        cancellation_ratio=(abs(reconstructed)/absolute_sum
                            if absolute_sum > 0 else None),
        strong_quotient=(abs(nonlinear)/(X*math.sqrt(Y))
                         if X > 0 and Y > 0 else None),
        weak_quotient=(abs(nonlinear)/(math.sqrt(X)*Y)
                       if X > 0 and Y > 0 else None),
        total_ordered_pairs=len(z), phase_rate_pair_count=int(np.sum(valid)),
        phase_relative_floor=relative_floor, top_triads=examples,
    )


def algebra_checks(sys, a, dt=1e-5):
    """Independent finite differences and transformations at one state."""
    z, zdot = triads(sys, a, sys.rhs(a))
    plus = triads(sys, sys.rk4(a, dt))
    minus = triads(sys, sys.rk4(a, -dt))
    fd = (plus - minus) / (2*dt)
    error = float(np.linalg.norm(fd - zdot) / max(1.0, np.linalg.norm(zdot)))
    shift = np.array([.19, -.31, .47])
    phases = np.exp(1j * (sys.waves @ shift))
    z_shift = triads(sys, a*phases[:, None])
    translation_error = float(np.max(np.abs(z_shift-z)))
    z_neg = triads(sys, -a)
    reversal_error = float(np.max(np.abs(z_neg+z)))
    viscous_adot = -sys.nu * sys.square[:, None] * a
    _, viscous_zdot = triads(sys, a, viscous_adot)
    predicted_viscous_zdot = -sys.nu * (
        sys.square[sys.out] + sys.square[sys.left]
        + sys.square[sys.right]
    ) * z
    viscous_product_error = float(np.max(np.abs(
        viscous_zdot - predicted_viscous_zdot)))
    active = np.abs(z) > 1e-12 * max(1., float(np.max(np.abs(z))))
    viscous_phase_rate_max = float(np.max(np.abs(
        np.imag(np.conj(z[active]) * viscous_zdot[active])
        / np.abs(z[active])**2
    ))) if np.any(active) else None
    if translation_error > 1e-10 or reversal_error > 1e-10:
        raise AssertionError('Triad transformation identity failed')
    if viscous_product_error > 1e-9:
        raise AssertionError('Viscous triad derivative identity failed')
    return dict(
        centered_complex_zdot_relative_error=error,
        centered_step=dt,
        translation_max_abs_error=translation_error,
        sign_reversal_max_abs_error=reversal_error,
        viscous_product_max_abs_error=viscous_product_error,
        viscous_phase_rate_max_abs_on_active_triads=viscous_phase_rate_max,
        max_abs_zdot=float(np.max(np.abs(zdot))),
    )


def run(cutoffs=(4, 7), scenarios=('reference',
            'combined_double_quarter_high'), dt=.0005, t_end=.005,
        s=2.0, relative_floor=1e-9, top_k=5):
    steps = round(t_end / dt)
    if steps < 2 or not math.isclose(steps*dt, t_end, abs_tol=1e-14):
        raise ValueError('t_end must be an integer multiple of dt, >=2 steps')
    rows = []
    for scenario in scenarios:
        for N in cutoffs:
            sys = System(N=N, nu=NU)
            a = make_initial(sys, *SCENARIOS[scenario])
            checks = algebra_checks(sys, a)
            series = {'persistence': [], 'smoothing': []}
            for j in range(steps+1):
                t = j*dt
                for label, schedule in (
                    ('persistence', schedule_persistence),
                    ('smoothing', schedule_smoothing),
                ):
                    sigma, _ = schedule(t)
                    row = snapshot(sys, a, s, sigma, relative_floor, top_k)
                    row.update(time=t, sigma=sigma)
                    series[label].append(row)
                if j < steps:
                    a = sys.rk4(a, dt)
            integral = {
                label: float(np.trapezoid(
                    [r['nonlinear'] for r in seq], dx=dt))
                for label, seq in series.items()
            }
            rows.append(dict(N=N, scenario=scenario, checks=checks,
                             schedules=series, signed_transfer_integrals=integral))
    return dict(s=s, nu=NU, dt=dt, interval=[0., t_end],
                relative_floor=relative_floor, rows=rows,
                scope='Finite Galerkin diagnostic; no phase-muting inequality or continuum regularity theorem.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cutoffs', type=int, nargs='+', default=[4, 7])
    parser.add_argument('--scenarios', nargs='+', choices=list(SCENARIOS),
                        default=['reference', 'combined_double_quarter_high'])
    parser.add_argument('--dt', type=float, default=.0005)
    parser.add_argument('--t-end', type=float, default=.005)
    parser.add_argument('--s', type=float, default=2.)
    parser.add_argument('--relative-floor', type=float, default=1e-9)
    parser.add_argument('--top-k', type=int, default=5)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('gevrey_phase_drift_results.json'))
    args = parser.parse_args()
    result = run(args.cutoffs, args.scenarios, args.dt, args.t_end,
                 args.s, args.relative_floor, args.top_k)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Wrote', args.output)
    for row in result['rows']:
        print(row['scenario'], 'N=', row['N'],
              'max reconstruction error=', max(
                  r['reconstruction_relative_error']
                  for seq in row['schedules'].values() for r in seq))
