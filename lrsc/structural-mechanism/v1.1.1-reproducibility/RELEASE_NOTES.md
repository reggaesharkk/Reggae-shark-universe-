# Release notes — LRSC v1.1.1

A separate reproducibility supplement for the M=99, k_idx=49, theta=0.08, A=0.50 single-step compression benchmark. Includes PDF, Python driver, C++17 exhaustive enumerator, and run output.

The source verifies all subsets at every exact cardinality K=1 through 10 and directly verifies one passing K=11 witness. It reproduces K_0.001=11 in IEEE double precision for this stated benchmark. This is not an interval-arithmetic or exact-rational proof.

The historical v1.1 files, frozen v1.2 theorem, and DOI 10.17605/OSF.IO/NM5BW are unchanged.

## Verification companion and wording correction (2026-09-23)

Research author: Prince Upadhyay, Independent Research. The separately
implemented `LRSC_v1_1_1_Independent_Companion.zip` reproduces the exhaustive
double-precision result using a different enumeration method. Its 50-digit
check evaluates only the K=10 optimum and one K=11 witness; it is not a
certified interval proof. The total K=1,...,10 subset count is 13,432,735,555.
Source audit labels now say `prior_claim_A/B`; only those labels and
documentation changed. Numerical values and the operator did not change.
