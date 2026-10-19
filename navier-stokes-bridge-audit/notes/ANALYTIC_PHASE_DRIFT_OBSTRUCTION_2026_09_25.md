# Analytic obstruction: instantaneous triad phase drift

**Prince Upadhyay, Independent Research — 25 September 2026**

**Status:** exact finite-dimensional algebraic obstruction.  
**Scope:** one explicit real, divergence-free Fourier state and its isolated helical-triad reduction.  
**Not claimed:** no persistent phase locking, no invariant six-mode subsystem, no continuum regularity theorem.

## 1. Question

A proposed regularizing mechanism was:

> sufficiently large signed triadic transfer must force a strictly positive instantaneous relative phase speed.

A representative form is

[
|dotPhi| ge gamma |T|,qquad gamma>0,
]

with (Phi) a triad collective phase.

This note gives an explicit instantaneous counterexample to any such lower bound based only on single-triad transfer geometry.

## 2. Explicit triad and helical basis

Take

[
k=(1,2,0),qquad p=(-1,0,1),qquad q=(0,-2,-1),
]

so (k+p+q=0), with helicities ((s_k,s_p,s_q)=(+,-,+)).

Use the normalized helical vectors

[
h_k^+=left(rac{2i}{sqrt{10}},-rac{i}{sqrt{10}},rac1{sqrt2}ight),
]

[
h_p^-=left(rac{i}{2},rac1{sqrt2},rac{i}{2}ight),
]

[
h_q^+=left(rac1{sqrt2},-rac{i}{sqrt{10}},rac{2i}{sqrt{10}}ight).
]

They satisfy

[
|h_j|=1,qquad jcdot h_j=0,qquad i,j	imes h_j=s_j|j|h_j.
]

For a real field, impose (widehat u_{-j}=overline{widehat u_j}).

## 3. Full reality-completed cyclic coefficients

Using the Fourier advection convention

[
widehat B_k
=
-iP_ksum_{a+b=k}(bcdot widehat u_a)widehat u_b,
]

the positive-mode equations receive the negative-mode input pairs
((-p,-q)), ((-q,-k)), and ((-k,-p)).

Projecting the full ordered-pair sums onto the corresponding helical directions gives

[
oxed{
C_k=
-rac{7sqrt{10}}{20}-rac25
+irac{sqrt2+sqrt5}{5}
}
]

[
oxed{C_p=0}
]

and

[
oxed{
C_q=
rac25+rac{7sqrt{10}}{20}
-irac{sqrt2+sqrt5}{5}
=-C_k.
}
]

Hence

[
C_k+C_p+C_q=0.
]

Numerically,

[
C_kapprox -1.506797181058933+0.730056307974577,i,
]

and

[
|C_k|=rac{3(8+sqrt{10})}{20}
approx 1.674341649025257.
]

The middle coefficient vanishes because (|k|=|q|=sqrt5) and (s_k=s_q=+1), giving the equal-length/same-helicity cancellation on the (p)-leg.

## 4. Reduced nonlinear amplitude equations

Let

[
A_j=r_j e^{i	heta_j},
qquad
C=C_k,
qquad
Phi=	heta_k+	heta_p+	heta_q.
]

The isolated triad nonlinear terms are

[
dot A_k=C,overline{A_p},overline{A_q},
qquad
dot A_p=0,
qquad
dot A_q=-C,overline{A_k},overline{A_p}.
]

Therefore

[
dot r_k=r_pr_q,Re(Ce^{-iPhi}),
]

[
dot r_q=-r_kr_p,Re(Ce^{-iPhi}),
]

[
dot	heta_k=-rac{r_pr_q}{r_k}Im(Ce^{-iPhi}),
]

[
dot	heta_q=rac{r_kr_p}{r_q}Im(Ce^{-iPhi}),
]

and (dot	heta_p=0). Thus

[
oxed{
dotPhi
=
r_pleft(
rac{r_k}{r_q}-rac{r_q}{r_k}
ight)Im(Ce^{-iPhi}).
}
]

## 5. Instantaneous counterexample

Choose

[
r_k=r_q=R>0,qquad r_p>0.
]

Then

[
oxed{dotPhi=0}
]

for every (Phi).

Now choose

[
Phi=arg C.
]

Then

[
Re(Ce^{-iPhi})=|C|>0,
]

so the nonlinear transfer into the (k)-mode is nonzero and maximal with respect to (Phi).

For the single-positive-mode enstrophy contribution

[
G_k=|k|^2|A_k|^2,
]

the nonlinear derivative is

[
left.rac{dG_k}{dt}ight|_{m NL}
=
2|k|^2 r_k r_p r_qRe(Ce^{-iPhi}).
]

At the chosen state,

[
oxed{
left.rac{dG_k}{dt}ight|_{m NL}
=
10R^2r_p|C|>0,
qquad
dotPhi=0.
}
]

If one counts the conjugate pair (pm k) together, this enstrophy-transfer value doubles. The zero-versus-nonzero obstruction is independent of that normalization convention.

Therefore no universal instantaneous lower bound of the form

[
|dotPhi|ge gamma |T_k|,
qquad gamma>0,
]

can follow solely from single-triad transfer geometry.

## 6. What this does not prove

This is an **instantaneous** obstruction only.

Because nonzero transfer gives

[
dot r_k>0,qquad dot r_q<0
]

at the maximizing state, the equality (r_k=r_q) is immediately lost. The phase lock is therefore not shown to persist for positive time.

Also, the reality-completed six-mode set ({pm k,pm p,pm q}) is not claimed to be invariant under the full Fourier convolution: cross-difference modes can be generated.

Accordingly this result does **not** rule out a network-level or time-integrated phase-mixing mechanism. It only removes the simpler instantaneous single-triad lower-bound route.

## 7. Next analytical target

The remaining question is whether full cross-shell coupling yields a useful time-integrated cancellation estimate, for example a cutoff-uniform control on an aggregate signed transfer or phase-mixing functional.

That is a distinct problem from the instantaneous phase-drift mechanism falsified here.
