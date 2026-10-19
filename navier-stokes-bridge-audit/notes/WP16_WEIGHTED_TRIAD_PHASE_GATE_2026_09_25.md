# WP16 Coefficient-Weighted Triad-Phase Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** prospective structural audit following the N=10/N=11 phase reverse-engineering gate.

## Target

The previous diagnostic found that individual optimized mode phases are nearly one-point-uniform and that unweighted relative triad phases

[
Theta_{kpq}=phi_p+phi_q-phi_k
]

are also nearly uniform. At the same time, the inherited N=10 phase core persists strongly into N=11.

The natural next question is therefore not whether all triads phase-lock equally. It is:

> Do the optimized relative phases preferentially align the triads carrying the largest nonlinear coefficients?

For every ordered high-advector interaction (p+q=k), write the base-state H2 contribution as

[
z_{kpq}^{(0)}.
]

Under the phase-only perturbation,

[
z_{kpq}
=
z_{kpq}^{(0)}
e^{i(phi_p+phi_q-phi_k)}.
]

The script reconstructs this identity directly and checks that

[
sumRe z_{kpq}=N_2^{>2}
]

and

[
sum|z_{kpq}^{(0)}|=A_2^{>2}
]

match the stored finite-search observables.

## Primary diagnostics

For (alpha_{kpq}=arg z_{kpq}^{(0)}+Theta_{kpq}), record:

[
chi
=
rac{sum |z_{kpq}^{(0)}|cosalpha_{kpq}}
{sum |z_{kpq}^{(0)}|},
]

together with:

- coefficient-weighted resultant of (Theta_{kpq});
- coefficient-weighted resultant of (alpha_{kpq});
- positive aligned-weight fraction;
- the same quantities by advector shell;
- old-only triads versus triads touching the newly opened shell;
- triads whose advector itself lies in the newly opened shell.

## Why this matters

A nearly uniform *unweighted* phase distribution is compatible with a strongly non-random nonlinear transfer if the optimizer aligns only the high-weight interactions.

If the N=11 gain is concentrated in a small class of shell-localized, high-weight relative phases, that class becomes the candidate for an explicit recursive construction.

If no such concentration exists, the mechanism is genuinely collective and the analytical strategy must change again.

## Scope boundary

This is an exact decomposition of a finite Galerkin state. Even a strong weighted-alignment pattern does not establish asymptotic growth or a Navier–Stokes singularity/regularity theorem.
