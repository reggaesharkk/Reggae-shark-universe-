# WP19 v0.21 — Certified same-datum chain N11–N18

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** finite-Galerkin computer-assisted certificate family.  
**Not claimed:** all-cutoff persistence, continuum regularity, finite-time singularity, or a Millennium-problem solution.

## Frozen problem

All eight certificates use the same fixed rational datum and the same observable:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- frozen K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- `nu = 0.1`
- `T = 0.003`
- `h = 0.000025`
- 120 whole-segment Arb residual/gradient enclosures at every cutoff
- no retuning between cutoffs; the N11 datum is embedded unchanged and new modes start at zero.

## Certified endpoint chain

| N | terminal L2 error upper | certified F(T) interval | whole-path normalizer lower | result |
|---:|---:|---:|---:|:---:|
| 11 | 0.000010526681 | [-54.748409847, -42.032667894] | > 48990.29795521 | PASS |
| 12 | 0.000011374869 | [-73.633221010, -70.396895629] | 49091.85228719 | PASS |
| 13 | 0.000012244529 | [-87.154087422, -83.563901281] | 48869.38355689 | PASS |
| 14 | 0.000012825905 | [-89.015834781, -85.160766265] | 48850.68586052 | PASS |
| 15 | 0.000013195722 | [-88.958192681, -84.896722370] | 48856.49133823 | PASS |
| 16 | 0.000013456103 | [-88.828357601, -84.589032046] | 48858.17452511 | PASS |
| 17 | 0.000013665541 | [-88.682140170, -84.277596371] | 48860.35300815 | PASS |
| 18 | 0.000013774643 | [-88.699660529, -84.159654865] | 48860.59568947 | PASS |

The common initial interval for N12–N18 is
`F(0) in [645.8037741471, 645.8037741472]`; the N11 exact initial sign is also positive.

Therefore the same frozen datum has a certified positive-to-negative sign crossing on `(0,0.003)` at every finite cutoff N=11,...,18.

A finite-range uniform statement also follows directly from the eight certificates:

- for every certified cutoff `11 <= N <= 18`, `F(T) <= -42.032667894 < 0`;
- the minimum recorded whole-path normalizer lower bound across the chain is `48850.68586052`;
- the maximum terminal trajectory-error upper bound is `0.000013774643`.

These are finite-range statements only.

## GitHub Actions provenance for N15–N18

Original matrix run: `36669057015`.

Artifact digests:

- N15: `sha256:824634cc562b7a958f2ce8ba94d2561a71aa1b8fcbdf2551f3b204f84b3d80c0`
- N16: `sha256:8e67a2de3b38338b0a61e9519f9433ba4684dc7957407d3f8b4b9c85cb8e034e`
- N17: `sha256:e38906e9ee170cfc8483ac7340df7c96ddcec8b2e33b2715e983b1dcf54387d2`

The original N18 matrix job reached the GitHub-hosted six-hour limit after preserving 99 completed segment certificates, `000..098`. Its partial artifact digest was:

`sha256:7399353fbf30e0c63c425b1c199db5042ea9d43e03131a846f7a1154edacd808`.

Recovery run `36706229638` verified those cached segment hashes against the preserved predictor arrays, computed only segments `099..119`, reran the global trajectory-error, endpoint-sign, and whole-path-normalizer gates, and returned PASS.

Recovered N18 artifact digest:

`sha256:72edeeaedc41516dda4c9745a079bbb0d62606953f7d856b347d9ce0ade6aa91`.

## What v0.21 changes

This closes the finite same-datum escalation through N18.

It does **not** close the continuum step. WP19 v0.19 already proves the direct newly-opened-shell contribution is summable by the boundary-annulus theorem. The remaining analytic obstruction is the recursive state/backreaction term

`Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)`.

WP19 v0.20 shows, non-rigorously, that a goal-oriented fixed-F11 adjoint strongly compresses the observed consecutive-cutoff effect. The next theorem target is to rigorize that dual-weighted transfer and its nonlinear remainder without replacing the exact recursive closure structure by a full-state worst-case bound.

## Claim boundary

The result is an eight-cutoff family of computer-assisted finite-dimensional theorems for one frozen initial datum. It is not an all-N theorem and does not establish a continuum Navier–Stokes singularity or global-regularity result.
