#!/usr/bin/env python3
"""WP19 v0.27c1 -- direct Arb VJP check plus saved adjoint reconstruction.

This is the arithmetic foundation for the backward-adjoint validator.  It
implements the adjoint of the dealiased quadratic Navier-Stokes nonlinearity
directly in Fourier convolution with Arb balls, using the same carry-free
polynomial encoding as the validated primal segment certificates.

The point test is deliberately interior in time so both the primal state and
adjoint have broad spectral support.  Agreement with the independent FFT
complex128 implementation is required before any whole-segment adjoint
residual certificate is attempted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from flint import acb, acb_poly, arb, ctx

H=0.000025
NU=0.1
STEPS=120
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"


def ball(z):
    return acb(str(float(np.real(z))),str(float(np.imag(z))))


def point_rows(a):
    return [[ball(z) for z in row] for row in np.asarray(a)]


def project_rows(system,rows):
    out=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        kk=int(system.square[ix])
        if kk==0:
            continue
        kd=sum((rows[ix][j]*int(k[j]) for j in range(3)),acb(0))
        out[ix]=[rows[ix][j]-kd*arb(int(k[j]))/kk for j in range(3)]
    return out


def carry_free_indices(system):
    base=4*system.N+1
    left=[
        (int(k[0])+system.N)
        +base*(int(k[1])+system.N)
        +base*base*(int(k[2])+system.N)
        for k in system.waves
    ]
    right=[
        (int(k[0])+2*system.N)
        +base*(int(k[1])+2*system.N)
        +base*base*(int(k[2])+2*system.N)
        for k in system.waves
    ]
    return left,right


def poly_field(rows,comp,left,n,deriv_direction=None,system=None):
    arr=[0]*n
    if deriv_direction is None:
        for ix,slot in enumerate(left):
            arr[slot]=rows[ix][comp]
    else:
        for ix,slot in enumerate(left):
            arr[slot]=rows[ix][comp]*acb(0,int(system.waves[ix,deriv_direction]))
    return acb_poly(arr)


def nonlinear_vjp_arb(system,u,lam):
    """Arb Fourier form of v23.nonlinear_vjp.

    q_j = sum_i lambda_i * partial_j u_i
          - sum_i u_i * partial_i lambda_j,
    followed by Leray projection at the output mode.
    """
    u=project_rows(system,u)
    lam=project_rows(system,lam)
    left,right=carry_free_indices(system)
    n=max(left)+1

    U=[poly_field(u,i,left,n) for i in range(3)]
    L=[poly_field(lam,i,left,n) for i in range(3)]

    q=[[acb(0) for _ in range(3)] for _ in system.modes]
    for j in range(3):
        first=None
        for i in range(3):
            du=poly_field(u,i,left,n,deriv_direction=j,system=system)
            prod=L[i]*du
            first=prod if first is None else first+prod
        second=None
        for i in range(3):
            dl=poly_field(lam,j,left,n,deriv_direction=i,system=system)
            prod=U[i]*dl
            second=prod if second is None else second+prod
        for ix,slot in enumerate(right):
            q[ix][j]=first[slot]-second[slot]

    return project_rows(system,q)


def l2_upper(rows):
    s=arb(0)
    for row in rows:
        for z in row:
            u=z.abs_upper()
            s+=u*u
    return s.sqrt().upper()


def direct_vjp_mode_float(system,u,lam,k):
    """Independent O(number-of-modes) Fourier sum for one output mode."""
    k=tuple(int(x) for x in k)
    q=np.zeros(3,dtype=np.complex128)
    for pi,p0 in enumerate(system.modes):
        p=tuple(int(x) for x in p0)
        r=tuple(k[d]-p[d] for d in range(3))
        ri=system.index.get(r)
        if ri is None:
            continue
        # ell_i(p) * partial_j u_i(r)
        dot_lu=np.dot(lam[pi],u[ri])
        for j in range(3):
            q[j]+=1j*float(r[j])*dot_lu
        # - u_i(p) * partial_i ell_j(r)
        adv=sum(float(r[i])*u[pi,i] for i in range(3))
        q-=1j*adv*lam[ri]
    ix=system.index[k]
    return system.projectors[ix]@q


def selected_rows_l2_upper(rows):
    s=arb(0)
    for row in rows:
        for z in row:
            u=z.abs_upper()
            s+=u*u
    return s.sqrt().upper()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--sign-chart",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--adjoint-values-output",type=Path,required=True)
    ap.add_argument("--adjoint-rhs-output",type=Path,required=True)
    args=ap.parse_args()

    if args.M not in (14,15,16,17):
        raise ValueError("supported M are 14,15,16,17")

    root=args.repo.resolve()
    sys.path.insert(0,str((root/"src").resolve()))
    sys.path.insert(0,str((root/"next-work"/"n14_same_datum"/"tools").resolve()))
    import wp19_v0_23_rk4_goal_adjoint as v23
    import wp19_v0_26_signed_goal_adjoint as v26
    import wp19_v0_27_terminal_gradient_arb as v27a
    import arb_common_n14 as common
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    if v26.sha256(args.sign_chart)!=EXPECTED_SIGN_CHART:
        raise ValueError("sign chart hash mismatch")
    coeff,_,_,sem=v26.load_coefficients(args.sign_chart,args.c500)
    if sem!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic mismatch")

    M=args.M
    low=DealiasedSystem(M,nu=NU)
    high=DealiasedSystem(M+1,nu=NU)
    fixed=DealiasedSystem(11,nu=NU)
    meta=json.loads((args.lower_dir/"metadata.json").read_text())
    if (
        meta.get("N")!=M
        or meta.get("witness_sha256")!=EXPECTED_WITNESS
        or meta.get("K36_keys_sha256")!=EXPECTED_K36
    ):
        raise ValueError("lower predictor metadata mismatch")

    lo_nodes=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    lo_rhs=np.load(args.lower_dir/"rhs.npy",mmap_mode="r")
    idx11=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    base11=v23.physical_project(fixed,np.asarray(lo_nodes[-1,idx11]))
    _,grad11=v26.torch_terminal_gradient(fixed,base11,coeff,v23.tangent_project)

    high_idx11=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    lam=np.zeros((len(high.modes),3),dtype=np.complex128)
    lam[high_idx11]=grad11
    lambdas=[None]*(2*STEPS+1)
    lambdas[-1]=lam.copy()

    def segval(j,theta):
        return v26.segment_value(v23,lo_nodes,lo_rhs,j,theta)
    def x_at(j,theta):
        return v23.embed(low,high,segval(j,theta))

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

    # Persist the complete 241-node half-step reconstruction. These are
    # binary64 centers, not interval enclosures. The next certificate stage
    # must enclose the polynomial residual around them and include predictor
    # and terminal-gradient uncertainty separately.
    lambda_values=np.asarray(lambdas,dtype=np.complex128)
    if lambda_values.shape!=(2*STEPS+1,len(high.modes),3):
        raise ValueError(("adjoint path shape mismatch",lambda_values.shape))
    if not np.isfinite(lambda_values.real).all() or not np.isfinite(lambda_values.imag).all():
        raise ValueError("non-finite adjoint path value")
    lambda_rhs=np.empty_like(lambda_values)
    for n, lam_node in enumerate(lambda_values):
        j_node=min(n//2,STEPS-1)
        theta_node=1.0 if n==2*STEPS else 0.5*(n%2)
        u_node=x_at(j_node,theta_node)
        lambda_rhs[n]=v23.adjoint_rhs(high,u_node,lam_node)
    if not np.isfinite(lambda_rhs.real).all() or not np.isfinite(lambda_rhs.imag).all():
        raise ValueError("non-finite adjoint RHS reconstruction")
    args.adjoint_values_output.parent.mkdir(parents=True,exist_ok=True)
    args.adjoint_rhs_output.parent.mkdir(parents=True,exist_ok=True)
    np.save(args.adjoint_values_output,lambda_values,allow_pickle=False)
    np.save(args.adjoint_rhs_output,lambda_rhs,allow_pickle=False)
    if len(lambda_values)!=2*STEPS+1:
        raise ValueError("adjoint path has missing time nodes")

    # Interior original node j=60, t=T/2.
    j=60
    n=2*j
    u_float=v23.embed(low,high,np.asarray(lo_nodes[j]))
    lam_float=np.asarray(lambdas[n])
    ref=v23.nonlinear_vjp(high,u_float,lam_float)

    ctx.prec=192
    got=nonlinear_vjp_arb(high,point_rows(u_float),point_rows(lam_float))

    # FFT is an independent implementation but at these very large adjoint
    # amplitudes its cancellation/roundoff is not a rigorous reference. Keep
    # its discrepancy as a diagnostic, then validate the Arb convolution
    # against a second, explicit Fourier sum on deterministic high-signal modes.
    diff=[]
    for ix in range(len(high.modes)):
        diff.append([got[ix][cc]-ball(ref[ix,cc]) for cc in range(3)])
    diff_upper=l2_upper(diff)
    ref_norm=float(np.linalg.norm(ref.ravel()))
    rel=(diff_upper/arb(str(max(1.0,ref_norm)))).upper()

    per=np.linalg.norm(ref,axis=1)
    top=np.argsort(per)[-12:][::-1]
    selected=[]
    arb_direct_diff=[]
    fft_direct_sq=0.0
    direct_sq=0.0
    for ix0 in top:
        ix=int(ix0)
        k=tuple(int(x) for x in high.modes[ix])
        direct=direct_vjp_mode_float(high,u_float,lam_float,k)
        direct_sq+=float(np.vdot(direct,direct).real)
        fft_direct_sq+=float(np.vdot(ref[ix]-direct,ref[ix]-direct).real)
        row=[]
        for cc in range(3):
            row.append(got[ix][cc]-ball(direct[cc]))
        arb_direct_diff.append(row)
        selected.append({
            "mode":[int(x) for x in k],
            "fft_L2":float(np.linalg.norm(ref[ix])),
            "direct_L2":float(np.linalg.norm(direct)),
            "fft_vs_direct_L2":float(np.linalg.norm(ref[ix]-direct)),
        })
    selected_diff=selected_rows_l2_upper(arb_direct_diff)
    selected_direct_norm=direct_sq**0.5
    selected_rel=(selected_diff/arb(str(max(1.0,selected_direct_norm)))).upper()
    fft_selected_rel=(fft_direct_sq**0.5)/max(1.0,selected_direct_norm)

    if selected_rel>arb("1e-12"):
        raise ValueError(("Arb convolution vs explicit Fourier sum discrepancy too large",str(selected_rel)))

    out={
        "schema":"wp19-v0.27c1-adjoint-path-export-v1",
        "status":"PASS ARB VJP CROSSCHECK AND ADJOINT PATH EXPORT",
        "M":M,
        "transition":f"{M}->{M+1}",
        "test_node":j,
        "test_time_decimal":"0.0015",
        "arb_precision_bits":ctx.prec,
        "frozen":{
            "witness_sha256":EXPECTED_WITNESS,
            "K36_sha256":EXPECTED_K36,
            "K36_sign_chart_sha256":EXPECTED_SIGN_CHART,
            "C500_portable_semantic_sha256":sem,
        },
        "reference_fft_vjp_L2":ref_norm,
        "arb_vs_fft_L2_difference_upper_decimal":common.decimal_upper(diff_upper,9),
        "arb_vs_fft_relative_difference_upper_decimal":common.decimal_upper(rel,15),
        "selected_mode_direct_crosscheck":{
            "mode_count":len(selected),
            "arb_vs_explicit_direct_L2_difference_upper_decimal":common.decimal_upper(selected_diff,9),
            "arb_vs_explicit_direct_relative_difference_upper_decimal":common.decimal_upper(selected_rel,15),
            "fft_vs_explicit_direct_relative_difference":fft_selected_rel,
            "rows":selected,
        },
        "adjoint_reconstruction":{
            "time_node_count":int(lambda_values.shape[0]),
            "time_step_decimal":"0.0000125",
            "time_interval_decimal":["0","0.003"],
            "values_shape":list(lambda_values.shape),
            "rhs_shape":list(lambda_rhs.shape),
            "values_file":args.adjoint_values_output.name,
            "values_sha256":sha256(args.adjoint_values_output),
            "rhs_file":args.adjoint_rhs_output.name,
            "rhs_sha256":sha256(args.adjoint_rhs_output),
            "lower_nodes_sha256":sha256(args.lower_dir/"nodes.npy"),
            "lower_rhs_sha256":sha256(args.lower_dir/"rhs.npy"),
            "lower_metadata_sha256":sha256(args.lower_dir/"metadata.json"),
            "sign_chart_sha256":sha256(args.sign_chart),
            "c500_rebuilt_file_sha256":sha256(args.c500),
            "C500_portable_semantic_sha256":sem,
            "interpretation":"Saved binary64 centers and continuous-RHS node evaluations for reproducible Hermite reconstruction only; no residual, trajectory, or quadrature enclosure is claimed by this export.",
        },
        "method":"Direct carry-free Arb convolution of q_j=sum_i lambda_i partial_j u_i - sum_i u_i partial_i lambda_j, followed by Leray projection. Arithmetic is fail-closed against an independent explicit Fourier sum on 12 deterministic high-signal modes; the dealiased FFT comparison is retained as a floating diagnostic rather than treated as exact ground truth.",
        "next_target":"Enclose the continuous Hermite residual on all 240 half-step segments with Arb/Bernstein, then propagate the adjoint error from terminal-gradient and predictor uncertainty.",
        "claim_boundary":"The VJP arithmetic is cross-checked at one interior point. The 241-node path is a binary64 reconstruction only, not an adjoint trajectory certificate; no all-N/continuum claim.",
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
