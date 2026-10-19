# WP19 v0.27c1 — executed adjoint-path export result

**Status:** PASS for the finite path-export and arithmetic cross-check gate only. This is not an adjoint trajectory certificate and does not establish cutoff transfer.

## Run and immutable outputs

- Repository: `reggaesharkk/navier-stokes-bridge-audit`
- Workflow run: [36763902966](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/36763902966)
- Source/workflow commit used by the run: `dc950e942bfc892ef11078d6bd08bb51084d23b4`
- Aggregate artifact: `wp19-v0-27c1-adjoint-path-export`, artifact ID `11120698789`
- Aggregate artifact SHA-256: `ef3ff8cca997b783b8a065072cce1d2793e9940d2f7db89076afffcc2298a13b`
- Aggregate size: 1,681,947,069 bytes; retained by GitHub Actions through 2026-10-30.
- Aggregate job completed successfully after downloading all four shards, verifying each self-excluding manifest, checking exact file coverage and per-file SHA-256 values, loading both NumPy arrays per transition, checking their shapes and internal hashes, then writing and verifying the archive manifest.

The four transition shards were `14→15`, `15→16`, `16→17`, and `17→18`. Every shard reports `PASS ARB VJP CROSSCHECK AND ADJOINT PATH EXPORT`, exports 241 binary64 adjoint nodes and 241 RHS samples, and passes the 12-mode Arb-versus-explicit-Fourier threshold of (10^{-12}).

| Transition | Arb vs explicit Fourier relative upper | Arb vs FFT relative diagnostic | Adjoint values SHA-256 | Adjoint RHS SHA-256 |
|---|---:|---:|---|---|
| 14→15 | (6\times10^{-15}) | (2.086308812\times10^{-6}) | `00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab` | `8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c` |
| 15→16 | (6\times10^{-15}) | (4.20399285\times10^{-7}) | `0c0e6c5280663728e089ac427d33b2141276265f3aef8365e55b6a0561b458af` | `3d8da365aef3bcb95826faaa328c42c174362bda724f979e8b426ce4c2c1510a` |
| 16→17 | (7\times10^{-15}) | (2.96920461\times10^{-7}) | `d4f105b690c28424f0431b0e8f39cc740643233ae55d03f18c50b38380ea950f` | `42e1291017850336b4552529c50222efa8db7deb36132f5206e1fd418fe348f7` |
| 17→18 | (7\times10^{-15}) | (3.1163889\times10^{-8}) | `798b1d4930d15f658d687af31991b862f271a46e964a8240d88e888e5de1a37f` | `7b38e7607e222f3191c44375d56a70fea5aef955cea0f654a19546b218204b1e` |

The FFT discrepancy is retained as a floating diagnostic; the pass threshold uses the Arb convolution compared against an independent explicit Fourier sum on deterministic high-signal modes.

## Frozen provenance

- Rational witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- C500 portable semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`
- (\nu=0.1), (T=0.003), 240 half-steps of (1.25\times10^{-5}) per transition.

## Claim boundary and next gate

These outputs are reproducible binary64 centers with nodewise VJP arithmetic cross-checks. They do **not** enclose the continuous adjoint path, its Hermite residual, primal predictor uncertainty, terminal-gradient uncertainty, or any signed C500 transfer correction. They do not change the v0.25b finite endpoint family and imply no all-(N), continuum, regularity, or blowup theorem.

The next gate is to import saved binary64 values as exact rationals (or enclosing intervals), enclose the continuous Hermite residual on every segment with outward-rounded arithmetic, and propagate the adjoint error using a verified (L^2) logarithmic-norm bound. Dual quadrature, nonlinear cutoff-transfer remainder, endpoint enclosure, independent verification, and normalizer positivity remain separate required gates.

The earlier v0.27c0 shard manifest packaging defect is not silently treated as passing. This c1 run uses archive-root filenames and self-excluding manifests; the aggregate step independently re-reads and verifies every shard and array.
