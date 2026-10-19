# LRSC K₀.₀₀₁(0.50) — uniform interval audit candidate v0.1

**Research author:** Prince Upadhyay, Independent Research.

**Status:** Reproducible computational certificate candidate for the fixed
M=99, k_idx=49, theta=0.08, A=0.50 single-step benchmark. The code and
arithmetic argument should receive independent review before this is described
as a formally established theorem. This candidate is separate from the
historical v1.1, frozen v1.2, and DOI 10.17605/OSF.IO/NM5BW.

## Claim and scope

With DC counted among 50 conjugate-balanced channels and relative Fourier L2
error at most 0.001 as the target, the recorded exhaustive enumeration finds no
passing subset for exact cardinality K=1,...,10 (13,432,735,555 total). A
directly constructed K=11 witness passes. The empty subset has error 1 because
the exact update vector has positive squared norm. No claim is made about other
amplitudes, masks, ring sizes, or iteration times.

This candidate adds an **exact-integer interval enclosure of the operator** and
a **uniform IEEE binary64 accumulation bound** to the distinct C bitmask
enumeration. It does not perform billions of interval evaluations. The
uniform bound applies to every enumerated subset.

## Bound architecture

Let E be the exact Fourier update, V_r its channels, and S the chosen subset.
For every S, the squared residual is

    R(S) = c + sum_{r in S} l_r + 2 sum_{r<t in S} g_{rt},

where c=||E||², l_r=||V_r||²−2 Re<E,V_r>, and
g_{rt}=Re<V_r,V_t>. Passing requires R(S) <= 10^-6 c.

`interval_certificate.py` represents each real enclosure as two signed
integers on the grid 2^-192. Integer addition is exact and every multiplication
or division rounds its lower endpoint down and upper endpoint up. It brackets
pi using the alternating arctangent series and Machin's identity
pi=16 arctan(1/5)−4 arctan(1/239); sine and cosine use finite Taylor sums and
explicit Lagrange remainder bounds for arguments in [-4,4]. The script checks
all mask inequalities, yielding N_act=81, and encloses every Fourier/channel
coefficient and every quadratic coefficient. None of these enclosures relies on
`mpmath`'s ordinary high-precision floating-point values.

Comparison to the exact binary64 values in `channels.bin` gives a single
worst-case bound for any K<=10 subset:

    |R_exact(S) − R_exact-of-stored-coefficients(S)| <= 8.173e-14.

The C scorer performs at most 55 sequential additions for K<=10. Under IEEE
binary64 round-to-nearest with the stated compiler options, the standard
gamma_55 summation bound, including a gradual-underflow allowance, is below
3.443e-14 uniformly. Multiplication of a finite stored Gram coefficient by
two is exact here. Combining these bounds, each true score differs from its
recorded C binary64 score by less than 1.162e-13. These displayed decimal
values are rounded summaries; the script compares integer/rational endpoints.

`search.c` prints each global minimum as `%a`, preserving the exact binary64
score in the run log. The script checks that the reconstructed score of that
subset equals the recorded hexadecimal value exactly, checks all visited
counts against Python integer binomial coefficients, and subtracts the
uniform error bound from every recorded minimum. The smallest certified
positive gap in squared-error units is approximately **4.098e-8** (K=10).
The interval upper bound of the stated K=11 witness falls approximately
**3.726e-8** below its squared-error threshold. Thus the decision margins
are over five orders of magnitude larger than the uniform arithmetic bound.

The logic depends on the C traversal really visiting every subset once, the
source/binary/log correspondence, exact Python integer and rational semantics,
and ordinary IEEE binary64 round-to-nearest for the compiled C scoring loop.
The relevant code is included for independent inspection; the count checks
alone would not prove traversal uniqueness. This is an implementation-level
candidate, pending review of those assumptions and the interval implementation.

## Reproduce

Requires Python 3, NumPy, and a C11 compiler. Run in this folder:

```sh
sha256sum -c SHA256SUMS.txt
bash run_all.sh
```

The full C search visits all K=1,...,10 subsets and can take several minutes.
To inspect just the interval calculations against the archived `channels.bin`
and hexadecimal search log, run `python3 interval_certificate.py`. The archive
includes both input files and a recorded `INTERVAL_AUDIT_OUTPUT.txt`. Running
the complete script regenerates the logs, so verify original hashes before
regenerating if you intend to check the archived bytes.

## Files

- `interval_certificate.py`: rational/dyadic interval construction and
  all-cardinality decision checks.
- `build_operator.py`, `search.c`, `run_all.sh`: numerical input generator,
  separately implemented exhaustive bitmask scorer, and reproduction commands.
- `channels.bin`, `VERIFICATION_OUTPUT_independent.txt`: exact archived
  binary64 input and full enumeration output with hexadecimal minima.
- `INTERVAL_AUDIT_OUTPUT.txt`: fixed-benchmark interval check output.
- `SHA256SUMS.txt`: hashes of the archived files other than this manifest.

**Attribution:** The LRSC operator, benchmark, and research claims are Prince
Upadhyay's. A separate implementation is used to check them; verification
method provenance does not transfer research authorship.
