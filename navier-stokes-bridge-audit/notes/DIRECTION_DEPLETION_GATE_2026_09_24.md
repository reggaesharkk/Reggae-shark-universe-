# Local vorticity-direction depletion gate (post-v0.2)

## Why this gate

The triadic hierarchy established

\[
|T_N|\le B_N\le A_N,
\]

and showed that substantial cancellation occurs inside each output Fourier
mode. However, any universal energy-only estimate of the form
\(B_N\lesssim G_N^{3/2}\) is blocked by the existing fixed-energy physical
concentration argument.

That points to a quantity that is **geometric and concentration-sensitive**,
rather than another magnitude-only Fourier norm.

Constantin and Fefferman proved that sufficiently coherent vorticity
direction in regions of large vorticity prevents singularity formation.
Their condition controls the angle between nearby vorticity directions;
later work weakened the required coherence. This gate does **not** attempt
to re-prove or numerically verify those theorems. It uses their geometry as
a diagnostic coordinate.

Reference:

- P. Constantin and C. Fefferman, *Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations*, Indiana Univ.
  Math. J. 42 (1993), 775-789, DOI 10.1512/iumj.1993.42.42034.

## Proxy definition

Let

\[
\xi(x)=\frac{\omega(x)}{|\omega(x)|}
\]

where \(\omega\ne0\). For axis-aligned periodic offsets \(h\) on the
\(32^3\) grid, define the positive magnitude weight

\[
W_h(x)=\frac{|\omega(x)|^2|\omega(x+h)|}{|h|^3}.
\]

Two dimensionless weighted depletion proxies are recorded:

\[
D_{\rm ang}(h)
=
\frac{\langle W_h |\xi(x)\times\xi(x+h)|\rangle}
{\langle W_h\rangle},
\]

and

\[
D_{\rm det}(h)
=
\frac{\langle
W_h |(\xi(x)\times\xi(x+h))\cdot\widehat h|
\rangle}
{\langle W_h\rangle}.
\]

The second quantity keeps the separation-direction determinant appearing
in the geometric structure of the stretching kernel. Both lie in
\([0,1]\).

These are **local proxies only**. They are not the full periodic
Biot-Savart singular integral.

## Tracked finite-Galerkin observation

The same four cases used by the triadic-coherence trajectory audit are
sampled at \(t=0,0.005,0.010,0.015\).

At the smallest grid separation:

- Reference, \(N=4\): \(D_{\rm ang}\) changes from about 0.11714 to
  0.11901 and \(D_{\rm det}\) from 0.06501 to 0.06617.
- Reference, \(N=7\): \(D_{\rm ang}\) changes from about 0.11714 to
  0.11989 and \(D_{\rm det}\) from 0.06501 to 0.06652.
- Combined double/quarter-phase/high-frequency, \(N=4\):
  \(D_{\rm ang}\) changes from about 0.14702 to 0.15078 while
  \(D_{\rm det}\) changes from 0.08058 to 0.07936.
- The same combined case at \(N=7\):
  \(D_{\rm ang}\) rises to about 0.16317 and
  \(D_{\rm det}\) rises to about 0.09189 by \(t=0.015\).

Thus the aggressive \(N=7\) combined trajectory develops measurably larger
small-scale directional disorder in this proxy than its \(N=4\) counterpart,
whereas the reference pair stays much closer.

This is consistent with the previously observed stronger growth of signed
triadic coherence and stretching in the combined \(N=7\) case, but it does
not establish causation or a regularity estimate.

## Why this is a better next coordinate

Unlike \(A_N\), \(B_N\), or \(G_N\), direction coherence can change under
physical concentration through the spatial oscillation scale of \(\xi\).
That makes it structurally capable of interacting with the concentration
obstruction that killed the energy-only candidates.

The next proof-level question is therefore not whether
\(D_{\rm ang}\) or \(D_{\rm det}\) is numerically small. It is whether one
can derive a scale-critical inequality in which a rigorously defined
direction-coherence modulus multiplies the singular stretching kernel and
is propagated strongly enough by the Navier-Stokes evolution.

## Scope

This gate uses:

- only four finite Galerkin trajectories;
- one \(32^3\) grid;
- three axis-aligned separations;
- data only through \(t=0.015\).

No continuum convergence, uniform bound, or blow-up exclusion is inferred.

Reproduce with:

\`\`\`bash
python src/direction_depletion_gate.py
\`\`\`
