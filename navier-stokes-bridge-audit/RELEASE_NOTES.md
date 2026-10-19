# Release 0.2 — phase, shells, and strain supplement

- Adds `MASTER_RECORD_SUPPLEMENT_2026_09_24.md` with a claim and evidence
  register, explicit limitations, numerical ledger, and conditional
  cutoff-uniform proof target.
- Adds four diagnostic scripts and four recorded JSON outputs under `src/`:
  `phase_cascade_trajectory`, `smooth_commutator_gate`,
  `strain_alignment_trajectory`, and `spacetime_strain_commutator_gate`.
- The supplementary initial field, short interval `[0, 0.02]`, and
  `N=4`/`N=5` cutoff comparison are distinct from the v0.1 WP1–10
  seeded trajectories. The exact strain decomposition and numerically
  checked space-time budget do not yield a cutoff-uniform bound.
- Updates citation, README, and license scope for v0.2. The new Zenodo
  version DOI is assigned only after this GitHub release is archived;
  the v0.1 DOI remains specific to the original archive.
- Provides `MANIFEST_v0_2.sha256` for the v0.2 snapshot; the older
  `MANIFEST.sha256` is retained for provenance of the original candidate.

**Status:** exploratory finite-mode audit and classical small-data
estimate. No proof of global smoothness or finite-time singularity for
arbitrary initial data. No claim of external peer review.

## Release 0.1 — finite Fourier audit (prior release)

- Bundled WP1–10 scripts, seeded JSON results, scope notes, a complete
  audit report, and a self-contained WP3 small-data proof audit.
- Incorporated the corrected WP8 FFT frequency indexing (v0.2 of WP8).
- Used the actual executed WP10 v0.1 helicity identity and recorded
  closure values. Rejected draft logs and unrelated projects are excluded.
- Scope: finite-mode diagnostics and a standard conservative small-data
  estimate. No general periodic Navier–Stokes smoothness claim.

The original tag is `v0.1` and the specific archived version DOI is
`10.5281/zenodo.22932635`.
