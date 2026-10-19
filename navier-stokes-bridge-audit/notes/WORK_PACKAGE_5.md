# Work Package 5: anisotropic Fourier support

**23 September 2026 | Unforced periodic Navier–Stokes (B) | Diagnostic only**

## Correction to the motivating summary

The Work Package 4 estimate uses `||u||∞≤C_s||u||_{H^s}` for `s>3/2`
on the three-dimensional torus. It does **not** control `||∇u||∞`.
Applying the same Fourier Cauchy–Schwarz argument to the gradient has
constant squared `Σ_k |k|²/(1+|k|²)^s`, finite only for `s>5/2`.
The new script lists truncated versions for `s=2, 2.5, 3`; it is the
lattice-series argument, not the finite list, that proves the threshold.

## Test design

At radii `L=2,3,4`, generate conjugate-symmetric divergence-free modes
in three frequency-space supports:

| Support | Wavevector restriction | Modes at L=2,3,4 |
|---|---|---|
| Line-like | `|i|≤L`, `|j|,|k|≤1` | 44, 62, 80 |
| Slab-like | `|i|,|j|≤L`, `|k|≤1` | 74, 146, 242 |
| Cube | `|i|,|j|,|k|≤L` | 124, 342, 728 |

These names describe **Fourier support**, not a physical-space filament
or fluid vortex. Normalize each field to total energy one, use two fixed
seeds for each of the nine geometry/size pairs, and compute exact ordered
convolutions at occupied output modes for the instantaneous low-shell
flux with `K=L`.

The cutoff-independent inequality from Work Package 4 is

`|Π_K| ≤ √(2E_{≤K}) C₂ ||u||_{H²} ||∇u||₂`, with
`C₂≤√(1+4π²+π⁴/45)≈6.53017`.

An anisotropic support cannot invalidate this proved all-field bound.
The script checks the bound, conservation over the full occupied
support, and a tighter **instantaneous-only** support constant obtained
by summing Fourier weights over occupied modes. This smaller constant
cannot be assumed to remain valid later because nonlinear evolution
creates modes outside the initial support.

## Results

All 18 checks passed. Across the sampled fields, the largest ratio of
actual low-shell flux to the global H² bound was about `0.000715`
(line-like support, L=2, first seed). Absolute flux did not increase
monotonically as the support grew, and no geometry yielded a violation.
The ratios are small because the universal embedding constant and
three-norm product are loose; they are **not** estimates of optimal
constants or of long-time behavior. Results and seeds are in
`anisotropic_results.json`.

## Verdict

The analytic bound survives every support geometry by proof; the finite
examples show only how loose it is for these inputs. The data offer no
evidence for a new invariant anisotropic support condition. An improved
candidate would need a precise mechanism that remains stable when
nonlinear interactions create new modes, and would still need all-time
control for arbitrary smooth initial data. No Besov or log-Lipschitz
criterion is claimed by this work package.
