# Navier–Stokes evidence timeline and current status

**As of:** 4 November 2026  
**Method:** Reconciles dated records, local archive manifests, GitHub Actions, and fresh finite N14 Arb runs on Windows ARM64 CPU at 128 and 192 bits. The N14 certificate is conditional on its supplied Galerkin trajectory-error radius and is not a continuum result.

This chronology distinguishes archived claims from file/hash review and recorded execution. A matching manifest establishes byte agreement with that manifest; it does not, by itself, reproduce a numerical result.

## Current status

**The continuum regularity question remains open.** These materials do not prove global regularity, blowup, or a cutoff-uniform limit for three-dimensional incompressible Navier–Stokes.

- **N11–N18:** The Sep 29–30 records report a same-datum Arb certificate family. The Nov 1 v0.29.1 bundle checks supplied finite records and arithmetic; raw upstream Arb trajectories and inputs needed to regenerate those enclosures are absent. This replay is not a fresh Arb reproduction.
- **N14 same datum, 4 Nov:** Fresh 128- and 192-bit Arb runs both returned PASS for one frozen rational datum at finite cutoff N14 (120 whole-segment enclosures; h=0.000025; T=0.003). The reported true-endpoint F interval is [-89.015834781, -85.160766265], conditional on the supplied trajectory-error radius. Sealed local ZIP hashes and full verification are recorded in [the audit note](WP19_N14_ARM64_CERTIFICATE_AND_ACTIONS_AUDIT_2026_11_04.md). This does not reproduce every archived N11–N18 certificate or establish continuum regularity.
- **WP19 M14/M15:** The v0.29.1 M14 recurrence replays three backward scalar steps (239, 238, 237), conditional on imported strain and residual bounds; it is not a full adjoint-path enclosure. The reported M15 conservative remainder is about 1.6406e14 versus a signed lower bound of about 5.7586e9, leaving a negative margin. The reported steps 220–239 reduction is not independently reproduced in the bundle. The pilot remains **STOP**.
- **Earlier M14 VJP archive:** The Downloads archive shown in Explorer contains M14_adjoint_rhs.npy, M14_adjoint_values.npy, M14_arb_vjp_point.json, and SHA256SUMS. The reviewed ZIP CRC and three manifest entries matched. Its metadata describes a binary64 saved reconstruction with one-point 192-bit Arb-versus-FFT VJP checks, including selected-mode checks; it does not supply a full adjoint trajectory, residual, or quadrature enclosure. The numerical checks were not recomputed in this review.
- **192-bit Arb producer:** The local extracted tree contains wp19_v0_29_adjoint_segment_arb_v3.py, which imports python-flint Arb/Acb and sets 192-bit precision. It is written for one finite M-to-M+1 transition half-step using supplied arrays. Those arrays and run outputs are absent from the tree; this review did not run it.
- **Downloads helper:** wp19_modewise_arb_bridge.py uses Python Decimal at 60-digit precision to read existing JSON segments. It does not call Arb or recreate the 192-bit calculation, so it is not new Arb evidence.
- **Nov 1 closure ZIP:** Its 27-entry SHA-256 manifest matched on inspection. Stored outputs report N14→N15 endpoint separation, while N15→N16, N16→N17, and N17→N18 intervals are not separated. The modewise-vector item is a validator self-test, not a supplied full M15 error vector. The manifest does not independently recompute these results.
- **Local folder in the screenshot:** ns_arb_verified_work/navier-stokes-bridge-audit is an extracted snapshot with no Git metadata. Its 44-entry root hash manifest matched 39 entries; five differed: .gitignore, CITATION.cff, LICENSE.md, README.md, and RELEASE_NOTES.md. Its patch ZIP contains older synthetic 2D versions of several verifier/runner files, so those files are not promoted to the active source branch.
- **GitHub Actions:** The corrected reverse-time sign-correction workflow [run 41832891663](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41832891663) and the v0.29.1 verification [run 41832891665](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41832891665) both passed after the README digest correction. Follow-up runs on the updated documentation commit [41835258480](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41835258480) and [41835258517](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41835258517) also passed. PR #167 remains open and unmerged.

## Dated record

| Date | Record or activity | Current reading |
|---|---|---|
| 24 Sep 2026 | First project record, Zenodo v0.2, [DOI 10.5281/zenodo.22940790](https://doi.org/10.5281/zenodo.22940790). | Initial finite Fourier diagnostics; exploratory scope. |
| 28 Sep 2026 | N11 finite-Galerkin crossing note; N17 mechanism-failure record. | Preserve both; neither establishes a continuum theorem. |
| 29 Sep 2026 | Zenodo n13-same-datum-v1, [DOI 10.5281/zenodo.23034545](https://doi.org/10.5281/zenodo.23034545). | Historical versioned record. |
| 29–30 Sep 2026 | WP19 v0.21 reports same-datum N11–N18 certificates. | Finite cutoff family; v0.29.1 checks supplied records, not original Arb enclosures. |
| 30 Sep 2026 | Downloads archive wp19-v0-27c1-M14 contains two saved adjoint arrays, a pointwise VJP JSON record, and a SHA256SUMS file. | ZIP CRC and three listed file hashes matched in the earlier archive review. | Metadata describes a binary64 path reconstruction and one-point Arb cross-checks; no full trajectory, residual, or quadrature certificate was supplied. |
| 1 Oct 2026 | WP19 v0.28 reverse-time viscosity-sign correction and recurrence follow-up. | Corrected sign convention; later M14 audit remains conditional and three-step. |
| 3 Oct 2026 | Draft PR #155 M14/M15 and active-support analysis; pilot disposition STOP. | Tail reduction reported, not independently reproduced; signed margin remains negative. |
| 18 Oct 2026 | Zenodo v3.5.0-PR155-Final, [DOI 10.5281/zenodo.23458745](https://doi.org/10.5281/zenodo.23458745). | Its description claims local regularity and elimination of finite-time blow-up; current audit does not support a continuum guarantee. Preserve historically and correct future metadata. |
| 19 Oct 2026 | Local `Reggae-Shark-Universe-v1.1.0-Release.zip`; the embedded Navier tree has a 30 Sep WP19 status note and the N14 runner/workflows. | Historical package snapshot; it contains no exact M15 lower-path input arrays. |
| 24 Oct 2026 | Umbrella update ZIP contains the portfolio index, standards, dossier PDF, README, and manifest only. | A dated umbrella/dossier snapshot, not a newer Navier source tree. |
| 26 Oct 2026 | Lightweight umbrella ZIP and full Git archive snapshot. | Lightweight ZIP has the Shark Protocol WP19 assumed-rate example; the separate full archive contains Navier code but no exact M15 lower-path inputs. |
| 1 Nov 2026 | v0.29 closure ZIP extracted; v0.29.1 audit PR opened. | 27-entry manifest matched; outputs do not supply the full-path M15 modewise certificate. PR #167 remains open. |
| 2 Nov 2026 | PR #167 CI run #18. | Confirms build and included package checks, not absent Arb inputs or a continuum result. |
| 2 Nov 2026 | Local ns_arb_verified_work tree timestamp shown in Explorer. | Extracted, non-Git snapshot with five manifest mismatches; Arb source presence does not prove it was run. |
| 4 Nov 2026 | Fresh N14 128-bit and 192-bit same-datum Arb certificates on Windows ARM64 CPU; archive reconciliation; Actions reruns. | Both finite N14 runs PASS, conditional on the supplied trajectory-error radius. The corrected reverse-time and v0.29.1 workflows both pass, including follow-up runs on the updated documentation commit. M14/M15 pilot remains STOP; continuum regularity remains OPEN. |

## Local Downloads snapshot audit

Read-only inventory covered the ZIP roots and full Navier subtree rather than only screenshots. These snapshots are separate points in time; the latest embedded WP19 status note in the Oct 19 release is still dated 30 September.

| Local archive | Inventory result | SHA-256 |
|---|---|---|
| `Reggae-Shark-Universe-v1.1.0-Release.zip` (19 Oct; 1,039 entries) | 808 Navier paths, including 23 workflow YAML files, the N14 same-datum runner, and v0.28 M14 recurrence outputs. The exact M15 lower-path `nodes.npy`, `rhs.npy`, and `metadata.json` inputs are absent. The filename says v1.1.0 while the embedded generic `RELEASE_MANIFEST.md` labels v3.5.0-PR155-Final; do not treat those labels as one reconciled release identity. | `e812078ff451f4b5a1cf554f9cc9f8134a7c60f8a2b19071b3722300d59599b5` |
| `Reggae_Shark_Universe_Umbrella_Update_2026-10-24.zip` (5 entries) | Portfolio index/README, standards, dossier PDF, and manifest only; no Navier source tree. | `4a41d1bd20c1869ddc192c2a531047479e1ac8640823adbc66caeb9b9d4aa332` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26.zip` (54 entries) | Lightweight umbrella including Shark Protocol v1.3.2. Its `wp19_segments.json` is explicitly an illustrative study based on assumed rates and marks all-cutoff status OPEN; it is not the Navier source tree. | `7a962763fc2b0d1e18f7f137d9a3605f0237ce845dd4b88d63254c7e64e98150` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26_git_archive.zip` (1,169 entries) | Full Git snapshot with 846 Navier paths, including the N14 runner and v0.28 records, but no N14 result payload and none of the exact M15 lower-path inputs. | `fb19c96c32509531fb30b31b8561d0199568337027a701090021a105db87144c` |

The Oct 19 archive's 23 workflows are definitions, not evidence that their runs passed. A separate Actions API review shows the manifest-corrected reverse-time workflow and v0.29.1 verification passing in runs 41832891663 and 41832891665, with both workflows passing again on the follow-up documentation commit in runs 41835258480 and 41835258517. The specialist GitHub release remains `n13-same-datum-v1` (29 Sep); the 18 Oct Zenodo record is not a Git tag, and the umbrella's `lrsc-v1.2.1-supplement` tag is unrelated to Navier.

## Next proof gate

Before reconsidering the M14/M15 pilot, supply and independently check: (1) a certified modewise M15-versus-M14 error vector over the relevant path; (2) a componentwise terminal-gradient mismatch bound; (3) a localized Hessian remainder small enough to preserve the signed margin; and (4) exact Arb inputs, source hashes, and captured run output.

Until then, keep the pilot **STOP** and the continuum bridge **OPEN**. The Oct 18 Zenodo record should be scope-corrected in a future version; this update does not edit that external record.

## Source trail

- [WP19 N14 certificate and Actions audit note](WP19_N14_ARM64_CERTIFICATE_AND_ACTIONS_AUDIT_2026_11_04.md)
- [WP19 v0.29.1 audit PR #167](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/167)
- [WP19 v0.28 reverse-time sign-correction note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_28_REVERSE_TIME_SIGN_CORRECTION_2026_10_01.md)
- [WP19 v0.21 N11–N18 chain note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md)
- [Umbrella mirror index](https://github.com/reggaesharkk/Reggae-shark-universe-/blob/main/docs/REPO_MIRROR_INDEX.md)

