# WP19 Current Status — 30 September 2026

**Author:** Prince Upadhyay, Independent Research  
**Repository:** `reggaesharkk/navier-stokes-bridge-audit`  
**Status:** current proof-state summary.

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
