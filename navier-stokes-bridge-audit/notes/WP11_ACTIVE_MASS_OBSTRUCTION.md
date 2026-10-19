# WP11: active triad mass and zero-mode activation

**Prince Upadhyay, Independent Research — 25 September 2026**

**Scope:** exact zero-radius Fourier-Galerkin identities and requirements for a future high-tail one-sided estimate. These statements do not prove an arbitrary-data bound as the cutoff tends to infinity.

## 1. What the Colab “mass” is

For `k=p+q` with `|p|>K`, write the **ordered triad** complex transfer

    z_{kpq}=−i |k|^{2s}(q·a_p)(conj(a_k)·a_q),
    N_high=Σ Re z_{kpq}.

At any snapshot select an active set `I` with `z≠0` and write `z=Ae^{iφ}`. The audit calls `M=Σ_I A` the *active triad magnitude sum*. It is a nonnegative accounting quantity, **not a fluid mass, a matrix, or a conserved quantity**. It depends on how the ordered convolution is decomposed and on the numerical threshold defining `I`. In particular `|z₁|+|z₂|` need not equal `|z₁+z₂|`. Nothing in its positivity gives a sign for the total `N_high`.

For a fixed active set at an instant, the exact derivative is

    dN_high/dt = M_dot μ + M[Cov_A(cosφ,A_dot/A)
                     − E_A(sinφ φ_dot)] + R_inactive,
    μ=E_A(cosφ),
    R_inactive=Σ_{not in I} Re z_dot.                 (A1)

The terms in (A1) may have either sign. A threshold crossing changes the set, so (A1) is a **snapshot derivative at fixed membership**. It does not by itself integrate to a time-interval formula with a moving threshold. In the all-nonzero case `R_inactive=0` and `N_high=M μ`; the signed mean alignment `μ` still has no guaranteed sign or magnitude.

## 2. A proved positive activation contribution

Let `B_k=P_k Σ_{p+q=k}i(q·a_p)a_q` be positive advection, and split it by the *advecting* index p into `B_k=L_k+H_k` for `|p|≤K` and `|p|>K`. Thus `a_dot_k=−B_k−ν|k|²a_k` and

    N_high=−Σ_k |k|^{2s} Re(conj(a_k)·H_k).

At a time `t₀` when `a_k(t₀)=0`, the **k-output contribution** has the exact derivative

    d[-|k|^{2s} Re(conj(a_k)·H_k)]/dt at t₀
      = |k|^{2s} Re(conj(L_k+H_k)·H_k).             (A2)

Indeed, the term containing `H_dot_k` vanishes because `a_k=0`; substitute `a_dot_k=−(L_k+H_k)`. In the clean case `L_k=0`, (A2) becomes

    |k|^{2s}|H_k|² ≥ 0.                              (A3)

The triadic phase is undefined at `a_k=0`. Formula (A3) proves that new output modes can supply positive initial transfer growth *without any existing phase angle to rotate*. If both `L_k` and `H_k` are present, the cross term `Re(conj(L_k)·H_k)` has no universal sign. This is an instantaneous lemma, not an assertion that growth persists for a finite interval or outruns viscosity.

On the stored combined perturbed initialization at `s=2, K=2`, an independent `System.nonlinear` and p-split check found 6 clean new outputs at N=4 and 18 at N=7. Their summed (A3) contributions were about `7.329e4` and `1.193e7`, respectively, with largest per-mode algebra residuals `9.1e−13` and `2.4e−10` before normalization. These finite snapshots illustrate (A3); the exact proof is (A2)–(A3).

## 3. What the uploaded trajectory does and does not show

The uploaded `wp11_phase(1).json` matches the earlier short Colab run. At N=7 and `t=0.0005`, the four terms of (A1) are approximately `+7.436e6`, `+5.786e6`, `−1.495e3`, and `−0.17`. At `t=0.005`, they are `+14.792e6`, **`−1.711e6`**, `+8.101e3`, and `−0.21`. Initially inactive triads at N=7 supply about `+13.291e6` to the derivative at `t=0`; these are not a measurement of a continuum production rate. The covariance is positive early but negative later while signed transfer continues to rise. The plotted phase term is small relative to large N=7 amplitude terms on this window; this does **not** establish that phase dynamics is universally too weak. Under another initial condition or cutoff it may behave differently.

The reported scaling residual `0.0` uses the invariant image sublattice and dyadic `λ=2`, both of which intentionally preserve the indexed arithmetic. It checks a **zero-radius Sobolev diagnostic**, not a positive-σ Gevrey transfer `N_{σ,s}`. It certifies covariance of these sampled discrete trajectories under `N,K→λN,λK`, `t→t/λ²`; it does not show independent continuum-limit convergence.

## 4. Requirements for a genuine estimate

The actual WP11 target is still a one-sided signed inequality on **every prefix** `[0,t]`, uniform in N, with a dissipation reserve or another independently controlled Grönwall coefficient. A proposal based on (A1) must explicitly account for

1. the `M_dot μ` term, with a justified time-integrated bound;
2. the signed amplitude covariance, which can change sign;
3. the signed `sinφ φ_dot` term without dividing by phase velocities at their zeros;
4. activation of triads with `z=0`, including the positive clean-output contribution (A3);
5. a moving threshold's crossings or a threshold-free limiting argument;
6. correct scaling of K, time, viscosity and every proposed coefficient; and
7. a cutoff-independent continuation step from the proven inequality.

It is enough to bound the **combined signed transfer**; one need not bound every term separately if a rigorous cancellation argument controls their total. Equations (A1)–(A3) supply exact accounting and a falsification gate for phase-only claims, not the missing global theorem. Draft PR #27 should remain labeled as such.
