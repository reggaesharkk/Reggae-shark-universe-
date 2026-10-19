# A cutoff-independent small-data bound for periodic 3D Navier–Stokes

**Author:** Prince Upadhyay, Independent Research  
**Claim sheet and proof audit, version 0.1:** 24 September 2026  
**Status:** self-checked, available for independent scrutiny; the mechanism is standard and no priority or novelty claim is made.

## Precise claim

Let the three-dimensional unforced incompressible Navier–Stokes equation
have viscosity `ν>0` on `[0,2π)³`. All spatial norms below use the
normalized torus mean, so Parseval has no volume factor. Let `u₀` be
smooth, real and divergence free; its mean `m=<u₀>` may be nonzero.
Define

    C₀ = sqrt(4π² + π⁴/45) = 6.453143735558639…,
    G₀ = ||∇u₀||₂²,
    δ = ν − C₀ sqrt(G₀).

**Proposition.** If `δ>0`, then for every Fourier ball cutoff `N`, the
Galerkin solution `u_N` satisfies, for all `t≥0`,

    ||∇u_N(t)||₂² ≤ ||∇u_N(0)||₂² exp(−2δt) ≤ G₀ exp(−2δt),

and

    ∫₀^∞ ||Δu_N(t)||₂² dt ≤ G₀/(2δ).

The constants do not depend on `N`; they are not claimed to be sharp.
Passing to the standard strong-solution limit gives a global smooth
solution for smooth `u₀` under this smallness condition, with the
corresponding estimates. The claim makes **no assertion** for data
violating the sufficient condition.

## Proof, including the zero mode and every factor

Write `u=u_N` and `v=u−m`. The projected finite ODE is

    ∂ₜu + Q_N 𝓟[(u·∇)u] = νΔu,

where `Q_N` keeps `|k|≤N`, `𝓟` is the Leray projector, and the initial
coefficients satisfy `a_{−k}=conj(a_k)` and `k·a_k=0`. Both projectors
are orthogonal for the normalized L² inner product; `−Δu` belongs to
their range. Define `G=||∇u||₂²`, `D=||Δu||₂²`, and `B=(u·∇)u`.
Testing the ODE against `−Δu` therefore gives **exactly**

    (1/2) G' + νD = <B·Δu>.

The constant mean contributes nothing:

    <[(m·∇)u]·Δu>
      = −(1/2) <m·∇|∇u|²> = 0.

Consequently, Cauchy–Schwarz and Hölder give

    |<B·Δu>| = |<[(v·∇)u]·Δu>|
             ≤ ||v||∞ ||∇u||₂ ||Δu||₂.

For a Fourier polynomial `v=Σ_{0<|k|≤N} a_k exp(ik·x)`, vector-valued
triangle and Fourier Cauchy–Schwarz give

    ||v||∞ ≤ Σ_{k≠0}|a_k|
           ≤ (Σ_{k≠0}|k|⁻⁴)^(1/2)
             (Σ_k |k|⁴ |a_k|²)^(1/2)
           = sqrt(S) sqrt(D).

To bound the infinite lattice sum `S`, group integer vectors by
`|k|∞=n`. The shell has exactly

    (2n+1)³ − (2n−1)³ = 24n²+2

points, each satisfying `|k|≥n`. Thus

    S = Σ_{k∈Z³\{0}} |k|⁻⁴
      ≤ Σ_{n=1}^∞ (24n²+2)/n⁴
      = 24ζ(2)+2ζ(4)
      = 4π²+π⁴/45 = C₀².

It follows that

    (1/2) G' + [ν−C₀ sqrt(G)]D ≤ 0.                 (1)

`Q_N` cannot increase `G` at `t=0`, so `G(0)≤G₀`. When `δ>0`, continuity
and (1) imply that `G(t)` never exceeds `G(0)`: until a first putative
exit, the bracket is at least `δ>0` and `G'≤0`, which precludes exit.
Hence `ν−C₀ sqrt(G(t))≥δ` and

    (1/2) G' + δD ≤ 0.                                (2)

The torus has smallest nonzero `|k|=1`, and the zero mode contributes
neither `G` nor `D`; therefore `D≥G`. Apply this to (2) and integrate
to obtain `G(t)≤G(0)exp(−2δt)`. Integrating (2) on `[0,∞)` yields
`∫D≤G(0)/(2δ)≤G₀/(2δ)`. These are uniform in `N`.

For clarity on the PDE step: on each finite time interval, the estimates
bound `u_N` in `L∞_t H¹_x ∩ L²_t H²_x`. The spatial mean remains `m`.
The already proved inequality `||u_N−m||∞≤C₀||Δu_N||₂` also yields

    ||(u_N·∇)u_N||₂
      ≤ (|m|+C₀||Δu_N||₂) ||∇u_N||₂,

which is bounded in `L²_t L²_x` on finite intervals. The ODE therefore
bounds `∂ₜu_N` in `L²_t L²_x`. On the torus the inclusion
`H²_x ⊂ H¹_x` is compact and `H¹_x ⊂ L²_x` is continuous. Applying
the Aubin–Lions compactness lemma with these three spaces gives,
after taking a subsequence, strong convergence in `L²_t H¹_x` on
every finite time interval. This suffices to pass to the quadratic
term in the equation; weak lower semicontinuity carries the displayed
estimates to the limit. A diagonal subsequence handles all finite
time intervals. The standard periodic `H¹` local theory, uniqueness,
continuation, and parabolic smoothing of smooth data identify this
limit with a global smooth solution. This passage invokes established
compactness and PDE theory; the explicit finite-N estimate and its
lattice constant were proved above.

## Numerical cross-check and its limits

Re-running the archived `small_data_bound.py` reproduced
`small_data_results.json` exactly. Direct enumeration of the first
four `|k|∞` shells gave 26, 98, 218, 386 points, agreeing with
`24n²+2`. For the archive's six-mode test field,
`G_base=39.58981376265963` and `ν=0.1`; hence the sufficient
amplitude is strictly below `0.002462844159697669`. The separate
general threshold is `||∇u₀||₂<ν/C₀≈0.01549632304778396` when
`ν=0.1`. Numerical examples illustrate the proposition; the proof
does not depend on them.

## Claim boundary and review question

The proved statements are the explicit lattice upper bound, the
cutoff-independent invariant region, and its resulting decay and
integrated dissipation estimate. This is a classical small-data
argument with a deliberately loose explicit constant. It supplies no
time-uniform bound for arbitrary-size data, no regularity criterion
outside this basin, and no solution of the unrestricted periodic
three-dimensional problem.

An external reviewer can check, in order: the shell count and
normalization; the sign of `<B·Δu>` in (1); cancellation of the mean;
the invariant-region step; the factor `2δ` in decay; and the standard
strong-solution limit. The statement is complete enough to be
criticized on those specific points without trusting its numerical
script.

## Primary context

- C. L. Fefferman, *Existence and Smoothness of the Navier–Stokes
  Equation*, in Clay Mathematics Institute, *The Millennium Prize
  Problems*, official formulation (B):
  https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf
- T. Tao, *A quantitative formulation of the global regularity problem
  for the periodic Navier–Stokes equation*, Proposition 2.2 and
  discussion of small `H¹` data:
  https://arxiv.org/pdf/0710.1604
