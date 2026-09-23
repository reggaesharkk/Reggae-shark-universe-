# LRSC v1.1.1 — Complete K0.001=11 Reproducibility Supplement

Author: Prince Upadhyay, Independent Research

This package reproduces the fixed single-step benchmark at M=99, k_idx=49, theta=0.08, A=0.50 using 50 channels (DC counted). It exhaustively enumerates every exact-cardinality subset for K=1,...,10 and directly checks a passing K=11 witness.

## Result

The K=10 global minimum is {0,1,42,43,44,45,46,47,48,49}, relative residual 0.0010398206190990441. The K=11 witness {0,1,3,42,43,44,45,46,47,48,49} has residual 0.00096236912766441347. Therefore K_0.001=11 for this benchmark under the stated floating-point computation. The empty subset has residual 1.

This is an exhaustive numerical certificate using IEEE double precision, not an interval-arithmetic or exact-rational proof. It is benchmark-specific. The full run enumerates all combinations for each K≤10; K=11 is a directly verified witness, not an optimized K=11 search.

An independently implemented verification is available in
`LRSC_v1_1_1_Independent_Companion.zip`. It separately enumerates the
13,432,735,555 subsets with a different C traversal and checks the K=10
optimum and K=11 witness at 50-digit numerical precision. The latter is a
two-subset cross-check, not a certified interval bound over the full search.
The LRSC research is authored by Prince Upadhyay; independent verification
does not transfer or change authorship of the research.

## Reproduce

Requirements: Python 3, NumPy, and a C++17 compiler (g++ by default). From this directory run:

```sh
python3 source/audit_k1_to_k10.py
```

The script compiles the recursive enumerator `source/exhaustive_search.cpp`, prints expected and visited combination counts, checks the Gram-objective best and runner-up by direct complex-vector reconstruction, and verifies the K=11 witness. Numerical low-order digits may vary across platforms.

## Files

- `LRSC_v1_1_1_K001_Reproducibility_Supplement.pdf` — concise methods/results/evidence-limits document.
- `LRSC_v1_1_1_Independent_Companion.zip` — separate, independently implemented numerical verification distributed alongside this source bundle.
- `source/audit_k1_to_k10.py` — operator arrays, Gram data, audit checks.
- `source/exhaustive_search.cpp` — memory-safe exact-cardinality subset enumeration.
- `source/VERIFICATION_OUTPUT.txt` — complete recorded run output.
- `source/SHA256SUMS.txt` — integrity hashes.

## OSF project DOI

[10.17605/OSF.IO/JAK5X](https://doi.org/10.17605/OSF.IO/JAK5X) identifies the separate OSF project for this numerical reproducibility supplement. The project contains the OSF deposit ZIP; this DOI identifies the project rather than a specific ZIP file version.

Deposit ZIP: `OSF_DEPOSIT_LRSC_v1_1_1_NUMERICAL.zip`  
SHA-256: `4db7cb2c0c03a2c99ae3674078dd14e1cc4db2c0e9255942680d2ae90df23dbe`

This checksum refers to the prepared deposit ZIP. Verify the file downloaded from OSF against this value to confirm it is the same version.

## Versioning

This supplement is separate from historical v1.1. Frozen v1.2 and DOI 10.17605/OSF.IO/NM5BW are not revised or replaced.
