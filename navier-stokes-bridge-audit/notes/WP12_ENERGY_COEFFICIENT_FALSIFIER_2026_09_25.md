# WP12: Energy-Level Coefficient Falsifier for the One-Sided High-Tail Target

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** exact scaling reduction plus finite-Galerkin falsification target.  
**Scope:** unforced periodic 3D Navier–Stokes, zero mean, \(\sigma=0\), \(s>3/2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Why test an energy-level coefficient first

WP11 asks whether the signed high-advector transfer can satisfy

\[
N_N^{>K}(t)
\le
\theta\nu Y_N(t)
+
b_{N,K}(t)X_N(t),
\qquad 0<\theta<1,
\]

with

\[
\sup_N\int_0^T b_{N,K}(t)\,dt<\infty
\]

from quantities controlled independently of the desired high norm.

A natural first class is coefficients built only from the energy-level norms

\[
\mathcal E(t)=\|u(t)\|_2^2,
\qquad
G(t)=\|\nabla u(t)\|_2^2.
\]

The energy identity gives

\[
\frac12\mathcal E'(t)+\nu G(t)=0,
\]

hence

\[
\int_0^T G(t)\,dt
\le
\frac{\mathcal E(0)}{2\nu}.
\]

Therefore \(\sqrt G\) is automatically time-integrable:

\[
\int_0^T \sqrt{G(t)}\,dt
\le
\sqrt{
T\int_0^T G(t)\,dt
}
\le
\sqrt{\frac{T\mathcal E(0)}{2\nu}}.
\]

If a one-sided estimate with coefficient \(C\sqrt G\) were true, L3 would follow immediately.

## 2. Uniqueness among monomials of \(\mathcal E\) and \(G\)

Consider a monomial coefficient

\[
b(\mathcal E,G)
=
C\mathcal E^\alpha G^\beta.
\]

At a fixed instant, under pure amplitude scaling \(u\mapsto Au\),

- \(N^{>K}\) is cubic in \(A\);
- \(X\) and \(Y\) are quadratic;
- therefore the coefficient multiplying \(X\) must be linear in \(A\).

Since \(\mathcal E,G\mapsto A^2(\mathcal E,G)\),

\[
\alpha+\beta=\frac12.
\]

Under the Navier–Stokes integer dilation on the torus image sublattice,

\[
u_\lambda(x,t)
=
\lambda u(\lambda x,\lambda^2 t),
\]

we have

\[
\mathcal E\mapsto\lambda^2\mathcal E,
\qquad
G\mapsto\lambda^4G.
\]

Because \(bX\) must scale with \(N^{>K}\), the coefficient must scale like \(\lambda^2\). Thus

\[
2\alpha+4\beta=2,
\]

or

\[
\alpha+2\beta=1.
\]

Solving the two equations gives

\[
\boxed{
\alpha=0,\qquad \beta=\frac12.
}
\]

Therefore the unique monomial made only from \(\mathcal E\) and \(G\) with the required amplitude and Navier–Stokes scaling is

\[
\boxed{
b_{\rm energy}(t)=C\sqrt{G(t)}.
}
\]

This does not prove that such a coefficient works. It only identifies the cleanest energy-level candidate.

## 3. The tautological target coefficient

For a chosen reserve fraction \(\theta\), define the exact descriptive quantity

\[
b_{\rm req}^{(\theta)}(t)
=
\frac{
\big[
N_N^{>K}(t)-\theta\nu Y_N(t)
\big]_+
}{
X_N(t)
},
\]

where \([x]_+=\max(x,0)\).

Then

\[
N_N^{>K}
\le
\theta\nu Y_N
+
b_{\rm req}^{(\theta)}X_N
\]

holds by construction.

This coefficient is **circular** and is not a proof device. Its sole role is to tell us what any noncircular candidate must dominate.

The dimensionless diagnostic for the energy-level candidate is

\[
\boxed{
Q_{\rm energy}^{(\theta)}
=
\frac{
b_{\rm req}^{(\theta)}
}{
\sqrt G
}.
}
\]

If a universal estimate

\[
N_N^{>K}
\le
\theta\nu Y_N
+
C\sqrt G\,X_N
\]

were true, then \(Q_{\rm energy}^{(\theta)}\le C\).

Finite simulations can falsify a proposed finite constant on sampled families, but cannot prove a uniform bound.

## 4. Scaling of the target

Under the exact Navier–Stokes dilation with \(N,K\mapsto\lambda N,\lambda K\),

\[
X\mapsto\lambda^{2s+2}X,
\]

\[
Y,\;N^{>K}\mapsto\lambda^{2s+4}(Y,N^{>K}).
\]

Therefore

\[
b_{\rm req}^{(\theta)}
\mapsto
\lambda^2b_{\rm req}^{(\theta)},
\]

while

\[
\sqrt G\mapsto\lambda^2\sqrt G.
\]

Hence

\[
\boxed{
Q_{\rm energy}^{(\theta)}
\text{ is exactly invariant under the image-sublattice Navier–Stokes dilation.}
}
\]

This is a dimensional-consistency check, not a continuum-limit theorem.

## 5. Falsification protocol

The companion script and Colab notebook must test:

1. \(N=4\) versus \(N=7\);
2. reserve fractions \(\theta\in\{0.25,0.5,0.75\}\);
3. the reference and combined perturbed scenarios;
4. amplitude multipliers;
5. exact image-sublattice dilation with \(N,K\mapsto\lambda N,\lambda K\);
6. all-prefix integrals of \(b_{\rm req}\) and \(\sqrt G\).

The audit records

\[
Q_{\rm energy}^{(\theta)}
=
b_{\rm req}^{(\theta)}/\sqrt G
\]

without fitting a theorem from finite data.

## 6. Interpretation barrier

A stable \(Q_{\rm energy}\) on a finite collection of trajectories would not prove L2–L3.

A growing or arbitrarily large \(Q_{\rm energy}\) on an explicit smooth family would refute the corresponding universal \(C\sqrt G\) coefficient.

If the energy-level candidate fails, the remaining route must use information beyond \(\mathcal E\) and \(G\): signed geometry, frequency localization, phase structure, or another independently controlled quantity.

No arbitrary-data Navier–Stokes regularity result is claimed in this gate.


## 7. Exact H2 concentration obstruction to the energy-level candidate

For the repository sparse triad with

\[
P=(1,0,0),\quad Q=(0,1,1),\quad R=(1,1,1),
\]

the polarizations in src/helicity_phase_gate.py, amplitude \(A=1\), and
phase \(\theta=\pi/2\), direct Fourier convolution gives

\[
N_{s=1}=4,
\qquad
N_{s=2}=24>0.
\]

Thus the periodic finite triad has strictly positive \(H^2\) nonlinear
transfer.

Use the same localization construction already recorded in
notes/CANDIDATE_INEQUALITY_GATE_2026_09_24.md: write the periodic field as
the curl of a periodic vector potential, multiply that potential by a smooth
large-scale cutoff, and take the curl. For sufficiently large localization
radius the leading volume contribution retains the positive \(H^2\) transfer;
terms in which derivatives hit the cutoff lose one power of the localization
radius. Fix one resulting smooth compactly supported divergence-free field
\(v\) with \(N_2(v)>0\).

Embed its support inside one torus cell and define

\[
u_\lambda(x)
=
\lambda^{3/2}v(\lambda(x-x_0)).
\]

The \(L^2\) norm is fixed. For \(s=2\),

\[
X_2(u_\lambda)=\lambda^4X_2(v),
\]

\[
Y_2(u_\lambda)=\lambda^6Y_2(v),
\]

\[
G(u_\lambda)=\lambda^2G(v),
\]

and the cubic \(H^2\) transfer satisfies

\[
N_2(u_\lambda)=\lambda^{13/2}N_2(v).
\]

Fix \(K\). The proved WP11 low-advector estimate gives

\[
|N_2^{\le K}(u_\lambda)|
\le
C_2(K)\|v\|_2X_2(v)\lambda^4.
\]

Hence

\[
N_2^{>K}(u_\lambda)
=
N_2(u_\lambda)-N_2^{\le K}(u_\lambda)
\ge
c\lambda^{13/2}-C_K\lambda^4
\]

for some \(c>0\), and is positive for all sufficiently large \(\lambda\).

Now suppose there were fixed \(0<\theta<1\) and finite \(C\) such that

\[
N_2^{>K}
\le
\theta\nu Y_2
+
C\sqrt G\,X_2
\]

for every smooth datum in this family. The right side scales at most as

\[
\theta\nu\,O(\lambda^6)
+
C\,O(\lambda^5),
\]

whereas the left side has positive leading order
\(O(\lambda^{13/2})\). This is impossible as \(\lambda\to\infty\).

Therefore

\[
\boxed{
N_2^{>K}
\le
\theta\nu Y_2
+
C\sqrt G\,X_2
}
\]

is **false as an all-smooth-data, fixed-K uniform estimate**.

As in the earlier concentration gate, sufficiently large finite Fourier
projections converge in the relevant smooth norms and preserve the
inequality violation after a small normalization if needed. The argument is
therefore not an artifact of an infinite Fourier representation.

This rejection concerns the specific energy-level coefficient
\(C\sqrt G\). It does not refute WP11 L2-L3 with a coefficient using stronger
or genuinely signed/geometric information.

## 8. Consequence for the search

The energy identity does provide an attractive time-integrable quantity
\(\sqrt G\), but physical concentration outruns both its contribution
\(\sqrt G\,X_2\) and a fixed viscous reserve \(\theta\nu Y_2\).

The next surviving coefficient must therefore encode information beyond
\(\mathcal E\) and \(G\). The finite falsifier and Colab notebook are retained
to compare future noncircular geometric/frequency candidates against the
exact target \(b_{\rm req}\); they are no longer being used to decide whether
the pure \(C\sqrt G\) theorem is true.


## 9. Executed finite-cutoff sweep

The repository audit was executed on N=4 and N=7 for the reference and
combined perturbed scenarios, amplitude multipliers 0.5, 1, 2, 4, reserve
fractions theta=0.25,0.5,0.75, dt=0.0005, and t in [0,0.005].

The exact image-sublattice dilation checks recorded zero relative scaling
error for X, Y, G, signed high transfer, b_required, sqrt(G), and Q_energy.
This checks the indexed finite-dimensional scaling map only.

The largest sampled Q_energy was

    0.13075951615326528

for the combined perturbed N=7 trajectory with amplitude multiplier 4 and
theta=0.25. At amplitude multiplier 1 and theta=0.25, the combined N=4 run
had Q_energy=0 throughout the sampled window, while N=7 reached about
0.05237054. For the reference field at amplitude 4 and theta=0.25, the
sampled maxima were about 0.00748086 (N=4) and 0.03884155 (N=7).

These finite differences are not used to prove the analytical rejection of
C*sqrt(G). That rejection is the concentration argument in Section 7.
The sweep is retained as a regression target for future candidate
coefficients that use additional signed/geometric information.
