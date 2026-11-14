# STRENGTH public source inventory

**Release label:** v5.0.1
**Scope:** source inventory and implementation notes
**License:** Proprietary Commercial Evaluation License (PCEL-2026)

## What the public files contain

- `b3_temporal_bottleneck.py` defines a seeded NumPy recurrent-layer prototype and one forward pass. It has no training loop or published trained checkpoint.
- `b3_hardware_accelerator.cpp` implements a dimension-guarded C ABI forward-pass helper. It is ordinary C++ source and does not demonstrate hardware acceleration or deployment.
- `h4_leakage_guard.py` makes a seeded random holdout split. It does not measure information gain or validate that a dataset split is independent.
- `test_pipeline_reproducibility.py` computes toy, seeded sequences and a toy block-coupling ratio. Those outputs are not measurements from trained STRENGTH models or network traffic.
- `strength_ns_engine.py` checks configured scalar limits using Python `float` (binary64) arithmetic and emits an unkeyed SHA-256 integrity digest. It does not provide formal verification, authentication, authorization, or sealing.
- `master_pipeline_audit.py` hashes a static configuration only. It does not run Lean, the model, or a runtime pipeline.
- `TitanInterceptor.lean` contains the elementary propositions and proof terms in that file; it is not connected to the Python or C++ code.

## Evidence and limits

This source inventory does not establish exact-zero gradient leakage, an H2 reset efficacy result, an H4 predictive premium, hardware validation, a production firewall, or a Navier–Stokes theorem. The public source should be read as an experimental prototype. The repository README records the evidence gates for stronger claims.

The archived `STRENGTH-INTENT-NS-LEAN-v5.0.0-Omega-Release.zip` remains a historical artifact. It may contain descriptions that do not match this corrected source inventory; the archive is not the current implementation specification.

