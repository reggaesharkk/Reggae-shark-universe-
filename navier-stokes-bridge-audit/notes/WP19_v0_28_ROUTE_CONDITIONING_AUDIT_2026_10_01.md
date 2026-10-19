# WP19 v0.28 route-conditioning audit

**Status:** diagnostic go/no-go analysis of the current scalar recurrence; not a theorem and not a Navier–Stokes result.

## Why this audit comes before another segment

Segments 239, 238, and 237 have each completed a continuous 192-bit Arb enclosure and a chained scalar error check. Before running segment 236, this audit decomposes what is driving the current recurrence and tests a clearly labeled stress scenario. The purpose is to decide whether the existing scalar enclosure is a useful route toward the signed-observable transfer gate.

The fixed witness, K36 keys and signs, sign chart, portable C500 identity, predictor arrays, viscosity, timestep, and continuous-segment method are unchanged.

## Archived observations

The machine-readable summary is `results/wp19_v0_28/route_conditioning_audit_20261001/route_conditioning_audit.json`. Its inputs are the archived JSON and check files for runs `36818369196`, `36819581437`, and `36820757066`, all bound by SHA-256 and the same frozen identities.

Across all three observed segments:

- the incoming adjoint error upper bound rises from `73,244,978,636.91` at segment 239 to `78,258,186,399.83` after segment 237;
- approximately `99.4%` of each one-segment recurrence increase comes from multiplying the incoming error by the exponential amplification factor;
- the additive residual term contributes less than `1%` of each observed increase;
- the primal-uncertainty contribution to the residual upper bound is `13,446`–`14,309` times the nominal residual upper bound.

This isolates the present bottleneck: **the current scalar recurrence is dominated by the logarithmic-norm amplification, while the current primal uncertainty treatment makes the residual enclosure about four orders of magnitude wider than its nominal part.**

## Conditional stress scenario

The audit repeats the largest observed logarithmic-norm and residual upper bounds on each of the 237 uncomputed M14 segments. Under that explicit, unverified assumption, the scalar error upper would exceed the v0.27 terminal-gradient L2 norm reference after 186 further steps and reach about `3.07` times that reference after 237 steps.

This is a **conditioning stress scenario only**. No evidence establishes that those three observed maxima bound the remaining segments, so this is neither a prediction nor a certificate about the uncomputed trajectory. The adjoint L2 error and signed-numerator margin have different units; the audit does not compare them as if they were interchangeable.

## Decision and next gate

Do not spend the next run on another segment using the same coarse uncertainty formula. The next decisive test is a **single frozen same-segment comparison** on segment 237: derive an Arb-enclosed directional/tangent-space bound for the primal-uncertainty contribution to the adjoint residual, retaining the divergence-free and reality constraints, and compare it with the archived componentwise/triangle bound. Keep segment 237's old result as the baseline; do not change the witness, K36, C500, predictors, signs, or time grid. Require an independent direct-convolution check and an outward recurrence check. If this structured bound does not materially reduce the uncertainty penalty, retire this scalar-bound route rather than marching through the remaining segments with an ineffective enclosure.

This audit does not prove the current method impossible, does not certify the remaining segments, and makes no all-cutoff or continuum claim.
