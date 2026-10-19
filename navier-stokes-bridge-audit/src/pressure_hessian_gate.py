"""Pressure-Hessian contribution to stretching at finite Galerkin snapshots.

Compute the instantaneous full-pressure Poisson solution for the trigonometric
field u_N. The Galerkin trajectory does not satisfy the unprojected local
velocity-gradient evolution law: omitted nonlinear modes create a residual.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields

HERE = Path(__file__).resolve().parent


def snapshot(sys, a, grid=32):
    # Quadratic source frequencies fit without aliasing; all unmasked quartic
    # means below integrate exactly when grid > 4*N.
    assert grid > 4*sys.N
    grad, omega, _, imag = spatial_fields(sys, a, grid)
    assert imag < 1e-10
    S = (grad+np.swapaxes(grad,-1,-2))/2
    source = np.einsum('...ij,...ji->...',grad,grad)
    frequencies = np.rint(np.fft.fftfreq(grid)*grid).astype(int)
    m = np.stack(np.meshgrid(frequencies,frequencies,frequencies,indexing='ij'),axis=-1)
    m2 = np.sum(m*m,axis=-1)
    source_hat = np.fft.fftn(source)
    assert abs(source_hat[0,0,0])/grid**3 < 1e-10

    # Independent pressure-source check: div[(u·grad)u]=tr[(grad u)^2].
    coeff = np.zeros((grid,grid,grid,3),complex)
    coeff[tuple((sys.waves%grid).T)] = grid**3*a
    velocity = np.fft.ifftn(coeff,axes=(0,1,2))
    assert np.max(abs(velocity.imag)) < 1e-10
    convection = np.einsum('...j,...ij->...i',velocity.real,grad)
    conv_hat = np.fft.fftn(convection,axes=(0,1,2))
    independent_hat = 1j*np.einsum('...i,...i->...',m,conv_hat)
    source_residual = float(np.max(abs(independent_hat-source_hat))/grid**3)
    assert source_residual < 1e-9

    h_hat = np.zeros((grid,grid,grid,3,3),complex)
    nonzero = m2 > 0
    h_hat[nonzero] = -(source_hat[nonzero,None,None]*
                       m[nonzero,:,None]*m[nonzero,None,:]/m2[nonzero,None,None])
    h = np.fft.ifftn(h_hat,axes=(0,1,2))
    assert np.max(abs(h.imag)) < 1e-10
    h = h.real
    trace_residual = float(np.max(abs(np.trace(h,axis1=-2,axis2=-1)+source)))
    assert trace_residual < 1e-9
    global_strain_pressure = float(np.mean(np.einsum('...ij,...ij->...',S,h)))
    assert abs(global_strain_pressure) < 1e-9

    w2 = np.sum(omega*omega,axis=-1)
    W = np.einsum('...ij,...j->...i',S,omega)
    self_term = np.sum(W*W,axis=-1)
    pressure_term = -np.einsum('...i,...ij,...j->...',omega,h,omega)
    # h=(tr h)I/3+deviator; tr h=-source.
    isotropic = w2*source/3
    deviatoric = pressure_term-isotropic
    mask = w2 >= np.quantile(w2,.9)
    # Smooth, predeclared emphasis on larger |omega|², without hard boundaries.
    smooth_weight = w2/(w2+np.mean(w2))
    T = float(np.mean(np.sum(omega*W,axis=-1)))
    spectral_T = -float(np.real(np.einsum('i,ij,ij->',sys.square,a.conj(),sys.nonlinear(a))))
    assert abs(T-spectral_T) < 1e-8*max(1,abs(spectral_T))

    def means(x):
        return dict(global_mean=float(np.mean(x)),
                    high_region_integral=float(np.mean(np.where(mask,x,0))),
                    outside_integral=float(np.mean(np.where(~mask,x,0))),
                    high_region_conditional_mean=float(np.mean(x[mask])))

    return dict(grid=grid,G=float(np.mean(w2)),T=T,
                high_region_volume=float(np.mean(mask)),
                high_region_G_fraction=float(np.mean(np.where(mask,w2,0))/np.mean(w2)),
                self_amplification=means(self_term),
                pressure_response=means(pressure_term),
                isotropic_pressure_response=means(isotropic),
                deviatoric_pressure_response=means(deviatoric),
                combined_inviscid_response=means(self_term+pressure_term),
                smooth_vorticity_weight=dict(
                    spatial_mean=float(np.mean(smooth_weight)),
                    weighted_pressure_integral=float(np.mean(smooth_weight*pressure_term)),
                    weighted_self_integral=float(np.mean(smooth_weight*self_term)),
                    weighted_pressure_mean=float(np.sum(smooth_weight*pressure_term)/np.sum(smooth_weight))),
                diagnostics=dict(pressure_source_max_error=source_residual,
                                 pressure_Poisson_max_error=trace_residual,
                                 global_S_dot_H=global_strain_pressure,
                                 Fourier_minus_spatial_T=spectral_T-T))


def evolve(scenario,N):
    sys=System(N=N,nu=NU)
    a=make_initial(sys,*SCENARIOS[scenario])
    initial=snapshot(sys,a)
    for _ in range(40):
        a=sys.rk4(a,DT)
    final=snapshot(sys,a)
    fine=snapshot(sys,a,48)
    return dict(scenario=scenario,N=N,initial=initial,final=final,
                endpoint_grid48_minus_grid32_high_pressure_integral=(
                    fine['pressure_response']['high_region_integral']-
                    final['pressure_response']['high_region_integral']),
                endpoint_grid48_minus_grid32_global_pressure_integral=(
                    fine['pressure_response']['global_mean']-
                    final['pressure_response']['global_mean']),
                endpoint_grid48_minus_grid32_smooth_weighted_pressure=(
                    fine['smooth_vorticity_weight']['weighted_pressure_integral']-
                    final['smooth_vorticity_weight']['weighted_pressure_integral']))


def run():
    rows=[]
    for scenario in ('reference','combined_double_quarter_high'):
        for N in (4,7):
            row=evolve(scenario,N)
            rows.append(row)
            print(scenario,N,'endpoint high pressure',
                  row['final']['pressure_response']['high_region_integral'],
                  'high self',row['final']['self_amplification']['high_region_integral'],flush=True)
    return dict(formula='Delta p=-tr[(grad u)^2]; H_ij=partial_i partial_j p. For full smooth NS, (D/Dt)(S omega)=-H omega+viscous terms; Galerkin gradient evolution has an additional cutoff residual.',
                warning='Pressure-response and self-amplification are instantaneous quartic diagnostics, not the observed time derivative of T in the truncated ODE. Mask and conditional statistics use approximate quadrature. No cutoff-uniform or a priori estimate.',rows=rows)


if __name__=='__main__':
    result=run()
    target=HERE/'pressure_hessian_results.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Wrote',target)
