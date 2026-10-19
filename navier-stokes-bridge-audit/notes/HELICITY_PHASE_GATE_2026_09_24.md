# Zero-helicity phase gate for enstrophy production

**Scope:** an exact instantaneous six-mode example on the unforced
periodic torus. This post-v0.2 note does not assert a long-time phase
law or settle a regularity criterion.

## Explicit real solenoidal field

Use the integer triad \(P=(1,0,0)\), \(Q=(0,1,1)\), \(R=P+Q=(1,1,1)\).
For any \(A>0\) and \(\theta\in\mathbb R\), set

\[
a_P=A(0,-1,-1),\quad
a_Q=A(-1,-1,1),\quad
a_R=Ae^{i\theta}(-1,0,1),\quad
a_{-k}=\overline{a_k}.
\]

Each coefficient is perpendicular to its wavevector. The three real
polarization vectors imply \(\overline{a_k}\cdot(i k\times a_k)=0\)
for **every occupied mode**, independently of \(\theta\). Thus both
the individual signed modal helicities and total helicity
\(H=\langle u\cdot\omega\rangle\) vanish exactly.

Direct evaluation of the six-mode triad convolution gives

\[
E=7A^2,\qquad G=28A^2,\qquad D=64A^2,\qquad
T=\langle\omega\cdot S\omega\rangle=4A^3\sin\theta.
\]

The modal powers and \(E,G,D,H\) are identical for all \(\theta\),
but \(T\) ranges from \(-4A^3\) to \(+4A^3\). At \(A=2\),
\(\theta=\pi/2\), and \(\nu=0.1\), \(T=32\), \(\nu D=25.6\),
and \(G'/2=T-\nu D=6.4>0\) instantaneously. This is ordinary
short-time enstrophy growth, not a singularity.

## What the example rules out

Zero total helicity, and even zero **signed helicity in every occupied
Fourier mode**, does not force zero or nonpositive vortex stretching.
A one-sided majorant whose proposed nonlinear remainder vanishes
whenever all these signed helicities vanish cannot hold for arbitrary
amplitude: \(T\) scales as \(A^3\), whereas \(D\) scales as \(A^2\).
Power spectra, scalar spectral entropies, and signed modal helicity
do not determine the exact signed transfer in this family.

This does **not** rule out a majorant that accounts for both helical
polarizations, local helicity density, geometry, or the full triad
phases. In particular, a *helical-decimated* equation that projects
onto one sign of helicity at each mode throughout evolution is a
different dynamical system; its known regularity result does not
transfer to the unrestricted Navier–Stokes evolution. See Biferale
and Titi, `https://arxiv.org/abs/1303.1215`.

## Reproduce and next gate

Run `python src/helicity_phase_gate.py` from the repository root.
The script writes `src/helicity_phase_results.json`, asserts the
closed-form values at \(\theta\in\{0,\pi/2,\pi,3\pi/2\}\) for
\(A\in\{1,2\}\), and independently checks spectral transfer against
spatial quadrature. Errors are at roundoff scale.

A proposed helicity-aware estimate should specify whether it uses
signed totals, magnitudes of opposite helicity components, local
helicity density, or time-persistent helical polarization. Evaluate
its amplitude and localized-concentration scaling before screening
the stored trajectory traces. No scalar-entropy or signed-helicity
summary can recover the missing relative triad phase here.
