# WP16 Phase-Velocity Source Compression Gate

Using the already-executed exact RHS source decomposition, rank ordered source-orbit groups in the q and k phase-velocity channels by absolute contribution.

For each state and channel, report the smallest number of source groups required to recover 50%, 75%, 90%, 95%, and 99% of total absolute source contribution.

Also report the signed cancellation ratio

[
rac{|sum_j c_j|}{sum_j |c_j|}
]

and persistent top-10 source groups across multiple cutoff steps.

The purpose is to distinguish a genuinely sparse single-source mechanism from a broad cancellation network.

No new PDE simulation is required. Finite instantaneous diagnostic only.
