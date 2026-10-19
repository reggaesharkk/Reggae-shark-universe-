# Stress test: amplitude, phase, and high-frequency occupancy

**Status:** exploratory finite Galerkin calculation following the v0.2
archive and the first cutoff space-time gate. No continuum bound or
arbitrary-data regularity theorem is claimed.

## Protocol

`src/adversarial_cutoff_gate.py` evolves the same real, divergence-free
initial Fourier field at each cutoff \(N\) on \([0,0.02]\), viscosity
\(\nu=0.1\), using exact non-aliased convolution, RK4 step \(0.0005\),
and composite Simpson quadrature of the **full signed transfer**
\(T_N=\langle\omega_N\cdot S_N\omega_N\rangle=Q_N+R_N\). It also records
\(\int(T_N)_+\) separately. Selected scenarios independently rerun at
step \(0.00025\). The reference field is the same as in the v0.2
supplement. The phase rotations below apply to the \(R\) coefficient
of each initial triad; they are not a global velocity sign reversal.

The high-frequency perturbation puts extra coefficients at
\(\pm(3,2,0)\) and \(\pm(2,-3,0)\), which are present for **every**
\(N\geq4\). Transverse conjugate polarizations preserve realness and
incompressibility. Their added initial enstrophy is 25% of the new
total. The initial condition for each scenario is identical across
its cutoffs; higher modes appear only through evolution. 'Double'
scales all coefficients of the original two-scale field by two before
the optional 25% high-frequency supplement is added.

## Integrated transfer

Entries are \(\int_0^{0.02}T_N(t)\,dt\). A dash means that cutoff was
not run for the scenario.

| Scenario | N=4 | N=5 | N=6 | N=7 |
| --- | ---: | ---: | ---: | ---: |
| Reference | 7.324594 | 9.079213 | 9.128854 | 9.150983¹ |
| Half amplitude | 0.683252 | 0.792234 | 0.794014 | — |
| Double amplitude | 86.253493 | 114.386996 | 116.278542 | 117.637120 |
| Quarter-turn phase | 3.200665 | 5.232464 | 5.269014 | — |
| Opposite triad phase | −0.915959 | 0.871698 | 0.910088 | — |
| Add 25% initial high-frequency enstrophy | 7.325084 | 12.598359 | 15.545937 | 16.555523 |
| Double, quarter-turn, add high frequencies | 44.752091 | 133.101513 | 170.887840 | 196.714450 |

¹ The reference N=7 value comes from the earlier
`src/cutoff_spacetime_results.json`, with a refined time step. The
other entries are in `src/adversarial_cutoff_results.json` (N=4–6)
and `src/adversarial_cutoff_N7_results.json` (selected N=7).

The largest successive increment for the combined case is 88.349422
(N=4 to 5), followed by 37.786326 and 25.826610; the last increment
is **not negligible** on this range. For the high-frequency-only case
the increments are 5.273275, 2.947578, and 1.009586. The reference
field's small high-cutoff increments therefore do not persist with
similar magnitude across these deliberately perturbed initial data.
These finite samples cannot establish that any increment stays positive,
vanishes, or diverges as \(N\to\infty\).

Phase also matters to the *signed* outcome: the opposite-phase case
starts at \(T(0)=-179.783646\) for every cutoff. Its N=4 signed
integral is negative, but \(\int(T_4)_+=0.291837\); at N=5 the
signed and positive-part integrals are 0.871698 and 1.595279.
The phase-blind enstrophy and initial power spectrum cannot encode
these changes in the initial signed transfer.

## Numerical and analytic limits

For the combined N=7 run, halving the time step changes the integrated
transfer by \(5.19\times10^{-6}\), much smaller than its 25.826610
cutoff increment. The N=4–6 scenarios selected for refinement show
integral changes up to \(4.22\times10^{-6}\). The largest coarse
integrated enstrophy budget residual for the combined N=4–7 runs is
less than \(8.3\times10^{-6}\). The code checks the energy budget,
reality, and divergence as well. These are numerical checks, not
rigorous error bounds.

The script records the diagnostic integral
\(\int_0^{.02}[(T_N-\nu D_N/2)_+/G_N]dt\). **This is not an a priori
regularity coefficient:** it is defined using the transfer it would
need to bound. The project’s analytic gate remains to derive a
cutoff-uniform time-integrable majorant from independently controlled
quantities. The next falsification step should try initial data with
varied high-frequency shapes and phase patterns, then test a *specified*
candidate inequality on the resulting trajectories; raw agreement of
signed transfer across a few cutoffs is not enough.

Reproduce with:

```bash
python src/adversarial_cutoff_gate.py
python src/adversarial_cutoff_gate.py --cutoffs 7 \
  --scenarios double_amplitude high_frequency_25pct_G combined_double_quarter_high \
  --refine combined_double_quarter_high \
  --output src/adversarial_cutoff_N7_results.json
```
