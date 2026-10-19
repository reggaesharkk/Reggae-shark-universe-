# Work Package 8 v0.2 correction — FFT frequency indexing

**24 September 2026.** During the Work Package 9 verification, a
shared helper was found to cast floating FFT frequencies directly to
integers. On a 96-point grid, a nominal frequency 7 can be represented
as `6.999999999999999` and cast to 6. The helper now uses
`np.rint(np.fft.fftfreq(M)*M).astype(int)` before computing the
pressure and residual frequencies.

The Work Package 8 localized energy calculation and its 64³/96³
comparison were rerun with this fix. The reported values and closure
statistics remain unchanged to the displayed precision. The v0.2
bundle contains the corrected executable and regenerated JSON. This
is a reproducibility correction, not a new mathematical conclusion.
