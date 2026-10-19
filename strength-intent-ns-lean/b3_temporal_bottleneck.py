"""
STRENGTH Framework ? Branch B3 Multiscale Temporal Bottleneck Layer
Author: Prince Upadhyay
"""
import numpy as np

class B3TemporalBottleneckEngine:
    def __init__(self, input_dim=1, hidden_dim=32, fast_split_ratio=0.5):
        self.hidden_dim = hidden_dim
        self.fast_dim = int(hidden_dim * fast_split_ratio)
        self.slow_dim = hidden_dim - self.fast_dim
        rng = np.random.default_rng(20261017)
        self.W_xh = rng.normal(0.0, 1.0 / np.sqrt(input_dim), size=(input_dim, hidden_dim)).astype(np.float64)
        self.W_fast = rng.normal(0.0, 1.0 / np.sqrt(self.fast_dim), size=(self.fast_dim, self.fast_dim)).astype(np.float64)
        self.W_slow = np.eye(self.slow_dim, dtype=np.float64)

    def forward_pass(self, x_t, h_prev, xi_t):
        input_projected = np.dot(x_t, self.W_xh)
        h_fast_prev = h_prev[:, :self.fast_dim]
        h_slow_prev = h_prev[:, self.fast_dim:]
        h_fast_next = np.tanh(np.dot(h_fast_prev, self.W_fast) + input_projected[:, :self.fast_dim])
        h_slow_next = np.tanh(np.dot(h_slow_prev, self.W_slow) + input_projected[:, self.fast_dim:])
        return np.concatenate([h_fast_next, h_slow_next], axis=1) + xi_t
