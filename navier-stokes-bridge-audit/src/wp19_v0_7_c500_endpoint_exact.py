#!/usr/bin/env python3
"""WP19 v0.7 exact-rational C500 endpoint upper certificate.

The saved predictor endpoint is interpreted by the same exact-decimal,
solenoidal-reality projection rule used by the Arb endpoint certificate.
G_C500 is then evaluated exactly with Fraction arithmetic.

The supplied existing endpoint certificate contributes the previously
Arb-certified universal coefficient-9 perturbation envelope. That envelope is
key-independent and therefore also applies to G_C500.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED_K36="7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47"
EXPECTED_C500="79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216"

def C(z): return (F(str(float(np.real(z)))),F(str(float(np.imag(z)))))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,s): return (a[0]*s,a[1]*s)
def conj(a): return (a[0],-a[1])

def vdot(a,b):
    r=(F(0),F(0))
    for x,y in zip(a,b):
        r=add(r,mul(conj(x),y))
    return r

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

def project(k,v):
    kk=sum(int(x)*int(x) for x in k)
    kd=(F(0),F(0))
    for x,y in zip(k,v):
        kd=add(kd,scale(y,int(x)))
    return [sub(y,scale(kd,F(int(x),kk))) for x,y in zip(k,v)]

def exact_decimal_projected_state(system,arr):
    a=[[(F(0),F(0)) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        if tuple(k)<=tuple(-int(v) for v in k):
            continue
        kk=int(system.square[ix])
        raw=[C(z) for z in arr[ix]]
        kd=(F(0),F(0))
        for j in range(3):
            kd=add(kd,scale(raw[j],int(k[j])))
        tr=[sub(raw[j],scale(kd,F(int(k[j]),kk))) for j in range(3)]
        a[ix]=tr
        a[system.neg[ix]]=[conj(v) for v in tr]
    return a

def fmt_scaled(n,places):
    sign='-' if n<0 else ''
    m=abs(n); s=10**places
    return f"{sign}{m//s}.{m%s:0{places}d}"

def floor_scaled(x,places):
    s=10**places
    return fmt_scaled(x.numerator*s//x.denominator,places)

def ceil_scaled(x,places):
    s=10**places
    return fmt_scaled(-((-x.numerator*s)//x.denominator),places)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo-src",type=Path,required=True)
    p.add_argument("--N",type=int,required=True)
    p.add_argument("--nodes",type=Path,required=True)
    p.add_argument("--k36",type=Path,required=True)
    p.add_argument("--c500",type=Path,required=True)
    p.add_argument("--arb-endpoint-certificate",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()

    if hashlib.sha256(a.k36.read_bytes()).hexdigest()!=EXPECTED_K36:
        raise SystemExit("K36 hash mismatch")
    if hashlib.sha256(a.c500.read_bytes()).hexdigest()!=EXPECTED_C500:
        raise SystemExit("C500 hash mismatch")

    sys.path.insert(0,str(a.repo_src.resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    system=DealiasedSystem(a.N)
    state=exact_decimal_projected_state(
        system,np.load(a.nodes,mmap_mode="r")[-1]
    )
    K36={(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
         for r in json.loads(a.k36.read_text())["keys"]}
    cobj=json.loads(a.c500.read_text())
    taus={(tuple(r["left_orbit"]),tuple(r["right_orbit"])):
          int(r["fixed_linear_sign"]) for r in cobj["keys"]}

    pidx,qidx,kidx=[system.index[x] for x in (P,Q,K)]
    qdot=(F(0),F(0))
    for j in range(3):
        qdot=add(qdot,scale(state[pidx][j],Q[j]))
    b=project(K,[mul((F(0),F(1)),mul(qdot,state[qidx][i]))
                 for i in range(3)])
    weight=int(system.square[kidx]**2)
    z=scale(vdot(state[kidx],b),-weight)
    z2=z[0]*z[0]+z[1]*z[1]
    if z2<=0:
        raise ValueError("zero normalizer")

    groups={}
    for li,ri in zip(system.left,system.right):
        wave=system.waves[ri]
        dot=(F(0),F(0))
        for j in range(3):
            dot=add(dot,scale(state[li][j],int(wave[j])))
        raw=[mul((F(0),F(1)),mul(dot,state[ri][i])) for i in range(3)]
        d=[scale(v,-1) for v in project(K,raw)]
        w=scale(vdot(d,b),-weight)
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]=add(groups.get(key,(F(0),F(0))),w)

    numerator=F(0); full_num=F(0); present=0
    for key,w in groups.items():
        n=w[1]*z[0]-w[0]*z[1]
        full_num += abs(n) if key in K36 else -9*abs(n)
        if key in K36:
            numerator += abs(n)
        elif key in taus:
            numerator -= 9*taus[key]*n
            present += 1

    G=numerator/z2
    fullF=full_num/z2
    if fullF>G:
        raise ValueError("exact F <= G check failed")
    if present!=500:
        raise ValueError(f"only {present}/500 C500 keys present")

    cert=json.loads(a.arb_endpoint_certificate.read_text())
    ep=cert.get("endpoint",cert)
    err=F(str(ep["F_error_upper_decimal"]))
    lo,hi=G-err,G+err

    result={
        "schema":"wp19-v0.7-c500-endpoint-certificate-v1",
        "status":"PASS" if hi<0 else "FAIL",
        "N":a.N,
        "K36_sha256":EXPECTED_K36,
        "C500_sha256":EXPECTED_C500,
        "exact_decimal_endpoint_rule":
            "same canonical decimal solenoidal-reality projection as Arb endpoint certificate",
        "exact_group_count":len(groups),
        "C500_present_key_count":present,
        "G_C500_exact_fraction":f"{G.numerator}/{G.denominator}",
        "G_C500_exact_decimal_15":format(float(G),".15g"),
        "full_F_exact_decimal_15":format(float(fullF),".15g"),
        "exact_F_le_G":fullF<=G,
        "reused_Arb_universal_weight9_error_upper_decimal":
            str(ep["F_error_upper_decimal"]),
        "trajectory_error_input_decimal":str(ep.get("E_input_decimal","unknown")),
        "G_true_lower_decimal_9":floor_scaled(lo,9),
        "G_true_upper_decimal_9":ceil_scaled(hi,9),
        "certified_G_C500_negative":hi<0,
        "continuum_claim":False
    }
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
