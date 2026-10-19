# WP16 Targeted Orbit-Family Result — [0,3,6] Persists, Smooth [0,3,m] Law Not Supported

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed targeted three-step family audit.  
**Source artifact:** `wp16_targeted_orbit_family_scan_results.json`

## Primary family

The targeted family was

[
[0,3,m],qquad m=3,dots,10.
]

Matched nearby controls were included:

[
[0,2,m],qquad [0,4,m],qquad [1,3,m].
]

The scan used the already-generated continuation states

[
N8	o N9,qquad N9	o N10,qquad N10	o N11.
]

## Strongest result — [0,3,6]

The orbit

[
oxed{[0,3,6]}
]

is present and positive in (dlog C) across all three available recursive steps:

[
dlog C=
0.0121484098quad(N8	o N9),
]

[
0.0092037462quad(N9	o N10),
]

[
0.0451562098quad(N10	o N11).
]

Its three-step geometric-mean positive response is

[
0.0171553869.
]

This makes [0,3,6] a substantially stronger persistence candidate than the broader arithmetic family itself.

## The [0,3,9] prospective test

The orbit

[
[0,3,9]
]

first becomes available in the inherited N10 support for the (N10	o N11) step.

Its measured directional response is

[
dlog N=0.0002860444,
]

[
-dlog P_+=-0.0002830200,
]

so that

[
oxed{dlog C=3.02437	imes10^{-6}>0}.
]

The full-orbit endpoint quotient gain is only

[
oxed{+0.0014536%}.
]

Thus the sign is positive, but the magnitude is extremely small compared with [0,3,6].

The prospective sign guess therefore succeeds only in the weak sense that the response is positive. It does not support a strong monotone or arithmetic growth law.

## Family-level interpretation

The family does not show uniform positive persistence.

For example:

- [0,3,7] is negative at N8→N9 but positive at the next two steps;
- [0,3,4] changes sign across the three steps;
- [0,3,3] becomes negative at N10→N11;
- [0,3,8] is positive over the two steps in which it is available;
- [0,3,9] is positive at its first available step, but only very weakly.

Therefore the data do not support a smooth rule of the form

[
[0,3,6]	o[0,3,7]	o[0,3,8]	o[0,3,9]
]

with stable or increasing efficacy.

The strongest structural interpretation is instead

[
oxed{	ext{[0,3,6] is an exceptional persistent orbit within the tested family.}}
]

## Control comparison

The matched controls show that positivity at (m=9) is not unique to [0,3,9]. Nearby families can also yield positive responses at the same step.

Therefore the positive sign of [0,3,9] should not be interpreted as evidence of a special arithmetic generator law.

## Next analytical target

The next gate should investigate why [0,3,6] is exceptional.

In particular, audit its triadic participation, coefficient weights, numerator/denominator split, and comparison with nearby ratio-related orbits such as

[
[0,2,4],qquad[0,4,8],
]

as well as neighboring members

[
[0,3,5],qquad[0,3,7].
]

The aim is to distinguish:

1. a true resonance/triad-geometry mechanism;
2. a denominator-depletion effect;
3. an optimizer-specific finite configuration.

## Scope boundary

This is a finite three-step targeted diagnostic. It does not establish an all-cutoff orbit law, asymptotic behavior, singularity formation, or global regularity.
