# Public source repositories

**Updated:** 18 November 2026.

This directory pins the **15 public specialist repositories** and the public account profile as Git submodules. The umbrella preserves independent project histories while providing one dated, reproducible source map. Exact commit pins and scope notes are listed in [the public repository map](../docs/REPO_MIRROR_INDEX.md).

## Clone all pinned sources

```sh
git clone --recurse-submodules https://github.com/reggaesharkk/Reggae-shark-universe-.git
```

For an existing clone:

```sh
git submodule update --init --recursive
```

GitHub’s normal ZIP download includes the gitlink records, not submodule contents. Use the recursive clone command to retrieve the pinned sources. Private repositories are excluded.

To retrieve only SharkByte:

```sh
git submodule update --init -- public-repositories/sharkbyte
```
