#!/usr/bin/env python3
"""Check serialized WP19 v0.28 segment bounds without importing project code.

This validates output identities and decimal-level relationships only. It does
not recompute the Arb Bernstein suprema or residual convolution.
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

M = 14
EXPECTED_SOURCE = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"
COMMON_INPUTS = {
    "adjoint_report_sha256": "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8",
    "adjoint_rhs_sha256": "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c",
    "adjoint_values_sha256": "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab",
    "lower_nodes_sha256": "e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0",
    "lower_rhs_sha256": "f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253",
}

def sqrt_upper(x: Fraction, places: int = 70) -> Fraction:
    if x < 0:
        raise ValueError("negative square-root input")
    scale = 10**places
    q = math.isqrt((x.numerator * scale * scale) // x.denominator)
    if q*q*x.denominator < x.numerator*scale*scale:
        q += 1
    return Fraction(q, scale)

def modes_and_weight(cutoff: int) -> tuple[int, int]:
    count = 0
    sum_k_squared = 0
    for kx in range(-cutoff, cutoff + 1):
        for ky in range(-cutoff, cutoff + 1):
            for kz in range(-cutoff, cutoff + 1):
                square = kx*kx + ky*ky + kz*kz
                if square <= cutoff*cutoff:
                    count += 1
                    sum_k_squared += square
    return count, sum_k_squared

def load(path: Path) -> dict:
    return json.loads(path.read_text())

def run(root: Path) -> dict:
    records = [
        (239, root/"results/wp19_v0_28/pilot_v2_36818369196/M14_segment_239.json"),
        (238, root/"results/wp19_v0_28/pilot_chained_238_36819581437/M14_segment_238.json"),
        (237, root/"results/wp19_v0_28/pilot_chained_237_36820757066/M14_segment_237.json"),
    ]
    count, ksq = modes_and_weight(M)
    if (count, ksq) != (11513, 1355442):
        raise AssertionError("independent Fourier-ball enumeration changed")
    output = []
    for step, path in records:
        row = load(path)
        b = row["bounds"]
        if row.get("M") != M or row.get("step") != step:
            raise AssertionError(f"scope mismatch for segment {step}")
        if row.get("source_sha256") != EXPECTED_SOURCE:
            raise AssertionError(f"producer identity mismatch for segment {step}")
        if {k: row["inputs"].get(k) for k in COMMON_INPUTS} != COMMON_INPUTS:
            raise AssertionError(f"common frozen input identity mismatch for segment {step}")
        if row.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
            raise AssertionError(f"claim scope mismatch for segment {step}")

        nominal = Fraction(b["nominal_residual_L2_upper"])
        penalty = Fraction(b["primal_uncertainty_residual_penalty_upper"])
        total = Fraction(b["residual_L2_upper"])
        # Each serialized component receives its own strict decimal slack.
        # The combined upper can therefore sit below the sum of two printed
        # component uppers by less than three grid units.
        additivity_margin = total - nominal - penalty
        residual_grid = Fraction(1, 10**6)
        if not (-3*residual_grid < additivity_margin < 0):
            raise AssertionError(f"residual decimal slack mismatch for segment {step}")

        delta = Fraction(b["true_primal_radius_upper"])
        adjoint_l2 = Fraction(b["adjoint_polynomial_L2_upper"])
        coarse_formula = (sqrt_upper(Fraction(ksq)) +
                          (M+1)*sqrt_upper(Fraction(count))) * delta * adjoint_l2
        coarse_inputs_reconstruct_penalty = penalty >= coarse_formula

        strain_floor = sqrt_upper(Fraction(ksq, 2))*delta
        strain_bound = Fraction(b["logarithmic_norm_upper"])
        if strain_bound < strain_floor:
            raise AssertionError(f"strain uncertainty floor mismatch for segment {step}")

        output.append({
            "step": step,
            "source_sha256_matches": True,
            "frozen_input_hashes_match": True,
            "residual_additivity_margin": str(additivity_margin),
            "residual_decimal_slack_consistent": True,
            "reported_strain_exceeds_uncertainty_only_floor": True,
            "coarse_serialized_inputs_reconstruct_penalty": coarse_inputs_reconstruct_penalty,
            "coarse_formula_minus_reported_penalty": str(coarse_formula-penalty),
        })
    return {
        "schema": "wp19-v0.28-output-bound-check-v1",
        "status": "PASS_OUTPUT_ARITHMETIC_WITH_PRECISION_LIMIT",
        "Fourier_ball_mode_count_including_zero": count,
        "sum_squared_wave_numbers": ksq,
        "segments": output,
        "scope": {
            "checks": [
                "frozen source and common array identities",
                "decimal slack consistency of residual component totals",
                "reported strain bound exceeds the independently recomputed uncertainty-only floor"
            ],
            "limitation": (
                "The printed 15-place primal radius and 6-place adjoint L2 bound "
                "are too coarse to independently reconstruct the reported perturbation penalty."
            ),
            "not_checked": [
                "the Arb Bernstein coefficient suprema",
                "the M14 residual convolution",
                "the complete continuous-segment strain or residual values"
            ]
        }
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = run(args.root)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")

if __name__ == "__main__":
    main()

