# Project status — v0.1.0 seed

**Date:** 28 September 2026

Implemented:

- canonical research-claim manifests;
- class-specific evidence obligations;
- SHA-256 artifact binding;
- verifier plugin API;
- LRSC coverage-log verifier;
- integer check of the LRSC K=14 witness summary;
- hash-chained claim-event ledger with tamper detection;
- dependency invalidation propagation;
- LRSC Demonstrator 001.

Local tests: **6/6 PASS**.

Current LRSC demonstrator result: **EVIDENCE_BOUND**.

That status is intentional. Several required artifacts are locally replayed while the formal definition and independent replication remain immutably bound to the canonical LRSC repository rather than fully vendored/re-executed inside VRK. The kernel therefore refuses to label its own local run `CERTIFIED`.

## Next gates

1. vendor or securely retrieve the complete LRSC verifier stack and promote Demonstrator 001 only after full replay;
2. add a Navier–Stokes adapter after the finite-N11 Arb package actually closes;
3. define the IntentSeal authorization-receipt interface for claim publication/execution;
4. add adversarial claim-promotion tests: forged evidence, scope widening, dependency removal, stale evidence and contradictory certificates;
5. specify signed public claim receipts and external ledger anchoring.
