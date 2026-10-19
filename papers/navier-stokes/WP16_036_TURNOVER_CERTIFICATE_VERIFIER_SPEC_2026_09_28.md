# WP16 finite-N11 turnover certificate verifier specification

**Date:** 28 September 2026  
**Status:** pre-publication verifier contract; no crossing certified here

This document freezes the **publication-side contract** for the forthcoming
validated N11 K36 crossing certificate. It is deliberately independent of the
segment generator. A complete certificate package must satisfy this contract
before any theorem wording is promoted from draft to result.

## Fixed public inputs

| object | SHA-256 |
|---|---|
| 112-pair witness | `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624` |
| K36 orbit keys | `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47` |
| exact initial-sign result | `327378d1ba2978a66484f1266d984d240fdfdaf4c5785889a48eb187c9650885` |

Fixed mathematical parameters:

- Galerkin cutoff: `N=11`
- viscosity: `nu=0.1`
- initial support description: 112 nonzero conjugate pairs before evolution
- endpoint time: `T=0.003`
- K36 threshold observable: `F=I-9O`
- exact initial enclosure:
  `[645.8037741471, 645.8037741472]`

## Fail-closed rules

The verifier must return **BLOCKED/FAIL**, never infer missing information, if
any of the following occurs:

- a fixed public hash differs;
- predictor hashes are absent;
- protocol/version identifiers are absent;
- a segment index is missing or duplicated;
- segment time intervals do not form one gap-free ordered cover of
  `[0,0.003]`;
- a segment refers to different predictor/input bytes;
- outward interval endpoints are malformed or reversed;
- the trajectory-error recurrence cannot be replayed;
- the normalizer lower bound is non-positive;
- the endpoint `F` upper bound is non-negative;
- the exact initial `F` lower bound is non-positive;
- stale or incompatible segment artifacts are mixed into the package.

No tolerance-based replacement of a mismatching SHA-256 is allowed.

## Required manifest

The canonical manifest must contain at least:

- schema/protocol version;
- status;
- creation timestamp;
- fixed witness/K36/exact-anchor hashes;
- hashes of both predictor arrays;
- arithmetic implementation and precision;
- `N`, `nu`, `T`;
- declared segment count;
- one record per segment;
- segment start/end times;
- segment artifact SHA-256;
- predictor hashes copied into each segment record;
- certified residual upper bound `R_n`;
- certified gradient upper bound `G_n`;
- accumulated trajectory radius after each segment;
- aggregate final trajectory radius;
- certified normalizer lower bound;
- certified endpoint `F` interval;
- exact initial `F` interval;
- generator hash;
- independent-verifier hash;
- independent-verifier result.

## Segment coverage

Let the segment records be sorted by index. The verifier must require:

`t_0 = 0`

`t_(n+1,start) = t_(n,end)`

`t_final = 0.003`

as exact decimal/rational equality in the exported manifest representation.

The number of records must equal the declared segment count. Every index from
0 through `segment_count-1` must appear exactly once.

## Error recurrence

For segment width `h_n`, certified residual upper bound `R_n`, certified
gradient upper bound `G_n`, and previous trajectory radius `eps_n`, the
verifier must independently recompute an outward upper bound for

`eps_(n+1) <= exp(G_n h_n) eps_n + R_n (exp(G_n h_n)-1)/G_n`

when `G_n>0`, with the continuous `G_n=0` limit `R_n h_n`.

The generator's stored accumulated radius is not authoritative. The verifier
must recompute the recurrence from `eps_0=0` and reject any stored radius that
is smaller than its independently reproduced upper bound.

## Normalizer gate

The package must prove a lower bound

`|z(u(t))| >= z_* > 0`

for every required point/ball used to define the grouped observable. A sampled
numerical value is insufficient.

The final manifest must expose the global certified lower bound and enough
per-segment/endpoint evidence for the independent checker to reproduce the
minimum.

## Endpoint gate

The manifest must contain an outward interval

`F(u(0.003)) in [F_-, F_+]`.

The certificate passes the endpoint gate only if

`F_+ < 0`.

The existing float64 value near `-48.39054` is diagnostic context only and
must never be substituted for this interval.

## Initial gate

The verifier must bind to the existing exact result and require

`645.8037741471 <= F(u(0)) <= 645.8037741472`

with strictly positive lower endpoint.

## Independent-verifier output

The independent verifier should emit a compact JSON result containing:

- fixed-input hash checks;
- predictor hash checks;
- segment count and coverage result;
- recurrence-recomputed terminal radius;
- global normalizer lower bound;
- initial `F` interval;
- endpoint `F` interval;
- final Boolean gates;
- overall status `PASS` only if all gates are true.

## Publication rule

A generator success message is not sufficient.

The crossing theorem may be published only after the independent verifier
returns PASS on the immutable complete package. If it fails, the failed package
must remain archived and any changed step size, precision, path construction or
reduction is a new explicitly post-hoc certificate candidate.

The scope remains one explicit rational initial field in the finite N11
Galerkin ODE.
