"""Seeded random holdout splitter for synthetic or caller-supplied IDs.

This utility does not check group independence, prevent leakage, or implement
cross-validation. Callers must ensure their own split protocol is valid.
"""
import math
from numbers import Real

import numpy as np

class H4RandomHoldoutSplitter:
    def __init__(self, total_networks=100, seed=20261017):
        if isinstance(total_networks, bool) or not isinstance(total_networks, int):
            raise TypeError("total_networks must be an integer")
        if total_networks < 2:
            raise ValueError("total_networks must be at least 2")
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self.total_networks = total_networks
        self.seed = seed

    def generate_random_holdout_split(self, train_ratio=0.8):
        if isinstance(train_ratio, bool) or not isinstance(train_ratio, Real):
            raise TypeError("train_ratio must be a real number")
        try:
            train_ratio = float(train_ratio)
        except (OverflowError, TypeError, ValueError) as exc:
            raise ValueError("train_ratio must be representable as a finite float") from exc
        if not math.isfinite(train_ratio) or not 0 < train_ratio < 1:
            raise ValueError("train_ratio must be finite and strictly between 0 and 1")

        rng = np.random.default_rng(self.seed)
        network_indices = np.arange(self.total_networks)
        rng.shuffle(network_indices)
        split_bound = int(self.total_networks * train_ratio)
        if not 0 < split_bound < self.total_networks:
            raise ValueError("train_ratio must leave at least one ID in each split")
        return network_indices[:split_bound], network_indices[split_bound:]

