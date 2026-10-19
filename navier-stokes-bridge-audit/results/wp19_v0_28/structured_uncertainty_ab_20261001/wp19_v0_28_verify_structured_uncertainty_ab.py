#!/usr/bin/env python3
"""Independent fail-closed Decimal/provenance check for the v0.28 A/B JSON."""
import argparse, hashlib, json
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path

SEGMENT_SHA="c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc"
PREVIOUS_SHA="c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c"
CURRENT_SHA="cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f"
VALUES_SHA="00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
RHS_SHA="8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
REPORT_SHA="981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
FROZEN={"witness_sha256":"4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
"K36_sha256":"7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
"K36_sign_chart_sha256":"de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
"C500_portable_semantic_sha256":"1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def D(x): return Decimal(str(x))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("result",type=Path); ap.add_argument("segment",type=Path)
    ap.add_argument("previous",type=Path); ap.add_argument("current",type=Path)
    a=ap.parse_args(); x=json.loads(a.result.read_text())
    assert x["schema"]=="wp19-v0.28-structured-primal-uncertainty-ab-v1"
    assert x["status"]=="MATERIAL_TIGHTENING" and x["M"]==14 and x["step"]==237
    assert x["baseline_segment_sha256"]==SEGMENT_SHA and sha(a.segment)==SEGMENT_SHA
    assert sha(a.previous)==PREVIOUS_SHA and sha(a.current)==CURRENT_SHA
    assert x["frozen"]==FROZEN and x["adjoint_report_sha256"]==REPORT_SHA
    assert x["adjoint_values_sha256"]==VALUES_SHA and x["adjoint_rhs_sha256"]==RHS_SHA
    assert x["independent_direct_convolution_self_check"]["status"]=="PASS"
    assert x["independent_direct_convolution_self_check"]["young_bound_dominates_direct_vjp"]=="PASS"
    segment=json.loads(a.segment.read_text()); prev=json.loads(a.previous.read_text()); cur=json.loads(a.current.read_text())
    assert segment["bounds"]["true_primal_radius_upper"]=="0.000055664765007"
    assert x["predeclared_materiality_threshold_new_over_old"]=="0.5"
    assert len(x["bernstein_control_upper_norms"])==4
    with localcontext() as c:
        c.prec=80; c.rounding=ROUND_CEILING
        controls=x["bernstein_control_upper_norms"]
        l1=max(D(z["L1_mode_upper"]) for z in controls)
        gl=max(D(z["gradient_L2_upper"]) for z in controls)
        root_n=D(x["mode_counts"]["low_M14"]).sqrt().next_plus()
        factor=(D(14)*l1+root_n*gl).next_plus()
        assert D(x["structured_fourier_young_factor_upper"])>=factor
        pen=(D(x["primal_L2_radius_upper"])*D(x["structured_fourier_young_factor_upper"])).next_plus()
        assert D(x["structured_fourier_young_penalty_upper"])>=pen
        ratio=(D(x["structured_fourier_young_penalty_upper"])/D(x["old_componentwise_triangle_penalty_upper"])).next_plus()
        assert D(x["new_over_old_penalty_upper"])>=ratio and ratio<=D("0.5")
        h=D(1)/D(80000); incoming=D(prev["backward_error_after_segment_upper"])
        L=D(x["logarithmic_norm_upper"]); amp=(L*h).exp().next_plus()
        old=amp*incoming+((amp-1)/L)*D(segment["bounds"]["residual_L2_upper"])
        new=amp*incoming+((amp-1)/L)*(D(x["nominal_residual_upper"])+D(x["structured_fourier_young_penalty_upper"]))
        rec=x["outward_recurrence"]
        assert D(rec["old_recomputed_outgoing_upper"])>=old
        assert D(rec["old_recomputed_outgoing_upper"])>=D(rec["old_archived_outgoing_upper"])
        assert D(rec["new_structured_outgoing_upper"])>=new
        assert D(rec["new_structured_outgoing_upper"])<=D(rec["old_recomputed_outgoing_upper"])
    print("PASS: frozen hashes, structured Young bound serialization, 2x tightening gate, explicit direct-convolution self-check, and independent outward Decimal recurrence")

if __name__=="__main__": main()
