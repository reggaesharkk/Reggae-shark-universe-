from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Callable

Plugin = Callable[[Path, dict], tuple[bool, str]]


def verify_text_status(path: Path, spec: dict) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    required = spec.get("required_strings", [])
    missing = [s for s in required if s not in text]
    if missing:
        return False, f"missing required strings: {missing}"
    forbidden = spec.get("forbidden_strings", [])
    present = [s for s in forbidden if s in text]
    if present:
        return False, f"forbidden strings present: {present}"
    return True, f"matched {len(required)} required strings"


def verify_lrsc_coverage_log(path: Path, spec: dict) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    k = int(spec["K"])
    n = int(spec.get("N", 50))
    expected = math.comb(n, k)
    m = re.search(rf"K={k} covered=(\d+) expected=(\d+)", text)
    if not m:
        return False, "coverage line missing"
    covered, logged_expected = map(int, m.groups())
    if logged_expected != expected:
        return False, f"logged expected {logged_expected} != comb({n},{k}) {expected}"
    if covered != expected:
        return False, f"covered {covered} != expected {expected}"
    if "STATUS=PROVED_NO_PASS_AT_K" not in text:
        return False, "proof status marker missing"
    if re.search(rf"K={k} .*capped=[1-9]", text):
        return False, "search was capped"
    if re.search(rf"K={k} .*unresolved=[1-9]", text):
        return False, "search has unresolved branches"
    return True, f"exact combinatorial coverage {covered}/{expected}; no passing subset at K={k}"


def verify_lrsc_witness_summary(path: Path, spec: dict) -> tuple[bool, str]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    upper_r2 = int(obj["residual_r2_interval_scaled_1e35"][1])
    c_lower = int(obj["target_norm2_lower_scaled_1e35"])
    tolerance = float(obj["relative_tolerance"])
    scale = int(round(1.0 / (tolerance * tolerance)))
    ok = upper_r2 * scale < c_lower
    if not ok:
        return False, f"witness fails integer gate: {upper_r2}*{scale} >= {c_lower}"
    subset = obj["subset"]
    if len(subset) != int(spec.get("K", len(subset))):
        return False, "witness cardinality mismatch"
    return True, f"witness passes: R^2/c < {tolerance**2:g}; |S|={len(subset)}"


PLUGINS: dict[str, Plugin] = {
    "text_status": verify_text_status,
    "lrsc_coverage_log": verify_lrsc_coverage_log,
    "lrsc_witness_summary": verify_lrsc_witness_summary,
}
