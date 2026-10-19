"""Exact local stretching budget of a finite Fourier-Galerkin trajectory.

R=(I-P_N) Leray[(u_N·grad)u_N] contains omitted solenoidal nonlinear
frequencies. Its global first-enstrophy-derivative pairing is zero, but its
local stretching-derivative pairing need not vanish.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields

HERE=Path(__file__).resolve().parent


def snapshot(sys,a,grid=32):
    assert grid>4*sys.N
    grad,omega,_,imag=spatial_fields(sys,a,grid)
    assert imag<1e-10
    S=(grad+np.swapaxes(grad,-1,-2))/2
    W=np.einsum('...ij,...j->...i',S,omega)
    frequencies=np.rint(np.fft.fftfreq(grid)*grid).astype(int)
    m=np.stack(np.meshgrid(frequencies,frequencies,frequencies,indexing='ij'),axis=-1)
    m2=np.sum(m*m,axis=-1)
    nz=m2>0

    coefficients=np.zeros((grid,grid,grid,3),complex)
    index=tuple((sys.waves%grid).T)
    coefficients[index]=grid**3*a
    velocity=np.fft.ifftn(coefficients,axes=(0,1,2))
    assert np.max(abs(velocity.imag))<1e-10
    conv=np.einsum('...j,...ij->...i',velocity.real,grad)
    conv_hat=np.fft.fftn(conv,axes=(0,1,2))
    source=np.einsum('...ij,...ji->...',grad,grad)
    source_hat=np.fft.fftn(source)
    source_error=float(np.max(abs(source_hat-1j*np.einsum('...i,...i->...',m,conv_hat)))/grid**3)
    assert source_error<1e-9
    h_hat=np.zeros((grid,grid,grid,3,3),complex)
    h_hat[nz]=-(source_hat[nz,None,None]*
                m[nz,:,None]*m[nz,None,:]/m2[nz,None,None])
    H=np.fft.ifftn(h_hat,axes=(0,1,2)).real

    leray_hat=np.zeros_like(conv_hat)
    leray_hat[nz]=conv_hat[nz]-m[nz]*(
        np.einsum('...i,...i->...',m,conv_hat)[nz]/m2[nz])[:,None]
    retained=leray_hat[index]/grid**3
    nonlinear=sys.nonlinear(a)
    low_error=float(np.max(abs(retained-nonlinear)))
    assert low_error<1e-9
    residual_hat=leray_hat.copy()
    residual_hat[m2<=sys.N**2]=0
    curl_hat=1j*np.cross(m,residual_hat)
    curlR=np.fft.ifftn(curl_hat,axes=(0,1,2)).real
    rgrad_hat=1j*residual_hat[..., :,None]*m[...,None,:]
    rgrad=np.fft.ifftn(rgrad_hat,axes=(0,1,2)).real
    symR=(rgrad+np.swapaxes(rgrad,-1,-2))/2

    omega_hat=np.fft.fftn(omega,axes=(0,1,2))
    S_hat=np.fft.fftn(S,axes=(0,1,2))
    lap_omega=np.fft.ifftn(-m2[...,None]*omega_hat,axes=(0,1,2)).real
    lap_S=np.fft.ifftn(-m2[...,None,None]*S_hat,axes=(0,1,2)).real
    self_term=np.sum(W*W,axis=-1)
    pressure=-np.einsum('...i,...ij,...j->...',omega,H,omega)
    viscous=NU*(2*np.sum(W*lap_omega,axis=-1)+
                 np.einsum('...i,...ij,...j->...',omega,lap_S,omega))
    projection=2*np.sum(W*curlR,axis=-1)+np.einsum(
        '...i,...ij,...j->...',omega,symR,omega)

    adot=sys.rhs(a)
    grad_dot,omega_dot,_,imag_dot=spatial_fields(sys,adot,grid)
    assert imag_dot<1e-10
    S_dot=(grad_dot+np.swapaxes(grad_dot,-1,-2))/2
    exact_T_dot=float(np.mean(2*np.sum(omega_dot*W,axis=-1)+
                      np.einsum('...i,...ij,...j->...',omega,S_dot,omega)))
    parts=dict(self_amplification=float(np.mean(self_term)),
               pressure_response=float(np.mean(pressure)),
               viscous_response=float(np.mean(viscous)),
               projection_response=float(np.mean(projection)))
    reconstructed=sum(parts.values())
    error=exact_T_dot-reconstructed
    assert abs(error)<1e-7*max(1,abs(exact_T_dot),*(abs(v) for v in parts.values()))

    G=float(np.mean(np.sum(omega*omega,axis=-1)))
    T=float(np.mean(np.sum(omega*W,axis=-1)))
    D=float(np.sum(sys.square[:,None]**2*abs(a)**2))
    residual_G=float(np.mean(np.sum(omega*curlR,axis=-1)))
    assert abs(residual_G)<1e-8*max(1,G)
    projected_curl_norm=float(np.sqrt(np.mean(np.sum(curlR*curlR,axis=-1))))
    viscous_curl_norm=float(NU*np.sqrt(np.mean(np.sum(lap_omega*lap_omega,axis=-1))))
    return dict(G=G,D=D,T=T,exact_T_time_derivative=exact_T_dot,
                terms=parts,budget_error=error,
                residual_enstrophy_pairing=residual_G,
                residual_curl_norm=projected_curl_norm,
                viscous_curl_norm=viscous_curl_norm,
                residual_to_viscous_curl_norm=(
                    projected_curl_norm/viscous_curl_norm if viscous_curl_norm else None),
                checks=dict(pressure_source_error=source_error,
                            retained_nonlinearity_error=low_error))


def stored_cases():
    result=[]
    for filename in ('candidate_inequality_results.json','candidate_inequality_N7_results.json'):
        data=json.loads((HERE/filename).read_text(encoding='utf-8'))
        for row in data['runs']:
            result.append((row['scenario'],row['N'],row['samples'][0],row['samples'][-1]))
    assert len(result)==24
    return result


def run():
    rows=[]
    for scenario,N,first,last in stored_cases():
        sys=System(N=N,nu=NU)
        a=make_initial(sys,*SCENARIOS[scenario])
        beginning=snapshot(sys,a)
        for _ in range(40):
            a=sys.rk4(a,DT)
        ending=snapshot(sys,a)
        for measured,stored in ((beginning,first),(ending,last)):
            for key,index in (('G',2),('D',3),('T',4)):
                assert abs(measured[key]-stored[index])<2e-7*max(1,abs(measured[key]))
        rows.append(dict(scenario=scenario,N=N,initial=beginning,final=ending))
        print(scenario,N,'endpoint projection dT/dt',
              round(ending['terms']['projection_response'],4),
              'versus viscous',round(ending['terms']['viscous_response'],4),flush=True)
    # Independent temporal check: central finite difference of the spectral
    # cubic transfer, rather than reusing the spatial budget terms.
    sys=System(N=4,nu=NU)
    state=make_initial(sys,*SCENARIOS['reference'])
    h=1e-5
    def spectral_transfer(x):
        return -float(np.real(np.einsum(
            'i,ij,ij->',sys.square,x.conj(),sys.nonlinear(x))))
    finite_difference=(spectral_transfer(sys.rk4(state,h))-
                       spectral_transfer(sys.rk4(state,-h)))/(2*h)
    exact=next(r['initial']['exact_T_time_derivative'] for r in rows
               if r['scenario']=='reference' and r['N']==4)
    assert abs(finite_difference-exact)<1e-6*max(1,abs(exact))
    return dict(identity='d/dt <omega·S omega> = <|S omega|² - omega·H omega> + nu<2(S omega)·Delta omega + omega·(Delta S)omega> + <2(S omega)·curl R + omega·sym(grad R)omega>, R=(I-P_N)Leray[(u·grad)u].',
                scope='24 previously recorded scenario-cutoff runs, t=0 and t=.02; 32³ exact unmasked quartic spatial quadrature, finite RK4 state evolution.',
                warning='R is orthogonal to omega in first enstrophy derivative, but not generally in stretching derivative. Finite time/endpoints and cutoffs do not give an a priori bound.',
                independent_time_derivative_check=dict(
                    scenario='reference',N=4,time=0,finite_difference_step=h,
                    spectral_central_difference=finite_difference,
                    analytic_Galerkin_derivative=exact),
                rows=rows)


if __name__=='__main__':
    result=run()
    target=HERE/'projection_residual_results.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Wrote',target)
