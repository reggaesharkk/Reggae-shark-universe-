#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED='7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47'
SQ=10**36

def C(z): return (F(str(float(np.real(z)))),F(str(float(np.imag(z)))))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,s): return (a[0]*s,a[1]*s)
def conj(a): return (a[0],-a[1])
def abs2(a): return a[0]*a[0]+a[1]*a[1]
def vdot(a,b):
    r=(F(0),F(0))
    for x,y in zip(a,b): r=add(r,mul(conj(x),y))
    return r
def orbit(k): return tuple(sorted(abs(int(x)) for x in k))
def project(k,v):
    kk=sum(int(x)*int(x) for x in k); kd=(F(0),F(0))
    for x,y in zip(k,v): kd=add(kd,scale(y,int(x)))
    return [sub(y,scale(kd,F(int(x),kk))) for x,y in zip(k,v)]
def exact_state(system,arr):
    a=[[(F(0),F(0)) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        if tuple(k)<=tuple(-int(v) for v in k): continue
        kk=int(system.square[ix]); raw=[C(z) for z in arr[ix]]; kd=(F(0),F(0))
        for j in range(3): kd=add(kd,scale(raw[j],int(k[j])))
        tr=[sub(raw[j],scale(kd,F(int(k[j]),kk))) for j in range(3)]
        a[ix]=tr; a[system.neg[ix]]=[conj(v) for v in tr]
    return a
def sqrt_upper(q:F,scale_int=SQ):
    if q<0: raise ValueError
    if q==0:return F(0)
    n=q.numerator*scale_int*scale_int; d=q.denominator
    m=math.isqrt(n//d)
    while F(m*m,scale_int*scale_int)<q: m+=1
    return F(m,scale_int)
def sqrt_lower(q:F,scale_int=SQ):
    if q<=0:return F(0)
    n=q.numerator*scale_int*scale_int; d=q.denominator
    m=math.isqrt(n//d)
    while F((m+1)*(m+1),scale_int*scale_int)<=q: m+=1
    while F(m*m,scale_int*scale_int)>q:m-=1
    return F(m,scale_int)
def norm_upper(vec): return sqrt_upper(sum((abs2(v) for v in vec),F(0)))
def dec(q,places=12): return f'{float(q):.{places}g}'

def run(N,nodes,keys_path,E_decimal,repo_src,out):
    sys.path.insert(0,str(Path(repo_src).resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem
    system=DealiasedSystem(N); arr=np.load(nodes,mmap_mode='r')[-1]; a=exact_state(system,arr)
    raw=Path(keys_path).read_bytes(); sha=hashlib.sha256(raw).hexdigest()
    if sha!=EXPECTED: raise SystemExit('K36 hash mismatch')
    krows=json.loads(raw)['keys']; keys=[(tuple(r['left_orbit']),tuple(r['right_orbit'])) for r in krows]; keyset=set(keys)
    p,q,k=[system.index[x] for x in (P,Q,K)]
    qdot=(F(0),F(0))
    for j in range(3): qdot=add(qdot,scale(a[p][j],Q[j]))
    b=project(K,[mul((F(0),F(1)),mul(qdot,a[q][i])) for i in range(3)])
    W=int(system.square[k]**2); z=scale(vdot(a[k],b),-W); z2=abs2(z)
    groups={}; ds={}
    for li,ri in zip(system.left,system.right):
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        if key not in keyset: continue
        wave=system.waves[ri]; dot=(F(0),F(0))
        for j in range(3): dot=add(dot,scale(a[li][j],int(wave[j])))
        rawv=[mul((F(0),F(1)),mul(dot,a[ri][i])) for i in range(3)]
        d=[scale(v,-1) for v in project(K,rawv)]
        w=scale(vdot(d,b),-W)
        groups[key]=add(groups.get(key,(F(0),F(0))),w)
        ds[key]=ds.get(key,F(0))+norm_upper(d)
    E=F(E_decimal); A=norm_upper([v for row in a for v in row]); bp,bq,bk=(norm_upper(a[ix]) for ix in (p,q,k)); B=norm_upper(b); dq=sqrt_upper(F(sum(x*x for x in Q)))
    db=dq*E*(bp+bq+E); dd=F(N)*(2*A*E+E*E); dz=F(W)*(E*B+(bk+E)*db); zup=sqrt_upper(z2); zlo=sqrt_lower(z2)
    outs=[]
    for row,key in zip(krows,keys):
        w=groups[key]; n=(mul(w,conj(z)))[1]; wup=sqrt_upper(abs2(w)); dw=F(W)*(dd*B+(ds[key]+dd)*db); dn=dw*zup+(wup+dw)*dz
        locked=abs(n)>dn; sgn=1 if n>0 else -1 if n<0 else 0
        ratio=abs(n)/dn if dn else F(10**99)
        outs.append({'left_orbit':row['left_orbit'],'right_orbit':row['right_orbit'],'nominal_sign':sgn,'sign_locked':locked,'abs_n_decimal':dec(abs(n),15),'delta_n_upper_decimal':dec(dn,15),'margin_ratio_decimal':dec(ratio,12),'n_exact_fraction':f'{n.numerator}/{n.denominator}','delta_n_upper_fraction':f'{dn.numerator}/{dn.denominator}'})
    locked_count=sum(x['sign_locked'] for x in outs); worst=min(outs,key=lambda x:float(x['margin_ratio_decimal']))
    res={'schema':'wp19-v0.9-k36-sign-lock-exact-rational-v1','status':'PASS' if locked_count==36 else 'PARTIAL','N':N,'E_input_decimal':E_decimal,'K36_sha256':sha,'group_count':36,'sign_locked_count':locked_count,'all_36_sign_locked':locked_count==36,'sqrt_bound_scale_decimal_digits':36,'z_abs_lower_decimal':dec(zlo,15),'delta_z_upper_decimal':dec(dz,15),'worst_sign_margin':{k:worst[k] for k in ['left_orbit','right_orbit','margin_ratio_decimal','abs_n_decimal','delta_n_upper_decimal']},'rows':outs}
    Path(out).write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({k:v for k,v in res.items() if k!='rows'},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--N',type=int,required=True); ap.add_argument('--nodes',required=True); ap.add_argument('--keys',required=True); ap.add_argument('--E',required=True); ap.add_argument('--repo-src',required=True); ap.add_argument('--out',required=True)
    x=ap.parse_args(); run(x.N,x.nodes,x.keys,x.E,x.repo_src,x.out)
