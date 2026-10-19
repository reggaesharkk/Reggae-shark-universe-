"""Coefficient-weighted gauge-invariant triad-phase audit.

For a completed phase-only continuation row, reconstruct the registered evolved
base state and decompose every ordered high-advector H2 triad as

    z_opt = z_base * exp(i * (phi_p + phi_q - phi_k)).

The relative phase is invariant under spatial translations
phi_j -> phi_j + j.x0.

The script aggregates the exact finite-Galerkin triad coefficients in chunks to
avoid allocating another full pair-sized complex tensor.

Finite diagnostic only. No asymptotic or regularity claim.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs

HERE = Path(__file__).resolve().parent


def signed_phase_array(system, row, base):
    pairs = active_pairs(system, base)
    support = [list(k) for _, _, k in pairs]
    if support != row["support_vectors"]:
        raise AssertionError("stored support does not match reconstructed active support")
    phases = np.asarray(row["best_phases"], dtype=float)
    if len(phases) != len(pairs):
        raise AssertionError("stored phase count does not match active support")

    psi = np.zeros(len(system.modes), dtype=float)
    for (i, j, _), phi in zip(pairs, phases):
        psi[i] = phi
        psi[j] = -phi
    return psi


def empty_bucket():
    return dict(
        A=0.0,
        N=0.0,
        count=0,
        positive_A=0.0,
        theta_vector_real=0.0,
        theta_vector_imag=0.0,
        alpha_vector_real=0.0,
        alpha_vector_imag=0.0,
        base_vector_real=0.0,
        base_vector_imag=0.0,
    )


def add_bucket(bucket, z0, theta):
    if len(z0) == 0:
        return
    amp = np.abs(z0)
    beta = np.angle(z0)
    alpha = beta + theta
    zopt = z0 * np.exp(1j * theta)

    bucket["A"] += float(np.sum(amp))
    bucket["N"] += float(np.sum(np.real(zopt)))
    bucket["count"] += int(len(z0))
    bucket["positive_A"] += float(np.sum(amp[np.real(zopt) > 0]))

    tv = np.sum(amp * np.exp(1j * theta))
    av = np.sum(amp * np.exp(1j * alpha))
    bv = np.sum(amp * np.exp(1j * beta))

    bucket["theta_vector_real"] += float(np.real(tv))
    bucket["theta_vector_imag"] += float(np.imag(tv))
    bucket["alpha_vector_real"] += float(np.real(av))
    bucket["alpha_vector_imag"] += float(np.imag(av))
    bucket["base_vector_real"] += float(np.real(bv))
    bucket["base_vector_imag"] += float(np.imag(bv))


def finalize_bucket(bucket):
    A = bucket["A"]
    if A <= 0:
        return dict(bucket)

    theta_vec = complex(
        bucket["theta_vector_real"],
        bucket["theta_vector_imag"],
    )
    alpha_vec = complex(
        bucket["alpha_vector_real"],
        bucket["alpha_vector_imag"],
    )
    base_vec = complex(
        bucket["base_vector_real"],
        bucket["base_vector_imag"],
    )

    out = dict(bucket)
    out.update(
        chi=bucket["N"] / A,
        positive_weight_fraction=bucket["positive_A"] / A,
        weighted_theta_resultant=abs(theta_vec) / A,
        weighted_theta_mean_angle=float(np.angle(theta_vec)),
        weighted_alpha_resultant=abs(alpha_vec) / A,
        weighted_alpha_mean_angle=float(np.angle(alpha_vec)),
        base_weighted_resultant=abs(base_vec) / A,
        base_weighted_mean_angle=float(np.angle(base_vec)),
        base_chi=float(np.real(base_vec) / A),
    )
    return out


def audit_row(row, chunk_size=250_000, Kcut=2):
    N = int(row["N"])
    system = System(N=N, nu=NU)
    base = base_state(system, float(row["amplitude"]), float(row["anchor_time"]))
    psi = signed_phase_array(system, row, base)

    weights = system.square.astype(float) ** 2.0
    total = empty_bucket()
    old_only = empty_bucket()
    touches_new = empty_bucket()
    advector_new = empty_bucket()
    shell_buckets = {}

    prevN = N - 1
    pair_count = len(system.out)

    for start in range(0, pair_count, chunk_size):
        stop = min(pair_count, start + chunk_size)
        out = system.out[start:stop]
        left = system.left[start:stop]
        right = system.right[start:stop]

        high = system.square[left] > Kcut * Kcut
        if not np.any(high):
            continue

        out = out[high]
        left = left[high]
        right = right[high]

        qdot = np.einsum(
            "ij,ij->i",
            system.waves[right],
            base[left],
        )
        raw = 1j * qdot[:, None] * base[right]
        projected = np.einsum(
            "kij,kj->ki",
            system.projectors[out],
            raw,
        )
        z0 = -weights[out] * np.einsum(
            "ij,ij->i",
            np.conj(base[out]),
            projected,
        )

        theta = psi[left] + psi[right] - psi[out]
        add_bucket(total, z0, theta)

        new_left = system.square[left] > prevN * prevN
        new_right = system.square[right] > prevN * prevN
        new_out = system.square[out] > prevN * prevN
        any_new = new_left | new_right | new_out

        add_bucket(old_only, z0[~any_new], theta[~any_new])
        add_bucket(touches_new, z0[any_new], theta[any_new])
        add_bucket(advector_new, z0[new_left], theta[new_left])

        shells = np.ceil(
            np.sqrt(system.square[left].astype(float)) - 1e-12
        ).astype(int)
        for shell in np.unique(shells):
            mask = shells == shell
            bucket = shell_buckets.setdefault(int(shell), empty_bucket())
            add_bucket(bucket, z0[mask], theta[mask])

    total = finalize_bucket(total)
    old_only = finalize_bucket(old_only)
    touches_new = finalize_bucket(touches_new)
    advector_new = finalize_bucket(advector_new)
    shells = {
        str(k): finalize_bucket(v)
        for k, v in sorted(shell_buckets.items())
    }

    stored = row["best_search_grid"]
    rel_N_error = abs(total["N"] - stored["H2_high_transfer"]) / max(
        1.0, abs(stored["H2_high_transfer"])
    )
    rel_A_error = abs(total["A"] - stored["H2_high_envelope"]) / max(
        1.0, abs(stored["H2_high_envelope"])
    )

    if rel_N_error > 2e-11 or rel_A_error > 2e-11:
        raise AssertionError(
            f"triad reconstruction mismatch N={rel_N_error} A={rel_A_error}"
        )

    return {
        "N": N,
        "active_conjugate_pairs": row["active_conjugate_pairs"],
        "previous_cutoff": prevN,
        "total": total,
        "old_only_triads": old_only,
        "triads_touching_new_shell": touches_new,
        "new_shell_as_advector": advector_new,
        "advector_shells": shells,
        "reconstruction_relative_error": {
            "H2_high_transfer": rel_N_error,
            "H2_high_envelope": rel_A_error,
        },
    }


def run(path, cutoffs, chunk_size):
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = {int(row["N"]): row for row in payload["rows"]}

    selected = []
    for N in cutoffs:
        if N not in rows:
            raise ValueError(f"N={N} is not present in continuation JSON")
        selected.append(audit_row(rows[N], chunk_size=chunk_size))

    return {
        "status": "executed coefficient-weighted triad-phase audit",
        "source": str(path),
        "cutoffs": list(cutoffs),
        "rows": selected,
        "interpretation_rule": (
            "Weighted triad alignment is an exact finite-Galerkin decomposition "
            "of the stored H2 high-advector transfer. It is not an asymptotic "
            "statement or a regularity theorem."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("continuation_json", type=Path)
    p.add_argument("--cutoffs", nargs="+", type=int, default=[10, 11])
    p.add_argument("--chunk-size", type=int, default=250_000)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/"
            "wp16_weighted_triad_phase_results.json"
        ),
    )
    args = p.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(args.continuation_json, args.cutoffs, args.chunk_size)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
