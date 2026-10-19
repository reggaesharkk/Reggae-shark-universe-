#!/usr/bin/env python3
"""WP19 v0.27a -- Arb terminal-gradient arithmetic certificate.

This subcertificate targets the fixed signed-C500 numerator introduced in
WP19 v0.26.  At each lower cutoff M=14,15,16,17 it encloses, with Arb
arithmetic, the gradient of the fixed P11 polynomial at the *nominal projected
binary64 endpoint* used by v0.26.

It is intentionally narrower than a full interval adjoint theorem:
  * the endpoint state itself is a fixed decimal image of the saved predictor;
  * the polynomial value and every gradient component are evaluated in Arb;
  * the analytic gradient is projected onto the divergence-free/reality
    tangent space exactly as in v0.23/v0.26;
  * the result is cross-checked against the independent PyTorch gradient and
    the v0.26 endpoint directional linear prediction.

State-uncertainty/Hessian propagation and backward-adjoint validation are
separate later gates.  No all-N or continuum claim is made here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from flint import acb, arb, ctx

P=(3,2,2)
Q=(3,-2,1)
K=(6,0,3)
NU=0.1
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"
EXPECTED_SELECTED_PAIRS=1048
EXPECTED_SELECTED_MODES=1159


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ball(z):
    return acb(str(float(np.real(z))),str(float(np.imag(z))))


def zero3():
    return [acb(0),acb(0),acb(0)]


def add3(a,b):
    return [a[j]+b[j] for j in range(3)]


def scale3(a,c):
    return [c*a[j] for j in range(3)]


def vdot(a,b):
    return sum((a[j].conjugate()*b[j] for j in range(3)),acb(0))


def project(k,v):
    kk=sum(int(x)*int(x) for x in k)
    kd=sum((v[j]*int(k[j]) for j in range(3)),acb(0))
    return [v[j]-kd*arb(int(k[j]))/kk for j in range(3)]


def point_state(arr):
    return [[ball(z) for z in row] for row in np.asarray(arr)]


def tangent_project(system,g):
    """Arb version of v0.23 tangent_project."""
    gp=[zero3() for _ in system.modes]
    for ix,k in enumerate(system.modes):
        kk=int(system.square[ix])
        kd=sum((g[ix][j]*int(k[j]) for j in range(3)),acb(0))
        gp[ix]=[g[ix][j]-kd*arb(int(k[j]))/kk for j in range(3)]
    out=[zero3() for _ in system.modes]
    for ix,k in enumerate(system.modes):
        negk=tuple(-int(v) for v in k)
        if tuple(k)<=negk:
            continue
        ni=int(system.neg[ix])
        geff=[(gp[ix][j]+gp[ni][j].conjugate())/2 for j in range(3)]
        out[ix]=geff
        out[ni]=[z.conjugate() for z in geff]
    return out


def l2_upper(rows):
    s=arb(0)
    for row in rows:
        for z in row:
            u=z.abs_upper()
            s+=u*u
    return s.sqrt().upper()


def l2_lower(rows):
    s=arb(0)
    for row in rows:
        for z in row:
            lo=z.abs_lower()
            s+=lo*lo
    return s.sqrt().lower()


def analytic_gradient(system,a,coeff):
    """Return Arb J and tangent gradient of the fixed degree-7 polynomial."""
    pi,qi,ki=(system.index[x] for x in (P,Q,K))
    W=int(system.square[ki]**2)
    qi_dot=sum((a[pi][j]*int(Q[j]) for j in range(3)),acb(0))
    b=project(K,[acb(0,1)*qi_dot*a[qi][j] for j in range(3)])
    z=-W*vdot(a[ki],b)

    pairs=[]
    incidence=[[] for _ in system.modes]
    D=zero3()
    support_modes={P,Q,K}
    for l0,r0 in zip(system.left,system.right):
        li=int(l0);ri=int(r0)
        key=(
            tuple(sorted(abs(int(x)) for x in system.modes[li])),
            tuple(sorted(abs(int(x)) for x in system.modes[ri])),
        )
        if key not in coeff:
            continue
        c=int(coeff[key])
        wave=tuple(int(x) for x in system.waves[ri])
        dot=sum((a[li][j]*wave[j] for j in range(3)),acb(0))
        d=[-x for x in project(K,[acb(0,1)*dot*a[ri][j] for j in range(3)])]
        D=add3(D,scale3(d,c))
        rec=(li,ri,wave,c)
        pos=len(pairs)
        pairs.append(rec)
        incidence[li].append(pos)
        if ri!=li:
            incidence[ri].append(pos)
        support_modes.add(tuple(system.modes[li]))
        support_modes.add(tuple(system.modes[ri]))

    if len(pairs)!=EXPECTED_SELECTED_PAIRS or len(support_modes)!=EXPECTED_SELECTED_MODES:
        raise ValueError(
            f"selected-support invariant mismatch: pairs={len(pairs)}, modes={len(support_modes)}"
        )

    w=-W*vdot(D,b)
    J=(w*z.conjugate()).imag

    raw=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix in range(len(system.modes)):
        for comp in range(3):
            deriv=[]
            for direction in (acb(1),acb(0,1)):
                db=zero3()
                if ix==pi:
                    term=project(K,[
                        acb(0,1)*int(Q[comp])*direction*a[qi][j]
                        for j in range(3)
                    ])
                    db=add3(db,term)
                if ix==qi:
                    vec=[acb(0),acb(0),acb(0)]
                    vec[comp]=acb(0,1)*qi_dot*direction
                    db=add3(db,project(K,vec))

                dD=zero3()
                for pos in incidence[ix]:
                    li,ri,wave,c=pairs[pos]
                    draw=zero3()
                    if ix==li:
                        scalar=acb(0,1)*int(wave[comp])*direction
                        draw=add3(draw,[scalar*a[ri][j] for j in range(3)])
                    if ix==ri:
                        dot=sum((a[li][j]*wave[j] for j in range(3)),acb(0))
                        vec=[acb(0),acb(0),acb(0)]
                        vec[comp]=acb(0,1)*dot*direction
                        draw=add3(draw,vec)
                    dd=[-x for x in project(K,draw)]
                    dD=add3(dD,scale3(dd,c))

                hk=zero3()
                if ix==ki:
                    hk[comp]=direction
                dz=-W*(vdot(hk,b)+vdot(a[ki],db))
                dw=-W*(vdot(dD,b)+vdot(D,db))
                dJ=(dw*z.conjugate()+w*dz.conjugate()).imag
                deriv.append(dJ)
            raw[ix][comp]=acb(deriv[0],deriv[1])

    return J,tangent_project(system,raw),{
        "selected_pair_count":len(pairs),
        "selected_mode_count":len(support_modes),
        "z_abs_lower":z.abs_lower().lower(),
        "z_abs_upper":z.abs_upper().upper(),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--higher-dir",type=Path,required=True)
    ap.add_argument("--k36",type=Path,required=True)
    ap.add_argument("--sign-chart",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--v026-result",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    if args.M not in (14,15,16,17):
        raise ValueError("v0.27a supports M=14,15,16,17 only")
    if sha256(args.k36)!=EXPECTED_K36:
        raise ValueError("K36 hash mismatch")
    if sha256(args.sign_chart)!=EXPECTED_SIGN_CHART:
        raise ValueError("prospective sign-chart hash mismatch")

    sys.path.insert(0,str((args.repo/"src").resolve()))
    sys.path.insert(0,str((args.repo/"next-work"/"n14_same_datum"/"tools").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    import wp19_v0_26_signed_goal_adjoint as v26
    import arb_common_n14 as common
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    coeff,_,_,sem=v26.load_coefficients(args.sign_chart,args.c500)
    if sem!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic mismatch")

    M=args.M
    H=M+1
    low=DealiasedSystem(M,nu=NU)
    high=DealiasedSystem(H,nu=NU)
    fixed=DealiasedSystem(11,nu=NU)
    for d,N in ((args.lower_dir,M),(args.higher_dir,H)):
        meta=json.loads((d/"metadata.json").read_text())
        if (
            meta.get("N")!=N
            or meta.get("witness_sha256")!=EXPECTED_WITNESS
            or meta.get("K36_keys_sha256")!=EXPECTED_K36
        ):
            raise ValueError("predictor metadata mismatch")

    lo=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    hi=np.load(args.higher_dir/"nodes.npy",mmap_mode="r")
    il=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    ih=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    base=v23.physical_project(fixed,np.asarray(lo[-1,il]))
    target=v23.physical_project(fixed,np.asarray(hi[-1,ih]))
    delta=np.asarray(target-base)

    ref=json.loads(args.v026_result.read_text())
    if ref.get("transition")!=f"{M}->{H}":
        raise ValueError("v0.26 transition mismatch")
    base_ref=float(ref["endpoint_identity"]["base_floating_J"])
    linear_ref=float(ref["endpoint_gradient_linear_prediction"])

    ctx.prec=192
    a=point_state(base)
    J,g,diag=analytic_gradient(fixed,a,coeff)
    J_ref_gap=abs(J-arb(str(float(base_ref)))).upper()
    J_ref_rel=(J_ref_gap/arb(str(max(1.0,abs(base_ref))))).upper()
    if J_ref_rel>arb("1e-10"):
        raise ValueError(("Arb/v0.26 objective discrepancy too large",str(J_ref_rel)))

    # Independent complex reverse-mode reference at the same nominal endpoint.
    torch_J,g_float=v26.torch_terminal_gradient(
        fixed,base,coeff,v23.tangent_project
    )
    if abs(torch_J-base_ref)/max(1.0,abs(base_ref))>5e-12:
        raise ValueError("independent PyTorch objective mismatch")

    diff=[]
    for ix in range(len(fixed.modes)):
        row=[]
        for j in range(3):
            row.append(g[ix][j]-ball(g_float[ix,j]))
        diff.append(row)
    grad_diff=l2_upper(diff)
    grad_upper=l2_upper(g)
    grad_lower=l2_lower(g)

    db=point_state(delta)
    directional=sum(
        ((g[ix][j].conjugate()*db[ix][j]).real
         for ix in range(len(fixed.modes)) for j in range(3)),
        arb(0)
    )
    directional_gap=abs(directional-arb(str(float(linear_ref)))).upper()
    directional_rel=(directional_gap/arb(str(max(1.0,abs(linear_ref))))).upper()
    if directional_rel>arb("1e-8"):
        raise ValueError(("Arb/v0.26 directional discrepancy too large",str(directional_rel)))

    # A dimensionless sanity ratio: arithmetic discrepancy against gradient size.
    denom=grad_lower
    rel=(grad_diff/denom).upper() if denom>0 else arb(0)

    out={
        "schema":"wp19-v0.27a-terminal-signed-numerator-gradient-arb-v1",
        "status":"PASS TERMINAL-GRADIENT ARB SUBCERTIFICATE",
        "M":M,
        "transition":f"{M}->{H}",
        "arb_precision_bits":ctx.prec,
        "frozen":{
            "witness_sha256":EXPECTED_WITNESS,
            "K36_sha256":EXPECTED_K36,
            "K36_sign_chart_sha256":EXPECTED_SIGN_CHART,
            "C500_portable_semantic_sha256":sem,
            "K36_signs_retuned":False,
            "C500_retuned":False,
        },
        "support":{
            "selected_ordered_pair_count":diag["selected_pair_count"],
            "selected_mode_count":diag["selected_mode_count"],
        },
        "nominal_endpoint_scope":"P11 projection of the saved lower-cutoff predictor endpoint, converted componentwise to exact decimal Arb points",
        "signed_numerator":{
            "arb_ball":str(J),
            "lower_decimal":common.decimal_lower(J.lower(),6),
            "upper_decimal":common.decimal_upper(J.upper(),6),
            "v0_26_reference":base_ref,
            "arb_vs_v0_26_absolute_discrepancy_upper_decimal":common.decimal_upper(J_ref_gap,12),
            "arb_vs_v0_26_relative_discrepancy_upper_decimal":common.decimal_upper(J_ref_rel,15),
        },
        "terminal_gradient":{
            "L2_lower_decimal":common.decimal_lower(grad_lower,6),
            "L2_upper_decimal":common.decimal_upper(grad_upper,6),
            "arb_vs_pytorch_L2_difference_upper_decimal":common.decimal_upper(grad_diff,12),
            "arb_vs_pytorch_relative_difference_upper_decimal":common.decimal_upper(rel,15),
            "component_count":len(fixed.modes)*3,
        },
        "directional_crosscheck":{
            "direction":"P11(u_{M+1}(T)-u_M(T)) from saved certified predictors",
            "arb_ball":str(directional),
            "lower_decimal":common.decimal_lower(directional.lower(),6),
            "upper_decimal":common.decimal_upper(directional.upper(),6),
            "v0_26_endpoint_gradient_linear_prediction":linear_ref,
            "arb_vs_v0_26_absolute_discrepancy_upper_decimal":common.decimal_upper(directional_gap,12),
            "arb_vs_v0_26_relative_discrepancy_upper_decimal":common.decimal_upper(directional_rel,15),
        },
        "normalizer_diagnostic":{
            "z_abs_lower":str(diag["z_abs_lower"]),
            "z_abs_upper":str(diag["z_abs_upper"]),
        },
        "method":"192-bit Arb evaluation of the collapsed fixed signed-C500 polynomial and its analytic real directional derivative in every complex Fourier coordinate, followed by the exact same solenoidal/reality tangent projection as v0.23/v0.26; independent PyTorch and v0.26 directional cross-checks.",
        "claim_boundary":"This certifies terminal-gradient arithmetic at the fixed nominal projected predictor endpoint only. It does not yet enclose gradient variation over the certified trajectory-error ball, backward adjoint propagation, quadrature, or nonlinear/endpoint Taylor remainders. No all-N or continuum theorem.",
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "M":M,
        "status":out["status"],
        "J":out["signed_numerator"],
        "gradient":out["terminal_gradient"],
        "directional":out["directional_crosscheck"],
    },indent=2))


if __name__=="__main__":
    main()
