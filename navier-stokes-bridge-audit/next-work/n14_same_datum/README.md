# N14 same-datum validation

This directory contains the prospective N14 validation code for the fixed 112-pair rational turnover witness.

## Frozen inputs

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- viscosity: `0.1`
- endpoint: `0.003`
- Hermite/RK4 step: `0.000025`
- segments: `120`
- initial field: exactly the same rational N11 witness embedded into N14 with no retuning

The N13 K36 numerator sign chart was already frozen in WP19 v0.9 before the N14 predictor was generated.

## Validation job

`.github/workflows/wp19_n14_arb.yml` installs `python-flint`, regenerates the N14 predictor, computes 120 whole-segment 128-bit Arb residual/gradient enclosures, propagates the symmetric-strain trajectory radius, evaluates the endpoint K36 sign interval, and checks whole-path normalizer nonvanishing.

The workflow uploads the complete result directory as an artifact.

A floating N14 predictor and step-refinement scout already exist in WP19 v0.11, but those values are **not** a validated trajectory certificate.

No all-N or continuum Navier–Stokes claim follows from this finite N14 computation.
