# WP19 v0.4 — One-Sided K36 Cutoff Bridge

**Author:** Prince Upadhyay, Independent Research  
**Date:** 29 September 2026  
**Status:** exact finite-dimensional algebraic theorem plus non-rigorous dynamic scouting.  
**Not claimed:** cutoff-uniform convergence, continuum regularity, blowup, or a Millennium Prize result.

## 1. Structural premise

The frozen observable is

[
F=I-9O,
]

where (I) is the sum of absolute normalized signed group masses whose **ordered orbit-pair key** belongs to the frozen K36 set, and (O) is the corresponding sum over all other group keys.

For the frozen K36 key file, every left or right orbit appearing in the selected 36 keys has squared Euclidean norm at most

[
93,
]

so every selected orbit has norm strictly less than 10.

The anchor modes are also low:

[
|P|^2=17,qquad |Q|^2=14,qquad |K|^2=45.
]

Thus every selected K36 group and the normalizer anchor are contained below cutoff 10.

Frozen K36 key SHA-256:

`7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`.

## 2. Exact cutoff-monotonicity theorem

Fix an integer cutoff (Nge10). Let (a) be any divergence-free Fourier state supported in (|k|le N), with nonzero K36 normalizer (z(a)). Let (h) be any additional divergence-free Fourier field supported entirely in modes (|k|>N). Keep all low coefficients fixed and define

[
widetilde a=a+h.
]

Then

[
oxed{F(widetilde a)le F(a).}
]

### Proof

Every K-channel contribution is indexed by an ordered orbit-pair key

[
(operatorname{orb}(p),operatorname{orb}(q)),
qquad p+q=K.
]

If a contribution uses at least one newly added mode, then at least one of its orbit norms is (>Nge10). But every orbit occurring in a frozen K36-selected key has norm at most (sqrt{93}<10).

Therefore no contribution involving a newly added mode can belong to a selected K36 key.

Consequently:

1. all selected group sums are unchanged, hence (I(widetilde a)=I(a));
2. the anchor coefficients (a_P,a_Q,a_K) are unchanged, hence the complex normalizer (z) is unchanged;
3. every previously existing outside-K36 group is unchanged;
4. newly created group keys are outside K36 and contribute nonnegative absolute mass to (O).

Thus (O(widetilde a)ge O(a)), and therefore

[
F(widetilde a)=I(a)-9O(widetilde a)le I(a)-9O(a)=F(a).
]

This is an exact algebraic statement about the frozen observable, not a statement about the dynamics.

## 3. Dynamic implication

For a higher-cutoff trajectory (u_M), with (M>Nge10), split

[
u_M=v+h,qquad v=Pi_Nu_M,quad h=(I-Pi_N)u_M.
]

The theorem gives

[
oxed{F_M(u_M(t))le F_N(Pi_Nu_M(t)).}
]

Thus direct occupation of modes above (N) cannot make the frozen K36 margin less negative. The only dangerous effect is the high-frequency tail's dynamical backreaction on the old low coefficients.

## 4. Same-datum endpoint counterfactuals

Floating-point endpoint diagnostics agree with the theorem.

| state | N11 -> N12 F(T) | N12 -> N13 F(T) |
|---|---:|---:|
| embedded lower endpoint | -48.390539 | -72.015058 |
| higher trajectory, old modes only | -60.450307 | -77.952771 |
| lower old modes + higher new shell | -59.953550 | -79.399922 |
| full higher endpoint | -72.015058 | -85.358994 |

When only the new shell is added to the frozen lower endpoint, (I) stays unchanged and (F) becomes more negative.

These values are diagnostics; the monotonicity theorem itself is exact and independent of them.

## 5. Low-mode backreaction equation

Let

[
e=Pi_Nu_{N+1}-u_N,qquad h=(I-Pi_N)u_{N+1},
]

and (v=Pi_Nu_{N+1}=u_N+e). Then

[
partial_t e-
uDelta e
+Pi_Nigl(B(e,u_N)+B(v,e)igr)
=
-Pi_Nigl(B(v,h)+B(h,v)+B(h,h)igr).
]

Because (v) is divergence-free,

[
langle B(v,e),eangle=0.
]

Hence

[
rac12rac{d}{dt}|e|_2^2+
u|
abla e|_2^2
le
|S(u_N)|_{L^infty,mathrm{op}}|e|_2^2
+
R_N(t)|e|_2,
]

where

[
R_N(t)=
left|
Pi_Nleft(B(v,h)+B(h,v)+B(h,h)ight)
ight|_2.
]

This is the **backreaction bridge**.

## 6. Backreaction scout

Using the saved N12 and N13 predictor trajectories only as diagnostics:

| quantity | N11 -> N12 | N12 -> N13 |
|---|---:|---:|
| max sampled low backreaction | 156.601695 | 140.005354 |
| sampled backreaction integral | 0.255256 | 0.224531 |
| recurrence using sampled physical strain | 0.373078 | 0.322998 |
| actual low-mode endpoint drift | 0.225582 | 0.203005 |
| actual new-shell endpoint norm | 0.495507 | 0.385041 |

The sampled backreaction integral decreases across the two tested transitions. The recurrence is about 1.65x and 1.59x the observed low-mode drift.

This remains non-rigorous node-sampled scouting.

## 7. Why the previous endpoint perturbation route cannot close the bridge

The existing global all-mode L2 endpoint perturbation inequality is far too pessimistic. A floating reconstruction gives approximate sign-preserving radii only

- N11 -> N12: (3.40	imes10^{-4}),
- N12 -> N13: (4.93	imes10^{-4}),

while the actual low-mode endpoint drifts are about 0.226 and 0.203.

So even a perfect full-state distance estimate would not make the old global endpoint Lipschitz envelope useful for cutoff transfer. The ordered-orbit structure must be retained.

## 8. Revised proof architecture

The next proof attempt should be two-tiered.

**Tier A: dynamics**

1. certify high-shell creation;
2. certify a sharp whole-segment physical-space strain supremum;
3. use them to certify low-mode backreaction.

**Tier B: observable**

1. use exact cutoff monotonicity to remove the direct high-shell effect;
2. build a low-mode-only perturbation bound;
3. preserve ordered group structure instead of collapsing all sources into one global triangle-inequality envelope.

The real bridge variable is now

[
Pi_Nu_{N+1}-u_N,
]

not the entire difference (u_{N+1}-u_N).

The older optimizer-derived N14-N17 program remains logically separate from the same-rational-datum Arb certificate family.
