# Navier–Stokes Work Package 2: enstrophy and viscosity

**Exploratory note, 23 September 2026.** Builds on Work Package 1 v0.2.

## 1. The correct finite-mode identity

For a divergence-free Fourier Galerkin velocity `u_N` on the periodic
three-torus, with the same volume-normalized convention as `galerkin.py`, set

`Ω_N = (1/2) Σ_{|k|≤N} |k|² |a_k|²`,
`D_N = Σ_{|k|≤N} |k|⁴ |a_k|² = ||Δu_N||₂²`,
`T_N = −Re Σ_{|k|≤N} |k|² conj(a_k)·N_k`,

where `N_k` is the projected convective term. Then exactly

`dΩ_N/dt = T_N − ν D_N`.

For the continuous trigonometric polynomial, integration by parts gives

`T_N = − ∫ Σ_{i,j,l} (∂_j u_i)(∂_i u_l)(∂_j u_l) dx`,

using the normalized torus integral. The term with
`u_i ∂_i∂_j u_l ∂_j u_l` vanishes by incompressibility. This identity
requires the complete Galerkin convolution, even though the energy inner
product at one instant can be computed on the occupied support alone.

## 2. What the sample establishes

The seeded six-mode field from Work Package 1 has `T_N < 0`. Reversing all
velocity amplitudes gives `T_N = +4.882583908687745`, while `D_N` is
unchanged at approximately `104.19498637605816`. The initial derivative is
positive precisely when `ν < ν_* = T_N/D_N ≈ 0.04686006571434863` for
that *specific* field. For `ν=0.01` it is `+3.8406340449271634`; for
`ν=0.1` it is `−5.536914728918071`.

Under `u(x) → A u(mx)` on the torus, `Ω_N` scales as `A²m²`, `T_N` as
`A³m³`, `D_N` as `A²m⁴`, and `ν_*` as `A/m`. Thus damping dominates this
instantaneous example at sufficiently high frequency with A and ν fixed;
amplitude increase can reverse the sign. The threshold depends on the
current velocity and cannot be treated as a universal safe viscosity.

## 3. A valid derivative-dependent estimate and its limit

On the three-torus, Hölder, interpolation, and Sobolev embedding give

`|T_N| ≤ C ||∇u_N||₂^(3/2) ||Δu_N||₂^(3/2)`.

The constant C can be chosen independently of the Galerkin cutoff N.
Young's inequality then yields, for another constant C' independent of N,

`dΩ_N/dt + (ν/2) D_N ≤ C' ν^(−3) Ω_N³`.

This **survives** the amplitude and frequency falsifiers of Work Package 1,
because the right side includes derivatives and ν. It is a standard local
control estimate, not a new global regularity theorem. The comparison ODE
`y' = C' ν^(−3) y³` has a finite time upper-bound horizon, so the estimate
does not provide a uniform bound on Ω for all time. Conversely, failure of
this estimate to settle global regularity does not imply PDE blowup.

## 4. Exact next mathematical question

Find and prove a stronger **resolution-independent** mechanism that prevents
the cubic enstrophy term from accumulating over all time for arbitrary
smooth periodic divergence-free data, or produce a genuine smooth-data
breakdown example satisfying the official problem formulation. The present
six-mode threshold, by itself, does neither. A broader triad network search
may help reject hypotheses but cannot replace the necessary uniform proof.

## 5. Reproducibility

Run `python3 validate_enstrophy.py` from this package directory. The
recorded results are `enstrophy_results.json`. The code checks both sides
of the H1 budget and the `A/m` threshold scaling to floating-point
precision. It uses the sparse-support implementation for instantaneous
inner products and the full operator for the derivative check. An
independent 16³-point physical-space quadrature of the cubic gradient
identity agrees with the Fourier evaluation within `4.5×10⁻¹⁵`.

Official target: Charles L. Fefferman, *Existence and Smoothness of the
Navier–Stokes Equation*, formulation (B),
https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf .
