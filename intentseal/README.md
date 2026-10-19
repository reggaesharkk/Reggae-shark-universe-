# IntentSeal Verification Kernel — Frozen Prototype Lineage

**Frozen prototype lineage:** v0.1.1 → v0.2.0 → v0.3.0 → v0.4.0 → v0.5.0  
**Freeze date:** 2026-09-28  
**Author:** Prince Upadhyay, Independent Research

**IntentSeal** is the public name of the research prototype previously developed under the working title **AgentOS Verification Kernel**. The five historical release ZIPs are preserved byte-for-byte under their original filenames so their provenance and hashes remain intact.

IntentSeal explores a narrow security question: how to let an untrusted or prompt-injected agent propose privileged tool actions while keeping authorization, budget, review, provenance attestation, and audit enforcement outside the agent's claimed identity.

It is a research prototype, not a production security boundary.

## Frozen lineage

| Historical release | Fresh Linux verification | Main milestone |
|---|---:|---|
| v0.1.1 | 10/10 | atomic policy/budget enforcement and keyed audit chain |
| v0.2.0 | 14/14 | authenticated loopback service |
| v0.3.0 | 34/34 | review workflow, audited rejection paths, timeout/schema hardening |
| v0.4.0 | 47/47 | agent identity separated from trusted provenance by exact attestation |
| v0.5.0 | 61/61 | usable consent lifecycle, trusted-side request IDs, scoped attesters, audited timing, rate limiting, restart fault tests |

The archived source/package names inside the historical releases still use `AgentOS` / `agentos_kernel`. They are intentionally unchanged.

## Frozen public archive

`IntentSeal_Verification_Kernel_Prototype_Lineage_v0_1_1_to_v0_5_0 (1).zip`

SHA-256:

`05ba923c90dfc481a70a3784b72d1cd71a0adeac2c34a22631169f545ae5d4c0`

Size: 161324 bytes.

## Historical release hashes

- v0.1.1 — `9766417faa5f63ff97bfbcf312b2c286c8cf497f1809a002a633e3bd09983662`
- v0.2.0 — `dbf73e7618747b4681fdd20f46f5601527d45a154d250bd07477ed2143ef2f77`
- v0.3.0 — `6174d62d96557916c9eeff3cfb1f2b3659eb16085dd72c59cd726c8569c7636d`
- v0.4.0 — `78cd8b1409a68a8f1d7c425ce7a272f8319ce1a7719271e7904b14eb83f87db2`
- v0.5.0 — `cde3e9ea62598f883912d8cc52f8aaf9f2d265dff4b863a687c59936f64df138`

## Freeze rule

The five historical release ZIPs are immutable. Corrections after this archive must be additive or receive a new semantic version. Renaming the public archive to IntentSeal does not rewrite the historical release bytes.

## License and DOI status

The outer archive LICENSE states All Rights Reserved. The historical inner ZIPs retain their own original provenance and are unchanged.

The earlier 148371-byte pre-publication outer archive was superseded; its hash is retained in historical records only.

## DOI status

This package is prepared for a Zenodo **software** deposit under the title:

**IntentSeal Verification Kernel: Frozen Prototype Lineage v0.1.1–v0.5.0**

The frozen v0.1.1–v0.5.0 Verification Kernel archive is now published on Zenodo: [10.5281/zenodo.23016445](https://doi.org/10.5281/zenodo.23016445) ([record](https://zenodo.org/records/23016445)). This DOI applies only to this frozen Verification Kernel lineage.
