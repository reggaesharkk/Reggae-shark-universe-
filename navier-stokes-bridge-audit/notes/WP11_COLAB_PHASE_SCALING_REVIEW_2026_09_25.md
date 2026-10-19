# WP11: review of the Colab phase run and dilation check

**Prince Upadhyay, Independent Research — 25 September 2026**

**Input:** user-supplied `wp11_phase(1).json` from the Google Colab run of draft PR #27. This note reviews its actual fields and establishes a separate exact scaling test. It does not prove the open L2–L3 bound.

## 1. What the uploaded JSON actually says

The 11 samples per cutoff cover `0≤t≤0.005`, `dt=0.0005`, `K=2`, `s=2` and `ν=0.1`. The signed trapezoid integrals are `−4.217396690401539` (N=4) and `+156.67253282148567` (N=7). These are **weighted high-advector H² transfer contributions**, not the unweighted kinetic-energy flux or a determination of the sign of total enstrophy production. They compare two different Galerkin ODEs; the difference alone does not identify a unique boundary-feedback mechanism.

| Uploaded field | N=4 maximum | N=7 maximum | Interpretation |
| --- | ---: | ---: | --- |
| `covariance_identity_error` | `8.75e−17` | `2.20e−16` | Normalized algebraic identity check; not a vector norm. |
| `viscous_phase_null_error` | `3.89e−16` | `1.46e−15` | Floating-point residual of the exact zero direct viscous phase contribution. |
| `finite_difference_error` | `2.73e−9` | `1.99e−10` | Directional central difference of the cubic transfer; it does not estimate RK4 time-discretization error. |
| `transfer_reconstruction_error` | `2.71e−15` | `4.50e−15` | Comparison to the projected nonlinear operator. |

The word *driven entirely* does not follow from the covariance plot. The exact derivative is

    d N_high/dt = M_dot E_A[cos φ]
                  + M Cov_A(cos φ,A_dot/A)
                  − M E_A[sin φ φ_dot]
                  + Σ_inactive Re z_dot.

At `N=7, t=0.0005`, these four terms are approximately `+7.436e6`, `+5.786e6`, `−1.495e3`, and `−0.17`. At `N=7, t=0.005`, they are approximately `+14.792e6`, **`−1.711e6`**, `+8.101e3`, and `−0.21`: transfer still rises while amplitude covariance has turned negative. At `t=0`, the `N=7` inactive-triad derivative is about `+13.291e6`, dominating the instantaneous transfer derivative as modes initially at zero amplitude activate. The phase contribution is also not always negligible: at `N=4, t=0.005` it is about `−5.740e4` against a total derivative of `+1.166e5`. Any universal amplitude-dominance or phase-muting conclusion is therefore unsupported by these rows.

## 2. Scale-consistent prediction

For integer `λ≥2` on the fixed torus, dilate both the field and the spectral definitions:

    a'_{λk}(t/λ²)=λ a_k(t),   N'=λN,  K'=λK,  ν'=ν.

The full Fourier ball at cutoff `λN` contains other wavevectors, but the invariant sublattice `λℤ³` cannot excite them through its own convolution. Thus an indexed image of the original ball exactly represents this particular dilated solution. The following weights follow from the **unweighted σ=0 definition** `z=−i |k|^{2s}(q·a_p)(conj(a_k)·a_q)`:

| Quantity | Scaling factor |
| --- | ---: |
| `z`, signed transfer, absolute triad mass `M` | `λ^{2s+4}` |
| `z_dot`, transfer derivative, `M_dot` | `λ^{2s+6}` |
| Phase rate, relative amplitude growth, their weighted covariances | `λ²` |
| Signed time integral over corresponding horizons | `λ^{2s+2}` |
| Mean `cos φ`, active mass fraction | `1` |

For `s=2, λ=2`, the predicted factors are `256`, `1024`, `4`, and `64`, respectively. The physical time horizon changes from `0.005` to `0.00125`. Holding K, horizon or input amplitude fixed instead would test **a different comparison**; it would not check Navier–Stokes scale covariance.

## 3. Executable result and limit

Run `python3 src/wp11_scaling_audit.py --output /tmp/wp11_scaling.json` or the companion Colab notebook. The audited base N=4 and N=7 trajectories map to N=8 and N=14 on the image sublattice. It checks each ODE right-hand side, RK4 state, signed transfer, decomposition terms, covariance, and integrated transfer against its predicted scaling. In the deterministic λ=2 execution, all reported normalized differences were `0.0` at printed precision; the integrated transfers scale by `64` when the horizon is quartered. Dyadic floating-point arithmetic and identical indexed operations can yield exactly matching computed paths, so zero in this check means **implementation covariance on these trajectories**, not a continuum estimate or independent evidence of decorrelation.

## 4. The next genuine mathematical question

A scale-covariant identity remains only an identity. To approach L2–L3 one must bound the **signed time integral** of the high-advector transfer for every smooth initial datum and each prefix `[0,t]` with constants independent of N. A useful candidate must survive the dilation test and give a noncircular bound on active-mass growth, covariance, phase contribution and zero-triad activation together. The present run shows that dismissing any one of those terms based on its small plotted value at one cutoff or time is not valid.
