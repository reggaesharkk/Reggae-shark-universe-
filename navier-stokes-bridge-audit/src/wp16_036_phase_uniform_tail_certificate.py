"""Measure the phase-invariant constants in a conditional k-source tail bound."""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from wp16_036_N12_frozen_K36_holdout import K, P, Q, get_row, reconstruct


def constants(system, a):
    ip, iq, ik = (system.index[x] for x in (P,Q,K))
    weight = float(system.square[ik]**2)
    B = system.projectors[ik] @ (1j * np.dot(np.asarray(Q,float),a[ip])*a[iq])
    overlap = abs(np.vdot(a[ik],B))
    assert overlap > 0
    z_abs = weight*overlap
    D = np.linalg.norm(B)/overlap
    M2 = float(np.sum((system.square.astype(float)**2)[:,None]*abs(a)**2))
    return {"D":float(D),"M2":M2,"z_abs":float(z_abs),
            "anchor_coefficient_abs":float(np.linalg.norm(a[ik])),
            "anchor_cosine_abs":float(overlap/(np.linalg.norm(a[ik])*np.linalg.norm(B)))}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--n11-json",type=Path,required=True)
    p.add_argument("--n12-json",type=Path,required=True)
    p.add_argument("--n13-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    j11=json.loads(a.n11_json.read_text()); j12=json.loads(a.n12_json.read_text()); j13=json.loads(a.n13_json.read_text())
    result={"status":"post-hoc conditional phase-uniform tail constants", "rows":{}}
    for N,prev,curr in ((12,get_row(j11,11),get_row(j12,12)),(13,get_row(j12,12),get_row(j13,13))):
        print("RECONSTRUCT",N,flush=True)
        system,states=reconstruct(prev,curr)
        vals={name:constants(system,state) for name,state in states.items()}
        reference=vals["inherited"]
        for name,row in vals.items():
            for field in ("D","M2","z_abs","anchor_coefficient_abs","anchor_cosine_abs"):
                assert math.isclose(row[field],reference[field],rel_tol=1e-12,abs_tol=1e-12),(N,name,field)
        for R in (8,10,12):
            reference[f"R{R}_high_shell_upper_bound"] = reference["D"]*reference["M2"]/(R-math.sqrt(sum(x*x for x in K)))**3
        result["rows"][str(N)]={"constants_by_state":vals,"phase_uniform_bounds":reference}
        print("CONSTANTS",N,reference,flush=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("SAVED",a.output,flush=True)


if __name__=="__main__":
    main()
