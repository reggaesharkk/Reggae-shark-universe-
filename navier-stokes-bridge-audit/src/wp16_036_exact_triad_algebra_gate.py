"""Exact algebra gate for the persistent [223]+[123]->[036] triad motif.

Representative:
    p = (-3,-2,-2)
    q = (-3,-1, 2)
    k = (-6,-3, 0) = p + q

This script:
1. verifies the exact integer geometry;
2. constructs the Leray projector P_k exactly with fractions;
3. records the exact H2 coefficient prefactor |k|^4 = 2025;
4. verifies that the uploaded symmetry-result structure (if supplied) has
   48 exact triads, one signed-permutation class, and the same canonical
   representative at N9, N10, and N11.

Finite algebraic certificate only.
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path

P = (-3, -2, -2)
Q = (-3, -1, 2)
K = (-6, -3, 0)
CANONICAL_FLAT = P + Q + K


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def leray_projector_exact(k):
    k2 = dot(k, k)
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            delta = Fraction(1, 1) if i == j else Fraction(0, 1)
            row.append(delta - Fraction(k[i]*k[j], k2))
        out.append(row)
    return out


def frac_matrix_to_strings(M):
    return [[str(x) for x in row] for row in M]


def verify_symmetry_result(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected_steps = ["N9_from_N8", "N10_from_N9", "N11_from_N10"]
    checks = {}
    for step in expected_steps:
        s = payload["steps"][step]
        cls = s["classes"]
        checks[step] = {
            "exact_triad_count": int(s["exact_triad_count"]),
            "symmetry_class_count": int(s["symmetry_class_count"]),
            "canonical_flat": list(cls[0]["canonical_flat"]) if cls else None,
            "passes": (
                int(s["exact_triad_count"]) == 48
                and int(s["symmetry_class_count"]) == 1
                and tuple(cls[0]["canonical_flat"]) == CANONICAL_FLAT
            ),
            "delta_N": float(s["total"]["delta_N"]),
            "chi_before": float(s["total"]["chi_before"]),
            "chi_after": float(s["total"]["chi_after"]),
        }
    return checks


def run(symmetry_result=None):
    p2, q2, k2 = dot(P, P), dot(Q, Q), dot(K, K)
    projector = leray_projector_exact(K)

    result = {
        "status": "exact persistent triad algebra certificate",
        "representative": {"p": list(P), "q": list(Q), "k": list(K)},
        "integer_identities": {
            "p_plus_q_equals_k": add(P, Q) == K,
            "p_norm_sq": p2,
            "q_norm_sq": q2,
            "k_norm_sq": k2,
            "p_dot_q": dot(P, Q),
            "p_dot_k": dot(P, K),
            "q_dot_k": dot(Q, K),
            "p_cross_q": list(cross(P, Q)),
        },
        "leray_projector_Pk_exact": frac_matrix_to_strings(projector),
        "H2_weight_prefactor_abs_k_fourth": k2*k2,
        "coefficient_reduction": (
            "For divergence-free a_k and p·a_p=0 with q=k-p, "
            "z0 = -|k|^4 i (q·a_p)(conj(a_k)·P_k a_q) "
            "= -2025 i (k·a_p)(conj(a_k)·a_q)."
        ),
        "scope": (
            "Exact algebra for one finite Fourier triad geometry. "
            "No cutoff-uniform or regularity theorem is implied."
        ),
    }

    if symmetry_result is not None:
        checks = verify_symmetry_result(symmetry_result)
        result["symmetry_result_checks"] = checks
        result["all_three_steps_pass"] = all(x["passes"] for x in checks.values())

    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--symmetry-result", type=Path)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    result = run(a.symmetry_result)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
