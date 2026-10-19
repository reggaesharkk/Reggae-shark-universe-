# WP16 Phase-Path Block Decomposition Result — Factorized Recursive Mechanism

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed finite N=11 mechanism audit on the verified continuation.  
**Source artifact:** `wp16_phase_path_block_decomposition_results.json`  
**Bytes:** 21,794  
**SHA-256:** `672a10e468fee00f26a08f044812f9f1bf519865edc608bf0fb0ac42f35f68c9`

## Question

The previous gates established that:

1. the new cutoff shell does not disproportionately carry signed H2 transfer;
2. the quotient increase is accompanied by broad depletion of
   [
   P_+=langle(omegacdot Somega)_+angle;
   ]
3. the inherited phase core is stable from N=10 to N=11.

This gate asks whether the N=11 improvement decomposes into separate functions of:

- the small corrections on the 2,084 inherited phase pairs;
- the large phases assigned to the 703 newly activated phase pairs.

## Phase displacement scales

The wrapped displacement magnitudes are sharply separated:

[
operatorname{mean}|Deltaphi|_{m old}
=
0.14326;	ext{rad},
]

[
operatorname{median}|Deltaphi|_{m old}
=
0.07694;	ext{rad},
]

while

[
operatorname{mean}|Deltaphi|_{m new}
=
1.53823;	ext{rad},
]

[
operatorname{median}|Deltaphi|_{m new}
=
1.52775;	ext{rad}.
]

Thus the recursive step consists of small inherited-core adjustments plus order-one phases on the newly opened shell.

## Refined endpoint decomposition

All endpoint values below are refined at (96^3).

### Inherited state

[
C_{m inh}=6.7874845947,
]

[
N_{m inh}=2.0308658870	imes10^7,
]

[
P_{+,m inh}=266002.7690.
]

### Old-core corrections only

Applying only the 2,084 inherited-core corrections gives

[
C_{m old}=7.3763815693,
]

an increase of

[
oxed{+8.6762%}.
]

Its mechanism is strongly denominator-weighted:

[
N: +2.2451%,
]

[
P_+: -5.9177%.
]

So small old-core phase corrections primarily act by depleting positive stretching while preserving and slightly improving the numerator.

### New-shell phases only

Applying only the 703 newly opened-shell phases gives

[
C_{m new}=7.3868613603,
]

an increase of

[
oxed{+8.8306%}.
]

Its mechanism is strongly numerator-weighted:

[
N: +7.9850%,
]

[
P_+: -0.7770%.
]

So the new shell primarily restores/increases signed high-frequency transfer while barely changing positive stretching.

### Full optimized state

Applying both blocks gives

[
C_{m full}=8.0348857964,
]

an increase of

[
oxed{+18.3780%}.
]

The combined changes are

[
N: +10.9762%,
]

[
P_+: -6.2526%.
]

## Near-factorization

The log-gain decomposition is

[
g_{m old}=0.0832028,
]

[
g_{m new}=0.0846225,
]

[
g_{m full}=0.1687124.
]

Therefore the interaction term

[
I
=
g_{m full}-g_{m old}-g_{m new}
=
0.0008871.
]

On the multiplicative scale this corresponds to only about

[
oxed{0.0887%}
]

extra interaction beyond the product of the old-core and new-shell gains.

Thus, on this finite N=11 state, the mechanism is almost multiplicatively separable.

## Phase-path behavior

### Old-core path

Along

[
phi(lambda)=phi_{m inh}+lambdaDeltaphi_{m old},
]

the quotient rises monotonically from

[
6.78767
]

to

[
7.37632.
]

Across the path, (P_+) decreases monotonically while the numerator increases modestly.

This is a clean denominator-relaxation direction.

### New-shell path

Along the new-shell-only path, the quotient rises from

[
6.78767
]

to a maximum near

[
7.39241
]

at (lambda=0.9), then decreases slightly to

[
7.38856
]

at (lambda=1).

The numerator rises strongly through most of the path, while (P_+) changes only weakly.

This is a clean numerator-building direction with a shallow overshoot near the registered endpoint.

### Full path

The full path rises monotonically from

[
6.78767
]

to

[
8.03476
]

on the (48^3) path grid, while (P_+) decreases monotonically.

The final refined (96^3) endpoint is

[
8.0348857964.
]

## Mechanistic interpretation

This is the first gate in the phase-only continuation sequence to yield a simple recursive decomposition:

[
oxed{
	ext{new shell} Rightarrow 	ext{numerator gain}
}
]

and

[
oxed{
	ext{small inherited-core correction} Rightarrow 	ext{denominator depletion}.
}
]

The two gains combine almost independently.

This explains several earlier observations simultaneously:

- the inherited phase core remains stable;
- newly opened phases are order-one;
- the newest shell need not dominate total transfer;
- old shell-4/5 interactions remain the transfer backbone;
- the quotient can still grow because old-core micro-adjustments lower (P_+).

## Candidate recursive construction template

A prospective analytical construction should now be organized recursively.

Given a phase state at cutoff (N):

1. embed it into cutoff (N+1);
2. assign order-one phases to newly activated modes to recover/increase (N_2^{>2});
3. apply small corrections to inherited phases to lower (P_+);
4. keep the two operations separated enough to estimate their gains independently.

The numerical target is no longer merely to maximize (C_N). It is to identify explicit rules

[
Deltaphi_{m new}(N)
]

and

[
deltaphi_{m old}(N)
]

for which one can derive lower bounds on numerator gain and denominator reduction.

## Next analytical gate

The next useful finite experiment is a **compressed block-gradient audit**.

Instead of perturbing thousands of phases individually, project the old-core phase correction onto structured mode classes:

- shell index;
- parity/sign classes;
- octants;
- shell-4/5 interaction participation;
- triad-degree/interaction-weight classes.

For each class, measure its first-order effect on

[
log N_2^{>2},
qquad
-log P_+,
qquad
log C.
]

The goal is to determine whether the 2,084-dimensional old-core correction can be approximated by a much lower-dimensional sign or shell rule without losing most of the (5.9%) denominator depletion.

A successful compression would be the clearest route yet toward an explicit recursive analytical construction.

## Scope boundary

This factorization is an observed finite N=11 property of the registered continuation. It does not prove that the same decomposition persists for all cutoffs, does not prove (C_N	oinfty), and does not establish Navier–Stokes blowup or global regularity.
