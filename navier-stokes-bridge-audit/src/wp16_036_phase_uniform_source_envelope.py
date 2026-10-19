"""Exact per-ordered-source magnitude envelope invariant under phase rotations."""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from wp16_036_N12_frozen_K36_holdout import K, P, Q, frozen_keys, get_row, k_channel_grouped, orbit, reconstruct


def envelope(system,a):
    pi,qi,ki=(system.index[k] for k in (P,Q,K))
    B=system.projectors[ki]@(1j*np.dot(np.asarray(Q,float),a[pi])*a[qi])
    z=-float(system.square[ki]**2)*np.vdot(a[ki],B)
    assert abs(z)>1e-30
    groups=defaultdict(float)
    for idx in np.nonzero(system.out==ki)[0]:
        li,ri=int(system.left[idx]),int(system.right[idx])
        raw=1j*np.dot(system.waves[ri],a[li])*a[ri]
        dak=-(system.projectors[ki]@raw)
        dz=-float(system.square[ki]**2)*np.vdot(dak,B)
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]+=float(abs(dz/z))
    return groups


def shell(k):
    radius=max(math.sqrt(sum(x*x for x in v)) for v in k)
    return "<8" if radius<8 else "8-10" if radius<10 else "10-12" if radius<12 else "12-13"


def main():
    p=argparse.ArgumentParser()
    for name in ("n11-json","n12-json","n13-json","source-json","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    j11=json.loads(a.n11_json.read_text());j12=json.loads(a.n12_json.read_text());j13=json.loads(a.n13_json.read_text())
    source=json.loads(a.source_json.read_text());keys=set(frozen_keys(source))
    result={"status":"conditional phase-uniform per-source magnitude envelope", "N":{}}
    for N,prev,curr in ((12,get_row(j11,11),get_row(j12,12)),(13,get_row(j12,12),get_row(j13,13))):
        print("RECONSTRUCT",N,flush=True)
        system,states=reconstruct(prev,curr)
        reference=None
        for name,state in states.items():
            groups=envelope(system,state)
            if reference is None:
                reference=groups
            else:
                assert groups.keys()==reference.keys()
                assert all(math.isclose(v,reference[k],rel_tol=1e-12,abs_tol=1e-10) for k,v in groups.items())
            signed,_,_=k_channel_grouped(system,state)
            assert all(abs(v)<=groups[k]+1e-10 for k,v in signed.items())
            print("ENVELOPE",N,name,flush=True)
        shells=defaultdict(float)
        for key,v in reference.items():
            if key not in keys:shells[shell(key)]+=v
        result["N"][str(N)]={
            "outside_envelope_total":sum(v for k,v in reference.items() if k not in keys),
            "K36_envelope_total":sum(v for k,v in reference.items() if k in keys),
            "outside_envelope_by_shell":dict(shells),
            "outside_group_envelopes_ranked":[
                {"left_orbit":list(k[0]),"right_orbit":list(k[1]),"phase_uniform_upper_bound":v}
                for k,v in sorted(((k,v) for k,v in reference.items() if k not in keys),key=lambda kv:-kv[1])
            ],
        }
        print("SHELLS",N,dict(shells),flush=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("SAVED",a.output,flush=True)


if __name__=="__main__":main()
