# LRSC Structural Mechanism Audit v1.1

**Author:** Prince Upadhyay, Independent Research  
**Status:** Historical audited intermediate release in the LRSC lineage  
**Locked benchmark:** `M=99`, `k=49`, `A=0.50`, `theta=0.08`

This stage sits between the original single-step spectral certificate (v1.0) and the odd-ring analytic family theorem (v1.2).

## What v1.1 established

For the locked M=99 single-step benchmark:

- the modular folding identities were isolated;
- the active reflection-orbit count is 41;
- interval arithmetic resolved all local-min branches and certified the required shedding Fourier scales `r=0,...,40` away from zero;
- Chebyshev/Vandermonde structure gives pre-stencil rank 41;
- a custom branch-and-bound / interval weak-duality audit excludes every binary subset with `|S|<=10` at tolerance `1e-3`;
- the explicit K=11 witness passes, so `K_0.001=11` for the locked benchmark.

## Scope boundary

This release is benchmark-specific. It does not claim that K=11 or rank 41 is universal, and it does not establish multi-step dynamics or a microscopic physical law.

The later v1.2 release supersedes the benchmark-only rank mechanism by proving the odd-ring rank law analytically for the stated family.

## Reproducibility note

The historical v1.1 author package records the final certificate and verification log, but it does not contain the full standalone Door-2 verifier source and full dual-witness/tree payload needed for maximal independent re-execution of every bound from the package alone. For that reason, v1.1 is preserved here as an intermediate audited record rather than promoted as the final family theorem release.

## Lineage

Previous: [v1.0 single-step spectral certificate](../../single-step/v1.0/)  
Next: [v1.2 odd-ring spectral rank theorem](../../odd-ring-rank-theorem/v1.2/)
