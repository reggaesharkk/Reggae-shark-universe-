#!/usr/bin/env python3
"""Fail-closed replay of the v0.28 reverse-time recurrence correction.

This is a separate arithmetic replay of the scalar recurrence. It is not an
independent derivation of the PDE estimate or a check of the Arb segment bounds.
"""
# Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
from __future__ import annotations

import hashlib
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/wp19_v0_28/reverse_time_sign_correction_20261001/reverse_time_sign_correction.json"
VERIFICATION_OUTPUT = DATA.with_name("separate_arithmetic_replay.txt")
EXPECTED = {
    "segments": [
        "d1b41363c88173594ec6c9e90453513cd3c8ed3e32c7037d2e73304d057a8c08",
        "c0bbf407df850b95e1a4b0daa3e1175962ce128e7e5f080d39127bd22b431fa6",
        "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
    ],
    "reports": [
        "41694c84922a28b0b99f9e2936589f8c2f8cb6c49fc2a68a281623a4fb39cb7e",
        "c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c",
        "cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f",
    ],
    "A_B": "b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a",
    "old_audit": "cd223389619c1780516514f7118c87ddc94e8d04c9c7528ce4cfc749948ee540",
    "old_audit_source": "55884d2d0c5b5c23100170f1e5bc167e70135eea2066b5be1b23a68e9cbbe2b7",
    "old_chain": "e8403177d80ac24d6658bc63e9ac6302af70b2bee8cdcdc61f5df11ff71f8e60",
    "producer": "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31",
    "adjoint_source": "0ba7cd0464076271a80864118d930d384d2cce6a1974650f278f8e02a7756e01",
    "galerkin_source": "c44824c9562c4e79b11e8838e663ecf77d0992ba5d146b4c5015717018baae14",
    "ab_source": "b746a70ed9b3d00b8e591b962358207e1050c1bfe378467729048cbcca2b8c77",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(x: Decimal, L: Decimal, R: Decimal) -> Decimal:
    # Recompute exp via a high precision Taylor series and bound its positive
    # tail by a geometric series. Directed rounding is used throughout.
    with localcontext() as ctx:
        ctx.prec = 110
        ctx.rounding = ROUND_CEILING
        z = L / Decimal(80000)
        term = Decimal(1)
        total = term
        n = 0
        while n < 120:
            n += 1
            term = term * z / Decimal(n)
            total += term
        next_term = term * z / Decimal(n + 1)
        ratio = z / Decimal(n + 2)
        tail_upper = next_term / (Decimal(1) - ratio)
        exp_upper = (total + tail_upper).next_plus()
        y = exp_upper * x + ((exp_upper - Decimal(1)) / L) * R
        return y.next_plus()


def main() -> None:
    d = json.loads(DATA.read_text())
    if d.get("schema") != "wp19-v0.28-reverse-time-sign-correction-v2":
        raise SystemExit("FAIL: schema mismatch")
    if not d.get("protocol", {}).get("no_retuning"):
        raise SystemExit("FAIL: no-retuning flag missing")
    if d.get("protocol", {}).get("cutoff_M") != 14 or d.get("protocol", {}).get("adjoint_support_M") != 15:
        raise SystemExit("FAIL: M14 segment / M15 adjoint support identity mismatch")
    base = ROOT / "results/wp19_v0_28"
    segpaths = [base / f"pilot_{name}/M14_segment_{step}.json" for name, step in [
        ("v2_36818369196", 239), ("chained_238_36819581437", 238), ("chained_237_36820757066", 237)]]
    reportpaths = [base / f"pilot_{name}/{report}" for name, report in [
        ("v2_36818369196", "verification.json"),
        ("chained_238_36819581437", "chain_verification.json"),
        ("chained_237_36820757066", "chain_verification.json")]]
    if [sha(p) for p in segpaths] != EXPECTED["segments"]:
        raise SystemExit("FAIL: frozen segment hash mismatch")
    if [sha(p) for p in reportpaths] != EXPECTED["reports"]:
        raise SystemExit("FAIL: frozen report hash mismatch")
    if sha(base / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json") != EXPECTED["A_B"]:
        raise SystemExit("FAIL: A/B hash mismatch")
    producer_paths = [
        base / "pilot_v2_36818369196/wp19_v0_28_adjoint_segment_arb.py",
        base / "pilot_chained_238_36819581437/wp19_v0_28_adjoint_segment_arb.py",
        base / "pilot_chained_237_36820757066/wp19_v0_28_adjoint_segment_arb.py",
    ]
    if [sha(p) for p in producer_paths] != [EXPECTED["producer"]] * 3:
        raise SystemExit("FAIL: archived producer source identity mismatch")
    if sha(ROOT / "src/wp19_v0_23_rk4_goal_adjoint.py") != EXPECTED["adjoint_source"]:
        raise SystemExit("FAIL: exact-adjoint source hash mismatch")
    if sha(ROOT / "src/wp16_036_dealiased_trajectory_gate.py") != EXPECTED["galerkin_source"]:
        raise SystemExit("FAIL: Galerkin-system source hash mismatch")
    if sha(base / "structured_uncertainty_ab_20261001/wp19_v0_28_structured_uncertainty_ab.py") != EXPECTED["ab_source"]:
        raise SystemExit("FAIL: A/B source hash mismatch")
    ab = json.loads((base / "structured_uncertainty_ab_20261001/structured_uncertainty_ab.json").read_text())
    segment_237 = json.loads(segpaths[-1].read_text())
    if (ab.get("step") != 237 or ab.get("M") != 14
            or ab.get("baseline_segment_sha256") != EXPECTED["segments"][-1]
            or ab.get("incoming_adjoint_error_upper") != json.loads(reportpaths[-1].read_text()).get("incoming_adjoint_error_upper")
            or ab.get("frozen") != segment_237.get("frozen")):
        raise SystemExit("FAIL: A/B baseline or incoming-radius identity mismatch")
    if sha(base / "backward_diffusion_audit_20261001/backward_diffusion_audit.json") != EXPECTED["old_audit"]:
        raise SystemExit("FAIL: prior audit hash mismatch")
    if sha(ROOT / "src/wp19_v0_28_backward_diffusion_log_norm_audit.py") != EXPECTED["old_audit_source"]:
        raise SystemExit("FAIL: prior source hash mismatch")
    if sha(base / "corrected_chain_20261001/corrected_recurrence_chain.json") != EXPECTED["old_chain"]:
        raise SystemExit("FAIL: prior chain hash mismatch")
    if [row["step"] for row in d["segment_rows"]] != [239, 238, 237]:
        raise SystemExit("FAIL: segment order mismatch")
    if d["sign_derivation"]["forward_time_error_equation"] != "de/dt = VJP(u,e) + nu*Lambda*e - r":
        raise SystemExit("FAIL: forward-time residual sign mismatch")
    if d["sign_derivation"]["backward_time_error_equation"] != "de/dtau = -VJP(u,e) - nu*Lambda*e + r":
        raise SystemExit("FAIL: reverse-time residual sign mismatch")
    if len(d["sign_derivation"].get("assumptions", [])) < 6:
        raise SystemExit("FAIL: required conditional assumptions are missing")
    if "M15" not in d["sign_derivation"].get("exact_adjoint_equation", ""):
        raise SystemExit("FAIL: exact adjoint support is not explicitly identified as M15")
    for row in d["segment_rows"]:
        if row["segment_source_sha256"] != EXPECTED["producer"]:
            raise SystemExit(f"FAIL: producer source not bound at step {row['step']}")
    radius = Decimal(d["segment_rows"][0]["incoming_error_upper"])
    for row in d["segment_rows"]:
        if Decimal(row["incoming_error_upper"]) != radius:
            raise SystemExit(f"FAIL: carry mismatch at step {row['step']}")
        got = replay(radius, Decimal(row["strain_log_norm_upper"]), Decimal(row["residual_L2_upper"]))
        archived = Decimal(row["archived_outgoing_upper_used_for_next_step"])
        if got > archived:
            raise SystemExit(f"FAIL: archived radius is below replay at step {row['step']}")
        if Decimal(row["optional_plus_diffusion_conservative_outgoing_upper"]) < archived:
            raise SystemExit(f"FAIL: comparison chain ordering at step {row['step']}")
        radius = archived
    if d.get("segment_237_A_B_rounding_reconciliation", {}).get("structured_residual_comparison_remains_diagnostic_only") is not True:
        raise SystemExit("FAIL: A/B diagnostic-only label absent")
    ab_view = d["segment_237_A_B_rounding_reconciliation"]
    for a, b in [("A_B_strain_upper", "segment_237_strain_upper"),
                 ("A_B_nominal_residual_upper", "segment_237_nominal_residual_upper"),
                 ("A_B_primal_radius_upper", "segment_237_true_primal_radius_upper")]:
        if Decimal(ab_view[a]) <= Decimal(ab_view[b]):
            raise SystemExit(f"FAIL: A/B upper must be strictly larger for {a}")
    if Decimal(ab_view["A_B_old_recomputed_outgoing_upper"]) <= Decimal(ab_view["archived_outgoing_upper"]):
        raise SystemExit("FAIL: A/B separate outgoing comparison changed")
    if ab_view["shared_baseline_segment_sha256"] != EXPECTED["segments"][-1]:
        raise SystemExit("FAIL: A/B baseline segment identity mismatch")
    if ab_view.get("nominal_residual_is_used_by_old_recurrence") is not False:
        raise SystemExit("FAIL: A/B old-recurrence input distinction absent")
    if abs(Decimal(ab_view["A_B_old_recurrence_replayed_upper"]) - Decimal(ab_view["A_B_old_recomputed_outgoing_upper"])) > Decimal("1e-60"):
        raise SystemExit("FAIL: A/B old recurrence did not replay")
    if abs(Decimal(ab_view["outgoing_difference_from_2e_9_strain_shift_using_shared_segment_residual"]) - Decimal(ab_view["A_B_minus_archived_outgoing_difference"])) > Decimal("1e-60"):
        raise SystemExit("FAIL: A/B output-gap attribution mismatch")
    if len(d.get("supersedes", [])) < 5:
        raise SystemExit("FAIL: machine-readable superseded-record links absent")
    if d.get("scope", {}).get("terminology") != "The verifier is a separate implementation of the recurrence, not an independent derivation of the PDE estimate.":
        raise SystemExit("FAIL: verifier scope label mismatch")
    report = (
        "PASS: hashes, source identities, order, radius carry, outward recurrence replay, conservative-chain ordering, A/B reconciliation, and scope labels\n"
        "LIMIT: conditional on producer-supplied segment strain/residual bounds; no endpoint transfer theorem\n"
        "METHOD: separate arithmetic implementation of the scalar recurrence; not an independent PDE derivation\n"
    )
    VERIFICATION_OUTPUT.write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
