"""
Independent, from-scratch reconstruction of the LRSC v1.1.1 operator and closure check.

This script does not import, call, or reuse any code from the author's
LRSC_v1_1_1_Source_Bundle (audit_k1_to_k10.py / exhaustive_search.cpp). It implements
the operator from the stated specification only (M=99, k_idx=49, theta=0.08, A=0.50,
normalized forward DFT, 50 conjugate-balanced channels with DC counted as channel 0).

It also derives the quadratic-form coefficients (linear term + pairwise Gram matrix)
for the squared relative residual ||E - sum_{i in S} V_i||^2 using DIRECT COMPLEX inner
products (numpy vdot/conj), not the real/imaginary-concatenation trick the author's
script uses. The two derivations are mathematically equivalent but were implemented
independently here.

Output: writes channels.bin (binary, read by the independent C search program) and
prints N_act and the closure check.
"""
import struct
import numpy as np

M, K_IDX, THETA, A = 99, 49, 0.08, 0.50
N_CHANNELS = 50


def build():
    idx = np.arange(M)
    kappa = 2.0 * np.pi * K_IDX / M
    X = 1.0 + A * np.cos(kappa * idx)
    left, right = np.roll(X, 1), np.roll(X, -1)
    j = X - np.minimum(np.minimum(left, X), right)
    stress = 0.5 * ((X - left) ** 2 + (X - right) ** 2)
    mask = (stress > THETA).astype(np.float64)

    m_hat = np.fft.fft(mask) / M
    j_hat = np.fft.fft(j) / M
    y_hat = np.fft.fft(mask * j) / M

    q = np.arange(M)
    stencil = np.cos(2.0 * np.pi * q / M) - 1.0
    E = stencil * y_hat  # target spectrum

    V = np.zeros((N_CHANNELS, M), dtype=np.complex128)
    V[0] = stencil * (j_hat[0] * m_hat)
    for r in range(1, N_CHANNELS):
        rc = M - r
        V[r] = stencil * (j_hat[r] * np.roll(m_hat, r) + j_hat[rc] * np.roll(m_hat, rc))

    return X, mask, E, V


def direct_residual(E, V, subset):
    resid = E - V[list(subset)].sum(axis=0)
    return float(np.linalg.norm(resid) / np.linalg.norm(E))


def quadratic_coefficients(E, V):
    """
    ||E - sum_i V_i||^2 = ||E||^2 - 2 Re<E, sum V_i> + ||sum V_i||^2
                        = ||E||^2 + sum_i lin[i] + sum_{i<j} 2*gram[i][j]
    where  lin[i]    = ||V_i||^2 - 2 Re<E, V_i>
           gram[i][j] = Re<V_i, V_j>                (i != j)
    using the standard complex inner product <a,b> = sum_q a_q * conj(b_q).
    Derived directly from complex arrays (no real/imag stacking).
    """
    n_ch = V.shape[0]
    lin = np.empty(n_ch, dtype=np.float64)
    for r in range(n_ch):
        lin[r] = np.real(np.vdot(V[r], V[r])) - 2.0 * np.real(np.vdot(E, V[r]))
    gram = np.zeros((n_ch, n_ch), dtype=np.float64)
    for a in range(n_ch):
        for b in range(a + 1, n_ch):
            g = np.real(np.vdot(V[a], V[b]))
            gram[a, b] = g
            gram[b, a] = g
    const = float(np.real(np.vdot(E, E)))
    return const, lin, gram


if __name__ == "__main__":
    X, mask, E, V = build()
    norm_E = np.linalg.norm(E)
    closure = np.linalg.norm(E - V.sum(axis=0)) / norm_E
    n_act = int(mask.sum())
    print(f"N_act = {n_act}")
    print(f"closure_relative = {closure:.17g}")

    const, lin, gram = quadratic_coefficients(E, V)

    # sanity: quadratic form must reproduce a few direct residuals
    for S in [(49,), (48, 49), (0, 1, 49), (0, 1, 45, 46, 47, 48, 49)]:
        q_val = const + sum(lin[i] for i in S)
        for a in range(len(S)):
            for b in range(a + 1, len(S)):
                q_val += 2.0 * gram[S[a], S[b]]
        q_err = (max(q_val, 0.0) ** 0.5) / norm_E
        d_err = direct_residual(E, V, S)
        assert abs(q_err - d_err) < 1e-10, (S, q_err, d_err)
    print("quadratic-form sanity checks against direct complex reconstruction: OK")

    with open("channels.bin", "wb") as f:
        f.write(struct.pack("<d", norm_E))
        f.write(struct.pack("<d", const))
        f.write(struct.pack(f"<{N_CHANNELS}d", *lin))
        f.write(struct.pack(f"<{N_CHANNELS*N_CHANNELS}d", *gram.flatten()))
        # also store E and V (real/imag interleaved) for the C program's OWN
        # direct-reconstruction cross-check (independent of the quadratic form)
        f.write(struct.pack(f"<{M}d", *E.real))
        f.write(struct.pack(f"<{M}d", *E.imag))
        for r in range(N_CHANNELS):
            f.write(struct.pack(f"<{M}d", *V[r].real))
            f.write(struct.pack(f"<{M}d", *V[r].imag))
    print("wrote channels.bin")
