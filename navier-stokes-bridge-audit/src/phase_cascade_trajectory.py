"""Short Fourier-Galerkin trajectory with explicitly defined component phases.

Run beside archived src modules: python src/phase_cascade_trajectory.py
Writes phase_cascade_trajectory_results.json. No continuum or statistical claim.
"""

import json
import math
from pathlib import Path

import numpy as np

from evolve_galerkin import System
from galerkin import nonlinear_on_support
from validate_enstrophy import h1_nonlinear_growth
from validate_sparse_triad import P, Q, R, make_field

NU = 0.1
N = 4
T_END = 0.02
DT = 0.0005
PEAK_ROTATION = 0.17469152063788906
SCALES = (1, 2)
BASE_AMPLITUDE = 3.0
SECOND_RELATIVE = 0.35


def neg(k):
    return tuple(-x for x in k)


def frames(k):
    kh = np.asarray(k, float)
    kh /= np.linalg.norm(kh)
    axis = np.eye(3)[np.argmin(abs(kh))]
    e1 = np.cross(kh, axis)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(kh, e1)
    return e1, e2


def initial(sys, offset):
    u = make_field()
    # The original seeded sign has negative T; reverse it first.
    if h1_nonlinear_growth(u, nonlinear_on_support(u)) < 0:
        u = {k:-a for k, a in u.items()}
    out = np.zeros((len(sys.modes), 3), dtype=complex)
    for m in SCALES:
        amp = BASE_AMPLITUDE*(SECOND_RELATIVE if m == 2 else 1.)
        for k, a in u.items():
            phase = (np.exp(1j*(PEAK_ROTATION+offset)) if k == R else
                     np.exp(-1j*(PEAK_ROTATION+offset)) if k == neg(R) else 1.)
            out[sys.index[tuple(m*x for x in k)]] += amp*a*phase
    return out


def choose_components(sys, a):
    chosen = {}
    for m in SCALES:
        for k in (P, Q, R):
            km = tuple(m*x for x in k)
            vectors = frames(km)
            index = int(np.argmax([abs(np.dot(e, a[sys.index[km]])) for e in vectors]))
            chosen[km] = vectors[index]
    return chosen


def component_phase(sys, a, da, chosen, m):
    data = []
    for k in (P, Q, R):
        km = tuple(m*x for x in k)
        e = chosen[km]
        z = np.dot(e, a[sys.index[km]])
        dz = np.dot(e, da[sys.index[km]])
        if abs(z) < 1e-8:
            return None
        data.append(dict(magnitude=float(abs(z)), angle=float(np.angle(z)),
                         angular_velocity=float(np.imag(np.conj(z)*dz)/abs(z)**2)))
    phi = data[2]["angle"] - data[0]["angle"] - data[1]["angle"]
    rate = data[2]["angular_velocity"] - data[0]["angular_velocity"] - data[1]["angular_velocity"]
    return dict(phi_wrapped=float(np.angle(np.exp(1j*phi))), phi_dot=rate,
                component_magnitudes=[x["magnitude"] for x in data],
                component_phase_velocities=[x["angular_velocity"] for x in data])


def isolated_transfer(sys, a, m):
    support = [tuple(m*x for x in k) for k in (P, Q, R, neg(P), neg(Q), neg(R))]
    u = {k:a[sys.index[k]].copy() for k in support}
    value = h1_nonlinear_growth(u, nonlinear_on_support(u))
    rm = tuple(m*x for x in R)
    u[rm] *= 1j
    u[neg(rm)] *= -1j
    quarter = h1_nonlinear_growth(u, nonlinear_on_support(u))
    maximum = math.hypot(value, quarter)
    return dict(T_projected=value, phase_maximum=maximum,
                fraction_of_phase_maximum=value/maximum if maximum>1e-12 else None,
                required_R_rotation_to_max=float(math.atan2(quarter,value)))


def snapshot(sys, a, chosen, t):
    da = sys.rhs(a)
    n = sys.nonlinear(a)
    squared = np.sum(abs(a)**2, axis=1)
    E = .5*float(np.sum(squared))
    G = float(np.dot(sys.square, squared))
    D = float(np.dot(sys.square**2, squared))
    T = -float(np.real(np.einsum('i,ij,ij->',sys.square,np.conj(a),n)))
    zero = sys.index[(0,0,0)]
    return dict(time=t, E=E, G=G, D=D, T=T,
                instant_enstrophy_growth=T-NU*D,
                low=component_phase(sys,a,da,chosen,1),
                high=component_phase(sys,a,da,chosen,2),
                low_projected=isolated_transfer(sys,a,1),
                high_projected=isolated_transfer(sys,a,2),
                mode_count_amplitude_gt_1e_8=int(np.sum(np.linalg.norm(a,axis=1)>1e-8)),
                reality_error=float(np.max(np.linalg.norm(a[sys.neg]-np.conjugate(a),axis=1))),
                divergence_error=float(np.max(abs(np.einsum('ij,ij->i',sys.waves,a)))),
                mean_magnitude=float(np.linalg.norm(a[zero])))


def integrate(sys, offset, dt):
    count = round(T_END/dt)
    assert math.isclose(count*dt,T_END,abs_tol=1e-12)
    a = initial(sys, offset)
    chosen = choose_components(sys,a)
    captures = {0,count//4,count//2,3*count//4,count}
    records = []
    for step in range(count+1):
        if step in captures:
            entry = snapshot(sys,a,chosen,step*dt)
            assert entry["reality_error"]<1e-9 and entry["divergence_error"]<1e-9
            records.append(entry)
        if step<count:
            a = sys.rk4(a,dt)
    return records, a


def main():
    sys = System(N=N,nu=NU)
    runs = []
    for label, offset in (("initial_R_phase_at_isolated_max",0.),
                          ("initial_R_phase_quarter_turn_from_max",math.pi/2)):
        coarse, ac = integrate(sys,offset,DT)
        fine, af = integrate(sys,offset,DT/2)
        discrepancy = float(np.linalg.norm(ac-af))
        for c,f in zip(coarse,fine):
            assert math.isclose(c["time"],f["time"],abs_tol=1e-12)
        runs.append(dict(label=label, offset=offset, snapshots=coarse,
                         final_full_fourier_dt_refinement_difference=discrepancy,
                         final_T_dt_refinement_difference=abs(coarse[-1]["T"]-fine[-1]["T"]),
                         final_low_phase_rate_dt_refinement_difference=abs(coarse[-1]["low"]["phi_dot"]-fine[-1]["low"]["phi_dot"])))
    # A single larger cutoff diagnoses whether the finite-N conclusion is stable.
    sys5 = System(N=5,nu=NU)
    larger, a5 = integrate(sys5,0.,DT)
    larger_fine, a5_fine = integrate(sys5,0.,DT/2)
    cutoff_comparison = dict(N=5, mode_count=len(sys5.modes),
                             ordered_pairs=len(sys5.out),
                             snapshots=larger,
                             final_full_fourier_dt_refinement_difference=float(np.linalg.norm(a5-a5_fine)),
                             final_T_dt_refinement_difference=abs(larger[-1]["T"]-larger_fine[-1]["T"]),
                             final_T_difference_N5_minus_N4=larger[-1]["T"]-runs[0]["snapshots"][-1]["T"],
                             final_G_difference_N5_minus_N4=larger[-1]["G"]-runs[0]["snapshots"][-1]["G"])
    return dict(N=N, nu=NU, mode_count=len(sys.modes), ordered_pairs=len(sys.out),
                dt=DT, refined_dt=DT/2, duration=T_END, scales=SCALES,
                amplitude=BASE_AMPLITUDE, second_relative=SECOND_RELATIVE,
                phase_definition="fixed transverse real frame for each k; choose larger initial component; phi=arg(z_R)-arg(z_P)-arg(z_Q); phi_dot=sum signed Im(conj(z)*dz)/|z|^2",
                caution="Component phases depend on frame and become unstable near z=0. Projected-triad optimum is not the optimum for full-flow T. Short finite-N trajectories cannot establish phase randomization or a PDE bound. N4/N5 discrepancy is cutoff sensitivity, not evidence of convergence.",
                runs=runs, cutoff_comparison=cutoff_comparison)


if __name__ == "__main__":
    result=main()
    target=Path(__file__).with_name("phase_cascade_trajectory_results.json")
    target.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {target.name}, {len(result['runs'])} trajectories")
