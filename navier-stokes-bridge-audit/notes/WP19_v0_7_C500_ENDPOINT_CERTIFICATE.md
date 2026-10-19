# WP19 v0.7 — Exact-Rational C500 Endpoint Certificate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** rigorous endpoint certificate composed from exact rational endpoint arithmetic and the existing Arb-certified trajectory/error envelopes.  
**Scope:** the already certified finite N11, N12, and N13 same-rational-datum Galerkin trajectories.  
**Not claimed:** a new N14 certificate, cutoff-uniform convergence, a continuum Navier–Stokes theorem, blowup, or global regularity.

## Result

WP19 v0.6 froze the signed C500 upper surrogate

`G_C500 = [sum_K36 |n_g| - 9 sum_C500 tau_g n_g] / |z|^2`

with `n_g = Im(w_g * conj(z))`, and proved algebraically that `F <= G_C500` whenever the tracked normalizer is nonzero.

v0.7 evaluates the saved endpoint field by the same exact-decimal solenoidal/reality projection rule used by the Arb certificate, but performs the endpoint group algebra with exact Python Fraction arithmetic.

The previously validated endpoint routine uses the global error envelope

`9 * (DeltaW / z_min + W_sum * DeltaZ / (z_min * |z0|))`.

That bound is key-independent. Its derivation uses only that every observable group coefficient has magnitude at most 9. Therefore it also bounds the perturbation of G_C500, whose coefficients have magnitudes 1, 9, or 0.

## Certified endpoint intervals

| cutoff | exact-decimal G_C500 | inherited Arb error | certified true interval |
|---:|---:|---:|---:|
| N11 | -47.8162782412826 | 6.357870977 | **[-54.174149219, -41.458407264]** |
| N12 | -55.1527982261793 | 1.61816269 | **[-56.770960917, -53.534635536]** |
| N13 | -55.7605067500938 | 1.795093071 | **[-57.555599822, -53.965413679]** |

All three upper endpoints are strictly negative. Hence the frozen C500 surrogate is itself rigorously negative on every already certified same-datum cutoff N11, N12, and N13.

Because `F <= G_C500`, this is consistent with and independently strengthens the endpoint-functional architecture of the existing finite-cutoff sign certificates.

## Endpoint construction

For each saved endpoint node:

1. positive-canonical complex coefficients are read from their finite decimal float strings;
2. the Leray projection is applied with exact rational arithmetic;
3. negative Fourier partners are defined by exact conjugation;
4. the K-channel anchor, ordered source groups, normalizer, full F, and G_C500 are evaluated exactly as rational expressions.

The script additionally checks exactly that `F <= G_C500` and that all 500 frozen C500 keys are present.

## Frozen identifiers

Witness SHA-256:

`4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`

K36 SHA-256:

`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`

C500 SHA-256:

`79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`

Predictor node SHA-256 values:

- N11: `b70bf7f7fe85a8c073c02c80e54e1f10d0642f5d030dfe569470c5970ebdda29`
- N12: `e9b35eb315ef5431c0a3a81de01485738416d1d4f0bdebfda00811c36bddf10b`
- N13: `d80274b3b5cfd1cf9f3a25dd1e8382a359c2b08821b498e9d0f6e363ef2546f1`

The exact inherited endpoint-source and endpoint-certificate hashes are recorded in `results/wp19_bridge/WP19_v0_7_PROVENANCE.json`.

## Why this matters

The endpoint functional selected for the dual-weighted bridge is no longer merely a floating diagnostic. It already survives the certified trajectory uncertainty at N11, N12, and N13 with a large negative margin.

The remaining problem is dynamic: certify how unresolved higher-cutoff dynamics can move this fixed scalar endpoint certificate before the higher-cutoff trajectory is known.

The next rigorous architecture is therefore

`validated cutoff defect -> validated adjoint weighting -> second-order remainder -> G_C500(T) < 0`.

v0.7 does not yet supply that next-cutoff prediction or any continuum implication.
