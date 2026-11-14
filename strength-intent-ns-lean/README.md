# STRENGTH B3 — research prototype

**Status:** experimental Python/NumPy and C++ code. This is not a deployable network firewall.

I use STRENGTH to explore multiscale recurrent state and intervention ideas. The public source supports a narrower description than the earlier repository page did. This README maps each claim to the code that is actually present and separates synthetic checks from model or security evidence.

## Start with the implementation

The main prototype is [`b3_temporal_bottleneck.py`](b3_temporal_bottleneck.py). It initializes a seeded 32-dimensional NumPy layer by default, splits its state into fast and slow blocks, and computes one caller-supplied forward step. The slow matrix starts as an identity matrix; the layer still applies `tanh`, input projection, and caller-provided `xi_t`. The file contains no training loop, trained checkpoint, packet capture, socket processing, or firewall integration.

Other files:

- [`h4_leakage_guard.py`](h4_leakage_guard.py) shuffles 100 integer IDs by default and returns an 80/20 partition. It does not measure information gain, fit a model, detect feature leakage, or validate a real dataset.
- [`test_pipeline_reproducibility.py`](test_pipeline_reproducibility.py) calculates synthetic fast/slow sequences and a synthetic block-coupling ratio. These toy values are not measurements from B3 training or network traffic.
- [`strength_ns_engine.py`](strength_ns_engine.py) checks two configured scalar limits using Python binary64 arithmetic. Its SHA-256 output is an unkeyed integrity digest, not a signature, authentication token, or IntentSeal authorization.
- [`master_pipeline_audit.py`](master_pipeline_audit.py) hashes a static JSON configuration. It does not run Lean, the B3 model, or a cryptographic signer.
- [`b3_hardware_accelerator.cpp`](b3_hardware_accelerator.cpp) is a bounded-dimension C ABI implementation of the same toy forward pass. It is ordinary C++ code; the repository does not provide hardware/NPU execution evidence.
- [`TitanInterceptor.lean`](TitanInterceptor.lean) proves two elementary inequalities under their stated assumptions. The Lean terms are not connected to the Python or C++ runtime.

## Current evidence boundary

The public source does not substantiate the previous claims of exact-zero gradient leakage, a `+59.9168%` H4 information-gain premium, an empirically validated 50% adversarial prediction floor, hardware validation, or a production firewall. The H2 and H4 examples in [SharkByte](https://github.com/reggaesharkk/SharkByte/tree/main/examples/research) are explicitly synthetic arithmetic and split-integrity demonstrations; they do not run this model.

No trained weights, evaluated dataset, prospective holdout result, latency profile, or live network interception result is published in this repository. This statement describes only this public source tree; it does not assert that no separate research runs exist. Results from outside this tree are not reproduced by this source, and H4 remains an open research question.

## Reproduce the toy check

With Python and NumPy installed, run:

```bash
python test_pipeline_reproducibility.py
```

This only reruns the synthetic calculations described above. A passing assertion would confirm those toy relationships for that run; it would not validate B3, H2, H4, or a security claim.

## Evidence gates for the next release

1. Freeze a documented dataset, labels, split protocol, seeds, and baseline before evaluating H4.
2. Implement the H2 intervention in the actual model and compare it against a no-intervention control.
3. Publish the training code, parameter provenance, metrics, and an independently reproducible evaluation before describing the model as trained or effective.
4. Measure ARM64 performance and review memory, pointer, and threat-model boundaries before discussing deployment.

## Rights

The repository's existing [`LICENSE.md`](LICENSE.md) governs use of this source. The historical `STRENGTH-INTENT-NS-LEAN-v5.0.0-Omega-Release.zip` is retained unchanged; it is not a substitute for the current source notes or evidence described here.

