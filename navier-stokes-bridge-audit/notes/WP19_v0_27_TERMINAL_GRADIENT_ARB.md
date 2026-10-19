# WP19 v0.27 — Arb Terminal Signed-C500 Gradient Certificate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** first intervalized component after the v0.26 pre-interval gate.

## Target

v0.26 established that the fixed signed-C500 numerator is the correct smooth
goal functional and that its floating Hermite goal-adjoint transfer is small
relative to the already rigorous negative endpoint margin.

v0.27 intervalizes the **terminal condition** of that adjoint.

For the frozen polynomial

[
J(a)=\sum_{g\in K36}\sigma_g n_g(a)-9\sum_{g\in C500}\tau_g n_g(a),
]

the code evaluates both (J) and (J'(a)) at the canonical decimal
(P_{11}) predictor endpoint with 128-bit Arb/acb arithmetic.

## Why this is tractable

The adjoint used in v0.26 is defined along the known cubic-Hermite
reconstruction. Therefore its terminal condition is the derivative at the
known predictor endpoint; it does **not** require placing the entire terminal
trajectory-error ball into automatic differentiation.

The signed numerator is degree seven, but it has frozen finite support:
36 K36 groups plus 500 C500 groups. An analytic reverse-mode formula is used
instead of interval finite differences.

## Independent formula check

Before the Arb version was committed, the same analytic reverse-mode formula
was evaluated in complex128 at the N14 endpoint and compared against the
existing v0.26 PyTorch reverse-mode terminal gradient. The relative L2
difference was approximately (1.15\times 10^{-15}), with both norms near
(4.691959667101\times10^{12}).

The workflow additionally performs a centered directional finite-difference
check and requires the Arb directional derivative interval to contain the
complex128 analytic result.

## Frozen provenance

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- prospective K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`

No datum, sign, coalition member, or coefficient is retuned.

## Decision

If all four transitions `14->15`, `15->16`, `16->17`, `17->18`
return a tight 128-bit terminal-gradient enclosure, the next stage is an
a-posteriori Arb validation of the **backward adjoint ODE** around the saved
floating half-step adjoint reconstruction, followed by rigorous dual
quadrature.

## Claim boundary

v0.27 certifies only the terminal polynomial value/gradient at the canonical
decimal predictor endpoint. It does not yet certify backward adjoint
propagation, dual quadrature, the nonlinear remainder, the endpoint Taylor
remainder, an all-N transfer theorem, or continuum Navier–Stokes behavior.
