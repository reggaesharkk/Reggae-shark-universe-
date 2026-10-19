# WP16 Cross-Cutoff Orbit/Rank Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** prospective LRSC-style structural audit.

The N=11 shell-7/shell-4 compression found that six sorted absolute-coordinate orbit families using only 84 of 314 phase pairs recover about 99.66% of the target quotient gain. The leading orbit is ([0,3,6]).

This gate tests whether that structure persists one cutoff earlier.

## Cross-cutoff reconstruction

Use the verified continuation states

[
N=9	o10
]

and

[
N=10	o11.
]

For each step, reconstruct the inherited phase field and the registered wrapped old-core correction.

Partition inherited modes by

[
mathcal O(k)=operatorname{sort}(|k_1|,|k_2|,|k_3|).
]

## Orbit response

For each orbit (mathcal O), apply a small fraction

[
arepsilon=0.1
]

of that orbit's registered old-core correction and estimate

[
rac{d}{dlambda}log N_2^{>2},
qquad
-rac{d}{dlambda}log P_+,
qquad
rac{d}{dlambda}log C.
]

The audit explicitly tracks the six N=11-dominant orbit families:

[
[0,3,6],;
[0,2,3],;
[1,4,5],;
[0,1,3],;
[0,1,6],;
[1,1,3].
]

## LRSC-style response rank

For every orbit shared by N=10 and N=11, construct a six-coordinate response vector

[
r_{mathcal O}
=
(
dlog N_{10},
-dlog P_{+,10},
dlog C_{10},
dlog N_{11},
-dlog P_{+,11},
dlog C_{11}
).
]

Stack these vectors into the orbit-response matrix and compute:

- raw singular values;
- column-standardized singular values;
- cumulative singular-value energy;
- numerical rank required to explain 99% of response energy.

A sharp singular spectrum would indicate that many geometric orbit responses are controlled by only a few effective directions.

## Decision value

Two outcomes matter.

**Persistence:** the same dominant orbit families have positive (dlog C) at both cutoffs.

**Low effective rank:** the shared orbit-response matrix has only a few dominant singular directions.

If both occur, the next analytical target becomes a small orbit-generator model rather than thousands of phase variables.

## Inputs

This gate needs both continuation artifacts:

- the earlier N=8/N=9 escalation JSON;
- the resumed N=10/N=11 escalation JSON.

## Scope boundary

This is a finite two-step diagnostic. It does not establish persistence for arbitrary cutoff, an asymptotic orbit law, divergence of the quotient, singularity formation, or global regularity.
