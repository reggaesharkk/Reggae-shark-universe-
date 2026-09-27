# Navier–Stokes bridge audit: N16 result status (27 September 2026)

The finite WP16 phase-only cutoff program now has a prospectively frozen N16 result. The N16 protocol was merged before any N16 scientific data was generated; the completed continuation used seed `20260941`, search grid 64, and 520/520 proposals. Its fixed-phase quotient refined to `10.150097983229115` on grid 128. The N11-derived K36 coalition and frozen gate were carried forward without retuning.

All three N16 states pass the predeclared static, early persistence, exit-window, signed-share, and local margin-rate sign tests. The inherited and target-only states first fall below the 90% absolute-mass threshold at sampled time `0.0023`. The optimized full-final state first falls below it at `0.0024`, within the frozen `[0.0015, 0.0030]` exit window. Its half-step sample at `0.00235` is already below 90%, while the coarse `0.00230` sample passes. Thus the stronger descriptive N14/N15 coincidence of all three exits at exactly `0.0023` does not repeat at N16.

The time-gate JSON SHA-256 is `111eb0407c60cb60c24c57e3c471ece05a9e1b94b88628a688d015a4249decf7`; the N16 continuation SHA-256 is `53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca`. See the [full N16 result](WP16_036_N16_PROSPECTIVE_TIME_GATE_RESULT_2026_09_27.md) and [compact result summary](wp16_036_N16_result_summary.json). The [earlier N16 freeze](WP16_036_N16_PROSPECTIVE_FREEZE_2026_09_27.md) and [pre-data status](CURRENT_STATUS_2026_09_27.md) remain historical records.

These are finite Fourier-Galerkin observations. They establish neither an all-cutoff theorem nor a continuum regularity or blow-up result.
