# Rank-one channel update across the 0.08 to 0.07 mask transition

This note analyzes the already certified finite benchmark at `M=99`,
`k_idx=49`, `A=1/2`. It adds an exact mechanism identity; it does not change
the frozen odd-ring theorem or replace the exhaustive subset certificates.

Let `S` be the periodic stencil, `m_08` and `m_07` the two stress masks, and
`j` the local-min shedding field. The only newly active sites at the lower
threshold are `a=41` and `-a=58` modulo 99. Directly from the near-Nyquist
field, `j_a=j_{-a}=0`. Put

\[
 d=\delta_a+\delta_{-a},\qquad h=S(d).
\]

Then `m_07=m_08+d` and the target satisfies the **exact identity**

\[
 E_{07}=S(m_{07}j)=S(m_{08}j)=E_{08}.
\]

Write the channel input as `w_0(t)=\hat j_0` and
`w_r(t)=2\hat j_r\cos(2\pi r t/99)` for `1<=r<=49`. Every `w_r` is even, so
`w_r(a)=w_r(-a)=b_r`. Linearity of `S` gives, for all 50 channels,

\[
 V_{r,07}=V_{r,08}+b_r h,\qquad
 b_0=\hat j_0,\quad
 b_r=2\hat j_r\cos(2\pi r a/99)\;(r\geq1).
\]

In matrix form, with channels as columns,

\[
 V_{07}=V_{08}+h b^{\mathsf T}.
\]

Thus the *difference* of the two dictionaries has rank one (provided `b` is
nonzero). This is independent of the theorem's rank of each dictionary: the
certified matrix ranks are 41 and 42, respectively. With the normalized
real-space inner product, `||h||²=3/99=1/33` exactly.

For an arbitrary fixed subset `A` of channel indices, define
`B_A=\sum_{r\in A} b_r` and
`R_{08}(A)=E_{08}-\sum_{r\in A}V_{r,08}`. The new residual is exactly

\[
 R_{07}(A)=R_{08}(A)-B_Ah,
\]

so

\[
 \|R_{07}(A)\|^2=\|R_{08}(A)\|^2
 -2 B_A\langle R_{08}(A),h\rangle+B_A^2/33.
\]

The relative residual uses the *same* denominator `||E||` in both cells. The
formula permits either an increase or decrease for a particular subset; it
does not imply monotonicity of the optimum over subsets or prove a minimum
cardinality without searching or a separate bound.

## Numerical mechanism check

The accompanying `rank_one_transition.py` reconstructs the definitions at
50 decimal digits and verifies the column update to `1.1e-49` maximum
absolute entry discrepancy. For the old 0.08 eleven-channel witness
`{0,1,3,42,43,44,45,46,47,48,49}`, `B_A=0.00335169416257103915` and its
relative residual moves from `0.000962369127664990` to
`0.001221072389216878`, crossing the `0.001` tolerance. That explains the
failure of **this witness**. The exhaustive 0.07 certificate, not this
identity, excludes all subsets with at most thirteen channels.

The certified 0.07 fourteen-channel witness
`{0,1,2,4,5,6,42,43,44,45,46,47,48,49}` has relative residual
`0.000974040815024211` after the update and passes. The displayed decimals
are high-precision diagnostics; the repository's interval/exact-integer
certificates support the formal finite pass/fail claims.

## Reproduction

From the Universe repository root, with `mpmath` installed:

```bash
python lrsc/finite-benchmark/mask-transition/rank_one_transition.py
```

The canonical script and report are also preserved in the
[LRSC specialist repository](https://github.com/reggaesharkk/lrsc-odd-ring-spectral-rank/tree/main/finite-benchmark/mask-transition).

The script imports the independent real-space construction in the additive
v1.2.2 supplement, performs no branch-and-bound search, and sends no network
requests. It neither modifies nor regenerates either frozen DOI archive.
