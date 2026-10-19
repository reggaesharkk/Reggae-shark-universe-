#!/usr/bin/env python3
"""WP19 v0.24 — Hermite-consistent goal-adjoint and nonlinear-remainder budget.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

Floating verification stage. It strengthens v0.23 by:
  * integrating the continuous adjoint on a half-step grid with RK4;
  * pairing against the FULL cubic-Hermite reconstruction residual
    f_{M+1}(E ubar_M) - E d_t ubar_M, including interior Hermite defect;
  * using Simpson quadrature on every original segment;
  * measuring the exact goal-error decomposition diagnostics;
  * testing the candidate nonlinear remainder inequality
        |<lambda,B(e,e)>| <= ||grad lambda||_infty ||e||_2^2
    with Fourier-l1 gradient control and certified-segment-radius inputs.

This is not an interval certificate.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

H = 0.000025
NU = 0.1
STEPS = 120
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_KEYS = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"


def hermite_derivative(a0, a1, f0, f1, theta):
    t=float(theta)
    dh00=6*t*t-6*t
    dh10=3*t*t-4*t+1
    dh01=-6*t*t+6*t
    dh11=3*t*t-2*t
    return (dh00*a0+dh01*a1)/H + dh10*f0 + dh11*f1


def segment_value(v23, nodes, rhs, j, theta):
    return v23.hermite(
        np.asarray(nodes[j]), np.asarray(nodes[j+1]),
        np.asarray(rhs[j]), np.asarray(rhs[j+1]), theta
    )


def halfgrid_error_schedule(directory: Path):
    """Binary64 replay of whole-segment certified scalar radius data.

    Original nodes use the same recurrence as the validated trajectory
    certificate. Midpoints use the within-segment Gronwall formula with the
    segment's certified residual/gradient bounds. This remains a floating
    replay of rigorous decimal inputs, so downstream use is labelled scout.
    """
    node=np.zeros(STEPS+1,dtype=np.float64)
    half=np.zeros(2*STEPS+1,dtype=np.float64)
    sqrt2=math.sqrt(2.0)
    half[0]=0.0
    for j in range(STEPS):
        row=json.loads((directory/f"{j:03d}.json").read_text())
        R=float(row["residual_L2_upper_decimal"])
        M=float(row["gradient_Fourier_l1_upper_decimal"])
        S=M/sqrt2
        tau=H/2
        half[2*j]=node[j]
        half[2*j+1]=math.exp(S*tau)*(node[j]+tau*R)
        node[j+1]=math.exp(S*H)*(node[j]+H*R)
        half[2*j+2]=node[j+1]
    return half


def simpson(values):
    values=np.asarray(values,dtype=np.float64)
    if len(values)!=2*STEPS+1:
        raise ValueError("Simpson grid length mismatch")
    return float((H/6.0)*sum(values[2*j]+4*values[2*j+1]+values[2*j+2] for j in range(STEPS)))


def grad_fourier_l1(system, lam):
    per=np.linalg.norm(np.asarray(lam),axis=1)
    return float(np.sum(np.sqrt(system.square.astype(np.float64))*per))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--higher-dir",type=Path,required=True)
    ap.add_argument("--keys",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    sys.path.insert(0,str((args.repo/"src").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    M=args.M
    low=DealiasedSystem(M,nu=NU)
    high=DealiasedSystem(M+1,nu=NU)
    fixed=DealiasedSystem(11,nu=NU)
    keys=v23.load_keys(args.keys)

    for directory,N in ((args.lower_dir,M),(args.higher_dir,M+1)):
        meta=json.loads((directory/"metadata.json").read_text())
        if meta["N"]!=N or meta["witness_sha256"]!=EXPECTED_WITNESS or meta["K36_keys_sha256"]!=EXPECTED_KEYS:
            raise ValueError("predictor metadata mismatch")

    lo_nodes=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    lo_rhs=np.load(args.lower_dir/"rhs.npy",mmap_mode="r")
    hi_nodes=np.load(args.higher_dir/"nodes.npy",mmap_mode="r")
    hi_rhs=np.load(args.higher_dir/"rhs.npy",mmap_mode="r")

    idx11_low=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    idx11_high=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    base11=v23.physical_project(fixed,np.asarray(lo_nodes[-1,idx11_low]))
    target11=v23.physical_project(fixed,np.asarray(hi_nodes[-1,idx11_high]))
    base_F,_=v23.numpy_F11(fixed,base11,keys)
    target_F,_=v23.numpy_F11(fixed,target11,keys)
    torch_F,grad11=v23.torch_terminal_gradient(fixed,base11,keys)
    if abs(torch_F-base_F)>2e-10:
        raise ValueError("terminal objective mismatch")

    delta11=target11-base11
    endpoint_linear=float(np.real(np.vdot(grad11.ravel(),delta11.ravel())))
    actual=float(target_F-base_F)
    endpoint_remainder=float(actual-endpoint_linear)
    eT=float(np.linalg.norm(delta11.ravel()))
    observed_directional_curvature=(
        2.0*abs(endpoint_remainder)/(eT*eT) if eT>0 else 0.0
    )

    high_idx11=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    lam=np.zeros((len(high.modes),3),dtype=np.complex128)
    lam[high_idx11]=grad11

    # Half-step grid: index n corresponds to t=n*H/2.
    lambdas=[None]*(2*STEPS+1)
    lambdas[-1]=lam.copy()

    def x_at(j,theta):
        return v23.embed(low,high,segment_value(v23,lo_nodes,lo_rhs,j,theta))

    dt=-H/2.0
    for j in range(STEPS-1,-1,-1):
        for sub in (1,0):
            theta1=(sub+1)/2.0
            theta0=sub/2.0
            thetam=0.5*(theta0+theta1)
            u1=x_at(j,theta1)
            um=x_at(j,thetam)
            u0=x_at(j,theta0)
            k1=v23.adjoint_rhs(high,u1,lam)
            k2=v23.adjoint_rhs(high,um,lam+0.5*dt*k1)
            k3=v23.adjoint_rhs(high,um,lam+0.5*dt*k2)
            k4=v23.adjoint_rhs(high,u0,lam+dt*k3)
            lam=lam+(dt/6.0)*(k1+2*k2+2*k3+k4)
            lam=v23.physical_project(high,lam)
            lambdas[2*j+sub]=lam.copy()
        if j%20==0:
            print("M",M,"half-step adjoint segment",j,flush=True)

    low_to_high=np.asarray([high.index[k] for k in low.modes],dtype=np.int64)
    err_low=halfgrid_error_schedule(args.lower_dir)
    err_high=halfgrid_error_schedule(args.higher_dir)

    dual_pair=np.empty(2*STEPS+1,dtype=np.float64)
    residual_norm=np.empty_like(dual_pair)
    lambda_grad_l1=np.empty_like(dual_pair)
    e_nom=np.empty_like(dual_pair)
    e_upper_scout=np.empty_like(dual_pair)

    for n in range(2*STEPS+1):
        if n==2*STEPS:
            j=STEPS-1; theta=1.0
        else:
            j=n//2
            theta=0.0 if n%2==0 else 0.5

        lo=segment_value(v23,lo_nodes,lo_rhs,j,theta)
        lodot=hermite_derivative(
            np.asarray(lo_nodes[j]),np.asarray(lo_nodes[j+1]),
            np.asarray(lo_rhs[j]),np.asarray(lo_rhs[j+1]),theta
        )
        hi=segment_value(v23,hi_nodes,hi_rhs,j,theta)

        x=v23.embed(low,high,lo)
        xdot=v23.embed(low,high,lodot)
        r=high.rhs(x)-xdot
        y=np.asarray(hi)
        e=y-x

        residual_norm[n]=float(np.linalg.norm(r.ravel()))
        dual_pair[n]=float(np.real(np.vdot(lambdas[n].ravel(),r.ravel())))
        lambda_grad_l1[n]=grad_fourier_l1(high,lambdas[n])
        e_nom[n]=float(np.linalg.norm(e.ravel()))
        e_upper_scout[n]=e_nom[n]+err_low[n]+err_high[n]

    eta=simpson(dual_pair)
    nonlinear_bound_nominal=simpson(lambda_grad_l1*e_nom*e_nom)
    nonlinear_bound_radius=simpson(lambda_grad_l1*e_upper_scout*e_upper_scout)
    dynamic_observed=float(endpoint_linear-eta)

    out={
        "schema":"wp19-v0.24-hermite-goal-adjoint-remainder-budget-v1",
        "copyright":"Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "status":"NON-RIGOROUS HERMITE-CONSISTENT GOAL-ADJOINT / REMAINDER SCOUT",
        "transition":f"{M}->{M+1}",
        "M":M,
        "base_F11":base_F,
        "target_F11":target_F,
        "actual_delta_F11":actual,
        "endpoint_gradient_linear_prediction":endpoint_linear,
        "endpoint_taylor_remainder_observed":endpoint_remainder,
        "endpoint_nominal_difference_L2":eT,
        "observed_directional_curvature_2R_over_e2":observed_directional_curvature,
        "hermite_simpson_dual_prediction":eta,
        "total_remainder_actual_minus_dual":float(actual-eta),
        "total_relative_remainder":abs(actual-eta)/max(abs(actual),1e-30),
        "dynamic_remainder_endpoint_linear_minus_dual":dynamic_observed,
        "full_reconstruction_residual_max_L2":float(residual_norm.max()),
        "adjoint_gradient_fourier_l1_max":float(lambda_grad_l1.max()),
        "adjoint_gradient_fourier_l1_simpson_integral":simpson(lambda_grad_l1),
        "state_difference": {
            "nominal_max_halfgrid_L2":float(e_nom.max()),
            "radius_augmented_max_halfgrid_L2_scout":float(e_upper_scout.max()),
            "nominal_endpoint_L2":float(e_nom[-1]),
            "radius_augmented_endpoint_L2_scout":float(e_upper_scout[-1])
        },
        "nonlinear_dynamic_remainder_candidate": {
            "identity_bound":"|<lambda,B(e,e)>| <= ||grad lambda||_infty ||e||_2^2 <= (sum_k |k||lambda_k||_2)||e||_2^2",
            "nominal_simpson_bound":nonlinear_bound_nominal,
            "radius_augmented_simpson_bound_scout":nonlinear_bound_radius,
            "observed_abs_dynamic_remainder":abs(dynamic_observed),
            "radius_bound_over_observed":(
                nonlinear_bound_radius/max(abs(dynamic_observed),1e-30)
            )
        },
        "method":"Half-step RK4 adjoint along cubic-Hermite embedded lower reconstruction; full Hermite residual f_high(xbar)-xbar_dot; per-segment Simpson dual quadrature; Fourier-l1 gradient bound for the quadratic nonlinear remainder; binary64 replay of certified segment radii at nodes/midpoints.",
        "claim_boundary":"Floating verification only. The adjoint, Simpson quadrature, midpoint radius replay, gradient-l1 values, and endpoint curvature are not interval-enclosed. No all-N or continuum theorem."
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "transition":out["transition"],
        "actual":actual,
        "eta":eta,
        "total_rel_remainder":out["total_relative_remainder"],
        "endpoint_remainder":endpoint_remainder,
        "dynamic_observed":dynamic_observed,
        "nonlinear_bound_radius":nonlinear_bound_radius,
        "grad_l1_max":out["adjoint_gradient_fourier_l1_max"]
    },indent=2))


if __name__=="__main__":
    main()
