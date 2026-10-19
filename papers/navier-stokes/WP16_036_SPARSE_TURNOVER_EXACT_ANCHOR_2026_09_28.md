# WP16 sparse turnover: exact rational initial anchor (28 September 2026)

This is an additive step after the [post-hoc 112-pair reduction](WP16_036_SPARSE_TURNOVER_REDUCTION_2026_09_28.md). It certifies an **instantaneous finite-Galerkin algebraic statement only**. The negative later-time value in the numerical experiment remains unvalidated.

Read each finite decimal entry of the fixed 112-pair coefficient table as an *exact rational number*. For every positive mode `k`, apply the rational Leray projection `a_k -> a_k - k(k·a_k)/|k|²`; then set `a_-k = conjugate(a_k)`. This defines a precisely specified, real, zero-mean, divergence-free trigonometric polynomial on the 3-torus. The largest component change from the decimal table is exactly `5e-15`. The exact checker verifies `k·a_k=0` as a rational identity for every listed mode.

With the **unchanged original K36 orbit-key file**, compute the tracked complex normalizer `z`, ordered convolution contributions `w_j`, and `g_j=Im(w_j/z)` using Python arbitrary-precision rational fractions. Summing `I=sum_{j in K36}|g_j|` and `O=sum_{j outside K36}|g_j|` gives the following *outward decimal enclosures of exact rational numbers*:

| Quantity | Exact rational lies in |
| --- | --- |
| `I` | `[947.7106558002, 947.7106558003]` |
| `O` | `[33.5452090725, 33.5452090726]` |
| `F(0)=I-9O` | `[645.8037741471, 645.8037741472]` |

Thus **`F(0)>0` is exact for this rationally projected finite field**. The output is [`wp16_036_sparse_turnover_exact_anchor.json`](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/results/wp16_n17_holdout/wp16_036_sparse_turnover_exact_anchor.json); the checker is [`wp16_036_sparse_turnover_exact_anchor.py`](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp16_036_sparse_turnover_exact_anchor.py). The fixed coefficient input SHA-256 is `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`; the K36 key SHA-256 is `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`. The exact result SHA-256 is `327378d1ba2978a66484f1266d984d240fdfdaf4c5785889a48eb187c9650885`.

```bash
PYTHONPATH=src python src/wp16_036_sparse_turnover_exact_anchor.py \
  --witness results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json \
  --keys results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json \
  --result results/wp16_n17_holdout/wp16_036_sparse_turnover_exact_anchor.json
```

Running the same N11 FFT/RK4 diagnostic after converting these *projected rational coefficients* back to float produces `F(.003)=-48.3904829635909` with `dt=.0001`. This is a numerical observation on the precisely specified starting field, **not** a certified value at `.003`. The exact computation uses no floating-point operations for the initial `F(0)` sign; the decimal intervals are obtained by integer floor and ceiling of the rational values.

The next proof gate is validated propagation of the 112-pair rational initial field under the *full N11 Galerkin ODE*, allowing other N11 modes to populate. An interval enclosure must keep `z` away from zero and bound the absolute-valued grouped contributions at `.003` strictly below the mass threshold. Only then does continuity certify a finite-Galerkin crossing. No such enclosure exists here, and even that result would require a separate uniform tail estimate for any continuum claim.
