#!/usr/bin/env python3
"""Independent real-space construction of the M=99 LRSC benchmark at 50 digits.
Target E = S(m*j), channels V_r = S(m*w_r), with w_0 = jhat_0, w_r = 2 jhat_r cos(2 pi r t/M).
Norms are divided by M so they match the repo's normalized-DFT convention (Parseval)."""
import sys, json
import mpmath as mp
mp.mp.dps = 50

M, KIDX = 99, 49
A = mp.mpf(1) / 2
t_all = range(M)
X = [1 + A * mp.cos(2 * mp.pi * KIDX * t / M) for t in t_all]
C = [((X[t] - X[t - 1]) ** 2 + (X[t] - X[(t + 1) % M]) ** 2) / 2 for t in t_all]
J = [X[t] - min(X[t - 1], X[t], X[(t + 1) % M]) for t in t_all]
jh = [mp.fsum(J[t] * mp.cos(2 * mp.pi * r * t / M) for t in t_all) / M for r in range(M)]
cosT = [[mp.cos(2 * mp.pi * r * t / M) for t in t_all] for r in range(50)]

def stencil(x):
    return [(x[(t + 1) % M] + x[t - 1]) / 2 - x[t] for t in t_all]

def build(theta):
    m = [1 if C[t] > theta else 0 for t in t_all]
    E = stencil([m[t] * J[t] for t in t_all])
    V = [stencil([m[t] * jh[0] for t in t_all])]
    for r in range(1, 50):
        V.append(stencil([m[t] * 2 * jh[r] * cosT[r][t] for t in t_all]))
    return m, E, V

def sq(x): return mp.fsum(v * v for v in x) / M

def rel_resid(E, V, S):
    R = [E[t] - mp.fsum(V[i][t] for i in S) for t in t_all]
    return mp.sqrt(sq(R) / sq(E)), sq(R)

if __name__ == "__main__":
    assert max(abs(J[t] - J[(M - t) % M]) for t in t_all) < mp.mpf(10) ** -45
    inv = max(abs(J[t] - (jh[0] + 2 * mp.fsum(jh[r] * cosT[r][t] for r in range(1, 50)))) for t in t_all)
    print(f"Fourier inversion sum_r w_r = j: max err {mp.nstr(inv, 3)}")

    lev = sorted({(mp.nstr(C[t], 30), min(t, M - t)) for t in t_all}, key=lambda z: mp.mpf(z[0]))
    byorb = {}
    for t in t_all: byorb.setdefault(min(t, M - t), C[t])
    mono = all(byorb[u] > byorb[u + 1] for u in range(49))
    print(f"stress strictly decreasing in |t| over all 50 orbits: {mono}")
    for u in (38, 39, 40, 41, 42):
        print(f"   orbit |t|={u:2d} (nodes {u},{M-u}): stress = {mp.nstr(byorb[u], 20)}")

    out = {}
    for theta_s in ("0.07", "0.08", "0.09"):
        theta = mp.mpf(theta_s)
        m, E, V = build(theta)
        act = [t for t in t_all if m[t]]
        inact = [t for t in t_all if not m[t]]
        s_lo = max(C[t] for t in inact); s_hi = min(C[t] for t in act)
        c = sq(E)
        clos = mp.sqrt(sq([E[t] - mp.fsum(V[i][t] for i in range(50)) for t in t_all]) / c)
        print(f"\ntheta={theta_s}: active nodes={len(act)}, orbits={len({min(t,M-t) for t in act})}, "
              f"inactive={inact[0]}..{inact[-1]}")
        print(f"   mask cell = [{mp.nstr(s_lo, 25)}, {mp.nstr(s_hi, 25)})")
        print(f"   c=||E||^2 = {mp.nstr(c, 20)}   closure |E-sum V|/|E| = {mp.nstr(clos, 3)}")
        out[theta_s] = dict(E=[float(x / mp.sqrt(M)) for x in E],
                            V=[[float(x / mp.sqrt(M)) for x in v] for v in V],
                            c=float(c), cell=[float(s_lo), float(s_hi)])
        wit = {"0.08": [(0, 1, 3, 42, 43, 44, 45, 46, 47, 48, 49), (0, 1, 42, 43, 44, 45, 46, 47, 48, 49)],
               "0.09": [(0, 1, 3, 42, 43, 44, 45, 46, 47, 48, 49), (0, 1, 3, 41, 42, 43, 44, 45, 46, 47, 48, 49)],
               "0.07": [(0, 1, 2, 4, 5, 6, 42, 43, 44, 45, 46, 47, 48, 49),
                        (0, 1, 3, 11, 12, 13, 14, 42, 43, 44, 45, 46, 47, 48, 49)]}[theta_s]
        for S in wit:
            rr, r2 = rel_resid(E, V, S)
            print(f"   |S|={len(S):2d} {S}: rel residual = {mp.nstr(rr, 15)}  pass={rr <= mp.mpf('0.001')}")
    json.dump(out, open("bench_vectors.json", "w"))
    print("\nexported float64 vectors to bench_vectors.json")
