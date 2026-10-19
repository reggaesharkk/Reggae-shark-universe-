# WP19 v0.28 output-level bound audit — 1 October 2026

## Scope

This additive check reads the frozen JSON records for M14 segments 239, 238, and 237. It uses Python's standard library, independently enumerates the Fourier ball, and checks exact rational relationships among the serialized decimal bounds. It does not import the bound producer.

This is an output-level arithmetic check only. It does **not** recompute the Arb Bernstein coefficient suprema, the M14 residual convolution, or the complete continuous-segment strain and residual bounds.

## Findings

The independent enumeration of the full integer Fourier ball `|k| <= 14`, including the zero mode, gives 11,513 modes and `sum |k|^2 = 1,355,442`.

| Segment | Residual total minus serialized components | Uncertainty-penalty reconstruction from printed inputs |
|---:|---:|---|
| 239 | `-0.000001` | The printed-input formula exceeds the reported penalty by about 17.5921 |
| 238 | `-0.000002` | The printed-input formula exceeds the reported penalty by about 17.5889 |
| 237 | `-0.000002` | The printed-input formula exceeds the reported penalty by about 17.5848 |

The small residual-total differences are consistent with the producer's strict outward decimal serialization: each component and the total receive separate slack on a (10^{-6}) grid. They do not indicate an underbound.

The penalty comparison exposes a record-precision limitation. The formula is
`(sqrt(sum |k|^2) + 15 sqrt(mode_count)) * true_primal_radius * adjoint_polynomial_L2`.
The JSON stores the radius to 15 decimal places and the adjoint L2 upper bound to 6 places. Multiplying those printed upward-rounded values yields a conservative result about 17.59 larger than the reported penalty. This does not show that the producer's internal Arb penalty is wrong; it shows the archived JSON does not expose enough intermediate precision to independently reconstruct that component.

For each segment, the recorded logarithmic norm is above the independently calculated uncertainty-only strain floor `sqrt(sum |k|^2 / 2) * true_primal_radius`. This checks only that floor relationship; it does not independently recompute the strain supremum.

## Status and next gate

The output-level checks pass, and the precision limitation is recorded. Before treating the imported whole-segment strain and residual bounds as independently validated, a separate coefficient-level computation must recheck the Bernstein strain and residual suprema from the frozen arrays. The exact frozen inputs, arithmetic, and thresholds remain unchanged. Segment 236 is not generated.

Run the lightweight check with:

```sh
python src/wp19_v0_28_independent_output_bound_check.py --root .
```

Machine status: `PASS_OUTPUT_ARITHMETIC_WITH_PRECISION_LIMIT`.
