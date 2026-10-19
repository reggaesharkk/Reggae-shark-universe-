# WP16 Phase-Structure Reverse-Engineering Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed structural diagnostic on the verified N=10/N=11 continuation.  
**Goal:** decide what object should be reverse-engineered before attempting an analytic phase-only construction.  
**Not claimed:** no analytic phase law, no asymptotic theorem, no global optimizer, no Navier–Stokes regularity result.

## 1. Why raw mode phases are not the right final object

The continuation applies conjugacy-preserving Fourier multipliers

[
a_kmapsto e^{iphi_k}a_k,qquad
phi_{-k}=-phi_k.
]

A spatial translation changes these phases by

[
phi_kmapstophi_k+kcdot x_0
]

without changing any translation-invariant objective used here.

Therefore a visually simple pattern in the raw (phi_k) is neither necessary nor gauge invariant.

For a triad (p+q=k), however,

[
Theta_{kpq}=phi_p+phi_q-phi_k
]

is invariant under that translation gauge. This is the natural phase variable entering the transformed quadratic interaction.

## 2. The inherited core is stable

The N=10 optimizer contains 2,084 active conjugate pairs. All 2,084 are inherited into the N=11 support.

After aligning the N=10/N=11 phase difference by the best small spatial-translation gauge, the residual has:

- circular resultant: **0.974137**
- mean absolute residual: **0.1450 rad**
- median absolute residual: **0.0764 rad**
- 90th percentile: **0.3922 rad**
- fraction below 0.25 rad: **79.08%**
- fraction below 0.50 rad: **94.58%**

Thus the N=11 optimizer does not replace the old phase organization wholesale. It keeps most of the inherited phase field close and extends/relaxes it.

This is the clearest evidence so far for a **recursive phase construction** rather than unrelated independent optima at each cutoff.

## 3. But the one-point phase distribution is almost incoherent

For the optimized positive-half phase vectors,

[
left|rac1Msum_k e^{iphi_k}ight|
]

is only

[
0.02296quad(N=10),
qquad
0.01191quad(N=11).
]

So the useful structure is not global locking of the individual mode phases.

A simple shell/radial "all phases point roughly together" picture is therefore rejected by the actual optimizer.

## 4. Unweighted triad phases are also almost uniform

A deterministic sample of 250,000 admissible mode pairs was used to form the gauge-invariant relative phase

[
Theta_{kpq}=phi_p+phi_q-phi_k.
]

The first circular resultants are

[
R_1approx0.00512quad(N=10),
]

[
R_1approx0.00163quad(N=11).
]

The second harmonics are also close to zero.

Therefore there is no evidence that **all triads equally weighted** are phase locked.

This is not a negative result for the mechanism. The nonlinear transfer does not weight all triads equally. Each interaction carries a complex coefficient determined by modal amplitudes, polarizations, Leray projection, derivative factors and the (H^2) weight.

The next quantity must therefore be the relative phase measured **against that complex triad coefficient**.

## 5. Optimization decomposes into two mechanisms

At N=10:

[
5.957745
	o
6.558836
	o
7.159723.
]

The first arrow comes from optimizing newly opened modes. During the final full-torus relaxation, the quotient gains another **9.16%** even though the signed high transfer falls by **6.16%**, because the positive-stretching denominator falls by **14.03%**.

That is a clean denominator-depletion step.

At N=11:

[
6.787949
	o
7.391223
	o
8.034575.
]

The full-torus stage gains **8.70%**, with signed high transfer increasing **2.69%** while the positive-stretching denominator falls **5.53%**.

So the recursive adversary has two distinguishable jobs:

1. use newly opened high-frequency phases to recover/increase favorable signed transfer;
2. slightly relax the inherited core to reduce positive stretching without sacrificing too much numerator.

This is consistent with the earlier satellite first-variation result, where an improving direction initially acted through denominator depletion.

## 6. Next analytical target

The next gate should reconstruct the base evolved Fourier state and, for every high-advector ordered triad, write its contribution as

[
z_{kpq}^{(0)}e^{iTheta_{kpq}},
]

where (z_{kpq}^{(0)}) is the complex base coefficient before the phase-only multiplier.

The key diagnostics are then:

[
alpha_{kpq}
=
arg z_{kpq}^{(0)}+Theta_{kpq},
]

the contribution weight (|z_{kpq}^{(0)}|), and the weighted alignment

[
rac{sum |z_{kpq}^{(0)}|cosalpha_{kpq}}
{sum |z_{kpq}^{(0)}|}.
]

Unlike raw (phi_k) or unweighted (Theta_{kpq}), this quantity is directly tied to the signed (H^2) transfer.

The corresponding physical-space side should track which small inherited phase corrections reduce

[
P=langle(omegacdot Somega)_+angle.
]

The desired constructive picture is therefore a **recursive weighted-triad extension plus denominator-relaxation rule**, not a low-degree formula for individual mode phases.

## 7. Scope barrier

The present gate identifies the representation in which a constructive law should be sought. It does not yet provide that law.

The observed N=10 to N=11 persistence is one continuation step. The N=7–11 increasing quotient sequence remains finite numerical evidence, not proof of asymptotic divergence.
