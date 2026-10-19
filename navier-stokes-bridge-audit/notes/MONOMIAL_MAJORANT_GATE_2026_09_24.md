# A scaling and integrability gate for enstrophy-only majorants

**Scope:** unforced, periodic, three-dimensional incompressible flow.
This is a narrow obstruction for one family of candidate inequalities,
not a theorem about all methods of controlling vortex stretching. The
v0.2 GitHub tag and Zenodo record remain frozen.

## The proposed family

Suppose one seeks a pointwise Galerkin estimate of the form

\[
T_N(t)\leq\frac{\nu}{2}D_N(t)
 + C(E_0,\nu,T_*)G_N(t)^{1+p},\qquad p\geq0,
\]

with a **single constant for all smooth data of a given energy** and
all cutoffs. The coefficient in the resulting \(H^1\) Grönwall estimate
is \(a_N=C G_N^p\). The energy identity alone bounds
\(\int_0^{T_*}G_N\leq E_0/\nu\), hence bounds
\(\int_0^{T_*}G_N^p\) for \(0\leq p\leq1\) by Hölder (and \(T_*\)).

The concentration construction in
`notes/CANDIDATE_INEQUALITY_GATE_2026_09_24.md` fixes the initial
energy while producing smooth mean-zero solenoidal fields with

\[
T_\lambda=\lambda^{9/2}T(v),\qquad
G_\lambda=\lambda^2G_*,\qquad
D_\lambda=\lambda^4D_*,\qquad T(v)>0.
\]

The viscous allowance grows only like \(\lambda^4\); the proposed
remainder grows like \(\lambda^{2(1+p)}\). Therefore **every
\(0\leq p<5/4\) is refuted at the initial time** for a constant
depending only on \(E_0,\nu,T_*\). In particular, all exponents
\(0\leq p\leq1\) whose time integral follows from energy are excluded.
At \(p\geq5/4\) this particular scaling does not refute the algebraic
estimate, but energy alone supplies no \(\int G_N^p\) bound. The two
requirements leave no exponent within this enstrophy-only family
that both survives the scaling test and has an energy-controlled
Grönwall coefficient. This says nothing about a coefficient with
additional independently controlled information or proven dynamical
cancellation.

## A dissipation-aware comparison

The standard periodic Sobolev/Gagliardo–Nirenberg estimate gives

\[
|T_N|\leq C\|\nabla u_N\|_{L^3}^3
\leq C G_N^{3/4}D_N^{3/4}.
\]

This is consistent with concentration:
\(G_\lambda^{3/4}D_\lambda^{3/4}\sim\lambda^{9/2}\).
Young's inequality then gives
\(T_N\leq\nu D_N/2+C_\nu G_N^3\). Its Grönwall coefficient is
\(C_\nu G_N^2\); the energy identity only controls \(\int G_N\), not
\(\int G_N^2\). A numerically small ratio to the instantaneous
majorant cannot supply the missing time integral.

## Stored-trace screen

`src/monomial_majorant_gate.py` reads the 24 time-resolved records in
`src/candidate_inequality_results.json` and
`src/candidate_inequality_N7_results.json`. It writes necessary sampled
constants for four exponents and the dimensionless ratio
\(|T|/(G^{3/4}D^{3/4})\) to
`src/monomial_majorant_results.json`. For the combined field, the
largest sampled \(|T|/(G^{3/4}D^{3/4})\) is 0.00596 at \(N=4\) and
0.01817 at \(N=7\). Those values are **descriptive ratios**, not
estimates of a universal constant or of continuum behavior. The
analytic exclusion of \(p<5/4\) does not depend on them.

Run from the repository root:

```bash
python src/monomial_majorant_gate.py
```

## Next route

Any proposed improvement must be stated with its independent input
norms, its signed/one-sided meaning, and the source of its
time-integrated coefficient. Check amplitude, frequency dilation,
and fixed-energy spatial concentration before using these traces as
falsification tests. Merely raising the exponent of \(G\) handles
concentration by losing energy-only time integrability.
