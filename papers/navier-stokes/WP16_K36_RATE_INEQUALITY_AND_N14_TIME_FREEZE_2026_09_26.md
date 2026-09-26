# WP16 rate inequality and prospective N14 time gate — 26 September 2026

The user's Windows VS Code N12/N13 quick trajectory reproduced all six archived t=0.001 mass fractions and signed shares to floating-point roundoff. N14 does not exist yet.

An exact finite ordered-source inequality for the frozen K36 90% mass margin `F=I−9O` is now recorded in the research repo: along a Galerkin trajectory with nonzero tracked denominator, `F(t)≥F(0)−∫[E_I+9E_O]dt`, where `E` sums the absolute complex source derivative magnitudes. A broader Cauchy–Schwarz bound uses `||a||₂, ||∇a||₂, ||dot a||₂, ||∇dot a||₂, |z|^{-1}`. At N12/N13 anchors the exact source loss envelope is 1.38–1.61 million, even though the actual margin is initially rising; the broad bound is 185–208 times looser. Thus neither estimate establishes K36 persistence.

**Pre-data amendment:** the first freeze mistakenly carried grid 40 from N13; N14 needs grid >42 for the spatial quadrature. The corrected search grid is **48**, with 48/64/96/128 refinements. No N14 state or score exists; git history preserves the original wording.

The prospective N14 protocol is frozen **before N14 data**: unchanged K36 keys and static gates, fixed continuation schedule and seed, time sampling through 0.003, first-exit and margin-velocity endpoints, and half-step validation. N14 optimization still requires a validated 16 GB memory-safe Windows implementation and has not been run.

[Full inequality, numeric audit, and frozen protocol](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP16_036_K36_RATE_INEQUALITY_AND_N14_FREEZE_2026_09_26.md) · [script](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/src/wp16_036_K36_margin_rate_envelope.py) · [data](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/results/wp16_n13_holdout/K36_margin_rate_envelope_N12_N13.json)
