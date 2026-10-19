# Satellite first-variation audit around the WP18 dominant triad

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** exact sparse-convolution first-variation identities plus deterministic shifted-grid directional derivative.  
**Scope:** the registered WP17 best-ladder direction, normalized around the WP18 dominant (m=2) sparse triad.  
**Not claimed:** no global optimizer, no cutoff-independent constant, no time-integral closure, no Navier–Stokes regularity theorem.

## 1. Question

WP17 found a refined ladder value

[
C_infty^{m ladder}approx 5.1129326,
]

while WP18 isolated the dominant (m=2) triad at

[
C_infty^{m isolated}approx 5.0596991.
]

The gap is about one percent.

The question here is narrower:

> Does the WP17 satellite direction already improve the quotient at first order around the isolated (m=2) state?

## 2. Perturbation family

Normalize the WP17 best state by its dominant amplitude

[
A_2=e^3approx20.0855369232.
]

Keep the registered WP17 phases and define

[
u_arepsilon
=
u_{m=2}
+
arepsilon,v_{m sat},
]

where (v_{m sat}) contains scales (m=1,3,4,5,6) with relative amplitudes

[
rac{A_m}{A_2}
=
(0.04978706837,;0.00247875218,;0.01081140030,;0.00247875218,;0.00704342772)
]

for (m=(1,3,4,5,6)).

Thus (arepsilon=0) is the isolated dominant triad and (arepsilon=1) is the normalized WP17 best ladder.

## 3. Exact sparse-convolution structure

Because the occupied Fourier support is finite, the quadratic norms are exact polynomials in (arepsilon):

[
G(arepsilon)
=
112
+
0.1776262007148688,arepsilon^2,
]

[
X_2(arepsilon)
=
1024
+
6.466168009632611,arepsilon^2.
]

Hence

[
G'(0)=X_2'(0)=0.
]

The signed high-advector (H^2) transfer is a cubic polynomial. Direct sparse-convolution evaluation gives

[
N_2^{>2}(arepsilon)
=
511.9999986
-
0.0344159907,arepsilon^3
]

up to floating-point roundoff from the registered phase value near (-pi/2). In particular,

[
oxed{(N_2^{>2})'(0)=0}
]

and the fitted quadratic coefficient is also numerically zero.

So the numerator and both quadratic norm factors have no linear response along this satellite direction.

## 4. Positive-stretching first variation

Write

[
P(arepsilon)
=
leftlangle
(omega_arepsiloncdot S_arepsilonomega_arepsilon)_+
ightangle .
]

Let

[
omega_arepsilon=omega_0+arepsilonomega_1,qquad
S_arepsilon=S_0+arepsilon S_1.
]

The exact local derivative of the cubic stretching density at (arepsilon=0) is

[
F_1
=
2,omega_1cdot S_0omega_0
+
omega_0cdot S_1omega_0.
]

Away from the zero level set of

[
F_0=omega_0cdot S_0omega_0,
]

the directional derivative of the positive part is

[
P'(0)
=
leftlangle
mathbf 1_{{F_0>0}}F_1
ightangle .
]

To avoid lattice alignment with the (F_0=0) set, the companion verifier averages four deterministic sub-cell shifts.

The shifted-grid estimates are:

| grid | (P(0)) | (P'(0)) |
| ---: | ---: | ---: |
| (48^3) | 11.08596054 | -0.20596758 |
| (64^3) | 11.08107080 | -0.20801339 |
| (96^3) | 11.07181555 | -0.21143403 |
| (128^3) | 11.07035739 | -0.21414334 |
| (160^3) | 11.07004735 | -0.21370281 |

The WP18 (4096^2) reduced quadrature gives

[
P(0)=8P_+(-pi/2)approx11.0678519450.
]

The three-dimensional shifted-grid values converge toward that independent baseline.

Most importantly, the directional derivative is stably negative:

[
oxed{P'(0)<0}
]

for the registered WP17 satellite direction.

## 5. Consequence for the quotient

The quotient is

[
C_infty(arepsilon)
=
rac{N_2^{>2}(arepsilon),G(arepsilon)}
{P(arepsilon),X_2(arepsilon)}
]

while the numerator remains positive.

Since

[
N'(0)=G'(0)=X_2'(0)=0,
]

we obtain

[
oxed{
rac{C_infty'(0)}{C_infty(0)}
=
-rac{P'(0)}{P(0)}.
}
]

Using the WP18 refined baseline and the (160^3) shifted-grid derivative gives the descriptive estimate

[
C_infty'(0)approx +0.0977.
]

Therefore the registered WP17 satellite direction is an **improving first-order direction** away from the isolated WP18 triad.

## 6. Interpretation

This identifies the source of the finite WP17 excess more sharply.

Along the registered direction:

- the (H^2) high-transfer numerator has no linear gain;
- (G) and (X_2) have no linear change;
- the positive-stretching denominator decreases linearly.

So the initial improvement is a **denominator-depletion effect**, not a first-order enhancement of the signed (H^2) transfer.

At finite (arepsilon), nonlinear satellite interactions also enter. The full (arepsilon=1) state reaches the registered WP17 value (approx5.11293), whereas the first variation only describes the local departure from (arepsilon=0).

## 7. Scope barrier

This is one directional derivative in one registered sparse family.

It does not prove that the WP18 state is not a local maximum against every perturbation, does not identify a global supremum, and does not establish any cutoff-independent bound.

The next sharper target is the **variational problem for the positive-stretching functional** around the isolated triad: characterize which satellite directions make

[
P'(0)<0
]

while leaving (N'(0)=G'(0)=X_2'(0)=0), and determine whether that directional gain is uniformly bounded.
