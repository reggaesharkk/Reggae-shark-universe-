"""Prospectively specified N17 finite-Galerkin K36 mechanism gate.

This evaluator only reads a completed N17 continuation. It does not search,
optimize, or generate an N17 state. Freeze this code before N17 data exist.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

N16_SHA = "53b0cc0a70de0d1a858e9d0c9d98feafcd5fea678c85adfe4d6253f6cf53b0ca"
KEYS_SHA = "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
SOURCE_SHA = "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e"
ORBIT = ((3, 3, 4), (0, 2, 3))
DT = 1e-4
H = (5e-9, 1e-8, 2e-8)


def checked_json(path, sha=None):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if sha is not None and digest != sha:
        raise ValueError(f"input SHA-256 mismatch: {path}: {digest}")
    return json.loads(raw), digest


def frozen_keys(payload):
    if payload["source_original_sha256"] != SOURCE_SHA:
        raise ValueError("K36 provenance mismatch")
    keys = {(tuple(x["left_orbit"]), tuple(x["right_orbit"])) for x in payload["keys"]}
    if len(keys) != 36 or ORBIT in keys:
        raise ValueError("frozen K36 is invalid for this gate")
    return keys


def complex_groups(system, a):
    pi, qi, ki = (system.index[x] for x in (hold.P, hold.Q, hold.K))
    b = system.projectors[ki] @ (1j * np.dot(hold.Q, a[pi]) * a[qi])
    weight = float(system.square[ki] ** 2)
    z = -weight * np.vdot(a[ki], b)
    if abs(z) < 1e-30:
        raise ValueError("tracked normalizer is zero/undefined")
    groups = defaultdict(complex)
    for li, ri, dak in hold.source_terms_for_output(system, a, ki):
        key = (hold.orbit(system.modes[li]), hold.orbit(system.modes[ri]))
        groups[key] += -weight * np.vdot(dak, b)
    return dict(groups), z


def group_rates(system, a, keys, h):
    v = system.rhs(a)
    gm, zm = complex_groups(system, a-h*v)
    g0, z = complex_groups(system, a)
    gp, zp = complex_groups(system, a+h*v)
    zdot = (zp-zm)/(2*h)
    rows = {}
    for key in sorted(set(gm) | set(g0) | set(gp)):
        w = g0.get(key, 0j)
        signed = float(np.imag(w/z))
        wdot = (gp.get(key, 0j)-gm.get(key, 0j))/(2*h)
        central = (abs(float(np.imag(gp.get(key,0j)/zp)))-
                   abs(float(np.imag(gm.get(key,0j)/zm))))/(2*h)
        if abs(signed) <= 1e-12:
            numerator = normalizer = None
        else:
            numerator = np.sign(signed)*float(np.imag(wdot/z))
            normalizer = np.sign(signed)*float(np.imag(-w*zdot/(z*z)))
            if abs(numerator+normalizer-central) > 1e-3:
                raise AssertionError(f"directional split failed: {key}")
        rows[key] = {"mass": abs(signed), "rate": central,
                     "numerator_rate": numerator, "normalizer_rate": normalizer,
                     "in_K36": key in keys}
    return rows, z


def summary(rows, keys):
    if ORBIT not in rows:
        raise ValueError("recurrent orbit absent")
    inside = [v for k,v in rows.items() if k in keys]
    outside = [v for k,v in rows.items() if k not in keys]
    I = sum(v["mass"] for v in inside)
    O = sum(v["mass"] for v in outside)
    Ir = sum(v["rate"] for v in inside)
    Or = sum(v["rate"] for v in outside)
    positive = sorted(((k,v["rate"]) for k,v in rows.items() if k not in keys),
                      key=lambda x: (-x[1],x[0]))
    if not positive:
        raise ValueError("outside groups absent")
    unique_leader = len(positive) == 1 or positive[0][1] > positive[1][1]
    return {"I": I, "O": O, "F": I-9*O, "I_rate": Ir, "O_rate": Or,
            "F_rate": Ir-9*Or, "leading_outside": positive[0][0],
            "unique_leader": unique_leader,
            "orbit": rows[ORBIT]}


def advance(system, a, steps):
    for _ in range(steps):
        a = system.rk4(a, DT)
    return a


def swap(groups_h, z_h, groups_f, z_f, keys):
    def mass(w,z): return abs(float(np.imag(w/z)))
    numerator = normalizer = delta = 0.0
    orbit_delta = None
    outside_deltas = []
    for key in sorted(set(groups_h) | set(groups_f)):
        if key in keys: continue
        wh, wf = groups_h.get(key,0j),groups_f.get(key,0j)
        aa, bb = mass(wh,z_h),mass(wf,z_h)
        cc, dd = mass(wh,z_f),mass(wf,z_f)
        n = ((bb-aa)+(dd-cc))/2
        q = ((cc-aa)+(dd-bb))/2
        d = dd-aa
        if abs(d-n-q) > 1e-10: raise AssertionError("swap identity failed")
        numerator += n; normalizer += q; delta += d
        outside_deltas.append((key,d))
        if key == ORBIT: orbit_delta = d
    if orbit_delta is None: raise ValueError("recurrent orbit absent")
    outside_deltas.sort(key=lambda x:(x[1],x[0]))
    unique_decrease = len(outside_deltas)==1 or outside_deltas[0][1]<outside_deltas[1][1]
    return {"delta_O":delta,"orbit_delta_O":orbit_delta,
            "largest_outside_decrease":outside_deltas[0][0],
            "unique_decrease":unique_decrease,
            "numerator_swap":numerator,"normalizer_swap":normalizer}


def run(n16_path,n17_path,keys_path):
    j16,sha16 = checked_json(n16_path,N16_SHA)
    j17,sha17 = checked_json(n17_path)
    frozen,sha_keys = checked_json(keys_path,KEYS_SHA)
    keys = frozen_keys(frozen)
    hold.System = DealiasedSystem
    system, states = hold.reconstruct(hold.get_row(j16,16),hold.get_row(j17,17))
    if system.N != 17: raise ValueError("expected N17")
    result = {"status":"prospective finite N17 mechanism evaluation",
              "inputs_sha256":{"n16":sha16,"n17":sha17,"keys":sha_keys},
              "dt":DT,"h_values":H,"states":{},"failure_rules":[],"joint_pass":False}
    at23 = {}
    for name,a0 in states.items():
        static = hold.evaluate_state(system,a0,keys)
        points = {}
        for step in (0,10):
            a = advance(system,a0,step)
            estimates = [summary(group_rates(system,a,keys,h)[0],keys) for h in H]
            spread = max(x["F_rate"] for x in estimates)-min(x["F_rate"] for x in estimates)
            orbit_spread = max(x["orbit"]["rate"] for x in estimates)-min(x["orbit"]["rate"] for x in estimates)
            if spread > 1e-3 or orbit_spread > 1e-3:
                result["failure_rules"].append(f"{name}: derivative step instability at {step}")
            x=estimates[1]
            points[str(step)]={"I":x["I"],"O":x["O"],"F":x["F"],
                "I_rate":x["I_rate"],"O_rate":x["O_rate"],"F_rate":x["F_rate"],
                "orbit_rate":x["orbit"]["rate"],
                "orbit_numerator_rate":x["orbit"]["numerator_rate"],
                "orbit_normalizer_rate":x["orbit"]["normalizer_rate"],
                "leading_outside":[list(y) for y in x["leading_outside"]],
                "unique_leader":x["unique_leader"],
                "F_rate_h_spread":spread,"orbit_rate_h_spread":orbit_spread}
        if not static["passes_preregistered_consistency_criteria"]:
            result["failure_rules"].append(f"{name}: static K36 gate")
        if not points["0"]["orbit_rate"] < 0:
            result["failure_rules"].append(f"{name}: orbit does not initially decay")
        x=points["10"]
        if (x["orbit_numerator_rate"] is None or
                points["0"]["orbit_numerator_rate"] is None):
            result["failure_rules"].append(f"{name}: recurrent orbit at a kink")
        if not (x["orbit_rate"]>0 and x["I_rate"]>0 and x["O_rate"]>0 and x["F_rate"]<0
                and x["unique_leader"]
                and tuple(tuple(y) for y in x["leading_outside"])==ORBIT):
            result["failure_rules"].append(f"{name}: t=.001 turnover/rank prediction")
        result["states"][name]={"static":static,"points":points}
        if name in ("inherited","full_final"):
            at23[name]=complex_groups(system,advance(system,a0,23))
    gh,zh=at23["inherited"]; gf,zf=at23["full_final"]
    s=swap(gh,zh,gf,zf,keys)
    if not (s["orbit_delta_O"]<0 and s["unique_decrease"]
            and s["largest_outside_decrease"]==ORBIT
            and s["normalizer_swap"]<0 and abs(s["normalizer_swap"])>abs(s["numerator_swap"])):
        result["failure_rules"].append("t=.0023 state-difference/normalizer prediction")
    result["state_difference_t0023"]={**s,
        "z_inherited":[zh.real,zh.imag],"z_full_final":[zf.real,zf.imag]}
    result["joint_pass"]=len(result["failure_rules"])==0
    result["interpretation"]=("finite holdout only; N12-N16 are discovery data; "
        "a missing/undefined observable is not a pass; no all-N or PDE claim")
    return result


def main():
    p=argparse.ArgumentParser()
    for name in ("n16","n17","keys","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    try:
        result=run(a.n16,a.n17,a.keys)
    except (ValueError, AssertionError) as exc:
        result={"status":"N17 mechanism evaluation failed or unevaluable",
                "joint_pass":False,"failure_rules":[str(exc)],
                "interpretation":"retain this failure; do not retune the frozen test"}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    tmp=a.output.with_name(a.output.name+".tmp")
    tmp.write_text(json.dumps(result,indent=2)+"\n")
    tmp.replace(a.output)
    print("PASS" if result["joint_pass"] else "FAIL",result["failure_rules"])
    if not result["joint_pass"]:
        sys.exit(1)


if __name__=="__main__":main()
