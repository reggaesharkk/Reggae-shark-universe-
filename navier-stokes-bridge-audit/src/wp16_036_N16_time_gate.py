"""Prospective frozen N16 K36 static and time-resolved gate evaluator."""

import argparse
import hashlib
import json
from pathlib import Path

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem, snapshot
from wp16_036_K36_margin_velocity import audit as margin_velocity

DT=.0001
STEPS=30


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_failure(rows, key):
    return next((i for i, row in enumerate(rows) if not row[key]), None)


def run(n15_path,n16_path,source_path,out_path):
    if sha(n15_path)!="c0bd97f554df3e8561d75e1ba62356d04200fbe4986f573e3305a98932ccb225":
        raise ValueError("N15 predecessor hash mismatch")
    if sha(source_path)!="193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e":
        raise ValueError("frozen K36 source hash mismatch")
    j15=json.loads(n15_path.read_text())
    j16=json.loads(n16_path.read_text())
    source=json.loads(source_path.read_text())
    if j16.get("cutoffs")!=[16] or j16.get("resume_from_N")!=15:
        raise ValueError("N16 continuation structure changed")
    row16=hold.get_row(j16,16)
    expected_search={
        "search_grid":64,"new_global_draws":16,"new_block_rounds":3,
        "full_block_rounds":4,"block_trials":72,"block_size":40,
        "initial_step":.30,
    }
    if row16.get("seed")!=20260941 or row16.get("search")!=expected_search:
        raise ValueError("N16 continuation does not match frozen schedule")
    hold.System=DealiasedSystem
    system,states=hold.reconstruct(hold.get_row(j15,15),row16)
    keys=hold.frozen_keys(source)
    result={
        "status":"prospective frozen N16 time-resolved K36 evaluation",
        "input_sha256":{"n15":sha(n15_path),"n16":sha(n16_path),"source":sha(source_path)},
        "dt":DT,"steps":STEPS,"nu":system.nu,
        "criteria":{"same_sign":True,"minimum_absolute_mass_fraction":.9,
                    "signed_share_interval":[.8,1.2]},
        "states":{},
    }
    for name,a0 in states.items():
        a=a0.copy()
        rows=[]
        for step in range(STEPS+1):
            row=snapshot(system,a,keys,step*DT)
            inside=row["absolute_mass_captured"]
            outside=row["k_channel_total_abs_group_contribution"]-inside
            row["K36_mass_margin"]=inside-9*outside
            row["mass_gate_pass"]=row["absolute_mass_fraction"]>=.9
            rows.append(row)
            if step<STEPS:a=system.rk4(a,DT)
        first_mass=first_failure(rows,"mass_gate_pass")
        first_any=first_failure(rows,"passes_preregistered_consistency_criteria")
        derivative_initial=margin_velocity(system,a0,keys)
        derivative_exit=None
        refined=None
        if first_mass is not None:
            exit_state=a0.copy()
            for _ in range(first_mass):
                exit_state=system.rk4(exit_state,DT)
            derivative_exit=margin_velocity(system,exit_state,keys)
            before=rows[max(0,first_mass-1)]["time_after_anchor"]
            after=rows[first_mass]["time_after_anchor"]
            half=a0.copy()
            refined_rows=[]
            for step in range(2*first_mass+1):
                if step in (max(0,2*first_mass-1),2*first_mass):
                    refined_rows.append(snapshot(system,half,keys,step*DT/2))
                if step<2*first_mass:half=system.rk4(half,DT/2)
            refined={"coarse_last_pass_time":before,"coarse_first_fail_time":after,
                     "half_step_rows":refined_rows,
                     "mass_fraction_difference_at_coarse_exit":
                     abs(rows[first_mass]["absolute_mass_fraction"]-
                         refined_rows[-1]["absolute_mass_fraction"])}
        result["states"][name]={
            "samples":rows,"first_mass_failure_index":first_mass,
            "first_any_failure_index":first_any,
            "margin_velocity_initial":derivative_initial,
            "margin_velocity_at_first_mass_exit":derivative_exit,
            "half_step_exit_check":refined,
            "static_gate_pass":rows[0]["passes_preregistered_consistency_criteria"],
            "all_samples_through_t001_pass_mass":
                all(x["mass_gate_pass"] for x in rows[:11]),
            "mass_exit_in_frozen_window":
                (first_mass is not None and .0015<=rows[first_mass]["time_after_anchor"]<=.0030),
            "signed_gate_at_first_mass_exit":(
                None if first_mass is None else bool(
                    rows[first_mass]["same_sign_as_channel_total"] is True and
                    .8<=rows[first_mass]["signed_share_of_channel_total"]<=1.2)),
            "initial_margin_rate_positive":
                derivative_initial["rates"]["1e-08"]["full"]["margin_central"]>0,
            "exit_full_radial_polarization_rates_negative":(
                None if derivative_exit is None else all(
                    derivative_exit["rates"]["1e-08"][part]["margin_central"]<0
                    for part in ("full","radial_magnitude","vector_polarization"))),
        }
        print("N16",name,"static",result["states"][name]["static_gate_pass"],
              "first mass exit",None if first_mass is None else rows[first_mass]["time_after_anchor"],
              flush=True)
    out_path.parent.mkdir(parents=True,exist_ok=True)
    tmp=out_path.with_name(out_path.name+".tmp")
    tmp.write_text(json.dumps(result,indent=2)+"\n")
    tmp.replace(out_path)
    print("SAVED",out_path,flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("n15-json","n16-json","source-json","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    run(a.n15_json,a.n16_json,a.source_json,a.output)
