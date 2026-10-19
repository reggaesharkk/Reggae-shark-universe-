"""WP16 structured phase-adversary search.

Preserves the exact support, modal magnitudes, polarizations, reality and
divergence-free constraints of the registered combined structured state while
varying only conjugacy-preserving modal phases.

Optimizes the large-amplitude quotient

    C_inf = max(N_H2_high,0)/(b_stretch*X2)

where b_stretch=<positive omega.S.omega>/G.

Finite deterministic search only.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import make_initial, SCENARIOS
from evolve_galerkin import System
from phase_cascade_trajectory import NU
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent


def canonical_half(k):
    for x in k:
        if x > 0:
            return True
        if x < 0:
            return False
    return False


DT = 0.0005

def structured_base(system):
    return make_initial(
        system, *SCENARIOS["combined_double_quarter_high"]
    )


def evolved_anchor(system, amplitude=4.0, time=0.0035):
    steps = round(time / DT)
    if not math.isclose(steps * DT, time, abs_tol=1e-14):
        raise ValueError("anchor time must lie on the registered dt grid")
    a = amplitude * structured_base(system)
    for _ in range(steps):
        a = system.rk4(a, DT)
    return a


def active_pairs(system, a, threshold=1e-8):
    pairs = []
    for i, k in enumerate(system.modes):
        if k == (0, 0, 0) or not canonical_half(k):
            continue
        if np.linalg.norm(a[i]) <= threshold:
            continue
        j = system.index[tuple(-x for x in k)]
        pairs.append((i, j, k))
    return pairs


def phase_rotate(a, pairs, phases):
    out = a.copy()
    for (i, j, _), phi in zip(pairs, phases):
        z = np.exp(1j * phi)
        out[i] = z * a[i]
        out[j] = np.conj(out[i])
    return out


def evaluate(system, a, s=2.0, K=2, grid=24):
    weights = system.square.astype(float) ** s
    X = float(np.sum(weights[:, None] * abs(a) ** 2))
    G = float(np.sum(system.square[:, None] * abs(a) ** 2))

    high = system.square[system.left] > K * K
    out, left, right = (
        x[high] for x in (system.out, system.left, system.right)
    )
    qdot = np.einsum("ij,ij->i", system.qwaves[high], a[left])
    raw = 1j * qdot[:, None] * a[right]
    projected = np.einsum(
        "kij,kj->ki", system.projectors[out], raw
    )
    z = -weights[out] * np.einsum(
        "ij,ij->i", np.conj(a[out]), projected
    )

    N_high = float(np.real(np.sum(z)))
    A_high = float(np.sum(np.abs(z)))
    chi = N_high / A_high if A_high else 0.0

    grad, omega, _, imag = spatial_fields(system, a, grid)
    if imag > 1e-10:
        raise AssertionError(f"imaginary field error {imag}")
    strain = (grad + np.swapaxes(grad, -1, -2)) / 2
    local = np.einsum("...i,...ij,...j->...", omega, strain, omega)
    positive = float(np.mean(np.maximum(local, 0.0)))
    signed = float(np.mean(local))
    grid_G = float(np.mean(np.sum(omega ** 2, axis=-1)))
    if abs(grid_G - G) > 5e-8 * max(1.0, G):
        raise AssertionError("grid/Fourier G mismatch")

    b_stretch = positive / G if G > 0 else 0.0
    denom = b_stretch * X
    C_inf = (
        max(N_high, 0.0) / denom
        if denom > 0
        else (float("inf") if N_high > 0 else 0.0)
    )

    reality = float(np.max(np.linalg.norm(
        a[system.neg] - np.conj(a), axis=1
    )))
    divergence = float(np.max(abs(np.einsum(
        "ij,ij->i", system.waves, a
    ))))
    if reality > 1e-10 or divergence > 1e-10:
        raise AssertionError("state constraints failed")

    return dict(
        X2=X,
        G=G,
        H2_high_transfer=N_high,
        H2_high_envelope=A_high,
        chi_H2_high=chi,
        H1_positive_stretching=positive,
        H1_signed_stretching=signed,
        b_stretch=b_stretch,
        C_infinity_stretch=C_inf,
        reality_error=reality,
        divergence_error=divergence,
    )


def search_one(
    N,
    seed,
    random_draws,
    local_rounds,
    local_trials,
    initial_step,
    grid,
    anchor,
):
    system = System(N=N, nu=NU)
    if anchor == "initial":
        base = structured_base(system)
    elif anchor == "evolved":
        base = evolved_anchor(system)
    else:
        raise ValueError(f"unknown anchor {anchor}")
    pairs = active_pairs(system, base)
    m = len(pairs)
    rng = np.random.default_rng(seed)

    best_phases = np.zeros(m)
    best = evaluate(system, base, grid=grid)
    baseline = dict(best)

    records = [dict(kind="baseline", trial=0, **best)]

    for trial in range(1, random_draws + 1):
        phases = rng.uniform(-math.pi, math.pi, size=m)
        state = phase_rotate(base, pairs, phases)
        q = evaluate(system, state, grid=grid)
        if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
            best = q
            best_phases = phases.copy()
            records.append(dict(kind="random_best", trial=trial, **q))

    step = initial_step
    counter = random_draws
    for round_index in range(local_rounds):
        improved = False
        for _ in range(local_trials):
            counter += 1
            proposal = best_phases.copy()
            j = int(rng.integers(0, m))
            proposal[j] += rng.normal(scale=step)
            proposal[j] = float(np.angle(np.exp(1j * proposal[j])))
            state = phase_rotate(base, pairs, proposal)
            q = evaluate(system, state, grid=grid)
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_phases = proposal
                improved = True
                records.append(dict(
                    kind="local_best",
                    trial=counter,
                    round=round_index,
                    coordinate=j,
                    **q
                ))
        step *= 0.5
        if not improved and step < 1e-3:
            break

    return dict(
        N=N,
        seed=seed,
        anchor=anchor,
        active_conjugate_pairs=m,
        support_vectors=[list(k) for _, _, k in pairs],
        baseline=baseline,
        best=best,
        best_phases=best_phases.tolist(),
        improvement_factor=(
            best["C_infinity_stretch"]
            / baseline["C_infinity_stretch"]
            if baseline["C_infinity_stretch"] > 0 else None
        ),
        records=records,
        search=dict(
            random_draws=random_draws,
            local_rounds=local_rounds,
            local_trials=local_trials,
            initial_step=initial_step,
            grid=grid,
        ),
    )


def run(
    cutoffs=(4, 7),
    seeds=(20260925, 20260926),
    random_draws=0,
    local_rounds=5,
    local_trials=128,
    initial_step=0.35,
    grid=24,
    anchor="evolved",
):
    if grid <= 3 * max(cutoffs):
        raise ValueError("grid must exceed 3*max(cutoffs)")

    rows = []
    for N in cutoffs:
        for seed in seeds:
            rows.append(search_one(
                N, seed, random_draws, local_rounds,
                local_trials, initial_step, grid, anchor
            ))

    return dict(
        objective=(
            "C_infinity_stretch=max(N_H2_high,0)/(b_stretch*X2), "
            "b_stretch=<positive omega.S.omega>/G"
        ),
        family=(
            "phase rotations of every active canonical Fourier pair in the "
            "selected registered structured anchor; modal magnitudes and "
            "polarizations fixed"
        ),
        anchor=anchor,
        evolved_anchor_definition=(
            "4 * combined_double_quarter_high evolved with RK4 dt=0.0005 "
            "to t=0.0035" if anchor == "evolved" else None
        ),
        cutoffs=list(cutoffs),
        seeds=list(seeds),
        warning=(
            "Finite deterministic optimization on one support family only. "
            "Best found value is not a global maximum and bounded values do "
            "not prove a universal constant."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output", type=Path,
        default=HERE / "wp16_structured_phase_adversary_results.json"
    )
    p.add_argument("--random-draws", type=int, default=0)
    p.add_argument("--local-rounds", type=int, default=5)
    p.add_argument("--local-trials", type=int, default=128)
    p.add_argument("--grid", type=int, default=24)
    p.add_argument("--anchor", choices=["initial","evolved"], default="evolved")
    a = p.parse_args()
    result = run(
        random_draws=a.random_draws,
        local_rounds=a.local_rounds,
        local_trials=a.local_trials,
        grid=a.grid,
        anchor=a.anchor,
    )
    a.output.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print("Wrote", a.output)
    for row in sorted(
        result["rows"],
        key=lambda x: x["best"]["C_infinity_stretch"],
        reverse=True
    ):
        print(
            "N=", row["N"],
            "seed=", row["seed"],
            "pairs=", row["active_conjugate_pairs"],
            "baseline=", row["baseline"]["C_infinity_stretch"],
            "best=", row["best"]["C_infinity_stretch"],
            "factor=", row["improvement_factor"],
            "chi=", row["best"]["chi_H2_high"],
            "bstretch=", row["best"]["b_stretch"],
        )
