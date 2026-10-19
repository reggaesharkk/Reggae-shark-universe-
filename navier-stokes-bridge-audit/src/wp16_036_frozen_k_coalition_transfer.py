"""Frozen N11 k-channel coalition transfer audit.

Use the ordered-orbit source ranking from N11_from_N10 / target_only / k_channel
as a fixed reference set. Freeze prefixes K={5,11,24,36,89}, corresponding to
the N11 target-only absolute-mass compression landmarks.

For every k-channel state at N9/N10/N11:
- sum signed contributions of the same frozen source keys;
- sum absolute contributions of those keys;
- compare against the state's full signed and absolute k-channel totals;
- report sign agreement and recovery ratios.

No new PDE simulation is run.
"""

import argparse
import json
from pathlib import Path

KS=(5,11,24,36,89)


def key(row):
    return (tuple(row["left_orbit"]),tuple(row["right_orbit"]))


def state_map(summary):
    return {
        key(r): float(r["alpha_dot_contribution"])
        for r in summary["top_groups"]
    }


def full_group_map(source_payload,step_name,state_name):
    rows=source_payload["steps"][step_name]["states"][state_name]["k_grouped_by_ordered_orbit_pair"]
    return {
        (tuple(r["left_orbit"]),tuple(r["right_orbit"])):float(r["alpha_dot_contribution"])
        for r in rows
    }


def run(compression_path,source_path):
    comp=json.loads(compression_path.read_text(encoding="utf-8"))
    source=json.loads(source_path.read_text(encoding="utf-8"))

    ref=comp["steps"]["N11_from_N10"]["states"]["target_only"]["k_channel"]
    ranked_keys=[
        (tuple(r["left_orbit"]),tuple(r["right_orbit"]))
        for r in ref["top_groups"]
    ]

    # top_groups stores first 25 only, so recover complete ranking directly
    # from the source decomposition and sort by absolute contribution.
    ref_rows=source["steps"]["N11_from_N10"]["states"]["target_only"]["k_grouped_by_ordered_orbit_pair"]
    ref_rows=sorted(ref_rows,key=lambda r:abs(float(r["alpha_dot_contribution"])),reverse=True)
    ranked_keys=[
        (tuple(r["left_orbit"]),tuple(r["right_orbit"]))
        for r in ref_rows
    ]

    result={
        "status":"executed frozen N11 target-only k-channel coalition transfer audit",
        "reference_step":"N11_from_N10",
        "reference_state":"target_only",
        "prefix_sizes":list(KS),
        "states":{},
    }

    for step_name,step in source["steps"].items():
        result["states"][step_name]={}
        for state_name,state in step["states"].items():
            rows=state["k_grouped_by_ordered_orbit_pair"]
            m={
                (tuple(r["left_orbit"]),tuple(r["right_orbit"])):float(r["alpha_dot_contribution"])
                for r in rows
            }
            total_signed=float(state["k_channel_total_alpha_dot"])
            total_abs=sum(abs(v) for v in m.values())

            rec={}
            for K in KS:
                keys=ranked_keys[:K]
                vals=[m.get(x,0.0) for x in keys]
                signed=sum(vals)
                abs_mass=sum(abs(v) for v in vals)
                rec[str(K)]={
                    "signed_contribution":signed,
                    "signed_share_of_channel_total":(
                        signed/total_signed if abs(total_signed)>1e-30 else None
                    ),
                    "absolute_mass_captured":abs_mass,
                    "absolute_mass_fraction":(
                        abs_mass/total_abs if total_abs>0 else None
                    ),
                    "same_sign_as_channel_total":(
                        signed*total_signed>0 if abs(signed)>1e-30 and abs(total_signed)>1e-30 else None
                    ),
                    "present_key_count":sum(1 for x in keys if x in m),
                }

            result["states"][step_name][state_name]={
                "k_channel_total_signed":total_signed,
                "k_channel_total_abs_group_contribution":total_abs,
                "prefix_recovery":rec,
            }

    # Compact transferability summary.
    transfer={}
    for K in KS:
        rows=[]
        for step_name,states in result["states"].items():
            for state_name,s in states.items():
                r=s["prefix_recovery"][str(K)]
                rows.append({
                    "step":step_name,
                    "state":state_name,
                    "signed_share":r["signed_share_of_channel_total"],
                    "abs_fraction":r["absolute_mass_fraction"],
                    "same_sign":r["same_sign_as_channel_total"],
                })
        transfer[str(K)]={
            "all_states_same_sign":all(r["same_sign"] is True for r in rows),
            "min_absolute_mass_fraction":min(r["abs_fraction"] for r in rows),
            "max_absolute_mass_fraction":max(r["abs_fraction"] for r in rows),
            "rows":rows,
        }
    result["transferability_by_prefix"]=transfer
    result["interpretation_rule"]=(
        "This is frozen-set accounting across already-generated finite states. "
        "A transferable coalition does not imply cutoff-uniform source sparsity "
        "or continuum phase dynamics."
    )
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--compression-json",type=Path,required=True)
    p.add_argument("--source-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    r=run(a.compression_json,a.source_json)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")

    print("\nFROZEN N11 K-CHANNEL COALITION TRANSFER")
    print("="*84)
    for step_name,states in r["states"].items():
        print("\n",step_name)
        for state_name,s in states.items():
            print(" ",state_name,"total=",s["k_channel_total_signed"])
            for K in KS:
                x=s["prefix_recovery"][str(K)]
                print(
                    "   K=",K,
                    "signed_share=",x["signed_share_of_channel_total"],
                    "abs_fraction=",x["absolute_mass_fraction"],
                    "same_sign=",x["same_sign_as_channel_total"],
                )
    print("\nTRANSFERABILITY")
    for K,x in r["transferability_by_prefix"].items():
        print(
            "K=",K,
            "all_same_sign=",x["all_states_same_sign"],
            "abs range=",x["min_absolute_mass_fraction"],x["max_absolute_mass_fraction"],
        )
    print("\nSAVED:",a.output)
