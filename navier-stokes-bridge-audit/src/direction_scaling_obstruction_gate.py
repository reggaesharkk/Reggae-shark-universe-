"""Concentration scaling obstruction for a normalized direction-slope candidate.

Reads the local direction-depletion results and converts the smallest-offset
weighted angular/determinant ratios into finite-difference slopes L~D(h)/|h|
and scale-normalized ratios Q=L/sqrt(G).

The accompanying note gives the exact fixed-energy concentration scaling:
L -> lambda L, G -> lambda^2 G, hence Q is invariant, while
T/G^(3/2) -> lambda^(3/2) T/G^(3/2).
"""

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run():
    prior = json.loads(
        (HERE / "direction_depletion_results.json").read_text(encoding="utf-8")
    )

    rows = []
    for case in prior["rows"]:
        samples = []
        for snap in case["samples"]:
            smallest = snap["scales"][0]
            radius = smallest["radius"]
            G = snap["G"]

            L_ang = smallest["angular_ratio"] / radius
            L_det = smallest["determinant_ratio"] / radius
            sqrtG = math.sqrt(G)

            samples.append(dict(
                time=snap["time"],
                G=G,
                T=snap["T"],
                L_ang=L_ang,
                L_det=L_det,
                Q_ang=L_ang/sqrtG,
                Q_det=L_det/sqrtG,
                T_over_G32=(snap["T"]/(G**1.5) if G else 0.0),
            ))

        rows.append(dict(
            scenario=case["scenario"],
            N=case["N"],
            samples=samples,
        ))

    return dict(
        source="direction_depletion_results.json",
        smallest_offset=prior["rows"][0]["samples"][0]["scales"][0]["radius"],
        exact_concentration_scaling={
            "map":"u_lambda(x)=lambda^(3/2) v(lambda x), fixed L2 energy",
            "omega":"lambda^(5/2)",
            "G":"lambda^2",
            "T":"lambda^(9/2)",
            "L_direction":"lambda",
            "Q_direction_equals_L_over_sqrtG":"lambda^0",
            "T_over_G32":"lambda^(3/2)",
        },
        obstruction=(
            "Any proposed bound T <= C(Q_direction,E0) G^(3/2), with fixed "
            "energy E0 and C depending only on the concentration-invariant "
            "Q_direction, is incompatible with the fixed-energy concentration "
            "family whenever the base field has positive stretching."
        ),
        limitation=(
            "The finite-grid L values are diagnostic weighted slopes, not the "
            "supremum modulus in the Constantin-Fefferman theorem. The analytic "
            "obstruction concerns the scaling class of any L/sqrt(G)-type "
            "normalization, not that theorem itself."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "direction_scaling_obstruction_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
