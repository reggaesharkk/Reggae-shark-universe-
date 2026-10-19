# WP16 Frozen k-Channel Coalition Transfer Result and N12 Holdout Gate

**Prince Upadhyay, Independent Research — 26 September 2026**

The frozen N11 target-only k-channel source ranking transfers strongly across all previously generated N9, N10, and N11 states.

For the fixed prefix

[
K=36,
]

the same ordered source-orbit set has the same sign as the full k-channel in all 9 tested states.

Its absolute source-mass recovery lies in

[
[0.9335,;0.9520],
]

and its signed share of the full k-channel lies approximately in

[
[0.8525,;1.1611].
]

The larger fixed prefix (K=89) recovers approximately 97.66%–99.02% of absolute source mass with the same sign in all states.

The smaller (K=5) set also gets the sign right in all 9 states, while capturing about 46.8%–57.3% of absolute mass.

The (K=11) prefix exhibits one sign failure at the N10 target-only state, showing that cancellation can make an apparently substantial partial source set misleading.

## Prospective N12 holdout

The next test is frozen before N12 is generated.

Primary frozen coalition:

[
oxed{K=36}
]

using the exact first 36 ordered source-orbit keys from the N11 target-only k-channel ranking already recorded in

[
	exttt{wp16_036_phase_velocity_rhs_sources.json}.
]

Generate one new continuation step

[
N11	o N12
]

with the existing deterministic continuation runner.

Then evaluate the frozen K=36 source set at three N12 states:

1. inherited N11 phases embedded in N12;
2. [036]-target-only correction;
3. full final N12 phase state.

### Prospectively declared descriptive criteria

The N12 result will be called **consistent with prior transfer behavior** only if all three states satisfy:

[
	ext{same sign as the full k-channel},
]

[
	ext{absolute source-mass fraction}ge0.90,
]

and

[
0.80le
rac{	ext{frozen K36 signed contribution}}
{	ext{full k-channel signed contribution}}
le1.20.
]

These thresholds are calibrated from the already-observed N9–N11 finite states and are not universal constants.

Failure of any criterion will be preserved as a failed holdout rather than retuning the source set.

Finite cutoff holdout only; no continuum or all-N claim.
