# WP19 v0.27b — Arb Endpoint Gradient-Ball Subcertificate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Parent checkpoint:** `notes/WP19_v0_27_RECOVERY_CHECKPOINT_2026_09_30.md`

## Purpose

v0.27a certified the signed-C500 terminal gradient at the nominal projected endpoint. v0.27b lifts that point calculation to the already certified terminal state uncertainty.

For each lower cutoff `M=14,15,16,17`, the whole-segment Arb trajectory certificate supplies a terminal `L2` error radius `r_M`. Because every individual real or imaginary Fourier coordinate is bounded in magnitude by the global `L2` error, widening every P11 real/imaginary coordinate by the full `r_M` produces a conservative Cartesian box containing the true endpoint uncertainty set.

The fixed signed-C500 polynomial and its analytic tangent gradient are evaluated on that full box with 192-bit Arb arithmetic.

## Frozen terminal radii

From `notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md`:

- N14: `0.000012825905`
- N15: `0.000013195722`
- N16: `0.000013456103`
- N17: `0.000013665541`

These values are not re-estimated by v0.27b.

## Rigorous endpoint Taylor bound

Let `a` be the nominal endpoint, `h` an admissible endpoint error, and `||h||_2 <= r_M`. The segment `a + theta h`, `0 <= theta <= 1`, lies inside the coordinatewise Arb box. Therefore

```
|J(a+h)-J(a)-<grad J(a),h>|
 <= r_M sup_theta ||grad J(a+theta h)-grad J(a)||_2.
```

v0.27b computes the right-hand side by interval evaluation of the analytic gradient over the larger Cartesian box.

The enlargement is deliberate. It ignores the correlation imposed by the single global L2 ball, divergence-free constraints, and reality symmetry when constructing the input box. Therefore an overly large result is a valid negative/sharpness result; it must not be repaired by retuning the datum.

## Integrity gate

A run is considered arithmetically valid only if:

- all frozen witness/K36/sign-chart/C500 identities match;
- lower/higher predictor metadata match the frozen problem;
- the Arb endpoint objective box contains the nominal Arb objective;
- every component of the Arb gradient box contains the corresponding nominal Arb gradient component;
- all reported bounds are finite.

The result also records whether the rigorous endpoint Taylor remainder is smaller than the already certified negative signed-numerator margin. This is a scientific budget diagnostic, not an excuse to discard a valid but loose enclosure.

## Next gate

If the endpoint uncertainty budget is usable, continue to the backward-adjoint interval propagation. If this naive Cartesian intervalization is too wide, the next legitimate refinement is a structured Hessian/directional enclosure respecting the L2/tangent geometry — not retuning the witness, coalition, or signs.

## Claim boundary

This is a finite-dimensional endpoint-uncertainty certificate. It does not certify backward adjoint propagation, dual quadrature, the dynamic nonlinear remainder, all-N persistence, or continuum Navier–Stokes regularity.
