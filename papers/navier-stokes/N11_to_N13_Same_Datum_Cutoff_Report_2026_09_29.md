# Same-datum crossings at finite Galerkin cutoffs N11–N13

**Prince Upadhyay — research checkpoint, 29 September 2026**

## Frozen problem

The certificate family uses the same fixed 112-pair rational initial field (SHA-256 `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`), viscosity `ν=0.1`, frozen K36 key file (SHA-256 `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`), observable `F=I−9O`, and time interval `[0,0.003]`. Between cutoffs, only the Galerkin cutoff changes; the witness is zero-padded into added modes. No observable, key, time grid, or pass threshold was retuned.

## Certified finite-cutoff results

| Gate | N11 | N12 | N13 |
| --- | ---: | ---: | ---: |
| Initial `F(0)` | positive | `[645.8037741471, 645.8037741472]` | `[645.8037741471, 645.8037741472]` |
| Certified `F(0.003)` | `[-54.748409847, -42.032667894]` | `[-73.63322101, -70.396895629]` | `[-87.154087422, -83.563901281]` |
| Terminal trajectory-error upper bound | `0.000010526681` | `0.000011374869` | `0.000012244529` |
| Whole-path normalizer lower bound | certified nonzero | `49091.85228719` | `48869.38355689` |
| Whole-segment Arb enclosures replayed | 120/120 | 120/120 | 120/120 |

The N11 archived certificate locates a zero between `t=0.0028859375` and `t=0.0028921875`. The N12 and N13 certificates establish a sign crossing somewhere in `[0,0.003]`; their reports do not claim a tighter crossing-time interval.

## N13 package and verification record

The complete N13 package is preserved in the [specialist repository](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/main/next-work/n13_same_datum). It contains the frozen protocol, runner and endpoint/normalizer source, predictor arrays, 120 saved segment enclosures, certificate, replay log, first-pass receipt, and `SHA256SUMS.txt`. The N13 run independently regenerated and accepted all 120 segment enclosures, then passed its endpoint and whole-path normalizer gates. The full distributable archive and its outer SHA-256 sidecar are in the [N13 same-datum v1 release](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/n13-same-datum-v1). Release ZIP SHA-256: `858eeec4a1cb323d23e91ffa9914af823a388a78ecc39c758abea3fcdec9ac5e`.

For N12, the post-audit certificate and replay evidence, source, and rerun instructions are preserved in the [specialist repository](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/main/next-work/n12_same_datum). N11's validated certificate and bracket are documented in the [N11 validated-turnover note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP16_036_N11_VALIDATED_TURNOVER_2026_09_28.md).

## Scope

These are results for three specified finite-dimensional Galerkin ODEs. They do not provide a cutoff-uniform high-frequency estimate, establish convergence to a continuum solution, imply blowup, or resolve global regularity for the three-dimensional Navier–Stokes equations.
