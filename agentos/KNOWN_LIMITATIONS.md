# Known Limitations at v0.5.0 Freeze

1. Gateway, confirmation/attester UI, and executor are not yet separated into mutually isolated OS processes/accounts.
2. Callback timeout stops waiting but cannot forcibly terminate a Python callback thread.
3. Bearer credentials do not yet have first-class credential IDs, rotation, or revocation.
4. Tool-specific argument schemas are not yet enforced before costing and dispatch.
5. Audit-chain anchors are not automatically retained outside the gateway host.
6. Consent receipts are not asymmetrically signed.
7. The host clock remains trusted; timing checks cannot prove wall-clock correctness across periods with no AgentOS events.
8. v0.5.0 attestation TTL currently behaves as an admission-time grant unless a later release explicitly changes dispatch-time freshness semantics.
9. A valid attester credential attempting an actor outside its allowed scope is rejected at the service layer, but v0.5.0 does not necessarily add that failure to the gateway's chained audit log.
10. Windows execution was not independently verified for this freeze.
11. The original v0.5.0 `SHA256SUMS.txt` includes a self-checksum entry that fails. Every other entry passes; the original ZIP remains preserved unchanged and is itself correctly hashed by the lineage archive.
