"""WP17 sparse multiscale ladder adversary.

Searches relative amplitudes and phases of scaled copies of the exact sparse
triad to maximize

    C_inf = max(N_H2_high,0)/(b_stretch*X2)

with b_stretch=<positive omega.S.omega>/G.

The H2 transfer is evaluated by exact sparse convolution on occupied outputs.
The positive stretching factor is checked on multiple physical grids.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from galerkin import leray
from helicity_phase_gate import POLARIZATIONS
from validate_sparse_triad import P, Q, R

HERE = Path(__file__).resolve().parent


def neg(k):
    return tuple(-x for x in k)


def make_ladder(log_amps, phases):
    L = len(phases)
    amps = [1.0] + [math.exp(x) for x in log_amps]
    u = {}
    for m in range(1, L + 1):
        A = amps[m - 1]
        theta = phases[m - 1]
        for k, v in POLARIZATIONS.items():
            km = tuple(m * x for x in k)
            phase = np.exp(1j * theta) if k == R else 1.0
            a = A * v.astype(complex) * phase
            u[km] = a
            u[neg(km)] = np.conj(a)
    return u, amps


def sparse_high_transfer(u, K=2, s=2.0):
    total = 0j
    envelope = 0.0
    for k, ak in u.items():
        k2 = sum(x*x for x in k)
        weight = k2 ** s
        for p, ap in u.items():
            if sum(x*x for x in p) <= K*K:
                continue
            q = tuple(k[d] - p[d] for d in range(3))
            aq = u.get(q)
            if aq is None:
                continue
            raw = 1j * np.dot(q, ap) * aq
            z = -weight * np.vdot(ak, leray(k) @ raw)
            total += z
            envelope += abs(z)
    return float(np.real(total)), float(envelope)


def spatial_positive_stretching(u, grid):
    shape = (grid, grid, grid, 3)
    grad = np.empty((grid, grid, grid, 3, 3), float)

    for direction in range(3):
        coeff = np.zeros(shape, complex)
        for k, a in u.items():
            idx = tuple(np.asarray(k) % grid)
            coeff[idx] = 1j * k[direction] * a * grid**3
        field = np.fft.ifftn(coeff, axes=(0, 1, 2))
        if np.max(np.abs(field.imag)) > 2e-10:
            raise AssertionError("imaginary reconstruction error")
        grad[..., :, direction] = field.real

    omega = np.stack(
        (
            grad[..., 2, 1] - grad[..., 1, 2],
            grad[..., 0, 2] - grad[..., 2, 0],
            grad[..., 1, 0] - grad[..., 0, 1],
        ),
        axis=-1,
    )
    strain = (grad + np.swapaxes(grad, -1, -2)) / 2
    local = np.einsum("...i,...ij,...j->...", omega, strain, omega)
    return float(np.mean(np.maximum(local, 0.0))), float(np.mean(local))


def evaluate(log_amps, phases, grid=32, K=2):
    u, amps = make_ladder(log_amps, phases)

    G = sum(
        sum(x*x for x in k) * float(np.vdot(a, a).real)
        for k, a in u.items()
    )
    X2 = sum(
        (sum(x*x for x in k) ** 2) * float(np.vdot(a, a).real)
        for k, a in u.items()
    )
    N2, envelope = sparse_high_transfer(u, K=K, s=2.0)
    positive, signed = spatial_positive_stretching(u, grid)

    b_stretch = positive / G if G > 0 else 0.0
    denominator = b_stretch * X2
    C = (
        max(N2, 0.0) / denominator
        if denominator > 0
        else (float("inf") if N2 > 0 else 0.0)
    )

    divergence = max(abs(np.dot(k, a)) for k, a in u.items())
    reality = max(
        np.linalg.norm(u[neg(k)] - np.conj(a))
        for k, a in u.items()
    )
    if divergence > 1e-10 or reality > 1e-10:
        raise AssertionError("sparse state constraints failed")

    return dict(
        amplitudes=amps,
        phases=list(map(float, phases)),
        G=G,
        X2=X2,
        H2_high_transfer=N2,
        H2_high_envelope=envelope,
        chi_H2_high=(N2/envelope if envelope else 0.0),
        H1_positive_stretching=positive,
        H1_signed_stretching=signed,
        b_stretch=b_stretch,
        C_infinity_stretch=C,
        grid=grid,
    )


def search_L(
    L,
    seed,
    random_draws,
    local_rounds,
    local_trials,
    log_amp_bound,
    grid,
):
    rng = np.random.default_rng(seed)

    # Include the coherent equal-amplitude quarter-phase state.
    best_logs = np.zeros(L - 1)
    best_phases = np.full(L, math.pi/2)
    best = evaluate(best_logs, best_phases, grid=grid)

    for _ in range(random_draws):
        logs = rng.uniform(-log_amp_bound, log_amp_bound, size=L-1)
        phases = rng.uniform(-math.pi, math.pi, size=L)
        q = evaluate(logs, phases, grid=grid)
        if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
            best = q
            best_logs = logs.copy()
            best_phases = phases.copy()

    phase_step = 0.5
    amp_step = 0.5
    for _round in range(local_rounds):
        for _ in range(local_trials):
            logs = best_logs.copy()
            phases = best_phases.copy()
            if L > 1 and rng.random() < 0.45:
                j = int(rng.integers(0, L-1))
                logs[j] = np.clip(
                    logs[j] + rng.normal(scale=amp_step),
                    -log_amp_bound,
                    log_amp_bound,
                )
            else:
                j = int(rng.integers(0, L))
                phases[j] += rng.normal(scale=phase_step)
                phases[j] = float(np.angle(np.exp(1j*phases[j])))

            q = evaluate(logs, phases, grid=grid)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_logs = logs
                best_phases = phases

        phase_step *= 0.5
        amp_step *= 0.5

    refine = {}
    for g in (48, 64, 96):
        refine[str(g)] = evaluate(best_logs, best_phases, grid=g)

    return dict(
        L=L,
        seed=seed,
        search_grid=grid,
        random_draws=random_draws,
        local_rounds=local_rounds,
        local_trials=local_trials,
        log_amp_bound=log_amp_bound,
        best_search_grid=best,
        refined=refine,
    )


def run(
    lengths=(2,3,4,5,6),
    seed=20260925,
    random_draws=384,
    local_rounds=4,
    local_trials=96,
    log_amp_bound=3.0,
    grid=32,
):
    if grid <= 3 * math.sqrt(3) * max(lengths):
        raise ValueError("search grid too small for registered anti-alias rule")

    rows = [
        search_L(
            L, seed, random_draws, local_rounds, local_trials,
            log_amp_bound, grid
        )
        for L in lengths
    ]

    return dict(
        objective=(
            "C_infinity_stretch=max(N_H2_high,0)/(b_stretch*X2)"
        ),
        family=(
            "scaled copies m=1..L of the registered sparse triad; "
            "A1=1, relative amplitudes and R phases searched"
        ),
        lengths=list(lengths),
        seed=seed,
        warning=(
            "Finite sparse-family optimization only. Refined grids test the "
            "positive-part quadrature but do not establish a universal bound."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output", type=Path,
        default=HERE / "wp17_sparse_multiscale_ladder_results.json"
    )
    p.add_argument("--random-draws", type=int, default=384)
    p.add_argument("--local-rounds", type=int, default=4)
    p.add_argument("--local-trials", type=int, default=96)
    p.add_argument("--log-amp-bound", type=float, default=3.0)
    p.add_argument("--grid", type=int, default=32)
    a = p.parse_args()

    result = run(
        random_draws=a.random_draws,
        local_rounds=a.local_rounds,
        local_trials=a.local_trials,
        log_amp_bound=a.log_amp_bound,
        grid=a.grid,
    )
    a.output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print("Wrote", a.output)
    for row in sorted(
        result["rows"],
        key=lambda x: x["refined"]["96"]["C_infinity_stretch"],
        reverse=True,
    ):
        b = row["best_search_grid"]
        r96 = row["refined"]["96"]
        print(
            "L=", row["L"],
            "searchC=", b["C_infinity_stretch"],
            "C96=", r96["C_infinity_stretch"],
            "amps=", np.round(b["amplitudes"], 5),
            "phases=", np.round(b["phases"], 5),
            "signedH1=", r96["H1_signed_stretching"],
            "N2high=", r96["H2_high_transfer"],
        )
