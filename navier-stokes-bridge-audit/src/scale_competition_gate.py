"""Scale-competition diagnostic between sampled coherence radius and vorticity-gradient length.

Joins the high-vorticity coherence-radius summary to the already-recorded
Galerkin G,D,T traces. Defines ell_omega=sqrt(G/D) and the sampled ratio
R_sample=rho_upper_sample/ell_omega.

Important: rho_upper_sample is an upper bound on an admissible sampled
coherence radius, not a certified lower bound. Therefore R_sample>1 is not a
regularity margin and does not imply geometric safety.
"""

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
NU = 0.1
TARGET_SCENARIOS = {"reference", "combined_double_quarter_high"}
TARGET_CUTOFFS = {4, 7}
TARGET_TIMES = {0.0, 0.005, 0.01, 0.015}


def load_traces():
    rows = {}
    for filename in ("candidate_inequality_results.json",
                     "candidate_inequality_N7_results.json"):
        data = json.loads((HERE / filename).read_text(encoding="utf-8"))
        for run in data["runs"]:
            scenario, N = run["scenario"], run["N"]
            if scenario not in TARGET_SCENARIOS or N not in TARGET_CUTOFFS:
                continue
            # sample columns:
            # time,E,G,D,T,high_G_fraction,required_C
            rows[(scenario, N)] = {
                round(sample[0], 12): dict(
                    time=sample[0],
                    G=sample[2],
                    D=sample[3],
                    T=sample[4],
                )
                for sample in run["samples"]
                if round(sample[0], 12) in TARGET_TIMES
            }
    return rows


def run():
    coherence = json.loads(
        (HERE / "high_vorticity_coherence_radius_verified_summary.json")
        .read_text(encoding="utf-8")
    )
    traces = load_traces()

    output = []
    for case in coherence["rows"]:
        scenario, N = case["scenario"], case["N"]
        if (scenario, N) not in traces:
            continue

        samples = []
        for snap in case["samples"]:
            time = round(snap["time"], 12)
            tr = traces[(scenario, N)][time]
            G, D, T = tr["G"], tr["D"], tr["T"]
            ell = math.sqrt(G / D)
            rho = snap["rho_upper"]
            ratio = (rho / ell) if rho is not None else None
            nonlinear_to_viscous = T / (NU * D)

            samples.append(dict(
                time=time,
                G=G,
                D=D,
                T=T,
                ell_omega=ell,
                rho_upper_sample=rho,
                R_sample=ratio,
                nonlinear_to_viscous=nonlinear_to_viscous,
                pair_count=snap["pair_count"],
            ))

        output.append(dict(scenario=scenario, N=N, samples=samples))

    return dict(
        definition=(
            "ell_omega=sqrt(G/D), with G=||omega||_2^2 and "
            "D=||grad omega||_2^2; "
            "R_sample=rho_upper_sample/ell_omega."
        ),
        exact_scaling=(
            "Under u_lambda(x)=lambda^(3/2)v(lambda x), "
            "G->lambda^2 G, D->lambda^4 D, hence "
            "ell_omega->lambda^(-1) ell_omega, matching the absolute "
            "coherence-length scaling."
        ),
        warning=(
            "rho_upper_sample=1/Lmax is only an upper bound on an admissible "
            "coherence radius for the sampled finite-grid pairs. "
            "R_sample>1 is NOT a regularity margin, safety certificate, or "
            "analyticity comparison. ell_omega is a vorticity-gradient length, "
            "not a proven Navier-Stokes analyticity radius."
        ),
        rows=output,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "scale_competition_results.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Wrote", target)
