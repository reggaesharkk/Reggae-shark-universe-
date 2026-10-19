# WP16 [0,3,6] Mechanism Result — Stable Numerator Construction with an Output-Channel Signature

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed finite mechanism audit.  
**Source artifact:** `wp16_036_resonance_mechanism_results.json`

## Main result

The orbit

[
oxed{[0,3,6]}
]

remains exceptional across all three tested recursive steps.

Its directional quotient responses are

[
dlog C=
0.0121484quad(N8	o N9),
]

[
0.00920375quad(N9	o N10),
]

[
0.0451562quad(N10	o N11).
]

Unlike the nearby controls, [0,3,6] also produces a positive numerator change at all three endpoints:

[
+0.5671%,quad +0.4851%,quad +2.3316%.
]

At the same time, (P_+) decreases at all three endpoints:

[
-0.7555%,quad -0.4679%,quad -0.4666%.
]

Thus the [0,3,6] effect is neither numerator-only nor denominator-only. It is a mixed mechanism with stable positive numerator construction plus positive quotient contribution from stretching depletion.

## Not explained by total triad participation

The target orbit touches only about 5% of the exact finite-Galerkin coefficient envelope:

[
4.93%,quad5.34%,quad5.10%
]

over the three steps.

The nearby orbit [0,3,5] touches more envelope, roughly 5.9–6.5%, yet its numerator response is weak or negative.

Therefore the exceptional [0,3,6] response is not explained by simply participating in more weighted triads.

The scaled-ratio controls also fail to reproduce the target:

- [0,2,4] remains much weaker;
- [0,4,8] is essentially inactive at N10 and N11.

This weakens a generic 1:2 coordinate-ratio explanation.

## Output-channel signature

At (N10	o N11), [0,3,6] changes the total high-tail transfer by

[
+473{,}520.844.
]

The role decomposition is:

[
	ext{target as advector}: +82{,}251.632,
]

[
	ext{target as advected mode}: -263{,}856.260,
]

[
	ext{target as output}: +655{,}425.350.
]

The output-role term alone is approximately

[
+3.2273%
]

of the pre-update total numerator and overcomes the negative advected-role contribution.

Moreover, the target-as-output triads move from negative signed transfer before the phase correction

[
-194{,}992.006
]

to positive signed transfer after it

[
+460{,}433.344.
]

This is the sharpest structural clue from the audit.

## Interpretation

The evidence favors:

[
oxed{
	ext{a specific partner-triad phase reorganization feeding the [0,3,6] output channel}
}
]

over the alternatives:

- generic large triad participation;
- generic scaled-coordinate geometry;
- denominator depletion alone;
- a smooth [0,3,m] arithmetic family law.

The term “resonance” remains only a hypothesis label. No resonance theorem has been established.

## Next gate

Decompose the target-as-output triads for [0,3,6] by the orbit classes of the two partner modes.

For each step, rank partner-orbit pairs by:

1. signed transfer change (Delta N);
2. coefficient envelope (A);
3. before/after coherence (chi).

Then test whether the same small set of partner-orbit pairs dominates across multiple cutoff steps.

A persistent partner-pair pattern would provide a concrete finite triad motif suitable for analytical reconstruction.

## Scope boundary

This is a finite Fourier-Galerkin mechanism result. It does not establish an all-cutoff resonance law, asymptotic divergence, singularity formation, or global regularity.
