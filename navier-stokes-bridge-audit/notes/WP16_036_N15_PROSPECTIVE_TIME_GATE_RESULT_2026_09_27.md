# WP16 N15 prospective K36 time-gate result (2026-09-27)

Prince Upadhyay, Independent Research

## Freeze and artifact provenance

The N15 hypotheses, search schedule, thresholds, time grid, and failure rules were frozen in `WP16_036_N15_PROSPECTIVE_FREEZE_2026_09_26.md` and merged in PR #90 before N15 data generation. The K36 ordered source-orbit keys are those selected from N11; no N15 retuning was applied.

| artifact | SHA-256 |
|---|---|
| N14 predecessor | `747dfb0bd0ea12271bd53b39fae7a4e18f396656bed3084bd4c632a9f3e5a3d9` |
| frozen K36 source JSON | `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e` |
| N15 atomic checkpoint | `2ad24749a9454c5377e627c103a7d8dd5f1701876958a4bc9c095e1fa222c4a6` |
| N15 continuation | `c0bd97f554df3e8561d75e1ba62356d04200fbe4986f573e3305a98932ccb225` |
| N15 frozen time gate | `e1a9d0d59b56375e2adf31098c97fcb71336d41ffa2e6098dfec744264a7d239` |

The checkpoint has completed trial 520 and its best phase vector and accepted-improvement records agree with the continuation. The time-gate JSON internally records the N14, N15, and K36 source hashes above. The checkpoint, full continuation, and full time trace were supplied separately; the compact checked summary in `results/wp16_n15_holdout/wp16_036_N15_result_summary.json` records their provenance and outcomes.

## Frozen continuation result

At N=15, seed 20260940, search grid 48, the 520-proposal search used 6,791 active conjugate pairs (5,638 inherited, 1,153 newly available). The winner's objective was `9.9109238004012` at grid 48. Fixed-phase refinement gave:

| grid | C_infinity_stretch |
|---:|---:|
| 48 | 9.9109238004012 |
| 64 | 9.910944916518424 |
| 96 | 9.911712653704301 |
| 128 | 9.911923711291015 |

The range is about 0.0101% of the grid-128 value. This is a fixed-state quadrature check and does not certify a global phase optimum or cutoff convergence.

## Preregistered time-gate outcome

The evaluator used viscosity 0.1, `dt=0.0001`, 30 steps through time 0.0030 after the anchor, mass fraction at least 0.90, same sign, and signed share in [0.8, 1.2]. All six stored boolean outcomes passed in every state: static criterion, mass persistence through 0.0010, exit in the frozen [0.0015, 0.0030] window, signed criterion at exit, positive initial margin rate, and negative full/radial-magnitude/vector-polarization rates at exit. The first failure of the complete consistency criterion is the mass criterion, at sample index 23 in all three states.

| state | first sampled mass exit | mass fraction at exit | signed share at exit | initial full dF/dt | exit full dF/dt |
|---|---:|---:|---:|---:|---:|
| inherited | 0.0023 | 0.8997898991761898 | 0.9156172047336606 | +102686.206236 | -377468.550300 |
| target_only | 0.0023 | 0.8997898991897335 | 0.9156172047189142 | +102686.206191 | -377468.550164 |
| full_final | 0.0023 | 0.8985000952027818 | 0.9067594375957017 | +279193.463263 | -406209.327025 |

At exit, radial-magnitude and vector-polarization rates are respectively `(-250880.403, -299061.795)`, `(-250880.403, -299061.795)`, and `(-216380.097, -305819.716)` for inherited, target_only, and full_final. Scalar-phase rates remain positive (`+172473.647`, `+172473.648`, `+115990.487`). These are local rate decompositions, not a sign theorem for all trajectories.

### Half-step crossing check

| state | fraction at 0.00225 | fraction at 0.00230 | coarse/half difference at 0.00230 |
|---|---:|---:|---:|
| inherited | 0.9012535913771097 | 0.8997898998214954 | 6.453055867439161e-10 |
| target_only | 0.9012535913898794 | 0.8997898998350387 | 6.453051426547063e-10 |
| full_final | 0.9001970380307064 | 0.8985000953949837 | 1.922018100231071e-10 |

The half-step samples bracket 0.90 on [0.00225, 0.00230]. They do not provide a rigorous continuous crossing-time enclosure.

## Claim boundary and next freeze

The N11-derived K36 mechanism prospectively reproduced the predeclared finite-Galerkin pattern at N14 and N15: short persistence, first sampled 90% mass exit at 0.0023, signed consistency at exit, and the declared local rate signs. The N14/N15 agreement is not an all-N theorem, a continuum-limit result, a phase global-optimum certificate, or a proof of Navier–Stokes regularity or blowup. N16 is frozen separately before generating its state or score; see `WP16_036_N16_PROSPECTIVE_FREEZE_2026_09_27.md`.
