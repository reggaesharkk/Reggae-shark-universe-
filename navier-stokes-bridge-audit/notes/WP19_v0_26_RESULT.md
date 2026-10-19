# WP19 v0.26 — Signed-C500 Numerator Goal-Adjoint Result

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** PASS PRE-INTERVAL SIGNED-NUMERATOR DESIGN GATE  
**Workflow run:** `36731923445`  
**Aggregate artifact SHA-256:** `b4a81b7a7fb392b48a36e99c35df6fb29c5d548a32f49afa3563c43ac1eba824`

## Result

The fixed signed-C500 numerator objective passed the pre-interval goal-oriented transfer gate on every sampled same-datum transition `N=14→15→16→17→18`, with no retuning of the witness, K36 keys, prospective K36 sign chart, or C500 coalition.

The floating endpoint polynomial agrees with the v0.25b exact-rational nominal numerator to a maximum relative discrepancy of `6.399219704558418e-15`. All 36 prospective K36 endpoint signs match the frozen chart at every endpoint.

| transition | actual ΔJ | adjoint prediction | |remainder| / rigorous base margin | nonlinear radius scout / margin | total scout budget / margin |
|---|---:|---:|---:|---:|---:|
| 14->15 | 5758688465.62 | 5758574520.36 | 8.39352e-07 | 0.0507755 | 0.0932043 |
| 15->16 | 1022846836.07 | 1023730304.83 | 6.79943e-06 | 0.0265857 | 0.0344654 |
| 16->17 | 259180420.749 | 259457491.295 | 2.15007e-06 | 0.0129307 | 0.0149442 |
| 17->18 | -72147169.7784 | -72095279.2217 | 4.03594e-07 | 0.00388801 | 0.00444875 |

The largest observed total adjoint remainder is `6.79943091515744e-06` of the rigorous negative numerator margin. The largest conservative scout budget is `0.09320427500431665` of that margin, attained on `14→15`. The final `17→18` transition reverses sign and the adjoint reproduces that reversal.

## Decision

`proceed_to_intervalization = true`.

The next target is exactly:

**interval terminal polynomial gradient + interval backward adjoint + rigorous dual quadrature + rigorous endpoint/nonlinear remainder, with the normalizer handled separately.**

## Provenance correction retained

During this run the historical v0.9 note's recorded sign-chart digest was audited. The tracked prospective N13 sign-chart file has git blob `f06df05437fd717337b5bf11939e997f2a7d165e`, is byte-identical to the file first committed in `5c0b34f4a887db62c2dc8d9f8558e98d38a4e0bd`, and its actual file SHA-256 is:

`de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`

The older recorded `7cbb307c...` digest was therefore a provenance-record error, not a change to any K36 key or sign.

## Claim boundary

This stage is a floating pre-interval design result. The N11–N18 v0.25b endpoint certificates remain the rigorous finite results. v0.26 does not establish an all-N persistence theorem or any continuum Navier–Stokes regularity/blowup conclusion.