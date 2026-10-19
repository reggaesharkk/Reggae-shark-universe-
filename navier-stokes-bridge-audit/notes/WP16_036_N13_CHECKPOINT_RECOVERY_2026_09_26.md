# N13 checkpoint recovery after Colab disconnect (2026-09-26)

The original N13 run disconnected after writing a checkpoint whose last accepted record is trial 200 of 520 (new-mode block round 2, zero-based). SHA-256 of the uploaded checkpoint: `c5b301986b1ec86b666f62c57a836effd23e073fe47328ac9a648f2d0ecbfa81`. It reports 4557 active conjugate pairs, 984 new pairs, and best search-grid C=8.84909804599571. No final N13 JSON or K36 holdout existed at this point.

`src/wp16_phase_cutoff_resume_from_checkpoint.py` reconstructs N13 from the frozen N12 input (SHA-256 `ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855`), replays the NumPy RNG draw stream through the checkpoint's last accepted trial without objective evaluations, and continues the unchanged 520-trial proposal schedule. It records recovery provenance in the final row and writes a separate recovery checkpoint after each 8 completed evaluations and at round boundaries. The original checkpoint is preserved. If another disconnect occurs, pass the latest recovery checkpoint as `--resume-checkpoint`.

**Scope:** The checkpoint did not record every evaluated trial or the actual evaluation count when Colab disconnected. Thus this is a deterministic continuation from the last *durable accepted state*, not a claim that all unsaved trials were recovered. It preserves the prospective N13 K36 gate and avoids tuning its thresholds. Evaluate the holdout only after full optimization and refinement finish; do not infer a holdout result from the partial best C.

Run with `--n12-json`, `--resume-checkpoint`, `--output-checkpoint`, and `--output`. Then run `src/wp16_036_N13_frozen_K36_holdout.py` with the completed N13 output and the frozen source JSON.
