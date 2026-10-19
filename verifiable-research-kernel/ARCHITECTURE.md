# Architecture

The long-term system separates three questions:

1. **Authority** — may this agent cause the action?
2. **Evidence** — what machine-checkable evidence supports this claim?
3. **Provenance** — can another verifier reconstruct what was authorized, executed and concluded?

IntentSeal provides the authority side. VRK begins the evidence/provenance side.

## v0.1.0 flow

```text
Research statement
      |
      v
Claim compiler
      |
      +--> claim class
      +--> explicit scope
      +--> dependencies
      +--> evidence roles
      +--> artifact hashes
      |
      v
Domain verifiers
      |
      v
Verification receipt
      |
      v
Hash-chained claim ledger
```

Dependencies form a directed graph. If an upstream claim becomes `FALSIFIED` or `RETRACTED`, descendants are not automatically called false; they are mechanically marked `REVIEW_REQUIRED`.

This prevents silent inheritance of invalid assumptions while preserving the distinction between “dependency failed” and “descendant disproved.”

## Fail-closed rule

Missing evidence is never converted into a confidence score.

An immutable external source can be bound by repository + commit + path + blob SHA, but a required external-only artifact prevents the local kernel from promoting the claim to `CERTIFIED`.

## Next layer

The next architectural interface is an IntentSeal authorization receipt attached to claim publication and expensive verification actions. The agent may propose a claim or experiment, but authority to publish/execute remains separate from the claim's epistemic status.
