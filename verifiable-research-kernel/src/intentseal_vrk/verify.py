from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from .canonical import digest_object, sha256_file
from .plugins import PLUGINS
from .types import CLAIM_CLASSES, REQUIRED_ROLES, Check


class VerificationError(ValueError):
    pass


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise VerificationError(msg)


def validate_claim_shape(claim: dict[str, Any]) -> None:
    for key in ("schema", "claim_id", "claim_text", "claim_class", "scope", "evidence", "dependencies"):
        _require(key in claim, f"missing required field: {key}")
    _require(claim["schema"] == "intentseal-vrk-claim-v1", "schema mismatch")
    _require(isinstance(claim["claim_id"], str) and claim["claim_id"], "claim_id must be nonempty")
    _require(isinstance(claim["claim_text"], str) and claim["claim_text"], "claim_text must be nonempty")
    _require(claim["claim_class"] in CLAIM_CLASSES, f"unknown claim_class: {claim['claim_class']}")
    _require(isinstance(claim["scope"], dict), "scope must be object")
    _require(isinstance(claim["evidence"], list), "evidence must be array")
    _require(isinstance(claim["dependencies"], list), "dependencies must be array")


def verify_claim(claim_path: str | Path) -> dict[str, Any]:
    claim_path = Path(claim_path).resolve()
    root = claim_path.parent
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    validate_claim_shape(claim)

    checks: list[Check] = []
    roles_present: set[str] = set()
    all_artifacts_bound = True
    all_plugins_pass = True

    for i, ev in enumerate(claim["evidence"]):
        role = ev.get("role")
        if not role:
            checks.append(Check(f"evidence[{i}].role", False, "missing role"))
            all_artifacts_bound = False
            continue
        roles_present.add(role)
        rel = ev.get("path")
        expected_sha = ev.get("sha256")
        if rel:
            p = (root / rel).resolve()
            try:
                p.relative_to(root)
            except ValueError:
                checks.append(Check(f"{role}.path", False, "path escapes claim directory"))
                all_artifacts_bound = False
                continue
            if not p.exists() or not p.is_file():
                checks.append(Check(f"{role}.artifact", False, f"missing file {rel}"))
                all_artifacts_bound = False
                continue
            actual = sha256_file(p)
            ok = isinstance(expected_sha, str) and actual == expected_sha
            checks.append(Check(f"{role}.sha256", ok, f"actual={actual}"))
            all_artifacts_bound &= ok
            plugin_name = ev.get("plugin")
            if plugin_name:
                plugin = PLUGINS.get(plugin_name)
                if not plugin:
                    checks.append(Check(f"{role}.plugin", False, f"unknown plugin {plugin_name}"))
                    all_plugins_pass = False
                else:
                    ok2, detail = plugin(p, ev.get("plugin_args", {}))
                    checks.append(Check(f"{role}.plugin:{plugin_name}", ok2, detail))
                    all_plugins_pass &= ok2
        else:
            ext = ev.get("external")
            ok = isinstance(ext, dict) and all(ext.get(k) for k in ("repository", "commit", "path", "git_blob_sha"))
            checks.append(Check(f"{role}.external_binding", ok, "immutable repository binding" if ok else "incomplete external binding"))
            all_artifacts_bound &= ok

    required = REQUIRED_ROLES[claim["claim_class"]]
    missing_roles = sorted(required - roles_present)
    checks.append(Check("required_evidence_roles", not missing_roles, "complete" if not missing_roles else f"missing {missing_roles}"))

    if claim["claim_class"] != "CONJECTURE":
        applies = claim["scope"].get("applies_to")
        excludes = claim["scope"].get("does_not_imply")
        scope_ok = isinstance(applies, list) and bool(applies) and isinstance(excludes, list) and bool(excludes)
        checks.append(Check("scope_boundary", scope_ok, "explicit applies_to + does_not_imply" if scope_ok else "scope boundary incomplete"))
    else:
        scope_ok = True

    dep_ok = all(isinstance(d, dict) and d.get("claim_id") and d.get("relation") for d in claim["dependencies"])
    checks.append(Check("dependencies", dep_ok, f"{len(claim['dependencies'])} dependency records"))

    has_external_only_required = any(ev.get("role") in required and not ev.get("path") for ev in claim["evidence"])

    if missing_roles or not scope_ok or not dep_ok or not all_artifacts_bound or not all_plugins_pass:
        kernel_status = "UNVERIFIED"
    elif has_external_only_required:
        kernel_status = "EVIDENCE_BOUND"
    else:
        kernel_status = "CERTIFIED"

    claim_for_digest = copy.deepcopy(claim)
    claimed_digest = claim_for_digest.pop("claim_digest", None)
    computed_digest = digest_object(claim_for_digest)
    digest_ok = claimed_digest in (None, computed_digest)
    checks.append(Check("claim_digest", digest_ok, f"computed={computed_digest}"))
    if not digest_ok:
        kernel_status = "UNVERIFIED"

    return {
        "schema": "intentseal-vrk-verification-v1",
        "claim_id": claim["claim_id"],
        "claim_class": claim["claim_class"],
        "kernel_status": kernel_status,
        "claim_digest": computed_digest,
        "checks": [c.__dict__ for c in checks],
        "pass": kernel_status in {"CERTIFIED", "EVIDENCE_BOUND"},
    }
