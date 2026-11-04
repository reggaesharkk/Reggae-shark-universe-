# Navier–Stokes evidence timeline and current status

**As of:** 4 November 2026  
**Method:** Read-only review of dated records, source files, manifests, and GitHub CI. No new PDE or Arb computation was run for this addendum.

This chronology distinguishes archived claims from file/hash review and recorded execution. A matching manifest establishes byte agreement with that manifest; it does not, by itself, reproduce a numerical result.

## Current status

**The continuum regularity question remains open.** These materials do not prove global regularity, blowup, or a cutoff-uniform limit for three-dimensional incompressible Navier–Stokes.

- **N11–N18:** The Sep 29–30 records report a same-datum Arb certificate family. The Nov 1 v0.29.1 bundle checks supplied finite records and arithmetic; raw upstream Arb trajectories and inputs needed to regenerate those enclosures are absent. This replay is not a fresh Arb reproduction.
- **WP19 M14/M15:** The v0.29.1 M14 recurrence replays three backward scalar steps (239, 238, 237), conditional on imported strain and residual bounds; it is not a full adjoint-path enclosure. The reported M15 conservative remainder is about 1.6406e14 versus a signed lower bound of about 5.7586e9, leaving a negative margin. The reported steps 220–239 reduction is not independently reproduced in the bundle. The pilot remains **STOP**.
- **Earlier M14 VJP archive:** The Downloads archive shown in Explorer contains M14_adjoint_rhs.npy, M14_adjoint_values.npy, M14_arb_vjp_point.json, and SHA256SUMS. The reviewed ZIP CRC and three manifest entries matched. Its metadata describes a binary64 saved reconstruction with one-point 192-bit Arb-versus-FFT VJP checks, including selected-mode checks; it does not supply a full adjoint trajectory, residual, or quadrature enclosure. The numerical checks were not recomputed in this review.
- **192-bit Arb producer:** The local extracted tree contains wp19_v0_29_adjoint_segment_arb_v3.py, which imports python-flint Arb/Acb and sets 192-bit precision. It is written for one finite M-to-M+1 transition half-step using supplied arrays. Those arrays and run outputs are absent from the tree; this review did not run it.
- **Downloads helper:** wp19_modewise_arb_bridge.py uses Python Decimal at 60-digit precision to read existing JSON segments. It does not call Arb or recreate the 192-bit calculation, so it is not new Arb evidence.
- **Nov 1 closure ZIP:** Its 27-entry SHA-256 manifest matched on inspection. Stored outputs report N14→N15 endpoint separation, while N15→N16, N16→N17, and N17→N18 intervals are not separated. The modewise-vector item is a validator self-test, not a supplied full M15 error vector. The manifest does not independently recompute these results.
- **Local folder in the screenshot:** ns_arb_verified_work/navier-stokes-bridge-audit is an extracted snapshot with no Git metadata. Its 44-entry root hash manifest matched 39 entries; five differed: .gitignore, CITATION.cff, LICENSE.md, README.md, and RELEASE_NOTES.md. Its patch ZIP contains older synthetic 2D versions of several verifier/runner files, so those files are not promoted to the active source branch.
- **GitHub CI:** PR #167 is open and unmerged. Actions run #18 passed the Lean build and axiom audit, plus the Python replay and seven tests in normal, -O, and -OO modes (21 test executions). This verifies the included package, not absent raw Arb trajectories.

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
| 24 Oct 2026 | Master Research Dossier snapshot supplied by the author. | Keep as a dated snapshot; this is the newer Navier-specific status. |
| 1 Nov 2026 | v0.29 closure ZIP extracted; v0.29.1 audit PR opened. | 27-entry manifest matched; outputs do not supply the full-path M15 modewise certificate. PR #167 remains open. |
| 2 Nov 2026 | PR #167 CI run #18. | Confirms build and included package checks, not absent Arb inputs or a continuum result. |
| 2 Nov 2026 | Local ns_arb_verified_work tree timestamp shown in Explorer. | Extracted, non-Git snapshot with five manifest mismatches; Arb source presence does not prove it was run. |
| 4 Nov 2026 | Review of local Arb producer, Downloads Decimal helper, and v0.29 outputs. | No new numerical run. Pilot remains stopped pending certified vector, componentwise terminal-gradient comparison, and localized Hessian remainder. |

## Next proof gate

Before reconsidering the M14/M15 pilot, supply and independently check: (1) a certified modewise M15-versus-M14 error vector over the relevant path; (2) a componentwise terminal-gradient mismatch bound; (3) a localized Hessian remainder small enough to preserve the signed margin; and (4) exact Arb inputs, source hashes, and captured run output.

Until then, keep the pilot **STOP** and the continuum bridge **OPEN**. The Oct 18 Zenodo record should be scope-corrected in a future version; this update does not edit that external record.

## Source trail

- [WP19 v0.29.1 audit PR #167](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/167)
- [WP19 v0.28 reverse-time sign-correction note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_28_REVERSE_TIME_SIGN_CORRECTION_2026_10_01.md)
- [WP19 v0.21 N11–N18 chain note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md)
- [Umbrella mirror index](https://github.com/reggaesharkk/Reggae-shark-universe-/blob/main/docs/REPO_MIRROR_INDEX.md)

