# WP19 v0.27c1 — Saved backward-adjoint reconstruction

**Purpose:** preserve the full numerical backward-adjoint reconstruction needed by the next continuous-segment residual experiment.

## Frozen scope

This stage reuses the v0.27c0 arithmetic gate and its exact transition matrix `14→15`, `15→16`, `16→17`, `17→18`. It does not change the witness, K36 keys or signs, C500 semantic object, viscosity, predictor data, or terminal observable.

The frozen input identities are:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- C500 portable semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`

## Reconstruction and outputs

For each transition, the runner recomputes the existing backward RK4 adjoint over 240 half-steps on `[0, 0.003]`, with half-step `1.25e-5`. It stores:

- `M*_adjoint_values.npy`: the 241 binary64 coefficient-vector centers;
- `M*_adjoint_rhs.npy`: the corresponding 241 evaluations of the continuous adjoint RHS, used as Hermite data;
- `M*_arb_vjp_point.json`: the prior one-interior-point Arb-vs-explicit-Fourier VJP cross-check plus hashes and dimensions of the saved path.

The runner and workflow verify finite values, array dimensions, each array's SHA-256, and the complete shard and aggregate manifests. Manifests exclude themselves and use archive-root filenames, so the recorded names match the uploaded ZIP members.

## Claim boundary

A PASS at this stage means only that (1) the VJP kernel passes the prior pointwise arithmetic cross-check and (2) all 241-node binary64 path values/RHS evaluations were saved and manifest-verified. The arrays are **centers**, not enclosures. This stage does not establish a continuous adjoint trajectory bound, a segment residual bound, dual quadrature, a corrected endpoint value, or an all-cutoff/continuum Navier–Stokes result.

The next gate must use outward-rounded arithmetic to enclose the continuous Hermite residual on every half-step interval, account for certified primal predictor uncertainty and terminal-gradient uncertainty, and propagate the resulting adjoint error with a fail-closed bound before any signed C500 transfer claim is promoted.
