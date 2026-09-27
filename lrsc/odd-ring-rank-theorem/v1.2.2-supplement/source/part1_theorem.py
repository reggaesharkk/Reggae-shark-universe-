#!/usr/bin/env python3
"""Independent recomputation of the LRSC odd-ring rank theorem (v1.2).
Written from the stated definitions only; does not import or copy the repo's code."""
import itertools, math
import numpy as np
import mpmath as mp

mp.mp.dps = 50

# ---------- 1. shedding field: direct local-min vs closed form (50-digit) ----------
def j_direct_mp(M, A):
    k = (M - 1) // 2
    X = [1 + A * mp.cos(2 * mp.pi * k * t / M) for t in range(M)]
    return [X[t] - min(X[(t - 1) % M], X[t], X[(t + 1) % M]) for t in range(M)]

def j_closed_mp(M, A):
    a = mp.pi / M; k = (M - 1) // 2; out = []
    for t in range(M):
        u = t if t <= k else M - t
        if u % 2: out.append(mp.mpf(0))
        elif u == 0: out.append(A * (1 + mp.cos(a)))
        else: out.append(A * (mp.cos(u * a) + mp.cos((u - 1) * a)))
    return out

worst = mp.mpf(0)
for M in list(range(9, 202, 2)) + [255, 299, 301, 401, 999]:
    for A in (mp.mpf('0.5'), mp.mpf('0.013'), mp.mpf(7)):
        d = max(abs(x - y) for x, y in zip(j_direct_mp(M, A), j_closed_mp(M, A)))
        worst = max(worst, d)
print(f"[1] shedding field closed form vs direct local-min, 50 digits: max diff = {mp.nstr(worst, 5)}")

# ---------- 2. Fourier closed forms B_r (both residue classes) vs direct DFT ----------
def B_closed(M, r):
    a = mp.pi / M; eps = -1 if r % 2 else 1
    D = mp.sin((2 * r - 1) * a) * mp.sin((2 * r + 1) * a)
    if M % 4 == 3:
        return -mp.sin(2 * a) * (eps * mp.cos(r * a) + mp.sin(a / 2)) / (2 * D)
    return -mp.sin(a) * (eps * mp.cos(r * a) * mp.cos(2 * r * a) + mp.cos(a) * mp.sin(a / 2)) / D

def jhat_direct(M, A, r, j):
    return mp.fsum(j[t] * mp.cos(2 * mp.pi * r * t / M) for t in range(M)) / M

maxrel = mp.mpf(0); count = 0; minabsB = (mp.inf, None)
A = mp.mpf('0.5')
for M in range(9, 302, 2):
    j = j_closed_mp(M, A); k = (M - 1) // 2
    for r in range(k):
        direct = jhat_direct(M, A, r, j)
        pred = 2 * A * mp.cos(mp.pi / M / 2) / M * B_closed(M, r)
        maxrel = max(maxrel, abs(direct - pred) / abs(direct))
        count += 1
print(f"[2] closed-form jhat_r vs direct 50-digit DFT: {count} coefficients (M=9..301, all 0<=r<k), "
      f"max relative diff = {mp.nstr(maxrel, 5)}")

# ---------- 3. each inequality step of the non-vanishing proof, large sweep (float) ----------
viol = []; worst_ratio = {"3mod4_odd_r": 9e9, "1mod4_low": 9e9, "1mod4_mid": 0, "1mod4_high": 9e9}
for M in range(9, 40002, 2):
    a = math.pi / M; k = (M - 1) // 2
    if M % 4 == 3:
        r = np.arange(1, k, 2)
        ratio = np.cos(r * a) / math.sin(a / 2)
        worst_ratio["3mod4_odd_r"] = min(worst_ratio["3mod4_odd_r"], ratio.min())
        if ratio.min() <= 1: viol.append(M)
    else:
        L = (M - 1) // 4; c = math.cos(a) * math.sin(a / 2)
        g = np.abs(np.cos(np.arange(k) * a) * np.cos(2 * np.arange(k) * a)) / c
        lo, mid, hi = g[:L], g[L], g[L + 1:2 * L]
        worst_ratio["1mod4_low"] = min(worst_ratio["1mod4_low"], lo.min())
        worst_ratio["1mod4_mid"] = max(worst_ratio["1mod4_mid"], mid)
        if hi.size: worst_ratio["1mod4_high"] = min(worst_ratio["1mod4_high"], hi.min())
        if lo.min() <= 1 or mid >= 1 or (hi.size and hi.min() <= 1): viol.append(M)
print(f"[3] inequality chain on every odd M=9..40001: violations = {viol}")
print("    worst ratios (need >1, <1, >1, >1): " + ", ".join(f"{k}={v:.4f}" for k, v in worst_ratio.items()))

# ---------- 4. rank(V) = p for every reflection-symmetric mask on small rings ----------
def channels(M, A, mask):
    k = (M - 1) // 2
    t = np.arange(M)
    X = 1 + A * np.cos(2 * np.pi * k * t / M)
    j = X - np.minimum(np.minimum(np.roll(X, 1), X), np.roll(X, -1))
    jh = np.fft.fft(j).real / M
    W = np.zeros((M, k + 1))
    W[:, 0] = mask * jh[0]
    for r in range(1, k + 1):
        W[:, r] = mask * 2 * jh[r] * np.cos(2 * np.pi * r * t / M)
    s = np.cos(2 * np.pi * np.arange(M) / M) - 1
    V = np.real(np.fft.ifft(s[:, None] * np.fft.fft(W, axis=0), axis=0))
    return W, V, jh

def numrank(Mx, tol=1e-9):
    sv = np.linalg.svd(Mx, compute_uv=False)
    if sv[0] == 0: return 0, sv
    return int((sv > tol * sv[0]).sum()), sv

tot = ok = 0; min_gap_in = 1.0; max_gap_out = 0.0; allact = []
for M in (9, 11, 13, 15, 17, 19, 21, 23, 25):
    k = (M - 1) // 2
    for bits in itertools.product((0, 1), repeat=k + 1):
        mask = np.array([bits[min(t, M - t)] for t in range(M)], float)
        p = sum(bits)
        W, V, _ = channels(M, 0.5, mask)
        rW, _ = numrank(W); rV, sv = numrank(V)
        if p <= k:
            tot += 1; ok += (rW == p and rV == p)
            if p: min_gap_in = min(min_gap_in, sv[p - 1] / sv[0])
            if p < len(sv) and sv[0] != 0: max_gap_out = max(max_gap_out, sv[p] / sv[0])
        else:
            allact.append((M, p, rW, rV))
print(f"[4] exhaustive masks with >=1 inactive orbit, M=9..25: {ok}/{tot} have rank(W)=rank(V)=p")
print(f"    smallest kept sigma ratio {min_gap_in:.2e}  vs largest discarded ratio {max_gap_out:.2e}")
print(f"    all-active mask (outside theorem): (M, p, rank W, rank V) = {allact}")

# ---------- 5. benchmark rings with the stress mask ----------
for M in (99, 101, 127):
    k = (M - 1) // 2; t = np.arange(M); A = 0.5; theta = 0.08
    X = 1 + A * np.cos(2 * np.pi * k * t / M)
    C = 0.5 * ((X - np.roll(X, 1)) ** 2 + (X - np.roll(X, -1)) ** 2)
    mask = (C > theta).astype(float)
    orbits = {min(i, M - i) for i in np.nonzero(mask)[0]}
    W, V, jh = channels(M, A, mask)
    rV, sv = numrank(V)
    p = len(orbits)
    print(f"[5] M={M}: active nodes={int(mask.sum())}, active orbits p={p}, rank(V)={rV}, "
          f"sigma_p/sigma_1={sv[p-1]/sv[0]:.2e}, sigma_(p+1)/sigma_1={sv[p]/sv[0]:.2e}")

# ---------- 6. random masks on M=99, 101, 127 ----------
rng = np.random.default_rng(1); bad = 0; n = 0
for M in (99, 101, 127):
    k = (M - 1) // 2
    for _ in range(300):
        bits = rng.integers(0, 2, k + 1)
        if bits.sum() == k + 1: bits[rng.integers(k + 1)] = 0
        mask = np.array([bits[min(t, M - t)] for t in range(M)], float)
        _, V, _ = channels(M, 0.5, mask)
        n += 1; bad += (numrank(V, 1e-11)[0] != bits.sum())
print(f"[6] random masks on M=99/101/127: {n - bad}/{n} with rank(V)=p")
