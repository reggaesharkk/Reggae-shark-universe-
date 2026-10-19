# WP19 v0.28 — Goal-oriented adjoint residual gate (design, not yet executed)

**Status:** frozen mathematical design target for the next implementation stage. No v0.28 residual values or certificate are claimed here.

## Fixed setting

Continue only the existing finite transition matrix `14→15`, `15→16`, `16→17`, `17→18`, with the same rational 112-pair witness, K36 signs, portable C500 polynomial, `nu=0.1`, `T=0.003`, and lower-cutoff predictor certificates. Do not tune any of them. v0.27c1 is intended to preserve the 241-node binary64 adjoint reconstruction and its continuous-RHS node values on each transition.

## Residual to enclose

For a transition `M→M+1`, let `u_M(t)` be the exact lower Galerkin trajectory embedded in the larger finite-dimensional divergence-free space. Write the finite-dimensional Navier–Stokes vector field as

`F(u) = -P[(u·∇)u] + nu Δu`.

In the backward time coordinate `s=T-t`, the continuous adjoint `mu(s)=lambda(T-s)` satisfies

`d mu / ds = DF(u_M(T-s))^* mu`.

Let `mu_h` be the cubic Hermite reconstruction from the saved adjoint values and RHS values. On every half-step interval, define the residual

`r(s) = d mu_h/ds - DF(u_M(T-s))^* mu_h(s)`.

The adjoint Hermite path and primal Hermite predictor are cubic in the segment parameter. Since the adjoint RHS is linear in the adjoint and linear in the primal velocity, the residual is a Fourier-valued polynomial of degree at most six. The implementation must enclose each complete polynomial segment, not a set of sample times.

The stored arrays remain binary64 source data. When building Arb inputs, represent every stored real/imaginary value by its exact `float.as_integer_ratio()` rational (or by an explicitly outward-rounded interval containing that rational). Do not treat `str(float_value)` as an enclosure of the underlying binary64 value. The Hermite reconstruction is the exact rational-coefficient surrogate defined by those imported nodes/RHS values; its residual, including all RK4/interpolation defects, is what the validated bound must control.

For each Fourier mode/component, convert the residual polynomial to Bernstein form on `[0,1]`. If its degree-six Bernstein coefficients are `b_0,...,b_6`, then

`sup_{s in segment} |r_mode,component(s)| <= max_l |b_l|`.

Summing the squared component bounds with Arb upper endpoints gives a segmentwise `R_j >= sup ||r(s)||_2`. All polynomial coefficients, arithmetic operations, and final square roots must be outward rounded. Primal coefficient uncertainty from the existing whole-segment trajectory certificates must be included in these enclosures; treating the saved binary64 predictor centers as the exact trajectory is forbidden.

## Sharper stability estimate from the Navier–Stokes energy structure

A generic full matrix norm for the adjoint Jacobian is the wrong first bound: it discards the skew transport cancellation and may be enormous. Use the L2 logarithmic norm instead.

For divergence-free `v` and `u`, orthogonality of the Leray projection and integration by parts give

`<v, DF(u)v> = -nu ||∇v||_2^2 - <v, S(u)v>`,

where `S(u)=(∇u+∇u^T)/2`. The transport term vanishes in this quadratic form. The same symmetric-part bound applies to `DF(u)^*`, hence

`<v, DF(u)^*v> <= ||S(u)||_infinity ||v||_2^2`.

Thus, for the adjoint error `e=mu-mu_h`,

`d||e||_2/ds <= L(s)||e||_2 + ||r(s)||_2`,

where a sufficient finite-dimensional bound is `L(s) >= ||S(u_M(T-s))||_infinity`. A Fourier majorant suitable for interval evaluation is

`||S(u)||_infinity <= sum_k |k|_2 |u_hat(k)|_2`,

with the exact normalization checked against the repository's Fourier convention. Compute an outward Arb upper bound `L_j` over each complete segment, including the primal trajectory enclosure.

With segment width `h_j`, `Lambda_j=h_j L_j`, `rho_j=h_j R_j`, and incoming adjoint-error radius `epsilon_j`, use the outward recurrence

`epsilon_{j+1} <= exp(Lambda_j) epsilon_j + (expm1(Lambda_j)/Lambda_j) rho_j`,

with the continuous value `1` for the quotient at `Lambda_j=0`. Initialize from the certified terminal-gradient uncertainty: combine the Arb-vs-binary64 center discrepancy with the v0.27b endpoint gradient-variation enclosure. Every recurrence value must be rounded outward.

This estimate is intentionally a gate. If the resulting radius is too large to preserve the signed transfer margin, record a rigorous failure and diagnose the bound; do not retune the data or replace a valid failure with a fitted constant.

## Remaining gates after the adjoint recurrence

Passing this residual/error gate would still not prove the cutoff-transfer claim. Separate certificates remain necessary for:

1. dual quadrature of the signed C500 numerator along the finite trajectory;
2. nonlinear/Taylor remainder from replacing the exact higher-cutoff state by the lower-cutoff linearization;
3. endpoint enclosure after combining the base value, adjoint correction, and all remainders;
4. an independently implemented fail-closed verifier;
5. the existing separate normalizer positivity certificate.

Only after all finite-transition gates pass may the package report a finite `N=14…18` transfer statement. No all-N, continuum, global-regularity, or blowup claim follows.
