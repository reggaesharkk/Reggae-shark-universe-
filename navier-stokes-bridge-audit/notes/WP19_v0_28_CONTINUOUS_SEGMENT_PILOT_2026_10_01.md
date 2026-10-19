# WP19 v0.28 continuous adjoint segment pilot

Base: merged v0.27c1, `eb58d058fbb39dcb5480690db070297e4e964780`.
No witness, K36, C500, signs, objective, or input trajectory is retuned.

## Frozen pilot

Only M14→15, forward half-step 239/80000→240/80000 (first backward segment).
Arb precision: 192 bits. Inputs: original N14 certificate and exported M14
adjoint, pinned by ZIP SHA-256 and internal predictor/report hashes.

Cubic Hermite polynomials are imported as exact binary64 dyadics, projected
onto the real divergence-free subspace, and convolved by carry-free
space/time polynomial multiplication. The degree-six residual is bounded
on the entire segment by the Bernstein convex hull, not by sampled nodes.
The original decimal predictor's validated radius is augmented by the
continuous discrepancy to the dyadic predictor. The archived conservative
primal recurrence is retained. Terminal gradient uncertainty is recomputed
about this centre; no nominal endpoint is treated as the true trajectory.

The nonlinear VJP uncertainty bound is
`(sqrt(sum |k|²)+(M+1)*sqrt(mode_count))*primal_radius*adjoint_norm`.
The backward logarithmic norm uses the symmetric strain envelope; viscosity
is dissipative in backward time. The independent Decimal checker propagates
one scalar error step. It does not independently recompute the residual.

## v1 serialization failure and v2 correction

Run `36816248131` completed the M14 segment computation but its independent
verifier correctly rejected the output. The printed total residual upper
(`771170816631.115284`) was `0.000082` below the exact sum of its two printed
component uppers (`771170816631.115366`). The full invalid artifact, source,
verifier, log, manifest, and exact failure calculation are preserved under
`results/wp19_v0_28/pilot_invalid_36816248131/`.

The v1 producer serialized Arb values through the shared helper that converts
to binary64 before decimal rounding. v2 replaces that path throughout the
pilot, including its scalar primal-error recurrence, with integer-only
outward decimal rounding from Arb's exact `(mid, radius, exponent)` enclosure.
The v2 self-check includes large-magnitude micro-decimal cases and a rational
`1/3` case. No residual, trajectory, witness, normalizer, or K36 quantity is
retuned. The same M14 half-segment was recomputed with v2; its accepted limited
result is recorded below. No wider claim is made.

## Corrected v2 execution

Run `36818369196` completed successfully in 288.454 seconds. The integer-only
formatter check and independent explicit Fourier temporal-coefficient check
passed; the same frozen input artifacts were retrieved and hash-checked; the
whole-segment Arb calculation completed; and the separate Decimal recurrence
verifier returned `PASS LIMITED PILOT RECURRENCE CHECK`. Its artifact digest is
`sha256:2d69fe0f090a8a82d70f5e2c2c9e431b41804c29bcdbf5a48ae3b9c841a6e268`.
The exact artifact files and manifest are preserved under
`results/wp19_v0_28/pilot_v2_36818369196/`.

The resulting bounds include:

| Quantity | v2 outward upper bound |
| --- | ---: |
| Nominal residual L2 | `53884259.691875` |
| Primal-uncertainty residual penalty | `770976002083.118621` |
| Total residual L2 | `771029886342.810495` |
| Backward logarithmic norm | `1758.617670280` |
| Adjoint polynomial L2 | `4691959667101.257366` |
| True primal radius | `0.000059241340007` |
| Terminal adjoint error | `73244978636.905585` |
| One-segment propagated adjoint error | `74882674993.048618657819149585465296325142145058928574913811532113780128124368218` |

The printed component uppers sum to `771029886342.810496`, one micro-unit
above the separately rounded total. The checker permits at most two units at
the six-decimal output precision for this separate-rounding effect; the
v1 discrepancy was 82 units and remains rejected. This PASS is limited to the
single continuous segment enclosure and its one-step scalar recurrence. The
other 239 M14 segments, other cutoff paths, dual quadrature, nonlinear
remainder, independent normalizer control, and final signed transfer
inequality remain pending. No theorem is promoted.

## Execution and failure preservation

A separate explicit Fourier/time-coefficient check must pass first.
The actual segment computation has a 1800-second limit. Convolution timings,
failed logs, and any atomic segment output are uploaded with a manifest.
A timeout is an unfinished computation, never a certificate PASS.
No automatic 960-segment expansion is authorized by this workflow.

## Pending gates

Complete backward path, rigorous dual quadrature, nonlinear remainder,
normalizer control, and signed observable transfer inequality remain open.
This pilot is not a continuum or all-cutoff result.

## Executed failure and computational repair

Run `36813631740`, source commit `864fe3b61bb76615b379ae675323e63d4915aeae`,
exited 124 at the frozen 1800-second limit. All archive hashes and the
independent coefficient check passed. Input/terminal-gradient preparation
took 5.836 seconds; packing six base polynomials took 793.876 seconds.
Only three of nine convolution groups completed. No segment JSON exists and
no recurrence verifier ran. The failure log is preserved under
`results/wp19_v0_28/pilot_timeout_36813631740/`.

The repair changes coefficient storage only: initialize the highest nonzero
coefficient first and assign the remaining nonzero coefficients in descending
order. Omitted coefficients are exactly zero. The same coefficient balls,
18 multiplication expressions, dyadic imports, 192-bit precision, Bernstein
bound, witness, signs, and time segment remain fixed. This is not the proposed
nine-product algebra rewrite. The independent explicit sum self-check still
passes with the same displayed arithmetic radius. A 793000-degree two-entry
construction took 0.118 seconds locally; this is a packing diagnostic, not a
prediction of full-segment execution time.
