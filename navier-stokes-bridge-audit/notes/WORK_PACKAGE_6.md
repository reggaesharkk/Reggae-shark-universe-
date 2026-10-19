# Work Package 6: short-time finite Galerkin evolution

**23 September 2026 | Unforced periodic Navier–Stokes (B) | Numerical diagnostic**

## Aim and exact numerical model

Work Package 5 checked instantaneous Fourier fields. This package evolves
two of them for a short time under the finite Fourier Galerkin ODE,

`d a_k/dt = −P_k i Σ_{p+q=k}(q·a_p)a_q − ν|k|²a_k`, `|k|≤N`,

using all ordered pairs inside the cutoff, no FFT grid, and classical
fourth-order Runge–Kutta time stepping. Parameters: `N=4` (257 modes),
31,129 ordered convolution pairs, `ν=0.1`, low cutoff `K=2`,
`Δt=0.0025`, 40 steps, terminal time `t=0.1`. Initial data are the
line-like and cube Fourier supports at `L=2`, seed 20260923, normalized
to total energy one. `P_0=I`; the zero mode remains zero here.

The previously proved instantaneous bound,

`|Π_K(t)| ≤ √(2E_{≤K}(t)) C₂ ||u_N(t)||_{H²} ||∇u_N(t)||₂`, 

with `C₂≤6.530165700177883`, holds for every Galerkin state, so a
valid computation cannot break it. Tracking its ratio shows only the
slack of this sufficient bound along these short trajectories.

## Recorded results

| Initial Fourier support | E(0) → E(0.1) | Π₂(0) → Π₂(0.1) | `|Π₂|/bound` at 0 → 0.1 | Initially absent modes above amplitude 10⁻⁸ at 0.1 |
|---|---:|---:|---:|---:|
| Line-like, 44 modes | 1 → 0.961393 | +0.057406 → +0.083235 | 0.00071451 → 0.00109899 | 212 |
| Cube, 124 modes | 1 → 0.936637 | −0.022135 → +0.002037 | 0.00016357 → 0.00001683 | 132 |

Intermediate snapshots are in `evolution_results.json`. Both runs
preserve conjugate reality and Fourier incompressibility to numerical
precision. Full nonlinear energy transfer cancels to approximately
machine precision at each stored snapshot, and total energy decreases.
The largest single-step residual in the integrated energy balance is
about `2.44×10⁻⁹`; it includes time-discretization and trapezoidal
quadrature error. Repeating the same terminal time with `Δt=0.00125`
changed final energy by at most `1.71×10⁻¹²` and final low flux by at
most `3.77×10⁻¹³` (`evolution_convergence.json`).

## Interpretation

Nonlinear evolution immediately creates frequencies outside the initial
support, so an initial-support-only embedding constant is not invariant.
The line-like case's low-flux magnitude grows during this interval; the
cube case's signed low flux crosses zero. These are trajectory facts of
**one fixed 257-mode ODE**. They do not imply a physical-space filament,
a monotone cascade, a long-time bound, or a singularity. The analytical
H² bound is cutoff-independent as an *instantaneous inequality*, yet its
right-hand Sobolev norm remains uncontrolled for arbitrary unforced PDE
data over all time. Numerical agreement at two time steps does not
address convergence as `N→∞`.

## Decision

No logarithmic or Besov correction has been established. Such a proposal
must first define a norm and an explicit estimate, including the
dependencies of its constants, before a numerical test has meaning.
