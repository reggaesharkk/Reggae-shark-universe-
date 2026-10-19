#!/usr/bin/env python3
"""Correct the sign interpretation of the v0.28 backward error recurrence.

This rechecks the three archived M14 scalar recurrences in backward time.
It does not regenerate or independently validate the segment residual/strain
enclosures supplied by the archived Arb producer.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/wp19_v0_28"
OUT = BASE / "reverse_time_sign_correction_20261001/reverse_time_sign_correction.json"
SEGMENTS = [
    BASE / "pilot_v2_36818369196/M14_segment_239.json",
    BASE / "pilot_chained_238_36819581437/M14_segment_238.json",
    BASE / "pilot_chained_237_36820757066/M14_segment_237.json",
]
REPORTS = [
    BASE / "pilot_v2_36818369196/verification.json",
    BASE / "pilot_chained_238_36819581437/chain_verification.json",
    BASE / "pilot_chained_237_36820757066/chain_verification.json",
]
AB = BASE / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json"
AB_SOURCE = BASE / "structured_uncertainty_ab_20261001/wp19_v0_28_structured_uncertainty_ab.py"
OLD_AUDIT = BASE / "backward_diffusion_audit_20261001/backward_diffusion_audit.json"
OLD_AUDIT_SOURCE = ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py"
OLD_CORRECTED_CHAIN = BASE / "corrected_chain_20261001/corrected_recurrence_chain.json"
PRODUCER_SOURCES = [
    BASE / "pilot_v2_36818369196/wp19_v0_28_adjoint_segment_arb.py",
    BASE / "pilot_chained_238_36819581437/wp19_v0_28_adjoint_segment_arb.py",
    BASE / "pilot_chained_237_36820757066/wp19_v0_28_adjoint_segment_arb.py",
]
ADJOINT_SOURCE = ROOT / "src/wp19_v0_23_rk4_goal_adjoint.py"
GALERKIN_SOURCE = ROOT / "src/wp16_036_dealiased_trajectory_gate.py"
EXPECTED_SEGMENTS = [
    "d1b41363c88173594ec6c9e90453513cd3c8ed3e32c7037d2e73304d057a8c08",
    "c0bbf407df850b95e1a4b0daa3e1175962ce128e7e5f080d39127bd22b431fa6",
    "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
]
EXPECTED_REPORTS = [
    "41694c84922a28b0b99f9e2936589f8c2f8cb6c49fc2a68a281623a4fb39cb7e",
    "c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c",
    "cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f",
]
EXPECTED_AB = "b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a"
EXPECTED_OLD_AUDIT = "cd223389619c1780516514f7118c87ddc94e8d04c9c7528ce4cfc749948ee540"
EXPECTED_OLD_AUDIT_SOURCE = "55884d2d0c5b5c23100170f1e5bc167e70135eea2066b5be1b23a68e9cbbe2b7"
EXPECTED_OLD_CHAIN = "e8403177d80ac24d6658bc63e9ac6302af70b2bee8cdcdc61f5df11ff71f8e60"
EXPECTED_PRODUCER = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"
EXPECTED_ADJOINT_SOURCE = "0ba7cd0464076271a80864118d930d384d2cce6a1974650f278f8e02a7756e01"
EXPECTED_GALERKIN_SOURCE = "c44824c9562c4e79b11e8838e663ecf77d0992ba5d146b4c5015717018baae14"
EXPECTED_AB_SOURCE = "b746a70ed9b3d00b8e591b962358207e1050c1bfe378467729048cbcca2b8c77"
SUPERSEDED = [
    {
        "path": "notes/WP19_v0_28_BACKWARD_DIFFUSION_RECURRENCE_CORRECTION_2026_10_01.md",
        "sha256": "f5611fd0feb0a7923749fbf353af3eab1910f233bec6cf1ee3e568ff7746d47b",
        "claims_superseded": ["viscosity requires +nu*max(|k|^2) in the backward error exponent",
                              "strain-only radii are invalid for backward error propagation"],
    },
    {
        "path": "results/wp19_v0_28/backward_diffusion_audit_20261001/backward_diffusion_audit.json",
        "sha256": "cd223389619c1780516514f7118c87ddc94e8d04c9c7528ce4cfc749948ee540",
        "claims_superseded": ["reverse-time viscosity is anti-diffusive for the propagated error norm",
                              "the +22.5 exponent contribution is required"],
    },
    {
        "path": "src/wp19_v0_28_backward_diffusion_log_norm_audit.py",
        "sha256": "55884d2d0c5b5c23100170f1e5bc167e70135eea2066b5be1b23a68e9cbbe2b7",
        "claims_superseded": ["the script's reverse-time sign interpretation and verdict"],
    },
    {
        "path": "results/wp19_v0_28/corrected_chain_20261001/corrected_recurrence_chain.json",
        "sha256": "e8403177d80ac24d6658bc63e9ac6302af70b2bee8cdcdc61f5df11ff71f8e60",
        "claims_superseded": ["historical_value_underbounds_corrected_value flag and historical_chain interpretation"],
    },
    {
        "path": "notes/WP19_v0_28_CORRECTED_RECURRENCE_CHAIN_2026_10_01.md",
        "sha256": "3dfe480575200082a62253055f4f7be035497c8661fa5436eb94dfbfab2266dd",
        "claims_superseded": ["the +22.5 recurrence is the governing corrected chain"],
    },
]
FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
H = Decimal(1) / Decimal(80000)
NU = Decimal("0.1")
PRECISION = 90


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recurrence(incoming: Decimal, L: Decimal, residual: Decimal) -> Decimal:
    """Upper recurrence over reverse time tau=T-t; L is the strain bound."""
    if incoming < 0 or L <= 0 or residual < 0:
        raise ValueError("invalid recurrence data")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_CEILING
        amp = (L * H).exp().next_plus()
        return amp * incoming + ((amp - Decimal(1)) / L) * residual


def conservative_recurrence(incoming: Decimal, L: Decimal, residual: Decimal) -> Decimal:
    """The prior +nu*max|k|^2 chain, retained only for comparison."""
    return recurrence(incoming, L + NU * Decimal(225), residual)


def build() -> dict:
    if [sha(p) for p in SEGMENTS] != EXPECTED_SEGMENTS:
        raise ValueError("frozen segment hash mismatch")
    if [sha(p) for p in REPORTS] != EXPECTED_REPORTS:
        raise ValueError("frozen recurrence report hash mismatch")
    if sha(AB) != EXPECTED_AB or sha(OLD_AUDIT) != EXPECTED_OLD_AUDIT:
        raise ValueError("frozen diagnostic artifact mismatch")
    producer_hashes = [sha(p) for p in PRODUCER_SOURCES]
    if (producer_hashes != [EXPECTED_PRODUCER] * 3
            or sha(ADJOINT_SOURCE) != EXPECTED_ADJOINT_SOURCE
            or sha(GALERKIN_SOURCE) != EXPECTED_GALERKIN_SOURCE
            or sha(AB_SOURCE) != EXPECTED_AB_SOURCE):
        raise ValueError("producer, adjoint-system, Galerkin-system, or A/B source hash mismatch")
    if sha(OLD_AUDIT_SOURCE) != EXPECTED_OLD_AUDIT_SOURCE or sha(OLD_CORRECTED_CHAIN) != EXPECTED_OLD_CHAIN:
        raise ValueError("historical audit/source hash mismatch")
    segs = [json.loads(p.read_text()) for p in SEGMENTS]
    reports = [json.loads(p.read_text()) for p in REPORTS]
    for i, (s, report) in enumerate(zip(segs, reports)):
        step = 239 - i
        if (s.get("schema") != "wp19-v0.28-adjoint-segment-arb-v2"
                or s.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY"
                or s.get("M") != 14 or s.get("step") != step
                or s.get("backward_order_index") != i
                or s.get("forward_time_interval_rational") != [f"{step}/80000", f"{step+1}/80000"]
                or s.get("frozen") != FROZEN):
            raise ValueError(f"segment identity/order mismatch at {step}")
        if report.get("segment_sha256") != sha(SEGMENTS[i]):
            raise ValueError(f"recurrence report does not bind segment {step}")
        if s.get("source_sha256") != EXPECTED_PRODUCER:
            raise ValueError(f"segment {step} does not pin the archived segment producer")
    incoming = Decimal(segs[0]["bounds"]["terminal_adjoint_error_upper"])
    conservative_incoming = incoming
    rows = []
    for i, (s, report) in enumerate(zip(segs, reports)):
        b = s["bounds"]
        L = Decimal(b["logarithmic_norm_upper"])
        R = Decimal(b["residual_L2_upper"])
        out = recurrence(incoming, L, R)
        c_out = conservative_recurrence(conservative_incoming, L, R)
        old_in_text = report.get("incoming_adjoint_error_upper", b["terminal_adjoint_error_upper"])
        old_in = Decimal(old_in_text)
        old_report_out_text = report.get("backward_error_after_one_segment_upper",
                                         report.get("backward_error_after_segment_upper"))
        if old_report_out_text is None:
            raise ValueError("archived recurrence report lacks outgoing bound")
        archived_out = Decimal(old_report_out_text)
        if old_in != incoming or out > archived_out or c_out < out:
            raise ValueError(f"archived strain-only chain mismatch or conservative ordering at step {s['step']}")
        rows.append({
            "step": s["step"],
            "forward_time_interval_rational": s["forward_time_interval_rational"],
            "segment_sha256": sha(SEGMENTS[i]),
            "segment_source_sha256": sha(PRODUCER_SOURCES[i]),
            "historical_recurrence_report_sha256": sha(REPORTS[i]),
            "incoming_error_upper": str(incoming),
            "strain_log_norm_upper": str(L),
            "residual_L2_upper": str(R),
            "recomputed_strain_only_outgoing_upper": str(out),
            "archived_outgoing_upper_used_for_next_step": str(archived_out),
            "archived_outgoing_is_outward_of_recomputation": True,
            "optional_plus_diffusion_conservative_outgoing_upper": str(c_out),
        })
        incoming = archived_out
        conservative_incoming = c_out

    ab = json.loads(AB.read_text())
    if (ab.get("schema") != "wp19-v0.28-structured-primal-uncertainty-ab-v1"
            or ab.get("status") != "MATERIAL_TIGHTENING"
            or ab.get("M") != 14 or ab.get("step") != 237
            or ab.get("baseline_segment_sha256") != sha(SEGMENTS[-1])
            or ab.get("frozen") != FROZEN
            or ab.get("incoming_adjoint_error_upper") != reports[-1]["incoming_adjoint_error_upper"]):
        raise ValueError("structured A/B record identity or incoming-radius mismatch")
    s237 = segs[-1]["bounds"]
    ab_fields = {
        "segment_237_strain_upper": s237["logarithmic_norm_upper"],
        "A_B_strain_upper": ab["logarithmic_norm_upper"],
        "segment_237_nominal_residual_upper": s237["nominal_residual_L2_upper"],
        "A_B_nominal_residual_upper": ab["nominal_residual_upper"],
        "segment_237_true_primal_radius_upper": s237["true_primal_radius_upper"],
        "A_B_primal_radius_upper": ab["primal_L2_radius_upper"],
        "residual_upper_used_by_A_B_old_recurrence": s237["residual_L2_upper"],
    }
    if (Decimal(ab_fields["A_B_strain_upper"]) < Decimal(ab_fields["segment_237_strain_upper"])
            or Decimal(ab_fields["A_B_nominal_residual_upper"]) < Decimal(ab_fields["segment_237_nominal_residual_upper"])
            or Decimal(ab_fields["A_B_primal_radius_upper"]) < Decimal(ab_fields["segment_237_true_primal_radius_upper"])):
        raise ValueError("A/B recomputed outward quantities are not upper of segment display")

    ab_incoming = Decimal(ab["incoming_adjoint_error_upper"])
    ab_L = Decimal(ab["logarithmic_norm_upper"])
    ab_R = Decimal(s237["residual_L2_upper"])
    ab_old_recomputed = recurrence(ab_incoming, ab_L, ab_R)
    ab_reported_old = Decimal(ab["outward_recurrence"]["old_recomputed_outgoing_upper"])
    if abs(ab_old_recomputed - ab_reported_old) > Decimal("1e-60"):
        raise ValueError("A/B old recurrence does not replay from its displayed strain and segment residual")
    archived_237 = Decimal(rows[-1]["archived_outgoing_upper_used_for_next_step"])
    ab_L_archived = Decimal(s237["logarithmic_norm_upper"])
    ab_same_R_with_segment_L = recurrence(ab_incoming, ab_L_archived, ab_R)
    ab_delta_from_strain = ab_old_recomputed - ab_same_R_with_segment_L
    ab_delta_total = ab_old_recomputed - archived_237
    if abs(ab_delta_from_strain - ab_delta_total) > Decimal("1e-60"):
        raise ValueError("A/B output gap is not explained by its strain shift under the shared residual input")

    return {
        "schema": "wp19-v0.28-reverse-time-sign-correction-v2",
        "status": "PASS_STRAIN_ONLY_BACKWARD_SCALAR_CHAIN; PRIOR SIGN CLAIM CORRECTED",
        "rights_notice": "Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "protocol": {"cutoff_M": 14, "viscosity": str(NU), "terminal_time": "3/1000",
                     "backward_segment_order": [239, 238, 237], "segment_width": str(H),
                     "adjoint_support_M": 15,
                     "witness_sha256": FROZEN["witness_sha256"], "K36_sha256": FROZEN["K36_sha256"],
                     "C500_portable_semantic_sha256": FROZEN["C500_portable_semantic_sha256"],
                     "no_retuning": True},
        "sign_derivation": {
            "producer_residual_definition": "r = dL/dt - VJP(u,L) - nu*Lambda*L",
            "exact_adjoint_equation": "for the M14-to-M15 segment, d(lambda)/dt = VJP(u,lambda) + nu*Lambda*lambda on the M15 high-system support, as defined by adjoint_rhs in src/wp19_v0_23_rk4_goal_adjoint.py",
            "error_definition": "e = lambda - L",
            "forward_time_error_equation": "de/dt = VJP(u,e) + nu*Lambda*e - r",
            "backward_time_variable": "tau = T - t",
            "backward_time_error_equation": "de/dtau = -VJP(u,e) - nu*Lambda*e + r",
            "energy_identity": "1/2*d||e||_2^2/dtau = -<VJP(u,e),e> - nu*<Lambda e,e> + <r,e>",
            "energy_bound": "D^+||e||_2/dtau <= ||S(u)||_{Linf,op}*||e||_2 + ||r||_2; -nu*<Lambda e,e> is nonpositive and may be dropped",
            "assumptions": [
                "e is real, divergence-free, and Hermitian-symmetric; the Leray projection commutes with Lambda",
                "u_true is exactly divergence-free",
                "the exact adjoint follows the finite M15 Galerkin ODE stated above for the M14-to-M15 segment, with the projected truncated convolution used by the archived system",
                "the same Fourier-coefficient ell2 norm is used for e, residual, primal-radius perturbations, and strain estimates",
                "archived strain L and residual R bound the relevant norms over each entire continuous half-segment",
                "the archived primal radius bounds the primal trajectory error throughout its associated segment",
                "the terminal error upper bound is valid in that same norm",
            ],
            "conclusion": "The archived strain-only scalar recurrence is a valid upper bound in the reverse-propagation ell2 energy estimate, conditional on the listed assumptions and producer-supplied continuous-segment strain/residual bounds. The viscous term is dissipative in this norm and direction. Adding +nu*max|k|^2=22.5 is conservative but unnecessary.",
            "system_source_sha256": EXPECTED_ADJOINT_SOURCE,
            "galerkin_source_sha256": EXPECTED_GALERKIN_SOURCE,
        },
        "segment_rows": rows,
        "segment_237_A_B_rounding_reconciliation": {
            **ab_fields,
            "shared_baseline_segment_sha256": ab["baseline_segment_sha256"],
            "shared_incoming_adjoint_error_upper": ab["incoming_adjoint_error_upper"],
            "A_B_old_recomputed_outgoing_upper": ab["outward_recurrence"]["old_recomputed_outgoing_upper"],
            "archived_outgoing_upper": ab["outward_recurrence"]["old_archived_outgoing_upper"],
            "A_B_old_recurrence_replayed_upper": str(ab_old_recomputed),
            "A_B_minus_archived_outgoing_difference": str(ab_delta_total),
            "outgoing_difference_from_2e_9_strain_shift_using_shared_segment_residual": str(ab_delta_from_strain),
            "nominal_residual_is_used_by_old_recurrence": False,
            "A_B_source_sha256": sha(AB),
            "A_B_code_source_sha256": sha(AB_SOURCE),
            "interpretation": "The A/B source recomputes and rounds its strain to 9 decimal places, then computes the old recurrence using that strain, the same incoming radius, and the segment's residual_L2_upper. The 2e-9 strain increase accounts for the full approximately 1.956341e-3 outgoing difference; the nominal residual field is not an input to this old recurrence. The source explains how the A/B computation is performed, but the packet lacks underlying arrays needed to explain why the re-evaluated strain differs by 2e-9. The A/B structured-residual comparison remains diagnostic-only and is not substituted into the official chain.",
            "structured_residual_comparison_remains_diagnostic_only": True,
        },
        "provenance_sha256": {
            "segments": [sha(p) for p in SEGMENTS], "historical_reports": [sha(p) for p in REPORTS],
            "structured_A_B": sha(AB), "prior_audit": sha(OLD_AUDIT),
            "prior_audit_source": sha(OLD_AUDIT_SOURCE), "prior_conservative_chain": sha(OLD_CORRECTED_CHAIN),
            "producer_sources": producer_hashes, "adjoint_system_source": sha(ADJOINT_SOURCE),
            "Galerkin_system_source": sha(GALERKIN_SOURCE), "structured_A_B_source": sha(AB_SOURCE),
            "correction_source": sha(Path(__file__)),
        },
        "supersedes": SUPERSEDED,
        "scope": {
            "established": "The strain-only Decimal recurrence reproduces the three archived outgoing radii from steps 239, 238, 237 and is a valid backward-time scalar upper recurrence, conditional on supplied bounds.",
            "not_established": ["independent validation of archived continuous-segment strain/residual bounds",
                                "full M14 adjoint path, dual quadrature, nonlinear remainder, normalizer, or signed endpoint transfer",
                                "all-cutoff, blow-up, or continuum Navier-Stokes regularity"],
            "terminology": "The verifier is a separate implementation of the recurrence, not an independent derivation of the PDE estimate.",
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=OUT)
    args = ap.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_suffix(".tmp")
    temp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temp.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
