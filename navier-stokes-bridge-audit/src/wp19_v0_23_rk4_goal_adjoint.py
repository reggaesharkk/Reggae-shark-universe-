#!/usr/bin/env python3
"""WP19 v0.23 — reproducible goal-oriented continuous-adjoint cross-check.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

This is a floating verification stage, not an interval certificate. It replaces
v0.20's first-order backward adjoint stepping by an RK4 integration of the
continuous adjoint along the cubic-Hermite lower-cutoff reconstruction and
checks the spectral VJP against finite directional differences.

The terminal objective is the fixed N11 observable
    F11 = I_K36 - 9 O_K36
evaluated only on P11 u(T).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

H = 0.000025
NU = 0.1
STEPS = 120
P = (3, 2, 2)
Q = (3, -2, 1)
K = (6, 0, 3)
EXPECTED_WITNESS = "4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_KEYS = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


def physical_project(system, a):
    """Float64/complex128 version of the endpoint solenoidal/reality projection."""
    out = np.zeros_like(np.asarray(a), dtype=np.complex128)
    for ix, k in enumerate(system.modes):
        negk = tuple(-int(v) for v in k)
        if tuple(k) <= negk:
            continue
        tr = system.projectors[ix] @ np.asarray(a[ix])
        out[ix] = tr
        out[system.neg[ix]] = np.conj(tr)
    return out


def tangent_project(system, g):
    """Project a real-objective complex gradient onto divergence/reality tangent space."""
    gp = np.einsum("kij,kj->ki", system.projectors, np.asarray(g))
    out = np.zeros_like(gp, dtype=np.complex128)
    for ix, k in enumerate(system.modes):
        negk = tuple(-int(v) for v in k)
        if tuple(k) <= negk:
            continue
        ni = int(system.neg[ix])
        geff = 0.5 * (gp[ix] + np.conj(gp[ni]))
        out[ix] = geff
        out[ni] = np.conj(geff)
    return out


def load_keys(path: Path):
    import hashlib
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_KEYS:
        raise ValueError("K36 key hash mismatch")
    obj = json.loads(raw)
    return {(tuple(r["left_orbit"]), tuple(r["right_orbit"])) for r in obj["keys"]}


def numpy_F11(system, a, keys):
    a = np.asarray(a)
    pi, qi, ki = (system.index[x] for x in (P, Q, K))
    Pk = system.projectors[ki]
    weight = float(system.square[ki] ** 2)
    B = Pk @ (1j * np.dot(np.asarray(Q, float), a[pi]) * a[qi])
    z = -weight * np.vdot(a[ki], B)
    if abs(z) < 1e-30:
        raise ValueError("normalizer vanished")
    groups = defaultdict(float)
    for li, ri in zip(system.left, system.right):
        li = int(li); ri = int(ri)
        raw = 1j * np.dot(system.waves[ri], a[li]) * a[ri]
        da = -(Pk @ raw)
        dz = -weight * np.vdot(da, B)
        groups[(orbit(system.modes[li]), orbit(system.modes[ri]))] += float(np.imag(dz / z))
    I = sum(abs(v) for key, v in groups.items() if key in keys)
    O = sum(abs(v) for key, v in groups.items() if key not in keys)
    return float(I - 9.0 * O), groups


def torch_terminal_gradient(system, a_np, keys):
    import torch
    torch.set_default_dtype(torch.float64)

    a = torch.tensor(np.asarray(a_np), dtype=torch.complex128, requires_grad=True)
    Pk = torch.tensor(system.projectors[system.index[K]], dtype=torch.float64).to(torch.complex128)
    qwave = torch.tensor(Q, dtype=torch.float64).to(torch.complex128)
    pi, qi, ki = (system.index[x] for x in (P, Q, K))
    weight = float(system.square[ki] ** 2)

    B = Pk @ (1j * torch.sum(qwave * a[pi]) * a[qi])
    z = -weight * torch.vdot(a[ki], B)

    groups = {}
    for li0, ri0 in zip(system.left, system.right):
        li = int(li0); ri = int(ri0)
        wave = torch.tensor(system.waves[ri], dtype=torch.float64).to(torch.complex128)
        raw = 1j * torch.sum(wave * a[li]) * a[ri]
        da = -(Pk @ raw)
        dz = -weight * torch.vdot(da, B)
        val = torch.imag(dz / z)
        key = (orbit(system.modes[li]), orbit(system.modes[ri]))
        groups[key] = groups.get(key, 0.0) + val

    I = None
    O = None
    for key, v in groups.items():
        term = torch.abs(v)
        if key in keys:
            I = term if I is None else I + term
        else:
            O = term if O is None else O + term
    if I is None or O is None:
        raise ValueError("objective group partition failed")
    F = I - 9.0 * O
    F.backward()
    g = a.grad.detach().cpu().numpy()
    return float(F.detach().cpu().numpy()), tangent_project(system, g)


def hermite(a0, a1, f0, f1, theta):
    t = float(theta)
    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2
    return h00*a0 + h10*H*f0 + h01*a1 + h11*H*f1


def embed(low, high, arr):
    out = np.zeros((len(high.modes), 3), dtype=np.complex128)
    idx = np.asarray([high.index[k] for k in low.modes], dtype=np.int64)
    out[idx] = np.asarray(arr)
    return out


def nonlinear_vjp(system, a, lam):
    """Adjoint of DN[a] for N(a)=P((u.grad)u) under Re Fourier L2 pairing."""
    L = system.L
    f = np.zeros((L, L, L, 3), dtype=np.complex128)
    lp = np.einsum("kij,kj->ki", system.projectors, np.asarray(lam))
    g = np.zeros_like(f)
    f[system.slots] = np.asarray(a)
    g[system.slots] = lp

    u = np.fft.ifftn(f, axes=(0, 1, 2)) * L**3
    ell = np.fft.ifftn(g, axes=(0, 1, 2)) * L**3
    q = np.zeros_like(u)

    # q_j += sum_i ell_i * partial_j u_i
    for j in range(3):
        grad_u = np.fft.ifftn(
            1j * system.waves_grid(j)[..., None] * f,
            axes=(0, 1, 2)
        ) * L**3
        q[..., j] += np.sum(ell * grad_u, axis=-1)

    # q_j -= sum_i u_i * partial_i ell_j
    for i in range(3):
        grad_l = np.fft.ifftn(
            1j * system.waves_grid(i)[..., None] * g,
            axes=(0, 1, 2)
        ) * L**3
        q -= u[..., i, None] * grad_l

    qhat = np.fft.fftn(q, axes=(0, 1, 2))[system.slots] / L**3
    return np.einsum("kij,kj->ki", system.projectors, qhat)


def adjoint_rhs(system, a, lam):
    # lambda_t = -Df(a)^* lambda = DN(a)^*lambda + nu*A*lambda
    return nonlinear_vjp(system, a, lam) + system.nu * system.square[:, None] * lam


def vjp_self_test(system):
    rng = np.random.default_rng(20260930 + system.N)
    a = rng.normal(size=(len(system.modes),3)) + 1j*rng.normal(size=(len(system.modes),3))
    d = rng.normal(size=a.shape) + 1j*rng.normal(size=a.shape)
    l = rng.normal(size=a.shape) + 1j*rng.normal(size=a.shape)
    a = physical_project(system, a)
    d = physical_project(system, d)
    l = physical_project(system, l)
    eps = 2e-7
    fd = (system.nonlinear(a + eps*d) - system.nonlinear(a - eps*d)) / (2*eps)
    lhs = float(np.real(np.vdot(l.ravel(), fd.ravel())))
    v = nonlinear_vjp(system, a, l)
    rhs = float(np.real(np.vdot(v.ravel(), d.ravel())))
    scale = max(1.0, abs(lhs), abs(rhs))
    rel = abs(lhs-rhs)/scale
    return {"lhs":lhs, "rhs":rhs, "relative_error":rel}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--lower-dir", type=Path, required=True)
    ap.add_argument("--higher-dir", type=Path, required=True)
    ap.add_argument("--keys", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    sys.path.insert(0, str((args.repo/"src").resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    M = args.M
    low = DealiasedSystem(M, nu=NU)
    high = DealiasedSystem(M+1, nu=NU)
    fixed = DealiasedSystem(11, nu=NU)
    keys = load_keys(args.keys)

    for directory, N in ((args.lower_dir,M),(args.higher_dir,M+1)):
        meta=json.loads((directory/"metadata.json").read_text())
        if meta["N"] != N or meta["witness_sha256"] != EXPECTED_WITNESS or meta["K36_keys_sha256"] != EXPECTED_KEYS:
            raise ValueError("predictor metadata mismatch")

    lo_nodes=np.load(args.lower_dir/"nodes.npy",mmap_mode="r")
    lo_rhs=np.load(args.lower_dir/"rhs.npy",mmap_mode="r")
    hi_nodes=np.load(args.higher_dir/"nodes.npy",mmap_mode="r")
    if len(lo_nodes)!=STEPS+1 or len(hi_nodes)!=STEPS+1:
        raise ValueError("unexpected node count")

    idx11_low=np.asarray([low.index[k] for k in fixed.modes],dtype=np.int64)
    idx11_high=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)

    base11=physical_project(fixed,np.asarray(lo_nodes[-1,idx11_low]))
    target11=physical_project(fixed,np.asarray(hi_nodes[-1,idx11_high]))
    base_F, _=numpy_F11(fixed,base11,keys)
    target_F, _=numpy_F11(fixed,target11,keys)
    torch_F, grad11=torch_terminal_gradient(fixed,base11,keys)
    if abs(torch_F-base_F) > 2e-10:
        raise ValueError(("torch/numpy objective mismatch",torch_F,base_F))

    delta11=target11-base11
    endpoint_linear=float(np.real(np.vdot(grad11.ravel(),delta11.ravel())))

    # Objective-gradient finite-difference check in the actual endpoint direction.
    dn=float(np.linalg.norm(delta11.ravel()))
    if dn == 0:
        raise ValueError("zero endpoint direction")
    direction=delta11/dn
    eps=1e-7
    fp,_=numpy_F11(fixed,physical_project(fixed,base11+eps*direction),keys)
    fm,_=numpy_F11(fixed,physical_project(fixed,base11-eps*direction),keys)
    fd=(fp-fm)/(2*eps)
    ad=float(np.real(np.vdot(grad11.ravel(),direction.ravel())))
    grad_check_rel=abs(fd-ad)/max(1.0,abs(fd),abs(ad))

    # Embed the fixed terminal gradient into cutoff M+1.
    lam=np.zeros((len(high.modes),3),dtype=np.complex128)
    high_idx11=np.asarray([high.index[k] for k in fixed.modes],dtype=np.int64)
    lam[high_idx11]=grad11
    terminal_norm=float(np.linalg.norm(lam.ravel()))

    lambdas=[None]*(STEPS+1)
    lambdas[STEPS]=lam.copy()

    # One independent spectral VJP check on a smaller N=4 system.
    test_system=DealiasedSystem(4,nu=NU)
    vjp_check=vjp_self_test(test_system)
    if vjp_check["relative_error"] > 5e-6:
        raise ValueError(("spectral VJP self-test failed",vjp_check))

    # Backward RK4 continuous-adjoint integration along cubic-Hermite lower path.
    for j in range(STEPS-1,-1,-1):
        a0=np.asarray(lo_nodes[j])
        a1=np.asarray(lo_nodes[j+1])
        f0=np.asarray(lo_rhs[j])
        f1=np.asarray(lo_rhs[j+1])
        u1=embed(low,high,a1)
        um=embed(low,high,hermite(a0,a1,f0,f1,0.5))
        u0=embed(low,high,a0)
        dt=-H
        k1=adjoint_rhs(high,u1,lam)
        k2=adjoint_rhs(high,um,lam+0.5*dt*k1)
        k3=adjoint_rhs(high,um,lam+0.5*dt*k2)
        k4=adjoint_rhs(high,u0,lam+dt*k3)
        lam=lam+(dt/6.0)*(k1+2*k2+2*k3+k4)
        lam=physical_project(high,lam)
        lambdas[j]=lam.copy()
        if j % 20 == 0:
            print("M",M,"adjoint node",j,flush=True)

    # Tail residual at saved nodes and trapezoid dual pairing.
    low_to_high=np.asarray([high.index[k] for k in low.modes],dtype=np.int64)
    contrib=[]
    residual_norm=[]
    pair=[]
    for j in range(STEPS+1):
        emb=np.zeros((len(high.modes),3),dtype=np.complex128)
        emb[low_to_high]=np.asarray(lo_nodes[j])
        rhs_hi=high.rhs(emb)
        rhs_lo_emb=np.zeros_like(rhs_hi)
        rhs_lo_emb[low_to_high]=np.asarray(lo_rhs[j])
        r=rhs_hi-rhs_lo_emb
        residual_norm.append(float(np.linalg.norm(r.ravel())))
        pair.append(float(np.real(np.vdot(lambdas[j].ravel(),r.ravel()))))
    for j in range(STEPS):
        contrib.append(H*0.5*(pair[j]+pair[j+1]))
    eta=float(sum(contrib))

    actual=float(target_F-base_F)
    remainder=float(actual-eta)
    sum_abs=float(sum(abs(x) for x in contrib))
    pos=float(sum(x for x in contrib if x>0))
    neg=float(sum(x for x in contrib if x<0))

    out={
        "schema":"wp19-v0.23-rk4-continuous-adjoint-crosscheck-v1",
        "copyright":"Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.",
        "status":"NON-RIGOROUS FLOATING RK4 CONTINUOUS-ADJOINT CROSS-CHECK",
        "transition":f"{M}->{M+1}",
        "M":M,
        "objective":"fixed F11(P11 u(T))",
        "base_F11":base_F,
        "target_F11":target_F,
        "actual_delta_F11":actual,
        "dual_prediction":eta,
        "remainder":remainder,
        "relative_remainder":abs(remainder)/max(abs(actual),1e-30),
        "sum_abs_step_contributions":sum_abs,
        "positive_sum":pos,
        "negative_sum":neg,
        "positive_steps":sum(x>0 for x in contrib),
        "negative_steps":sum(x<0 for x in contrib),
        "terminal_adjoint_norm":terminal_norm,
        "initial_adjoint_norm":float(np.linalg.norm(lambdas[0].ravel())),
        "max_tail_rhs_norm":max(residual_norm),
        "endpoint_gradient_linear_prediction":endpoint_linear,
        "endpoint_gradient_remainder":float(actual-endpoint_linear),
        "objective_gradient_directional_check_relative_error":grad_check_rel,
        "spectral_vjp_self_test":vjp_check,
        "method":"Terminal F11 gradient by complex128 PyTorch reverse-mode on the fixed N11 objective; analytic dealiased spectral VJP; backward RK4 continuous adjoint along cubic-Hermite embedded lower trajectory; node-trapezoid dual pairing with newly opened-shell residual.",
        "claim_boundary":"Floating cross-check only. Neither terminal gradient nor adjoint evolution is interval-enclosed; no all-N or continuum theorem."
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in ("spectral_vjp_self_test",)},indent=2))


if __name__=="__main__":
    main()
