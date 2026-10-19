# WP19 v0.26 -- Signed-C500 Numerator Goal-Adjoint Pre-Interval Gate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Copyright:** (c) 2026 Prince Upadhyay. All Rights Reserved.  
**Status:** live floating design gate after the successful v0.25b portable C500 endpoint certificates.

## Why v0.26 exists

WP19 v0.23-v0.24 showed that a reconstruction-specific goal-oriented adjoint can predict the cutoff-to-cutoff change of a fixed low observable far more sharply than a generic full-state Lipschitz bound. Those stages used `F11(P11 u(T))` as a proxy objective.

WP19 v0.25b now supplies the object that should actually be transferred: the exact-rational signed-C500 numerator is rigorously negative at every tested cutoff `N=11,...,18`, the C500 coalition has a portable semantic identity, and the same prospective N13 K36 sign chart is realized and locked at every N14-N18 endpoint.

Therefore the next target is no longer the nonsmooth ratio surrogate. It is one fixed smooth polynomial on `P11 u(T)`:

`J_C500 = sum_{g in K36} sigma_g n_g - 9 sum_{g in C500} tau_g n_g`,

where `sigma_g` is the frozen N13 prospective K36 numerator sign and `tau_g` is the frozen C500 linear sign.

The denominator/normalizer is kept separate, exactly as required by the v0.25b next-target statement.

## Frozen identities

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- prospective N13 K36 sign-chart file SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1` (tracked git blob `f06df05437fd717337b5bf11939e997f2a7d165e`; unchanged since its first commit)
- portable C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`
- `nu = 0.1`, `T = 0.003`, `h = 0.000025`, 120 steps.

No sign, key, coalition rank, or datum may be retuned in v0.26.

## Calculation

For each same-datum transition `M -> M+1`, `M=14,15,16,17`:

1. project both certified predictor endpoints to the fixed N11 space;
2. evaluate the fixed signed polynomial `J_C500` and require agreement with the v0.25b exact-rational nominal numerator;
3. require all 36 K36 endpoint signs to equal the frozen prospective N13 sign chart at both ends;
4. obtain `J_C500'(P11 u_M(T))` by reverse-mode differentiation and cross-check it with a centered directional derivative;
5. embed that terminal gradient into cutoff `M+1`;
6. integrate the continuous adjoint backward with half-step RK4 along the cubic-Hermite reconstruction of the lower trajectory;
7. pair the adjoint by Simpson quadrature with the full reconstruction residual

`r(t) = f_{M+1}(E ubar_M(t)) - E d_t ubar_M(t)`;

8. measure the exact floating decomposition

`delta J = eta_M + dynamic remainder + endpoint Taylor remainder`;

9. replay the certified whole-segment trajectory radii in binary64 and form the conservative candidate nonlinear envelope

`integral ||grad lambda||_infty ||e||_2^2 dt`;

10. express the actual transfer, dual remainder, nonlinear envelope, and combined scout budget as fractions of the **rigorous negative numerator margin** already certified by v0.25b at the lower cutoff.

## Decision rule

v0.26 is a pre-interval design gate, not a theorem. It recommends spending interval-arithmetic effort on the signed-numerator adjoint when:

- all frozen identity/sign checks pass;
- the objective and gradient self-checks pass;
- the dual remainder is small relative to the rigorous negative numerator margin; and
- the conservative scout transfer budget remains comfortably below that margin across all four sampled transitions.

A failure is retained as a negative design result; the workflow must not hide it by retuning the objective.

## Claim boundary

The N11-N18 v0.25b endpoint certificates remain the rigorous finite results. v0.26 uses floating adjoint propagation, floating Simpson quadrature, and a binary64 replay of certified scalar radii. It is therefore **not** an interval transfer theorem, **not** an all-N persistence theorem, and **not** a continuum regularity or blowup result.

If the gate is favorable, the next stage is intervalization of the fixed polynomial terminal gradient, backward adjoint propagation, dual quadrature, and nonlinear/endpoint remainder budgets, with the normalizer handled independently.