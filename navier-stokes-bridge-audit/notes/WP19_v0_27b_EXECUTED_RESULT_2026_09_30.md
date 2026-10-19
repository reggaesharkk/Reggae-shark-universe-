# WP19 v0.27b — Executed Result

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Workflow run:** `36750819173`  
**Source commit:** `9b4ec5e801acd767309c887029d2540d0060fcbf`  
**Aggregate artifact:** `wp19-v0-27b-endpoint-gradient-ball-arb`  
**Artifact id:** `11113784188`  
**Artifact ZIP digest:** `sha256:740b55a53efa854f2fbb4e140e6b20d2a9e00e81d25371c6df8590793e5a26c1`

## Verdict

All four matrix jobs and the aggregate job passed the fail-closed integrity checks.

`PASS ENDPOINT-GRADIENT-BALL ARB SUBCERTIFICATE`

All four rigorous endpoint first-order Taylor remainder bounds are below their corresponding already-certified negative signed-numerator margins.

## Per-transition certified endpoint uncertainty budgets

| transition | certified terminal L2 radius | gradient-variation L2 upper | endpoint Taylor remainder / base margin upper |
|---|---:|---:|---:|
| 14->15 | 0.000012825905 | 15845467881.27747 | 0.000001497069 |
| 15->16 | 0.000013195722 | 16301397742.549378 | 0.000001655541 |
| 16->17 | 0.000013456103 | 16622536128.074724 | 0.000001735717 |
| 17->18 | 0.000013665541 | 16881279926.025994 | 0.000001794275 |

Maximum certified endpoint Taylor remainder / base margin upper:

`1.794275e-06`

Maximum linear terminal-state uncertainty / base margin upper:

`0.000499055225`

The intentionally much looser direct objective-box deviation reaches approximately `0.04684` of the base margin at M17, but the gradient-variation Taylor control remains about six orders of magnitude below the margin.

## Meaning

v0.27a certified the terminal gradient at the nominal endpoint. v0.27b now certifies that the already validated terminal trajectory uncertainty does not destabilize that first-order terminal linearization at any transition N14->N18.

This closes the terminal-state uncertainty subgate required before the backward-adjoint interval stage.

## Frozen continuation target

Next: `v0.27c` — validate the backward continuous adjoint along the fixed lower-cutoff cubic-Hermite reconstruction with a rigorous adjoint-trajectory error envelope. The terminal adjoint uncertainty is initialized from the v0.27b gradient-variation bound. The primal datum, K36 signs, C500 coalition, objective, and cutoff transitions remain frozen.

## Claim boundary

Finite-dimensional endpoint uncertainty certificate only. No all-N persistence theorem and no continuum Navier–Stokes regularity or blowup claim.
