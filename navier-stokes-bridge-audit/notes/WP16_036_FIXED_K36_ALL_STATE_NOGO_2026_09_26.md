# Fixed K36 mass dominance cannot hold for all Galerkin states

**Post-hoc scope check · 26 September 2026.** This note does not change the N12/N13 holdout criteria or their observed results. It tests a stronger universal interpretation that those finite observations do not claim.

Let the tracked output wavevector be `K=(6,0,3)` and the anchor triad be `P=(3,2,2)`, `Q=(3,-2,1)`, so `P+Q=K`. In the canonical evaluator, `k_channel_grouped` sums contributions to the phase velocity of this output, grouped by ordered pairs of wavevector orbits. The N11-selected K36 is a fixed set of 36 such group keys.

Choose another admissible pair `l=(-1,0,3)`, `r=(7,0,0)` with `l+r=K`. Both ordered orbit pairs `(orbit(l),orbit(r))` and its reverse are outside K36. At `N=7`, put nonzero transverse Fourier coefficients at `±P, ±Q, ±K, ±l, ±r`, respecting conjugate reality. Hold the first three positive-mode coefficients fixed and multiply the coefficients at `±l, ±r` by `L`. The tracked anchor `z` in the evaluator is independent of `L`. The two new outside source terms in the `K` equation are quadratic in `L`, while K36 source terms stay fixed. Generic transverse complex polarizations give a nonzero outside phase contribution, as witnessed below. Thus the K36 absolute-mass fraction tends to zero as `L→∞`. Zero extension gives the same witness at larger cutoffs. A universal ≥0.90 K36 mass fraction over all divergence-free real Galerkin states is therefore false.

The deterministic script `src/wp16_036_fixed_K36_all_state_counterexample.py` uses seed `20260926`, verifies divergence and conjugate reality below `1e-12`, and yields:

| `L` | K36 absolute mass | Outside absolute mass | K36 fraction |
|---:|---:|---:|---:|
| 1 | 3.2141186525 | 3.9623376983 | 0.4478698811 |
| 10 | 3.2141186525 | 396.2337698263 | 0.0080464029 |
| 100 | 3.2141186525 | 39623.3769826281 | 0.0000811101 |

This is a finite explicit witness plus an algebraic amplitude-scaling argument. A uniform rescaling of every coefficient preserves these ratios, so one may normalize the total L2 energy while making the fixed anchor modes small but nonzero. The construction does **not** contradict dominance on the particular evolved, phase-only, amplitude-preserving states used in the N12/N13 holdouts. It shows that any future uniform theorem needs an explicit restriction to a state class or a trajectory estimate that supplies the required control of outside modes relative to the tracked anchor. Such an estimate is currently open.
