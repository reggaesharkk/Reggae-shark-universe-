# WP16 Positive-Stretching Depletion Result — Broad Redistribution, Not Extreme-Tail Clipping

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed physical-space audit on the verified N=11 continuation.  
**Source artifact:** `wp16_positive_stretching_depletion_results.json`

## Comparison

The audit compares two N=11 states with identical evolved modal magnitudes and polarizations:

1. the inherited N=10 optimized phase map embedded into the N=11 support, with newly opened phases set to zero;
2. the final optimized N=11 phase map.

Only Fourier phases differ.

The local field is

[
F(x)=omega(x)cdot S(x)omega(x),
qquad
P_+=langle F_+angle.
]

The calculation was repeated on (48^3,64^3,96^3) grids.

## Result 1 — stable depletion across grid refinement

At (96^3),

[
P_+^{m inherited}=266002.7690,
]

[
P_+^{m optimized}=249370.5601,
]

so

[
oxed{Delta P_+/P_+approx-6.2526%}.
]

The corresponding changes are (-6.2486%) at (48^3) and (-6.2404%) at (64^3).

Thus the depletion is stable across the tested physical grids.

## Result 2 — positive-set volume shrinks only modestly

At (96^3),

[
	ext{vol}(F>0):
0.37538	o0.36846,
]

a relative change of only

[
oxed{-1.8437%}.
]

The reduction in (P_+) is therefore much larger than the reduction in the volume of the positive set.

This rejects the simplest picture in which the denominator falls mainly because a large portion of the positive region changes sign.

## Result 3 — the normalized tail contribution is nearly unchanged

At (96^3), the top fractions of all grid points contribute:

- top 1%: (12.81%	o12.94%);
- top 5%: (41.43%	o41.63%);
- top 10%: (63.30%	o63.82%).

The relative concentration of the positive-stretching mass in the upper tail therefore changes only slightly.

This rejects a pure "clip the single hottest tail" mechanism.

## Result 4 — suppression is strongest in the middle-to-upper inherited positive quantiles

Using quantile bins defined by the inherited positive field, the optimized/inherited positive-sum ratios at (96^3) are

[
[0,50%]:quad 1.0180,
]

[
[50,90%]:quad 0.9041,
]

[
[90,95%]:quad 0.8777,
]

[
[95,99%]:quad 0.8758,
]

[
[99,100%]:quad 0.9049.
]

Thus the lowest half of inherited positive-stretching points slightly gains positive mass, while the upper half is depleted.

The strongest relative suppression occurs in the inherited 90–99% region, not in the top 1% alone.

This is a broad redistribution/depression mechanism with a pronounced upper-middle suppression band.

## Result 5 — the hot regions move substantially

At (96^3):

- positive-set Jaccard overlap: (0.7911);
- top-5% Jaccard overlap: (0.6208);
- top-1% Jaccard overlap: (0.5593).

So the optimizer does not simply scale down the same spatial hot spots. The hottest regions are reorganized appreciably while the broader positive set remains mostly overlapping.

## Interpretation

Together with the coefficient-weighted triad result, the current finite mechanism is:

1. the signed H2 transfer remains dominated by the old shell-4/5 core;
2. the new shell does not disproportionately carry the transfer;
3. the optimizer lowers global normalized triad coherence rather than raising it;
4. nevertheless the quotient rises because (P_+) falls;
5. that fall is not caused by removing a tiny extreme tail;
6. instead, positive stretching is broadly redistributed, with strongest suppression in inherited 90–99% positive quantiles and substantial movement of the hottest spatial regions.

The next useful object is therefore the **phase path** connecting the inherited and optimized states, not another static shell statistic.

## Next gate

Parameterize the shortest wrapped phase displacement by

[
phi(lambda)
=
phi_{m inherited}
+
lambda,Deltaphi,
qquad
0lelambdale1.
]

Along this path measure:

[
P_+(lambda),qquad
N_2^{>2}(lambda),qquad
C(lambda),
]

and compare three perturbation blocks:

- inherited-core phase corrections only;
- newly opened-shell phases only;
- both together.

This will determine whether the N=11 improvement is approximately additive, synergistic, or dominated by old-core denominator relaxation.

## Scope boundary

This is a finite physical-space diagnostic on one evolved N=11 state. It does not establish asymptotic growth, singularity formation, or arbitrary-data regularity.
