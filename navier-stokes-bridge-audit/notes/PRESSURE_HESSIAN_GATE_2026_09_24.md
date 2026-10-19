# Pressure Hessian and local stretching response (post-v0.2)

## Why pressure is a different gate

The previous Riesz audit verified a spatial relation between $S$ and $\omega$. To examine an actual dynamical term, let $W=S\omega$ and $H=\nabla^2p$. For a smooth solution of the **unprojected** incompressible equations, differentiation gives

\[
\Delta p=-\operatorname{tr}[(\nabla u)^2],\qquad
\frac{D W}{Dt}=-H\omega+\nu[(\Delta S)\omega+S\Delta\omega].
\]

Consequently the inviscid contribution to the material derivative of the *local* stretching $\omega\cdot W$ is $|W|^2-\omega\cdot H\omega$. The pressure term can have either sign. The Galerkin trajectory obeys a projected equation, whose local gradient evolution also contains a cutoff residual. Thus the displayed terms, evaluated on $u_N$, must **not** be identified with the observed derivative along that truncated trajectory. The classical strain and pressure-gradient equations are also discussed in [Buaria and Pumir, *Journal of Fluid Mechanics*](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/role-of-pressure-in-the-dynamics-of-intense-velocity-gradients-in-turbulent-flows/19A1B3483B38CBFAB9D772236AB1CC3A) and [Yang et al., *Journal of Fluid Mechanics*](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/structure-and-role-of-the-pressure-hessian-in-regions-of-strong-vorticity-in-turbulence/BC81BEF4DD7D44ED72D2724AF4E974A6).

`src/pressure_hessian_gate.py` computes $H$ by a Fourier Poisson solve from the full quadratic source of each finite trigonometric field. A separate computation of $\nabla\cdot[(u\cdot\nabla)u]$ verifies the source. The maximum source discrepancy is below $2.5\times10^{-13}$ in the runs; $\operatorname{tr}H=-\operatorname{tr}[(\nabla u)^2]$, $\langle S:H\rangle=0$, and Fourier versus spatial $T$ also close numerically. These identities check the implementation, not any regularity bound. The unmasked quartic averages are exactly integrated by the 32³ grid for $N\leq7$, since its side length exceeds $4N$.

## Signed results

The table gives volume averages of the nonnegative self term $A=\langle|W|^2\rangle$ and signed pressure contribution $B=-\langle\omega\cdot H\omega\rangle$, as well as the *integral over the whole torus of the pressure term restricted to* the top 10% of grid points ranked by $|\omega|^2$. These quantities scale quartically with amplitude and are not normalized against enstrophy growth.

| Field | $N$ | Time | $A$ | $B$ | Pressure in top tenth | Isotropic part of $B$ | Deviatoric part of $B$ |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Reference | 4 or 7 | 0 | 25,637 | +2,971 | −366 | −4,604 | +7,575 |
| Reference | 4 | .02 | 24,543 | +2,363 | +383 | −3,687 | +6,050 |
| Reference | 7 | .02 | 25,706 | +2,098 | +300 | −3,562 | +5,661 |
| Combined | 4 or 7 | 0 | 938,308 | +111,902 | −40,472 | −480,570 | +592,472 |
| Combined | 4 | .02 | 976,222 | +133,037 | −56,349 | −557,073 | +690,111 |
| Combined | 7 | .02 | 966,771 | +82,415 | +20,310 | −379,977 | +462,392 |

The global pressure contribution $B$ is **positive in every tested snapshot**. In these fields it does not supply a signed global penalty against $|W|^2$. Its isotropic part is negative while its nonlocal deviatoric part outweighs that contribution. The sign inside the top-vorticity region varies by field and time. These observations do not contradict pressure attenuation seen in other flow ensembles: they test these specific initial states and short intervals.

## Grid sensitivity and smooth weight

The sharp top-tenth mask has noticeable grid sensitivity. At the reference $N=7$ endpoint, the masked pressure integral changes by +115 between 32³ and 48³, while the exact global pressure integral changes by less than $10^{-9}$. For the combined $N=7$ endpoint the masked change is −2,961. For comparison, use the fixed smooth weight $w=|\omega|^2/(|\omega|^2+\langle|\omega|^2\rangle)$: the weighted pressure integrals at 32³ are +1,129.991 (reference $N=7$) and +38,107.717 (combined $N=7$), with cross-grid changes +.007 and +.029 respectively. This weight is a diagnostic, not a new inequality or a proof of convergence as $N\to\infty$.

The top-tenth region and smooth weight are recomputed at each snapshot. Two times, two cutoffs, and two fields do not establish an enduring pressure mechanism. A predictive regularity argument would have to bound the signed coupling and all Galerkin cutoff remainders in a way uniform for arbitrary smooth data; the verified Poisson identity alone supplies no such estimate.

Reproduce from the repository root using `python src/pressure_hessian_gate.py`. Data: `src/pressure_hessian_results.json`.
