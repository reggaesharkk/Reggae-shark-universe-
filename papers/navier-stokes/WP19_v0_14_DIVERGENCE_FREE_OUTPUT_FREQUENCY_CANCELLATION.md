# WP19 v0.14 — Divergence-Free Output-Frequency Cancellation and Energy-Level Closure Tail

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** exact Fourier inequality plus explicit closure-tail estimates.  
**Not claimed:** all-cutoff persistence, continuum regularity, singularity, or a Millennium Prize result.

## Incompressibility removes the high derivative

For a Fourier output mode k = p+q,

```
Bhat(a,b)(k) = i sum_{p+q=k} (a_p dot q) b_q.
```

If the advecting field a is divergence-free, then

```
a_p dot p = 0.
```

Therefore

```
a_p dot q
= a_p dot (k-p)
= a_p dot k.
```

So for a fixed low output k, the derivative factor is the output frequency |k|, not the potentially large input frequency |q|.

## Exact fixed-output bilinear theorem

Let P_K be the divergence-free Fourier projector onto nonzero modes with |k| <= K.

For divergence-free a,

```
|P_K B(a,b) hat (k)|
<= |k| sum_{p+q=k} |a_p| |b_q|
<= |k| ||a||_2 ||b||_2.
```

Summing over the fixed output modes gives

```
||P_K B(a,b)||_2
<= C_K ||a||_2 ||b||_2,

C_K^2 = sum_{0<|k|<=K} |k|^2.
```

For K=11, independent Wolfram enumeration gives

```
number of nonzero output modes = 5574
sum |k|^2 = 404724
C_11 = sqrt(404724) = 636.179220031588...
```

The constant depends only on the fixed output projector, not on the outer Galerkin cutoff.

This removes the high-input derivative appearing in the weaker v0.13 estimate.

## Stronger continuum closure truncation

Write

```
v = P11 u
h = (I-P11)u

Gamma(u) = -P11[
    B(v,h)
  + B(h,v)
  + B(h,h)
].
```

Let

```
h_M = (P_M-P11)u
r_M = h-h_M.
```

Then

```
||Gamma-Gamma_M||_2
<= C_11 [
     2 (||v||_2 + ||h_M||_2) ||r_M||_2
     + ||r_M||_2^2
   ].
```

Using orthogonality,

```
||v||_2 + ||h_M||_2 <= sqrt(2) ||u||_2,
```

so

```
||Gamma-Gamma_M||_2
<= C_11 [
     2 sqrt(2) ||u||_2 ||r_M||_2
     + ||r_M||_2^2
   ].
```

Thus for a divergence-free trajectory bounded in L-infinity(0,T;L2), spectral-tail convergence gives

```
Gamma_M(u) -> Gamma(u)
in L1(0,T;L2).
```

The fixed-output closure estimate itself is energy-level.

## Direct addition of one high shell

Let s be a newly added divergence-free shell and w = v+h the previously resolved field. Then

```
DeltaGamma = -P11[
    B(w,s)
  + B(s,w)
  + B(s,s)
].
```

Hence

```
||DeltaGamma||_2
<= C_11 [
     2 ||w||_2 ||s||_2
     + ||s||_2^2
   ].
```

The direct shell-to-low forcing is therefore controlled by shell energy rather than shell gradient.

## Absolute shell summability inside one fixed Leray-Hopf solution

Let

```
s_m = (P_{m+1}-P_m)u.
```

Because every mode in s_m has frequency larger than m,

```
||s_m||_2 <= m^{-1} ||grad s_m||_2.
```

By Cauchy-Schwarz across shells,

```
sum_{m>=M} ||s_m||_2
<= c_M ||grad u||_2,

c_M^2 = sum_{m>=M} m^{-2}.
```

Also,

```
sum_{m>=M} ||s_m||_2^2
<= M^{-2} ||grad u||_2^2.
```

If

```
U = ||u||_{L-infinity_t L2_x}
D = ||grad u||_{L2_t L2_x},
```

then

```
sum_{m>=M} ||DeltaGamma_m||_{L1_t L2_x}
<= C_11 [
     2 U c_M sqrt(T) D
     + M^{-2} D^2
   ].
```

Using the Leray-Hopf energy inequality,

```
U <= ||u_0||_2
D^2 <= ||u_0||_2^2 / (2 nu),
```

so

```
sum_{m>=M} ||DeltaGamma_m||_{L1_t L2_x}
<= C_11 ||u_0||_2^2 [
     sqrt(2T/nu) c_M
     + 1/(2 nu M^2)
   ].
```

Since c_M behaves like M^{-1/2}, this tail tends to zero.

Therefore direct high-shell-to-low closure increments are absolutely summable inside one fixed Leray-Hopf solution.

## Consecutive Galerkin systems: the remaining obstruction

For separate Galerkin solutions u_M and u_{M+1}, the newly opened shell belongs to a different solution at each M.

Uniform energy/dissipation control gives only a worst-case direct single-step estimate with leading O(1/M), which is not summable over M.

Therefore energy control alone is enough for:
- fixed-solution closure truncation;
- absolute direct-shell summability inside one fixed solution;

but not for summable consecutive-Galerkin transfer.

A sufficient upgrade would be integrated shell decay

```
||s_M||_{L1_t L2_x}
<= C M^{-1-epsilon}
```

for some epsilon > 0.

A uniform positive regularity gain, Gevrey tail, or dissipation-wavenumber estimate could supply such decay.

The recursive state-drift term

```
Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)
```

remains separate and is the natural target of the fixed-Pi11 stability/adjoint machinery.

## Revised proof architecture

The all-cutoff problem is now

```
direct shell term
+
recursive state-drift term.
```

Incompressibility removes the high derivative from the direct term. The remaining issue is shell-energy decay plus backreaction control.

## Claim boundary

v0.14 does not prove all-cutoff negativity or continuum regularity. It proves that direct high-frequency coupling into the fixed N11 output space is weaker than a naive derivative count suggests and isolates the remaining non-summable worst-case mechanism under energy-only control.
