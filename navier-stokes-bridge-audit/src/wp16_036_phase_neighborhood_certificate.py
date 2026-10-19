"""Conditional, deterministic phase-neighborhood certificate for the frozen K36 gate.

Inputs are the archived holdout and per-ordered-source magnitude-envelope files.
All state magnitudes and vector polarizations are fixed; only conjugate-symmetric
Fourier coefficient phases may change. This is not a trajectory certificate.
"""

import argparse
import json
from pathlib import Path


def certify(holdout, envelope):
    output = {"status": "post-hoc deterministic local phase certificate", "N": {}}
    for n in (12, 13):
        ei = envelope["N"][str(n)]["K36_envelope_total"]
        eo = envelope["N"][str(n)]["outside_envelope_total"]
        states = {}
        for name, row in holdout[n]["states"].items():
            s = row["k_channel_total_signed"]
            inside = row["frozen_K36_signed_contribution"]
            outside = s - inside
            ai = row["absolute_mass_captured"]
            ao = row["k_channel_total_abs_group_contribution"] - ai
            assert s > 0 and ai > 9 * ao and .2 * s > abs(outside)
            # Each ordered source acquires phase delta_k-delta_l-delta_r.
            # |exp(i theta)-1| <= |theta| <= 3 epsilon.
            signed_radius = (.2 * s - abs(outside)) / (3 * (eo + .2 * (ei + eo)))
            mass_radius = (ai / 9 - ao) / (3 * (eo + ei / 9))
            states[name] = {
                "signed_margin": .2 * s - abs(outside),
                "absolute_mass_margin": ai / 9 - ao,
                "signed_gate_radius_radians": signed_radius,
                "mass_gate_radius_radians": mass_radius,
                "joint_radius_radians": min(signed_radius, mass_radius),
                "joint_triad_defect_radius_radians": 3 * min(signed_radius, mass_radius),
                "cancellation_ratio": abs(s) / row["k_channel_total_abs_group_contribution"],
            }
        output["N"][str(n)] = {"K36_envelope": ei, "outside_envelope": eo, "states": states}
    output["minimum_joint_radius_radians"] = min(
        d["joint_radius_radians"] for n in output["N"].values() for d in n["states"].values()
    )
    output["minimum_joint_triad_defect_radius_radians"] = 3 * output["minimum_joint_radius_radians"]
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n12-holdout", type=Path, required=True)
    parser.add_argument("--n13-holdout", type=Path, required=True)
    parser.add_argument("--envelope", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    a = parser.parse_args()
    inputs = [json.loads(p.read_text()) for p in (a.n12_holdout, a.n13_holdout, a.envelope)]
    result = certify({12: inputs[0], 13: inputs[1]}, inputs[2])
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print("minimum joint radius (radians):", result["minimum_joint_radius_radians"])


if __name__ == "__main__":
    main()
