# WP19 v0.13 — Fixed-Output Bilinear Closure Bound and Continuum Low-Mode Passage

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact Fourier inequality + continuum low-mode closure theorem + weak-limit transfer criterion.  
**Not claimed:** all-N negativity, singularity, global regularity, or uniqueness of Leray–Hopf weak solutions.

## 1. Fixed-output bilinear estimate

Let (P_{11}) project to the nonzero integer Fourier modes with (|k|le11). There are exactly 5574 such output wavevectors.

For divergence-free Fourier fields (a,b),

[
widehat{P_{11}B(a,b)}(k)
=
P_ksum_{p+q=k}i(qcdot hat a_p)hat b_q.
]

The modewise Leray projector has operator norm at most one, so Cauchy–Schwarz gives, for each fixed output (k),

[
|widehat{P_{11}B(a,b)}(k)|
le
|a|_{ell^2}|b|_{dot H^1}.
]

Summing over the fixed 5574 outputs yields

[
oxed{
|P_{11}B(a,b)|_{ell^2}
le
sqrt{5574},
|a|_{ell^2}
|b|_{dot H^1}
}
]

with

[
sqrt{5574}approx74.659225819720.
]

The constant is independent of the outer Galerkin cutoff.

## 2. Continuum closure truncation

For a velocity field (u), write

[
v=P_{11}u,qquad h=(I-P_{11})u.
]

Define

[
Gamma(u)
=
-P_{11}[B(v,h)+B(h,v)+B(h,h)].
]

Let

[
h_M=(P_M-P_{11})u,qquad r_M=h-h_M,
]

and define (Gamma_M(u)) by replacing (h) with (h_M).

Then

[
Gamma-Gamma_M
=
-P_{11}[B(v,r_M)+B(r_M,v)+B(h_M,r_M)+B(r_M,h_M)+B(r_M,r_M)].
]

Applying the fixed-output bilinear estimate gives

[
egin{aligned}
|Gamma-Gamma_M|_2
le C_{11}ig(&
|v|_2|r_M|_{dot H^1}
+|r_M|_2|v|_{dot H^1}\
&+|h_M|_2|r_M|_{dot H^1}
+|r_M|_2|h_M|_{dot H^1}
+|r_M|_2|r_M|_{dot H^1}
ig).
end{aligned}
]

For any Leray–Hopf solution,

[
uin L^infty(0,T;L^2)cap L^2(0,T;H^1),
]

and the spectral tail (r_M	o0) in (L^2_tL^2_xcap L^2_tH^1_x). Hence

[
oxed{
Gamma_M(u)	oGamma(u)
quad	ext{in }L^1(0,T;L^2).
}
]

So fixed low-mode recursive closure has a well-defined continuum weak-solution limit without assuming smoothness.

## 3. Passage of the frozen observable

Standard Fourier–Galerkin compactness gives, along a Leray construction subsequence, convergence of the finitely many (P_{11}) Fourier coefficients uniformly in time.

The frozen signed C500 numerator (J) is a finite polynomial in exactly those coefficients. Therefore

[
oxed{
J(P_{11}u_M(T))
	o
J(P_{11}u(T))
}
]

along that subsequence.

Consequently, if a future theorem establishes a cutoff-uniform margin

[
J(P_{11}u_M(T))le-delta<0
]

for all sufficiently large cutoffs, then the same negative signed numerator passes to the Leray–Hopf weak limit.

For (G=J/|z|^2), a uniform nonzero-normalizer lower bound is additionally required.

This is a continuum observable passage, not a regularity theorem.

## 4. Direct shell-addition bound

For one fixed state, add a new high shell (s) to an existing resolved high field (h). Then

[
DeltaGamma
=
-P_{11}[B(v+h,s)+B(s,v+h)+B(s,s)].
]

Therefore

[
oxed{
|DeltaGamma|_2
le
C_{11}
[
|v+h|_2|s|_{dot H^1}
+
|s|_2|v+h|_{dot H^1}
+
|s|_2|s|_{dot H^1}
].
}
]

This is an explicit cutoff-independent estimate for the direct shell-to-low closure increment.

It is not yet the full consecutive-Galerkin estimate because the already existing low and high coefficients also drift when the cutoff changes.

## 5. Next decomposition

For consecutive Galerkin solutions,

[
Gamma_{M+1}(u_{M+1})-Gamma_M(u_M)
]

should be split into

[
[
Gamma_{M+1}(u_{M+1})-Gamma_M(P_Mu_{M+1})
]
+
[
Gamma_M(P_Mu_{M+1})-Gamma_M(u_M)
].
]

The first term is the direct new-shell contribution and is attacked by the shell-addition estimate.

The second term is the recursive state/backreaction drift and requires the existing stability/adjoint machinery.

This yields the next architecture:

[
oxed{
	ext{new shell}
	o
	ext{direct closure forcing}
	o
	ext{state drift}
	o
	ext{fixed signed numerator}.
}
]

No moving endpoint support is needed.

## Claim boundary

v0.13 proves a cutoff-independent fixed-output bilinear estimate and a continuum truncation theorem for the low-mode closure forcing. It also shows how a future all-cutoff negative signed-numerator margin would pass to a Leray–Hopf weak limit.

It does not prove that such an all-cutoff margin exists, and it does not turn the low-mode observable into a regularity or singularity criterion.
