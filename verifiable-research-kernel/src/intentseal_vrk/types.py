from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

CLAIM_CLASSES = {
    "CONJECTURE",
    "NUMERICAL_OBSERVATION",
    "REPRODUCED_RESULT",
    "EXHAUSTIVE_FINITE_RESULT",
    "INTERVAL_CERTIFIED_RESULT",
    "ANALYTIC_THEOREM",
}

REQUIRED_ROLES: dict[str, FrozenSet[str]] = {
    "CONJECTURE": frozenset(),
    "NUMERICAL_OBSERVATION": frozenset({"definition", "execution_record"}),
    "REPRODUCED_RESULT": frozenset({"definition", "execution_record", "independent_replication"}),
    "EXHAUSTIVE_FINITE_RESULT": frozenset({
        "definition", "passing_witness", "exclusion_certificate", "coverage_certificate"
    }),
    "INTERVAL_CERTIFIED_RESULT": frozenset({"definition", "interval_certificate", "verifier"}),
    "ANALYTIC_THEOREM": frozenset({"definition", "proof", "scope_statement"}),
}


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str
