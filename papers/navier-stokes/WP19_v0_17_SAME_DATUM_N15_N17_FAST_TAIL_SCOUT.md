# WP19 v0.17 — Same-Datum N15–N17 Fast Tail Scout

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** prospective floating same-datum scouting beyond the separately certified N14 base.  
**Not claimed:** N15–N17 Arb validation, geometric decay theorem, all-cutoff persistence, continuum regularity, or blowup.

The unchanged rational witness was evolved at N15, N16 and N17 with `nu=0.1`, `T=0.003`, `h=0.000025`, 120 RK4 steps, and no retuning.

Endpoint diagnostics:

| N | F(T) | G_C500(T) |
|---:|---:|---:|
| 14 | -87.088300523 | -52.841462912 |
| 15 | -86.927457526 | -50.622544817 |
| 16 | -86.708694823 | -50.226878627 |
| 17 | -86.479868270 | -50.123036025 |

Successive positive G increments are approximately `2.21891809`, `0.39566619`, and `0.10384260`, with observed ratios `0.1783` and `0.2625`.

Endpoint P11 state drifts shrink from `1.5767e-2` to `8.5441e-3` to `3.2720e-3`.

The newly opened shell endpoint L2 norms are approximately `0.13645`, `0.10239`, and `0.06831`.

At every fifth saved node, the fixed-low closure difference was decomposed into direct new-shell and recursive backreaction pieces. Node-trapezoid L1_t L2_x totals are approximately:

| pair | direct | backreaction | total |
|---|---:|---:|---:|
| 14→15 | 0.00773144 | 0.01425319 | 0.01715920 |
| 15→16 | 0.00326381 | 0.00788305 | 0.00906981 |
| 16→17 | 0.00155282 | 0.00316159 | 0.00350017 |

The observed total-closure ratios are about `0.529` and `0.386`.

These trends are useful for theorem design, but they are not a summability proof. The next rigorous target is a goal-oriented dual-weighted estimate of the effect of the full-PDE tail residual on the signed C500 numerator.

Archive SHA-256: `ef2f7307ed4b15ea5d59b2f162f4fde9797bf3473c17c20642fd21aefaab7621`.

Drive file ID: `1xKM626lD-G8733trnJUZ7dx4QHGdgk_o`.
