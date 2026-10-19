"""Post-hoc sparse N11 turnover witness derived from the N17 inherited state.

This is a finite Fourier-Galerkin numerical experiment, not an interval
certificate, a prospective N17 test, or a claim about the continuum PDE.
The exported coefficient table lets verification run without the large N17
continuation files. Coefficients are finite decimal input data.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_N17_mechanism_gate import complex_groups, frozen_keys
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

N = 11
PAIR_COUNT = 112
DT = 0.0001
STEPS = 30
EXPECTED_N16 = "53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca"
EXPECTED_N17 = "755a36f966b64c8c44cd468c6f2e8212a7ed64eebeaf8aa795ee2c3197c4c3ec"
EXPECTED_KEYS = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"


def read_checked(path, expected):
    data = path.read_bytes()
    found = hashlib.sha256(data).hexdigest()
    if found != expected:
        raise ValueError(f"SHA-256 mismatch for {path}: {found}")
    return json.loads(data)


def representative(k):
    return tuple(k) > tuple(-v for v in k)


def build_coefficients(n16, n17):
    hold.System = DealiasedSystem
    big, states = hold.reconstruct(hold.get_row(n16, 16), hold.get_row(n17, 17))
    amplitudes = dict(zip(big.modes, states["inherited"]))
    small = DealiasedSystem(N)
    base = np.asarray([amplitudes[k] for k in small.modes])
    choices = [i for i, k in enumerate(small.modes)
               if representative(k) and np.linalg.norm(base[i]) > 1e-13]
    # Stable tie breaker is the canonical mode enumeration index.
    choices.sort(key=lambda i: (-float(np.linalg.norm(base[i])), i))
    anchor = {small.index[k] if representative(k) else int(small.neg[small.index[k]])
              for k in (hold.P, hold.Q, hold.K)}
    selected = sorted(set(choices[:PAIR_COUNT]) | anchor)
    if len(selected) != PAIR_COUNT:
        raise AssertionError("anchor changes selected pair count")
    rows = []
    for i in selected:
        rows.append({"wavevector": list(small.modes[i]),
                     "coefficient": [[float(z.real), float(z.imag)] for z in base[i]]})
    return rows


def restore(rows):
    system = DealiasedSystem(N)
    a = np.zeros((len(system.modes), 3), complex)
    for row in rows:
        k = tuple(row["wavevector"])
        if not representative(k):
            raise ValueError(f"not a positive representative: {k}")
        i = system.index[k]
        a[i] = np.array([complex(*z) for z in row["coefficient"]])
        a[system.neg[i]] = np.conj(a[i])
    if len(rows) != PAIR_COUNT:
        raise ValueError("wrong number of selected conjugate pairs")
    return system, a


def margin(system, a, keys):
    groups, z = complex_groups(system, a)
    mass = {key: abs(float(np.imag(w / z))) for key, w in groups.items()}
    inside = sum(mass.get(key, 0.0) for key in keys)
    outside = sum(value for key, value in mass.items() if key not in keys)
    return {"I": inside, "O": outside, "F": inside - 9 * outside,
            "fraction": inside / (inside + outside), "normalizer_abs": abs(z)}


def direct_output_nonlinear(system, a):
    ki = system.index[hold.K]
    out = np.zeros(3, complex)
    for li, ri in zip(system.left, system.right):
        out += 1j * np.dot(system.waves[ri], a[li]) * a[ri]
    return system.projectors[ki] @ out


def run(system, initial, keys, dt):
    count = round(STEPS * DT / dt)
    if abs(count * dt - STEPS * DT) > 1e-15:
        raise ValueError("dt does not divide endpoint")
    a = initial.copy()
    samples = {"0": margin(system, a, keys)}
    energy = [float(np.sum(abs(a) ** 2))]
    max_reality = max_divergence = max_skew = max_k_discrepancy = 0.0
    for step in range(count + 1):
        nonlinear = system.nonlinear(a)
        max_skew = max(max_skew, abs(float(np.real(np.vdot(a, nonlinear)))))
        max_k_discrepancy = max(max_k_discrepancy,
             float(np.max(abs(nonlinear[system.index[hold.K]] - direct_output_nonlinear(system, a)))))
        max_reality = max(max_reality, float(np.max(abs(a[system.neg] - np.conj(a)))))
        max_divergence = max(max_divergence,
             float(np.max(abs(np.einsum("ij,ij->i", system.waves, a)))))
        if step == count:
            break
        a = system.rk4(a, dt)
        energy.append(float(np.sum(abs(a) ** 2)))
        if (step + 1) * dt in (0.001, 0.002, 0.003):
            samples[str(round((step + 1) * dt, 4))] = margin(system, a, keys)
    samples["0.003"] = margin(system, a, keys)
    return {"dt": dt, "samples": samples,
            "energy_start": energy[0], "energy_end": energy[-1],
            "max_energy_increase": max((y-x for x, y in zip(energy, energy[1:])), default=0.0),
            "max_reality_error": max_reality, "max_divergence_error": max_divergence,
            "max_energy_skew_error": max_skew, "max_direct_K_convolution_error": max_k_discrepancy}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n16", type=Path)
    parser.add_argument("--n17", type=Path)
    parser.add_argument("--keys", type=Path, required=True)
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    keys = frozen_keys(read_checked(args.keys, EXPECTED_KEYS))
    if args.n16 or args.n17:
        if not args.n16 or not args.n17:
            parser.error("provide both continuations for construction")
        rows = build_coefficients(read_checked(args.n16, EXPECTED_N16),
                                  read_checked(args.n17, EXPECTED_N17))
        args.witness.parent.mkdir(parents=True, exist_ok=True)
        args.witness.write_text(json.dumps({"status": "post-hoc N17-derived N11 witness",
            "N": N, "selection": "top 112 N11 inherited positive conjugate pairs by vector norm; anchors forced",
            "N16_sha256": EXPECTED_N16, "N17_sha256": EXPECTED_N17,
            "keys_sha256": EXPECTED_KEYS, "pairs": rows}, indent=2) + "\n")
    raw = args.witness.read_bytes()
    witness = json.loads(raw)
    system, initial = restore(witness["pairs"])
    coarse = run(system, initial, keys, DT)
    fine = run(system, initial, keys, DT / 2)
    quarter = run(system, initial, keys, DT / 4)
    discrepancy = abs(coarse["samples"]["0.003"]["F"] - fine["samples"]["0.003"]["F"])
    finer_discrepancy = abs(fine["samples"]["0.003"]["F"] - quarter["samples"]["0.003"]["F"])
    output = {"status": "post-hoc finite N11 sparse turnover diagnostic; not a certificate",
              "witness_sha256": hashlib.sha256(raw).hexdigest(), "N": N,
              "pair_count": len(witness["pairs"]), "K36_keys_sha256": EXPECTED_KEYS,
              "coarse": coarse, "half_step": fine, "quarter_step": quarter,
              "endpoint_F_discrepancy": discrepancy,
              "endpoint_F_half_vs_quarter_discrepancy": finer_discrepancy,
              "turnover_observed": coarse["samples"]["0"]["F"] > 0 and
                  coarse["samples"]["0.003"]["F"] < 0 and
                  fine["samples"]["0.003"]["F"] < 0 and
                  quarter["samples"]["0.003"]["F"] < 0,
              "claim_boundary": "selected after N17 inspection; float64 RK4; no interval enclosure, no PDE tail bound"}
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(output, indent=2) + "\n")
    print("turnover_observed", output["turnover_observed"],
          "F0", coarse["samples"]["0"]["F"],
          "F003", coarse["samples"]["0.003"]["F"],
          "half_step_difference", discrepancy,
          "quarter_step_difference", finer_discrepancy)
    if not output["turnover_observed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
