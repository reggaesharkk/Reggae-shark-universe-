# Proof Ledger - LRSC Odd-Ring Spectral Rank Theorem v1.2

Author: Prince Upadhyay, Independent Research

## ESTABLISHED ANALYTICALLY

- Exact centered-carrier identity `X_t = 1 + A(-1)^t cos(pi t/M)`.
- Exact local shedding field: odd sites shed zero; even sites have the stated cosine-sum formula.
- Exact residue-class Fourier formulas for `M=4L+1` and `M=4L+3`.
- Non-vanishing `jhat_r != 0` for every odd `M>=9` and every integer `0<=r<(M-1)/2`.
- Chebyshev/Vandermonde independence of the first `p` pre-stencil channels when `p` active reflection orbits are present.
- Stencil injectivity on the masked channel span when at least one reflection orbit is inactive.
- Therefore `rank(V)=p` under the theorem assumptions.

## COMPUTATIONAL CORROBORATION

- Closed spatial formula checked against the original local-min operator.
- Simplified Fourier formulas checked over every odd ring `M=9,...,2001` (500,494 coefficients).
- Exact cyclotomic non-vanishing checks for all required coefficients at `M=99`, `M=101`, and `M=127`.
- The finite checks are not used as substitutes for the analytic proof.

## NOT CLAIMED

- No universal value of `K_tau`.
- No multi-step dynamical theorem.
- No microscopic physical law.
- No statement resolving the separate entropy-to-horizon bridge question.
