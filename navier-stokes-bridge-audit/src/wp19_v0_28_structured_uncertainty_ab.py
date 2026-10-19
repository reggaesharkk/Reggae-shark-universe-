#!/usr/bin/env python3
"""Frozen one-segment A/B audit of the v0.28 primal-uncertainty residual bound.

This does not recompute the adjoint residual. It compares the archived
componentwise/triangle uncertainty penalty with a structured Fourier L2
Young bound for the same M14 segment 237, frozen primal radius, and Hermite
adjoint polynomial. All input binary64 values are imported as exact dyadics;
Arb encloses every norm and arithmetic operation.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx
import wp19_v0_28_adjoint_segment_arb as base
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

ctx.prec = 192
M, STEP = 14, 237
SEGMENT_SHA = "c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc"
REPORT_SHA = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
VALUES_SHA = "00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
RHS_SHA = "8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
PREVIOUS_VERIFICATION_SHA = "c611b9eb2c5770d1880e64fdc7e0fc9f5136aef2f71b8b9afc4e1f533d09596c"
CURRENT_VERIFICATION_SHA = "cbfb935af79cd7bb359c5688831c4a7329b70011ee9e6c1934442147a836f77f"
FROZEN = {
    "witness_sha256": "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
    "K36_sha256": "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
    "K36_sign_chart_sha256": "de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
    "C500_portable_semantic_sha256": "1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}
PREDECLARED_MAX_RATIO = arb("0.5")  # require at least a 2x reduction to call it material

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def direct_vjp(s,u,lam):
    """Independent explicit Fourier convolution for the bilinear VJP."""
    out=[[acb(0) for _ in range(3)] for _ in s.modes]
    for ki,k0 in enumerate(s.modes):
        k=tuple(int(x) for x in k0)
        for pi,p0 in enumerate(s.modes):
            p=tuple(int(x) for x in p0)
            q=tuple(k[t]-p[t] for t in range(3))
            qi=s.index.get(q)
            if qi is None: continue
            dot=sum((lam[pi][j]*u[qi][j] for j in range(3)),acb(0))
            adv=sum((u[pi][j]*q[j] for j in range(3)),acb(0))
            for j in range(3): out[ki][j]+=acb(0,1)*(q[j]*dot-adv*lam[qi][j])
        kk=int(s.square[ki])
        if kk:
            kd=sum((out[ki][j]*k[j] for j in range(3)),acb(0))
            out[ki]=[out[ki][j]-kd*k[j]/kk for j in range(3)]
        else: out[ki]=[acb(0)]*3
    return out

def direct_convolution_self_check():
    s=DealiasedSystem(2,nu=.1); rng=np.random.default_rng(20261001)
    u=base.projected_rows(s,rng.integers(-4,5,(len(s.modes),3))+1j*rng.integers(-4,5,(len(s.modes),3)))
    lam=base.projected_rows(s,rng.integers(-4,5,(len(s.modes),3))+1j*rng.integers(-4,5,(len(s.modes),3)))
    zero=[[acb(0) for _ in range(3)] for _ in s.modes]
    packed=base.packed_vjp(s,[u,zero,zero,zero],[lam,zero,zero,zero])[0]
    direct=direct_vjp(s,u,lam)
    for i in range(len(s.modes)):
        for j in range(3):
            if not (packed[i][j]-direct[i][j]).contains(0):
                raise ValueError(("packed/direct VJP disagreement",i,j,str(packed[i][j]-direct[i][j])))
    eps=base.norm(u); l1=sum((base.norm([row]) for row in lam),arb(0))
    gl2=arb(0)
    for k,ksq,row in zip(s.modes,s.square,lam):
        gl2+=int(ksq)*base.norm([row])**2
    young=(2*l1+arb(len(s.modes)).sqrt()*gl2.sqrt()).upper()*eps
    if not base.norm(direct)<=young: raise ValueError("explicit Fourier VJP exceeds L2 Young bound")
    return {"status":"PASS","direct_vjp_identity":"PASS Arb interval overlap coefficientwise",
            "young_bound_dominates_direct_vjp":"PASS","actual_L2_upper":base.safe_decimal_upper(base.norm(direct),18),
            "young_L2_upper":base.safe_decimal_upper(young,18)}

def recurrence_upper(incoming,L,R):
    """Outward Decimal one-step Gronwall recurrence, independent of Arb path."""
    with localcontext() as c:
        c.prec=80; c.rounding=ROUND_CEILING
        h=Decimal("0.0000125")
        a=(L*h).exp().next_plus()
        return a*incoming+((a-1)/L)*R

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-check",action="store_true")
    ap.add_argument("--adjoint-dir",type=Path)
    ap.add_argument("--segment",type=Path)
    ap.add_argument("--previous-verification",type=Path)
    ap.add_argument("--current-verification",type=Path)
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    if a.self_check:
        print(json.dumps(direct_convolution_self_check(),indent=2),flush=True); return
    if any(x is None for x in (a.adjoint_dir,a.segment,a.previous_verification,a.current_verification,a.output)):
        ap.error("A/B run requires --adjoint-dir, --segment, both recurrence verifiers, and --output")
    seg=json.loads(a.segment.read_text())
    if sha(a.segment)!=SEGMENT_SHA: raise ValueError("segment 237 baseline hash mismatch")
    if seg.get("schema")!="wp19-v0.28-adjoint-segment-arb-v2" or seg.get("step")!=STEP or seg.get("M")!=M or seg.get("frozen")!=FROZEN:
        raise ValueError("baseline segment identity mismatch")
    if seg.get("status")!="CONTINUOUS_SEGMENT_ENCLOSURE_ONLY": raise ValueError("baseline segment status mismatch")
    if sha(a.previous_verification)!=PREVIOUS_VERIFICATION_SHA or sha(a.current_verification)!=CURRENT_VERIFICATION_SHA:
        raise ValueError("chained recurrence verification hash mismatch")
    previous=json.loads(a.previous_verification.read_text()); current=json.loads(a.current_verification.read_text())
    if previous.get("status")!="PASS LIMITED CHAINED SEGMENT RECURRENCE CHECK" or previous.get("step")!=238 or current.get("step")!=237:
        raise ValueError("adjacent segment recurrence provenance mismatch")
    report=a.adjoint_dir/"M14_arb_vjp_point.json"
    if sha(report)!=REPORT_SHA: raise ValueError("frozen M14 adjoint report hash mismatch")
    rec=json.loads(report.read_text()).get("adjoint_reconstruction",{})
    values=a.adjoint_dir/rec.get("values_file","")
    rhs=a.adjoint_dir/rec.get("rhs_file","")
    if sha(values)!=VALUES_SHA or sha(rhs)!=RHS_SHA: raise ValueError("frozen M14 adjoint arrays hash mismatch")
    if rec.get("values_sha256")!=VALUES_SHA or rec.get("rhs_sha256")!=RHS_SHA: raise ValueError("report does not bind frozen adjoint arrays")

    high=DealiasedSystem(M+1,nu=.1)
    low=DealiasedSystem(M,nu=.1)
    adj=np.load(values,mmap_mode="r"); arhs=np.load(rhs,mmap_mode="r")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape: raise ValueError("adjoint path array shape mismatch")
    # Same exact-dyadic projection, Hermite interpolant and Bernstein controls as v0.28.
    rows=[base.projected_rows(high,x) for x in (adj[STEP],adj[STEP+1],arhs[STEP],arhs[STEP+1])]
    L=base.hermite(*rows,base.HALF_H)
    controls=base.bernstein(L)
    per=[]
    for b in controls:
        l1=arb(0); grad2=arb(0); l2=base.norm(b)
        for k,ksq,row in zip(high.modes,high.square,b):
            v=base.norm([row])
            l1+=v
            grad2+=arb(int(ksq))*(v**2)
        per.append({"L2_upper":l2.upper(),"L1_mode_upper":l1.upper(),"gradient_L2_upper":grad2.sqrt().upper()})
    eps=arb(seg["bounds"]["true_primal_radius_upper"])
    old_penalty_text=seg["bounds"]["primal_uncertainty_residual_penalty_upper"]
    old_penalty=arb(old_penalty_text)
    per_text=[{k:base.safe_decimal_upper(v,12) for k,v in x.items()} for x in per]
    l2sup=max(arb(x["L2_upper"]) for x in per_text)
    l1sup=max(arb(x["L1_mode_upper"]) for x in per_text)
    grad_sup=max(arb(x["gradient_L2_upper"]) for x in per_text)
    old_factor=(arb(sum(int(x) for x in low.square)).sqrt()+(M+1)*arb(len(low.modes)).sqrt())*l2sup
    # Bilinear VJP perturbation, after the norm-one Leray projection:
    # ||(grad e)^T L||_2 <= || |k|e ||_2 ||L||_1 <= M||e||_2||L||_1;
    # ||(e.grad)L||_2 <= ||e||_1 ||grad L||_2 <= sqrt(n)||e||_2||grad L||_2.
    new_factor=(M*l1sup+arb(len(low.modes)).sqrt()*grad_sup).upper()
    factor_text=base.safe_decimal_upper(new_factor,12)
    eps_text=base.safe_decimal_upper(eps,15)
    new_factor=arb(factor_text)
    eps=arb(eps_text)
    new_penalty=(eps*new_factor).upper()
    penalty_text=base.safe_decimal_upper(new_penalty,6)
    new_penalty=arb(penalty_text)
    ratio=(new_penalty/old_penalty).upper()
    status="MATERIAL_TIGHTENING" if ratio<=PREDECLARED_MAX_RATIO else "NO_MATERIAL_TIGHTENING"
    incoming=arb(previous["backward_error_after_segment_upper"])
    L=arb(seg["bounds"]["logarithmic_norm_upper"])
    nominal=arb(seg["bounds"]["nominal_residual_L2_upper"])
    incoming_d=Decimal(previous["backward_error_after_segment_upper"])
    L_text=base.safe_decimal_upper(L,9)
    nominal_text=base.safe_decimal_upper(nominal,6)
    L_d=Decimal(L_text)
    old_out=recurrence_upper(incoming_d,L_d,Decimal(seg["bounds"]["residual_L2_upper"]))
    new_out=recurrence_upper(incoming_d,L_d,Decimal(nominal_text)+Decimal(penalty_text))
    if new_out>old_out: raise ValueError("structured residual did not improve the outward recurrence")
    old_archived=Decimal(current["backward_error_after_segment_upper"])
    if old_out<old_archived: raise ValueError("recomputed old recurrence undercuts archived outward value")
    direct_check=direct_convolution_self_check()
    out={
      "schema":"wp19-v0.28-structured-primal-uncertainty-ab-v1",
      "status":status,"M":M,"step":STEP,"interval_rational":["237/80000","238/80000"],
      "precision_bits":ctx.prec,"baseline_segment_sha256":sha(a.segment),
      "adjoint_report_sha256":sha(report),"adjoint_values_sha256":sha(values),"adjoint_rhs_sha256":sha(rhs),
      "frozen":FROZEN,"predeclared_materiality_threshold_new_over_old":"0.5",
      "primal_L2_radius_upper":eps_text,
      "old_componentwise_triangle_penalty_upper":old_penalty_text,
      "old_formula_recomputed_factor_upper":base.safe_decimal_upper(old_factor,12),
      "structured_fourier_young_factor_upper":factor_text,
      "structured_fourier_young_penalty_upper":penalty_text,
      "new_over_old_penalty_upper":base.safe_decimal_upper(ratio,12),
      "incoming_adjoint_error_upper":previous["backward_error_after_segment_upper"],
      "nominal_residual_upper":nominal_text,
      "logarithmic_norm_upper":L_text,
      "outward_recurrence":{"step_width":"1/80000",
        "old_recomputed_outgoing_upper":str(old_out),
        "old_archived_outgoing_upper":current["backward_error_after_segment_upper"],
        "new_structured_outgoing_upper":str(new_out),
        "comparison":"new <= old recomputed; old recomputed >= archived verifier value"},
      "independent_direct_convolution_self_check":direct_check,
      "bernstein_control_upper_norms":per_text,
      "mode_counts":{"low_M14":len(low.modes),"high_M15":len(high.modes)},
      "method":"For each time Bernstein control, compute Arb bounds on sum_k |L_k|, |||k|L_k||_2, and ||L||_2. Apply discrete Young inequalities to the bilinear VJP perturbation and the norm-one Leray projection. The global primal error enters only through its frozen L2 radius; divergence-free/reality fields are included as a subset of the ambient L2 ball.",
      "claim_boundary":"One same-segment uncertainty-bound comparison only. It does not recompute the nominal residual or certify the remaining adjoint path, dual quadrature, normalizer, transfer inequality, or any continuum Navier-Stokes claim."
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    tmp=a.output.with_suffix(".tmp"); tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); tmp.replace(a.output)
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__": main()
