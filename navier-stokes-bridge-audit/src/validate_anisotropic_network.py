"""Fourier-support anisotropy audit of the proven H^2 flux inequality."""

import json
import math
import numpy as np

from galerkin import (energy, flux, gradient_norm, leray,
                      nonlinear_on_support, sobolev_norm)
from validate_network_hs import C2


def allowed(i, j, k, L, shape):
    if shape == 'line':
        return abs(i) <= L and abs(j) <= 1 and abs(k) <= 1
    if shape == 'slab':
        return abs(i) <= L and abs(j) <= L and abs(k) <= 1
    if shape == 'cube':
        return max(abs(i), abs(j), abs(k)) <= L
    raise ValueError(shape)


def field(L, shape, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for i in range(-L, L+1):
        for j in range(-L, L+1):
            for k in range(-L, L+1):
                p = (i, j, k)
                minus = (-i, -j, -k)
                if p == (0, 0, 0) or p < minus or not allowed(i,j,k,L,shape):
                    continue
                z = rng.normal(size=3) + 1j*rng.normal(size=3)
                a = (leray(p) @ z)/(1+i*i+j*j+k*k)**0.9
                out[p], out[minus] = a, np.conjugate(a)
    cutoff = math.sqrt(3)*L + 1e-9
    scale = 1/math.sqrt(energy(out, cutoff))
    return {k: scale*a for k,a in out.items()}


def finite_gradient_embedding(s,N):
    # Fourier Cauchy-Schwarz constant for ||grad u||_infinity <= C ||u||_Hs.
    return math.sqrt(sum((i*i+j*j+k*k)/(1+i*i+j*j+k*k)**s
                         for i in range(-N,N+1) for j in range(-N,N+1)
                         for k in range(-N,N+1)
                         if i*i+j*j+k*k <= N*N))


def run():
    rows=[]
    for L in (2,3,4):
        for shape in ('line','slab','cube'):
            for seed in (20260923,20260924):
                u=field(L,shape,seed)
                n=nonlinear_on_support(u)
                cutoff=math.sqrt(3)*L+1e-9
                K=float(L)
                actual=abs(flux(u,n,K))
                core=math.sqrt(2*energy(u,K))*sobolev_norm(u,2)*gradient_norm(u)
                universal_bound=C2*core
                support_c=math.sqrt(sum((1+sum(x*x for x in p))**(-2)
                                        for p in u))
                support_bound=support_c*core
                total=abs(flux(u,n,cutoff))
                assert actual<=support_bound*(1+1e-11)
                assert support_bound<=universal_bound*(1+1e-11)
                assert total<1e-9
                rows.append({'L':L,'shape':shape,'seed':seed,'modes':len(u),
                             'absolute_low_flux':actual,
                             'global_bound':universal_bound,
                             'ratio_global':actual/universal_bound,
                             'support_bound_instantaneous_only':support_bound,
                             'ratio_support':actual/support_bound,
                             'full_flux_error':total})
    return {'global_C2':C2,'rows':rows,
            'finite_gradient_embedding_constants':{
                str(s):{str(N):finite_gradient_embedding(s,N)
                        for N in (2,4,8,16)} for s in (2,2.5,3)},
            'scope':'Fourier-support geometry at one instant; no physical-space filament or all-time estimate.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
