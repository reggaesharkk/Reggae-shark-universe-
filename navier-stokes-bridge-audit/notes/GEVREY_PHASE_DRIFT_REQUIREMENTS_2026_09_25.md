# Gevrey phase drift: analytical requirements before a tracker

**Prince Upadhyay, Independent Research — draft gate, 25 September 2026**

**Scope:** unforced periodic 3D Navier–Stokes; finite Galerkin diagnostics. No phase-muting theorem or arbitrary-data regularity claim.

## 1. Baseline and correction

PR #22 verifies the weighted Galerkin identity. PR #23 proves the cutoff-independent product bound

\[
|\mathcal N_{\sigma,s}|\le C_s^{G}X_{\sigma,s}\sqrt{Y_{\sigma,s}}
\le C_s^{G}\sqrt{X_{\sigma,s}}Y_{\sigma,s},\qquad s>3/2,
\]

where `C_s^G=2c_s(Σ_{m≠0}|m|^{-2s})^{1/2}` does not depend on the cutoff or exponential radius. A sampled quotient increasing from `N=4` to `N=7` does not make this constant cutoff dependent. For large `X`, the resulting weighted inequality does not absorb the nonlinear term into viscosity. That is the remaining gap.

The two radius schedules in PR #22 are weights used to evaluate *the same physical trajectory*. Changing the schedule alone is not evidence that viscosity changed or damped that trajectory. Comparisons must include the changing `X`, `Y`, and weights, not just a quotient of quotients.

## 2. Exact objects to measure

Use `k=p+q`, repository Fourier normalization and Leray projector `P_k`. For each ordered, nonzero, retained triad set

\[
z_{kpq}=\widehat u_k^*\cdot P_k[(q\cdot\widehat u_p)\widehat u_q],
\qquad w_k=e^{2\sigma|k|}|k|^{2s}.
\]

Then the existing nonlinear transfer satisfies exactly

\[
\mathcal N_{\sigma,s}=\sum_{k=p+q} w_k\operatorname{Im}z_{kpq}.
\]

For `z≠0`, define its instantaneous angular velocity by

\[
\dot\phi_{kpq}=\frac{\operatorname{Im}(\overline z_{kpq}\dot z_{kpq})}{|z_{kpq}|^2},
\]

with `dot z` obtained by the product rule from the same Galerkin ODE as PR #22. This is an identity on intervals where `z≠0`; it says nothing by itself about the sign of transfer. At a zero of `z`, phase is undefined. Store real and imaginary parts, amplitude and derivative; do not divide there or unwrap across a zero. Apply a declared relative amplitude floor only for displaying phase rates and report its sensitivity. Any raw transfer sum must include all triads, including ones excluded from a phase-rate display.

Define an *instantaneous cancellation diagnostic* when its denominator is positive:

\[
Q_N(t)=\frac{|\sum w_k\operatorname{Im}z_{kpq}|}
{\sum w_k|z_{kpq}|}\in[0,1].
\]

Set `Q_N` undefined when the denominator vanishes. Do not call a small `Q_N` a universal regularity mechanism. It may reflect one trajectory, exact symmetries, or phase cancellation at one instant. Retain the signed `\mathcal N`, absolute sum, `X`, `Y`, `Z`, and both majorant quotients from PR #23 alongside `Q_N`.

## 3. Validation gate for an executable tracker

1. Reconstruct `\mathcal N` by summing the displayed triads and compare with the independently computed nonlinear term from the repository system at every checkpoint. Include reality-conjugate and ordered-pair multiplicities exactly once according to the repository convention.
2. Compare `dot z` from product differentiation of the Galerkin RHS with centered differences of complex `z` away from endpoints and zeros. State truncation and time-step errors separately from algebraic residuals.
3. Verify invariance of `\mathcal N` and `Q_N` under spatial translations. A translation changes each `a_j` by `e^{ij·x_0}` and leaves `z_{kpq}` invariant because `k=p+q`.
4. Check `u→−u` at a fixed instant: `z` and signed `\mathcal N` change sign, while `Q_N` does not. Compute `dot z` separately for each sign-reversed initial state: the Navier–Stokes flow is not invariant under `u→−u`, so the resulting angular rates need not agree. This blocks interpreting an instantaneous cancellation ratio as a sign predictor.
5. Compare matched `N=4` and `N=7` initial data and both prescribed radius schedules, recording whether high-frequency perturbations differ. Do not infer an `N→∞` limit from two cutoffs.
6. Show time series of signed transfer and the interval integral of that transfer. A histogram of rapid phase rates alone cannot establish cancellation of the signed integral, since amplitudes and weights evolve too.


## 4. Scaling and the sufficient space-time target

The 3D Navier–Stokes equation (with the same viscosity) has the scaling

\[
u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t).
\]

Here \(u_\lambda\) denotes a rescaled velocity; it is not the viscosity \(\nu\). For integer \(\lambda\), periodicity is retained on the same torus. The suggested \(\lambda^{3/2}v(\lambda x)\) is an \(L^2\)-preserving spatial rescaling on \(\mathbb R^3\), not the Navier–Stokes scaling, and on the torus the integer dilation repeats the field rather than changing the domain volume. Under the integer torus scaling at \(t=0\), \(X_{\sigma/\lambda,s}(u_\lambda)=\lambda^{2s+2}X_{\sigma,s}(u)\), \(Y_{\sigma/\lambda,s}(u_\lambda)=\lambda^{2s+4}Y_{\sigma,s}(u)\), and the weighted nonlinear injection scales as \(\lambda^{2s+4}\mathcal N_{\sigma,s}(u)\). A proposed inequality must respect these powers (and its time integral scales with an additional \(\lambda^{-2}\) under \(t\mapsto\lambda^2t\)).

A statement merely asserting \(\int_0^{T_*}\mathcal N(t)\,dt<\infty\) is automatic for every finite Galerkin trajectory on a finite interval and is not a useful proof target. One **sufficient template to investigate**, for a fixed radius \(\sigma=0\), is the following estimate for each finite \(T\) and all Galerkin cutoffs:

\[
\int_0^T\mathcal N_{0,s}(t)\,dt
\le \theta\nu\int_0^T Y_{0,s}(t)\,dt
+F_s(T,\nu,u_0),\qquad 0\le\theta<1.
\]

Here \(F_s\) must be finite for every finite \(T\), computable from specified initial norms and parameters, and independent of \(N\) and any unknown solution norm on \([0,T]\). The weighted identity would then give \(X_{0,s}(T)/2+(1-\theta)\nu\int_0^T Y_{0,s}\le X_{0,s}(0)/2+F_s\). With \(s>3/2\), a genuinely proved version of this bound for arbitrary smooth data would yield a uniform high-norm bound on every finite interval and enable standard continuation. This is a research target, not a result of phase tracking; it may be as hard as the original problem.

For time-varying \(\sigma\), the extra \(\int\sigma'Z\,dt\) must also be controlled without a cutoff-dependent or circular bound. A measured small phase-cancellation ratio or large angular velocity does not establish either required inequality.

## 5. Proof gate after measurement

The mechanism would require a *stated theorem candidate*: for example, a bound on the positive nonlinear injection integrated over a time interval, with its exact dependence on `X`, `Y`, `ν`, initial data and interval length. Prove every constant independent of `N` and close the resulting energy estimate for arbitrary smooth data before drawing a global-regularity conclusion. If the proposed inequality only holds when a smallness or coherence assumption is imposed, state that restriction. Numerical phase drift, even when reproduced, supplies a diagnostic and cannot supply the universal bound.

## 6. Executed finite-Galerkin tracker

Run `python3 src/gevrey_phase_drift_tracker.py` from the repository root; the concise executed record is `src/gevrey_phase_drift_verified_summary.json`. The script uses s=2, ν=0.1, dt=0.0005, t in [0,0.005], the reference and combined perturbed fields, both N=4/N=7, and the two PR #22 weight schedules. Each weight evaluates the same evolved state within a case.

The worst relative reconstruction error for the signed weighted nonlinear transfer was 5.37e-15. A centered complex-triad derivative check at N=7 improved from 1.19e-8 to 2.97e-9 in the reference case and from 3.76e-7 to 9.40e-8 in the perturbed case when its test step was halved from 1e-5 to 5e-6. Translation invariance and sign reversal were checked to approximately 7.1e-14 and zero, respectively.

At t=0.005, the perturbed persistence-weight cancellation ratio Q was approximately 0.0704 (N=4) and 0.4083 (N=7); the corresponding parabolic-weight values were 0.0715 and 0.2743. The signed transfer integrals over [0,0.005] were positive in all four perturbed cases, with magnitudes recorded in the JSON. These are trajectory-dependent weighted diagnostics. They do not show that phase drift forces cancellation as cutoff grows; in this comparison Q is *larger* at N=7. Nor is a positive integral on a short track evidence of singularity.

The relative phase-rate floor controls only which individual angular rates are displayed. All ordered triads, including those below the display floor, contribute to the reconstructed transfer, absolute envelope, Q, and time integral.

## 7. Phase law, viscous contribution, and commutator boundary

For a nonzero scalar component c_k in a *fixed* transverse frame, the Galerkin equation gives

\[
\frac{d}{dt}\arg c_k
=\operatorname{Im}\frac{\dot c_k}{c_k}
=-\operatorname{Im}\frac{B_k^{\rm component}}{c_k}.
\]

The term \(-\nu|k|^2c_k\) has a real multiplier and contributes **zero** to this instantaneous angular rate. For a full complex vector coefficient, the scalar \(\operatorname{Im}(\widehat u_k^*\cdot\dot{\widehat u}_k/|\widehat u_k|^2)\) tracks a particular common complex phase; it does not encode both transverse polarizations or vorticity–strain orientation. The phase of the actual scalar interaction \(z_{kpq}\) in Section 2 avoids substituting this common phase for the interaction geometry. In general its angle is *not* simply \(\theta_k-\theta_p-\theta_q\): the contractions \(q\cdot\widehat u_p\) and \(\widehat u_k^*\cdot P_k\widehat u_q\) also have phases and can vanish.

The product rule gives the exact **direct viscous** contribution
\[
\dot z_{kpq}\big|_{\rm visc}
=-\nu(|k|^2+|p|^2+|q|^2)z_{kpq}.
\]
Consequently \(\operatorname{Im}(\overline z\,\dot z|_{\rm visc})/|z|^2=0\) wherever \(z\ne0\). The updated executable checks this identity on the stored initial fields: the maximum absolute product-rule residual is below \(3.5\times10^{-14}\), and the largest computed direct viscous phase rate on active triads is below \(2.7\times10^{-16}\). **This does not remove viscosity from the full phase dynamics:** viscous amplitude changes alter later nonlinear interactions.

The observed \(Q_N\) change \(0.4083-0.0704\approx0.3379\) is about **33.8 percentage points**. \(Q_N\) is an absolute-ordered-triad normalization of weighted \(H^s\) transfer. At \(s=2\), it is neither a measured efficiency of local vortex stretching nor a geometric alignment angle. The matched \(N=4/N=7\) simulations share initial modes but evolve under different Galerkin systems, so the discrepancy alone does not identify a causal high-mode population mechanism.

The repository's space-time strain commutator decomposes unweighted enstrophy stretching into shell terms. Its remainder \(\mathcal R_{j,N}\) is not identical to the Gevrey \(H^s\) transfer \(\mathcal N_{\sigma,s}\). A proposed bridge must first write a correct weighted identity with explicit shell multipliers, projection and boundary terms, then prove an inequality such as the cutoff-uniform template in Section 4. A covariance between phase rate and stretching is descriptive: without a sign, integration-by-parts estimate, or equivalent uniform bound, it cannot close that inequality.
