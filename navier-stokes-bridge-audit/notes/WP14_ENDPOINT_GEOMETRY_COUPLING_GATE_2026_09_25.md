# WP14: Endpoint–Geometry Coupling Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** matched finite-Galerkin endpoint/geometry diagnostic.  
**Scope:** unforced periodic 3D Navier–Stokes, zero mean, \(\sigma=0\), \(s=2\), fixed high-advector threshold \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Target left by WP13

WP13 showed that under the fixed-energy concentration family

\[
u_\lambda(x)=\lambda^{3/2}v(\lambda x),
\]

the tautological coefficient required by the signed high-advector estimate scales as

\[
b_{\rm req}^{(\theta)}
\sim \lambda^{5/2},
\]

while

\[
\|\omega\|_{L^\infty}
\sim \lambda^{5/2}.
\]

Therefore the residual factor

\[
\boxed{
\Gamma_{\rm req}
=
\frac{b_{\rm req}^{(\theta)}}{\|\omega\|_{L^\infty}}
}
\]

is dimensionless under physical concentration.

A finite-grid implementation uses

\[
\Gamma_{\rm req}^{\rm grid}
=
\frac{b_{\rm req}^{(\theta)}}{\|\omega\|_{\infty,\rm grid}},
\]

with the explicit warning that the grid maximum is only a sampled lower estimate of the continuum supremum.

This gate asks whether the remaining dimensionless factor co-moves with matched geometric depletion diagnostics on the same Galerkin state.

## 2. Scaling filter for candidate geometry

The following quantities are dimensionless under the same concentration map.

### 2.1 Direction-disorder number

Let

\[
\ell_\omega=\sqrt{G/D}
\]

and let \(L_{\max}\) be the sampled high-vorticity direction slope

\[
L_{\max}
=
\max
\frac{|\xi(x)\times\xi(x+h)|}{|h|},
\qquad
\xi=\omega/|\omega|,
\]

restricted to sampled pairs whose endpoints both satisfy

\[
|\omega|\ge 2\sqrt G.
\]

Since

\[
\ell_\omega\mapsto\lambda^{-1}\ell_\omega,
\qquad
L_{\max}\mapsto\lambda L_{\max},
\]

the product

\[
\boxed{
g_{\rm dir}=\ell_\omega L_{\max}
}
\]

is invariant.

Where \(L_{\max}>0\), the previously used sampled coherence-ratio proxy is

\[
R_{\rm sample}
=
\frac{\rho_{\rm upper}^{\rm sample}}{\ell_\omega}
=
\frac{1}{g_{\rm dir}}.
\]

Neither quantity is a theorem-compatible lower coherence radius.

### 2.2 Endpoint-normalized positive strain alignment

Define

\[
g_{\rm stretch}
=
\frac{
\langle(\omega\cdot S\omega)_+\rangle
}{
\|\omega\|_{\infty,\rm grid}\,G
}.
\]

The numerator and denominator have the same fixed-energy concentration scaling, so this ratio is dimensionless.

It measures the positive pointwise stretching burden relative to an endpoint vorticity scale; it is not a regularity criterion.

### 2.3 Matched high-tail H2 triadic coherence

For the exact WP11 high-advector split \(|p|>K\), define ordered-triad terms

\[
Z_{k,p,q}^{(2)}
=
-|k|^4
\left\langle
a_k,\,
P_k\big[i(q\cdot a_p)a_q\big]
\right\rangle ,
\qquad k=p+q.
\]

Then

\[
N_2^{>K}
=
\Re\sum_{|p|>K} Z_{k,p,q}^{(2)}
\]

and

\[
A_{2,\rm high}
=
\sum_{|p|>K}|Z_{k,p,q}^{(2)}|.
\]

Define

\[
\boxed{
\chi_{2,\rm high}
=
\frac{N_2^{>K}}{A_{2,\rm high}}
}
\]

whenever the envelope is nonzero.

This is an exact finite-Galerkin signed phase-coherence factor for the same high-advector quantity used by WP11. It is dimensionless and satisfies

\[
|\chi_{2,\rm high}|\le1.
\]

The envelope \(A_{2,\rm high}\) is cubic and is not independently controlled; \(\chi_{2,\rm high}\) alone is therefore diagnostic rather than a proof coefficient.

## 3. Matched-state protocol

The companion audit evaluates the following on the same state:

1. the WP11 signed high-advector transfer \(N_2^{>K}\);
2. \(X_2,Y_2,G,D\);
3. the tautological
   \[
   b_{\rm req}^{(\theta)}
   =
   [N_2^{>K}-\theta\nu Y_2]_+/X_2;
   \]
4. \(\Gamma_{\rm req}^{\rm grid}\);
5. \(g_{\rm dir}\) and \(R_{\rm sample}\);
6. \(g_{\rm stretch}\);
7. \(\chi_{2,\rm high}\).

The run uses the reference and combined perturbed trajectories at \(N=4,7\), amplitude multipliers \(1,2,4\), reserve fractions \(\theta=0.25,0.5,0.75\), and the short interval \([0,0.005]\).

## 4. Falsification logic

No finite correlation establishes L2–L3.

The diagnostic is useful in the opposite direction:

- if a proposed geometric factor is identically small while \(\Gamma_{\rm req}\) becomes large, that factor alone cannot explain the sampled endpoint burden;
- if a candidate varies in the wrong direction under amplitude or cutoff changes, it is a poor standalone depletion variable;
- if a candidate tracks \(\Gamma_{\rm req}\) robustly across matched states, it becomes eligible for a later analytical gate, but still requires an independently controlled time integral or a theorem-compatible structural estimate.

No regression fit from the circular target is promoted into an a priori inequality.

## 5. Interpretation barrier

WP14 is a geometry-selection gate, not a proof of geometric depletion.

In particular:

- \(g_{\rm dir}\) uses a finite grid, axis-aligned nearest-neighbor pairs, and a diagnostic moving threshold;
- \(R_{\rm sample}\) is built from an upper bound on a sampled coherence radius;
- \(g_{\rm stretch}\) uses the sampled grid maximum of vorticity;
- \(\chi_{2,\rm high}\) measures cancellation inside a cubic envelope that is itself not controlled.

A later proof gate must derive a noncircular inequality before any of these quantities can contribute to L2–L3.


## 6. Executed finite diagnostic

The matched-state audit completed successfully on the registered short-window
families.

For the pooled active samples, the descriptive Pearson correlations with
(Gamma_{m req}^{m grid}) were

[
r(g_{m dir})approx 0.7994,
qquad
r(g_{m stretch})approx 0.7426,
qquad
r(chi_{2,m high})approx -0.7355.
]

Pooling mixes different trajectories, amplitudes, and reserve fractions, so
these numbers are descriptive only.

On the aggressive combined (N=7) family considered separately, the
correlations were substantially sharper:

[
r(g_{m dir})approx0.9725,
]

[
r(g_{m stretch})approx0.9875,
]

[
r(chi_{2,m high})approx-0.7738.
]

The negative coherence correlation means that the signed high-tail coherence
factor by itself moves in the opposite direction to the required endpoint
burden over this sampled family. It therefore does not behave as a standalone
positive depletion factor here.

For the combined (N=7), amplitude-4, (	heta=0.25) trajectory, the largest
sampled endpoint target was approximately

[
Gamma_{m req}^{m grid}=0.0428798.
]

At that same stage the endpoint-normalized positive-stretching factor was of
comparable magnitude, approximately (0.04215) near the target peak.

This numerical proximity is not an inequality. It identifies the algebraic
candidate

[
|omega|_infty g_{m stretch}
=
rac{langle(omegacdot Somega)_+angle}{G}.
]

The next analytical gate should test the noncircular candidate

[
b_{m stretch}
=
rac{langle(omegacdot Somega)_+angle}{G}
]

against the exact signed (H^2) high-advector remainder, and separately test
whether any all-prefix time integral of (b_{m stretch}) follows from
independently controlled quantities.

The present data do not establish either statement.
