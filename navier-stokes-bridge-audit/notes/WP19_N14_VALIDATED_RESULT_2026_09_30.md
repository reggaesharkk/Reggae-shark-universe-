# WP19 — N14 same-datum Arb validation result

**Date:** 30 September 2026  
**Status:** PASS  
**Scope:** one fixed finite N14 Fourier–Galerkin trajectory; no continuum claim.

The GitHub Actions workflow `.github/workflows/wp19_n14_arb.yml` completed successfully on run `36608785015`.

Frozen inputs:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- `nu = 0.1`
- `T = 0.003`
- `h = 0.000025`
- 120 whole-segment 128-bit Arb enclosures
- same rational N11 witness embedded unchanged into N14; no retuning

Validated outputs:

- result: `PASS`
- terminal trajectory-error upper bound: `0.000012825905`
- exact initial F interval: `[645.8037741471, 645.8037741472]`
- endpoint F interval: `[-89.015834781, -85.160766265]`
- whole-path normalizer lower bound: `48850.68586052`

The workflow artifact `wp19-n14-arb-certificate` contains 126 files and has artifact ZIP SHA-256

`b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`.

Artifact ID: `11059294923`.

This extends the rigorous same-datum finite-cutoff chain to N11, N12, N13, N14. It does not establish cutoff-uniform persistence, a continuum singularity, or global regularity.
