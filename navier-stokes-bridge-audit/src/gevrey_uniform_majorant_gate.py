"""Verify the cutoff-independent Gevrey product majorant on repository states.

Analytical gate:
  |N_sigma,s| <= C_s^G X_sigma,s sqrt(Y_sigma,s)
with C_s^G=2*c_s*K_s and
  K_s^2=sum_{m in Z^3\\{0}} |m|^{-2s}.

The full K_s is an infinite-lattice constant and is proved finite for s>3/2.
This script uses a finite-radius lower approximation to C_s^G only as a
diagnostic reference; numerical checks do not prove the theorem.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from smooth_gevrey_identity_audit import (
    functionals,
    schedule_persistence,
    schedule_smoothing,
)

HERE = Path(__file__).resolve().parent


def polynomial_constant(s):
    return 1.0 if s <= 1.0 else 2.0**(s-1.0)


def truncated_K_s(s, radius=60):
    total = 0.0
    R2 = radius*radius
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            for k in range(-radius, radius+1):
                r2 = i*i+j*j+k*k
                if r2 == 0 or r2 > R2:
                    continue
                total += r2**(-s)
    return math.sqrt(total)


def evolve(sys, scenario, dt, steps):
    state = make_initial(sys, *SCENARIOS[scenario])
    states = [state.copy()]
    for _ in range(steps):
        state = sys.rk4(state, dt)
        states.append(state.copy())
    return states


def state_checks(sys, a):
    zero = sys.index[(0,0,0)]
    mean_norm = float(np.linalg.norm(a[zero]))
    divergence = float(np.max(np.abs(
        np.einsum("ij,ij->i", sys.waves, a)
    )))
    reality = float(np.max(np.linalg.norm(
        a[sys.neg]-np.conj(a), axis=1
    )))
    return mean_norm, divergence, reality


def run(cutoffs, scenarios, s=2.0, dt=DT, t_end=0.005, lattice_radius=60):
    if s <= 1.5:
        raise ValueError("Require s>3/2.")

    steps = round(t_end/dt)
    capture = sorted(set([0, steps//2, steps]))
    c_poly = polynomial_constant(s)
    K_trunc = truncated_K_s(s, lattice_radius)
    C_trunc = 2*c_poly*K_trunc

    rows = []
    schedules = {
        "persistence": schedule_persistence,
        "smoothing": schedule_smoothing,
    }

    for scenario in scenarios:
        for N in cutoffs:
            sys = System(N=N, nu=NU)
            states = evolve(sys, scenario, dt, steps)
            schedule_rows = {}

            for schedule_name, schedule in schedules.items():
                samples = []
                for j in capture:
                    t = j*dt
                    sigma, sigma_prime = schedule(t)
                    if sigma_prime is None:
                        continue

                    a = states[j]
                    mean_norm, divergence, reality = state_checks(sys, a)
                    if mean_norm > 1e-12:
                        raise AssertionError(
                            f"Nonzero mean in {scenario} N={N}: {mean_norm}"
                        )
                    if divergence > 1e-9 or reality > 1e-9:
                        raise AssertionError("State invariants failed.")

                    X, Y, Z, nonlinear, _ = functionals(
                        sys, a, s, sigma
                    )
                    lam_strong = (
                        abs(nonlinear)/(X*math.sqrt(Y))
                        if X > 0 and Y > 0 else None
                    )
                    lam_weak = (
                        abs(nonlinear)/(math.sqrt(X)*Y)
                        if X > 0 and Y > 0 else None
                    )

                    samples.append(dict(
                        time=t,
                        sigma=sigma,
                        X=X,
                        Y=Y,
                        Z=Z,
                        nonlinear=nonlinear,
                        Lambda_strong=lam_strong,
                        Lambda_weak=lam_weak,
                        truncated_constant_reference=C_trunc,
                        mean_norm=mean_norm,
                        divergence_error=divergence,
                        reality_error=reality,
                    ))

                schedule_rows[schedule_name] = samples

            rows.append(dict(
                scenario=scenario,
                N=N,
                schedules=schedule_rows,
            ))

    return dict(
        theorem_target=(
            "|N| <= C_s^G X sqrt(Y) <= C_s^G sqrt(X) Y, "
            "C_s^G=2*c_s*K_s independent of cutoff N and sigma"
        ),
        s=s,
        c_s=c_poly,
        lattice_radius_for_diagnostic= lattice_radius,
        truncated_K_s=K_trunc,
        truncated_constant_reference=C_trunc,
        warning=(
            "The finite-radius lattice sum is a lower approximation to the "
            "full analytical constant, not a proof upper bound. "
            "Cutoff independence comes from the analytic convolution proof."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cutoffs", nargs="+", type=int, default=[4,7])
    p.add_argument(
        "--scenarios", nargs="+", choices=list(SCENARIOS),
        default=["reference","combined_double_quarter_high"]
    )
    p.add_argument("--s", type=float, default=2.0)
    p.add_argument("--dt", type=float, default=DT)
    p.add_argument("--t-end", type=float, default=0.005)
    p.add_argument("--lattice-radius", type=int, default=60)
    p.add_argument(
        "--output", type=Path,
        default=HERE/"gevrey_uniform_majorant_results.json"
    )
    a = p.parse_args()
    result = run(
        a.cutoffs, a.scenarios, a.s, a.dt, a.t_end, a.lattice_radius
    )
    a.output.write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8"
    )
    print("Wrote", a.output)
    print("truncated_constant_reference=",
          result["truncated_constant_reference"])
