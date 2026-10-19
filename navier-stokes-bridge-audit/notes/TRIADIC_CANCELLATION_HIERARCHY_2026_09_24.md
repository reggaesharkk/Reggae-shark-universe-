# Triadic cancellation hierarchy gate (post-v0.2)

## Exact hierarchy

For the ordered triad contributions already defined by

[
Z_{k,p,q}
=
-|k|^2
leftlangle
widehat u_k,,
P_k[i(qcdotwidehat u_p)widehat u_q]
ightangle,
qquad k=p+q,
]

define

[
A_N=sum_{k,p,q}|Z_{k,p,q}|,
]

then first collect all convolution pairs feeding one output mode,

[
C_k=sum_{p+q=k} Z_{k,p,q},
qquad
B_N=sum_k |C_k|,
]

and finally recover the signed transfer

[
T_N=operatorname{Re}sum_k C_k.
]

The triangle inequality gives the exact hierarchy

[
|T_N|le B_Nle A_N.
]

Thus (A_N	o B_N) measures cancellation among convolution pairs feeding the **same output mode**, while (B_N	o |T_N|) measures the remaining cancellation among output modes and complex phases.

## Dense-field observation

Using the same deterministic real divergence-free (G=1) fields as the triadic envelope growth gate:

For the full-ball family, the median (B_N/G^{3/2}) across the three seeds is

[
0.166, 0.162, 0.193, 0.170, 0.163, 0.172
]

for (N=2,ldots,7).

At the same time, the median within-mode survival factor (B_N/A_N) falls

[
0.348, 0.165, 0.122, 0.0795, 0.0563, 0.0473.
]

For the outer-half family, median (B_N/G^{3/2}) stays between about (0.125) and (0.142), while (B_N/A_N) falls from about (0.401) to (0.0578).

So in these dense random fields, the large growth of the raw absolute envelope (A_N) is mostly removed **before** summing across output modes. The dominant sampled cancellation is already inside each exact Fourier convolution coefficient.

## Why this is not yet a closure theorem

The apparent finite-cutoff stability of (B_N/G^{3/2}) is not universal evidence. Since

[
B_Nge |T_N|,
]

the fixed-energy concentration construction from the candidate-inequality gate transfers immediately: any universal estimate

[
B_Nle C(E_0),G_N^{3/2}
]

would imply the already-rejected energy-only estimate for (|T_N|). Hence no such energy-only cutoff-uniform bound can hold for arbitrary smooth data.

The value of (B_N) is structural rather than final: it identifies where the numerically observed cancellation occurs and narrows the next search to a mechanism that controls **modewise convolution coherence under physical concentration**.

## Next proof question

A surviving quantity must do both:

1. retain the strong within-output-mode cancellation seen here; and
2. change appropriately under fixed-energy physical concentration, where (T/G^{3/2}) can grow without bound.

That points away from absolute Fourier envelopes and toward a scale-critical geometric or concentration-sensitive depletion factor.

Reproduce with:

```bash
python src/triadic_cancellation_hierarchy_gate.py
```
