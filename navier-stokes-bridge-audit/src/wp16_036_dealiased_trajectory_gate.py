"""Short finite-Galerkin K36 trajectory diagnostic with exact dealiased FFT convolution."""

import argparse
import json
from pathlib import Path

import numpy as np

from galerkin import modes_in_ball, leray
import wp16_036_N12_frozen_K36_holdout as hold
from wp16_expanded_phase_search import base_state


class DealiasedSystem:
    def __init__(self, N=4, nu=.1):
        self.N, self.nu = N, nu
        self.modes = modes_in_ball(N)
        self.index = {k: i for i, k in enumerate(self.modes)}
        self.waves = np.asarray(self.modes, dtype=np.int32)
        self.square = np.einsum('ij,ij->i', self.waves, self.waves)
        self.projectors = np.asarray([leray(k) for k in self.modes])
        self.neg = np.asarray([self.index[tuple(-x for x in k)] for k in self.modes])
        self.L = 4 * N + 1
        self.slots = tuple(self.waves[:, j] % self.L for j in range(3))
        ki = self.index.get(hold.K)
        left, right = [], []
        for li, p in enumerate(self.modes) if ki is not None else ():
            q = tuple(hold.K[j]-p[j] for j in range(3))
            ri = self.index.get(q)
            if ri is not None:
                left.append(li); right.append(ri)
        self.left = np.asarray(left, dtype=np.int32)
        self.right = np.asarray(right, dtype=np.int32)
        self.out = np.full(len(left), -1 if ki is None else ki, dtype=np.int32)

    def nonlinear(self, a):
        f = np.zeros((self.L, self.L, self.L, 3), complex)
        f[self.slots] = a
        u = np.fft.ifftn(f, axes=(0, 1, 2)) * self.L**3
        prod = np.zeros_like(u)
        for j in range(3):
            grad = np.fft.ifftn(1j * self.waves_grid(j)[..., None] * f,
                                axes=(0, 1, 2)) * self.L**3
            prod += u[..., j, None] * grad
        conv = np.fft.fftn(prod, axes=(0, 1, 2))[self.slots] / self.L**3
        return np.einsum('kij,kj->ki', self.projectors, conv)

    def waves_grid(self, j):
        shape = [1, 1, 1]
        shape[j] = self.L
        return (np.fft.fftfreq(self.L) * self.L).reshape(shape)

    def rhs(self, a):
        return -self.nonlinear(a) - self.nu*self.square[:, None]*a

    def rk4(self, a, dt):
        k1 = self.rhs(a)
        k2 = self.rhs(a+dt*k1/2)
        k3 = self.rhs(a+dt*k2/2)
        k4 = self.rhs(a+dt*k3)
        return a+(dt/6)*(k1+2*k2+2*k3+k4)


def validate():
    from evolve_galerkin import System
    rng = np.random.default_rng(20260926)
    errors = {}
    for N in (4, 7):
        original = System(N=N)
        replacement = DealiasedSystem(N=N)
        a = rng.normal(size=(len(original.modes), 3))+1j*rng.normal(size=(len(original.modes), 3))
        a = np.einsum('kij,kj->ki',original.projectors,a)
        a[original.index[(0,0,0)]] = 0
        assert original.modes == replacement.modes
        error = float(np.max(np.abs(original.rhs(a)-replacement.rhs(a))))
        assert error < 2e-10, (N,error)
        errors[str(N)] = error
    return errors


def snapshot(system, a, keys, t):
    row = hold.evaluate_state(system, a, keys)
    row['time_after_anchor'] = t
    row['energy'] = float(.5*np.sum(abs(a)**2))
    row['reality_error'] = float(np.max(abs(a[system.neg]-np.conj(a))))
    row['divergence_error'] = float(np.max(abs(np.einsum('ij,ij->i', system.waves, a))))
    return row


def main():
    p = argparse.ArgumentParser()
    for n in ('n11-json','n12-json','n13-json','source-json','output'):
        p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--steps',type=int,default=2)
    p.add_argument('--dt',type=float,default=0.00001)
    p.add_argument('--cutoffs',type=int,nargs='+',default=[12,13])
    p.add_argument('--states',nargs='+',default=['inherited','target_only','full_final'])
    args = p.parse_args()
    validation = validate()
    j11,j12,j13,source = [json.loads(getattr(args,n.replace('-','_')).read_text())
                            for n in ('n11-json','n12-json','n13-json','source-json')]
    keys = hold.frozen_keys(source)
    hold.System = DealiasedSystem
    result = {'status':'post-hoc finite trajectory diagnostic', 'rhs_validation_max_abs':validation,
              'dt':args.dt,'steps':args.steps,'N':{}}
    for N,prev,curr in ((12,hold.get_row(j11,11),hold.get_row(j12,12)),
                        (13,hold.get_row(j12,12),hold.get_row(j13,13))):
        if N not in args.cutoffs:continue
        print('RECONSTRUCT',N,flush=True)
        system,states=hold.reconstruct(prev,curr)
        result['N'][str(N)]={}
        for name,a in states.items():
            if name not in args.states:continue
            rows=[]
            for step in range(args.steps+1):
                rows.append(snapshot(system,a,keys,step*args.dt))
                if step < args.steps:a=system.rk4(a,args.dt)
            result['N'][str(N)][name]=rows
            print('STATE',N,name,[r['passes_preregistered_consistency_criteria'] for r in rows],flush=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
