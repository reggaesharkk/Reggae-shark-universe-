# WP16 local phase-network certificate (post-hoc)

Prince Upadhyay, Independent Research — 26 September 2026

## Exact conditional statement

Fix a finite Galerkin state, all Fourier magnitudes and complex vector polarizations, and the N11-frozen K36 ordered source-orbit set. Rotate each coefficient by a phase `exp(i δ_j)`, respecting the real-field relation `δ_-j = -δ_j`. Let `k=(6,0,3)` and let `l+r=k` denote each ordered nonlinear source. Assume the anchor `z` is nonzero (its magnitude stays fixed under these rotations).

In the output-mode channel, the complex contribution of each ordered source to `dot z/z` changes by exactly `exp(i(δ_k-δ_l-δ_r))` (up to conjugation convention, which does not affect the bounds). The factors from the two anchor modes in `B` cancel between numerator and denominator. Define the maximum circular triad defect

`ρ = max_{l+r=k} |wrap(δ_k-δ_l-δ_r)|`.

The source envelopes `E_I` and `E_O` are sums of the magnitudes of the **ordered** complex terms inside and outside K36. Thus the change of the signed sums and the change of the grouped absolute masses, separately, are bounded by `ρ E_I` and `ρ E_O`: use `|exp(iθ)-1| ≤ |θ|`, the triangle inequality within each orbit group, and `||u|-|v|| ≤ |u-v|`. This is conservative but exact. If every individual phase has circular displacement at most `ε`, then `ρ≤3ε`.

For original signed total `S>0`, outside signed sum `O`, inside/outside absolute group masses `A_I,A_O`, the frozen gate remains true whenever

`ρ < min{ (0.2 S-|O|)/(E_O+0.2(E_I+E_O)), (A_I/9-A_O)/(E_O+E_I/9) }`.

The first term enforces `|O_new| < 0.2 S_new`, hence positive same sign and signed share in `(0.8,1.2)`. The second enforces `A_I,new > 9 A_O,new`, hence absolute fraction `>0.9`. These are sufficient conditions; crossing the certified radius does not imply failure. Strict inequalities avoid boundary ambiguity.

## Evaluated using the archived envelopes and holdouts

| N | State | Signed defect radius (rad) | Mass defect radius (rad) | Joint phase radius `ε` (rad) |
|---|---|---:|---:|---:|
| 12 | inherited | 0.197032 | 0.150758 | 0.050253 |
| 12 | target_only | 0.197028 | 0.150766 | 0.050255 |
| 12 | full_final | 0.154208 | 0.122337 | **0.040779** |
| 13 | inherited | 0.156477 | 0.124229 | 0.041410 |
| 13 | target_only | 0.171280 | 0.145817 | 0.048606 |
| 13 | full_final | 0.173755 | 0.124850 | 0.041617 |

The common sufficient radius is `ρ<0.12233655561258345` radians in all output triad defects, or `ε<0.04077885187086115` radians for every coefficient. It is a local certificate around **each of the six evaluated states**, at that state's fixed magnitudes and polarizations. The N12 envelopes are `(E_I,E_O)=(1822.58672605,116.58414255)`; N13 `(1825.02788955,116.35441821)`. The certificate can be recomputed without a Galerkin allocation from the archived JSON using `src/wp16_036_phase_neighborhood_certificate.py`.

## Translation symmetry and what information matters

For a spatial translation `δ_j=j·x`, every output triad obeys `δ_k-δ_l-δ_r=0`. Therefore all these contributions, and the gate, are exactly invariant even if individual mode phases move by more than the stated radius. This is a concrete network/cocycle interpretation: the measured information resides in translation-invariant triad phase differences, not in raw absolute Fourier phases. It does not attribute intelligence to a fluid or imply a biological or quantum mechanism.

The earlier N9–N11 phase-dynamics audit found local **de-alignment** of the optimized motif under the finite Galerkin vector field. The present certificate is static: it gives no bound on how long an actual trajectory stays in the neighborhood. The 64 exploratory random-phase N13 draws preserve magnitudes; nine fail the signed gate while all pass the mass gate. They are not required to be near this local neighborhood. In particular, draw 20 has total signed channel `0.8105` and signed share `10.2798`: a clear near-cancellation sensitivity. The local certificate and this global phase counterexample are compatible.

## Next analytic gate

On an **actual** N12/N13 Galerkin trajectory, compute the phase-defect derivative `dot δ_k-dot δ_l-dot δ_r` for the source network, after choosing a translation gauge, together with time-dependent `S,A_I,A_O,E_I,E_O`. Test whether the trajectory remains inside its moving certified region for a nonzero interval, or exits immediately. A continuum claim would additionally need cutoff-uniform envelope and noncancellation bounds and an actual PDE trajectory argument. Neither is established here. The counterexample to any unconditional all-state 90% K36 theorem remains in force.

## Context from primary research

Waleffe's original helical-triad study analyzes the interaction geometry of homogeneous turbulence ([NASA record](https://ntrs.nasa.gov/citations/19920038608)); its decomposition suggests a possible *future* polarization-resolved check, but no helical conclusion is used above. Kang and Protas examine phase alignment in Burgers and three-dimensional Navier–Stokes flows ([original preprint](https://arxiv.org/abs/2105.09425)); the present certificate is a different, state-specific deterministic bound on this project's output channel. Chemistry, biology, and quantum analogies presently add no equation-level prediction to the gate.

Inputs: the canonical N12/N13 holdout JSON and `phase_uniform_source_envelope_N12_N13.json` from the frozen branch. This analysis is post-hoc and changes neither the frozen K36 definition nor the prospective holdout results.
