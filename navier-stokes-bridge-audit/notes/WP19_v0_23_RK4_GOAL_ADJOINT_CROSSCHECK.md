# WP19 v0.23 — RK4 goal-oriented adjoint cross-check

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Copyright:** © 2026 Prince Upadhyay. All Rights Reserved.  
**Status:** public floating verification stage following the v0.22 falsification result.

## Why this stage exists

WP19 v0.22 rejected the simple full-state Lipschitz route as numerically useless at the current constants. The remaining viable route is goal-oriented: propagate only the sensitivity of the fixed low observable instead of paying a worst-case norm for the entire state.

The target is the already studied fixed observable

`F11(P11 u_M(T))`.

v0.20 found a very sharp first-order continuous-adjoint scout, but used first-order backward stepping and node-trapezoid pairing. v0.23 independently rebuilds that calculation with stronger numerical controls before interval rigorization.

## New numerical controls

v0.23 does four things:

1. computes the terminal gradient of the fixed N11 observable by reverse-mode differentiation of the actual finite objective;
2. implements the adjoint of the dealiased quadratic Navier–Stokes nonlinearity analytically in physical/Fourier space;
3. validates that spectral VJP against a centered finite directional derivative on an independent N=4 divergence-free/reality-symmetric state;
4. integrates the continuous adjoint backward with RK4 along the cubic-Hermite reconstruction of the lower-cutoff trajectory.

The dual-weighted newly opened-shell residual is then paired on the 121 saved nodes for each transition

`14->15, 15->16, 16->17, 17->18`.

## Decision gate

The v0.23 run is successful only as a *route-selection* result if the independently rebuilt adjoint continues to reproduce the actual fixed-F11 cutoff changes with small remainders and passes its internal derivative/VJP checks.

If it does, the next stage is interval rigorization of the terminal gradient, adjoint propagation, quadrature, and nonlinear remainder. If it does not, the discrepancy is investigated before any claim is strengthened.

## Claim boundary

v0.23 is floating verification, not a computer-assisted theorem. The existing N11–N18 Arb certificates remain the rigorous finite results. No all-N or continuum conclusion follows from v0.23.
