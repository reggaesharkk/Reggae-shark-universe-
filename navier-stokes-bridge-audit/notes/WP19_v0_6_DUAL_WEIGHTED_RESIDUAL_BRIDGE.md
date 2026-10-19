# WP19 v0.6 — Dual-Weighted Residual Bridge

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact algebraic upper-certificate reduction plus non-rigorous discrete-adjoint scouting.  
**Not claimed:** cutoff-uniform convergence, continuum regularity, blowup, or a Millennium Prize result.

## 1. Why v0.6 exists

v0.4 showed that newly opened high-frequency groups cannot directly increase the frozen K36 observable once the old coefficients are held fixed.

v0.5 then reduced an endpoint upper certificate to a fixed finite coalition.

The remaining difficulty was that norm-first perturbation estimates were still far too pessimistic.

v0.6 changes the order of operations:

> **weight the cutoff defect by the endpoint objective first, and only then bound it.**

This is a goal-oriented / dual-weighted residual architecture.

## 2. A stronger exact endpoint upper bound

For every ordered K-channel group (g), write

[
y_g(a)=\operatorname{Im}\frac{w_g(a)}{z(a)}.
]

Define

[
n_g(a)=\operatorname{Im}(w_g(a)\overline{z(a)}).
]

Whenever (z(a)\neq0),

[
y_g(a)=\frac{n_g(a)}{|z(a)|^2}.
]

Freeze 500 outside-K36 groups by the deterministic N11 rule:

> rank the outside groups by their absolute normalized N11 endpoint contribution and keep ranks 1 through 500.

For each frozen outside group set

[
\tau_g=\operatorname{sign} n_g(a_{11}(T)).
]

Now define

[
G_{C500}(a)=
\frac{
\sum_{g\in K36}|n_g(a)|
-
9\sum_{g\in C500}\tau_g n_g(a)
}{|z(a)|^2}.
]

For **every** state with nonzero normalizer,

[
\boxed{F(a)\le G_{C500}(a)}.
]

Indeed, (-|n_g|\le-\tau_g n_g) for every fixed (	au_g\in\{-1,+1\}), and dropping outside groups not in C500 can only raise the full observable. No C500 sign-preservation assumption is required.

## 3. Fixed finite support

The frozen K36+C500 key set contains only orbit types of squared norm at most 121. Thus every selected orbit has norm at most 11.

Direct enumeration gives the same support at N=11,12,13,14,17:

- **1,048 ordered K-channel source pairs**
- **1,159 unique Fourier modes**, including the anchor modes.

Therefore for every cutoff (M\ge11), the surrogate (G_{C500}(u_M(T))) depends on the same fixed low-frequency coordinates. Higher shells cannot create new terms inside this endpoint surrogate.

C500 captures **99.94122%** of the total N11 outside-group absolute mass.

K36 SHA-256:

`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`

C500 SHA-256:

`79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`

The materialized 500-key JSON is retained in the archived v0.6 ZIP. The repository builder deterministically reconstructs it from the saved N11 endpoint and verifies the hash above.

## 4. Discrete cutoff defect and adjoint

Let (a_j) be the lower-cutoff saved RK4 predictor and

[
v_j=\Pi_Nu_{N+1}(t_j)
]

the higher-cutoff predictor projected back to the old cutoff.

Let (Phi_N) denote one lower-cutoff RK4 step and define

[
d_j=v_{j+1}-\Phi_N(v_j).
]

For the endpoint objective (G_{C500}), define the linearized discrete adjoint

[
\lambda_{120}=\nabla G_{C500}(a_{120}),
qquad
\lambda_j=D\Phi_N(a_j)^T\lambda_{j+1}.
]

The first-order endpoint shift is then

[
\Delta G_{C500}\approx
\sum_{j=0}^{119}\langle\lambda_{j+1},d_j\rangle.
]

This retains the direction of the cutoff defect rather than replacing the defect by a full-state norm.

## 5. N11 -> N12 scout

The lower endpoint gives

[
G_{C500}(a_{11}(T))=-47.81627824.
]

The N12 trajectory projected back to N11 gives

[
G_{C500}(\Pi_{11}u_{12}(T))=-55.15279823.
]

Hence the actual projected-low change is

[
\Delta G=-7.33651998.
]

The discrete-adjoint first-order prediction is

[
\sum_j\langle\lambda_{j+1},d_j\rangle=-7.50592311,
]

with observed numerical remainder

[
+0.16940312.
]

Even discarding the sign of every observed first-order contribution, the sum of their absolute magnitudes is only

[
9.48944154,
]

well below the starting negative margin (47.81627824). There are 100 negative and 20 positive step contributions.

## 6. N12 -> N13 scout

The same frozen C500 surrogate gives

[
G_{C500}(a_{12}(T))=-55.15279823
]

and

[
G_{C500}(\Pi_{12}u_{13}(T))=-55.76050675.
]

Thus

[
\Delta G=-0.60770852.
]

The linearized adjoint prediction is

[
-0.60494057,
]

with numerical remainder

[
-0.00276795.
]

The sum of absolute first-order step contributions is only

[
6.19885296,
]

again well below the starting negative margin (55.15279823).

## 7. What changed

The old proof architecture was

[
\text{vector cutoff error}
\rightarrow
\|e(T)\|_2
\rightarrow
\text{global Lipschitz constant}
\rightarrow
F(T).
]

That destroys almost all of the margin.

The new architecture is

[
\text{cutoff defect at each step}
\rightarrow
\text{adjoint-weighted scalar residual}
\rightarrow
G_{C500}(T).
]

The quantity being bounded is now the effect of the unresolved dynamics on the specific endpoint certificate.

## 8. Exact versus scouting

### Exact

1. (F\le G_{C500}) whenever the normalizer is nonzero.
2. C500+K36 uses exactly 1,159 fixed Fourier modes and 1,048 ordered source pairs for every cutoff at least 11.
3. Modes opened above cutoff 11 cannot enter the frozen C500 endpoint formula directly.

### Scouting only

1. The saved RK4 cutoff defects.
2. The floating discrete adjoint.
3. The first-order defect sums.
4. The observed nonlinear remainders.

These quantities are not yet interval-enclosed.

## 9. Next rigorous gate

The next certificate should certify the scalar dual-weighted representation rather than 1,159 coordinate errors independently.

A rigorous version needs:

1. a validated tube around the lower predictor;
2. a whole-step enclosure of the projected cutoff defect;
3. an enclosure of the discrete Jacobian-vector / adjoint recursion over that tube;
4. an interval bound on each scalar product (langle\lambda_{j+1},d_j\rangle);
5. a second-order remainder bound for the nonlinear RK4 map and endpoint objective;
6. the existing whole-path nonzero-normalizer guard.

The N11 scout leaves approximately (47.82-9.49\approx38.33) units of first-order sign margin after replacing every observed dual-weighted contribution by its absolute value. The analogous N12 quantity is (55.15-6.20\approx48.95).

These are scouting margins, not certified margins, but they justify building the rigorous dual-weighted gate.

## 10. Freeze boundary

C500 is a post-hoc exploratory design choice made after examination of the existing N11-N13 material.

It is now frozen by SHA-256. Any future untouched same-datum cutoff test must use the exact same coalition size, ordering, and fixed signs to count as a prospective transfer test.

The historical optimizer-derived N14-N17 track remains logically separate from the same-rational-datum Arb family.
