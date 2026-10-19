# Direction-scaling obstruction gate (post-v0.2)

## Candidate that must be tested before further fitting

The local direction-depletion gate measures a finite-difference direction
slope of the form

\[
L_{\rm dir}(h)
\sim
\frac{|\sin\theta(x,x+h)|}{|h|}.
\]

Because the fixed-energy concentration construction already killed every
energy-only \(G^{3/2}\) majorant, a natural attempt is to normalize this
geometric slope by the enstrophy scale:

\[
Q_{\rm dir}
=
\frac{L_{\rm dir}}{\sqrt G}.
\]

This is dimensionless under the specific fixed-energy concentration family.
That sounds attractive. It is also precisely why it cannot, by itself, repair
the rejected \(G^{3/2}\) closure.

## Exact concentration scaling

Take the same compactly supported divergence-free base field \(v\) used in
the candidate-inequality obstruction and define

\[
u_\lambda(x)
=
\lambda^{3/2}v(\lambda(x-x_0)).
\]

Then the \(L^2\) energy is fixed, while

\[
\omega_\lambda(x)
=
\lambda^{5/2}\omega_v(\lambda(x-x_0)).
\]

The vorticity direction is therefore just spatially compressed:

\[
\xi_\lambda(x)
=
\xi_v(\lambda(x-x_0)).
\]

For any direction modulus based on a first spatial difference,

\[
L_{\rm dir}(u_\lambda)
=
\lambda L_{\rm dir}(v).
\]

At the same time,

\[
G(u_\lambda)=\lambda^2G(v),
\qquad
T(u_\lambda)=\lambda^{9/2}T(v).
\]

Hence

\[
Q_{\rm dir}(u_\lambda)
=
\frac{\lambda L_{\rm dir}(v)}
{\sqrt{\lambda^2G(v)}}
=
Q_{\rm dir}(v),
\]

but

\[
\frac{T(u_\lambda)}
{G(u_\lambda)^{3/2}}
=
\lambda^{3/2}
\frac{T(v)}
{G(v)^{3/2}}.
\]

Therefore no inequality of the form

\[
T
\le
C(E_0,Q_{\rm dir})\,G^{3/2}
\]

can hold uniformly over this fixed-energy concentration family whenever the
base field has positive stretching, because the right-hand coefficient is
unchanged while the necessary coefficient grows like \(\lambda^{3/2}\).

This is an **analytic scaling obstruction**, not a finite-data inference.

## What survives

This does **not** contradict the Constantin-Fefferman theorem.

Their hypothesis retains an **absolute spatial coherence scale**: roughly,
the vorticity direction must satisfy a bound such as

\[
|\sin\theta(x,y,t)|
\le
\frac{|x-y|}{\rho}
\]

in high-vorticity regions for a positive coherence length \(\rho\). Under the
concentration above, that physical coherence length shrinks like
\(\rho_\lambda\sim\rho/\lambda\). The concentration therefore violates a
fixed absolute coherence scale rather than hiding inside a dimensionless
normalization.

Reference:

- P. Constantin and C. Fefferman, *Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations*, Indiana Univ.
  Math. J. 42 (1993), 775-789, DOI 10.1512/iumj.1993.42.42034.

## Finite trajectory values

The companion script reads the already-validated
direction_depletion_results.json file and records

\[
L_{\rm ang}=\frac{D_{\rm ang}(h_1)}{|h_1|},
\qquad
L_{\rm det}=\frac{D_{\rm det}(h_1)}{|h_1|},
\]

at the smallest sampled offset \(h_1=2\pi/32\), together with

\[
Q_{\rm ang}=\frac{L_{\rm ang}}{\sqrt G},
\qquad
Q_{\rm det}=\frac{L_{\rm det}}{\sqrt G}.
\]

For example, the combined \(N=7\) trajectory has

\[
Q_{\rm ang}:
0.01407\to0.01519
\]

through \(t=0.015\), while the reference \(N=7\) trajectory has

\[
Q_{\rm ang}:
0.02589\to0.02642.
\]

So the aggressive stretching case does **not** simply correspond to a larger
normalized direction-disorder ratio. That is consistent with the analytic
obstruction: the normalized scalar \(Q_{\rm dir}\) throws away the absolute
coherence length that the geometric regularity mechanism needs.

## Next proof target

The next surviving object must retain an **absolute or dynamically generated
length scale**. A natural candidate is therefore a coherence radius
\(\rho(t)\) extracted from high-vorticity geometry and compared directly
with a viscous/analyticity length scale, rather than divided away by
\(\sqrt G\).

That is a qualitatively different route from every failed norm-only closure
tested so far.

## Scope

The scaling argument is exact for the stated concentration family.
The numerical \(Q\) values are only finite-grid diagnostics and are not
the Constantin-Fefferman modulus itself.

Reproduce with:

    python src/direction_scaling_obstruction_gate.py
