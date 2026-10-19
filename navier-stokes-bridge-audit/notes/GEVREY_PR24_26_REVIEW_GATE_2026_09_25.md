# Review gate for PRs #24–26

**Prince Upadhyay, Independent Research — 25 September 2026**

This procedure was used for PRs #24 and #25 and remains the review gate for draft PR #26. Passing it supports merging finite-Galerkin diagnostics and precise scope notes. It
would **not** certify a new Navier–Stokes regularity theorem, an
independent peer review, or an analyticity radius for arbitrary data.

## 1. Baseline and merge order

Confirm `main` contains merged PR #23 and its Gevrey uniform majorant.
PR #24 merged at `cc1920dae3d0f6fa3e048b22fb2ca3ca8757e9cd`. PR #25 merged at `98e8e8107a652900343f0bcff7dd01be11156db7` in that order. The procedure was: review and merge [PR #24](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/24)
before [PR #25](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/25),
then review and merge [PR #26](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/26).
The code in #25 does not import #24, but its note interprets the #24
phase work; the Master Record in #26 registers both. After each merge,
check the remaining branches against the new `main` and resolve any
conflict without rewriting recorded numerical values. Do not treat
GitHub's `mergeable` flag as code review.

Before merging #26, verify its status table records the two actual merge
commits above. The table has been refreshed on the #26 branch.

## 2. Reproduce the finite identities

From a clean checkout with `requirements.txt` installed, run:

```bash
python3 src/gevrey_phase_drift_tracker.py --output /tmp/gevrey_phase_drift_review.json
python3 src/gevrey_commutator_identity_audit.py --output /tmp/gevrey_commutator_review.json
```

Compare outputs with the concise `src/*verified_summary.json` files in
the corresponding PRs. The #24 audit should reconstruct the weighted
nonlinear transfer to relative error no larger than `1e-11` on its
recorded cases, with recorded worst observed `5.37e-15`. The #25 audit
should close its global commutator, each shell commutator, transport
cancellation, and square partition under its `1e-10` assertion gate;
recorded worst global relative error is `4.74e-15`. These tolerances
verify finite floating-point algebra only. Compare values with sensible
floating-point tolerance across platforms; do not require bitwise
equality of JSON text.

For #24, verify `k=p+q`, ordered-pair and conjugate multiplicities,
projection, the sign of `−Re(i z)=Im(z)`, zero-amplitude phase handling,
and that display thresholds leave *all* triads in total transfer.
Check the product-rule `dot z` against centered differences, including
the halved-step error change. Confirm the direct viscous part is a real
multiple `−ν(|k|²+|p|²+|q|²)z`, not a contribution to instantaneous
triad angular velocity. Viscosity can still affect later nonlinear
phases through amplitudes.

For #25, verify the symbol is `m(k)=e^(σ|k|)|k|^s`, with its **square**
in X and Y. Re-derive `m(k)−m(q)` with both polynomial and exponential
parts. Confirm that `Σ_j ψ_j(k)²=1` on every retained nonzero mode and
that the signed shell sum recovers the original nonlinear transfer.
The unweighted strain commutator from earlier work is a different
identity; no direct bridge between them is claimed.

## 3. Numerical and proof-claim audit

Keep the original Master Record N=4/5, t=0.02 strain results distinct
from the new N=4/7, t≤0.005 Gevrey runs. The phase cancellation ratio
in #24 is about 0.0704 versus 0.4083 in the perturbed persistence
case at t=0.005: a difference of about **33.8 percentage points**, not
an unexplained “31.75% local transfer gap.” It is a signed weighted
H²-transfer diagnostic, neither local vortex-stretching efficiency nor
a trend as N tends to infinity. Shell operators filter **frequency**;
they are not spatial cutoffs. A sampled quotient increasing with N
does not contradict PR #23's analytically uniform constant.

Reject any merged README, release text, or Master Record language
asserting that these finite tests prove phase muting, establish a
favorable commutator sign, exclude every termwise proof strategy, or
solve arbitrary-data global regularity. The sufficient one-sided
space-time inequality in #24–26 is unproved. Under a moving radius,
`∫σ'Z` needs an additional estimate. The singular `σ'~t^(−1/2)` is
locally integrable and does not itself mean a physical or analytic
breakdown; the naive Young bound produces the troublesome `1/t`.

## 4. Decision record

Merge only after the code executes from the documented checkout, the
math symbols and signs pass the checks above, and the prose retains
the stated scope. If a check fails, leave the affected PR in draft and
record the failed command, exact discrepancy, and the corrective
commit. The status references in #26 have been refreshed with the two merge
commits. Recheck them against GitHub immediately before its merge. Preserve the original v0.1 Master Record numbers and its
historical WP1–10 scope.
