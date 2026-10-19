"""Exact Gevrey weighted-identity audit on the repository Galerkin system.

This module does NOT fit exponential Fourier tails. It verifies the exact
finite-Galerkin identity

  1/2 dX/dt + nu Y = N + sigma'(t) Z

using the real repository ODE, then performs an independent centered
finite-difference cross-check and records descriptive nonlinear ratios.

Finite cutoff behavior is diagnostic only and is not a continuum analyticity
radius or regularity theorem.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU

HERE = Path(__file__).resolve().parent


def schedule_persistence(t, sigma0=0.2, gamma=0.5):
    raw = sigma0 - gamma*t
    if raw > 0:
        return raw, -gamma
    return 0.0, 0.0


def schedule_smoothing(t, alpha=0.1, nu=NU):
    if t <= 0:
        return 0.0, None
    sigma = alpha*math.sqrt(nu*t)
    sigma_prime = alpha*nu/(2*math.sqrt(nu*t))
    return sigma, sigma_prime


def functionals(sys, a, s, sigma):
    r = np.sqrt(sys.square.astype(float))
    positive = r > 0
    weight = np.zeros_like(r)
    weight[positive] = np.exp(2*sigma*r[positive]) * r[positive]**(2*s)

    norm2 = np.sum(np.abs(a)**2, axis=1)
    X = float(np.dot(weight, norm2))
    Y = float(np.dot(weight*sys.square, norm2))
    Z = float(np.dot(weight*r, norm2))

    B = sys.nonlinear(a)
    nonlinear = -float(np.real(np.einsum(
        "i,ij,ij->", weight, np.conj(a), B
    )))
    return X, Y, Z, nonlinear, weight


def exact_identity(sys, a, s, sigma, sigma_prime):
    X, Y, Z, nonlinear, weight = functionals(sys, a, s, sigma)
    rhs = sys.rhs(a)

    state_half_derivative = float(np.real(np.einsum(
        "i,ij,ij->", weight, np.conj(a), rhs
    )))
    half_dX_dt = state_half_derivative + sigma_prime*Z

    lhs = half_dX_dt + sys.nu*Y
    rhs_identity = nonlinear + sigma_prime*Z
    residual = lhs - rhs_identity
    residual_scale = max(
        1.0, abs(lhs), abs(rhs_identity), abs(nonlinear),
        abs(sigma_prime*Z), abs(sys.nu*Y)
    )
    relative_residual = abs(residual)/residual_scale

    return dict(
        X=X,
        Y=Y,
        Z=Z,
        nonlinear=nonlinear,
        half_dX_dt=half_dX_dt,
        lhs=lhs,
        rhs=rhs_identity,
        identity_residual=residual,
        identity_relative_residual=relative_residual,
        ratio_absN_over_sqrtX_Y=(
            abs(nonlinear)/(math.sqrt(X)*Y) if X > 0 and Y > 0 else None
        ),
        ratio_absN_over_X_sqrtY=(
            abs(nonlinear)/(X*math.sqrt(Y)) if X > 0 and Y > 0 else None
        ),
        ratio_absN_over_Y=(
            abs(nonlinear)/Y if Y > 0 else None
        ),
    )


def evolve_states(sys, scenario, dt, steps):
    state = make_initial(sys, *SCENARIOS[scenario])
    out = [state.copy()]
    for _ in range(steps):
        state = sys.rk4(state, dt)
        out.append(state.copy())
    return out


def centered_fd_X(sys, states, index, dt, s, schedule):
    if index <= 0 or index >= len(states)-1:
        return None
    t_minus = (index-1)*dt
    t_plus = (index+1)*dt
    sigma_minus, _ = schedule(t_minus)
    sigma_plus, _ = schedule(t_plus)
    X_minus = functionals(sys, states[index-1], s, sigma_minus)[0]
    X_plus = functionals(sys, states[index+1], s, sigma_plus)[0]
    return (X_plus-X_minus)/(2*dt)


def audit_case(N, scenario, s, dt, steps, capture_steps):
    sys = System(N=N, nu=NU)
    states = evolve_states(sys, scenario, dt, steps)

    schedules = {
        "persistence": schedule_persistence,
        "smoothing": schedule_smoothing,
    }
    result = {}

    for name, schedule in schedules.items():
        rows = []
        for j in capture_steps:
            t = j*dt
            sigma, sigma_prime = schedule(t)
            if sigma_prime is None:
                continue

            exact = exact_identity(
                sys, states[j], s, sigma, sigma_prime
            )
            fd = centered_fd_X(
                sys, states, j, dt, s, schedule
            )
            if fd is not None:
                exact["centered_fd_dX_dt"] = fd
                exact["centered_fd_minus_exact_dX_dt"] = (
                    fd - 2*exact["half_dX_dt"]
                )
                exact["centered_fd_relative_error"] = (
                    abs(exact["centered_fd_minus_exact_dX_dt"])
                    / max(1.0, abs(2*exact["half_dX_dt"]))
                )
            else:
                exact["centered_fd_dX_dt"] = None
                exact["centered_fd_minus_exact_dX_dt"] = None
                exact["centered_fd_relative_error"] = None

            exact["time"] = t
            exact["sigma"] = sigma
            exact["sigma_prime"] = sigma_prime
            rows.append(exact)

        max_identity = max(abs(r["identity_residual"]) for r in rows)
        max_relative_identity = max(
            r["identity_relative_residual"] for r in rows
        )
        finite_fd = [
            r["centered_fd_relative_error"]
            for r in rows
            if r["centered_fd_relative_error"] is not None
            and r["time"] >= 2*dt
        ]
        result[name] = dict(
            rows=rows,
            max_abs_identity_residual=max_identity,
            max_relative_identity_residual=max_relative_identity,
            max_relative_centered_fd_error_away_from_t0=(
                max(finite_fd) if finite_fd else None
            ),
        )

    return dict(
        scenario=scenario,
        N=N,
        mode_count=len(sys.modes),
        ordered_convolution_pairs=len(sys.out),
        s=s,
        dt=dt,
        schedules=result,
    )


def run(cutoffs, scenarios, s=2.0, dt=DT, t_end=0.005):
    if s <= 1.5:
        raise ValueError("This v0.2 audit requires s>3/2.")
    steps = round(t_end/dt)
    assert math.isclose(steps*dt, t_end, abs_tol=1e-14)

    capture_steps = sorted(set(
        [1, steps//2, steps] + [j for j in range(0, steps+1)
                                if math.isclose((j*dt) % 0.005, 0.0, abs_tol=1e-12)]
    ))

    rows = [
        audit_case(N, scenario, s, dt, steps, capture_steps)
        for scenario in scenarios
        for N in cutoffs
    ]

    max_identity = max(
        block["max_abs_identity_residual"]
        for row in rows
        for block in row["schedules"].values()
    )
    max_relative_identity = max(
        block["max_relative_identity_residual"]
        for row in rows
        for block in row["schedules"].values()
    )
    if max_relative_identity > 1e-12:
        raise AssertionError(
            f"Gevrey relative identity residual too large: "
            f"{max_relative_identity}"
        )

    return dict(
        identity="1/2 dX/dt + nu Y = N_sigma,s + sigma'(t) Z",
        s=s,
        nu=NU,
        dt=dt,
        interval=[0.0, t_end],
        cutoffs=cutoffs,
        scenarios=scenarios,
        schedules={
            "persistence":{
                "sigma":"max(0.2 - 0.5 t, 0)",
                "sigma_prime":"-0.5 while positive, else 0",
            },
            "smoothing":{
                "sigma":"0.1 sqrt(nu t)",
                "sigma_prime":"0.1 nu/(2 sqrt(nu t)), t>0",
            },
        },
        warning=(
            "Finite Galerkin identity audit only. Descriptive nonlinear "
            "ratios are not registered majorants and finite cutoff behavior "
            "does not establish cutoff-uniform analyticity or regularity."
        ),
        max_abs_identity_residual=max_identity,
        max_relative_identity_residual=max_relative_identity,
        rows=rows,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoffs", nargs="+", type=int, default=[4, 7])
    parser.add_argument(
        "--scenarios",
        nargs="+",
        choices=list(SCENARIOS),
        default=["reference", "combined_double_quarter_high"],
    )
    parser.add_argument("--s", type=float, default=2.0)
    parser.add_argument("--dt", type=float, default=DT)
    parser.add_argument("--t-end", type=float, default=0.005)
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "smooth_gevrey_identity_results.json",
    )
    args = parser.parse_args()

    result = run(
        args.cutoffs, args.scenarios, args.s, args.dt, args.t_end
    )
    args.output.write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8"
    )
    print(f"Wrote {args.output}")
    print(
        "max_abs_identity_residual=",
        result["max_abs_identity_residual"],
        "relative=", result["max_relative_identity_residual"],
    )
