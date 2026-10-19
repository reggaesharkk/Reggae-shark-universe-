#!/usr/bin/env python3
"""Independent Decimal recurrence check, not independent residual recomputation."""
import hashlib
import json
import sys
from decimal import Decimal, localcontext, ROUND_CEILING
from pathlib import Path

def verify(path):
    x=json.loads(path.read_text())
    if x['schema']!='wp19-v0.28-adjoint-segment-arb-v1' or x['status']!='CONTINUOUS_SEGMENT_ENCLOSURE_ONLY':
        raise ValueError('unexpected segment protocol/status')
    if x['M']!=14 or x['step']!=239 or x['backward_order_index']!=0 or x['forward_time_interval_rational']!=['239/80000','240/80000']:
        raise ValueError('pilot is not the first backward segment')
    source=Path(__file__).with_name('wp19_v0_28_adjoint_segment_arb.py')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=x['source_sha256']:
        raise ValueError('source identity mismatch')
    frozen=x['frozen']
    expected={
        'witness_sha256':'4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624',
        'K36_sha256':'7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47',
        'K36_sign_chart_sha256':'de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1',
        'C500_portable_semantic_sha256':'1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f'}
    if frozen!=expected: raise ValueError('frozen identities changed')
    b={k:Decimal(v) for k,v in x['bounds'].items()}
    if not all(v.is_finite() and v>=0 for v in b.values()): raise ValueError('invalid bound')
    with localcontext() as ctx:
        ctx.prec=80; ctx.rounding=ROUND_CEILING
        R=b['residual_L2_upper']; L=b['logarithmic_norm_upper']; e=b['terminal_adjoint_error_upper']; h=Decimal('0.0000125')
        if R < b['nominal_residual_L2_upper']+b['primal_uncertainty_residual_penalty_upper']:
            # Individual printed bounds may each round up beyond their sum's print.
            if R+Decimal('0.000002') < b['nominal_residual_L2_upper']+b['primal_uncertainty_residual_penalty_upper']:
                raise ValueError('residual sum inconsistent')
        amplification=(L*h).exp().next_plus()
        integral=(amplification-1)/L if L else h
        final=amplification*e+integral*R
    return {'status':'PASS LIMITED PILOT RECURRENCE CHECK','segment_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'backward_error_after_one_segment_upper':str(final),
        'verified_scope':'provenance, scalar bounds, and outward Decimal recurrence only; residual enclosure supplied by Arb producer',
        'pending':['239 remaining M14 segments','other cutoff paths','rigorous dual quadrature','nonlinear remainder','normalizer transfer'],
        'claim_boundary':'No full adjoint or signed-numerator cutoff-transfer certificate.'}

if __name__=='__main__':
    result=verify(Path(sys.argv[1])); out=Path(sys.argv[2]); tmp=out.with_suffix('.tmp')
    tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); tmp.replace(out)
    print(json.dumps(result,indent=2))
