# WP19 v0.22 — Recursive state/backreaction drift Lipschitz gate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Copyright:** © 2026 Prince Upadhyay. All Rights Reserved.  
**Status:** falsification-first floating scout built on the completed N11–N18 certificate family.

## Target

WP19 v0.19 removed the direct newly-opened-shell term as the structural all-cutoff obstruction. The remaining term is

`Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)`.

For

`Gamma_M(u) = -P11[B(u,u)-B(P11u,P11u)]`,

the v0.14 fixed-output inequality gives, for exact states `x,y`,

`||Gamma_M(x)-Gamma_M(y)||_2 <= 2 C11 (||x||_2+||y||_2)||x-y||_2`.

Because both Galerkin solutions share the same datum and obey the finite-dimensional energy identity,

`||x||_2, ||y||_2 <= ||u0||_2`,

so

`||Gamma_M(x)-Gamma_M(y)||_2 <= 4 C11 ||u0||_2 ||x-y||_2`,

with `C11=sqrt(404724)`.

This inequality is analytic. The question is whether its constants are numerically useful on the certified same-datum family.

## Scout

For each transition `14->15`, `15->16`, `16->17`, and `17->18`, the GitHub workflow downloads the preserved predictor/certificate artifacts and measures

`||P_M ubar_{M+1}(t_j)-ubar_M(t_j)||_2`

at all 121 saved nodes.

The independently certified segment residual/gradient values are replayed through the same scalar trajectory-error recurrence and added to the nominal nodewise difference. A trapezoid integral then supplies a conservative design-level estimate of

`integral_0^T ||P_M u_{M+1}-u_M||_2 dt`.

That input is inserted into the exact Lipschitz inequality above.

The run also records the exact-form v0.19 direct-shell theorem bound

`C11 ||u0||_2^2/(2 nu) [1/(M(M-11)) + 1/M^2]`.

## Decision rule

This is a **falsification gate**, not a certificate.

- If the simple recursive-drift bound is already small and decays usefully, the next step is to interval-enclose the node/segment state-difference integral.
- If the simple bound is grossly too large, do not spend time rigorizing it. Move directly to the goal-oriented adjoint architecture identified in v0.20, where the terminal observable filters most of the full-state amplification.

## Claim boundary

The analytic Lipschitz inequality is exact. The new numerical values produced by v0.22 are floating scouts, even though they reuse outward-rounded quantities from the previously completed Arb certificates.

No new all-N persistence theorem, continuum regularity theorem, or singularity theorem is claimed.

## Executed result

GitHub Actions run `36714882801` completed successfully; artifact digest `sha256:3b0eb255dabe1f0480334d31a8021b3f3dc3c775f0985361aa17df70483acb58`.

The radius-augmented recursive-drift contribution decreases from about `17.19` to `4.17` across `14->15` through `17->18`, but the exact-form v0.19 direct-shell energy bound is enormous at these cutoffs: about `1.14e6, 8.31e5, 6.46e5, 5.22e5`. The combined simple route is therefore numerically useless for preserving the available endpoint margin.

**Decision:** do not spend interval-computation budget on the full-state Lipschitz route. It is retained as a correct structural estimate and a negative result. The next live route is the goal-oriented adjoint/dual-weighted formulation from v0.20.
