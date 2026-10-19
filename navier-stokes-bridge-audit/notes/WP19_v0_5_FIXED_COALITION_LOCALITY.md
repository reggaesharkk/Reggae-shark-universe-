# WP19 v0.5 — Fixed Finite Coalition Locality Gate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact algebraic reduction plus floating endpoint transfer diagnostics.  
**Not claimed:** a cutoff-uniform dynamical estimate, continuum convergence, blowup, or global regularity.

## Result

The v0.4 one-sided theorem showed that newly opened high-frequency groups cannot directly increase the frozen K36 observable

[
F=I-9O.
]

v0.5 sharpens this substantially.

A fixed set of 200 outside-K36 orbit-pair groups, selected once from the N11 endpoint and then frozen, gives the upper observable

[
U_{C200}(a)
=
sum_{gin K36}|y_g(a)|
-
9sum_{gin C200}|y_g(a)|.
]

Because every omitted outside group enters (F) with coefficient (-9),

[
oxed{F_M(a)le U_{C200}(a)}
]

for every cutoff (M) for which the frozen keys are present.

Thus (U_{C200}<0) is sufficient for (F<0).

## Exact support locality

The union K36 ∪ C200 contains 236 ordered orbit-pair keys.

Every orbit occurring in those keys has squared norm at most 121, hence norm at most 11. Therefore, for every cutoff (Mge11), all terms entering (U_{C200}) already live in the same fixed low-frequency set. Newer Fourier shells cannot create additional terms inside K36 or C200.

Direct enumeration gives:

- **461 ordered K-channel source pairs**
- **569 unique Fourier modes**, including the anchor modes

and exactly the same 461 / 569 support at N=11, 12, 13, 14, and 17.

Hence (U_{C200}(u_M(T))) is a fixed finite-coordinate object for every (Mge11).

## Frozen coalition provenance

The coalition was selected post-hoc at N11 by the deterministic rule:

> rank every outside-K36 ordered orbit-pair group by its absolute normalized contribution at the saved N11 same-datum endpoint and retain the first 200.

It is now frozen and must not be retuned at later cutoffs.

K36 SHA-256:

`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`

C200 SHA-256:

`4fb5531fcc6c4490aa7826992ff843f27fefdbc1427c7587ac0544027420e698`

The repository builder/checker regenerates C200 from the saved N11 endpoint and verifies this digest. The archived v0.5 ZIP also contains the materialized C200 JSON.

## Unchanged-coalition transfer scout

The same 200 outside keys were evaluated without retuning at N11, N12, and N13.

| cutoff | K36 inside mass | C200 outside mass | U_C200 | full float F |
|---:|---:|---:|---:|---:|
| 11 | 928.603857 | 106.864698 | **-33.178421** | -48.390539 |
| 12 | 926.576550 | 107.866347 | **-44.220575** | -72.015058 |
| 13 | 930.386164 | 108.499973 | **-46.113595** | -85.358994 |

The same finite upper certificate is negative at all three saved endpoints, with no coalition retuning.

These endpoint values are floating diagnostics. The inequality (Fle U_{C200}) and the finite-support locality are exact algebraic statements.

## Deletion robustness

Because (U_{C200}=I-9O_{C200}), the amount of retained outside mass that could disappear before the upper bound reaches zero is (-U_{C200}/9).

At the saved endpoints this is approximately:

- N11: 3.686491
- N12: 4.913397
- N13: 5.123733

Thus a later interval proof does not need all 200 retained outside terms to stay sharply bounded away from zero.

## What still fails

A group-by-group sensitivity scout using one global isotropic low-mode L2 radius remains too pessimistic.

Approximate sign-preserving global radii for C200 are only:

- N11: (5.81	imes10^{-4})
- N12: (8.37	imes10^{-4})

while the observed total low-mode endpoint drifts are about 0.226 and 0.203.

So the fixed-coalition reduction does not close the bridge by itself. It identifies why the next gate must be support-aware or direction-aware rather than using one scalar L2 ball.

## Next gate

WP19 v0.6 should propagate error only on the fixed 569-mode support, preferably in mode or orbit blocks, and interval-evaluate the 236 retained groups directly.

The exact target becomes

[
e_k(t)=u_M(k,t)-u_{11}(k,t),qquad kin S_{569}.
]

If a cutoff-uniform bound on those fixed coordinates keeps (U_{C200}(T)<0), the endpoint sign problem no longer grows in dimension with the Fourier cutoff.

## Research boundary

The principal exact result of v0.5 is

[
oxed{
F_M(a)le U_{C200}(a),
qquad
U_{C200}	ext{ uses only 569 fixed modes for every }Mge11.
}
]

The unresolved problem is uniform dynamical control of those modes under backreaction from higher shells.
