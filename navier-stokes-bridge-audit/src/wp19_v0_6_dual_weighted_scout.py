#!/usr/bin/env python3
"""WP19 v0.6 dual-weighted cutoff-defect scout.

NON-RIGOROUS scouting code. Uses saved floating predictor arrays and PyTorch
automatic differentiation. Outputs are diagnostics, not interval certificates.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path
import numpy as np
import torch

P,Q,K=(3,2,2),(3,-2,1),(6,0,3)

def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))

class TorchDealiased:
    def __init__(self,system,nu=0.1):
        self.s=system; self.nu=float(nu); self.L=system.L
        self.slots=[torch.tensor(x,dtype=torch.long) for x in system.slots]
        self.square=torch.tensor(system.square,dtype=torch.float64)
        self.projectors=torch.tensor(system.projectors,dtype=torch.float64)
        freq=torch.fft.fftfreq(self.L,d=1.0/self.L,dtype=torch.float64)
        self.kgrids=[]
        for j in range(3):
            shape=[1,1,1]; shape[j]=self.L
            self.kgrids.append(freq.reshape(shape))

    def rhs(self,a):
        f=torch.zeros((self.L,self.L,self.L,3),dtype=torch.complex128)
        f[self.slots[0],self.slots[1],self.slots[2],:]=a
        u=torch.fft.ifftn(f,dim=(0,1,2))*self.L**3
        prod=torch.zeros_like(u)
        for j in range(3):
            grad=torch.fft.ifftn(
                1j*self.kgrids[j][...,None]*f,
                dim=(0,1,2)
            )*self.L**3
            prod=prod+u[...,j,None]*grad
        conv=torch.fft.fftn(prod,dim=(0,1,2))[
            self.slots[0],self.slots[1],self.slots[2],:
        ]/self.L**3
        out=torch.einsum("kij,kj->ki",self.projectors.to(conv.dtype),conv)
        return -out-self.nu*self.square[:,None]*a

    def rk4_real(self,x,h):
        a=x[...,0]+1j*x[...,1]
        k1=self.rhs(a); k2=self.rhs(a+h*k1/2)
        k3=self.rhs(a+h*k2/2); k4=self.rhs(a+h*k3)
        y=a+(h/6)*(k1+2*k2+2*k3+k4)
        return torch.stack((y.real,y.imag),dim=-1)

class C500Upper:
    def __init__(self,system,k36_rows,c500_rows):
        self.s=system
        self.k36=[(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
                  for r in k36_rows]
        self.c500=[(tuple(r["left_orbit"]),tuple(r["right_orbit"]))
                   for r in c500_rows]
        groups=self.k36+self.c500
        gid={g:i for i,g in enumerate(groups)}
        li=[]; ri=[]; waves=[]; gids=[]
        for l,r in zip(system.left,system.right):
            key=(orbit(system.modes[l]),orbit(system.modes[r]))
            if key in gid:
                li.append(l); ri.append(r); waves.append(system.waves[r])
                gids.append(gid[key])
        self.groups=groups
        self.li=torch.tensor(li,dtype=torch.long)
        self.ri=torch.tensor(ri,dtype=torch.long)
        self.waves=torch.tensor(np.asarray(waves),dtype=torch.float64)
        self.gids=torch.tensor(gids,dtype=torch.long)
        self.K=torch.tensor(K,dtype=torch.float64)
        self.Q=torch.tensor(Q,dtype=torch.float64)
        self.K2=float(sum(x*x for x in K))
        self.p,self.q,self.k=(system.index[x] for x in (P,Q,K))
        self.weight=float(system.square[self.k]**2)
        self.tau=torch.tensor(
            [int(r["fixed_linear_sign"]) for r in c500_rows],
            dtype=torch.float64
        )

    def evaluate(self,xr):
        x=xr[...,0]+1j*xr[...,1]
        def project(v):
            kd=(v*self.K).sum(-1)
            return v-kd[...,None]*self.K/self.K2
        b=project(1j*(x[self.p]*self.Q).sum()*x[self.q])
        z=-self.weight*(torch.conj(x[self.k])*b).sum()
        raw=1j*(x[self.li]*self.waves).sum(-1)[:,None]*x[self.ri]
        d=-project(raw)
        grouped=torch.zeros(
            (len(self.groups),3),dtype=torch.complex128
        ).index_add(0,self.gids,d)
        w=-self.weight*(torch.conj(grouped)*b[None,:]).sum(-1)
        n=torch.imag(w*torch.conj(z))
        J=torch.abs(n[:len(self.k36)]).sum()-9*(
            self.tau*n[len(self.k36):]
        ).sum()
        return J/(torch.abs(z)**2)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--lower-N",type=int,required=True)
    p.add_argument("--lower-nodes",type=Path,required=True)
    p.add_argument("--higher-nodes",type=Path,required=True)
    p.add_argument("--k36",type=Path,required=True)
    p.add_argument("--c500",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--h",type=float,default=0.000025)
    p.add_argument("--nu",type=float,default=0.1)
    p.add_argument("--threads",type=int,default=6)
    a=p.parse_args()

    torch.set_num_threads(a.threads)
    sys.path.insert(0,str(a.repo.resolve()/"src"))
    from wp16_036_dealiased_trajectory_gate import DealiasedSystem

    low_sys=DealiasedSystem(a.lower_N,nu=a.nu)
    high_sys=DealiasedSystem(a.lower_N+1,nu=a.nu)
    torch_sys=TorchDealiased(low_sys,a.nu)

    k36=json.loads(a.k36.read_text())["keys"]
    c500=json.loads(a.c500.read_text())
    if c500.get("coalition_size")!=500:
        raise ValueError("wrong C500 file")
    objective=C500Upper(low_sys,k36,c500["keys"])

    lower=np.load(a.lower_nodes,mmap_mode="r")
    higher=np.load(a.higher_nodes,mmap_mode="r")
    if lower.shape[0]!=higher.shape[0]:
        raise ValueError("time-node count mismatch")
    steps=lower.shape[0]-1
    idx=np.asarray([high_sys.index[k] for k in low_sys.modes],dtype=np.int64)
    projected=np.asarray(higher[:,idx,:])
    lower_arr=np.asarray(lower)

    t0=time.time()
    xT=torch.tensor(
        np.stack([lower_arr[-1].real,lower_arr[-1].imag],axis=-1),
        dtype=torch.float64,requires_grad=True
    )
    base=objective.evaluate(xT)
    lam=torch.autograd.grad(base,xT)[0].detach()
    vT=torch.tensor(
        np.stack([projected[-1].real,projected[-1].imag],axis=-1),
        dtype=torch.float64
    )
    high=float(objective.evaluate(vT).detach())

    contributions=[]; defects=[]; adj=[float(torch.linalg.vector_norm(lam))]
    for j in range(steps-1,-1,-1):
        pred=low_sys.rk4(projected[j],a.h)
        defect=projected[j+1]-pred
        dr=torch.tensor(
            np.stack([defect.real,defect.imag],axis=-1),
            dtype=torch.float64
        )
        contributions.append([j,float((lam*dr).sum())])
        defects.append([j,float(np.linalg.norm(defect))])
        x=torch.tensor(
            np.stack([lower_arr[j].real,lower_arr[j].imag],axis=-1),
            dtype=torch.float64,requires_grad=True
        )
        y=torch_sys.rk4_real(x,a.h)
        lam=torch.autograd.grad((y*lam).sum(),x)[0].detach()
        adj.append(float(torch.linalg.vector_norm(lam)))

    contributions.reverse(); defects.reverse()
    vals=np.asarray([x[1] for x in contributions])
    linear=float(vals.sum()); basef=float(base.detach()); actual=high-basef
    result={
        "status":"NON-RIGOROUS discrete-adjoint scouting",
        "lower_N":a.lower_N,"upper_N":a.lower_N+1,
        "steps":steps,"h":a.h,"nu":a.nu,
        "base_upper_G_C500":basef,
        "higher_projected_upper_G_C500":high,
        "actual_delta_G":actual,
        "linearized_dual_weighted_defect_sum":linear,
        "linearization_remainder":actual-linear,
        "sum_absolute_dual_weighted_defect_contributions":float(np.abs(vals).sum()),
        "max_absolute_single_step_contribution":float(np.abs(vals).max()),
        "positive_step_count":int((vals>0).sum()),
        "negative_step_count":int((vals<0).sum()),
        "positive_contribution_sum":float(vals[vals>0].sum()) if np.any(vals>0) else 0.0,
        "negative_contribution_sum":float(vals[vals<0].sum()) if np.any(vals<0) else 0.0,
        "terminal_adjoint_norm":adj[0],
        "max_adjoint_norm":max(adj),
        "initial_adjoint_norm":adj[-1],
        "elapsed_seconds":time.time()-t0,
        "contributions":contributions,
        "defect_norms":defects,
        "adjoint_norms_backward":adj
    }
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ("contributions","defect_norms","adjoint_norms_backward")},
                     indent=2))

if __name__=="__main__":
    main()
