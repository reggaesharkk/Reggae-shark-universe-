# WP16 Phase-Only Cutoff Escalation Gate

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** prospective finite-cutoff falsification search.  
**Target:** determine whether the refined WP16 evolved-spectrum phase-only quotient continues to rise beyond (N=7).  
**Not claimed:** no asymptotic theorem, no global optimizer, no cutoff-independent bound, no Navier–Stokes regularity result.

## Locked starting point

The completed expanded WP16 search produced a fixed-state refined phase-only benchmark

[
C_{infty,7}^{m phase}approx3.7441266968
]

at

[
N=7,qquad t=0.005,qquad A=4,
]

with 709 active conjugate phase pairs.

The new search does not alter modal magnitudes or polarizations. It varies only conjugacy-preserving phases.

## Escalation design

The default run tests

[
N=8,;9
]

at the same evolved anchor time (t=0.005) and amplitude (A=4).

The search uses **phase continuation**:

1. reconstruct the registered (N=7) optimized state from the completed raw JSON;
2. transfer its phase to every matching active Fourier pair at (N=8);
3. initialize genuinely new (N=8) active pairs at zero phase;
4. optimize new-pair phases first;
5. relax the full (N=8) phase torus;
6. transfer the resulting optimized (N=8) phase map into (N=9);
7. repeat the new-pair and full-torus relaxation.

This tests whether the previously found adversarial organization survives when new Fourier degrees of freedom are opened.

## Search protocol

Default deterministic settings:

- source state: (N=7,t=0.005), best completed expanded-WP16 phase vector;
- cutoffs: (N=8,9);
- search grid: (32^3);
- new-mode global draws: 24;
- new-mode block rounds: 3;
- full-torus block rounds: 4;
- 96 proposals per block round;
- block size: 32;
- initial phase step: 0.35 radians;
- deterministic seed derived from 20260925 and the cutoff.

Checkpoint JSON is written after every accepted improvement.

Each final state is reevaluated, without re-optimization, on all admissible grids among

[
32^3,;40^3,;48^3,;64^3,;96^3.
]

## Decision logic

Three qualitatively different finite outcomes are possible.

### Continued rise

If the refined values satisfy

[
C_{infty,7}^{m phase}
<
C_{infty,8}^{m phase}
<
C_{infty,9}^{m phase},
]

that is finite evidence that the phase-only obstruction remains active as the cutoff opens. It motivates a further (N=10) or analytical sequence construction, but does not prove divergence.

### Saturation

If (N=8,9) remain close to (3.7441), that suggests the evolved-spectrum phase-only family may be saturating. It still does not prove a cutoff-independent bound.

### Decline

If refined values decrease, the (N=7) maximum may be a finite-cutoff feature or the continuation optimizer may not have found the relevant higher-dimensional region. A decline is therefore not a theorem either.

## Relation to WP17

The broader WP17 sparse amplitude+phase family has a refined finite benchmark of approximately

[
5.1129326.
]

The present gate is intentionally narrower. It asks whether **phase freedom alone**, on evolved spectra with fixed modal magnitudes, exhibits further cutoff growth.

A refined (N=8) or (N=9) value above (5.1129326) would exceed the current finite WP17 benchmark, but would still be only a finite-family lower benchmark for any possible universal constant.

## Scope barrier

Every conclusion from this gate is finite-dimensional and conditional on the registered search family and optimizer.

No outcome proves or disproves the Millennium regularity conjecture.
