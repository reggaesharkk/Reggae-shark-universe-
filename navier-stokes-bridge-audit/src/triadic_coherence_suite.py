"""Stress-test triadic coherence on the existing 24-case audit universe.

Uses the same initial fields/cutoffs as projection_residual_results.json and the
same four tracked trajectories as projection_shell_gate.py. This is a finite
Galerkin diagnostic, not a cutoff-uniform PDE estimate.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU

HERE = Path(__file__).resolve().parent
TRACK = {("reference",4),("reference",7),
         ("combined_double_quarter_high",4),
         ("combined_double_quarter_high",7)}


def snapshot(sys, a):
    # Exact ordered-pair decomposition using the convolution index arrays
    # already constructed by System. For each k=p+q:
    # Z=-|k|^2 <a_k, P_k[i(q.a_p)a_q]>.
    qdot = np.einsum("ij,ij->i", sys.qwaves, a[sys.left])
    raw = 1j * qdot[:,None] * a[sys.right]
    projected = np.einsum(
        "kij,kj->ki", sys.projectors[sys.out], raw)
    z = -sys.square[sys.out] * np.einsum(
        "ij,ij->i", np.conj(a[sys.out]), projected)

    T = float(np.real(np.sum(z)))
    imag = float(np.imag(np.sum(z)))
    A = float(np.sum(np.abs(z)))
    chi = T/A if A else 0.0

    n = sys.nonlinear(a)
    direct = -float(np.real(np.einsum(
        "i,ij,ij->", sys.square, np.conj(a), n)))
    err = abs(T-direct)

    assert err < 1e-8 * max(1.0, abs(direct))
    assert abs(imag) < 1e-8 * max(1.0, abs(T), A)
    assert abs(chi) <= 1 + 1e-12
    return dict(
        T=direct,
        A=A,
        chi=chi,
        ordered_triad_terms=int(len(z)),
        decomposition_error=err,
        complex_sum_imag=imag,
    )


def cases():
    prior = json.loads(
        (HERE / "projection_residual_results.json").read_text(encoding="utf-8"))
    return [(row["scenario"], row["N"]) for row in prior["rows"]]


def run():
    initial = []
    tracked = []
    for scenario, N in cases():
        sys = System(N=N, nu=NU)
        a = make_initial(sys, *SCENARIOS[scenario])
        initial.append(dict(scenario=scenario, N=N, **snapshot(sys,a)))

        if (scenario,N) in TRACK:
            samples = []
            for step in range(41):
                if step % 10 == 0:
                    samples.append(dict(time=step*DT, **snapshot(sys,a)))
                if step < 40:
                    a = sys.rk4(a, DT)
            tracked.append(dict(scenario=scenario,N=N,samples=samples))

    return dict(
        case_source="projection_residual_results.json (24 existing cases)",
        tracked_cases=[list(x) for x in sorted(TRACK)],
        definition="A=sum|Z_kpq|, chi=T/A for exact ordered Fourier triads",
        warning=(
            "Finite cutoffs and short trajectories only. Cutoff stability in "
            "these samples is not a cutoff-uniform bound; A remains cubic."
        ),
        initial=initial,
        tracked=tracked,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "triadic_coherence_suite_results.json"
    target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", target)
