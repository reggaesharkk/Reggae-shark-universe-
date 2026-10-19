"""Vorticity/strain eigenframe audit of two short Fourier-Galerkin runs.

Run alongside the archived src modules. Outputs strain_alignment_results.json.
Finite cutoff data do not establish a continuum or long-time regularity bound.
"""

import json
from pathlib import Path

import numpy as np

from phase_cascade_trajectory import DT, NU, System, initial
from smooth_commutator_gate import multipliers


def spatial_fields(sys, a, grid, psi=None):
    """Return real A_ij=partial_j u_i, omega, and optionally filtered omega.

    Inverse FFT uses coefficients multiplied by grid**3 to match the Fourier
    convention u(x)=sum_k a_k exp(i k dot x). For grid>3*N all cubic spatial
    averages used below have exact trapezoidal quadrature (no alias to zero).
    """
    assert grid > 3 * sys.N
    shape = (grid, grid, grid, 3)
    index = tuple((sys.waves % grid).T)
    grad = np.empty((grid, grid, grid, 3, 3), float)
    max_imag = 0.0
    for direction in range(3):
        coeff = np.zeros(shape, complex)
        coeff[index] = 1j * sys.waves[:, direction, None] * a * grid**3
        transformed = np.fft.ifftn(coeff, axes=(0, 1, 2))
        max_imag = max(max_imag, float(np.max(abs(transformed.imag))))
        grad[..., :, direction] = transformed.real
    omega = np.stack((grad[..., 2, 1] - grad[..., 1, 2],
                      grad[..., 0, 2] - grad[..., 2, 0],
                      grad[..., 1, 0] - grad[..., 0, 1]), axis=-1)
    if psi is None:
        return grad, omega, None, max_imag
    cross = np.cross(sys.waves, a)
    filtered = []
    for multiplier in psi:
        coeff = np.zeros(shape, complex)
        coeff[index] = 1j * cross * multiplier[:, None] * grid**3
        transformed = np.fft.ifftn(coeff, axes=(0, 1, 2))
        max_imag = max(max_imag, float(np.max(abs(transformed.imag))))
        filtered.append(transformed.real)
    return grad, omega, filtered, max_imag


def eigen_statistics(omega, eigenvalues, eigenvectors):
    projections = np.einsum('...ij,...i->...j', eigenvectors, omega)
    projected_square = projections**2
    omega_square = float(np.mean(np.sum(omega**2, axis=-1)))
    contributions = np.mean(eigenvalues * projected_square, axis=(0, 1, 2))
    alignment = (np.mean(projected_square, axis=(0, 1, 2)) / omega_square
                 if omega_square > 1e-25 else None)
    local_stretching = np.sum(eigenvalues * projected_square, axis=-1)
    return dict(vorticity_square=omega_square,
                eigenframe_cosine_square_weighted=(alignment.tolist() if alignment is not None else None),
                eigenframe_stretching_contributions=contributions.tolist(),
                stretching=float(np.mean(local_stretching)),
                positive_part=float(np.mean(np.maximum(local_stretching, 0))),
                negative_part=float(np.mean(np.minimum(local_stretching, 0))))


def snapshot(sys, a, time, grid=32):
    psi = multipliers(sys)
    grad, omega, filtered, imaginary_error = spatial_fields(sys, a, grid, psi)
    strain = (grad + np.swapaxes(grad, -1, -2)) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(strain)
    full = eigen_statistics(omega, eigenvalues, eigenvectors)
    shells = [dict(level=j, **eigen_statistics(w, eigenvalues, eigenvectors))
              for j, w in enumerate(filtered)]
    n = sys.nonlinear(a)
    fourier_T = -float(np.real(np.einsum('i,ij,ij->', sys.square, a.conj(), n)))
    fourier_G = float(np.sum(sys.square[:, None] * abs(a)**2))
    fourier_D = float(np.sum(sys.square[:, None]**2 * abs(a)**2))
    assert abs(full['stretching'] - fourier_T) < 3e-8
    assert abs(full['vorticity_square'] - fourier_G) < 3e-8
    assert abs(sum(full['eigenframe_cosine_square_weighted'])-1) < 1e-10
    assert abs(sum(full['eigenframe_stretching_contributions'])-fourier_T) < 3e-8
    assert abs(sum(s['vorticity_square'] for s in shells)-fourier_G) < 3e-8
    assert imaginary_error < 1e-10
    assert float(np.max(abs(np.trace(strain, axis1=-2, axis2=-1)))) < 1e-10
    # At repeated eigenvalues only the spectral subspace, not its chosen basis,
    # is intrinsic. Report a numerical count rather than assigning a direction.
    gaps = np.diff(eigenvalues, axis=-1)
    repeated_fraction = float(np.mean(np.min(abs(gaps), axis=-1) < 1e-8))
    return dict(time=time, grid=grid, G=fourier_G, D=fourier_D,
                T=fourier_T, half_G_derivative=fourier_T-sys.nu*fourier_D,
                full=full, filtered_vorticity_shells=shells,
                repeated_eigenvalue_fraction_at_threshold_1e_8=repeated_fraction,
                numerical_checks=dict(max_imaginary_field_error=imaginary_error,
                    max_strain_trace_error=float(np.max(abs(np.trace(strain, axis1=-2, axis2=-1)))),
                    Fourier_minus_grid_T=fourier_T-full['stretching'],
                    Fourier_minus_grid_G=fourier_G-full['vorticity_square'],
                    sum_shell_stretching_minus_global=sum(s['stretching'] for s in shells)-fourier_T))


def run():
    results = []
    for cutoff in (4, 5):
        sys = System(N=cutoff, nu=NU)
        state = initial(sys, 0.0)
        captures = []
        for step in range(41):
            if step % 10 == 0:
                captures.append(snapshot(sys, state, step * DT))
            if step < 40:
                state = sys.rk4(state, DT)
        refined_spatial = snapshot(sys, state, 0.02, grid=40)
        results.append(dict(N=cutoff, mode_count=len(sys.modes),
                            captures=captures,
                            final_grid_40_T_difference=refined_spatial['full']['stretching']-captures[-1]['full']['stretching'],
                            final_grid_40_alignment_difference=(np.asarray(refined_spatial['full']['eigenframe_cosine_square_weighted'])-np.asarray(captures[-1]['full']['eigenframe_cosine_square_weighted'])).tolist()))
    return dict(trajectory='Unforced periodic Fourier-Galerkin N=4 and N=5; same aligned two-scale initial field',
                nu=NU, dt=DT, grid='32^3; final snapshot independently checked at 40^3',
                formula='T=<omega dot S omega>=sum_{r=1}^3 <lambda_r |omega dot e_r|^2>; lambda ascending',
                notes='omega-weighted cosine squares are undefined at omega=0 pointwise but computed via integrals. Filtered-vorticity quadratic forms with full S are not additive across shells; shell vorticity squares are additive due to the square partition. Individual eigenvector directions at degenerate eigenvalues are not intrinsic. Snapshots give no uniform-in-cutoff or time-integrated bound.',
                results=results)


if __name__ == '__main__':
    result = run()
    path = Path(__file__).with_name('strain_alignment_results.json')
    path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {path}')
    for run_data in result['results']:
        print('N', run_data['N'])
        for snap in run_data['captures']:
            print(f"  t={snap['time']:.3f} T={snap['T']:.6f} ",
                  'cos²=',np.round(snap['full']['eigenframe_cosine_square_weighted'],4),
                  'contributions=',np.round(snap['full']['eigenframe_stretching_contributions'],4),
                  f"shell_gap={snap['numerical_checks']['sum_shell_stretching_minus_global']:.5f}")
