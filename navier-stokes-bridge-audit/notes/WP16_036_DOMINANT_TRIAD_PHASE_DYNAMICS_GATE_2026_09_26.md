# WP16 Dominant-Triad Instantaneous Phase-Dynamics Gate

**Prince Upadhyay, Independent Research — 26 September 2026**

The finite optimizer hierarchy has reduced to the explicit conjugate pair

[
(3,2,2)+(3,-2,1)	o(6,0,3)
]

and its conjugate.

Define its exact H² coefficient

[
z(t)
=
-|k|^4,
overline{a_k}cdot
P_k!left(i(qcdot a_p)a_qight),
qquad
alpha(t)=arg z(t).
]

For (z
e0),

[
oxed{
dotalpha
=
Im!left(rac{dot z}{z}ight)
}.
]

The derivative (dot z) is computed analytically by the product rule after substituting the **full finite Galerkin Navier–Stokes RHS** for (dot a_p,dot a_q,dot a_k).

At each of the three recursive cutoff steps, evaluate:

1. the inherited phase state;
2. the [036]-target-only registered correction;
3. the full final registered phase state.

Report

[
alpha,qquad
dotalpha,qquad
rac{d}{dt}|alpha|,
qquad
rac{d}{dt}cosalpha.
]

A negative local (d|alpha|/dt) means the actual finite Galerkin vector field is instantaneously pushing that triad coefficient toward the favorable phase alignment at that state.

The gate also isolates the viscous contribution. Because viscosity multiplies each Fourier coefficient by a real scalar, its contribution to phase velocity should vanish up to numerical roundoff.

This is an instantaneous finite-dimensional diagnostic only. It does not establish phase locking, attraction, persistence, an all-cutoff law, or continuum regularity.
