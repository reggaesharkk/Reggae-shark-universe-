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
- **GitHub Actions:** The corrected reverse-time sign-correction [run 41840289264](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41840289264) and v0.29.1 verification [run 41840288927](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41840288927) both passed on PR head `3faa7e3cee8909037c26d19f77456ca88011b1fe`. After PR #167 merged, main-commit verification [run 41843154820](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41843154820) also passed on `43d9bbf1b9dd1d47fa6ee60793e4c54d749af0ea`. These checks cover the correction replay, package integrity, Python regression suite, and declared Lean build/axiom checks; they do not supply missing raw M15 trajectory or adjoint enclosures. PR #167 is merged; M14/M15 remains STOP and continuum regularity OPEN.

## Dated record

| Date | Record or activity | Current reading |
|---|---|---|
| 24 Sep 2026 | First project record, Zenodo v0.2, [DOI 10.5281/zenodo.22940790](https://doi.org/10.5281/zenodo.22940790). | Initial finite Fourier diagnostics; exploratory scope. |
| 28 Sep 2026 | N11 finite-Galerkin crossing note; N17 mechanism-failure record. | Preserve both; neither establishes a continuum theorem. |
| 29 Sep 2026 | Zenodo n13-same-datum-v1, [DOI 10.5281/zenodo.23034545](https://doi.org/10.5281/zenodo.23034545). | Historical versioned record. |
| 29–30 Sep 2026 | WP19 v0.21 reports same-datum N11–N18 certificates. | Finite cutoff family; v0.29.1 checks supplied records, not original Arb enclosures. |
| 30 Sep 2026 | Downloads archive wp19-v0-27c1-M14 contains two saved adjoint arrays, a pointwise VJP JSON record, and a SHA256SUMS file. | ZIP CRC and three listed file hashes matched in the earlier archive review. | Metadata describes a binary64 path reconstruction and one-point Arb cross-checks; no full trajectory, residual, or quadrature certificate was supplied. |
| 1 Oct 2026 | WP19 v0.28 reverse-time viscosity-sign correction and recurrence follow-up. | Corrected sign convention; later M14 audit remains conditional and three-step. |
| 3 Oct 2026 | PR #155, opened 2 Oct, updated its M14/M15 forced-radius, weighted-remainder, and active-support audit; pilot disposition STOP. | The PR reports 12 frozen M15 shards / 240 half-steps, but its conservative remainder does not close the signed margin; the reported tail reduction is not independently reproduced. |
| 18 Oct 2026 | Zenodo v3.5.0-PR155-Final, [DOI 10.5281/zenodo.23458745](https://doi.org/10.5281/zenodo.23458745). | Its description claims local regularity and elimination of finite-time blow-up; current audit does not support a continuum guarantee. Preserve historically and correct future metadata. |
| 15–19 Oct 2026 | Reconstructed from the local Downloads/release trail and repository snapshots; the Oct 19 umbrella ZIP carries the Navier tree and workflow definitions. | The ZIP contains historical code and scalar/endpoint records, not the exact lower-path M15 arrays or a 120-slice M15 enclosure set; workflow YAML files alone are not run evidence. |
| 24 Oct 2026 | Umbrella update ZIP contains the portfolio index, standards, dossier PDF, README, and manifest only. | A dated umbrella/dossier snapshot, not a newer Navier source tree. |
| 26 Oct 2026 | Lightweight umbrella ZIP and full Git archive snapshot. | Lightweight ZIP has the Shark Protocol WP19 assumed-rate example; the separate full archive contains Navier code but no exact M15 lower-path inputs. |
| 1 Nov 2026 | v0.29 closure ZIP extracted; v0.29.1 audit PR opened. | 27-entry manifest matched; outputs do not supply the full-path M15 modewise certificate. PR #167 was opened for review and later merged on 4 Nov. |
| 2 Nov 2026 | PR #167 CI run #18. | Confirms build and included package checks, not absent Arb inputs or a continuum result. |
| 2 Nov 2026 | Local ns_arb_verified_work tree timestamp shown in Explorer. | Extracted, non-Git snapshot with five manifest mismatches; Arb source presence does not prove it was run. |
| 4 Nov 2026 | Fresh N14 128-bit and 192-bit same-datum Arb certificates on Windows ARM64 CPU; main-tree/PR #155 M15 input audit; Actions reruns. | Both finite N14 runs PASS, conditional on the supplied trajectory-error radius. PR #167 merged as source commit `43d9bbf1b9dd1d47fa6ee60793e4c54d749af0ea`; its merge-commit verification run 41843154820 passed. M14/M15 pilot remains STOP; continuum regularity remains OPEN. |

## 15–19 October M15 trail: what the files do and do not contain

The repository tree on `main` (842 tracked paths) and the open PR #155 file list were checked against the M15 trajectory claim. The tracked tree contains `next-work/n12_same_datum/`, the 120 JSON slices for `next-work/n13_same_datum/results/full_run/`, and `next-work/n14_same_datum/tools/`, but no `next-work/n15_same_datum/`, no `results/wp19_multin/N15/`, and no `M15_segment_*.json` adjoint records. `results/wp16_n15_holdout/` contains only its N15 summary JSON. The v0.28 segment records are M14 records (237–239 and baseline 237), not M15.

The v0.26/v0.27 `M14_to_M15.json` records are endpoint comparisons. Their own claim boundaries say the v0.26 floating design does not interval-enclose adjoint propagation, quadrature, or endpoint Taylor control; v0.27 certifies a terminal polynomial value/gradient only and explicitly excludes the backward adjoint, quadrature, nonlinear remainder, all-cutoff transfer, and continuum behavior. The v0.28 scalar recurrence propagates three M14 segment bounds (239, 238, 237) using imported strain/residual bounds; it is not a live M15 trajectory enclosure.

PR #155 (opened 2 Oct; updated through 2 Nov) adds frozen M15 forced-radius and weighted-remainder summaries, active-support records, and a localized Hessian audit. Its recorded result remains `NO_CLOSURE_CURRENT_CONSERVATIVE_MAJORANTS`: remainder upper about `1.6406308768e14` versus signed-integral lower bound about `5.7585744356e9`. Its changed-file list contains summary/replay outputs, not `nodes.npy`, `rhs.npy`, `metadata.json`, or a 120-slice M15 trajectory/enclosure set. Thus it advances a parametric/scalar-majorant audit, not full trajectory-certified M15 transfer. The October workflow files are recipes; their presence in a ZIP does not establish that a run completed.

This is an inventory finding, not proof that no copy exists outside the checked Git trees and archives. The inspected Oct 19 and Oct 26 local archives also lack the exact prescribed lower-path arrays. M14/M15 remains **STOP** until those exact inputs, matching adjoint data, and a sign-preserving remainder enclosure are supplied and independently verified.

## Local Downloads snapshot audit

Read-only inventory covered the ZIP roots and full Navier subtree rather than only screenshots. These snapshots are separate points in time; the latest embedded WP19 status note in the Oct 19 release is still dated 30 September.

| Local archive | Inventory result | SHA-256 |
|---|---|---|
| `Reggae-Shark-Universe-v1.1.0-Release.zip` (19 Oct; 1,039 entries) | 808 Navier paths, including 23 workflow YAML files, the N14 same-datum runner, and v0.28 M14 recurrence outputs. The exact M15 lower-path `nodes.npy`, `rhs.npy`, and `metadata.json` inputs are absent. The filename says v1.1.0 while the embedded generic `RELEASE_MANIFEST.md` labels v3.5.0-PR155-Final; do not treat those labels as one reconciled release identity. | `e812078ff451f4b5a1cf554f9cc9f8134a7c60f8a2b19071b3722300d59599b5` |
| `Reggae_Shark_Universe_Umbrella_Update_2026-10-24.zip` (5 entries) | Portfolio index/README, standards, dossier PDF, and manifest only; no Navier source tree. | `4a41d1bd20c1869ddc192c2a531047479e1ac8640823adbc66caeb9b9d4aa332` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26.zip` (54 entries) | Lightweight umbrella including Shark Protocol v1.3.2. Its `wp19_segments.json` is explicitly an illustrative study based on assumed rates and marks all-cutoff status OPEN; it is not the Navier source tree. | `7a962763fc2b0d1e18f7f137d9a3605f0237ce845dd4b88d63254c7e64e98150` |
| `Reggae_Shark_Universe_Umbrella_2026-10-26_git_archive.zip` (1,169 entries) | Full Git snapshot with 846 Navier paths, including the N14 runner and v0.28 records, but no N14 result payload and none of the exact M15 lower-path inputs. | `fb19c96c32509531fb30b31b8561d0199568337027a701090021a105db87144c` |

The Oct 19 archive's 23 workflows are definitions, not evidence that their runs passed. A separate Actions API review shows the manifest-corrected reverse-time and v0.29.1 workflows passed in runs 41832891663 and 41832891665, again in 41835258480 and 41835258517, and runs 41837999304 and 41837999345 on the earlier PR #167 head `c96b9de`. The latest PR-head checks [41840289264](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41840289264) and [41840288927](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41840288927) passed on `3faa7e3cee8909037c26d19f77456ca88011b1fe`; after merge, main verification [41843154820](https://github.com/reggaesharkk/navier-stokes-bridge-audit/actions/runs/41843154820) passed on `43d9bbf1b9dd1d47fa6ee60793e4c54d749af0ea`. The latest specialist same-datum certificate release remains `n13-same-datum-v1` (29 Sep). The 4 Nov [WP19 v0.29.1 audit-correction release](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/wp19-v0.29.1-audit-correction) is a separate review package, not a replacement certificate. The 18 Oct Zenodo record is not a Git tag, and the umbrella's `lrsc-v1.2.1-supplement` tag is unrelated to Navier.

## Next proof gate

Before reconsidering the M14/M15 pilot, supply and independently check: (1) a certified modewise M15-versus-M14 error vector over the relevant path; (2) a componentwise terminal-gradient mismatch bound; (3) a localized Hessian remainder small enough to preserve the signed margin; and (4) exact Arb inputs, source hashes, and captured run output.

Until then, keep the pilot **STOP** and the continuum bridge **OPEN**. The Oct 18 Zenodo record should be scope-corrected in a future version; this update does not edit that external record.

## Source trail

- [WP19 N14 certificate and Actions audit note](WP19_N14_ARM64_CERTIFICATE_AND_ACTIONS_AUDIT_2026_11_04.md)
- [M14/M15 audit PR #155](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/155)
- [WP19 v0.29.1 audit PR #167](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/167)
- [WP19 v0.28 reverse-time sign-correction note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_28_REVERSE_TIME_SIGN_CORRECTION_2026_10_01.md)
- [WP19 v0.21 N11–N18 chain note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md)
- [Umbrella mirror index](https://github.com/reggaesharkk/Reggae-shark-universe-/blob/main/docs/REPO_MIRROR_INDEX.md)

