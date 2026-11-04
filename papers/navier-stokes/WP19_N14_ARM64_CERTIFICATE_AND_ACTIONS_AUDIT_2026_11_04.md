# WP19 N14 finite-cutoff certificate and audit status — 4 November 2026

## Fresh same-datum N14 run

The existing same-datum N14 certificate workflow was freshly run on Windows ARM64 CPU at Arb precision 128 and 192 bits. The 192-bit pass used a copied source snapshot with higher precision; it did not modify the original source checkout or the expired Actions artifact. This is one finite Galerkin ODE result for the frozen datum.

- Protocol: cutoff `N=14`, `nu=0.1`, `T=0.003`, 120 RK4/Hermite segments of width `0.000025`, and 11,513 Fourier modes.
- Datum: the frozen rational N11 witness embedded unchanged in N14, all other modes zero. Witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`. K36 keys SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`.
- Both precisions returned `PASS`. Initial `F` interval: `[645.8037741471, 645.8037741472]`; reported true-endpoint `F` interval: `[-89.015834781, -85.160766265]`; terminal trajectory-error upper bound: `0.000012825905`; whole-path normalizer lower bound: `48850.68586052`.
- The endpoint record states `certified_negative_if_E_valid: true`; the endpoint margin is conditional on validity of the supplied Galerkin L2 error radius. This is not a fresh reproduction of every archived N11–N18 enclosure, and it is not a continuum regularity result.
- The 192-bit exact-decimal Arb endpoint lower ball is `[-87.0883005229810938276854765616754135198801457016266337349 +/- 1.74e-56]`; the whole-path `z_abs` lower ball is `[51090.2936694763477704213170935998933387343615847466155308 +/- 2.91e-53]`.

Sealed local review packages:

| Precision | File | Bytes | SHA-256 |
|---|---|---:|---|
| 128-bit | `WP19_N14_ARM64_CERTIFICATE_128BIT_20261104.zip` | 128,288,656 | `32e558d1a077790c16491847c546badc98f0eae107df6ae6dd5f4027476fd392` |
| 192-bit | `WP19_N14_ARM64_CERTIFICATE_192BIT_20261104.zip` | 128,288,661 | `d951f6a95b2e5457fa01fe824506eb40b82a350469092d8211aae15820e259c1` |

Both archives contain 356 SHA-256-listed files (357 ZIP entries including the manifest); every listed digest matched, ZIP CRC checks passed, and each external `.sha256.txt` sidecar matched its archive. The packages remain operator-local; the hashes are recorded here for review. Windows and historical Linux binary64 trajectory arrays have different hashes, so bytewise cross-platform identity is not claimed.

The Windows runs used Python 3.12.10 ARM64, NumPy 2.3.5, and python-flint 0.9.0. They ran on the CPU. Although the operator's device is a Snapdragon X Copilot+ PC, the NPU was not used by this Python/Arb workflow.

## Previous GitHub Actions runs

- [Run 41815716048](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41815716048) passed on the open specialist PR #167. The Lean build and axiom checks, package checksums, finite arithmetic replay, and seven-test suite in normal, `-O`, and `-OO` modes passed.
- [Run 41815716233](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41815716233) recomputed the reverse-time correction, passed its separate recurrence replay and verifier, then failed the final checksum command because the `README.md` digest in the v0.28 correction manifest was stale. All other listed files passed. The manifest entry is being corrected on PR #167; a new run is needed to confirm that repair.
- Neither run supplied the missing raw M15 trajectory or adjoint enclosures. CI verifies the committed package and code paths only.

## Tags and current release

The latest published specialist Navier tag/release remains `n13-same-datum-v1` from 29 September 2026; the other specialist tags are `v0.1` and `v0.2`. The umbrella repository has only `lrsc-v1.2.1-supplement`, which is unrelated to Navier. Tags are fixed commit labels and do not move as PRs change. PR #167 and mirror PR #55 are open and unmerged, so no new Navier release tag is created from them. After review and merge, a new, scoped finite-cutoff audit tag can be considered; it must not claim a continuum theorem.

## Remaining M14/M15 gate

The M14/M15 pilot remains **STOP**. It still lacks the exact lower-path `nodes.npy`, `rhs.npy`, and `metadata.json` with their prescribed hashes, plus the matching adjoint payload. The recovered M14 VJP archive provides a binary64 path reconstruction and pointwise cross-checks, not a full trajectory, residual, or quadrature enclosure. The four Downloads scripts reviewed on 4 November also do not close this gate: the supposed 192-bit Arb helper uses Decimal at 60 digits on stored JSON; the M18+ escalation projects hard-coded values; the asymptotic script assumes its nonlinear-decay bound and samples seven cutoffs; the adversarial-cutoff file is a finite floating-point diagnostic.

Until the modewise M15 error vector, componentwise terminal-gradient mismatch, and sufficiently small localized Hessian remainder are enclosed from exact inputs, keep the pilot **STOP** and continuum regularity **OPEN**.