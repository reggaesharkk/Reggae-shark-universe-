#!/usr/bin/env python3
"""WP19 consecutive-cutoff bridge diagnostic.

NON-RIGOROUS scouting version: node sampled only.
The proof version must replace node sampling by whole-segment Arb/Bernstein
enclosures on each cubic-Hermite segment.

Uses only the LOWER-cutoff predictor path.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np

def l2(a):
    return float(np.sqrt(np.sum(np.abs(a)**2)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--predictor-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()

    repo=args.repo.resolve()
    pred=args.predictor_dir.resolve()
    sys.path.insert(0,str(repo/"src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    meta=json.loads((pred/"metadata.json").read_text())
    N=int(meta["N"])
    nu=float(meta.get("nu_exact_decimal","0.1"))
    h=float(meta.get("h_exact_decimal","0.000025"))
    nodes=np.load(pred/"nodes.npy",mmap_mode="r")

    low=DealiasedSystem(N=N,nu=nu)
    high=DealiasedSystem(N=N+1,nu=nu)

    if nodes.shape[1] != len(low.modes):
        raise ValueError("predictor mode count mismatch")

    low_to_high=np.array([high.index[k] for k in low.modes],dtype=np.int64)
    new_mask=np.array([k not in low.index for k in high.modes],dtype=bool)

    rows=[]
    E=0.0
    for j in range(nodes.shape[0]):
        a=np.asarray(nodes[j])
        ah=np.zeros((len(high.modes),3),dtype=np.complex128)
        ah[low_to_high]=a

        bh=high.nonlinear(ah)
        H=l2(bh[new_mask])

        mode_norm=np.sqrt(np.sum(np.abs(a)**2,axis=1))
        M=float(np.sum(np.sqrt(low.square)*mode_norm))
        S=M/np.sqrt(2.0)

        if j < nodes.shape[0]-1:
            E=np.exp(S*h)*(E+h*H)

        rows.append({
            "node":j,
            "time":j*h,
            "new_shell_force_L2_sampled":H,
            "gradient_fourier_l1_sampled":M,
            "symmetric_strain_majorant_sampled":S,
            "propagated_sampled_E_like":E,
        })

    result={
        "schema":"wp19-consecutive-cutoff-bridge-diagnostic-v0.1",
        "status":"NON-RIGOROUS NODE-SAMPLED SCOUTING ONLY",
        "lower_cutoff_N":N,
        "upper_cutoff_N":N+1,
        "nu":nu,
        "h":h,
        "node_count":len(rows),
        "new_mode_count":int(new_mask.sum()),
        "max_sampled_shell_force_L2":max(r["new_shell_force_L2_sampled"] for r in rows),
        "max_sampled_symmetric_strain_majorant":max(r["symmetric_strain_majorant_sampled"] for r in rows),
        "terminal_sampled_recurrence_value":rows[-1]["propagated_sampled_E_like"],
        "rigorous_next_step":"Whole-segment Arb/Bernstein enclosure of the new-shell forcing.",
        "rows":rows,
    }
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},indent=2))

if __name__=="__main__":
    main()
