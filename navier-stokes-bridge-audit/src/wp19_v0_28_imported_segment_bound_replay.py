#!/usr/bin/env python3
"""Rebuild the three frozen WP19 v0.28 segment-bound records from pinned inputs.

This is a deterministic producer replay and input-integrity check. It is not a
second mathematical implementation of the Bernstein or residual bounds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "src/wp19_v0_28_adjoint_segment_arb.py"
FROZEN = [
    (239, ROOT / "results/wp19_v0_28/pilot_v2_36818369196/M14_segment_239.json"),
    (238, ROOT / "results/wp19_v0_28/pilot_chained_238_36819581437/M14_segment_238.json"),
    (237, ROOT / "results/wp19_v0_28/pilot_chained_237_36820757066/M14_segment_237.json"),
]
EXPECTED_PRODUCER_SHA256 = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def rebuild(step: int, frozen_path: Path, args: argparse.Namespace) -> dict:
    frozen = read_json(frozen_path)
    if frozen.get("step") != step or frozen.get("M") != 14:
        raise AssertionError(f"frozen segment scope mismatch at step {step}")
    out_path = args.output_dir / f"M14_segment_{step}_replay.json"
    log_path = args.output_dir / f"M14_segment_{step}_replay.log"
    command = [
        sys.executable, str(PRODUCER), "--M", "14", "--step", str(step),
        "--lower-dir", str(args.lower_dir),
        "--adjoint-dir", str(args.adjoint_dir),
        "--sign-chart", str(args.sign_chart),
        "--c500", str(args.c500),
        "--output", str(out_path),
    ]
    with log_path.open("w") as log:
        subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                       check=True, timeout=args.step_timeout)
    regenerated = read_json(out_path)
    if regenerated.get("step") != step or regenerated.get("M") != 14:
        raise AssertionError(f"regenerated segment scope mismatch at step {step}")
    if regenerated.get("source_sha256") != EXPECTED_PRODUCER_SHA256:
        raise AssertionError(f"producer source hash mismatch at step {step}")
    if regenerated.get("inputs") != frozen.get("inputs"):
        raise AssertionError(f"frozen input identities differ at step {step}")
    if regenerated.get("bounds") != frozen.get("bounds"):
        raise AssertionError(f"regenerated bound values differ at step {step}")
    if regenerated.get("forward_time_interval_rational") != frozen.get("forward_time_interval_rational"):
        raise AssertionError(f"segment interval differs at step {step}")
    return {
        "step": step,
        "frozen_record": frozen_path.relative_to(ROOT).as_posix(),
        "frozen_record_sha256": digest(frozen_path),
        "producer_sha256": regenerated["source_sha256"],
        "input_sha256": regenerated["inputs"],
        "bounds_match_exactly": True,
        "bounds": regenerated["bounds"],
        "replay_log": log_path.relative_to(ROOT).as_posix(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lower-dir", type=Path, required=True)
    parser.add_argument("--adjoint-dir", type=Path, required=True)
    parser.add_argument("--sign-chart", type=Path, required=True)
    parser.add_argument("--c500", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--step-timeout", type=int, default=2400)
    args = parser.parse_args()
    args.output_dir = args.output_dir.resolve()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if digest(PRODUCER) != EXPECTED_PRODUCER_SHA256:
        raise AssertionError("frozen producer source SHA-256 mismatch")
    rows = [rebuild(step, path, args) for step, path in FROZEN]
    result = {
        "schema": "wp19-v0.28-imported-segment-bound-replay-v1",
        "status": "PASS_DETERMINISTIC_PRODUCER_REPLAY",
        "segment_order": [239, 238, 237],
        "steps": rows,
        "scope": {
            "checks": [
                "pinned input artifact archives were SHA-256 verified by the workflow",
                "producer validated internal array identities and regenerated each frozen segment",
                "all archived input hashes and bound fields matched exactly"
            ],
            "not_checked": [
                "a second implementation of the Bernstein suprema or residual convolution",
                "independent mathematical validation of the producer's bound formulas",
                "independent reconstruction of the true continuous-segment bounds"
            ],
            "no_segment_236": True
        }
    }
    result_path = args.output_dir / "imported_segment_bound_replay.json"
    temp_path = result_path.with_suffix(".tmp")
    temp_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temp_path.replace(result_path)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
