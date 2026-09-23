"""Experimental exact-integer interval enclosure for the fixed LRSC benchmark.

Research author: Prince Upadhyay, Independent Research.
This script has not undergone independent verification and is not a release proof.
All endpoint arithmetic below is done with Python integers, rounded outward on
a fixed dyadic grid; trigonometric constants use rational Machin and Taylor
remainders. The external exhaustive-search log is treated as an input witness.
"""
from __future__ import annotations

import math
import re
import struct
import hashlib
from fractions import Fraction
from pathlib import Path

M = 99
N = 50
SCALE = 1 << 192


def ceiling_div(a: int, b: int) -> int:
    return -((-a) // b)


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: int, hi: int | None = None):
        self.lo = lo
        self.hi = lo if hi is None else hi
        assert self.lo <= self.hi

    @staticmethod
    def rational(q: Fraction) -> I:
        a = q.numerator * SCALE
        return I(a // q.denominator, ceiling_div(a, q.denominator))

    @staticmethod
    def integer(a: int) -> I:
        return I(a * SCALE)

    def __add__(self, b: I) -> I:
        return I(self.lo + b.lo, self.hi + b.hi)

    def __neg__(self) -> I:
        return I(-self.hi, -self.lo)

    def __sub__(self, b: I) -> I:
        return self + -b

    def __mul__(self, b: I) -> I:
        values = (self.lo * b.lo, self.lo * b.hi,
                  self.hi * b.lo, self.hi * b.hi)
        return I(min(values) // SCALE, ceiling_div(max(values), SCALE))

    def div_int(self, n: int) -> I:
        assert n > 0
        return I(self.lo // n, ceiling_div(self.hi, n))

    def lower_float(self) -> float:
        return self.lo / SCALE

    def upper_float(self) -> float:
        return self.hi / SCALE


ZERO = I.integer(0)
ONE = I.integer(1)
HALF = I.rational(Fraction(1, 2))
THETA = I.rational(Fraction(2, 25))
TOL2 = I.rational(Fraction(1, 1000000))


def atan_remainder_bound_denominator(z: int, terms: int) -> int:
    return (2 * terms + 1) * z ** (2 * terms + 1)


def atan_bounds(z: int, terms: int = 100) -> tuple[Fraction, Fraction]:
    # Arctan(1/z) has a strictly alternating series with decreasing terms.
    approx = sum(((-1) ** n * Fraction(1, (2*n+1)*z**(2*n+1))
                  for n in range(terms)), Fraction(0))
    tail = Fraction(1, atan_remainder_bound_denominator(z, terms))
    return (approx, approx + tail) if terms % 2 == 0 else (approx - tail, approx)


def pi_interval() -> I:
    a_lo, a_hi = atan_bounds(5)
    b_lo, b_hi = atan_bounds(239)
    lo, hi = 16*a_lo-4*b_hi, 16*a_hi-4*b_lo
    return I(I.rational(lo).lo, I.rational(hi).hi)


PI = pi_interval()
assert 3 * SCALE < PI.lo < PI.hi < 4 * SCALE


def trig_table() -> tuple[list[I], list[I]]:
    # Taylor remainder for cos degree 130 and sin degree 131 on [-4,4]
    # is respectively at most 4^131/131! and 4^132/132!, both < 1/SCALE.
    num_terms = 66
    assert 4**(2*num_terms-1)*SCALE < math.factorial(2*num_terms-1)
    assert 4**(2*num_terms)*SCALE < math.factorial(2*num_terms)
    cosines: list[I] = []
    sines: list[I] = []
    for t in range(M):
        t0 = t if t <= M//2 else t-M
        x = PI * I.rational(Fraction(2*t0, M))
        x2 = x*x
        c, tc = ZERO, ONE
        s, ts = ZERO, x
        for n in range(num_terms):
            c = c + tc
            s = s + ts
            tc = -(tc*x2).div_int((2*n+1)*(2*n+2))
            ts = -(ts*x2).div_int((2*n+2)*(2*n+3))
        # Both Taylor remainder magnitudes are < one grid unit.
        cosines.append(I(c.lo-1, c.hi+1))
        sines.append(I(s.lo-1, s.hi+1))
    return cosines, sines


def complex_mul(a: tuple[I, I], b: tuple[I, I]) -> tuple[I, I]:
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def complex_add(a: tuple[I, I], b: tuple[I, I]) -> tuple[I, I]:
    return a[0]+b[0], a[1]+b[1]


def dft(x: list[I], cosines: list[I], sines: list[I]) -> list[tuple[I, I]]:
    out=[]
    for q in range(M):
        re, im = ZERO, ZERO
        for i, xi in enumerate(x):
            t = (q*i) % M
            re = re + xi*cosines[t]
            im = im - xi*sines[t]
        out.append((re.div_int(M),im.div_int(M)))
    return out


def build_coefficients() -> tuple[I,list[I],list[list[I]], int]:
    cosines, sines = trig_table()
    X = [ONE + HALF*cosines[(49*i)%M] for i in range(M)]
    j=[];mask=[]
    active=0
    for i in range(M):
        l,c,r = X[(i-1)%M],X[i],X[(i+1)%M]
        minimum=I(min(l.lo,c.lo,r.lo), min(l.hi,c.hi,r.hi))
        j.append(c-minimum)
        stress=((c-l)*(c-l)+(c-r)*(c-r))*HALF
        if stress.lo>THETA.hi:
            mask.append(ONE); active+=1
        elif stress.hi<=THETA.lo:
            mask.append(ZERO)
        else:
            raise ArithmeticError(f"Threshold mask not certified at i={i}")
    y=[j[i] if mask[i].lo==SCALE else ZERO for i in range(M)]
    mh,jh,yh=(dft(field,cosines,sines) for field in (mask,j,y))
    stencil=[cosines[q]-ONE for q in range(M)]
    E=[(stencil[q]*yh[q][0],stencil[q]*yh[q][1]) for q in range(M)]
    V=[]
    for r in range(N):
        row=[]
        for q in range(M):
            v0=complex_mul(jh[r],mh[(q-r)%M])
            if r:
                v0=complex_add(v0,complex_mul(jh[M-r],mh[(q-(M-r))%M]))
            row.append((stencil[q]*v0[0],stencil[q]*v0[1]))
        V.append(row)
    def dot(a:list[tuple[I,I]],b:list[tuple[I,I]]) -> I:
        out=ZERO
        for k in range(M):
            out=out+(a[k][0]*b[k][0]+a[k][1]*b[k][1])
        return out
    c=dot(E,E)
    assert c.lo>0
    lin=[dot(v,v)-I.integer(2)*dot(E,v) for v in V]
    gram=[[ZERO for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(a+1,N):
            gram[a][b]=gram[b][a]=dot(V[a],V[b])
    return c,lin,gram,active


def float_grid(x:float) -> int:
    a,b=x.as_integer_ratio()
    assert SCALE%b==0
    return a*(SCALE//b)


def radius(x:I,v:float) -> int:
    fv=float_grid(v)
    return max(abs(x.lo-fv),abs(x.hi-fv))


def score_f64(subset, c, lin, gram):
    val=c
    for i in subset:
        val+=lin[i]
    for a in range(len(subset)):
        for b in range(a+1,len(subset)):
            val+=2.0*gram[subset[a]][subset[b]]
    return val


def audit(c, lin, gram, active):
    file=Path(__file__).resolve().parent/'channels.bin'
    data=file.read_bytes()
    v=struct.unpack('<'+str(len(data)//8)+'d',data)
    norm_d,cd=v[:2]
    ld=list(v[2:52]); gd=[v[52+i*N:52+(i+1)*N] for i in range(N)]
    dc=radius(c,cd)
    dl=max(radius(lin[i],ld[i]) for i in range(N))
    dg=max(radius(gram[i][j],gd[i][j]) for i in range(N) for j in range(i+1,N))
    coefficient_error=dc+10*dl+90*dg
    # IEEE 754 binary64 round-to-nearest, 55 additions for 10 terms/45 pairs.
    # Powers-of-two scaling of stored finite gram entries does not round or overflow.
    assert all(math.isfinite(gd[i][j]) and abs(gd[i][j])<1 for i in range(N) for j in range(i+1,N))
    L=abs(Fraction.from_float(cd))+10*max(map(lambda x:abs(Fraction.from_float(x)),ld))+90*max(abs(Fraction.from_float(gd[i][j])) for i in range(N) for j in range(i+1,N))
    # Include an additive allowance for gradual underflow, even though the
    # observed search scores are normal. This is conservative for every subset.
    float_error=Fraction(55,2**53-55)*L+Fraction(110,2**1074)
    assert float_error < Fraction(1,10**12)
    log=(Path(__file__).resolve().parent/'VERIFICATION_OUTPUT_independent.txt').read_text()
    parsed=re.findall(r'^K=(\d+) expected=(\d+) visited=(\d+).*?best_subset=\(([^)]+)\) best_score_hex=(0x[0-9a-f.]+p[+-]\d+) quad_err=([0-9.e-]+)',log,re.M)
    assert len(parsed)==10
    bounds=[]
    for k,expected,visited,indices,hex_score,reported in parsed:
        subset=tuple(int(i) for i in indices.split(','));k=int(k)
        assert len(subset)==k and int(expected)==int(visited)==math.comb(N,k)
        qv=score_f64(subset,cd,ld,gd)
        best_score=float.fromhex(hex_score)
        assert best_score>0 and qv==best_score
        assert abs(math.sqrt(qv)/norm_d-float(reported))<1e-14
        # %a prints the exact binary64 minimum; it involves no decimal
        # formatting uncertainty or sqrt/division rounding analysis.
        best_score_lower=Fraction.from_float(best_score)
        # Exact operator coefficient differences and C summation error are
        # uniform over all subsets, irrespective of which subset is best.
        uniform_error=Fraction(coefficient_error,SCALE)+float_error
        lower=I.rational(best_score_lower-uniform_error)
        threshold=c*TOL2
        gap=lower.lo-threshold.hi
        bounds.append((k,gap))
        assert gap>0,f'No certified gap for K={k}: {gap/SCALE}'
    # Direct interval evaluation of the selected K=11 witness objective.
    k11=(0,1,3,42,43,44,45,46,47,48,49)
    q11=c
    for i in k11:q11=q11+lin[i]
    for a in range(11):
        for b in range(a+1,11):q11=q11+I.integer(2)*gram[k11[a]][k11[b]]
    witness_margin=(c*TOL2).lo-q11.hi
    assert witness_margin>0
    print('active',active,'pi_width', (PI.hi-PI.lo)/SCALE)
    print('channel_binary_sha256',hashlib.sha256(data).hexdigest())
    print('search_log_sha256',hashlib.sha256(log.encode()).hexdigest())
    print('max_coefficient_differences',dc/SCALE,dl/SCALE,dg/SCALE)
    print('coefficient_error_uniform_K_le_10',coefficient_error/SCALE)
    print('double_summation_error_upper',float(float_error))
    print('K_lower_gap_squared',[(k,gap/SCALE) for k,gap in bounds])
    print('K11_witness_gap_squared',witness_margin/SCALE)


if __name__=='__main__':
    audit(*build_coefficients())
