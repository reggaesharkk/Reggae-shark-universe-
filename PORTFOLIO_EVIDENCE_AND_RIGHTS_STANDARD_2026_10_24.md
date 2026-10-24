# Portfolio Evidence and Rights Standard (24 October 2026 Update)

**Effective Date:** 24 October 2026 · **Maintainer:** Prince Upadhyay ([ORCID: 0009-0002-1170-4487](https://orcid.org/0009-0002-1170-4487))  
**Supersedes Additively:** `PORTFOLIO_EVIDENCE_AND_RIGHTS_STANDARD_2026_10_01.md`

This standard connects the nine research programs in the Reggae Shark Universe portfolio through shared provenance, verification, and claim-boundary practice. It does not combine their scientific claims, mathematical models, datasets, or proof domains.

---

## 1. Shared Eight-Field Evidence Record

Every result promoted to a repository's current status or consolidated into the Master Research Dossier must carry an explicit record containing:

1. **Claim** — one exact sentence with its assumptions, domain, and quantifiers.
2. **Evidence Class** — `PROVED / ANALYTIC`, `CERTIFIED / COMPUTER-ASSISTED`, `SIMULATED`, `PREREGISTERED`, `DIAGNOSTIC`, `FALSIFIED / FAILED / UNEVALUABLE`, or `OPEN`.
3. **Frozen Inputs** — artifact names, versions, parameter values, and cryptographic SHA-256 hashes.
4. **Producer and Checker** — exact commands, toolchains (e.g., Lean `v4.15.0`, Python `3.12`, `python-flint` Arb 128/192-bit, C++ exact integer enumerator), and whether the checker is an independent implementation, multi-solver cross-check, or same-code replay.
5. **Decision Rule** — predeclared pass/fail/unscorable gates, precision and error tolerances, and any sampled-versus-continuous or basin-dependent distinction.
6. **Outcome** — `PASS`, `FAIL`, `UNRESOLVED`, or `UNTESTED`; preserve failed and invalid runs with their hashes.
7. **Claim Boundary (`does_not_imply`)** — what the result explicitly does not establish.
8. **Rights and Provenance** — author, date, applicable file/release license, external inputs, and persistent DOIs/commits.

> A SHA-256 hash proves byte identity, not the mathematical truth of a broader conjecture. A passing CI workflow proves that the workflow completed under its declared checks, not that the claim extends beyond those checks.

---

## 2. Cross-Program Verification Architecture & Fixed Boundaries

| # | Program | Reusable Methodological Contribution | Fixed Boundary (`does_not_imply`) |
|---|---|---|---|
| **01** | **Self-Referential Processing + Design Lab** | Preregistration (`v8.6.3`), 1,000-seed null calibration harness, and paired 4,000-fit GLMM Monte Carlo architecture screening (`M1` vs `M2`) | Synthetic Phase 7 results do not become live confirmatory evidence; `v8.6.3` live collection remains paused (`FAIL-CLOSED`). |
| **02** | **Psi ($\Psi$) Self-Modeling Benchmark** | Deterministic 2AFC self-vs-peer matching, anonymization, style controls, and additive OSF manifest auditing | Benchmark scores do not establish machine consciousness, subjective selfhood, or sentience. |
| **03** | **Information-Theoretic Physics (`v1.0–v1.5`)** | Exact 93/28-monomial Hopf positivity (`l_1 > 0`), soft-wall dissipative completion (`v1.5`), and Lean 4 6-face box invariance | Internal to the specified 3D phenomenological ODE; Gate 0 microscopic observer-to-horizon bridge remains `OPEN`. |
| **04** | **LRSC Odd-Ring Spectral Rank** | Analytic Chebyshev/Vandermonde odd-ring rank proof ($\operatorname{rank}(V)=p$) + 13.43B-subset outward-rounded interval enumeration ($K_{0.001}=11$) | Single-step finite ring operator only; does not imply universal compression or continuum PDE regularity. |
| **05** | **Navier–Stokes Bridge Audit** | 128-bit Arb whole-segment Galerkin certificates (`N=11..18`), signed-`C500` terminal gradient intervalization, and preserved prospective gate failures (`N17`) | Finite-cutoff ODE results do not establish continuum 3D Navier–Stokes regularity, blow-up, or an all-cutoff theorem. |
| **06** | **IntentSeal + VRK (`v0.3.1`)** | Typed proposition/evidence/authority separation, dual-seal promotion gates, and adversarial tampering rejection (`33/33`) | Validates manifest structure and deterministic replay gates; not a universal mathematical truth oracle or production security boundary. |
| **07** | **Riemann Bandwidth-One Verification (`WP84`)** | Discrete Loewner $C^2$ band-truncation proof (constant `12`), 150-term $C_5$ rational polyhedral sign proof, and order-4 counterexamples | Finite/matrix theorems and conditional (`68.82%`) or model (`79.63%`) consumers do not establish an unconditional $>79\%$ zero-proportion record or the Riemann Hypothesis. |
| **08** | **Theory of Bounded Existence (`Appendix B v1.0`)** | 17-theorem Lean 4 8-face boundary suite (`ExistenceVerification.lean`), exact rational $de_c/d\mathcal{P}_0 > 0$ proof, variational Floquet (`< 10^-8`), and $\Psi$-memory zero-drive bistability | Illustrative dimensionless 4D ODE with unit constants and no thermodynamic energy accounting; basin-dependent cycle threshold from $x_0$ is not a continuation-certified global SNLC. |
| **09** | **STRENGTH H4-BRIDGE-1 & Attack Board `v0.6`** | Exact BPTT gradient audit (`100` recurrent networks), $D-2$ causal marker SNR falsification, Sheppard's orthant theorem, and 7-problem falsification gates | Falsifies naive $D-2$ variance markers and defines prospective gates; does not claim solution of the seven open Clay/physics problems. |

---

## 3. Rights and Licensing Policy Across the Portfolio

- **Umbrella & Default Policy (effective 1 October 2026):** Unless a specific repository release or file notice states an express open license, new author-owned original material is **All Rights Reserved** (`Copyright (c) 2026 Prince Upadhyay`). Prior express licenses remain permanently attached to the historical releases they cover.
- **Explicit Open-License Releases:**
  - **The Theory of Bounded Existence (`v1.0.0`, [Zenodo `10.5281/zenodo.23608244`](https://doi.org/10.5281/zenodo.23608244) & [GitHub `theory-of-bounded-existence`](https://github.com/reggaesharkk/theory-of-bounded-existence)):** Dual-licensed for open scientific reproduction — **MIT License** for all source code (`verify_all.py`, `ExistenceVerification.lean`, CI workflows) and **Creative Commons Attribution 4.0 International (CC BY 4.0)** for the manuscript (`theory_of_existence_v1_0.tex` / `.pdf`), certificate data, and figures.
  - **Historical `v0.1` / `v0.2` Navier–Stokes & OSF Releases:** Governed by their contemporaneous MIT / CC BY 4.0 license notices as recorded in their respective `LICENSE.md` and `RIGHTS_POLICY_2026_10_01.md` files.
