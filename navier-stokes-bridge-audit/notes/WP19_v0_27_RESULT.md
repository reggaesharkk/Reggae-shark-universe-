# WP19 v0.27 — Terminal Signed-C500 Gradient Arb Result

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** **PASS TERMINAL-GRADIENT INTERVALIZATION**  
**Workflow run:** `36756532625`  
**Aggregate artifact digest:** `sha256:a523e85336fa9a24393d4ad58e527b8a592d986bb7cf0627fa86f87072db7e51`

## Result

The first genuinely intervalized component of the v0.26 signed-C500
goal-adjoint chain has passed.

For each same-datum transition `14->15`, `15->16`, `16->17`,
and `17->18`, v0.27 evaluated the fixed degree-7 signed-C500 polynomial
and its analytic terminal gradient using 128-bit Arb/acb arithmetic at the
canonical decimal (P_{11}) predictor endpoint.

All four jobs returned:

`PASS 128-BIT ARB TERMINAL-GRADIENT CERTIFICATE`.

| transition | Arb linear interval | Arb width / |floating prediction| | gradient L2 upper |
|---|---:|---:|---:|
| 14->15 | [5757388589.282617, 5757388589.282621] | 3e-18 | 4691959667101.255187 |
| 15->16 | [1022749302.136833, 1022749302.136838] | 3e-18 | 4693885687244.997204 |
| 16->17 | [259166849.114831, 259166849.114835] | 3e-18 | 4695147409827.675138 |
| 17->18 | [-72146755.960730, -72146755.960725] | 3e-18 | 4695324835717.131266 |

Maximum centered finite-difference relative error of the independent
complex128 analytic-gradient cross-check:

`1.1176688676425961e-07`.

The N14 analytic reverse-mode formula was also independently compared against
the existing PyTorch reverse-mode implementation before intervalization, with
relative L2 discrepancy approximately `1.15e-15`.

## Meaning

The terminal condition of the signed-C500 adjoint is no longer merely a
floating reverse-mode object. Its polynomial value and terminal gradient at
the frozen predictor endpoint now have a reproducible 128-bit interval
certificate.

This removes one of the explicit open items listed after v0.26.

## Next live gate

The next target is v0.28:

**an Arb a-posteriori residual/enclosure certificate for backward adjoint
propagation around the saved floating half-step adjoint reconstruction,
followed by rigorous dual quadrature.**

The normalizer remains a separate certified guard.

## Provenance

Frozen inputs remain unchanged:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`

The aggregate SHA manifest now deliberately excludes `SHA256SUMS.txt`
itself, correcting the self-hash packaging defect found during the independent
v0.25b verifier audit.

## Claim boundary

v0.27 certifies the terminal polynomial value/gradient only. It does not yet
certify backward adjoint propagation, dual quadrature, the nonlinear dynamic
remainder, the endpoint Taylor remainder, an all-N persistence theorem, or
continuum Navier–Stokes regularity/blowup.
