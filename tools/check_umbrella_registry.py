#!/usr/bin/env python3
"""Verify Umbrella documentation files and mirrored Program 10 tree against registry.json."""
import hashlib
import json
import re
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

    # Verify OSF and Zenodo DOI sets in RESEARCHER_AND_ARCHIVE_INDEX_2026_10_25.md
    idx_text = (root / "RESEARCHER_AND_ARCHIVE_INDEX_2026_10_25.md").read_text(encoding="utf-8")
    found_osf = sorted(set(re.findall(r"10\.17605/OSF\.IO/[A-Z0-9]+", idx_text)))
    found_zenodo = sorted(set(re.findall(r"10\.5281/zenodo\.\d+", idx_text)))
    expected_osf = sorted(set(reg["osf_dois"]))
    expected_zenodo = sorted(set(reg["zenodo_dois"]))

    if found_osf != expected_osf:
        errors.append(f"OSF DOI mismatch: found {len(found_osf)} vs expected {len(expected_osf)}")
    if found_zenodo != expected_zenodo:
        errors.append(f"Zenodo DOI mismatch: found {len(found_zenodo)} vs expected {len(expected_zenodo)}")

    sp = reg["shark_protocol"]
    rel_dir = root / sp["path"]
    if not rel_dir.exists():
        errors.append(f"Missing mirrored protocol release directory: {rel_dir}")
    else:
        pyc_files = list(rel_dir.rglob("*.pyc"))
        if pyc_files:
            errors.append(f"Found stray .pyc files in {rel_dir}: {pyc_files}")
        all_sp_files = [p for p in rel_dir.rglob("*") if p.is_file()]
        if len(all_sp_files) != sp["tracked_files"]:
            errors.append(
                f"Expected {sp['tracked_files']} files in {sp['path']}, found {len(all_sp_files)}"
            )

    spec_pdf = root / sp["spec_pdf_path"]
    if not spec_pdf.exists():
        errors.append(f"Missing mirrored specification PDF: {spec_pdf}")
    else:
        pdf_bytes = spec_pdf.read_bytes()
        pdf_sha = hashlib.sha256(pdf_bytes).hexdigest()
        if pdf_sha != sp["spec_pdf_sha256"]:
            errors.append(f"Specification PDF SHA-256 mismatch: {pdf_sha} != {sp['spec_pdf_sha256']}")
        if len(pdf_bytes) != sp["spec_pdf_bytes"]:
            errors.append(f"Specification PDF size mismatch: {len(pdf_bytes)} != {sp['spec_pdf_bytes']}")
        in_repo_pdf = rel_dir / "paper" / "specification.pdf"
        if in_repo_pdf.exists() and in_repo_pdf.read_bytes() != pdf_bytes:
            errors.append("docs/research PDF does not match protocols/shark_protocol_v1_3_2/paper/specification.pdf")

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1

    print(
        f"OK: verified {len(doc_files)} umbrella markdown files, "
        f"{len(expected_osf)} OSF DOIs, {len(expected_zenodo)} Zenodo DOIs, "
        f"and {sp['tracked_files']} mirrored files in {sp['path']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
