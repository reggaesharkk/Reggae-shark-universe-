# WP19 v0.28 reverse-time sign correction

**Date:** 1 October 2026  
**Author:** Prince Upadhyay  
**Rights:** Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

## Correction

An initial v0.28 audit misread the sign of viscosity while the adjoint-error radius was propagated backward from terminal time. The producer residual is
`r = dL/dt - VJP(u,L) - nu*Lambda*L`.
With reverse time `tau=T-t`, the corresponding error equation contains `-nu*Lambda*e`. Since `<Lambda e,e> >= 0`, viscosity contracts the error in the reverse-time norm estimate. The previously archived strain-only recurrence is therefore valid under its stated segment bounds. Adding `nu*max|k|^2 = 22.5` is a conservative enlargement, not a required correction.

## Replayed finite chain

For the fixed M14, `nu=0.1`, `T=0.003` pilot, the frozen half-segments remain in order `239 -> 238 -> 237`. A separate arithmetic replay reproduced the archived strain-only outgoing radii and confirmed that each archived outward value covers the replay:

| Segment | Recomputed strain-only outgoing upper |
|---:|---:|
| 239 | 74,882,674,993.048618657819… |
| 238 | 76,553,735,316.602437456115… |
| 237 | 78,258,186,399.829279366902… |

The optional +22.5 comparison chain is larger. The N237 A/B artifact reuses the same baseline segment and incoming radius but separately reports slightly larger strain, residual, and primal-radius bounds. It is kept diagnostic-only and is not substituted into the archived chain.

## Evidence and limits

The canonical repository contains the pinned inputs, correction runner, separate arithmetic replay, output JSON, and SHA-256 manifest:
- [Correction note and artifacts in the canonical repository](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/main/results/wp19_v0_28/reverse_time_sign_correction_20261001)
- [Correction runner](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp19_v0_28_reverse_time_sign_correction.py)
- [Separate arithmetic replay](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp19_v0_28_verify_reverse_time_sign_correction.py)

The recurrence conclusion is conditional on producer-supplied continuous-segment strain and residual enclosures; their underlying predictor arrays and upstream inputs are not independently reconstructed by this replay. This does not certify the full adjoint path, dual quadrature, nonlinear remainder, normalizer, endpoint transfer, any all-cutoff statement, or continuum Navier–Stokes regularity.
