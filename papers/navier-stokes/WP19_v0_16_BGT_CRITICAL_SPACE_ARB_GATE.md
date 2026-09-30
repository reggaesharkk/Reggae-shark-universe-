# WP19 v0.16 — Rigorous Critical-Space A-Posteriori No-Go for the N14 Reconstruction

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** 160-bit Arb screen of one published sufficient strong-existence criterion.  
**Not claimed:** blowup, singularity, failure of continuum strong existence, an all-cutoff theorem, or a Millennium Prize result.

## 1. Question

WP19 v0.15 found that the full-PDE truncation residual of the validated N14 Galerkin trajectory is much smaller in negative Sobolev norms than in positive Sobolev norms.

v0.16 asks whether the critical-space a-posteriori criterion of Brunk, Giesselmann and Tscherpel can rigorously certify a continuum strong solution on the interval corresponding to the existing N14 reconstruction.

The paper uses a periodic unit torus, an (L^\infty_tL^3_x)-based conditional stability theorem, and residuals measured in negative Sobolev norms. Its published criterion is sufficient, not necessary.

## 2. Normalization

The project uses

[
u(x,t)=\sum_k a_k(t)e^{ik\cdot x}
]

on ([0,2\pi)^3), with volume-normalized spatial norms.

To match the unit torus, v0.16 uses the exact Navier–Stokes parabolic scaling

[
U(y,s)=2\pi,u(2\pi y,4\pi^2s).
]

Thus

[
T_\mathrm{unit}=\frac{0.003}{4\pi^2}
\approx 7.599088773175334\times10^{-5},
]

and viscosity remains (\nu=0.1).

The paper's explicit constants used here are

[
c_{\Pi,1}=14,\qquad
c_{\Pi,2}=35,\qquad
c_{e,1}=24,\qquad
c_{e,2}=22.
]

## 3. Immutable N14 provenance

The screen uses exactly the N14 cubic-Hermite reconstruction already validated by the same-datum workflow:

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- `nodes.npy` SHA-256: `e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0`
- `rhs.npy` SHA-256: `f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253`
- N14 workflow-artifact SHA-256: `b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`
- certified low-mode whole-segment residual maximum: `0.000216927907`

No trajectory was retuned.

## 4. First-segment lower gate

A single omitted Fourier mode was chosen from the prior floating residual scout:

[
k_*=(12,5,6),\qquad |k_*|^2=205>14^2.
]

This mode lies outside the N14 Galerkin ball, so the low-mode Hermite residual cannot cancel it.

Using 160-bit Arb arithmetic and the exact rational initial state, v0.16 proves over the **entire first Hermite segment**:

- initial original-torus (L^2) norm lower: `111.22062618900332957644131182146961031683424706`
- total first-segment state variation (L^2) upper: `0.20191508932990209009433679062071986606139307527`
- first-segment (L^2) norm lower: `111.01871109967342748634697503084889045077285398`
- omitted-mode coefficient at segment start lower: `12.168410232983179160866311411127012336129541966`
- coefficient derivative in normalized segment time upper: `0.22977132412642886902192501195319778035713322028`
- omitted-mode coefficient whole-segment lower: `11.938638908856750291844386399173814555772408745`
- resulting unit-torus (W^{-1,2}) residual lower from this one mode: `32.916283452305218229613865172324996701687395009`

Therefore the criterion's nonnegative quantity (A) satisfies already from this one mode and one segment

[
oxed{A>0.0072042895280746927301928259268113655639331528449}.
]

## 5. The decisive obstruction is the stability exponential

On the unit torus,

[
\|U\|_6\ge \|U\|_2.
]

Using only the first-segment (L^2) lower bound inside the positive quartic term of the published stability exponent gives

[
oxed{\log M>9326757996764.8738490354363009704209812823016322}.
]

No high-norm upper estimate is needed for this lower obstruction.

Using only one positive term of the criterion's left-hand side then gives

[
oxed{
\log(\mathrm{criterion\ LHS})
>
6217838664529.3108075792426229113633088599335314
>0.
}
]

Hence the required inequality `LHS <= 1` is rigorously false for this N14 Hermite reconstruction with the stated published constants.

The gap is not marginal. Even ignoring every other positive contribution, the first term would require approximately

[
\log A \lesssim -9.326758\times10^{12},
]

whereas the certified one-mode/one-segment lower bound gives

[
\log A > \log(0.0072042895280746927301928259268113655639331528449)
\approx -4.933079.
]

Thus simply sharpening the residual estimate cannot rescue this particular sufficient criterion. The dominant issue is the stability/Gronwall architecture for this high-amplitude reconstruction.

## 6. Whole-path Arb upper envelopes

For completeness, v0.16 also computes rigorous but intentionally conservative whole-path envelopes. The high residual is bounded with Fourier inequalities while the low component uses the already certified Hermite residual bound.

The resulting unit-torus bounds include:

- `sup ||U||_2 <= 698.81980432605884578748197527645369769168428325`
- `sup ||U||_(W^1,2) <= 8982.0323411688547341185136235298126070299323532`
- Fourier coefficient `l1 <= 4325.1221853759392525136446910721976648571208126`
- full residual `W^-1,2` maximum upper `2645826649.0987594799472040940823639671156236873`
- full residual `W^-1,3` maximum upper `18706683.102229440552840763331779342002013351536`
- `integral ||r||_(W^-1,2)^2 <= 508774442987785.95412593162631368247800151206311`
- `integral ||r||_(W^-1,3)^3 <= 314123572910245797.15766044455595656616781382577`

These whole-path upper envelopes are deliberately coarse and are **not** used to prove the no-go. The no-go is supplied by the separate first-segment lower gate.

## 7. Result

[
oxed{\text{The published BGT sufficient criterion does not certify this N14 reconstruction.}}
]

This is stronger than saying that our upper bounds are too loose: a rigorous **lower bound** on the criterion's own left-hand side already exceeds one by an enormous margin.

It does **not** imply finite-time blowup, singularity, nonexistence of a continuum strong solution, failure of another a-posteriori theorem, or failure of a sharper reconstruction-specific stability estimate.

## 8. What this changes

The v0.15 plan was to spend substantial effort tightening (W^{-1,3}) and whole-segment residual estimates and then try the published critical-space condition.

v0.16 shows that this would not be productive for this reconstruction and criterion. The first-segment stability exponential is already fatal.

The continuum program therefore pivots from generic universal constants to a reconstruction-specific stability calculation:

[
oxed{\text{validated Fourier-linearized stability about the N14 path}}.
]

That calculation should separate:

1. the finite low/intermediate linearized block, propagated with validated tangent/adjoint evolution;
2. the sufficiently high tail, where (\nu|k|^2) gives explicit damping;
3. the quadratic error term, handled by a bootstrap radius;
4. the known full-PDE residual (Q_{14}B(v,v)).

A successful contraction would certify continuum strong existence for this explicit datum and interval. A failure would be retained as a quantitative obstruction.

## References

- A. Brunk, J. Giesselmann, T. Tscherpel, *A posteriori existence of strong solutions to the Navier-Stokes equations in 3D*, arXiv:2509.25105.
- M. Dashti, J. C. Robinson, *An A Posteriori Condition on the Numerical Approximations of the Navier-Stokes Equations for the Existence of a Strong Solution*, SIAM J. Numer. Anal. 46 (2008), 3136–3150.
- S. I. Chernyshenko, P. Constantin, J. C. Robinson, E. S. Titi, *A Posteriori Regularity of the Three-dimensional Navier-Stokes Equations from Numerical Computations*, J. Math. Phys. 48 (2007), 065204.

## Claim boundary

This result rules out one sufficient certification route for one fixed reconstruction. It is not evidence for singularity and does not resolve continuum Navier-Stokes regularity.
