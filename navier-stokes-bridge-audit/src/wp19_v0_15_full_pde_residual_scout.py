#!/usr/bin/env python3
"""WP19 v0.15 full-PDE truncation-residual scout.

NON-RIGOROUS: evaluates saved N14 predictor nodes in floating point.
The separately validated N14 Galerkin certificate is not replaced by this scout.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

def modes_in_ball(N):
    return np.asarray([(i,j,k)
        for i in range(-N,N+1)
        for j in range(-N,N+1)
        for k in range(-N,N+1)
        if i*i+j*j+k*k <= N*N], dtype=np.int16)

def trap(vals,h):
    vals=np.asarray(vals,float)
    return h*(0.5*vals[0]+vals[1:-1].sum()+0.5*vals[-1])

def lp_time(vals,h,p):
    vals=np.asarray(vals,float)
    return (h*(0.5*vals[0]**p+(vals[1:-1]**p).sum()+0.5*vals[-1]**p))**(1/p)

def projected_full_nonlinear(a,modes,N):
    L=4*N+1
    slots=tuple((modes[:,j].astype(int)%L) for j in range(3))
    f=np.zeros((L,L,L,3),np.complex128)
    f[slots]=a
    u=np.fft.ifftn(f,axes=(0,1,2))*L**3
    freqs=np.fft.fftfreq(L)*L
    prod=np.zeros_like(u)
    for j in range(3):
        shape=[1,1,1]; shape[j]=L
        kg=freqs.reshape(shape)
        grad=np.fft.ifftn(1j*kg[...,None]*f,axes=(0,1,2))*L**3
        prod += u[...,j,None]*grad
    conv=np.fft.fftn(prod,axes=(0,1,2))/L**3
    kx=freqs[:,None,None]; ky=freqs[None,:,None]; kz=freqs[None,None,:]
    k2=kx*kx+ky*ky+kz*kz
    kd=conv[...,0]*kx+conv[...,1]*ky+conv[...,2]*kz
    out=conv.copy()
    nz=k2>0
    for comp,kg in enumerate((kx,ky,kz)):
        correction=np.zeros_like(kd)
        correction[nz]=(kd*kg)[nz]/k2[nz]
        out[...,comp]-=correction
    return out,k2,u

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nodes",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--N",type=int,default=14)
    ap.add_argument("--h",type=float,default=0.000025)
    args=ap.parse_args()

    modes=modes_in_ball(args.N)
    nodes=np.load(args.nodes,mmap_mode="r")
    if nodes.shape[1] != len(modes):
        raise ValueError("mode count mismatch")
    sq=np.sum(modes.astype(np.int64)**2,axis=1).astype(float)

    h1=[];h2=[];h3=[];l2=[]
    rm1=[];r0=[];r1=[];r2=[]
    l3=[];l6=[]

    for a in nodes:
        coeff2=np.sum(np.abs(a)**2,axis=1)
        l2.append(float(np.sqrt(np.sum(coeff2))))
        h1.append(float(np.sqrt(np.sum(coeff2*sq))))
        h2.append(float(np.sqrt(np.sum(coeff2*sq**2))))
        h3.append(float(np.sqrt(np.sum(coeff2*sq**3))))

        ng,k2,u=projected_full_nonlinear(np.asarray(a),modes,args.N)
        mask=k2>args.N**2
        q2=k2[mask]
        vec2=np.sum(np.abs(ng[mask])**2,axis=1)
        rm1.append(float(np.sqrt(np.sum(vec2/q2))))
        r0.append(float(np.sqrt(np.sum(vec2))))
        r1.append(float(np.sqrt(np.sum(vec2*q2))))
        r2.append(float(np.sqrt(np.sum(vec2*q2**2))))

        mag=np.sqrt(np.sum(np.abs(u)**2,axis=3))
        l3.append(float(np.mean(mag**3)**(1/3)))
        l6.append(float(np.mean(mag**6)**(1/6)))

    result={
      "status":"NON-RIGOROUS NODE-SAMPLED SCOUT",
      "N":args.N,"h":args.h,"nodes":len(nodes),
      "solution":{
        "Linf_L2":max(l2),"Linf_Hdot1":max(h1),
        "Linf_Hdot2":max(h2),"Linf_Hdot3":max(h3),
        "Linf_L3_grid":max(l3),"Linf_L6_grid":max(l6),
        "L4t_L6_grid":lp_time(l6,args.h,4),
        "L2t_Hdot2":lp_time(h2,args.h,2)
      },
      "tail_residual":{
        "Hminus1_max":max(rm1),"Hminus1_L1t":trap(rm1,args.h),
        "Hminus1_L2t":lp_time(rm1,args.h,2),
        "Hminus1_L3t":lp_time(rm1,args.h,3),
        "L2_max":max(r0),"L2_L1t":trap(r0,args.h),
        "L2_L2t":lp_time(r0,args.h,2),
        "H1_max":max(r1),"H1_L1t":trap(r1,args.h),
        "H1_L2t":lp_time(r1,args.h,2),
        "H2_max":max(r2),"H2_L1t":trap(r2,args.h)
      }
    }
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
