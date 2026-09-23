#!/usr/bin/env python3
"""Memory-safe exhaustive cardinality 1..10 audit for the stated M=99 LRSC operator.

Requires Python 3, NumPy, and a C++17 compiler (g++ by default). The search
enumerates all combinations in compiled code and never materializes them.
The result is a numerical exhaustive certificate, not an interval proof.
"""
from __future__ import annotations

import ctypes
import math
import os
from pathlib import Path
import subprocess

import numpy as np

M, K_IDX, THETA, A = 99, 49, 0.08, 0.50
K_MAX = 10


class Result(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_uint64),
        ("best", ctypes.c_double),
        ("second", ctypes.c_double),
        ("best_indices", ctypes.c_int * 10),
        ("second_indices", ctypes.c_int * 10),
    ]


def operator_arrays():
    i = np.arange(M)
    k = 2.0 * np.pi * K_IDX / M
    x = 1.0 + A * np.cos(k * i)
    left, right = np.roll(x, 1), np.roll(x, -1)
    j = x - np.minimum(np.minimum(left, x), right)
    stress = 0.5 * ((x - left) ** 2 + (x - right) ** 2)
    mask = (stress > THETA).astype(float)

    hm = np.fft.fft(mask) / M
    hj = np.fft.fft(j) / M
    hy = np.fft.fft(mask * j) / M
    q = np.arange(M)
    stencil = np.cos(2.0 * np.pi * q / M) - 1.0
    target = stencil * hy
    norm_target = np.linalg.norm(target)

    # Rows V_r are the displayed scalar DC channel and conjugate-balanced
    # channel pairs, in the same normalized DFT convention as target.
    V = np.zeros((M // 2 + 1, M), dtype=np.complex128)
    V[0] = stencil * (hj[0] * np.roll(hm, 0))
    for r in range(1, M // 2 + 1):
        rc = M - r
        V[r] = stencil * (
            hj[r] * np.roll(hm, r) + hj[rc] * np.roll(hm, rc)
        )

    closure = np.linalg.norm(target - V.sum(axis=0)) / norm_target
    # The norm on C^M equals the real dot product on concatenated real/imag.
    E = np.concatenate((target.real, target.imag))
    R = np.concatenate((V.real, V.imag), axis=1)
    c = float(E @ E)
    f = np.asarray(-2.0 * (R @ E), dtype=np.float64)
    gram = np.asarray(R @ R.T, dtype=np.float64)
    return x, j, mask, target, V, norm_target, closure, c, f, gram


def direct_error(target, V, norm_target, subset):
    residual = target - np.sum(V[list(subset)], axis=0)
    return float(np.linalg.norm(residual) / norm_target)


def main():
    source = Path(__file__).with_name("exhaustive_search.cpp")
    lib_path = Path(__file__).with_name("exhaustive_search.so")
    compiler = os.environ.get("CXX", "g++")
    subprocess.run(
        [compiler, "-O3", "-std=c++17", "-shared", "-fPIC", str(source), "-o", str(lib_path)],
        check=True,
    )
    lib = ctypes.CDLL(str(lib_path))
    lib.exhaustive_search.argtypes = [ctypes.c_int,
        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double]
    lib.exhaustive_search.restype = Result

    _, _, mask, target, V, norm_target, closure, c, f, gram = operator_arrays()
    f_c = f.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    q_c = gram.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    results = {}
    for cardinality in range(1, K_MAX + 1):
        found = lib.exhaustive_search(cardinality, f_c, q_c, c)
        best = tuple(int(found.best_indices[t]) for t in range(cardinality))
        second = tuple(int(found.second_indices[t]) for t in range(cardinality))
        best_direct = direct_error(target, V, norm_target, best)
        second_direct = direct_error(target, V, norm_target, second)
        expected = math.comb(50, cardinality)
        print(f"K={cardinality}: expected={expected}; visited={found.count}; best_subset={best}; direct_error={best_direct:.17g}; second_error={second_direct:.17g}; threshold_pass={best_direct <= 0.001}", flush=True)
        if found.count != expected:
            raise SystemExit(f"FAIL at K={cardinality}: enumerated {found.count}, expected {expected}")
        if abs(best_direct - math.sqrt(max(0.0, found.best)) / norm_target) > 2e-12:
            raise SystemExit(f"FAIL at K={cardinality}: direct-vector check disagrees with Gram score")
        results[cardinality] = (best_direct, best, found)

    found = results[7][2]
    best = results[7][1]
    best_direct = results[7][0]
    second = tuple(int(found.second_indices[t]) for t in range(7))
    second_direct = direct_error(target, V, norm_target, second)
    claimed_a = (0, 1, 2, 46, 47, 48, 49)
    claimed_b = (0, 1, 3, 46, 47, 48, 49)
    archived = (0, 1, 45, 46, 47, 48, 49)

    print("LRSC K=1..10 MEMORY-SAFE EXHAUSTIVE AUDIT")
    print(f"M={M}; k_idx={K_IDX}; theta={THETA}; A={A}; channels=50; N_act={int(mask.sum())}")
    print(f"closure_relative={closure:.17g}")
    print(f"K7_combinations_expected={math.comb(50, 7)}; K7_combinations_visited={found.count}")
    print(f"K7_global_min_subset={best}; quadratic_squared_residual={found.best:.17g}")
    print(f"K7_global_min_direct_error={best_direct:.17g}; percent={100*best_direct:.15g}%")
    print(f"K7_second_subset={second}; K7_second_direct_error={second_direct:.17g}")
    print(f"K7_quadratic_objective_gap={found.second-found.best:.17g}")
    for label, subset in [("Google_claim_A", claimed_a), ("Google_claim_B", claimed_b), ("archived_v1_0", archived)]:
        print(f"{label}_subset={subset}; direct_error={direct_error(target,V,norm_target,subset):.17g}")
    k8_error, k8_subset, k8_result = results[8]
    print(f"K8_best_subset={k8_subset}; K8_direct_error={k8_error:.17g}; K8_runner_up_error={direct_error(target,V,norm_target,tuple(int(k8_result.second_indices[t]) for t in range(8))):.17g}")
    k10_error, k10_subset, k10_result = results[10]
    print(f"K10_best_subset={k10_subset}; K10_direct_error={k10_error:.17g}; K10_runner_up_error={direct_error(target,V,norm_target,tuple(int(k10_result.second_indices[t]) for t in range(10))):.17g}")
    k11_witness = (0, 1, 3, 42, 43, 44, 45, 46, 47, 48, 49)
    k11_error = direct_error(target, V, norm_target, k11_witness)
    print(f"K11_witness={k11_witness}; K11_witness_direct_error={k11_error:.17g}; threshold_pass={k11_error <= 0.001}")
    print(f"K0_empty_subset_error=1.0")
    first_pass = next((card for card, (err, _, _) in results.items() if err <= 0.001), None)
    print(f"first_exact_cardinality_passing_0.001={first_pass}")
    print(f"threshold_0.001_pass_at_K7={best_direct <= 0.001}; threshold_0.001_pass_at_K8={k8_error <= 0.001}; threshold_0.001_pass_at_K10={k10_error <= 0.001}")
    print("STATUS=PASS (all subsets for K=1..10 enumerated; finite-precision numerical certificate only)")


if __name__ == "__main__":
    main()
