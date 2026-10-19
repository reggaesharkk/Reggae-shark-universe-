# WP16 Shell-7 / Shell-4 Internal Compression Result — Strong Orbit Compression with Mechanism Mismatch

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed finite N=11 structured-class compression audit.  
**Source artifact:** `wp16_shell7_shell4_internal_compression_results.json`

## Target

The dominant radial subset contains 314 inherited old-core phase pairs from shells 7 and 4.

Applied together, they yield

[
C: 6.7876710 	o 7.1346684,
]

for

[
oxed{+5.1122%}
]

quotient gain, with

[
N_2^{>2}: +1.6965%,
qquad
P_+: -3.2495%.
]

## Strongest taxonomy — sorted absolute-coordinate orbit

The classes

[
operatorname{sort}(|k_1|,|k_2|,|k_3|)
]

produce the sharpest compression.

The dominant single orbit is

[
oxed{[0,3,6]},
]

containing only 12 phase pairs. Applied alone, it gives

[
C:+2.8114%,
qquad
N_2^{>2}:+2.3316%,
qquad
P_+:-0.4666%.
]

Thus one 12-pair orbit recovers about 55.0% of the total shell-7/4 quotient gain.

The first three ranked orbit classes

[
[0,3,6],quad[0,2,3],quad[1,4,5]
]

use 48 phase pairs and yield

[
C:+4.2873%,
]

about 83.9% of the full target gain.

The first six ranked orbit classes

[
[0,3,6],;
[0,2,3],;
[1,4,5],;
[0,1,3],;
[0,1,6],;
[1,1,3]
]

use only 84 of 314 pairs, about 26.8% of the target set, yet yield

[
oxed{C:+5.0946%},
]

which is about

[
oxed{99.66%}
]

of the full shell-7/4 quotient gain.

This is strong structural compression.

## Important mechanism mismatch

The 84-pair six-orbit subset does **not** reproduce the full denominator depletion.

For the six-orbit subset,

[
P_+:-2.3298%,
]

whereas the full 314-pair target gives

[
P_+:-3.2495%.
]

So the six-orbit set recovers only about 71.7% of the full positive-stretching depletion.

It matches the quotient because its numerator gain is larger:

[
N_2^{>2}:+2.6461%
]

versus

[
+1.6965%
]

for the full target.

Therefore the compression result is:

[
oxed{
	ext{strong compression of quotient gain}
}
]

but not yet

[
oxed{
	ext{equally strong compression of the denominator-relaxation mechanism}.
}
]

## Other taxonomies

The parity partition is coarser. Its leading 45-pair class ([0,0,1]) gives about (+2.98%) in (C), but recovering the full target quotient gain requires most parity classes.

The sign-pattern taxonomy also compresses reasonably well. A 225-pair cumulative subset reaches about (+5.098%) in (C), roughly 99.7% of the full quotient gain, while recovering about 93.8% of the full positive-stretching depletion. However, this uses about 71.7% of the target pairs, so it is less compact than the absolute-coordinate orbit basis.

## Interpretation

The strongest new structural clue is the coordinate-magnitude orbit

[
[0,3,6].
]

This orbit alone carries over half of the shell-7/4 quotient gain with only 12 phase pairs.

The next five useful absolute-coordinate orbits then nearly saturate the quotient gain.

This suggests that the apparently 314-dimensional correction is governed by a small number of geometric mode families.

However, the compact orbit basis reproduces the quotient more efficiently than it reproduces the denominator depletion itself. Therefore the next question is whether these same orbit families persist across the previous cutoff step and whether their first-order effects span a low-rank gain space.

## Next gate

Perform a cross-cutoff orbit/rank audit on the N=10 and N=11 old-core corrections.

For each cutoff step:

1. construct the same sorted absolute-coordinate orbit classes;
2. measure each orbit's directional effect on
   [
   deltalog N_2^{>2},
   qquad
   -deltalog P_+,
   qquad
   deltalog C;
   ]
3. build an orbit-response matrix;
4. compute its singular spectrum and numerical rank;
5. test whether dominant orbits such as ([0,3,6]) recur or scale naturally.

This is the direct LRSC-style crossover: replace thousands of phases by a finite orbit basis and ask for the effective response rank.

## Scope boundary

This is a finite N=11 structured compression result. It does not establish persistence across cutoffs, an all-N orbit law, asymptotic divergence, singularity formation, or global regularity.
