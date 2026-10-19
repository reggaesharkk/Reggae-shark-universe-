# Preserved invalid v0.28 pilot output

GitHub Actions run: `36816248131`  
Artifact ZIP SHA-256: `2639c2a297be80588a912ef433ed7ae26f03bbcaf48f79fb583d1aad90a28d4c`  
Archived result SHA-256: `f6305bbab871e1c5b006dbc62690de7e106ba75b1d89085ccb2ba262465e18c7`

The independent verifier rejected this output. Exact decimal arithmetic gives:

```text
nominal residual upper                 53884259.691876
primal-uncertainty penalty upper  771116932371.42349
sum of printed component uppers   771170816631.115366
printed total residual upper      771170816631.115284
shortfall                                  0.000082
```

The reported total is below its component bounds. This artifact is invalid and
must not be used as a residual certificate. The archived producer used the
shared decimal formatter, which passes Arb values through binary64; the new
v2 producer replaces that serialization for every bound in this pilot with
integer-only outward rounding from Arb's exact midpoint/radius/exponent
enclosure. The original ZIP files and manifest are retained here unchanged.
