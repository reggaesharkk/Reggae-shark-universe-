# IntentSeal Verifiable Research Kernel (VRK)

Part of program 06, IntentSeal. The historical v0.1.0 seed remains preserved below.

## Current finite demonstrator, 28 September 2026

The immutable v0.3.0 archive (`b01178e81b0e0f07c67a883d8e51430f8af0dc608c5246ee925f6c5c17c0b52c`) locally reproduced 22 tests, 13 semantic mutations, exact K0–K13 coverage of 527046644056 subsets, and a rigorous K14 witness for the finite LRSC M=99, theta=0.07 benchmark. Its proposition digest is `c8e24478afe2579f25020ded46f93e379b414caf4dc466f45e0dac0a854ec0cf`. The scientific status is bounded by the implemented domain verifier.

A v0.3.1 deterministic clean-room candidate is in audit. It is not yet a final release or DOI deposit. The evidence seal does not confer publication authority. No continuum Navier–Stokes or universal physical claim follows.

## Historical v0.1.0 seed


Implemented and locally tested:

- canonical claim manifests;
- class-specific evidence obligations;
- SHA-256 artifact binding;
- domain-verifier plugin interface;
- hash-chained claim-event ledger;
- dependency invalidation propagation;
- LRSC Demonstrator 001.

The executable v0.1.0 package passed 6/6 local tests.

Frozen development artifact:

`IntentSeal_Verifiable_Research_Kernel_v0_1_0.zip`

SHA-256:

`ed4a2842e44a2d23785417f2e76054122b0c7da31e30054aa2ea4e3183abc49a`

## Demonstrator 001 in the historical v0.1.0 seed

Claim:

> For the specified LRSC M=99, k_idx=49, A=1/2, theta=0.07 finite benchmark, the minimum passing channel-subset cardinality at relative residual tolerance 1e-3 is K_0.001=14.

The kernel verifies the locally included K=14 integer witness summary and exact combinatorial coverage/status logs for K=11,12,13, while immutably binding the formal definition and independent replication to the canonical LRSC repository commit.

The resulting kernel status is intentionally:

`EVIDENCE_BOUND`

rather than `CERTIFIED`, because not every required external domain artifact is vendored and replayed inside VRK yet.

That distinction is a feature: the kernel refuses to claim more than it actually rechecked.

## Long-term direction

VRK is intended to connect to IntentSeal's action-authority layer so one system can answer both:

- **Was this action authorized?**
- **Is this scientific claim supported at the level it asserts?**

Research prototype. No universal scientific-truth or production-security claim is made.
