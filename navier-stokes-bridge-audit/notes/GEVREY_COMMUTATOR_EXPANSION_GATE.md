# Gevrey commutator expansion: an exact Fourier and shell blueprint

**Prince Upadhyay, Independent Research — draft analytical gate, 25 September 2026**

**Scope:** unforced periodic 3D Navier–Stokes on `[0,2π)^3`, zero-mean real divergence-free Galerkin fields. The identities below are exact at every finite cutoff. No large-data estimate or continuum analyticity radius is proved.

## 1. Multiplier and transport cancellation

Let `A=A_{σ,s}` have real even Fourier symbol `m(k)=exp(σ|k|)|k|^s` for `k≠0`, and `m(0)=0`, with `σ≥0` and `s>3/2`. At a fixed time, set `v=Au`, `X=||v||₂²`, `Y=||∇v||₂²`. Let `B=(u·∇)u`, `Q_N` be the ball cutoff, and `P` the Leray projector. Because `v` is real, divergence-free, and already in the Galerkin range,

    N_{σ,s} = −Re <v,A Q_N P B> = −Re <v,A B>.

Define `[A,u·∇]u = A((u·∇)u) − (u·∇)(Au)`. The real part of `<v,(u·∇)v>` vanishes by periodic integration and `div u=0`. Hence

    N_{σ,s} = −Re <Au,[A,u·∇]u>.                           (1)

This is a cancellation identity, not an estimate. It does not state that the right side is small or negative. A nonzero spatial mean may be removed by a Galilean transform; this note uses the repository's zero-mean fields.

## 2. Exact multiplier difference

With `k=p+q` and the repository's ordered-pair convention,

    ([A,u·∇]u)^∧_k
      = i Σ_{p+q=k} (q·a_p) [m(k)−m(q)] a_q.               (2)

Pairing this with `m(k) conj(a_k)` gives the exact cubic sum for (1). Inserting `P_k` on the summed vector does not change the pairing because `a_k` is transverse. The only relevant terms have retained output `|k|≤N`; the full product may also have outputs beyond `N`, which are orthogonal to `Au` in this **global** inner product. Do not drop the corresponding residual from a separately localized physical-space identity.

The difference contains both a Sobolev and an exponential part:

    m(k)−m(q)
      = exp(σ|q|)(|k|^s−|q|^s)
        + |k|^s[exp(σ|k|)−exp(σ|q|)].                    (3)

The second term is zero only when `σ=0` or the two magnitudes happen to agree. A proposed commutator estimate that retains only the polynomial difference has omitted a real contribution.

## 3. A square-partition shell expansion

Let real even smooth multipliers `ψ_j(k)` satisfy `Σ_j ψ_j(k)^2=1` on all nonzero retained modes, as in `src/smooth_commutator_gate.py`. Write `A_j=P_j A` with symbol `m_j(k)=ψ_j(k)m(k)`. For each shell define

    N_j = −Re <A_j u,A_j B>.

Then `Σ_j N_j=N_{σ,s}` exactly, and the same transport cancellation gives

    N_j = −Re <A_j u,[A_j,u·∇]u>,

    ([A_j,u·∇]u)^∧_k
      = i Σ_{p+q=k}(q·a_p)[m_j(k)−m_j(q)]a_q.            (4)

Equation (4) is the cross-frequency commutator remainder. Its shell difference includes both `ψ_j(k)−ψ_j(q)` and the *full* Gevrey symbol difference. Neither `N_j` nor the commutator remainder has a fixed sign. Summing shell terms in absolute value would erase the cancellations one hopes to use.

This expansion is **not** the repository's local enstrophy strain commutator `R_{j,N}=<P_j ω,[P_j,S]ω>`. That identity concerns different operators and an unweighted vorticity budget. Relating it to (4) requires an additional derived identity, including any stretching, pressure/projection, and localization terms; matching both objects only by the word “commutator” is invalid.

## 4. What a useful new bound must accomplish

The weighted Galerkin budget is

    (1/2)X' + νY = N_{σ,s} + σ'Z,  Z=Σ e^{2σ|k|}|k|^{2s+1}|a_k|².

For `σ=0`, one sufficient large-data target on every finite horizon is

    ∫₀ᵀ Σ_j N_j(t) dt
      ≤ θν∫₀ᵀY(t)dt + F_s(T,ν,u₀),  0≤θ<1,             (5)

with `F_s` finite for every finite `T`, specified from prior data and parameters, and independent of `N` or an unknown trajectory norm. This would give a cutoff-uniform finite-time `H^s` bound for arbitrary smooth data. Equation (4) alone does not imply (5); standard termwise estimates lead back to the large-data factor `C_s^G sqrt(X)Y` from PR #23.

For a growing radius, a corresponding estimate must also control `∫σ'Z`. Although `Z≤sqrt(XY)`, Young's inequality bounds `σ'Z` by a portion of `νY` **plus** a multiple of `(σ')²X/ν`. Under `σ(t)=α sqrt(νt)`, `(σ')²` behaves like `1/t` near zero. A naive integration starting at `t=0` is therefore circular or divergent for nonzero `X(0)`. A separate initial-layer argument, different radius schedule, or a proof starting at positive time is required before claiming a uniform positive analyticity radius.

## 5. Verification and rejection tests

The companion `src/gevrey_commutator_identity_audit.py` compares (1), (2), and the sum of (4) against `System.nonlinear` for the matched repository states. It checks `Σψ_j²=1`, both radius schedules, `N=4` and `N=7`, and `σ=0`. Algebraic closure in finite arithmetic verifies the bookkeeping, not inequality (5). Any candidate for (5) must also be checked against sign reversal, amplitude and integer-frequency scaling, and time-integrated transfer before a proof is attempted.

An executed `s=2`, `ν=0.1`, `dt=0.0005`, `t∈{0,0.005}` check for the reference and combined perturbed fields is recorded in `src/gevrey_commutator_identity_verified_summary.json`. Its worst relative nonlinear reconstruction discrepancy is `4.74e-15`, worst relative transport cancellation residual `1.29e-15`, worst shell identity discrepancy `4.17e-15`, and worst square-partition error `3.34e-16`. These numbers validate the finite arithmetic only; they do not favor a sign for the integrated transfer.

## Primary context

- Foias and Temam, *Gevrey class regularity for the solutions of the Navier–Stokes equations*, J. Funct. Anal. 87 (1989): https://www.sciencedirect.com/science/article/pii/0022123689900153 . The present finite-cutoff algebra is not claimed to originate the Gevrey approach.
- Tao, *A quantitative formulation of the global regularity problem for the periodic Navier–Stokes equation*: https://arxiv.org/abs/0710.1604 .
