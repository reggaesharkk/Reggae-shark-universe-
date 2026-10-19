# WP11: one-sided cross-frequency proof package

**Prince Upadhyay, Independent Research — design draft, 25 September 2026**

**Target:** unforced periodic three-dimensional Navier–Stokes, zero-mean smooth divergence-free initial data. This is a falsifiable plan for a new inequality, not a proof of arbitrary-data regularity.

## 1. Freeze the equations before computation

Use the normalized torus `[0,2π)^3` and Fourier-ball Galerkin system from `src/evolve_galerkin.py`. Write `a_k` for its real-conjugate, transverse coefficients and `k=p+q` for every ordered interaction. Fix `s>3/2` and initially set the Gevrey radius to **σ=0**. For a later positive-radius study, the moving-weight term `σ'Z` needs its own initial-layer estimate and cannot be silently folded into this package.

Let `A` be the real, even multiplier `m(k)=|k|^s` for `k≠0`, `m(0)=0`, and set

    X_N=||Au_N||₂²,  Y_N=||∇Au_N||₂²,
    N_N=−Re <Au_N,A[(u_N·∇)u_N]>.

The exact budget is `(1/2)X_N' + νY_N=N_N`. The projection and cutoff disappear inside this *global* pairing because `Au_N` is divergence-free and retained. They cannot be dropped from a separately localized physical-space balance.

## 2. A second, symmetrized exact identity

The PR #25 commutator identity has an equivalent skew-transport form:

    N_N=−(1/2)Re <u_N,[A²,u_N·∇]u_N>
       =−(1/2)Re Σ_{k=p+q} i(q·a_p)
           [m(k)²−m(q)²] conj(a_k)·a_q.                (1)

Here every sum retains `|k|,|p|,|q|≤N`, including its reality partners and ordered pairs. To derive the factor `1/2`, use the real skew-adjointness of `u·∇`: `Re<u,(u·∇)A²u>=−Re<(u·∇)u,A²u>`. A direct calculation on the repository's combined perturbed N=4 initial state at s=2 and σ=0.2 gave direct transfer `4208.027871404247` and formula (1), with `m=e^{σ|k|}|k|^s` for that cross-check, `4208.027871404245` (relative difference `4.32e−16`). This is a check of identity (1), not evidence for a one-sided bound. With a positive fixed radius, (1) uses the *entire squared symbol* `e^{2σ|k|}|k|^{2s}`; WP11's first inequality remains at σ=0.

The squared-symbol difference in (1) makes the cancellation at nearby donor and output frequencies explicit. That algebra alone does not imply a sign: the velocity coefficients carry phases, and high-high interactions need not have a small frequency difference.

## 3. Isolate a tractable low-advector contribution

Choose an integer frequency threshold `K≥1` that may depend on specified initial data, viscosity and finite horizon T, but **not** on Galerkin cutoff N or an unknown solution norm. Split the right side of (1) according to the advecting mode `p`:

    N_N=N_N^{≤K}+N_N^{>K},  using |p|≤K or |p|>K.

The low-advector lemma is **proved** for σ=0 and `s>3/2`:

    |N_N^{≤K}(t)| ≤ C_s(K) ||u_N(t)||₂ X_N(t),        (L1)
    C_s(K)=sK(1+K)^{s−1}√M_K,
    M_K=#{p∈ℤ³:0<|p|≤K}.

Indeed, writing `v=P_{≤K}u_N`, skew-adjointness of `v·∇` gives the same low-advector contribution in the unsymmetrized form

    N_N^{≤K}=−Re <Au_N,[A,v·∇]u_N>.

For `k=p+q`, `|p|≤K`, and nonzero `q,k`, the mean-value theorem and `|q|≥1` imply

    |q| ||k|^s−|q|^s|
      ≤ s|p||q|(|q|+|p|)^{s−1}
      ≤ sK(1+K)^{s−1}|q|^s.

The zero output has no contribution because `a_0=0`. Bound `|q·a_p|≤|q||a_p|`, apply Cauchy–Schwarz to the shifted `q` sum for each `p`, and then use `Σ_{0<|p|≤K}|a_p|≤√M_K ||u_N||₂`. This proves (L1) including low donor/output cases. The energy identity bounds `||u_N(t)||₂≤||u₀||₂`. The constant grows with fixed K but is independent of N. This elementary finite-band estimate makes no claim at positive Gevrey radius: differentiating the exponential symbol can cost another high-mode derivative.

Thus (L1) contributes at most `C_s(K)||u₀||₂ X_N` in the budget. This is an ordinary finite-horizon Grönwall coefficient and does not settle the high-advector problem.

## 4. Candidate large-data lemma and its precise consequence

The genuinely open WP11 candidate is a *one-sided* estimate on the remaining signed interactions: for every smooth datum and every finite horizon T, find a fixed reserve fraction `0<θ<1` and a nonnegative `b_{N,K}` such that

    N_N^{>K}(t) ≤ θνY_N(t) + b_{N,K}(t)X_N(t)       (L2)

for almost every `t∈[0,T]`, with

    sup_N ∫₀ᵀ b_{N,K}(t)dt ≤ B_s(u₀,ν,T,K)<∞.       (L3)

The construction of `b` and the bound B must use independently controlled quantities; defining `b` afterward from the unknown positive transfer is circular. No assumption of rapid phase rotation, favorable shell sign, or decay may be inserted without proof. A directly integrated alternative is acceptable if it yields the same non-circular Grönwall bound on every prefix `[0,t]`, `t≤T`.

If (L1)–(L3) held, the exact budget would give

    (1/2)X_N' +(1−θ)νY_N
      ≤ [C_s(K)||u₀||₂+b_{N,K}(t)]X_N,

and thus `sup_{t≤T}X_N(t)≤X_N(0) exp(2C_s(K)||u₀||₂T+2B_s)` uniformly in N, alongside an integrated Y bound. With s>3/2 and standard periodic continuation/compactness, this would be substantial arbitrary-data regularity progress. The elementary (L1) proof above leaves (L2)–(L3) open; they may be as hard as the original problem.

## 5. Rejection tests before any long run

1. **Dimensions and scaling.** Check each proposed C, b, and B under `u_λ(x,t)=λu(λx,λ²t)` for integer λ on the torus, including how a fixed K classifies the rescaled modes. State the viscosity and torus normalization. A bound that secretly grows with N fails.
2. **Sign and amplitude.** Test `u→−u`, then `u→A u` for large A. The transfer is cubic while X and Y are quadratic at a fixed instant; any extra coefficient must have justified amplitude dependence. A single positive-transfer field is enough to refute an overstrong universal sign claim.
3. **Sparse triads.** Use the WP1–3 nonzero-transfer triad and its dilations to challenge (L1) and (L2), with both signs. Check interactions where donor and output are far apart as well as close.
4. **Spectral bookkeeping.** Reconstruct (1) from the independent `System.nonlinear` route at finite cutoffs; distinguish a square partition for the **output energy** from any partition of the two input fields. Do not invent a favorable three-way remainder decomposition.
5. **Only then evolve.** Short N=4/N=7 trajectories can falsify a concrete proposed inequality; success cannot prove `sup_N` control. A long-time run remains descriptive until (L1)–(L3) are analytically supported.

## 6. Completion criteria and prior context

WP11 records the elementary proof of (L1). A future result may be a counterexample to a precisely stated (L2) or a proved replacement for (L2)–(L3). Mark each separately. Do not call WP11 a global Navier–Stokes solution unless a valid all-data, cutoff-uniform continuation argument is independently checked. The phrase “machine precision” applies to finite algebraic diagnostics only; it cannot certify the continuum theorem or exclude all coding mistakes.

This problem is related to classical commutator and frequency-localization methods; no novelty is claimed for the algebraic symmetrization. The sufficiency of an a priori high-norm bound for periodic global regularity is consistent with Tao's quantitative formulation (https://arxiv.org/abs/0710.1604). The preceding audited gates are `notes/GEVREY_UNIFORM_MAJORANT_GATE_2026_09_25.md`, `notes/GEVREY_PHASE_DRIFT_REQUIREMENTS_2026_09_25.md`, `notes/GEVREY_COMMUTATOR_EXPANSION_GATE.md`, and the v0.2 `MASTER_RECORD_SUPPLEMENT_2026_09_24.md`.
