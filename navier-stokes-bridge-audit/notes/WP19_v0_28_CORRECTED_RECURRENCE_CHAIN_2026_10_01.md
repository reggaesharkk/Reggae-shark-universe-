# WP19 v0.28 corrected M14 recurrence chain

**Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.**

**Status: limited scalar recurrence PASS.** This result replaces the three old strain-only recurrence radii for continuation. It does not replace or alter their archived segment records, and it does not complete the M14 adjoint or the signed-observable certificate.

## Fixed scope and inputs

This audit recomputes, in backward order, the already-frozen M14 half-segments 239, 238, and 237. It preserves the fixed 112-pair witness, K36 set, sign chart, C500 semantic identity, viscosity `nu=0.1`, and terminal time `T=0.003`. No state, witness, coalition, predictor, residual polynomial, or segment bound was retuned or regenerated.

The segment JSON files, their historical recurrence reports, the structured A/B diagnostic, and the earlier reverse-diffusion audit are pinned by SHA-256 in the machine certificate. The independent verifier checks these hashes and recomputes the scalar recurrence from the imported segment bounds. The residual and strain bounds remain producer-supplied whole-segment enclosures; this work does not independently reconstruct them.

## Corrected estimate

For each continuous segment of width `h = 1/80000`, the error norm obeys the scalar Gronwall estimate

\[
 e_{\rm out}\leq e^{Lh}e_{\rm in}+\frac{e^{Lh}-1}{L}R,
 \qquad L=L_{\rm strain}+\nu\max_{|k|\leq15}|k|^2.
\]

The Fourier support check gives `max |k|^2 = 225`, so the reverse-diffusion contribution is `nu*225 = 22.5`. The earlier recurrence used only the strain part and therefore underbounded the propagated error. Decimal arithmetic uses 90 digits, ceiling rounding for arithmetic, and one `next_plus()` step after `exp`.

| Backward segment | Imported strain upper | Corrected total `L` | Incoming error upper | Corrected outgoing error upper |
|---:|---:|---:|---:|---:|
| 239 | 1758.617670280 | 1781.117670280 | 73,244,978,636.905585 | 74,903,737,341.768086947967642… |
| 238 | 1755.447052426 | 1777.947052426 | 74,903,737,341.768086947967642… | 76,596,803,403.200881441529181… |
| 237 | 1752.285153301 | 1774.785153301 | 76,596,803,403.200881441529181… | 78,324,232,548.824619630745751… |

The exact Decimal outputs and provenance are in [the corrected-chain JSON](../results/wp19_v0_28/corrected_chain_20261001/corrected_recurrence_chain.json). The independent verifier record is alongside it.

The structured residual A/B result for step 237 is retained as a sensitivity-only comparison: using its smaller residual gives outgoing radius `78,318,144,302.507836…`, a reduction of about `6.088 million` (`0.007773%`). It is **not substituted** into the official chain.

## Verification and boundary

Run from the repository root:

```bash
python src/wp19_v0_28_corrected_recurrence_chain.py
python src/wp19_v0_28_verify_corrected_recurrence_chain.py \
  results/wp19_v0_28/corrected_chain_20261001/corrected_recurrence_chain.json \
  --output results/wp19_v0_28/corrected_chain_20261001/independent_verification.json
sha256sum -c results/wp19_v0_28/corrected_chain_20261001/SHA256SUMS.txt
```

This is a corrected outward scalar recurrence chain across three already archived continuous segments, conditional on their pinned producer-supplied bounds. It does **not** establish a full adjoint enclosure, independent residual-polynomial or strain-bound reconstruction, dual quadrature, nonlinear remainder control, normalizer lower bound, endpoint sign for `F`, cutoff-uniform behavior, blow-up, or continuum Navier–Stokes regularity. No segment 236 or later was generated.
