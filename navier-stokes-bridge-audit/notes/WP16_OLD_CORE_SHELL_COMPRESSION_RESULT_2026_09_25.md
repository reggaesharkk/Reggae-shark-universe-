# WP16 Old-Core Shell Compression Result — Moderate Radial Compression

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed finite N=11 shell-block compression audit.  
**Source artifact:** `wp16_old_core_shell_compression_results.json`

## Baseline

The full inherited-core correction contains 2,084 active phase pairs and yields, on the registered (48^3) audit grid,

[
C: 6.7876710 	o 7.3763172,
]

for an old-core gain of

[
oxed{+8.6723%},
]

with

[
N_2^{>2}: +2.2451%,
qquad
P_+: -5.9143%.
]

## Strongest single shell

Shell 7 contains 247 inherited pairs and is the strongest isolated radial block:

[
C	ext{-gain}=+3.4218%,
]

[
N_2^{>2}: +1.4161%,
]

[
P_+: -1.9394%.
]

Its small-amplitude directional estimate is also the largest:

[
dlog C/dlambdaapprox0.05678.
]

Thus shell 7 is the clearest radial candidate for further internal compression.

## Cumulative shell compression

Ranking radial blocks by isolated endpoint log-C gain gives

[
7,;4,;8,;5,;6,;10,;9,;3,;2,;1.
]

The cumulative gains are:

- shell 7 only: (+3.4218%);
- shells 7+4: (+5.1122%);
- shells 7+4+8: (+6.3600%);
- shells 7+4+8+5: (+7.1614%);
- shells 7+4+8+5+6: (+7.7218%).

The five-shell set uses 993 of the 2,084 inherited pairs, about 47.65% of the old core, yet recovers:

- about **89.0% of the full old-core quotient gain**;
- about **85.5% of the full old-core positive-stretching depletion**.

This is meaningful compression, but not a collapse to a tiny number of modes.

## Denominator role by shell

Several shells improve (C) primarily by reducing (P_+):

- shell 4:
  [
  C:+1.4273%,quad N:+0.0478%,quad P_+:-1.3601%;
  ]
- shell 6:
  [
  C:+0.5831%,quad N:-0.5579%,quad P_+:-1.1344%.
  ]

Shell 7 improves both numerator and denominator and is therefore the strongest mixed radial block.

## Interpretation

The old-core denominator-relaxation mechanism is **moderately compressible by radial shell**.

A small number of shells do carry most of the useful effect, but the compression is not yet analytically simple enough to be called a shell law. Nearly half of the inherited active pairs are still needed to recover roughly 89% of the quotient gain.

The strongest next target is therefore not another radial decomposition. It is to compress the dominant shell blocks internally.

## Next gate

Focus on shells 7 and 4 first.

Within each shell, partition inherited active modes by structured classes such as:

- parity signature ((|k_1|,|k_2|,|k_3|)mod2);
- octant/sign pattern;
- coordinate-magnitude orbit after sorting ((|k_1|,|k_2|,|k_3|));
- participation weight in the dominant shell-4/5 transfer network.

Evaluate each class alone and cumulatively.

The goal is to determine whether the shell-7 and shell-4 effects are carried by a small symmetry/interaction family rather than hundreds of idiosyncratic phase corrections.

## Scope boundary

This is a finite N=11 compression result on the registered optimizer. It does not establish an all-cutoff shell law, asymptotic divergence, singularity formation, or global regularity.
