# WP19 v0.27c0 — Executed VJP point-crosscheck result

**Workflow run:** `36754853972`
**Source commit:** `0dde836d2efa97630091a3425d00504bf577eb65`
**Aggregate artifact:** `wp19-v0-27c0-arb-adjoint-vjp-point`
**Artifact id:** `11115399800`
**GitHub artifact digest:** `sha256:c7d13bfeb148437e43f53a49c6686a7dfe5567c5014dc27a3ce0e62a47fd5260`

## Numerical result

The four matrix checks passed the frozen pointwise arithmetic gate at the interior point `t=0.0015` (node 60). Each compares the carry-free Arb convolution VJP against a separate explicit Fourier sum on 12 deterministic high-signal output modes. The dealiased FFT is recorded as a floating diagnostic, not accepted as exact ground truth.

| Transition | Arb vs. explicit Fourier relative upper | Arb vs. FFT relative upper | Result |
|---|---:|---:|---|
| 14→15 | `6e-15` | `2.086308812e-6` | PASS |
| 15→16 | `6e-15` | `4.20399285e-7` | PASS |
| 16→17 | `7e-15` | `2.96920461e-7` | PASS |
| 17→18 | `7e-15` | `3.1163889e-8` | PASS |

The discrepancy between Arb and the FFT does not change the cross-check result: Arb agrees with the independently assembled explicit Fourier sums to approximately `1e-14` on the selected modes, while the FFT remains cancellation-sensitive at the adjoint amplitudes used here.

## Frozen provenance

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- C500 portable semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`

No witness, K36, sign, or C500 retuning occurred.

## Packaging correction

The workflow's numerical jobs and aggregate job reported success, but independent strict verification found the uploaded aggregate archive's `SHA256SUMS.txt` was not archive-root consistent: its entries use `final/...` although the ZIP stores those files at the root, and it includes a purported hash of the manifest itself. The manifest's actual byte SHA-256 is `e944bc9fab154c1c9dfe331a6bfb03f6db7d43261ee274c76bd8753236083725`, which differs from the self-entry `5a237744bcf9d8683bb2dbfab5cc7fdc22bd6c2262dae195b756e50a196d67a0`.

Accordingly, the correct status is **VJP point arithmetic PASS; aggregate manifest FAIL**. Do not treat the c0 ZIP as a clean immutable package. v0.27c1 repairs this by using root filenames, excluding the manifest from its own contents, and verifying every member before upload.

## Meaning and next gate

This is a one-point implementation cross-check of the finite-dimensional adjoint nonlinear operator. It does not certify an adjoint trajectory or continuous-segment residual. The c1 stage saves the full 241-node binary64 adjoint reconstruction and matching RHS data for each transition, with separate fail-closed manifests. The next mathematical gate remains an outward-rounded, continuous-time residual enclosure on every half-step, including primal-predictor and terminal-gradient uncertainty.

No all-N persistence or continuum Navier–Stokes claim follows from v0.27c0.
