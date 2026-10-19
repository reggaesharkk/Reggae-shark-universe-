"""Riesz-strain reconstruction and vorticity-weighted stretching localization.

Descriptive finite Galerkin diagnostic. The 90th-percentile spatial mask is
fixed before comparing fields; it is not a proposed regularity criterion.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent


def riesz_strain(sys, a, grid):
    """Independent strain path via omega_hat=i k cross a_k.

    S_ij(k)=-[k_j(k cross omega_hat)_i+k_i(k cross omega_hat)_j]
             /(2 |k|^2) for nonzero k.
    """
    k = sys.waves
    omega_hat = 1j * np.cross(k, a)
    kcross = np.cross(k, omega_hat)
    coeff = np.zeros((len(k), 3, 3), complex)
    nonzero = sys.square > 0
    coeff[nonzero] = -(kcross[nonzero, :, None]*k[nonzero, None, :] +
                       k[nonzero, :, None]*kcross[nonzero, None, :])/(2*sys.square[nonzero, None, None])
    grid_coeff = np.zeros((grid, grid, grid, 3, 3), complex)
    grid_coeff[tuple((k % grid).T)] = grid**3 * coeff
    out = np.fft.ifftn(grid_coeff, axes=(0, 1, 2))
    assert np.max(abs(out.imag)) < 1e-10
    return out.real


def snapshot(sys, a, grid=32):
    grad, omega, _, imaginary = spatial_fields(sys, a, grid)
    direct = (grad + np.swapaxes(grad, -1, -2))/2
    riesz = riesz_strain(sys, a, grid)
    discrepancy = float(np.max(abs(direct-riesz)))
    assert imaginary < 1e-10 and discrepancy < 1e-10
    w2 = np.sum(omega**2, axis=-1)
    z = np.einsum('...i,...ij,...j->...', omega, riesz, omega)
    threshold = float(np.quantile(w2, .9))
    mask = w2 >= threshold
    assert abs(float(np.mean(mask))-.1) < .001
    G = float(np.mean(w2))
    T = float(np.mean(z))
    positive = float(np.mean(np.maximum(z, 0)))
    negative = float(np.mean(np.minimum(z, 0)))
    spectral = -float(np.real(np.einsum('i,ij,ij->', sys.square, a.conj(), sys.nonlinear(a))))
    assert abs(T-spectral) < 1e-8*max(1, abs(spectral))
    high_positive = float(np.mean(np.where(mask, np.maximum(z, 0), 0)))
    high_negative = float(np.mean(np.where(mask, np.minimum(z, 0), 0)))
    return dict(grid=grid, G=G, T=T, positive_local=positive,
                negative_local=negative, top_decile_threshold_w2=threshold,
                top_decile_volume=float(np.mean(mask)),
                top_decile_G_fraction=float(np.mean(np.where(mask,w2,0))/G),
                top_decile_positive_fraction=high_positive/positive if positive else None,
                top_decile_negative_magnitude_fraction=high_negative/negative if negative else None,
                top_decile_signed_T=high_positive+high_negative,
                bottom_nine_deciles_signed_T=T-high_positive-high_negative,
                max_strain_path_discrepancy=discrepancy,
                Fourier_minus_Riesz_T=spectral-T)


def evolve(scenario, N):
    sys = System(N=N, nu=NU)
    a = make_initial(sys, *SCENARIOS[scenario])
    first = snapshot(sys, a)
    for _ in range(40):
        a = sys.rk4(a, DT)
    last = snapshot(sys, a)
    fine = snapshot(sys, a, grid=48)
    return dict(scenario=scenario, N=N, initial=first, final=last,
                endpoint_grid48_minus_grid32_top_positive_fraction=(
                    fine['top_decile_positive_fraction']-last['top_decile_positive_fraction']),
                endpoint_grid48_minus_grid32_T=fine['T']-last['T'])


def run():
    rows = []
    for scenario in ('reference', 'combined_double_quarter_high'):
        for N in (4, 7):
            row = evolve(scenario,N)
            rows.append(row)
            print(scenario, N, 'positive share',
                  round(row['initial']['top_decile_positive_fraction'], 6),
                  round(row['final']['top_decile_positive_fraction'], 6), flush=True)
    return dict(derivation='S_ij(k)=-(k_j(k cross omega_hat)_i + k_i(k cross omega_hat)_j)/(2|k|^2), omega_hat=i k cross u_hat',
                mask='top 10% of physical-grid |omega|^2 at each snapshot; no universal status',
                limitation='Two times, two cutoffs, two initial conditions; grid percentiles and positive parts are approximate quadratures. No a priori or cutoff-uniform time estimate.',
                rows=rows)


if __name__ == '__main__':
    result = run()
    target = HERE/'riesz_stretching_results.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('Wrote',target)
