"""Arb endpoint K36 margin enclosure conditional on a validated N14 L2 radius."""
import hashlib, json, sys
from pathlib import Path
import numpy as np
from flint import acb, arb, ctx

_ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(_ROOT/"src"))
import wp16_036_sparse_turnover_exact_anchor as exact
from wp16_036_dealiased_trajectory_gate import DealiasedSystem
import arb_common_n14 as runner
import arb_segment_n14 as segment

EXPECTED_KEYS="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"

def vdot(a,b):
    return sum((a[i].conjugate()*b[i] for i in range(3)),acb(0))

def norm_upper(v):
    return segment.ball_l2_upper(v)

def projection(k,vector):
    kk=sum(x*x for x in k)
    kd=sum((vector[i]*int(k[i]) for i in range(3)),acb(0))
    return [vector[i]-kd*int(k[i])/kk for i in range(3)]

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def evaluate(nodes_path,keys_path,E_decimal):
    ctx.prec=128
    system=DealiasedSystem(14)
    arr=np.load(nodes_path,mmap_mode="r")[-1]
    a=segment.solenoidal_reality_projection(system,arr)
    keys_raw=keys_path.read_bytes()
    if hashlib.sha256(keys_raw).hexdigest()!=EXPECTED_KEYS:
        raise ValueError("K36 key hash mismatch")
    keys={(tuple(row["left_orbit"]),tuple(row["right_orbit"])) for row in json.loads(keys_raw)["keys"]}
    p,q,k=(system.index[x] for x in (exact.P,exact.Q,exact.K))
    b=projection(exact.K,[acb(0,1)*sum((a[p][j]*exact.Q[j] for j in range(3)),acb(0))*a[q][i] for i in range(3)])
    weight=int(system.square[k]**2)
    z=-weight*vdot(a[k],b)
    groups={}; d_sum=arb(0)
    for li,ri in zip(system.left,system.right):
        wave=system.waves[ri]
        raw=[acb(0,1)*sum((a[li][j]*int(wave[j]) for j in range(3)),acb(0))*a[ri][i] for i in range(3)]
        d=[-v for v in projection(exact.K,raw)]
        d_sum+=norm_upper(d)
        w=-weight*vdot(d,b)
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]=groups.get(key,acb(0))+w
    I=arb(0); O=arb(0)
    for key,w in groups.items():
        mass=abs((w/z).imag)
        if key in keys: I+=mass
        else: O+=mass
    Fv=I-9*O
    E=arb(E_decimal)
    A=norm_upper([v for row in a for v in row])
    bp,bq,bk=(norm_upper(a[ix]) for ix in (p,q,k))
    B=norm_upper(b)
    dq=arb(sum(x*x for x in exact.Q)).sqrt().upper()
    delta_b=dq*E*(bp+bq+E)
    delta_d=arb(system.N)*(2*A*E+E*E)
    delta_z=weight*(E*B+(bk+E)*delta_b)
    z_abs=z.abs_lower().lower()
    z_lower=(z_abs-delta_z).lower()
    if not z_lower>0:
        raise ValueError("normalizer lower bound failed")
    delta_w=weight*(delta_d*B+(d_sum+delta_d)*delta_b)
    w_sum=weight*d_sum*B
    error=(9*(delta_w/z_lower+w_sum*delta_z/(z_lower*z_abs))).upper()
    upper=(Fv+error).upper(); lower=(Fv-error).lower()
    return {
        "status":"Arb endpoint margin conditional on supplied Galerkin L2 error radius",
        "N":14,
        "E_input_decimal":E_decimal,
        "F_of_exact_decimal_endpoint_upper":runner.decimal_upper(Fv.upper(),9),
        "F_of_exact_decimal_endpoint_lower_ball":str(Fv.lower()),
        "F_of_exact_decimal_endpoint_lower_decimal":runner.decimal_lower(Fv.lower(),9),
        "z_abs_lower_decimal":str(z_abs),
        "z_perturbation_upper_decimal":runner.decimal_upper(delta_z.upper(),9),
        "F_error_upper_decimal":runner.decimal_upper(error,9),
        "F_true_lower_decimal":runner.decimal_lower(lower,9),
        "F_true_upper_decimal":runner.decimal_upper(upper,9),
        "certified_negative_if_E_valid":upper<0,
        "ordered_group_count":len(groups)
    }
