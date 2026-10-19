"""Arb endpoint K36 margin enclosure conditional on an L2 trajectory radius.

The radius must come from a completed validated segment runner. This module
encloses the exact decimal endpoint field, all ordered K-channel groups, and
the global weighted perturbation inequality, including absolute-value kinks.
"""

import json
from pathlib import Path

import numpy as np
from flint import acb, arb, ctx

import wp16_036_sparse_turnover_exact_anchor as exact
import wp16_036_turnover_arb_runner as runner
import wp16_036_turnover_arb_segment as segment
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


def vdot(a,b):
    return sum((a[i].conjugate()*b[i] for i in range(3)),acb(0))


def norm_upper(v):
    return segment.ball_l2_upper(v)


def projection(k,vector):
    kk=sum(x*x for x in k)
    kd=sum((vector[i]*int(k[i]) for i in range(3)),acb(0))
    return [vector[i]-kd*int(k[i])/kk for i in range(3)]


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


def evaluate(nodes_path,keys_path,E_decimal):
    ctx.prec=128
    system=DealiasedSystem(13)
    arr=np.load(nodes_path,mmap_mode='r')[-1]
    a=segment.solenoidal_reality_projection(system,arr)
    keys_raw=keys_path.read_bytes()
    if __import__('hashlib').sha256(keys_raw).hexdigest() != "7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47":
        raise ValueError('K36 key hash mismatch')
    keys={(tuple(row['left_orbit']),tuple(row['right_orbit']))
          for row in json.loads(keys_raw)['keys']}
    p,q,k=(system.index[x] for x in (exact.P,exact.Q,exact.K))
    b=projection(exact.K,[acb(0,1)*sum((a[p][j]*exact.Q[j] for j in range(3)),acb(0))*a[q][i]
                          for i in range(3)])
    weight=int(system.square[k]**2)
    z=-weight*vdot(a[k],b)
    groups={}
    d_sum=arb(0)
    for li,ri in zip(system.left,system.right):
        wave=system.waves[ri]
        raw=[acb(0,1)*sum((a[li][j]*int(wave[j]) for j in range(3)),acb(0))*a[ri][i]
             for i in range(3)]
        d=[-v for v in projection(exact.K,raw)]
        d_sum+=norm_upper(d)
        w=-weight*vdot(d,b)
        key=(orbit(system.modes[li]),orbit(system.modes[ri]))
        groups[key]=groups.get(key,acb(0))+w
    I=arb(0); O=arb(0)
    for key,w in groups.items():
        mass=abs((w/z).imag)
        if key in keys:I+=mass
        else:O+=mass
    Fv=I-9*O
    E=arb(E_decimal)
    A=norm_upper([v for row in a for v in row])
    bp,bq,bk=(norm_upper(a[ix]) for ix in (p,q,k))
    B=norm_upper(b)
    dq=arb(sum(x*x for x in exact.Q)).sqrt().upper()
    delta_b=dq*E*(bp+bq+E)
    delta_d=arb(system.N)*(2*A*E+E*E)
    delta_z=weight*(E*B+(bk+E)*delta_b)
    z_abs=z.abs_lower().lower()
    z_lower=(z_abs-delta_z).lower()
    if not z_lower > 0:
        raise ValueError('normalizer lower bound failed')
    delta_w=weight*(delta_d*B+(d_sum+delta_d)*delta_b)
    w_sum=weight*d_sum*B
    error=(9*(delta_w/z_lower+w_sum*delta_z/(z_lower*z_abs))).upper()
    upper=(Fv+error).upper()
    lower=(Fv-error).lower()
    return {'status':'Arb endpoint margin conditional on supplied Galerkin L2 error radius',
            'E_input_decimal':E_decimal,
            'F_of_exact_decimal_endpoint_upper':runner.decimal_upper(Fv.upper(),9),
            'F_of_exact_decimal_endpoint_lower_ball':str(Fv.lower()),
            'F_of_exact_decimal_endpoint_lower_decimal':runner.decimal_lower(Fv.lower(),9),
            'z_abs_lower_decimal':str(z_abs),
            'z_perturbation_upper_decimal':runner.decimal_upper(delta_z.upper(),9),
            'F_error_upper_decimal':runner.decimal_upper(error,9),
            'F_true_lower_decimal':runner.decimal_lower(lower,9),
            'F_true_upper_decimal':runner.decimal_upper(upper,9),
            'certified_negative_if_E_valid':upper<0,
            'ordered_group_count':len(groups)}


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--keys',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    aggregate=json.loads((args.directory/'aggregate.json').read_text())
    if aggregate['steps']!=120 or aggregate['witness_sha256']!=exact.EXPECTED_WITNESS:
        raise ValueError('wrong aggregate provenance')
    result=evaluate(args.directory/'nodes.npy',args.keys,
                    aggregate['terminal_L2_error_upper_decimal'])
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
