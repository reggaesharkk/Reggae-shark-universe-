"""Local vorticity-direction depletion diagnostic.

Computes Constantin-Fefferman-inspired local direction-misalignment proxies on
the same four tracked Galerkin trajectories used by the triadic coherence gate.

These are local finite-grid proxies, not an evaluation of the full periodic
Biot-Savart stretching kernel and not a regularity criterion.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent
TRACK = {
    ("reference", 4),
    ("reference", 7),
    ("combined_double_quarter_high", 4),
    ("combined_double_quarter_high", 7),
}
CAPTURE_STEPS = (0, 10, 20, 30)
GRID = 32
OFFSETS = (1, 2, 4)


def local_direction_proxy(sys, a, grid=GRID, offsets=OFFSETS):
    grad, omega, _, imaginary = spatial_fields(sys, a, grid)
    assert imaginary < 1e-10

    magnitude = np.linalg.norm(omega, axis=-1)
    direction = np.zeros_like(omega)
    nonzero = magnitude > 1e-12
    direction[nonzero] = omega[nonzero] / magnitude[nonzero, None]

    spacing = 2*np.pi/grid
    scale_rows = []

    for step in offsets:
        raw = 0.0
        angular = 0.0
        determinant = 0.0

        for axis in range(3):
            magnitude_y = np.roll(magnitude, -step, axis=axis)
            direction_y = np.roll(direction, -step, axis=axis)

            cross = np.cross(direction, direction_y)
            sin_angle = np.linalg.norm(cross, axis=-1)
            determinant_factor = np.abs(cross[..., axis])

            weight = magnitude**2 * magnitude_y
            radius = step*spacing
            kernel = radius**-3

            raw += float(np.mean(weight))*kernel
            angular += float(np.mean(weight*sin_angle))*kernel
            determinant += float(np.mean(weight*determinant_factor))*kernel

        scale_rows.append(dict(
            grid_step=step,
            radius=step*spacing,
            angular_ratio=(angular/raw if raw else 0.0),
            determinant_ratio=(determinant/raw if raw else 0.0),
        ))

    strain = (grad + np.swapaxes(grad, -1, -2))/2
    local_stretching = np.einsum(
        "...i,...ij,...j->...", omega, strain, omega)
    T = float(np.mean(local_stretching))
    G = float(np.mean(magnitude**2))

    n = sys.nonlinear(a)
    fourier_T = -float(np.real(np.einsum(
        "i,ij,ij->", sys.square, np.conj(a), n)))
    fourier_G = float(np.sum(sys.square[:, None]*abs(a)**2))

    assert abs(T-fourier_T) < 3e-8*max(1.0, abs(fourier_T))
    assert abs(G-fourier_G) < 3e-8*max(1.0, abs(fourier_G))

    return dict(
        G=G,
        T=T,
        scales=scale_rows,
    )


def run():
    rows = []
    for scenario, N in sorted(TRACK):
        sys = System(N=N, nu=NU)
        state = make_initial(sys, *SCENARIOS[scenario])
        samples = []
        for step in range(max(CAPTURE_STEPS)+1):
            if step in CAPTURE_STEPS:
                entry = local_direction_proxy(sys, state)
                entry["time"] = step*DT
                samples.append(entry)
            if step < max(CAPTURE_STEPS):
                state = sys.rk4(state, DT)
        rows.append(dict(scenario=scenario, N=N, samples=samples))

    return dict(
        grid=GRID,
        offsets=list(OFFSETS),
        tracked_cases=[list(x) for x in sorted(TRACK)],
        interval=[0.0, max(CAPTURE_STEPS)*DT],
        definition=(
            "For axis-aligned offsets h, weight by "
            "|omega(x)|^2|omega(x+h)|/|h|^3. "
            "angular_ratio inserts |xi(x) cross xi(x+h)|; "
            "determinant_ratio inserts "
            "|(xi(x) cross xi(x+h)) dot h_hat|."
        ),
        literature_context=(
            "Inspired by Constantin-Fefferman vorticity-direction depletion. "
            "The exact theorem uses geometric coherence in high-vorticity "
            "regions; this script is only a finite-grid local proxy."
        ),
        warning=(
            "Not the full periodic Biot-Savart kernel, not a proof criterion, "
            "and not a continuum limit. Grid offsets are fixed physical "
            "separations on a 32^3 torus grid. Values can be grid-sensitive."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "direction_depletion_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
