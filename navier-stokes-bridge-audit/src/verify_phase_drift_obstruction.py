"""Exact/numerical verification of the analytic phase-drift obstruction.

This script checks the normalized helical basis, the full reality-completed
cyclic coefficients, the coefficient sum, and the instantaneous state with
nonzero transfer and zero collective phase drift.

Scope: finite-dimensional algebraic verification only.
"""

import cmath
import math
import numpy as np


def leray(k):
    k = np.asarray(k, dtype=float)
    return np.eye(3) - np.outer(k, k) / np.dot(k, k)


k = np.array([1.0, 2.0, 0.0])
p = np.array([-1.0, 0.0, 1.0])
q = np.array([0.0, -2.0, -1.0])

hk = np.array([2j / math.sqrt(10), -1j / math.sqrt(10), 1 / math.sqrt(2)], dtype=complex)
hp = np.array([1j / 2, 1 / math.sqrt(2), 1j / 2], dtype=complex)
hq = np.array([1 / math.sqrt(2), -1j / math.sqrt(10), 2j / math.sqrt(10)], dtype=complex)


def check_basis():
    tests = []
    for j, h, s in [(k, hk, +1), (p, hp, -1), (q, hq, +1)]:
        tests.append(abs(np.vdot(h, h).real - 1.0))
        tests.append(abs(np.dot(j, h)))
        tests.append(np.linalg.norm(1j * np.cross(j, h) - s * np.linalg.norm(j) * h))
    return max(float(x) for x in tests)


def cyclic_coefficient(target, ht, a, ha, b, hb):
    # target = (-a) + (-b); reality gives h_-a = conj(h_a), h_-b = conj(h_b)
    term = ((-b) @ np.conj(ha)) * np.conj(hb) + ((-a) @ np.conj(hb)) * np.conj(ha)
    B = -1j * (leray(target) @ term)
    return np.vdot(ht, B)


Ck = cyclic_coefficient(k, hk, p, hp, q, hq)
Cp = cyclic_coefficient(p, hp, q, hq, k, hk)
Cq = cyclic_coefficient(q, hq, k, hk, p, hp)

Ck_exact_numeric = (
    -7 * math.sqrt(10) / 20
    - 2 / 5
    + 1j * (math.sqrt(2) + math.sqrt(5)) / 5
)
Cq_exact_numeric = -Ck_exact_numeric

assert check_basis() < 1e-12
assert abs(Ck - Ck_exact_numeric) < 1e-12
assert abs(Cp) < 1e-12
assert abs(Cq - Cq_exact_numeric) < 1e-12
assert abs(Ck + Cp + Cq) < 1e-12

# Instantaneous obstruction state.
R = 1.0
rp = 1.0
Phi = cmath.phase(Ck)

z = Ck * cmath.exp(-1j * Phi)
phase_rate = rp * (R / R - R / R) * z.imag

# Single-positive-mode enstrophy contribution G_k = |k|^2 |A_k|^2.
transfer_Gk = 2 * np.dot(k, k) * R * rp * R * z.real

assert abs(phase_rate) < 1e-12
assert abs(z.imag) < 1e-12
assert transfer_Gk > 0

print("basis_max_error =", check_basis())
print("Ck =", Ck)
print("Cp =", Cp)
print("Cq =", Cq)
print("Ck+Cp+Cq =", Ck + Cp + Cq)
print("|Ck| =", abs(Ck))
print("arg(Ck) degrees =", math.degrees(Phi))
print("phase_rate =", phase_rate)
print("single-mode enstrophy transfer =", transfer_Gk)
print("PASS: nonzero instantaneous transfer with zero collective phase drift")
