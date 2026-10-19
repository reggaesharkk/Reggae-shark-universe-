#!/usr/bin/env python3
"""Recompute the corrected outward M14 adjoint-error recurrence for steps 239..237.

This consumes only the three frozen continuous-segment records and their old
recurrence reports. It does not regenerate trajectories, Arb polynomials, or
segment residual/strain bounds. Those imported whole-segment bounds remain
producer-certified inputs; this program corrects and chains the scalar
backward-error recurrence by including reverse diffusion.
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
OUT = BASE / "corrected_chain_20261001/corrected_recurrence_chain.json"
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
OLD_AUDIT = BASE / "backward_diffusion_audit_20261001/backward_diffusion_audit.json"
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
EXPECTED_FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
NU = Decimal("0.1")
N_HIGH = 15
H = Decimal(1) / Decimal(80000)
PRECISION = 90


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def max_squared_ball_radius(n: int) -> int:
    support = [i*i + j*j + k*k
               for i in range(-n, n + 1)
               for j in range(-n, n + 1)
               for k in range(-n, n + 1)
               if i*i + j*j + k*k <= n*n]
    if not support or max(support) != n*n:
        raise ValueError("unexpected Fourier-ball support")
    return max(support)


def upper_step(incoming: Decimal, log_norm: Decimal, residual: Decimal) -> Decimal:
    """Outward scalar Gronwall step, with one extra ulp after Decimal exp."""
    if incoming < 0 or residual < 0 or log_norm <= 0:
        raise ValueError("nonpositive/invalid recurrence input")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_CEILING
        amp = (log_norm * H).exp().next_plus()
        integral = (amp - Decimal(1)) / log_norm
        return amp * incoming + integral * residual


def validate_inputs() -> tuple[list[dict], list[dict], dict, int, Decimal]:
    if [sha(p) for p in SEGMENTS] != EXPECTED_SEGMENTS:
        raise ValueError("frozen segment hash mismatch")
    if [sha(p) for p in REPORTS] != EXPECTED_REPORTS:
        raise ValueError("frozen historical recurrence-report hash mismatch")
    if sha(AB) != EXPECTED_AB or sha(OLD_AUDIT) != EXPECTED_OLD_AUDIT:
        raise ValueError("frozen A/B or prior correction-audit hash mismatch")
    old_audit = json.loads(OLD_AUDIT.read_text())
    audit_source = ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py"
    if sha(audit_source) != EXPECTED_OLD_AUDIT_SOURCE:
        raise ValueError("prior correction-audit source hash mismatch")
    if old_audit.get("schema") != "wp19-v0.28-backward-diffusion-log-norm-audit-v1":
        raise ValueError("unexpected prior audit schema")

    segs = [json.loads(p.read_text()) for p in SEGMENTS]
    reports = [json.loads(p.read_text()) for p in REPORTS]
    for idx, (seg, report) in enumerate(zip(segs, reports)):
        expected_step = 239 - idx
        if (seg.get("schema") != "wp19-v0.28-adjoint-segment-arb-v2"
                or seg.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY"
                or seg.get("M") != 14 or seg.get("step") != expected_step
                or seg.get("backward_order_index") != idx
                or seg.get("forward_time_interval_rational") !=
                [f"{expected_step}/80000", f"{expected_step + 1}/80000"]
                or seg.get("precision_bits") != 192
                or seg.get("frozen") != EXPECTED_FROZEN):
            raise ValueError(f"segment {expected_step} identity/protocol mismatch")
        b = seg["bounds"]
        for key in ("logarithmic_norm_upper", "residual_L2_upper", "terminal_adjoint_error_upper",
                    "nominal_residual_L2_upper", "primal_uncertainty_residual_penalty_upper"):
            value = Decimal(b[key])
            if not value.is_finite() or value < 0:
                raise ValueError(f"invalid segment {expected_step} bound {key}")
        # The source reports six decimal places; allow at most 2 micro-units
        # for the independently rounded component sum.
        with localcontext() as ctx:
            ctx.prec = 80
            ctx.rounding = ROUND_CEILING
            components = Decimal(b["nominal_residual_L2_upper"]) + Decimal(b["primal_uncertainty_residual_penalty_upper"])
            if Decimal(b["residual_L2_upper"]) + Decimal("0.000002") < components:
                raise ValueError(f"segment {expected_step} residual underbounds its components")
        if report.get("segment_sha256") != sha(SEGMENTS[idx]):
            raise ValueError(f"historical recurrence report is not tied to segment {expected_step}")

    ab = json.loads(AB.read_text())
    if (ab.get("schema") != "wp19-v0.28-structured-primal-uncertainty-ab-v1"
            or ab.get("step") != 237 or ab.get("status") != "MATERIAL_TIGHTENING"):
        raise ValueError("structured A/B diagnostic identity mismatch")
    k2 = max_squared_ball_radius(N_HIGH)
    if k2 != 225:
        raise ValueError("unexpected maximum squared wave number")
    return segs, reports, ab, k2, NU * k2


def build() -> dict:
    segs, reports, ab, k2, reverse_diffusion = validate_inputs()
    incoming = Decimal(segs[0]["bounds"]["terminal_adjoint_error_upper"])
    rows = []
    for i, (seg, report) in enumerate(zip(segs, reports)):
        b = seg["bounds"]
        strain = Decimal(b["logarithmic_norm_upper"])
        total_log_norm = strain + reverse_diffusion
        residual = Decimal(b["residual_L2_upper"])
        outgoing = upper_step(incoming, total_log_norm, residual)
        # Independently show why the archived outgoing value is historical:
        # it reproduces the strain-only recurrence but falls below this result.
        old_in_text = report.get("incoming_adjoint_error_upper")
        if old_in_text is None:
            old_in_text = b["terminal_adjoint_error_upper"]
        old_in = Decimal(old_in_text)
        old_amp = upper_step(old_in, strain, residual)
        old_out_text = report.get("backward_error_after_one_segment_upper",
                                  report.get("backward_error_after_segment_upper"))
        if old_out_text is None:
            raise ValueError("historical recurrence report lacks endpoint")
        old_out = Decimal(old_out_text)
        if old_amp > old_out or old_out >= outgoing:
            raise ValueError(f"segment {seg['step']} does not show the expected superseded chain")
        rows.append({
            "step": seg["step"],
            "forward_time_interval_rational": seg["forward_time_interval_rational"],
            "segment_sha256": sha(SEGMENTS[i]),
            "historical_recurrence_report_sha256": sha(REPORTS[i]),
            "incoming_error_upper_corrected_chain": str(incoming),
            "strain_log_norm_upper_imported": str(strain),
            "reverse_diffusion_log_norm_upper": str(reverse_diffusion),
            "total_log_norm_upper_used": str(total_log_norm),
            "residual_L2_upper_imported": str(residual),
            "outgoing_error_upper_corrected_chain": str(outgoing),
            "historical_strain_only_recurrence_recomputed": str(old_amp),
            "historical_archived_outgoing_error_upper": str(old_out),
            "historical_value_underbounds_corrected_value": True,
        })
        incoming = outgoing

    # Preserve the previously recorded structured-residual comparison as a
    # sensitivity diagnostic only. It is not substituted into the official
    # three-step chain and does not change the frozen base residuals.
    last = segs[-1]["bounds"]
    log_norm_237 = Decimal(last["logarithmic_norm_upper"]) + reverse_diffusion
    structured_residual = Decimal(ab["nominal_residual_upper"]) + Decimal(ab["structured_fourier_young_penalty_upper"])
    base_in = Decimal(rows[-1]["incoming_error_upper_corrected_chain"])
    base_out = Decimal(rows[-1]["outgoing_error_upper_corrected_chain"])
    structured_out = upper_step(base_in, log_norm_237, structured_residual)

    generator = Path(__file__)
    verifier = ROOT / "src/wp19_v0_28_verify_corrected_recurrence_chain.py"
    return {
        "schema": "wp19-v0.28-corrected-adjoint-error-chain-v1",
        "status": "PASS_LIMITED_CORRECTED_SCALAR_RECURRENCE_CHAIN",
        "rights_notice": "Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "protocol": {
            "version": "v0.28-reverse-diffusion-corrected-decimal-g1",
            "cutoff_M": 14,
            "viscosity": str(NU),
            "terminal_time": "3/1000",
            "frozen_segments_in_backward_order": [239, 238, 237],
            "step_width": str(H),
            "decimal_precision_digits": PRECISION,
            "rounding": "ROUND_CEILING; Decimal.exp upper-rounded by next_plus",
            "fixed_witness_sha256": EXPECTED_FROZEN["witness_sha256"],
            "K36_sha256": EXPECTED_FROZEN["K36_sha256"],
            "C500_portable_semantic_sha256": EXPECTED_FROZEN["C500_portable_semantic_sha256"],
            "no_retuning": True,
        },
        "recurrence": "e_out <= exp(L*h)*e_in + ((exp(L*h)-1)/L)*R; L = imported strain_log_norm_upper + nu*max_{|k|<=15}|k|^2",
        "spectral_support_check": {"support": "integer Fourier ball |k|<=15", "max_k_squared": k2,
                                   "reverse_diffusion_growth_bound": str(reverse_diffusion)},
        "provenance_sha256": {
            "segments": [sha(p) for p in SEGMENTS],
            "historical_recurrence_reports": [sha(p) for p in REPORTS],
            "structured_A_B_diagnostic": sha(AB),
            "prior_correction_audit": sha(OLD_AUDIT),
            "prior_correction_audit_source": sha(ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py"),
            "generator_source": sha(generator),
            "independent_verifier_source": sha(verifier),
        },
        "segments": rows,
        "segment_237_structured_residual_sensitivity_only": {
            "structured_A_B_source_sha256": sha(AB),
            "penalty_ratio": ab["new_over_old_penalty_upper"],
            "base_residual_outgoing_upper": str(base_out),
            "structured_residual_outgoing_upper": str(structured_out),
            "reduction": str(base_out - structured_out),
            "used_in_official_chain": False,
        },
        "scope": {
            "established": "Corrected outward scalar error recurrence across the three already-frozen M14 segments, conditional on their imported whole-segment residual and strain bounds.",
            "not_established": [
                "independent reconstruction of the segment residual polynomials or continuous strain bounds",
                "full M14 backward adjoint enclosure beyond these three half-segments",
                "dual quadrature, nonlinear remainder, normalizer bound, or signed F endpoint transfer",
                "all-cutoff, blow-up, or continuum Navier-Stokes regularity theorem",
            ],
            "historical_chain": "Earlier strain-only outgoing radii remain immutable historical records and are superseded for continuation.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    tmp.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
