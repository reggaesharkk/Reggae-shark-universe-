# Portfolio Evidence and Rights Standard

**Effective 1 October 2026 · Maintainer: Prince Upadhyay**

This standard connects the six specialist programs through shared provenance and review practice. It does not combine their scientific claims, models, datasets, or proof domains.

## Shared evidence record

Every new result promoted to a repository's current status should have a compact record containing:

1. **Claim** — one exact sentence with its assumptions, domain, and quantifiers.
2. **Evidence class** — analytic proof, computer-assisted certificate, finite numerical result, synthetic simulation, confirmatory observation, or interpretation.
3. **Frozen inputs** — artifact names, versions, parameter values, and cryptographic hashes.
4. **Producer and checker** — exact commands and source versions; state whether the checker is independent, same-code replay, or a consistency check.
5. **Decision rule** — predeclared pass/fail/unscorable gates, precision and error bounds, and any sampled-versus-continuous distinction.
6. **Outcome** — PASS, FAIL, UNRESOLVED, or UNTESTED; preserve failed and invalid runs.
7. **Claim boundary** — what the result does not establish.
8. **Rights and provenance** — author, date, applicable file/release license, external inputs, and citations.

A hash proves byte identity, not the truth of a claim. A successful workflow proves that the workflow completed under its checks, not that the claim is broader than the check.

## Cross-program use

| Program | Reusable contribution to the portfolio | Boundary that stays fixed |
|---|---|---|
| Self-Referential Processing + Design Lab | Preregistration, calibration, negative controls, and simulation-analysis audit patterns | Synthetic/diagnostic results do not become live confirmatory evidence |
| Psi Self-Modeling Benchmark | Matching, anonymization, deterministic seeds, and self-vs-peer control design | A benchmark outcome does not establish consciousness or a general self-modeling mechanism |
| Information-Theoretic Physics | Exact symbolic/algebraic checks and explicit parameter-domain statements | The Hopf result stays inside its stated phenomenological ODE; it does not establish a microscopic physical law |
| LRSC | Exact finite combinatorics, interval/exhaustive certificates, and theorem-domain discipline | The odd-ring theorem and finite subset benchmark do not imply universal compression or Navier–Stokes results |
| Navier–Stokes Bridge Audit | Finite-Galerkin identities, validated computation, and explicit continuum proof obligations | Finite-cutoff results do not establish continuum regularity, blow-up, or an all-cutoff theorem |
| IntentSeal + VRK | Typed provenance, integrity checks, authorization records, and evidence-package validation | Software can validate structure and replay gates; it is not an oracle for mathematical truth |

Techniques, code, or schemas may be reused across projects only with a recorded source/version, license check, and domain-specific re-derivation. A result in one program never supplies evidence for a claim in another merely because the same verification tool was used.

## Release and status discipline

- Freeze a protocol and its inputs before prospective data generation.
- Keep exploratory, confirmatory, analytic, and finite-computation evidence distinguishable.
- Never retune a frozen rule on its holdout; log a failure or unscorable outcome and begin any revised rule as a new version.
- Preserve invalid, timed-out, and negative runs with hashes and a short disposition.
- Promote a claim only after its stated verifier/checker passes; report its exact scope and limitations.
- Keep frozen records immutable. Corrections are dated, additive, and point to the superseded statement.

The specialist repositories remain the canonical homes for project code and detailed evidence. This umbrella standard defines only shared recordkeeping and cross-project boundaries.

## Rights

Each specialist repository publishes a dated rights policy:

- [Self-Referential Processing + Design Lab](https://github.com/reggaesharkk/self-referential-processing-designlab/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [Psi Self-Modeling Benchmark](https://github.com/reggaesharkk/psi-self-modeling-benchmark/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [Information-Theoretic Physics](https://github.com/reggaesharkk/physics-v1-dynamical-sector/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [LRSC](https://github.com/reggaesharkk/lrsc-odd-ring-spectral-rank/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [Navier–Stokes Bridge Audit](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [IntentSeal + VRK](https://github.com/reggaesharkk/intentseal/blob/main/RIGHTS_POLICY_2026_10_01.md)
- [Umbrella archive](https://github.com/reggaesharkk/Reggae-shark-universe-/blob/main/RIGHTS_POLICY_2026_10_01.md)

As of 1 October 2026, new author-owned original work is All Rights Reserved by default unless an item-specific notice says otherwise. Prior express licenses remain attached to their historical material.