> Universe mirror of [the canonical conditional tail analysis](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/755919384c5829e8e26db753a65146a85aa8a36c/notes/WP16_036_PHASE_UNIFORM_TAIL_AND_SIGNED_GAP_2026_09_26.md). [Reproduction code and raw post-hoc data](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/755919384c5829e8e26db753a65146a85aa8a36c/results/wp16_n13_holdout/) remain in the specialist repository.

# WP16 K36: phase-uniform source envelope and remaining signed gap

**Post-hoc analytic audit · Prince Upadhyay, Independent Research · 26 September 2026.** This note does not revise the frozen K36 coalition or N12/N13 holdout. It states an exact conditional inequality and tests whether it explains those finite observations.

## Exact source-tail inequality

Use the evaluator's tracked `k=K=(6,0,3)`, anchor `P=(3,2,2)`, `Q=(3,-2,1)`, and Fourier state `a`. Let `B=P_k(i(Q·a_P)a_Q)`, `w=|k|^4`, `z=-w⟨a_k,B⟩` with the first slot conjugated, and assume `z≠0`. For an ordered convolution pair `l+r=k`, the code sets `dot a_k^(l,r)=-P_k(i(r·a_l)a_r)` and its phase-velocity source is `I_(l,r)=Im[-w⟨dot a_k^(l,r),B⟩/z]`. Projection and Cauchy–Schwarz give

`|I_(l,r)| ≤ D |r| |a_l| |a_r|`, where `D=w|B|/|z|=|B|/|⟨a_k,B⟩|`.

For `s≥1`, `M_s=Σ_(j≠0)|j|^(2s)|a_j|²`, and `R>|k|`, the grouped absolute source mass from ordered orbit-pair groups with `max(|l|,|r|)≥R` obeys

`A_≥R ≤ D M_s (R-|k|)^(1-2s)`.

Indeed `l+r=k` makes both frequencies at least `R-|k|` on this set. After factoring `|l|^s|a_l| · |r|^s|a_r|`, Cauchy–Schwarz over the convolution pairs gives `M_s`; grouping can only decrease the sum of absolute values. The constant is independent of the Galerkin cutoff **if** `D` and `M_s` are independently bounded across cutoffs. No such global-in-time, large-data bound is established here.

For the phase rotations in this experiment, every mode changes only by a unit complex scalar (with conjugate reality). Thus `M_s`, `|B|`, `|z|`, and `D` are **exactly invariant under all phase choices at a fixed cutoff**. The inequality holds on the entire fixed-magnitude phase torus, not merely at the three measured states.

## Numerical sharpness and the low outside groups

At N12, `(D,M_2)=(1.3041502881,585396.0013)`; at N13, `(1.3049970724,588209.2428)`. The broad `R=12` bound is about **5,152** at N12 and **5,180** at N13, so it is mathematically valid but numerically vacuous compared with the observed high-shell contributions.

The exact magnitude `|-w⟨dot a_k^(l,r),B⟩/z|` of each ordered source is also phase-invariant. Summing these per-source magnitudes gives a sharper phase-uniform envelope for grouped outside-K36 mass at each finite cutoff:

| Outside shell by `max(|l|,|r|)` | N12 envelope | N12 observed full-final | N13 envelope | N13 observed full-final |
|---|---:|---:|---:|---:|
| `<8` | 63.84434 | 33.31371 | 63.90250 | 37.56236 |
| `8–10` | 37.67162 | 19.77026 | 37.95692 | 20.25758 |
| `10–12` | 15.06770 | 11.59955 | 12.69642 | 8.81220 |
| `12–13` | 0.00048 | 0.00038 | 1.79858 | 1.33411 |
| **All outside** | **116.58414** | **64.68390** | **116.35442** | **67.96625** |

The low shells `<10` contribute about 85% of the observed N13 full-final outside mass. A high-frequency tail estimate alone therefore cannot establish the 90% K36 gate. At N13, even the sharper outside envelope `116.35` would require a phase-uniform K36 absolute-mass lower bound of at least `9×116.35≈1047.19` to certify 90%; the three observed K36 masses are about `934.42`, `994.73`, and `970.29`. The envelope is conservative, and no such lower bound has been proved.

## Fixed magnitudes do not ensure the full signed gate

A deterministic, exploratory sample of 64 independent uniform phase draws at N13 (seed `20260926`) preserved the evolved magnitudes and polarizations. All 64 had K36 absolute-mass fraction in `[0.90957,0.95885]`, but only **55/64** passed all three frozen criteria. The other nine failed the signed-share or sign condition. Draw 20 had full signed channel `0.81050` and signed share `10.27984`; draw 37 had signed share `−1.15498`, a sign mismatch. These are post-hoc phase probes, not a probabilistic guarantee or prospective holdout.

The remaining analytic task is consequently more specific: control the **low outside groups and signed cancellation** on the dynamically or algorithmically selected phase states while keeping the tracked channel away from zero. Fixed magnitudes yield an exact finite-cutoff upper envelope and a conditional high-tail bound, but neither alone proves the frozen signed gate or any N-uniform closure. The optimized phase states are not shown to be a Navier–Stokes trajectory after phase rotation.

**Reproduction:** `src/wp16_036_phase_uniform_tail_certificate.py`, `src/wp16_036_phase_uniform_source_envelope.py`, `src/wp16_036_outside_K36_shells.py`, and `src/wp16_036_fixed_magnitude_phase_probe.py`. The corresponding raw JSON files in `results/wp16_n13_holdout/` retain full precision and post-hoc labels.
