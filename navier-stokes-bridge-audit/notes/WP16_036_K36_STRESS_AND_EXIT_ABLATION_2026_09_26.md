# WP16 K36 stress and finite-time exit ablation

Prince Upadhyay, Independent Research — 26 September 2026

This **post-hoc** stress suite retains the N11-frozen K36 source keys and all three gate criteria. It tests numerical grid independence, arbitrary perturbations around the two N12/N13 full-final states, and hybrid states assembled at each of the six previously observed first sampled trajectory exits. None of these stresses is a new prospective holdout.

## Numerical kernel and static perturbations

The dealiased FFT Galerkin derivative was compared at each N12/N13 full-final state using grid sides `3N+1`, `4N+1`, and `5N+1`. The largest absolute component difference from the `4N+1` derivative was `2.79e-12` at N12 and `2.75e-12` at N13. All three sizes avoid convolution aliasing in the retained ball. The separate comparison with the original explicit-convolution derivative at N4/N7 was archived with the trajectory result.

For each cutoff and perturbation level, 32 independent fixed-seed draws varied every conjugate-paired coefficient by a uniformly sampled bounded scalar phase or real amplitude factor. At both full-final states, all 32 draws passed at each level: per-mode phase changes bounded by 0.04, 0.08, and 0.20 radians, and per-mode relative amplitude changes bounded by 2%, 5%, and 10%. The smallest observed mass fraction was 0.910869 at N13 with phase bound 0.20. These are descriptive draws; they are not confidence intervals or universal bounds. The rigorous smaller phase neighborhood was archived separately.

The ranked outside-group envelope provides targeted static stresses. Boosting all modes in the first five outside orbit pairs by a factor of 2 still passes at both cutoffs (mass fractions 0.912535 N12 and 0.912878 N13); a factor of 3 fails the mass gate (0.886238 and 0.887106). Boosting only the first outside pair by 3 fails N13 (0.899256) but passes N12 (0.914786). A radial weighting `exp(2 |j|²/N²)` fails both. These large modifications demonstrate a failure route, not a minimal adversarial perturbation.

## Hybrid-state ablation at the first sampled exits

Let `a_j` be an optimized anchor coefficient and `b_j` that coefficient after the finite Galerkin trajectory reaches its first coarse sampled gate failure. Hybrids preserve reality and divergence freedom. “Magnitudes only” uses `|b_j| a_j/|a_j|`; “directions only” uses `|a_j| b_j/|b_j|`. A third hybrid uses evolved magnitudes and scalar phases `arg(<a_j,b_j>)` while retaining the initial complex vector polarization. Hybrids are constructed fields, not actual trajectories.

| N | State | Actual evolved mass fraction | Magnitudes only | Directions only | Magnitudes + scalar phases, initial polarization |
|---|---|---:|---:|---:|---:|
| 12 | inherited | **0.898398 fail** | 0.915301 pass | 0.928982 pass | 0.918221 pass |
| 12 | target_only | **0.898401 fail** | 0.915325 pass | 0.928980 pass | 0.918225 pass |
| 12 | full_final | **0.896459 fail** | 0.916838 pass | 0.923388 pass | 0.919797 pass |
| 13 | inherited | **0.896877 fail** | 0.916916 pass | 0.922896 pass | 0.916952 pass |
| 13 | target_only | **0.896990 fail** | 0.920121 pass | 0.923098 pass | 0.917948 pass |
| 13 | full_final | **0.899648 fail** | 0.908264 pass | 0.925714 pass | 0.922502 pass |

The scalar-phase-only hybrid also passes all six exits. The signed-share gate passes in every shown hybrid and in the actual evolved fields at these first mass exits. Relative full-field `L²` displacement from the anchor is 0.144–0.186; relative vector-magnitude `L²` displacement is 0.092–0.113. The tracked advector `p=(3,2,2)` magnitude has already fallen to 0.598–0.698 of its initial value across these states.

**Observed mechanism:** the first mass-gate exit is a non-additive interaction of evolved magnitudes and complex vector directions. Neither one-factor hybrid reproduces the failure; retaining initial vector polarizations with evolved magnitudes and scalar phases also does not. This identifies a missing ingredient for a persistence estimate but does not isolate a unique causal triad or prove a continuum mechanism.

## What to prove next

An analytic trajectory bound must control the evolving outside-to-inside absolute group mass ratio while accounting jointly for magnitudes, scalar phases, and vector polarization. The earlier fixed-magnitude phase certificate cannot do this. The static prospective holdouts and their frozen gates remain untouched; the trajectory exits remain finite sampled results. No chemical, biological, or quantum analogy currently supplies the needed inequality.

Reproduce from `src/wp16_036_K36_stress_suite.py`, `src/wp16_036_K36_exit_ablation.py`, and the archived continuation/source/envelope/crossing JSON. Results are `results/wp16_n13_holdout/K36_stress_suite_N12_N13.json` and `results/wp16_n13_holdout/K36_exit_ablation_N12_N13.json`.
