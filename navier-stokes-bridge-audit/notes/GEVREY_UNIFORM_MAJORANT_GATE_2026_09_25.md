# Gevrey Uniform Majorant Gate: Cutoff-Independent Bilinear Bound

**Author:** Prince Upadhyay, Independent Research  
**Version:** 0.2, 25 September 2026  
**Target:** Explicit cutoff-independent upper bound for the Gevrey nonlinear transfer  
**Status:** Analytical majorant plus finite-Galerkin verification; no arbitrary-data global regularity claim.

## 1. Setup

Use the repository convention

\[
\widehat{B(u,u)}_k
=
iP_k\sum_{p+q=k}(q\cdot\widehat u_p)\widehat u_q,
\]

and the Gevrey quantities

\[
X_{\sigma,s}
=
\sum_{k\neq0}
e^{2\sigma|k|}
|k|^{2s}
|\widehat u_k|^2,
\]

\[
Y_{\sigma,s}
=
\sum_{k\neq0}
e^{2\sigma|k|}
|k|^{2s+2}
|\widehat u_k|^2.
\]

Assume zero spatial mean. This is natural for the repository fields and removes the uncontrolled \(k=0\) component from the homogeneous norm. A constant mean can in any case be separated as a uniform transport/Galilean component.

Let

\[
\mathcal N_{\sigma,s}
=
-\operatorname{Re}
\sum_{k\neq0}
e^{2\sigma|k|}
|k|^{2s}
\widehat u_k^*\cdot\widehat{B(u,u)}_k.
\]

The Leray projector is orthogonal, hence \(\|P_k\|_{\ell^2\to\ell^2}\le1\).

## 2. Fourier majorant

Set

\[
A_k=e^{\sigma|k|}|k|^s|\widehat u_k|,
\qquad
B_k=e^{\sigma|k|}|k|^{s+1}|\widehat u_k|.
\]

For \(k=p+q\),

\[
e^{\sigma|k|}
\le
e^{\sigma|p|}e^{\sigma|q|}.
\]

For \(s>0\),

\[
|k|^s
\le
c_s\big(|p|^s+|q|^s\big),
\qquad
c_s=
\begin{cases}
1,&0<s\le1,\\
2^{s-1},&s\ge1.
\end{cases}
\]

Therefore

\[
e^{\sigma|k|}|k|^s|q|\,|\widehat u_p|\,|\widehat u_q|
\]

is bounded by

\[
c_s
\left[
\left(e^{\sigma|p|}|p|^s|\widehat u_p|\right)
\left(e^{\sigma|q|}|q||\widehat u_q|\right)
+
\left(e^{\sigma|p|}|\widehat u_p|\right)
\left(e^{\sigma|q|}|q|^{s+1}|\widehat u_q|\right)
\right].
\]

Define the lattice constant

\[
K_s
=
\left(
\sum_{m\in\mathbb Z^3\setminus\{0\}}
|m|^{-2s}
\right)^{1/2}.
\]

This is finite exactly when \(s>3/2\).

By Cauchy-Schwarz,

\[
\sum_{q\neq0}
e^{\sigma|q|}|q||\widehat u_q|
\le
K_s\,Y_{\sigma,s}^{1/2},
\]

and

\[
\sum_{p\neq0}
e^{\sigma|p|}|\widehat u_p|
\le
K_s\,X_{\sigma,s}^{1/2}.
\]

Applying discrete Young's inequality to the two convolution terms gives

\[
\|\text{weighted convolution}\|_{\ell^2}
\le
2c_sK_s
X_{\sigma,s}^{1/2}Y_{\sigma,s}^{1/2}.
\]

Pairing with the output factor \(A_k\) yields

\[
\boxed{
|\mathcal N_{\sigma,s}|
\le
C_s^{\rm G}\,
X_{\sigma,s}\,
Y_{\sigma,s}^{1/2},
}
\]

with the explicit cutoff-independent constant

\[
\boxed{
C_s^{\rm G}=2c_sK_s.
}
\]

The constant depends on \(s\) and the torus lattice only. It does not depend on \(N\) or on \(\sigma\).

Since all nonzero torus modes satisfy \(|k|\ge1\),

\[
X_{\sigma,s}\le Y_{\sigma,s}.
\]

Hence the weaker but convenient form

\[
\boxed{
|\mathcal N_{\sigma,s}|
\le
C_s^{\rm G}
X_{\sigma,s}^{1/2}Y_{\sigma,s}
}
\]

also holds uniformly in the cutoff.

## 3. Why the earlier commutator draft is not used

The factor

\[
\big||k|^s-|p|^s\big|
\]

does not arise directly from the raw nonlinear term. It requires a separate commutator/skew-symmetry derivation.

For a Gevrey multiplier the relevant commutator is built from the full symbol

\[
e^{\sigma|k|}|k|^s,
\]

so replacing it by only the polynomial difference risks omitting the exponential-symbol contribution.

This gate therefore proves the simpler product-type estimate first.

## 4. Consequence for the weighted identity

PR #22 established

\[
\frac12 X'
+
\nu Y
=
\mathcal N
+
\sigma'Z.
\]

Using the uniform majorant,

\[
\frac12 X'
+
\big(\nu-C_s^{\rm G}\sqrt X\big)Y
\le
\sigma'Z.
\]

This exposes the actual obstruction.

If

\[
C_s^{\rm G}\sqrt X<\nu,
\]

the nonlinear contribution can be absorbed by viscosity.

For arbitrary large data, however, this estimate alone does not guarantee that condition. Thus cutoff-uniformity of the bilinear constant is **not** the missing global-regularity theorem.

The next problem is to obtain a sharper inequality, a dynamically small coefficient, a geometric depletion factor, or another mechanism capable of controlling the large-data regime.

## 5. Numerical role

The companion script does not attempt to infer \(N\to\infty\) from a few cutoffs.

It verifies:

1. zero-mean and divergence-free assumptions on the repository trajectories;
2. the exact nonlinear transfer;
3. the empirical quotient
   \[
   \Lambda_N=
   \frac{|\mathcal N_{\sigma,s}|}
   {X_{\sigma,s}Y_{\sigma,s}^{1/2}};
   \]
4. the weaker quotient
   \[
   \widetilde\Lambda_N=
   \frac{|\mathcal N_{\sigma,s}|}
   {X_{\sigma,s}^{1/2}Y_{\sigma,s}};
   \]
5. that the observed values remain below the explicit truncated-lattice approximation to \(C_s^{\rm G}\).

The analytical proof, not the numerical behavior, is what establishes cutoff independence.

## 6. Scope

This gate proves a standard-strength Gevrey product majorant for zero-mean periodic fields with \(s>3/2\).

It does **not** prove global regularity for arbitrary smooth 3D Navier-Stokes data.
