#!/usr/bin/env python3
import hashlib
import json
import math
from numbers import Real

class StrengthIntentNSEngine:
    def __init__(self):
        self.version = "v5.0.1"
        self.author = "Prince Upadhyay"
        self.a2_bound = 0.184920
        self.lipschitz_ceiling = 49123.01
        self.strain_threshold = 39453.02

    def audit_state(self, velocity: float, strain: float) -> dict:
        values = {"velocity": velocity, "strain": strain}
        for name, value in values.items():
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(f"{name} must be a real number")
            try:
                numeric_value = float(value)
            except (OverflowError, TypeError, ValueError) as exc:
                raise ValueError(f"{name} must be representable as a finite float") from exc
            if not math.isfinite(numeric_value):
                raise ValueError(f"{name} must be finite")
            if numeric_value < 0:
                raise ValueError(f"{name} must be non-negative")
            values[name] = numeric_value

        velocity = values["velocity"]
        strain = values["strain"]
        if strain > self.strain_threshold:
            raise ValueError(
                f"[BOUND_CHECK_FAILED] Strain {strain} exceeds configured threshold "
                f"{self.strain_threshold}"
            )

        contracted_val = velocity * self.a2_bound
        if contracted_val > self.lipschitz_ceiling:
            raise ValueError(
                f"[BOUND_CHECK_FAILED] Contracted value {contracted_val} exceeds "
                f"configured ceiling {self.lipschitz_ceiling}"
            )

        payload = {
            "framework": "STRENGTH-INTENT-NS-LEAN",
            "version": self.version,
            "velocity": velocity,
            "strain": strain,
            "contracted_value": contracted_val,
            "arithmetic": "Python float (binary64)",
            "status": "BOUNDS_CHECKED_ONLY"
        }
        
        canonical_str = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
        
        return {
            "payload": payload,
            "integrity_digest_sha256": digest,
            "authentication": "none"
        }

if __name__ == '__main__':
    engine = StrengthIntentNSEngine()
    result = engine.audit_state(velocity=12500.5, strain=1420.0)
    print(json.dumps(result, indent=2))

