# Riesz strain and spatial stretching concentration (post-v0.2)

## Question and independent identity

The preceding alignment audit found that the signed ratio (T/M) rises at sampled early times. Where in physical space does its positive stretching occur? A spatial diagnostic should preserve the full strain–vorticity coupling without choosing an eigenvector frame.

For nonzero Fourier wavevectors (k), (\widehat\omega=i k\times\widehat u), and incompressibility implies

\[
\widehat S_{ij}(k)=-\frac{k_j(k\times\widehat\omega)_i+k_i(k\times\widehat\omega)_j}{2|k|^2}.
\]

The zero mode of (S) is zero. `src/riesz_stretching_gate.py` reconstructs (S) using this Fourier multiplier and independently reconstructs (S) by differentiating the velocity. Their maximum pointwise discrepancy is below the asserted (10^{-10}) tolerance for every snapshot. The spatial (T=\langle\omega\cdot S\omega\rangle) also agrees with the Galerkin convolution transfer to numerical precision. This is an implementation check on two equivalent formulas, not a new estimate.

## Prespecified localization diagnostic

At each snapshot, call the 10% of physical-grid points with the largest (|\omega|^2) the *high-vorticity region*. Compute its share of (G), its share of the positive local stretching (P=\langle(\omega\cdot S\omega)_+\rangle), and its contribution to signed (T). The region changes with time and cutoff; the percentile is descriptive, not a universal threshold. The negative local stretching is retained explicitly, so large positive and negative terms cannot masquerade as a small net (T).

| Field | (N) | Time | High-region share of (G) | High-region share of (P) | Total signed (T) | Signed (T) in high region | Signed (T) outside |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Reference | 4 | 0 | .2846 | .5589 | 179.784 | 385.019 | −205.236 |
| Reference | 4 | .02 | .2937 | .6428 | 544.026 | 615.293 | −71.266 |
| Reference | 7 | .02 | .3193 | .7160 | 728.563 | 794.515 | −65.952 |
| Combined | 4 | 0 | .2921 | .3795 | ≈0 | 1703.656 | −1703.656 |
| Combined | 4 | .02 | .3191 | .4739 | 3939.380 | 4130.118 | −190.738 |
| Combined | 7 | .02 | .3384 | .5573 | 18151.283 | 12367.170 | 5784.113 |

The high-vorticity region's share of positive local stretching rises over this interval in these runs. The reference (N=7) endpoint has positive signed stretching in that region and negative signed stretching outside it; the combined (N=7) endpoint has positive signed contributions in both regions. The initial combined case has nearly zero global transfer because positive and negative spatial contributions cancel, even though their magnitudes are large.

Endpoint cross-grid checks compare (32^3) and (48^3) evaluations. The change in the high-region share of (P) is −.00468 (reference (N=4)), +.01615 (reference (N=7)), −.00256 (combined (N=4)), and −.00237 (combined (N=7)). The signed (T) agrees to roundoff across grids because it is a cubic trigonometric integral here; the percentile and positive-part statistics are not trigonometric polynomials and have measurable grid error. The 1.6 percentage point difference for reference (N=7) cautions against reading small differences in the reported concentration shares as physically decisive.

## Analytical boundary

These are two times, two initial conditions, two cutoffs, and a moving mask. They cannot establish persistent concentration, a vortex-direction regularity criterion, or a cutoff-uniform time-integrated bound. The Riesz transform is nonlocal, so its exact reconstruction cannot be converted into a bound merely by localizing positive stretching. An independently derived estimate, uniform for arbitrary smooth initial data and cutoffs, is still needed. In particular, defining (\int (T)_+/G) from the observed solution is only a growth diagnostic until its finiteness is bounded from known data and proved inequalities.

Reproduce from the repository root with `python src/riesz_stretching_gate.py`. Data: `src/riesz_stretching_results.json`.
