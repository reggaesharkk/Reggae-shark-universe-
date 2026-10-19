"""Localized energy equality for a finite Fourier-Galerkin trajectory.

Includes the pressure and the exact Galerkin projection residual. Spatial
FFT grids are used only for dealiased polynomial evaluation and quadrature.
"""

import json
import numpy as np

from evolve_galerkin import System
from validate_anisotropic_network import field


def terminal(sys,shape):
    a=np.zeros((len(sys.modes),3),complex)
    for k,v in field(2,shape,20260923).items():
        a[sys.index[k]]=v
    for _ in range(40): a=sys.rk4(a,.0025)
    return a


def grid_fields(sys,a,M):
    ahat=np.zeros((M,M,M,3),complex)
    dhat=np.zeros((M,M,M,3,3),complex)
    that=np.zeros_like(ahat)
    at=sys.rhs(a)
    for k,v,dv in zip(sys.modes,a,at):
        cell=tuple(x%M for x in k)
        ahat[cell]=v;that[cell]=dv
        for j in range(3):dhat[cell+(j,slice(None))]=1j*k[j]*v
    u=(np.fft.ifftn(ahat,axes=(0,1,2))*M**3).real
    grad=(np.fft.ifftn(dhat,axes=(0,1,2))*M**3).real
    ut=(np.fft.ifftn(that,axes=(0,1,2))*M**3).real
    conv=np.einsum('...j,...ji->...i',u,grad)
    chat=np.fft.fftn(conv,axes=(0,1,2))/M**3
    freq=np.rint(np.fft.fftfreq(M)*M).astype(int)
    kx,ky,kz=np.meshgrid(freq,freq,freq,indexing='ij')
    kvec=np.stack((kx,ky,kz),axis=-1)
    sq=np.sum(kvec*kvec,axis=-1)
    dot=np.sum(kvec*chat,axis=-1)
    div_over_sq=np.divide(dot,sq,out=np.zeros_like(dot),where=sq!=0)
    p_hat=1j*div_over_sq
    pc_hat=chat-kvec*div_over_sq[...,None]
    # The nonlinear polynomial has frequencies |coordinate|<=8.
    # Remove FFT roundoff outside the exact convolution support.
    rhat=np.where(((sq>sys.N**2)&(sq<=(2*sys.N)**2))[...,None],
                  pc_hat,0)
    p=(np.fft.ifftn(p_hat,axes=(0,1,2))*M**3).real
    residual=(np.fft.ifftn(rhat,axes=(0,1,2))*M**3).real
    e=.5*np.sum(u*u,axis=-1)
    gradsq=np.sum(grad*grad,axis=(-2,-1))
    return u,ut,p,residual,e,gradsq


def window(M,kappa):
    x=2*np.pi*np.arange(M)/M
    c=[np.cos(x).reshape(tuple(M if j==d else 1 for j in range(3)))
       for d in range(3)]
    s=[np.sin(x).reshape(tuple(M if j==d else 1 for j in range(3)))
       for d in range(3)]
    phi=np.exp(kappa*(c[0]+c[1]+c[2]-3))
    dphi=np.stack(np.broadcast_arrays(*[-kappa*phi*sd for sd in s]),axis=-1)
    lap=phi*sum(-kappa*cd+kappa*kappa*sd*sd for cd,sd in zip(c,s))
    return phi,dphi,lap


def evaluate(fields,M,kappa,nu):
    u,ut,p,R,e,gradsq=fields
    phi,dphi,lap=window(M,kappa)
    lhs=float(np.mean(phi*np.sum(u*ut,axis=-1)))
    adv=float(np.mean((e+p)*np.sum(u*dphi,axis=-1)))
    diffusion=float(nu*np.mean(e*lap))
    dissipation=float(-nu*np.mean(phi*gradsq))
    projection=float(np.mean(phi*np.sum(u*R,axis=-1)))
    rhs=adv+diffusion+dissipation+projection
    return {'kappa':kappa,'window_mean':float(np.mean(phi)),
            'lhs_local_energy_derivative':lhs,
            'advective_plus_pressure_boundary':adv,
            'diffusion_window_term':diffusion,
            'viscous_dissipation':dissipation,
            'projection_residual':projection,
            'rhs':rhs,'closure_error':abs(lhs-rhs),
            'error_if_projection_omitted':abs(lhs-(rhs-projection))}


def run():
    sys=System(N=4,nu=.1)
    results=[]
    for shape in ('line','cube'):
        a=terminal(sys,shape)
        grids={M:grid_fields(sys,a,M) for M in (64,96)}
        rows=[]
        for kappa in (0,1,4,9,16):
            x=evaluate(grids[64],64,kappa,sys.nu)
            y=evaluate(grids[96],96,kappa,sys.nu)
            x['grid64_vs_grid96_lhs_diff']=abs(x['lhs_local_energy_derivative']-
                                             y['lhs_local_energy_derivative'])
            x['grid64_vs_grid96_projection_diff']=abs(x['projection_residual']-
                                                      y['projection_residual'])
            assert x['closure_error']<1e-9
            assert y['closure_error']<1e-9
            rows.append(x)
        results.append({'shape':shape,'time':.1,'rows':rows})
    return {'N':4,'nu':.1,'window':'exp(kappa*(cos x+cos y+cos z-3))',
            'identity':'d/dt<phi e> = <(e+p)u.grad phi> + nu<e lap phi> - nu<phi |grad u|^2> + <phi u.R_N>',
            'results':results,
            'scope':'Finite Galerkin local equality with residual, not a local energy inequality for the infinite PDE.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
