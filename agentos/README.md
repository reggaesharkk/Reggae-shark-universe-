# AgentOS Verification Kernel — Prototype Lineage Archive

**Frozen prototype lineage:** v0.1.1 → v0.2.0 → v0.3.0 → v0.4.0 → v0.5.0  
**Freeze date:** 2026-09-28  
**Author:** Prince Upadhyay, Independent Research

AgentOS is a research prototype for mediating tool calls from an untrusted or prompt-injected agent through a deterministic policy, budget, review, provenance, and audit layer. It is not a production security boundary.

## Frozen lineage

| Release | Fresh Linux tests | Main milestone |
|---|---:|---|
| v0.1.1 | 10/10 | atomic policy/budget enforcement and keyed audit chain |
| v0.2.0 | 14/14 | authenticated loopback service |
| v0.3.0 | 34/34 | review workflow, audited rejection paths, timeout/schema hardening |
| v0.4.0 | 47/47 | separate attestation/provenance channel |
| v0.5.0 | 61/61 | usable consent lifecycle, trusted-side request IDs, scoped attesters, audited timing, rate limiting, restart fault tests |

The frozen all-in-one archive is:

`AgentOS_Prototype_Frozen_Lineage_v0_1_1_to_v0_5_0.zip`

SHA-256:

`e853fcf1e75f48ee91dbcb64f4dbe8f3558aa25d05d0102e8bbaea8883913afa`

The archive preserves the five original release ZIPs unchanged, includes a pristine expansion of v0.5.0, fresh Linux verification logs, release hashes, freeze metadata, citation metadata, and Zenodo-ready metadata.

## Scope

The current prototype demonstrates local program invariants under its stated assumptions. It does **not** prove prompt-injection immunity, host compromise resistance, financial settlement correctness, or secure process isolation.

Known limitations and the freeze boundary are recorded in this directory. Future hardening should receive a new semantic version instead of rewriting this frozen lineage.

## DOI status

The archive is prepared for a Zenodo software deposit. A DOI is **not yet claimed in this repository**. When Zenodo mints the DOI, add it through a new additive commit/release; do not alter the frozen release bytes.
