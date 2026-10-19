#!/usr/bin/env python3
"""Fail-closed structural preflight for a completed WP16 N11 turnover certificate.

This is NOT the independent interval-arithmetic verifier. It checks that a
candidate publication manifest is complete, self-consistent, bound to the
fixed public inputs, and already records all theorem gates as passed.

Exit 0: structurally ready for the independent mathematical verifier.
Exit 2: blocked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

EXPECTED = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_keys_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "exact_anchor_result_sha256": "327378d1ba2978a66484f1266d984d240fdfdaf4c5785889a48eb187c9650885",
}
EXPECTED_N = 11
EXPECTED_NU = Decimal("0.1")
EXPECTED_T = Decimal("0.003")
EXPECTED_SEGMENTS = 120
PLACEHOLDER = re.compile(r"PENDING|REPLACE|TODO|TBD", re.I)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def blocked(msg: str) -> None:
    raise ValueError(msg)


def dec(x, name: str) -> Decimal:
    try:
        y = Decimal(str(x))
    except (InvalidOperation, ValueError):
        blocked(f"{name}: not a decimal")
    if not y.is_finite():
        blocked(f"{name}: not finite")
    return y


def resolved(x) -> bool:
    return isinstance(x, str) and bool(x.strip()) and not PLACEHOLDER.search(x)


def check_sha(x, name: str) -> None:
    if not isinstance(x, str) or not SHA256_RE.fullmatch(x):
        blocked(f"{name}: invalid SHA-256")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--output", type=Path, default=Path("turnover_certificate_preflight.json"))
    args = ap.parse_args()

    report = {"status": "BLOCKED", "checks": [], "manifest": str(args.manifest)}

    try:
        obj = json.loads(args.manifest.read_text(encoding="utf-8"))

        if obj.get("schema") != "wp16-finite-n11-turnover-certificate-v1":
            blocked("schema mismatch")
        if not resolved(obj.get("protocol_version")):
            blocked("protocol_version unresolved")
        if not resolved(obj.get("created_at_utc")):
            blocked("created_at_utc unresolved")
        if obj.get("status") not in {"COMPLETE_VERIFIED", "CERTIFIED"}:
            blocked("status is not a verified completed-certificate state")

        fixed = obj.get("fixed_inputs", {})
        for k, v in EXPECTED.items():
            if fixed.get(k) != v:
                blocked(f"fixed input mismatch: {k}")

        prm = obj.get("parameters", {})
        if int(prm.get("N", -1)) != EXPECTED_N:
            blocked("N mismatch")
        if dec(prm.get("nu"), "nu") != EXPECTED_NU:
            blocked("nu mismatch")
        if dec(prm.get("T"), "T") != EXPECTED_T:
            blocked("T mismatch")
        if prm.get("observable") != "F=I-9O":
            blocked("observable mismatch")
        if int(prm.get("initial_pair_count", -1)) != 112:
            blocked("initial pair count mismatch")

        predictors = obj.get("predictors", {})
        for k in ("predictor_a_sha256", "predictor_b_sha256"):
            check_sha(predictors.get(k), k)

        arithmetic = obj.get("arithmetic", {})
        if not resolved(arithmetic.get("library")):
            blocked("arithmetic library unresolved")
        if not isinstance(arithmetic.get("precision_bits"), int) or arithmetic["precision_bits"] <= 0:
            blocked("precision_bits unresolved")
        if arithmetic.get("outward_rounding") is not True:
            blocked("outward_rounding must be true")

        if int(obj.get("segment_count", -1)) != EXPECTED_SEGMENTS:
            blocked("segment_count mismatch")
        segs = obj.get("segments")
        if not isinstance(segs, list) or len(segs) != EXPECTED_SEGMENTS:
            blocked("segments must contain exactly 120 records")

        ids = []
        previous_end = Decimal("0")
        pa = predictors["predictor_a_sha256"]
        pb = predictors["predictor_b_sha256"]
        for pos, s in enumerate(segs):
            if not isinstance(s, dict):
                blocked(f"segment {pos}: not an object")
            idx = s.get("index")
            if idx != pos:
                blocked(f"segment order/index mismatch at position {pos}")
            ids.append(idx)
            start = dec(s.get("t_start"), f"segment {idx} t_start")
            end = dec(s.get("t_end"), f"segment {idx} t_end")
            if start != previous_end:
                blocked(f"segment {idx}: gap/overlap at start")
            if end <= start:
                blocked(f"segment {idx}: nonpositive width")
            previous_end = end
            check_sha(s.get("artifact_sha256"), f"segment {idx} artifact_sha256")
            if s.get("predictor_a_sha256") != pa or s.get("predictor_b_sha256") != pb:
                blocked(f"segment {idx}: predictor hash mismatch")
            if s.get("protocol_version") != obj["protocol_version"]:
                blocked(f"segment {idx}: protocol version mismatch")
            for fld in ("residual_L2_upper", "gradient_Linf_upper", "trajectory_radius_upper"):
                v = dec(s.get(fld), f"segment {idx} {fld}")
                if v < 0:
                    blocked(f"segment {idx}: negative {fld}")

        if len(set(ids)) != EXPECTED_SEGMENTS:
            blocked("duplicate segment index")
        if previous_end != EXPECTED_T:
            blocked("segment cover does not end exactly at T=0.003")

        agg = obj.get("aggregate", {})
        radius = dec(agg.get("terminal_L2_error_radius_upper"), "terminal radius")
        if radius < 0:
            blocked("negative terminal radius")
        zlo = dec(agg.get("normalizer_abs_lower"), "normalizer lower")
        if zlo <= 0:
            blocked("normalizer lower bound is not positive")

        f0 = agg.get("F0_interval")
        ft = agg.get("FT_interval")
        if not (isinstance(f0, list) and len(f0) == 2):
            blocked("F0_interval malformed")
        if not (isinstance(ft, list) and len(ft) == 2):
            blocked("FT_interval malformed")
        f0lo, f0hi = dec(f0[0], "F0 lower"), dec(f0[1], "F0 upper")
        ftlo, fthi = dec(ft[0], "FT lower"), dec(ft[1], "FT upper")
        if not (f0lo <= f0hi and f0lo > 0):
            blocked("initial margin interval does not prove positivity")
        if not (ftlo <= fthi and fthi < 0):
            blocked("endpoint margin interval does not prove negativity")

        for section in ("generator", "independent_verifier"):
            block = obj.get(section, {})
            if not resolved(block.get("path")):
                blocked(f"{section}.path unresolved")
            check_sha(block.get("sha256"), f"{section}.sha256")
        iv = obj["independent_verifier"]
        check_sha(iv.get("result_sha256"), "independent_verifier.result_sha256")
        if iv.get("status") != "PASS":
            blocked("independent verifier status is not PASS")

        gates = obj.get("gates", {})
        required_gates = (
            "fixed_input_hashes",
            "predictor_hashes",
            "segment_coverage",
            "error_recurrence",
            "normalizer_positive",
            "initial_margin_positive",
            "endpoint_margin_negative",
            "independent_verifier_pass",
        )
        missing = [k for k in required_gates if gates.get(k) is not True]
        if missing:
            blocked("false/unresolved theorem gates: " + ", ".join(missing))

        report["status"] = "PASS"
        report["checks"] = [
            "fixed inputs",
            "protocol and arithmetic metadata",
            "120-segment exact cover",
            "per-segment predictor/protocol binding",
            "positive normalizer lower bound",
            "positive initial margin interval",
            "negative endpoint margin interval",
            "independent verifier PASS",
            "all publication gates true",
        ]

    except Exception as e:
        report["error"] = str(e)

    serialized = json.dumps(report, indent=2) + "\n"
    args.output.write_text(serialized, encoding="utf-8")
    print(report["status"])
    if "error" in report:
        print(report["error"])
    print("report_sha256 =", hashlib.sha256(serialized.encode()).hexdigest())
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
