# WP16 N14 prospective K36 time-gate result (2026-09-26)

Prince Upadhyay, Independent Research

## Freeze provenance

The N14 hypotheses, thresholds, continuation schedule, time grid, and failure rules were frozen in `WP16_036_K36_RATE_INEQUALITY_AND_N14_FREEZE_2026_09_26.md` before any N14 continuation state or score existed. The same N11-derived K36 ordered source-orbit coalition was retained without retuning.

The completed artifacts supplied after the Windows run have these SHA-256 values:

- N13 continuation: `13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd`
- N14 continuation: `747dfb0bd0ea12271bd53b39fae7a4e18f396656bed3084bd4c632a9f3e5a3d9`
- N14 atomic checkpoint: `1cc7d70b8d974dfa9b8907af56c6ab1571c981d72b84cac8db26fe1bad4eaa6f`
- frozen source decomposition JSON: `193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`
- N14 frozen time-gate result: `9593d606c4a146fc2bcacf2ded3f961e2df80582ca987b864ae994c17c84de87`

The time-gate JSON internally records the same N13, N14, and frozen-source hashes. It used `dt=0.0001`, 30 steps through `t=0.0030`, `nu=0.1`, same-sign, absolute-mass fraction >= 0.90, and signed-share interval [0.80,1.20].

## N14 continuation completion

The frozen CPU continuation completed all 520 proposals with seed `20260939` and search grid 48. The winning phase vector was then evaluated without retuning at the registered refinement grids:

| grid | C_infinity_stretch |
|---:|---:|
| 48 | 9.638517781099937 |
| 64 | 9.63795623848849 |
| 96 | 9.639409099290948 |
| 128 | 9.639582105538732 |

The four-grid spread is about 0.0169% relative to the grid-128 value. This is a numerical consistency check, not a proof of a global optimum.

## Prospective N14 time-gate outcome

All three preregistered N14 states passed all six stored boolean checks.

| state | static gate | mass passes through t=0.0010 | first mass exit | signed gate at exit | initial dF > 0 | exit full/radial/polarization < 0 |
|---|---:|---:|---:|---:|---:|---:|
| inherited | pass | pass | 0.0023 | pass | pass | pass |
| target_only | pass | pass | 0.0023 | pass | pass | pass |
| full_final | pass | pass | 0.0023 | pass | pass | pass |

The first failure of any preregistered consistency criterion was the mass gate at index 23 for all three states; the same-sign and signed-share criteria still passed at that sampled exit.

### Exit values

| state | mass fraction at exit | signed share at exit | F at start | dF/dt at start | F at exit | dF/dt at exit |
|---|---:|---:|---:|---:|---:|---:|
| inherited | 0.8990100657488133 | 0.9175928896243938 | 358.5663398235836 | +122266.14303472161 | -12.400315899480347 | -362236.0725898943 |
| target_only | 0.8990121011658782 | 0.9175823966147850 | 358.57334807944517 | +122262.2251248140 | -12.37727186501229 | -356404.6157976008 |
| full_final | 0.8990775620544299 | 0.9176292439527933 | 342.11809246060136 | +102278.8475552261 | -11.78620750694813 | -386591.4133257320 |

At the first sampled mass exit, the radial-magnitude and vector-polarization components were also negative in every state:

| state | radial-magnitude rate | vector-polarization rate |
|---|---:|---:|
| inherited | -246299.08411952783 | -281253.7558270378 |
| target_only | -246356.34628111802 | -277971.6562713474 |
| full_final | -260566.16566165758 | -296958.89709273615 |

The scalar-phase component remains positive at the exit; therefore the negative total margin velocity is not a statement that every component is negative.

## Half-step crossing validation

The frozen protocol required a half-step check around the first coarse exit. With `dt=0.00005`:

| state | mass fraction at t=0.00225 | mass fraction at t=0.00230 | coarse/half-step difference at 0.00230 |
|---|---:|---:|---:|
| inherited | 0.9004224286735126 | 0.8990100644182566 | 1.330556664846938e-09 |
| target_only | 0.9004245186975955 | 0.8990120999611644 | 1.2047137731840962e-09 |
| full_final | 0.9005717855754409 | 0.8990775624862959 | 4.3186598741584703e-10 |

Thus all three states remain above 0.90 at 0.00225 and are below 0.90 at 0.00230. These are sampled numerical brackets, not rigorously certified continuous crossing times.

## Joint interpretation

The prospective N14 test passed the three predeclared hypotheses in all three states:

1. **Static transfer:** all three initial N14 states satisfy the unchanged frozen K36 criteria.
2. **Transient time pattern:** each state passes the mass gate through t=0.0010, then has its first sampled mass exit at t=0.0023, inside the frozen [0.0015,0.0030] window, while the signed criterion still passes.
3. **Local velocity pattern:** dF/dt is positive initially, while at the first mass exit the full, radial-magnitude, and vector-polarization margin rates are negative.

This is a clean prospective finite-Galerkin replication at N=14. It is not an all-N theorem, not a continuum-limit result, not a global-optimization certificate, and not a proof of Navier-Stokes regularity. The N14 hypotheses themselves were chosen after observing N12/N13; their prospective evidential status applies specifically to the untouched N14 cutoff.
