#!/usr/bin/env python3
"""Whole-segment adjoint residual pilot; no cutoff-transfer theorem.

Saved binary64 data are imported as exact dyadic rationals, then exactly
projected. Spatial/time convolution uses carry-free Kronecker substitution.
Each output is atomic and bound to its inputs and this source file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from fractions import Fraction
import numpy as np
from flint import acb, acb_poly, arb, ctx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "next-work/n14_same_datum/tools"))
import arb_segment_n14 as primal
import arb_common_n14 as common
import wp19_v0_27a_terminal_gradient_arb as goal
import wp19_v0_26_signed_goal_adjoint as frozen_goal
import wp16_036_sparse_turnover_exact_anchor as exact
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

PROTOCOL = "wp19-v0.28-adjoint-segment-arb-v2"
ctx.prec = 192
H = arb(1) / 40000
HALF_H = arb(1) / 80000
NU = arb(1) / 10
WITNESS = ROOT / "results/wp16_n17_holdout/wp16_036_sparse_turnover_112_pairs.json"
K36 = ROOT / "results/wp16_n12_holdout/frozen_K36_ordered_source_orbits.json"
EXPECTED_C1_M14 = "981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"

def sha(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def safe_decimal_upper(x, places=12):
    """Return an outward decimal upper bound using integer arithmetic only.

    The shared legacy formatter converts through binary64, which can lose
    several decimal units for large values. Here Arb supplies an exact
    integer midpoint/radius/exponent enclosure; its upper rational endpoint
    is rounded upward to the requested decimal grid without floats.
    """
    if places < 0:
        raise ValueError("places must be nonnegative")
    mid, rad, exp = (int(v) for v in x.mid_rad_10exp())
    upper_integer = mid + rad
    shift = exp + places
    if shift >= 0:
        exact_grid_numerator = upper_integer * (10 ** shift)
        units = exact_grid_numerator
    else:
        denominator = 10 ** (-shift)
        exact_grid_numerator = upper_integer
        units = -((-upper_integer) // denominator)
    # Strict slack in the last printed decimal place.
    units += 1
    sign = "-" if units < 0 else ""
    digits = str(abs(units)).zfill(places + 1)
    if places:
        digits = digits[:-places] + "." + digits[-places:]
    candidate = sign + digits
    if shift >= 0:
        strictly_above = units > exact_grid_numerator
    else:
        strictly_above = units * denominator > exact_grid_numerator
    if not strictly_above:
        raise ArithmeticError("integer outward decimal conversion failed")
    return candidate

def decimal_fraction(text):
    """Parse a finite decimal string as an exact rational for self-checks."""
    sign = -1 if text.startswith("-") else 1
    body = text[1:] if sign < 0 else text
    if "." not in body:
        return Fraction(sign * int(body), 1)
    whole, fractional = body.split(".")
    den = 10 ** len(fractional)
    return Fraction(sign * (int(whole) * den + int(fractional)), den)

def dyadic(x):
    # Never use a decimal repr as an enclosure of a stored binary64 value.
    n, d = float(x).as_integer_ratio()
    return arb(n) / arb(d)

def point(z):
    return acb(dyadic(z.real), dyadic(z.imag))

def projected_rows(s, a):
    out = [[acb(0) for _ in range(3)] for _ in s.modes]
    for i, k in enumerate(s.modes):
        if tuple(k) <= tuple(-x for x in k): continue
        v = [point(z) for z in a[i]]
        kd = sum((v[j] * int(k[j]) for j in range(3)), acb(0))
        v = [v[j] - kd * int(k[j]) / int(s.square[i]) for j in range(3)]
        out[i] = v
        out[int(s.neg[i])] = [z.conjugate() for z in v]
    return out

def hermite(a, b, f, g, h):
    return [a,
            [[h*z for z in v] for v in f],
            [[3*(b[i][j]-a[i][j])-h*(2*f[i][j]+g[i][j]) for j in range(3)] for i in range(len(a))],
            [[2*(a[i][j]-b[i][j])+h*(f[i][j]+g[i][j]) for j in range(3)] for i in range(len(a))]]

def restrict(c, start, width):
    """Exact substitution theta=start+width*x in a cubic."""
    return [[[sum((c[d][i][j]*math.comb(d,r)*start**(d-r)*width**r
                    for d in range(r,4)),acb(0))
              for j in range(3)] for i in range(len(c[0]))] for r in range(4)]

def embed(low, high, c):
    out = [[[acb(0) for _ in range(3)] for _ in high.modes] for _ in c]
    for i, k in enumerate(low.modes):
        for d in range(len(c)): out[d][high.index[k]] = c[d][i]
    return out

def bernstein(c):
    degree = len(c)-1
    return [[[sum((c[d][i][t]*math.comb(j,d)/math.comb(degree,d)
                    for d in range(j+1)),acb(0)) for t in range(3)]
             for i in range(len(c[0]))] for j in range(degree+1)]

def norm(rows):
    q = arb(0)
    for row in rows:
        for z in row: q += z.abs_upper()**2
    return q.sqrt().upper()

def sup_norm(c):
    maximum = arb(0)
    for b in bernstein(c):
        maximum = maximum.max(norm(b)).upper()
    return maximum

def sup_strain(s, c):
    # For transverse a_k, ||sym(i k tensor a_k)||_F=|k| |a_k|/sqrt(2).
    maximum = arb(0)
    for b in bernstein(c):
        val = arb(0)
        for k, row in zip(s.modes,b):
            val += arb(sum(int(x)**2 for x in k)).sqrt()*norm([row])/arb(2).sqrt()
        maximum = maximum.max(val).upper()
    return maximum

def packed_vjp(s, u, lam):
    """Coefficients of P[(grad u)^T lam-(u.grad)lam], degree <=6.

    Each spatial input digit lies in [0,2N]. A product digit is in [0,4N]
    and is strictly below B=4N+1. The time stride B**3 therefore has no
    spatial carry. Temporal degrees add from 0..3 to 0..6.
    """
    tick = time.monotonic()
    B = 4*s.N+1; stride = B**3
    left = [(int(k[0])+s.N)+B*(int(k[1])+s.N)+B*B*(int(k[2])+s.N) for k in s.modes]
    right = [(int(k[0])+2*s.N)+B*(int(k[1])+2*s.N)+B*B*(int(k[2])+2*s.N) for k in s.modes]
    def pack(c, comp, derivative=None):
        # Set the highest coefficient first, then only nonzero entries.
        # A dense constructor repeatedly normalizes long zero gaps.
        values = {}
        for i, slot in enumerate(left):
            factor = acb(0,int(s.modes[i][derivative])) if derivative is not None else 1
            for d in range(4):
                z = c[d][i][comp]*factor
                if not z.is_zero(): values[slot+d*stride] = z
        poly = acb_poly([])
        for slot in sorted(values, reverse=True): poly[slot] = values[slot]
        return poly
    U = [pack(u,j) for j in range(3)]
    L = [pack(lam,j) for j in range(3)]
    print("packed base fields",round(time.monotonic()-tick,3),flush=True)
    out = [[[acb(0) for _ in range(3)] for _ in s.modes] for _ in range(7)]
    for j in range(3):
        product = acb_poly([0])
        for i in range(3):
            product += L[i]*pack(u,i,j)-U[i]*pack(lam,j,i)
            print("convolution",j,i,round(time.monotonic()-tick,3),flush=True)
        for i, slot in enumerate(right):
            for d in range(7): out[d][i][j] = product[slot+d*stride]
    for d in range(7):
        for i,k in enumerate(s.modes):
            kk = int(s.square[i])
            if not kk: out[d][i] = [acb(0)]*3; continue
            kd = sum((out[d][i][j]*int(k[j]) for j in range(3)),acb(0))
            out[d][i] = [out[d][i][j]-kd*int(k[j])/kk for j in range(3)]
    return out

def old_radius_and_identity(directory, nodes, rhs, M):
    meta = json.loads((directory/"metadata.json").read_text())
    if meta.get("initial_error_bound_decimal") != "0" or meta.get("h_exact_decimal") != "0.000025" or meta.get("steps") != 120:
        raise ValueError("primal arithmetic/time protocol mismatch")
    if meta.get("N") != M or meta.get("witness_sha256") != goal.EXPECTED_WITNESS or meta.get("K36_keys_sha256") != goal.EXPECTED_K36:
        raise ValueError("lower predictor identity mismatch")
    if sha(directory/"nodes.npy") != meta["nodes_sha256"] or sha(directory/"rhs.npy") != meta["rhs_sha256"]:
        raise ValueError("lower predictor hash mismatch")
    E = arb(0); bounds=[]
    for j in range(120):
        row=json.loads((directory/f"{j:03d}.json").read_text())
        digest=hashlib.sha256(b"".join(a.tobytes() for a in (nodes[j],nodes[j+1],rhs[j],rhs[j+1]))).hexdigest()
        if row["step"]!=j or row["input_binary_sha256"]!=digest:
            raise ValueError(("primal segment input mismatch",j))
        if j==0 and row.get("exact_rational_initial_field_sha256")!=goal.EXPECTED_WITNESS:
            raise ValueError("exact initial field missing")
        R=arb(row["residual_L2_upper_decimal"]); G=arb(row["gradient_Fourier_l1_upper_decimal"])
        if not R>=0 or not G>=0: raise ValueError("negative primal majorant")
        # Reproduce the archived conservative recurrence without tightening it.
        S=G
        E=arb(safe_decimal_upper((S*H).exp()*(E+H*R),12))
        bounds.append(E)
    return bounds

def primal_coefficients(low,nodes,rhs,j):
    binary=[projected_rows(low,a) for a in (nodes[j],nodes[j+1],rhs[j],rhs[j+1])]
    decimal=[primal.solenoidal_reality_projection(low,a) for a in (nodes[j],nodes[j+1],rhs[j],rhs[j+1])]
    if j==0:
        field,_,whash=exact.input_state(WITNESS)
        if whash!=goal.EXPECTED_WITNESS: raise ValueError("witness hash mismatch")
        initial=primal.exact_rational_state(low,field)
        binary[0]=initial; decimal[0]=initial
    ub=hermite(*binary,H); ud=hermite(*decimal,H)
    difference=[[[ub[d][i][t]-ud[d][i][t] for t in range(3)] for i in range(len(low.modes))] for d in range(4)]
    return ub,sup_norm(difference)

def terminal_error(low,high,nodes,adj,primal_radius,coeff):
    fixed=DealiasedSystem(11,nu=.1)
    a=projected_rows(low,nodes[-1])
    point_a=[a[low.index[k]] for k in fixed.modes]
    decimal_a=primal.solenoidal_reality_projection(low,nodes[-1])
    delta=norm([[a[i][j]-decimal_a[i][j] for j in range(3)] for i in range(len(a))])
    radius=(primal_radius+delta).upper()
    box=[[acb(z.real+arb(0,radius),z.imag+arb(0,radius)) for z in row] for row in point_a]
    _, gbox, _=goal.analytic_gradient(fixed,box,coeff)
    terminal=projected_rows(high,adj[-1])
    gfull=[[acb(0) for _ in range(3)] for _ in high.modes]
    for i,k in enumerate(fixed.modes): gfull[high.index[k]]=gbox[i]
    return norm([[gfull[i][j]-terminal[i][j] for j in range(3)] for i in range(len(high.modes))]),radius

def self_check():
    ctx.prec=192
    # Regression gate: large values at micro precision must serialize above
    # the exact Arb upper endpoint without a binary64 round trip.
    for raw, places in (("771116932371.42349", 6),
                        ("771170816631.115284", 6),
                        ("1e100", 6), ("1/3", 18)):
        x = arb(raw) if raw != "1/3" else arb(1) / 3
        text = safe_decimal_upper(x, places)
        mid, rad, exp = (int(v) for v in x.mid_rad_10exp())
        exact_arb_upper = Fraction(mid + rad) * (Fraction(10) ** exp)
        if decimal_fraction(text) <= exact_arb_upper:
            raise ValueError("outward-decimal formatter self-check failed")
    print("PASS integer-only outward decimal serialization",flush=True)
    s=DealiasedSystem(2,nu=.1); rng=np.random.default_rng(20261001)
    c=[]
    for _ in range(8):
        x=(rng.integers(-3,4,(len(s.modes),3))+1j*rng.integers(-3,4,(len(s.modes),3)))/8
        c.append(projected_rows(s,x))
    u,lam=c[:4],c[4:]
    got=packed_vjp(s,u,lam)
    direct=[[[acb(0) for _ in range(3)] for _ in s.modes] for _ in range(7)]
    for ki,k in enumerate(s.modes):
        kk=int(s.square[ki])
        if not kk: continue
        for pi,p in enumerate(s.modes):
            qi=s.index.get(tuple(int(k[t])-int(p[t]) for t in range(3)))
            if qi is None: continue
            q=s.modes[qi]
            for a in range(4):
                for b in range(4):
                    dot=sum((lam[a][pi][i]*u[b][qi][i] for i in range(3)),acb(0))
                    adv=sum((u[b][pi][i]*int(q[i]) for i in range(3)),acb(0))
                    for j in range(3): direct[a+b][ki][j]+=acb(0,1)*(int(q[j])*dot-adv*lam[a][qi][j])
        for d in range(7):
            kd=sum((direct[d][ki][t]*int(k[t]) for t in range(3)),acb(0))
            for t in range(3): direct[d][ki][t]-=kd*int(k[t])/kk
    max_error=arb(0)
    for d in range(7):
        for i in range(len(s.modes)):
            for t in range(3):
                diff=got[d][i][t]-direct[d][i][t]
                if not diff.contains(0): raise ValueError(("independent polynomial coefficient disagreement",d,i,t,str(diff)))
                max_error=max_error.max(diff.abs_upper()).upper()
    if not max_error<arb("1e-45"): raise ValueError("self-check arithmetic radius too wide")
    print("PASS independent explicit Fourier temporal-coefficient check",str(max_error),flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-check",action="store_true")
    ap.add_argument("--M",type=int,default=14)
    ap.add_argument("--step",type=int,default=239,help="forward half-step index; backward order is 239..0")
    for name in ("lower-dir","adjoint-dir","sign-chart","c500","output"):
        ap.add_argument("--"+name,type=Path)
    args=ap.parse_args(); ctx.prec=192
    if args.self_check: self_check(); return
    if args.M!=14 or not 0<=args.step<240: raise ValueError("this pilot supports M14 only")
    if any(getattr(args,n.replace('-','_')) is None for n in ("lower-dir","adjoint-dir","sign-chart","c500","output")):
        ap.error("pilot requires all input directories/files and --output")
    started=time.monotonic(); M=args.M; n=args.step; j=n//2; sub=n%2
    if sha(WITNESS)!=goal.EXPECTED_WITNESS or sha(K36)!=goal.EXPECTED_K36: raise ValueError("frozen input mismatch")
    coeff, _, _, semantic = frozen_goal.load_coefficients(args.sign_chart,args.c500)
    if semantic != goal.EXPECTED_C500_SEMANTIC:
        raise ValueError("coefficient semantic mismatch")
    report_path=args.adjoint_dir/f"M{M}_arb_vjp_point.json"
    if sha(report_path)!=EXPECTED_C1_M14: raise ValueError("c1 report not the frozen M14 report")
    report=json.loads(report_path.read_text()); identities=report["frozen"]
    if report.get("status") != "PASS ARB VJP CROSSCHECK AND ADJOINT PATH EXPORT":
        raise ValueError("c1 report did not pass")
    if identities.get("witness_sha256") != goal.EXPECTED_WITNESS or identities.get("K36_sha256") != goal.EXPECTED_K36 or identities.get("K36_sign_chart_sha256") != goal.EXPECTED_SIGN_CHART:
        raise ValueError("c1 frozen identities mismatch")
    if identities["C500_portable_semantic_sha256"]!=goal.EXPECTED_C500_SEMANTIC: raise ValueError("c1 semantic mismatch")
    rec=report["adjoint_reconstruction"]
    paths={k:args.adjoint_dir/rec[k+"_file"] for k in ("values","rhs")}
    for k,p in paths.items():
        if sha(p)!=rec[k+"_sha256"]: raise ValueError("adjoint array hash mismatch")
    for k in ("nodes","rhs","metadata"):
        p=args.lower_dir/(k+".json" if k=="metadata" else k+".npy")
        if sha(p)!=rec["lower_"+k+"_sha256"]: raise ValueError("c1 lower input hash mismatch")
    low=DealiasedSystem(M,nu=.1); high=DealiasedSystem(M+1,nu=.1)
    nodes=np.load(args.lower_dir/"nodes.npy",mmap_mode="r"); rhs=np.load(args.lower_dir/"rhs.npy",mmap_mode="r")
    adj=np.load(paths["values"],mmap_mode="r"); arhs=np.load(paths["rhs"],mmap_mode="r")
    if adj.shape!=(241,len(high.modes),3) or arhs.shape!=adj.shape or nodes.shape!=(121,len(low.modes),3) or rhs.shape!=nodes.shape:
        raise ValueError("array shape mismatch")
    radii=old_radius_and_identity(args.lower_dir,nodes,rhs,M)
    epsilon0,terminal_radius=terminal_error(low,high,nodes,adj,radii[-1],coeff)
    ub,delta=primal_coefficients(low,nodes,rhs,j)
    ub=restrict(ub,arb(sub)/2,arb(1)/2)
    U=embed(low,high,ub)
    L=hermite(*[projected_rows(high,a) for a in (adj[n],adj[n+1],arhs[n],arhs[n+1])],HALF_H)
    print("input and terminal-gradient enclosure ready",round(time.monotonic()-started,3),flush=True)
    vjp=packed_vjp(high,U,L)
    residual=[]
    for d in range(7):
        residual.append([[((d+1)*L[d+1][i][t]/HALF_H if d<3 else 0)
                          -vjp[d][i][t]-(NU*int(high.square[i])*L[d][i][t] if d<4 else 0)
                          for t in range(3)] for i in range(len(high.modes))])
    Rpoly=sup_norm(residual); lsup=sup_norm(L)
    delta_true=(radii[j]+delta).upper()
    ksq=sum(int(v) for v in low.square); count=len(low.modes)
    perturb=(arb(ksq).sqrt()+arb(M+1)*arb(count).sqrt())*delta_true*lsup
    R=(Rpoly+perturb).upper()
    strain=(sup_strain(low,ub)+(arb(ksq)/2).sqrt()*delta_true).upper()
    out={"schema":PROTOCOL,"status":"CONTINUOUS_SEGMENT_ENCLOSURE_ONLY","M":M,"step":n,
         "forward_time_interval_rational":[f"{n}/80000",f"{n+1}/80000"],"backward_order_index":239-n,
         "precision_bits":ctx.prec,"source_sha256":sha(Path(__file__)),"frozen":identities,
         "inputs":{"adjoint_report_sha256":sha(report_path),"adjoint_values_sha256":sha(paths["values"]),
                   "adjoint_rhs_sha256":sha(paths["rhs"]),"lower_nodes_sha256":sha(args.lower_dir/"nodes.npy"),
                   "lower_rhs_sha256":sha(args.lower_dir/"rhs.npy"),"primal_segment_sha256":sha(args.lower_dir/f"{j:03d}.json")},
         "bounds":{"nominal_residual_L2_upper":safe_decimal_upper(Rpoly,6),
                   "primal_uncertainty_residual_penalty_upper":safe_decimal_upper(perturb,6),
                   "residual_L2_upper":safe_decimal_upper(R,6),"logarithmic_norm_upper":safe_decimal_upper(strain,9),
                   "adjoint_polynomial_L2_upper":safe_decimal_upper(lsup,6),
                   "binary_decimal_predictor_distance_upper":safe_decimal_upper(delta,18),
                   "true_primal_radius_upper":safe_decimal_upper(delta_true,15),
                   "terminal_primal_radius_upper":safe_decimal_upper(terminal_radius,15),
                   "terminal_adjoint_error_upper":safe_decimal_upper(epsilon0,6)},
         "whole_segment_method":"degree-six Fourier-valued residual; Bernstein convex-hull L2 bound; exact dyadic imports/projections; old primal radius plus predictor-centre discrepancy",
         "elapsed_seconds":time.monotonic()-started,
         "claim_boundary":"One finite M14->15 half-step enclosure only; no complete adjoint path, dual quadrature, transfer theorem, all-N or continuum claim."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    tmp=args.output.with_suffix(".tmp"); tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); tmp.replace(args.output)
    print(json.dumps(out,indent=2),flush=True)

if __name__=="__main__": main()
