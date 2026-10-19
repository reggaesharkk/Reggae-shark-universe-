# WP16 Two-Step Cross-Cutoff Orbit/Rank Result — Persistence Confirmed, Rank Test Saturates Algebraic Maximum

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed finite cross-cutoff orbit-response audit.  
**Source artifact:** `wp16_cross_cutoff_orbit_rank_results.json`

## Persistence result

The audit compared the registered inherited-core corrections for

[
N=9	o10
]

and

[
N=10	o11.
]

There are 109 absolute-coordinate orbit families shared across both steps.

All six orbit families previously identified as dominant at N=11 are present at N=10 and retain positive (dlog C) at both cutoffs:

[
[0,3,6],;
[0,2,3],;
[1,4,5],;
[0,1,3],;
[0,1,6],;
[1,1,3].
]

The strongest persistent orbit is again

[
oxed{[0,3,6]}.
]

Its directional response is

[
dlog Capprox0.00920quad(N=10),
]

[
dlog Capprox0.04516quad(N=11).
]

It is the top persistent-positive orbit by geometric-mean score across the two steps.

## Old-core mechanism changes across cutoffs

The full old-core correction improves the quotient at both steps, but the numerator behavior differs.

For (N9	o N10):

[
C:+7.2743%,
qquad
N_2^{>2}:-7.7434%,
qquad
P_+:-13.9993%.
]

For (N10	o N11):

[
C:+8.6723%,
qquad
N_2^{>2}:+2.2451%,
qquad
P_+:-5.9143%.
]

Thus denominator depletion persists as a common beneficial mechanism, while the numerator contribution is not sign-stable across the two steps.

## Rank interpretation correction

The original response matrix used six columns:

[
(
dlog N_{10},
-dlog P_{+,10},
dlog C_{10},
dlog N_{11},
-dlog P_{+,11},
dlog C_{11}
).
]

But at each cutoff,

[
dlog C
=
dlog N
+
(-dlog P_+),
]

so the matrix has two exact algebraic column dependencies.

Therefore its maximum possible rank is only 4.

The executed SVD gives four nonzero singular values and two values at numerical roundoff:

[
7.6	imes10^{-15},
qquad
7.4	imes10^{-15}
]

in the raw matrix.

The reported 99% effective rank of 4 therefore means the matrix attains its algebraic maximum. It is **not evidence of hidden low-rank collapse**.

The same conclusion holds after column standardization.

## Interpretation

The two-step gate yields a split result:

[
oxed{	ext{orbit persistence: supported}}
]

but

[
oxed{	ext{low-rank claim from this matrix: not supported}}.
]

The orbit family ([0,3,6]) is now a stronger candidate because it persists and remains positive across both steps.

However, the rank representation must be corrected before drawing structural conclusions.

## Next gate

Use three consecutive steps:

[
N8	o N9,quad N9	o N10,quad N10	o N11,
]

and construct the SVD only from the independent responses

[
(dlog N,,-dlog P_+)
]

at each cutoff.

This gives six genuinely independent response coordinates and tests both:

1. three-step persistence of the dominant orbit families;
2. meaningful numerical rank of the orbit-response space.

## Scope boundary

This is a finite two-step persistence result. It does not establish an all-cutoff orbit law, asymptotic divergence, singularity formation, or global regularity.
