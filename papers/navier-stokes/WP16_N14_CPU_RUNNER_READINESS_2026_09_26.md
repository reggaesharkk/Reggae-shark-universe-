# WP16 N14 memory-bounded CPU runner ready — 26 September 2026

The corrected prospective N14 protocol was merged before any N14 scores. A memory-bounded implementation now preserves the original phase objective: compact high-advector source indices plus chunked per-ordered-triad transfer and absolute envelope, dealiased FFT for the base-state ODE, and the original positive-stretching grid calculation. The required N14 search grid is **48** (grid must exceed 3N=42).

Archived N12/N13 best-state objective fields were reproduced to summation-order precision; the quotient `C` differed by only about `2e-14`. At N14, the compact table has 61,783,500 entries (~707 MiB); trial-0 baseline/inherited and a single checkpointed proposal used about 807 MiB peak resident memory in the Linux smoke environment. This does **not** establish Windows peak memory or complete the 520-trial optimization.

The runner writes an atomic checkpoint after every trial with its RNG state and phase vector. A separate evaluator applies the frozen K36 static/time-resolved gates only after a completed continuation. No N14 holdout verdict exists yet.

[Implementation and validation note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP16_036_N14_CPU_IMPLEMENTATION_READINESS_2026_09_26.md) · [CPU continuation](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp16_036_N14_cpu_continuation.py) · [time gate](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp16_036_N14_time_gate.py)
