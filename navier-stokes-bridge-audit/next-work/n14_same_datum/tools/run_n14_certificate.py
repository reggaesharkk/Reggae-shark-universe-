#!/usr/bin/env python3
"""Generate the prospective same-datum N14 whole-segment Arb certificate."""
from __future__ import annotations
import argparse, hashlib, json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from flint import arb, ctx

ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/"src"
WITNESS=ROOT/"results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json"
KEYS=ROOT/"results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json"
sys.path.insert(0,str(SRC))
sys.path.insert(0,str(Path(__file__).resolve().parent))

import wp16_036_sparse_turnover_exact_anchor as exact
from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import arb_common_n14 as common
import arb_segment_n14 as segment
import endpoint_n14 as endpoint
import normalizer_n14 as normalizer

N=14
STEPS=120
EXPECTED_WITNESS="4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624"
EXPECTED_KEYS="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def make_predictor(out:Path)->None:
    system=DealiasedSystem(N,nu=.1)
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
    h=1/40000
    for step in range(STEPS+1):
        nodes[step]=a
        rhs[step]=system.rhs(a)
        if step<STEPS:
            a=system.rk4(a,h)
        if step%20==0:
            print("predictor node",step,flush=True)
    nodes.flush();rhs.flush();del nodes,rhs
    ntmp.replace(out/"nodes.npy");rtmp.replace(out/"rhs.npy")
    metadata={
        "schema":"wp19-n14-same-datum-hermite-predictor-v1",
        "N":N,"nu_exact_decimal":"0.1","T_exact_decimal":"0.003",
        "h_exact_decimal":"0.000025","steps":STEPS,"modes":len(system.modes),
        "witness_sha256":witness_sha,"K36_keys_sha256":sha(KEYS),
        "initial_L2_error_bound_decimal":"0","initial_error_bound_decimal":"0",
        "initial_field_rule":"exact rational N11 witness embedded unchanged into N14; all other modes zero",
        "nodes_sha256":sha(out/"nodes.npy"),"rhs_sha256":sha(out/"rhs.npy"),
        "status":"PREDICTOR_READY"
    }
    (out/"metadata.json").write_text(json.dumps(metadata,indent=2,sort_keys=True)+"\n")

def segment_worker(out_s:str,step:int)->tuple[int,str]:
    out=Path(out_s); path=out/f"{step:03d}.json"
    nodes=np.load(out/"nodes.npy",mmap_mode="r")
    rhs=np.load(out/"rhs.npy",mmap_mode="r")
    system=DealiasedSystem(N,nu=.1)
    digest=hashlib.sha256(b"".join(x.tobytes() for x in (
        nodes[step],nodes[step+1],rhs[step],rhs[step+1]
    ))).hexdigest()
    if path.exists():
        old=json.loads(path.read_text())
        if old.get("input_binary_sha256")==digest:
            return step,"cached"
    field=exact.input_state(WITNESS)[0] if step==0 else None
    R,M=segment.enclose(system,nodes[step],nodes[step+1],rhs[step],rhs[step+1],common.H,field)
    result={
        "step":step,"input_binary_sha256":digest,
        "residual_L2_upper_decimal":common.decimal_upper(R,12),
        "gradient_Fourier_l1_upper_decimal":common.decimal_upper(M,6),
        "status":"128-bit Arb whole-segment N14 polynomial enclosure"
    }
    if step==0:
        result["exact_rational_initial_field_sha256"]=EXPECTED_WITNESS
    tmp=path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    tmp.replace(path)
    return step,"computed"

def generate_segments(out:Path,workers:int)->None:
    missing=[i for i in range(STEPS) if not (out/f"{i:03d}.json").exists()]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(segment_worker,str(out),i) for i in missing]
        for future in as_completed(futures):
            step,status=future.result()
            print("segment",step,status,flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--workers",type=int,default=2)
    args=ap.parse_args()
    if not 1<=args.workers<=8:
        ap.error("--workers must be 1..8")
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    if sha(WITNESS)!=EXPECTED_WITNESS or sha(KEYS)!=EXPECTED_KEYS:
        raise ValueError("frozen witness or K36 keys changed")

    ctx.prec=128
    h_exact=arb("0.000025")
    if not (out/"nodes.npy").exists() or not (out/"rhs.npy").exists():
        make_predictor(out)
    meta=json.loads((out/"metadata.json").read_text())
    if meta["N"]!=N or meta["witness_sha256"]!=EXPECTED_WITNESS or meta["K36_keys_sha256"]!=EXPECTED_KEYS:
        raise ValueError("predictor metadata does not match frozen N14 protocol")
    if sha(out/"nodes.npy")!=meta["nodes_sha256"] or sha(out/"rhs.npy")!=meta["rhs_sha256"]:
        raise ValueError("predictor array digest mismatch")

    generate_segments(out,args.workers)
    aggregate=common.aggregate(out)

    E=arb(0);E_grad=arb(0);max_strain=arb(0);max_grad=arb(0)
    sqrt2_lower=arb(2).sqrt().lower()
    for step in range(STEPS):
        row=json.loads((out/f"{step:03d}.json").read_text())
        R=arb(row["residual_L2_upper_decimal"])
        M=arb(row["gradient_Fourier_l1_upper_decimal"])
        Ms=arb(common.decimal_upper(M.upper()/sqrt2_lower,6))
        max_grad=max_grad.max(M);max_strain=max_strain.max(Ms)
        E_grad=(M*h_exact).exp()*(E_grad+h_exact*R)
        E_grad=arb(common.decimal_upper(E_grad,12))
        E=(Ms*h_exact).exp()*(E+h_exact*R)
        E=arb(common.decimal_upper(E,12))
    E_decimal=common.decimal_upper(E,12)

    initial=exact.compute(WITNESS,KEYS)
    if not initial["exact_F0_positive"]:
        raise ValueError("exact initial N14 sign gate failed")
    final=endpoint.evaluate(out/"nodes.npy",KEYS,E_decimal)
    if not final["certified_negative_if_E_valid"] or not arb(final["F_true_upper_decimal"])<0:
        raise ValueError("N14 endpoint sign gate failed")
    guard=normalizer.guard(out,E_decimal,WITNESS)
    if not guard["all_120_segments_pass"]:
        raise ValueError("N14 whole-path normalizer guard failed")

    result={
        "schema":"wp19-n14-same-datum-certificate-v1",
        "result":"PASS","N":N,
        "nu_exact_decimal":"0.1","T_exact_decimal":"0.003",
        "h_exact_decimal":"0.000025","steps":STEPS,
        "witness_sha256":EXPECTED_WITNESS,"K36_keys_sha256":EXPECTED_KEYS,
        "initial_F_interval_decimal":initial["F0_interval_decimal"],
        "aggregate_gradient_l1":aggregate,
        "symmetric_strain_error_upper_decimal":E_decimal,
        "gradient_l1_error_upper_decimal":common.decimal_upper(E_grad,12),
        "max_gradient_l1_upper_decimal":common.decimal_upper(max_grad,6),
        "max_symmetric_strain_upper_decimal":common.decimal_upper(max_strain,6),
        "endpoint":final,"normalizer_guard":guard,
        "scope":"same fixed rational trigonometric datum embedded unchanged from N11 into finite cutoff N14",
        "continuum_claim":False
    }
    (out/"n14_same_datum_certificate.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "result":result["result"],"N":N,"terminal_error":E_decimal,
        "F0":initial["F0_interval_decimal"],
        "FT_interval":[final["F_true_lower_decimal"],final["F_true_upper_decimal"]],
        "normalizer_lower":guard["z_abs_uniform_lower_decimal"]
    },indent=2))

if __name__=="__main__":
    main()
