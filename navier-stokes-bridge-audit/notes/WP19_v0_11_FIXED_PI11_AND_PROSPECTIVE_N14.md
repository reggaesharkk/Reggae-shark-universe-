# WP19 v0.11 — Fixed-Pi11 Locality and Prospective N14 Transfer Scout

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact endpoint-support theorem plus prospective floating N14 diagnostics.  
**Not claimed:** a validated N14 Galerkin trajectory, an interval dual-weighted bridge, cutoff-uniform convergence, or a continuum Navier–Stokes theorem.

## 1. Exact fixed-Pi11 support theorem

For the frozen endpoint architecture:

- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- C500 SHA-256: `79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`
- K36 keys: 36
- C500 keys: 500
- maximum selected orbit squared norm: 121
- maximum selected orbit norm: 11
- maximum coordinate magnitude in any selected orbit: 10

The norm-11 orbit types are `(2,6,9)` and `(6,6,7)`. The anchor modes
`P=(3,2,2)`, `Q=(3,-2,1)`, and `K=(6,0,3)` also lie inside N11.

Therefore every Fourier coefficient entering the frozen C500 endpoint numerator and normalizer is already present in the N11 Galerkin state.

For any Fourier state `a` at cutoff `M >= 11`,

[
H_{C500}(a)=H_{C500}(\Pi_{11}a),
]

and, whenever the tracked normalizer is nonzero,

[
G_{C500}(a)=G_{C500}(\Pi_{11}a).
]

This is an exact algebraic locality statement, not a numerical trend. It sharpens the earlier fixed-support count in v0.6: the endpoint objective itself can be evaluated entirely on the fixed N11 projection for every later cutoff.

## 2. Prospective same-datum N14 predictor

The N13 K36 numerator sign chart was frozen in v0.9 before this N14 predictor was generated.

The N14 predictor uses the same unchanged 112-pair rational witness with no retuning:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- `nu = 0.1`
- `T = 0.003`
- `h = 0.000025`
- 120 RK4 steps
- 11,513 N14 modes

Predictor hashes:

- `nodes.npy`: `e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0`
- `rhs.npy`: `f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253`

These arrays are predictor data only. They are not an Arb-certified N14 trajectory.

## 3. N14 endpoint diagnostics

Exact rational endpoint algebra was applied to the precisely defined decimal predictor endpoint after the same solenoidal/reality projection convention used by the existing endpoint certificates.

Coarse predictor:

- `F_14(T) ~= -87.088300522981`
- `G_C500(T) ~= -52.8414629120453`

Independent half-step predictor, with `h=0.0000125`:

- `F_14(T) ~= -87.088300789981`
- `G_C500(T) ~= -52.8414630837451`

The coarse/half-step endpoint state difference is approximately

[
6.11631981594\times10^{-9}.
]

This is a numerical refinement diagnostic, not an interval error bound.

The prospectively frozen N13 numerator-sign chart matches the N14 predictor endpoint:

- coarse N14: 36/36
- half-step N14: 36/36
- observed sign changes: 0

The full N14 state and its N11 projection give the same floating C500 value to machine precision. That equality is predicted by the exact fixed-Pi11 support theorem above.

## 4. Fixed-Pi11 transfer diagnostics

Using one N11 endpoint objective and projecting later saved/predictor trajectories all the way to N11 gives:

| target cutoff | G_C500(Pi11 u_M(T)) | Delta G from N11 |
|---:|---:|---:|
| N12 | -55.152798226 | -7.336519985 |
| N13 | -55.760506750 | -7.944228509 |
| N14 | -52.841462912 | -5.025184671 |

The N14 value is less negative than N13. Therefore the N11->N13 decrease must not be extrapolated as a monotone cutoff trend.

## 5. Prospective N13->N14 dual-weighted scout

The N13 sign chart used here was frozen before N14 generation. The N14 nominal endpoint remains in the same observed K36 sign chamber.

For the frozen signed C500 numerator:

- base N13 `G_C500 = -55.760506750094`
- target N14 `G_C500 = -52.841462912045`
- actual `Delta G = +2.919043838049`
- actual signed-numerator change: `+7737987742.583984`
- dual-weighted first-order sum: `+7741527672.657514`
- linearization remainder: `-3539930.073529`
- absolute remainder / actual signed-numerator change: `0.04575%`
- sum of absolute step contributions: `7741527672.657514`
- positive steps: 120
- negative steps: 0
- observed K36 sign flips: 0
- quadratic kink correction: `5118480.742228`

All 120 observed first-order step contributions are positive. Thus the N13->N14 increase does not rely on cancellation in this floating scout.

These are non-rigorous diagnostics of the saved predictor paths.

## 6. Rigorization budget

v0.10 certified the N13 signed C500 numerator upper bound at approximately

[
-1.435881433635466\times 10^{11}.
]

For design purposes only, charging this certified base bound by the observed N13->N14 absolute first-order sum, the absolute observed remainder, and the observed quadratic correction still leaves approximately

[
1.3583795728\times 10^{11}
]

of negative numerator margin.

This is not a certificate because the added dynamic terms have not been interval-enclosed. It is a quantitative tolerance budget for a future validated dual-weighted calculation.

## 7. Current validation blocker

The next direct validation step is the N14 whole-segment Arb trajectory certificate, using the same 120-segment Hermite architecture as N11-N13.

The present execution runtime does not provide the `python-flint` / `flint` module required by the existing Arb segment implementation. No substitute floating computation is being labeled as a certificate.

## 8. Claim boundary

The new exact result in v0.11 is the fixed-support identity

[
G_{C500}(a)=G_{C500}(\Pi_{11}a),\qquad M\ge 11,
]

with the analogous identity for its signed numerator.

The N14 trajectory, endpoint values, step-refinement comparison, and dual-weighted transfer remain predictor/scouting results until the whole-segment validated enclosure is completed.

No all-N or continuum conclusion follows.
