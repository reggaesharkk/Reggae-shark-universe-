# WP16 K36 mass-margin velocity: two-stage finite exit

Prince Upadhyay, Independent Research — 26 September 2026

This post-hoc diagnostic keeps the N11-frozen K36 keys and works on the same six N12/N13 optimized finite Galerkin initial states. Define `I(t)` as the sum of absolute **grouped** K36 output-source contributions and `O(t)` as the corresponding sum outside K36. The registered 90% gate is exactly `F(t)=I(t)-9 O(t)≥0`. This avoids a ratio denominator in the local calculation.

At a state `a` with Galerkin velocity `v=da/dt`, decompose each complex divergence-free vector coefficient orthogonally over the complex line spanned by `a_j`:

`r_j = Re(<a_j,v_j>)/|a_j|²; ω_j = Im(<a_j,v_j>)/|a_j|²`

`v_j = r_j a_j + i ω_j a_j + (v_j-r_j a_j-i ω_j a_j)`.

The three parts are radial magnitude, scalar phase, and residual complex vector polarization. All modal amplitudes in these evaluated states are nonzero. The real-field conjugacy and divergence constraints are preserved by each part. We measured central directional differences of `F` at steps `h=1e-8` and `2e-8`, and also separated viscous from nonlinear velocity. Grouped absolute values can have kinks at zero; these are high-precision local directional diagnostics, not a theorem of differentiability at every group.

## Six-state result

| N | State | Anchor full `dF/dt` | Anchor scalar-phase part | First-exit full `dF/dt` | Exit radial part | Exit polarization part |
|---|---|---:|---:|---:|---:|---:|
| 12 | inherited | +401,321 | +376,744 | −239,822 | −235,733 | −109,140 |
| 12 | target_only | +401,330 | +376,757 | −239,458 | −235,645 | −109,066 |
| 12 | full_final | +209,854 | +227,023 | −522,435 | −279,084 | −212,296 |
| 13 | inherited | +208,744 | +226,552 | −521,902 | −289,930 | −203,922 |
| 13 | target_only | +187,392 | +216,522 | −500,289 | −266,184 | −212,086 |
| 13 | full_final | +121,277 | +175,458 | −365,536 | −252,127 | −284,093 |

The sampled mass fraction first peaks at `t=0.0001–0.0004` after the anchor, then falls through 90% at the previously reported first exits around `t=0.0020–0.0026`. Anchor polarization contribution is negative in all six (`−41,235` to `−62,602`), while anchor radial and scalar-phase contributions are positive. At exit, **both radial and polarization contributions are negative in all six**. The scalar-phase exit contribution varies by state (`−31,055` to `+170,685`). The viscous contribution to `F` is small and positive at every anchor and exit (`+2,224` to `+4,108`); the net adverse rate comes from the nonlinear term.

For N13 full-final, the frozen mass margin moves from `F=+358.596` at the anchor to `F=−4.406` at the first failing sample `t=0.0023`; its local full rate changes from `+121,277` to `−365,536`. The earlier endpoint hybrid ablation found that evolved magnitudes or evolved directions alone still pass at this exit. The local rates explain why static one-factor tests do not capture the nonlinear path: the state moves through a changing combination of radial and polarization velocities.

## Checks and boundary

At each of the 12 evaluated states, the three component central rates sum to the full central rate within `2.85e-4` absolute, compared with full rates of order `1e5`. Changing `h` from `1e-8` to `2e-8` changes the full rate by at most `1.20e-4`. The FFT convolution was independently checked against direct convolution at smaller cutoffs and across alias-free grids at N12/N13 in the prior trajectory and stress audits. These checks do not establish an exact continuum or cutoff-uniform result.

This is the concrete analytic target now: bound `d(I-9O)/dt` under joint radial magnitude and vector-polarization evolution, and determine whether any useful cutoff-uniform lower bound exists. The initially favorable scalar-phase contribution by itself cannot prevent the observed finite exits. No source keys or holdout criteria were retuned.

Reproduce with `src/wp16_036_K36_margin_velocity.py`, archived continuation/source JSON and `dealiased_trajectory_gate_N12_N13_summary.json`. Full central/forward rates at both steps, all six states and both times are in `results/wp16_n13_holdout/K36_margin_velocity_N12_N13.json`.
