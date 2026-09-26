# Navier–Stokes Bridge Audit — Current Status

**Prince Upadhyay, Independent Research**  
**Updated:** 27 September 2026

Canonical specialist repository: https://github.com/reggaesharkk/navier-stokes-bridge-audit

## Frozen lineage

The N11-derived K36 ordered source-orbit coalition and its three-state static criteria were fixed before the N12 test. Finite N12 and N13 holdouts passed the frozen transfer gates. The N14 time-resolved hypotheses were then frozen before N14 data; N14 passed all three tests in all three states. The N15 continuation and time-gate protocol was frozen and merged in canonical [PR #90](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/90) before N15 data. The completed [N15 prospective result](WP16_036_N15_PROSPECTIVE_TIME_GATE_RESULT_2026_09_27.md) and [summary](WP16_036_N15_result_summary.json) were recorded in [PR #91](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/91), which also froze the [N16 protocol](WP16_036_N16_PROSPECTIVE_FREEZE_2026_09_27.md) before any N16 state or score.

## N15 completed prospective test

N15 seed `20260940`, search grid 48, and the frozen 520-proposal schedule produced a best search-grid `C_infinity_stretch=9.9109238004012`; fixed-winner grid-128 refinement gave `9.911923711291015`. Its 6,791 active conjugate pairs comprised 5,638 inherited and 1,153 new pairs. Checkpoint, continuation, and time-gate SHA-256 hashes are listed in the result note and summary.

The frozen time gate used viscosity 0.1, steps of 0.0001 through 0.0030, the same 36 source-orbit keys, mass fraction at least 0.90, same sign, and signed share in [0.8, 1.2].

| N15 state | static | mass through 0.0010 | first sampled mass exit | signed at exit | initial dF/dt > 0 | exit full/radial/polarization < 0 |
|---|---|---|---:|---|---|---|
| inherited | pass | pass | 0.0023 | pass | pass | pass |
| target_only | pass | pass | 0.0023 | pass | pass | pass |
| full_final | pass | pass | 0.0023 | pass | pass | pass |

At each exit the full and radial/polarization margin rates are negative while scalar-phase contribution remains positive. The half-step samples at 0.00225 remain above the 90% threshold and those at 0.00230 fall below it. This independently frozen cutoff reproduces the N14 sampled exit pattern. The samples do not certify a continuous crossing-time interval by rigorous numerical enclosure.

## N16 frozen before data

Seed `20260941`, unchanged K36 and its criteria, the same 520-proposal structure, and the same three-state time-gate tests are now frozen. Search grid 64 replaces 48 because the objective requires `grid > 3N` and `3*16=48`. The fixed winner will be checked at 64/96/128. The trial-0 smoke scores only baseline and inherited states after the freeze merge; no N16 proposal or N16 scientific output was included in that commit. The Windows runner and specialist code live in the canonical repository.

## Proof boundary

The N14 and N15 results are prospective **finite-Galerkin** replications. They do not establish an all-N property, cutoff-uniform estimate, continuum convergence, global phase optimum, finite-time blowup, or global regularity of three-dimensional Navier–Stokes. A fixed K36 mass fraction at least 90% is known to be false over arbitrary Galerkin states; the observed transfer applies to the prescribed continuation trajectories. The [26 September status](CURRENT_STATUS_2026_09_26.md) is preserved as historical state at the time it was written.
