# WP19 v0.27a — Arb Terminal Signed-Numerator Gradient Subcertificate

**Author:** Prince Upadhyay, Independent Research  
**Date:** 30 September 2026  
**Status:** intervalization subgate following the successful WP19 v0.26 pre-interval design gate.

## Target

WP19 v0.26 established that the fixed signed-C500 numerator is the useful goal functional for cutoff transfer and that its floating continuous-adjoint predictions are small compared with the already rigorous negative numerator margin.

The first intervalization task is deliberately narrow: certify the arithmetic of the terminal gradient of the fixed polynomial at the exact nominal projected endpoint used by v0.26.

For

[
J(a)=sum_{gin K36}sigma_g n_g(a)-9sum_{gin C500}	au_g n_g(a),
]

the 36 signs (sigma_g), the 500 C500 signs (	au_g), the witness, and all selected orbit-pair groups remain frozen.

Using the real pairing (dJ=operatorname{Re}langle g,hangle), v0.27a evaluates the analytic directional derivative in the real and imaginary coordinate directions for every fixed-N11 Fourier coefficient, constructs the complex gradient, and applies the same divergence-free/reality tangent projection used in v0.23-v0.26.

## Algebraic collapse

Because all frozen coefficients are real, the 536 retained group contributions can be combined before differentiation.

Let

- (b=P_K,i(Qcdot a_p)a_q),
- (z=-Wlangle a_k,bangle),
- (D=sum_g c_g d_g), where (c_g=sigma_g) for K36 and (c_g=-9	au_g) for C500,
- (w=-Wlangle D,bangle).

Then

[
J=operatorname{Im}(woverline z).
]

For a perturbation (h),

[
db=P_K i[(Qcdot h_p)a_q+(Qcdot a_p)h_q],
]

[
dz=-W(langle h_k,bangle+langle a_k,dbangle),
]

[
dw=-W(langle dD,bangle+langle D,dbangle),
]

and

[
dJ=operatorname{Im}(dw,overline z+w,overline{dz}).
]

This is evaluated with 192-bit Arb arithmetic.

## Frozen identities

- witness SHA-256: `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`
- K36 SHA-256: `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`
- corrected prospective N13 K36 sign-chart SHA-256: `de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1`
- portable C500 semantic SHA-256: `1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f`
- selected ordered source pairs: 1048
- selected source modes: 1159

No datum, sign, key, rank, or coalition member is retuned.

## Matrix

The subcertificate is evaluated at the lower endpoint of each already studied transfer:

- N14 for 14→15,
- N15 for 15→16,
- N16 for 16→17,
- N17 for 17→18.

Each job downloads the existing certified predictor artifacts, reconstructs C500 from the byte-identical historical N11 predictor, and compares the Arb result against two independent v0.26 quantities:

1. the PyTorch reverse-mode terminal gradient;
2. the saved v0.26 endpoint directional linear prediction along (P_{11}(u_{M+1}(T)-u_M(T))).

## Pass meaning

A PASS means the fixed nominal terminal-gradient arithmetic has been independently enclosed with Arb and agrees with the floating implementation used by v0.26.

It **does not** yet certify:

- variation of the terminal gradient over the certified endpoint state-error ball;
- backward adjoint propagation;
- dual quadrature;
- endpoint Taylor remainder;
- dynamic nonlinear remainder;
- an all-N persistence theorem;
- any continuum Navier–Stokes regularity or blowup claim.

Those are separate subsequent interval subgates.
