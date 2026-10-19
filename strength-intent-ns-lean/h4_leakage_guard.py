"""
STRENGTH Framework ? H4 Cross-Validation Data Leakage Guard
Author: Prince Upadhyay
"""
import numpy as np

class H4PredictiveDataSplitter:
    def __init__(self, total_networks=100, seed=20261017):
        self.total_networks = total_networks
        self.seed = seed
        
    def generate_orthogonal_cross_validation_splits(self, train_ratio=0.8):
        rng = np.random.default_rng(self.seed)
        network_indices = np.arange(self.total_networks)
        rng.shuffle(network_indices)
        split_bound = int(self.total_networks * train_ratio)
        return network_indices[:split_bound], network_indices[split_bound:]
