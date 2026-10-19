# WP16 Exact Separable Motif Variational Gate

**Prince Upadhyay, Independent Research — 26 September 2026**

For the persistent motif

[
[223]_{m advector}+[123]_{m advected}	o[036]_{m output},
]

vary only the 12 conjugate-pair phases of the target output orbit [036], holding the two input-orbit phases and all amplitudes fixed.

Because [036] appears only in the output slot, the motif functional separates exactly by target pair:

[
F(phi_1,dots,phi_{12})
=
sum_{r=1}^{12}Re!left[C_r e^{-iphi_r}ight].
]

For pair (r), the complex coefficient (C_r) is obtained by summing the fixed input-side phasors for output (+k_r) and the conjugated phasors for output (-k_r).

Therefore each pair has the exact finite motif-only maximizer

[
oxed{phi_r^*=arg C_rpmod{2pi}},
]

and exact pair maximum

[
F_r^{max}=|C_r|.
]

The gate compares the inherited and registered [036]-only phases against these exact pairwise optima and reports:

- number of target pairs moving toward their exact optimum;
- coefficient-weighted mean phase distance to the exact optima;
- motif objective before and after the registered correction;
- exact separable motif optimum;
- fraction of available motif-only gain captured.

This is an exact finite variational statement for the isolated motif with fixed inputs. It is not a characterization of the full phase objective or continuum dynamics.
