# Triadic envelope cutoff-growth gate (post-v0.2)

## Question

The phase-sensitive gate writes the exact enstrophy transfer as

[
T_N = chi_N A_N,qquad
A_N=sum_{k=p+q}|Z_{k,p,q}|,qquad |chi_N|le 1.
]

A natural next attempt would be to prove a cutoff-independent estimate

[
A_N le C,G_N^{3/2},
]

because (A_N) and (G_N^{3/2}) have the same amplitude and frequency-dilation scaling.

This gate asks whether that route looks plausible on dense finite Galerkin fields.

## Construction

For each (N=2,ldots,7), three deterministic seeded real divergence-free fields are generated in two families:

- **ball:** all nonzero modes with (|k|le N);
- **outer_half:** only modes with (N/2<|k|le N).

Each field is normalized so that

[
G_N=sum_k |k|^2|widehat u_k|^2=1.
]

Therefore the reported (A_N) is exactly (A_N/G_N^{3/2}), and the reported (T_N) is exactly (T_N/G_N^{3/2}).

## Observed finite-cutoff pattern

For the full-ball family, the median (A_N/G_N^{3/2}) across the three seeds rises

[
0.487, 0.980, 1.543, 2.147, 2.909, 3.635
]

for (N=2,ldots,7).

For the outer-half family it rises

[
0.317, 0.664, 1.054, 1.330, 1.986, 2.504.
]

At the same time, signed coherence is much smaller than the absolute envelope. In the full-ball family, median (|chi_N|) falls from about (1.67	imes10^{-2}) at (N=2) to (2.82	imes10^{-5}) at (N=7). The outer-half family falls from about (4.32	imes10^{-2}) to (2.36	imes10^{-4}).

This makes the absolute-envelope-only closure route look increasingly poor on these dense samples: the uncancelled cubic envelope grows while the signed transfer remains strongly cancellation-dominated.

## Scope

This is **not** a proof that (A_N/G_N^{3/2}	oinfty), and it is **not** a proof that (chi_N	o0). Six finite cutoffs and three seeds cannot establish either asymptotic statement.

The result is an obstruction diagnostic: any successful closure based on this decomposition must exploit cancellation or additional structure, rather than simply replace (T_N) by the absolute envelope (A_N).

Reproduce with:

```bash
python src/triadic_envelope_growth_gate.py
```
