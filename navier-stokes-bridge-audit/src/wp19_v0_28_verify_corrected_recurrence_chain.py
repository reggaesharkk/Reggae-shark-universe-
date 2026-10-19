#!/usr/bin/env python3
"""Independent fail-closed verifier for the corrected three-segment chain.

This deliberately does not import the chain producer. It reopens every pinned
segment/report and independently recomputes the outward recurrence with
Decimal, including reverse diffusion.
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
GENERATOR = ROOT / "src/wp19_v0_28_corrected_recurrence_chain.py"
VERIFIER = Path(__file__)
FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
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
EXPECTED_AUDIT = "cd223389619c1780516514f7118c87ddc94e8d04c9c7528ce4cfc749948ee540"
EXPECTED_AUDIT_SOURCE = "55884d2d0c5b5c23100170f1e5bc167e70135eea2066b5be1b23a68e9cbbe2b7"
H = Decimal(1) / Decimal(80000)
NU = Decimal("0.1")
PREC = 90


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recurrence(e0: Decimal, lbound: Decimal, rbound: Decimal) -> Decimal:
    if e0 < 0 or lbound <= 0 or rbound < 0:
        raise AssertionError("invalid nonnegative recurrence data")
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_CEILING
        z = (lbound * H).exp().next_plus()
        # All operands are nonnegative. ROUND_CEILING therefore encloses each
        # product, division, and final sum from above.
        return z * e0 + ((z - Decimal(1)) / lbound) * rbound


def fail(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(artifact_path: Path) -> dict:
    artifact = json.loads(artifact_path.read_text())
    fail(artifact.get("schema") == "wp19-v0.28-corrected-adjoint-error-chain-v1", "schema mismatch")
    fail(artifact.get("status") == "PASS_LIMITED_CORRECTED_SCALAR_RECURRENCE_CHAIN", "status mismatch")
    fail(artifact.get("rights_notice") == "Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.", "rights notice mismatch")
    fail(digest(GENERATOR) == artifact["provenance_sha256"]["generator_source"], "generator source hash mismatch")
    fail(digest(VERIFIER) == artifact["provenance_sha256"]["independent_verifier_source"], "verifier source hash mismatch")
    fail([digest(p) for p in SEGMENTS] == EXPECTED_SEGMENTS, "frozen segment hash mismatch")
    fail([digest(p) for p in REPORTS] == EXPECTED_REPORTS, "historical report hash mismatch")
    fail(digest(AB) == EXPECTED_AB and digest(OLD_AUDIT) == EXPECTED_AUDIT, "frozen diagnostic input hash mismatch")
    old_source = ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py"
    fail(digest(old_source) == EXPECTED_AUDIT_SOURCE, "prior audit source hash mismatch")

    protocol = artifact["protocol"]
    fail(protocol["cutoff_M"] == 14 and protocol["viscosity"] == "0.1", "cutoff/viscosity changed")
    fail(protocol["terminal_time"] == "3/1000" and protocol["frozen_segments_in_backward_order"] == [239, 238, 237], "scope/order changed")
    fail(protocol["fixed_witness_sha256"] == FROZEN["witness_sha256"] and protocol["K36_sha256"] == FROZEN["K36_sha256"], "frozen witness/K36 changed")
    fail(protocol["C500_portable_semantic_sha256"] == FROZEN["C500_portable_semantic_sha256"] and protocol["no_retuning"] is True, "C500 semantics/retuning flag changed")

    max_k2 = max(i*i + j*j + k*k for i in range(-15, 16) for j in range(-15, 16)
                 for k in range(-15, 16) if i*i + j*j + k*k <= 225)
    fail(max_k2 == 225, "Fourier support maximum not 225")
    anti_diffusion = NU * max_k2
    fail(artifact["spectral_support_check"]["max_k_squared"] == max_k2, "artifact support maximum mismatch")
    fail(Decimal(artifact["spectral_support_check"]["reverse_diffusion_growth_bound"]) == anti_diffusion, "reverse diffusion bound mismatch")
    rows = artifact.get("segments")
    fail(isinstance(rows, list) and len(rows) == 3, "expected exactly three segment rows")
    incoming = Decimal(json.loads(SEGMENTS[0].read_text())["bounds"]["terminal_adjoint_error_upper"])
    recomputed = []
    for idx, row in enumerate(rows):
        seg = json.loads(SEGMENTS[idx].read_text())
        report = json.loads(REPORTS[idx].read_text())
        stepno = 239 - idx
        fail(seg["step"] == stepno and row["step"] == stepno, "segment order mismatch")
        fail(row["forward_time_interval_rational"] == [f"{stepno}/80000", f"{stepno+1}/80000"], "continuous segment interval mismatch")
        fail(row["segment_sha256"] == digest(SEGMENTS[idx]) and row["historical_recurrence_report_sha256"] == digest(REPORTS[idx]), "row provenance mismatch")
        bounds = seg["bounds"]
        strain = Decimal(bounds["logarithmic_norm_upper"])
        residual = Decimal(bounds["residual_L2_upper"])
        total_l = strain + anti_diffusion
        expected = recurrence(incoming, total_l, residual)
        oldincoming = report.get("incoming_adjoint_error_upper", bounds["terminal_adjoint_error_upper"])
        historical_strain_result = recurrence(Decimal(oldincoming), strain, residual)
        historical_claim = Decimal(report.get("backward_error_after_one_segment_upper", report.get("backward_error_after_segment_upper")))
        fail(Decimal(row["incoming_error_upper_corrected_chain"]) == incoming, "chain incoming radius mismatch")
        fail(Decimal(row["strain_log_norm_upper_imported"]) == strain, "strain bound mismatch")
        fail(Decimal(row["reverse_diffusion_log_norm_upper"]) == anti_diffusion, "per-segment diffusion term mismatch")
        fail(Decimal(row["total_log_norm_upper_used"]) == total_l, "total growth coefficient mismatch")
        fail(Decimal(row["residual_L2_upper_imported"]) == residual, "residual bound mismatch")
        fail(Decimal(row["outgoing_error_upper_corrected_chain"]) == expected, "corrected outgoing recurrence mismatch")
        fail(Decimal(row["historical_strain_only_recurrence_recomputed"]) == historical_strain_result, "historical recurrence reconstruction mismatch")
        fail(historical_strain_result <= historical_claim < expected, "old chain not shown underbounded by corrected chain")
        fail(row["historical_value_underbounds_corrected_value"] is True, "supersession marker missing")
        recomputed.append(expected)
        incoming = expected

    ab = json.loads(AB.read_text())
    lastseg = json.loads(SEGMENTS[-1].read_text())["bounds"]
    l237 = Decimal(lastseg["logarithmic_norm_upper"]) + anti_diffusion
    r_ab = Decimal(ab["nominal_residual_upper"]) + Decimal(ab["structured_fourier_young_penalty_upper"])
    rowdiag = artifact["segment_237_structured_residual_sensitivity_only"]
    base_in = Decimal(rows[-1]["incoming_error_upper_corrected_chain"])
    base_out = recurrence(base_in, l237, Decimal(lastseg["residual_L2_upper"]))
    ab_out = recurrence(base_in, l237, r_ab)
    fail(rowdiag["used_in_official_chain"] is False, "structured sensitivity improperly included in official chain")
    fail(Decimal(rowdiag["base_residual_outgoing_upper"]) == base_out and Decimal(rowdiag["structured_residual_outgoing_upper"]) == ab_out, "A/B sensitivity mismatch")
    fail(Decimal(rowdiag["reduction"]) == base_out - ab_out and ab_out < base_out, "A/B sensitivity reduction mismatch")
    scope = artifact["scope"]
    fail("independent reconstruction of the segment residual polynomials or continuous strain bounds" in scope["not_established"], "scope caveat missing")
    fail("full M14 backward adjoint enclosure beyond these three half-segments" in scope["not_established"], "full-adjoint caveat missing")
    return {
        "schema": "wp19-v0.28-corrected-chain-independent-verification-v1",
        "status": "PASS_LIMITED_CORRECTED_SCALAR_RECURRENCE_CHAIN",
        "input_chain_sha256": digest(artifact_path),
        "verifier_source_sha256": digest(VERIFIER),
        "segments_verified_once_in_backward_order": [239, 238, 237],
        "reverse_diffusion_log_norm_upper": str(anti_diffusion),
        "corrected_outgoing_error_upper_by_step": {str(n): str(v) for n, v in zip((239, 238, 237), recomputed)},
        "scope": "Scalar outward recurrence recheck only, conditional on the pinned producer-supplied whole-segment bounds; not a full adjoint or observable certificate.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = verify(args.artifact)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        tmp = args.output.with_suffix(".tmp")
        tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        tmp.replace(args.output)


if __name__ == "__main__":
    main()
