> **Historical template notice — superseded later on 28 September 2026.**  
> The final interval certificate passed. See [WP16_036_N11_VALIDATED_TURNOVER_2026_09_28.md](WP16_036_N11_VALIDATED_TURNOVER_2026_09_28.md) for the certified finite theorem and final bounds.

# WP16 finite-N11 K36 crossing — publication note template

**Prince Upadhyay — Independent Research**  
**Date:** 28 September 2026  
**Status:** HOLD — do not publish as a theorem until the complete interval certificate passes

## Proposed result title

**A certified K36 mass-threshold crossing in one explicit finite N11
Navier-Stokes Galerkin trajectory**

## Result to state only after certification

For the explicitly specified rational, real, divergence-free initial
trigonometric polynomial obtained from the fixed 112-pair witness, evolve the
unforced periodic N11 Fourier-Galerkin Navier-Stokes ODE with viscosity
`nu=0.1`. Let the unchanged N11-derived K36 ordered source-orbit coalition
define

`F(t)=I(t)-9 O(t)`.

If the final immutable certificate verifies the currently pending endpoint
gate, the result statement will be:

> The exact initial margin is positive, the tracked complex normalizer stays
> nonzero on `[0,0.003]`, and a validated enclosure gives a strictly negative
> K36 margin at `t=0.003`. Therefore continuity implies at least one
> `t* in (0,0.003)` at which `F(t*)=0`, equivalently the K36 absolute-mass
> fraction crosses 90%.

## Already certified

The initial field and initial sign are already exact:

`F(0) in [645.8037741471, 645.8037741472]`.

This is tied to:

- witness SHA-256
  `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`;
- K36 SHA-256
  `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`;
- exact-anchor result SHA-256
  `327378d1ba2978a66484f1266d984d240fdfdaf4c5785889a48eb187c9650885`.

## Numerical motivation only

The archived float64 diagnostic gives approximately:

| time | numerical F |
|---:|---:|
| 0 | +645.804 |
| 0.001 | +730.419 |
| 0.002 | +359.047 |
| 0.003 | -48.3905 |

The endpoint converges under step refinement, but those values are not theorem
bounds.

## Fields to replace from the completed certificate

- certificate protocol/version: **PENDING**
- predictor A SHA-256: **PENDING**
- predictor B SHA-256: **PENDING**
- arithmetic library/version: **PENDING**
- interval precision: **PENDING**
- complete segment count: **PENDING**
- terminal L2 trajectory radius upper bound: **PENDING**
- global normalizer lower bound: **PENDING**
- certified endpoint F interval: **PENDING**
- certificate package SHA-256: **PENDING**
- generator SHA-256: **PENDING**
- independent verifier SHA-256: **PENDING**
- verifier result SHA-256: **PENDING**

## Required final checks

Do not remove the HOLD status until:

- all continuous segments are complete under one protocol and one pair of
  predictor hashes;
- the a posteriori error recurrence has been independently replayed;
- the global normalizer lower bound is strictly positive;
- the exact initial lower margin is strictly positive;
- the validated endpoint upper margin is strictly negative;
- the independent verifier returns PASS;
- the immutable final manifest passes
  `src/wp16_036_turnover_certificate_preflight.py`.

## Scope statement

Even after PASS, this is a theorem about **one explicit solution of one finite
N11 Fourier-Galerkin ODE**. It is not an all-N theorem, does not establish
cutoff-uniform persistence or continuum convergence, and does not prove
finite-time singularity or global regularity for the three-dimensional
Navier-Stokes PDE.
