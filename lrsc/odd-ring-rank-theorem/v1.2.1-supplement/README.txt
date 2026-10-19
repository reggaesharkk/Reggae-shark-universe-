LRSC v1.2.1 — Proof Clarification & Verification Supplement

This is a separate draft supplement to the frozen LRSC v1.2 release. It does not alter v1.2 or DOI 10.17605/OSF.IO/NM5BW.

Contents
- LRSC_v1_2_1_Proof_Clarification_Supplement.tex: complete LaTeX source
- verify_LRSC_v1_2_1_independent.py: independent finite numerical verifier
- VERIFICATION_OUTPUT.txt: captured result from the verifier

Reproduce the numerical checks with Python 3 and NumPy installed:
  python3 verify_LRSC_v1_2_1_independent.py

The verifier checks finite cases only; it is corroboration, not a proof of the universal theorem. The proof is given in the supplement.

Reported check summary: 197 odd rings (9 through 401); 20,094 coefficients; maximum direct finite-sum error below 2e-14; 35/35 rank cases passed at relative SVD tolerance 1e-10.
