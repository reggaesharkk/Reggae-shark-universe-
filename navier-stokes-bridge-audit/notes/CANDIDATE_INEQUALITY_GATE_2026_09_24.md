# Time-resolved candidate inequality gate

**Status:** analytical rejection of one energy-only candidate, accompanied
by finite Galerkin diagnostics. This is subsequent exploratory work after
the frozen v0.2 release. It does not resolve global regularity.

## Candidate and sufficient consequence

Test the trial inequality

\[
T_N(t)\leq\frac{\nu}{2}D_N(t)+C(E_0,\nu)G_N(t)^{3/2},
\qquad G_N=\langle|\omega_N|^2\rangle,
\quad D_N=\langle|\nabla\omega_N|^2\rangle.
\]

Here **one constant** must work for every smooth, real, divergence-free
mean-zero initial datum with the same energy \(E_0\), every cutoff \(N\),
and all times of existence. The full signed transfer is
\(T_N=\langle\omega_N\cdot S_N\omega_N\rangle=\sum_j(Q_{j,N}+R_{j,N})\).

This would be powerful if true. The exact energy identity
\(E_N'=-\nu G_N\) gives \(\int_0^{T_*}G_N\,dt\leq E_0/\nu\), hence
\(\int_0^{T_*}\sqrt{G_N}\,dt\leq\sqrt{T_* E_0/\nu}\). Pairing the
candidate with \(G_N'/2=T_N-\nu D_N\), dividing by \(G_N>0\), and
integrating would give

\[
G_N(t)\leq G_N(0)\exp\!\left(2C(E_0,\nu)
\sqrt{T_*E_0/\nu}\right),\qquad 0\leq t\leq T_*.
\]

The energy dependence of \(C\) is specified: merely fitting a
different constant to every datum or every cutoff supplies no such
energy-only majorant.

## Exact static scaling obstruction

The candidate is **false** even at \(t=0\). Let \(v\) be a smooth,
compactly supported divergence-free vector field in \(\mathbb R^3\)
with \(T(v)=\int\omega(v)\cdot S(v)\omega(v)\,dx>0\). Such a field
exists: start from the explicit smooth, mean-zero periodic finite triad
in this repository with positive spatially averaged transfer, write it
as the curl of a smooth periodic vector potential \(A\), and set
\(v_R=\nabla\times[\chi(x/R)A(x)]\), with a nonnegative smooth cutoff
\(\chi\) equal to one on a ball and supported in a larger ball. As
\(R\to\infty\), its cubic transfer is
\(R^3\langle\omega\cdot S\omega\rangle\int\chi^3+O(R^2)>0\)
for sufficiently large \(R\): each derivative falling on the cutoff
costs \(1/R\), and the nonzero periodic Fourier frequencies have
vanishing large-scale weighted average. Fix one such \(v=v_R\).

Embed the compact support inside one torus cell and define, for large
\(\lambda\), \(u_\lambda(x)=\lambda^{3/2}v(\lambda(x-x_0))\), extended
periodically by zero. These are individually smooth, divergence-free,
mean-zero data. Their energy is the same \(E_0>0\) for all \(\lambda\),
whereas (using the same volume normalization throughout)

\[
G(u_\lambda)=\lambda^2G(v),\quad
D(u_\lambda)=\lambda^4D(v),\quad
T(u_\lambda)=\lambda^{9/2}T(v).
\]

Consequently their necessary coefficient satisfies

\[
\frac{[T(u_\lambda)-\nu D(u_\lambda)/2]_+}
{G(u_\lambda)^{3/2}}
=\frac{T(v)}{G(v)^{3/2}}\lambda^{3/2}
-\frac{\nu D(v)}{2G(v)^{3/2}}\lambda
\longrightarrow\infty.
\]

At each sufficiently large finite \(\lambda\), the initial field is
smooth. Fourier projections of it converge in all relevant norms;
normalize each finite projection back to the fixed energy \(E_0\).
The needed coefficient remains arbitrarily large at some sufficiently
large **finite Galerkin cutoff**. The argument rules out the stated uniform
\(C(E_0,\nu)\). It does not rule out a coefficient depending on more
information about the fixed datum, nor all other routes to regularity.

## Time-resolved finite-cutoff screen

`src/candidate_inequality_gate.py` records \(E,G,D,T\), the upper-band
enstrophy fraction, and the necessary sampled coefficient
\(C_{\rm req}=[T-\nu D/2]_+/G^{3/2}\) at every RK4 step. It processes
the seven existing scenarios at \(N=4,5,6\) (21 runs) and three selected
scenarios at \(N=7\), with \(\Delta t=0.0005\) on \([0,0.02]\). A time
series and its Simpson integrals are stored for each run. The compact
`sample_columns` list names the seven values in each sample row;
positive transfer and net growth are recoverable as \(T_+\) and
\(T-\nu D\).

| Scenario | max sampled \(C_{\rm req}\), N=4 | N=5 | N=6 | N=7 |
| --- | ---: | ---: | ---: | ---: |
| Reference | 0.032679 | 0.045857 | 0.046421 | 0.046754 |
| Add 25% initial high-frequency enstrophy | 0.015623 | 0.039237 | 0.054119 | 0.059848 |
| Double, quarter-turn phase, add high frequencies | 0.019330 | 0.056707 | 0.080132 | 0.094592 |

These measured maxima occur at the final sampled time \(t=0.02\);
unsampled times could have larger values. A finite table cannot prove
the analytic obstruction or a uniform bound: the former follows from
the concentration construction above. The historical RK4 step-halving
checks for these same scenarios are in
`src/adversarial_cutoff_results.json` and
`src/adversarial_cutoff_N7_results.json`. The present trace uses the
coarser step and independently checks the energy/enstrophy budgets.

Run from the repository root:

```bash
python src/candidate_inequality_gate.py
python src/candidate_inequality_gate.py --cutoffs 7 \
  --scenarios reference high_frequency_25pct_G combined_double_quarter_high \
  --output src/candidate_inequality_N7_results.json
```

## Next proof gate

A surviving candidate must account for physical concentration and
high-frequency interactions. The standard derivative-dependent
majorants do so but yield time coefficients that the energy identity
does not currently control. Specify the new coefficient *before*
running more data, derive its scaling under localized concentration,
and only then screen its pointwise and time-integrated predictions on
these stored traces. No amount of fitting \(C_{\rm req}\) from the
unknown transfer constitutes an a priori estimate.
