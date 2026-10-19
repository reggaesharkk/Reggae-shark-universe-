# WP16 frozen N16 Windows runner

Only after the N16 protocol commit is merged, pull the canonical repository's main branch and run from its root:

1. `01_N16_SMOKE.cmd` — construct N16; score baseline/inherited only; save trial-0 checkpoint.
2. `02_N16_FULL_RESUME.cmd` — resume and complete 520 frozen proposals after reviewing smoke resources.
3. `03_N16_TIME_GATE.cmd` — evaluate the frozen time gate after continuation completes.

The launcher verifies the N15 predecessor and K36 source hashes before each run. The search grid is 64 because 48 fails the strict `grid > 3N` condition at N16. Refinement grids are 64, 96, 128. Seed 20260941; 16 global draws; 3 new-mode and 4 full-support block rounds; 72 trials per round; block size 40; phase step 0.30 with multiplier 0.6. Checkpoint resume verifies code and input fingerprints.

The trial-0 smoke does not run any proposal. Keep its checkpoint for the full run. N16 output belongs in `results/wp16_n16_holdout/` and should not be interpreted as PDE or continuum evidence.
