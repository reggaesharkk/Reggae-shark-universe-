#!/usr/bin/env python3
"""WP19 sampled physical-space symmetric-strain diagnostic.

NON-RIGOROUS scouting tool. It evaluates ||S(u_N)|| on a finite dealiased
physical grid at saved predictor nodes. The result is not a certified
continuum L-infinity supremum; it is used only to locate proof loss.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np

def sampled_strain(repo: Path, N: int, nodes_path: Path):
    sys.path.insert(0, str(repo / "src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem
    s = DealiasedSystem(N, nu=0.1)
    nodes = np.load(nodes_path, mmap_mode="r")
    vals = []
    for a in nodes:
        f = np.zeros((s.L, s.L, s.L, 3), complex)
        f[s.slots] = a
        grads = []
        for j in range(3):
            grad = np.fft.ifftn(
                1j * s.waves_grid(j)[..., None] * f,
                axes=(0, 1, 2),
            ) * s.L**3
            grads.append(grad.real)
        G = np.stack(grads, axis=-1)
        S = 0.5 * (G + np.swapaxes(G, -1, -2))
        fro = np.sqrt(np.sum(S * S, axis=(-2, -1)))
        vals.append(float(np.max(fro)))
    return s.L, vals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--nodes", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    L, vals = sampled_strain(args.repo.resolve(), args.N, args.nodes.resolve())
    result = {
        "N": args.N,
        "grid_L": L,
        "status": (
            "sampled physical-grid Frobenius strain upper bound on operator norm "
            "at grid points; NOT continuum supremum"
        ),
        "values": vals,
        "max": max(vals),
        "avg": sum(vals[:-1]) / len(vals[:-1]),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "values"}, indent=2))

if __name__ == "__main__":
    main()
