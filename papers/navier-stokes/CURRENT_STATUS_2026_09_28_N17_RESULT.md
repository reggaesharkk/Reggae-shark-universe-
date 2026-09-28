# Navier–Stokes bridge audit: N17 result status (28 September 2026)

The N17 protocol was frozen in the specialist repository before scientific N17 data (PR #98, commit `71fb018aab7e028406698a82e8a8a5bcd87f64c5`). The completed seed `20260942`, grid-64 continuation ran 520/520 proposals. Its fixed winner refined to `10.356696358903514` on grid 128. The N11-derived K36 coalition was retained without retuning.

**Broad time gate:** all three states pass the frozen static, early persistence, exit-window, signed-share, and local margin-rate sign tests. Inherited, target-only, and full-final first fall below the 90% mass threshold at sampled `t=0.0024`, with the signed criterion still passing. The half-step differences at the coarse exit are at most `1.33e-8`. This repeats the broad finite-cutoff pattern, though N16's full-final extra coarse step relative to inherited is absent at N17.

**Separate mechanism gate:** the frozen evaluator returned nonzero at `directional split failed: ((1, 7, 9), (2, 7, 15))`, before completing the joint prediction list. The prospective outcome is **failed or unevaluable**. A separate post-hoc diagnostic identified an absolute-value kink and additional substantive misses: the recurrent orbit does not become the leading positive outside rate at `t=.001` in any of the three N17 states, and the `.0023` normalizer sign/dominance prediction does not hold. This is not a repaired prospective pass.

See the [dated result note](WP16_036_N17_RESULT_AND_MECHANISM_FAILURE_2026_09_28.md) for hashes, values, and the boundary between frozen and exploratory observations. Canonical output artifacts and the [machine summary](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/results/wp16_n17_holdout/wp16_036_N17_result_summary.json) are in the specialist repository, merged in [PR #99](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/99). The [N16 status](CURRENT_STATUS_2026_09_27_N16_RESULT.md) is retained as historical record.

These finite Galerkin observations establish neither an all-cutoff theorem nor continuum regularity or singularity.

The [post-hoc N11 sparse turnover reduction](papers/navier-stokes/WP16_036_SPARSE_TURNOVER_REDUCTION_2026_09_28.md) retains 112 initial conjugate pairs and numerically changes the K36 margin from positive to negative by `t=.003`. Its [exact rational initial anchor](papers/navier-stokes/WP16_036_SPARSE_TURNOVER_EXACT_ANCHOR_2026_09_28.md) certifies `F(0)>0` for a precisely projected rational field. The evolved negative sign is not yet interval-certified.
