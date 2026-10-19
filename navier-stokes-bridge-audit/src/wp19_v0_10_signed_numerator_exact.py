#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
P,Q,K=(3,2,2),(3,-2,1),(6,0,3)
EXPECTED_K36='7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47'
EXPECTED_C500='79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216'
SCALE=10**30

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
def sqrt_upper(q:F):
    if q<=0:return F(0)
    n=q.numerator*SCALE*SCALE; d=q.denominator; m=math.isqrt(n//d)
    while F(m*m,SCALE*SCALE)<q:m+=1
    return F(m,SCALE)
def sqrt_lower(q:F):
    if q<=0:return F(0)
    n=q.numerator*SCALE*SCALE; d=q.denominator; m=math.isqrt(n//d)
    while F((m+1)*(m+1),SCALE*SCALE)<=q:m+=1
    while F(m*m,SCALE*SCALE)>q:m-=1
    return F(m,SCALE)
def norm_upper(v): return sqrt_upper(sum((abs2(x) for x in v),F(0)))
def fmt(q,n=16): return f'{float(q):.{n}g}'

def run(N,nodes,k36_path,c500_path,E_decimal,repo_src,out):
    sys.path.insert(0,str(Path(repo_src).resolve()))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem
    if hashlib.sha256(Path(k36_path).read_bytes()).hexdigest()!=EXPECTED_K36: raise SystemExit('K36 hash mismatch')
    if hashlib.sha256(Path(c500_path).read_bytes()).hexdigest()!=EXPECTED_C500: raise SystemExit('C500 hash mismatch')
    s=DealiasedSystem(N); a=exact_state(s,np.load(nodes,mmap_mode='r')[-1]); E=F(E_decimal)
    krows=json.loads(Path(k36_path).read_text())['keys']; K36=[(tuple(r['left_orbit']),tuple(r['right_orbit'])) for r in krows]; Kset=set(K36)
    crows=json.loads(Path(c500_path).read_text())['keys']; taus={(tuple(r['left_orbit']),tuple(r['right_orbit'])):int(r['fixed_linear_sign']) for r in crows}; Cset=set(taus)
    wanted=Kset|Cset
    p,q,k=[s.index[x] for x in (P,Q,K)]; qdot=(F(0),F(0))
    for j in range(3): qdot=add(qdot,scale(a[p][j],Q[j]))
    b=project(K,[mul((F(0),F(1)),mul(qdot,a[q][i])) for i in range(3)])
    W=int(s.square[k]**2); z=scale(vdot(a[k],b),-W); z2=abs2(z)
    groups={}; pairmap={}; dsum={}
    mode_norm={i:norm_upper(a[i]) for i in range(len(a))}
    for li,ri in zip(s.left,s.right):
        key=(orbit(s.modes[li]),orbit(s.modes[ri]))
        if key not in wanted: continue
        wave=s.waves[ri]; dot=(F(0),F(0))
        for j in range(3): dot=add(dot,scale(a[li][j],int(wave[j])))
        raw=[mul((F(0),F(1)),mul(dot,a[ri][i])) for i in range(3)]
        d=[scale(v,-1) for v in project(K,raw)]; w=scale(vdot(d,b),-W)
        groups[key]=add(groups.get(key,(F(0),F(0))),w); dsum[key]=dsum.get(key,F(0))+norm_upper(d)
        pairmap.setdefault(key,[]).append((li,ri,int(sum(int(x)*int(x) for x in wave))))
    B=norm_upper(b); bp,bq,bk=(mode_norm[ix] for ix in (p,q,k)); dq=sqrt_upper(F(sum(x*x for x in Q)))
    db=dq*E*(bp+bq+E); dz=F(W)*(E*B+(bk+E)*db); zup=sqrt_upper(z2); zlo=sqrt_lower(z2); ztrue_lower=zlo-dz; ztrue_upper=zup+dz
    if ztrue_lower<=0: raise ValueError('normalizer guard failed')
    vals={}; locked=0
    for key,pairs in pairmap.items():
        cp={}; cq={}; q2sum=0
        for li,ri,q2 in pairs:
            qn=sqrt_upper(F(q2)); cp[li]=cp.get(li,F(0))+qn*mode_norm[ri]; cq[ri]=cq.get(ri,F(0))+qn*mode_norm[li]; q2sum+=q2
        C1=sqrt_upper(sum((x*x for x in cp.values()),F(0))); C2=sqrt_upper(sum((x*x for x in cq.values()),F(0))); C3=sqrt_upper(F(q2sum))
        dd=(C1+C2)*E+C3*E*E; dw=F(W)*(dd*B+(dsum[key]+dd)*db); w=groups[key]; n=mul(w,conj(z))[1]; wup=sqrt_upper(abs2(w)); dn=dw*zup+(wup+dw)*dz
        vals[key]={'n':n,'dn':dn,'pairs':len(pairs),'dd':dd}
    J=F(0); err=F(0); signrows=[]
    for key,row in zip(K36,krows):
        n=vals[key]['n']; dn=vals[key]['dn']; sgn=1 if n>0 else -1 if n<0 else 0; lock=abs(n)>dn; locked+=lock; J+=sgn*n; err+=dn
        signrows.append({'left_orbit':row['left_orbit'],'right_orbit':row['right_orbit'],'sign':sgn,'locked':lock,'abs_n':fmt(abs(n)),'delta_n':fmt(dn),'ratio':fmt(abs(n)/dn,12)})
    for key,tau in taus.items():
        n=vals[key]['n']; dn=vals[key]['dn']; J-=9*tau*n; err+=9*dn
    upper=J+err; lower=J-err
    res={'schema':'wp19-v0.10-signed-c500-numerator-certificate-v1','status':'PASS' if locked==36 and upper<0 else 'FAIL','N':N,'E_input_decimal':E_decimal,'K36_sha256':EXPECTED_K36,'C500_sha256':EXPECTED_C500,'K36_sign_locked_count':locked,'normalizer_true_lower_bound_decimal':fmt(ztrue_lower),'normalizer_true_upper_bound_decimal':fmt(ztrue_upper),'nominal_signed_numerator_decimal':fmt(J),'signed_numerator_error_upper_decimal':fmt(err),'true_signed_numerator_lower_decimal':fmt(lower),'true_signed_numerator_upper_decimal':fmt(upper),'certified_signed_numerator_negative':upper<0,'certified_G_upper_decimal':fmt(upper/(ztrue_upper*ztrue_upper)) if upper<0 else None,'nominal_G_from_signed_numerator_decimal':fmt(J/z2),'error_as_nominal_z2_ratio_decimal':fmt(err/z2),'pairwise_group_perturbation_method':'For each retained group, bound source perturbation by Cauchy over repeated left/right indices: delta_d_g <= (C1_g+C2_g)E + C3_g E^2; then propagate through w_g and n_g exactly with rational upper square-root enclosures.','sqrt_grid_denominator':'1e30','K36_sign_rows':signrows,'continuum_claim':False}
    Path(out).write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({k:v for k,v in res.items() if k!='K36_sign_rows'},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--N',type=int,required=True); ap.add_argument('--nodes',required=True); ap.add_argument('--k36',required=True); ap.add_argument('--c500',required=True); ap.add_argument('--E',required=True); ap.add_argument('--repo-src',required=True); ap.add_argument('--out',required=True)
    x=ap.parse_args(); run(x.N,x.nodes,x.k36,x.c500,x.E,x.repo_src,x.out)
