"""WP15 positive-stretching coefficient stress test.

Tests the finite-field quotient

  C_req_stretch =
    max(N_H2_high - theta*nu*Y2, 0) / (b_stretch*X2),

where
  b_stretch = <(omega.S.omega)_+>/G.

This is a falsification screen only, not a proof of a uniform constant.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from strain_alignment_trajectory import spatial_fields
from triadic_envelope_growth_gate import dense_field

HERE = Path(__file__).resolve().parent
SEEDS = tuple(range(20260925, 20260935))


def quantities(system, a, s=2.0, K=2, theta=0.25, grid=24):
    weights = system.square.astype(float)**s
    X = float(np.sum(weights[:, None]*abs(a)**2))
    Y = float(np.sum((weights*system.square)[:, None]*abs(a)**2))
    G = float(np.sum(system.square[:, None]*abs(a)**2))

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

    grad, omega, _, imag = spatial_fields(system, a, grid)
    if imag > 1e-10:
        raise AssertionError(f"imaginary field error {imag}")
    grid_G = float(np.mean(np.sum(omega**2, axis=-1)))
    if abs(grid_G-G) > 5e-8*max(1.0,G):
        raise AssertionError("grid/Fourier G mismatch")

    strain = (grad + np.swapaxes(grad,-1,-2))/2
    local = np.einsum("...i,...ij,...j->...",omega,strain,omega)
    positive = float(np.mean(np.maximum(local,0.0)))
    signed = float(np.mean(local))

    # Independent Fourier H1 signed transfer.
    n = system.nonlinear(a)
    T1 = -float(np.real(np.einsum(
        "i,ij,ij->", system.square, np.conj(a), n
    )))
    if abs(signed-T1) > 5e-8*max(1.0,abs(T1)):
        raise AssertionError("grid/Fourier H1 stretching mismatch")

    b_stretch = positive/G if G > 0 else 0.0
    residual = max(N_high-theta*system.nu*Y,0.0)
    denominator = b_stretch*X
    C_req = residual/denominator if denominator > 0 else (
        float("inf") if residual > 0 else 0.0
    )

    return dict(
        X=X,Y=Y,G=G,
        H2_high_transfer=N_high,
        H1_signed_stretching=T1,
        H1_positive_stretching=positive,
        b_stretch=b_stretch,
        reserve=theta*system.nu*Y,
        positive_residual=residual,
        C_required_stretch=C_req,
    )


def run(
    cutoffs=(3,4,5,6,7),
    families=("ball","outer_half"),
    seeds=SEEDS,
    amplitude=4.0,
    s=2.0,
    K=2,
    theta=0.25,
    grid=24,
):
    if grid <= 3*max(cutoffs):
        raise ValueError("grid must exceed 3*max(cutoffs)")

    rows=[]
    for family in families:
        for N in cutoffs:
            system=System(N=N,nu=NU)
            samples=[]
            for seed in seeds:
                # dense_field has G=1 before the amplitude multiplier.
                a=amplitude*dense_field(system,seed,family)
                q=quantities(system,a,s=s,K=K,theta=theta,grid=grid)
                samples.append(dict(seed=seed,**q))
            finite=[
                x["C_required_stretch"] for x in samples
                if np.isfinite(x["C_required_stretch"])
            ]
            rows.append(dict(
                family=family,
                N=N,
                amplitude=amplitude,
                theta=theta,
                samples=samples,
                max_C_required=(max(finite) if finite else None),
                median_C_required=(
                    float(np.median(finite)) if finite else None
                ),
                positive_residual_count=sum(
                    x["positive_residual"]>0 for x in samples
                ),
            ))

    return dict(
        definition=(
            "C_required_stretch="
            "max(N_H2_high-theta*nu*Y2,0)/(b_stretch*X2), "
            "b_stretch=<positive omega.S.omega>/G"
        ),
        seeds=list(seeds),
        cutoffs=list(cutoffs),
        families=list(families),
        amplitude=amplitude,
        theta=theta,
        s=s,
        K=K,
        grid=grid,
        warning=(
            "Deterministic finite random stress test only. "
            "A bounded sample does not prove a cutoff-independent constant; "
            "growth with N does not prove asymptotic divergence."
        ),
        rows=rows,
    )


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument(
        "--output",type=Path,
        default=HERE/"wp15_positive_stretching_results.json"
    )
    p.add_argument("--grid",type=int,default=24)
    p.add_argument("--amplitude",type=float,default=4.0)
    p.add_argument("--theta",type=float,default=0.25)
    a=p.parse_args()
    result=run(grid=a.grid,amplitude=a.amplitude,theta=a.theta)
    a.output.write_text(
        json.dumps(result,indent=2)+"\n",encoding="utf-8"
    )
    print("Wrote",a.output)
    for row in sorted(
        result["rows"],
        key=lambda x:(x["max_C_required"] or -1),
        reverse=True
    ):
        print(
            row["family"],"N=",row["N"],
            "positive=",row["positive_residual_count"],
            "medianC=",row["median_C_required"],
            "maxC=",row["max_C_required"]
        )
