# WP19 v0.12 — Recursive Low/High Closure Theorem and Regularity Compatibility Gate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact projection identities and abstract cutoff-transfer theorem; regularity no-go results; literature-linked next gate.  
**Not claimed:** an all-N cutoff theorem, a continuum singularity theorem, global regularity, or a Millennium Prize result.

## 0. New validated context: N14 passed

The prospective same-rational-datum N14 GitHub Actions validation completed successfully.

Frozen data:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- `nu = 0.1`
- `T = 0.003`
- 120 whole-segment 128-bit Arb enclosures

Validated N14 result:

- result: `PASS`
- terminal trajectory-error upper bound: `0.000012825905`
- exact initial F interval: `[645.8037741471, 645.8037741472]`
- endpoint F interval: `[-89.015834781, -85.160766265]`
- whole-path normalizer lower bound: `48850.68586052`

Thus the rigorous same-datum finite-Galerkin chain is now N11, N12, N13, N14.

This still does not imply an all-N or continuum result.

---

# Part I — Recursive closure as an exact Navier–Stokes projection identity

Consider the periodic incompressible Navier–Stokes Galerkin system

[
partial_t u_M+
u A u_M+P_M B(u_M,u_M)=0,
qquad 
ablacdot u_M=0,
]

with (A=-Delta), (B(a,b)=(acdot
abla)b), and (P_M) the divergence-free Fourier projector to cutoff (M).

Fix

[
P:=P_{11},qquad Q_M:=P_M-P.
]

For every (Mge11), split

[
u_M=v_M+h_M,
qquad
v_M=Pu_M,
qquad
h_M=Q_Mu_M.
]

The same-datum experiment has (h_M(0)=0).

Applying (P) gives the exact low equation

[
oxed{
partial_t v_M+
u A v_M+P B(v_M,v_M)=Gamma_M,
}
]

where

[
oxed{
Gamma_M=
-Pigl(
B(v_M,h_M)+B(h_M,v_M)+B(h_M,h_M)
igr).
}
]

The high subsystem is

[
oxed{
partial_t h_M+
u A h_M+
Q_M B(v_M+h_M,v_M+h_M)=0.
}
]

Hence the exact feedback loop is

[
v_Mlongrightarrow h_Mlongrightarrow Gamma_Mlongrightarrow v_M.
]

This is the precise mathematical form of recursive closure.

Since (h_M(0)=0),

[
h_M(t)=
-int_0^t e^{-
u A(t-s)}
Q_M B(v_M+h_M,v_M+h_M)(s),ds.
]

Substitution into the low equation produces an exact non-Markovian finite-dimensional equation for (v_M). Equivalently, ((v_M,h_M)) is a fixed point of the coupled Duhamel map. This is the PDE analogue of an abstract relation (C(U^*)=U^*).

---

# Part II — Recursive Low-Mode Closure Theorem

Define

[
mathcal F(v)=-
u Av-PB(v,v).
]

Then

[
dot v_M=mathcal F(v_M)+Gamma_M.
]

For (M,Lge11), let

[
e=v_M-v_L.
]

Subtracting the two low equations yields

[
partial_t e+
u Ae+
Pigl(B(e,v_L)+B(v_M,e)igr)
=
Gamma_M-Gamma_L.
]

Because (v_M) is divergence free,

[
langle B(v_M,e),eangle=0.
]

Therefore

[
rac12rac{d}{dt}|e|_2^2
+
u|
abla e|_2^2
le
|S(v_L)|_{L^infty,mathrm{op}}|e|_2^2
+
|Gamma_M-Gamma_L|_2|e|_2.
]

Since (v_L) always lies in the fixed N11 space,

[
|S(v_L)|_infty
le C_{11}|v_L|_2
le C_{11}|u_0|_2,
]

where one valid Fourier coefficient constant is

[
C_{11}
=
left(
sum_{0<|k|le11}|k|^2
ight)^{1/2}
]

up to the fixed torus normalization convention.

Thus

[
oxed{
|v_M(t)-v_L(t)|_2
le
e^{C_{11}|u_0|_2t}
int_0^t
|Gamma_M(s)-Gamma_L(s)|_2,ds.
}
]

This is the Recursive Low-Mode Closure Theorem.

### Consequence

If (Gamma_M) is Cauchy in (L^1(0,T;L^2)), then (v_M=P_{11}u_M) is Cauchy in (C([0,T];L^2)).

The stability coefficient is fixed once N11 and the initial energy are fixed; there is no moving-cutoff strain constant.

---

# Part III — Transfer of the frozen signed numerator

WP19 v0.11 proved that for every (Mge11), the frozen C500 signed numerator and its normalizer depend only on (v_M=P_{11}u_M).

Inside a fixed K36 sign chamber define

[
J(v)
=
sum_{gin K36}sigma_g n_g(v)
-
9sum_{gin C500}	au_g n_g(v).
]

This is a finite polynomial in the N11 Fourier coordinates.

On the energy ball (|v|_2le|u_0|_2), there is a finite computable Lipschitz constant (L_J) with

[
|J(v)-J(w)|le L_J|v-w|_2.
]

Hence

[
oxed{
|J(v_M(T))-J(v_L(T))|
le
L_J e^{C_{11}|u_0|_2T}
|Gamma_M-Gamma_L|_{L^1_tL^2_x}.
}
]

A sufficient all-cutoff sign condition is

[
J(v_{N_0}(T))
+
L_J e^{C_{11}|u_0|_2T}
sum_{M=N_0}^{infty}
|Gamma_{M+1}-Gamma_M|_{L^1_tL^2_x}
<0.
]

If this inequality were certified, the frozen signed numerator would remain negative at every later cutoff.

This is the rigorous mathematical role of recursive closure in the current program.

---

# Part IV — What K36/C500 measures

Let

[
z=-|K|^4langle a_K,bangle
]

be the tracked complex normalizer. For an ordered nonlinear source group (g), let (d_g) be its contribution to the (K)-mode right-hand side and define

[
w_g=-|K|^4langle d_g,bangle.
]

Then

[
y_g=
rac{operatorname{Im}(w_goverline z)}{|z|^2}
]

is the contribution of that (K)-mode nonlinear source group to the angular velocity of (z) through the (a_K)-derivative term.

The complete derivative of (arg z) also contains the viscous contribution to (dot a_K) and the derivative of the anchor (b), because (a_P) and (a_Q) evolve.

Therefore K36 is not the complete phase derivative of (z).

The original margin

[
F=I-9O
]

compares the absolute nonlinear angular forcing carried by the frozen selected orbit families against the absolute forcing carried by all other source families.

The validated crossing is therefore a redistribution of nonlinear phase-turnover forcing among source-orbit families.

---

# Part V — Static regularity no-go theorem

The project contains smooth finite Fourier states with negative K36/C500 endpoint values.

A finite trigonometric polynomial is smooth, indeed analytic, in space.

Therefore

[
F(a)<0
quad	ext{or}quad
G_{C500}(a)<0
]

cannot by itself imply that the state (a) is singular.

Taking such a smooth divergence-free finite Fourier field as continuum Navier–Stokes initial data gives, by standard local well-posedness, a smooth solution for a nonzero time interval.

Hence no universal theorem of the form

[
G_{C500}(u(t))<0
Longrightarrow
	ext{loss of local smoothness at }t
]

can be true.

This rules out the naive observable-to-singularity bridge.

---

# Part VI — High-frequency blindness no-go theorem

For every (Mge11),

[
G_{C500}(a)=G_{C500}(P_{11}a)
]

whenever the normalizer is nonzero.

Fix a low field (v=P_{11}a), and add an arbitrary smooth divergence-free field (h) supported above N11.

Then

[
G_{C500}(v+h)=G_{C500}(v),
]

while high-frequency quantities such as

[
|omega|_infty,qquad
|u|_{H^s},qquad
lambda_q^{-1}|u_q|_infty/
u
]

can be made arbitrarily large by changing the frequency and amplitude of (h).

Therefore G alone cannot control a high-frequency continuation quantity or a determining/dissipation wavenumber.

The fixed-support theorem is useful for cutoff transfer, but it simultaneously proves that the observable is blind to arbitrarily high-frequency state information.

---

# Part VII — Correct regularity architecture

Published 3D Navier–Stokes regularity theory includes time-dependent determining/dissipation wavenumbers. A representative high-frequency condition has the form

[
lambda_p^{-1}|u_p(t)|_infty<c_0
u
quad	ext{for all shells }p>q.
]

This identifies a dissipation range where viscosity dominates the high shells.

Work by Cheskidov, Dai, Kavlie and subsequent authors links such wavenumbers and high-frequency vorticity criteria to regularity/blowup behavior.

Therefore the viable architecture is not

[
G<0Rightarrow	ext{regularity or singularity}.
]

It is

[
oxed{
	ext{fixed low-mode recursive closure}
+
	ext{independent high-frequency dissipation control}.
}
]

The low coordinate is (J(P_{11}u)).

The high coordinate must actually see the tail, for example a determining/dissipation wavenumber, a high-shell vorticity integral, or an established continuation quantity.

---

# Part VIII — New theorem target

The next theorem should connect the two coordinates through the closure increment:

[
oxed{
|Gamma_{M+1}-Gamma_M|_{L^1(0,T;L^2)}
le mathcal E_M,
}
]

where (mathcal E_M) is controlled by a high-frequency quantity that is summable or viscously absorbable in a regular regime.

Then:

1. high-frequency dissipation gives a summable closure budget;
2. recursive low-mode stability gives convergence of (P_{11}u_M);
3. the signed-numerator estimate transfers the negative endpoint margin;
4. standard Galerkin compactness passes fixed low modes to a Leray–Hopf weak limit;
5. regularity still requires the independent high-frequency continuation criterion.

The genuinely new coupling question is:

> Can the shellwise closure increment (Gamma_{M+1}-Gamma_M) be bounded sharply enough by a dissipation-wavenumber or vorticity-tail quantity to obtain a summable all-cutoff budget?

This is the correct place to test the recursive-closure idea against regularity theory.

---

# References

- A. Cheskidov, M. Dai, L. Kavlie, *Determining modes for the 3D Navier–Stokes equations*, Physica D 374–375 (2018), 1–9. DOI: 10.1016/j.physd.2017.11.014. arXiv:1507.05908.
- A. Cheskidov, M. Dai, *Regularity criteria for the 3D Navier–Stokes and MHD equations*, Proceedings of the Edinburgh Mathematical Society 68 (2025), 1262–1296. DOI: 10.1017/S0013091525100813. arXiv:1507.06611.

## Claim boundary

v0.12 does not prove that the observable implies regularity or blowup.

It proves the useful opposite fact: the observable alone cannot do that.

What it provides is an exact recursive low/high closure architecture and a sufficient mathematical condition for cutoff-uniform transfer of the frozen signed numerator. The next gate is a shellwise high-to-low closure estimate compatible with an established high-frequency regularity criterion.
