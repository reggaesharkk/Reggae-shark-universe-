#!/usr/bin/env python3
# Usage: g++ -O3 -o bnb bnb.cpp && python3 part2_build.py && python3 run_bnb.py 0.08 1,2,3,4,5,6,7,8,9,10,11 pca
# Args: theta cell (0.07 | 0.08 | 0.09), comma-separated K list, basis (pca | even).
import json, sys, subprocess, math, itertools
import numpy as np

data = json.load(open("bench_vectors.json"))
TAU = 1e-3

def even_coords(x):
    x = np.asarray(x); M = len(x); k = (M - 1) // 2
    assert np.max(np.abs(x[1:k + 1] - x[::-1][:k])) < 1e-13
    return np.concatenate(([x[0]], math.sqrt(2) * x[1:k + 1]))

def prepare(theta, basis):
    d = data[theta]
    E = even_coords(d["E"]); V = np.array([even_coords(v) for v in d["V"]])
    c = float(E @ E)
    if basis == "pca":
        _, _, Vt = np.linalg.svd(V, full_matrices=True)
        E, V = Vt @ E, V @ Vt.T
    return E, V, c

def local_search(E, V, K, restarts=60, seed=0):
    rng = np.random.default_rng(seed); n = len(V); bestv, bests = np.inf, None
    for rep in range(restarts):
        if rep == 0:
            S = []
            for _ in range(K):
                P = V[S].sum(0) if S else 0
                S.append(min((i for i in range(n) if i not in S),
                             key=lambda i: np.sum((E - P - V[i]) ** 2)))
        else:
            S = list(rng.choice(n, K, replace=False))
        val = np.sum((E - V[S].sum(0)) ** 2)
        improved = True
        while improved:
            improved = False
            P = V[S].sum(0)
            for a in range(K):
                for b in range(n):
                    if b in S: continue
                    v = np.sum((E - P + V[S[a]] - V[b]) ** 2)
                    if v < val - 1e-18:
                        S[a] = b; val = v; improved = True; break
                if improved: break
        if val < bestv: bestv, bests = val, sorted(int(i) for i in S)
    return bestv, bests

def run(theta, K, basis="pca", order="norm"):
    E, V, c = prepare(theta, basis)
    n = len(V)
    ub, heur = local_search(E, V, K)
    perm = np.argsort(-np.linalg.norm(V, axis=1)) if order == "norm" else np.arange(n)
    Vp = V[perm]
    with open("/tmp/bnb_in.txt", "w") as f:
        f.write(f"{n} {len(E)} {K} {ub * (1 + 1e-9):.17e}\n")
        f.write(" ".join(f"{x:.17e}" for x in E) + "\n")
        for row in Vp: f.write(" ".join(f"{x:.17e}" for x in row) + "\n")
        f.write(" ".join(str(int(i)) for i in perm) + "\n")
    out = subprocess.run(["./bnb", "/tmp/bnb_in.txt"], capture_output=True, text=True).stdout
    return out, c, ub, heur

if __name__ == "__main__":
    theta = sys.argv[1]; Ks = [int(x) for x in sys.argv[2].split(",")]
    basis = sys.argv[3] if len(sys.argv) > 3 else "pca"
    for K in Ks:
        out, c, ub, heur = run(theta, K, basis)
        line = out.strip().splitlines()
        minR2 = float(line[1].split()[0].split("=")[1]) if len(line) > 1 and line[1].startswith("min_R2") else float("nan")
        rel = math.sqrt(minR2 / c)
        print(f"theta={theta} K={K}: {line[0]}")
        print(f"    {line[1] if len(line)>1 else ''}")
        print(f"    exact min relative residual = {rel:.12f}   pass(<=1e-3)={rel <= TAU}   "
              f"(local-search start {math.sqrt(ub/c):.12f} {heur})", flush=True)
