# WP19 v0.28 — structured primal-uncertainty A/B result

**Status:** one-segment finite diagnostic; no transfer theorem.

## Frozen test

The comparison reused M14 segment 237, the same adjoint path, and the same
primal L2 radius. It did not change the witness, K36, C500 polynomial, signs,
predictor, or time interval. The tested continuous interval was
`[237/80000, 238/80000]`, at 192-bit Arb precision.

Frozen identifiers:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`
- segment 237 SHA-256: `c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc`
- M14 adjoint value-array SHA-256: `00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab`
- M14 adjoint RHS-array SHA-256: `8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c`

## Bound and recurrence comparison

The old componentwise/triangle residual-uncertainty penalty was
`724,168,354,547.568286`. A Fourier L2 Young bound, evaluated on all four
Bernstein controls of the same adjoint Hermite segment, gave
`242,491,337,769.886902`. The outward ratio is
`0.334854921854`, below the prospectively frozen `0.5` gate (at least a 2x
reduction). The penalty fell by about 66.5%.

The smaller residual term barely changes the one-step propagated adjoint
error because exponential amplification of the incoming error remains the
dominant term:

- archived old outgoing upper: `78,258,186,399.829279...`
- conservatively recomputed old upper: `78,258,186,399.831235707571984...`
- structured-bound outgoing upper: `78,252,099,012.758983559287748...`
- reduction from the recomputed old upper: about `6.09 million`, or `0.00778%`.

The explicit small-system Fourier-convolution cross-check and the independent
outward-Decimal recurrence verifier both passed. The direct-convolution check
tests the bilinear identity and Young bound on a deterministic M2 case; it is
not a second computation of the full M14 segment residual.

## Decision

This passes the predeclared **bound-tightening** gate, so the L2 Young formula
is materially sharper than the previous uncertainty estimate on this one
segment. It does not fix the scalar recurrence's conditioning: the total
one-step error changes by less than 0.01%. Do not infer that the remaining 237
segments or the signed observable are now controlled. The next proof gate
should target the logarithmic-norm/exponential-amplification estimate or a
goal-directed propagation that avoids collapsing all perturbations into one
scalar norm, before spending compute on a long segment batch.

## Reproduction and archive

- Workflow run: [36826572808](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/36826572808)
- Commit: `b6f301db70e13a9a92480e514cee8898d1c03df8`
- Artifact: `wp19-v0-28-structured-uncertainty-ab-M14-step237`
- Artifact SHA-256: `69e18706e6ec4b82a65fbfaeb85b18bf7da9b618183e848af26f686619b4ca60`
- Result JSON SHA-256: `b67857abf2392d963985714415e3def7d0fb4f536235765058b6a118a73bba4a`

The complete small result package, scripts, input certificates, and checksum
manifest are stored beside this note under
`results/wp19_v0_28/structured_uncertainty_ab_20261001/`.

This remains one finite M14 segment diagnostic. It does not certify the full
adjoint path, dual quadrature, normalizer, signed-observable transfer, any
other cutoff, or continuum Navier–Stokes regularity or blowup.
