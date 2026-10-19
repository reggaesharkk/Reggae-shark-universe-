# WP16 Coefficient-Weighted Triad-Phase Result — Outer-Shell Alignment Falsified

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed exact finite-Galerkin decomposition on the verified N=10/N=11 phase-only continuation.  
**Source artifact:** `wp16_weighted_triad_phase_results.json`  
**Bytes:** 25,215  
**SHA-256:** `964eed439c04c6ee77a03a2da03b0ce39142d60f2ecb160b1a1849c88ac09e31`

## Question

The previous reverse-engineering gate found that raw mode phases and unweighted relative triad phases are nearly uniform, while the inherited phase core is strongly preserved from N=10 to N=11.

This gate asked whether the apparently random phase field hides a simpler mechanism:

> Does the optimizer preferentially align the strongest nonlinear triads, especially those touching the newly opened cutoff shell?

For each ordered high-advector interaction (p+q=k), the executed audit reconstructed

[
z_{kpq}
=
z_{kpq}^{(0)}
e^{i(phi_p+phi_q-phi_k)}
]

and verified the exact finite sums against the stored H2 high-transfer and absolute-envelope observables.

The relative reconstruction errors are below (1.6	imes10^{-15}) at N=10 and below (6.3	imes10^{-16}) at N=11.

## Result 1 — the new outer shell does not dominate the signed transfer

At N=10, triads touching the newly opened shell account for

- 12.5895% of the absolute H2 envelope;
- only 9.8321% of signed high transfer.

The new shell acting specifically as the advector accounts for only

- 0.6980% of the envelope;
- 0.5204% of signed transfer.

At N=11, triads touching the newly opened shell account for

- 10.5090% of the envelope;
- only 8.4491% of signed transfer.

The new shell acting specifically as the advector accounts for only

- 0.5503% of the envelope;
- 0.2137% of signed transfer.

Thus the simple hypothesis that cutoff growth is driven by a disproportionately effective newly opened shell is rejected on these two executed states.

## Result 2 — the older core carries the transfer

At N=10, old-only triads carry 87.4105% of the absolute envelope but 90.1679% of the signed transfer.

At N=11, old-only triads carry 89.4910% of the envelope but 91.5509% of the signed transfer.

The dominant advector shell is shell 4:

[
rac{N_{	ext{shell }4}}{N_{m total}}
approx0.69947quad(N=10),
]

[
rac{N_{	ext{shell }4}}{N_{m total}}
approx0.69779quad(N=11).
]

Shells 4 and 5 together carry about 91.07% of signed transfer at N=10 and 91.10% at N=11.

So the high-cutoff quotient growth is not accompanied by a migration of the dominant signed transfer to the newest shell.

## Result 3 — optimization does not increase global normalized triad coherence

At N=10:

[
chi_{m base}=0.1910356,
qquad
chi_{m opt}=0.1605984.
]

At N=11:

[
chi_{m base}=0.1901496,
qquad
chi_{m opt}=0.1585907.
]

Therefore the optimizer actually reduces the global signed-transfer fraction relative to the absolute triad envelope.

The coefficient-weighted phase resultant remains moderate:

[
R_Theta^{(w)}approx0.17684quad(N=10),
qquad
0.17573quad(N=11).
]

This rejects the stronger interpretation that the growing quotient is primarily produced by increasing global coefficient-weighted triad alignment.

## Result 4 — high shells can be phase-repaired without driving the total

Some high advector shells have negative base coherence but positive optimized coherence. For example, at N=11:

- shell 8: base (chiapprox-0.14775), optimized (chiapprox0.17417);
- shell 9: base (chiapprox-0.15095), optimized (chiapprox0.19662);
- shell 10: base (chiapprox-0.17616), optimized (chiapprox0.10571);
- shell 11: base (chiapprox-0.17151), optimized (chiapprox0.06159).

This demonstrates real phase repair in the high shells, but those shells carry too little absolute weight to explain the total quotient growth by themselves.

## Interpretation

The weighted-triad hypothesis has therefore narrowed the mechanism rather than produced the desired constructive shell law.

The finite evidence now supports the following picture:

1. low/mid shells, especially shell 4, continue to carry most signed H2 transfer;
2. newly opened high shells can be phase-repaired, but they are not disproportionately responsible for the total signed transfer;
3. the global optimized triadic coherence fraction decreases rather than increases;
4. meanwhile the previously verified quotient (C_N) rises and (b_{m stretch}) falls.

The leading target is therefore the denominator

[
P_+
=
leftlangle(omegacdot Somega)_+ightangle,
]

not further numerator-only phase alignment.

## Next gate

The next diagnostic should compare the N=11 inherited state against the final optimized state in physical space and determine how (P_+) is depleted:

- positive-set volume fraction;
- distribution and upper quantiles of positive stretching;
- contribution of the top 1%, 5%, and 10% of grid points;
- overlap and displacement of positive-stretching regions;
- inherited-field quantile bins evaluated after optimization.

If the optimizer suppresses a small, high-amplitude positive-stretching set while leaving the transfer-carrying core nearly intact, that could provide a much more explicit constructive mechanism.

## Scope boundary

This is an exact decomposition of two finite Galerkin states. It falsifies a specific finite mechanism for these states. It does not establish the asymptotic behavior of the phase-only supremum, an unbounded universal constant, singularity formation, or arbitrary-data regularity.
