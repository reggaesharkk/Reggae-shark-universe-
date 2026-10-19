#!/usr/bin/env python3
"""Reproducible conditioning audit of the first three M14 v0.28 segments.

The observed-segment arithmetic is bound to archived segment/checker hashes.
The repeated-worst-segment tail is deliberately labeled a scenario, not a
uniform bound or prediction for unseen segments.
"""
import hashlib
import json
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "results/wp19_v0_28/pilot_v2_36818369196"
S238 = ROOT / "results/wp19_v0_28/pilot_chained_238_36819581437"
S237 = ROOT / "results/wp19_v0_28/pilot_chained_237_36820757066"
FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
SOURCE_SHA = "e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31"
H = Decimal("0.0000125")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def check_segment(path, step):
    x = read_json(path)
    if (x.get("schema") != "wp19-v0.28-adjoint-segment-arb-v2" or
        x.get("status") != "CONTINUOUS_SEGMENT_ENCLOSURE_ONLY" or
        x.get("M") != 14 or x.get("step") != step or
        x.get("backward_order_index") != 239-step or
        x.get("forward_time_interval_rational") != [f"{step}/80000", f"{step+1}/80000"] or
        x.get("precision_bits") != 192 or x.get("frozen") != FROZEN or
        x.get("source_sha256") != SOURCE_SHA):
        raise ValueError(f"frozen provenance/segment check failed for step {step}")
    return x


def upper_recurrence(incoming, L, R):
    # Same 80-digit outward Decimal formula as the chain verifiers.
    with localcontext() as c:
        c.prec = 80
        c.rounding = ROUND_CEILING
        a = (L * H).exp().next_plus()
        add = ((a - 1) / L) * R if L else H * R
        amp = (a - 1) * incoming
        return a * incoming + ((a - 1) / L) * R if L else incoming + add, amp, add


def build():
    paths = {
        239: (V2 / "M14_segment_239.json", V2 / "verification.json"),
        238: (S238 / "M14_segment_238.json", S238 / "chain_verification.json"),
        237: (S237 / "M14_segment_237.json", S237 / "chain_verification.json"),
    }
    segs = {n: check_segment(p[0], n) for n, p in paths.items()}
    checks = {n: read_json(p[1]) for n, p in paths.items()}
    if checks[239].get("status") != "PASS LIMITED PILOT RECURRENCE CHECK":
        raise ValueError("step 239 check status mismatch")
    for n in (238, 237):
        if checks[n].get("status") != "PASS LIMITED CHAINED SEGMENT RECURRENCE CHECK":
            raise ValueError(f"step {n} chain status mismatch")
        prev = n + 1
        if checks[n].get("previous_segment_sha256") != sha(paths[prev][0]):
            raise ValueError(f"step {n} is not hash-chained to prior segment")
        if checks[n].get("previous_verification_sha256") != sha(paths[prev][1]):
            raise ValueError(f"step {n} is not hash-chained to prior check")
    for n in (239, 238, 237):
        if checks[n].get("segment_sha256") != sha(paths[n][0]):
            raise ValueError(f"step {n} check does not bind its segment")

    incoming = {
        239: Decimal(segs[239]["bounds"]["terminal_adjoint_error_upper"]),
        238: Decimal(checks[239]["backward_error_after_one_segment_upper"]),
        237: Decimal(checks[238]["backward_error_after_segment_upper"]),
    }
    rows = []
    for n in (239, 238, 237):
        b = {k: Decimal(v) for k, v in segs[n]["bounds"].items()}
        out, amp, add = upper_recurrence(incoming[n], b["logarithmic_norm_upper"], b["residual_L2_upper"])
        claimed_key = "backward_error_after_one_segment_upper" if n == 239 else "backward_error_after_segment_upper"
        claimed = Decimal(checks[n][claimed_key])
        if out != claimed:
            raise ValueError(f"step {n} recurrence reproduction disagrees with archived verifier")
        growth = out - incoming[n]
        rows.append({
            "step": n,
            "segment_sha256": sha(paths[n][0]),
            "incoming_error_upper": str(incoming[n]),
            "outgoing_error_upper": str(out),
            "logarithmic_norm_upper": str(b["logarithmic_norm_upper"]),
            "residual_L2_upper": str(b["residual_L2_upper"]),
            "nominal_residual_L2_upper": str(b["nominal_residual_L2_upper"]),
            "primal_uncertainty_penalty_upper": str(b["primal_uncertainty_residual_penalty_upper"]),
            "uncertainty_penalty_over_nominal": str(b["primal_uncertainty_residual_penalty_upper"] / b["nominal_residual_L2_upper"]),
            "growth_from_exponential_amplification": str(amp),
            "growth_from_additive_residual": str(add),
            "amplification_share_of_total_growth": str(amp / growth),
        })

    # Conditional sensitivity scenario only: repeat the largest observed L,R
    # pair for the 237 uncomputed steps. This is not assumed to hold in reality.
    maxL = max(Decimal(segs[n]["bounds"]["logarithmic_norm_upper"]) for n in segs)
    maxR = max(Decimal(segs[n]["bounds"]["residual_L2_upper"]) for n in segs)
    gradient_note = ROOT / "notes/WP19_v0_27_RESULT.md"
    gradient_note_text = gradient_note.read_text()
    gradient_literal = "4691959667101.255187"
    if gradient_literal not in gradient_note_text:
        raise ValueError("v0.27 N14->15 gradient reference missing or changed")
    terminal_grad = Decimal(gradient_literal)
    start = Decimal(checks[237]["backward_error_after_segment_upper"])
    x = start
    crossing = None
    with localcontext() as c:
        c.prec = 80
        c.rounding = ROUND_CEILING
        for j in range(1, 238):
            x, _, _ = upper_recurrence(x, maxL, maxR)
            if crossing is None and x >= terminal_grad:
                crossing = j

    return {
        "schema": "wp19-v0.28-route-conditioning-audit-v1",
        "status": "DIAGNOSTIC_ONLY_NO_ROUTE_FAILURE_THEOREM",
        "audit_source_sha256": sha(__file__),
        "frozen": FROZEN,
        "input_files_sha256": {
            str(paths[n][0].relative_to(ROOT)): sha(paths[n][0]) for n in (239, 238, 237)
        } | {
            str(paths[n][1].relative_to(ROOT)): sha(paths[n][1]) for n in (239, 238, 237)
        } | {str(gradient_note.relative_to(ROOT)): sha(gradient_note)},
        "observed_segments": rows,
        "conditional_repeated_worst_segment_scenario": {
            "remaining_step_count": 237,
            "assumption": "repeat the maximum L and residual upper observed among steps 239, 238, and 237 on every remaining segment",
            "assumption_status": "untested; not an a-priori bound and not a prediction",
            "maximum_observed_logarithmic_norm_upper": str(maxL),
            "maximum_observed_residual_L2_upper": str(maxR),
            "starting_error_upper": str(start),
            "v027_terminal_gradient_L2_upper_reference": str(terminal_grad),
            "first_repeated_step_exceeding_gradient_norm_reference": crossing,
            "error_after_237_repeated_steps": str(x),
            "ratio_to_gradient_norm_reference": str(x / terminal_grad),
            "interpretation": "conditioning stress scenario only; no comparison to signed-numerator margin because the norms have different units",
        },
        "route_diagnosis": {
            "observed_fact": "Across these three steps, about 99.4% of each scalar recurrence increase comes from exponential amplification of incoming adjoint error; additive residual contribution is below 1% of the increase.",
            "observed_fact_2": "The primal-uncertainty residual penalty is roughly 13,446 to 14,309 times the nominal residual L2 upper.",
            "next_gate": "Before more sequential segments, run a frozen one-segment comparison of a structured L2/tangent-space primal-uncertainty enclosure against the current componentwise/triangle bound. Preserve the current output and protocol as baseline; accept a sharper method only if its derivation is rigorous and independently checked.",
            "claim_boundary": "This audit does not prove the scalar recurrence will remain at these values, does not prove the adjoint route impossible, and does not establish any all-cutoff or continuum Navier-Stokes claim.",
        },
    }


if __name__ == "__main__":
    import sys
    result = build()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "results/wp19_v0_28/route_conditioning_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    tmp.replace(out)
    print(json.dumps(result, indent=2))
