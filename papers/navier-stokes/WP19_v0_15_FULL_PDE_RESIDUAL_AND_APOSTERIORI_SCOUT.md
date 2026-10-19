# WP19 v0.15 — Full-PDE Residual and A-Posteriori Regularity Scout

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** non-rigorous residual scouting built on the separately validated finite-N14 Galerkin trajectory.  
**Not claimed:** a continuum strong-solution certificate, regularity theorem, blowup theorem, or Millennium Prize result.

## 1. Why this gate exists

WP19 v0.12-v0.14 isolated a fixed low-mode recursive closure and showed that the frozen K36/C500 observable cannot by itself be a regularity criterion.

A different route is therefore required to connect the finite Galerkin computation to continuum regularity.

There is established a-posteriori Navier-Stokes theory in which a sufficiently accurate numerical/Galerkin approximation can certify existence of a strong continuum solution on a finite interval. Older criteria use relatively strong residual norms; recent work develops criteria based on critical `L^3` stability and negative Sobolev residual norms.

This gate asks a narrower question:

> What does the already validated N14 predictor look like when its **full continuum PDE residual outside the N14 Galerkin space** is measured in several Sobolev norms?

## 2. Object measured

The N14 Galerkin trajectory satisfies the projected equation

```
du14/dt + nu A u14 + P14 B(u14,u14) = 0
```

up to the separately certified time-path error.

Viewed as an approximation to the **full** periodic Navier-Stokes equation, the spatial truncation residual is

```
R_tail(t) = (I-P14) B(u14(t),u14(t)).
```

Because `u14` is supported in `|k|<=14`, the quadratic residual is supported in frequencies up to 28 and can be computed without aliasing on the existing `57^3` dealiased grid.

This scout evaluates `R_tail` at the 121 saved predictor nodes.

It does **not** yet provide a whole-segment interval enclosure.

## 3. N14 predictor norms

The saved predictor gives:

| quantity | sampled value |
|---|---:|
| `sup_t ||u14||_2` | 111.220626189 |
| `sup_t ||u14||_Hdot1` | 226.827893385 |
| `sup_t ||u14||_Hdot2` | 746.305816779 |
| `sup_t ||u14||_Hdot3` | 3926.973541104 |
| `||u14||_(L2_t Hdot2)` | 40.025001955 |

On the natural `57^3` dealiased physical grid, using volume-normalized spatial averages:

| quantity | sampled value |
|---|---:|
| `sup_t ||u14||_L3` | 117.844184420 |
| `sup_t ||u14||_L6` | 133.428131351 |
| `||u14||_(L4_t L6_x)` | 31.081463808 |

These are floating node/grid diagnostics.

## 4. Full-PDE omitted residual

For `R_tail = Q14 B(u14,u14)`, the node-sampled values are:

| norm | maximum | time norm / integral |
|---|---:|---:|
| `H^-1` | 10.751542055 | `L1_t=0.0166855303` |
| `H^-1` | — | `L2_t=0.3312582611` |
| `H^-1` | — | `L3_t=0.9360002088` |
| `L2` | 160.907430579 | `L1_t=0.2502340502` |
| `L2` | — | `L2_t=4.9703990588` |
| `H1` | 2418.959546632 | `L1_t=3.7718196582` |
| `H1` | — | `L2_t=74.9506155266` |
| `H2` | 36551.079067900 | `L1_t=57.1776595761` |

The difference between positive and negative residual norms is substantial:

```
||R||_(L1_t H1) / ||R||_(L1_t H^-1) ~= 226.05
```

and

```
||R||_(L2_t L2) / ||R||_(L2_t H^-1) ~= 15.00.
```

## 5. Result: the old positive-norm route is not the natural next certificate

Classical a-posteriori regularity work by Chernyshenko-Constantin-Robinson-Titi and Dashti-Robinson establishes rigorous numerical verification routes for 3D Navier-Stokes strong solutions.

The minimal-regularity Dashti-Robinson framework still involves positive residual norms such as `L1_t H1` and `L2_t L2`, together with high norms of the approximate solution.

For the present N14 predictor, the raw omitted PDE residual is not small in those positive norms:

```
||R_tail||_(L1_t H1) ~= 3.77
||R_tail||_(L2_t L2) ~= 4.97.
```

This does not prove that the older criterion fails after every possible sharpening, because this scout is not a rigorous evaluation of its full constants and continuous-time terms.

It does show that simply plugging the N14 trajectory into a coarse positive-Sobolev residual test is not an attractive route.

## 6. Result: negative residual norms are materially smaller

Recent a-posteriori work on the periodic 3D equations formulates a strong-solution verification criterion around critical `L-infinity_t L3_x` stability and uses weak residual norms, including `L2_t W^-1,2_x` and `L3_t W^-1,3_x`.

The Fourier `H^-1 = W^-1,2` part of the N14 truncation residual is much smaller:

```
||R_tail||_(L2_t H^-1) ~= 0.331258261.
```

The `L1_t H^-1` diagnostic is only

```
0.0166855303.
```

This does **not** establish the modern criterion. In particular:

- `W^-1,3` has not yet been bounded;
- the criterion's embedding/projection constants have not been specialized to this normalization;
- the reconstruction must be treated continuously in time;
- the existing Arb Galerkin path error must be combined with the full-PDE residual;
- all required quantities must be enclosed rigorously.

But the negative-norm reduction identifies the more plausible continuum-regularity verification route.

## 7. Important distinction from the K36/C500 theorem

This gate does not attempt to prove

```
G<0 => regularity
```

or

```
G<0 => singularity.
```

Those shortcuts were already ruled out.

Instead, the program becomes:

1. **finite observable:** preserve the fixed low-mode signed numerator across cutoffs;
2. **continuum existence:** independently certify a strong continuum solution on `[0,0.003]` with an a-posteriori residual theorem;
3. only then ask whether the continuum K36/C500 behavior has a useful PDE interpretation.

This keeps the recursive-closure theorem and the regularity theorem logically separate.

## 8. Next rigorous gate

The next regularity-side computation should target the modern negative-residual framework:

1. construct a continuous-time divergence-free N14 reconstruction from the already certified Hermite path;
2. rigorously enclose the full PDE residual, including `Q14 B(v,v)`;
3. certify its `L2_t W^-1,2` norm;
4. derive/certify a usable `L3_t W^-1,3` bound;
5. certify the reconstruction's `L-infinity_t H1`, `L-infinity_t L3`, and `L4_t L6` terms;
6. evaluate the published a-posteriori strong-solution inequality with explicit torus constants.

A PASS would certify continuum strong existence only for this explicit datum and time interval.

A FAIL would be retained as a quantitative obstruction and would not imply singularity.

## References

- S. I. Chernyshenko, P. Constantin, J. C. Robinson, E. S. Titi, *A Posteriori Regularity of the Three-dimensional Navier-Stokes Equations from Numerical Computations*, Journal of Mathematical Physics 48 (2007), 065204. DOI: 10.1063/1.2372512.
- M. Dashti, J. C. Robinson, *An A Posteriori Condition on the Numerical Approximations of the Navier-Stokes Equations for the Existence of a Strong Solution*, SIAM Journal on Numerical Analysis. arXiv:math/0701341.
- A. Brunk, J. Giesselmann, T. Tscherpel, *A posteriori existence of strong solutions to the Navier-Stokes equations in 3D*, arXiv:2509.25105 (2025).

## Claim boundary

All residual values in v0.15 are floating, node-sampled diagnostics. The finite N14 Galerkin trajectory has a separate Arb validation, but the full continuum residual has not yet been interval-enclosed. No continuum regularity conclusion is claimed.
