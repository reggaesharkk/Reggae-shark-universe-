#!/usr/bin/env python3
"""Independent fail-closed check of the v0.28 reverse-diffusion audit."""
from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/wp19_v0_28"
SEGMENTS = [
    BASE / "pilot_v2_36818369196/M14_segment_239.json",
    BASE / "pilot_chained_238_36819581437/M14_segment_238.json",
    BASE / "pilot_chained_237_36820757066/M14_segment_237.json",
]
VERIFY_FILES = [
    BASE / "pilot_v2_36818369196/verification.json",
    BASE / "pilot_chained_238_36819581437/chain_verification.json",
    BASE / "pilot_chained_237_36820757066/chain_verification.json",
]
AB = BASE / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json"
SEGMENT_HASHES = [
    "d1b41363c88173594ec6c9e90453513cd3c8ed3e32c7037d2e73304d057a8c08",
    "c0bbf407df850b95e1a4b0daa3e1175962ce128e7e5f080d39127bd22b431fa6",
    "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
]
VERIFY_HASHES = [
    "41694c84922a28b0b99f9e2936589f8c2f8cb6c49fc2a68a281623a4fb39cb7e",
    "c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c",
    "cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f",
]
AB_HASH = "b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a"
AUDIT_HASH = "cd223389619c1780516514f7118c87ddc94e8d04c9c7528ce4cfc749948ee540"
SOURCE = ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py"
H = Decimal(1) / Decimal(80000)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def step(incoming: Decimal, L: Decimal, R: Decimal) -> Decimal:
    with localcontext() as c:
        c.prec = 90
        c.rounding = ROUND_CEILING
        q = (L * H).exp().next_plus()
        return q * incoming + (q - 1) / L * R


def verify(path: Path) -> None:
    audit = json.loads(path.read_text())
    assert audit["schema"] == "wp19-v0.28-backward-diffusion-log-norm-audit-v1"
    assert audit["status"] == "RECURRENCE_CORRECTION_REQUIRED"
    assert audit["audit_source_sha256"] == sha(SOURCE)
    assert sha(path) == AUDIT_HASH
    assert sha(AB) == AB_HASH
    assert [sha(p) for p in SEGMENTS] == SEGMENT_HASHES
    assert [sha(p) for p in VERIFY_FILES] == VERIFY_HASHES

    support_max = max(i*i+j*j+k*k
                      for i in range(-15, 16)
                      for j in range(-15, 16)
                      for k in range(-15, 16)
                      if i*i+j*j+k*k <= 225)
    assert support_max == 225
    viscous = Decimal("0.1") * support_max
    assert audit["constants"]["reverse_diffusion_log_norm_upper"] == str(viscous)

    incoming = Decimal(json.loads(SEGMENTS[0].read_text())["bounds"]["terminal_adjoint_error_upper"])
    rows = audit["segment_rows"]
    assert len(rows) == 3
    for idx, (segment_path, verification_path, row) in enumerate(zip(SEGMENTS, VERIFY_FILES, rows)):
        segment = json.loads(segment_path.read_text())
        archived = json.loads(verification_path.read_text())
        bounds = segment["bounds"]
        assert segment["step"] == 239 - idx and row["step"] == segment["step"]
        strain = Decimal(bounds["logarithmic_norm_upper"])
        residual = Decimal(bounds["residual_L2_upper"])
        total = strain + viscous
        corrected = step(incoming, total, residual)
        assert Decimal(row["incoming_error_upper_corrected_chain"]) == incoming
        assert Decimal(row["corrected_total_log_norm_upper"]) == total
        assert Decimal(row["recomputed_outgoing_error_upper"]) == corrected

        old_in = Decimal(archived.get("incoming_adjoint_error_upper",
                                     bounds["terminal_adjoint_error_upper"]))
        old_computed = step(old_in, strain, residual)
        old_claim = Decimal(archived.get("backward_error_after_one_segment_upper",
                                        archived.get("backward_error_after_segment_upper")))
        assert Decimal(row["strain_only_recomputed_outgoing_upper"]) == old_computed
        assert old_computed <= old_claim < corrected
        assert row["archived_recurrence_underbounds_corrected"] is True
        incoming = corrected

    ab = json.loads(AB.read_text())
    last = audit["segment_237_structured_ab_recomputed_with_corrected_growth"]
    segment237 = json.loads(SEGMENTS[-1].read_text())
    L = Decimal(segment237["bounds"]["logarithmic_norm_upper"]) + viscous
    residual_old = Decimal(segment237["bounds"]["residual_L2_upper"])
    residual_new = Decimal(ab["nominal_residual_upper"]) + Decimal(ab["structured_fourier_young_penalty_upper"])
    corrected_input = Decimal(rows[-1]["incoming_error_upper_corrected_chain"])
    old_out = step(corrected_input, L, residual_old)
    new_out = step(corrected_input, L, residual_new)
    assert Decimal(last["old_residual_recurrence_outgoing_upper"]) == old_out
    assert Decimal(last["structured_residual_recurrence_outgoing_upper"]) == new_out
    assert new_out < old_out
    assert ab["new_over_old_penalty_upper"] == last["penalty_ratio_unchanged_from_frozen_a_b"]
    print("PASS: frozen input hashes, exact reverse-diffusion contribution, all three corrected outward recurrences, and structured segment-237 comparison")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python src/wp19_v0_28_verify_backward_diffusion_audit.py <audit.json>")
    verify(Path(sys.argv[1]))
