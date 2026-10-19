# WP16 Expanded Phase-Torus Search — Fixed-State Grid Refinement

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** executed retrospective refinement of the completed expanded WP16 phase-only search.  
**Scope:** one fixed optimized phase state, no re-optimization during refinement.  
**Not claimed:** no global maximum, no monotone cutoff theorem, no cutoff-independent bound, no regularity result.

## 1. Source run

The completed Colab search used

[
Nin{5,6,7},qquad
tin{0.0025,0.0035,0.005},
]

two deterministic seeds, 96 global phase draws, six block-coordinate rounds, 160 trials per round, block size 24, and a (24^3) physical grid for the positive-stretching denominator.

The raw search artifact is:

```
wp16_expanded_phase_search_results.json
sha256:8f8dfa510f7156aa5b029f42d88fe302b490e4007afd9335f785a2431d1da972
size: 4,191,774 bytes
```

The search produced the phase-only candidate

[
oxed{
C_infty^{m stretch}=3.745590706681554
}
]

at

[
N=7,qquad t=0.005,qquad 	ext{seed}=20260925,
]

with 709 active conjugate phase pairs.

The corresponding fixed Fourier quantities are

[
X_2=535519.8723055569,
]

[
G=51405.61153956244,
]

[
N_2^{>2}=16772068.34294506,
]

[
chi_{2,m high}=0.214534228750574.
]

## 2. Why refine

The optimization used a (24^3) physical grid for

[
leftlangle(omegacdot Somega)_+ightangle.
]

A coarse positive-part grid can bias the quotient, so the best phase vector was frozen and reevaluated without any further optimization.

Only the physical-grid evaluation changes. The Fourier quantities and the 709 optimized phases remain fixed.

## 3. Fixed-state refinement

| grid | positive stretching | (C_infty^{m stretch}) |
| ---: | ---: | ---: |
| (24^3) | 429834.47292654467 | 3.745590706681554 |
| (32^3) | 430106.34208012186 | 3.743223128072629 |
| (48^3) | 429976.3363793314 | 3.744354912091437 |
| (64^3) | 429998.5730269491 | 3.7441612791215664 |
| (96^3) | 429992.61252859357 | 3.7442131801693903 |
| (128^3) | 430002.5446785433 | **3.744126696758515** |

The signed (H^1) stretching is grid-stable at

[
leftlangleomegacdot Somegaightangle
=
-314901.247218617
]

to the shown precision.

The Fourier/grid enstrophy check remained at roundoff scale throughout refinement.

## 4. Interpretation

The expanded WP16 candidate survives physical-grid refinement:

[
rac{3.7441266968}{3.7455907067}approx0.99961.
]

Thus the (24^3) search value overestimated the refined value by only about (0.039%).

This makes

[
oxed{
3.7441266968
}
]

the refined benchmark for this **WP16 evolved-spectrum phase-only family**.

It is not the repository-wide benchmark. WP17 later expanded the admissible family to relative amplitudes and phases on a sparse multiscale ladder and obtained the larger refined finite value

[
C_infty^{m stretch}approx5.1129326.
]

Accordingly:

- WP16 expanded phase-only benchmark: (approx3.74413);
- WP17 sparse amplitude+phase benchmark: (approx5.11293).

They answer different finite-family optimization questions.

## 5. Finite trend only

Within the executed WP16 expanded search, the best (24^3) candidates increased with cutoff:

[
N=5:;1.668866,
qquad
N=6:;2.826826,
qquad
N=7:;3.745591.
]

The best (N=7) candidate also increased over the tested anchor times:

[
2.375461
	o
3.259517
	o
3.745591.
]

These are descriptive finite-search trends only. Three cutoffs and three short anchor times do not establish asymptotic growth.

## 6. Scope barrier

This refinement establishes only that one optimized WP16 phase-only state is not a coarse-grid artifact.

It does not prove:

- that the reported phase vector is globally optimal;
- that the phase-only quotient diverges with cutoff;
- that a cutoff-independent pointwise constant exists or fails;
- that the WP15 time-integral requirement closes;
- or any continuum Navier–Stokes regularity statement.
