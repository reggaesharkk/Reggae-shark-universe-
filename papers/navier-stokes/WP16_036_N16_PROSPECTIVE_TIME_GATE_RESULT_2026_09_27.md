# WP16 N16 prospective K36 time-gate result (2026-09-27)

Prince Upadhyay, Independent Research

## Prospective boundary and provenance

The N16 search and time-gate rules were frozen and merged in canonical PR #91 (squash commit `cf0666d8f356a7525885b63b0aa131ece032e761`) before any N16 state, score, or checkpoint existed. This audit uses that rule without retuning the N11-derived K36 ordered source-orbit keys, phase objective, seed, schedule, thresholds, time window, or interpretation after seeing N16. The 26 September N14 and 27 September N15 results were known before this N16 freeze.

| artifact | SHA-256 |
|---|---|
| N15 predecessor continuation | `c0bd97f554df3e8561d75e1ba62356d04200fbe4986f573e3305a98932ccb225` |
| frozen K36 source JSON | `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e` |
| N16 checkpoint | `057c5846cc28f86099408f3f7563d7551d64b1f6414758cadeecf1fa99d656ba` |
| N16 continuation | `53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca` |
| N16 frozen time gate | `111eb0407c60cb60c24c57e3c471ece05a9e1b94b88628a688d015a4249decf7` |

The checkpoint and continuation were retrieved from the uploaded Drive results folder; the time-gate JSON was supplied separately. Their byte hashes above were checked. The time-gate JSON internally records the same N15, N16, and frozen-source hashes. The compact checked result is in `results/wp16_n16_holdout/wp16_036_N16_result_summary.json`. The full machine-generated files are retained in the uploaded results folder, rather than committed as large repository artifacts.

## Frozen continuation completed

At N=16, seed 20260941 and alias-safe search grid 64, all 520 proposals completed. The support has 7,973 active conjugate pairs, of which 6,771 are inherited and 1,202 new. The checkpoint best phases, score, and improvement records exactly match the final continuation. The fixed phase winner, with no refinement retuning, scored:

| grid | C_infinity_stretch |
|---:|---:|
| 64 | 10.149314859960093 |
| 96 | 10.15014144419499 |
| 128 | 10.150097983229115 |

This is a quadrature consistency check on one selected finite state, not a global phase-optimum or cutoff-convergence certificate. The stored search winner has reality error `2.66e-16` and divergence error `6.47e-15`.

## Time-gate outcome under the unchanged rules

The frozen gate used `nu=0.1`, `dt=0.0001`, 30 steps through time 0.0030 after the anchor, the 90% grouped absolute-mass threshold, same sign, and signed share in [0.8, 1.2]. All three N16 states passed each of the six stored checks: static gate; mass at every sampled point through 0.0010; first mass exit inside [0.0015, 0.0030]; signed criterion at exit; positive initial full margin velocity; and negative exit full, radial-magnitude, and vector-polarization margin velocities.

| state | first sampled mass exit | mass fraction at exit | signed share at exit | initial full dF/dt | exit full dF/dt |
|---|---:|---:|---:|---:|---:|
| inherited | 0.0023 | 0.8985154141285887 | 0.9075863004743228 | +278501.061251 | -405645.350622 |
| target_only | 0.0023 | 0.8985340354239556 | 0.9075805522356793 | +278340.825849 | -405443.270597 |
| full_final | **0.0024** | 0.8972532948158594 | 0.91810410437316 | +265221.101597 | -365503.272792 |

The first failure of the full consistency criterion is the mass gate at indices 23, 23, and 24 respectively. Same sign and signed share still pass at those samples. At exit, radial-magnitude and vector-polarization rates are negative in all states; scalar-phase rates remain positive (about +120774, +120952, and +91376). This repeats the declared sign structure while retaining the visible change in the full-final sampled exit.

### Half-step check and precise sampling statement

| state | last passing sample used | next failing half-step sample | half-step fraction at failure | coarse/half difference at coarse exit |
|---|---:|---:|---:|---:|
| inherited | 0.00225: 0.900204294643131 | 0.00230 | 0.8985154127057607 | 1.4228279665573496e-09 |
| target_only | 0.00225: 0.9002217183171562 | 0.00230 | 0.898534033985691 | 1.4382646185140402e-09 |
| full_final | 0.00230 coarse: 0.900469470023854 | 0.00235 | 0.8988413518444025 | 1.2301629048749874e-08 |

For `full_final`, the two saved half-step rows are **both below** 0.90: 0.8988413518444025 at 0.00235 and 0.8972532825142303 at 0.00240. The preceding coarse sample at 0.00230 is above 0.90. Thus the sampled bracket supported by the stored coarse and half-step values is [0.00230, 0.00235]; the pair of saved half-step rows alone does not straddle the threshold. It would be incorrect to say that all three states first exit at 0.0023 or that the half-step rows themselves bracket the full-final crossing.

The stored time samples have decreasing energy and reality/divergence errors at roundoff scale. These finite differences and sample brackets are descriptive; no rigorous continuous-time crossing enclosure is certified.

## Joint conclusion and next analytic use

N16 **passes the predeclared broad prospective finite-Galerkin gate**, extending the tested lineage through three time-resolved cutoffs N14–N16. The sharper descriptive coincidence of all three states first exiting at 0.0023, observed at N14 and N15, does **not** repeat: N16 `full_final` exits one coarse sample later. This discrepancy is kept as mechanism data and must not be hidden by changing the frozen window or retroactively imposing an exact-time criterion.

The result neither establishes all-N persistence, continuum convergence, a cutoff-uniform estimate, a global phase optimum, Navier–Stokes regularity, nor finite-time blowup. The next mathematical question is why optimized `full_final` gains an additional sampled step at N16 while inherited and target-only trajectories retain their earlier exit.
