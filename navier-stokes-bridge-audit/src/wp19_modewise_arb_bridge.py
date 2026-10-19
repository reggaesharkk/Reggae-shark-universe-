"""
WP19 v0.27 & v0.28 Exact 192-Bit Arb & 3D Cutoff Escalator Bridge
-----------------------------------------------------------------
Ingests exact Decimal bounds from:
1. WP19 v0.28 M14 Adjoint Segments (237, 238, 239)
2. WP19 v0.28 Structured Primal Uncertainty AB & Corrected Recurrence Chain
3. WP19 v0.27 3D Fourier-Galerkin Consecutive Cutoff Escalator (M14 -> M18)
"""

import json
from decimal import Decimal, getcontext
from pathlib import Path

# Set Decimal precision to 60 digits (exceeding 192-bit ~ 58 decimal digits)
getcontext().prec = 60

REPO_ROOT = Path(__file__).resolve().parent.parent
WP19_V28 = REPO_ROOT / "results" / "wp19_v0_28"
WP19_V27 = REPO_ROOT / "results" / "wp19_bridge" / "wp19_v0_27"

def run_exact_wp19_audit():
    print("=" * 78)
    print("1. WP19 v0.28 192-BIT ARB SEGMENT & PRIMAL ENCLOSURE AUDIT (M=14)")
    print("=" * 78)

    seg_paths = [
        WP19_V28 / "pilot_chained_237_36820757066" / "M14_segment_237.json",
        WP19_V28 / "pilot_chained_238_36819581437" / "M14_segment_238.json",
        WP19_V28 / "pilot_v2_36818369196" / "M14_segment_239.json",
    ]

    for sp in seg_paths:
        if not sp.exists():
            continue
        data = json.loads(sp.read_text(encoding="utf-8"))
        b = data["bounds"]
        step = data.get("step")
        interval = data.get("forward_time_interval_rational")
        true_primal = Decimal(str(b["true_primal_radius_upper"]))
        pred_dist = Decimal(str(b["binary_decimal_predictor_distance_upper"]))
        nom_res = Decimal(str(b["nominal_residual_L2_upper"]))
        log_norm = Decimal(str(b["logarithmic_norm_upper"]))

        primal_certified = true_primal < Decimal("1e-4")
        print(f"Segment {step} ({interval[0]} -> {interval[1]}) [{data['status']}]")
        print(f"  -> True Primal Radius Upper      : {true_primal:.15e} ({'CERTIFIED < 1e-4' if primal_certified else 'CHECK'})")
        print(f"  -> Predictor Distance Upper      : {pred_dist:.15e}")
        print(f"  -> Nominal Residual L2 Upper     : {nom_res:.6f}")
        print(f"  -> Logarithmic Norm Upper (L)    : {log_norm:.10f}")
        print("-" * 78)

    print("\n" + "=" * 78)
    print("2. WP19 v0.28 STRUCTURED FOURIER-YOUNG TIGHTENING & RECURRENCE CHAIN")
    print("=" * 78)
    ab_path = WP19_V28 / "structured_uncertainty_ab_20261001" / "structured_uncertainty_ab.json"
    if ab_path.exists():
        ab = json.loads(ab_path.read_text(encoding="utf-8"))
        ratio = Decimal(str(ab["new_over_old_penalty_upper"]))
        thresh = Decimal(str(ab["predeclared_materiality_threshold_new_over_old"]))
        modes = ab["mode_counts"]
        print(f"Mode Split     : Low M14 = {modes['low_M14']} modes | High M15 = {modes['high_M15']} modes")
        print(f"Old Penalty    : {Decimal(str(ab['old_componentwise_triangle_penalty_upper'])):.6f}")
        print(f"New FY Penalty : {Decimal(str(ab['structured_fourier_young_penalty_upper'])):.6f}")
        print(f"Tightening     : {ratio:.12f} <= {thresh} Threshold [{ab['status']}]")

    chain_path = WP19_V28 / "corrected_chain_20261001" / "corrected_recurrence_chain.json"
    if chain_path.exists():
        ch = json.loads(chain_path.read_text(encoding="utf-8"))
        spec = ch["spectral_support_check"]
        print(f"Spectral Ball  : {spec['support']} (max |k|^2 = {spec['max_k_squared']}, nu*|k|^2 = {spec['reverse_diffusion_growth_bound']})")
        print(f"Chain Status   : {ch['status']}")

    print("\n" + "=" * 78)
    print("3. WP19 v0.27 3D FOURIER-GALERKIN CUTOFF ESCALATOR (M14 -> M18)")
    print("=" * 78)
    for trans_file in sorted(WP19_V27.glob("M*_to_M*.json")):
        t_data = json.loads(trans_file.read_text(encoding="utf-8"))
        trans = t_data.get("transition")
        obj_hi = Decimal(str(t_data["objective"]["arb_upper_decimal"]))
        grad_hi = Decimal(str(t_data["terminal_gradient"]["L2_upper_decimal"]))
        dir_lo = Decimal(str(t_data["actual_cutoff_direction"]["arb_linear_prediction_lower_decimal"]))
        width = Decimal(str(t_data["actual_cutoff_direction"]["arb_interval_width_decimal"]))
        signed_pass = obj_hi < Decimal("0")
        print(f"Transition {trans:<8} | Status: {t_data['status']}")
        print(f"  -> Signed C500 Objective Upper : {obj_hi:.7f} ({'STRICTLY NEGATIVE' if signed_pass else 'UNSIGNED'})")
        print(f"  -> Cutoff Direction Pred Lower : {dir_lo:.6f} (Arb Width: {width})")
        print(f"  -> Terminal Gradient L2 Upper  : {grad_hi:.6f}")
        print("-" * 78)

if __name__ == "__main__":
    run_exact_wp19_audit()
