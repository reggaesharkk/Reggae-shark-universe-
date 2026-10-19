"""Cumulative source-compression audit for dominant-triad phase velocity.

Consumes wp16_036_phase_velocity_rhs_sources.json.

For q and k channels at inherited, target_only, and full_final states:
- rank ordered-orbit source groups by absolute alpha_dot contribution;
- compute cumulative recovery of absolute source mass;
- compute cumulative signed recovery relative to the channel total;
- report smallest group count reaching 50/75/90/95/99% absolute mass;
- track persistence of leading ordered-orbit sources across steps.

No new PDE simulation is run.
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict

THRESHOLDS=(0.50,0.75,0.90,0.95,0.99)


def k_for_fraction(cumsum,total,frac):
    if total<=0:
        return None
    target=frac*total
    for i,x in enumerate(cumsum,1):
        if x>=target:
            return i
    return len(cumsum)


def summarize_groups(groups,total_signed):
    ranked=sorted(groups,key=lambda r:abs(float(r["alpha_dot_contribution"])),reverse=True)
    absvals=[abs(float(r["alpha_dot_contribution"])) for r in ranked]
    total_abs=sum(absvals)
    cabs=[]
    s=0.0
    for x in absvals:
        s+=x
        cabs.append(s)

    out={
        "group_count":len(ranked),
        "total_signed":float(total_signed),
        "total_abs_group_contribution":float(total_abs),
        "signed_cancellation_ratio":(
            abs(float(total_signed))/total_abs if total_abs>0 else None
        ),
        "threshold_group_counts_absolute":{
            str(frac):k_for_fraction(cabs,total_abs,frac) for frac in THRESHOLDS
        },
        "top_groups":[],
    }

    signed_running=0.0
    for rank,row in enumerate(ranked[:25],1):
        signed_running+=float(row["alpha_dot_contribution"])
        out["top_groups"].append({
            "rank":rank,
            "left_orbit":row["left_orbit"],
            "right_orbit":row["right_orbit"],
            "count":int(row["count"]),
            "alpha_dot_contribution":float(row["alpha_dot_contribution"]),
            "abs_fraction":(
                abs(float(row["alpha_dot_contribution"]))/total_abs if total_abs>0 else None
            ),
            "cumulative_abs_fraction":(
                cabs[rank-1]/total_abs if total_abs>0 else None
            ),
            "cumulative_signed_over_channel_total":(
                signed_running/float(total_signed) if abs(float(total_signed))>1e-30 else None
            ),
        })
    return out


def key(row,channel):
    return (
        channel,
        tuple(row["left_orbit"]),
        tuple(row["right_orbit"]),
    )


def run(path):
    payload=json.loads(path.read_text(encoding="utf-8"))
    result={
        "status":"executed phase-velocity source-compression audit",
        "steps":{},
    }

    memberships=defaultdict(list)

    for step_name,step in payload["steps"].items():
        out_states={}
        for state_name,state in step["states"].items():
            qsum=summarize_groups(
                state["q_grouped_by_ordered_orbit_pair"],
                state["q_channel_total_alpha_dot"],
            )
            ksum=summarize_groups(
                state["k_grouped_by_ordered_orbit_pair"],
                state["k_channel_total_alpha_dot"],
            )
            out_states[state_name]={"q_channel":qsum,"k_channel":ksum}

            for channel_name,summary in [("q_channel",qsum),("k_channel",ksum)]:
                for row in summary["top_groups"][:10]:
                    memberships[key(row,channel_name)].append({
                        "step":step_name,
                        "state":state_name,
                        "rank":row["rank"],
                        "alpha_dot_contribution":row["alpha_dot_contribution"],
                    })
        result["steps"][step_name]={"N":step["N"],"states":out_states}

    persistent=[]
    for (channel,left,right),vals in memberships.items():
        step_set={v["step"] for v in vals}
        if len(step_set)>=2:
            persistent.append({
                "channel":channel,
                "left_orbit":list(left),
                "right_orbit":list(right),
                "distinct_step_count":len(step_set),
                "occurrences":vals,
                "mean_rank":sum(v["rank"] for v in vals)/len(vals),
            })

    persistent.sort(
        key=lambda r:(-r["distinct_step_count"],r["mean_rank"])
    )
    result["persistent_top10_source_groups"]=persistent
    result["interpretation_rule"]=(
        "Compression is descriptive for finite instantaneous source groups. "
        "It does not establish cutoff-uniform sparsity or continuum dominance."
    )
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    r=run(a.source_json)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")

    print("\nPHASE-VELOCITY SOURCE COMPRESSION")
    print("="*80)
    for step_name,step in r["steps"].items():
        print("\n",step_name)
        for state_name,state in step["states"].items():
            print(" ",state_name)
            for ch in ("q_channel","k_channel"):
                s=state[ch]
                print(
                    "  ",ch,
                    "signed=",s["total_signed"],
                    "abs=",s["total_abs_group_contribution"],
                    "cancel_ratio=",s["signed_cancellation_ratio"],
                    "K90=",s["threshold_group_counts_absolute"]["0.9"],
                    "K95=",s["threshold_group_counts_absolute"]["0.95"],
                    "K99=",s["threshold_group_counts_absolute"]["0.99"],
                )
    print("\nPERSISTENT TOP SOURCE GROUPS")
    for row in r["persistent_top10_source_groups"][:20]:
        print(row)
    print("\nSAVED:",a.output)
