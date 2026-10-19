# WP16 N16 outside-K36 group attribution and normalizer audit

Prince Upadhyay, Independent Research — post-hoc diagnostic, 27 September 2026

## Boundary and reproduction

This follows the frozen N16 result (canonical PR #92) and the aggregate exit
accounting (PR #93). It is **not** a prospective N16 test. The original N15
and N16 continuation JSONs and N16 time-gate JSON have pinned SHA-256 hashes
in the reproduction script. The 36 frozen ordered orbit pairs come from the
pre-N12 committed key list; the script checks that list's byte hash and its
original N11 source provenance field. Neither keys nor phases are retuned.

```bash
OPENBLAS_NUM_THREADS=1 python src/wp16_036_N16_group_attribution.py \
  --n15 wp16_phase_cutoff_escalation_N15.json \
  --n16 wp16_phase_cutoff_escalation_N16.json \
  --time-gate wp16_036_N16_frozen_time_gate.json \
  --frozen-keys results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json \
  --output wp16_036_N16_group_attribution_reproduced.json
```

The script reconstructs `inherited` and `full_final` using the existing N16
Galerkin ODE (`dt=0.0001`) through index 24. At **every** step it recalculates
inside mass, total absolute mass, and total signed contribution and compares
them with the archived time-gate rows (absolute tolerance `2e-7`). At seven
selected indices it ranks the ordered source-orbit groups; the compact output
retains the largest decreases/increases and the exact remainder sum. The
original continuation and time-gate JSONs are held in the user's results
folder; this repository stores the code, checked compact output, and note.

## Which groups changed?

At the critical `t=0.0023` sample, define `Δ=full_final−inherited`. The
previous accounting found `ΔI=-16.951556`, `ΔO=-4.445196`, and
`ΔF=ΔI−9ΔO=+23.055211`. There are 6,066 outside-K36 ordered orbit groups in
the reconstructed output channel. The largest decrease belongs to the
ordered pair `([3,3,4], [0,2,3])`:

| quantity at `t=0.0023` | inherited | full_final | difference in absolute mass |
|---|---:|---:|---:|
| outside group `([3,3,4],[0,2,3])` | +13.79519 | +9.28693 | **−4.50827** |
| all outside-K36 groups | 120.259756 | 115.814559 | **−4.445196** |

The one group decreases by slightly **more** than the entire net outside
decrease. Other groups collectively offset part of it. The twelve largest
outside decreases sum to `−7.019025`; all remaining outside groups together
sum to `+2.573829`. The leading increases include
`([0,1,3],[0,1,6])` (`+0.49014`) and `([1,4,7],[1,1,1])` (`+0.45146`).
The group ordering is `left_orbit, right_orbit`; reversing it is generally a
different ordered source.

## The denominator correction

The grouped diagnostic is `g_j=Im(C_j/z)`, with a **complex tracked
normalizer** `z` that itself changes between the two states. A smaller
`|g_j|` does not by itself mean the unnormalized source interaction is
smaller. To expose this ambiguity, write `A(C,z)=|Im(C/z)|` and use the exact
symmetric two-factor swap between inherited `(C_h,z_h)` and full-final
`(C_f,z_f)`:

`Δ_num = {A(C_f,z_h)−A(C_h,z_h)+A(C_f,z_f)−A(C_h,z_f)}/2`,

`Δ_z = {A(C_h,z_f)−A(C_h,z_h)+A(C_f,z_f)−A(C_f,z_h)}/2`.

Then `Δ_num+Δ_z=A(C_f,z_f)−A(C_h,z_h)` exactly, even across absolute-value
kinks. This is **counterfactual algebraic attribution**, not a physical
intervention, causal estimate, or time derivative. Aggregated over all outside
groups:

| sample | observed `ΔO` | complex group numerator swap | tracked normalizer swap |
|---:|---:|---:|---:|
| 0.0011 | −0.664375 | +0.456636 | −1.121011 |
| 0.0020 | −3.456491 | +0.232624 | −3.689115 |
| **0.0023** | **−4.445196** | **+0.858025** | **−5.303222** |
| 0.0024 | −4.906747 | +1.023709 | −5.930455 |

At `0.0023`, `|z_f|/|z_h|≈1.045573` and
`arg(z_f/z_h)≈−0.011143` radians. The leading decreasing group has a
`−3.89831` numerator-swap component and `−0.60995` normalizer-swap component;
the rest of the outside groups offset enough numerator decreases to make the
**aggregate** numerator-swap component positive. The net outside-mass
advantage is therefore predominantly a **normalization effect** in this
specific comparison. Calling it universal suppression of physical outside
triads would be incorrect.

The complete inside mass is also normalization-sensitive: at `0.0023`, its
numerator-swap component is `+40.514894` and its normalizer-swap component
`−57.466449`, summing to the observed `ΔI=−16.951556`. The signed comparison
remains the exact margin identity; the swap reveals why its ingredients must
not be read as standalone dynamical laws.

## What remains open

This identifies one leading ordered orbit and the crucial changing
normalizer for a **single finite N16 comparison**. It does not explain why
the ODE changes `z` by this amount, prove that the same orbit dominates at
other cutoffs, or bound the time integral of any source rate. A future
mechanistic hypothesis should specify the evolution of both the tracked
normalizer and the leading complex group numerators, then freeze its prediction
before testing on new data. None of these observations establishes an
all-cutoff theorem, a continuum limit, regularity, or blowup.
