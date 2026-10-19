"""Exact phase-sensitive triadic coherence diagnostic.

Decomposes the H1 nonlinear transfer into ordered Fourier-triad contributions.
This is an algebraic diagnostic only; it is not an a priori regularity bound.
"""

import json
import math
from pathlib import Path

import numpy as np

from galerkin import leray, nonlinear_on_support
from helicity_phase_gate import field
from validate_enstrophy import h1_nonlinear_growth


HERE = Path(__file__).resolve().parent
TOL = 1e-10


def triadic_decomposition(data):
    """Return exact ordered-triad decomposition of H1 transfer.

    For k=p+q,
      Z_{k,p,q} = -|k|^2 <a_k, P_k[i (q.a_p) a_q]>
    so T = Re sum Z and A = sum |Z| is a positive cubic envelope.
    The coherence ratio chi=T/A satisfies |chi|<=1 whenever A>0.
    """
    zsum = 0j
    envelope = 0.0
    count = 0
    for k, ak in data.items():
        k2 = float(sum(x*x for x in k))
        if k2 == 0:
            continue
        Pk = leray(k)
        for p, ap in data.items():
            q = tuple(k[d] - p[d] for d in range(3))
            aq = data.get(q)
            if aq is None:
                continue
            term = 1j * np.dot(q, ap) * aq
            z = -k2 * np.vdot(ak, Pk @ term)
            zsum += z
            envelope += float(abs(z))
            count += 1
    T = float(zsum.real)
    chi = T / envelope if envelope else 0.0
    return dict(
        ordered_triad_terms=count,
        transfer=T,
        complex_sum_imag=float(zsum.imag),
        cubic_envelope=envelope,
        coherence=chi,
    )


def dilate(data, m):
    return {tuple(m*x for x in k): a.copy() for k, a in data.items()}


def negate(data):
    return {k: -a for k, a in data.items()}


def scale(data, A):
    return {k: A*a for k, a in data.items()}


def run():
    rows = []
    phase_rows = []

    for A in (1.0, 2.0):
        for theta in (0.0, math.pi/2, math.pi, 3*math.pi/2):
            data = field(A, theta)
            d = triadic_decomposition(data)
            direct = h1_nonlinear_growth(data, nonlinear_on_support(data))

            assert abs(d["transfer"] - direct) < TOL
            assert abs(d["complex_sum_imag"]) < TOL
            assert abs(d["coherence"]) <= 1 + TOL
            assert abs(d["transfer"] - 4*A**3*math.sin(theta)) < TOL

            row = dict(amplitude=A, phase_radians=theta, **d)
            rows.append(row)
            if A == 1.0:
                phase_rows.append(row)

    # The cubic envelope is phase-invariant for this sparse family while
    # the signed transfer changes with relative phase.
    envelopes = [r["cubic_envelope"] for r in phase_rows]
    assert max(envelopes) - min(envelopes) < TOL

    base = field(1.0, math.pi/2)
    b = triadic_decomposition(base)

    neg = triadic_decomposition(negate(base))
    assert abs(neg["transfer"] + b["transfer"]) < TOL
    assert abs(neg["cubic_envelope"] - b["cubic_envelope"]) < TOL
    assert abs(neg["coherence"] + b["coherence"]) < TOL

    amp = triadic_decomposition(scale(base, 2.0))
    assert abs(amp["transfer"] - 8*b["transfer"]) < TOL
    assert abs(amp["cubic_envelope"] - 8*b["cubic_envelope"]) < TOL
    assert abs(amp["coherence"] - b["coherence"]) < TOL

    freq = triadic_decomposition(dilate(base, 3))
    assert abs(freq["transfer"] - 27*b["transfer"]) < TOL
    assert abs(freq["cubic_envelope"] - 27*b["cubic_envelope"]) < TOL
    assert abs(freq["coherence"] - b["coherence"]) < TOL

    return dict(
        definition=(
            "Z_kpq=-|k|^2<a_k,P_k[i(q.a_p)a_q]>, "
            "A_N=sum|Z_kpq|, chi_N=T_N/A_N"
        ),
        identity="T_N=Re(sum Z_kpq), hence |T_N|<=A_N and |chi_N|<=1.",
        transformation_checks={
            "u_to_minus_u":"T and chi change sign; A_N is unchanged.",
            "u_to_2u":"T and A_N scale by 2^3; chi is unchanged.",
            "k_to_3k":"T and A_N scale by 3^3; chi is unchanged.",
        },
        sparse_family=(
            "For the zero-modal-helicity triad, T(A,theta)=4 A^3 sin(theta). "
            "The cubic envelope is constant across theta at fixed A, while chi "
            "tracks the signed phase coherence."
        ),
        limitation=(
            "A_N is itself a cubic Fourier quantity and is not shown to be "
            "controlled by energy/enstrophy uniformly in cutoff. This gate "
            "therefore does not close the PDE or prove regularity."
        ),
        rows=rows,
    )


if __name__ == "__main__":
    result = run()
    target = HERE / "triadic_coherence_results.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target.name}")
