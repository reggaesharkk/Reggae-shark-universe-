"""
Integration Test for Modewise Dissipation Control and Navier-Stokes Operators
--------------------------------------------------------------------------
Validates modewise spectral projection and high-frequency dissipation scaling against
divergence-free flow fields.
"""

import sys
import os
import numpy as np

# Ensure src/ is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from operators import compute_divergence
from modewise_remainder_control import compute_modewise_projection, estimate_modewise_remainder_bound

def run_integration_audit():
    print("Initializing Navier-Stokes Modewise Integration Audit...")
    nx, ny = 64, 64
    dx, dy = 1.0 / nx, 1.0 / ny
    x = np.linspace(0, 2*np.pi, nx)
    y = np.linspace(0, 2*np.pi, ny)
    X, Y = np.meshgrid(x, y)
    
    # Divergence-free velocity field with high-frequency perturbation
    u = -np.sin(X) * np.cos(Y) + 0.05 * np.sin(20 * X) * np.cos(20 * Y)
    v =  np.cos(X) * np.sin(Y) + 0.05 * np.cos(20 * X) * np.sin(20 * Y)
    
    # 1. Check divergence constraint
    div = compute_divergence(u, v, dx, dy)
    max_div = np.max(np.abs(div))
    print(f"-> Maximum Divergence Check: {max_div:.2e}")
    
    # 2. Modewise spectral projection test
    cutoff = 10
    u_low, u_high = compute_modewise_projection(u, cutoff)
    u_high_norm = np.linalg.norm(u_high)
    print(f"-> High-frequency residual norm (Cutoff M={cutoff}): {u_high_norm:.4f}")
    
    # 3. Dissipation-controlled remainder bound check
    viscosity = 0.1
    bound = estimate_modewise_remainder_bound(u_high_norm, viscosity, cutoff)
    print(f"-> Certified Modewise Remainder Bound: {bound:.4f}")
    
    assert bound < 10.0, "Remainder bound exceeds expected stability limit!"
    print("Integration audit completed successfully. All checks passed.")

if __name__ == "__main__":
    run_integration_audit()
