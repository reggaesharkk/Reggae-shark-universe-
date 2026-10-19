# WP19 v0.28 follow-up audit clarifications — 1 October 2026

This additive record addresses the remaining provenance and wording findings for the finite three-segment reverse-time recurrence. It does not alter any earlier result, input, verifier, workflow, or checksum file.

## Segment-237 A/B rounding

The A/B producer reads the already-rounded decimal strings in the segment record and passes them through `safe_decimal_upper`. It does not re-evaluate strain, nominal residual, or primal radius from predictor arrays. The source-level operation explains why the recorded A/B fields are higher by two decimal-grid units at the respective 9, 6, and 15 decimal places. A source-level emulation reproduces all three displayed values; the Arb-backed rounding itself was not independently executed in that emulation, so the two-unit explanation is supported by the code path and matching emulation, not a fresh array evaluation.

For the old recurrence, A/B uses its rounded strain, the segment's `residual_L2_upper`, and the shared incoming radius. The nominal-residual field is not an input. The approximately 0.001956341 outgoing difference is accounted for by the 2e-9 strain increase. The structured-residual result remains diagnostic-only and is not substituted into the official strain-only chain. The A/B artifact's existing `MATERIAL_TIGHTENING` status is retained without promoting it to the official chain.

## Superseded claims and retained artifacts

The machine-readable register at `results/wp19_v0_28/followup_audit_clarifications_20261001/record.json` names the legacy claims by exact path, field, and repository object identity. It covers the former anti-diffusion verdict, the optional +22.5 chain as a purported required correction, stale verifier assertions and their workflow snapshots, and the earlier status-note statements. Those files remain as historical records. A pass from a legacy verifier or workflow only replays its archived specification and does not revive the withdrawn claim.

Prior edits to the status note, top-level README, and corrected-chain checksum file are recorded by their current Git blob identifiers in the register. This supplement makes no further in-place edits to those files; their earlier versions remain available in repository history. New checksum entries in this supplement are repository-root-relative and are verified from the repository root.

## Scientific scope

The strain-only recurrence for steps 239, 238, and 237 remains valid in the backward ℓ2 energy estimate, conditional on the stated finite M15 adjoint model, the imported whole-segment strain and residual bounds, norm consistency, and the terminal error bound. The predictor and adjoint arrays required to reconstruct those imported bounds are not included in this record.

This is a limited scalar recurrence result. It is not a complete adjoint certificate, signed endpoint-transfer proof, all-cutoff result, blow-up result, or continuum Navier–Stokes regularity result.
