# WP19 v0.28 reverse-time correction follow-up

**Date:** 1 October 2026  
**Author:** Prince Upadhyay  
**Rights:** Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.

## Corrected sign convention

The archived producer defines
`r = dL/dt - VJP(u,L) - nu*Lambda*L`.
The finite-Galerkin adjoint implemented in `src/wp19_v0_23_rk4_goal_adjoint.py` satisfies
`d(lambda)/dt = VJP(u,lambda) + nu*Lambda*lambda`.
For `e=lambda-L),
`de/dt = VJP(u,e) + nu*Lambda*e - r`.
With `tau=T-t),
`de/dtau = -VJP(u,e) - nu*Lambda*e + r`.

The reverse-time energy identity is
`(1/2)d||e||_2^2/dtau = -<VJP(u,e),e> - nu<Lambda e,e> + <r,e>`.
Since `<Lambda e,e> >= 0`, viscosity is dissipative in the propagated ell2 energy estimate and may be dropped when deriving an upper bound. The archived strain-only scalar recurrence is therefore valid under its imported continuous-segment bounds. The optional `+22.5` exponent is a conservative enlargement, not a required correction.

## Assumptions and scope

This conclusion assumes: the error is real, divergence-free and Hermitian-symmetric; the Leray projection commutes with `Lambda`; the true primal field is divergence-free; the exact adjoint is the finite Galerkin system above with the archived projected/truncated convolution; one Fourier-coefficient ell2 convention is used throughout; the strain and residual bounds hold over each entire continuous segment; the primal radius bounds the primal error throughout that segment; and the terminal error bound is valid in that norm.

The correction pins the producer source copies, adjoint source and Galerkin system source by SHA-256 in its machine-readable result. The predictor and adjoint arrays, lower nodes, and upstream primal-segment inputs needed to reconstruct the continuous-segment bounds are absent. The recurrence result is conditional; it does not verify the exact adjoint trajectory or producer bounds.

## N237 A/B clarification

The A/B old recurrence uses its separately rounded strain upper, the shared incoming radius, and the segment's `residual_L2_upper`. It does not use the displayed nominal-residual field. The A/B strain is 1752.285153303 versus the segment value 1752.285153301. Holding the incoming radius and segment residual fixed, the 2e-9 strain increase accounts for the full approximately 0.001956341 outgoing difference. The source shows that the strain was separately reevaluated and rounded; absent arrays prevent determining why the value shifted. The structured-residual comparison remains diagnostic-only and is not inserted into the archived chain.

The first correction note and historical audit artifacts remain preserved. The canonical correction's JSON names the superseded claims and their exact hashes. The pilot checksum manifests are directory-relative; the correction, corrected-chain, backward-audit, and package manifests are repository-root-relative.

This is a finite M14 scalar recurrence audit, conditional on supplied bounds. It is not a full adjoint certificate, endpoint-transfer theorem, all-cutoff result, blow-up result, or continuum Navier–Stokes regularity result.

Canonical correction record: https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_28_REVERSE_TIME_SIGN_CORRECTION_2026_10_01.md  
Canonical follow-up PR: https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/149
