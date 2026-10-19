# WP19 bridge results

This folder records the compact, repository-friendly outputs from the three WP19 bridge packages archived separately in Drive.

## Archive ZIP hashes

- WP19_Consecutive_Cutoff_Bridge_Gate_v0_1.zip  
  SHA-256: 83001f1ec9bfbcccac8d06dd23abe81c477e68ec397e55097a1a0dff9212d8aa
- WP19_v0_2_Evidence_Inventory_and_Bridge_Map.zip  
  SHA-256: a53e8636ae7e4fe3b1dc10d573e4c2355b4124bbe9d727e754aafd1f687acd53
- WP19_v0_3_Consecutive_Cutoff_Bridge_Scout.zip  
  SHA-256: baedca8e915f479240bd5704a41a154757dcde4602b3e35bc6c407919c86246d

## Repository contents

- `N14_N17_ARTIFACT_INVENTORY.json` — provenance map for the earlier N14-N17 prospective cutoff program.
- `N14_N17_EVIDENCE_LEDGER.csv` — compact evidence-class ledger.
- `WP19_v0_2_BRIDGE_PLAN.json` — proof-first bridge plan keeping the optimizer-derived N14-N17 track separate from the later same-rational-datum Arb track.
- `WP19_v0_3_SCOUT_RESULTS.json` — compact scouting metrics for N11->N12 and N12->N13.
- `BRIDGE_SCOUT_TABLE.csv` — headline comparison table.

The full node-by-node scouting traces and sampled physical-strain arrays are retained in the archived v0.3 ZIP. They are reproducible with the scripts in `src/`.

## Evidence boundary

The v0.3 computation is explicitly **non-rigorous scouting**. It identifies the current proof-loss bottleneck: the Fourier-l1 strain majorant is much looser than the sampled physical-space symmetric strain. The next proof target is a whole-segment rigorous enclosure of `||S(u_N)||_{L-infinity,op}`, combined with an Arb enclosure of the newly opened-shell forcing.

The historical N14-N17 phase/time-gate data are not the same datum as the later N11-N13 rational-witness Arb certificate family and must not be relabeled as such.

## v0.4 one-sided observable bridge

WP19 v0.4 proves an exact finite algebraic monotonicity statement for the frozen K36 observable: once the low coefficients are fixed and the cutoff is at least 10, newly added higher modes cannot increase F=I-9O. They cannot enter any selected K36 orbit-pair key, while new outside-key masses contribute nonnegatively to O.

The dynamic cutoff problem therefore reduces to controlling the high shell's backreaction on the old low modes. The accompanying scout records low-mode endpoint drifts 0.225582 for N11->N12 and 0.203005 for N12->N13, with sampled backreaction recurrences 0.373078 and 0.322998. These are diagnostics, not certificates.

The archived v0.4 ZIP SHA-256 is `1cfa821bc7ccadc50db77c068dc756cfd1b89051595e2caa7b708625f8a123a4`.


## v0.5 fixed finite coalition locality

WP19 v0.5 freezes a post-hoc N11-derived set of 200 outside-K36 orbit-pair groups. Because omitted outside groups only decrease the full observable, the retained coalition defines an exact upper observable `U_C200` with `F <= U_C200`.

The union of K36 and C200 uses exactly 461 ordered K-channel source pairs and 569 unique Fourier modes. Every retained orbit has norm at most 11, so this support is unchanged at N=11,12,13,14,17 and, algebraically, for every larger cutoff.

The unchanged C200 upper observable is negative at the saved same-datum endpoints:
- N11: -33.178421
- N12: -44.220575
- N13: -46.113595

These three values are floating transfer diagnostics. The support-locality theorem and `F <= U_C200` inequality are exact. A single global low-mode L2 perturbation ball remains far too loose, so the next gate must propagate support-aware or direction-aware error on the fixed 569-mode set.

C200 SHA-256: `4fb5531fcc6c4490aa7826992ff843f27fefdbc1427c7587ac0544027420e698`.

The archived v0.5 ZIP SHA-256 is `fa1c440248016c015bd974b191232d1ffc687f2b5b722eabb31bf61ee30a5a5f`.


## v0.6 dual-weighted residual bridge

WP19 v0.6 replaces the norm-first endpoint perturbation route with a goal-oriented discrete-adjoint scout.

A post-hoc N11-derived C500 outside coalition is frozen with SHA-256 `79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`. Using
`n_g = Im(w_g * conj(z))` and fixed signs `tau_g`, it defines the exact upper surrogate

`G_C500 = (sum_K36 |n_g| - 9 sum_C500 tau_g n_g)/|z|^2`

with `F <= G_C500` whenever the normalizer is nonzero.

The C500 surrogate depends on exactly 1,048 ordered source pairs and 1,159 Fourier modes for every cutoff at least 11. The materialized C500 JSON is retained in the v0.6 archive; `src/wp19_v0_6_build_fixed_c500.py` deterministically regenerates it and verifies its hash.

The non-rigorous discrete-adjoint scout gives:

- N11->N12: base upper margin `-47.816278`, projected-higher value `-55.152798`, linearized dual-weighted defect sum `-7.505923`, observed nonlinear remainder `+0.169403`, and sum of absolute step contributions `9.489442`.
- N12->N13: base upper margin `-55.152798`, projected-higher value `-55.760507`, linearized dual-weighted defect sum `-0.604941`, observed remainder `-0.002768`, and sum of absolute step contributions `6.198853`.

These are floating scouting quantities, not interval certificates. The next proof target is a rigorous scalar dual-weighted residual bound plus a second-order remainder enclosure, not a global state-norm bound.

The archived v0.6 ZIP SHA-256 is `ed6346092007e9cd15ad17c157aa55b69990606fdaed4397874edff037d9dedd`.


## v0.7 exact-rational C500 endpoint certificate

WP19 v0.7 validates the v0.6 C500 endpoint surrogate on the already certified same-datum N11-N13 trajectories.

The saved endpoint node is reconstructed using the same exact-decimal solenoidal/reality projection rule as the Arb endpoint certificate, and `G_C500` is evaluated with exact rational arithmetic. The previously certified endpoint error formula is a key-independent coefficient-9 source/normalizer envelope, so it also encloses perturbations of `G_C500`.

Certified intervals are:

- N11: `[-54.174149219, -41.458407264]`
- N12: `[-56.770960917, -53.534635536]`
- N13: `[-57.555599822, -53.965413679]`

All three upper endpoints are strictly negative. This certifies the C500 upper functional at the existing finite cutoffs; it does not yet certify a lower-cutoff-only next-cutoff prediction or any continuum statement.

The archived v0.7 ZIP SHA-256 is `17c3d67aaa9ef113b6534f61e83532c914eeba28f21c46550ca30a71ff46113c`.


## v0.8 kink-safe quadratic dual bridge

WP19 v0.8 removes the absolute-value sign-flip obstruction from the dual-weighted endpoint architecture with the exact scalar inequality

`|x| <= sign(x0)*x + (x-x0)^2/(2|x0|)`.

Applied groupwise at the lower endpoint, this gives

`G_C500(v) <= G_C500(a) + [L_a(v)-L_a(a)] + Q_a(v)`,

where `L_a` is a smooth signed endpoint functional and `Q_a` is an explicit nonnegative quadratic correction over only the 36 K36 ratios. No K36 sign-stability assumption is required.

On the saved transitions the observed quadratic corrections are `0.750228` for N11->N12 and `0.268059` for N12->N13. Reinterpreting the v0.6 adjoint as the first-order sensitivity of `L_a`, the smooth observed remainders are only `-0.048112` and `-0.002768`.

After charging the v0.7 certified base upper margin, the sum of absolute observed first-order terms, the observed Q term, and the absolute smooth remainder, the scouting residual margins are approximately `31.17` and `47.06`. These are design budgets, not interval certificates.

The archived v0.8 ZIP SHA-256 is `b192fd222da5e7d50d908cf4037981f83f2ce4c6a79a9b4517d1f21bfa804b47`.


## v0.9 certified K36 sign chambers

WP19 v0.9 resolves the 36 K36 absolute-value signs inside each existing certified endpoint ball.

All 36 numerator signs are certified at N11, N12, and N13. The weakest sign-margin ratios `|n_g|/Delta n_g` are approximately `3.1054`, `1.9571`, and `5.2772`, respectively.

N12 and N13 lie in the same 36-sign chamber. N11 differs in exactly one frozen key, `((2,2,2),(2,5,8))`.

The N13 sign chart is frozen prospectively for a future same-datum N14 test with SHA-256 `7cbb307c70aa14fabdc28ae07f0965716bf498e63c371b61e1b9bfd00611c7bd`.

The archived v0.9 ZIP SHA-256 is `ee1fda165f6f980fd77f6907017c832c729bc9ebaf29c0ee93ef3e3cf309c566`.

## v0.10 signed C500 numerator certificate

WP19 v0.10 uses the v0.9 sign locks to remove the K36 absolute values from the current endpoint balls and certifies the signed C500 numerator directly.

Instead of charging every retained group with the global source perturbation, v0.10 uses a group-specific Cauchy bound over the repeated source indices. Certified C500 upper bounds improve to approximately:

- N11: `-44.8446856075`
- N12: `-54.4140649514`
- N13: `-54.9610084477`

The corresponding signed numerator upper bounds are all strictly negative, and the independent normalizer lower bounds remain positive.

The dynamic cutoff-transfer problem is still open. The next rigorous target is a validated dual-weighted residual plus second-order remainder for this frozen signed numerator.

The archived v0.10 ZIP SHA-256 is `e8875372558cfc805e0082bf74f5cf6fa90ccbb8a96e5a7acb3b9d5911ffab5a`.


## v0.11 fixed-Pi11 locality and prospective N14 transfer

WP19 v0.11 sharpens the v0.6 support result to an exact projection identity. Every orbit entering the frozen K36+C500 numerator has norm at most 11, and the normalizer anchors are also inside N11. Therefore, for every cutoff `M>=11`, the signed numerator depends only on `Pi_11 a`, and whenever the normalizer is nonzero,

`G_C500(a) = G_C500(Pi_11 a)`.

A same-rational-datum N14 predictor was then generated **after** the v0.9 N13 K36 sign chart had been frozen. The predictor uses the unchanged witness, `nu=0.1`, `T=0.003`, 120 RK4 steps and no retuning. Predictor array hashes are recorded in `N14_SAME_DATUM_PREDICTOR_METADATA.json`.

The prospective floating N14 endpoint gives approximately `F=-87.088300523` and `G_C500=-52.841462912`. An independent half-step run differs by only `6.1163e-9` in endpoint L2 and preserves the frozen N13 K36 numerator sign chart 36/36. These are numerical diagnostics, not an Arb trajectory certificate.

For the prospectively frozen N13->N14 signed-numerator adjoint scout, `Delta G=+2.919044`. The signed-numerator change is about `+7.73799e9`, the first-order dual sum is about `+7.74153e9`, and the floating remainder is about `-3.54e6` (roughly 0.04575% of the actual numerator change). All 120 observed first-order step contributions are positive.

Thus the earlier N11->N13 decrease in G does not continue monotonically at N14. The current runtime lacks `python-flint`, so the N14 120-segment Arb enclosure has not been run here.

The archived v0.11 ZIP SHA-256 is `0f3853212d697c0dcc3619454e15e6543a21f2d05a039f988ccc1f54c09ffe86`.


## v0.12 recursive low/high closure and regularity compatibility gate

The prospective N14 same-datum Arb validation passed with terminal trajectory-error upper bound `0.000012825905`, endpoint interval `[-89.015834781,-85.160766265]`, and whole-path normalizer lower bound `48850.68586052`. The rigorous same-datum finite-cutoff chain is now N11-N14.

v0.12 translates the recursive-closure idea into the exact fixed projection `P=P11`. For `u_M=v_M+h_M`, the low state satisfies

`dv_M/dt + nu A v_M + P B(v_M,v_M) = Gamma_M`

with

`Gamma_M=-P[B(v_M,h_M)+B(h_M,v_M)+B(h_M,h_M)]`.

For two cutoffs, the fixed finite-dimensional energy estimate gives a cutoff-independent stability inequality of the form

`||v_M-v_L|| <= exp(C11||u0||T) ||Gamma_M-Gamma_L||_{L1_t L2_x}`.

This reduces all-cutoff transfer of the frozen signed numerator to a summable high-to-low closure budget.

v0.12 also records two exact obstructions to a naive regularity interpretation. First, a negative K36/C500 value is compatible with a smooth finite Fourier state, so the static sign cannot itself imply singularity. Second, because `G_C500(a)=G_C500(Pi11 a)`, arbitrarily large high-frequency tails can be added without changing G; therefore G alone cannot control a high-frequency regularity criterion or determining wavenumber.

The next gate is to bound the shellwise closure increment by a genuine high-frequency dissipation/continuation quantity. The archived v0.12 ZIP SHA-256 is `6d59f7d9c62ad968cae86034ef333883488364c0540c234d6f1afa9e526af702`.


## v0.13 fixed-output closure and weak-limit passage

WP19 v0.13 proves the fixed-output Fourier estimate

`||P11 B(a,b)||_2 <= sqrt(5574) ||a||_2 ||b||_{H1}`,

where `sqrt(5574) ~= 74.6592258197` and the constant is independent of the outer cutoff.

Applied to the exact high-to-low closure forcing, this shows that for any Leray-Hopf weak solution the spectrally truncated closure converges to the full fixed-low closure in `L1_t L2_x`. Standard Galerkin compactness then implies that a future cutoff-uniform negative margin for the fixed polynomial signed numerator would pass to a Leray-Hopf weak limit through the finitely many `P11` coefficients.

v0.13 also gives an explicit direct shell-addition bound for the closure increment. The remaining hard term is the state/backreaction drift between `P_M u_{M+1}` and `u_M`, which is the target for the existing stability/adjoint machinery.

The archived v0.13 ZIP SHA-256 is `fd236ae9056711c139ede0db750c8c566e47ee571fa62b9a1417023bbcf72606`.


## N14 same-datum Arb validation — PASS

The prospective N14 whole-segment validation completed successfully on GitHub Actions run `36608785015`.

Frozen setup:

- same 112-pair rational witness as N11-N13;
- witness SHA-256 `4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624`;
- frozen K36 SHA-256 `7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47`;
- `nu=0.1`, `T=0.003`, 120 whole-segment 128-bit Arb enclosures;
- no N14 retuning.

Validated outputs:

- terminal trajectory-error upper bound: `0.000012825905`;
- `F(0) in [645.8037741471,645.8037741472]`;
- `F(0.003) in [-89.015834781,-85.160766265]`;
- whole-path normalizer lower bound: `48850.68586052`.

The rigorous same-datum finite-Galerkin chain is therefore N11-N14.

The complete workflow artifact contains 126 files, is 127,530,612 bytes, and has SHA-256 `b0bb454fa320887c2b17dfd8a0bae916273253bb057ecff7acee3d6218234698`.

This remains a finite-Galerkin certificate, not an all-N or continuum theorem.

## v0.14 divergence-free output-frequency cancellation

WP19 v0.14 sharpens the fixed-output closure estimate using incompressibility.

For `k=p+q` and divergence-free advecting coefficient `a_p`,

`a_p dot q = a_p dot (k-p) = a_p dot k`.

Thus a high input frequency does not appear as a derivative loss when the output is restricted to the fixed low projector. The exact estimate is

`||P_K B(a,b)||_2 <= C_K ||a||_2 ||b||_2`

with

`C_K^2 = sum_{0<|k|<=K} |k|^2`.

For `K=11`, independent Wolfram enumeration gives 5,574 nonzero output modes,

`sum |k|^2 = 404724`

and

`C_11 = sqrt(404724) ~= 636.179220031588`.

Applied to the recursive closure forcing, this replaces the v0.13 derivative-bearing bound by an energy-level estimate. For one fixed Leray-Hopf solution, the direct high-shell-to-low closure increments are absolutely summable. For **consecutive different Galerkin solutions**, uniform energy/dissipation alone gives only a worst-case `O(1/M)` direct increment, which is not summable. The remaining all-cutoff target is therefore shell-energy decay stronger than `1/M` plus the recursive state/backreaction drift.

The archived v0.14 ZIP SHA-256 is `0afb76a98ffc8e6c67858ce61cac50e71e4b39b22e726cb382735d4e11f01f68`.


## v0.15 full-PDE residual and a-posteriori regularity scout

WP19 v0.15 measures the continuum truncation residual
`Q14 B(u14,u14)` on the 121 saved nodes of the separately Arb-validated N14 predictor.

This is explicitly **floating node-sampled scouting**, not a continuum certificate.

Headline diagnostics:

- `||R_tail||_(L2_t H^-1) ~= 0.3312582611`
- `||R_tail||_(L1_t H^-1) ~= 0.0166855303`
- `||R_tail||_(L2_t L2) ~= 4.9703990588`
- `||R_tail||_(L1_t H1) ~= 3.7718196582`
- sampled `sup_t ||u14||_L3 ~= 117.844184420`
- sampled `||u14||_(L4_t L6) ~= 31.081463808`

The positive-norm residual route is therefore not an attractive direct next certificate at N14. The Fourier `H^-1` residual is materially smaller: the `L1_t H1` diagnostic is about 226 times the `L1_t H^-1` diagnostic.

This redirects the continuum-regularity verification effort toward a modern negative-residual a-posteriori criterion. The missing rigorous pieces include whole-segment residual enclosure, `W^-1,3`, explicit torus constants, and combination with the existing Galerkin path radius.

Drive archive ID: `12ucoktQPMr74ARBcSGGEeJHboEi6pGr-`.

The archived v0.15 ZIP SHA-256 is `dc2811af36412ca93ac0602f90b3b9a22bea1505708f4ad4bcc0fe84b3822d1b`.


## v0.16 rigorous critical-space a-posteriori no-go

WP19 v0.16 evaluates the published Brunk-Giesselmann-Tscherpel critical-space sufficient strong-existence criterion against the exact N14 cubic-Hermite reconstruction.

After the exact unit-torus Navier-Stokes rescaling, a 160-bit Arb lower gate uses only the first Hermite segment and one omitted Fourier mode `k=(12,5,6)`. It proves `A>0.00720428952807`, `log M>9.326757996764e12`, and therefore `log(criterion LHS)>6.217838664529e12>0`. The sufficient condition `LHS<=1` is rigorously false for this reconstruction.

This does not imply blowup or failure of continuum strong existence. It rules out this particular generic-constant certification route and motivates reconstruction-specific Fourier-linearized stability with modewise viscosity.

The archived v0.16 ZIP SHA-256 is `382c9cdff7902990132ba36f1d593e72cf1f6bdf66ec3878352f903d6a57073c`.


## v0.17-v0.18 same-datum fast tail scouts

The untouched same rational datum was extended in floating arithmetic through N15, N16, N17 and N18 with no retuning.

The original K36 endpoint remains strongly negative numerically through N18. The fixed C500 surrogate gives approximately:

`N14 -52.84146, N15 -50.62254, N16 -50.22688, N17 -50.12304, N18 -50.15012`.

N18 therefore breaks any simple monotone-in-N story. The absolute sizes of the successive G corrections nevertheless have ratios about `0.178, 0.262, 0.261`.

More directly, the sampled fixed-low closure differences have L1_t L2_x totals about

`0.017159, 0.009070, 0.003500, 0.000997`

for N14->15 through N17->18, with ratios about `0.529, 0.386, 0.285`.

These are floating theorem-design diagnostics, not infinite-tail bounds.

To minimize wall time, whole-segment same-datum Arb validation for N15-N18 was launched as a four-way GitHub Actions matrix, run `36669057015`.

Archive hashes:
- v0.17: `ef2f7307ed4b15ea5d59b2f162f4fde9797bf3473c17c20642fd21aefaab7621`
- v0.18: `ad3678c4db7aa78b35e27574eb01044a0417c84a745d22e63893c810df7b365e`
