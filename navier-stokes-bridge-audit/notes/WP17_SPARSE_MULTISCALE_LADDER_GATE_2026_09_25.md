# WP17: Sparse Multiscale Ladder Adversary

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** sparse amplitude/phase adversarial search against the WP15 positive-stretching coefficient.  
**Scope:** instantaneous smooth periodic divergence-free Fourier fields, \(s=2\), fixed high-advector split \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Motivation

WP16 showed that phase-only rearrangement on one evolved spectrum can raise

\[
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}{b_{\rm stretch}X_2}
\]

from about 1.038 to about 1.078.

A stronger adversary is allowed to change the **relative amplitudes between coherent scales** as well as their phases.

Use scaled copies of the exact sparse triad

\[
P=(1,0,0),\quad Q=(0,1,1),\quad R=(1,1,1)
\]

at integer scales \(m=1,\ldots,L\).

For each scale, keep the registered divergence-free polarizations and assign a real amplitude \(A_m>0\) plus an \(R\)-mode phase \(\theta_m\).

Global amplitude is irrelevant to \(C_\infty^{\rm stretch}\), so fix \(A_1=1\) and search only relative amplitudes and phases.

## 2. Scaling consistency

For one isolated scaled triad with fixed coefficient amplitude,

\[
G_m\sim m^2,
\qquad
X_{2,m}\sim m^4,
\qquad
\langle(\omega\cdot S\omega)_+\rangle_m\sim m^3,
\qquad
N_{2,m}\sim m^5.
\]

Therefore

\[
b_{{\rm stretch},m}
=
\frac{\langle(\omega\cdot S\omega)_+\rangle_m}{G_m}
\sim m,
\]

and

\[
b_{{\rm stretch},m}X_{2,m}\sim m^5,
\]

matching the \(H^2\) nonlinear transfer scale.

Thus the ladder is not rejected by dimensional mismatch.

## 3. Exact sparse objective

For each sparse field compute

\[
X_2=\sum_k |k|^4|a_k|^2,
\qquad
G=\sum_k |k|^2|a_k|^2.
\]

The high-advector transfer is computed exactly on occupied output modes:

\[
N_2^{>K}
=
-\Re
\sum_{k}
|k|^4\,
\overline{a_k}\cdot
P_k
\sum_{\substack{p+q=k\\|p|>K}}
i(q\cdot a_p)a_q.
\]

The physical-space coefficient is

\[
b_{\rm stretch}
=
\frac{\langle(\omega\cdot S\omega)_+\rangle}{G}.
\]

The adversarial quotient is

\[
\boxed{
C_\infty^{\rm stretch}
=
\frac{[N_2^{>K}]_+}{b_{\rm stretch}X_2}.
}
\]

## 4. Deterministic search

The companion audit searches ladder lengths \(L=2,\ldots,6\).

For each \(L\):

- fix \(A_1=1\);
- sample logarithmic relative amplitudes for \(A_2,\ldots,A_L\);
- sample phases \(\theta_1,\ldots,\theta_L\);
- retain the best state;
- refine it by local single-coordinate perturbations;
- recompute the best candidate on finer spatial grids.

The search grid is \(32^3\). Best states are independently checked at \(48^3\) and \(64^3\).

## 5. Falsification logic

If \(C_\infty^{\rm stretch}\) grows without apparent control as ladder length or amplitude contrast increases, that would motivate an explicit analytical counterexample family to the WP15 pointwise coefficient.

If the quotient remains bounded in this finite search, no theorem follows.

A finite optimizer can only raise the tested lower benchmark for any universal constant.

## 6. Interpretation barrier

The ladder is a specific sparse family, not all smooth fields. Search maxima are not global maxima. Positive stretching contains a pointwise positive part and therefore requires grid refinement.

No cutoff-independent constant, time-integral estimate, or global regularity result is claimed.


## 7. Executed search and grid refinement

The deterministic search completed for ladder lengths (L=2,ldots,6).
Every best state was reevaluated at (48^3), (64^3), and (96^3).

The refined (96^3) values were:

| (L) | (C_infty^{m stretch}) |
| ---: | ---: |
| 2 | 5.0584507 |
| 3 | 5.0574121 |
| 4 | 5.0825132 |
| 5 | 5.0817697 |
| 6 | **5.1129326** |

The best (L=6) state had

[
N_2^{>K}approx4.1485	imes10^6,
]

[
langle(omegacdot Somega)_+angleapprox8.8327	imes10^4,
]

while the **signed** (H^1) stretching was strongly negative,

[
langleomegacdot Somegaangleapprox-2.5930	imes10^5.
]

Its matched high-tail triadic coherence was

[
chi_{2,m high}approx0.7993.
]

This gives a concrete derivative-level sign separation: negative global signed
(H^1) stretching can coexist with a large positive signed (H^2)
high-advector transfer.

The coarse (32^3) search value for this state was about 5.23166. Refinement
reduced it monotonically:

[
5.23166;(32^3),
quad
5.14904;(48^3),
quad
5.12994;(64^3),
quad
5.11293;(96^3).
]

Thus the effect survives refinement, while the coarse search grid
overestimates its magnitude.

The workflow artifact digest is

    sha256:187fa4f160b5faca78c710a83ef24b7d423a074ebf2872cf3050a51ca01dedee

## 8. Structural interpretation

The search does **not** show growth with ladder length.

Instead, every optimized ladder drove the second-scale amplitude to the
registered logarithmic search boundary,

[
A_2=e^3approx20.0855,
]

while most additional scales became comparatively small.

The best states therefore approach a dominant scale-2 sparse-triad geometry
rather than an expanding multiscale cascade.

This raises the current finite adversarial benchmark for the WP15 coefficient
from approximately 1.078 (WP16) to approximately

[
oxed{5.113}
]

on the refined registered ladder family.

It does not show that the required constant is unbounded.

The next analytical target is correspondingly simpler: characterize the
dominant scale-2 triad / singular amplitude-ratio limit and determine whether
its (C_infty^{m stretch}) has a finite exact supremum.
