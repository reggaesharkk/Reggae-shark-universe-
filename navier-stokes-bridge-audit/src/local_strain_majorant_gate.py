"""Frame-invariant local strain envelope for exact and evolved fields.

M=<lambda_max(S)_+ |omega|^2> is an exact pointwise majorant for T,
but its time-integrated coefficient M/G is not known a priori.
"""

import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from helicity_phase_gate import field as triad_field
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields


def measure(sys, a, grid=32):
    grad,omega,_,imag=spatial_fields(sys,a,grid)
    S=(grad+np.swapaxes(grad,-1,-2))/2
    w2=np.sum(omega**2,axis=-1)
    local=np.einsum('...i,...ij,...j->...',omega,S,omega)
    top=np.linalg.eigvalsh(S)[...,-1]
    M=float(np.mean(np.maximum(top,0.)*w2))
    T=float(np.mean(local))
    P=float(np.mean(np.maximum(local,0.)))
    G=float(np.mean(w2))
    n=sys.nonlinear(a)
    spectral=-float(np.real(np.einsum('i,ij,ij->',sys.square,a.conj(),n)))
    assert abs(T-spectral)<1e-8*max(1,abs(spectral))
    assert abs(G-float(np.sum(sys.square[:,None]*abs(a)**2)))<1e-8*max(1,G)
    assert M+1e-8>=P>=max(T,0)-1e-8
    assert imag<1e-10
    return dict(grid=grid,G=G,T=T,positive_local_stretching=P,
                max_eigenvalue_envelope=M,
                weighted_max_strain=M/G,
                positive_local_to_envelope=P/M if M else None,
                signed_to_envelope=T/M if M else None,
                Fourier_minus_spatial_T=spectral-T)


def phase_family():
    sys=System(N=2,nu=NU)
    rows=[]
    for amplitude in (1.,2.):
        for theta in (0.,math.pi/2,math.pi,3*math.pi/2):
            u=triad_field(amplitude,theta)
            a=np.zeros((len(sys.modes),3),complex)
            for k,v in u.items(): a[sys.index[k]]=v
            rows.append(dict(amplitude=amplitude,phase_radians=theta,
                             **measure(sys,a,grid=32)))
    return rows


def simpson(values,dt):
    return dt/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+
                 2*sum(values[2:-1:2]))


def dynamic(scenario,N):
    sys=System(N=N,nu=NU)
    a=make_initial(sys,*SCENARIOS[scenario])
    snaps=[]
    for step in range(41):
        if step%10==0:
            snaps.append(dict(time=step*DT,**measure(sys,a,grid=32)))
        if step<40: a=sys.rk4(a,DT)
    fine=measure(sys,a,grid=48)
    weights=[x['weighted_max_strain'] for x in snaps]
    integral_five=simpson(weights,.005)
    integral_three=simpson(weights[::2],.01)
    return dict(scenario=scenario,N=N,mode_count=len(sys.modes),
                snapshots=snaps,
                coarse_simpson_integral_weighted_max_strain=integral_five,
                three_point_simpson_integral_weighted_max_strain=integral_three,
                five_minus_three_sampling_difference=integral_five-integral_three,
                endpoint_grid48_minus_grid32_envelope=fine['max_eigenvalue_envelope']-snaps[-1]['max_eigenvalue_envelope'],
                endpoint_grid48_minus_grid32_weighted_max_strain=fine['weighted_max_strain']-snaps[-1]['weighted_max_strain'])


def run():
    triads=phase_family()
    trajectories=[]
    for scenario in ('reference','combined_double_quarter_high'):
        for N in (4,5,6,7):
            item=dynamic(scenario,N)
            trajectories.append(item)
            last=item['snapshots'][-1]
            print(scenario,N,'T',round(last['T'],5),
                  'M',round(last['max_eigenvalue_envelope'],5),
                  'integral M/G',round(item['coarse_simpson_integral_weighted_max_strain'],6),flush=True)
    return dict(majorant='T=<omega.S.omega> <= <lambda_max(S)_+ |omega|^2>=M; a=M/G',
                proof='Rayleigh quotient omega.S.omega<=lambda_max(S)|omega|^2 pointwise, followed by the positive part and averaging.',
                limitation='M depends on the full solution. No independently controlled cutoff-uniform time integral of M/G is proved. Nonpolynomial eigenvalue quadrature is approximate even where cubic transfer integrates exactly.',
                phase_family=triads,dynamic_trajectories=trajectories)


if __name__=='__main__':
    result=run()
    target=Path(__file__).with_name('local_strain_majorant_results.json')
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Wrote',target)
