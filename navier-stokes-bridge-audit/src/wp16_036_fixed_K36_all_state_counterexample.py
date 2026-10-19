"""Construct arbitrary finite Galerkin states outside the selected K36 family."""

import argparse
import gzip
import json
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from wp16_036_N12_frozen_K36_holdout import K, P, Q, frozen_keys, k_channel_grouped, orbit


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-json-gz", type=Path, required=True)
    args = p.parse_args()
    source = json.loads(gzip.open(args.source_json_gz, "rt").read())
    keys = set(frozen_keys(source))
    system = System(N=7, nu=0.1)
    rng = np.random.default_rng(20260926)
    forbidden = {P, Q, K, tuple(-x for x in P), tuple(-x for x in Q), tuple(-x for x in K)}
    l, r = (-1, 0, 3), (7, 0, 0)
    assert tuple(l[i] + r[i] for i in range(3)) == K
    assert l in system.index and r in system.index
    assert l not in forbidden and r not in forbidden
    assert (orbit(l), orbit(r)) not in keys and (orbit(r), orbit(l)) not in keys

    def transverse(k):
        v = system.projectors[system.index[k]] @ (rng.normal(size=3) + 1j*rng.normal(size=3))
        return v / np.linalg.norm(v)

    vectors = {k:transverse(k) for k in (P,Q,K,l,r)}

    def state(L):
        a = np.zeros((len(system.modes),3),complex)
        for k,v0 in vectors.items():
            v = (L if k in (l,r) else 1.0)*v0
            a[system.index[k]] = v
            a[system.index[tuple(-x for x in k)]] = np.conj(v)
        return a

    results = []
    for L in (1.0,10.0,100.0):
        a = state(L)
        groups,total,absolute = k_channel_grouped(system,a)
        inside = sum(abs(groups.get(k,0.0)) for k in keys)
        assert np.max(np.linalg.norm(a[system.neg]-np.conj(a),axis=1)) < 1e-12
        assert np.max(abs(np.einsum('ij,ij->i',system.waves,a))) < 1e-12
        results.append({"L":L,"inside_fraction":inside/absolute,"inside_absolute":inside,
                        "outside_absolute":absolute-inside,"total_signed":total})
    assert results[-1]["inside_fraction"] < 0.01
    print(json.dumps({"N":7,"seed":20260926,"l":l,"r":r,"results":results},indent=2))


if __name__ == "__main__":
    main()
