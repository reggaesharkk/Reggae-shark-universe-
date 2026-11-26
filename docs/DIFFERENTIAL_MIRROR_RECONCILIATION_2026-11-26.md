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


## DesignLab run 4 and v9 stabilization

- I advanced reggaesharkk/self-referential-processing-designlab on main and v9-0-prospective-runner to commit 914b4a685db1064f4686ee8da14612ef3774fae7.
- I archived the run 4 source ZIP at SHA-256 50618f7279799d08f562490455f261bd024094617b72f95ca9d37f799f116f1b and its receipt at SHA-256 32a7b3323613f2ac99ee80791916b5b124093a28ad6048b8966e34221e2b7c74. The receipt records 70 HTTP 200 responses and USD 0.00350597 estimated spend. Gemma and Mistral each completed all 25 item-stage pairs; Qwen and Llama each completed 2.
- My cumulative DesignLab record contains four prospective Pilot B runs, 190 calls, 190 responses, and USD 0.01018135 estimated spend. I count 10 engineering connectivity POST probes separately. Pilot A runs remain at 0 and confirmatory study runs remain at 0. Including three catalog metadata GETs, the saved DesignLab evidence contains 203 provider HTTP requests. Across DesignLab and PSI, I document five live experimental executions (four Pilot B plus one PSI); PSI's exact external request count remains unknown.
- I updated the shared style scrubber to use Gemma for Qwen, Llama, and Mistral outputs, and Mistral for Gemma outputs. Fallback to Mistral is enabled only for Qwen and Llama, so no model scrubs its own tested output. The runner retries HTTP 429/503 up to three times with 2/4/8-second backoff and 0.35-second minimum spacing. It accepts 5, 50, or 260 items; the evaluation stages remain locked at 16 tokens.
- I ran 9 offline unit checks, Python compilation, notebook syntax validation, and 5/50/260-item dry runs. I sent no provider requests during this update. The frozen v8.6.3 files and the 75,875-byte item pool were not changed.
- I rebuilt D:\v9_0_colab_pilot_bundle.zip at SHA-256 6109cf147c3b7967c1aa178586d044c4e5caae44ca90cf7d3e65bc9dba05c2d4 (165,559 bytes, 46 ZIP members). The bundle retains the verified item-pool SHA-256 128ff78bb6beb1640fa51897ab97dbb9d07dc56de276973d05a48dda524b53d3, has one notebook code cell, verifies its eight-file source manifest, and had zero credential-shaped matches in the recursive ZIP scan.
- I preserved the replaced bundle at D:\Self_Referential_DesignLab_Audit_2026-11-26\v9_0_colab_pilot_bundle_pre_run4_stabilization_2026-11-26.zip. The separate D: publication record contains the current bundle SHA-256.


## DesignLab run 5 and Pilot A preparation

- I advanced `reggaesharkk/self-referential-processing-designlab` on `main` and `v9-0-prospective-runner` to commit `289f316f903da5f4365aac8a34c11223c4550ca6`. I updated the DesignLab submodule pointer in this repository to the same commit.
- I archived the run 5 source ZIP at measured SHA-256 `44873ec36a8ea48d29a4f98506b0ee9ce7b82af5edf2388f538bcfaf170afe64`. Its `pilot_b_v9_result.json` SHA-256 is `5a7357e69b3a15e853d61df1e94d0f571e4a478907358caf6d2d6d643e0a5149`, matching the supplied receipt digest. It records 127 HTTP 200 Pilot B calls, zero transient retries, and USD `0.00908310` estimated spend. Qwen, Gemma, Llama, and Mistral each completed 25/25 item-stage pairs across `TR_01`–`TR_05`.
- My cumulative Pilot B record now contains five executions, 317 calls, 317 responses, and USD `0.01926445` estimated spend. I classify Pilot A as not yet run and confirmatory study executions as zero.
- I counted the connectivity outputs bundled with runs 2–5 separately: 16 November engineering probes, all HTTP 200. Together with six 27 September probes, I document 22 engineering probes (20 HTTP 200, one HTTP 400, one HTTP 404). I count 339 model-inference POSTs across these engineering probes and Pilot B receipts; three catalog metadata GETs bring the saved DesignLab provider-request total to 342. I do not have provider-side account logs.
- I prepared `pilot_a_v9.py` and `DesignLab_v9_0_Colab_PilotA.ipynb` for the first 50 verified items, classified as `prospective_pilot_a_not_confirmatory_study`, with `confirmatory_data_collected: false` and a USD `0.50` pre-request cap. Based on run 5's observed rate, the 50-item planning estimate is USD `0.090831`; this is not a guaranteed cost. I ran offline checks only, so Pilot A remains at zero executions.
- I rebuilt `D:\v9_0_colab_pilot_a_bundle.zip` at SHA-256 `2b8133a422851af4285fc282ab4d863f1acda0031ae050fb5112af0506c227ef` and synchronized `D:\v9_0_colab_pilot_b_bundle.zip` at SHA-256 `8563de264762681a407be0c5d8d7ae8c174ccd7516e47a0e4261bb7c13f78c92`. Each ZIP has 59 members, includes the verified 75,875-byte item pool at SHA-256 `128ff78bb6beb1640fa51897ab97dbb9d07dc56de276973d05a48dda524b53d3`, and had zero credential-pattern matches.
- I ran 11 offline unit checks, Python compilation, one-code-cell notebook compilation, and 5/50-item dry runs. I sent no provider requests, read or logged no API key, and modified no frozen v8.6.3 files or item-pool bytes while preparing this update.
