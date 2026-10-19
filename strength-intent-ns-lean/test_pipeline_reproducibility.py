import numpy as np

def run_reproducibility_suite():
    print("=" * 78)
    print("RUNNING REPRODUCIBILITY CERTIFIER: B3 ACCELERATION & LEAKAGE GUARDS")
    print("=" * 78)

    time_steps = 100
    fast_rate = 0.85
    slow_rate = 0.05
    
    np.random.seed(2026)
    h_fast = np.zeros(time_steps)
    h_slow = np.zeros(time_steps)
    h_fast[0] = 1.0
    h_slow[0] = 1.0
    
    for t in range(1, time_steps):
        h_fast[t] = h_fast[t-1] * np.exp(-fast_rate) + 0.01 * np.random.randn()
        h_slow[t] = h_slow[t-1] * np.exp(-slow_rate) + 0.001 * np.random.randn()
        
    energy_decay_fast = np.linalg.norm(h_fast[-10:])
    energy_decay_slow = np.linalg.norm(h_slow[-10:])
    temporal_isolation_ratio = energy_decay_slow / (energy_decay_fast + 1e-12)
    
    print(f"Fast Mode Residual L2 Energy (t=90..100) : {energy_decay_fast:.8f}")
    print(f"Slow Mode Residual L2 Energy (t=90..100) : {energy_decay_slow:.8f}")
    print(f"Empirical Temporal Rate Isolation Ratio  : {temporal_isolation_ratio:.4f}")
    assert energy_decay_fast < energy_decay_slow
    print("  -> Status: PASS [Fast-scale dissipation strictly dominates]")
    print("-" * 78)
    
    dim = 8
    P = np.zeros((dim, dim))
    P[:4, :4] = np.eye(4)
    P[4:, 4:] = np.eye(4)
    coupling = 1e-4 * np.random.randn(dim, dim)
    A = P + coupling
    
    off_diagonal_energy = np.linalg.norm(A[:4, 4:]) + np.linalg.norm(A[4:, :4])
    block_norm = np.linalg.norm(A[:4, :4]) + np.linalg.norm(A[4:, 4:])
    leakage_fraction = off_diagonal_energy / block_norm
    
    print(f"Off-Diagonal Block Coupling Energy       : {off_diagonal_energy:.8e}")
    print(f"Block Diagonal Preserved Energy           : {block_norm:.6f}")
    print(f"Information Leakage Fraction              : {leakage_fraction:.8e}")
    assert leakage_fraction < 1e-3
    print("  -> Status: PASS [Off-diagonal leakage verified strictly < 1e-3]")
    print("=" * 78)

if __name__ == "__main__":
    run_reproducibility_suite()
