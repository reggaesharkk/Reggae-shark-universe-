# WP16 N17 K36 mechanism prefreeze — 27 September 2026

Prince Upadhyay, Independent Research

## Status and discovery boundary

This is a **mechanism prefreeze**, written after inspecting the N12/N13
source-rate audit and N16 fixed-time attribution and before any N17 state,
score, checkpoint, or trajectory is generated. All N12–N16 observations are
discovery data for this new mechanism. This file and
`src/wp16_036_N17_mechanism_gate.py` must be committed before N17 data exist.
The N17 continuation runner, seed, schedule, grid, and full time-gate must
also be frozen in a separate commit **before** any N17 generation. This
prefreeze alone is not permission to generate N17 data or a complete N17
scientific protocol. Do not call N17 an untouched mechanism holdout if any
N17 state or score was inspected before both freezes.

The N11-derived K36 keys are unchanged. No source identity, threshold,
sampling time, or pass condition may be retuned using N17. Preserve every
failure and undefined observable. The prior N14–N16 prospective results and
post-hoc analyses remain historical records.

## Frozen input and observables

- N16 predecessor continuation SHA-256:
  `53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca`.
- Compact frozen K36 keys SHA-256:
  `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`.
  Their original N11 source SHA-256 is
  `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`.
- The N17 continuation SHA-256 is unknown by design and must be recorded
  upon first evaluation. Reconstruct `inherited`, `target_only`, and
  `full_final` through the existing `hold.reconstruct` semantics and exact
  dealiased finite Galerkin RHS with viscosity 0.1.
- At each state and time, use the tracked k-channel P=(3,2,2), Q=(3,-2,1),
  K=(6,0,3). For an ordered source-orbit group `j`, let its complex
  numerator be `w_j` and the tracked complex normalizer be `z`. Its signed
  contribution is `g_j=Im(w_j/z)`. Set `I=sum_{j in K36}|g_j|`,
  `O=sum_{j outside K36}|g_j|`, `F=I-9O`.
- The recurrent outside orbit is **exactly**
  `j*=([3,3,4],[0,2,3])`; order matters. Do not replace this key with a
  radial shell or a newly selected top-ranked group.

## Predetermined sampling and numerical checks

Use RK4 with `dt=0.0001`. At `t=0` and `t=0.0010`, evaluate all three
states. At `t=0.0023`, compare `full_final` and `inherited` at the same time.
For a directional rate at a fixed state `a`, evaluate each group at
`a ± h RHS(a)` with `h=5e-9, 1e-8, 2e-8`; use `h=1e-8` for the reported
decision. Require the spread of both `F'` and the recurrent group absolute
mass rate across those three `h` values to be at most `0.001` in each
state/time. An undefined tracked normalizer, missing recurrent orbit,
reconstruction failure, or unstable derivative is a failure, not a pass.

Where `g_j` is nonzero, report the exact local split

`d|g_j|/dt = sign(g_j) Im(w'_j/z) + sign(g_j) Im(-w_j z'/z^2)`.

Compute `w'_j,z'` by central directional differences along the RHS and
check that the two terms sum to the directly differenced absolute rate
within `0.001`. At `g_j=0` the absolute-value derivative may have a kink;
report the central diagnostic but leave the split undefined. An undefined
split for the recurrent orbit fails its mechanism test. The split identifies
numerator and normalizer contributions algebraically; neither term alone is
an independently evolving physical process.

## Prospective predictions and failure rules

The following must hold for **each** of the three N17 states:

1. The original static K36 test passes at `t=0`: same sign, absolute mass
   fraction at least 0.90, signed share in `[0.8,1.2]`.
2. The recurrent orbit's absolute-mass rate is strictly negative at `t=0`.
3. At `t=0.0010` it is strictly positive and is the unique largest positive
   outside-K36 ordered-group rate. Also `I'>0`, `O'>0`, and `F'<0`.

At `t=0.0023`, compare `full_final` minus `inherited` at that same sample.
The orbit must have a strictly negative outside absolute-mass difference and
be the single largest outside-group decrease. Decompose the total outside
difference into complex numerator and normalizer changes using the symmetric
two-order swap already defined in `src/wp16_036_N16_group_attribution.py`.
The normalizer swap must be negative and have strictly greater absolute
magnitude than the numerator swap. Ties fail. The comparison is a state
difference and must never be reported as a time derivative or a causal
intervention.

The machine result reports each component and every failed condition.
Joint pass requires all predictions and numerical checks; otherwise the
result is a failure or unevaluable with the reason retained. The numerator
and normalizer *time-rate split* is predeclared as a diagnostic: its signs
are not a pass condition because N16 state-difference data do not establish
their time-rate signs. No retrospective promotion of a favorable sign is
allowed.

## Interpretation boundary

Even a joint pass would be one finite N17 holdout of a mechanism pattern,
not a cutoff-uniform invariant, a continuum-limit estimate, or a
Navier–Stokes regularity result. A failure identifies which proposed
source-level prediction failed without changing K36 or this protocol.
