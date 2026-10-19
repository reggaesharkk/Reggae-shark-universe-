"""WP13 endpoint-vorticity diagnostic.

Finite-p vorticity coefficients are rejected analytically by concentration.
This script compares the circular required L2 coefficient with finite-grid
vorticity norms and a rigorous finite-Fourier l1 envelope for ||omega||_inf.

Finite data are diagnostic only. Spatial vorticity is evaluated once per
state and reused for all reserve fractions.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import NU
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent


def high_transfer(system, a, s, K):
    weights = system.square.astype(float)**s
    high = system.square[system.left] > K*K
    out, left, right = (x[high] for x in
                        (system.out, system.left, system.right))
    qdot = np.einsum("ij,ij->i", system.qwaves[high], a[left])
    z = -1j*weights[out]*qdot*np.einsum(
        "ij,ij->i", np.conj(a[out]), a[right])
    return float(np.real(np.sum(z)))


def state_observables(system, a, s, K, grid):
    weights = system.square.astype(float)**s
    X = float(np.sum(weights[:, None]*abs(a)**2))
    Y = float(np.sum((weights*system.square)[:, None]*abs(a)**2))
    G = float(np.sum(system.square[:, None]*abs(a)**2))
    N_high = high_transfer(system, a, s, K)

    _, omega, _, imag = spatial_fields(system, a, grid)
    if imag > 1e-10:
        raise AssertionError(f"imaginary field error {imag}")
    mag = np.linalg.norm(omega, axis=-1)

    L2_grid = float(np.mean(mag**2))**0.5
    L4_grid = float(np.mean(mag**4))**0.25
    L8_grid = float(np.mean(mag**8))**0.125
    Linf_grid = float(np.max(mag))

    omega_l1_envelope = float(np.sum(
        np.sqrt(system.square)*np.linalg.norm(a, axis=1)
    ))

    if abs(L2_grid-math.sqrt(G)) > 5e-8*max(1.0, math.sqrt(G)):
        raise AssertionError("grid/Fourier L2 vorticity mismatch")

    return dict(
        X=X,
        Y=Y,
        G=G,
        high_transfer=N_high,
        omega_L2=math.sqrt(G),
        omega_L4_grid=L4_grid,
        omega_L8_grid=L8_grid,
        omega_Linf_grid=Linf_grid,
        omega_L1_fourier_envelope=omega_l1_envelope,
    )


def with_reserve(base, theta, nu):
    residual = max(base["high_transfer"]-theta*nu*base["Y"], 0.0)
    b_req = residual/base["X"] if base["X"] > 0 else 0.0

    def ratio(v):
        return b_req/v if v > 0 else 0.0

    return dict(
        **base,
        reserve_fraction=theta,
        b_required=b_req,
        ratio_b_over_L2=ratio(base["omega_L2"]),
        ratio_b_over_L4=ratio(base["omega_L4_grid"]),
        ratio_b_over_L8=ratio(base["omega_L8_grid"]),
        ratio_b_over_Linf_grid=ratio(base["omega_Linf_grid"]),
        ratio_b_over_L1_envelope=ratio(
            base["omega_L1_fourier_envelope"]
        ),
    )


def run(
    cutoffs=(4,7),
    scenarios=("reference","combined_double_quarter_high"),
    amplitudes=(1.0,2.0,4.0),
    thetas=(0.25,0.5,0.75),
    s=2.0,
    K=2,
    dt=0.0005,
    t_end=0.005,
    grid=32,
):
    if grid <= 3*max(cutoffs):
        raise ValueError("grid must exceed 3*max(cutoffs)")

    results = []
    steps = round(t_end/dt)

    for scenario in scenarios:
        for N in cutoffs:
            system = System(N=N, nu=NU)
            for amplitude in amplitudes:
                a = amplitude*make_initial(system, *SCENARIOS[scenario])
                rows_by_theta = {theta: [] for theta in thetas}

                for step in range(steps+1):
                    base = state_observables(system, a, s, K, grid)
                    for theta in thetas:
                        row = with_reserve(base, theta, system.nu)
                        row["time"] = step*dt
                        rows_by_theta[theta].append(row)
                    if step < steps:
                        a = system.rk4(a, dt)

                for theta in thetas:
                    rows = rows_by_theta[theta]
                    results.append(dict(
                        scenario=scenario,
                        N=N,
                        amplitude_multiplier=amplitude,
                        theta=theta,
                        max_ratio_L2=max(r["ratio_b_over_L2"] for r in rows),
                        max_ratio_L4=max(r["ratio_b_over_L4"] for r in rows),
                        max_ratio_L8=max(r["ratio_b_over_L8"] for r in rows),
                        max_ratio_Linf_grid=max(
                            r["ratio_b_over_Linf_grid"] for r in rows
                        ),
                        max_ratio_L1_envelope=max(
                            r["ratio_b_over_L1_envelope"] for r in rows
                        ),
                        rows=rows,
                    ))

    return dict(
        s=s,
        K=K,
        nu=NU,
        grid=grid,
        interval=[0.0,t_end],
        warning=(
            "b_required is circular. Grid Linf is a sampled lower estimate "
            "of the true continuum supremum. The Fourier l1 envelope is a "
            "rigorous finite-mode upper bound on ||omega||_inf. "
            "Finite-p coefficient failure is analytical, not inferred from "
            "these trajectories."
        ),
        results=results,
    )


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument(
        "--output", type=Path,
        default=HERE/"wp13_endpoint_vorticity_results.json"
    )
    p.add_argument("--t-end", type=float, default=0.005)
    p.add_argument("--grid", type=int, default=32)
    a=p.parse_args()
    result=run(t_end=a.t_end, grid=a.grid)
    a.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", a.output)
    rows=sorted(
        result["results"],
        key=lambda x:x["max_ratio_Linf_grid"],
        reverse=True
    )[:12]
    for r in rows:
        print(
            r["scenario"], "N=",r["N"], "A=",r["amplitude_multiplier"],
            "theta=",r["theta"],
            "max b/Linf(grid)=",r["max_ratio_Linf_grid"],
            "max b/L1env=",r["max_ratio_L1_envelope"]
        )
