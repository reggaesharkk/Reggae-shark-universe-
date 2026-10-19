# Short-time signed alignment and strain envelope (post-v0.2)

## Exact diagnostic

Write (G=\langle|\omega|^2\rangle), (D=\langle|\nabla\omega|^2\rangle), (T=\langle\omega\cdot S\omega\rangle), and (M=\langle\lambda_{\max}(S)_+|\omega|^2\rangle). For (G,M>0), define (\alpha=T/M) and (b=M/G). The Galerkin enstrophy identity gives

\[
\frac12\frac{d}{dt}\log G=\alpha b-\nu\frac DG.
\]

Here (\alpha\leq 1), but it can be negative; it is a signed diagnostic, not an angle or a probability. In particular, a small (\alpha) at one time does not control the positive part of its integral later. The identity is exact for the Fourier–Galerkin system, but defining (\alpha) this way alone supplies no a priori regularity bound.

## Reanalysis of stored trajectories

`src/alignment_dynamics_gate.py` joins five stored spatial strain evaluations at (t=0,.005,.01,.015,.02) to 41 independently stored scalar (E,G,D,T) samples spaced by .0005. It checks matching (G,T), integrates the local diagnostic by Simpson quadrature, and checks the exact log-enstrophy budget against the dense scalar trace. The following values describe the existing reference and combined double-amplitude, quarter-phase, high-frequency cases; no new PDE trajectory was run.

| Case | Cutoff (N) | (\alpha(0)\to\alpha(.02)) | (\int_0^{.02}b\,dt) | (\int_0^{.02}T/G\,dt\,/\,\int_0^{.02}b\,dt) | (\frac12\log[G(.02)/G(0)]) |
|:--|--:|--:|--:|--:|--:|
| Reference | 4 | .02431 → .07456 | .27536 | .05002 | .003317 |
| Reference | 5 | .02431 → .09664 | .27598 | .06169 | .006476 |
| Reference | 6 | .02431 → .09742 | .27617 | .06198 | .006563 |
| Reference | 7 | .02431 → .09801 | .27616 | .06213 | .006602 |
| Combined | 4 | ≈0 → .04897 | .56699 | .02795 | .001543 |
| Combined | 5 | ≈0 → .11875 | .56993 | .08032 | .030402 |
| Combined | 6 | ≈0 → .16380 | .57260 | .10141 | .042192 |
| Combined | 7 | ≈0 → .18985 | .57429 | .11548 | .049923 |

At all five sampled times for each of these eight runs, the signed (\alpha) increases. Thus these runs do **not** exhibit immediate alignment depletion. In the combined (N=7) run, (b(.02)=30.558) and (T/G(.02)=5.801): the signed transfer rises even as the envelope remains loose. The dense positive-part integral (\int(T)_+/G) equals (\int T/G) to the displayed precision for these particular trajectories; future negative-transfer cases need the positive-part field retained separately.

The largest absolute dense-budget residual (\left|\frac12\log[G(.02)/G(0)]-\int T/G+\nu\int D/G\right|) is (3.3\times10^{-9}). Five-point versus 41-point (\int T/G) differences range from (10^{-8}) to (2.2\times10^{-5}), depending on the run. The (M) quadrature itself also has spatial-grid error: for the previously audited six-mode (\theta=\pi/2) field, the recorded (32^3\) to (48^3\) change is approximately (-0.0013349), not (-0.000133).

## Proof boundary and next gate

Five snapshots do not establish monotonicity between snapshots, or any long-time trend. Four low cutoffs do not establish a cutoff-uniform continuum bound. A large initial (b) from spatial concentration does not itself preclude an integrable time history. None of these calculations rules out every conceivable one-sided majorant or proves geometric cancellation.

A non-tautological regularity criterion would need an independently controlled space-time quantity, for instance a bound on (\int_0^{T_*}\alpha_+(t)b(t)\,dt=\int_0^{T_*}(T(t))_+/G(t)\,dt), uniform in Galerkin cutoff and justified from initial data and known estimates. Establishing that bound for arbitrary large smooth data is the open analytical step. The current runs instead show that a claim of automatically decreasing (T/M) would already fail on this short interval.

Data: `src/alignment_dynamics_results.json`; input traces: `src/local_strain_majorant_results.json`, `src/candidate_inequality_results.json`, `src/candidate_inequality_N7_results.json`.
