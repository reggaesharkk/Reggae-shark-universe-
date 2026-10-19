# WP19 v0.28 backward-diffusion recurrence correction

**Status: correction required; the archived three-segment scalar recurrence is not a valid adjoint-error enclosure as written.** This is a finite M14 audit only. The archived residual-polynomial enclosures remain separate results; this note does not certify a full adjoint path or signed-observable transfer.

## Finding

The segment producer encloses the backward adjoint residual using

\[
L' - \mathrm{VJP}(u,L)-\nu\Lambda L = r,
\]

so the corresponding error equation contains the reverse-time viscosity term with a **plus** sign:

\[
e'=P\big((\nabla u)^T e-(u\cdot\nabla)e\big)+\nu\Lambda e+r.
\]

On the periodic Galerkin space, the transport term is skew in the \(L^2\) energy identity, Leray projection drops against divergence-free \(e\), the stretching term is bounded by \(\|S(u)\|_{L^\infty,op}\), and \(\nu\Lambda\) contributes at most \(\nu\max_{k}|k|^2\). Thus

\[
\frac{d}{dt}\|e\|_2\le
\big(\|S(u)\|_{L^\infty,op}+\nu\max_{k}|k|^2\big)\|e\|_2+\|r\|_2.
\]

The archived recurrence used the reported strain bound as its full logarithmic norm and omitted the second term. Since the adjoint support is the ball \(|k|\le15\) and \(\nu=0.1\), the missing contribution is exactly bounded by \(0.1\cdot15^2=22.5\) per unit time. It is small relative to the strain bound but cannot be omitted from a rigorous recurrence.

## Recomputed values

The audit script reads the archived segment and verifier records by fixed SHA-256, preserves their residual bounds, and recomputes only the Decimal recurrence with the corrected growth coefficient.

| Backward segment | Archived strain bound | Corrected total log-norm bound | Archived outgoing error | Corrected outgoing error |
|---:|---:|---:|---:|---:|
| 239 | 1758.617670280 | 1781.117670280 | 74,882,674,993.048619 | 74,903,737,341.768087 |
| 238 | 1755.447052426 | 1777.947052426 | 76,553,735,316.602437 | 76,596,803,403.200881 |
| 237 | 1752.285153301 | 1774.785153301 | 78,258,186,399.829279 | 78,324,232,548.824620 |

For the frozen segment-237 structured uncertainty A/B, the penalty ratio remains \(0.334854921854\), so its **residual-penalty** tightening is unchanged. Re-evaluating the outgoing recurrence after correcting the incoming chain gives:

- old residual formula: `78,324,232,548.824620`
- structured residual formula: `78,318,144,302.507836`
- reduction: `6,088,246.316783`, or about `0.007773%` of the corrected old outgoing bound.

This remains a one-segment comparison and is not an endpoint-sign result. The corrected error radius is larger than the previously archived value; the structured residual still improves that corrected bound slightly.

## Reproduction and frozen inputs

Run from the repository root:

```bash
python src/wp19_v0_28_backward_diffusion_log_norm_audit.py
```

The script verifies the exact archived SHA-256 values for segments 239, 238, 237, their recurrence reports, and the structured A/B result. It recomputes the maximum squared wave number from the frozen spherical support definition and fails if it is not 225. The machine result is:

`results/wp19_v0_28/backward_diffusion_audit_20261001/backward_diffusion_audit.json`

The audit status is deliberately `RECURRENCE_CORRECTION_REQUIRED`: the old recurrence reports are retained as historical artifacts and are not rewritten. No further segment should be chained from their outgoing error values. A corrected fail-closed chain verifier must replace them before segment continuation.

## Claim boundary

This correction concerns the reverse-diffusion contribution in a finite-dimensional backward-adjoint error estimate for three archived M14 half-segments. It establishes no complete adjoint enclosure, dual quadrature, normalizer bound, C500 endpoint transfer, all-cutoff persistence, blow-up, or continuum Navier–Stokes regularity result.
