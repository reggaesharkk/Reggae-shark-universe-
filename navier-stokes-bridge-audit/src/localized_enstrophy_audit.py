"""Localized vorticity/enstrophy identity for the finite Galerkin system."""

import json
import numpy as np

from evolve_galerkin import System
from localized_energy_audit import terminal, grid_fields, window


def fields(sys,a,M):
    u,ut,_,R,_,_=grid_fields(sys,a,M)
    axes=(0,1,2)
    wave=np.rint(np.fft.fftfreq(M)*M).astype(int)
    k=np.stack(np.meshgrid(wave,wave,wave,indexing='ij'),axis=-1)
    def curl(v):
        vh=np.fft.fftn(v,axes=axes)/M**3
        return 1j*np.cross(k,vh)
    w_hat=curl(u)
    wt_hat=curl(ut)
    cr_hat=curl(R)
    uh=np.fft.fftn(u,axes=axes)/M**3
    guhat=1j*k[..., :, None]*uh[..., None, :]
    gwhat=1j*k[..., :, None]*w_hat[..., None, :]
    def real_ifft(a):return (np.fft.ifftn(a,axes=axes)*M**3).real
    w=real_ifft(w_hat)
    wt=real_ifft(wt_hat)
    cr=real_ifft(cr_hat)
    gu=real_ifft(guhat)
    gw=real_ifft(gwhat)
    S=(gu+np.swapaxes(gu,-1,-2))/2
    enstrophy=.5*np.sum(w*w,axis=-1)
    stretch=np.einsum('...i,...ij,...j->...',w,S,w)
    gradw_sq=np.sum(gw*gw,axis=(-1,-2))
    res=np.sum(w*cr,axis=-1)
    return u,w,wt,S,enstrophy,stretch,gradw_sq,res


def evaluate(f,M,kappa,nu):
    u,w,wt,S,enstrophy,stretch,gradw_sq,res=f
    phi,dphi,lap=window(M,kappa)
    lhs=float(np.mean(phi*np.sum(w*wt,axis=-1)))
    stretching=float(np.mean(phi*stretch))
    transport=float(np.mean(enstrophy*np.sum(u*dphi,axis=-1)))
    diffusion=float(nu*np.mean(enstrophy*lap))
    dissipation=float(-nu*np.mean(phi*gradw_sq))
    residual=float(np.mean(phi*res))
    rhs=stretching+transport+diffusion+dissipation+residual
    weight=phi*enstrophy
    fraction_positive=float(np.sum(weight*(stretch>0))/np.sum(weight))
    return {'kappa':kappa,'window_mean':float(phi.mean()),
            'localized_enstrophy':float(np.mean(phi*enstrophy)),
            'lhs_enstrophy_derivative':lhs,
            'vortex_stretching':stretching,
            'transport_window_term':transport,
            'diffusion_window_term':diffusion,
            'viscous_vorticity_dissipation':dissipation,
            'curl_projection_residual':residual,
            'rhs':rhs,'closure_error':abs(lhs-rhs),
            'error_if_residual_omitted':abs(lhs-(rhs-residual)),
            'enstrophy_weighted_fraction_positive_stretch':fraction_positive}


def eigendirection_diagnostic(f,M,kappa):
    # Subsample to 16^3 points. This describes one field at one time;
    # it is not a geometric regularity criterion.
    _,w,_,S,_,_,_,_=f
    stride=M//16
    w=w[::stride,::stride,::stride]
    S=S[::stride,::stride,::stride]
    eigval,eigvec=np.linalg.eigh(S)
    direction=eigvec[..., :, -1]
    strength=np.sum(w*w,axis=-1)
    cos2=np.divide(np.sum(w*direction,axis=-1)**2,strength,
                   out=np.zeros_like(strength),where=strength>1e-20)
    ph=window(16,kappa)[0]
    return {'kappa':kappa,
            'weighted_cos2_vorticity_vs_max_strain_eigenvector':
                float(np.sum(ph*strength*cos2)/np.sum(ph*strength)),
            'weighted_max_strain_eigenvalue':
                float(np.sum(ph*strength*eigval[...,-1])/np.sum(ph*strength)),
            'sample_grid':'16^3 subsample of 64^3'}


def run():
    sys=System(N=4,nu=.1)
    results=[]
    for shape in ('line','cube'):
        a=terminal(sys,shape)
        f64=fields(sys,a,64)
        rows=[]
        for kappa in (0,1,4,9,16):
            x=evaluate(f64,64,kappa,sys.nu)
            rows.append(x)
            assert x['closure_error']<1e-8
        alignment=[eigendirection_diagnostic(f64,64,k) for k in (0,9)]
        del f64
        f96=fields(sys,a,96)
        for x in rows:
            y=evaluate(f96,96,x['kappa'],sys.nu)
            x['grid64_vs_grid96_lhs_diff']=abs(x['lhs_enstrophy_derivative']-
                                              y['lhs_enstrophy_derivative'])
            assert y['closure_error']<1e-8
        del f96
        results.append({'shape':shape,'time':.1,'rows':rows,
                        'alignment_diagnostic':alignment})
    return {'N':4,'nu':.1,
            'identity':'d<phi |omega|^2/2>/dt = <phi omega.S.omega> + <(|omega|^2/2)u.grad phi> + nu<(|omega|^2/2)lap phi> - nu<phi |grad omega|^2> + <phi omega.curl R_N>',
            'results':results,
            'scope':'Finite Galerkin localized vorticity balance; alignment samples do not test a regularity theorem.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
