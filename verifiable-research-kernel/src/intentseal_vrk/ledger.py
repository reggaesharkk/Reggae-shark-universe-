from __future__ import annotations

import json
from pathlib import Path

from .canonical import canonical_json_bytes, sha256_bytes

GENESIS = "0" * 64


def append_event(path: str | Path, event: dict) -> dict:
    p = Path(path)
    prev = GENESIS
    seq = 1
    if p.exists():
        lines = [line for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            last = json.loads(lines[-1])
            prev = last["event_hash"]
            seq = int(last["seq"]) + 1
    body = {"seq": seq, "prev_hash": prev, "event": event}
    event_hash = sha256_bytes(canonical_json_bytes(body))
    row = {**body, "event_hash": event_hash}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    return row


def verify_ledger(path: str | Path) -> tuple[bool, str]:
    p = Path(path)
    prev = GENESIS
    expected_seq = 1
    if not p.exists():
        return True, "empty ledger"
    for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            if row["seq"] != expected_seq:
                return False, f"line {line_no}: seq mismatch"
            if row["prev_hash"] != prev:
                return False, f"line {line_no}: prev_hash mismatch"
            body = {"seq": row["seq"], "prev_hash": row["prev_hash"], "event": row["event"]}
            actual = sha256_bytes(canonical_json_bytes(body))
            if actual != row["event_hash"]:
                return False, f"line {line_no}: event_hash mismatch"
            prev = row["event_hash"]
            expected_seq += 1
        except Exception as e:
            return False, f"line {line_no}: {e}"
    return True, f"{expected_seq-1} events; head={prev}"
