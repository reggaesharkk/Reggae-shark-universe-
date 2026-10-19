"""High-vorticity sampled coherence-radius diagnostic.

Restricts pairs to points satisfying |omega| >= 2 sqrt(G) at both endpoints,
then measures finite-grid direction slopes |sin(theta)|/|h| and determinant
slopes at three axis-aligned offsets.

This is a diagnostic threshold and sampled proxy, not the Constantin-Fefferman
hypothesis itself.
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
THRESHOLD_MULTIPLIER = 2.0


def snapshot(sys, a):
    _, omega, _, imaginary = spatial_fields(sys, a, GRID)
    assert imaginary < 1e-10

    magnitude = np.linalg.norm(omega, axis=-1)
    G = float(np.mean(magnitude**2))
    threshold = THRESHOLD_MULTIPLIER*np.sqrt(G)

    direction = np.zeros_like(omega)
    nonzero = magnitude > 1e-12
    direction[nonzero] = omega[nonzero] / magnitude[nonzero, None]

    spacing = 2*np.pi/GRID
    scales = []

    for step in OFFSETS:
        slopes = []
        determinant_slopes = []

        for axis in range(3):
            magnitude_y = np.roll(magnitude, -step, axis=axis)
            direction_y = np.roll(direction, -step, axis=axis)
            mask = (magnitude >= threshold) & (magnitude_y >= threshold)

            cross = np.cross(direction, direction_y)
            radius = step*spacing
            slopes.extend(
                (np.linalg.norm(cross, axis=-1)[mask]/radius).tolist()
            )
            determinant_slopes.extend(
                (np.abs(cross[..., axis])[mask]/radius).tolist()
            )

        slopes = np.asarray(slopes)
        determinant_slopes = np.asarray(determinant_slopes)

        if len(slopes):
            Lmax = float(np.max(slopes))
            L95 = float(np.quantile(slopes, .95))
            Lmean = float(np.mean(slopes))
            Dmax = float(np.max(determinant_slopes))
            D95 = float(np.quantile(determinant_slopes, .95))
            rho_sample_upper = 1.0/Lmax if Lmax else None
        else:
            Lmax = L95 = Lmean = Dmax = D95 = rho_sample_upper = None

        scales.append(dict(
            grid_step=step,
            radius=step*spacing,
            pair_count=int(len(slopes)),
            Lmax=Lmax,
            L95=L95,
            Lmean=Lmean,
            determinant_max=Dmax,
            determinant_95=D95,
            sampled_coherence_radius_upper=rho_sample_upper,
        ))

    return dict(G=G, threshold=threshold, scales=scales)


def run():
    rows = []
    for scenario, N in sorted(TRACK):
        sys = System(N=N, nu=NU)
        state = make_initial(sys, *SCENARIOS[scenario])
        samples = []

        for step in range(max(CAPTURE_STEPS)+1):
            if step in CAPTURE_STEPS:
                entry = snapshot(sys, state)
                entry["time"] = step*DT
                samples.append(entry)
            if step < max(CAPTURE_STEPS):
                state = sys.rk4(state, DT)

        rows.append(dict(scenario=scenario, N=N, samples=samples))

    return dict(
        grid=GRID,
        offsets=list(OFFSETS),
        threshold_rule="|omega| >= 2 sqrt(G) at both endpoints",
        interval=[0.0, max(CAPTURE_STEPS)*DT],
        interpretation=(
            "For sampled pairs, Lmax=max |sin(theta)|/|h|. "
            "If a Lipschitz-style coherence inequality "
            "|sin(theta)| <= |h|/rho held on all sampled pairs, "
            "then rho cannot exceed 1/Lmax."
        ),
        warning=(
            "The moving threshold 2 sqrt(G), finite grid, axis-aligned offsets, "
            "and sampled maximum are diagnostic choices. This is not the "
            "Constantin-Fefferman theorem and does not establish a continuum "
            "coherence radius."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "high_vorticity_coherence_radius_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
