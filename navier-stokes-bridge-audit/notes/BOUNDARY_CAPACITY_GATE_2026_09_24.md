# Retained-shell enstrophy and omitted boundary response (post-v0.2)

## A direct limit on a two-shell predictor

Consider a rule that observes **only** the coefficients in the two highest retained radial shells $(N-2,N-1]$ and $(N-1,N]$ and attempts to infer the omitted nonlinear field $R_N=(I-P_N)\mathbb P[(u_N\cdot\nabla)u_N]$ or its stretching-rate contribution $\mathcal J_N$.

At $N=6$, the existing combined double-amplitude, quarter-phase, high-frequency initial field has zero coefficients in **both** observed shells: all occupied wavevectors lie below or at $|k|=4$. Nevertheless, its quadratic low–low interactions generate a first omitted-shell residual of $\|R_{(6,7]}\|_2=45.343749$ and $\mathcal J_6=-67{,}231.557$. The zero field has exactly the same two-shell input (all coefficients zero) but $R_6=0$ and $\mathcal J_6=0$. This is an exact algebraic non-identifiability witness for a deterministic predictor using only those two shell fields, even if it uses every vector component and phase *within* them. It says nothing against a model that also receives lower shells or other informative inputs.

The first omitted shell at cutoff $N=6$ is $(6,7]$, not $[7,8)$. The latter notation would miss noninteger lattice magnitudes between 6 and 7. The same interval convention applies at every cutoff.

## Short-time occupancy audit

The script src/boundary_capacity_gate.py replays four previously recorded Galerkin trajectories with $dt=0.0005$, checks full $G$ and $T$ against the archived scalar traces at five times, and computes exact modal $G$ and its derivative in the two highest retained shells at all 41 steps. Each band obeys $\frac12G_j'=T_j-\nu D_j$; Simpson-integrated band-budget errors have magnitude at most about $1.7\times10^{-6}$. At five times, the script joins these bands to the independently computed omitted-shell $R$ and $\mathcal J_N$ of the earlier shell audit.

| Field | $N$ | $G_{(N-1,N]}(0)$ | $G_{(N-1,N]}(.02)$ | $\|R_{(N,N+1]}\|_2(0)$ | $\|R_{(N,N+1]}\|_2(.02)$ | $\mathcal J_N(.02)$ |
|:--|--:|--:|--:|--:|--:|--:|
| Reference | 4 | 139.979 | 138.847 | 31.616 | 31.454 | −9,495 |
| Combined | 4 | 1,267.781 | 1,196.933 | 286.138 | 323.674 | −976,862 |
| Reference | 7 | 0 | .103 | 0 | 1.715 | −105 |
| Combined | 7 | 0 | 94.980 | 0 | 95.497 | −382,166 |

In the combined $N=4$ case, top-retained-shell enstrophy **decreases** over the interval while the first omitted-shell residual norm **increases**. At $N=7$, the initially empty retained shells populate along with the omitted response. These observations refute a blanket identification of omitted residual magnitude with the amount of enstrophy stored in the last retained shell. Quadratic convolution couples many pairs of lower frequencies; the capacity of a selected upper shell is neither a sufficient input nor a dynamical closure by itself.

At $t=.02$, the highest-band instantaneous $G'$ is approximately $-5{,}156$ for combined $N=4$ and $+11{,}918$ for combined $N=7$. These rates, like the five stored snapshots, describe finite ODE paths only. No speed of a continuum cascade, cutoff-uniform time integral, or general sign theorem is established.

Data: src/boundary_capacity_results.json. Reproduce from the repository root using python src/boundary_capacity_gate.py.
