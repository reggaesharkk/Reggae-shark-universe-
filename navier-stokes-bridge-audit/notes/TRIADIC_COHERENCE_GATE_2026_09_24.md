# Phase-sensitive triadic coherence gate (post-v0.2)

## Purpose

The retained-shell capacity audit shows that the last two retained shells do not determine the omitted nonlinear response. The next question is therefore whether a quantity that retains **relative Fourier phase information** exposes structure hidden by shell energies and other magnitude-only summaries.

This gate introduces an exact ordered-triad decomposition of the enstrophy-transfer term. For each interaction (k=p+q),

[
Z_{k,p,q}
=
-|k|^2
leftlangle
widehat u_k,,
P_k!left[i,(qcdot widehat u_p)widehat u_qight]
ightangle .
]

Then

[
T_N=operatorname{Re}sum_{k=p+q} Z_{k,p,q}.
]

Define the positive cubic envelope

[
A_N=sum_{k=p+q}|Z_{k,p,q}|
]

and, when (A_N>0),

[
chi_N=rac{T_N}{A_N}.
]

The triangle inequality gives the exact algebraic bound

[
|T_N|le A_N,qquad |chi_N|le1.
]

## Why this is different from a shell-energy statistic

(T_N) is cubic and sign-sensitive. A statistic depending only on modal magnitudes cannot in general encode the relative phases responsible for cancellation or reinforcement between triads. The ratio (chi_N) explicitly records that signed coherence.

For the existing sparse zero-modal-helicity family,

[
T(A,	heta)=4A^3sin	heta .
]

The script verifies that the cubic envelope is constant as the relative phase (	heta) changes at fixed amplitude, while the signed transfer and (chi) change with phase.

It also checks the structural transformations required of a stretching diagnostic:

- (umapsto-u): (T) and (chi) change sign, while (A_N) is unchanged.
- (umapsto 2u): both (T) and (A_N) scale by (2^3), while (chi) is unchanged.
- Fourier dilation (kmapsto3k): both (T) and (A_N) scale by (3^3), while (chi) is unchanged.

## What this does **not** establish

This is not a closure theorem. The envelope (A_N) is itself a cubic Fourier quantity. No cutoff-uniform estimate of (A_N) by energy, enstrophy, dissipation, or another time-integrable a priori quantity is proved here.

The value of this gate is narrower: it isolates an exact phase-sensitive coordinate for the nonlinear transfer and gives a clean target for the next falsification step. Any proposed closure based on triadic coherence must still produce a cutoff-uniform estimate strong enough to survive the continuum limit.

Reproduce with:

```bash
python src/triadic_coherence_gate.py
```
