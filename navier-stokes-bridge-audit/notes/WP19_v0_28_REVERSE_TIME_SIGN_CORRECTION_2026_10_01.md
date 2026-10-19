# WP19 v0.28 reverse-time sign correction

**Status: strain-only scalar recurrence reproduced; conclusion is conditional on the archived continuous-segment bounds.**

This additive correction supersedes the sign interpretation in the earlier v0.28 backward-diffusion audit and its follow-up corrected-chain note. Those records remain unchanged as history; the new machine-readable result lists their hashes and the specific claims superseded. The claim that adding `nu * max(|k|^2) = 22.5` was required is withdrawn: the error radius is propagated from terminal time toward decreasing forward time, and viscosity is dissipative in the reverse-propagation `ell2` energy estimate.

## Sign derivation

The archived producer source, copied byte-identically into all three pilot folders (SHA-256 `e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31`), defines the residual by

\[
r = \partial_t L - \operatorname{VJP}(u,L) - \nu\Lambda L.
\]

The exact adjoint equation used here is the finite Galerkin system

\[
\partial_t\lambda=\operatorname{VJP}(u,\lambda)+\nu\Lambda\lambda,
\]

as written in `src/wp19_v0_23_rk4_goal_adjoint.py` (SHA-256 `0ba7cd0464076271a80864118d930d384d2cce6a1974650f278f8e02a7756e01`), with its Galerkin vector field in `src/wp16_036_dealiased_trajectory_gate.py` (SHA-256 `c44824c9562c4e79b11e8838e663ecf77d0992ba5d146b4c5015717018baae14`). These M14 half-segments embed into the finite M15 high-system support used by the adjoint. For `e=\lambda-L`, subtraction gives

\[
\partial_t e = \operatorname{VJP}(u,e)+\nu\Lambda e-r,
\]

Set reverse time \(\tau=T-t\). Then

\[
\partial_\tau e=-\operatorname{VJP}(u,e)-\nu\Lambda e+r.
\]

In the \(L^2\) energy estimate, the transport part is skew, the Leray projection drops against divergence-free \(e\), the strain contribution is bounded by \(\|S(u)\|_{L^\infty,op}\), and

\[
\langle \Lambda e,e\rangle=\sum_k |k|^2|e_k|^2\ge 0.
\]

Under the assumptions below, the transport contribution is skew after projection, the remaining linear contribution is bounded by the symmetric strain, and \(\langle\Lambda e,e\rangle\ge0\). Therefore, in reverse time,

\[
D^+\|e\|_2/D\tau \le \|S(u)\|_{L^\infty,op}\|e\|_2+\|r\|_2.
\]

The negative viscous term can be dropped for an upper bound. The archived strain-only scalar recurrence is valid under the assumptions and imported whole-segment bounds below. Adding `22.5` to the exponent coefficient remains a valid but looser upper recurrence, not a required correction.

The argument is conditional on all of the following: (1) the error is real, divergence-free, and Hermitian-symmetric, with the Leray projection commuting with \(\Lambda\); (2) the true primal field is exactly divergence-free; (3) the exact adjoint is the solution of the finite M15 Galerkin adjoint ODE above for the M14-to-M15 segment, using the archived projected/truncated convolution; (4) one Fourier-coefficient \(\ell^2\) convention is used consistently for the error, residual, primal perturbation, and strain bounds; (5) the supplied strain \(L\) and residual \(R\) bound their norms continuously over the entire half-segment; (6) the supplied primal radius bounds the primal error throughout that segment; and (7) the terminal error bound is valid in the same norm. This packet identifies and hashes the equations and producer sources but does not reconstruct the exact adjoint trajectory or independently prove the supplied segment bounds.

## Recomputed recurrence

The fixed sequence is backward segments `239 -> 238 -> 237`, width `1/80000`, and decimal precision 90. The correction runner pins the segment, recurrence-report, A/B, prior audit, prior audit-source, and prior conservative-chain hashes. The separate verifier replays the recurrence using a Taylor expansion with an outward geometric tail bound. This is a second arithmetic implementation, **not** an independent derivation of the PDE estimate.

| Step | Strain upper \(L\) | Residual upper \(R\) | Recomputed strain-only radius | Archived outward radius | Optional `L+22.5` radius |
|---:|---:|---:|---:|---:|---:|
| 239 | 1758.617670280 | 771,029,886,342.810495 | 74,882,674,993.048618657819… | 74,882,674,993.048618657819…218 | 74,903,737,341.768086947968… |
| 238 | 1755.447052426 | 770,889,881,044.051112 | 76,553,735,316.602437456115… | 76,553,735,316.602437456115…384 | 76,596,803,403.200881441529… |
| 237 | 1752.285153301 | 724,222,211,753.270303 | 78,258,186,399.829279366902… | 78,258,186,399.829279366902…394 | 78,324,232,548.824619630746… |

For each step, the incoming radius is the preceding archived outward value. The replay is no larger than the archived value, and the optional `L+22.5` chain is larger. The archived strain-only radii are the governing values for this three-step scalar recurrence.

## Segment 237 A/B reconciliation

The A/B record pins the same baseline segment-237 SHA-256 and incoming radius, but it separately re-evaluates the strain, residual, and primal-radius upper bounds. Its displayed upper values are slightly larger than the segment record:

| Quantity | Segment 237 | A/B re-evaluation |
|---|---:|---:|
| strain upper | 1752.285153301 | 1752.285153303 |
| nominal residual upper (not used by the old recurrence) | 53857205.702019 | 53857205.702021 |
| primal radius upper | 0.000055664765007 | 0.000055664765009 |

The A/B source (`results/wp19_v0_28/structured_uncertainty_ab_20261001/wp19_v0_28_structured_uncertainty_ab.py`, SHA-256 `b746a70ed9b3d00b8e591b962358207e1050c1bfe378467729048cbcca2b8c77`) computes its old-formula recurrence using its separately rounded strain upper (1752.285153303), the same incoming radius, and the segment's `residual_L2_upper` (724222211753.270303). It does **not** use either displayed nominal-residual value in that old recurrence. Replaying those inputs gives `78258186399.831235707571984…`, which exceeds the archived outgoing value `78258186399.829279366902453…` by about `0.00195634067`. Replacing only the A/B strain by the segment strain while keeping the same incoming radius and segment residual accounts for that entire difference. The packet does not include the arrays needed to explain why the separately recomputed/rounded strain is larger by `2e-9`; that cause remains unresolved. The structured-residual comparison remains diagnostic-only and is not substituted into the archived official chain. The A/B JSON's historical status label is left untouched; this correction labels the comparison diagnostic-only within its own record.

## Provenance and reproduction

Run from the repository root:

```bash
python src/wp19_v0_28_reverse_time_sign_correction.py
python src/wp19_v0_28_verify_reverse_time_sign_correction.py
sha256sum -c results/wp19_v0_28/reverse_time_sign_correction_20261001/SHA256SUMS.txt
```

The result and manifest are under `results/wp19_v0_28/reverse_time_sign_correction_20261001/`. The package includes the two files that were missing from the earlier review bundle and listed in its inner manifests: `notes/WP19_CURRENT_STATUS_2026_09_30.md` and `.github/workflows/wp19_v0_28_backward_diffusion_audit.yml`. The main correction, corrected-chain, and backward-audit manifests use repository-root-relative paths and must be checked from the repository root. The three historical pilot manifests use paths relative to their own directories; check them from inside each pilot directory:

```bash
for d in results/wp19_v0_28/pilot_v2_36818369196 results/wp19_v0_28/pilot_chained_238_36819581437 results/wp19_v0_28/pilot_chained_237_36820757066; do
  (cd "$d" && sha256sum -c SHA256SUMS.txt)
done
```

The archived predictor arrays, adjoint arrays, lower nodes, and primal segment JSON inputs needed to independently reconstruct the producer's segment bounds are not included in this correction package. The reported whole-segment strain and residual enclosures are therefore **not independently re-established here**; the recurrence conclusion is conditional on those archived bounds and their producer provenance. The replay verifier is a separate arithmetic implementation of the same scalar recurrence, not an independent derivation of the PDE estimate.

## Claim boundary

This corrects one finite M14 backward-time scalar error-radius recurrence over three archived half-segments. It does not certify the full adjoint path, dual quadrature, nonlinear remainder, normalizer, signed-observable endpoint transfer, an all-cutoff statement, blow-up, or continuum Navier–Stokes regularity.

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
