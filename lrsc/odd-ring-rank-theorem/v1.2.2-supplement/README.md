# LRSC Odd-Ring Spectral Rank Theorem — v1.2.2 Supplement

**Prince Upadhyay — Independent Research**  
**Date:** 27 September 2026  
**Status:** additive errata and independent-replication supplement

This supplement does **not** modify the frozen v1.2 theorem release or the
v1.2.1 proof-clarification supplement. It records two non-substantive
corrections to the explanatory v1.2.1 text, clarifies the distinction between
matrix rank and finite subset cardinality, and archives an independently
written recomputation of both the analytic theorem checks and the finite
M=99 benchmark.

The frozen v1.2 DOI remains:

**10.17605/OSF.IO/NM5BW**

## Corrections recorded here

### 1. Derivative typo in the v1.2.1 explanation

For `f(x) = cos(x) cos(2x)`, the derivative is

`f'(x) = -sin(x) [cos(2x) + 4 cos^2(x)]`,

not

`-sin(x) [cos(2x) + 4 cos(x)]`.

On the interval used by the proof, `0 < x < pi/4`, the corrected bracket is
strictly positive, so the required strict decrease of `f` and the
non-vanishing conclusion are unchanged.

### 2. First admissible M in the 4L+1 class

The v1.2.1 text says that the first admissible ring in this residue class is
`M=13`. The correct first admissible value is

`M=9=4*2+1`.

The proof already uses the valid bound `alpha=pi/M <= pi/9`. At `M=9`,
the step `cos(3 alpha) >= 1/2` reaches equality, so the argument remains
valid.

Neither correction changes the theorem statement `rank(V)=p` under the
v1.2 hypotheses.

## Terminology clarification

The theorem quantity and the finite benchmark quantity are different:

- `rank(V)=p` is the **matrix/channel-space rank** from the odd-ring theorem.
- `K_0.001` is the **minimum passing channel-subset cardinality** in a
  specified finite benchmark.

The values 11, 12, and 14 in the M=99 threshold cells are therefore not
matrix ranks. The unambiguous notation is:

| threshold | active reflection orbits p | theorem rank rank(V) | minimum passing cardinality K_0.001 |
|---:|---:|---:|---:|
| 0.07 | 42 | 42 | 14 |
| 0.08 | 41 | 41 | 11 |
| 0.09 | 40 | 40 | 12 |

Historical directory names are retained for stable repository links.

## Independent theorem recomputation

The source in `source/part1_theorem.py` is written directly from the stated
definitions. It does not import the repository theorem verifier.

The recorded run checks:

- direct local-min shedding field against the closed form at 50-digit precision;
- 11,319 Fourier coefficients for odd `M=9,...,301`;
- every odd `M=9,...,40001` in the inequality-chain sweep;
- all 16,343 reflection-symmetric masks with at least one inactive orbit for
  `M=9,11,...,25`;
- the benchmark stress masks at `M=99,101,127`;
- 900 additional random masks on those three rings.

The output reports no non-vanishing inequality violations and reproduces
`rank(V)=41,42,52` at `M=99,101,127`.

A one-line diagnostic guard was added to the archived runnable copy so the
all-zero mask does not divide by a zero leading singular value when reporting
a discarded-singular-value ratio. That guard does not change any rank test.

## Independent finite-benchmark reconstruction

`source/part2_build.py` rebuilds the fixed `M=99`, `k_idx=49`,
`A=1/2` target and all 50 channels directly in real space at 50-digit
precision. It then exports float64 vectors for an independent subset search.

The reconstruction gives:

| threshold | active nodes | active orbits | last failing residual | first passing residual | K_0.001 |
|---:|---:|---:|---:|---:|---:|
| 0.07 | 83 | 42 | K=13: 0.001070386927 | K=14: 0.000974040815 | **14** |
| 0.08 | 81 | 41 | K=10: 0.001039820619 | K=11: 0.000962369128 | **11** |
| 0.09 | 79 | 40 | K=11: 0.001001168188 | K=12: 0.000947945578 | **12** |

The decisive searches were repeated in two orthonormal coordinate systems:
the direct reflection-even basis and an SVD/PCA basis. Both produce the same
winning subsets and residuals to displayed precision, while the branch
coverage counters exactly equal the relevant binomial counts.

The branch-and-bound code uses float64 arithmetic. It is therefore strong
independent numerical corroboration, not a replacement for the repository's
outward-rounded interval and exact-integer certificates. The rigorous
certificates remain the basis for the formal finite claims.

## Structural observation at theta=0.07

The mask change from 0.08 to 0.07 activates nodes 41 and 58. Those are odd
sites of the near-Nyquist shedding field, where `j=0`. Consequently the
target `E=S(mj)` is unchanged between these two cells, while the masked
channel family changes. This explains why the minimum passing cardinality can
move from 11 to 14 even though the target itself is unchanged.

## Reproduction

From this directory:

```bash
python source/part1_theorem.py
python source/part2_build.py
g++ -O3 -std=c++17 -Wall -Wextra source/bnb.cpp -o bnb

python source/run_bnb.py 0.08 10,11 pca
python source/run_bnb.py 0.09 11,12 pca
python source/run_bnb.py 0.07 13,14 pca

python source/run_bnb.py 0.08 10,11 even
python source/run_bnb.py 0.09 11,12 even
python source/run_bnb.py 0.07 13,14 even
```

The archived outputs are under `output/`.

## Claim boundary

This supplement strengthens auditability of the stated odd-ring theorem and
three finite M=99 mask cells. It does not enlarge the theorem beyond its
single-step odd-ring hypotheses, make `K_0.001` universal, establish a
multi-step dynamical result, or imply a continuum fluid theorem.
