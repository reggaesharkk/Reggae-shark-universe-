# WP19 v0.12 — Recursive Low/High Closure Theorem and Regularity Compatibility Gate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact projection identities and an abstract cutoff-transfer theorem, plus regularity no-go results.  
**Not claimed:** an all-N cutoff theorem, continuum singularity theorem, global regularity theorem, or Millennium Prize solution.

## Validated context

The prospective same-rational-datum N14 validation passed.

Frozen setup:
- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- nu = 0.1
- T = 0.003
- 120 whole-segment 128-bit Arb enclosures

Validated N14 outputs:
- result: PASS
- terminal L2 trajectory-error upper bound: `0.000012825905`
- F(0) in `[645.8037741471, 645.8037741472]`
- F(T) in `[-89.015834781, -85.160766265]`
- whole-path normalizer lower bound: `48850.68586052`

Thus the rigorous same-datum finite-Galerkin chain is N11, N12, N13, N14.

## Exact recursive closure identity

Fix the low projector P = P11. For each cutoff M >= 11, split

```
u_M = v_M + h_M
v_M = P11 u_M
h_M = (P_M - P11) u_M
```

The same frozen datum lies entirely inside N11, so h_M(0) = 0.

Applying P11 to the Galerkin equation gives

```
d v_M/dt + nu A v_M + P11 B(v_M,v_M) = Gamma_M
```

with exact high-to-low feedback

```
Gamma_M = -P11[
    B(v_M,h_M)
  + B(h_M,v_M)
  + B(h_M,h_M)
]
```

The high subsystem is

```
d h_M/dt + nu A h_M
+ (P_M-P11) B(v_M+h_M, v_M+h_M) = 0.
```

So the exact feedback loop is

```
v_M -> h_M -> Gamma_M -> v_M.
```

This is the mathematical version of the recursive-closure idea. It is a direct Fourier projection identity, not a cosmological assumption.

Because h_M(0)=0, the high state also has the exact Duhamel form

```
h_M(t) = - integral_0^t exp[-nu A(t-s)]
          (P_M-P11) B(v_M+h_M, v_M+h_M)(s) ds.
```

Substituting this into the low equation gives an exact non-Markovian equation for the fixed low state.

## Recursive Low-Mode Closure Theorem

For two cutoffs M,L >= 11, let e = v_M - v_L. Subtracting the two low equations and using incompressibility gives the energy inequality

```
1/2 d/dt ||e||_2^2 + nu ||grad e||_2^2
<= ||S(v_L)||_{L-infinity,op} ||e||_2^2
 + ||Gamma_M-Gamma_L||_2 ||e||_2.
```

Since v_L always belongs to the fixed N11 Fourier space,

```
||S(v_L)||_infinity <= C_strain,11 ||v_L||_2
                     <= C_strain,11 ||u_0||_2.
```

One explicit coefficient-space choice is

```
C_strain,11 = sqrt( sum_{0<|k|<=11} |k|^2 ).
```

Therefore

```
||v_M(t)-v_L(t)||_2
<= exp(C_strain,11 ||u_0||_2 t)
   integral_0^t ||Gamma_M(s)-Gamma_L(s)||_2 ds.
```

Hence, if Gamma_M is Cauchy in L1(0,T;L2), the fixed low projections P11 u_M are Cauchy in C([0,T];L2).

## Transfer of the frozen signed numerator

WP19 v0.11 proved that the frozen C500 signed numerator and normalizer depend only on P11 u_M for every M >= 11.

Inside one fixed K36 sign chamber, define

```
J(v) =
  sum_{g in K36} sigma_g n_g(v)
  - 9 sum_{g in C500} tau_g n_g(v).
```

J is a finite polynomial on the fixed N11 coordinate space. On the energy ball there is therefore a finite Lipschitz constant L_J such that

```
|J(v)-J(w)| <= L_J ||v-w||_2.
```

Combining with the closure theorem gives the sufficient transfer estimate

```
|J(v_M(T))-J(v_L(T))|
<= L_J exp(C_strain,11 ||u_0||_2 T)
   ||Gamma_M-Gamma_L||_{L1_t L2_x}.
```

A sufficient all-cutoff sign condition is that the starting negative numerator margin dominates the summed future closure increments.

## What K36/C500 actually measures

For each retained ordered nonlinear source group g, the quantity used in the observable is the normalized imaginary component of that group's contribution to the tracked complex K-mode turnover normalizer.

It captures a source-resolved nonlinear angular-forcing contribution. The complete time derivative of the phase also contains the viscous contribution and the time derivative of the P,Q anchor because those coefficients evolve.

Therefore the K36 observable is a source-orbit redistribution diagnostic, not the complete phase derivative and not a singularity indicator.

## Static regularity no-go result

Negative F or negative G_C500 can occur on a finite Fourier state. Such a state is a smooth trigonometric polynomial.

Therefore a theorem of the form

```
G_C500(u(t)) < 0  =>  singularity at t
```

cannot be universally true.

This rules out the naive observable-to-singularity shortcut.

## High-frequency blindness no-go result

For every cutoff M >= 11,

```
G_C500(a) = G_C500(P11 a)
```

whenever the tracked normalizer is nonzero.

Thus one can alter arbitrarily high-frequency smooth components without changing G_C500. Therefore G_C500 alone cannot control a high-frequency continuation quantity such as a vorticity supremum, high Sobolev norm, shell Reynolds number, or determining/dissipation wavenumber.

## Correct regularity architecture

The viable architecture is two-coordinate:

```
fixed low-mode recursive closure
+
independent high-frequency dissipation/continuation control.
```

The low coordinate is the fixed signed numerator J(P11 u). The high coordinate must genuinely see the tail.

A natural next target is

```
||Gamma_{M+1}-Gamma_M||_{L1_t L2_x} <= E_M
```

with E_M controlled by a high-frequency quantity whose tail is summable or viscously absorbable.

## Claim boundary

v0.12 does not prove all-N persistence, singularity, or regularity. It identifies the exact recursive feedback variable Gamma_M and the mathematical condition under which a future all-cutoff negative signed-numerator theorem would follow.
