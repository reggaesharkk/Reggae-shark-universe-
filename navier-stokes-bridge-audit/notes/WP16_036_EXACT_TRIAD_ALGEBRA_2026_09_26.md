# WP16 Exact [223]+[123]→[036] Triad Algebra

**Prince Upadhyay, Independent Research — 26 September 2026**

The exact symmetry gate collapses all 48 signed/permuted triads in the persistent partner motif to a single cubic signed-permutation class at each tested step:

[
N8	o N9,qquad N9	o N10,qquad N10	o N11.
]

A canonical representative is

[
p=(-3,-2,-2),qquad
q=(-3,-1,2),qquad
k=(-6,-3,0),
]

with the exact triad relation

[
p+q=k.
]

Its integer geometry is

[
|p|^2=17,qquad |q|^2=14,qquad |k|^2=45,
]

[
pcdot q=7,qquad
pcdot k=24,qquad
qcdot k=21,
]

and

[
p	imes q=(-6,12,-3).
]

For (k=(-6,-3,0)),

[
P_k=I-rac{kotimes k}{|k|^2}
=
egin{pmatrix}
1/5 & -2/5 & 0\
-2/5 & 4/5 & 0\
0 & 0 & 1
end{pmatrix}.
]

The ordered H² high-advector triad coefficient used by the finite Galerkin code is

[
z_0
=
-|k|^4,overline{a_k}cdot
P_k!left(i(qcdot a_p)a_qight).
]

Since (a_k) is divergence-free,

[
P_k a_k=a_k,
]

and therefore, by self-adjointness of (P_k),

[
overline{a_k}cdot P_k a_q
=
overline{a_k}cdot a_q.
]

Also, since (pcdot a_p=0) and (q=k-p),

[
qcdot a_p=kcdot a_p.
]

Thus the representative coefficient reduces exactly to

[
oxed{
z_0=-2025,i,
(kcdot a_p)
(overline{a_k}cdot a_q)
}
]

because

[
|k|^4=45^2=2025.
]

This is the current smallest exact algebraic description of the persistent finite motif.

## Interpretation boundary

The one-class collapse is a statement about the discrete cubic symmetry of this finite triad family. The 48 numerical contributions need not be equal because the evolved Fourier amplitudes are not themselves cubically symmetric.

The exact coefficient formula does not establish a cutoff-uniform bound or a Navier–Stokes regularity theorem. The next useful question is whether the phase optimization repeatedly drives the dominant members of this class toward a simple phase condition maximizing

[
Re!left[z_0 e^{i	heta}ight].
]
