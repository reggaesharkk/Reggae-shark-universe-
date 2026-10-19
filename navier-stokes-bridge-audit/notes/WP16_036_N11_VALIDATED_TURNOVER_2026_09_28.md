# WP16: certified finite N11 K36 crossing

28 September 2026. This document records a **post-hoc, single-datum, finite-dimensional** computer-assisted calculation. The underlying 112-pair datum was selected after exploratory N17 diagnostics. It is neither a prospective cutoff test nor a theorem about the infinite-dimensional Navier–Stokes equation.

## Precisely defined problem

On the normalized three-torus, retain the divergence-free Fourier modes with (|k|leq 11), set the mean mode to zero, and evolve the unforced Fourier–Galerkin Navier–Stokes ODE with exact decimal viscosity (
u=1/10). Interpret the finite decimals in `wp16_036_sparse_turnover_112_pairs.json` as rationals and apply the rational Leray projector to each positive representative. Negative coefficients are their conjugates. The file's SHA-256 digest is `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`.

The frozen 36 ordered source-orbit keys come from `frozen_K36_ordered_source_orbits.json`, SHA-256 `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`. Use the same anchor (P=(3,2,2)), (Q=(3,-2,1)), (K=P+Q=(6,0,3)) and the previously defined complex-normalized signed group masses. The margin is (F=I-9O), with (I) and (O) the sums of absolute imaginary signed group shares inside and outside K36. This observable is continuous whenever its complex normalizer (z) is nonzero.

## Validated trajectory method

The approximate path (v) has 120 cubic Hermite pieces, each of duration (h=1/40000). Its node and derivative arrays originate from an FFT/RK4 predictor. The first path node is the **exact projected rational witness**, and all other nodes and derivatives are interpreted as finite decimals and projected with the exact Leray multiplier. Thus the mathematically defined path is real, divergence free, continuous, and piecewise polynomial. The predictor's floating-point integration is not used as an error claim.

For each piece, outward Arb complex-ball convolution encloses the full degree-six residual polynomial
[
r=v_t+P_{11}[(vcdot
abla)v]-
uDelta v.
]

Conversion to Bernstein coefficients yields the bound (R_jgeqsup|r|_2), while the degree-three Bernstein coefficients yield (M_jgeqsupsum_k |k|,|v_k|geqsup|
abla v|_infty). These are whole-segment bounds, not sampled maxima. Each input node quartet is identified by a binary SHA-256 digest in its segment JSON.

Let (u) be the exact finite Galerkin solution and (E=|u-v|_2). The divergence-free energy identity and the Galerkin projector give
[
E'leq M_j E+R_j,
qquad
E_{j+1}leq e^{hM_j}(E_j+hR_j).
]

The exact initial error is **zero**. The recurrence is accumulated with outward Arb rounding. The endpoint observable bound accounts for every ordered source pair, the absolute-value kinks in (I,O), the perturbed complex numerator and normalizer, and the weighted factor nine. A separate interval guard keeps (|z(u(t))|>0) on all 120 pieces.

## Certified finite-dimensional theorem

**Theorem (one fixed N11 datum).** Let (u(t)) be the finite N11 Fourier–Galerkin solution from the exact rational witness above at viscosity (
u=1/10). For the frozen K36 observable (F=I-9O) defined above, its complex normalizer is nonzero throughout ([0,0.003]), and there exists at least one (t_*in(0,0.003)) such that (F(u(t_*))=0).

The certified bounds are:

| Gate | Outward bound |
| --- | ---: |
| Exact initial margin (F(u(0))) | ([645.8037741471,645.8037741472]) |
| Maximum whole-segment residual (|r|_2) | (<0.000197004885) |
| Maximum whole-segment Fourier gradient majorant | (<2331.907656) |
| Initial trajectory error | (0) exactly |
| Final trajectory error (|u(0.003)-v(0.003)|_2) | (<0.00004588841) |
| Uniform normalizer (|z(u(t))|) | (>48990.29795521) on ([0,0.003]) |
| Final margin (F(u(0.003))) | ([-54.748409847,-42.032667894]) |

All 120 whole-segment residual and gradient enclosures passed a second complete Arb replay from the preserved arrays. Each replayed upper bound was strictly below its stored outward-rounded bound; the verifier returned `PASS`. An independent exact-Fraction/Taylor recurrence gives final error (<0.000045868444), below the intentionally padded Arb radius used in the endpoint proof. The exact positive starting sign, the strictly negative ending interval, and the continuous nonzero denominator imply the crossing by the intermediate value theorem. No unique crossing time or first crossing interval is certified.

## Certificate identity

Archive:

`N11_K36_Turnover_Certificate_2026-09-28.zip`

SHA-256:

`d29224e1dd4ad9f9454951415a3b080bc9f092839e24caaeddd056013785cfbe`

The archive contains 257 entries, including the fixed inputs, predictor arrays, 120 segment enclosures, source snapshot, verifier materials, and SHA-256 manifest.

## Reproducibility

The validated implementation uses `numpy==2.3.5` and `python-flint==0.9.0`. The archived predictor arrays allow byte-identical interval replay without regenerating the floating predictor.

## Claim boundary

The theorem addresses one explicit rational initial field in one finite N11 ODE, selected post hoc. It does not bound discarded Fourier modes as the cutoff grows, establish a continuum Navier–Stokes solution, prove blowup, establish all-cutoff persistence, or address global regularity.
