"""Decompose Galerkin stretching-rate residual by omitted unit-width shells.

Shell contributions are linear in R and exactly add to the full residual.
The snapshot times are descriptive, not monotonicity or continuum tests.
"""

import json
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import DT, NU
from strain_alignment_trajectory import spatial_fields

HERE=Path(__file__).resolve().parent
TRACK={('reference',4),('reference',7),
       ('combined_double_quarter_high',4),('combined_double_quarter_high',7)}


def snapshot(sys,a,grid=32):
    assert grid>4*sys.N
    grad,omega,_,imag=spatial_fields(sys,a,grid)
    assert imag<1e-10
    S=(grad+np.swapaxes(grad,-1,-2))/2
    W=np.einsum('...ij,...j->...i',S,omega)
    freqs=np.rint(np.fft.fftfreq(grid)*grid).astype(int)
    m=np.stack(np.meshgrid(freqs,freqs,freqs,indexing='ij'),axis=-1)
    m2=np.sum(m*m,axis=-1)
    coeff=np.zeros((grid,grid,grid,3),complex)
    coeff[tuple((sys.waves%grid).T)]=grid**3*a
    velocity=np.fft.ifftn(coeff,axes=(0,1,2))
    assert np.max(abs(velocity.imag))<1e-10
    conv=np.einsum('...j,...ij->...i',velocity.real,grad)
    conv_hat=np.fft.fftn(conv,axes=(0,1,2))
    leray=np.zeros_like(conv_hat)
    nz=m2>0
    leray[nz]=conv_hat[nz]-m[nz]*(
        np.einsum('...i,...i->...',m,conv_hat)[nz]/m2[nz])[:,None]
    Rhat=leray.copy()
    Rhat[m2<=sys.N**2]=0
    assert np.max(abs(Rhat[m2>(2*sys.N)**2]))/grid**3<1e-9
    parts=[]
    for j in range(1,sys.N+1):
        shell=(m2>(sys.N+j-1)**2)&(m2<=(sys.N+j)**2)
        selected=np.zeros_like(Rhat)
        selected[shell]=Rhat[shell]
        curl=np.fft.ifftn(1j*np.cross(m,selected),axes=(0,1,2))
        dR=np.fft.ifftn(1j*selected[..., :,None]*m[...,None,:],axes=(0,1,2))
        assert np.max(abs(curl.imag))<1e-9
        sym=(dR.real+np.swapaxes(dR.real,-1,-2))/2
        curl_part=float(np.mean(2*np.sum(W*curl.real,axis=-1)))
        strain_part=float(np.mean(np.einsum('...i,...ij,...j->...',omega,sym,omega)))
        norm=float(np.sqrt(np.sum(abs(selected)**2)/grid**6))
        parts.append(dict(radial_shell=(sys.N+j-1,sys.N+j),
                          frequency_count=int(np.count_nonzero(shell & (np.sum(abs(selected)**2,axis=-1)>1e-20))),
                          R_l2=norm,curl_coupling=curl_part,
                          strain_coupling=strain_part,total=curl_part+strain_part))
    # Independent full R assembly and orthogonality checks.
    fullcurl=np.fft.ifftn(1j*np.cross(m,Rhat),axes=(0,1,2))
    fullgrad=np.fft.ifftn(1j*Rhat[..., :,None]*m[...,None,:],axes=(0,1,2))
    fullsym=(fullgrad.real+np.swapaxes(fullgrad.real,-1,-2))/2
    total=float(np.mean(2*np.sum(W*fullcurl.real,axis=-1)+
          np.einsum('...i,...ij,...j->...',omega,fullsym,omega)))
    assert abs(total-sum(x['total'] for x in parts))<1e-8*max(1,abs(total))
    first_enstrophy_pair=float(np.mean(np.sum(omega*fullcurl.real,axis=-1)))
    assert abs(first_enstrophy_pair)<1e-8
    return dict(projection_response=total,shells=parts,
                positive_shell_sum=sum(max(0,x['total']) for x in parts),
                negative_shell_sum=sum(min(0,x['total']) for x in parts),
                first_enstrophy_pair=first_enstrophy_pair)


def cases():
    prior=json.loads((HERE/'projection_residual_results.json').read_text(encoding='utf-8'))
    return prior['rows']


def run():
    rows=[]
    for previous in cases():
        scenario,N=previous['scenario'],previous['N']
        sys=System(N=N,nu=NU)
        a=make_initial(sys,*SCENARIOS[scenario])
        samples=[]
        for step in range(41):
            if step in (0,40) or ((scenario,N) in TRACK and step%10==0):
                result=snapshot(sys,a)
                result['time']=step*DT
                recorded=previous['initial' if step==0 else 'final'] if step in (0,40) else None
                if recorded:
                    target=recorded['terms']['projection_response']
                    assert abs(result['projection_response']-target)<1e-8*max(1,abs(target))
                samples.append(result)
            if step<40:
                a=sys.rk4(a,DT)
        rows.append(dict(scenario=scenario,N=N,samples=samples))
        final=samples[-1]
        print(scenario,N,'endpoint',round(final['projection_response'],3),
              'positive bands',round(final['positive_shell_sum'],3),flush=True)
    return dict(shells='Unit radial intervals (N+j-1,N+j], j=1,...,N; R=(I-P_N)Leray[(u·grad)u].',
                tracked_intermediate_cases=[list(x) for x in sorted(TRACK)],
                warning='Only initial/end snapshots for all 24 cases and five times for four selected cases; a positive shell can coexist with negative total. No spectral or time monotonicity is inferred.',
                rows=rows)


if __name__=='__main__':
    result=run()
    target=HERE/'projection_shell_results.json'
    target.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
    print('Wrote',target)
