# OSF Deposit Metadata — LRSC Odd-Ring Spectral Rank Theorem v1.2

**Author:** Prince Upadhyay  
**Affiliation:** Independent Research  
**Date:** 22 September 2026  
**License:** CC BY 4.0

## Recommended title

LRSC Odd-Ring Spectral Rank Theorem: Exact Channel-Space Rank for Near-Nyquist Odd Cyclic Systems — v1.2

## Recommended description

This release presents an analytic family theorem for the single-step near-Nyquist LRSC operator on odd cyclic lattices. For odd M>=9, if the binary mask is reflection-symmetric and has at least one inactive reflection orbit, the conjugate-balanced post-stencil channel matrix V has rank exactly equal to p, the number of active reflection orbits.

The proof proceeds through four components: an exact closed form for the local shedding field; residue-class formulas proving non-vanishing of the required Fourier coefficients for M=4L+1 and M=4L+3; a Chebyshev/Vandermonde argument establishing pre-stencil independence; and injectivity of the circulant stencil on the masked channel span.

A computational verification companion corroborates the algebra by checking 500,494 Fourier-coefficient comparisons over all odd M=9,...,2001 and exact cyclotomic non-vanishing for M=99,101,127. The finite checks are corroborative and do not replace the analytic proof.

The result is a structural rank theorem. It does not claim a universal fixed-unit compression number K_tau, a microscopic physical law, or a multi-step dynamical theorem.

## Recommended keywords

LRSC; odd cyclic lattice; spectral rank; Fourier analysis; Chebyshev polynomials; Vandermonde determinant; cyclic systems; local redistribution; near-Nyquist carrier; spectral decomposition; structural theorem; computational verification

## Files for the frozen deposit

- LRSC_Odd_Ring_Rank_Theorem_v1_2.pdf
- LRSC_Odd_Ring_Rank_Theorem_v1_2.tex
- THEOREM_v1_2.md
- PROOF_LEDGER.md
- verify_lrsc_odd_ring_rank_v1_2.py
- VERIFICATION_OUTPUT.txt
- ENVIRONMENT.txt
- README.md
- SHA256SUMS.txt
- LRSC_Odd_Ring_Rank_Theorem_v1.2.zip

## Release hashes

Theorem PDF SHA-256:
`18702fa4b2609460c91321a2b59469453529ed07abb54ea6f09d754008ad898f`

Release ZIP SHA-256:
`ef0f0066166f8957056842f06d898360330c56ebb428da5302e7325a0f30184d`

## Lineage

- LRSC single-step spectral certificate v1.0
- LRSC structural mechanism audit v1.1
- LRSC odd-ring spectral rank theorem v1.2
- Multi-step dynamics: future development stage, not part of the v1.2 frozen claim
