"""Smooth dyadic square partition and exact finite-Galerkin commutator audit.

Run beside archived src modules: python src/smooth_commutator_gate.py
Writes smooth_commutator_results.json. This does not prove any uniform bound.
"""

import json
import math
from pathlib import Path

import numpy as np

from phase_cascade_trajectory import System, initial, integrate, DT, NU


def bump(t):
    out=np.zeros_like(t,dtype=float)
    inside=np.abs(t)<1
    out[inside]=np.exp(-1/(1-t[inside]**2))
    return out


def multipliers(sys):
    r=np.sqrt(sys.square)
    positive=r>0
    t=np.zeros_like(r)
    t[positive]=np.log2(r[positive])
    levels=range(math.ceil(math.log2(sys.N))+1)
    raw=np.array([bump(t-j) for j in levels])
    raw[:,~positive]=0
    length=np.sqrt(np.sum(raw**2,axis=0))
    assert np.min(length[positive])>0
    psi=np.divide(raw,length[None,:],out=np.zeros_like(raw),where=length[None,:]>0)
    assert np.max(abs(np.sum(psi[:,positive]**2,axis=0)-1))<1e-14
    return psi


def shell(sys,a,psi,j):
    pk=psi[j]
    out,left,right=sys.out,sys.left,sys.right
    qdot=np.einsum('ij,ij->i',sys.qwaves,a[left])
    aq=a[right]
    base=(1j*qdot)[:,None]*aq
    B=np.zeros_like(a)
    np.add.at(B,out,base)
    # C=[P_j,u.grad]u. The raw transport u.grad P_j u pairs to zero with P_j u.
    commE=np.zeros_like(a)
    np.add.at(commE,out,base*(pk[out]-pk[right])[:,None])
    aj=pk[:,None]*a
    S=-float(np.real(np.vdot(aj,pk[:,None]*B)))
    S_comm=-float(np.real(np.vdot(aj,commE)))
    assert np.isclose(S,S_comm,atol=1e-9,rtol=1e-12)
    Cgrad=np.zeros((len(a),3,3),complex)
    Stretch=np.zeros_like(Cgrad)
    for ell in range(3):
        cg=np.zeros_like(a)
        stretch=np.zeros_like(a)
        np.add.at(cg,out,base*(1j*sys.qwaves[:,ell]*(pk[out]-pk[right]))[:,None])
        np.add.at(stretch,out,base*(1j*sys.waves[left,ell]*pk[out])[:,None])
        Cgrad[:,ell,:]=cg
        Stretch[:,ell,:]=stretch
    grad_aj=1j*sys.waves[:,:,None]*aj[:,None,:]
    Tcomm=-float(np.real(np.vdot(grad_aj,Cgrad)))
    Tstretch=-float(np.real(np.vdot(grad_aj,Stretch)))
    n=np.einsum('kij,kj->ki',sys.projectors,B)
    term=np.real(np.einsum('ij,ij->i',np.conj(a),n))
    T=-float(np.dot(sys.square*pk**2,term))
    assert np.isclose(T,Tcomm+Tstretch,atol=1e-8,rtol=1e-12)
    weights=pk**2*np.sum(abs(a)**2,axis=1)
    E=.5*float(np.sum(weights))
    G=float(np.dot(sys.square,weights))
    D=float(np.dot(sys.square**2,weights))
    rhs=-n-NU*sys.square[:,None]*a
    Eprime=float(np.real(np.vdot(aj,pk[:,None]*rhs)))
    halfGprime=float(np.real(np.einsum('i,ij,ij->',sys.square*pk**2,np.conj(a),rhs)))
    assert np.isclose(Eprime,S-NU*G,atol=1e-9)
    assert np.isclose(halfGprime,T-NU*D,atol=1e-9)
    return dict(j=j,E=E,G=G,D=D,S=S,S_commutator=S_comm,
                T=T,T_gradient_commutator=Tcomm,T_stretching=Tstretch,
                half_G_derivative=halfGprime,energy_derivative=Eprime)


def snapshot(sys,a,t):
    psi=multipliers(sys)
    rows=[shell(sys,a,psi,j) for j in range(len(psi))]
    total=dict(E=.5*float(np.sum(abs(a)**2)),
               G=float(np.dot(sys.square,np.sum(abs(a)**2,axis=1))),
               D=float(np.dot(sys.square**2,np.sum(abs(a)**2,axis=1))))
    for key in ('E','G','D'):
        assert abs(sum(s[key] for s in rows)-total[key])<1e-9
    n=sys.nonlinear(a)
    T=-float(np.real(np.einsum('i,ij,ij->',sys.square,np.conj(a),n)))
    assert abs(sum(s['T'] for s in rows)-T)<1e-9
    assert abs(sum(s['S'] for s in rows))<1e-9
    return dict(time=t,global_totals=dict(**total,T=T),rows=rows)


def main():
    runs=[]
    for N in (4,5):
        sys=System(N=N,nu=NU)
        a0=initial(sys,0.)
        _,af=integrate(sys,0.,DT)
        runs.append(dict(N=N,mode_count=len(sys.modes),start=snapshot(sys,a0,0.),
                         end=snapshot(sys,af,.02)))
    return dict(filter="h(t)=exp(-1/(1-t²)) for |t|<1; psi_j(k)=h(log2|k|-j)/sqrt(sum_l h(log2|k|-l)^2) on nonzero torus modes; sum_j psi_j²=1",
                energy_identity="S_j=-<P_j u,[P_j,u.grad]u> (negative sign)",
                enstrophy_identity="T_j=-<grad P_j u,[P_j,u.grad]grad u>-<grad P_j u,P_j((grad u).grad u)>; stretching remains",
                limitations="Finite-N numerical identity check; no uniform commutator estimate, positive-transfer bound, continuum convergence or regularity theorem.",
                runs=runs)


if __name__=='__main__':
    result=main()
    out=Path(__file__).with_name('smooth_commutator_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Wrote',out.name)
