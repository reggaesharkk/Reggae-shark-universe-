# WP16 N16 exit mechanism: outside-K36 suppression

Prince Upadhyay, Independent Research — post-hoc analysis, 27 September 2026

## Provenance and question

This analysis uses the frozen N16 time-gate JSON, SHA-256
`111eb0407c60cb60c24c57e3c471ece05a9e1b94b88628a688d015a4249decf7`.
The protocol was frozen in PR #91; the result was recorded in PR #92. The present
accounting was designed **after** seeing the N16 result. It is a mechanism
diagnostic, not another prospective holdout or a change to the frozen gate.

The N14 and N15 optimized `full_final` states first failed the sampled 90% K36
mass gate at `t=0.0023`. At N16, `inherited` and `target_only` again first fail
at `0.0023`, but `full_final` remains above 90% at that sample and first fails
at `0.0024`. Which measured term gives it the extra sampled step?

Run the independent, low-memory arithmetic audit on the original JSON:

```bash
python src/wp16_036_N16_exit_accounting.py \
  --time-gate wp16_036_N16_frozen_time_gate.json \
  --output wp16_036_N16_exit_accounting_reproduced.json
```

The script requires the input's exact byte hash, checks all 31 stored samples
per state against the mass and margin identities, checks first failure indices,
and emits `results/wp16_n16_holdout/wp16_036_N16_exit_accounting.json`. The
full time-gate JSON is retained in the supplied results folder; this repository
holds its checked summary and the present derived output.

## Exact accounting, with a defined proof boundary

Write `I(t)` for the sum of absolute **normalized, grouped channel**
contributions in the frozen K36 coalition and `O(t)` for those outside it.
These are diagnostic masses of the chosen tracked channel, not physical
enstrophy or energy. For `I+O>0`, the frozen criterion is

`m=I/(I+O)>=0.9` if and only if `F=I-9O>=0`.

For two trajectories `f=full_final` and `h=inherited`, the exact comparison is

`F_f-F_h=(I_f-I_h)-9(O_f-O_h)`.

Thus a reduction in outside mass by more than one ninth of any inside mass
deficit gives `full_final` a positive margin advantage. At a differentiable
time with `I,O>0`, the log-odds identity is

`d/dt log(I/O) = I'/I - O'/O`.

This identifies a possible dynamic target: control relative outside growth
against inside growth. It supplies **no** a priori bound on either term. The
group absolute values may have kinks; the time-gate's finite samples cannot
certify a continuous-time derivative or crossing. The prior exact ordered-source
rate bound remains conditional on higher norms and a nonvanishing tracked
normalizer; it is too loose to explain this observed persistence.

## Observed N16 turnover

| state | first negative `F` secant | sampled `F` peak | first sampled mass exit |
|---|---:|---:|---:|
| inherited | 0.0007 → 0.0008 | 474.849394 at 0.0007 | 0.0023 |
| target_only | 0.0007 → 0.0008 | 474.579958 at 0.0007 | 0.0023 |
| full_final | 0.0006 → 0.0007 | 441.952104 at 0.0006 | 0.0024 |

The optimized state turns down *earlier* and peaks lower. Its later exit does
not arise from a higher initial margin or a delayed first turnover. The first
sample where its outside mass is lower than inherited, and its margin is
higher, is index 11 (`t=0.0011`). The earlier, independently recorded local
rates also change sign between the anchor and exit, but their exact turnover
time is not determined by this sample audit.

| time | `I_f-I_h` | `O_f-O_h` | `-9(O_f-O_h)` | `F_f-F_h` |
|---:|---:|---:|---:|---:|
| 0 | -1.621783 | +1.691719 | -15.225469 | -16.847252 |
| 0.0010 | -6.222522 | +1.118646 | -10.067817 | -16.290339 |
| 0.0011 | -5.821589 | -0.664375 | +5.979375 | +0.157786 |
| 0.0020 | -18.478536 | -3.456491 | +31.108421 | +12.629885 |
| **0.0023** | **-16.951556** | **-4.445196** | **+40.006767** | **+23.055211** |
| 0.0024 | -19.288198 | -4.906747 | +44.160720 | +24.872522 |

At `0.0023`, inherited has `F=-17.592419` while `full_final` has
`F=+5.462793`. The latter has **less** inside mass (`1047.793826` versus
`1064.745382`). Its outside mass is lower by `4.445196`, which contributes
`+40.006767` to the margin and outweighs the inside deficit of `16.951556`.
This exact decomposition explains the different sampled gate outcomes at that
time. The `full_final` margin falls to `-31.622102` at `0.0024`.

At the full-final exit step `0.0023 → 0.0024`, inside mass drops `14.809453`
and outside mass rises `2.475049`, so `F` falls `37.084895`. These are
differences of stored samples, not rigorous instantaneous velocities. The
half-step result narrows the sampled full-final bracket to a passing coarse
row at `0.00230` and a failing half-step row at `0.00235`; both saved half-step
rows fail.

## Next falsifiable mechanism question

The measured advantage lies in the **outside-K36 normalized group mass**, not
the absolute inside mass. An explanatory model should predict which omitted
source-orbit groups produce the `4.445196` reduction at `0.0023`, and whether
their signed/radial/polarization rates predict its onset near `0.0011`. This
requires state reconstruction and groupwise attribution; the aggregate JSON
cannot identify those groups. Such a model must be tested on untouched data
after its rules are frozen. The present result establishes no all-cutoff
persistence, cutoff-uniform space-time inequality, or PDE regularity claim.
