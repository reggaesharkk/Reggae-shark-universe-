# Where the omitted-mode stretching residual sits in frequency (post-v0.2)

## Correction carried forward

The projection residual audit's original description mistakenly called five tiny positive initial values “positive cases.” They are floating-point roundoff of order $10^{-26}$ to $10^{-28}$. The corrected classification is **16 negative and eight zero initial totals**, then **24 negative endpoint totals** at the recorded times. PR #12 corrected that note. The exact first-enstrophy orthogonality is $\langle\omega_N\cdot(\nabla\times R_N)\rangle=0$. The stretching-rate residual has no factor of viscosity:

$$
\mathcal J_N=\left\langle
2(S_N\omega_N)\cdot(\nabla\times R_N)
+\omega_N\cdot(\operatorname{sym}\nabla R_N)\omega_N
\right\rangle,\qquad
R_N=(I-P_N)\mathbb P[(u_N\cdot\nabla)u_N].
$$

## Linear shell split

For each cutoff $N$, split the omitted solenoidal field $R_N$ into unit-width radial shells $(N+j-1,N+j]$, $j=1,\ldots,N$. Its Fourier support cannot exceed $2N$ for quadratic convolution of a field supported in $|k|\leq N$. Because $\mathcal J_N$ is linear in $R_N$ when $u_N$ is held fixed, its shell contributions sum **exactly** to the full residual. The code independently assembles full $R_N$, checks the shell sum against it, and matches the previously recorded $\mathcal J_N$ at $t=0,.02$.

| Field | $N$ | Time | First omitted shell | Second omitted shell | Other omitted shells | Total $\mathcal J_N$ |
|:--|--:|--:|--:|--:|--:|--:|
| Reference | 4 | 0 | −8,990.325 | −106.178 | ≈0 | −9,096.503 |
| Reference | 4 | .02 | −9,188.707 | −163.482 | −143.061 | −9,495.249 |
| Reference | 7 | 0 | ≈0 | ≈0 | ≈0 | ≈0 |
| Reference | 7 | .02 | −68.038 | −34.887 | −2.326 | −105.252 |
| Combined | 4 | 0 | −476,350.255 | −231,283.526 | −67,231.557 | −774,865.338 |
| Combined | 4 | .02 | −717,686.203 | −191,635.526 | −67,540.097 | −976,861.825 |
| Combined | 7 | 0 | ≈0 | ≈0 | ≈0 | ≈0 |
| Combined | 7 | .02 | −179,030.774 | −163,756.644 | −39,378.169 | −382,165.586 |

For the reference $N=4$ endpoint, the first omitted shell accounts for about $96.8\%$ of the magnitude of the total. For the combined $N=7$ endpoint, the first two account for about $89.7\%$. This localization helps explain why a small change in a low cutoff can change $\dot T_N$ appreciably; it does not imply any limit as $N\to\infty$.

The scanner evaluates both endpoints for all 24 previously stored scenario–cutoff cases. For the reference and combined cases at $N=4,7$, it additionally samples $t=.005,.01,.015$; all sampled **nonzero** totals and resolved individual shell contributions are negative. In particular, the combined $N=7$ residual starts exactly at zero and reaches approximately −10,310, −65,427, −200,261, and −382,166 at these four later times. The data contains no positive sign flip. Five spaced samples cannot establish a sign between them, and the finite collection cannot establish a universal sign theorem. A proposed accelerator example requires a separate, resolved witness.

The shell widths are defined relative to each cutoff. Their values cannot be compared as if they indexed the same fixed physical frequencies across $N$. Quadrature of the unmasked quartic couplings is alias-free on the 32³ grid for $N\leq7$, but these remain finite-dimensional trajectories; no cutoff-uniform time-integrated bound follows.

Reproduce from the repository root with python src/projection_shell_gate.py. Data: src/projection_shell_results.json.
