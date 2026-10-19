"""WP18 isolated scale-2 triad reduction.

Verifies exact sparse H2 high-advector algebra and computes the positive
stretching factor through deterministic two-angle quadrature.

No exact closed form for the positive-part integral is claimed.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from galerkin import leray
from helicity_phase_gate import POLARIZATIONS
from validate_sparse_triad import P, Q, R

HERE = Path(__file__).resolve().parent


def neg(k):
    return tuple(-x for x in k)


def field(A, theta, m=2):
    u = {}
    for k, v in POLARIZATIONS.items():
        km = tuple(m*x for x in k)
        phase = np.exp(1j*theta) if k == R else 1.0
        a = A*v.astype(complex)*phase
        u[km] = a
        u[neg(km)] = np.conj(a)
    return u


def high_transfer(u, K=2, s=2):
    total = 0j
    for k, ak in u.items():
        k2 = sum(x*x for x in k)
        for p, ap in u.items():
            if sum(x*x for x in p) <= K*K:
                continue
            q = tuple(k[d]-p[d] for d in range(3))
            aq = u.get(q)
            if aq is None:
                continue
            raw = 1j*np.dot(q, ap)*aq
            total += -(k2**s)*np.vdot(ak, leray(k) @ raw)
    return float(np.real(total))


def F(theta, a, b):
    return 2*(
        -2*np.sin(a)
        +4*np.sin(b)
        +2*np.sin(theta)
        -2*np.sin(2*a+theta)
        -2*np.sin(2*b+theta)
        -2*np.sin(a-b+theta)
        +4*np.sin(a+b+theta)
        -np.sin(a+2*b+2*theta)
        -2*np.sin(a+3*b+theta)
        +2*np.sin(2*a+b+2*theta)
        +2*np.sin(2*a+2*b+theta)
        -2*np.sin(2*a+3*b+2*theta)
        +np.sin(3*a+2*b+2*theta)
    )


def positive_average(theta, n):
    b = 2*np.pi*np.arange(n)/n
    total = 0.0
    signed = 0.0
    for j in range(n):
        a = 2*np.pi*j/n
        values = F(theta, a, b)
        total += float(np.sum(np.maximum(values, 0.0)))
        signed += float(np.sum(values))
    denom = float(n*n)
    return total/denom, signed/denom


def C_from_positive(theta, positive):
    return max(-7*math.sin(theta), 0.0)/positive if positive > 0 else 0.0


def exact_checks():
    rows = []
    for A in (1.0, 2.0):
        for theta in (0.0, math.pi/2, math.pi, 3*math.pi/2):
            u = field(A, theta)
            N = high_transfer(u)
            expected = -512*A**3*math.sin(theta)
            G = sum(
                sum(x*x for x in k)*float(np.vdot(a,a).real)
                for k,a in u.items()
            )
            X2 = sum(
                (sum(x*x for x in k)**2)*float(np.vdot(a,a).real)
                for k,a in u.items()
            )
            assert abs(N-expected) < 1e-10*max(1.0,abs(expected))
            assert abs(G-112*A*A) < 1e-10
            assert abs(X2-1024*A*A) < 1e-10
            rows.append(dict(
                amplitude=A,
                theta=theta,
                N2_high=N,
                expected_N2_high=expected,
                G=G,
                X2=X2,
            ))
    return rows


def run(scan_points=361, scan_grid=192):
    checks = exact_checks()

    thetas = np.linspace(-math.pi, 0.0, scan_points)
    scan = []
    for theta in thetas:
        positive, signed = positive_average(float(theta), scan_grid)
        scan.append(dict(
            theta=float(theta),
            P_positive=positive,
            signed_average=signed,
            C_infinity=C_from_positive(float(theta), positive),
        ))

    best = max(scan, key=lambda x:x["C_infinity"])

    refinement = []
    candidate_theta = best["theta"]
    for n in (256, 512, 1024, 2048, 4096):
        positive, signed = positive_average(candidate_theta, n)
        refinement.append(dict(
            n=n,
            theta=candidate_theta,
            P_positive=positive,
            signed_average=signed,
            C_infinity=C_from_positive(candidate_theta, positive),
        ))

    return dict(
        exact_formula="N2_high(theta)=-512 A^3 sin(theta), G=112 A^2, X2=1024 A^2",
        reduced_formula="C_infinity(theta)=max(-7 sin(theta),0)/P_positive(theta)",
        exact_checks=checks,
        phase_scan=dict(
            points=scan_points,
            quadrature_n=scan_grid,
            best=best,
            rows=scan,
        ),
        refinement=refinement,
        warning=(
            "The phase maximum is established only within the finite scan. "
            "P_positive is numerical quadrature; no exact closed form or "
            "global all-field constant is claimed."
        ),
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output", type=Path,
        default=HERE/"wp18_isolated_triad_limit_results.json"
    )
    p.add_argument("--scan-points", type=int, default=361)
    p.add_argument("--scan-grid", type=int, default=192)
    a = p.parse_args()

    result = run(a.scan_points, a.scan_grid)
    a.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Wrote", a.output)
    print("scan best", result["phase_scan"]["best"])
    for row in result["refinement"]:
        print("refine", row)
