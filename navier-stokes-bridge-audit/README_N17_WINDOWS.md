# WP16 frozen N17 Windows runner

This package overlays the existing WP16 VS Code CPU runner. Keep the N16
continuation at `results/wp16_n16_holdout/wp16_phase_cutoff_escalation_N16.json`.
The launcher checks its SHA-256 against
`53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca`.
Do not edit or regenerate that file to make a mismatched hash pass.

**Only after the complete N17 protocol commit is merged**, use the repository
root (or overlay the supplied N17 files onto the existing standalone WP16
runner root). Then run these one at a time:

1. `01_N17_SMOKE.cmd`: build N17 and score baseline and inherited only. Saves
   a trial-0 checkpoint, with zero proposals evaluated. This may take time.
2. `02_N17_FULL_RESUME.cmd`: resume the same checkpoint through 520 proposals.
   It refuses to start unless the trial-0 checkpoint exists.
3. `03_N17_TIME_GATE.cmd`: evaluate the original frozen K36 three-state gate
   through `t=0.0030`, including half-step exit checks.
4. `04_N17_MECHANISM_GATE.cmd`: apply the previously frozen ordered-orbit and
   normalizer test. It requires the broad time-gate file first. A failed
   mechanism result is saved and must be retained.

The continuation uses seed `20260942`, grid 64 (strictly above `3*17=51`),
the unchanged 16+3×72+4×72 schedule, chunked exact objective, and 64/96/128
fixed-winner refinement. Checkpoints atomically save the RNG and code/input
fingerprints. The source archive and compact K36 keys are already in the
standalone N16 bundle. If the N16 predecessor JSON or those files are missing,
the launcher stops before the N17 score.

The N12–N16 data used to design the source-level mechanism are discovery data.
N17 is one finite Galerkin holdout. A pass or failure does not establish a
cutoff-uniform PDE estimate or resolve Navier–Stokes regularity.
