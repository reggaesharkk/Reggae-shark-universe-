"""Memory-bounded implementation of the unchanged WP16 phase-search objective."""

import numpy as np

from strain_alignment_trajectory import spatial_fields
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


class LowMemorySearchSystem(DealiasedSystem):
    def __init__(self, N, nu=.1):
        super().__init__(N=N, nu=nu)
        index_cube=np.full((2*N+1,)*3,-1,dtype=np.int32)
        coords=self.waves+N
        index_cube[coords[:,0],coords[:,1],coords[:,2]]=np.arange(len(self.modes),dtype=np.int32)
        high_left=np.flatnonzero(self.square>4)

        def outputs(pi):
            sums=self.waves+ self.waves[pi]
            within=np.all((sums>=-N)&(sums<=N),axis=1)
            right=np.flatnonzero(within)
            candidate=sums[within]+N
            out=index_cube[candidate[:,0],candidate[:,1],candidate[:,2]]
            good=out>=0
            return right[good],out[good]

        total=sum(len(outputs(int(pi))[0]) for pi in high_left)
        self.high_out=np.empty(total,dtype=np.int32)
        self.high_left=np.empty(total,dtype=np.int32)
        self.high_right=np.empty(total,dtype=np.int32)
        pos=0
        for pi in high_left:
            right,out=outputs(int(pi))
            end=pos+len(right)
            self.high_out[pos:end]=out
            self.high_left[pos:end]=pi
            self.high_right[pos:end]=right
            pos=end
        assert pos==total


def evaluate_lowmem(system,a,s=2.0,K=2,grid=48,chunk=100_000):
    if K!=2:
        raise ValueError('frozen search uses K=2; rebuild the source table for another K')
    if grid<=3*system.N:
        raise ValueError('grid must exceed 3N for exact cubic spatial averages')
    weights=system.square.astype(float)**s
    X=float(np.sum(weights[:,None]*abs(a)**2))
    G=float(np.sum(system.square[:,None]*abs(a)**2))
    signed=0.
    envelope=0.
    for start in range(0,len(system.high_out),chunk):
        stop=min(start+chunk,len(system.high_out))
        out=system.high_out[start:stop]
        left=system.high_left[start:stop]
        right=system.high_right[start:stop]
        qdot=np.einsum('ij,ij->i',system.waves[right],a[left])
        raw=1j*qdot[:,None]*a[right]
        projected=np.einsum('kij,kj->ki',system.projectors[out],raw)
        z=-weights[out]*np.einsum('ij,ij->i',np.conj(a[out]),projected)
        signed+=float(np.real(np.sum(z)))
        envelope+=float(np.sum(np.abs(z)))
    chi=signed/envelope if envelope else 0.

    grad,omega,_,imag=spatial_fields(system,a,grid)
    if imag>1e-10:
        raise AssertionError('imaginary field error')
    strain=(grad+np.swapaxes(grad,-1,-2))/2
    local=np.einsum('...i,...ij,...j->...',omega,strain,omega)
    positive=float(np.mean(np.maximum(local,0.)))
    signed_stretch=float(np.mean(local))
    grid_G=float(np.mean(np.sum(omega**2,axis=-1)))
    if abs(grid_G-G)>5e-8*max(1.,G):
        raise AssertionError('grid/Fourier G mismatch')
    b_stretch=positive/G if G>0 else 0.
    denom=b_stretch*X
    C=(max(signed,0.)/denom if denom>0 else
       (float('inf') if signed>0 else 0.))
    reality=float(np.max(np.linalg.norm(a[system.neg]-np.conj(a),axis=1)))
    divergence=float(np.max(abs(np.einsum('ij,ij->i',system.waves,a))))
    if reality>1e-10 or divergence>1e-10:
        raise AssertionError('state constraints failed')
    return dict(X2=X,G=G,H2_high_transfer=signed,H2_high_envelope=envelope,
                chi_H2_high=chi,H1_positive_stretching=positive,
                H1_signed_stretching=signed_stretch,b_stretch=b_stretch,
                C_infinity_stretch=C,reality_error=reality,
                divergence_error=divergence)
