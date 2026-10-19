# WP16 N13 prospective holdout gate — frozen before N13

**Prince Upadhyay, Independent Research · 26 September 2026**

**Status:** test specification and code frozen; N13 result pending. The N12 holdout passed all three states and was archived in PR #74. N12 is prior evidence, not part of the N13 holdout.

## Fixed inputs

- Coalition: the exact 36 ordered source-orbit keys selected from the N11-from-N10 target-only k-channel ranking, ordered by absolute signed contribution. The keys and full source ranking are archived under `results/wp16_n12_holdout/`.
- Uncompressed ranking input SHA-256: `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`.
- N12 continuation input SHA-256: `ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855`.
- No new ranking, coalition size choice, phase adjustment, or threshold tuning based on N13 is permitted for this gate.

## N13 generation

Resume the existing deterministic phase-only continuation from the archived N12 final state. Use one new cutoff `13`, amplitude and anchor inherited from N12 (`A=4`, `t=0.005`), default base seed `20260925` (effective seed `20260938`), search grid `40`, 16 new-mode global draws, 3 new-mode block rounds, 4 full block rounds, 72 trials per round, block size 40, and initial step 0.30. The existing runner refines the final fixed state on grids 40, 48, 64, and 96, as allowed by its `grid > 3N` rule. Preserve the checkpoint and completed JSON.

## Three prespecified evaluations

For the resulting N13 row, reconstruct:

1. `inherited`: N12 optimized phases on overlapping modes, zero phase for newly active pairs;
2. `target_only`: apply the N13 final phase change only on inherited pairs in target orbit `(0,3,6)`;
3. `full_final`: all final optimized N13 phases.

The evaluator uses the same `reconstruct`, `frozen_keys`, and `evaluate_state` functions as the N12 test, with the same source ordering and grouping rule. Input hashes and the single-step N12-to-N13 structure are checked before evaluation.

## Unchanged descriptive pass criteria

**Each** of the three states must satisfy:

- K36 signed contribution has the same sign as the complete k-channel;
- K36 captures at least `0.90` of the absolute grouped k-channel source mass;
- K36 signed contribution divided by complete signed k-channel is in `[0.80, 1.20]`.

The overall result passes only if all three states pass. A failure is recorded as observed; no replacement coalition or revised criterion counts as this test. These criteria were calibrated from N9–N11 and already used at N12. Passing N13 would add one more finite holdout; it would not establish an all-N theorem, a continuum phase mechanism, or Navier–Stokes regularity.

**Executable evaluator:** `src/wp16_036_N13_frozen_K36_holdout.py`. The Colab launcher is pinned to a fixed commit containing this gate and evaluator. No N13 output was available when this gate was written.
