#!/usr/bin/env python3
"""Verification companion for Prince Upadhyay, LRSC Odd-Ring Rank Theorem v1.2.

This script is not the proof.  It checks the closed-form identities numerically,
checks the decisive inequalities over a large finite range, and performs exact
cyclotomic non-vanishing checks for M=99,101,127.
"""
import math
import numpy as np
import sympy as sp

A0=0.5
THETA=0.08

def closed_j(M,A=A0):
    k=(M-1)//2
    idx=np.arange(M)
    t=np.where(idx<=k,idx,idx-M)
    u=np.abs(t)
    out=np.zeros(M)
    even=(u%2==0)
    out[even & (u==0)] = A*(1+np.cos(np.pi/M))
    nz=even & (u>0)
    out[nz] = A*(np.cos(np.pi*u[nz]/M)+np.cos(np.pi*(u[nz]-1)/M))
    return out

def direct_j(M,A=A0):
    k=(M-1)//2
    i=np.arange(M)
    X=1+A*np.cos(2*np.pi*k*i/M)
    return X-np.minimum.reduce([np.roll(X,1),X,np.roll(X,-1)])

def simple_jhat(M,r,A=A0):
    alpha=math.pi/M
    eps=-1 if r%2 else 1
    den=math.sin((2*r-1)*alpha)*math.sin((2*r+1)*alpha)
    pref=2*A*math.cos(alpha/2)/M
    if M%4==3:
        B=-math.sin(2*alpha)*(eps*math.cos(r*alpha)+math.sin(alpha/2))/(2*den)
    else:
        B=-math.sin(alpha)*(eps*math.cos(r*alpha)*math.cos(2*r*alpha)+math.cos(alpha)*math.sin(alpha/2))/den
    return pref*B

def active_orbits(M,A=A0,theta=THETA):
    k=(M-1)//2
    i=np.arange(M)
    X=1+A*np.cos(2*np.pi*k*i/M)
    L=np.roll(X,1); R=np.roll(X,-1)
    C=.5*((X-L)**2+(X-R)**2)
    act=np.where(C>theta)[0]
    return len(set(np.minimum(act,M-act).tolist()))

z=sp.symbols('z')
def cyclo_poly_reduced(M,r):
    L=(M-1)//4
    N=2*M
    coeff=[0]*N
    def add(e,c=1): coeff[e%N]+=c
    add(0,2); add(1); add(-1)
    for u in range(1,L+1):
        for a in (2*u,-2*u,2*u-1,-(2*u-1)):
            for b in (4*r*u,-4*r*u):
                add(a+b)
    return sp.Poly.from_dict({(e,):c for e,c in enumerate(coeff) if c},z,domain=sp.ZZ)

def exact_ring(M,p):
    phi=sp.Poly(sp.cyclotomic_poly(2*M,z),z,domain=sp.ZZ)
    zeros=[]
    for r in range(p):
        rem=cyclo_poly_reduced(M,r).rem(phi)
        if rem.is_zero:
            zeros.append(r)
    return zeros

def main():
    print("LRSC ODD-RING RANK THEOREM v1.2 - VERIFICATION COMPANION")
    print("Author: Prince Upadhyay, Independent Research")
    print()

    spatial_max=0.0
    for M in [9,11,99,101,127,301]:
        spatial_max=max(spatial_max,float(np.max(np.abs(direct_j(M)-closed_j(M)))))
    print(f"[1] closed spatial shedding formula max discrepancy = {spatial_max:.17e}")

    maxerr=0.0
    minabs=float('inf')
    minloc=None
    count=0
    for M in range(9,2002,2):
        k=(M-1)//2
        hj=np.fft.fft(closed_j(M))/M
        for r in range(k):
            v=simple_jhat(M,r)
            err=abs(v-hj[r].real)
            maxerr=max(maxerr,err)
            if abs(v)<minabs:
                minabs=abs(v); minloc=(M,r)
            count+=1
    print(f"[2] simplified Fourier formula checks = {count}")
    print(f"    max discrepancy = {maxerr:.17e}")
    print(f"    smallest observed |jhat_r| = {minabs:.17e} at M={minloc[0]}, r={minloc[1]}")

    failures=[]
    for M in range(9,2002,4):
        L=(M-1)//4
        alpha=math.pi/M
        c=math.cos(alpha)*math.sin(alpha/2)
        mid=abs(math.cos(L*alpha)*math.cos(2*L*alpha))
        others=[abs(math.cos(r*alpha)*math.cos(2*r*alpha)) for r in range(2*L) if r!=L]
        if not (mid<c and min(others)>c):
            failures.append(M)
    print(f"[3] M=4L+1 decisive inequality failures on M<=2001 = {failures}")

    for M in [99,101,127]:
        p=active_orbits(M)
        zeros=exact_ring(M,p)
        print(f"[4] exact cyclotomic M={M}, required r=0..{p-1}: zeros={zeros}")

    if failures:
        raise SystemExit("FAIL: inequality stress check")
    print("\nSTATUS: PASS")
    print("NOTE: finite checks support the analytic proof; they do not replace it.")

if __name__=='__main__':
    main()
