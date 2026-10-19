# Navier–Stokes Work Package 1: sparse Fourier triad

Exploratory companion to `Navier_Stokes_Bridge_Audit_v0_1.md`, 23 September 2026.

## Run

```bash
python3 validate_sparse_triad.py
```

Requires Python 3 and NumPy. The recorded seeded output is `triad_results.json`.

## What is computed

`galerkin.py` implements the three-dimensional periodic Fourier Galerkin
operator with exact mode-pair convolution. The Leray projector is
`P_k = I - kkᵀ/|k|²` for nonzero k and the identity for the zero mode.
The wavevector cutoff is a ball in integer frequency space. No FFT grid or
wraparound is used. The Fourier normalization is specified in the module.

The sparse field uses the real-field-conjugate six-mode triad
`P=(1,0,0), Q=(0,1,1), R=P+Q=(1,1,1)` with seeded complex coefficients
orthogonally projected to divergence-free vectors. With `N=2`, `K=1.2`,
and `ν=0.07`, the script checks:

- reality conjugacy and divergence-free input/output;
- a separately enumerated two-pair formula for the nonlinear coefficient at P;
- total nonlinear energy cancellation at the full cutoff;
- equal and opposite low/high nonlinear transfer;
- the finite-cutoff energy derivative and viscous dissipation identity.

For this sample the signed low-mode flux is approximately `-2.30290648`.
Its sign shows transfer into the lowest selected shell at this instant. It
does not establish a directional cascade or any behavior over time.

## Falsified candidate

The script tests `|Π_K| ≤ C E_total` with an absolute constant C independent
of initial amplitude. Under `u → A u`, the instantaneous flux scales as
`A³` and the energy as `A²`. The nonzero triad flux thus disproves this
candidate for every finite universal C, even at fixed cutoff. At amplitude
scale 100, the tested `|Π_K|/E_total` is approximately 25.7774, disproving
the particular C=1 case directly. This does **not** rule out estimates whose
constants depend on the initial data, time, viscosity, or another norm.

## Interpretation and limit

The checks exercise finite-dimensional algebra and floating-point code. They
do not establish any bound uniform in resolution, global smoothness, or
breakdown for the three-dimensional Navier–Stokes PDE. The next attempt must
specify a nontrivial candidate bound with its exact dependence on initial
data, viscosity, cutoff, and time, then test scaling and triads before proof.

## Disjoint shells and a second falsifier

`validate_shells_and_dilation.py` computes signed nonlinear contributions to
three disjoint shells using `−Π_1.2`, `Π_1.2−Π_1.5`, and `Π_1.5−Π_2.0`.
The outputs are approximately `+2.30290648`, `+0.27677095`, and
`−2.57967743`; they sum to zero. These are instantaneous nonlinear
contributions; viscosity adds a separate negative term to each shell's
energy derivative.

The script also tests the stronger amplitude-consistent candidate
`|Π_K| ≤ C E_total^(3/2)` with C independent of Fourier cutoff. Spatial
frequency dilation `u(x) → u(mx)` keeps energy fixed and multiplies the
instantaneous flux by m, while the low cutoff K and full cutoff N also scale
by m. The ratio rises from `0.08624` at m=1 to `1.37988` at m=16. Since
m can be any positive integer, no finite universal C works. This does not
exclude bounds involving derivatives, viscosity, initial norms, or time.

The sparse-support convolution is valid for an instantaneous energy inner
product because absent Fourier modes have zero amplitude. It does not compute
their time derivatives; those modes can be generated immediately by the PDE.

## Review of the proposed Google example

Its Leray matrix formula is correct; `P_0=I` is a natural Fourier definition,
not an extra clause of Fefferman's problem statement. Its displayed triad
has **real** amplitudes, so multiplying by `i` yields purely imaginary inner
products and its proposed `real_transfer` is zero. All three wavevectors
have norm `sqrt(2)`, so a radial cutoff cannot put them in disjoint shells.
It calculates only one ordered convolution term; a real-valued velocity field
also requires conjugate modes and all admissible ordered pairs. Its method
mutates the same amplitudes at every scaling call, making `[1, 5, 25]`
cumulative factors `[1, 5, 125]`. The proposed linear envelope is not tied
to a stated scale-consistent PDE inequality. Our seeded six-mode example and
the two explicit falsifiers address those issues.
