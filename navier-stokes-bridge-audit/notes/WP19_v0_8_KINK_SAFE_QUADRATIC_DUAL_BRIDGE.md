# WP19 v0.8 — Kink-Safe Quadratic Dual Bridge

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact algebraic endpoint reduction plus floating retrospective scouting.  
**Not claimed:** an interval dual-weighted cutoff bridge, an unseen-cutoff prediction, an all-N theorem, or a continuum Navier–Stokes result.

## Exact scalar envelope

For any real `x0 != 0`, with `sigma = sign(x0)`, and any real `x`,

`|x| <= sigma*x + (x-x0)^2/(2|x0|)`.

This is global; it does not assume sign stability.

Apply this to the 36 K36 normalized group ratios `y_g` at a lower/base endpoint `a`. Freeze
`sigma_g = sign(y_g(a))`, while retaining the already frozen C500 signs `tau_g`.

Define the smooth signed endpoint functional

`L_a(x) = sum_K36 sigma_g y_g(x) - 9 sum_C500 tau_g y_g(x)`.

Then for every target state `v` with nonzero normalizer,

`G_C500(v) <= G_C500(a) + [L_a(v)-L_a(a)] + Q_a(v)`

where

`Q_a(v) = sum_K36 (y_g(v)-y_g(a))^2 / (2|y_g(a)|)`.

This is an exact algebraic upper bound. It isolates every possible K36 absolute-value sign flip into one explicit nonnegative quadratic correction.

## N11 -> N12 scout

Using the saved same-datum endpoints:

- base `G_C500 = -47.8162782413`
- projected N12 `G_C500 = -55.1527982262`
- smooth signed change `Delta L = -7.5540346777`
- v0.6 dual-weighted first-order sum `-7.5059231080`
- smooth linearization remainder `-0.0481115697`
- quadratic kink correction `Q = 0.7502275670`
- exact quadratic-envelope target upper on the floating states `-54.6200853520`

One K36 group changes sign, and the quadratic term absorbs it automatically.

Starting instead from the v0.7 certified base upper bound `-41.458407264`, then pessimistically charging the sum of absolute v0.6 first-order terms `9.489441537`, the observed `Q`, and the absolute observed smooth remainder, approximately `31.170626590` units of negative margin remain.

That margin is a scouting budget, not an interval certificate.

## N12 -> N13 scout

- base `G_C500 = -55.1527982262`
- projected N13 `G_C500 = -55.7605067501`
- smooth signed change `Delta L = -0.6077085239`
- v0.6 first-order sum `-0.6049405734`
- smooth remainder `-0.0027679505`
- quadratic correction `Q = 0.2680589788`
- floating quadratic-envelope target upper `-55.4924477713`

No K36 sign flip is observed.

Starting from the v0.7 certified base upper bound `-53.534635536`, then charging the absolute first-order sum `6.198852955`, observed `Q`, and absolute smooth remainder, approximately `47.064955652` units remain.

## Uniform quadratic-budget form

Let

`H(a) = sum_K36 1/(2|y_g(a)|)`.

If every K36 normalized group changes by at most `r`, then

`Q_a(v) <= H(a) r^2`.

At the saved lower endpoints:

- N11: `H = 4.407900894`
- N12: `H = 8.562553541`

The corresponding observed maximum group changes are `1.531704923` and `0.929533876`.

## Why this helps

The v0.6 endpoint gradient is already the gradient of `L_a` at the lower endpoint, since all 36 lower-endpoint K36 group values are nonzero. Thus the dual-weighted first-order scout is naturally reinterpreted as the sensitivity of a smooth signed objective.

The rigorous target is now:

`certified base upper + dual residual bound + smooth second-order bound + quadratic kink bound < 0`.

No interval result for those dynamic terms is claimed in v0.8.
