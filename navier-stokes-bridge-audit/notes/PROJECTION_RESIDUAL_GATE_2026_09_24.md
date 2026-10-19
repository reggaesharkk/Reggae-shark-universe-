# Galerkin projection residual in the stretching-rate budget (post-v0.2)

## Exact finite-cutoff identity

Let $P_N$ retain divergence-free Fourier modes $|k|\leq N$, let $\mathbb P$ be the Leray projector, and set $R_N=(I-P_N)\mathbb P[(u_N\cdot\nabla)u_N]$. The exact Galerkin evolution can be written in physical space as

$$\partial_tu_N+(u_N\cdot\nabla)u_N+\nabla p_N=\nu\Delta u_N+R_N,$$

where $\Delta p_N=-\operatorname{tr}[(\nabla u_N)^2]$ is the **full quadratic pressure** of the finite trigonometric field, including pressure frequencies above $N$. This convention fixes the plus sign of $R_N$. Differentiating yields, with $W=S\omega$ and $H=\nabla^2p_N$,

$$\frac{D W}{Dt}=-H\omega+\nu[(\Delta S)\omega+S\Delta\omega]
  +(\operatorname{sym}\nabla R_N)\omega+S(\nabla\times R_N).$$

Integration of the derivative of $T_N=\langle\omega\cdot S\omega\rangle$ on the periodic torus therefore gives the exact identity

$$
T_N'=\underbrace{\langle|W|^2\rangle}_{\mathrm{self}}
-\underbrace{\langle\omega\cdot H\omega\rangle}_{\mathrm{pressure}}
+\underbrace{\nu\langle2W\cdot\Delta\omega+
       \omega\cdot(\Delta S)\omega\rangle}_{\mathrm{viscous}}
+\underbrace{\langle2W\cdot(\nabla\times R_N)+
       \omega\cdot(\operatorname{sym}\nabla R_N)\omega\rangle}_{\mathrm{projection}} .
$$

In contrast, $\langle\omega\cdot(\nabla\times R_N)\rangle=0$ exactly: $\omega$ has support inside $N$ and the residual outside $N$. A zero contribution to the **first** global enstrophy derivative therefore conceals a potentially large contribution to $T_N'$. The pressure-only response recorded previously cannot be interpreted as the entire observed time derivative without this term and viscosity.

## Reproducible numerical audit

The script src/projection_residual_gate.py re-evolves all 24 cases from the existing scenario–cutoff traces to $t=.02$ with the previously used step $0.0005$. At both endpoints it independently computes $T_N'$ by differentiating the cubic spectral observable along the Galerkin ODE, and checks it against the four-term spatial budget. The largest relative budget error is $2.2\times10^{-15}$; the maximum absolute first-enstrophy residual pairing is $5.7\times10^{-13}$. The retained Fourier convection agrees with the existing Galerkin convolution within $1.8\times10^{-13}$. At reference $N=4$, $t=0$, a separate central difference with step $10^{-5}$ estimates $T_N'=19{,}321.187173$ versus analytic $19{,}321.187286$.

Selected **endpoint** contributions to $T_N'$ (same derivative units; rounded):

| Field | $N$ | Self | Pressure | Viscous | Projection | Full $T_N'$ |
|:--|--:|--:|--:|--:|--:|--:|
| Reference | 4 | +24,543 | +2,363 | −666 | −9,495 | +16,745 |
| Reference | 5 | +25,445 | +2,086 | −1,249 | −1,358 | +24,924 |
| Reference | 6 | +25,601 | +2,088 | −1,293 | −653 | +25,742 |
| Reference | 7 | +25,706 | +2,098 | −1,326 | −105 | +26,374 |
| Combined | 4 | +976,222 | +133,037 | −4,766 | −976,862 | +127,632 |
| Combined | 7 | +966,771 | +82,415 | −74,368 | −382,166 | +592,652 |

At $t=0$, the same reference field has a projection contribution of approximately −9,097 at $N=4$, −106 at $N=5$, and zero at $N=6,7$ because the initial nonlinear frequencies do not extend past those last cutoffs. Nonlinear evolution populates previously empty modes; the endpoint contribution is no longer zero. The initial combined field likewise has zero residual at $N=7$, but its endpoint projection term is approximately −382,166.

For these 24 sampled endpoints the projection contribution is negative. At the initial snapshots 16 contributions are negative and eight are zero within $10^{-8}$; tiny positive floating-point values in five nominally zero cases (about $10^{-26}$–$10^{-28}$) are **not** evidence of positive contributions. The sampled signs do not establish a general sign theorem, monotone cutoff decay, or a continuum limit. Comparing the projection and viscous *contributions to $T_N'$* is dimensionally appropriate; comparing a raw residual norm to the enstrophy dissipation $\nu D_N$ would mix different observables.

## Proof boundary

The unmasked degree-four spatial integrals are alias-free on the 32³ grid at these cutoffs ($32>4N$). Their exact quadrature does not turn the finite Galerkin paths into exact solutions of the unprojected PDE. The cancellation of the first-enstrophy residual is algebraic; the signed stretching-rate residual needs its own estimate uniform in cutoff. Its values at finitely many snapshots do not provide that estimate or establish a protective long-time mechanism.

Data: src/projection_residual_results.json. Reproduce from the repository root with python src/projection_residual_gate.py.
