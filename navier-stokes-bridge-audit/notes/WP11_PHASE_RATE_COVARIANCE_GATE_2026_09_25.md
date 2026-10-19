# WP11 phase-rate covariance gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** exact finite-Galerkin differentiation identity and runnable diagnostics; no proved cutoff-independent signed transfer bound. This supplements draft PR #27, whose high-tail L2–L3 remains open.

## Exact definitions at fixed weight

Take `σ=0`, `s=2`, an advecting-mode threshold `K=2`, the Galerkin field `a`, and each ordered `k=p+q` with `|p|>K`. Define the **complex scalar transfer contribution**

    z_{kpq}=−i |k|^{2s} (q·a_p) (conj(a_k)·a_q).

Then the signed high-advector contribution is exactly `N_N^{>K}=Σ Re z_{kpq}`. The scalar is defined directly by the transverse vector coefficients and the Fourier convention; it needs no arbitrarily chosen local polarization frame. With `a_dot=−P_N(u·∇u)−ν|k|²a_k`, differentiate every factor:

    z_dot=−i |k|^{2s} [
      (q·a_dot_p)(conj(a_k)·a_q)
      +(q·a_p)(conj(a_dot_k)·a_q+conj(a_k)·a_dot_q)].

Its direct viscous part is `z_dot_visc=−ν(|k|²+|p|²+|q|²)z`. Hence viscosity has **zero direct instantaneous phase rate** when `z≠0`; it can still alter later phases through amplitude changes and nonlinear coupling.

For nonzero `z=A e^{iφ}`, the pointwise phase and amplitude derivatives are

    φ_dot=Im(conj(z) z_dot)/A²,
    A_dot=Re(conj(z) z_dot)/A,
    d(Re z)/dt=A_dot cos φ−A sin φ φ_dot.          (P1)

At a single time, choose an active set of nonzero triads, set `M=Σ A`, and let `E_A`/`Cov_A` denote averages/covariance with weights `A/M`. Then the **exact snapshot identity** is

    Σ_active d(Re z)/dt
      =M_dot E_A[cos φ]
       +M (Cov_A(cos φ, A_dot/A)−E_A[sin φ φ_dot]),
    M_dot=Σ_active A_dot.                          (P2)

This follows by expanding the covariance. The first covariance concerns **relative amplitude growth**, whereas the signed phase term involves `sin φ φ_dot`. An empirical `Cov_A(cos φ, |φ_dot|)` is a different diagnostic and does not carry a definite sign for (P2). For zero or near-zero triads the phase rate is undefined or unstable; retain their derivative `Σ_inactive Re z_dot` directly. The active set is held fixed when taking the snapshot derivative. A moving active threshold would need additional crossing terms for a time-integrated identity.

## Runnable Colab experiment

Open `notebooks/WP11_phase_rate_colab.ipynb` on the draft branch in Google Colab and run all cells. Or, from the repository root, run

    python3 src/wp11_phase_rate_audit.py --output /tmp/wp11_phase.json

The script evolves the existing combined perturbed initial state to `t=0.005` with `dt=0.0005`, `ν=0.1` at N=4 and N=7. It checks transfer reconstruction against `System.nonlinear`, the direct viscous phase null, (P1), (P2), and the derivative against a central directional finite difference of the exact cubic triad transfer. It emits the full rows and trapezoid-integrated **signed** high transfer. The covariance uses a relative phase floor `10⁻⁹`; the excluded derivative remains in the ledger. No presupposed decorrelation condition is used.

On the initial execution, the N=4 and N=7 signed high-advector integrals over this short window were approximately `−4.2174` and `+156.6725`. The largest normalized transfer reconstruction discrepancy was below `4.37e−15`; the phase-amplitude decomposition discrepancy was below `1.60e−16`; the direct viscous phase residual was below `1.46e−15`. The central-difference derivative's largest relative error was `2.73e−9`. These are **finite-cutoff, short-time** figures sensitive to initial data, resolution, K and quadrature. They cannot justify extending a sign, phase-muting rule, or bound to all cutoffs and all times.

## Falsification target

A proposed global cancellation argument must control the *total signed* `Σ Re z` on every prefix `[0,t]`, with a cutoff-independent bound obtained from independently controlled data. Equations (P1)–(P2) supply exact accounting but do not force fast phase rotation, a negative phase term, or a uniform lower bound on `|φ_dot|`; they also do not handle the changing analyticity radius of the positive-σ Gevrey gate. A phase velocity may vanish at a transfer maximum. Any integration-by-parts argument dividing by `φ_dot` must separately control its zeros, amplitude derivatives, boundary terms, and their cutoff dependence.

Related primary research on Fourier triad phase alignment in 3D Navier–Stokes includes D. Kang, B. Protas and M. D. Bustamante, *Alignments of Triad Phases in 1D Burgers and 3D Navier–Stokes Flows*, https://arxiv.org/abs/2105.09425. The present exercise uses a particular weighted ordered-triad diagnostic and makes no priority claim about triad phase analysis.
