"""Exact finite-Galerkin high-advector triad phase and amplitude audit.

Run: python3 src/wp11_phase_rate_audit.py --output /tmp/wp11_phase.json
No covariance or finite trajectory here establishes a continuum sign bound.
"""

import argparse
import json

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System


def triad_values(sys, a, s, high):
    """Complex contributions z and the exact directional derivative z-dot."""
    out, left, right = (x[high] for x in (sys.out, sys.left, sys.right))
    q = sys.qwaves[high]
    da = sys.rhs(a)
    m2 = sys.square[out].astype(float)**s
    qdot = np.einsum('ij,ij->i', q, a[left])
    dqdot = np.einsum('ij,ij->i', q, da[left])
    pair = np.einsum('ij,ij->i', np.conj(a[out]), a[right])
    dpair = (np.einsum('ij,ij->i', np.conj(da[out]), a[right])
             + np.einsum('ij,ij->i', np.conj(a[out]), da[right]))
    z = -1j*m2*qdot*pair
    dz = -1j*m2*(dqdot*pair + qdot*dpair)
    dz_visc = -sys.nu*(sys.square[out]+sys.square[left]
                        +sys.square[right])*z
    return z, dz, dz_visc


def weighted_cov(x, y, w):
    total = float(np.sum(w))
    if total == 0:
        return 0.0
    return float(np.sum(w*x*y)/total
                 - np.sum(w*x)*np.sum(w*y)/(total*total))


def snapshot(sys, a, s, K, phase_floor=1e-9):
    high = sys.square[sys.left] > K*K
    z, dz, dz_visc = triad_values(sys, a, s, high)
    magnitude = abs(z)
    active = magnitude > phase_floor*max(float(np.max(magnitude)), 1e-300)
    phase_rate = np.imag(np.conj(z[active])*dz[active])/magnitude[active]**2
    amplitude_rate = np.real(np.conj(z[active])*dz[active])/magnitude[active]
    cos_phase = z[active].real/magnitude[active]
    sin_phase = z[active].imag/magnitude[active]
    phase_term = -magnitude[active]*sin_phase*phase_rate
    amplitude_term = amplitude_rate*cos_phase
    reconstructed = amplitude_term+phase_term
    dz_scale = max(1.0, float(np.sum(abs(dz))))
    algebra_error = float(np.sum(abs(reconstructed-dz[active].real)))/dz_scale
    visc_rate = np.imag(np.conj(z[active])*dz_visc[active])/magnitude[active]**2
    visc_error = float(np.max(abs(visc_rate))) if len(visc_rate) else 0.0

    # Independent directional finite difference of the same cubic transfer.
    h = 1e-6
    da = sys.rhs(a)
    plus = triad_values(sys, a+h*da, s, high)[0].real.sum()
    minus = triad_values(sys, a-h*da, s, high)[0].real.sum()
    fd = (plus-minus)/(2*h)
    derivative = float(np.real(np.sum(dz)))
    fd_error = abs(fd-derivative)/max(1.0, abs(fd), abs(derivative))

    # Independent full projected convolution checks the total signed transfer.
    total = -float(np.real(np.einsum('k,kj,kj->',
        sys.square.astype(float)**s, np.conj(a), sys.nonlinear(a))))
    low = ~high
    low_out, low_left, low_right = (x[low] for x in
                                    (sys.out, sys.left, sys.right))
    low_qdot = np.einsum('ij,ij->i', sys.qwaves[low], a[low_left])
    low_z = -1j*sys.square[low_out].astype(float)**s*low_qdot*np.einsum(
        'ij,ij->i', np.conj(a[low_out]), a[low_right])
    high_value = float(np.real(np.sum(z)))
    transfer_error = abs(total-(high_value+float(np.real(np.sum(low_z))))) / max(1.0, abs(total))
    assert algebra_error < 2e-11
    assert visc_error < 1e-10
    assert fd_error < 2e-7
    assert transfer_error < 2e-11

    w = magnitude[active]
    weighted_speed = float(np.sum(w*abs(phase_rate))/np.sum(w)) if len(w) else 0.0
    cov = weighted_cov(cos_phase, abs(phase_rate), w)
    M = float(np.sum(w))
    mean_cos = float(np.sum(w*cos_phase)/M) if M else 0.0
    growth = amplitude_rate/w if M else np.zeros_like(w)
    cov_growth = weighted_cov(cos_phase, growth, w)
    mean_sin_rate = float(np.sum(w*sin_phase*phase_rate)/M) if M else 0.0
    active_derivative_from_cov = (float(np.sum(amplitude_rate))*mean_cos
                                  + M*(cov_growth-mean_sin_rate))
    covariance_error = abs(active_derivative_from_cov
                           - float(np.sum(dz[active].real))) / dz_scale
    assert covariance_error < 2e-11
    return dict(high_transfer=high_value, total_transfer=total,
                high_absolute_mass=float(np.sum(abs(z.real))),
                high_complex_mass=float(np.sum(magnitude)),
                high_transfer_derivative=derivative,
                phase_derivative_sum=float(np.sum(phase_term)),
                amplitude_derivative_sum=float(np.sum(amplitude_term)),
                inactive_derivative_sum=float(np.sum(dz[~active].real)),
                active_weight_fraction=(float(np.sum(w))/float(np.sum(magnitude))
                                        if np.sum(magnitude) else 0.0),
                weighted_abs_phase_rate=weighted_speed,
                covariance_cos_phase_abs_rate=cov,
                covariance_cos_phase_amplitude_growth=cov_growth,
                weighted_mean_sin_phase_rate=mean_sin_rate,
                active_mass=M,
                active_mean_cos_phase=mean_cos,
                active_mass_derivative=float(np.sum(amplitude_rate)),
                covariance_identity_error=covariance_error,
                phase_decomposition_error=algebra_error,
                viscous_phase_null_error=visc_error,
                finite_difference_error=fd_error,
                transfer_reconstruction_error=transfer_error)


def run(dt=0.0005, t_end=0.005, K=2, s=2.0,
        scenario='combined_double_quarter_high'):
    if scenario not in SCENARIOS:
        raise ValueError('Unknown scenario: '+scenario)
    steps = round(t_end/dt)
    if abs(steps*dt-t_end) > 1e-12:
        raise ValueError('t_end must be a multiple of dt')
    results = []
    for N in (4, 7):
        sys = System(N=N, nu=0.1)
        a = make_initial(sys, *SCENARIOS[scenario])
        rows = []
        for step in range(steps+1):
            row = snapshot(sys, a, s, K)
            row['time'] = step*dt
            rows.append(row)
            if step < steps:
                a = sys.rk4(a, dt)
        integrated_transfer = float(np.trapezoid(
            [row['high_transfer'] for row in rows], dx=dt))
        results.append(dict(cutoff=N, scenario=scenario, K=K, s=s, dt=dt,
                            integrated_high_transfer=integrated_transfer,
                            rows=rows))
    return dict(description='Finite-cutoff phase/amplitude derivative diagnostic',
                results=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='/tmp/wp11_phase.json')
    parser.add_argument('--dt', type=float, default=0.0005)
    parser.add_argument('--t-end', type=float, default=0.005)
    parser.add_argument('--scenario', default='combined_double_quarter_high')
    args = parser.parse_args()
    result = run(dt=args.dt, t_end=args.t_end, scenario=args.scenario)
    with open(args.output, 'w', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    for branch in result['results']:
        print('N=', branch['cutoff'], 'integrated signed high transfer=',
              branch['integrated_high_transfer'], 'worst derivative error=',
              max(row['finite_difference_error'] for row in branch['rows']))
