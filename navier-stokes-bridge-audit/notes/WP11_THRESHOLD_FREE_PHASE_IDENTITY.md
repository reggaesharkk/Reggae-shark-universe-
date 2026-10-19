# WP11: threshold-free transfer derivative identity

**25 September 2026 — algebraic diagnostic, not a regularity theorem.**

For each ordered high-advector triad, let `z(t)` be the complex transfer in
`src/wp11_phase_rate_audit.py`, and let `ε>0` have the same units as `z`.
Put `d=|z|²+ε²`. Direct complex algebra gives, at every time including `z=0`,

    d Re(z)/dt = [Re(conj(z) z_dot)/d] Re(z)
                 − [Im(conj(z) z_dot)/d] Im(z)
                 + [ε²/d] Re(z_dot).                         (R1)

The terms are respectively a regularized radial term, a regularized angular
term, and an **activation remainder**. At `z=0`, the first two vanish and the
last equals `Re(z_dot)` exactly. No active-set threshold, phase division by
zero, or derivative of moving membership is needed. Summing (R1) over the
fixed finite ordered-triad index set yields the exact derivative of the signed
high-advector transfer.

To verify (R1), set `h=conj(z) z_dot`. The first two numerators combine as
`Re(h) Re(z)−Im(h) Im(z)=|z|² Re(z_dot)`; adding the last numerator gives
`d Re(z_dot)`. For fixed `z≠0`, the remainder tends to zero as `ε→0`, and the
first two terms tend to the ordinary amplitude and angular terms. **No
uniform limit can be inferred at zeros**; for small `|z|` the activation
remainder can remain substantial. In particular (R1) supplies no favorable
sign and no bound on its integral independent of the cutoff.

`python3 src/wp11_regularized_phase_audit.py` evaluates two ε values at
`N=4,7`, `t=0,0.0025`, and checks both the full identity and its exact
zero-triad activation. This is a regression check on finite Galerkin fields.
The open WP11 task remains a cutoff-independent, one-sided estimate on every
time prefix for the *combined signed high-advector transfer*, with an
independently controlled Grönwall coefficient or viscous reserve.
