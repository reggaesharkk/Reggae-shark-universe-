# WP16 K36 rate inequality and prospective N14 time gate

Prince Upadhyay, Independent Research — frozen 26 September 2026, before N14 continuation exists

**Pre-data correction (same day):** the first merged version mistakenly carried search grid 40 from N13 to N14. Since `spatial_fields` requires `grid>3N`, N14 requires a grid above 42. The corrected frozen N14 search grid is 48, with refinement grids 48/64/96/128. This amendment was committed before any N14 state or score existed; the original version remains visible in git history.

## Exact finite inequality

Fix the frozen N11-derived ordered source-orbit coalition `K36`, output `k=(6,0,3)`, tracked anchor `p=(3,2,2)`, `q=(3,-2,1)`, and a finite Galerkin trajectory with `z≠0`. Set `w=|k|⁴`, `B=P_k(i(q·a_p)a_q)`, `z=-w<a_k,B>`. For each ordered source `l+r=k`, set `d_{lr}=-P_k(i(r·a_l)a_r)`, `C_{lr}=-w<d_{lr},B>`, and `x_{lr}=C_{lr}/z`. The signed group `c_g` is the sum of `Im x_{lr}` over the ordered pairs in orbit group `g`.

Let `I=Σ_{g∈K36}|c_g|`, `O=Σ_{g∉K36}|c_g|`. The registered 90% mass gate is exactly `F=I−9O≥0`. Under `v=dot a`,

`dot B=P_k i[(q·v_p)a_q+(q·a_p)v_q]`,

`dot d_{lr}=-P_k i[(r·v_l)a_r+(r·a_l)v_r]`,

`dot z=-w[<v_k,B>+<a_k,dot B>]`,

`dot C_{lr}=-w[<dot d_{lr},B>+<d_{lr},dot B>]`, and

`dot x_{lr}=dot C_{lr}/z-C_{lr}dot z/z²`.

Since `|d|c_g|/dt|≤|dot c_g|≤Σ_{(l,r)∈g}|dot x_{lr}|` whenever differentiable, and the same lower directional bound holds at zero groups by local Lipschitzness,

the lower one-sided directional rate of `F` is at least `−E_I(t)−9E_O(t)`,

where `E_I,E_O` sum `|dot x_{lr}|` over ordered sources in/outside K36. Hence for any interval with `z≠0`,

`F(t) ≥ F(0)−∫₀ᵗ [E_I(s)+9E_O(s)] ds`.

This is a conditional finite identity/inequality, not a positive lower bound or a continuum theorem. It is rigorous across absolute-value kinks in the integrated Lipschitz form. A cutoff-independent sufficient condition would need uniform control of the integral and of the nonzero tracked denominator along the actual flow.

## A broad norm bound and its limitation

By `|d_{lr}|≤|r||a_l||a_r|`, Cauchy–Schwarz on the convolution constraint `l+r=k` gives `S₀=Σ|r||a_l||a_r|≤||a||₂||∇a||₂` and `S₁=Σ|r|(|v_l||a_r|+|a_l||v_r|)≤||v||₂||∇a||₂+||a||₂||∇v||₂`. Thus

`E_I+9E_O ≤ (9w/|z|){|B|S₁ + [|dot B|+|B||dot z|/|z|]S₀}`.

The estimate is independent of the number of Galerkin modes **conditional on** the displayed norms, `|z|^{-1}`, and their integrability. It is not an unconditional Navier–Stokes regularity estimate: `||∇v||₂` demands higher control, and `z` may approach zero. The prior all-state counterexample also forbids a universal K36 mass theorem.

## N12/N13 audit of usefulness

The reproducible script `src/wp16_036_K36_margin_rate_envelope.py` evaluates the exact ordered-source envelope and the broad norm bound at all six optimized anchors without finite-differencing source derivatives. The analytic grouped margin rate agrees with the previous central finite-difference full rate to at most about `5.7e-5` absolute.

The user also ran the independent Windows VS Code quick package and supplied `trajectory_quick.json` (SHA-256 `02815c710562eb59c3614e6da0c5643ff95feb766db8eafb35b14ad0f54a393c`). Its six `t=0.001` mass fractions and signed shares match the archived values within floating-point roundoff; the N4/N7 derivative validation differences were `6.59e-14` and `6.36e-13`. This reproduces the finite quick trajectory on the user's laptop, not N14.

| N/state | Initial F | Exact loss envelope `E_I+9E_O` | Broad H¹ loss bound | Observed local `dot F` |
|---|---:|---:|---:|---:|
| 12 inherited | +432.95 | 1,607,471 | 298,095,111 | +401,321 |
| 12 target-only | +432.98 | 1,607,464 | 298,097,846 | +401,330 |
| 12 full-final | +351.33 | 1,379,013 | 286,462,715 | +209,854 |
| 13 inherited | +356.81 | 1,393,542 | 287,123,251 | +208,744 |
| 13 target-only | +418.82 | 1,384,988 | 282,152,524 | +187,392 |
| 13 full-final | +358.60 | 1,399,461 | 286,367,544 | +121,277 |

The broad bound is about 185–208 times the already conservative exact source envelope. Initial `F/(E_I+9E_O)` is only `0.000255–0.000302`; initial `F/(broad bound)` is about `1.2–1.5×10⁻⁶`. These quotients are **instantaneous scales, not certified survival times**, because rate envelopes evolve. The actual sampled exits occur near `0.0020–0.0026`. This route does not explain persistence; its loss of phase/polarization cancellation is measurable.

## Prospective N14 time-resolved protocol — frozen now

No N14 continuation or outcomes have been generated. Use exactly the existing N11-frozen K36 keys and the existing static same-sign, 90% grouped absolute mass, signed-share `[0.8,1.2]` criteria. Use the N13 continuation row as previous state and construct N14 `inherited`, `target_only`, `full_final` with the existing `reconstruct` semantics. Keep `ν=0.1`, the existing base-state amplitude/anchor-time semantics, and the exact finite Galerkin ODE. Do not retune keys or thresholds on N14.

**Continuation schedule to implement and validate before running:** use seed `20260939`, **search grid 48**, 16 new-mode global draws, 3 new-mode block rounds, 4 full-support block rounds, 72 trials per round, block size 40, initial step 0.30, and the same objective `C_infinity_stretch` as the N13 continuation. Select the best phases using grid 48 and report refinements at grids 48, 64, 96, and 128 without retuning the phase vector. The original `spatial_fields` requires `grid>3N`; at N14, grid 40 would violate this (`40≤42`), so carrying the N13 grid forward is invalid. This correction was made before any N14 data. This is a new prospective schedule choice; document any unavoidable deviation *before* viewing N14 results. The memory-efficient evaluator must agree with the original evaluator to a specified numerical tolerance on feasible lower cutoffs and archived N12/N13 states. Checkpoint every completed trial by atomic write with seed, RNG state/draw position, best phases, score, input hashes, and code version. Profile RAM on a smaller cutoff and abort if estimated N14 peak exceeds 12 GiB on the user's 16 GB Windows machine.

**Time grid and validation:** from each N14 state, integrate at `dt=0.0001` and sample every step through `t=0.0030` after the optimized anchor. Record `I,O,F`, mass fraction, signed share, same-sign gate, energy, reality/divergence errors, and the local `F` radial/phase/polarization/viscous velocity decomposition at `t=0` and at the first sampled 90% mass exit (if any). Repeat the first-exit bracket at half step `dt=0.00005` and compare mass fractions at common times. Report first failure of *any* static gate as well as the first mass-gate exit. If `z` vanishes, report undefined normalized channel and stop that state's gate rather than dividing by zero.

**Predeclared tests (all three states reported, including failures):**

1. Static transfer: all three N14 initial states meet the original frozen criteria.
2. Transient time pattern: each state initially meets the mass criterion at every sampled point through `t=0.0010`, then has its first sampled mass exit in `[0.0015,0.0030]`; signed criterion still passes at that mass exit.
3. Local velocity pattern: `dot F>0` initially; at first mass exit `dot F<0` and both radial and vector-polarization components are negative. If no mass exit occurs by `0.0030`, test 3's exit signs are untested, not assumed false.

These hypotheses were chosen after observing N12/N13; they are **prospective only for N14**. Report each individually and the joint outcome. A state that fails the initial static criterion fails test 1; its later trajectory remains descriptive rather than being counted as a successful persistence/exit test. Record floating-point and time-step disagreement and never convert sampled times into rigorously certified continuous crossing times.

**Freeze boundary:** merge this note and its code/JSON in the research repo and status mirror before any N14 data generation. The later N14 implementation must cite this commit. N14 optimization on Windows has not yet been made safe or executed.
