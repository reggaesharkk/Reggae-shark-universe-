# WP16 [0,3,6] Resonance-Mechanism Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** prospective finite mechanism audit.

The targeted family scan rejected a smooth strong ([0,3,m]) law while finding that

[
[0,3,6]
]

remains positive across all three tested recursive steps. This gate asks why that orbit is exceptional.

## Target and controls

Primary target:

[
[0,3,6].
]

Controls:

[
[0,2,4],qquad
[0,4,8],qquad
[0,3,5],qquad
[0,3,7].
]

The first two preserve a 1:2 coordinate ratio and test whether the effect is a generic scaled geometry. The latter two are immediate neighbors in the same ([0,3,m]) family.

## Steps

Use existing continuation states only:

[
N8	o N9,qquad
N9	o N10,qquad
N10	o N11.
]

No new phase optimization is performed.

## Measurements

For each available orbit:

1. reconstruct the inherited state and registered old-core phase displacement;
2. measure directional and endpoint changes in
   [
   N_2^{>2},quad P_+,quad C;
   ]
3. use the existing exact finite-Galerkin H² high-advector triad decomposition;
4. measure the fraction of total coefficient envelope (A) in triads touching the target orbit;
5. measure signed-transfer share before the target update;
6. measure signed-transfer change caused by the target orbit update;
7. split triad participation by the target orbit appearing as advector, advected mode, or output mode.

## Decision logic

A candidate resonance-style explanation becomes more plausible if ([0,3,6]):

- touches an unusually large or unusually coherent weighted triad set;
- changes signed numerator transfer much more strongly than neighboring controls;
- shows a stable role pattern across cutoffs.

A denominator-dominant explanation is favored if its (C) gain is large while direct triadic numerator change is weak and (-dlog P_+) carries most of the response.

A generic scaled-geometry explanation is weakened if ([0,2,4]) and ([0,4,8]) do not reproduce the effect.

## Scope boundary

This is a finite Galerkin mechanism diagnostic. The term “resonance” is a hypothesis label only; the gate does not establish a resonance theorem, an all-cutoff invariant, singularity formation, or global regularity.
