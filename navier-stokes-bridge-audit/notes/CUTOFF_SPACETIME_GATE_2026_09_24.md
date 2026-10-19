# Cutoff and time-step gate for total stretching

**Status:** exploratory numerical diagnostic, 24 September 2026. This note
extends the aligned two-scale trajectory in the v0.2 Master Record supplement.
It is subsequent work, not part of the frozen GitHub/Zenodo v0.2 release.

## Definition and protocol

For the unforced periodic Fourier-ball Galerkin system, set
\(G_N=\sum_k|k|^2|a_k|^2\), \(D_N=\sum_k|k|^4|a_k|^2\), and
\(T_N=-\mathrm{Re}\sum_k|k|^2\overline{a_k}\cdot P_k[(u_N\cdot\nabla)u_N]_k\).
Thus \(G_N'/2=T_N-\nu D_N\). The previously audited strain identity
identifies \(T_N=\langle\omega_N\cdot S_N\omega_N\rangle=Q_N+R_N\).
We compute this **total signed quantity directly in Fourier space**;
no shell remainder is dropped. The code does not reevaluate \(Q_N\) and
\(R_N\) individually for the new cutoffs.

Run `python src/cutoff_spacetime_gate.py` from the repository root. It uses
the unchanged initial field in `phase_cascade_trajectory.initial`, viscosity
\(\nu=0.1\), the interval \([0,0.02]\), cutoffs \(N=4,5,6,7\), and RK4
time steps \(0.0005\) and \(0.00025\). Each temporal grid is integrated
separately; composite Simpson quadrature samples every time step. Exact
mode-pair convolution has no FFT grid aliasing. All four Fourier balls
contain the same initial nonzero modes.

## Results

| N | Modes | \(\int_0^{.02}T_Ndt\) | \(T_N(.02)\) | \(G_N(.02)\) | Max fraction of \(G_N\) in \(|k|>0.75N\) |
|---:|---:|---:|---:|---:|---:|
| 4 | 257 | 7.324593959 | 544.026440 | 534.433072 | 0.263664 |
| 5 | 515 | 9.079213265 | 716.764733 | 537.820060 | 0.012770 |
| 6 | 925 | 9.128853620 | 724.199657 | 537.914255 | 0.004121 |
| 7 | 1419 | 9.150983418 | 728.562802 | 537.956166 | 0.000503 |

The \(N=4,5\) integrated transfer agrees with the archived v0.2
space-time strain commutator ledger at its displayed precision.
Successive changes in the integral are \(1.754619306\), \(0.049640356\),
and \(0.022129798\). \(T_N(t)>0\) at every sampled point for these
runs, so the recorded integral of \((T_N)_+\) equals the signed integral.
The max resolved-band enstrophy fraction is a **cutoff-dependent band
diagnostic**, not a common physical shell or a quantitative tail bound.

Across all four runs, refining the RK4 step changes \(\int T_Ndt\) by
at most \(1.77\times10^{-9}\); the largest final full-state \(\ell^2\)
difference is below \(10^{-9}\). Refined-run integrated energy and
enstrophy budget residuals are below \(7\times10^{-12}\) and
\(1.1\times10^{-10}\), respectively. These independently check temporal
and accounting accuracy at each fixed cutoff. The full data, including
\(\int D_Ndt\), positive net growth, and shared-mode endpoint differences,
are in `src/cutoff_spacetime_results.json`.

## Interpretation and next analytic gate

For this one smooth datum and short interval, the large \(N=4\)-to-\(N=5\)
gap becomes much smaller at the next two cutoffs. This is evidence of
*empirical stabilization on this interval*, not a proved convergence
rate, monotonicity, a universal cutoff bound, or global smoothness.
Indeed, the positive net-growth integral increases from 2.014180 at
\(N=4\) to 3.696688 at \(N=7\); the observed stabilization of a signed
quantity does not imply dissipation dominates pointwise.

The project's phase-parity and smooth-shell audits constrain the next
candidate: if it predicts signed transfer, it must retain orientation;
if it only bounds positive transfer, it may be parity-even. In either
case it must include the cross-frequency strain interactions or bound
their omission and must produce a time-integrable, cutoff-uniform
coefficient **from independently controlled norms**. Comparing a
candidate's predictions against this one trajectory may falsify it;
matching the table cannot prove the required inequality for arbitrary
smooth data. A natural next falsification study varies amplitudes,
phases, and initial high-frequency occupancy before attempting a theorem.
