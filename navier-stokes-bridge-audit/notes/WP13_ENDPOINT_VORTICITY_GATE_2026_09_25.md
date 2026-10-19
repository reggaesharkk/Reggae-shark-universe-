# WP13: Endpoint Vorticity / Concentration Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** analytical concentration obstruction for finite-p vorticity coefficients, plus finite-Galerkin endpoint diagnostics.  
**Scope:** unforced periodic 3D Navier–Stokes, zero mean, \(\sigma=0\), \(s=2\), fixed \(K\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Required coefficient scaling under fixed-energy concentration

For the compactly supported fixed-energy concentration family

\[
u_\lambda(x)=\lambda^{3/2}v(\lambda(x-x_0)),
\]

the homogeneous \(H^s\) quantities scale as

\[
X_s=\|\Lambda^s u\|_2^2
\mapsto
\lambda^{2s}X_s,
\]

\[
Y_s=\|\Lambda^{s+1}u\|_2^2
\mapsto
\lambda^{2s+2}Y_s,
\]

and the signed \(H^s\) nonlinear transfer scales as

\[
N_s\mapsto\lambda^{2s+5/2}N_s.
\]

For the positive-transfer localized base field from WP12 and fixed \(K\), the proved low-advector term is only \(O(\lambda^{2s})\). Therefore the signed high-advector transfer has positive leading order \(O(\lambda^{2s+5/2})\).

The viscous reserve is \(O(\lambda^{2s+2})\), so the tautological coefficient required after subtracting a fixed reserve fraction satisfies

\[
b_{\rm req}^{(\theta)}
=
\frac{[N_s^{>K}-\theta\nu Y_s]_+}{X_s}
\sim
\lambda^{5/2}.
\]

Thus any surviving noncircular coefficient must be capable of seeing this \(\lambda^{5/2}\) concentration scale.

## 2. Finite-p vorticity norms are too weak

The vorticity obeys

\[
\omega_\lambda(x)
=
\lambda^{5/2}\omega_v(\lambda(x-x_0)).
\]

Hence for \(1\le p<\infty\),

\[
\|\omega_\lambda\|_{L^p}
=
\lambda^{5/2-3/p}
\|\omega_v\|_{L^p},
\]

while

\[
\|\omega_\lambda\|_{L^\infty}
=
\lambda^{5/2}
\|\omega_v\|_{L^\infty}.
\]

Suppose there were a universal fixed-\(K\) estimate

\[
N_s^{>K}
\le
\theta\nu Y_s
+
C\|\omega\|_{L^p}X_s
\]

with finite \(p\) and fixed finite \(C\). The coefficient term scales only as

\[
\lambda^{2s+5/2-3/p},
\]

strictly below the positive leading \(O(\lambda^{2s+5/2})\) high transfer.

Therefore, for every finite \(p\),

\[
\boxed{
N_s^{>K}
\le
\theta\nu Y_s
+
C\|\omega\|_{L^p}X_s
}
\]

is false as an all-smooth-data fixed-\(K\) uniform estimate on the concentration family.

The endpoint \(p=\infty\) is not rejected by this scaling argument.

## 3. Why the endpoint does not close the theorem by itself

A coefficient proportional to \(\|\omega\|_\infty\) has the correct concentration scaling. However, a proof of

\[
\sup_N\int_0^T \|\omega_N(t)\|_\infty\,dt<\infty
\]

for arbitrary smooth data is not supplied by the energy identity and would itself be an endpoint continuation-type control.

Thus raw \(\|\omega\|_\infty\) identifies the correct scale but does not provide the missing noncircular L3 estimate.

The remaining route must exploit additional structure, for example geometric depletion, sparseness, direction coherence, or a signed frequency-localized endpoint quantity whose time integral can be controlled independently.

## 4. Finite-Galerkin diagnostics

For the repository trajectories, define again

\[
b_{\rm req}^{(\theta)}
=
\frac{[N_N^{>K}-\theta\nu Y_N]_+}{X_N}.
\]

The companion audit compares this circular target with:

- exact \(\|\omega\|_2=\sqrt G\);
- sampled physical-space \(\|\omega\|_4\);
- sampled \(\|\omega\|_8\);
- sampled grid maximum \(\max|\omega|\);
- the rigorous finite-Fourier envelope
  \[
  \Omega_\Sigma=\sum_k |k|\,|a_k|,
  \]
  which satisfies
  \[
  \|\omega\|_\infty\le\Omega_\Sigma.
  \]

The sampled \(L^p\) values are diagnostic physical-grid quadratures. The finite-\(p\) theorem candidates are already rejected analytically; the endpoint quantities are retained to identify what geometric factor may be missing.

## 5. Interpretation barrier

A bounded sampled ratio \(b_{\rm req}/\|\omega\|_\infty\) cannot prove L2–L3 because \(b_{\rm req}\) is circular and no independent time-integral estimate for the endpoint norm has been established.

The purpose of WP13 is to narrow the search:

\[
\boxed{
\text{finite }L^p\text{ magnitude-only coefficients fail; the surviving scale is endpoint/local.}
}
\]

The next gate should therefore test whether vorticity-direction geometry or another signed local structure can deplete the endpoint coefficient.

No arbitrary-data global-regularity result is claimed.
