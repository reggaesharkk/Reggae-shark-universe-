# N13 Same-Datum Result — 29 September 2026

The completed N13 certificate extends the same frozen finite-dimensional test used at N11 and N12 to one additional Galerkin cutoff.

- Frozen initial field: 112-pair rational datum, SHA-256 `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- Frozen K36 key file SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- Viscosity: `ν=0.1`; observable: `F=I−9O`; interval: `[0,0.003]`
- N13 initial observable: `[645.8037741471, 645.8037741472]`
- Certified endpoint observable: `[-87.154087422, -83.563901281]`
- Terminal trajectory-error upper bound: `0.000012244529`
- Whole-path normalizer lower bound: `48869.38355689`
- Independently replayed whole-segment Arb enclosures: `120/120`

The report establishes a sign crossing somewhere in `[0,0.003]` at N13. It does not provide a tighter crossing-time interval. With N11 and N12, the report verifies the same-datum crossing at three specified finite Galerkin cutoffs. It does not establish a cutoff-uniform estimate, convergence to a continuum solution, blowup, or global regularity.

- [Full N11–N13 report](N11_to_N13_Same_Datum_Cutoff_Report_2026_09_29.md)
- [Canonical N13 package and machine-readable evidence](https://github.com/reggaesharkk/navier-stokes-bridge-audit/tree/main/next-work/n13_same_datum)
- [N13 release archive](https://github.com/reggaesharkk/navier-stokes-bridge-audit/releases/tag/n13-same-datum-v1) — ZIP SHA-256: `858eeec4a1cb323d23e91ffa9914af823a388a78ecc39c758abea3fcdec9ac5e`
- [Specialist report](https://github.com/reggaesharkk/navier-stokes-bridge-audit/blob/main/notes/N11_to_N13_Same_Datum_Cutoff_Report_2026_09_29.md)
