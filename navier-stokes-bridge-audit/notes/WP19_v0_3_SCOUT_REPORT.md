# WP19 v0.3 — Consecutive-Cutoff Bridge Scouting Result

**Author:** Prince Upadhyay, Independent Research  
**Status:** computational scouting only; not a rigorous certificate.  
**Date:** 29 September 2026

## Result in one sentence

The first lower-cutoff-only bridge experiment works numerically in the right direction, and it identifies the dominant obstruction very clearly:

> **the crude Fourier-l1 strain majorant, not the newly opened-shell forcing, is currently destroying the rigorous cutoff-error bound.**

## Data used

This run used the already saved same-rational-datum predictor trajectories.

- N11 -> N12
- N12 -> N13
- nu = 0.1
- T = 0.003
- 120 steps, h = 0.000025
- same 112-pair rational witness
- no retuning

The higher-cutoff trajectories were used only after producing the lower-cutoff scouting bound, to measure how loose the bound is.

## Consecutive-cutoff forcing

The bridge quantity is

    h_N(t) = ||(Pi_(N+1)-Pi_N) B(u_N,u_N)||_2.

Node-sampled results:

| quantity | N11 -> N12 | N12 -> N13 |
|---|---:|---:|
| maximum sampled shell forcing | 369.376661535 | 253.062075988 |
| sampled integral h * sum H_j | 0.692499578 | 0.523924449 |
| actual predictor endpoint L2 difference | 0.544439983 | 0.435278880 |
| higher-cutoff endpoint new-shell L2 | 0.495507397 | 0.385041115 |

The sampled forcing integral falls from 0.692500 to 0.523924, a decrease of about 24.34%.

The actual endpoint cutoff difference also falls from 0.544440 to 0.435279, about 20.05% lower.

This is encouraging finite-cutoff behavior, but it is not an asymptotic theorem.

## Where the original bridge bound loses sharpness

The existing certificate's easy symmetric-strain majorant is essentially a Fourier-l1 bound.

Average sampled coefficient:

- N11: 1436.294
- N12: 1454.999

Over T=0.003 this produces total exponential amplification factors of roughly

- N11 -> N12: 74.36
- N12 -> N13: 78.65

and node-sampled bridge recurrences of

- N11 -> N12: 11.159885
- N12 -> N13: 8.730731

Those are about 20.5x and 20.1x the observed endpoint differences.

So the basic energy inequality is not the main problem. The global strain majorant is.

## Physical-space strain diagnostic

I then evaluated the symmetric strain on the natural dealiased physical grids and used the pointwise Frobenius norm as an operator-norm upper bound **at the sampled grid points**.

This is still not a continuum supremum certificate.

Average sampled physical-grid strain bound:

- N11: 324.395
- N12: 325.364

Maximum sampled values:

- N11: 332.031
- N12: 333.201

The corresponding accumulated amplifications collapse to only

- N11 -> N12: 2.646
- N12 -> N13: 2.654

and the same recurrence becomes

- N11 -> N12: **1.113713**
- N12 -> N13: **0.845564**

Compared with actual endpoint differences:

- N11 -> N12 actual: 0.544440
- N12 -> N13 actual: 0.435279

The gap is now only about 2.05x and 1.94x.

That is a major reduction from the ~20x gap produced by the Fourier-l1 strain majorant.

## Endpoint observable behavior

Floating-point evaluation of the same frozen K36 observable at the saved predictor endpoints gives approximately:

- N11: F(T) = -48.390539
- N12: F(T) = -72.015058
- N13: F(T) = -85.358994

The lower-cutoff endpoint embedded into the next cutoff gives exactly the same floating F before the new trajectory evolves, as expected under zero padding.

These floating values are diagnostics only. The certified endpoint intervals remain the authoritative sign statements.

## What this changes

The next rigorous task should **not** focus first on reducing the shell forcing.

The shell forcing already decreases from N11->12 to N12->13.

The target should be a rigorous whole-segment enclosure of

    ||S(v_N(t))||_(L-infinity, operator)

that is much closer to the actual physical-space strain than the global Fourier-l1 majorant.

A viable implementation path is:

1. express every spatial derivative of the cubic-Hermite path as a trigonometric polynomial with cubic time coefficients;
2. form the six independent symmetric-strain entries;
3. obtain a certified physical-space supremum using interval FFT / Bernstein subdivision / branch-and-bound boxes;
4. use a matrix-norm enclosure for the largest eigenvalue magnitude;
5. combine that segmentwise strain bound with the already proposed whole-segment new-shell forcing enclosure;
6. propagate the consecutive-cutoff recurrence with outward Arb arithmetic;
7. pass the terminal radius to the existing K36 endpoint and normalizer perturbation machinery.

## Current research interpretation

The first scouting result does **not** prove a cutoff bridge.

It does show something much more useful than a blind next run:

- the new-shell forcing is moderate and decreases across the two available transitions;
- the observed consecutive-cutoff state difference also decreases;
- the current proof loss is overwhelmingly caused by the crude strain exponent;
- a substantially sharper strain enclosure could plausibly move the bridge from a 20x-overestimate regime to roughly a 2x-overestimate regime before any further optimization.

That identifies the next mathematical bottleneck.
