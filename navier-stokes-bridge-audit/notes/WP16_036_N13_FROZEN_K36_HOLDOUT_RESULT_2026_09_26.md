# WP16 N13 frozen K36 holdout result (2026-09-26)

The N11-derived ordered source-orbit coalition and three N13 acceptance criteria were committed before N13 data existed in the [pending gate](WP16_036_N13_FROZEN_K36_HOLDOUT_GATE_2026_09_26.md). No coalition member or threshold was changed. Each of the inherited, target-only, and full-final states must have the same k-channel sign, at least 0.90 of the absolute source mass, and signed share in [0.80, 1.20].

| N13 state | Same sign | Absolute mass fraction | Signed share | Gate |
|---|---:|---:|---:|---:|
| inherited | yes | 0.9357313342785715 | 1.0298764382622643 | pass |
| target_only | yes | 0.9395587492958438 | 1.0246809360677684 | pass |
| full_final | yes | 0.9345382166902921 | 1.0259280159186226 | pass |

**Overall: pass in all three states.** N13 had 4,557 active conjugate pairs. The search-grid best was 9.34087392249185; the finest refined C was 9.341290048632342 (grid 96). These are finite-cutoff diagnostics, not a global optimization certificate or an all-N or continuum estimate.

## Recovery and input record

Colab disconnected during the original optimization. The uploaded original checkpoint preserved the last accepted improvement at trial 200. A direct rerun overwrote its Drive pathname with an earlier checkpoint, so the uploaded original copy was restored under a separate filename. The subsequent recovery script continued the frozen RNG proposal schedule from that last durable best state and saved completed-trial checkpoints. The available trial-304 recovery checkpoint and final trial-520 checkpoint are archived. The final N13 JSON records another restart from trial 320 with input checkpoint SHA-256 `6a1bd7493e0dcdd7dcf2c61b5c5345ad15f1aa2027e603d736c23a3c216d25f3`; that intermediate checkpoint was not supplied for this archive. The original checkpoint does not record every evaluated trial at disconnection, so any unsaved candidate evaluations cannot be reconstructed. This is a recovery from durable accepted states, not a claim of a single uninterrupted execution.

The final checkpoint and N13 row have identical best phases, best search-grid evaluation, and accepted-improvement records. Their final accepted improvement is trial 519, and the checkpoint states all 520 proposals were processed. The frozen evaluator hashes the N12 continuation (`ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855`), N11 source ranking (`193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e`), and N13 result (`13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd`). Raw bytes and hashes are in `results/wp16_n13_holdout/`. The N11 source input is archived losslessly under `results/wp16_n12_holdout/`.

Passing this additional finite holdout supports transfer of the frozen descriptive coalition through N13. It does not establish persistence for arbitrary N, a continuum mechanism, or Navier–Stokes regularity.
