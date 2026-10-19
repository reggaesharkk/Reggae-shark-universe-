#!/usr/bin/env python3
"""Fail-closed recurrence verifier for the M14 segment 237 continuation.

Checks fixed provenance, whole-segment Arb output scalars and their outward
component sum, then chains the Decimal error recurrence from segment 238.
It does not independently recompute the Arb residual polynomial.
"""
import hashlib
import json
import sys
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path

PROTOCOL = "wp19-v0.28-adjoint-segment-arb-v2"
EXPECTED_FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
CURRENT_STEP = 237
PREVIOUS_STEP = 238


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_segment(x, step):
    if x.get("schema") != PROTOCOL or x.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
        raise ValueError("unexpected schema/status")
    if x.get("M") != 14 or x.get("step") != step or x.get("backward_order_index") != 239 - step:
        raise ValueError("segment/cutoff order mismatch")
    if x.get("forward_time_interval_rational") != [f"{step}/80000", f"{step + 1}/80000"]:
        raise ValueError("continuous interval mismatch")
    if x.get("precision_bits") != 192 or x.get("frozen") != EXPECTED_FROZEN:
        raise ValueError("precision or frozen identity mismatch")
    source = Path(__file__).with_name("wp19_v0_28_adjoint_segment_arb.py")
    if sha(source) != x.get("source_sha256"):
        raise ValueError("Arb producer source hash mismatch")
    bounds = {k: Decimal(v) for k, v in x["bounds"].items()}
    if not all(v.is_finite() and v >= 0 for v in bounds.values()):
        raise ValueError("non-finite or negative reported bound")
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.rounding = ROUND_CEILING
        component_sum = bounds["nominal_residual_L2_upper"] + bounds["primal_uncertainty_residual_penalty_upper"]
        if bounds["residual_L2_upper"] < component_sum - Decimal("0.000002"):
            raise ValueError("total residual undercuts components beyond output rounding")
    return bounds


def verify(current_path, previous_path, previous_verification_path):
    current_path, previous_path = Path(current_path), Path(previous_path)
    previous_verification_path = Path(previous_verification_path)
    current = json.loads(current_path.read_text())
    previous = json.loads(previous_path.read_text())
    previous_check = json.loads(previous_verification_path.read_text())
    cb = check_segment(current, CURRENT_STEP)
    check_segment(previous, PREVIOUS_STEP)

    previous_digest = sha(previous_path)
    previous_check_digest = sha(previous_verification_path)
    if previous_check.get("status") != "PASS LIMITED CHAINED SEGMENT RECURRENCE CHECK":
        raise ValueError("preceding segment did not pass its chained recurrence check")
    if previous_check.get("step") != PREVIOUS_STEP or previous_check.get("segment_sha256") != previous_digest:
        raise ValueError("preceding recurrence report is not bound to segment 238")
    if previous.get("frozen") != current.get("frozen"):
        raise ValueError("frozen identities changed across segment boundary")

    # Backward propagation: use segment 238's already-propagated error as input.
    incoming = Decimal(previous_check["backward_error_after_segment_upper"])
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.rounding = ROUND_CEILING
        h = Decimal("0.0000125")
        L, R = cb["logarithmic_norm_upper"], cb["residual_L2_upper"]
        amplification = (L * h).exp().next_plus()
        residual_factor = ((amplification - 1) / L) if L else h
        outgoing = amplification * incoming + residual_factor * R

    return {
        "status": "PASS LIMITED CHAINED SEGMENT RECURRENCE CHECK",
        "M": 14,
        "step": CURRENT_STEP,
        "backward_order_index": 239 - CURRENT_STEP,
        "segment_sha256": sha(current_path),
        "previous_segment_sha256": previous_digest,
        "previous_verification_sha256": previous_check_digest,
        "incoming_adjoint_error_upper": str(incoming),
        "backward_error_after_segment_upper": str(outgoing),
        "verified_scope": "provenance, frozen identities, producer-supplied Arb scalar bounds, component consistency, and outward Decimal recurrence; no independent residual recomputation",
        "pending": ["237 remaining M14 segments", "other cutoff paths", "rigorous dual quadrature", "nonlinear remainder", "normalizer transfer"],
        "claim_boundary": "Three consecutive finite M14 half-segment recurrence steps only; no full adjoint or signed-numerator cutoff-transfer certificate.",
    }


if __name__ == "__main__":
    result = verify(sys.argv[1], sys.argv[2], sys.argv[3])
    out = Path(sys.argv[4])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    tmp.replace(out)
    print(json.dumps(result, indent=2), flush=True)
