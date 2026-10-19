# Gevrey Lower-Bound Gate v0.2: Cutoff-Uniform Analyticity

**Author:** Prince Upadhyay, Independent Research  
**Version:** 0.2, 25 September 2026  
**Target:** Cutoff-uniform Gevrey bookkeeping and nonlinear-estimate audit for periodic 3D Navier-Stokes  
**Status:** Exact finite-Galerkin identity plus validation prerequisites; no continuum analyticity lower bound claimed.

## 1. Standardized Fourier convention

The repository uses

\[
u(x)=\sum_k \widehat u_k e^{ik\cdot x},
\qquad
k=p+q,
\]

with the projected advection coefficient

\[
\widehat{B(u,u)}_k
=
iP_k
\sum_{p+q=k}
(q\cdot \widehat u_p)\widehat u_q .
\]

The Galerkin ODE is

\[
\partial_t\widehat u_k
=
-\widehat{B(u,u)}_k
-\nu |k|^2\widehat u_k.
\]

This matches the repository Galerkin implementation.

## 2. Gevrey-Sobolev functionals

For \(s>3/2\), \(\sigma(t)\ge0\), and the nonzero Fourier modes, define

\[
X_{\sigma,s}
=
\sum_k e^{2\sigma |k|}|k|^{2s}|\widehat u_k|^2,
\]

\[
Y_{\sigma,s}
=
\sum_k e^{2\sigma |k|}|k|^{2s+2}|\widehat u_k|^2,
\]

\[
Z_{\sigma,s}
=
\sum_k e^{2\sigma |k|}|k|^{2s+1}|\widehat u_k|^2.
\]

The zero mode contributes zero to these homogeneous quantities for \(s>0\).

Define the signed weighted nonlinear injection

\[
\mathcal N_{\sigma,s}
=
-\operatorname{Re}
\sum_k
e^{2\sigma |k|}
|k|^{2s}
\widehat u_k^*
\cdot
\widehat{B(u,u)}_k.
\]

Then direct differentiation along the finite Galerkin ODE gives the exact identity

\[
\boxed{
\frac12\frac{d}{dt}X_{\sigma,s}
+
\nu Y_{\sigma,s}
=
\mathcal N_{\sigma,s}
+
\sigma'(t)Z_{\sigma,s}.
}
\]

This identity is finite-dimensional bookkeeping. Its usefulness for the PDE depends on estimates whose constants remain independent of the cutoff \(N\).

## 3. Cutoff-uniform nonlinear-estimate target

The proof-level target is not a fitted spectral tail. It is a bound of the form

\[
|\mathcal N_{\sigma,s}|
\le
\Phi(X_{\sigma,s},Y_{\sigma,s},E,G,\nu)
\]

with every structural constant independent of \(N\).

The exponential weight is submultiplicative because for \(k=p+q\),

\[
e^{\sigma|k|}
\le
e^{\sigma|p|}e^{\sigma|q|}.
\]

Termwise absolute values therefore do not automatically force cutoff divergence. Whether a useful cutoff-uniform estimate closes depends on the precise convolution/Sobolev inequality.

The present audit records several descriptive cubic ratios only to expose finite-\(N\) behavior. None is registered as a theorem candidate until derived analytically.

## 4. Radius schedules

Two distinct schedules are kept separate.

### A. Persistence of pre-existing analyticity

For \(\sigma_0>0\),

\[
\sigma_A(t)=\max(\sigma_0-\gamma t,0),
\qquad
\sigma_A'(t)=
\begin{cases}
-\gamma,&\sigma_0-\gamma t>0,\\
0,&\text{otherwise}.
\end{cases}
\]

This tests persistence of an already positive exponential weight.

### B. Positive-time parabolic smoothing schedule

For Sobolev initial data with \(\sigma(0)=0\),

\[
\sigma_B(t)=\alpha\sqrt{\nu t},
\qquad t>0,
\]

\[
\sigma_B'(t)=\frac{\alpha\nu}{2\sqrt{\nu t}}.
\]

The derivative is singular at \(t=0\), so the identity audit begins this schedule at the first positive time step. This schedule is a testing weight, not by itself a proven analyticity lower bound.

## 5. Executable validation requirements

The companion executable audit must:

1. use the real repository System and make_initial routines;
2. compute \(X,Y,Z,\mathcal N\) directly from the Fourier state;
3. compute \(dX/dt\) exactly from the Galerkin RHS and moving weight;
4. verify the boxed identity to floating-point precision;
5. independently cross-check the same derivative with centered finite differences;
6. compare matched \(N=4\) and \(N=7\) trajectories;
7. report descriptive nonlinear ratios without interpreting finite stability as cutoff-uniform proof.

## 6. Interpretation barrier

A finite Fourier-Galerkin state is a trigonometric polynomial and therefore cannot be used to infer a continuum analyticity radius by tail fitting.

A genuine lower radius requires a cutoff-uniform Gevrey estimate that survives \(N\to\infty\).

The next gate after this identity audit is therefore analytical:

> derive or reject a concrete cutoff-uniform nonlinear majorant in the weighted norm.


## 7. Executed v0.2 audit

The companion audit was executed for \(s=2\), \(\nu=0.1\), \(\Delta t=0.0005\), \(N\in\{4,7\}\), and the reference plus combined double/quarter-phase/high-frequency scenarios through \(t=0.005\).

The exact weighted identity passed with worst relative residual

\[
4.14\times10^{-15}.
\]

The centered finite-difference derivative was used only as a secondary check. The first positive smoothing step is not treated as a convergence benchmark because \(\sigma'(t)\sim t^{-1/2}\) is singular at \(t=0\). At the interior checkpoint \(t=0.0025\), the hardest combined \(N=7\) smoothing case had relative finite-difference error about

\[
1.58\times10^{-3}.
\]

For the descriptive cubic ratio

\[
R_{\rm desc}
=
\frac{|\mathcal N_{\sigma,s}|}{\sqrt{X_{\sigma,s}}\,Y_{\sigma,s}},
\]

the \(t=0.005\) combined perturbed case gave

\[
R_{\rm desc}(N=4)\approx2.23\times10^{-4},
\qquad
R_{\rm desc}(N=7)\approx4.54\times10^{-3}
\]

under the persistence weight, a sampled \(N=7/N=4\) factor of about \(20.3\).

Under the smoothing weight the same sampled factor was about \(10.3\).

These ratios are descriptive only. The finite separation does not establish divergence with \(N\) and is not a registered nonlinear majorant.

The next proof gate must derive a specific cutoff-uniform Gevrey convolution estimate analytically before using further numerical screening.
