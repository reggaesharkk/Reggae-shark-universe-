# WP19 v0.18 — N18 Stress Test and Parallel Arb Escalation

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** same-datum floating N18 stress test plus launch of parallel N15–N18 Arb validation.  
**Not claimed:** N15–N18 certification until the matrix jobs pass; geometric decay theorem; all-N result; continuum regularity; blowup.

The unchanged same datum was evolved at N18 with `nu=0.1`, `T=0.003`, `h=0.000025`, 120 steps, and no retuning.

The N18 endpoint is approximately

[
F_{18}(T)=-86.429657697,
qquad
G_{C500,18}(T)=-50.150121025.
]

The C500 sequence is therefore

[
-52.84146,;-50.62254,;-50.22688,;-50.12304,;-50.15012
]

for N14 through N18. The N17→N18 increment changes sign. Thus a monotone-in-N story is false.

The more relevant observation is that the magnitudes of successive G corrections are

[
2.21891809,;0.39566619,;0.10384260,;0.02708500,
]

with ratios approximately

[
0.1783,;0.2625,;0.2608.
]

The endpoint P11 drift continues to shrink:

[
1.5767	imes10^{-2},
;8.5441	imes10^{-3},
;3.2720	imes10^{-3},
;9.2681	imes10^{-4}.
]

The newly opened shell endpoint L2 norms are

[
0.13645,;0.10239,;0.06831,;0.04533.
]

The sampled L1_t L2_x total closure differences are

[
0.0171592,;0.0090698,;0.0035002,;0.0009968,
]

with ratios approximately

[
0.529,;0.386,;0.285.
]

This is the exact recursive-closure quantity singled out by WP19 v0.12–v0.14. The observed decrease is a target for a proof, not the proof itself.

To reduce wall time, N15, N16, N17 and N18 whole-segment Arb validations were launched in parallel in GitHub Actions run `36669057015`. Each matrix job independently regenerates the unchanged same-datum predictor, computes 120 whole-segment 128-bit Arb enclosures, propagates the trajectory radius, checks the original K36 endpoint interval and whole-path normalizer, and uploads its result.

Archive SHA-256: `ad3678c4db7aa78b35e27574eb01044a0417c84a745d22e63893c810df7b365e`.

Drive file ID: `19pkWxPzj_w-fz6DlIo6TJnNsQPk3qoan`.

## Claim boundary

N18 remains a floating stress test until the parallel Arb job closes. The decreasing correction/closure sequence does not establish an infinite-tail bound.
