# WP16 — Frozen N14 Windows Runner

This launcher continues the exact WP16 state frozen on **26 September 2026**. It does not contain or invent a new N14 result. It wraps the already-merged canonical scripts so the prospective N14 continuation can be run on Windows without manually editing paths or parameters.

Put the launcher files in the repository root, next to `src/`, `results/`, and `requirements.txt`.

Canonical inputs:
- `results/wp16_n13_holdout/wp16_phase_cutoff_escalation_N13.json`
- `results/wp16_n12_holdout/wp16_036_phase_velocity_rhs_sources.json.gz`

The launcher verifies the frozen N13 SHA-256:
`13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd`.

Recommended sequence:
1. `01_N14_SMOKE.cmd`: build N14 table, score baseline/inherited state, write trial-0 checkpoint, no proposal.
2. `02_N14_FULL_RESUME.cmd`: run/resume all 520 frozen proposals and then refinements at grids 48/64/96/128.
3. `03_N14_TIME_GATE.cmd`: run the prospective static/time gate after the final N14 continuation exists.

`04_N14_ALL_IN_ONE.cmd` runs all three stages. If interrupted during the long search, rerun it; the atomic checkpoint resumes after the last completed proposal.

Outputs:
- `results/wp16_n14_holdout/wp16_N14_checkpoint.json`
- `results/wp16_n14_holdout/wp16_phase_cutoff_escalation_N14.json`
- `results/wp16_n14_holdout/wp16_036_N14_frozen_time_gate.json`

Frozen schedule: seed 20260939; search grid 48; 16 global new-mode draws; 3×72 new-mode block trials; 4×72 full-support block trials; block size 40; initial step 0.30; total 520 proposals; refinement grids 48/64/96/128; immutable N11-derived K36; viscosity 0.1; N14 time grid dt=0.0001 through t=0.0030.

This is finite computation, not a continuum theorem or a global optimum.
