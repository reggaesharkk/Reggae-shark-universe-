#!/usr/bin/env python3
"""Audit the v0.28 backward-error recurrence for the reverse-diffusion term.

This is a small Decimal-only re-evaluation of three already archived M14
segments. It does not regenerate any trajectory or Arb polynomial. The frozen
segment records provide outward strain/residual/terminal-error bounds; this
script adds the exact spectral upper bound nu*N_high**2 to the logarithmic
norm because the backward adjoint evolves with +nu*|k|^2.
"""
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
VERIFICATIONS = [
    BASE / "pilot_v2_36818369196/verification.json",
    BASE / "pilot_chained_238_36819581437/chain_verification.json",
    BASE / "pilot_chained_237_36820757066/chain_verification.json",
]
AB_PATH = BASE / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json"
EXPECTED_SEGMENT_SHA = [
    "d1b41363c88173594ec6c9e90453513cd3c8ed3e32c7037d2e73304d057a8c08",
    "c0bbf407df850b95e1a4b0daa3e1175962ce128e7e5f080d39127bd22b431fa6",
    "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
]
EXPECTED_VERIFICATION_SHA = [
    "41694c84922a28b0b99f9e2936589f8c2f8cb6c49fc2a68a281623a4fb39cb7e",
    "c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c",
    "cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f",
]
EXPECTED_AB_SHA = "b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a"
NU = Decimal("0.1")
N_HIGH = 15
H = Decimal(1) / Decimal(80000)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upper_recurrence(incoming: Decimal, L: Decimal, R: Decimal) -> Decimal:
    """Outward Decimal one-step Gronwall recurrence."""
    with localcontext() as c:
        c.prec = 90
        c.rounding = ROUND_CEILING
        amp = (L * H).exp().next_plus()
        return amp * incoming + ((amp - 1) / L) * R


def max_squared_radius(n: int) -> int:
    vals = [i*i + j*j + k*k
            for i in range(-n, n+1)
            for j in range(-n, n+1)
            for k in range(-n, n+1)
            if i*i + j*j + k*k <= n*n]
    if not vals or max(vals) != n*n:
        raise ValueError("unexpected spherical Fourier support")
    return max(vals)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=BASE / "backward_diffusion_audit_20261001/backward_diffusion_audit.json")
    args = ap.parse_args()

    for p, expected in zip(SEGMENTS, EXPECTED_SEGMENT_SHA):
        if sha(p) != expected:
            raise ValueError(f"frozen segment hash mismatch: {p}")
    for p, expected in zip(VERIFICATIONS, EXPECTED_VERIFICATION_SHA):
        if sha(p) != expected:
            raise ValueError(f"frozen verifier hash mismatch: {p}")
    if sha(AB_PATH) != EXPECTED_AB_SHA:
        raise ValueError("frozen structured A/B artifact hash mismatch")
    if not all(p.is_file() for p in VERIFICATIONS + [AB_PATH]):
        raise FileNotFoundError("required archived recurrence or A/B artifact missing")

    max_k2 = max_squared_radius(N_HIGH)
    diffusion_log_norm = NU * Decimal(max_k2)
    rows = []
    incoming = None
    for i, (seg_path, ver_path) in enumerate(zip(SEGMENTS, VERIFICATIONS)):
        seg = json.loads(seg_path.read_text())
        ver = json.loads(ver_path.read_text())
        if seg.get("schema") != "wp19-v0.28-adjoint-segment-arb-v2" or seg.get("M") != 14 or seg.get("step") != 239-i:
            raise ValueError("segment identity/order mismatch")
        if seg.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY":
            raise ValueError("segment did not complete its archived enclosure")
        b = seg["bounds"]
        if incoming is None:
            incoming = Decimal(b["terminal_adjoint_error_upper"])
        strain = Decimal(b["logarithmic_norm_upper"])
        corrected_L = strain + diffusion_log_norm
        R = Decimal(b["residual_L2_upper"])
        corrected_out = upper_recurrence(incoming, corrected_L, R)
        old_out_text = ver.get("backward_error_after_one_segment_upper", ver.get("backward_error_after_segment_upper"))
        if old_out_text is None:
            raise ValueError("archived verifier output lacks recurrence endpoint")
        old_out = Decimal(old_out_text)
        archived_in_text = ver.get("incoming_adjoint_error_upper")
        if archived_in_text is None:
            archived_in = Decimal(b["terminal_adjoint_error_upper"])
        else:
            archived_in = Decimal(archived_in_text)
        archived_formula_out = upper_recurrence(archived_in, strain, R)
        if archived_formula_out > old_out:
            raise ValueError("archived recurrence endpoint undercuts strain-only recomputation")
        rows.append({
            "step": seg["step"],
            "segment_sha256": sha(seg_path),
            "archived_verification_sha256": sha(ver_path),
            "incoming_error_upper_corrected_chain": str(incoming),
            "strain_log_norm_upper": str(strain),
            "reverse_diffusion_log_norm_upper": str(diffusion_log_norm),
            "corrected_total_log_norm_upper": str(corrected_L),
            "residual_upper": str(R),
            "archived_incoming_error_upper": str(archived_in),
            "strain_only_recomputed_outgoing_upper": str(archived_formula_out),
            "archived_outgoing_error_upper": str(old_out),
            "recomputed_outgoing_error_upper": str(corrected_out),
            "archived_outgoing_matches_strain_only_recurrence_with_outward_slack": True,
            "archived_recurrence_underbounds_corrected": corrected_out > old_out,
        })
        incoming = corrected_out

    ab = json.loads(AB_PATH.read_text())
    if ab.get("schema") != "wp19-v0.28-structured-primal-uncertainty-ab-v1" or ab.get("step") != 237 or ab.get("status") != "MATERIAL_TIGHTENING":
        raise ValueError("structured A/B result identity/status mismatch")
    seg237 = json.loads(SEGMENTS[-1].read_text())
    L237 = Decimal(seg237["bounds"]["logarithmic_norm_upper"]) + diffusion_log_norm
    old_R = Decimal(seg237["bounds"]["residual_L2_upper"])
    new_R = Decimal(ab["nominal_residual_upper"]) + Decimal(ab["structured_fourier_young_penalty_upper"])
    old_ab_out = upper_recurrence(Decimal(rows[-1]["incoming_error_upper_corrected_chain"]), L237, old_R)
    new_ab_out = upper_recurrence(Decimal(rows[-1]["incoming_error_upper_corrected_chain"]), L237, new_R)
    result = {
        "schema": "wp19-v0.28-backward-diffusion-log-norm-audit-v1",
        "status": "RECURRENCE_CORRECTION_REQUIRED",
        "audit_source_sha256": sha(Path(__file__)),
        "frozen_scope": "M14 backward-adjoint finite segments 239, 238, 237 only; no trajectory or residual regenerated",
        "equation_used": "e' = P[(grad u)^T e - (u.grad)e] + nu*Lambda*e + r",
        "energy_identity_bound": "d||e||_2/dt <= (||S(u)||_op_infinity + nu*max_k|k|^2)||e||_2 + ||r||_2",
        "reason": "The backward adjoint reverses the forward viscous sign: +nu|k|^2 is anti-diffusive and belongs in the growth exponent. The archived recurrence used the strain bound alone.",
        "constants": {"nu": str(NU), "high_cutoff": N_HIGH, "max_k_squared_verified_from_ball_support": max_k2,
                      "reverse_diffusion_log_norm_upper": str(diffusion_log_norm), "step_width": str(H)},
        "input_hashes": {"segments": [sha(p) for p in SEGMENTS], "verifications": [sha(p) for p in VERIFICATIONS], "structured_ab": sha(AB_PATH)},
        "segment_rows": rows,
        "segment_237_structured_ab_recomputed_with_corrected_growth": {
            "old_residual_recurrence_outgoing_upper": str(old_ab_out),
            "structured_residual_recurrence_outgoing_upper": str(new_ab_out),
            "absolute_reduction": str(old_ab_out-new_ab_out),
            "relative_reduction": str((old_ab_out-new_ab_out)/old_ab_out),
            "penalty_ratio_unchanged_from_frozen_a_b": ab["new_over_old_penalty_upper"],
        },
        "verdict": "Archived residual enclosures and the standalone A/B penalty reduction remain as recorded. The old chained scalar recurrence values are low because they omit backward anti-diffusion; they must not be used as validated adjoint-error radii. Recompute the chain with this corrected logarithmic norm before any further segment continuation.",
        "claim_boundary": "Finite-segment recurrence audit only. Not a complete adjoint enclosure, signed-observable transfer certificate, all-cutoff result, blow-up result, or continuum regularity theorem.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    tmp.replace(args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
