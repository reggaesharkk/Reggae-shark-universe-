# WP11 high-tail coefficient gate: proved estimate and energy obstruction

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** rigorous conditional bound and a counterexample to a proposed *energy-only coefficient control*. The all-data, cutoff-independent space-time estimate L2–L3 of draft PR #27 remains open.

## 1. A rigorous high-advector estimate

Use WP11's zero-mean periodic Fourier-ball Galerkin solution, `s>3/2`, `σ=0`, `X_N=Σ_{|k|≤N}|k|^{2s}|a_k|²`, and a fixed integer `K≥1`. Set

    D_{s,K,N}(t)=Σ_{K<|p|≤N}|p|^s |a_p(t)|.

The `p`-restricted nonlinear transfer satisfies, for every cutoff and time,

    |N_N^{>K}(t)| ≤ s 2^s D_{s,K,N}(t) X_N(t).       (H1)

**Proof.** Let `w=P_{>K}u_N`. Since `w` is divergence-free, the real pairing of `Au_N` with `w·∇Au_N` vanishes, and the restricted transfer equals `−Re<Au_N,[A,w·∇]u_N>`. For `k=p+q` with nonzero `p,q,k`, the mean-value theorem gives

    |q| ||k|^s−|q|^s|
      ≤ s|p||q|(|p|+|q|)^{s−1}
      ≤ s 2^{s−1} (|p|^s|q|+|p||q|^s)
      ≤ s 2^s |p|^s |q|^s.

Here `|p|,|q|≥1`. The term with `k=0` vanishes because `a_0=0`, and `q=0` vanishes because the field has zero mean. After bounding `|q·a_p|≤|q||a_p|`, apply Cauchy–Schwarz to the shifted pair `q,k=q+p` for each `p`; its sum is at most `X_N`. Sum over `|p|>K`. Every step respects the Galerkin cutoff, and the coefficient `s 2^s` does not depend on N. This is an elementary absolute-value estimate, not a phase-cancellation theorem.

Combining (H1) with WP11's proved low-band estimate gives the **conditional continuation criterion**

    (1/2)X_N' + νY_N
      ≤ [C_s(K)||u₀||₂+s 2^s D_{s,K,N}(t)] X_N.

Thus a new, independently established bound

    sup_N ∫₀ᵀ D_{s,K,N}(t)dt < ∞                 (H2)

would yield a uniform `X_N` bound on `[0,T]` by Grönwall. It would imply WP11's L2–L3 with `b=s 2^s D_{s,K,N}` and any `0<θ<1`. **No proof of (H2) for arbitrary data is known here.** Defining the required coefficient from `D` is useful only when its integral is controlled without assuming the desired high-norm bound.

## 2. Why the standard energy budget does not supply (H2)

For arbitrarily large integer R, select a symmetric collection `S_R` of `M_R≈R³` lattice points with `R≤|p|≤2R` and `|p_1|≤R/4`. Choose real transverse coefficients along the normalized projection of `e_1` to `p⊥`, and use the same coefficient at `−p`. Normalize their common amplitude so that `||∇u_{0,R}||₂=1`. Each active amplitude is comparable to `1/(R√M_R)`. These are real, divergence-free, zero-mean *smooth finite Fourier fields*. For `R>K`, their weighted tail obeys

    D_{s,K,2R}(0) ≳ M_R R^s/(R√M_R)
                    ≍ R^{s+1/2}.

Even for the **linear heat flow** from these data, each mode decays by `e^{−ν|p|²t}`. For `0≤t≤R^{−2}`, this factor is at least `e^{−4ν}`. Consequently,

    ∫₀^{R^{−2}} D_{s,K,2R}(t)dt
       ≳ e^{−4ν} R^{s−3/2} → ∞,  since s>3/2.   (H3)

To rule out even a bound by an arbitrary function of the **exact values** of both energy-level norms, rescale the high shell to `||∇v_R||₂²=δ=1/2`, and write `h_R=||v_R||₂²=O(R^{−2})`. Add two fixed divergence-free real low Fourier pairs at frequencies of length 1 and 2. Choose their squared L² masses `x_R,y_R` by

    x_R+y_R=1−h_R,     x_R+4y_R=2−δ,
    y_R=(1−δ+h_R)/3,  x_R=(2+δ−4h_R)/3.

For large R both masses are positive. The resulting smooth fields have **exactly** `||u_{0,R}||₂²=1` and `||∇u_{0,R}||₂²=2` for every R, while their high-shell heat-flow contribution in (H3) still diverges. Thus no finite upper bound for this coefficient's integral can be a function of just these two norm values and ν, uniform over such smooth data and cutoffs. This example is about the proposed coefficient and heat flow; it is **not** a counterexample to Navier–Stokes smoothness or WP11's one-sided L2–L3, where signed cancellations may matter. Dependence on stronger norms of a *fixed* datum is also not excluded.

## 3. Next analytical gate

An actual advance beyond (H1) must control the **signed** high-advector transfer with a coefficient whose time integral follows from independently established estimates, or derive another noncircular reserve inequality directly. Test any phase-decorrelation claim against slowly rotating or phase-aligned sparse triads, parabolic dilation, and all time prefixes. The low-frequency proof and a small finite-cutoff residual cannot replace (H2) or L2–L3. A fixed positive Gevrey radius adds the exponential symbol and needs a separate commutator estimate; a moving radius also adds `σ'Z`.

For context on the strength of a uniform high-norm bound, see T. Tao, *A quantitative formulation of the global regularity problem for the periodic Navier–Stokes equation*, https://arxiv.org/abs/0710.1604. No global-regularity result is claimed here.
