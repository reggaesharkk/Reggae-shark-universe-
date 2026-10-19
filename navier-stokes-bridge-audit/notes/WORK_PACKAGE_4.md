# Work Package 4: fractional Sobolev flux bound and growing networks

**23 September 2026 | Unforced periodic Navier–Stokes (B) | Exploratory audit**

## Candidate and exact proof

Use the `[0,2π)^3` Fourier convention and volume-normalized norms from the
earlier work packages. Let `P_N` be a Galerkin cutoff and `P_{≤K}` the
orthogonal low-frequency projector, where `K≤N`. Let `E_{≤K}` be half the
low-mode L² norm squared and `Π_K` its signed nonlinear flux. For `s>3/2`,

`|Π_K| ≤ √(2E_{≤K}) C_s ||u_N||_{H^s} ||∇u_N||₂`,

where `C_s = [Σ_{k∈Z³}(1+|k|²)^(−s)]^(1/2) < ∞`. The same C_s works for
every cutoff N and every shell boundary K.

Proof: orthogonal projection cannot increase the L² norm, so

`|Π_K| ≤ ||P_{≤K}u_N||₂ ||P_N P[(u_N·∇)u_N]||₂
        ≤ ||P_{≤K}u_N||₂ ||u_N||∞ ||∇u_N||₂`.

Pointwise Fourier Cauchy–Schwarz gives `||u_N||∞≤C_s||u_N||_{H^s}`.
The lattice series converges in three dimensions exactly when `s>3/2`.
This is a standard, fairly loose estimate. For `s=2`, the earlier explicit
lattice bound yields `C₂≤√(1+4π²+π⁴/45)≈6.530165700177883`.

The bound is cubic in velocity amplitude, so the Work Package 1 amplitude
counterexample does not touch it. Under `u(x)→u(mx)` at fixed amplitude,
its right side can grow as `m^(s+1)` while the tested energy flux grows
as m. This bound survives that frequency test, but it neither keeps the
H^s norm bounded over time nor proves arbitrary-data global smoothness.

## Why `s>1` was too broad for this mechanism

The suggested range `s>1` includes `1<s≤3/2`. In that range the full
three-dimensional lattice embedding constant above diverges with N.
At `s=3/2` it grows logarithmically at the level of its square, and at
`s<3/2` it grows by a power. The script lists truncated constants for
`s=1, 1.5, 2` at cutoffs `N=2,4,8,16`; these values illustrate the
trend, while convergence/divergence follows from lattice-point counting.
Other estimates at lower regularity may exist; the failure here is only
for this direct L∞ embedding route.

## Network stress test

`validate_network_hs.py` builds real-valued, divergence-free seeded
Fourier fields with all nonzero modes in cubes of radii `L=1,2,3`,
containing 26, 124, and 342 modes. Each field has total energy one.
All ordered interacting pairs are evaluated at occupied output modes;
this suffices for an *instantaneous* flux inner product, while absent
modes can acquire nonzero derivatives under the full equation.

Nine runs (three seeds at each radius) checked the H² bound and full
nonlinear energy cancellation. The largest observed ratio of actual
low-mode flux to the explicit upper bound is about `0.00191` in this
sample; this bound is very loose. The growing field does **not** show
monotonic flux in the sampled seeds. Random sampling cannot establish a
maximum or certify a universal inequality; the analytic proof above
establishes it independently.

The first implementation failed an energy-cancellation check because a
floating-point expression for the outer-radius cutoff rounded just below
the squared norm of a corner mode. The corrected script adds `1e−9` to
that diagnostic full cutoff; its low cutoff and convolution are unchanged.

## Research verdict

**A cutoff-independent flux inequality survives, but it is classical and
requires an uncontrolled higher Sobolev norm.** No log-Lipschitz weight
was introduced: the proposal did not specify a justified operator or
inequality for it. To make progress on unforced (B), a new mechanism must
control the time evolution of a suitable critical or subcritical norm for
arbitrary smooth data, or yield a genuine smooth-data breakdown example.
The expanding-network testbed can falsify proposed mechanisms; it cannot
establish that missing all-time control by itself.
