"""WP14 endpoint-geometry coupling diagnostic.

Matches the circular endpoint-normalized target Gamma_req with dimensionless
direction, strain, and H2 high-tail triadic-coherence diagnostics on the same
Galerkin state.

Finite data select future hypotheses only; they do not prove WP11 L2-L3.
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


def fourier_quantities(system, a, s, K):
    weights = system.square.astype(float)**s
    X = float(np.sum(weights[:, None]*abs(a)**2))
    Y = float(np.sum((weights*system.square)[:, None]*abs(a)**2))
    G = float(np.sum(system.square[:, None]*abs(a)**2))
    D = float(np.sum(
        (system.square.astype(float)**2)[:, None]*abs(a)**2
    ))

    high = system.square[system.left] > K*K
    out, left, right = (
        x[high] for x in (system.out, system.left, system.right)
    )
    qdot = np.einsum("ij,ij->i", system.qwaves[high], a[left])
    raw = 1j*qdot[:, None]*a[right]
    projected = np.einsum(
        "kij,kj->ki", system.projectors[out], raw
    )
    z = -weights[out]*np.einsum(
        "ij,ij->i", np.conj(a[out]), projected
    )

    N_high = float(np.real(np.sum(z)))
    A_high = float(np.sum(np.abs(z)))
    chi_high = N_high/A_high if A_high else 0.0

    # Independent direct high-tail reconstruction without the projector in the
    # pairing: a_k is divergence free, so <a_k,P_k v>=<a_k,v>.
    direct = -float(np.real(np.sum(
        weights[out]
        * qdot
        * 1j
        * np.einsum("ij,ij->i", np.conj(a[out]), a[right])
    )))
    err = abs(N_high-direct)/max(1.0, abs(N_high), abs(direct))
    if err > 2e-12:
        raise AssertionError(f"high-tail triad reconstruction error {err}")

    return dict(
        X=X, Y=Y, G=G, D=D,
        high_transfer=N_high,
        high_triad_envelope=A_high,
        chi_H2_high=chi_high,
        high_transfer_reconstruction_error=err,
    )


def spatial_geometry(system, a, G, D, grid):
    grad, omega, _, imag = spatial_fields(system, a, grid)
    if imag > 1e-10:
        raise AssertionError(f"imaginary field error {imag}")

    magnitude = np.linalg.norm(omega, axis=-1)
    omega_linf = float(np.max(magnitude))
    grid_G = float(np.mean(magnitude**2))
    if abs(grid_G-G) > 5e-8*max(1.0, G):
        raise AssertionError("grid/Fourier G mismatch")

    strain = (grad + np.swapaxes(grad, -1, -2))/2
    local_stretch = np.einsum(
        "...i,...ij,...j->...", omega, strain, omega
    )
    positive_stretch = float(np.mean(np.maximum(local_stretch, 0.0)))
    g_stretch = (
        positive_stretch/(omega_linf*G)
        if omega_linf > 0 and G > 0 else 0.0
    )

    ell = math.sqrt(G/D) if D > 0 else None

    threshold = 2.0*math.sqrt(G)
    direction = np.zeros_like(omega)
    nonzero = magnitude > 1e-12
    direction[nonzero] = omega[nonzero]/magnitude[nonzero, None]

    spacing = 2*math.pi/grid
    slopes = []
    determinant_slopes = []
    for axis in range(3):
        mag_y = np.roll(magnitude, -1, axis=axis)
        dir_y = np.roll(direction, -1, axis=axis)
        mask = (magnitude >= threshold) & (mag_y >= threshold)
        cross = np.cross(direction, dir_y)
        slopes.extend(
            (np.linalg.norm(cross, axis=-1)[mask]/spacing).tolist()
        )
        determinant_slopes.extend(
            (np.abs(cross[..., axis])[mask]/spacing).tolist()
        )

    if slopes:
        Lmax = float(np.max(slopes))
        L95 = float(np.quantile(slopes, 0.95))
        detmax = float(np.max(determinant_slopes))
        pair_count = len(slopes)
        g_dir = ell*Lmax if ell is not None else None
        R_sample = 1.0/g_dir if g_dir and g_dir > 0 else None
    else:
        Lmax = L95 = detmax = g_dir = R_sample = None
        pair_count = 0

    # Rigorous finite-Fourier endpoint envelope.
    omega_l1_envelope = float(np.sum(
        np.sqrt(system.square)*np.linalg.norm(a, axis=1)
    ))

    return dict(
        omega_Linf_grid=omega_linf,
        omega_L1_fourier_envelope=omega_l1_envelope,
        ell_omega=ell,
        high_vorticity_pair_count=pair_count,
        direction_Lmax=Lmax,
        direction_L95=L95,
        determinant_Lmax=detmax,
        g_direction= g_dir,
        R_sample=R_sample,
        positive_stretching=positive_stretch,
        g_stretch=g_stretch,
    )


def add_reserve(base, theta, nu):
    residual = max(
        base["high_transfer"] - theta*nu*base["Y"], 0.0
    )
    b_req = residual/base["X"] if base["X"] > 0 else 0.0
    linf = base["omega_Linf_grid"]
    envelope = base["omega_L1_fourier_envelope"]

    gamma_grid = b_req/linf if linf > 0 else 0.0
    gamma_envelope = b_req/envelope if envelope > 0 else 0.0

    row = dict(base)
    row.update(
        reserve_fraction=theta,
        positive_residual=residual,
        b_required=b_req,
        Gamma_req_grid=gamma_grid,
        Gamma_req_fourier_envelope=gamma_envelope,
    )
    return row


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

    steps = round(t_end/dt)
    results = []

    for scenario in scenarios:
        for N in cutoffs:
            system = System(N=N, nu=NU)
            for amplitude in amplitudes:
                a = amplitude*make_initial(
                    system, *SCENARIOS[scenario]
                )
                rows_by_theta = {theta: [] for theta in thetas}

                for step in range(steps+1):
                    fq = fourier_quantities(system, a, s, K)
                    geom = spatial_geometry(
                        system, a, fq["G"], fq["D"], grid
                    )
                    base = dict(**fq, **geom, time=step*dt)

                    for theta in thetas:
                        rows_by_theta[theta].append(
                            add_reserve(base, theta, system.nu)
                        )

                    if step < steps:
                        a = system.rk4(a, dt)

                for theta in thetas:
                    rows = rows_by_theta[theta]
                    active = [r for r in rows if r["Gamma_req_grid"] > 0]

                    def max_or_none(key):
                        vals = [
                            r[key] for r in active
                            if r[key] is not None
                        ]
                        return max(vals) if vals else None

                    results.append(dict(
                        scenario=scenario,
                        N=N,
                        amplitude_multiplier=amplitude,
                        theta=theta,
                        active_samples=len(active),
                        max_Gamma_req_grid=max_or_none("Gamma_req_grid"),
                        max_Gamma_req_fourier_envelope=max_or_none(
                            "Gamma_req_fourier_envelope"
                        ),
                        max_g_direction=max_or_none("g_direction"),
                        max_g_stretch=max_or_none("g_stretch"),
                        max_abs_chi_H2_high=(
                            max(abs(r["chi_H2_high"]) for r in active)
                            if active else None
                        ),
                        rows=rows,
                    ))

    # Pool active rows for transparent descriptive correlations only.
    pooled = []
    for case in results:
        for row in case["rows"]:
            if row["Gamma_req_grid"] <= 0:
                continue
            pooled.append(row)

    correlations = {}
    if len(pooled) >= 3:
        target = np.array([r["Gamma_req_grid"] for r in pooled])
        for key in ("g_direction", "g_stretch", "chi_H2_high"):
            pairs = [
                (r["Gamma_req_grid"], r[key])
                for r in pooled if r[key] is not None
            ]
            if len(pairs) >= 3:
                x=np.array([p[0] for p in pairs])
                y=np.array([p[1] for p in pairs])
                correlations[key] = float(np.corrcoef(x,y)[0,1])

    return dict(
        definition=(
            "Gamma_req_grid=b_required/omega_Linf_grid; "
            "g_direction=ell_omega*Lmax; "
            "g_stretch=<positive omega.S.omega>/(omega_Linf_grid*G); "
            "chi_H2_high=N_H2_high/sum|Z_H2_high|"
        ),
        warning=(
            "All correlations are descriptive and pool dependent states. "
            "Gamma_req is circular; grid Linf and direction metrics are "
            "finite-grid diagnostics; chi_H2_high has an uncontrolled cubic "
            "envelope. No fitted relationship is an a priori estimate."
        ),
        s=s, K=K, nu=NU, grid=grid,
        interval=[0.0,t_end],
        descriptive_pearson_active_pool=correlations,
        results=results,
    )


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument(
        "--output", type=Path,
        default=HERE/"wp14_endpoint_geometry_results.json"
    )
    p.add_argument("--t-end", type=float, default=0.005)
    p.add_argument("--grid", type=int, default=32)
    a=p.parse_args()
    result=run(t_end=a.t_end, grid=a.grid)
    a.output.write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8"
    )
    print("Wrote", a.output)
    print(
        "descriptive active-pool Pearson:",
        result["descriptive_pearson_active_pool"]
    )
    top=sorted(
        result["results"],
        key=lambda x:x["max_Gamma_req_grid"] or -1,
        reverse=True
    )[:12]
    for r in top:
        print(
            r["scenario"],"N=",r["N"],"A=",r["amplitude_multiplier"],
            "theta=",r["theta"],
            "active=",r["active_samples"],
            "maxGamma=",r["max_Gamma_req_grid"],
            "maxgdir=",r["max_g_direction"],
            "maxgstretch=",r["max_g_stretch"],
            "max|chi2high|=",r["max_abs_chi_H2_high"],
        )
