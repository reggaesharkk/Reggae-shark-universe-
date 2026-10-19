# WP16 sparse turnover: validated-trajectory feasibility gate

28 September 2026. This note follows the 112-pair numerical reduction and exact rational `F(0)>0` certificate. It is a **proof design and floating-point feasibility diagnostic**, not a certified `F(.003)<0` result.

## A posteriori error identity

In the full N11 divergence-free Galerkin space, let `u` solve the ODE from the exactly projected rational initial field. Let `v(t)` be a continuous, transverse, real, explicitly specified approximate path with the *same* initial condition, and define its residual

`r = v' + P_11[(v·∇)v] - nu Δv`.

For `e=u-v`, the incompressible transport terms satisfy `<e,(v·∇)e>=<e,(e·∇)e>=0`. The remaining quadratic pairing is bounded by `||∇v||_{L∞} ||e||_2²`, and viscosity is nonpositive. Therefore, with the standard normalized torus norm,

`d||e||_2/dt <= ||∇v||_{L∞} ||e||_2 + ||r||_2` almost everywhere,

and for matching initial conditions,

`||e(T)||_2 <= ∫_0^T ||r(s)||_2 exp(∫_s^T ||∇v(q)||_{L∞} dq) ds`.

This identity needs no arbitrary-data Navier–Stokes regularity assumption: it concerns the finite polynomial N11 ODE. It also avoids an exponentially large global Lipschitz constant based on every pair of Fourier modes. The right side becomes a **certificate only if both the residual and gradient integrals are enclosed over every continuous time segment**, including numerical roundoff.

For the margin `F=I-9O`, the grouped signed term has `g_j(a)=Im(w_j(a)/z(a))`. At states with `|z|>=z_*>0`, a sufficient endpoint error calculation can sum the weighted bounds

`|g_j(u)-g_j(v)| <= |w_j(u)-w_j(v)|/z_* + |w_j(v)| |z(u)-z(v)|/z_*²`.

Here `w_j` is quartic and `z` cubic in the Fourier coefficients. Exact or outward interval evaluation of their derivatives on the enclosing coefficient ball must turn the `L²` trajectory radius into a certified `F` interval. Absolute values are 1-Lipschitz, so a grouped contribution crossing zero does not invalidate this *value* bound. The endpoint condition needed is `upper(F(u(.003)))<0`.

## Floating-point feasibility screen

For the projected-rational initial field converted back to float64, RK4 at `dt=.0001` returned `F(.003)=-48.3904829635909`, consistent with the archived 112-pair replay. On the original replay, the `dt=.0001`, `.00005`, and `.000025` endpoints were `-48.39048296359124`, `-48.39053556544013`, and `-48.390538870127216`. These are *not error bounds*.

Selected sampled values along the `dt=.0001` numerical path:

| t | F | grid-sampled max Frobenius `|∇v|` | `sum_k |k| |a_k|` | `|z|` |
| ---: | ---: | ---: | ---: | ---: |
| 0 | +645.804 | 449.192 | 1831.546 | 136716.051 |
| .001 | +730.419 | 444.723 | 1939.129 | 92412.444 |
| .002 | +359.047 | 441.247 | 2093.493 | 68682.771 |
| .003 | -48.390 | 442.568 | 2331.908 | 51423.933 |

The spatial-grid maxima are lower diagnostics, not analytic `L∞` upper bounds. The Fourier `l¹` expression is a valid *pointwise upper bound for an individual recorded trigonometric polynomial*, but the table does not bound the interpolant between samples. The observed nonzero `z` values likewise do not prove a lower bound along the full path or its error ball.

For a single cubic Hermite segment joining the first RK4 step, the *sampled*, unvalidated `L²` residual at local time fraction `.25` was:

| step h | sampled `||r(.25h)||₂` |
| ---: | ---: |
| .0001 | .00696293003 |
| .00005 | .00086344517 |
| .000025 | .00010761763 |
| .0000125 | .00001343644 |

At `h=.0001`, the same `.25` residual was `.00679`–`.00710` at sampled path steps 15 and 29. The roughly eightfold reduction on halving h suggests that a smaller step may make the a posteriori estimate effective, but maximum residuals over each entire segment, roundoff, and endpoint sensitivity are unbounded here. No pass decision is made from this screen.

## Concrete certificate implementation gate

1. Represent the rationally projected initial field exactly and compute a reproducible approximate full N11 path. Specify each piecewise polynomial `v` by finite decimals interpreted as rationals, projecting all coefficient vectors exactly so `v(t)` remains solenoidal and real.
2. For every segment, enclose the polynomial residual `r(t)` over its **whole time interval**, preferably via outward-rounded Bernstein coefficients of the quadratic Galerkin vector field. Enclose the Fourier `l¹` gradient of the same polynomial segment. Record independently checkable segment bounds and their arithmetic precision.
3. Accumulate the energy error inequality with outward rounding from zero initial error. Enclose `|z|` away from zero and the quartic numerator variations throughout the endpoint error ball. Reject the candidate if the final upper bound on `F` reaches zero.
4. Build a second checker for the exported segment certificate, independent of the search/generator. Compare the certificate against the fixed coefficient hash and the exact initial-sign output. Preserve any failed enclosure; change a step size or reduction only as a new, explicitly post-hoc candidate.

Passing these gates proves a **finite N11 trajectory crossing** for one explicit rational initial field. A statement about the continuum PDE needs a separate cutoff-uniform tail argument. The current work establishes only the initial exact sign and a numerical later-time sign.
