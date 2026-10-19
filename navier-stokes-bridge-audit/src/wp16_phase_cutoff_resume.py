"""Resume WP16 phase-only cutoff continuation from a prior escalation JSON.

Example:
  python src/wp16_phase_cutoff_resume.py \
    --resume-json /content/drive/MyDrive/WP16_CUTOFF_ESCALATION/wp16_phase_cutoff_escalation_results.json \
    --output /content/drive/MyDrive/WP16_CUTOFF_ESCALATION/wp16_phase_cutoff_escalation_N10_N11.json \
    --cutoffs 10 11

Finite deterministic continuation only.
"""

import argparse, json, math
from pathlib import Path

from wp16_phase_cutoff_escalation import optimize_continuation


def finest(row):
    if not row.get("refined"):
        return row["best_search_grid"]["C_infinity_stretch"]
    g=max(map(int,row["refined"]))
    return row["refined"][str(g)]["C_infinity_stretch"]


def run(args):
    prior=json.loads(args.resume_json.read_text(encoding="utf-8"))
    if not prior.get("rows"):
        raise ValueError("resume JSON contains no rows")

    last=max(prior["rows"], key=lambda r:int(r["N"]))
    if int(args.cutoffs[0]) <= int(last["N"]):
        raise ValueError("first new cutoff must exceed the last cutoff in resume JSON")

    phase_map={
        tuple(k): float(phi)
        for k,phi in zip(last["support_vectors"],last["best_phases"])
    }

    amplitude=float(last["amplitude"])
    anchor_time=float(last["anchor_time"])
    rows=[]

    for N in args.cutoffs:
        checkpoint=args.output.parent/f"wp16_cutoff_escalation_N{N}_checkpoint.json"
        row=optimize_continuation(
            N=N,
            phase_map=phase_map,
            amplitude=amplitude,
            anchor_time=anchor_time,
            seed=args.seed+N,
            search_grid=args.search_grid,
            new_global_draws=args.new_global_draws,
            new_block_rounds=args.new_block_rounds,
            full_block_rounds=args.full_block_rounds,
            block_trials=args.block_trials,
            block_size=args.block_size,
            initial_step=args.initial_step,
            checkpoint=checkpoint,
        )
        rows.append(row)
        phase_map={
            tuple(k): float(phi)
            for k,phi in zip(row["support_vectors"],row["best_phases"])
        }

    best=max(rows,key=finest)
    return {
        "status":"completed resumed WP16 phase-only cutoff escalation",
        "resume_source":str(args.resume_json),
        "resume_from_N":int(last["N"]),
        "resume_from_refined_C":float(finest(last)),
        "cutoffs":list(args.cutoffs),
        "anchor_time":anchor_time,
        "rows":rows,
        "best_refined_case":{"N":int(best["N"]),"C":float(finest(best))},
        "interpretation_rule":"Finite cutoff continuation only; growth does not establish divergence and saturation does not prove a universal bound."
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--resume-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--cutoffs",nargs="+",type=int,default=[10,11])
    p.add_argument("--seed",type=int,default=20260925)
    p.add_argument("--search-grid",type=int,default=40)
    p.add_argument("--new-global-draws",type=int,default=16)
    p.add_argument("--new-block-rounds",type=int,default=3)
    p.add_argument("--full-block-rounds",type=int,default=4)
    p.add_argument("--block-trials",type=int,default=72)
    p.add_argument("--block-size",type=int,default=40)
    p.add_argument("--initial-step",type=float,default=0.30)
    args=p.parse_args()

    if args.search_grid <= 3*max(args.cutoffs):
        raise ValueError("search grid must exceed 3*max(cutoffs)")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    result=run(args)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"best_refined_case":result["best_refined_case"],"output":str(args.output)},indent=2))
