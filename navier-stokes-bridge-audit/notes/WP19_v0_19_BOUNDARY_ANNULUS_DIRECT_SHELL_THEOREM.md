# WP19 v0.19 — Boundary-Annulus Theorem for the Direct Consecutive-Cutoff Term

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact Fourier support theorem + cutoff-summable direct-shell estimate.  
**Not claimed:** summability of recursive state drift, all-N persistence, continuum regularity, or blowup.

For a transition M->M+1, let
`s_{M+1}=(P_{M+1}-P_M)u_{M+1}` and `w_M=P_Mu_{M+1}`.

For a fixed low output |k|<=11, if q is in the new shell (|q|>M) and p+q=k, then any old partner must satisfy |p|>M-11. Hence only the boundary annulus

`b_M=(P_M-P_{M-11})u_{M+1}`

can couple the new shell directly into P11.

Therefore the direct same-state cutoff increment obeys the exact support identity

`DeltaGamma_M^direct = -P11[B(b_M,s)+B(s,b_M)+B(s,s)]`.

Using the v0.14 fixed-output divergence-free estimate,

`||P11 B(a,b)||_2 <= C11 ||a||_2 ||b||_2`, with
`C11=sqrt(404724)=636.179220031588...`,

gives

`||DeltaGamma_M^direct||_2 <= C11[2||b_M||_2||s||_2 + ||s||_2^2]`.

Since `||b_M||_2 <= ||grad b_M||_2/(M-11)` and
`||s||_2 <= ||grad s||_2/M`, while the two Fourier supports are disjoint,

`2||grad b_M||||grad s|| <= ||grad b_M||^2+||grad s||^2 <= ||grad u_{M+1}||^2`.

Thus, for M>11,

`||DeltaGamma_M^direct||_2 <= C11 [1/(M(M-11)) + 1/M^2] ||grad u_{M+1}||_2^2`.

The Galerkin energy identity then yields

`||DeltaGamma_M^direct||_{L1_t L2_x} <= C11 ||u0||_2^2/(2 nu) [1/(M(M-11))+1/M^2]`.

The first series telescopes:

`sum_{M>=M0} 1/[M(M-11)] = (1/11) sum_{j=M0-11}^{M0-1} 1/j`.

Therefore

`sum_M ||DeltaGamma_M^direct||_{L1_t L2_x} < infinity`.

**Conclusion:** the direct new-shell term is analytically summable across the separate consecutive Galerkin solutions using only common initial energy and viscosity.

This corrects the coarser v0.14 statement that the direct term had an energy-only O(1/M) obstruction. That loss came from pairing the new shell with the full old state instead of the boundary annulus.

The remaining hard term is

`Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)`,

the recursive state/backreaction drift.

Floating same-datum annulus-bound diagnostics (measured direct closure vs theorem-form bound):
- N14->N15: 0.0077314 vs 8.4354
- N15->N16: 0.0032638 vs 2.7993
- N16->N17: 0.0015528 vs 1.0367
- N17->N18: 0.0003826 vs 0.3740

The theorem is structural rather than margin-closing at the current constants.
