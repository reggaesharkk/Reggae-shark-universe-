"""Short-time exact-convolution Fourier Galerkin evolution on T^3.

RK4 integrates the finite-dimensional ODE. Every convolution pair is kept;
there is no FFT aliasing. Time stepping is not a PDE regularity proof.
"""

import json
import math
import numpy as np

from galerkin import modes_in_ball, leray
from validate_anisotropic_network import field
from validate_network_hs import C2


class System:
    def __init__(self, N=4, nu=.1):
        self.N, self.nu = N, nu
        self.modes = modes_in_ball(N)
        self.index = {k:i for i,k in enumerate(self.modes)}
        self.waves = np.array(self.modes)
        self.square = np.sum(self.waves*self.waves,axis=1)
        self.projectors = np.array([leray(k) for k in self.modes])
        self.neg = np.array([self.index[tuple(-x for x in k)]
                             for k in self.modes])
        out, left, right = [], [], []
        for pi,p in enumerate(self.modes):
            for qi,q in enumerate(self.modes):
                k=tuple(p[d]+q[d] for d in range(3))
                ki=self.index.get(k)
                if ki is not None:
                    out.append(ki);left.append(pi);right.append(qi)
        self.out=np.array(out,dtype=np.int32)
        self.left=np.array(left,dtype=np.int32)
        self.right=np.array(right,dtype=np.int32)
        self.qwaves=self.waves[self.right]

    def nonlinear(self,a):
        qdot=np.einsum('ij,ij->i',self.qwaves,a[self.left])
        terms=1j*qdot[:,None]*a[self.right]
        sums=np.zeros_like(a)
        np.add.at(sums,self.out,terms)
        return np.einsum('kij,kj->ki',self.projectors,sums)

    def rhs(self,a):
        return -self.nonlinear(a)-self.nu*self.square[:,None]*a

    def rk4(self,a,dt):
        k1=self.rhs(a)
        k2=self.rhs(a+dt*k1/2)
        k3=self.rhs(a+dt*k2/2)
        k4=self.rhs(a+dt*k3)
        return a+(dt/6)*(k1+2*k2+2*k3+k4)

    def snapshot(self,a,K,initial_support):
        n=self.nonlinear(a)
        norm2=np.sum(abs(a)**2,axis=1)
        low=self.square<=K*K
        E=.5*float(np.sum(norm2))
        El=.5*float(np.sum(norm2[low]))
        G=float(np.dot(self.square,norm2))
        H2=math.sqrt(float(np.dot((1+self.square)**2,norm2)))
        Pi=float(np.real(np.einsum('ij,ij->',np.conj(a[low]),n[low])))
        total_flux=float(np.real(np.einsum('ij,ij->',np.conj(a),n)))
        bound=math.sqrt(2*El)*C2*H2*math.sqrt(G)
        reality=float(np.max(np.linalg.norm(a[self.neg]-np.conj(a),axis=1)))
        divergence=float(np.max(abs(np.einsum('ij,ij->i',self.waves,a))))
        emerged=sum(float(norm2[i])>1e-16 for i in range(len(a))
                    if i not in initial_support)
        return {'energy':E,'gradient_square':G,'H2':H2,
                'low_flux':Pi,'ratio_flux_to_bound':abs(Pi)/bound,
                'full_flux_error':abs(total_flux),'reality_error':reality,
                'divergence_error':divergence,
                'new_modes_above_amplitude_1e-8':emerged}


def run(dt=.0025,steps=40):
    sys=System(N=4,nu=.1)
    K=2.0
    results=[]
    for shape in ('line','cube'):
        u=field(2,shape,20260923)
        a=np.zeros((len(sys.modes),3),dtype=complex)
        initial={sys.index[k] for k in u}
        for k,v in u.items(): a[sys.index[k]]=v
        snapshots=[]
        max_budget_step_error=0.
        for j in range(steps+1):
            if j in (0,steps//4,steps//2,3*steps//4,steps):
                s=sys.snapshot(a,K,initial)
                s['time']=j*dt
                snapshots.append(s)
                assert s['full_flux_error']<1e-10
                assert s['reality_error']<1e-10
                assert s['divergence_error']<1e-10
                assert s['ratio_flux_to_bound']<=1+1e-10
            if j==steps: break
            Eold=.5*float(np.sum(abs(a)**2))
            Gold=float(np.sum(sys.square[:,None]*abs(a)**2))
            a=sys.rk4(a,dt)
            Enew=.5*float(np.sum(abs(a)**2))
            Gnew=float(np.sum(sys.square[:,None]*abs(a)**2))
            budget_error=abs(Enew-Eold+sys.nu*dt*(Gold+Gnew)/2)
            max_budget_step_error=max(max_budget_step_error,budget_error)
            assert Enew<=Eold+1e-10
        results.append({'shape':shape,'initial_occupied_modes':len(initial),
                        'max_step_energy_budget_error':max_budget_step_error,
                        'snapshots':snapshots})
    return {'N':sys.N,'nu':sys.nu,'mode_count':len(sys.modes),
            'ordered_convolution_pairs':len(sys.out),'dt':dt,'steps':steps,
            'K':K,'runs':results,
            'scope':'Finite-dimensional short-time RK4 trajectory; not infinite-resolution regularity.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
