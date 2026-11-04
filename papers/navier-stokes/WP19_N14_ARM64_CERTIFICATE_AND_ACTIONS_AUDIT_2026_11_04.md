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

## Previous and latest GitHub Actions runs

- [Run 41815716048](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41815716048) passed the v0.29.1 package verification on an earlier PR commit: Lean build/axiom checks, package checksums, finite arithmetic replay, and seven tests in normal, `-O`, and `-OO` modes.
- [Run 41815716233](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41815716233) passed the reverse-time correction replay and verifier but failed the final checksum command because the README digest in the correction manifest was stale.
- The stale README digest was corrected on the open PR branch. Fresh [run 41832891663](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41832891663) passed the correction workflow including the final checksum.
- The corrected [v0.29.1 verification run 41832891665](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41832891665) passed. The follow-up v0.28 correction [run 41835258480](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41835258480) and v0.29.1 verification [run 41835258517](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41835258517) also passed on the updated documentation commit.
- These CI runs verify the committed package and code paths. They do not supply the missing raw M15 trajectory or adjoint enclosures.

## Local Downloads snapshots and timeline

The October screenshots correspond to real ZIP members; the archives were inspected read-only through their roots and Navier trees.

| Snapshot | What is inside | SHA-256 |
|---|---|---|
| `Reggae-Shark-Universe-v1.1.0-Release.zip` (19 Oct; 1,039 entries) | Its Navier subtree contains 808 paths and 23 workflow YAML files, the N14 same-datum runner, and v0.28 M14 recurrence outputs. The embedded WP19 status note is dated 30 Sep. It lacks the exact M15 lower-path `nodes.npy`, `rhs.npy`, and `metadata.json` inputs. The ZIP filename says v1.1.0 while its generic internal release manifest says v3.5.0-PR155-Final; these are not reconciled release labels. | `e812078ff451f4b5a1cf554f9cc9f8134a7c60f8a2b19071b3722300d59599b5` |
| `Reggae_Shark_Universe_Umbrella_Update_2026-10-24.zip` (5 entries) | Portfolio index/README, standards, dossier PDF, and checksum manifest only; no Navier source tree. | `4a41d1bd20c1869ddc192c2a531047479e1ac8640823adbc66caeb9b9d4aa332` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26.zip` (54 entries) | Lightweight umbrella and Shark Protocol v1.3.2 mirror. The included WP19 JSON identifies an illustrative study using assumed rates and explicitly leaves all-cutoff status OPEN. | `7a962763fc2b0d1e18f7f137d9a3605f0237ce845dd4b88d63254c7e64e98150` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26_git_archive.zip` (1,169 entries) | Full umbrella Git snapshot with 846 Navier paths. It includes N14 code and v0.28 records, but no N14 result payload and none of the exact M15 lower-path inputs. | `fb19c96c32509531fb30b31b8561d0199568337027a701090021a105db87144c` |

Chronology: initial finite Fourier project/version records on 24 Sep; the N11–N18 finite-cutoff record on 29–30 Sep; M14/M15 v0.28 sign/recurrence audits on 1 Oct; Zenodo v3 on 18 Oct; the umbrella release ZIP with an older 30 Sep Navier status note on 19 Oct; dossier-only umbrella update on 24 Oct; lightweight and full Git umbrella snapshots on 26 Oct; v0.29.1 audit PR on 1 Nov; and fresh local N14 128/192-bit CPU runs plus the corrected Actions rerun on 4 Nov. These are distinct records at distinct dates, not one continuously updated artifact.

## Remaining M14/M15 gate

The M14/M15 pilot remains **STOP**. It still lacks the exact lower-path `nodes.npy`, `rhs.npy`, and `metadata.json` with their prescribed hashes, plus the matching adjoint payload. The recovered M14 VJP archive provides a binary64 path reconstruction and pointwise cross-checks, not a full trajectory, residual, or quadrature enclosure. The four Downloads scripts reviewed on 4 November also do not close this gate: the supposed 192-bit Arb helper uses Decimal at 60 digits on stored JSON; the M18+ escalation projects hard-coded values; the asymptotic script assumes its nonlinear-decay bound and samples seven cutoffs; the adversarial-cutoff file is a finite floating-point diagnostic.

Until the modewise M15 error vector, componentwise terminal-gradient mismatch, and sufficiently small localized Hessian remainder are enclosed from exact inputs, keep the pilot **STOP** and continuum regularity **OPEN**.