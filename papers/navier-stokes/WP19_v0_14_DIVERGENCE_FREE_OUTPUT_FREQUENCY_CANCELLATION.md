# WP19 v0.14 — Divergence-Free Output-Frequency Cancellation and Energy-Level Closure Tail

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact Fourier inequality + explicit closure-tail estimates.  
**Not claimed:** all-cutoff persistence, continuum regularity, singularity, or a Millennium Prize result.

## 1. Incompressibility removes the high derivative

For a Fourier output mode `k=p+q`,

[
widehat{B(a,b)}(k)
=
isum_{p+q=k}(hat a_pcdot q)hat b_q.
]

If the advecting field `a` is divergence-free, then (hat a_pcdot p=0), hence

[
oxed{hat a_pcdot q=hat a_pcdot(k-p)=hat a_pcdot k.}
]

So for a fixed low output `k`, the derivative factor is the output frequency (|k|), not the high input frequency (|q|).

## 2. Exact fixed-output bilinear theorem

Let `P_K` be the divergence-free Fourier projector onto nonzero modes with (|k|le K). Then, for divergence-free `a`,

[
|widehat{P_KB(a,b)}(k)|
le
|k|sum_{p+q=k}|hat a_p||hat b_q|
le
|k||a|_2|b|_2.
]

Therefore

[
oxed{
|P_KB(a,b)|_2
le
C_K|a|_2|b|_2,
qquad
C_K=
left(sum_{0<|k|le K}|k|^2ight)^{1/2}.
}
]

For `K=11`, independent Wolfram enumeration gives:

- nonzero lattice modes: `5574`;
- (sum_{0<|k|le11}|k|^2=404724);
- (C_{11}=sqrt{404724}approx636.179220031588).

This supersedes the weaker v0.13 `L2 x H1` estimate for the present divergence-free velocity inputs.

## 3. Stronger continuum closure truncation

Write

[
v=P_{11}u,qquad h=(I-P_{11})u,
]

and define

[
Gamma(u)
=
-P_{11}[B(v,h)+B(h,v)+B(h,h)].
]

Let (h_M=(P_M-P_{11})u) and (r_M=h-h_M). Then

[
Gamma-Gamma_M
=
-P_{11}[B(v,r_M)+B(r_M,v)+B(h_M,r_M)+B(r_M,h_M)+B(r_M,r_M)].
]

Every first argument is divergence-free, so

[
oxed{
|Gamma-Gamma_M|_2
le
C_{11}left[
2(|v|_2+|h_M|_2)|r_M|_2+|r_M|_2^2
ight].
}
]

Using orthogonality,

[
|v|_2+|h_M|_2lesqrt2,|u|_2,
]

hence

[
oxed{
|Gamma-Gamma_M|_2
le
C_{11}left[
2sqrt2,|u|_2|r_M|_2+|r_M|_2^2
ight].
}
]

Thus, for a divergence-free trajectory bounded in (L^infty(0,T;L^2)), spectral-tail convergence implies

[
Gamma_M(u)	oGamma(u)
quad	ext{in }L^1(0,T;L^2).
]

The fixed-output closure estimate itself is energy-level.

## 4. Direct addition of one high shell

Let `s` be a newly added divergence-free shell and `w=v+h` the previously resolved field. Then

[
DeltaGamma
=
-P_{11}[B(w,s)+B(s,w)+B(s,s)].
]

Therefore

[
oxed{
|DeltaGamma|_2
le
C_{11}left[
2|w|_2|s|_2+|s|_2^2
ight].
}
]

The direct shell-to-low forcing is controlled by shell energy, not shell gradient.

## 5. Absolute shell summability for one Leray-Hopf solution

Let (s_m=(P_{m+1}-P_m)u). Since frequencies in `s_m` satisfy (|k|>m),

[
|s_m|_2le m^{-1}|
abla s_m|_2.
]

Consequently

[
sum_{mge M}|s_m|_2
le
c_M|
abla u|_2,
qquad
c_M=left(sum_{mge M}m^{-2}ight)^{1/2},
]

and

[
sum_{mge M}|s_m|_2^2
le
M^{-2}|
abla u|_2^2.
]

Writing

[
U=|u|_{L^infty_tL^2_x},
qquad
D=|
abla u|_{L^2_tL^2_x},
]

gives

[
oxed{
sum_{mge M}
|DeltaGamma_m|_{L^1_tL^2_x}
le
C_{11}left[
2U,c_Msqrt T,D+M^{-2}D^2
ight].
}
]

Using the Leray-Hopf energy inequality yields

[
oxed{
sum_{mge M}
|DeltaGamma_m|_{L^1_tL^2_x}
le
C_{11}|u_0|_2^2
left[
sqrt{rac{2T}{
u}},c_M+rac{1}{2
u M^2}
ight].
}
]

Because (c_Msim M^{-1/2}), the tail tends to zero. Thus direct shell-to-low closure increments are absolutely summable **within one fixed Leray-Hopf solution**.

## 6. Consecutive Galerkin systems: remaining obstruction

For separate Galerkin solutions `u_M` and `u_{M+1}`, the newly opened shell belongs to a different solution at every cutoff. Uniform energy/dissipation control gives only a worst-case direct single-step estimate with leading (O(M^{-1})), which is not summable over `M`.

Therefore energy control alone is enough for fixed-solution closure truncation and direct-shell summability inside one fixed solution, but not by itself for summable consecutive-Galerkin transfer.

A sufficient upgrade would be integrated shell decay

[
|s_M|_{L^1_tL^2_x}le C M^{-1-arepsilon}
]

for some (arepsilon>0). A uniform positive regularity gain, Gevrey tail, or dissipation-wavenumber estimate could supply such decay.

The recursive state-drift term

[
Gamma_M(P_Mu_{M+1})-Gamma_M(u_M)
]

remains the natural target of the fixed-(Pi_{11}) stability/adjoint machinery.

## 7. Revised proof architecture

The all-cutoff problem is now decomposed into

[
oxed{
	ext{direct shell term}
+
	ext{recursive state-drift term}.
}
]

Incompressibility removes the high derivative from the direct term. The remaining issue is shell-energy decay plus backreaction control.

## Claim boundary

v0.14 is an exact refinement of the fixed-output closure estimates. It does not prove all-cutoff negativity or continuum regularity. It shows that direct high-frequency coupling into the fixed N11 output space is substantially weaker than a naive derivative count suggests and isolates the remaining non-summable worst-case mechanism under energy control alone.
