# WP11 draft PR #27: mathematical review gate

**25 September 2026 — Prince Upadhyay, Independent Research**

**Scope:** audit the new signed transfer identity, the fixed-band low-advector proof, and the exact statement of the open high-advector target. This gate reviews a proof design; it does not certify global smoothness.

## Review order and pass criteria

1. **Fourier convention and sign.** Check `src/evolve_galerkin.py`: the nonlinear coefficient is `+i P_k Σ_{p+q=k}(q·a_p)a_q`, while the equation uses its negative. The budget has `N=−Re<Au,A(u·∇u)>`. Every restricted sum includes all ordered pairs within the Fourier ball. The `p` split restricts the *advecting* input, not the output shell.
2. **Symmetrized identity.** With `A` real, even, and positive as defined in WP11, check that divergence-free transport is skew-adjoint on the real pairing. Its consequence is the **difference of squared symbols**, `m(k)^2−m(q)^2`, with prefactor `−1/2`. At positive fixed radius the squared symbol is `e^{2σ|k|}|k|^{2s}`. The radius derivative is absent from this instantaneous identity.
3. **Fixed-band lemma.** At `σ=0`, `s>3/2`, and integer `K≥1`, check the mean-value bound, the mean-zero exclusion of `q=0`, the zero output contribution, and the shifted Cauchy–Schwarz sum. The explicit bound is `|N_N^{≤K}|≤sK(1+K)^{s−1}√M_K ||u_N||₂ X_N`, where `M_K=#{p∈ℤ³:0<|p|≤K}`. The coefficient may grow with K; K must be selected without depending on N. This is a standard finite-band commutator estimate.
4. **Numerical cross-check.** From the repository root run `python3 src/wp11_review_audit.py`. The script independently compares `System.nonlinear` with the squared-symbol triad formula, checks the low-mode split against its symmetrized and commutator forms, and samples the proven L1 bound. It checks N=4 and N=7, K=1 and K=2, σ=0 and σ=0.2, and t=0 and t=0.0025 using the existing perturbed initialization. Require normalized discrepancies below `2e−12`; only `σ=0` samples claim L1. A finite passing sample is a regression check, not proof of L1 or L2.
5. **Open claim and continuation.** L2–L3 must stay labeled as unproved and must require `b_{N,K}≥0` with an independently established uniform time integral. No measured phase drift or transfer ratio implies that bound. For the conditional Grönwall conclusion, the initial `X_N(0)` is uniformly bounded by the given smooth datum, and the `s>3/2` continuation step remains conditional on proving L2–L3. A later Gevrey extension needs separate `σ'Z` control, especially at initialization.

## Observed finite-cutoff review output

The audit completed all 16 snapshots/parameter combinations. The largest normalized direct-versus-symmetrized discrepancy was `5.09e−15`; the largest low-mode discrepancy was `1.77e−15`; the largest sampled `|N_N^{≤K}|/(C_s(K)||u_N||₂ X_N)` was `0.001161`. At the original N=4, t=0, σ=0.2 checkpoint, direct and symmetrized values were `4208.027871404247` and `4208.027871404245`. The values are evidence of consistency in these finite computations only.

## Merge decision

The identity, lemma, and statement of the open target have passed this internal review. Draft PR #27 can be considered for merge as a **proof-design and finite-band lemma package**, subject to independent mathematical review of the displayed proof. Do not represent the high-frequency one-sided estimate, phase-muting mechanism, or arbitrary-data continuum regularity as achieved.
