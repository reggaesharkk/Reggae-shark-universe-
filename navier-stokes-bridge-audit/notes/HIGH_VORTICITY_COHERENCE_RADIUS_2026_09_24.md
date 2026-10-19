# High-vorticity sampled coherence-radius gate (post-v0.2)

## Motivation

The direction-scaling obstruction shows that normalizing
\(L_{\rm dir}\) by \(\sqrt G\) removes exactly the absolute length scale
that concentration changes.

The classical Constantin-Fefferman mechanism instead keeps an absolute
coherence scale in regions where vorticity is large. This gate therefore
returns to an absolute sampled slope and an associated physical length.

It remains a diagnostic only.

## Diagnostic high-vorticity set

At each snapshot define

\[
\Omega_{\rm diag}=2\sqrt G,
\qquad
G=\langle|\omega|^2\rangle.
\]

A sampled pair \((x,x+h)\) is retained only when

\[
|\omega(x)|\ge\Omega_{\rm diag},
\qquad
|\omega(x+h)|\ge\Omega_{\rm diag}.
\]

The multiplier \(2\) is a transparent diagnostic choice. It is **not** the
fixed threshold appearing in the Constantin-Fefferman theorem.

For each retained pair define

\[
L(x,h)
=
\frac{|\sin\theta(x,x+h)|}{|h|}.
\]

The gate reports

\[
L_{\max}^{\rm sample}
=
\max_{\rm retained\ pairs}L(x,h).
\]

If a Lipschitz-style condition

\[
|\sin\theta(x,x+h)|
\le
\frac{|h|}{\rho}
\]

were to hold on all sampled pairs, then necessarily

\[
\rho
\le
\frac{1}{L_{\max}^{\rm sample}}.
\]

Accordingly the file reports

\[
\rho_{\rm upper}^{\rm sample}
=
1/L_{\max}^{\rm sample}.
\]

This is an upper bound on an admissible coherence radius for the sampled
pairs only; it is not a continuum theorem quantity.

## Main sampled result

At the smallest grid separation \(2\pi/32\):

### Combined double/quarter-phase/high-frequency

For \(N=4\),

\[
L_{\max}:
0.905\to1.296
\]

from \(t=0\) to \(t=0.015\), giving

\[
\rho_{\rm upper}^{\rm sample}:
1.105\to0.771.
\]

For \(N=7\),

\[
L_{\max}:
0.905\to1.839,
\]

giving

\[
\rho_{\rm upper}^{\rm sample}:
1.105\to0.544.
\]

The number of retained nearest-neighbor high-vorticity pairs also grows:

- \(N=4\): 406 to 911;
- \(N=7\): 406 to 1104.

The determinant-based maximum follows the same separation:

- combined \(N=4\): about \(0.808\to1.170\);
- combined \(N=7\): about \(0.808\to1.646\).

Thus the perturbed \(N=7\) trajectory develops both a larger high-vorticity
pair population and a smaller sampled absolute coherence length than its
\(N=4\) counterpart.

### Reference field

The \(N=4\) reference trajectory has no neighboring pairs satisfying the
chosen \(2\sqrt G\) threshold over the sampled interval.

At \(N=7\), nearest-neighbor qualifying pairs appear after \(t=0\), but the
sampled maximum slope remains near \(0.20\), far below the perturbed cases.

This threshold sensitivity is itself a reminder that the gate is a finite
diagnostic, not a theorem.

## Relationship to the triadic results

The same combined \(N=7\) trajectory was the case in which:

- signed triadic coherence developed most rapidly;
- total stretching became much larger than at \(N=4\);
- the global local-direction proxy showed the largest growth.

The high-vorticity restriction sharpens that contrast substantially.

This supports the working hypothesis that the relevant cancellation failure
is localized in intense-vorticity geometry rather than captured by a single
global norm or dimensionless coherence score.

It does not establish causation.

## Next proof target

The next non-numerical task is to connect an **absolute high-vorticity
coherence radius** to a viscous or analyticity scale in an inequality that
is stable under the Navier-Stokes evolution.

At that point the question becomes genuinely scale-competitive:

> can viscosity keep the analyticity/diffusion scale from falling below the
> geometric coherence scale required for stretching depletion?

That is closer to known geometric regularity mechanisms than the rejected
energy-only closures.

## Scope

This gate uses a \(32^3\) grid, three axis-aligned offsets, four finite
Galerkin trajectories, and data through \(t=0.015\). The threshold is
snapshot-dependent.

No continuum radius, blow-up criterion, or regularity theorem follows.

Reproduce with:

    python src/high_vorticity_coherence_radius_gate.py
