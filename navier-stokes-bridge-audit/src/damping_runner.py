"""
Automated High-Frequency Damping & Dissipation Runner
-----------------------------------------------------
Systematically evaluates modewise remainder bounds across varying spectral 
cutoffs (M) and viscosities to verify robust damping behavior for PR #155.
"""

import numpy as np

def evaluate_damping_sweep(nx=64, ny=64):
    print("Running Automated High-Frequency Damping & Dissipation Sweep...")
    
    # Generate synthetic multi-scale field
    x = np.linspace(0, 2*np.pi, nx)
    y = np.linspace(0, 2*np.pi, ny)
    X, Y = np.meshgrid(x, y)
    
    u = -np.sin(X) * np.cos(Y) + 0.08 * np.sin(18 * X) * np.cos(18 * Y)
    u_fft = np.fft.fft2(u)
    
    viscosities = [0.01, 0.05, 0.1, 0.5]
    cutoffs = [4, 8, 12, 16]
    
    print(f"{'Viscosity (v)':<15} | {'Cutoff (M)':<12} | {'High-Freq Norm':<18} | {'Remainder Bound':<15}")
    print("-" * 68)
    
    for nu in viscosities:
        for M in cutoffs:
            ny_dim, nx_dim = u.shape
            ky = np.fft.fftfreq(ny_dim, d=1.0/ny_dim)
            kx = np.fft.fftfreq(nx_dim, d=1.0/nx_dim)
            KX, KY = np.meshgrid(kx, ky)
            mask_high = np.sqrt(KX**2 + KY**2) > M
            
            u_high = np.real(np.ifft2(u_fft * mask_high))
            u_high_norm = np.linalg.norm(u_high)
            
            dissipation_rate = nu * (M ** 2)
            bound = u_high_norm / max(dissipation_rate, 1e-8)
            
            print(f"{nu:<15.2f} | {M:<12} | {u_high_norm:<18.4f} | {bound:<15.4f}")

if __name__ == "__main__":
    evaluate_damping_sweep()
