# Local strain majorant: phase sensitivity and the missing time estimate

**Status:** an exact one-sided algebraic inequality, followed by finite
Galerkin diagnostics. These results are exploratory and postdate the
frozen v0.2 release.

## Frame-invariant candidate

Let \(S=(\nabla u+\nabla u^T)/2\), \(\omega=\nabla\times u\), and
\(\lambda_{\max}(S)\) be the largest eigenvalue at each point. Define

\[
M(u)=\left\langle\lambda_{\max}(S)_+|\omega|^2\right\rangle,
\qquad b(u)=M(u)/G(u),\quad G=\langle|\omega|^2\rangle.
\]

The Rayleigh quotient gives the **exact pointwise** inequality
\(\omega\cdot S\omega\leq\lambda_{\max}(S)_+|\omega|^2\), so
\(T(u)=\langle\omega\cdot S\omega\rangle\leq M(u)=b(u)G(u)\).
This uses the entire local strain and vorticity geometry and allows
different signs of transfer. It does not create new a priori control:
\(b(u)\) depends on the unknown solution, and no independently bounded
\(\sup_N\int_0^{T_*}b(u_N(t))dt\) is proved. The inequality also leaves
the viscous term unused; an added \(\nu D/2\) does not resolve the
integrability of \(b\).

## Exact triad phase gate

Apply this scanner to the zero-helicity six-mode family in
`notes/HELICITY_PHASE_GATE_2026_09_24.md` with \(A=1\). At each phase,
\(E=7\), \(G=28\), \(D=64\), and every signed modal helicity is zero:

| \(\theta\) | Exact \(T\) | Local positive \(\langle(\omega\cdot S\omega)_+\rangle\) | \(M\) on \(32^3\) grid |
|---:|---:|---:|---:|
| 0 | 0 | 3.39695 | 81.83733 |
| \(\pi/2\) | +4 | 5.37250 | 76.72931 |
| \(\pi\) | 0 | 3.39695 | 81.83733 |
| \(3\pi/2\) | −4 | 1.37250 | 86.51391 |

The majorant notices the phase through the spatial strain field but
remains **positive and loose when signed transfer is negative**. At
\(\theta=\pi/2\), \(M\) changes by about \(-0.00133\) between
\(32^3\) and \(48^3\) quadrature; unlike \(T\), an eigenvalue
functional is not a cubic trigonometric polynomial with exact
low-grid trapezoidal averaging.

## Short evolved-field screen

Recompute the Galerkin states for the reference and the doubled,
quarter-turn, high-frequency scenarios at \(N=4,5,6,7\), viscosity
\(0.1\), and \(t=0,0.005,0.01,0.015,0.02\). The previous scalar
time-trace JSON does not contain pointwise fields, so the scanner
reconstructs them from the original deterministic initialization and
solver. Composite Simpson integration of the **five sampled values**
gives:

| Scenario | N=4 | N=5 | N=6 | N=7 |
|---|---:|---:|---:|---:|
| Reference, \(\int_0^{.02} b\,dt\) | 0.275359 | 0.275975 | 0.276169 | 0.276160 |
| Combined perturbation, \(\int_0^{.02} b\,dt\) | 0.566993 | 0.569930 | 0.572597 | 0.574287 |

Using only every other sample changes the Simpson estimate by at most
about 0.00060 across the eight runs; this is an empirical time-sampling
check, not an integration error bound. These finite-run quadrature
estimates do not show a cutoff-uniform bound over every \(N\), every
datum, or longer times.
The largest \(32^3\)-to-\(48^3\) endpoint difference in \(M\) among
these eight runs is about 1.06, compared with endpoint \(M\) from
roughly 7,000 to 96,000; it measures only spatial quadrature for the
given finite Fourier fields. The code checks each spatial \(T\)
against independent Fourier transfer and asserts
\(M\geq\langle(\omega\cdot S\omega)_+\rangle\geq T_+\).

## What comes next

Spatial concentration at fixed energy scales
\(M\sim\lambda^{9/2}\) and \(G\sim\lambda^2\), hence
\(b=M/G\sim\lambda^{5/2}\) for a concentrated nontrivial profile.
This rules out a fixed-energy *pointwise* bound on \(b\); it does not
by itself decide the integral along an actual trajectory. A useful
regularity route must prove a time-integrated control of the full
strain-vorticity geometry from independent information, or exploit
a cancellation that makes the signed \(T\) substantially smaller than
this geometric envelope. Fitting the observed \(b\) after solving the
Galerkin ODE is not such a proof.

Reproduce: `python src/local_strain_majorant_gate.py` from the
repository root. It writes `src/local_strain_majorant_results.json`.
