#!/usr/bin/env python3
"""WP19 v0.27b -- endpoint uncertainty / gradient-ball Arb subcertificate.

For each lower cutoff M=14,15,16,17, take the already certified terminal
L2 trajectory-error radius r_M and the nominal P11 endpoint used by v0.26/
v0.27a.  The true P11 endpoint lies in the L2 ball of radius r_M around that
nominal point.  Every complex Fourier coordinate therefore has real and
imaginary error at most r_M, so the Cartesian Arb box with radius r_M in every
real/imaginary coordinate is a rigorous (deliberately larger) enclosure.

The fixed signed-C500 polynomial and its analytic tangent gradient are then
evaluated on that full box using the same v0.27a formula.  This gives a
rigorous enclosure of terminal-gradient variation over the certified endpoint
uncertainty set.  The induced first-order Taylor-remainder bound is

    |J(a+h)-J(a)-<grad J(a),h>|
      <= ||h||_2 sup_{theta in [0,1]} ||grad J(a+theta h)-grad J(a)||_2
      <= r_M * Gvar_box.

The box is conservative because it ignores correlations, solenoidality and
the single global L2 constraint when intervalizing coordinates.  A large bound
is therefore a valid negative result, not a reason to retune the datum.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from flint import acb, arb, ctx

NU=0.1
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"

# Certified terminal L2 trajectory-error upper bounds from
# notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md.
CERTIFIED_TERMINAL_ERROR={
    14:"0.000012825905",
    15:"0.000013195722",
    16:"0.000013456103",
    17:"0.000013665541",
}


def box_scalar(x,rad):
    return arb(str(float(x)), rad)


def box_state(arr,rad):
    out=[]
    for row in np.asarray(arr):
        out.append([
            acb(box_scalar(np.real(z),rad),box_scalar(np.imag(z),rad))
            for z in row
        ])
    return out


def all_contains(outer,inner):
    for i in range(len(inner)):
        for j in range(3):
            if not outer[i][j].contains(inner[i][j]):
                return False,(i,j,str(outer[i][j]),str(inner[i][j]))
    return True,None


def finite_text(*vals):
    s=" ".join(str(v).lower() for v in vals)
    return ("nan" not in s) and ("inf" not in s)


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

    if args.M not in CERTIFIED_TERMINAL_ERROR:
        raise ValueError("v0.27b supports M=14,15,16,17 only")

    root=args.repo.resolve()
    sys.path.insert(0,str((root/"src").resolve()))
    sys.path.insert(0,str((root/"next-work"/"n14_same_datum"/"tools").resolve()))

    import wp19_v0_27a_terminal_gradient_arb as v27a
    import wp19_v0_26_signed_goal_adjoint as v26
    import wp19_v0_23_rk4_goal_adjoint as v23
    import arb_common_n14 as common
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    if v27a.sha256(args.k36)!=EXPECTED_K36:
        raise ValueError("K36 hash mismatch")
    if v27a.sha256(args.sign_chart)!=EXPECTED_SIGN_CHART:
        raise ValueError("prospective sign-chart hash mismatch")

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
            raise ValueError(("predictor metadata mismatch",str(d),meta.get("N")))

    lo=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    il=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    base=v23.physical_project(fixed,np.asarray(lo[-1,il]))

    ref=json.loads(args.v026_result.read_text())
    if ref.get("transition")!=f"{M}->{H}":
        raise ValueError("v0.26 transition mismatch")
    base_margin=arb(str(float(ref["margin"]["base_rigorous_negative_margin"])))
    if base_margin<=0:
        raise ValueError("base certified margin must be positive")

    radius_text=CERTIFIED_TERMINAL_ERROR[M]
    radius=arb(radius_text)
    ctx.prec=192

    point=v27a.point_state(base)
    box=box_state(base,radius_text)

    J0,g0,diag0=v27a.analytic_gradient(fixed,point,coeff)
    Jbox,gbox,diagbox=v27a.analytic_gradient(fixed,box,coeff)

    if not Jbox.contains(J0):
        raise ValueError(("objective box does not contain nominal objective",str(Jbox),str(J0)))
    contained,where=all_contains(gbox,g0)
    if not contained:
        raise ValueError(("gradient box does not contain nominal gradient",where))

    g0_upper=v27a.l2_upper(g0)
    gbox_upper=v27a.l2_upper(gbox)
    variation=[]
    for i in range(len(g0)):
        variation.append([gbox[i][j]-g0[i][j] for j in range(3)])
    gvar_upper=v27a.l2_upper(variation)

    objective_dev=abs(Jbox-J0).upper()
    linear_uncertainty=(radius*g0_upper).upper()
    taylor_remainder=(radius*gvar_upper).upper()
    taylor_over_margin=(taylor_remainder/base_margin).upper()
    linear_over_margin=(linear_uncertainty/base_margin).upper()
    objective_box_over_margin=(objective_dev/base_margin).upper()

    if not finite_text(
        g0_upper,gbox_upper,gvar_upper,objective_dev,
        linear_uncertainty,taylor_remainder,taylor_over_margin
    ):
        raise ValueError("non-finite interval quantity")

    budget_closing=bool(taylor_remainder < base_margin)
    status=(
        "PASS ENDPOINT-GRADIENT-BALL ARB SUBCERTIFICATE / BUDGET-CLOSING"
        if budget_closing else
        "PASS ENDPOINT-GRADIENT-BALL ARB SUBCERTIFICATE / BUDGET-OPEN"
    )

    out={
        "schema":"wp19-v0.27b-endpoint-gradient-ball-arb-v1",
        "status":status,
        "integrity_pass":True,
        "budget_closing":budget_closing,
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
        "certified_endpoint_uncertainty":{
            "source":"notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md",
            "lower_cutoff_terminal_L2_error_upper_decimal":radius_text,
            "embedding":"Each real and imaginary P11 Fourier coordinate is widened by the full certified L2 radius. This Cartesian box contains the certified L2 uncertainty ball but is deliberately larger.",
        },
        "nominal":{
            "objective_ball":str(J0),
            "gradient_L2_upper_decimal":common.decimal_upper(g0_upper,6),
            "z_abs_lower":str(diag0["z_abs_lower"]),
        },
        "endpoint_box":{
            "objective_ball":str(Jbox),
            "objective_deviation_from_nominal_upper_decimal":common.decimal_upper(objective_dev,6),
            "gradient_L2_upper_decimal":common.decimal_upper(gbox_upper,6),
            "gradient_variation_L2_upper_decimal":common.decimal_upper(gvar_upper,6),
            "contains_nominal_objective":True,
            "contains_every_nominal_gradient_component":True,
            "z_abs_lower":str(diagbox["z_abs_lower"]),
        },
        "rigorous_budgets":{
            "base_rigorous_negative_margin_decimal":common.decimal_lower(base_margin,6),
            "linear_terminal_state_uncertainty_upper_decimal":common.decimal_upper(linear_uncertainty,6),
            "linear_terminal_state_uncertainty_over_margin_upper_decimal":common.decimal_upper(linear_over_margin,12),
            "endpoint_first_order_taylor_remainder_upper_decimal":common.decimal_upper(taylor_remainder,6),
            "endpoint_first_order_taylor_remainder_over_margin_upper_decimal":common.decimal_upper(taylor_over_margin,12),
            "direct_objective_box_deviation_over_margin_upper_decimal":common.decimal_upper(objective_box_over_margin,12),
        },
        "proof_logic":"For any admissible endpoint perturbation h with ||h||_2 <= r_M, the segment a+theta h lies inside the coordinatewise Arb box. The interval analytic gradient therefore encloses grad J on the full segment, and r_M times the interval L2 upper bound on grad J(a+theta h)-grad J(a) encloses the first-order Taylor remainder.",
        "claim_boundary":"Finite-dimensional endpoint uncertainty subcertificate only. It does not certify backward adjoint propagation, dual quadrature, dynamic nonlinear remainder, all-N persistence, or continuum Navier-Stokes regularity.",
    }

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "M":M,
        "status":status,
        "radius":radius_text,
        "gradient_variation_L2_upper":out["endpoint_box"]["gradient_variation_L2_upper_decimal"],
        "taylor_remainder_over_margin":out["rigorous_budgets"]["endpoint_first_order_taylor_remainder_over_margin_upper_decimal"],
        "direct_objective_box_deviation_over_margin":out["rigorous_budgets"]["direct_objective_box_deviation_over_margin_upper_decimal"],
    },indent=2))


if __name__=="__main__":
    main()
