# WP19 Recovery Checkpoint — v0.27a

**Author:** Prince Upadhyay, Independent Research  
**Frozen at:** 2026-09-30  
**Purpose:** durable restart point after the v0.27a interval terminal-gradient gate. This file is a state ledger, not a new mathematical claim.

## Repository state

- repository: `reggaesharkk/navier-stokes-bridge-audit`
- branch: `wp19-v0.27-terminal-gradient-arb`
- certified source commit before this ledger: `8274cefc0332a049bcdf56646109d3021504cf14`
- workflow run: `36735640067`
- workflow conclusion: **success**
- workflow: `.github/workflows/wp19_v0_27a_terminal_gradient_arb.yml`

## Frozen scientific inputs

- finite Galerkin datum: unchanged
- viscosity: `nu = 0.1`
- endpoint: `T = 0.003`
- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 key SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- prospective N13 K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- portable C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`
- historical N11 predictor byte SHA-256: `b70bf7f7fe85a8c073c02c80e54e1f10d0642f5d030dfe569470c5970ebdda29`

No datum, sign, key, rank, coalition member, or target functional may be retuned in later v0.27 gates.

## v0.26 prerequisite

Run `36734129400`, commit `70b6645e212f80d3461359b285bb19984f7e6ff0`, completed successfully on `main`.

Aggregate status:

`PASS PRE-INTERVAL SIGNED-NUMERATOR DESIGN GATE`

Maximum observed/scout quantities from `results/wp19_bridge/WP19_v0_26_SUMMARY.json`:

- max actual positive transfer / base certified margin: `0.04242008674259059`
- max floating total remainder / base certified margin: `6.79943091515744e-06`
- max conservative nonlinear-radius scout / base certified margin: `0.05077545236647035`
- max scout total budget / base certified margin: `0.09320427500431665`

These are design/scout values except where separately certified.

## v0.27a result

All jobs passed:

- `prepare-c500`
- `gradient (14)`
- `gradient (15)`
- `gradient (16)`
- `gradient (17)`
- `aggregate`

The fail-closed terminal-gradient certificate check passed for all four transitions:

- 14 -> 15
- 15 -> 16
- 16 -> 17
- 17 -> 18

Meaning: the fixed nominal terminal gradient of the signed-C500 polynomial is independently enclosed with 192-bit Arb arithmetic and agrees with the independent floating implementation at the certified nominal endpoint.

It does **not** yet enclose terminal-gradient variation over state uncertainty, backward adjoint propagation, quadrature, endpoint Taylor remainder, or dynamic nonlinear remainder.

## Workflow artifacts

- aggregate `wp19-v0-27a-terminal-gradient-arb`
  - artifact id: `11106234189`
  - ZIP digest: `sha256:3e611b7aab3d146bed1d2037d9ffd1eb96a3e90fb7b6076ecee23ed54652339c`
- frozen C500
  - artifact id: `11107306881`
  - ZIP digest: `sha256:893db000c2a9dce5abf47666732250c4b9b18f71b2027397cf07b940ed2f0eb6`
- M14
  - artifact id: `11105889400`
  - digest: `sha256:00751f8badf6d07034057e5117c21d6b21b22e04304c4ecd2bb264f376f285f3`
- M15
  - artifact id: `11107037236`
  - digest: `sha256:51fe9ad9f41c6f8a17872c06b75db3ee7c8e22eb1dd26e3a2b8ae3d89163af76`
- M16
  - artifact id: `11106093799`
  - digest: `sha256:e7ce1bb98d3203549090337774a23336379df18180f65eb3c617d9831e13de57`
- M17
  - artifact id: `11107775424`
  - digest: `sha256:9017551c68bcee96b322759a3d207411584a14ca79cd1c3990e2357bd418ce65`

## Next proof gates — fixed order

The continuation is fail-closed and incremental:

1. **v0.27b:** certify terminal-gradient variation over the certified endpoint uncertainty ball, or derive a rigorous local Hessian/Lipschitz enclosure sufficient to convert the point terminal gradient into a terminal set.
2. **v0.27c:** rigorously propagate the adjoint backward along the lower-cutoff certified reconstruction.
3. **v0.27d:** rigorously enclose the dual quadrature for the consecutive-cutoff forcing/residual.
4. **v0.27e:** certify endpoint Taylor and dynamic nonlinear remainders.
5. **v0.27f:** combine only certified pieces against the already certified negative signed-numerator margin; keep the normalizer as a separate positivity gate.

No later gate may silently replace a failed bound by a floating estimate.

## Claim boundary

This checkpoint records a finite-Galerkin proof program. It is not an all-N persistence theorem and not a continuum Navier–Stokes regularity or blowup claim.
