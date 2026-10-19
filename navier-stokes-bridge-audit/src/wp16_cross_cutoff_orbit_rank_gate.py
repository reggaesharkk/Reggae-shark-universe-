"""Cross-cutoff LRSC-style orbit-response and rank audit for WP16.

Reconstructs the inherited-core phase corrections for:
  N9 -> N10  (using prior N8/N9 escalation JSON)
  N10 -> N11 (using resumed N10/N11 JSON)

Each old-core correction is partitioned by sorted absolute-coordinate orbit:
    orbit(k) = sort(|k1|, |k2|, |k3|)

For every orbit we estimate a small-amplitude directional response:
    dlogN, -dlogPplus, dlogC
at epsilon * registered wrapped phase correction.

We also evaluate the six dominant N11 orbit families as a fixed basis at both
cutoffs and compute singular spectra of the shared-orbit response matrix.

Finite diagnostic only; not an all-cutoff theorem.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict

import numpy as np

from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import base_state, active_pairs, phase_rotate, evaluate


DOMINANT_N11_ORBITS = [
    (0, 3, 6),
    (0, 2, 3),
    (1, 4, 5),
    (0, 1, 3),
    (0, 1, 6),
    (1, 1, 3),
]


def wrapped(x):
    return np.angle(np.exp(1j * x))


def orbit_key(k):
    return tuple(sorted(abs(int(x)) for x in k))


def get_row(payload, N):
    rows = {int(r["N"]): r for r in payload["rows"]}
    if N not in rows:
        raise KeyError(f"missing N={N} row")
    return rows[N]


def reconstruct_step(prev_row, curr_row):
    N = int(curr_row["N"])
    system = System(N=N, nu=NU)
    base = base_state(system, float(curr_row["amplitude"]), float(curr_row["anchor_time"]))
    pairs = active_pairs(system, base)

    support = [list(k) for _, _, k in pairs]
    if support != curr_row["support_vectors"]:
        raise AssertionError(f"N={N}: support mismatch")

    prev_map = {
        tuple(k): float(phi)
        for k, phi in zip(prev_row["support_vectors"], prev_row["best_phases"])
    }

    inherited = np.zeros(len(pairs), dtype=float)
    old = np.zeros(len(pairs), dtype=bool)
    keys = []

    for j, (_, _, k) in enumerate(pairs):
        kt = tuple(int(x) for x in k)
        keys.append(orbit_key(kt))
        if kt in prev_map:
            inherited[j] = prev_map[kt]
            old[j] = True

    final = np.asarray(curr_row["best_phases"], dtype=float)
    delta = wrapped(final - inherited)

    expected = int(curr_row["inherited_pairs"])
    if int(old.sum()) != expected:
        raise AssertionError(
            f"N={N}: inherited count {int(old.sum())} != stored {expected}"
        )

    return system, base, pairs, inherited, final, delta, old, keys


def qeval(system, base, pairs, phases, grid):
    return evaluate(system, phase_rotate(base, pairs, phases), grid=grid)


def log_response(q, q0):
    return {
        "dlogN": float(np.log(q["H2_high_transfer"] / q0["H2_high_transfer"])),
        "minus_dlogPplus": float(-np.log(
            q["H1_positive_stretching"] / q0["H1_positive_stretching"]
        )),
        "dlogC": float(np.log(
            q["C_infinity_stretch"] / q0["C_infinity_stretch"]
        )),
    }


def endpoint_metrics(q, q0):
    return {
        "C": float(q["C_infinity_stretch"]),
        "N_high": float(q["H2_high_transfer"]),
        "P_plus": float(q["H1_positive_stretching"]),
        "C_gain_pct": 100.0 * (
            q["C_infinity_stretch"] / q0["C_infinity_stretch"] - 1.0
        ),
        "N_change_pct": 100.0 * (
            q["H2_high_transfer"] / q0["H2_high_transfer"] - 1.0
        ),
        "P_plus_change_pct": 100.0 * (
            q["H1_positive_stretching"] / q0["H1_positive_stretching"] - 1.0
        ),
    }


def analyze_step(prev_row, curr_row, grid, epsilon):
    N = int(curr_row["N"])
    system, base, pairs, inh, final, delta, old, keys = reconstruct_step(prev_row, curr_row)
    q0 = qeval(system, base, pairs, inh, grid)
    qfull = qeval(system, base, pairs, inh + delta * old, grid)

    groups = defaultdict(list)
    for i, key in enumerate(keys):
        if old[i]:
            groups[key].append(i)

    orbit_rows = []
    for key in sorted(groups):
        inds = groups[key]
        mask = np.zeros(len(pairs), dtype=bool)
        mask[inds] = True

        qeps = qeval(system, base, pairs, inh + epsilon * delta * mask, grid)
        qend = qeval(system, base, pairs, inh + delta * mask, grid)

        dr = log_response(qeps, q0)
        dr = {k: v / epsilon for k, v in dr.items()}

        orbit_rows.append({
            "orbit": list(key),
            "pair_count": len(inds),
            "mean_abs_delta": float(np.mean(np.abs(delta[inds]))),
            "directional_per_unit_lambda": dr,
            "endpoint": endpoint_metrics(qend, q0),
        })

    by_orbit = {tuple(r["orbit"]): r for r in orbit_rows}

    dominant_basis = []
    mask = np.zeros(len(pairs), dtype=bool)
    for rank, key in enumerate(DOMINANT_N11_ORBITS, 1):
        inds = groups.get(key, [])
        if inds:
            mask[inds] = True
        q = qeval(system, base, pairs, inh + delta * mask, grid)
        dominant_basis.append({
            "rank": rank,
            "added_orbit": list(key),
            "orbit_present": bool(inds),
            "added_pair_count": len(inds),
            "cumulative_pair_count": int(mask.sum()),
            **endpoint_metrics(q, q0),
        })

    return {
        "N": N,
        "old_core_pair_count": int(old.sum()),
        "baseline": endpoint_metrics(q0, q0),
        "full_old_core": endpoint_metrics(qfull, q0),
        "orbit_rows": orbit_rows,
        "dominant_six_basis": dominant_basis,
        "_by_orbit": by_orbit,
    }


def svd_summary(matrix):
    if matrix.size == 0:
        return {
            "shape": list(matrix.shape),
            "singular_values": [],
            "energy_fraction": [],
            "cumulative_energy_fraction": [],
            "effective_rank_99pct": 0,
        }

    s = np.linalg.svd(matrix, full_matrices=False, compute_uv=False)
    e = s * s
    frac = e / e.sum() if e.sum() > 0 else np.zeros_like(e)
    cum = np.cumsum(frac)
    rank99 = int(np.searchsorted(cum, 0.99) + 1) if len(cum) else 0
    return {
        "shape": list(matrix.shape),
        "singular_values": [float(x) for x in s],
        "energy_fraction": [float(x) for x in frac],
        "cumulative_energy_fraction": [float(x) for x in cum],
        "effective_rank_99pct": rank99,
    }


def run(prior_path, current_path, grid, epsilon):
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    current = json.loads(current_path.read_text(encoding="utf-8"))

    r9 = get_row(prior, 9)
    r10 = get_row(current, 10)
    r11 = get_row(current, 11)

    step10 = analyze_step(r9, r10, grid, epsilon)
    step11 = analyze_step(r10, r11, grid, epsilon)

    by10 = step10.pop("_by_orbit")
    by11 = step11.pop("_by_orbit")

    shared = sorted(set(by10) & set(by11))
    rows = []
    matrix = []

    for key in shared:
        a = by10[key]["directional_per_unit_lambda"]
        b = by11[key]["directional_per_unit_lambda"]
        vec = [
            a["dlogN"],
            a["minus_dlogPplus"],
            a["dlogC"],
            b["dlogN"],
            b["minus_dlogPplus"],
            b["dlogC"],
        ]
        matrix.append(vec)

        rows.append({
            "orbit": list(key),
            "N10_pair_count": by10[key]["pair_count"],
            "N11_pair_count": by11[key]["pair_count"],
            "N10_response": a,
            "N11_response": b,
            "sign_consistency": {
                "dlogN": bool(np.sign(a["dlogN"]) == np.sign(b["dlogN"])),
                "minus_dlogPplus": bool(
                    np.sign(a["minus_dlogPplus"]) == np.sign(b["minus_dlogPplus"])
                ),
                "dlogC": bool(np.sign(a["dlogC"]) == np.sign(b["dlogC"])),
            },
        })

    M = np.asarray(matrix, dtype=float)

    # Raw response spectrum.
    raw_svd = svd_summary(M)

    # Column-standardized response spectrum; preserves orbit rows while removing
    # arbitrary scale differences between the six response coordinates.
    if M.size:
        scale = np.std(M, axis=0, ddof=0)
        scale[scale == 0] = 1.0
        Mz = M / scale
    else:
        Mz = M
    standardized_svd = svd_summary(Mz)

    dom = []
    for key in DOMINANT_N11_ORBITS:
        a = by10.get(key)
        b = by11.get(key)
        dom.append({
            "orbit": list(key),
            "present_N10": a is not None,
            "present_N11": b is not None,
            "N10_pair_count": a["pair_count"] if a else 0,
            "N11_pair_count": b["pair_count"] if b else 0,
            "N10_directional": a["directional_per_unit_lambda"] if a else None,
            "N11_directional": b["directional_per_unit_lambda"] if b else None,
            "dlogC_sign_consistent": (
                bool(np.sign(a["directional_per_unit_lambda"]["dlogC"]) ==
                     np.sign(b["directional_per_unit_lambda"]["dlogC"]))
                if a and b else None
            ),
        })

    # Rank shared orbits by geometric mean of positive dlogC magnitudes across
    # the two cutoffs; negative values score zero.
    persistence_rank = []
    for row in rows:
        x = max(0.0, row["N10_response"]["dlogC"])
        y = max(0.0, row["N11_response"]["dlogC"])
        score = float(np.sqrt(x * y))
        persistence_rank.append({
            "orbit": row["orbit"],
            "persistent_positive_dlogC_score": score,
            "N10_dlogC": row["N10_response"]["dlogC"],
            "N11_dlogC": row["N11_response"]["dlogC"],
        })
    persistence_rank.sort(
        key=lambda r: r["persistent_positive_dlogC_score"],
        reverse=True,
    )

    return {
        "status": "executed cross-cutoff orbit-response and rank audit",
        "prior_source": str(prior_path),
        "current_source": str(current_path),
        "grid": grid,
        "epsilon": epsilon,
        "steps": {
            "N10_from_N9": step10,
            "N11_from_N10": step11,
        },
        "dominant_N11_orbit_recurrence": dom,
        "shared_orbit_count": len(shared),
        "shared_orbit_responses": rows,
        "persistent_positive_dlogC_ranking": persistence_rank,
        "raw_response_svd": raw_svd,
        "column_standardized_response_svd": standardized_svd,
        "interpretation_rule": (
            "This is a finite cross-cutoff response/rank diagnostic. "
            "Persistence or low numerical rank across N10 and N11 does not "
            "establish an all-N orbit law or Navier-Stokes regularity result."
        ),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prior-json", type=Path, required=True)
    p.add_argument("--current-json", type=Path, required=True)
    p.add_argument("--grid", type=int, default=48)
    p.add_argument("--epsilon", type=float, default=0.1)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "/content/drive/MyDrive/WP16_CUTOFF_ESCALATION/"
            "wp16_cross_cutoff_orbit_rank_results.json"
        ),
    )
    args = p.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        args.prior_json,
        args.current_json,
        args.grid,
        args.epsilon,
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 84)
    print("CROSS-CUTOFF ORBIT/RANK AUDIT")
    print("=" * 84)
    print("shared orbits:", result["shared_orbit_count"])

    print("\nDOMINANT N11 ORBITS")
    for r in result["dominant_N11_orbit_recurrence"]:
        print(
            r["orbit"],
            "N10=", r["present_N10"],
            "N11=", r["present_N11"],
            "sign=", r["dlogC_sign_consistent"],
            "N10 dlogC=",
            None if r["N10_directional"] is None else r["N10_directional"]["dlogC"],
            "N11 dlogC=",
            None if r["N11_directional"] is None else r["N11_directional"]["dlogC"],
        )

    print("\nTOP PERSISTENT POSITIVE dlogC ORBITS")
    for r in result["persistent_positive_dlogC_ranking"][:15]:
        print(r)

    print("\nRAW SVD")
    print(json.dumps(result["raw_response_svd"], indent=2))

    print("\nCOLUMN-STANDARDIZED SVD")
    print(json.dumps(result["column_standardized_response_svd"], indent=2))

    print("\nSAVED:", args.output)
