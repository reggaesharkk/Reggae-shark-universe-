# Work Package 8: localized energy identity with Galerkin residual

**23 September 2026 | Unforced periodic Navier–Stokes (B) | Finite-mode audit**

## Why this is the next check

Work Package 7 resolved global Fourier-shell energy exchanges at one
instant. A spatial window probes local concentration, but a finite
Galerkin trajectory does **not** obey the full PDE pointwise. Its local
energy identity contains a truncation residual. Treating a discrepancy
as a PDE violation without that term would be a mathematical error.
We retain the unforced equation; adding a forcing term changes the
case-(B) research target.

## Exact finite-dimensional identity

For the `N=4` Galerkin velocity `u_N`, let `P` be Leray projection,
`P_N` the Fourier cutoff, and `B=(u_N·∇)u_N`. Choose pressure p so that
`P B=B+∇p` with zero spatial mean of p. Define

`R_N=(I−P_N)P B`.

Then the smooth trigonometric polynomial satisfies pointwise

`∂_t u_N+B+∇p=νΔu_N+R_N`.

For a time-independent nonnegative smooth periodic window φ and
`e=|u_N|²/2`, normalized spatial integration gives

`d/dt ⟨φ e⟩ = ⟨(e+p)u_N·∇φ⟩ + ν⟨e Δφ⟩
                 −ν⟨φ|∇u_N|²⟩ + ⟨φ u_N·R_N⟩`.

At `φ=1`, `⟨u_N·R_N⟩=0` by Fourier orthogonality and this is the
ordinary global energy identity. At variable φ the weighted residual
need not vanish. Pressure contributes a nonlocal window term even
though its global energy contribution is zero. This is an equality for
the finite Galerkin ODE, not a proof of a local energy inequality for
an infinite-dimensional weak solution.

## Windows, evaluation, and outputs

Use `φ_κ(x)=exp[κ(cos x₁+cos x₂+cos x₃−3)]`, for
`κ=0,1,4,9,16`. Every window is strictly positive on the torus;
larger κ concentrates weight near the origin but does not create a
compactly supported bump. Its gradient and Laplacian are evaluated
analytically. Use the same line-like and cube terminal states at
`t=0.1` as Work Packages 6–7. The Fourier convolution and pressure
are evaluated with 64³ and 96³ spatial grids. Their sizes exceed the
maximum coordinate frequency of the cubic polynomial products,
avoiding aliasing in those products; the smooth exponential window
has a rapidly decaying rather than finite Fourier series, so grid
agreement is checked separately.

| Initial Fourier support | Global `d⟨e⟩/dt` (κ=0) | Residual at κ=1 | Residual at κ=16 | Maximum identity closure error |
|---|---:|---:|---:|---:|
| Line-like | −0.37844910 | +0.00017919 | +0.00002342 | about 2.1×10⁻¹⁷ |
| Cube | −0.60581787 | +0.00028727 | −0.00003330 | about 1.1×10⁻¹⁶ |

The residual values are **weighted integrals** `⟨φu·R_N⟩`, not pointwise
forces. Omitting that term creates an error of exactly its magnitude.
The window mean falls from 1 at κ=0 to about 0.001016 at κ=16, so
raw weighted energy rates across κ should not be compared as though
the windows had equal mass. The 64³-versus-96³ differences in the
reported local-energy derivatives were at most about `4.5×10⁻¹⁶`
for these cases. Full term-by-term results are in
`localized_energy_results.json`.

## Interpretation and remaining gap

This validates finite-cutoff bookkeeping with pressure and the missing
high-frequency projection term. It does **not** show physical-space
singularity formation, local regularity, or a persistent cascade. A
shrinking-window study near a putative singularity would need a
space-time sequence, appropriate scale-normalized quantities,
control of pressure, and a proven passage as both the window scale
and Fourier cutoff change. None of those limiting steps is supplied
by this work package. Claims that the cubic-support field provides
a protective “structural buffer” are unsupported by these tests.
