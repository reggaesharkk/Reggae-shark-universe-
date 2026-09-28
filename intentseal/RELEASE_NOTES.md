# IntentSeal Verification Kernel — Prototype Freeze Release Notes

Public project name at freeze: **IntentSeal Verification Kernel**.  
Historical working title appearing inside v0.1.1–v0.5.0 artifacts: **AgentOS Verification Kernel**.

## v0.1.1
Deterministic gateway core: registered tools, source authorization, per-call caps, per-actor UTC-day budget reservation, idempotent request IDs, SQLite state, and keyed audit chaining.

## v0.2.0
Authenticated loopback HTTP service. Host-owned bearer-token mappings determine actor and source; clients cannot self-assert trusted identity fields.

## v0.3.0
Actor-namespaced request IDs, audited rejections, human-review state machine, approval/denial credentials, service hardening, timeout semantics, finish-transition checks, and schema versioning.

## v0.4.0
Separated low-trust agent identity from trusted provenance through exact attestation bound to actor, request ID, tool and canonical arguments.

## v0.5.0
Made the consent workflow usable and more scoped: missing-provenance denials no longer burn the ID; trusted-side ID minting; actor-scoped attesters; audit timestamps; bounded clock-regression handling; credential rate limits; restart fault tests.

## Freeze interpretation
v0.5.0 is the terminal historical implementation in this prototype lineage archive. The public rename to IntentSeal does not alter those release bytes. Any further hardening should receive a new semantic version under the IntentSeal name.
