# WP16 post-hoc sparse turnover reduction (28 September 2026)

This is a **post-hoc numerical witness**, constructed after seeing the N17
outcome. It is a new N11 Galerkin initial value problem derived from the N17
inherited state, not an untouched N17 holdout, a minimal-support theorem, an
interval certificate, or a continuum Navier–Stokes result.

## Construction and reproducibility

Project the N17 inherited initial Fourier field to the ball `|k|<=11`, rank
its positive conjugate representatives by the Euclidean norm of each complex
vector coefficient (canonical mode index breaks ties), retain the first 112,
and force the anchor `P=(3,2,2)`, `Q=(3,-2,1)`, `K=(6,0,3)` to remain. All three
anchors were already in the first 112, so the resulting field has exactly 112
nonzero conjugate pairs. Zero the other modes. Evolve that field with the
unforced, viscosity `nu=.1`, N11 Fourier-Galerkin ODE and the existing exactly
dealiased FFT convolution. The N11 ODE still permits all frequencies inside
its ball to become active along the trajectory; 112 counts only the nonzero
*initial* pairs. This is not a closed 112-pair dynamical subsystem.

The retained coefficient table is
[`wp16_036_sparse_turnover_112_pairs.json`](../results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json).
It is sufficient to replay the experiment without the large N17 input files.
It records the inherited input hashes. The executable
[`wp16_036_sparse_turnover_witness.py`](../src/wp16_036_sparse_turnover_witness.py)
also reconstructs it from the frozen N16 and completed N17 continuations if
those are available. The same original N11-derived K36 ordered orbit keys
define `I`, `O` and `F=I-9O`; no K36 retuning occurs.

| Input or output | SHA-256 |
| --- | --- |
| N16 continuation | `53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca` |
| N17 continuation | `755a36f966b64c8c44cd468c6f2e8212a7ed64eebeaf8aa795ee2c3197c4c3ec` |
| K36 keys | `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47` |
| Exported 112-pair witness | `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624` |
| Numerical result | `8c6c89090faaaadae1d4d78f8e95ae703bb2d360c9096835e162a0af70fbaa0b` |

To replay directly from the exported coefficients at the repository root:

```bash
PYTHONPATH=src python src/wp16_036_sparse_turnover_witness.py \
  --keys results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json \
  --witness results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json \
  --result results/wp16_n17_holdout/wp16_036_sparse_turnover_112_result.json
```

## Observation and checks

| Time | F with RK4 dt=.0001 |
| ---: | ---: |
| 0 | +645.803774147178 |
| .001 | +730.4189743994361 |
| .002 | +359.0474400160358 |
| .003 | -48.39048296359124 |

The endpoint values with half and quarter steps are respectively
`-48.39053556544013` and `-48.390538870127216`. Coarse-to-half endpoint
discrepancy is `5.260184889266384e-5`; half-to-quarter is
`3.3046870839825715e-6`. These are convergence diagnostics, **not rigorous
rounding/error enclosures**. The minimum tested initial support under this
particular magnitude-prefix screen has not been determined: 96 pairs did not
cross by `.003`, while 112 did, and neither result establishes global
minimality over arbitrary supports or phases.

The direct ordered-pair convolution at tracked output K agrees with the FFT
nonlinearity within `1.94e-12` across the runs. Maximum observed real-field
and divergence residuals are below `4e-15` and `3e-14`; nonlinear energy
pairing residual is below `7e-11`. Discrete energy decreases at every sampled
step. The initial field has zero mean, real conjugate symmetry, and transverse
coefficients to floating precision.

## Certificate gate before any headline theorem

The coefficient decimals can be interpreted as rational data, but the
printed field is only approximately transverse. A rigorous certificate must
first project or parameterize those rational coefficients **exactly** in each
transverse plane and account for that perturbation. It must then enclose the
N11 ODE trajectory, the complex normalizer `z` away from zero, and every
group's signed contribution through the absolute-value kinks at both endpoint
times. The certified endpoint intervals must satisfy `F(0)>0` and
`F(.003)<0`. Continuity would then give a finite-Galerkin crossing. None of
these interval enclosures has yet been constructed. A continuum statement
would additionally need an independent, cutoff-uniform PDE-tail estimate.

The N17 frozen orbit/normalizer mechanism failure remains unchanged. This
post-hoc reduction isolates a different question: whether a smaller initial
support can exhibit the same global K36 margin turnover. It does not rescue
the failed prospective orbit prediction.
