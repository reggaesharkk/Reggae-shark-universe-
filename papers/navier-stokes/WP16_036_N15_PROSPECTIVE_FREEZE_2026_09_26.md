# WP16 prospective N15 continuation and K36 time gate — frozen 2026-09-26

Prince Upadhyay, Independent Research

**Freeze boundary:** this protocol is written after the completed N14 prospective result and before any N15 state, N15 score, N15 checkpoint, or N15 time-gate output exists. No N15 scientific data may be generated before this note and the corresponding implementation are merged.

## Purpose

N15 is a new untouched finite-cutoff replication. The protocol deliberately keeps the N14 hypotheses broad and unchanged rather than narrowing them around the observed N14 exit at 0.0023.

The N11-derived K36 coalition, same-sign requirement, 90% grouped absolute-mass threshold, signed-share interval [0.80,1.20], viscosity, anchor semantics, reconstruction semantics, objective, time window, and local-rate sign tests remain unchanged.

## Frozen inputs

- previous continuation: N14 SHA-256 `747dfb0bd0ea12271bd53b39fae7a4e18f396656bed3084bd4c632a9f3e5a3d9`
- frozen source decomposition JSON SHA-256 `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`
- K36: exactly the same N11-derived 36 ordered source-orbit keys already frozen before N12
- `nu=0.1`
- existing amplitude and anchor-time semantics
- exact finite Galerkin ODE and dealiased trajectory solver

If the N14 input hash differs, the continuation must stop rather than silently accepting a modified predecessor.

## Frozen N15 continuation schedule

Use the N14 winning phase vector as the inherited predecessor on the N15 support. New N15-only modes begin with phase zero before proposals.

- cutoff: N=15
- deterministic seed: `20260940`
- search grid: 48
- alias-free condition: `48 > 3*15 = 45`
- objective: unchanged `C_infinity_stretch`
- new-mode global draws: 16
- new-mode block rounds: 3
- full-support block rounds: 4
- trials per block round: 72
- block size: 40
- initial Gaussian phase step: 0.30
- round step multiplier: 0.6
- total proposals: 520
- refinement grids after the frozen winner is selected: 48, 64, 96, 128
- no phase retuning during refinement

The bounded high-triad table and chunked exact objective remain the required evaluator. The candidate proposal schedule and acceptance rule are unchanged from N14.

## Checkpoint and memory rules

The runner must atomically checkpoint every completed proposal with N, seed, search grid, input/code fingerprints, PCG64 RNG state, last completed trial, best phases, best score, accepted-improvement records, and elapsed time.

Before the 520-proposal run, execute a trial-0 smoke that constructs the N15 source table and scores baseline/inherited states without evaluating any proposal. On the user's 16 GB Windows machine, abort before search proposals if estimated or observed peak resident memory exceeds 12 GiB. An interruption after search begins must resume from the durable atomic checkpoint; do not restart with a different seed or altered schedule.

## Frozen N15 time-resolved gate

After and only after the N15 continuation completes, construct the same three states using the existing reconstruction semantics:

- inherited
- target_only
- full_final

For each state:

- integrate with `dt=0.0001`
- sample every step through `t=0.0030`
- retain the same frozen K36 keys
- record absolute-mass fraction, signed share, same-sign criterion, K36 margin `F=I-9O`, energy, reality error, divergence error
- record local full/nonlinear/viscous/radial-magnitude/scalar-phase/vector-polarization margin velocities at t=0 and at the first sampled mass exit
- if the tracked normalization denominator vanishes, record the normalized channel as undefined and stop that state's gate instead of dividing by zero
- repeat the first coarse mass-exit bracket with half-step `dt=0.00005`

## Predeclared N15 tests

Report every state, including failures. Do not retune any key or threshold after viewing N15.

1. **Static transfer:** all three N15 initial states meet the original K36 criteria: same sign, absolute-mass fraction >= 0.90, signed share in [0.80,1.20].
2. **Transient time pattern:** for each state, every sampled point through t=0.0010 passes the mass criterion; the first sampled mass exit lies in [0.0015,0.0030]; and the signed criterion still passes at that mass exit.
3. **Local velocity pattern:** dF/dt is positive initially; at the first sampled mass exit dF/dt is negative and both radial-magnitude and vector-polarization margin rates are negative. If no mass exit occurs by t=0.0030, the exit-sign part is untested, not silently counted as false or true.

The joint N15 outcome is a pass only if all three tests pass for all three states.

## Interpretation boundary

A positive N15 result would extend the prospective finite-cutoff replication by one more untouched cutoff. A negative N15 result is retained without retuning and would falsify the corresponding N15 replication claim. Neither outcome proves or disproves global Navier-Stokes regularity, establishes an all-N theorem, certifies a continuum limit, or certifies a global optimum of the phase search.
