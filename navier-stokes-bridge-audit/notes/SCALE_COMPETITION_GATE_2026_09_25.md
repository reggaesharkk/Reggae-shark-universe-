# Scale-competition gate: sampled coherence length versus vorticity-gradient length (post-v0.2)

## Why this gate

The previous gates established two facts:

1. a useful geometric coordinate must retain an **absolute length scale**;
2. the high-vorticity sampled coherence radius shrinks most strongly in the
   aggressively perturbed \(N=7\) trajectory.

The next step is therefore to compare that geometric length to a second,
independently defined dynamical length available directly from the Fourier
state.

## Exact vorticity-gradient length

Define

\[
G(t)=\|\omega(t)\|_2^2,
\qquad
D(t)=\|\nabla\omega(t)\|_2^2,
\]

and

\[
\ell_\omega(t)
=
\sqrt{\frac{G(t)}{D(t)}}.
\]

This has a direct spectral interpretation:

\[
\ell_\omega^{-2}
=
\frac{\sum_k |k|^4|\widehat u_k|^2}
{\sum_k |k|^2|\widehat u_k|^2},
\]

so \(\ell_\omega^{-1}\) is an RMS vorticity wavenumber.

It is **not** labeled an analyticity radius in this gate.

Under the fixed-energy concentration map

\[
u_\lambda(x)=\lambda^{3/2}v(\lambda x),
\]

we have

\[
G_\lambda=\lambda^2G,
\qquad
D_\lambda=\lambda^4D,
\]

hence

\[
\ell_{\omega,\lambda}
=
\lambda^{-1}\ell_\omega.
\]

This is the same absolute-length scaling as a physical coherence radius.

## Sampled comparison

The high-vorticity gate reports

\[
\rho_{\rm upper}^{\rm sample}
=
\frac1{L_{\max}^{\rm sample}}.
\]

Define the diagnostic ratio

\[
\mathcal R_{\rm sample}
=
\frac{\rho_{\rm upper}^{\rm sample}}
{\ell_\omega}.
\]

### Combined double/quarter-phase/high-frequency case

At \(N=4\),

\[
\ell_\omega:
0.3734\to0.3741,
\]

while

\[
\rho_{\rm upper}^{\rm sample}:
1.1054\to0.7713,
\]

giving

\[
\mathcal R_{\rm sample}:
2.96\to2.06.
\]

At \(N=7\),

\[
\ell_\omega:
0.3734\to0.3348,
\]

while

\[
\rho_{\rm upper}^{\rm sample}:
1.1054\to0.5437,
\]

giving

\[
\boxed{
\mathcal R_{\rm sample}:
2.96\to1.62
}
\]

through \(t=0.015\).

The same \(N=7\) trajectory also has

\[
\frac{T}{\nu D}:
0\to5.49,
\]

while the \(N=4\) trajectory reaches only about

\[
\frac{T}{\nu D}\approx1.61.
\]

Thus the case with the strongest nonlinear dominance is also the case in
which the sampled geometric coherence scale closes most rapidly toward the
vorticity-gradient scale.

## Critical interpretation rule

This ratio must **not** be read as a regularity margin.

The reason is one-sidedness:

\[
\rho_{\rm upper}^{\rm sample}
=
1/L_{\max}^{\rm sample}
\]

is only an **upper bound** on an admissible sampled coherence radius. The
actual continuum coherence radius, if defined through a theorem-level
condition, could be smaller.

Therefore

\[
\mathcal R_{\rm sample}>1
\]

does **not** prove that geometric coherence safely exceeds the active
gradient scale.

Likewise, \(\ell_\omega=\sqrt{G/D}\) is an exact RMS vorticity-gradient
length, not a proven analyticity radius.

This is the main correction to the manually operated visualization: labels
such as “Regular,” “Critical,” or a numerical “margin” are not justified by
the current mathematics.

## What the gate does establish

It establishes a reproducible and scaling-consistent comparison between two
absolute lengths:

- sampled high-vorticity geometric coherence;
- exact vorticity-gradient length.

Both scale like \(\lambda^{-1}\) under the concentration family that defeated
the earlier normalized candidates.

That makes this comparison structurally appropriate for the next stage of
the audit.

## Next proof target

A proof-level continuation would need one of the following:

1. a **lower bound** on a theorem-compatible high-vorticity coherence radius;
2. a rigorous viscous/analyticity lower scale;
3. or a differential inequality coupling those two quantities.

Without such a one-sided estimate, numerical crossings or ratios cannot be
promoted to regularity conclusions.

## Scope

This gate joins previously recorded finite-Galerkin quantities at
\(t=0,0.005,0.010,0.015\) for the tracked \(N=4\) and \(N=7\) cases.
No continuum convergence, analyticity radius, or regularity theorem is
claimed.

Reproduce with:

    python src/scale_competition_gate.py
