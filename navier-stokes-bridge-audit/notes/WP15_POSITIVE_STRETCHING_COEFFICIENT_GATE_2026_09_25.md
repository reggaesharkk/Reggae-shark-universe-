# WP15: Positive-Stretching Coefficient Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** analytical scaling survivor plus finite stress test.  
**Scope:** unforced periodic 3D Navier–Stokes, zero mean, \(\sigma=0\), \(s=2\), fixed high-advector threshold \(K=2\).  
**Open theorem:** WP11 L2–L3 remains unproved.

## 1. Candidate exposed by WP14

WP14 found strong descriptive co-movement between the endpoint-normalized target

\[
\Gamma_{\rm req}
=
\frac{b_{\rm req}}{\|\omega\|_\infty}
\]

and the endpoint-normalized positive stretching factor

\[
g_{\rm stretch}
=
\frac{
\langle(\omega\cdot S\omega)_+\rangle
}{
\|\omega\|_\infty G
}.
\]

Multiplying by the endpoint scale eliminates \(\|\omega\|_\infty\) and exposes the noncircular candidate

\[
\boxed{
b_{\rm stretch}
=
\frac{
\langle(\omega\cdot S\omega)_+\rangle
}{
G
}.
}
\]

The pointwise L2-L3 candidate becomes

\[
\boxed{
N_2^{>K}
\le
\theta\nu Y_2
+
C\,b_{\rm stretch}\,X_2.
}
\]

No constant \(C\) is fitted or registered in advance.

## 2. Scaling check

Under fixed-energy concentration

\[
u_\lambda(x)=\lambda^{3/2}v(\lambda x),
\]

we have

\[
G\mapsto\lambda^2G.
\]

The local stretching density contains two vorticity factors and one velocity gradient, and its spatial mean/integral scales as

\[
\langle(\omega\cdot S\omega)_+\rangle
\mapsto
\lambda^{9/2}
\langle(\omega\cdot S\omega)_+\rangle.
\]

Therefore

\[
\boxed{
b_{\rm stretch}\mapsto\lambda^{5/2}b_{\rm stretch}.
}
\]

For \(s=2\),

\[
X_2\mapsto\lambda^4X_2,
\]

so

\[
b_{\rm stretch}X_2
\mapsto
\lambda^{13/2}
b_{\rm stretch}X_2,
\]

exactly matching the positive leading concentration scale of the signed \(H^2\) transfer.

Thus WP12/WP13 concentration scaling does not reject this candidate.

## 3. Unit constant already fails on the registered trajectory

The WP14 matched-state data contain a sampled point with

\[
\frac{b_{\rm req}}{b_{\rm stretch}}
\approx
1.023889
\]

for the combined perturbed \(N=7\), amplitude-4, \(\theta=0.25\) trajectory near \(t=0.0035\).

Therefore the special choice \(C=1\) is already false on that finite sample.

This does not reject a larger cutoff-independent constant.

## 4. Static stress-test quotient

For any smooth finite Galerkin field define

\[
C_{\rm req}^{\rm stretch}
=
\frac{
[N_2^{>K}-\theta\nu Y_2]_+
}{
b_{\rm stretch}X_2
}
\]

when \(b_{\rm stretch}X_2>0\).

If a universal pointwise estimate with finite \(C\) exists, then

\[
C_{\rm req}^{\rm stretch}\le C
\]

for every admissible field.

Finite random sampling cannot establish such a uniform bound. It can, however, falsify proposed constants and expose growth with cutoff or spectral family.

The companion audit therefore tests deterministic real divergence-free fields from:

- full Fourier balls;
- outer-half spectral shells;
- several deterministic seeds;
- cutoffs \(N=3,\dots,7\);
- a fixed amplitude chosen so that nonlinear transfer is not trivially buried by the viscous reserve.

## 5. Independent time-integral problem

Even if the pointwise estimate survives, WP11 L3 separately requires an independently controlled all-prefix integral of \(b_{\rm stretch}\).

The exact enstrophy identity uses the **signed** stretching

\[
\frac12 G'
=
\langle\omega\cdot S\omega\rangle-\nu D,
\]

not its positive part.

Therefore

\[
\langle(\omega\cdot S\omega)_+\rangle
\]

cannot simply be replaced by the signed quantity in the identity, and the energy identity alone does not supply

\[
\int_0^T b_{\rm stretch}(t)\,dt.
\]

This gate keeps pointwise domination and time-integrability as separate obligations.

## 6. Interpretation barrier

A bounded sampled \(C_{\rm req}^{\rm stretch}\) does not prove a cutoff-independent constant.

Growth in a deterministic finite family is evidence only until converted into an explicit analytical counterexample family.

If the candidate survives numerical stress, the next step is to seek either:

1. an analytical inequality for the pointwise bound; or
2. an explicit phase/spectral family making \(C_{\rm req}^{\rm stretch}\) unbounded.

No arbitrary-data global-regularity result is claimed.


## 7. Executed nonlinear-dominant static stress test

The first (A=4) random-field run was not informative because the viscous
reserve dominated every sampled cubic transfer. The same deterministic fields
were therefore rerun at amplitude (A=1024), which isolates the
nonlinear-dominant static quotient without changing its large-amplitude
geometric limit.

The run used:

- full-ball and outer-half-shell random divergence-free fields;
- (N=3,ldots,7);
- ten deterministic seeds per family/cutoff;
- (K=2), (s=2), (	heta=0.25).

The largest sampled required constants were:

| family | N | max (C_{m req}^{m stretch}) |
| --- | ---: | ---: |
| outer half | 3 | 0.168837 |
| full ball | 3 | 0.146289 |
| full ball | 4 | 0.115567 |
| outer half | 4 | 0.101578 |
| full ball | 6 | 0.060236 |
| outer half | 6 | 0.046709 |
| full ball | 7 | 0.044081 |
| outer half | 5 | 0.034917 |
| full ball | 5 | 0.012502 |
| outer half | 7 | 0.000000 |

No monotone growth with cutoff appears in this finite random family.

By contrast, the structured WP14 combined (N=7), amplitude-4,
(	heta=0.25) trajectory reached

[
C_{m req}^{m stretch}approx1.023889.
]

Thus the registered structured phase-cascade trajectory is substantially more
demanding for this candidate than the tested random-phase fields.

This does not prove a universal finite constant. It suggests that any
counterexample or proof mechanism is likely to depend on structured phase and
geometry rather than generic spectral occupancy alone.

The workflow artifact for the nonlinear-dominant random stress test has
SHA-256 digest

    sha256:fcc5a67d704e394c75de136d96e4debcc8f826db3c58f75033b7b36bbd9e3df7

## 8. Current decision

The pointwise candidate

[
N_2^{>K}
le
	heta
u Y_2
+
C,b_{m stretch}X_2
]

survives the present finite stress suite for some (C>1.023889), but no
cutoff-independent analytical constant has been proved.

The L3 time-integral requirement is also completely open.

The next gate should therefore target one of two failure modes directly:

1. a structured phase family with unbounded
   (C_{m req}^{m stretch}); or
2. an obstruction to independently controlling
   (int b_{m stretch},dt).

