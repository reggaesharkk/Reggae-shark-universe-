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

## Account-local provider activity count

- The September 27 audit evidence records 6 non-study engineering connectivity POST probes (4 HTTP 200, 1 HTTP 400, 1 HTTP 404) and 3 provider catalog GET requests. No `api_ping_check` requests or output were evidenced in that audit snapshot.
- The attached receipt adds one prospective Pilot B run with 10 HTTP calls started and 10 responses. It is a partial run on `TR_01`, with USD `0.00053603` estimated spend. It is not a confirmatory study run.
- Across the retrieved records, that is 16 documented model inference POST calls (6 engineering + 10 Pilot B) and 19 external provider HTTP requests when the 3 metadata GETs are included. Pilot A runs: 0. Confirmatory study runs: 0.
- This is a local-artifact count, not provider-side billing evidence. This update sent no new LLM calls, and provider account/billing logs were not queried.

## PSI v5 work

- Source: `reggaesharkk/psi-self-modeling-benchmark`, branch `main`, commit `70abb1ae17dfa55b59ce8d8f99e75c5e485cdc85`.
- This published commit contains the v5.0 VRK-aligned update and `vrk_live_results/` artifacts. The local `Downloads\_psi_github_push` checkout matched its `origin/main` commit.
- Twelve non-manifest files in `psi_self_modeling_benchmark_v5_sync (1).zip` were compared byte-for-byte with that published checkout; all 12 matched. Four files in `psi_benchmark_v5_LIVE_artifacts.zip` were also compared and all four matched. These were already on GitHub; the Umbrella PSI submodule pointer was simply behind.
- The Umbrella's previous PSI pointer was `3c76eea6b0d64e11f9e7bc18eeb8f69e87f0e1cf`. It now pins `70abb1ae17dfa55b59ce8d8f99e75c5e485cdc85`. No PSI source files or results were edited during this update.

## Umbrella changes

The Umbrella `main` update advances the DesignLab and PSI submodule pointers and refreshes `SPECIALIST_REPOSITORIES.md`, `docs/REPO_MIRROR_INDEX.md`, and the SHA-256 manifest. The PSI project boundary remains diagnostic; it does not establish consciousness or general self-awareness. This document records provenance only and makes no additional scientific claim.


## DesignLab run 3 update

- I advanced `reggaesharkk/self-referential-processing-designlab` on `main` and `v9-0-prospective-runner` to commit `7d04419461ddedd2fe3f4a16664c5b34e3d28caa` and updated the Umbrella submodule pointer to that commit.
- I archived the supplied run 3 source ZIP and its 80-call receipt. The request stated source ZIP SHA-256 `68859768a5bf7ff1f682df2ad54fe938dd28b70b3c66ad4ae692912d59430680`; the supplied bytes hash to `68859768a5bf7ff1f682df2ad54fe938dd28b70b3c66ad4ae692912d59430600`. I preserved the bytes and recorded both values rather than substituting the stated digest.
- The receipt records 80 HTTP 200 responses and USD `0.00494411` estimated spend. Gemma completed 25/25 item-stage pairs across all five items; Llama completed 17/25, including complete pipelines for `TR_01`–`TR_03`. The cumulative DesignLab record now contains three Pilot B executions, 120 calls, and USD `0.00667538` estimated spend. Confirmatory study runs remain at 0.
- I raised style-scrub `max_tokens` to 192 and updated the base and repair prompts to request three plain, neutral sentences totaling strictly 48–52 whitespace-separated words within the 45–55 word window. Phase 1 and Domain 2 evaluation caps remain at 16 tokens.
- I rebuilt `D:\v9_0_colab_pilot_bundle.zip` with 34 members. Its SHA-256 is `a78e6e6541d1fadbb9e523cbc21769186a256674fb11aa7d67aa2c8b23ee0f75`. The 75,875-byte pool retained SHA-256 `128ff78bb6beb1640fa51897ab97dbb9d07dc56de276973d05a48dda524b53d3`; the one-code-cell notebook, manifests, nested archives, and ZIP integrity verified. The credential-shaped scan found zero matches.
- I preserved the prior bundle in the D: audit folder. I made no provider API requests, read or logged no API keys, and modified no frozen v8.6.3 files or item-pool bytes.
