#!/usr/bin/env python3
"""Verify Umbrella documentation files against registry.json single source of truth."""
import json
import sys
from pathlib import Path

def main() -> int:
    root = Path(__file__).resolve().parent.parent
    reg = json.loads((root / "registry.json").read_text(encoding="utf-8"))
    tokens = reg["required_tokens_in_docs"]
    doc_files = reg["doc_files"]
    errors = []
    for doc_rel in doc_files:
        p = root / doc_rel
        if not p.exists():
            errors.append(f"Missing doc file: {doc_rel}")
            continue
        text = p.read_text(encoding="utf-8")
        for tok in tokens:
            if tok not in text:
                errors.append(f"{doc_rel}: missing required token {tok!r}")
    for rel_key in ("v1_2_0_zenodo_v4", "v1_3_1_remediated"):
        rel_path = root / reg["shark_protocol_releases"][rel_key]["path"]
        if not rel_path.exists():
            errors.append(f"Missing protocol release directory: {rel_path}")
    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1
    print(f"OK: verified {len(doc_files)} umbrella markdown files and {len(tokens)} registry tokens.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
