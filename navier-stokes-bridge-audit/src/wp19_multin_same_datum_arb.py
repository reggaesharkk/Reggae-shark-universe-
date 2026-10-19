#!/usr/bin/env python3
"""Generic same-datum Arb certificate runner for N >= 14.

Reuses the validated N14 whole-segment Hermite/Arb machinery with N supplied
at runtime. The frozen 112-pair rational witness, K36 keys, viscosity, endpoint,
and time step are unchanged. No cutoff retuning is permitted.
"""
from __future__ import annotations

import argparse, hashlib, json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"src"
TOOLS=ROOT/"next-work"/"n14_same_datum"/"tools"
WITNESS=ROOT/"results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json"
KEYS=ROOT/"results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json"
sys.path.insert(0,str(SRC))
sys.path.insert(0,str(TOOLS))

import wp16_036_sparse_turnover_exact_anchor as exact
from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import arb_common_n14 as common
import arb_segment_n14 as segment

STEPS=120
H="0.000025"
NU="0.1"
T="0.003"
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_KEYS="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def vdot(a,b):
    return sum((a[i].conjugate()*b[i] for i in range(3)),acb(0))

def norm_upper(v):
    return segment.ball_l2_upper(v)

def projection(k,vector):
    kk=sum(x*x for x in k)
    kd=sum((vector[i]*int(k[i]) for i in range(3)),acb(0))
    return [vector[i]-kd*int(k[i])/kk for i in range(3)]

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def make_predictor(N:int,out:Path)->None:
    system=DealiasedSystem(N,nu=float(NU))
    field,_,witness_sha=exact.input_state(WITNESS)
    if witness_sha!=EXPECTED_WITNESS:
        raise ValueError("witness hash mismatch")
    a=np.asarray([
        [complex(float(z[0]),float(z[1])) for z in field.get(k,(exact.ZERO,)*3)]
        for k in system.modes
    ],dtype=np.complex128)
    shape=(STEPS+1,len(system.modes),3)
    ntmp=out/"nodes.npy.tmp"; rtmp=out/"rhs.npy.tmp"
    nodes=np.lib.format.open_memmap(ntmp,mode="w+",dtype=np.complex128,shape=shape)
    rhs=np.lib.format.open_memmap(rtmp,mode="w+",dtype=np.complex128,shape=shape)
    h=float(H)
    for step in range(STEPS+1):
        nodes[step]=a
        rhs[step]=system.rhs(a)
        if step<STEPS:
            a=system.rk4(a,h)
        if step%20==0:
            print("N",N,"predictor node",step,flush=True)
    nodes.flush(); rhs.flush(); del nodes,rhs
    ntmp.replace(out/"nodes.npy"); rtmp.replace(out/"rhs.npy")
    metadata={
        "schema":"wp19-generic-same-datum-hermite-predictor-v1",
        "N":N,"nu_exact_decimal":NU,"T_exact_decimal":T,
        "h_exact_decimal":H,"steps":STEPS,"modes":len(system.modes),
        "witness_sha256":witness_sha,"K36_keys_sha256":sha(KEYS),
        "initial_L2_error_bound_decimal":"0","initial_error_bound_decimal":"0",
        "initial_field_rule":"exact rational N11 witness embedded unchanged; all other modes zero",
        "nodes_sha256":sha(out/"nodes.npy"),"rhs_sha256":sha(out/"rhs.npy"),
        "status":"PREDICTOR_READY"
    }
    (out/"metadata.json").write_text(json.dumps(metadata,indent=2,sort_keys=True)+"\n")

def segment_worker(out_s:str,N:int,step:int)->tuple[int,str]:
    out=Path(out_s); path=out/f"{step:03d}.json"
    nodes=np.load(out/"nodes.npy",mmap_mode="r")
    rhs=np.load(out/"rhs.npy",mmap_mode="r")
    system=DealiasedSystem(N,nu=float(NU))
    digest=hashlib.sha256(b"".join(x.tobytes() for x in (
        nodes[step],nodes[step+1],rhs[step],rhs[step+1]
    ))).hexdigest()
    if path.exists():
        old=json.loads(path.read_text())
        if old.get("input_binary_sha256")==digest:
            return step,"cached"
    field=exact.input_state(WITNESS)[0] if step==0 else None
    R,M=segment.enclose(system,nodes[step],nodes[step+1],rhs[step],rhs[step+1],float(H),field)
    result={
        "step":step,"N":N,"input_binary_sha256":digest,
        "residual_L2_upper_decimal":common.decimal_upper(R,12),
        "gradient_Fourier_l1_upper_decimal":common.decimal_upper(M,6),
        "status":f"128-bit Arb whole-segment N{N} polynomial enclosure"
    }
    if step==0:
        result["exact_rational_initial_field_sha256"]=EXPECTED_WITNESS
    tmp=path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    tmp.replace(path)
    return step,"computed"

def cached_segment_status(out:Path,N:int):
    """Validate recovered segment JSONs against the exact predictor bytes.

    Interrupted GitHub jobs upload only atomically-renamed JSONs, but recovery
    must still verify every cached segment before trusting it.
    """
    nodes=np.load(out/"nodes.npy",mmap_mode="r")
    rhs=np.load(out/"rhs.npy",mmap_mode="r")
    valid=[]; removed=[]
    for step in range(STEPS):
        path=out/f"{step:03d}.json"
        if not path.exists():
            continue
        try:
            old=json.loads(path.read_text())
            digest=hashlib.sha256(b"".join(x.tobytes() for x in (
                nodes[step],nodes[step+1],rhs[step],rhs[step+1]
            ))).hexdigest()
            ok=(
                old.get("step")==step
                and old.get("N",N)==N
                and old.get("input_binary_sha256")==digest
                and "residual_L2_upper_decimal" in old
                and "gradient_Fourier_l1_upper_decimal" in old
            )
            if step==0:
                ok=ok and old.get("exact_rational_initial_field_sha256")==EXPECTED_WITNESS
            if ok:
                valid.append(step)
                continue
        except Exception:
            pass
        path.unlink(missing_ok=True)
        removed.append(step)
    return valid,removed

def generate_segments(out:Path,N:int,workers:int)->None:
    valid,removed=cached_segment_status(out,N)
    print(
        "N",N,"validated cached segments",len(valid),
        "removed stale/corrupt",removed,
        flush=True
    )
    missing=[i for i in range(STEPS) if i not in set(valid)]
    print("N",N,"missing segments",missing,flush=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(segment_worker,str(out),N,i) for i in missing]
        for future in as_completed(futures):
            step,status=future.result()
            print("N",N,"segment",step,status,flush=True)

def endpoint_evaluate(N:int,nodes_path:Path,keys_path:Path,E_decimal:str):
    ctx.prec=128
    system=DealiasedSystem(N,nu=float(NU))
    arr=np.load(nodes_path,mmap_mode="r")[-1]
    a=segment.solenoidal_reality_projection(system,arr)
    keys_raw=keys_path.read_bytes()
    if hashlib.sha256(keys_raw).hexdigest()!=EXPECTED_KEYS:
        raise ValueError("K36 key hash mismatch")
    keys={(tuple(row["left_orbit"]),tuple(row["right_orbit"])) for row in json.loads(keys_raw)["keys"]}
    p,q,k=(system.index[x] for x in (exact.P,exact.Q,exact.K))
    b=projection(exact.K,[acb(0,1)*sum((a[p][j]*exact.Q[j] for j in range(3)),acb(0))*a[q][i] for i in range(3)])
    weight=int(system.square[k]**2)
    z=-weight*vdot(a[k],b)
    groups={}; d_sum=arb(0)
    for li,ri in zip(system.left,system.right):
        wave=system.waves[ri]
        raw=[acb(0,1)*sum((a[li][j]*int(wave[j]) for j in range(3)),acb(0))*a[ri][i] for i in range(3)]
        d=[-v for v in projection(exact.K,raw)]
        d_sum+=norm_upper(d)
        w=-weight*vdot(d,b)
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]=groups.get(key,acb(0))+w
    I=arb(0); O=arb(0)
    for key,w in groups.items():
        mass=abs((w/z).imag)
        if key in keys: I+=mass
        else: O+=mass
    Fv=I-9*O
    E=arb(E_decimal)
    A=norm_upper([v for row in a for v in row])
    bp,bq,bk=(norm_upper(a[ix]) for ix in (p,q,k))
    B=norm_upper(b)
    dq=arb(sum(x*x for x in exact.Q)).sqrt().upper()
    delta_b=dq*E*(bp+bq+E)
    delta_d=arb(system.N)*(2*A*E+E*E)
    delta_z=weight*(E*B+(bk+E)*delta_b)
    z_abs=z.abs_lower().lower()
    z_lower=(z_abs-delta_z).lower()
    if not z_lower>0:
        raise ValueError("normalizer lower bound failed")
    delta_w=weight*(delta_d*B+(d_sum+delta_d)*delta_b)
    w_sum=weight*d_sum*B
    error=(9*(delta_w/z_lower+w_sum*delta_z/(z_lower*z_abs))).upper()
    upper=(Fv+error).upper(); lower=(Fv-error).lower()
    return {
        "status":"Arb endpoint margin conditional on supplied Galerkin L2 error radius",
        "N":N,
        "E_input_decimal":E_decimal,
        "F_of_exact_decimal_endpoint_upper":common.decimal_upper(Fv.upper(),9),
        "F_of_exact_decimal_endpoint_lower_ball":str(Fv.lower()),
        "F_of_exact_decimal_endpoint_lower_decimal":common.decimal_lower(Fv.lower(),9),
        "z_abs_lower_decimal":str(z_abs),
        "z_perturbation_upper_decimal":common.decimal_upper(delta_z.upper(),9),
        "F_error_upper_decimal":common.decimal_upper(error,9),
        "F_true_lower_decimal":common.decimal_lower(lower,9),
        "F_true_upper_decimal":common.decimal_upper(upper,9),
        "certified_negative_if_E_valid":upper<0,
        "ordered_group_count":len(groups)
    }

def anchor_projection(k,raw):
    kk=sum(x*x for x in k)
    kd=sum((raw[j]*k[j] for j in range(3)),acb(0))
    return [raw[j]-kd*k[j]/kk for j in range(3)]

def anchor_coefficients(k,a,b,f,g,exact_a=None):
    h=arb(H)
    A,B,F,G=(anchor_projection(k,[segment.ball(v) for v in row]) for row in (a,b,f,g))
    if exact_a is not None:
        A=[acb(arb(re.numerator)/arb(re.denominator),arb(im.numerator)/arb(im.denominator)) for re,im in exact_a]
    c1=[h*v for v in F]
    c2=[3*(B[j]-A[j])-h*(2*F[j]+G[j]) for j in range(3)]
    c3=[2*(A[j]-B[j])+h*(F[j]+G[j]) for j in range(3)]
    radius=sum((segment.ball_l2_upper(v) for v in (c1,c2,c3)),arb(0)).upper()
    return A,radius

def normalizer_guard(N:int,directory:Path,error_decimal:str):
    ctx.prec=128
    system=DealiasedSystem(N,nu=float(NU))
    nodes=np.load(directory/"nodes.npy",mmap_mode="r")
    rhs=np.load(directory/"rhs.npy",mmap_mode="r")
    E=arb(error_decimal)
    exact_field,_,sha0=exact.input_state(WITNESS)
    if sha0!=EXPECTED_WITNESS:
        raise ValueError("witness hash mismatch")
    qnorm=arb(sum(x*x for x in exact.Q)).sqrt().upper()
    minimum=None
    for step in range(STEPS):
        fields={}
        for k in (exact.P,exact.Q,exact.K):
            i=system.index[k]
            fields[k]=anchor_coefficients(
                k,nodes[step,i],nodes[step+1,i],rhs[step,i],rhs[step+1,i],
                exact_field[k] if step==0 else None
            )
        (p,dp),(q,dq),(k,dk)=(fields[x] for x in (exact.P,exact.Q,exact.K))
        b=anchor_projection(exact.K,[acb(0,1)*sum((p[j]*exact.Q[j] for j in range(3)),acb(0))*q[i] for i in range(3)])
        B=segment.ball_l2_upper(b)
        bp,bq,bk=(segment.ball_l2_upper(v) for v in (p,q,k))
        z=-sum((k[j].conjugate()*b[j] for j in range(3)),acb(0))*2025
        tp,tq,tk=dp+E,dq+E,dk+E
        delta_b=qnorm*(tp*bq+bp*tq+tp*tq)
        delta_z=2025*(tk*B+(bk+tk)*delta_b)
        lower=(z.abs_lower()-delta_z).lower()
        if not lower>0:
            raise ValueError(f"normalizer not certified at segment {step}")
        minimum=lower if minimum is None else minimum.min(lower).lower()
    return {
        "status":"Arb normalizer nonvanishing guard conditional on uniform L2 radius",
        "N":N,
        "E_uniform_input_decimal":error_decimal,
        "z_abs_uniform_lower_decimal":common.decimal_lower(minimum,8),
        "all_120_segments_pass":True
    }

def aggregate_errors(out:Path):
    ctx.prec=128
    h_exact=arb(H)
    E=arb(0); E_grad=arb(0); max_strain=arb(0); max_grad=arb(0); max_res=arb(0)
    sqrt2_lower=arb(2).sqrt().lower()
    for step in range(STEPS):
        row=json.loads((out/f"{step:03d}.json").read_text())
        R=arb(row["residual_L2_upper_decimal"])
        M=arb(row["gradient_Fourier_l1_upper_decimal"])
        Ms=arb(common.decimal_upper(M.upper()/sqrt2_lower,6))
        max_res=max_res.max(R); max_grad=max_grad.max(M); max_strain=max_strain.max(Ms)
        E_grad=(M*h_exact).exp()*(E_grad+h_exact*R)
        E_grad=arb(common.decimal_upper(E_grad,12))
        E=(Ms*h_exact).exp()*(E+h_exact*R)
        E=arb(common.decimal_upper(E,12))
    return {
        "maximum_residual_upper_decimal":common.decimal_upper(max_res,12),
        "maximum_gradient_l1_upper_decimal":common.decimal_upper(max_grad,6),
        "maximum_symmetric_strain_upper_decimal":common.decimal_upper(max_strain,6),
        "gradient_l1_error_upper_decimal":common.decimal_upper(E_grad,12),
        "symmetric_strain_error_upper_decimal":common.decimal_upper(E,12)
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--workers",type=int,default=2)
    args=ap.parse_args()
    N=args.N
    if N<14:
        ap.error("N must be >=14")
    if not 1<=args.workers<=8:
        ap.error("--workers must be 1..8")
    if sha(WITNESS)!=EXPECTED_WITNESS or sha(KEYS)!=EXPECTED_KEYS:
        raise ValueError("frozen witness or K36 keys changed")

    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    ctx.prec=128

    if not (out/"nodes.npy").exists() or not (out/"rhs.npy").exists():
        make_predictor(N,out)
    meta=json.loads((out/"metadata.json").read_text())
    if meta["N"]!=N or meta["witness_sha256"]!=EXPECTED_WITNESS or meta["K36_keys_sha256"]!=EXPECTED_KEYS:
        raise ValueError("predictor metadata mismatch")
    if sha(out/"nodes.npy")!=meta["nodes_sha256"] or sha(out/"rhs.npy")!=meta["rhs_sha256"]:
        raise ValueError("predictor array digest mismatch")

    generate_segments(out,N,args.workers)
    agg=aggregate_errors(out)
    E_decimal=agg["symmetric_strain_error_upper_decimal"]

    initial=exact.compute(WITNESS,KEYS)
    if not initial["exact_F0_positive"]:
        raise ValueError("exact initial sign gate failed")
    final=endpoint_evaluate(N,out/"nodes.npy",KEYS,E_decimal)
    if not final["certified_negative_if_E_valid"] or not arb(final["F_true_upper_decimal"])<0:
        raise ValueError("endpoint sign gate failed")
    guard=normalizer_guard(N,out,E_decimal)
    if not guard["all_120_segments_pass"]:
        raise ValueError("normalizer guard failed")

    result={
        "schema":"wp19-multin-same-datum-certificate-v1",
        "result":"PASS","N":N,
        "nu_exact_decimal":NU,"T_exact_decimal":T,"h_exact_decimal":H,"steps":STEPS,
        "witness_sha256":EXPECTED_WITNESS,"K36_keys_sha256":EXPECTED_KEYS,
        "nodes_sha256":meta["nodes_sha256"],"rhs_sha256":meta["rhs_sha256"],
        "initial_F_interval_decimal":initial["F0_interval_decimal"],
        **agg,
        "endpoint":final,
        "normalizer_guard":guard,
        "scope":f"same fixed rational datum embedded unchanged into finite cutoff N{N}",
        "continuum_claim":False
    }
    cert=out/f"n{N}_same_datum_certificate.json"
    cert.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "result":"PASS","N":N,
        "terminal_error":E_decimal,
        "F0":initial["F0_interval_decimal"],
        "FT_interval":[final["F_true_lower_decimal"],final["F_true_upper_decimal"]],
        "normalizer_lower":guard["z_abs_uniform_lower_decimal"],
        "nodes_sha256":meta["nodes_sha256"],
        "rhs_sha256":meta["rhs_sha256"]
    },indent=2))

if __name__=="__main__":
    main()
