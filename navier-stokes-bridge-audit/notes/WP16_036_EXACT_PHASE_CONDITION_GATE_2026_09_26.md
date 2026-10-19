# WP16 Exact [223]+[123]→[036] Phase-Condition Gate

**Prince Upadhyay, Independent Research — 26 September 2026**

The persistent motif has now been reduced to one exact signed-permutation symmetry class with canonical triad

[
p=(-3,-2,-2),qquad
q=(-3,-1,2),qquad
k=(-6,-3,0).
]

For an individual exact triad term,

[
z_0=-|k|^4,i,(qcdot a_p)(overline{a_k}cdot a_q),
]

and after applying relative phase (	heta),

[
N_{m triad}(	heta)
=
Re!left[z_0e^{i	heta}ight]
=
|z_0|cosalpha,
]

where

[
alpha=arg(z_0)+	heta.
]

Therefore the exact pointwise maximizing condition is

[
oxed{alpha=0pmod{2pi}}.
]

This gate tests whether the registered [0,3,6] phase correction moves the 48 exact motif triads toward that phase condition.

For each of N8→N9, N9→N10, and N10→N11, compute coefficient-envelope-weighted:

- mean (|alpha|);
- RMS (alpha);
- (chi=langlecosalphaangle_A);
- envelope fraction within 0.10, 0.25, and 0.50 radians of the pointwise maximum;
- envelope fraction with positive signed contribution.

The decisive finite mechanism signature is:

[
	ext{weighted phase error decreases while weighted }chi	ext{ increases}
]

across all three recursive steps.

This is a finite-state phase-alignment diagnostic only. It does not claim that continuum Navier–Stokes dynamics enforces the maximizing condition.
