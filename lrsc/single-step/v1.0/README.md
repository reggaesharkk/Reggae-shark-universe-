# LRSC Single-Step Spectral Certificate v1.0

**Author:** Prince Upadhyay, Independent Research  
**Status:** Frozen-candidate computational certificate  
**Locked baseline:** `M=99`, `k_idx=49`, `theta=0.08`, `A=0.50`  
**Tolerance:** relative complex L2 error <= `0.001`

## Claim
For the locked one-step LRSC operator and specified conjugate-balanced 50-channel decomposition, the recorded global subset optimization gives the first threshold crossing at K=11: **K_0.001(0.50) = 11.**

This is benchmark- and tolerance-specific. It is not a claim of physical dimensionality, a physical law, or a multi-step dynamical theorem.

Fresh direct reconstruction: active nodes **81**; full-channel closure relative error **2.3808015585084204e-16**.

## Threshold boundary
K=10: `0.0010398206190990441` — FAIL.  
K=11: `0.00096236912766441347` — PASS.

Recorded K=11 subset: `{0,1,3,42,43,44,45,46,47,48,49}`.

## Provenance boundary
The subset identities are recorded outputs of the completed fixed-cardinality global search/optimization stage. The verifier in this release independently rebuilds the operator and directly recomputes the residuals. The verifier does **not** itself re-solve all combinatorial optimization problems, so it is not presented as a fresh exhaustive optimizer.

## Claim boundary
ESTABLISHED BY DIRECT REPRODUCTION HERE: operator construction, N_act=81, full-channel closure, residuals of recorded K=1..11 subsets, K10 failure, K11 success.

RECORDED GLOBAL-SEARCH RESULT: global minimizing subset identities K=1..11.

OPEN: analytic explanation of the high-index edge block/channel 3, parameter dependence, other carrier modes, other M, and recursive/multi-step behavior.

NOT CLAIMED: microscopic physics, emergent spacetime validation, universal spectral dimension, or a result outside the locked benchmark.

Frozen release ZIP SHA-256: `5a82e2eabdc12bad4aa48414285091814cdf79b0192be8b079c2eee3955ea0ef`  
PDF SHA-256: `4e1f03f6fa997031a557a70e2d7aa8daa72453104017b415b815485e03f8b11f`
