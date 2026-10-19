# Work Package 9: localized enstrophy and strain–vorticity diagnostics

**24 September 2026 | Unforced periodic Navier–Stokes (B) | Finite-mode audit**

## Analytical identity

For the same `N=4`, `ν=0.1` Galerkin trajectories and terminal fields
at `t=0.1`, let `ω=∇×u`, `S=(∇u+(∇u)ᵀ)/2`,
`e_ω=|ω|²/2`, and `R_N=(I−P_N)P[(u·∇)u]`. Curling the finite Galerkin
equation gives

`∂_tω+(u·∇)ω=(ω·∇)u+νΔω+∇×R_N`.

For any static smooth periodic nonnegative window φ,

`d⟨φe_ω⟩/dt = ⟨φ ω·Sω⟩ + ⟨e_ω u·∇φ⟩
                + ν⟨e_ω Δφ⟩ − ν⟨φ|∇ω|²⟩
                + ⟨φ ω·(∇×R_N)⟩`.

Pressure drops out on taking curl. The final term is needed for a
*localized finite-Galerkin* identity; its global integral vanishes by
Fourier orthogonality. Every term here is an instantaneous scalar
integral. `ω·Sω` is signed vortex stretching and is not itself a
criterion for regularity.

## Numerical evaluation

Use the windows `φ_κ=exp[κ(cos x₁+cos x₂+cos x₃−3)]` from Work Package
8, for `κ=0,1,4,9,16`. These concentrate weight near the origin but
are never compactly supported. Fourier derivatives, vorticity, strain,
and the curl of the projection residual were evaluated on 64³ and
96³ grids. The wavevector conversion uses *rounding to the nearest
integer* before casting; direct integer casting can misread a frequency
such as `6.999999999999999` as `6` on the 96³ grid.

| Initial Fourier support | Global enstrophy derivative κ=0 | Local weighted derivative κ=9 | Global stretching κ=0 | Local stretching κ=9 |
|---|---:|---:|---:|---:|
| Line-like | −0.68382922 | +0.00114930 | +0.44921093 | +0.00768204 |
| Cube | −2.56054203 | −0.00930789 | +0.48465331 | +0.00317455 |

The line-like field's *weighted* enstrophy integral increases at this
one instant for κ=4,9,16 while its global enstrophy decreases. The
cube field's weighted integral decreases in all tested windows.
Different κ values have very different window masses; the raw weighted
derivatives cannot be interpreted as equal-volume local rates. Neither
sign implies later localization or a singularity.

The maximum closure error in the localized identity is about
`4.5×10⁻¹⁶`; the greatest 64³-to-96³ difference in the left side is
about `4.0×10⁻¹⁵`. Omitting `⟨φω·curl R_N⟩` creates a visible error in
most nonconstant windows. All term values and comparison errors are
in `localized_enstrophy_results.json`.

## Limited eigenvector diagnostic

On a 16³ subsample of the 64³ grid, diagonalize the symmetric strain
matrix. Compute the enstrophy-weighted mean squared cosine between
vorticity and the eigenvector of the **largest strain eigenvalue**:

| Initial support | κ=0 | κ=9 |
|---|---:|---:|
| Line-like | 0.38480 | 0.83969 |
| Cube | 0.37828 | 0.51188 |

The statistic depends on the sample, window, field, and choice of
eigenvector. It is **not** a test of a Constantin–Fefferman–Majda
geometric regularity hypothesis, which concerns more than a pair of
instantaneous angles. Their cited 1996 geometric-constraints paper
specifically treats the 3D *Euler* equations; it must not be silently
presented as a theorem directly certified for this Navier–Stokes run.

## Verdict and limits

This package verifies a localized finite-Galerkin enstrophy *equality*
and reports vortex stretching and alignment diagnostics for two
short trajectories. It supplies neither a localized enstrophy bound
uniform as `N→∞` nor time-uniform control for arbitrary unforced data.
Pressure is absent from the curl equation, but the projection residual
remains; a true infinite-PDE limiting argument would have to control
that term and the evolution of the windows.

Primary literature context: P. Constantin, C. Fefferman, and A. J.
Majda, “Geometric constraints on potentially singular solutions for
the 3-D Euler equations,” *Communications in Partial Differential
Equations* 21 (1996), 559–571.
