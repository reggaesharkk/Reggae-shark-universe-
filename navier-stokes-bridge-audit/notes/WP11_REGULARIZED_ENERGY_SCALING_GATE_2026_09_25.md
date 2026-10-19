# WP11: threshold-free derivative and energy scaling gate

**25 September 2026 — finite-Galerkin consistency check.** This audit applies
to the unweighted `σ=0` Sobolev transfer, not a moving Gevrey radius.

On the normalized periodic torus, use the integer dilation
`a_{λk}(t/λ²)=λa_k(t)` on its invariant image sublattice, with
`N,K→λN,λK` and unchanged viscosity. For the `H^s` budget

    X=Σ |k|^{2s}|a_k|²,       Y=Σ |k|^{2s+2}|a_k|²,
    (1/2)X_dot+νY=N_total,

the powers are `X→λ^(2s+2)X` and
`Y, (1/2)X_dot, N_total, N_high→λ^(2s+4)`.
The derivative of an ordered high transfer, and each of the three terms
in the exact regularized identity (R1), scale by `λ^(2s+6)` **provided**
the absolute regularization parameter transforms with its underlying
complex triad transfer: `ε→λ^(2s+4)ε`. A fixed numerical ε in both
systems does not respect this scaling. Choosing the same dimensionless
fraction of the largest `|z|` in each system enforces the required rule.

Run from repository root:

    python3 src/wp11_regularized_energy_scaling_audit.py --output /tmp/wp11_energy_scaling.json

The script checks the exact instantaneous energy budget, (R1), and all
listed scaling powers at `t=0, 0.0025, 0.005` for both `N=4→8` and
`N=7→14`, `K=2→4`, `λ=2`, `s=2`, with relative ε of `1e−3` and `1e−6`.
The largest combined normalized discrepancy is `3.43e−16` for N=4 and
`3.23e−15` for N=7 (double precision, on this trajectory). At relative
ε=`1e−6`, the *base-system* decomposition is:

| N | Time | Signed high transfer | Radial derivative | Angular derivative | Activation derivative |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.0025 | −797.782 | +248983.476 | −34535.847 | +18.275 |
| 7 | 0.0025 | +31372.962 | +13032480.248 | +4266.029 | −65.189 |
| 4 | 0.0050 | −388.447 | +174010.134 | −57396.872 | +11.820 |
| 7 | 0.0050 | +63982.598 | +13080346.558 | +8125.793 | +140.692 |

The three derivative entries add to `dN_high/dt`, **not** to `N_high`.
Their signs and magnitudes depend on the datum, cutoff, time, ordered
decomposition, and ε. At `t=0` the activation term alone is about
`3.14816e5` (N=4) and `1.32910e7` (N=7), reflecting initially zero
triad transfers. The small interior activation values do not show that
zero crossings are negligible on arbitrary trajectories. Nor does a
small angular term in this sample establish a general failure of phase
cancellation; no time-integrated one-sided high-tail estimate follows.

The representation is the **scaled image sublattice**. It is invariant
under convolution and exact for the rescaled finite ODE, but is not a
new independently populated full N=8 or N=14 Fourier ball. Agreement
checks dimensional consistency and code paths; it is no evidence of
convergence as N tends to infinity. The open WP11 target remains a
cutoff-independent signed estimate on every time prefix with a
noncircular continuation argument.
