# Work Package 3: an explicit small-data invariant region

**Exploratory audit, 23 September 2026.** This is a conservative version of a
standard small-data result, not a solution of the arbitrary-data Clay problem.

## Exact assumptions

Use the unforced incompressible three-dimensional periodic Navier–Stokes
equation, viscosity `ν>0`, torus `[0,2π)^3`, and normalized integral so
Parseval reads `||u||₂² = Σ_k |a_k|²`. Let `u_N` be a Fourier Galerkin
solution, `G_N=||∇u_N||₂²`, `D_N=||Δu_N||₂²`, and `Ω_N=G_N/2`.

The constant mean velocity contributes zero to the integrated enstrophy
transfer. Write `v_N=u_N−mean(u_N)`. With

`S = Σ_{k∈Z³, k≠0} |k|⁻⁴`,

Fourier Cauchy–Schwarz gives `||v_N||∞ ≤ √S ||Δu_N||₂` for every cutoff N.
Hölder, applied to the enstrophy transfer in the form
`T_N = ∫ (v_N·∇u_N)·Δu_N`, gives

`|T_N| ≤ √S √G_N D_N`.

An explicit lattice-series upper bound avoids an unevaluated constant:
there are exactly `24n²+2` lattice points with `|k|∞=n`, and each has
`|k|≥n`. Therefore

`S ≤ Σ_{n≥1} (24n²+2)/n⁴ = 4π² + π⁴/45`,

so `C₀ = √(4π²+π⁴/45) ≈ 6.453143735558639` suffices, independently of N.
The bound is intentionally loose.

## Invariant small-data ball

The exact identity from Work Package 2 implies

`dΩ_N/dt ≤ −[ν−C₀√G_N] D_N`.

If `C₀√G_N(0) < ν`, then the bracket is initially positive. A continuity
argument keeps `G_N(t) ≤ G_N(0)` for all finite t: within that region the
derivative is nonpositive, so a first exit is impossible. This yields a
cutoff-independent H¹ bound and time-integrated H² dissipation. For smooth
initial data satisfying `C₀||∇u₀||₂<ν`, the standard Galerkin limit and
strong-solution continuation give global smoothness. This is a **sufficient
small-data case already accessible to standard PDE analysis**. It says
nothing about arbitrary-size initial data.

## Numerical diagnostic

`small_data_bound.py` checks the explicit envelope and a few rescalings of
our existing triad. For `ν=0.1` and this triad's base `G≈39.58981`, the
conservative sufficient amplitude is strictly below `0.00246284416`.
At amplitude `0.01` the criterion fails even though the actual initial
enstrophy derivative is negative: sufficient does not mean necessary.
At amplitude `5` the derivative is positive, still without any conclusion
about finite-time blowup.

The finite-cutoff `C_N` reported by the script is a diagnostic only.
Restricting a constant to the initially occupied six modes cannot establish
an invariant result because nonlinear evolution creates new modes.

## Correction to the proposed summary

The inequality written as `dΩ/dt ≤ Cν⁻³Ω³−νD` is not what one obtains
after absorbing nonlinear growth by Young's inequality; that step spends
part of the viscous term, yielding a coefficient such as `−(ν/2)D`.
The exact identity is `dΩ/dt=T−νD`. Also, under frequency dilation with
amplitude fixed, the tested `T` scales as `m³` while viscous `νD` scales
as `m⁴`. Thus our finite triad does not show viscosity losing to arbitrarily
high frequencies. Its ratio depends on both amplitude and frequency.

## Next target

The explicit ball closes a known small-data subcase. The gap is an
arbitrary-data, cutoff-independent a priori estimate or a valid breakdown
construction. A stochastic triad search is useful only to falsify a *new,
precisely stated* estimate; it cannot turn this small-data argument into an
arbitrary-data proof.
