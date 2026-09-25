# Navier–Stokes Bridge Audit: finite Fourier diagnostics

**Author:** Prince Upadhyay, Independent Research  
**Report version:** 0.1, 24 September 2026  
**Mathematical target:** smooth, unforced, periodic three-dimensional Navier–Stokes, as in Fefferman's formulation (B).  
**Status:** reproducible finite-mode audit and standard conditional estimates; no resolution of the arbitrary-data PDE problem.

## Abstract

This audit asks which claims from earlier finite-channel algebra and short
fluid models survive translation to a genuine incompressible Fourier
Galerkin discretization. It checks scaling obstructions, standard
derivative-dependent bounds, a short N=4 trajectory, spectral-shell
exchange, and localized energy, enstrophy, and helicity balances. A
conservative, cutoff-independent small-data bound is recorded. The
unforced large-data regularity question is untouched: neither these
instantaneous identities nor one 257-mode simulation provides a norm bound
uniform over both time and Fourier cutoff.

## 1. Definitions and reproducibility boundary

The torus is [0,2π)³, with spatial **mean** denoted by <·>. The velocity
is a real-valued, divergence-free Fourier polynomial, with coefficients
`a_{−k}=conj(a_k)` and `k·a_k=0`. The Galerkin model is

    ∂ₜu_N = −Q_N 𝓟[(u_N·∇)u_N] + νΔu_N,

where `Q_N` keeps `|k|≤N` and `𝓟` is the Leray projector, with
`P_k=I−kkᵀ/|k|²` for `k≠0` and `P_0=I`. The larger simulation uses
`N=4` (257 Fourier modes, including zero), `ν=0.1`, 31,129 ordered
convolution pairs, and 40 RK4 steps of `Δt=0.0025` ending at `t=0.1`.
The two seeded initial fields have 44 (line-like) and 124 (cube)
occupied modes at energy one. Their names refer to **Fourier support**.

`N=4` is a *fixed* spectral cutoff. A 64³, 96³, or other physical-space
FFT grid used for quadrature is a distinct parameter. Changing only
the quadrature grid does not establish convergence as N→∞. Derivatives
of localized quantities below use the instantaneous Galerkin ODE right
hand side, **not** finite differences between time snapshots.

## 2. Findings across the ten packages

| Package | Mathematical or computational finding | Boundary |
| --- | --- | --- |
| WP1 | Real, divergence-free triad validates Leray filtering and energy conservation. The chosen low/high transfer is approximately −2.30290648/+2.30290648. Amplitude scaling makes flux cubic while energy stays quadratic; integer frequency dilation leaves energy fixed while flux grows linearly. | Rules out proposed universal energy-only flux inequalities; does not rule out derivative-dependent bounds. |
| WP2 | Finite enstrophy balance `Ω'=T−νD`, where `Ω=||∇u||₂²/2` and `D=||Δu||₂²`; standard estimate `Ω'+(ν/2)D≤C'ν⁻³Ω³`. | Its comparison estimate does not control arbitrary-size data for all time. |
| WP3 | Fourier lattice estimate gives `C₀=√(4π²+π⁴/45)≈6.45314373556` and a sufficient invariant region `C₀||∇u₀||₂<ν`. For the tested triad at `ν=0.1`, sufficient amplitude is below `0.00246284416`. | Classical, conservative small-data condition; failing it says nothing about blow-up. |
| WP4 | Classical instantaneous flux bound `|Π_K|≤√(2E_{≤K}) C_s||u||_{H^s}||∇u||₂` for `s>3/2`, with cutoff-independent `C_s`; nine network samples of 26, 124, and 342 occupied modes check the H² instance. | Controls `u` in `L∞` via its H^s norm, but does not bound that norm in time. |
| WP5 | Gradient `L∞` by the same Fourier embedding requires `s>5/2`. Eighteen line-like/slab-like/cube support samples obey the proven H² flux estimate; maximum observed ratio ≈0.000715. | Support geometry is in frequency space; sampled ratios are not optimal constants. |
| WP6 | At `t=0.1`, total energy is about 0.961393 (line) and 0.936637 (cube). The low-cutoff flux changes +0.057406→+0.083235 (line) and −0.022135→+0.002037 (cube). | One short N=4 trajectory, with no long-time or N→∞ claim. |
| WP7 | At `t=0.1`, donor–recipient–advector transfers across `(0,1],(1,2],(2,3],(3,4]` satisfy donor–recipient antisymmetry; an independent physical-space energy calculation agrees to roundoff. | Tensor depends on donor convention, field, instant, and shell edges; no persistent cascade shown. |
| WP8 v0.2 | Local energy equality closes when pressure and the high-frequency Galerkin residual are included. Frequency indexing fixed using `rint` before integer conversion; maximal recorded 64³/96³ projection-term difference is `3.49354×10⁻¹⁸`. | Finite Galerkin identity; a localized test window sees terms that vanish in the global integral. |
| WP9 v0.1 | Local enstrophy identity with vortex stretching and curl residual closes within `4.44×10⁻¹⁶` on stored 64³ outputs. Global enstrophy derivatives are −0.68382922 (line), −2.56054203 (cube). | Alignment values from a 16³ subsample at one time do not test a geometric regularity theorem. |
| WP10 v0.1 | Local helicity identity closes within `1.66533×10⁻¹⁶` on stored 64³ outputs; global Fourier Parseval check agrees within the same tolerance. | Helicity is signed; these numbers do not show stabilization, chirality causing transport, or a PDE regularity result. |

There is **no MILP model or certificate** in WP4–5. The alleged WP10
long-time decay module and earlier localized-helicity draft were rejected:
they are not executed packages and their numbers are excluded.

## 3. What the local identities actually say

Write `B=(u_N·∇)u_N`, choose `p` by `𝓟B=B+∇p`, and set
`R_N=(I−Q_N)𝓟B`. Then the exact finite Galerkin momentum equation is

    ∂ₜu_N+B+∇p=νΔu_N+R_N.

For the smooth periodic window
`φ_κ=exp[κ(cos x₁+cos x₂+cos x₃−3)]`, the local energy calculation uses
`e=|u|²/2`:

    d<φe>/dt = <(e+p)u·∇φ> + ν<eΔφ−φ|∇u|²> + <φu·R_N>.

For `ω=∇×u`, `e_ω=|ω|²/2` and symmetric strain `S`:

    d<φe_ω>/dt = <φω·Sω> + <e_ωu·∇φ>
                  + ν<e_ωΔφ−φ|∇ω|²> + <φω·curl R_N>.

For the signed helicity density `h=u·ω`:

    d<φh>/dt = <[hu+(p−e)ω]·∇φ>
                + ν<hΔφ−2φ∇u:∇ω>
                + <φ[ω·R_N+u·curl R_N]>.

`Q_N`, `𝓟`, and curl commute as Fourier multipliers; multiplication
by `φ` need not commute with the cutoff. The residual has the sign
shown above. A global integral with `φ=1` removes it by orthogonality
between low modes `|k|≤N` and residual modes `|k|>N`. This makes it a
finite-cutoff bookkeeping term in a local identity, not evidence for
an intrinsic extra source in the continuous equation.

At `t=0.1`, the helicity results include:

| Support | κ | <φh> | d<φh>/dt | Projection contribution |
| --- | ---: | ---: | ---: | ---: |
| line-like | 0 | −0.468766445 | +0.363401239 | ≈0 |
| line-like | 4 | −0.020392649 | +0.025443236 | +0.000503235 |
| cube | 0 | −0.217053870 | +0.108448856 | ≈0 |
| cube | 4 | +0.000856879 | +0.001149426 | +0.002838510 |

The line and cube WP10 grid differences for the helicity derivative
are at most `3.88578×10⁻¹⁶` over the stored windows. These windows
have unequal spatial means across κ, so raw weighted values for
different κ should not be read as equal-volume local concentrations.
Likewise, a helicity density or its integral does not by itself measure
`u`–`ω` alignment or causally suppress vortex stretching.

## 4. Verification levels and corrections to external summaries

The shipped scripts and JSON supply direct reproducibility of each
package's *own* implementation. WP10 also checks the global derivative
by a Fourier Parseval calculation within the shipped script. A separate
review supplied by the project owner reports: independent derivation
of the WP10 signs; direct 257-mode sums with no FFT for global helicity;
and a separately coded grid route using 80³/112³ points agreeing with
the archived values to floating-point precision. **This report records
that review as reported evidence; its independent source code and raw
run were not supplied here for direct inspection.** The review states
its grid route reuses prior trajectory logic and is not a blind second
solver.

Some circulating summaries misstate the actual archive. The valid
package currently bears the filename and note **WP10 v0.1**, not
`WP10 v1.0` or an unversioned final certificate. Its maximum stored
closure error is `1.6653345369377348×10⁻¹⁶`, not the alternative
`1.458291×10⁻¹⁶`, `2.110223×10⁻¹⁶`, `2.45×10⁻¹⁶`, or
`3.01×10⁻¹⁶` numbers in the pasted summaries. Its left side is
computed from `u_t` and `ω_t` supplied by the Galerkin ODE, not
finite-difference temporal tracking. Nor does the archive calculate
a WP10 velocity–vorticity alignment index or demonstrate sustained
chirality-driven attenuation.

## 5. Research conclusion and next mathematical requirement

The archive establishes credible, reproducible **finite-dimensional
consistency checks** and records two classes of statements: negative
scaling examples for overstrong energy-only bounds, and familiar
conditional inequalities requiring higher norms or small data. It does
not demonstrate a new cutoff-independent, time-uniform estimate for
arbitrary smooth initial fields. In particular, agreement between
physical-space grids, cancellation inside N=4, or a small
instantaneous residual does not control the effect of `R_N` as N→∞
along arbitrary evolving solutions.

A submission claiming progress on the full periodic regularity question
would need a new, fully stated estimate with constants independent of
N and an argument closing that estimate over all times for arbitrary
smooth data, or a valid breakdown construction matching the official
formulation. That result is not present in WP1–10. The appropriate
external review target now is the finite-mode identities, code, and
their sharply stated limits, rather than a claim to solve the
Millennium problem.

## Source and archive map

- Primary formulation: C. L. Fefferman, [*Existence and Smoothness of
  the Navier–Stokes Equation*](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf),
  in *The Millennium Prize Problems*, statement (B).
- WP1–3: `galerkin.py`, `validate_sparse_triad.py`,
  `validate_shells_and_dilation.py`, `validate_enstrophy.py`,
  `small_data_bound.py`, their result JSONs, and WP2–3 scope notes.
- WP4–7: `validate_network_hs.py`, `validate_anisotropic_network.py`,
  `evolve_galerkin.py`, `extract_shell_cascade.py`, their result JSONs,
  and WP4–7 notes.
- WP8–10: `localized_energy_audit.py`, `localized_enstrophy_audit.py`,
  `verify_helical_cascade.py`, the three result JSONs, WP8 correction
  note, and WP8–10 scope notes. Use corrected WP8 v0.2 code.

This report is a scoped research audit. It does not certify peer review,
originality of the standard estimates, or a theorem about global
smoothness of the three-dimensional PDE.
