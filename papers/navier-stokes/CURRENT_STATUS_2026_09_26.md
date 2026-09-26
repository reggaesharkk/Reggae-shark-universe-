# Navier–Stokes Bridge Audit — Current Status

**Prince Upadhyay, Independent Research**  
**Updated:** 26 September 2026

Canonical specialist repository: https://github.com/reggaesharkk/navier-stokes-bridge-audit

## Prospectively frozen N12 holdout

The ordered K36 source-orbit coalition and descriptive three-state pass criteria were fixed in [PR #73](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/73) before N12 generation. The new finite N12 continuation was then evaluated without changing the coalition or thresholds. [The full result](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/9caa90e3defb5e64efbe132a45623a24902b3ba0/notes/WP16_036_N12_FROZEN_K36_HOLDOUT_RESULT_2026_09_26.md) and [raw files with checksums](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/9caa90e3defb5e64efbe132a45623a24902b3ba0/results/wp16_n12_holdout/) are in the specialist repository; [the result note is mirrored here](WP16_036_N12_FROZEN_K36_HOLDOUT_2026_09_26.md).

| N12 state | Absolute source mass captured | K36 signed / full signed | Same sign | Predeclared gate |
|---|---:|---:|---|---|
| Inherited | 94.0485% | 1.014401 | Yes | Pass |
| Target only | 94.0487% | 1.014404 | Yes | Pass |
| Full final | 93.5198% | 1.031871 | Yes | Pass |

The required absolute mass fraction was at least 90%, and the signed share had to lie in [0.80, 1.20], with the same sign as the full channel, at each state. All 36 frozen keys were present in each state. Stored ratios, flags, and checkpoint/final-row consistency were checked; this is not a separate independent solver run.

The fixed-phase, grid-96 refined quotient at N12 is **8.692984814467122**. The prior refined values are N7 3.744126696758515, N8 4.656046627246442, N9 6.261042251605425, N10 7.159655718793216, and N11 8.034885796422683. Each value is from a finite optimized state at its cutoff. Their increase does not prove growth at every cutoff or in the limit.

## Scope

This is one successful out-of-sample **finite-cutoff** transfer test of a coalition selected at N11. It does not establish an all-N phase law, a cutoff-uniform estimate, a continuum result, finite-time blowup, or arbitrary-data global regularity. The historical [25 September status](CURRENT_STATUS_2026_09_25.md) remains available unchanged.
