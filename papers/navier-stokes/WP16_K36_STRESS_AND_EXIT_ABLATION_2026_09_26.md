# WP16 K36 stress and exit ablation — 26 September 2026

The frozen coalition remains unchanged. The alias-free N12/N13 Galerkin derivative agrees across three FFT grid sizes to about `3e-12` maximum absolute difference. In 32 fixed-seed draws at each setting, both full-final states pass under every tested bounded per-mode phase perturbation (up to `±0.20` radians) and bounded real amplitude perturbation (up to `±10%`). This is descriptive robustness, not a universal bound.

Targeted amplification of the leading outside-source orbit modes can break the static 90% mass gate: multiplying modes in the first five outside ranked orbit pairs by 3 yields mass fractions **0.8862 (N12)** and **0.8871 (N13)**. The corresponding factor 2 cases still pass.

At **all six actual first sampled finite-time gate exits**, hybrids carrying only evolved modal magnitudes, or only evolved complex vector directions, still pass. Hybrids carrying evolved magnitudes and scalar phases with initial polarizations also pass. The evolved states fail the mass gate. This post-hoc ablation points to a coupled magnitude–direction–polarization change; it does not prove a unique causal source or continuum result.

[Full research note](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/WP16_036_K36_STRESS_AND_EXIT_ABLATION_2026_09_26.md) · [stress data](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/results/wp16_n13_holdout/K36_stress_suite_N12_N13.json) · [six-state ablation](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/results/wp16_n13_holdout/K36_exit_ablation_N12_N13.json)
