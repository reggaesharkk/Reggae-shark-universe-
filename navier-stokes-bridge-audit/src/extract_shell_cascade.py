"""Exact-convolution donor/receiver/advector shell transfer on T^3.

T[n,m,l] = energy rate into recipient shell n from donor shell m,
mediated by advecting velocity in shell l. The donor assignment uses the
unsymmetrized convective term, for which pairwise antisymmetry is exact.
"""

import json
import math
import numpy as np

from evolve_galerkin import System
from validate_anisotropic_network import field

EDGES=(0.,1.,2.,3.,4.)
GRID=32


def shell_ids(system):
    radius=np.sqrt(system.square)
    shell=np.searchsorted(EDGES,radius,side='left')-1
    assert all((s==-1 and k==(0,0,0)) or 0<=s<4
               for s,k in zip(shell,system.modes))
    return shell


def terminal(system,shape):
    a=np.zeros((len(system.modes),3),complex)
    for k,v in field(2,shape,20260923).items():
        a[system.index[k]]=v
    for _ in range(40): a=system.rk4(a,.0025)
    return a


def transfer_tensor(system,a,shell):
    # In System's convolution arrays, left=advector, right=donor.
    out,adv,don=system.out,system.left,system.right
    derivative=np.einsum('ij,ij->i',system.qwaves,a[adv])
    donor_overlap=np.einsum('ij,ij->i',np.conj(a[out]),a[don])
    pieces=-np.real(1j*derivative*donor_overlap)
    valid=(shell[out]>=0)&(shell[don]>=0)&(shell[adv]>=0)
    T=np.zeros((4,4,4),float)
    np.add.at(T,(shell[out[valid]],shell[don[valid]],shell[adv[valid]]),
              pieces[valid])
    return T


def physical_shell_energy_rates(system,a,shell,grid=GRID):
    # 3D trigonometric polynomial. Triple-product coordinate frequencies
    # have magnitude at most 3N=12; grid=32 gives an exact periodic mean
    # of the cubic polynomial, up to floating-point roundoff.
    shape=(grid,grid,grid)
    ahat=np.zeros(shape+(3,),complex)
    dhat=np.zeros(shape+(3,3),complex)
    for idx,(k,v) in enumerate(zip(system.modes,a)):
        cell=tuple(x%grid for x in k)
        ahat[cell]=v
        for j in range(3): dhat[cell+(j,slice(None))]=1j*k[j]*v
    u=np.fft.ifftn(ahat,axes=(0,1,2))*grid**3
    grad=np.fft.ifftn(dhat,axes=(0,1,2))*grid**3
    conv=np.einsum('...j,...ji->...i',u,grad)
    rates=[]
    for s in range(4):
        shat=np.zeros_like(ahat)
        for idx in np.flatnonzero(shell==s):
            k=system.modes[idx]
            shat[tuple(x%grid for x in k)]=a[idx]
        us=np.fft.ifftn(shat,axes=(0,1,2))*grid**3
        rates.append(-float(np.real(np.sum(np.conj(us)*conv,axis=-1)).mean()))
    return np.array(rates)


def run():
    sys=System(N=4,nu=.1)
    shells=shell_ids(sys)
    results=[]
    for shape in ('line','cube'):
        a=terminal(sys,shape)
        T=transfer_tensor(sys,a,shells)
        rates=T.sum(axis=(1,2))
        n=sys.nonlinear(a)
        direct=np.array([-np.real(np.vdot(a[shells==s],n[shells==s]))
                         for s in range(4)])
        physical=physical_shell_energy_rates(sys,a,shells)
        antisym=float(np.max(abs(T+T.transpose(1,0,2))))
        energy_conservation=abs(float(rates.sum()))
        direct_error=float(np.max(abs(rates-direct)))
        physical_error=float(np.max(abs(rates-physical)))
        assert antisym<1e-10 and energy_conservation<1e-10
        assert direct_error<1e-10 and physical_error<1e-10
        results.append({'shape':shape,'time':.1,'shell_edges':EDGES,
                        'T_receiver_donor_advector':T.tolist(),
                        'receiver_donor_matrix':T.sum(axis=2).tolist(),
                        'net_shell_nonlinear_rates':rates.tolist(),
                        'physical_space_shell_rates':physical.tolist(),
                        'antisymmetry_error':antisym,
                        'conservation_error':energy_conservation,
                        'direct_budget_error':direct_error,
                        'physical_space_error':physical_error})
    return {'N':sys.N,'grid_for_independent_cubic_integral':GRID,
            'tensor_convention':'positive T[n,m,l] = energy into receiver n from donor m via advector l',
            'runs':results,
            'scope':'Exact finite Galerkin triads at t=.1; not a PDE cascade theorem.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
