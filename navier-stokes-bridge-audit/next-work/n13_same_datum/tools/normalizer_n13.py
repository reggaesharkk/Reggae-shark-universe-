"""Arb nonvanishing guard for the tracked K-channel normalizer on [0,.003].

Uses an a priori uniform L2 trajectory-error radius. The guard is valid only
when that radius is certified by all residual segments.
"""

import json
from pathlib import Path

import numpy as np
from flint import acb, arb, ctx

import wp16_036_sparse_turnover_exact_anchor as exact
import wp16_036_turnover_arb_runner as runner
import wp16_036_turnover_arb_segment as segment
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


def anchor_projection(k, raw):
    kk=sum(x*x for x in k)
    kd=sum((raw[j]*k[j] for j in range(3)),acb(0))
    return [raw[j]-kd*k[j]/kk for j in range(3)]


def coefficients(k, a, b, f, g, exact_a=None):
    h=arb('0.000025')
    A,B,F,G=(anchor_projection(k,[segment.ball(v) for v in row])
             for row in (a,b,f,g))
    if exact_a is not None:
        A=[acb(arb(re.numerator)/arb(re.denominator),
               arb(im.numerator)/arb(im.denominator)) for re,im in exact_a]
    c1=[h*v for v in F]
    c2=[3*(B[j]-A[j])-h*(2*F[j]+G[j]) for j in range(3)]
    c3=[2*(A[j]-B[j])+h*(F[j]+G[j]) for j in range(3)]
    radius=sum((segment.ball_l2_upper(v) for v in (c1,c2,c3)),arb(0)).upper()
    return A,radius


def guard(directory, error_decimal='0.001', witness=None):
    ctx.prec=128
    system=DealiasedSystem(13)
    nodes=np.load(directory/'nodes.npy',mmap_mode='r')
    rhs=np.load(directory/'rhs.npy',mmap_mode='r')
    E=arb(error_decimal)
    if witness is None:raise ValueError('exact rational witness required for first segment')
    exact_field,_,sha=exact.input_state(Path(witness))
    if sha!=exact.EXPECTED_WITNESS:raise ValueError('witness hash mismatch')
    qnorm=arb(sum(x*x for x in exact.Q)).sqrt().upper()
    minimum=None
    for step in range(120):
        fields={}
        for k in (exact.P,exact.Q,exact.K):
            i=system.index[k]
            fields[k]=coefficients(k,nodes[step,i],nodes[step+1,i],
                                   rhs[step,i],rhs[step+1,i],
                                   exact_field[k] if step==0 else None)
        (p,dp),(q,dq),(k,dk)=(fields[x] for x in (exact.P,exact.Q,exact.K))
        b=anchor_projection(exact.K,[acb(0,1)*sum((p[j]*exact.Q[j] for j in range(3)),acb(0))*q[i]
                                     for i in range(3)])
        B=segment.ball_l2_upper(b)
        bp,bq,bk=(segment.ball_l2_upper(v) for v in (p,q,k))
        z=-sum((k[j].conjugate()*b[j] for j in range(3)),acb(0))*2025
        delta_b_path=qnorm*(dp*bq+bp*dq+dp*dq)
        delta_z_path=2025*(dk*B+(bk+dk)*delta_b_path)
        # Enclose the true field relative to the segment's initial anchor.
        tp,tq,tk=dp+E,dq+E,dk+E
        delta_b=qnorm*(tp*bq+bp*tq+tp*tq)
        delta_z=2025*(tk*B+(bk+tk)*delta_b)
        lower=(z.abs_lower()-delta_z).lower()
        if not lower>0:
            raise ValueError(f'normalizer not certified at segment {step}')
        if minimum is None:minimum=lower
        else:minimum=minimum.min(lower).lower()
    return {'status':'Arb normalizer nonvanishing guard conditional on uniform L2 radius',
            'E_uniform_input_decimal':error_decimal,
            'z_abs_uniform_lower_decimal':runner.decimal_lower(minimum,8),
            'all_120_segments_pass':True}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--E',default='0.001')
    p.add_argument('--witness',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=guard(a.directory,a.E,a.witness)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result)
