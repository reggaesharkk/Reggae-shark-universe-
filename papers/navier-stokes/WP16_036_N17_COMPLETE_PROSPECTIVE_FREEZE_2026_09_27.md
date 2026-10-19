# WP16 N17 continuation and K36 gates — complete pre-data freeze

Prince Upadhyay, Independent Research — 27 September 2026

## Activation and provenance

This completes the N17 execution freeze following the separately committed
[source and normalizer mechanism prefreeze](WP16_036_N17_MECHANISM_PREFREEZE_2026_09_27.md).
The N12–N16 source-rate and attribution observations are discovery data for
that new prediction. **No N17 state, score, checkpoint, or trajectory may be
generated until this note, the runner, gates, and launchers are merged.** A
trial-0 smoke is permitted only after merge. If N17 data existed before both
freezes, report it as post-hoc and do not call it an untouched holdout.

The predecessor is the completed N16 continuation with SHA-256
`53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca`.
The original N11-derived K36 source JSON has SHA-256
`193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`.
The compact K36 keys used by the mechanism evaluator have SHA-256
`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`.
Reject mismatched bytes. The N17 output hash is unknown and must be recorded
after execution. Preserve the N16 file and all N17 failures.

## Phase continuation

- Cutoff `N=17`, seed `20260942`, continuing the N14–N16 sequence.
- Viscosity `nu=0.1`; inherited amplitude and anchor time, active-pair
  threshold, conjugate reality, zero phase for newly active pairs, and
  inherited phases on common support follow the N16 reconstruction.
- Same `C_infinity_stretch` objective, bounded high-triad table, chunked
  exact transfer, and physical positive-stretch average. Search grid **64**:
  the cubic spatial average requires `grid > 3N`, and `64 > 51`. No N17
  score was used to choose this grid. Fixed-winner refinement grids are
  `64,96,128`; refinement does not re-optimize phases.
- Exactly 16 new-mode global draws; three new-mode block rounds and four
  full-support block rounds, 72 trials each: **520 proposals** total. Block
  size 40; initial Gaussian phase step 0.30, multiplied by 0.6 each round.
  Accept only a strictly higher search-grid objective.
- Atomic checkpoint after baseline/inherited trial 0 and each completed
  proposal. Store PCG64 state, phases, score, schedule records, support counts,
  elapsed time, and input/code fingerprints; refuse incompatible resume.
  Default source chunk is 100,000. The full launcher requires a trial-0
  checkpoint. Trial-0 scores only baseline and inherited, no proposal.

The N16 predecessor continuation JSON is an external local input to the
Windows overlay; it is not included in the Git repository or this freeze.
The user retains its original bytes in the standalone WP16 runner's
`results/wp16_n16_holdout/` folder. No file may be fabricated to satisfy
the predecessor hash.

## Time-resolved broad gate

After 520 proposals and refinement, reconstruct `inherited`, `target_only`,
and `full_final` with the existing ordered-orbit target mask. Use the exact
dealiased finite Galerkin RHS, RK4 `dt=0.0001`, 30 steps through `t=0.0030`,
and `nu=0.1`. Record the same sign, K36 absolute mass fraction, signed share,
margin `F=I-9O`, energy, reality/divergence errors at every sample. Compute
the initial and first mass-exit local margin rates (full, nonlinear, viscous,
radial magnitude, scalar phase, vector polarization), and repeat the exit
bracket with `dt=0.00005`.

For all three states, the same frozen broad predictions apply: static same
sign, mass fraction ≥0.90, signed share in `[0.8,1.2]`; mass criterion at
every sample through `t=0.0010`; first sampled mass exit in
`[0.0015,0.0030]` while the sign and signed-share criteria still pass;
initial full margin rate positive; exit full/radial/vector-polarization
rates negative. No exit by the endpoint leaves exit-dependent predictions
untested, never passed. The N14/N15 `t=0.0023` coincidence and N16
full-final `t=0.0024` exit are comparison observations, not exact-time
requirements. Undefined normalizers or reconstruction errors are failures.

## Source and normalizer mechanism gate

Run the previously committed `src/wp16_036_N17_mechanism_gate.py` after the
broad time gate. Its ordered source identity, sampling times, directional
steps, unique rank and sign requirements, symmetric two-order complex
numerator/normalizer swap, numerical spread and failure rules remain exactly
as in the prefreeze. The broad gate and mechanism gate are distinct recorded
outcomes; never alter one to rescue the other. A failed mechanism command
writes a JSON result before returning a nonzero status. Retain it.

The comparison at `t=0.0023` is a fixed-time state difference between
`full_final` and `inherited`; it is not a time derivative or causal effect.
Only one N17 finite-cutoff holdout is claimed. Neither a joint pass nor a
failure yields an all-cutoff theorem, a continuum bound, or a solution to
3D Navier–Stokes regularity.
