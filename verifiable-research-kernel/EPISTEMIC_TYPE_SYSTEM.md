# Epistemic type discipline

VRK deliberately does not reduce evidence to one scalar confidence score.

Current evidence/claim classes:

- `CONJECTURE`
- `NUMERICAL_OBSERVATION`
- `REPRODUCED_RESULT`
- `EXHAUSTIVE_FINITE_RESULT`
- `INTERVAL_CERTIFIED_RESULT`
- `ANALYTIC_THEOREM`

Lifecycle states such as `FALSIFIED`, `RETRACTED`, and `REVIEW_REQUIRED` are separate from claim classes.

Each class has its own evidence obligations. The relation is therefore a partial type discipline, not a ladder in which every class is “stronger” than the previous one.

The kernel rejects silent casts such as:

`NUMERICAL_OBSERVATION -> ANALYTIC_THEOREM`

unless a theorem-specific claim object supplies the required definition, proof and scope evidence.

## Design invariant

**A claim cannot acquire a stronger-sounding label by prose.**

Promotion is a machine-checkable state transition whose obligations are explicit.
