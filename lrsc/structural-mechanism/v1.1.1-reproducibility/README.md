# LRSC v1.1.1 — Complete K0.001=11 Reproducibility Supplement

Author: Prince Upadhyay, Independent Research

This companion supplement documents the single-step benchmark at M=99, k_idx=49, theta=0.08, A=0.50, using 50 channels with DC counted. It exhaustively searches every exact-cardinality subset for K=1 through 10 and directly verifies one passing K=11 witness.

## Result

For each K=1,...,10, every binomial(50,K) subset was visited. The smallest residual at K=10 is 0.0010398206190990441, above 0.001. A K=11 witness, {0,1,3,42,43,44,45,46,47,48,49}, has directly recomputed residual 0.00096236912766441347. Thus K_0.001=11 for this benchmark under the stated IEEE double-precision computation. Full-channel closure is 2.3808015585084204e-16.

The result is an exhaustive numerical certificate, not an interval-arithmetic, exact-rational, or formally verified rounding-error proof. It applies only to this benchmark. K=11 is a passing witness, not an exhaustive optimization at K=11.

## Files

- [Supplement PDF](LRSC_v1_1_1_K001_Reproducibility_Supplement.pdf)
- [Complete source bundle ZIP](LRSC_v1_1_1_Source_Bundle.zip)
- source/audit_k1_to_k10.py — operator/channel construction, Gram objective, direct checks
- source/exhaustive_search.cpp — recursive enumeration without materializing combinations
- source/VERIFICATION_OUTPUT.txt — recorded full output
- source/SHA256SUMS.txt — integrity hashes (run from this directory's parent package root)
- RELEASE_NOTES.md

Run from the extracted source bundle: python3 audit_k1_to_k10.py (Python 3, NumPy, C++17 compiler required).

Historical v1.1, frozen v1.2, and DOI 10.17605/OSF.IO/NM5BW remain unchanged.
