# Frozen N13 same-datum cutoff test

**State:** protocol frozen before generating the N13 predictor.  
**Question:** Does the exact rational N11 witness retain the certified K36 margin crossing under the N13 Galerkin dynamics when embedded by zero-padding?

## Immutable inputs and dynamics

- Exact projected rational witness: SHA-256 `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`.
- Frozen ordered K36 source-orbit key file: SHA-256 `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`.
- Cutoff: `N=13`; every mode absent from the N11 witness is initialized to exact zero.
- Viscosity: `nu=1/10` exactly.
- Time interval: `[0, 0.003]`.
- Hermite grid: 120 segments, `h=1/40000`.
- Observable: unchanged `F=I-9O`, anchors `(3,2,2)`, `(3,-2,1)`, output `K=(6,0,3)`, and the same frozen ordered K36 keys as the N11/N12 certificates.

No phase optimization, witness change, key reranking, endpoint change, viscosity change, grid change, or threshold change is allowed after the N13 predictor is generated.

## Frozen pass criteria

The N13 test passes only if every item below holds:

1. The predictor is tied to the exact zero-padded witness; all node/RHS arrays are SHA-256 recorded.
2. Each of the 120 whole-segment residual enclosures is independently regenerated with Arb from the archived Hermite data and accepted against its saved outward-rounded bound.
3. The finite Galerkin trajectory error is rigorously bounded from exact zero initial error using the residual and symmetric-strain Gronwall coefficient. For divergence-free Fourier coefficients, `||sym(i k tensor v_k)||_F = |k| ||v_k||_2 / sqrt(2)`.
4. The K36 normalizer has a strictly positive Arb lower bound on all 120 segments using the certified uniform trajectory-error radius.
5. The exact initial sign is positive and the Arb endpoint upper bound at `T=0.003` is strictly negative.

A failed gate is recorded as a failure; no input, grid, observable, or criterion may be altered and rerun for a pass. A pass adds evidence at one more finite Galerkin cutoff for this same datum. It does not prove cutoff-uniform persistence, a continuum limit, blowup, or global regularity.
