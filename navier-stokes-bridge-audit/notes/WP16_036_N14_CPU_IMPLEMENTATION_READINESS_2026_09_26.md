# WP16 N14 memory-bounded CPU implementation readiness

Prince Upadhyay, Independent Research — 26 September 2026

This implementation follows the corrected pre-data N14 protocol in `WP16_036_K36_RATE_INEQUALITY_AND_N14_FREEZE_2026_09_26.md`: seed 20260939; selection grid 48 (the required alias-free grid exceeds 3N=42); 16 global new-mode draws; 3×72 new-block and 4×72 full-block trials; block size 40; initial step 0.30; refinement grids 48/64/96/128. The original `C_infinity_stretch` objective and phase proposal semantics are retained.

## Method and validation

`src/wp16_036_low_memory_objective.py` constructs the same ordered high-advector convolution table as the original solver using compact integer arrays, then evaluates the unchanged projected per-triad H² transfer and its absolute envelope in bounded chunks. The latter cannot be replaced by the FFT sum because the absolute value occurs **before** summation. Base-state RK4 uses the previously validated alias-free FFT convolution. Physical-space positive vorticity stretching uses the original `spatial_fields` routine and the specified grid.

Two random divergence-free N4 states matched the original objective exactly to displayed precision. At N7, two random states agreed to numerical summation-order precision (maximum absolute field difference under `1e-6` for quantities of much larger scale; transfer difference under `5e-9` in one run). On the archived N12 best phase vector at grid 40, every score field matched within `1e-9` relative and `1e-6` absolute; `C` differed by about `2.0e-14`. At archived N13 best phases at grid 40, the H² transfer differed by `6.71e-8` on `2.43e7`, the absolute envelope by `2.98e-7` on `1.58e8`, and `C` by `2.31e-14`. This validates the lower-cutoff objective equivalence numerically, not as a bit-for-bit identity.

At N14 the high-advector table contains `61,783,500` ordered sources and uses `707.06 MiB` in the three compact index arrays. A trial-0 baseline/inherited smoke run (after the protocol freeze) completed in about 60 seconds with measured Linux peak resident memory `806.91 MiB`. A checkpoint resume through trial 1 completed with a similar peak `806.64 MiB`. These are limited smoke trials; **the 520-trial continuation has not completed**. Windows memory and timing may differ. The user's laptop has 16 GB RAM / 512 GB storage; the run should still begin with the packaged trial-0 smoke test, then proceed through the atomic checkpoint runner.

## Files and stop/resume contract

- `src/wp16_036_N14_cpu_continuation.py`: validates the exact archived N13 input SHA, schedule and code fingerprints; saves best phases, score, RNG bit-generator state, trial index and records atomically after **every** completed proposal. If interrupted, rerun the same command with the same checkpoint and identical code/input; it resumes after the last completed trial. `--stop-after-trial 0` performs only baseline/inherited scoring and saves a checkpoint.
- `src/wp16_036_N14_time_gate.py`: after a complete N14 continuation, uses the frozen K36 keys to evaluate all three states through `t=0.003` at `dt=0.0001`, their initial/exit margin rates and half-step exit check. It refuses an N14 continuation with the wrong seed or search grid. It never retunes the coalition.

The time-gate runner is syntax checked and uses the same reconstruction and trajectory primitives validated at N12/N13. It has not been run on a completed N14 continuation because none exists. The trial-0/1 smoke checkpoint is not a completed N14 holdout and must not be interpreted as one.

Do not publish a static or time-resolved N14 verdict until all scheduled optimization trials finish, the final phase vector is refined at the frozen grids, and the time-gate output is checked. This implementation was prepared after the frozen protocol and before a complete N14 optimization.
