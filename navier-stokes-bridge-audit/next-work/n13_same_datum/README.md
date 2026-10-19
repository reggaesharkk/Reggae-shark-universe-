# N13 same-datum cutoff check

The frozen test is specified in `PROTOCOL.md`; it uses the same exact rational
witness, K36 key file, viscosity, time grid, observable, and pass gates as N12,
with only the Galerkin cutoff changed to N13.

## Result

All 120 whole-segment enclosures were independently regenerated with Arb and
accepted against their saved outward-rounded bounds. The endpoint and
whole-path normalizer gates passed in the same run.

| Gate | Certified value |
| --- | ---: |
| Exact initial observable `F(0)` | `[645.8037741471, 645.8037741472]` |
| N13 trajectory error at `T=0.003` | `<= 0.000012244529` |
| True endpoint observable `F(T)` | `[-87.154087422, -83.563901281]` |
| Whole-path K36 normalizer absolute value | `>= 48869.38355689` |
| Independent Arb segment replay | `120/120 PASS` |

Together with the N11 and N12 certificates, this is a validated sign crossing
for the same datum at three finite Galerkin cutoffs. It does not establish a
cutoff-uniform estimate, a continuum result, blowup, or global regularity.

The earlier N13 K36 holdout in `n11-full-replay/src/` is a different test and
is not an input to this certificate. The final machine-readable result and
replay log are in `results/full_run/`; the `first_pass_receipt.md` records the
intermediate checkpoint and points to the final receipt.
