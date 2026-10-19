# Work Package 10 v0.1 — localized helicity balance

Author: Prince Upadhyay, Independent Research. Date: 24 September 2026.

## Scope and conventions

This is a finite Galerkin identity check for the unforced periodic N=4
(257-mode) model, evaluated at t=0.1 for the established seeded line and cube
fields. The fields, pressure, and residual are reconstructed by WP8 code.
The 64^3 and 96^3 physical grids resolve the polynomial interactions;
the spatial window is smooth and periodic.

Let B=(u·∇)u, P be Leray projection, Q_N be the spectral ball cutoff,
and choose p so P B=B+∇p. Then the ODE is

    u_t=-Q_N P B+νΔu,
    u_t+B+∇p=νΔu+R_N,    R_N=(I-Q_N)P B.

In particular, R_N has **positive** high-frequency projected-B sign in the
momentum equation. The sharp Fourier cutoff, Leray projector, and curl commute
where defined as Fourier multipliers. The cutoff need not commute with
multiplication by the window.

Set ω=∇×u, h=u·ω and e=|u|²/2. For static smooth periodic φ,

    d<φh>/dt = <[hu+(p-e)ω]·∇φ>
              + ν<hΔφ-2φ∇u:∇ω>
              + <φ(ω·R_N+u·curl R_N)>.

Here <·> is the torus spatial **mean** (not the unnormalized integral).
The equality follows by dotting the momentum equation with ω, dotting its
curl with u, and integrating the resulting divergence terms by parts.
For φ=1 the transport term and projection residual integrate to zero;
global helicity is signed and its viscous derivative need not be negative.

## Execution and checks

Run from this directory:

    python verify_helical_cascade.py > helicity_results.json

Two fields × five window concentrations κ=0,1,4,9,16 were checked at
64^3 and 96^3. The largest |lhs-rhs| across stored 64^3 rows is
1.6653345369377348e-16; the largest 64^3-versus-96^3 lhs difference is
3.885780586188048e-16. The separate Parseval calculation of the global
helicity derivative agrees with the global viscous expression to at most
1.6653345369377348e-16.

| Field | κ | <φh> | d<φh>/dt | Residual contribution |
| --- | ---: | ---: | ---: | ---: |
| line | 0 | -0.468766445 | +0.363401239 | ≈0 |
| line | 4 | -0.020392649 | +0.025443236 | +0.000503235 |
| cube | 0 | -0.217053870 | +0.108448856 | ≈0 |
| cube | 4 | +0.000856879 | +0.001149426 | +0.002838510 |

The residual is zero only for the global window up to roundoff; local windows
can see it. These checks establish the algebra and numerical consistency of
this particular finite system and two initial fields. They do not provide a
uniform estimate as N→∞, a persistent alignment mechanism, or a regularity
result for the continuous three-dimensional Navier–Stokes equations.

The executable reuses WP8 field reconstruction, so it is not a blind second
solver; the Fourier global identity and second grid test distinct consequences
of that reconstruction. Independent review of the analytical and numerical
steps remains welcome before any external scientific claim.
