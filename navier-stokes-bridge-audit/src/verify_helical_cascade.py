"""Localized helicity equality at t=.1 for the finite N=4 Galerkin ODE.

Q_N denotes the scalar Fourier ball cutoff and P the Leray projector.
With B=(u.grad)u, p chosen so P B=B+grad p, the residual in
u_t+B+grad p=nu Delta u+R_N is R_N=(I-Q_N)P B.

This program shares the already checked WP8 field reconstruction, so its
agreement is an internal check of a new analytic identity, not a blind solver.
"""

import json

import numpy as np

from evolve_galerkin import System
from localized_energy_audit import grid_fields, terminal, window


def spectral_fields(sys, a, M):
    u, ut, p, R, _, _ = grid_fields(sys, a, M)
    axes = (0, 1, 2)
    k1 = np.rint(np.fft.fftfreq(M) * M).astype(int)
    k = np.stack(np.meshgrid(k1, k1, k1, indexing="ij"), axis=-1)

    def transform(v):
        return np.fft.fftn(v, axes=axes) / M**3

    def invert(v):
        return (np.fft.ifftn(v, axes=axes) * M**3).real

    uh, uth, Rh = map(transform, (u, ut, R))
    curl = lambda v: 1j * np.cross(k, v)
    w = invert(curl(uh))
    wt = invert(curl(uth))
    cr = invert(curl(Rh))

    # grad[...,j,i] = partial_j velocity_i; same layout for vorticity.
    gu = invert(1j * k[..., :, None] * uh[..., None, :])
    gw = invert(1j * k[..., :, None] * curl(uh)[..., None, :])
    grad_pair = np.sum(gu * gw, axis=(-2, -1))
    h = np.sum(u * w, axis=-1)
    ht = np.sum(ut * w + u * wt, axis=-1)
    residual = np.sum(w * R + u * cr, axis=-1)
    return u, p, w, h, ht, grad_pair, residual, uh, uth, k


def evaluate(f, M, kappa, nu):
    u, p, w, h, ht, grad_pair, residual, *_ = f
    phi, dphi, lap = window(M, kappa)
    e = .5 * np.sum(u*u, axis=-1)
    flux = h[..., None]*u + (p-e)[..., None]*w
    lhs = float(np.mean(phi*ht))
    transport = float(np.mean(np.sum(flux*dphi, axis=-1)))
    diffusion = float(nu*np.mean(h*lap))
    dissipation = float(-2*nu*np.mean(phi*grad_pair))
    projection = float(np.mean(phi*residual))
    rhs = transport+diffusion+dissipation+projection
    return {'kappa': kappa, 'window_mean': float(np.mean(phi)),
            'localized_helicity': float(np.mean(phi*h)),
            'lhs_helicity_derivative': lhs,
            'transport_and_pressure': transport,
            'diffusion_window_term': diffusion,
            'viscous_gradient_pair': dissipation,
            'projection_residual': projection,
            'rhs': rhs, 'closure_error': abs(lhs-rhs),
            'error_if_residual_omitted': abs(lhs-(rhs-projection))}


def fourier_global_derivative(f, nu):
    # Independent global Parseval check using Galerkin Fourier coefficients.
    *_, uh, uth, k = f
    wh = 1j*np.cross(k, uh)
    wth = 1j*np.cross(k, uth)
    lhs = float(np.real(np.sum(uth*np.conj(wh)+uh*np.conj(wth))))
    sq = np.sum(k*k, axis=-1)
    viscous = float(-2*nu*np.real(np.sum(sq[..., None]*uh*np.conj(wh))))
    return {'lhs_fourier': lhs, 'viscous_fourier': viscous,
            'global_fourier_error': abs(lhs-viscous)}


def run():
    sys = System(N=4, nu=.1)
    cases = []
    for shape in ('line', 'cube'):
        a = terminal(sys, shape)
        f64 = spectral_fields(sys, a, 64)
        rows = [evaluate(f64, 64, kap, sys.nu) for kap in (0, 1, 4, 9, 16)]
        global_check = fourier_global_derivative(f64, sys.nu)
        del f64
        f96 = spectral_fields(sys, a, 96)
        for row in rows:
            check = evaluate(f96, 96, row['kappa'], sys.nu)
            row['grid64_vs_grid96_lhs_diff'] = abs(
                row['lhs_helicity_derivative']-check['lhs_helicity_derivative'])
            row['grid64_vs_grid96_residual_diff'] = abs(
                row['projection_residual']-check['projection_residual'])
            assert row['closure_error'] < 1e-10
            assert check['closure_error'] < 1e-10
            assert row['grid64_vs_grid96_lhs_diff'] < 1e-10
            assert row['grid64_vs_grid96_residual_diff'] < 1e-10
        del f96
        assert global_check['global_fourier_error'] < 1e-10
        assert abs(rows[0]['projection_residual']) < 1e-10
        cases.append({'shape': shape, 'time': .1, 'rows': rows,
                      'global_fourier_check': global_check})
    return {'N': 4, 'nu': .1, 'mode_count': len(sys.modes),
            'window': 'exp(kappa*(cos(x)+cos(y)+cos(z)-3))',
            'residual_convention': 'R_N=(I-Q_N)P[(u.grad)u], P=Leray, Q_N=Fourier ball cutoff',
            'identity': 'd<phi u.omega>/dt = <[h u+(p-|u|^2/2)omega].grad phi> + nu<h lap phi-2 phi grad u:grad omega> + <phi(omega.R_N+u.curl R_N)>',
            'results': cases,
            'scope': 'Finite N=4 Galerkin identity for two fields at t=.1; no infinite-resolution or regularity result.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
