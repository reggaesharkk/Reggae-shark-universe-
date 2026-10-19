# WP19 v0.13 — Fixed-Output Closure and Weak-Limit Passage

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** valid intermediate result; its fixed-output estimate is superseded by the stronger divergence-free v0.14 estimate.  
**Not claimed:** all-N negativity, singularity, global regularity, or uniqueness of Leray-Hopf weak solutions.

## Historical fixed-output estimate

v0.13 first used the bound

```
||P11 B(a,b)||_2
<= sqrt(5574) ||a||_2 ||b||_{H1}
```

for fixed low outputs.

There are 5,574 nonzero integer modes with |k| <= 11.

This estimate is valid but not optimal for the present divergence-free velocity inputs. WP19 v0.14 uses incompressibility to replace the high-input derivative by the fixed output frequency and obtains the stronger energy-level estimate

```
||P11 B(a,b)||_2
<= sqrt(404724) ||a||_2 ||b||_2.
```

The v0.13 conclusions below remain valid; v0.14 sharpens their hypotheses and tail bounds.

## Continuum closure truncation

For a velocity field u, define

```
v = P11 u
h = (I-P11) u

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

Then Gamma(u)-Gamma_M(u) is the sum of five bilinear terms, each containing at least one copy of r_M.

The original v0.13 estimate used L2/H1 spectral-tail convergence to prove

```
Gamma_M(u) -> Gamma(u)
in L1(0,T;L2)
```

for a Leray-Hopf weak solution.

WP19 v0.14 strengthens this to an energy-level tail estimate.

## Passage of the frozen observable

The frozen signed C500 numerator J depends only on finitely many P11 coefficients.

Along a standard Fourier-Galerkin construction of a Leray-Hopf weak solution, the fixed finite set of low Fourier coefficients admits subsequential uniform-in-time convergence.

Therefore

```
J(P11 u_M(T)) -> J(P11 u(T))
```

along the Galerkin subsequence.

Consequently, if a future theorem establishes a cutoff-uniform margin

```
J(P11 u_M(T)) <= -delta < 0
```

for all sufficiently large M, that finite-dimensional negative margin passes to the corresponding Leray-Hopf weak limit.

For the normalized surrogate G = J/|z|^2, a uniform positive lower bound on the normalizer is also required.

This is a continuum passage for the fixed observable, not a regularity theorem.

## Consecutive-cutoff decomposition

For consecutive Galerkin solutions, the closure difference naturally splits into

```
Gamma_{M+1}(u_{M+1}) - Gamma_M(u_M)

= [Gamma_{M+1}(u_{M+1}) - Gamma_M(P_M u_{M+1})]
+ [Gamma_M(P_M u_{M+1}) - Gamma_M(u_M)].
```

The first bracket is the direct new-shell contribution.

The second bracket is recursive state/backreaction drift.

WP19 v0.14 sharpens the first bracket to an energy-level shell estimate. The second remains the target of the fixed-Pi11 stability/adjoint machinery.

## Claim boundary

v0.13 establishes the weak-limit passage architecture for a fixed finite observable. Its first bilinear estimate has been superseded by v0.14, but the continuum observable-passage conclusion remains part of the proof program.
