# WP19 — Validated N14 Same-Datum Result

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** completed finite-Galerkin computer-assisted certificate.

## Frozen problem

- cutoff: N=14
- viscosity: nu=0.1
- endpoint: T=0.003
- Hermite/RK4 step: 0.000025
- segments: 120
- initial datum: same fixed 112-pair rational witness used at N11-N13, embedded unchanged with no retuning
- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`

The N13 K36 numerator sign chart had already been frozen before the N14 predictor was generated.

## GitHub Actions validation

Workflow run: `36608785015`

The clean GitHub Actions runner installed Python 3.12, NumPy 2.3.5, and python-flint 0.9.0; regenerated the N14 predictor; computed all 120 whole-segment 128-bit Arb enclosures; propagated the validated trajectory radius; evaluated the endpoint margin; and checked whole-path normalizer nonvanishing.

Every workflow step completed successfully.

## Certified result

- result: PASS
- terminal L2 trajectory-error upper bound: `0.000012825905`
- F(0) in `[645.8037741471, 645.8037741472]`
- F(0.003) in `[-89.015834781, -85.160766265]`
- whole-path normalizer lower bound: `48850.68586052`

Therefore the same fixed rational datum has a certified positive-to-negative K36 crossing at finite cutoff N14.

Together with the earlier certificates, the rigorous same-datum finite-Galerkin chain is:

```
N = 11, 12, 13, 14.
```

## Artifact provenance

- GitHub Actions artifact: `wp19-n14-arb-certificate`
- artifact ID: `11059294923`
- artifact size: `127530612` bytes
- uploaded artifact ZIP SHA-256: `b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`
- files in artifact: 126

The artifact contains the predictor arrays, all 120 segment JSON records, aggregate/certificate outputs, and SHA manifest.

## Scope

This is a theorem about one explicit finite N14 Fourier-Galerkin ODE trajectory.

It strengthens the same-datum finite-cutoff chain, but it does not establish all-cutoff persistence, continuum convergence, finite-time singularity, global regularity, or a solution of the three-dimensional Navier-Stokes Millennium problem.
