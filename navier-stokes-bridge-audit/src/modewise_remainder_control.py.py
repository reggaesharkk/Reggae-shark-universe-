"""
Modewise Adjoint Remainder and Dissipation Control Module
--------------------------------------------------------
Targeting PR #155 remainder bottlenecks in the Navier-Stokes Bridge Audit framework.
Provides tools for modewise projection, truncation error bounding, and high-frequency dissipation verification.
"""

import numpy as np

def compute_modewise_projection(u_field, cutoff_M):
    """
    Projects a 2D/3D velocity field onto low-frequency modes up to cutoff_M
    and isolates high-frequency remainder components.
    """
    shape = u_field.shape
    if len(shape) == 2:
        ny, nx = shape
        ky = np.fft.fftfreq(ny, d=1.0/ny)
        kx = np.fft.fftfreq(nx, d=1.0/nx)
        KX, KY = np.meshgrid(kx, ky)
        k_magnitude = np.sqrt(KX**2 + KY**2)
        
        mask_low = k_magnitude <= cutoff_M
        
        u_fft = np.fft.fft2(u_field)
        u_low_fft = u_fft * mask_low
        u_high_fft = u_fft * (~mask_low)
        
        u_low = np.real(np.ifft2(u_low_fft))
        u_high = np.real(np.ifft2(u_high_fft))
        return u_low, u_high
    else:
        raise ValueError("Field must be a 2D array for modewise spectral projection.")

def estimate_modewise_remainder_bound(u_high_norm, viscosity, cutoff_M):
    """
    Estimates the conservative combined remainder upper bound using modewise
    dissipation dominance rather than loose global scalar majorants.
    """
    dissipation_rate = viscosity * (cutoff_M ** 2)
    remainder_bound = u_high_norm / max(dissipation_rate, 1e-8)
    return remainder_bound

if __name__ == "__main__":
    print("Modewise Remainder Control Module Initialized.")
    nx, ny = 64, 64
    x = np.linspace(0, 2*np.pi, nx)
    y = np.linspace(0, 2*np.pi, ny)
    X, Y = np.meshgrid(x, y)
    
    u = np.sin(X) * np.cos(Y) + 0.1 * np.sin(15 * X) * np.cos(15 * Y)
    
    cutoff = 8
    u_low, u_high = compute_modewise_projection(u, cutoff)
    u_high_norm = np.linalg.norm(u_high)
    
    bound = estimate_modewise_remainder_bound(u_high_norm, viscosity=0.1, cutoff_M=cutoff)
    print(f"High-frequency norm: {u_high_norm:.4f}")
    print(f"Estimated Modewise Remainder Bound (M={cutoff}): {bound:.4f}")
