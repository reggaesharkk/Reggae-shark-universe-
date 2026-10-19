"""Frozen N15 phase continuation with bounded memory and atomic checkpoints.

Protocol frozen after the N14 prospective result and before any N15 state or score exists.
No change to the WP16 phase-search objective or candidate proposal schedule.
Resume uses the saved PCG64 state after the last completed trial.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

from phase_cascade_trajectory import NU
from wp16_expanded_phase_search import active_pairs, base_state, phase_rotate
from wp16_036_low_memory_objective import LowMemorySearchSystem, evaluate_lowmem

N14_SHA256 = "747dfb0bd0ea12271bd53b39fae7a4e18f396656bed3084bd4c632a9f3e5a3d9"
SEED = 20260940
GRID = 48
GLOBAL_DRAWS = 16
NEW_ROUNDS = 3
FULL_ROUNDS = 4
TRIALS_PER_ROUND = 72
BLOCK = 40
INITIAL_STEP = .30
TOTAL = GLOBAL_DRAWS+(NEW_ROUNDS+FULL_ROUNDS)*TRIALS_PER_ROUND


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(obj, indent=2)+"\n", encoding="utf-8")
    tmp.replace(path)


def schedule(trial):
    if trial<=GLOBAL_DRAWS:
        return "new_modes_global", None, None
    offset=trial-GLOBAL_DRAWS-1
    if offset<NEW_ROUNDS*TRIALS_PER_ROUND:
        rnd=offset//TRIALS_PER_ROUND
        return "new_modes_block", rnd, INITIAL_STEP*.6**rnd
    offset-=NEW_ROUNDS*TRIALS_PER_ROUND
    rnd=offset//TRIALS_PER_ROUND
    return "full_block", rnd, INITIAL_STEP*.6**rnd


def run(n14_path, checkpoint_path, output_path, stop_after_trial, chunk):
    if sha(n14_path)!=N14_SHA256:
        raise ValueError("N14 input hash differs from the frozen continuation")
    source=json.loads(n14_path.read_text(encoding="utf-8"))
    if source.get("cutoffs")!=[14] or source.get("resume_from_N")!=13:
        raise ValueError("N14 continuation structure differs")
    prev=source["rows"][0]
    if prev["N"]!=14:
        raise ValueError("N14 row missing")
    fingerprints={
        "n14_json": N14_SHA256,
        "continuation_py": sha(Path(__file__)),
        "objective_py": sha(Path(__file__).with_name("wp16_036_low_memory_objective.py")),
        "solver_py": sha(Path(__file__).with_name("wp16_036_dealiased_trajectory_gate.py")),
    }
    started=time.time()
    print("BUILD N15 MODE AND SOURCE TABLE",flush=True)
    system=LowMemorySearchSystem(15,nu=NU)
    print("N15 high ordered sources",len(system.high_out),flush=True)
    base=base_state(system,float(prev["amplitude"]),float(prev["anchor_time"]))
    pairs=active_pairs(system,base)
    previous={tuple(k):float(phi) for k,phi in zip(prev["support_vectors"],prev["best_phases"])}
    phases0=np.zeros(len(pairs),float)
    inherited=np.zeros(len(pairs),bool)
    for j,(_,_,k) in enumerate(pairs):
        if tuple(k) in previous:
            phases0[j]=previous[tuple(k)]
            inherited[j]=True
    new_idx=np.flatnonzero(~inherited)
    all_idx=np.arange(len(pairs))
    rng=np.random.default_rng(SEED)

    def score(phases,grid=GRID):
        return evaluate_lowmem(system,phase_rotate(base,pairs,phases),grid=grid,chunk=chunk)

    if checkpoint_path.exists():
        cp=json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if cp["fingerprints"]!=fingerprints or cp["N"]!=15 or cp["seed"]!=SEED:
            raise ValueError("checkpoint input/code fingerprint mismatch")
        if cp["active_conjugate_pairs"]!=len(pairs) or cp["inherited_pairs"]!=int(inherited.sum()):
            raise ValueError("checkpoint support mismatch")
        rng.bit_generator.state=cp["rng_state"]
        best=cp["best"]
        best_phases=np.asarray(cp["best_phases"],float)
        baseline=cp["unrotated_baseline"]
        continuation=cp["inherited_continuation"]
        records=cp["records"]
        last=int(cp["last_processed_trial"])
        elapsed_before=float(cp["elapsed_seconds"])
        print("RESUMED after trial",last,"C",best["C_infinity_stretch"],flush=True)
    else:
        print("SCORING BASELINE AND INHERITED STATE",flush=True)
        baseline=score(np.zeros(len(pairs)))
        continuation=score(phases0)
        best=dict(continuation)
        best_phases=phases0.copy()
        records=[dict(kind="unrotated_baseline",trial=0,**baseline),
                 dict(kind="inherited_continuation",trial=0,**continuation)]
        last=0
        elapsed_before=0.

    if len(best_phases)!=len(pairs) or not 0<=last<=TOTAL:
        raise ValueError("invalid checkpoint phase vector or trial number")

    def save(trial):
        atomic_json(checkpoint_path,{
            "N":15,"seed":SEED,"search_grid":GRID,
            "active_conjugate_pairs":len(pairs),"inherited_pairs":int(inherited.sum()),
            "new_pairs":len(new_idx),"last_processed_trial":trial,
            "fingerprints":fingerprints,"rng_state":rng.bit_generator.state,
            "unrotated_baseline":baseline,"inherited_continuation":continuation,
            "best":best,"best_phases":best_phases.tolist(),
            "records":records,"elapsed_seconds":elapsed_before+time.time()-started,
        })

    if not checkpoint_path.exists():
        save(0)
    if stop_after_trial is not None and last>=stop_after_trial:
        print("CHECKPOINTED STOP at trial",last,flush=True)
        return
    for trial in range(last+1,TOTAL+1):
        kind,rnd,step=schedule(trial)
        if kind=="new_modes_global":
            proposal=phases0.copy()
            proposal[new_idx]=rng.uniform(-math.pi,math.pi,size=len(new_idx))
        else:
            eligible=new_idx if kind=="new_modes_block" else all_idx
            indices=rng.choice(eligible,size=min(BLOCK,len(eligible)),replace=False)
            proposal=best_phases.copy()
            proposal[indices]=np.angle(np.exp(1j*(
                proposal[indices]+rng.normal(scale=step,size=len(indices)))))
        q=score(proposal)
        if q["C_infinity_stretch"]>best["C_infinity_stretch"]:
            best,best_phases=q,proposal.copy()
            row=dict(kind=kind+"_best",trial=trial,**q)
            if rnd is not None:row.update(round=rnd,step=step)
            records.append(row)
        save(trial)
        print(f"N15 trial {trial}/{TOTAL} C={best['C_infinity_stretch']:.9f}",flush=True)
        if stop_after_trial is not None and trial>=stop_after_trial:
            print("CHECKPOINTED STOP at trial",trial,flush=True)
            return

    refined={}
    for grid in (48,64,96,128):
        refined[str(grid)]=score(best_phases,grid=grid)
        print("N15 REFINE",grid,refined[str(grid)]["C_infinity_stretch"],flush=True)
    row={
        "N":15,"anchor_time":float(prev["anchor_time"]),
        "amplitude":float(prev["amplitude"]),"seed":SEED,
        "active_conjugate_pairs":len(pairs),
        "support_vectors":[list(k) for _,_,k in pairs],
        "inherited_pairs":int(inherited.sum()),"new_pairs":len(new_idx),
        "unrotated_baseline":baseline,"inherited_continuation":continuation,
        "best_search_grid":best,"best_phases":best_phases.tolist(),
        "refined":refined,"records":records,
        "search":{"search_grid":GRID,"new_global_draws":GLOBAL_DRAWS,
                  "new_block_rounds":NEW_ROUNDS,"full_block_rounds":FULL_ROUNDS,
                  "block_trials":TRIALS_PER_ROUND,"block_size":BLOCK,
                  "initial_step":INITIAL_STEP},
        "elapsed_seconds":elapsed_before+time.time()-started,
        "memory_safe_method":"bounded high-triad table and chunked exact objective",
    }
    result={"status":"completed frozen N15 cutoff continuation",
            "resume_source":str(n14_path),"resume_from_N":14,"cutoffs":[15],
            "anchor_time":row["anchor_time"],"rows":[row],
            "best_refined_case":{"N":15,"C":refined["128"]["C_infinity_stretch"]},
            "interpretation_rule":"finite phase search; not a global optimum or PDE theorem"}
    atomic_json(output_path,result)
    save(TOTAL)
    print("N15 COMPLETE",output_path,flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--n14-json",type=Path,required=True)
    p.add_argument("--checkpoint",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--stop-after-trial",type=int)
    p.add_argument("--chunk",type=int,default=100_000)
    a=p.parse_args()
    if a.stop_after_trial is not None and not 0<=a.stop_after_trial<=TOTAL:
        raise ValueError("stop-after-trial outside schedule")
    run(a.n14_json,a.checkpoint,a.output,a.stop_after_trial,a.chunk)
