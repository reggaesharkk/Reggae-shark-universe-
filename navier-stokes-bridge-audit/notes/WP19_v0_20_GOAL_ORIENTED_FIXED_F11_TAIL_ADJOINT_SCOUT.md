# WP19 v0.20 — Goal-Oriented Fixed-F11 Tail Adjoint Scout

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** floating reconstruction-specific continuous-adjoint scout.  
**Not claimed:** interval adjoint validation, infinite-tail theorem, continuum regularity, or blowup.

Fix the low observable once and for all:

`F_low(u_M(T)) = F_11(P_11 u_M(T))`.

Observed endpoint values:
- N14: -60.7794636103
- N15: -58.4633275505
- N16: -58.0253626973
- N17: -57.8961734515
- N18: -57.9151672166

For each transition M->M+1, embed the lower trajectory in the higher system with the new shell set to zero. The difference of vector fields is the newly generated shell forcing

`r_M = f_{M+1}(E u_M)-E f_M(u_M)`.

Propagate the terminal gradient of the fixed F11 objective backward through the continuous linearization,

`-lambda_dot = Df_{M+1}(E u_M)^* lambda`,

and evaluate the first-order goal-oriented correction

`eta_M = integral <lambda,r_M> dt`.

Floating results:

| pair | actual delta F11 | dual prediction | remainder | relative remainder |
|---|---:|---:|---:|---:|
| 14->15 | +2.31613606 | +2.30313158 | +0.01300448 | 0.56% |
| 15->16 | +0.43796485 | +0.43296471 | +0.00500014 | 1.14% |
| 16->17 | +0.12918925 | +0.13233789 | -0.00314865 | 2.44% |
| 17->18 | -0.01899377 | -0.01729383 | -0.00169994 | 8.95% |

Dual-effect magnitudes:
`2.30313, 0.432965, 0.132338, 0.017294`.

Successive magnitude ratios:
`0.188, 0.306, 0.131`.

The N18 sign reversal is captured by the adjoint.

The terminal gradient norm stays near 3071. An independent endpoint Taylor check is extremely linear: the N14 terminal gradient predicts the cumulative N14->N18 fixed-F11 change as 2.86464378 versus actual 2.86429639, a remainder of only -3.47e-4.

Thus endpoint nonlinearity is not the observed bottleneck. The dynamic shell-to-low transfer is the relevant object.

The next rigorous target is an interval enclosure of the dual-weighted quantity `eta_M` plus a nonlinear remainder bound, combined with the v0.19 summable direct-shell theorem.

Claim boundary: this is a floating first-order scout using node-sampled continuous adjoint propagation, not a proof.
