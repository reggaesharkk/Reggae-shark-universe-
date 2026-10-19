# WP16 K36 finite trajectory gate: transient survival and exit

Prince Upadhyay, Independent Research — 26 September 2026

## Question and method

The N11-frozen K36 coalition passed the prospective N12/N13 static holdouts. Do those six phase-optimized Galerkin states retain the gate when released under the unmodified finite Navier–Stokes vector field, with viscosity `ν=0.1`?

From each of `inherited`, `target_only`, and `full_final` at N12 and N13, integrate the **full finite Galerkin ODE** by RK4. The original solver materializes every convolution pair; this equivalent implementation computes the full quadratic term by FFT on a grid of side `4N+1`, which exceeds the `3N` alias-free requirement for outputs `|k|≤N`. The K36 channel itself is always evaluated from the original explicit ordered-source formula at `k=(6,0,3)`. There is no spectral omission or closure model.

An independent derivative check against the original direct-convolution `System.rhs` on random divergence-free finite states gave maximum absolute differences `6.48e-14` at N4 and `6.46e-13` at N7. At time zero, all six mass fractions and signed shares reproduce the archived holdouts. Reality and divergence residuals along the trajectory remain at numerical roundoff. This validates the implementation at smaller cutoffs and the initial reconstruction; it is not an interval-arithmetic proof of time integration at N12/N13.

## Sampled first exits

| Cutoff | Start state | Last passing sample | First failing sample | First failing mass fraction | Signed share then |
|---|---|---:|---:|---:|---:|
| N12 | inherited | 0.0025 | 0.0026 | 0.898398 | 0.890153 |
| N12 | target_only | 0.0025 | 0.0026 | 0.898401 | 0.890127 |
| N12 | full_final | 0.0020 | 0.0021 | 0.896459 | 0.915356 |
| N13 | inherited | 0.0019 | 0.0020 | 0.896877 | 0.927534 |
| N13 | target_only | 0.0019 | 0.0020 | 0.896990 | 0.922374 |
| N13 | full_final | 0.0022 | 0.0023 | 0.899648 | 0.919678 |

Time is measured **after** each optimized anchor state (the base-state anchor time was `0.005`). At every sampled time through `0.001`, all six gates pass. At each first sampled failure, the **absolute mass fraction** has fallen below `0.90`; the signed share is still inside `[0.8,1.2]` and has the same sign.

RK4 with `dt=0.0001` was compared with `dt=0.00005` through `t=0.001` in all six states. The maximum difference of the three displayed endpoint quantities (mass fraction, signed share, total signed channel) is under `1.84e-5` in their respective units. The first-exit brackets were also checked at half step size for four representative states: N12 inherited `[0.00250,0.00255]`, N12 full-final `[0.00200,0.00205]`, N13 inherited `[0.00190,0.00195]`, N13 full-final `[0.00225,0.00230]`. At the coarse first-fail samples, their coarse/half-step mass-fraction differences are at most `1.25e-8`. N12 target-only and N13 target-only were checked at half step through `t=0.001` but not at their exit brackets.

## Interpretation and scope

The static prospective K36 holdout remains valid. The coalition's **90% mass gate is not persistent for these initialized finite trajectories**: direct finite dynamics redistributes source mass outside the frozen set within a few thousandths of a time unit. The earlier static local phase certificate applies only to fixed magnitudes and polarizations, so it cannot be extended along this trajectory without tracking their evolution. These initialized states arise from phase optimization, not from an assertion that the baseline Galerkin trajectory reaches them spontaneously.

This is sampled finite-dimensional evidence. It neither proves a continuous-time crossing to arbitrary numerical precision nor supplies an all-cutoff continuum statement. The next analytic target is a differential inequality for the evolving **outside/inside absolute source mass**, including magnitude and polarization changes. A phase-only bound cannot control the observed exit by itself. None of the chemistry, biology, or quantum analogies supplies that missing inequality.

Reproduce with `src/wp16_036_dealiased_trajectory_gate.py` and the archived N11/N12/N13 continuation JSON plus N11 source ranking. The repository includes full sampled `t≤0.005` output, half-step checks, and a compact summary. No coalition or pass criterion was retuned.

The full sampled JSON files are stored as `*.json.gz.b64` text. Decode with `base64 -d FILE.json.gz.b64 | gzip -d > FILE.json`. The compact summary is ordinary JSON.
