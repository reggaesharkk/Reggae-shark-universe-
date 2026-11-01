# Public source repositories

**Updated:** 1 November 2026.

I keep the project source in its own GitHub repository and pin each public source here as a submodule. This preserves independent histories while giving the Umbrella one complete, versioned map.

## Clone all pinned sources

```sh
git clone --recurse-submodules https://github.com/reggaesharkk/Reggae-shark-universe-.git
```

For an existing clone:

```sh
git submodule update --init --recursive
```

GitHub’s normal ZIP download includes gitlink records, not the submodule file contents. Use the recursive clone command to retrieve the pinned repositories. Private repositories are intentionally excluded.
