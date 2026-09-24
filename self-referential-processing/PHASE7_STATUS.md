# Phase 7 — final inferential-validation status

Final production:
- 10 production blocks
- 500 deterministic replicates
- 4 DGP cells
- 2 fit architectures
- 4,000 total GLMM fits
- final aggregation integrity pass

Primary all-evaluable-fit stratum:

- Null, rho=0: M1 rejection 0.066 / coverage 0.934; M2 rejection 0.072 / coverage 0.928
- Null, rho=.30: M1 rejection 0.064 / coverage 0.936; M2 rejection 0.074 / coverage 0.926
- Effect=.10 log-odds: both architectures showed very high descriptive power, but power was not the validity criterion

Under the locked exact-binomial compatibility rule, M1 satisfied the null calibration and coverage screens under both rho conditions; M2 did not.

Interpretation is deliberately narrow: this supports M1 as the candidate architecture under the tested simulation DGP. It does not establish universal validity, equivalence to nominal calibration, or existence of a live Self effect.
