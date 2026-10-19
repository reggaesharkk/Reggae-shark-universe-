# N12 fixed-datum cutoff check

The question and pass gates were frozen in `PROTOCOL.md` before the N12 run.
The same exact rational trigonometric datum used for the N11 certificate was
embedded in the N12 Galerkin system by assigning zero to every new mode.
The viscosity, endpoint, observable, ordered K36 keys, and 120-step grid were
kept fixed.

## Result

All 120 Arb whole-segment enclosures were generated, and a separate second
Arb pass recomputed and accepted every one of them. The endpoint and
normalizer evaluation from the saved enclosures gives:

| Gate | Certified value |
| --- | ---: |
| Exact initial observable `F(0)` | `[645.8037741471, 645.8037741472]` |
| Galerkin trajectory error at `T=0.003`, symmetric-strain bound | `<= 0.000011374869` |
| Original full-gradient error bound for comparison | `<= 0.000050798503` |
| True N12 endpoint observable `F(T)` | `[-73.63322101, -70.396895629]` |
| Whole-path K36 normalizer absolute value | `>= 49091.85228719` |

Thus the same fixed datum has a rigorously certified sign crossing at both
N11 and N12. This is evidence at two finite cutoffs. It establishes neither
cutoff-uniform control nor a continuum Navier–Stokes theorem. A zero need not
be unique or occur at the same time at the two cutoffs.

`results/post_audit_replay_20260929/` records the cleaned-up runner's full
replay. It independently recomputed and accepted all 120 segment enclosures,
then completed the trajectory, endpoint, and whole-path normalizer checks in
the same invocation. Its certificate reports
`independent_arb_segment_replay: true`. Earlier receipts remain in
`results/full_run/` and `results/independent_replay_20260929/` as historical
records; use the post-audit receipt for the current source. The updated
endpoint writer labels the raw Arb lower ball and rounded decimal lower bound
separately.

The norm inequality remains valid at zeros of `w`: for `ε>0`, put
`y_ε=(||w||₂²+ε²)^(1/2)`. The energy inequality implies
`y_ε'≤S y_ε+R`, where `S=||S(v)||∞,op` and `R=||r||₂`; integrate this
scalar inequality on each segment and let `ε` decrease to zero. The code's
update `e^(Sh)(E+hR)` bounds the resulting Grönwall expression because
`(e^(Sh)-1)/S≤h e^(Sh)` for `S≥0` (including its limit at `S=0`).

## Reproduce

From the directory containing `vrk-zenodo`, install `numpy==2.3.5` and
`python-flint==0.9.0` in a Python environment, then run:

```bash
python vrk-zenodo/next-work/n12_same_datum/tools/run_n12_certificate.py \
  --output-dir vrk-zenodo/next-work/n12_same_datum/results/full_run \
  --workers 8 --recompute-segments
```

The script checks the witness/key SHA-256, predictor array hashes, all 120
segment input hashes, symmetric-strain error recurrence, exact initial sign,
endpoint Arb interval, and whole-path normalizer bound. The two Arb passes
take substantial CPU time. Rerunning without `--recompute-segments` quickly
rechecks the stored segment digests and final gates but does not regenerate
the Arb enclosures.

The three downloadable ZIPs extract into one `vrk-zenodo` directory: the
source/certificate ZIP contains this note, scripts, frozen witness and keys,
their source dependencies, and all 120 segment enclosures; the other two
contain the predictor node and RHS arrays. Extract all three into the same
parent directory before checking hashes or running the full replay. These
packages were produced without changing the frozen N11 or N17 releases.

From `vrk-zenodo`, check all 250 archived files before replay:

```bash
sha256sum -c next-work/n12_same_datum/SHA256SUMS.txt
```
