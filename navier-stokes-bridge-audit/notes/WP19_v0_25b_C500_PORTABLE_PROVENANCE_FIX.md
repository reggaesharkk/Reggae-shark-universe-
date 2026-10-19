# WP19 v0.25b — Portable C500 provenance repair

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Copyright:** © 2026 Prince Upadhyay. All Rights Reserved.  
**Status:** provenance repair only; no coalition retuning.

## What failed

The v0.25 runs failed before any N14–N18 endpoint certificate was attempted.

The second failed run established an important fact first: the historical N11 predictor was reproduced **byte-identically** with SHA-256

`b70bf7f7fe85a8c073c02c80e54e1f10d0642f5d030dfe569470c5970ebdda29`.

Despite that exact predictor match, rebuilding the v0.6 C500 JSON on the GitHub runner produced a different full-file byte SHA from the historical v0.6 SHA.

The reason is that the historical JSON stores full-precision floating diagnostic values in addition to the actual mathematical coalition identity. Those diagnostic decimal strings can vary at the last bits across floating-point environments even when the selected rank/orbit/sign coalition is unchanged.

Therefore the old full-file byte hash is too strict as a cross-platform identity test.

## Portable mathematical identity

The mathematical C500 object used by every subsequent theorem consists of the ordered 500 selected orbit-pair groups and their frozen signs.

v0.25b defines a portable semantic identity from exactly

- rank,
- left orbit,
- right orbit,
- fixed linear sign,

for all 500 rows.

The resulting semantic SHA-256 is

`1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`.

This identity is checked before any endpoint calculation.

The historical v0.6 full-file SHA remains recorded unchanged:

`79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`.

It is retained as provenance for the original serialization, not treated as a portable floating-point hash.

## Independent historical invariants

The reconstructed semantic coalition must also reproduce the original v0.6 N11 invariants:

- `G_C500(N11) = -47.8162782412821` to numerical tolerance;
- N11 outside absolute-mass capture fraction `0.9994122170697335`;
- exactly `1048` retained ordered source pairs;
- exactly `1159` fixed Fourier modes.

Any failure of the semantic SHA or these invariants aborts the workflow.

## Endpoint gate

Only after the N11 predictor SHA and portable C500 identity pass does v0.25b run the existing exact-rational v0.10 endpoint perturbation arithmetic at N14–N18.

For each cutoff the gate still requires:

- 36/36 K36 signs locked;
- signed C500 numerator upper bound strictly negative;
- normalizer lower bound strictly positive.

No endpoint inequality, error radius, sign condition, or coalition membership is relaxed.

## Claim boundary

This repair changes only the provenance representation used to identify C500 across floating-point environments. It does not alter the selected coalition, its signs, the same-datum trajectories, or any certificate inequality.

No all-N or continuum Navier–Stokes conclusion is claimed.
