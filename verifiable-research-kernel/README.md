# IntentSeal Verifiable Research Kernel (VRK)

Part of program 06, IntentSeal.

## Current release — v0.3.1

Artifact:

`IntentSeal_Verifiable_Research_Kernel_v0_3_1.zip`

SHA-256:

`c18c4c697d8188490e96530cfb5ddcb2e63f7c65aa560415401b1541e575cd79`

Size: **177,783 bytes**  
ZIP entries: **89**  
Checksum-manifest entries: **88**

Deterministic certificate digest:

`09209816a034020076e0f66e1b8924b6dd1567c95f7159070f58ce62ac597a8f`

The release was replayed twice from the final source tree and once from a fresh extraction of the final ZIP. The canonical deterministic certificate digest matched across all release-path runs.

### Demonstrator 001 — finite LRSC

Finite benchmark: `M=99`, `k_idx=49`, `A=1/2`, `theta=0.07`, relative tolerance `1e-3`.

- VRK state: **CERTIFIED**
- K0..K13 exact coverage: **527,046,644,056 / 527,046,644,056**
- K13 search nodes: **3,432**
- K14 integer interval witness: PASS
- tests: **30/30 PASS**
- claim/evidence mutations: **20/20 rejected**
- release/trust/authority mutations: **13/13 rejected**
- promotion: **EVIDENCE_BOUND -> CERTIFIED**
- certificate-bound dual seal: PASS

Verifier-source trust-root digest:

`f010a99d78b360b8fd5dc9b727f21b898889c6e75e3093cc22d6f04d005a0d0f`

Public anchor commit:

`e3b43046346c91faf2333d18d50c87012c8b162a`

### Demonstrator 002 — finite N11 K36 crossing

Scientific certificate archive SHA-256:

`d29224e1dd4ad9f9454951415a3b080bc9f092839e24caaeddd056013785cfbe`

The optional v0.3.1 package checker returns PASS for the frozen certificate archive, including the checksum inventory, exactly 120 segment-certificate records, theorem gates, and independent exact-Fraction recurrence.

VRK state: **EVIDENCE_BOUND**.

This lower status is deliberate. The external Navier–Stokes project has a completed finite-N11 computer-assisted theorem, but v0.3.1 does not independently regenerate all 120 Arb enclosures and therefore does not silently promote the claim to local `CERTIFIED`.

See [VRK v0.3.1 final audit](VRK_v0_3_1_FINAL_2026_09_28.md).

## Historical releases

- v0.3.0 frozen baseline: `b01178e81b0e0f07c67a883d8e51430f8af0dc608c5246ee925f6c5c17c0b52c`
- v0.1.0 public seed: `ed4a2842e44a2d23785417f2e76054122b0c7da31e30054aa2ea4e3183abc49a`

Historical versions remain unchanged.

## Boundary

`CERTIFIED` is a VRK finite-domain verifier state, not peer review or a universal truth label. The included authority seal is a symmetric HMAC demonstration, not production authorization infrastructure.

No continuum Navier–Stokes theorem or universal physical claim follows from either demonstrator.

No VRK DOI is claimed yet.
