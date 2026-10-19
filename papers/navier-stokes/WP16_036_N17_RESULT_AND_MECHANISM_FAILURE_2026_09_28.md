# WP16 N17 prospective result: broad gate passes; mechanism gate stops

Prince Upadhyay, Independent Research — 28 September 2026

This is the first result under the complete N17 pre-data freeze merged as PR #98, commit `71fb018aab7e028406698a82e8a8a5bcd87f64c5` (27 September, 10:34 UTC). The three uploaded result inputs were found in the top-level Drive `results` folder. Their source files remain frozen and unchanged. This note records a successful broad K36 test and a **failed or unevaluable separate mechanism test**. It does not rescue or retune the mechanism prediction.

## Inputs and continuation

| File | SHA-256 |
| --- | --- |
| N16 predecessor continuation | `53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca` |
| N17 checkpoint (uploaded) | `f4a8da892f666e2dffa2c02915801870a1be4e4ba2fd357f8f3455760ca08b32` |
| N17 completed continuation (uploaded) | `755a36f966b64c8c44cd468c6f2e8212a7ed64eebeaf8aa795ee2c3197c4c3ec` |
| Expanded N11-derived K36 source JSON | `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e` |

The checkpoint records N17, seed `20260942`, grid 64 (`64 > 3×17`), 9,246 active conjugate pairs = 7,942 inherited + 1,304 new, and `last_processed_trial=520`. The completed result agrees with its checkpoint on all support vectors, best phases, best search score, and 214 saved schedule records. Two records at trial zero are the baseline and inherited states; they are not duplicate proposals. Search-grid `C_infinity_stretch=10.355251314392905`; fixed-winner refinements are `10.356742053923659` at 96 and `10.356696358903514` at 128. The 64-to-128 relative difference is about 0.014%. The N16 fixed-winner score was `10.150097983229115`. Reality and divergence errors of the N17 refined state are below `10^-12`. This is finite search evidence, not a global optimum or continuum bound.

## Broad frozen time gate

The unchanged evaluator `src/wp16_036_N17_time_gate.py` (SHA-256 `6fc3413742f94438ce76fee616f31fe3aba6afc445aff153440cd6fc1f50b952`) was independently executed on the uploaded N17 file, the frozen N16 file, and a source JSON expanded from the archived gzip and checked against the exact frozen hash. The output SHA-256 is `905237d19724ee4535866168dd6ea010f794f070c1befef11b78e8e06ebc4a5b`.

| State | Static | Mass through .001 | First sampled mass exit | Signed at exit | Initial F' positive | Exit full/radial/polarization negative |
| --- | --- | --- | --- | --- | --- | --- |
| inherited | pass | pass | .0024 | pass | pass | pass |
| target_only | pass | pass | .0024 | pass | pass | pass |
| full_final | pass | pass | .0024 | pass | pass | pass |

The last passing mass fractions at `.0023` are respectively `0.9003525861`, `0.9003522714`, and `0.9003208464`; at `.0024` they are `0.8971247842`, `0.8971245033`, and `0.8967448854`. The signed shares at exit are `0.9179688945`, `0.9179669220`, and `0.9243488831`, within the frozen `[0.8,1.2]` interval. Half-step differences at the coarse exit are at most `1.33e-8`. `joint_pass=true`, with an empty `failure_rules` list. The N16 full-final extra step did not recur here: all three N17 states exit at `.0024`. The frozen criterion required an exit window, not an exact time.

## Separate frozen mechanism gate: not passed

The unchanged evaluator `src/wp16_036_N17_mechanism_gate.py` (SHA-256 `df17370a28a4c61442dee29cb0712dac10597bf286cd107e077e3b329a07fbdc`) returned nonzero and wrote its prescribed failure JSON (SHA-256 `64a584b5d2a715b228528bf055a2453460e1ab6d951c19e5342b668eee98b0e8`):

`directional split failed: ((1, 7, 9), (2, 7, 15))`

It stopped before the joint mechanism predictions were completely evaluated. The frozen mechanism outcome is therefore **failed or unevaluable**, not a pass. In a separate post-hoc diagnostic, the named group's signed contribution at inherited `t=.001` was approximately `2.019256e-11`; the `h=2e-8` directional step crosses the absolute-value kink. The frozen split asserted a smooth-sign decomposition for that group and produced a discrepancy of approximately `0.00144669` at this step. This explains the stop but does not change the preregistered outcome.

An explicitly **post-hoc** exploratory run bypassed only that diagnostic assertion to inspect the remainder. It did not alter the frozen evaluator or count as validation. Its observed failure list included the inherited derivative-step spread, all three `t=.001` turnover/rank predictions, the full-final initial-orbit decay prediction, and the `.0023` normalizer prediction. At `.001`, the recurrent orbit had rates about `-8254.5`, `-8254.5`, and `-7071.1` in inherited, target-only, and full-final; it was not the leading positive outside group. At `.0023`, the orbit still had the largest outside decrease between full-final and inherited (`-2.771377`), but the symmetric swap gave numerator `-6.236278` and normalizer `+4.046790`, opposite the frozen normalizer-sign and dominance prediction. These exploratory numbers expose a substantive mechanism miss beyond the numerical kink. They are not a retrospectively repaired holdout.

## Boundary and next analysis

Retain both gate artifacts and the input hashes. Any revised directional-split rule or new orbit hypothesis must be labeled post-hoc for N17 and tested on a later untouched cutoff. The broad gate only describes one finite Galerkin trajectory family; neither its pass nor the mechanism miss proves an all-cutoff result or resolves 3D Navier–Stokes regularity.
