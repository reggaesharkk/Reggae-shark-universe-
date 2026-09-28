# IntentSeal Verifiable Research Kernel (VRK) v0.1.0

A proof-carrying claim kernel for AI-assisted research.

The core rule is:

> **No evidence type, no epistemic promotion.**

VRK turns a research claim into a canonical machine-readable object carrying scope, dependencies, evidence bindings, verifier outputs, and a cryptographic digest. It is designed to make category errors mechanically visible: a numerical observation cannot silently become a theorem; an exhaustive finite result cannot silently become a continuum statement; a falsified dependency forces downstream review rather than disappearing into prose.

## v0.1.0 seed

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

## Demonstrator 001

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
