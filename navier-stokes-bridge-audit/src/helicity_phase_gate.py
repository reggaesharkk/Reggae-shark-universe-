"""An exact zero-modal-helicity triad with phase-dependent H1 transfer.

This is an instantaneous obstruction to using total or per-mode signed
helicity as a universal predictor of signed enstrophy production.
"""

import json
import math
from pathlib import Path

import numpy as np

from galerkin import nonlinear_on_support
from validate_enstrophy import h1_nonlinear_growth, physical_space_growth
from validate_sparse_triad import P, Q, R


POLARIZATIONS={P:np.array([0.,-1.,-1.]),
               Q:np.array([-1.,-1.,1.]),
               R:np.array([-1.,0.,1.])}


def field(amplitude,phase):
    data={k:complex(amplitude)*v.astype(complex)*
          (np.exp(1j*phase) if k==R else 1.)
          for k,v in POLARIZATIONS.items()}
    data.update({tuple(-x for x in k):a.conj() for k,a in list(data.items())})
    return data


def metrics(data):
    powers={str(k):float(np.vdot(a,a).real) for k,a in data.items()}
    mode_helicities={str(k):float(np.real(np.vdot(a,1j*np.cross(k,a))))
                     for k,a in data.items()}
    E=.5*sum(powers.values())
    G=sum(sum(x*x for x in k)*float(np.vdot(a,a).real)
          for k,a in data.items())
    D=sum(sum(x*x for x in k)**2*float(np.vdot(a,a).real)
          for k,a in data.items())
    T=h1_nonlinear_growth(data,nonlinear_on_support(data))
    return dict(E=E,G=G,D=D,T=T,total_helicity=sum(mode_helicities.values()),
                mode_helicities=mode_helicities,powers=powers,
                divergence_error=max(abs(np.dot(k,a)) for k,a in data.items()),
                reality_error=max(np.linalg.norm(data[tuple(-x for x in k)]-a.conj())
                                  for k,a in data.items()))


def run():
    rows=[]
    for A in (1.,2.):
        for theta in (0.,math.pi/2,math.pi,3*math.pi/2):
            data=field(A,theta)
            row=dict(amplitude=A,phase_radians=theta,**metrics(data))
            row['physical_minus_spectral_transfer']=physical_space_growth(data)-row['T']
            assert abs(row['T']-4*A**3*math.sin(theta))<1e-12
            assert abs(row['total_helicity'])<1e-12
            assert max(abs(x) for x in row['mode_helicities'].values())<1e-12
            assert row['divergence_error']<1e-12 and row['reality_error']<1e-12
            assert abs(row['physical_minus_spectral_transfer'])<1e-12
            assert abs(row['E']-7*A*A)<1e-12
            assert abs(row['G']-28*A*A)<1e-12
            assert abs(row['D']-64*A*A)<1e-12
            rows.append(row)
    # At A=2 and nu=.1, the positive-phase choice has positive net H1 growth.
    assert abs(rows[5]['T']-.1*rows[5]['D']-6.4)<1e-12
    return dict(triad=[P,Q,R],polarizations={str(k):v.tolist() for k,v in POLARIZATIONS.items()},
                exact_formula='T(A,theta)=4 A^3 sin(theta), E=7 A^2, G=28 A^2, D=64 A^2; H(k)=H_total=0 for every phase',
                limitation='Instantaneous example only. Zero signed helicity does not imply dynamical decimation or phase locking, and does not rule out majorants using local or sign-definite helical information.',
                rows=rows)


if __name__=='__main__':
    output=Path(__file__).with_name('helicity_phase_results.json')
    output.write_text(json.dumps(run(),indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {output.name}')
