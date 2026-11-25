# DesignLab and PSI mirror reconciliation

**Date:** 26 November 2026
**Umbrella repository:** `reggaesharkk/Reggae-shark-universe-`
**Purpose:** Record which source commits and artifacts were mirrored and how the local evidence was reconciled.

The Umbrella stores submodule pointers. Each specialist repository remains the authoritative source for its files, data, and history; this update does not flatten either source repository into the Umbrella.

## DesignLab v9 differential

- Source: `reggaesharkk/self-referential-processing-designlab`, branch `v9-0-prospective-runner`, commit `7df10e4fdac6c258c5b51258c6cc9b3620b6c049`.
- The commit adds the prior live Pilot B receipt and updates the v9 OpenRouter routing, one-to-one model rate card, bounded style-scrub repair, documentation, and receipt manifest.
- The changed paths are confined to `research/v9_0_prospective/`. Frozen v8.6.3 paths and `items_pool_v1.json` were not changed or committed.
- The local Colab bundle is `D:\v9_0_colab_pilot_bundle.zip`, SHA-256 `0be63f216f3496c2f4a1efc12397aa45e13e2c362eddb47937edbe78488b0035`. It includes the verified pool, one-code-cell notebook, updated runner files, and receipt provenance. The bundle scan found zero credential-shaped matches.
- The archived receipt is SHA-256 `db82e60bf1aaffa3ecd76909c34aa1a90160224d5e2b5f8f6b3afb346fcdcfc3`, copied from source ZIP SHA-256 `7d0d9103e112288137bd52cc315f0560b0f20df45c23e70cb2140e888902b4a7`.
- That earlier Pilot B receipt records 10 HTTP calls started, 10 HTTP responses, and USD `0.00053603` estimated spend. It is explicitly prospective Pilot B; confirmatory data collected is `false`. Confirmatory study runs remain at 0.
- The script changes were checked offline against the verified 260-item pool. No new provider API requests were sent during this reconciliation.

## PSI v5 work

- Source: `reggaesharkk/psi-self-modeling-benchmark`, branch `main`, commit `70abb1ae17dfa55b59ce8d8f99e75c5e485cdc85`.
- This published commit contains the v5.0 VRK-aligned update and `vrk_live_results/` artifacts. The local `Downloads\_psi_github_push` checkout matched its `origin/main` commit.
- Twelve non-manifest files in `psi_self_modeling_benchmark_v5_sync (1).zip` were compared byte-for-byte with that published checkout; all 12 matched. Four files in `psi_benchmark_v5_LIVE_artifacts.zip` were also compared and all four matched. These were already on GitHub; the Umbrella PSI submodule pointer was simply behind.
- The Umbrella's previous PSI pointer was `3c76eea6b0d64e11f9e7bc18eeb8f69e87f0e1cf`. It now pins `70abb1ae17dfa55b59ce8d8f99e75c5e485cdc85`. No PSI source files or results were edited during this update.

## Umbrella changes

The Umbrella `main` update advances the DesignLab and PSI submodule pointers and refreshes `SPECIALIST_REPOSITORIES.md`, `docs/REPO_MIRROR_INDEX.md`, and the SHA-256 manifest. The PSI project boundary remains diagnostic; it does not establish consciousness or general self-awareness. This document records provenance only and makes no additional scientific claim.
