# WP19 Current Status — 30 September 2026

**Author:** Prince Upadhyay, Independent Research  
**Repository:** `reggaesharkk/navier-stokes-bridge-audit`  
**Status:** current proof-state summary.

## Final 30 September update — authoritative current state

This update supersedes older same-day statements below wherever they still describe N11–N14 as the full rigorous same-datum chain or describe the direct consecutive-shell term as non-summable.

The unchanged rational datum is now rigorously certified at **every cutoff N=11,...,18**. N15, N16, and N17 completed in GitHub Actions run `36669057015`. N18 reached the six-hour hosted-job limit after preserving 99 completed segment certificates; recovery run `36706229638` hash-validated segments `000–098`, computed `099–119`, reran the aggregate error, endpoint sign, and whole-path normalizer gates, and returned **PASS**.

Certified endpoint intervals for N15–N18 are:

- N15: `[-88.958192681, -84.896722370]`, terminal error `0.000013195722`, normalizer lower `48856.49133823`;
- N16: `[-88.828357601, -84.589032046]`, terminal error `0.000013456103`, normalizer lower `48858.17452511`;
- N17: `[-88.682140170, -84.277596371]`, terminal error `0.000013665541`, normalizer lower `48860.35300815`;
- N18: `[-88.699660529, -84.159654865]`, terminal error `0.000013774643`, normalizer lower `48860.59568947`.

Across the certified finite family `N=11,...,18`, the endpoint is uniformly bounded above by `-42.032667894 < 0`; the minimum recorded whole-path normalizer lower bound is `48850.68586052`; and the maximum terminal error upper bound is `0.000013774643`.

WP19 v0.19 also corrects the earlier coarse direct-shell obstruction: boundary-annulus localization makes the direct newly-opened-shell contribution absolutely summable. The remaining hard term is the **recursive state/backreaction drift**

`Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)`.

The next theorem target is therefore a rigorous goal-oriented/dual-weighted control of that recursive drift and its nonlinear remainder. The full finite-chain record is [WP19 v0.21](WP19_v0_21_N11_N18_CERTIFIED_CHAIN.md).


## 1. Rigorous same-datum chain

The same frozen 112-pair rational datum has now been validated at four consecutive finite Galerkin cutoffs:

```
N = 11, 12, 13, 14.
```

Frozen witness SHA-256:

`4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`

Frozen K36 SHA-256:

`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`

Common parameters:

- `nu = 0.1`
- `T = 0.003`
- no retuning of the datum between cutoffs.

The prospective N14 certificate used 120 whole-segment 128-bit Arb enclosures and returned:

- terminal L2 trajectory-error upper bound: `0.000012825905`
- `F(0) in [645.8037741471, 645.8037741472]`
- `F(0.003) in [-89.015834781, -85.160766265]`
- whole-path normalizer lower bound: `48850.68586052`
- result: **PASS**

The N14 workflow artifact contains 126 files. Its ZIP SHA-256 is:

`b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`

## 2. Historical N14-N17 track is separate

The earlier WP16 phase-only / optimizer-derived continuation reached N17 and remains part of the research record.

That track is not the same experiment as the later same-rational-datum Arb family. The older N14-N17 states were optimizer-derived and were used for prospective mechanism/time-gate stress tests. They must not be relabeled as N14-N17 same-datum Arb certificates.

The historical N17 broad gate passed, while its separately frozen mechanism gate failed or became unevaluable. That negative result remains preserved.

## 3. Fixed endpoint support

WP19 v0.11 proves that every Fourier coefficient entering the frozen K36+C500 signed numerator and normalizer is contained in the N11 space.

Therefore, whenever the tracked normalizer is nonzero,

```
G_C500(a) = G_C500(P11 a)
```

for every outer cutoff `M >= 11`.

Thus the endpoint observable itself does not grow in dimension as the Galerkin cutoff increases.

## 4. Recursive closure variable

For

```
u_M = v_M + h_M,
v_M = P11 u_M,
h_M = (P_M-P11)u_M,
```

the exact low equation is

```
d v_M/dt + nu A v_M + P11 B(v_M,v_M) = Gamma_M
```

with

```
Gamma_M = -P11[
    B(v_M,h_M)
  + B(h_M,v_M)
  + B(h_M,h_M)
].
```

So all influence of the unresolved/high-frequency state on the fixed low state is mediated through `Gamma_M`.

A fixed-dimensional energy estimate gives

```
||v_M(t)-v_L(t)||_2
<= exp(C_strain,11 ||u_0||_2 t)
   integral_0^t ||Gamma_M-Gamma_L||_2 ds.
```

Hence a summable/Cauchy closure budget would transfer directly to the fixed low state and then to the frozen signed numerator.

## 5. Divergence-free output-frequency cancellation

WP19 v0.14 sharpens the closure estimate.

For `k=p+q` and a divergence-free advecting coefficient `a_p`,

```
a_p dot q = a_p dot (k-p) = a_p dot k.
```

Therefore a fixed low-output interaction pays the low output frequency `|k|`, not the potentially large high input frequency.

The resulting exact estimate is

```
||P_K B(a,b)||_2 <= C_K ||a||_2 ||b||_2,
C_K^2 = sum_{0<|k|<=K} |k|^2.
```

For `K=11`, independent Wolfram enumeration gives:

- 5,574 nonzero integer output modes;
- `sum |k|^2 = 404724`;
- `C_11 = sqrt(404724) ~= 636.179220031588`.

## 6. What is now proved about the continuum closure

For one fixed Leray-Hopf solution, the direct high-shell-to-low closure increments are absolutely summable.

The v0.14 estimate yields, for direct shell additions,

```
||Delta Gamma||_2
<= C_11 [2 ||w||_2 ||s||_2 + ||s||_2^2].
```

Together with the Leray-Hopf energy inequality, the direct tail inside one fixed solution tends to zero.

This establishes a well-defined fixed-low closure limit for a weak solution.

## 7. What remains open for all-cutoff transfer

For the **different** consecutive Galerkin solutions `u_M` and `u_{M+1}`, energy/dissipation control alone gives only a worst-case direct contribution with leading `O(1/M)` behavior.

That is not summable.

The exact consecutive-cutoff closure difference is decomposed into:

```
direct new-shell contribution
+
recursive state/backreaction drift.
```

The direct term needs stronger shell decay than the energy-only worst case, such as an integrated `M^{-1-epsilon}` bound, a Gevrey tail, or a suitable dissipation-wavenumber estimate.

The state-drift term remains the target of the fixed-P11 stability / dual-weighted residual machinery.

## 8. Regularity claim boundary

The project has also proved two useful no-go facts:

1. Negative K36/C500 values can occur on smooth finite Fourier states, so a negative static observable is not itself a singularity criterion.
2. Because the observable depends only on P11, it cannot by itself control arbitrarily high-frequency vorticity or a determining/dissipation wavenumber.

Therefore the viable regularity architecture is:

```
fixed low-mode recursive closure
+
independent high-frequency continuation/dissipation control.
```

## 9. Current next target

The current theorem target is to prove a summable bound on

```
||Gamma_{M+1}-Gamma_M||_{L1_t L2_x}
```

by combining:

- the v0.14 energy-level direct-shell estimate;
- stronger high-frequency shell decay;
- a rigorous dual-weighted or stability bound for recursive state drift;
- the existing negative signed-C500 numerator margin.

A successful result would be an all-cutoff transfer theorem for the fixed observable. It would still not, by itself, solve 3D Navier-Stokes regularity.

## Claim boundary

Current rigorous achievements are finite-Galerkin certificates, exact algebraic/Fourier inequalities, and a fixed-low weak-solution closure-passage framework.

No all-N persistence theorem, finite-time singularity theorem, arbitrary-data global-regularity theorem, or Millennium Prize solution is claimed.


## 10. Continuum a-posteriori scout

WP19 v0.15 now measures the full continuum truncation residual `Q14 B(u14,u14)` on the saved N14 predictor nodes.

The strongest immediate diagnostic is the norm separation:

- `L2_t H^-1 ~= 0.3312582611`;
- `L1_t H^-1 ~= 0.0166855303`;
- `L2_t L2 ~= 4.9703990588`;
- `L1_t H1 ~= 3.7718196582`.

Thus the node-sampled `L1_t H1` residual is about 226 times the `L1_t H^-1` residual.

This does not certify a continuum solution. It redirects the regularity-side work toward a negative-Sobolev a-posteriori criterion with rigorous whole-segment residual enclosures and an explicit `W^-1,3` bound.


## 11. v0.16 critical-space a-posteriori no-go

WP19 v0.16 specializes the sufficient strong-existence criterion of Brunk, Giesselmann and Tscherpel to the exact N14 cubic-Hermite reconstruction after the unit-torus Navier-Stokes rescaling.

Using 160-bit Arb arithmetic, one omitted mode `k=(12,5,6)`, and only the first Hermite segment, the gate proves:

- whole-segment omitted-mode coefficient lower: `11.93863890885675...`;
- corresponding unit-torus `W^-1,2` residual lower: `32.9162834523052...`;
- criterion quantity `A > 0.00720428952807...`;
- `log M > 9.326757996764e12`;
- `log(criterion LHS) > 6.217838664529e12 > 0`.

Therefore the published sufficient condition `LHS <= 1` is rigorously false for this particular N14 Hermite reconstruction and the stated published constants.

This is a no-go for one certification route only. It does not imply blowup, singularity, or nonexistence of a continuum strong solution.

The continuum-side next target is now a reconstruction-specific Fourier-linearized stability proof that retains mode-by-mode viscous damping instead of using a universal high-amplitude Gronwall factor.


## 12. Fast same-datum extension through N18

Floating same-datum predictors have now been generated prospectively for N15-N18 with no retuning.

Numerical endpoint values remain strongly negative:

- N15: `F ~= -86.92746`
- N16: `F ~= -86.70869`
- N17: `F ~= -86.47987`
- N18: `F ~= -86.42966`

The C500 surrogate is not monotone: its N17->N18 change is slightly negative. The magnitude of successive N14->N18 C500 corrections nevertheless shrinks sharply, with the last three observed absolute ratios near `0.178, 0.262, 0.261`.

The sampled fixed-low closure difference also decreases rapidly. Its L1_t L2_x total is approximately `0.01716, 0.00907, 0.00350, 0.000997` over N14->15 through N17->18.

These are scouting results only.

## 13. Parallel rigorous escalation

A generic same-datum whole-segment validator now runs N15, N16, N17 and N18 in parallel on GitHub Actions run `36669057015`.

Each job repeats the N14 proof architecture independently at its cutoff: 120 whole-segment 128-bit Arb residual/gradient enclosures, trajectory-error propagation, K36 endpoint sign gate, and whole-path normalizer guard.

Until those jobs finish successfully, the rigorous same-datum chain remains N11-N14.


## 14. v0.19 boundary-annulus correction: direct shell is summable

WP19 v0.19 corrects the remaining direct-shell conclusion from v0.14.

For a fixed low output `|k|<=11`, a newly opened shell `s_{M+1}` can couple to the old state only through the boundary annulus

`M-11 < |p| <= M`.

Thus the direct consecutive-cutoff closure term obeys

`||DeltaGamma_M^direct||_{L1L2} <= C11 ||u0||_2^2/(2nu) [1/(M(M-11))+1/M^2]`.

The series is absolutely summable because

`1/[M(M-11)] = (1/11)[1/(M-11)-1/M]`.

Therefore the direct new-shell term is no longer the all-cutoff obstruction. The remaining hard term is the recursive state/backreaction drift

`Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)`.

## 15. v0.20 goal-oriented fixed-F11 adjoint scout

A reconstruction-specific adjoint scout now targets the fixed low observable

`F11(P11 u_M(T))`.

Observed endpoint values remain strongly negative from N14 through N18:

`-60.7795, -58.4633, -58.0254, -57.8962, -57.9152`.

The first-order dual-weighted shell corrections for N14->15 through N17->18 are approximately

`2.30313, 0.432965, 0.132338, -0.017294`.

Their magnitude ratios are about

`0.188, 0.306, 0.131`.

The linearized predictions reproduce the actual fixed-F11 cutoff changes with observed remainders of about 0.56%, 1.14%, 2.44%, and 8.95% respectively. The N18 sign reversal is captured.

This is floating scouting, not an interval adjoint certificate. It identifies the goal-oriented dual-weighted transfer—not a generic full-state norm—as the next rigorization target.


## Addendum — 1 October 2026: WP19 v0.28 recurrence correction

PR [#145](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/145), merged as `a99414216bddc9da83054d254485b79ca9b134b9`, freezes a correction to the separate v0.28 backward-adjoint pilot. The backward adjoint has reverse-time anti-diffusion (+\nu |k|^2); the earlier scalar error recurrence omitted its bound (\nu\max |k|^2=22.5). The strain-only outgoing radii for three M14 half-segments are therefore superseded for adjoint-error use. The corrected sequential upper bounds are 74,903,737,341.768087 (segment 239), 76,596,803,403.200881 (238), and 78,324,232,548.824620 (237).

The original recurrence files remain unchanged as historical records. The continuous residual enclosures and standalone structured-penalty comparison remain separately recorded, but no complete adjoint chain is certified; do not continue from the old radii. This correction concerns the v0.28 adjoint pilot only. It does not alter the separate validated finite N11–N18 signed-C500 endpoint certificates in v0.25b. No continuum Navier–Stokes claim follows.


## Follow-up audit — 1 October 2026

The initial WP19 v0.28 recurrence correction was followed by PR [#149](https://github.com/reggaesharkk/navier-stokes-bridge-audit/pull/149), which fixes the residual sign convention, identifies the exact finite-Galerkin adjoint and system sources by hash, lists the assumptions behind the strain-only estimate, and reconciles the N237 A/B old-recurrence inputs. The correction is conditional on the producer-supplied continuous-segment strain/residual bounds; the underlying arrays and exact adjoint path remain unverified here. See the [follow-up audit note](WP19_v0_28_REVERSE_TIME_SIGN_CORRECTION_FOLLOWUP_2026_10_01.md).

Copyright (c) 2026 Prince Upadhyay. All Rights Reserved.
