# Fixed-datum crossing at two finite Galerkin cutoffs

**Prince Upadhyay — research checkpoint, 28 September 2026**

## Precise result

For the fixed 112-pair rational initial field (SHA-256
`4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`),
viscosity `ν=0.1`, the frozen K36 observable `F=I−9O`, and time interval
`[0,0.003]`, a sign change has now been certified at each of two finite
Fourier–Galerkin cutoffs. At N12 the initial field is exactly the N11 field
zero-padded into the extra modes. No parameter was retuned.

| Gate | N11 | N12 |
| --- | ---: | ---: |
| Exact initial `F(0)` | positive | `[645.8037741471, 645.8037741472]` |
| Certified endpoint `F(0.003)` | `[-54.748409847, -42.032667894]` (original bound) | `[-73.63322101, -70.396895629]` |
| Refined terminal trajectory-error upper bound | `0.000010526681` | `0.000011374869` |
| Whole-path normalizer | certified nonzero | `≥49091.85228719` |

The N11 archived trajectory, with the improved symmetric-strain bound and
rational Hermite probes, further encloses at least one zero between
`t=0.0028859375` and `t=0.0028921875`, a width of `0.00000625` seconds.
The N12 check establishes existence of a zero somewhere in `[0,0.003]`;
it has **not** located its time inside the N11 bracket.

## Why the error bound improved

For the exact finite solution `u`, approximate Hermite path `v`, error
`w=u−v`, and validated residual `r`, the transport energy identity involves
the symmetric strain `S(v)`, giving

`(1/2) d||w||₂²/dt + ν||∇w||₂² ≤ ||S(v)||∞,op ||w||₂² + ||r||₂||w||₂`.

For a divergence-free Fourier coefficient `v_k`,

`||sym(i k⊗v_k)||²_F = |k|²||v_k||²₂/2`.

Consequently the already certified whole-segment Fourier-gradient majorant
`M_j` can be replaced in the error recurrence by `M_j/√2`. At N11, this
reduces the terminal bound from `0.000045888408` to `0.000010526681`.
At N12, the corresponding bounds are `0.000050798503` and `0.000011374869`.

To justify the norm inequality even when `w=0`, set
`y_ε=(||w||₂²+ε²)^{1/2}` for `ε>0`. The energy inequality gives, almost
everywhere, `y_ε' ≤ S y_ε + R`, where `S=||S(v)||∞,op` and `R=||r||₂`;
this follows from `||w||₂/y_ε≤1` and `||w||₂²/y_ε≤y_ε`. Grönwall on a
segment of length `h` yields
`y_ε(t+h) ≤ e^{Sh}y_ε(t)+R(e^{Sh}−1)/S` (with the continuous `S=0`
limit). Letting `ε↓0` gives the same inequality for `||w||₂` at zeros too.
The implemented update `e^{Sh}(E+hR)` is a valid, slightly looser upper
bound because `(e^{Sh}−1)/S ≤ h e^{Sh}` for `S≥0`. In the N12 runner,
`h=0.000025` is now formed as an Arb decimal rather than through a Python
float representation.

## Verification and limits

The post-audit N12 run used 120 whole-segment Arb enclosures at 128-bit
precision. It independently recomputed and accepted all 120 saved segment
enclosures, then completed the trajectory, endpoint, and whole-path
normalizer gates in the same invocation. Its certificate and log are in
`results/wp16_n12_same_datum/post_audit_replay_20260929/`; the certificate
reports `independent_arb_segment_replay=true`. This run used the updated
runner, including the Arb decimal timestep, endpoint lower-bound labels, and
the GitHub/ZIP layout fallback. The predictor arrays and segment inputs are
SHA-256 tied to the frozen witness and K36 keys. Earlier receipts remain
available in the local N12 package as historical records.

This is a rigorous result for **two finite-dimensional ODEs**. It does not
bound the difference between successive cutoffs for all N, certify a
continuum solution at this time, or relate a crossing of `F` to blowup.
The present crossing alone is not a resolution of the Navier–Stokes
regularity problem.

## Next exact target

Derive and validate a cutoff-uniform estimate for the high Fourier tail and
for the effect of changing the cutoff on the K36 observable over this fixed
time interval. A useful theorem must provide explicit constants strong enough
to preserve a negative endpoint margin and a positive normalizer lower bound
as N grows, together with convergence to the continuum solution. After that,
one must prove what the persistent crossing implies for the continuum PDE.
The two finite certificates give concrete margins against which any proposed
tail estimate can be tested.

The full N12 data are split into `N12_Source_and_Certificate_v1.zip`,
`N12_Predictor_Nodes_v1.zip`, and `N12_Predictor_RHS_v1.zip`; extract all
three into the same directory. The source package includes the frozen
protocol, executable verifier, report, segment files, and a 250-file checksum
manifest. The N11 bracket has its own small companion ZIP.
