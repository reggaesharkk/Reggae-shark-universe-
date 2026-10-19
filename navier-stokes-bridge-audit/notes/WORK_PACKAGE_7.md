# Work Package 7: spectral shell transfer geometry

**23 September 2026 | Unforced periodic Navier–Stokes (B) | Exact finite-cutoff diagnostic**

## Transfer convention and correction

Use the Work Package 6 terminal fields at `t=0.1` in the 257-mode
`N=4` Galerkin system. Partition nonzero Fourier wavevectors into four
shells: `(0,1]`, `(1,2]`, `(2,3]`, `(3,4]` by their Euclidean norm.
There are no `(4,8]` or `(8,16]` modes at this cutoff.

For `k=p+q`, define a *recipient* k, a *donor* p, and an *advecting*
mode q. The signed triadic energy rate into k from p, mediated by q, is

`τ(k←p | q) = −Re { i (p·a_q) [conj(a_k)·P_k a_p] }`.

Since `a_k` is divergence free, `conj(a_k)·P_k a_p=conj(a_k)·a_p`.
Summing τ over recipient, donor, and advector shells gives `T[n,m,l]`.
**Positive** `T[n,m,l]` means energy enters shell n from shell m by
interactions mediated by shell l. The exchange with recipient and donor
reversed uses `−q`; reality (`a_{−q}=conj(a_q)`) and incompressibility
give `T[n,m,l]=−T[m,n,l]`. The same statement holds after summing l to
the pair matrix `T[n,m]`.

This donor-assigned, unsymmetrized transfer definition matters. The
proposed symmetrized `P_ijl(k)` expression omits normalization and does
not, without a donor convention, establish the claimed pairwise
antisymmetry. The physical-space cubic-*gradient* integral belongs to
the enstrophy budget. Here the independent energy check is
`−∫u_shell·(u·∇)u dx`.

## Finite results

The table reports net nonlinear energy contribution to each shell,
excluding viscous dissipation. Values add to zero within each row.

| Initial support | `(0,1]` | `(1,2]` | `(2,3]` | `(3,4]` |
|---|---:|---:|---:|---:|
| Line-like | −0.07315623 | −0.01007878 | +0.07346371 | +0.00977130 |
| Cube | +0.04857267 | −0.05060963 | −0.05079837 | +0.05283533 |

For the line-like run, pair transfers include `+0.07535419` from
shell `(0,1]` to `(1,2]`, `+0.08272785` from `(1,2]` to `(2,3]`,
and `+0.00718298` from `(2,3]` to `(3,4]`, alongside smaller reverse
and nonadjacent exchanges. For the cube run, the lowest shell receives
about `+0.02473198` from `(1,2]` and `+0.02374210` from `(2,3]`, while
the `(3,4]` shell receives `+0.04838615` from `(2,3]`. Thus the cube
case has simultaneous transfers in both directions across different
shell pairs. The complete signed 4×4 pair matrices and 4×4×4 tensors
are in `shell_transfer_results.json`.

## Independent checks

All 31,129 ordered Fourier convolution pairs were evaluated without
FFT-grid aliasing. The maximum error in `T[n,m,l]+T[m,n,l]` was
`2.1×10⁻¹⁷`. The sum of `T[n,m,l]` at each recipient shell agreed with
the direct Galerkin `−Re Σ conj(a_k)·N_k` budget to roundoff.

An independently computed 32³-point physical-space trigonometric
quadrature of `−∫u_shell·(u·∇)u` agreed to at most `3.5×10⁻¹⁷`.
Here each input has coordinate frequency at most 4, so the cubic
integrand's coordinate frequency has magnitude at most 12; the
32-point grid resolves its exact periodic mean without aliasing,
apart from floating-point error. These are consistency checks for a
fixed finite Galerkin state, not an infinite-resolution theorem.

## Limits

These transfers are instantaneous at `t=0.1`. Their signs depend on
the velocity field, shell edges, and donor convention. The data do not
show a statistically or temporally persistent cascade, and they do not
explain *why* any geometry universally channels energy efficiently.
No all-time smoothness or breakdown result follows. The zero mode is
absent from these data; a nonzero mean velocity would require it to be
handled explicitly in the decomposition.
