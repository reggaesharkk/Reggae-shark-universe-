# WP16 frozen N15 Windows runner

This launcher implements the N15 protocol frozen in `notes/WP16_036_N15_PROSPECTIVE_FREEZE_2026_09_26.md`.

Use in this order only after pulling the freeze commit:

1. `01_N15_SMOKE.cmd` — trial-0 construction and baseline/inherited scoring only.
2. `02_N15_FULL_RESUME.cmd` — resume/complete the fixed 520-proposal search.
3. `03_N15_TIME_GATE.cmd` — run the time gate only after the final N15 continuation exists.

The runner verifies the exact N14 predecessor hash and exact frozen source JSON hash before executing.

Frozen N15 schedule: seed 20260940; search grid 48; 16 global new-mode draws; 3 new-mode block rounds; 4 full-support block rounds; 72 trials per round; block size 40; initial step 0.30; 520 total proposals; refinement grids 48/64/96/128.

Do not alter K36, thresholds, seed, schedule, objective, time window, or failure rules after viewing N15 output.
