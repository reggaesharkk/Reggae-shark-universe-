# Navier–Stokes Bridge Audit — Current Status

**Prince Upadhyay, Independent Research**  
**Updated:** 26 September 2026

Canonical specialist repository: https://github.com/reggaesharkk/navier-stokes-bridge-audit

## Prospectively frozen N12 holdout

The ordered K36 source-orbit coalition and descriptive three-state pass criteria were fixed in [PR #73](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/73) before N12 generation. The new finite N12 continuation was then evaluated without changing the coalition or thresholds. [The full result](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/9caa90e3defb5e64efbe132a45623a24902b3ba0/notes/WP16_036_N12_FROZEN_K36_HOLDOUT_RESULT_2026_09_26.md) and [raw files with checksums](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/9caa90e3defb5e64efbe132a45623a24902b3ba0/results/wp16_n12_holdout/) are in the specialist repository; [the result note is mirrored here](WP16_036_N12_FROZEN_K36_HOLDOUT_2026_09_26.md).

| N12 state | Absolute source mass captured | K36 signed / full signed | Same sign | Predeclared gate |
|---|---:|---:|---|---|
| Inherited | 94.0485% | 1.014401 | Yes | Pass |
| Target only | 94.0487% | 1.014404 | Yes | Pass |
| Full final | 93.5198% | 1.031871 | Yes | Pass |

The required absolute mass fraction was at least 90%, and the signed share had to lie in [0.80, 1.20], with the same sign as the full channel, at each state. All 36 frozen keys were present in each state. Stored ratios, flags, and checkpoint/final-row consistency were checked; this is not a separate independent solver run.

The fixed-phase, grid-96 refined quotient at N12 is **8.692984814467122**. The prior refined values are N7 3.744126696758515, N8 4.656046627246442, N9 6.261042251605425, N10 7.159655718793216, and N11 8.034885796422683. Each value is from a finite optimized state at its cutoff. Their increase does not prove growth at every cutoff or in the limit.

## N13 frozen K36 holdout — completed

[PR #75](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/75) froze the same K36 source set, three state definitions, and criteria before N13 generation. The [gate](WP16_036_N13_FROZEN_K36_HOLDOUT_GATE_2026_09_26.md) and [completed result](WP16_036_N13_FROZEN_K36_HOLDOUT_RESULT_2026_09_26.md) are mirrored here; the [raw files and checksums](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/2aeb208341a5dc1b60aa25fb3c0c4965a8f2175e/results/wp16_n13_holdout/) are in the specialist repository.

| N13 state | Absolute source mass captured | K36 signed / full signed | Same sign | Frozen gate |
|---|---:|---:|---|---|
| Inherited | 93.5731% | 1.029876 | Yes | Pass |
| Target only | 93.9559% | 1.024681 | Yes | Pass |
| Full final | 93.4538% | 1.025928 | Yes | Pass |

The N13 grid-96 refined quotient is **9.341290048632342**. Colab disconnected during optimization; the run was resumed from saved accepted states under the same deterministic proposal schedule. The original checkpoint cannot establish which candidate evaluations, if any, were lost between its last save and disconnection. Recovery provenance and its limitations are stated in the result note.

## N14 prospective frozen K36 time gate — completed

The N14 continuation and time-resolved hypotheses were frozen in the specialist repository before any N14 state or score existed, with the N11-derived K36 coalition and thresholds unchanged. The completed [prospective N14 result](WP16_036_N14_PROSPECTIVE_TIME_GATE_RESULT_2026_09_26.md) is now mirrored here; the canonical specialist merge is [PR #90](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/90).

The frozen continuation completed all 520 proposals with seed `20260939` and search grid 48. The same winning phase vector was then evaluated without retuning at grids 48/64/96/128, giving `C_infinity_stretch` values 9.6385177811, 9.6379562385, 9.6394090993, and 9.6395821055 respectively.

The prospective time gate then evaluated `inherited`, `target_only`, and `full_final` under the unchanged K36 criteria. All three states:
- passed the static gate;
- passed the 90% mass criterion at every sampled point through `t=0.0010`;
- had their first sampled mass exit at `t=0.0023`, inside the predeclared `[0.0015,0.0030]` window;
- still passed the signed criterion at that exit;
- had positive initial `dF/dt`;
- had negative full, radial-magnitude, and vector-polarization margin rates at the first mass exit.

The half-step check at `dt=0.00005` kept all three states above 0.90 at `t=0.00225` and below 0.90 at `t=0.00230`, with coarse/half-step mass-fraction differences at the coarse exit of order `10^-9` or smaller.

This is a clean prospective finite-Galerkin replication at N14. It is not an all-N theorem, continuum-limit result, global-optimization certificate, or proof of Navier–Stokes regularity.

## N15 prospective protocol — frozen before data

After recording N14, [the N15 continuation and time-gate protocol](WP16_036_N15_PROSPECTIVE_FREEZE_2026_09_26.md) was frozen and merged before any N15 state, score, checkpoint, or time-gate output existed. It retains the same K36 coalition, thresholds, objective, reconstruction semantics, time window, and local-rate tests.

The frozen N15 continuation uses seed `20260940`, search grid 48 (`48 > 3*15`), the same 520-proposal schedule, and refinement grids 48/64/96/128. The exact N14 predecessor hash and frozen source-decomposition hash are locked. A trial-0 memory/smoke check must precede any N15 search proposal. No N15 scientific outcome exists at the time of this status update.

## Post-hoc outside-K36 composition

[The N12–N13 source-group breakdown](WP16_036_OUTSIDE_K36_N12_N13_POSTHOC_2026_09_26.md) reproduces the frozen holdout totals for all six states. There are 2,160 outside groups at N12 and 2,926 at N13; in the full-final N13 state, the 766 new groups contribute only 1.33380 of 67.96625 outside absolute mass. The largest outside groups were already present at N12, and positive and negative terms cancel substantially. This finite diagnostic does not establish a uniform-in-N bound.

## All-state scope boundary

An [explicit N=7 real divergence-free witness](WP16_036_FIXED_K36_ALL_STATE_NOGO_2026_09_26.md) shows that a fixed K36 absolute-mass fraction of at least 90% is false over arbitrary Galerkin states: scaling two source modes outside K36 makes the fraction tend to zero. This post-hoc result leaves the N12/N13 phase-only holdouts intact and narrows any future analytic claim to a controlled state or trajectory class.

## Conditional phase-uniform bound and open signed gap

[The post-hoc analysis](WP16_036_PHASE_UNIFORM_TAIL_AND_SIGNED_GAP_2026_09_26.md) proves an N-independent high-shell inequality conditional on uniform H² energy and nondegeneracy of the tracked anchor. The exact source-magnitude envelope is invariant under phase rotations at each fixed cutoff. Low outside groups dominate the finite residual; a high-tail bound alone does not certify the frozen K36 gate. In 64 exploratory fixed-magnitude N13 phase draws, all met the 90% mass condition but nine failed the signed condition. These draws are not a prospective holdout or a theorem about all phases.

## Scope

The project now contains successful prospective finite-cutoff transfer evidence at N12, N13, and the stronger time-resolved N14 test, all using the N11-derived K36 coalition without retuning. N15 is frozen prospectively but has not yet been run. None of this establishes an all-N phase law, a cutoff-uniform estimate, a continuum result, finite-time blowup, or arbitrary-data global regularity. The historical [25 September status](CURRENT_STATUS_2026_09_25.md) remains available unchanged.
