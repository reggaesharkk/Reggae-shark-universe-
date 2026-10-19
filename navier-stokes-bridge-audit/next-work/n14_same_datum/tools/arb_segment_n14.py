"""Arb ball enclosure of one cubic-Hermite Galerkin residual segment.

Requires python-flint. This is the same polynomial/Bernstein construction used
by the validated N11-N13 certificate family, made local to the N14 package.
"""
from math import comb
import numpy as np
from flint import acb, acb_poly, arb, ctx

def ball(z):
    return acb(str(float(np.real(z))), str(float(np.imag(z))))

def solenoidal_reality_projection(system, array):
    result=[[acb(0) for _ in range(3)] for _ in system.modes]
    for ix,k in enumerate(system.modes):
        if tuple(k)<=tuple(-v for v in k):
            continue
        kk=int(system.square[ix])
        raw=[ball(z) for z in array[ix]]
        kd=sum((raw[j]*int(k[j]) for j in range(3)),acb(0))
        transverse=[raw[j]-kd*int(k[j])/kk for j in range(3)]
        result[ix]=transverse
        result[system.neg[ix]]=[v.conjugate() for v in transverse]
    return result

def exact_rational_state(system, field):
    result=[]
    for k in system.modes:
        row=[]
        for real,imag in field.get(k,((0,0),)*3):
            rb=arb(real.numerator)/arb(real.denominator) if hasattr(real,"numerator") else arb(0)
            ib=arb(imag.numerator)/arb(imag.denominator) if hasattr(imag,"numerator") else arb(0)
            row.append(acb(rb,ib))
        result.append(row)
    return result

def carry_free_indices(system):
    base=4*system.N+1
    left=[(int(k[0])+system.N)+base*(int(k[1])+system.N)+base*base*(int(k[2])+system.N) for k in system.waves]
    right=[(int(k[0])+2*system.N)+base*(int(k[1])+2*system.N)+base*base*(int(k[2])+2*system.N) for k in system.waves]
    return left,right

def nonlinear(system,state,left,right):
    n=max(left)+1
    fields=[]
    for j in range(3):
        arr=[0]*n
        for ix,slot in enumerate(left):
            arr[slot]=state[ix][j]
        fields.append(acb_poly(arr))
    result=[[acb(0) for _ in range(3)] for _ in system.modes]
    for target in range(3):
        component=[acb(0) for _ in system.modes]
        for direction in range(3):
            arr=[0]*n
            for ix,slot in enumerate(left):
                arr[slot]=state[ix][target]*acb(0,int(system.waves[ix,direction]))
            product=fields[direction]*acb_poly(arr)
            component=[v+product[slot] for v,slot in zip(component,right)]
        for ix,v in enumerate(component):
            result[ix][target]=v
    for ix,k in enumerate(system.waves):
        kk=int(system.square[ix])
        if kk==0:
            result[ix]=[acb(0)]*3
            continue
        kd=sum(result[ix][j]*int(k[j]) for j in range(3))
        result[ix]=[result[ix][j]-kd*arb(int(k[j]))/kk for j in range(3)]
    return result

def ball_l2_upper(values):
    total=arb(0)
    for z in values:
        v=z.abs_upper()
        total+=v*v
    return total.sqrt().upper()

def enclose(system,a,b,f,g,h,exact_initial_field=None):
    ctx.prec=128
    hh=arb(str(h))
    A,B,F,G=[solenoidal_reality_projection(system,array) for array in (a,b,f,g)]
    if exact_initial_field is not None:
        A=exact_rational_state(system,exact_initial_field)
    C=[]
    for i in range(len(system.modes)):
        c0=A[i]
        c1=[hh*v for v in F[i]]
        c2=[3*(B[i][j]-A[i][j])-hh*(2*F[i][j]+G[i][j]) for j in range(3)]
        c3=[2*(A[i][j]-B[i][j])+hh*(F[i][j]+G[i][j]) for j in range(3)]
        C.append((c0,c1,c2,c3))
    power=[[C[k][i] for k in range(len(C))] for i in range(4)]
    left,right=carry_free_indices(system)
    base=[nonlinear(system,v,left,right) for v in power]
    quadratic=[[[acb(0) for _ in range(3)] for _ in system.modes] for _ in range(7)]
    for i in range(4):
        for k in range(len(system.modes)):
            for t in range(3):
                quadratic[2*i][k][t]+=base[i][k][t]
        for j in range(i+1,4):
            summed=[[power[i][k][t]+power[j][k][t] for t in range(3)] for k in range(len(system.modes))]
            mix=nonlinear(system,summed,left,right)
            for k in range(len(system.modes)):
                for t in range(3):
                    quadratic[i+j][k][t]+=mix[k][t]-base[i][k][t]-base[j][k][t]
    residual=[]
    for degree in range(7):
        row=[]
        for k in range(len(system.modes)):
            row.append([
                quadratic[degree][k][t]
                +(power[degree][k][t]*arb(str(system.nu))*int(system.square[k]) if degree<4 else 0)
                +(power[degree+1][k][t]*(degree+1)/hh if degree<3 else 0)
                for t in range(3)
            ])
        residual.append(row)
    R=arb(0)
    for j in range(7):
        row=[]
        for k in range(len(system.modes)):
            row.extend(
                sum((residual[i][k][t]*arb(comb(j,i))/comb(6,i) for i in range(j+1)),acb(0))
                for t in range(3)
            )
        R=R.max(ball_l2_upper(row))
    M=arb(0)
    for j in range(4):
        bound=arb(0)
        for k in range(len(system.modes)):
            values=[
                sum((power[i][k][t]*arb(comb(j,i))/comb(3,i) for i in range(j+1)),acb(0))
                for t in range(3)
            ]
            bound+=ball_l2_upper(values)*arb(int(system.square[k])).sqrt()
        M=M.max(bound.upper())
    return R.upper(),M.upper()
