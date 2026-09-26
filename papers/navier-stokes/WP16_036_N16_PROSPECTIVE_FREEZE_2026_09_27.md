# WP16 prospective N16 continuation and K36 time gate — frozen 2026-09-27

Prince Upadhyay, Independent Research

**Freeze boundary:** This protocol and its code are committed after the completed N15 prospective test and before any N16 state, score, checkpoint, or time-gate result is generated. No N16 proposal is evaluated until the protocol commit is merged. N15 is discovery/replication history for this freeze; N16 is the next untouched cutoff.

## Immutable inputs and reconstruction

- N15 completed continuation SHA-256: `c0bd97f554df3e8561d75e1ba62356d04200fbe4986f573e3305a98932ccb225`.
- Frozen N11-derived K36 source decomposition JSON SHA-256: `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`.
- Viscosity `nu=0.1`, predecessor amplitude and anchor-time semantics, exactly the existing finite Fourier-Galerkin ODE.
- Active support uses the existing `active_pairs` threshold and `base_state` reconstruction. Inherit phases on matching conjugate support vectors; use zero phase for newly available vectors. The three time-gate states are `inherited`, `target_only`, and `full_final` using the existing ordered-orbit target mask.
- The N11-derived 36 source-orbit keys, their ranking origin, and the original same-sign and signed-share definitions are unchanged. No retuning of K36.

The runner rejects a predecessor or K36 source whose bytes fail these hashes. A cutoff-dependent active threshold can drop some old pairs; inherited count means the exact intersection of active supports, rather than necessarily all predecessor pairs.

## Frozen phase continuation

- Cutoff N=16, deterministic seed `20260941`, following N14 `20260939` and N15 `20260940`.
- Unchanged objective `C_infinity_stretch` calculated by the bounded high-triad source table and chunked exact transfer with physical-space positive stretching.
- Search grid **64**. The objective's cubic spatial average requires `grid > 3N`; 48 equals `3*16` and is invalid. Grid 64 is the smallest already exercised and supported refinement grid above 48 in the N15 protocol. It changes quadrature resolution, not the objective or proposal law.
- Same schedule: 16 new-mode global draws, three new-mode block rounds, four full-support block rounds, 72 trials per round, block size 40, initial Gaussian step 0.30, multiplier 0.6, total **520 proposals**. Accept a proposal only on strictly larger search-grid objective.
- Evaluate the selected fixed phase vector at grids `64, 96, 128`; never use 48 or retune during refinement.
- Atomically save the PCG64 state, phase vector, score, records, trial number, support counts, code/input fingerprints, and elapsed time after each completed proposal. Reject incompatible checkpoints. The bounded-memory implementation and default chunk of 100,000 sources are unchanged.
- First run `01_N16_SMOKE.cmd`: construct N16 and score only the baseline and inherited states, save trial-0 checkpoint, stop. No proposal may be evaluated until after the freeze commit is merged. The smoke itself runs only after merge, as requested for the Windows machine.

## Frozen time gate

After all 520 proposals and fixed-phase refinement, run the same three reconstructions and exact dealiased Galerkin trajectory evaluator. Use `dt=0.0001`, 30 steps through `t=0.0030`, and `nu=0.1`. At every sample record the original absolute grouped mass fraction, signed share, same-sign boolean, margin `F=I-9O`, energy, reality/divergence errors. Record initial and first mass-exit local margin rates: full, nonlinear, viscous, radial magnitude, scalar phase, and vector polarization.

The unchanged preregistered criteria are same sign, absolute mass fraction at least 0.90, and signed share in [0.8, 1.2]. If a normalization denominator vanishes, the normalized channel is undefined and that state's gate stops; it cannot be counted as passing. Repeat the exit bracket with half-step `dt=0.00005`.

## Predeclared tests and failure handling

For each of the three states:

1. Static sample at t=0 passes all original K36 criteria.
2. Every sample through t=0.0010 passes mass; first sampled mass exit is within [0.0015, 0.0030]; same-sign and signed-share tests still pass at that exit.
3. The local full margin rate is initially positive. At first mass exit the full, radial-magnitude, and vector-polarization margin rates are negative.

Joint pass requires every item for all three states. No mass exit by t=0.0030 leaves exit-dependent items untested, not passed. Preserve every failure and the full trace; do not retune keys, thresholds, schedule, or the exit window after viewing N16. The prior N14/N15 exit at sampled time 0.0023 is a comparison datum, not a new exact-time pass criterion.

## Interpretation

N16 is one prospective finite-Galerkin replication. Neither a pass nor a failure establishes an all-N theorem, continuum convergence, global phase optimality, or regularity/blowup for the Navier–Stokes PDE. A later analytic turnover study may use N14/N15 as discovery data, with any new rule separately frozen before an untouched holdout.
