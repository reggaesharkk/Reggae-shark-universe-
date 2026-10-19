"""Exploratory phase-torus probe at fixed N13 evolved Fourier magnitudes."""

import argparse
import json
from pathlib import Path

import numpy as np

from wp16_036_N12_frozen_K36_holdout import (
    active_pairs, frozen_keys, get_row, k_channel_grouped, phase_rotate, reconstruct,
)


def main():
    p=argparse.ArgumentParser()
    for name in ("n12-json","n13-json","source-json","output"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--draws",type=int,default=64)
    a=p.parse_args()
    n12=json.loads(a.n12_json.read_text());n13=json.loads(a.n13_json.read_text())
    src=json.loads(a.source_json.read_text());keys=frozen_keys(src)
    system,states=reconstruct(get_row(n12,12),get_row(n13,13))
    base=states["inherited"]
    pairs=active_pairs(system,base)
    rng=np.random.default_rng(20260926)
    results=[]
    for i in range(a.draws):
        phases=rng.uniform(-np.pi,np.pi,len(pairs))
        state=phase_rotate(base,pairs,phases)
        groups,total,total_abs=k_channel_grouped(system,state)
        signed=sum(groups.get(k,0.0) for k in keys)
        inside_abs=sum(abs(groups.get(k,0.0)) for k in keys)
        frac=inside_abs/total_abs
        share=signed/total if abs(total)>1e-30 else None
        passed=(signed*total>0 and frac>=0.90 and share is not None and 0.80<=share<=1.20)
        results.append({"draw":i,"fraction":frac,"signed_share":share,"total_signed":total,"pass":passed})
        if (i+1)%8==0:print("DRAW",i+1,"MIN",min(r["fraction"] for r in results),flush=True)
    payload={"status":"exploratory random phase probe, not a frozen holdout",
             "N":13,"seed":20260926,"draws":a.draws,"active_pairs":len(pairs),
             "pass_count":sum(r["pass"] for r in results),
             "min_abs_fraction":min(r["fraction"] for r in results),
             "max_abs_fraction":max(r["fraction"] for r in results),
             "results":results}
    a.output.write_text(json.dumps(payload,indent=2)+"\n")
    print("SAVED",a.output,"PASS",payload["pass_count"],"/",a.draws,flush=True)


if __name__=="__main__":main()
