# WP19 v0.10 — Signed C500 Numerator Certificate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** rigorous exact-rational endpoint certificate composed with the validated trajectory radii.  
**Not claimed:** a dynamic next-cutoff bridge, unseen N14 result, all-N estimate, or continuum theorem.

## Reduction

v0.9 certifies all 36 K36 numerator signs inside each current endpoint ball.

Therefore, on each such ball,

`H_C500 = sum_K36 sigma_g n_g - 9 sum_C500 tau_g n_g`

is exactly the numerator of the C500 upper surrogate.

Its sign can be certified **before dividing by the normalizer**.

## Group-specific perturbation bound

For one retained ordered group `g`, write its source-pair set as `G`.

For perturbation `e` with `||e||_2 <= E`, the source-vector change satisfies

`delta_d_g <= (C1_g + C2_g) E + C3_g E^2`

where the first two coefficients are Cauchy-Schwarz bounds over repeated left/right indices and

`C3_g = sqrt(sum_(p,q in G) |q|^2)`.

The group-specific bound is then propagated through `w_g` and
`n_g = Im(w_g conj(z))`. All endpoint coefficients are exact Fractions and every square root is outward-enclosed by a rational grid.

## Certified results

| N | nominal signed numerator | error upper | certified numerator upper | certified G upper |
|---:|---:|---:|---:|---:|
| 11 | -126446372544.2311 | 7824215175.758824 | -118622157368.4723 | **-44.84468560750583** |
| 12 | -145437499213.9031 | 1937865563.687478 | -143499633650.2157 | **-54.41406495135733** |
| 13 | -145665731048.3027 | 2077587684.756144 | -143588143363.5466 | **-54.96100844772338** |

All numerator upper bounds are strictly negative.

The independent normalizer lower bounds remain positive:

- N11: 51416.57915303983
- N12: 51349.83296890201
- N13: 51109.15921574555

Hence the C500 upper surrogate is rigorously negative at all three current cutoffs.

## Improvement over v0.7

v0.7 used one key-independent universal coefficient-9 perturbation envelope.

v0.10 retains the fixed finite C500 support and charges each retained group only for its own source geometry.

The dynamic proof target is now cleaner:

`validated cutoff defect -> signed polynomial numerator -> separate normalizer guard`.

The remaining bridge is dynamic: a validated dual-weighted residual plus second-order remainder for this frozen signed numerator.

No continuum conclusion follows.
