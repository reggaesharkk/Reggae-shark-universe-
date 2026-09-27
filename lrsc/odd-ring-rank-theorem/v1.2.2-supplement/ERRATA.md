# v1.2.2 errata ledger

This ledger is additive. Frozen v1.2 and v1.2.1 files are not rewritten.

| Location in v1.2.1 | Printed text | Correct text | Effect on conclusion |
|---|---|---|---|
| M=4L+1, monotonicity step | `f'(x)=-sin(x)[cos(2x)+4cos(x)]` | `f'(x)=-sin(x)[cos(2x)+4cos^2(x)]` | None. The corrected bracket is positive on the interval used, so `f` is still strictly decreasing. |
| M=4L+1, admissible-ring sentence | first admissible M is 13 | first admissible M is 9 | None. The proof already uses `alpha <= pi/9`; the endpoint case satisfies the required non-strict bound. |

## Terminology

Use **matrix rank** only for `rank(V)=p`.

Use **minimum passing channel cardinality**, **subset cardinality**, or
`K_0.001` for the finite M=99 values:

- `theta=0.07: K_0.001=14`;
- `theta=0.08: K_0.001=11`;
- `theta=0.09: K_0.001=12`.

The corresponding theorem ranks are 42, 41, and 40 because those are the
numbers of active reflection orbits in the three cells.
