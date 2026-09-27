# WP16 N12/N13 source-resolved K36 turnover audit

Prince Upadhyay, Independent Research — post-hoc diagnostic, 27 September 2026

## Boundary

This analysis follows the frozen N12/N13 holdouts and the later prospective
N14/N15/N16 time gates. It is **post-hoc mechanism analysis**. The N11-derived
K36 coalition, all frozen pass criteria, and every archived prospective result
remain unchanged. Nothing in this note is a new prospective holdout.

The reconstruction uses the exact finite Galerkin states and dealiased ODE
already used by the trajectory audits. The input byte hashes are pinned in
`src/wp16_036_N12_N13_turnover_source_rates.py`:

- N10/N11 continuation:
  `34a10cf119ab6614c46d29540c4d4701eab082229582fb0a8189add0cd8f96a5`
- N12 continuation:
  `ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855`
- N13 continuation:
  `13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd`
- original N11 RHS source record:
  `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`

## Quantity differentiated

Write the frozen grouped absolute mass as

`F = I - 9 O`,

where `I` is K36 absolute mass and `O` is the sum of all outside-K36
ordered source-orbit absolute masses. For each reconstructed state, every
ordered group is evaluated at `a-hRHS(a)`, `a`, and `a+hRHS(a)` with
`h=1e-8`. Central directional differences give the group absolute-mass
rates. Summing them gives

`F' = I' - 9 O'`.

Because absolute values are present, these are local directional derivatives
of the finite diagnostic, not a smooth global identity across possible kinks.

The six anchor `F'` values agree with the previously archived
`K36_margin_velocity_N12_N13.json` diagnostic to better than `1.2e-4`.
A dedicated N13-inherited anchor stability check gives:

| finite-difference h | F' |
|---:|---:|
| 5e-9 | 208744.06745301446 |
| 1e-8 | 208744.06745198860 |
| 2e-8 | 208744.06745008568 |

The spread is about `2.93e-6`.

## Aggregate turnover

| cutoff | state | F'(0) | I'(0.001) | O'(0.001) | F'(0.001) |
|---|---|---:|---:|---:|---:|
| N12 | inherited | +401321.345 | +82978.875 | +37243.395 | **-252211.678** |
| N12 | target_only | +401330.158 | +82984.418 | +37238.027 | **-252157.821** |
| N12 | full_final | +209854.161 | +212112.718 | +49727.978 | **-235439.081** |
| N13 | inherited | +208744.067 | +184492.903 | +50077.037 | **-266200.434** |
| N13 | target_only | +187391.873 | +56749.214 | +38729.845 | **-291819.387** |
| N13 | full_final | +121276.530 | +67719.361 | +34063.935 | **-238856.054** |

Thus the turnover is not caused by the inside K36 mass beginning to shrink at
`t=0.001`: **I' remains positive in every state.** The sign reversal occurs
because the outside absolute mass is also growing, and `9 O'` has become
larger than `I'`.

## A recurrent outside ordered orbit

The most conspicuous source-level observation is the ordered orbit pair

`([3,3,4], [0,2,3])`.

At the anchor, its outside absolute-mass rate is negative in all six states:

| state | N12 rate at t=0 | N13 rate at t=0 |
|---|---:|---:|
| inherited | -3961.399 | -2870.921 |
| target_only | -3961.346 | -3719.041 |
| full_final | -2855.785 | -1696.481 |

By `t=0.001`, the sign has reversed and this same ordered orbit is the
**largest positive outside-K36 group rate in all six states**:

| state | N12 rate at t=0.001 | N13 rate at t=0.001 |
|---|---:|---:|
| inherited | +13224.116 | +13260.982 |
| target_only | +13224.359 | +12044.980 |
| full_final | +13445.567 | +9597.679 |

For the six `t=0.001` snapshots this single group contributes roughly
27%–36% of the **net** outside-mass growth rate. It is therefore a major
finite-trajectory contributor to the adverse `-9O'` term, although it does
not by itself account for the full turnover.

Several other ordered orbit identities recur in the top-10 positive outside
rates across all twelve anchor/`t=0.001` snapshots. In particular
`([1,4,4],[1,1,2])`, `([0,2,3],[2,3,9])`, and
`([1,1,2],[1,2,8])` appear in the top ten in all twelve snapshots. This is
descriptive persistence of source identities, not a proof of an invariant
finite source set.

## Connection to the N16 post-hoc attribution

PR #94 independently found that at N16 `t=0.0023`, the same ordered orbit
`([3,3,4],[0,2,3])` is the **largest outside-mass decrease** when comparing
`full_final` against `inherited`: its absolute contribution is lower by
about `4.50827`, while total outside mass is lower by about `4.44520`.

These are two different diagnostics:

- the N12/N13 quantity here is a **time-directional rate** along one
  trajectory;
- the N16 PR #94 quantity is a **state difference** between two trajectories
  at a fixed time.

The repeated ordered-orbit identity is therefore a useful structural clue,
but it is not valid to equate the two quantities or call the N16 difference a
measured suppression rate. PR #94 also showed that the N16 net outside
advantage is predominantly tied to the changing tracked complex normalizer,
so any stronger mechanistic model must track both the orbit numerator and the
normalizer.

## What this explains, and what it does not

The finite N12/N13 turnover now has a source-resolved description:

1. K36 inside mass is still growing at `t=0.001`.
2. Outside-K36 mass growth accelerates enough that `9O'` overtakes `I'`.
3. A recurrent ordered orbit, `([3,3,4],[0,2,3])`, changes from decaying at
   the anchor to the largest outside growth rate at `t=0.001` in all six
   N12/N13 states.
4. The same orbit reappears as the leading N16 state-difference attribution,
   but N16 also demonstrates that the tracked complex normalizer matters
   materially.

This does **not** prove that the orbit dominates at every cutoff or later
time, does not control the time integral of `O'`, and does not produce an
all-N or continuum estimate. The next prospective mechanism test, if one is
created, must freeze predictions for both the recurrent complex-group
numerator and the tracked normalizer before looking at new cutoff data.

## Reproduction

After decompressing the canonical source JSON, run:

```bash
OPENBLAS_NUM_THREADS=1 python src/wp16_036_N12_N13_turnover_source_rates.py \
  --n10-n11 results/wp16_n12_holdout/wp16_phase_cutoff_escalation_N10_N11.json \
  --n12 results/wp16_n12_holdout/wp16_phase_cutoff_escalation_N12.json \
  --n13 results/wp16_n13_holdout/wp16_phase_cutoff_escalation_N13.json \
  --source wp16_036_phase_velocity_rhs_sources.json \
  --output K36_turnover_source_rates_N12_N13_reproduced.json
```

The repository stores the compact checked summary in
`results/wp16_n13_holdout/K36_turnover_source_rate_summary_N12_N13.json`.
The runner emits the top five outside growth groups for all twelve snapshots
plus cross-snapshot frequency and the finite-difference stability record.
