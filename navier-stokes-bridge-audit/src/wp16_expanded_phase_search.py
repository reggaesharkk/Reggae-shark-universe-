"""Expanded Colab phase-torus search for WP16.

This is a larger falsification search for the WP15 positive-stretching
coefficient. It preserves modal magnitudes, polarizations, reality and
divergence freedom while varying only conjugacy-preserving phases.

It extends the registered WP16 search with:
  * multiple cutoffs,
  * multiple evolved anchor times,
  * global random phase draws,
  * block-coordinate proposals,
  * deterministic seeds.

Finite optimization only. No universal bound is proved.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from adversarial_cutoff_gate import make_initial, SCENARIOS
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent
DT = 0.0005


def canonical_half(k):
    for x in k:
        if x > 0:
            return True
        if x < 0:
            return False
    return False


def base_state(system, amplitude, anchor_time):
    a = amplitude * make_initial(
        system, *SCENARIOS["combined_double_quarter_high"]
    )
    steps = round(anchor_time / DT)
    if not math.isclose(steps * DT, anchor_time, abs_tol=1e-14):
        raise ValueError("anchor time must lie on the registered dt grid")
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


def phase_rotate(base, pairs, phases):
    out = base.copy()
    for (i, j, _), phi in zip(pairs, phases):
        z = np.exp(1j * phi)
        out[i] = z * base[i]
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


def optimize_case(
    N,
    anchor_time,
    amplitude,
    seed,
    global_draws,
    block_rounds,
    block_trials,
    block_size,
    block_step,
    grid,
):
    system = System(N=N, nu=NU)
    base = base_state(system, amplitude, anchor_time)
    pairs = active_pairs(system, base)
    m = len(pairs)
    rng = np.random.default_rng(seed)

    zero_phases = np.zeros(m)
    best_phases = zero_phases.copy()
    baseline = evaluate(system, base, grid=grid)
    best = dict(baseline)

    records = [dict(kind="baseline", trial=0, **baseline)]
    trial_counter = 0

    for _ in range(global_draws):
        trial_counter += 1
        phases = rng.uniform(-math.pi, math.pi, size=m)
        q = evaluate(system, phase_rotate(base, pairs, phases), grid=grid)
        if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
            best = q
            best_phases = phases.copy()
            records.append(dict(
                kind="global_best",
                trial=trial_counter,
                **q
            ))

    step = block_step
    effective_block = max(1, min(block_size, m))
    for round_index in range(block_rounds):
        improved = False
        for _ in range(block_trials):
            trial_counter += 1
            proposal = best_phases.copy()
            idx = rng.choice(m, size=effective_block, replace=False)
            proposal[idx] += rng.normal(scale=step, size=effective_block)
            proposal[idx] = np.angle(np.exp(1j * proposal[idx]))
            q = evaluate(
                system,
                phase_rotate(base, pairs, proposal),
                grid=grid
            )
            if q["C_infinity_stretch"] > best["C_infinity_stretch"]:
                best = q
                best_phases = proposal.copy()
                improved = True
                records.append(dict(
                    kind="block_best",
                    trial=trial_counter,
                    round=round_index,
                    block_size=effective_block,
                    **q
                ))
        step *= 0.6
        if not improved and step < 0.03:
            break

    return dict(
        N=N,
        anchor_time=anchor_time,
        amplitude=amplitude,
        seed=seed,
        active_conjugate_pairs=m,
        baseline=baseline,
        best=best,
        best_phases=best_phases.tolist(),
        improvement_factor=(
            best["C_infinity_stretch"]
            / baseline["C_infinity_stretch"]
            if baseline["C_infinity_stretch"] > 0
            else None
        ),
        search=dict(
            global_draws=global_draws,
            block_rounds=block_rounds,
            block_trials=block_trials,
            block_size=effective_block,
            initial_block_step=block_step,
            grid=grid,
        ),
        records=records,
    )


def run(
    cutoffs=(5, 6, 7),
    anchor_times=(0.0025, 0.0035, 0.0050),
    seeds=(20260925, 20260926),
    amplitude=4.0,
    global_draws=96,
    block_rounds=6,
    block_trials=160,
    block_size=24,
    block_step=0.45,
    grid=24,
):
    if grid <= 3 * max(cutoffs):
        raise ValueError("grid must exceed 3*max(cutoffs)")

    rows = []
    for N in cutoffs:
        for anchor_time in anchor_times:
            for seed in seeds:
                rows.append(optimize_case(
                    N=N,
                    anchor_time=anchor_time,
                    amplitude=amplitude,
                    seed=seed,
                    global_draws=global_draws,
                    block_rounds=block_rounds,
                    block_trials=block_trials,
                    block_size=block_size,
                    block_step=block_step,
                    grid=grid,
                ))

    return dict(
        objective=(
            "C_infinity_stretch=max(N_H2_high,0)/(b_stretch*X2), "
            "b_stretch=<positive omega.S.omega>/G"
        ),
        registered_WP16_benchmark=1.077899704172086,
        family=(
            "conjugacy-preserving phase rotations of evolved "
            "combined_double_quarter_high states"
        ),
        cutoffs=list(cutoffs),
        anchor_times=list(anchor_times),
        seeds=list(seeds),
        amplitude=amplitude,
        warning=(
            "Finite deterministic optimization only. A best value is not a "
            "global maximum; lack of growth does not prove a universal bound."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=HERE / "wp16_expanded_phase_search_results.json"
    )
    p.add_argument("--cutoffs", nargs="+", type=int, default=[5,6,7])
    p.add_argument(
        "--anchor-times",
        nargs="+",
        type=float,
        default=[0.0025,0.0035,0.005]
    )
    p.add_argument("--seeds", nargs="+", type=int, default=[20260925,20260926])
    p.add_argument("--amplitude", type=float, default=4.0)
    p.add_argument("--global-draws", type=int, default=96)
    p.add_argument("--block-rounds", type=int, default=6)
    p.add_argument("--block-trials", type=int, default=160)
    p.add_argument("--block-size", type=int, default=24)
    p.add_argument("--block-step", type=float, default=0.45)
    p.add_argument("--grid", type=int, default=24)
    a = p.parse_args()

    result = run(
        cutoffs=tuple(a.cutoffs),
        anchor_times=tuple(a.anchor_times),
        seeds=tuple(a.seeds),
        amplitude=a.amplitude,
        global_draws=a.global_draws,
        block_rounds=a.block_rounds,
        block_trials=a.block_trials,
        block_size=a.block_size,
        block_step=a.block_step,
        grid=a.grid,
    )
    a.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8"
    )
    print("Wrote", a.output)

    ranked = sorted(
        result["rows"],
        key=lambda x: x["best"]["C_infinity_stretch"],
        reverse=True
    )
    for row in ranked[:20]:
        print(
            "N=", row["N"],
            "t=", row["anchor_time"],
            "seed=", row["seed"],
            "pairs=", row["active_conjugate_pairs"],
            "baseline=", row["baseline"]["C_infinity_stretch"],
            "best=", row["best"]["C_infinity_stretch"],
            "factor=", row["improvement_factor"],
            "chi=", row["best"]["chi_H2_high"],
        )
