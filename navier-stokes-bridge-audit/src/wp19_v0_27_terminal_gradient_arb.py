#!/usr/bin/env python3
"""WP19 v0.27 -- 128-bit Arb terminal-gradient certificate.

This intervalizes the terminal condition for the signed-C500 goal adjoint.
The objective is the fixed degree-7 polynomial from v0.26, evaluated at the
canonical decimal P11 predictor endpoint.  An analytic reverse-mode formula is
used both in complex128 and in python-flint acb arithmetic.

Scope: terminal polynomial gradient only.  Backward adjoint propagation,
dual quadrature, and nonlinear/endpoint remainder intervalization remain open.
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
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_SIGN_CHART="de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1"
EXPECTED_C500_SEMANTIC="1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f"

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def sha256(path:Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def c500_semantic_sha(path:Path):
    obj=json.loads(path.read_text())
    semantic={
        "schema":"wp19-c500-semantic-identity-v1",
        "coalition_size":int(obj["coalition_size"]),
        "keys":[{
            "rank":int(r["rank_from_N11_endpoint"]),
            "left_orbit":[int(x) for x in r["left_orbit"]],
            "right_orbit":[int(x) for x in r["right_orbit"]],
            "fixed_linear_sign":int(r["fixed_linear_sign"]),
        } for r in obj["keys"]],
    }
    raw=(json.dumps(semantic,sort_keys=True,separators=(",",":"))+"\n").encode()
    return hashlib.sha256(raw).hexdigest()

def load_coefficients(sign_chart:Path,c500_path:Path):
    if sha256(sign_chart)!=EXPECTED_SIGN_CHART:
        raise ValueError("frozen K36 sign-chart SHA mismatch")
    s=json.loads(sign_chart.read_text())
    if s.get("K36_sha256")!=EXPECTED_K36 or len(s.get("keys",[]))!=36:
        raise ValueError("K36 sign-chart identity mismatch")
    if c500_semantic_sha(c500_path)!=EXPECTED_C500_SEMANTIC:
        raise ValueError("C500 semantic identity mismatch")
    c=json.loads(c500_path.read_text())
    if int(c.get("coalition_size",-1))!=500:
        raise ValueError("C500 size mismatch")
    coeff={}
    for r in s["keys"]:
        key=(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
        sig=int(r["fixed_numerator_sign"])
        if sig not in (-1,1) or key in coeff: raise ValueError("invalid K36 sign")
        coeff[key]=sig
    for r in c["keys"]:
        key=(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
        tau=int(r["fixed_linear_sign"])
        if tau not in (-1,1) or key in coeff: raise ValueError("invalid/disjoint C500")
        coeff[key]=-9*tau
    if len(coeff)!=536:
        raise ValueError("frozen coefficient count mismatch")
    return coeff

def project_np(k,v):
    kk=float(sum(int(x)*int(x) for x in k))
    kv=np.asarray(k,float)
    return np.asarray(v)-kv*np.dot(kv,np.asarray(v))/kk

def project_ball(k,v):
    kk=sum(int(x)*int(x) for x in k)
    kd=sum((v[j]*int(k[j]) for j in range(3)),acb(0))
    return [v[j]-kd*int(k[j])/kk for j in range(3)]

def vdot_np(a,b):
    return np.vdot(np.asarray(a),np.asarray(b))

def vdot_ball(a,b):
    return sum((a[j].conjugate()*b[j] for j in range(3)),acb(0))

def tangent_project_np(system,g):
    gp=np.zeros_like(g,dtype=np.complex128)
    for ix,k in enumerate(system.modes):
        if system.square[ix]==0:
            gp[ix]=g[ix]
        else:
            gp[ix]=project_np(k,g[ix])
    out=np.zeros_like(gp)
    for ix,k in enumerate(system.modes):
        negk=tuple(-int(v) for v in k)
        if tuple(k)<=negk: continue
        ni=int(system.neg[ix])
        geff=0.5*(gp[ix]+np.conj(gp[ni]))
        out[ix]=geff; out[ni]=np.conj(geff)
    return out

def tangent_project_ball(system,g):
    gp=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        gp[ix]=g[ix][:] if int(system.square[ix])==0 else project_ball(k,g[ix])
    out=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        negk=tuple(-int(v) for v in k)
        if tuple(k)<=negk: continue
        ni=int(system.neg[ix])
        geff=[(gp[ix][j]+gp[ni][j].conjugate())/2 for j in range(3)]
        out[ix]=geff
        out[ni]=[v.conjugate() for v in geff]
    return out

def numpy_value_gradient(system,a,coeff):
    a=np.asarray(a,dtype=np.complex128)
    pi,qi,ki=(system.index[x] for x in (P,Q,K))
    Pk=system.projectors[ki]; W=float(system.square[ki]**2)
    B=Pk@(1j*np.dot(np.asarray(Q,float),a[pi])*a[qi])
    z=-W*vdot_np(a[ki],B)
    groups={}; pairs={}
    wanted=set(coeff)
    for l0,r0 in zip(system.left,system.right):
        l=int(l0);r=int(r0);key=(orbit(system.modes[l]),orbit(system.modes[r]))
        if key not in wanted: continue
        d=-(Pk@(1j*np.dot(system.waves[r],a[l])*a[r]))
        groups[key]=groups.get(key,np.zeros(3,np.complex128))+d
        pairs.setdefault(key,[]).append((l,r,np.asarray(system.waves[r],float)))
    if set(groups)!=wanted: raise ValueError("objective support mismatch")
    J=0.0; g=np.zeros_like(a); gB=np.zeros(3,np.complex128); gz=0j; gD={}
    for key,c in coeff.items():
        D=groups[key]; w=-W*vdot_np(D,B); n=float(np.imag(w*np.conj(z))); J+=c*n
        gw=c*1j*z; gz+=c*(-1j*w)
        gD[key]=-W*np.conj(gw)*B
        gB+=-W*gw*D
    g[ki]+=-W*np.conj(gz)*B
    gB+=-W*gz*a[ki]

    def back(gout,l,r,qvec,sign):
        gu=sign*(Pk@gout)
        sval=np.dot(qvec,a[l])
        gr=(-1j*np.conj(sval))*gu
        cscalar=1j*vdot_np(gu,a[r])
        gl=np.conj(cscalar)*qvec
        return gl,gr

    gl,gr=back(gB,pi,qi,np.asarray(Q,float),1.0)
    g[pi]+=gl;g[qi]+=gr
    for key,rows in pairs.items():
        for l,r,qvec in rows:
            gl,gr=back(gD[key],l,r,qvec,-1.0)
            g[l]+=gl;g[r]+=gr
    return float(J),tangent_project_np(system,g)

def arb_value_gradient(system,a,coeff):
    pi,qi,ki=(system.index[x] for x in (P,Q,K))
    W=int(system.square[ki]**2)
    qdot=sum((a[pi][j]*int(Q[j]) for j in range(3)),acb(0))
    B=project_ball(K,[acb(0,1)*qdot*a[qi][j] for j in range(3)])
    z=-W*vdot_ball(a[ki],B)
    groups={};pairs={};wanted=set(coeff)
    for l0,r0 in zip(system.left,system.right):
        l=int(l0);r=int(r0);key=(orbit(system.modes[l]),orbit(system.modes[r]))
        if key not in wanted: continue
        qvec=[int(x) for x in system.waves[r]]
        s=sum((a[l][j]*qvec[j] for j in range(3)),acb(0))
        d=[-x for x in project_ball(K,[acb(0,1)*s*a[r][j] for j in range(3)])]
        if key not in groups: groups[key]=[acb(0) for _ in range(3)]
        groups[key]=[groups[key][j]+d[j] for j in range(3)]
        pairs.setdefault(key,[]).append((l,r,qvec))
    if set(groups)!=wanted: raise ValueError("Arb objective support mismatch")

    J=arb(0)
    g=[[acb(0) for _ in range(3)] for _ in system.modes]
    gB=[acb(0) for _ in range(3)];gz=acb(0);gD={}
    for key,c in coeff.items():
        D=groups[key];w=-W*vdot_ball(D,B);n=(w*z.conjugate()).imag
        J+=n*int(c)
        gw=acb(0,int(c))*z
        gz+=acb(0,-int(c))*w
        gD[key]=[-W*gw.conjugate()*B[j] for j in range(3)]
        gB=[gB[j]-W*gw*D[j] for j in range(3)]
    g[ki]=[g[ki][j]-W*gz.conjugate()*B[j] for j in range(3)]
    gB=[gB[j]-W*gz*a[ki][j] for j in range(3)]

    def back(gout,l,r,qvec,sign):
        gu=project_ball(K,gout)
        if sign==-1: gu=[-x for x in gu]
        sval=sum((a[l][j]*int(qvec[j]) for j in range(3)),acb(0))
        gr=[-acb(0,1)*sval.conjugate()*gu[j] for j in range(3)]
        cscalar=acb(0,1)*vdot_ball(gu,a[r])
        gl=[cscalar.conjugate()*int(qvec[j]) for j in range(3)]
        return gl,gr

    gl,gr=back(gB,pi,qi,Q,1)
    g[pi]=[g[pi][j]+gl[j] for j in range(3)]
    g[qi]=[g[qi][j]+gr[j] for j in range(3)]
    for key,rows in pairs.items():
        for l,r,qvec in rows:
            gl,gr=back(gD[key],l,r,qvec,-1)
            g[l]=[g[l][j]+gl[j] for j in range(3)]
            g[r]=[g[r][j]+gr[j] for j in range(3)]
    return J,tangent_project_ball(system,g)

def real_ball_contains(b,x):
    xx=arb(str(float(x)))
    return not (xx < b.lower() or xx > b.upper())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--M",type=int,required=True)
    ap.add_argument("--lower-dir",type=Path,required=True)
    ap.add_argument("--higher-dir",type=Path,required=True)
    ap.add_argument("--sign-chart",type=Path,required=True)
    ap.add_argument("--c500",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    ctx.prec=128
    sys.path.insert(0,str((args.repo/"src").resolve()))
    sys.path.insert(0,str((args.repo/"next-work"/"n14_same_datum"/"tools").resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem
    import arb_segment_n14 as segment
    import arb_common_n14 as common

    M=args.M
    low=DealiasedSystem(M,nu=0.1);high=DealiasedSystem(M+1,nu=0.1);fixed=DealiasedSystem(11,nu=0.1)
    coeff=load_coefficients(args.sign_chart,args.c500)
    for d,N in ((args.lower_dir,M),(args.higher_dir,M+1)):
        meta=json.loads((d/"metadata.json").read_text())
        if meta["N"]!=N or meta["witness_sha256"]!=EXPECTED_WITNESS or meta["K36_keys_sha256"]!=EXPECTED_K36:
            raise ValueError("predictor metadata mismatch")

    lo=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    hi=np.load(args.higher_dir/"nodes.npy",mmap_mode="r")
    il=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    ih=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)

    # Same solenoidal/reality canonicalization used by the finite certificates.
    base_np=np.zeros((len(fixed.modes),3),dtype=np.complex128)
    target_np=np.zeros_like(base_np)
    for source,out in ((np.asarray(lo[-1,il]),base_np),(np.asarray(hi[-1,ih]),target_np)):
        for ix,k in enumerate(fixed.modes):
            negk=tuple(-int(v) for v in k)
            if tuple(k)<=negk: continue
            tr=project_np(k,source[ix]);out[ix]=tr;out[fixed.neg[ix]]=np.conj(tr)

    Jnp,gnp=numpy_value_gradient(fixed,base_np,coeff)
    abase=segment.solenoidal_reality_projection(fixed,np.asarray(lo[-1,il]))
    atarget=segment.solenoidal_reality_projection(fixed,np.asarray(hi[-1,ih]))
    Jarb,garb=arb_value_gradient(fixed,abase,coeff)

    # The rigorous direction is formed inside Arb from the separately
    # canonicalized target and base endpoints.  Do not first subtract two
    # binary64 projections and then pretend that rounded difference is exact.
    delta=target_np-base_np
    dball=[[atarget[ix][j]-abase[ix][j] for j in range(3)] for ix in range(len(fixed.modes))]
    directional=sum((vdot_ball(garb[ix],dball[ix]).real for ix in range(len(fixed.modes))),arb(0))
    dir_np=float(np.real(np.vdot(gnp.ravel(),delta.ravel())))

    # Floating finite-difference validation of the analytic reverse formula.
    # This is an independent implementation check, not the interval proof.
    dn=float(np.linalg.norm(delta.ravel()))
    if dn<=0: raise ValueError("zero endpoint direction")
    direction=delta/dn
    eps=1e-7
    fp=numpy_value_gradient(fixed,base_np+eps*direction,coeff)[0]
    fm=numpy_value_gradient(fixed,base_np-eps*direction,coeff)[0]
    fd=(fp-fm)/(2*eps)
    ad=float(np.real(np.vdot(gnp.ravel(),direction.ravel())))
    fd_rel=abs(fd-ad)/max(1.0,abs(fd),abs(ad))
    if fd_rel>2e-5: raise ValueError(("analytic gradient finite-difference check failed",fd,ad,fd_rel))

    grad_norm=segment.ball_l2_upper([z for row in garb for z in row])
    dlow=directional.lower();dupp=directional.upper()
    width=(dupp-dlow).upper()
    scale=max(abs(dir_np),1.0)
    width_rel=(width/arb(str(scale))).upper()

    # complex128 and Arb evaluate slightly different exact inputs/rounding
    # conventions.  Compare them by relative discrepancy; the certificate
    # itself is the Arb interval, not containment of the floating value.
    dir_gap=abs(directional-arb(str(dir_np))).upper()
    dir_gap_rel=(dir_gap/arb(str(scale))).upper()
    jscale=max(abs(Jnp),1.0)
    j_gap=abs(Jarb-arb(str(Jnp))).upper()
    j_gap_rel=(j_gap/arb(str(jscale))).upper()
    if not dir_gap_rel < arb("1e-10"):
        raise ValueError(("Arb/complex128 directional discrepancy too large",dir_gap_rel))
    if not j_gap_rel < arb("1e-10"):
        raise ValueError(("Arb/complex128 objective discrepancy too large",j_gap_rel))

    jlo=Jarb.lower();jhi=Jarb.upper()

    out={
        "schema":"wp19-v0.27-terminal-signed-c500-gradient-arb-v1",
        "copyright":"Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "status":"PASS 128-BIT ARB TERMINAL-GRADIENT CERTIFICATE",
        "transition":f"{M}->{M+1}",
        "M":M,
        "precision_bits":128,
        "frozen":{
            "witness_sha256":EXPECTED_WITNESS,
            "K36_sha256":EXPECTED_K36,
            "K36_sign_chart_sha256":EXPECTED_SIGN_CHART,
            "C500_semantic_sha256":EXPECTED_C500_SEMANTIC,
            "coefficient_count":len(coeff),
        },
        "objective":{
            "complex128_value":Jnp,
            "arb_lower_decimal":common.decimal_lower(jlo,8),
            "arb_upper_decimal":common.decimal_upper(jhi,8),
            "arb_vs_complex128_relative_gap_upper_decimal":common.decimal_upper(j_gap_rel,18),
        },
        "terminal_gradient":{
            "L2_upper_decimal":common.decimal_upper(grad_norm,6),
            "analytic_complex128_L2":float(np.linalg.norm(gnp.ravel())),
            "formula":"manual reverse-mode of fixed degree-7 signed numerator under Re Fourier-L2 pairing, followed by exact Leray/reality tangent projection",
        },
        "actual_cutoff_direction":{
            "complex128_linear_prediction":dir_np,
            "arb_linear_prediction_lower_decimal":common.decimal_lower(dlow,6),
            "arb_linear_prediction_upper_decimal":common.decimal_upper(dupp,6),
            "arb_vs_complex128_relative_gap_upper_decimal":common.decimal_upper(dir_gap_rel,18),
            "arb_interval_width_decimal":common.decimal_upper(width,6),
            "arb_width_over_abs_complex128_prediction_upper_decimal":common.decimal_upper(width_rel,18),
            "finite_difference_relative_error":fd_rel,
        },
        "next_target":"certify the backward adjoint itself by an Arb residual/enclosure around the floating half-step adjoint reconstruction, then rigorously enclose dual quadrature",
        "claim_boundary":"This certifies only the terminal polynomial value/gradient at the canonical decimal predictor endpoint. It does not intervalize backward adjoint propagation, quadrature, nonlinear remainder, endpoint Taylor remainder, all-N transfer, or continuum behavior."
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
