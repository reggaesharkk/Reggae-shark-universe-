# WP19 v0.2 — Evidence Inventory and Bridge Compatibility Map

## What was found

The old WP16 cutoff program really does continue through N17.

### Track A — prospective phase/K36 cutoff program

- N14: completed prospective K36 time gate; all three states passed the frozen six-check gate. First sampled mass exit: 0.0023 in all three states.
- N15: completed 520-proposal continuation; all three frozen checks passed. First sampled mass exit: 0.0023 in all three states.
- N16: completed 520-proposal continuation; broad gate passed. Inherited and target-only exit at 0.0023; full-final exits at 0.0024. The full-final [0.00230,0.00235] sampling bracket is descriptive, not an interval proof.
- N17: completed 520-proposal continuation. Broad gate passed at 0.0024 for all three states. The separately frozen mechanism gate failed or became unevaluable at a directional-split assertion, and later post-hoc inspection found substantive prediction misses. The failure is retained.

### Track B — rigorous same-datum Arb certificate program

This is a different experiment.

The fixed 112-pair rational witness is zero-padded without retuning and currently has whole-segment Arb sign-crossing certificates at:

- N11
- N12
- N13

These certificates use the same rational datum, viscosity, endpoint, K36 keys, and observable.

### Why the tracks must not be merged casually

The N14-N17 phase/time-gate states are optimizer-derived finite states from the older WP16 program. They are not the same zero-padded 112-pair rational witness used in the later N11-N13 Arb certificate family.

Therefore an N14-N17 time-gate pass cannot be relabeled as an N14-N17 same-datum Arb sign certificate.

## What the old N14-N17 data are useful for

They are valuable as:

1. mechanism/discovery evidence;
2. finite-cutoff stress tests;
3. evidence that the K36 broad transient pattern continued prospectively through N17;
4. a source of counterexamples to over-simple mechanism stories, especially the N17 mechanism miss;
5. target cutoffs for a future extension of the same-datum rigorous family.

They are **not** direct proof inputs to the new consecutive-cutoff inequality unless we deliberately define and freeze a separate bridge experiment on those optimizer states.

## WP19 bridge strategy after inventory

The correct proof-first order is:

### Phase 1 — retrospective validation on certified same-datum data

Run the lower-cutoff-only shell forcing bound on:

- N11 -> N12
- N12 -> N13

The higher-cutoff trajectory may be used only after the bound is produced, for validation of sharpness.

### Phase 2 — extend same-datum family

Only after Phase 1 works, build the same rational-witness certificate at N14.

Do not substitute the older N14 optimizer state.

### Phase 3 — use historical N14-N17 program as a stress map

The old sequence suggests the broad K36 timing is not perfectly rigid:
- N14: 0.0023
- N15: 0.0023
- N16 full-final: 0.0024
- N17: 0.0024

So any continuum claim must be based on a robust sign/energy estimate, not an exact crossing-time pattern.

The N17 mechanism failure also argues against freezing a simple orbit/normalizer story as the tail mechanism.

## Most important consequence

We do **not** need to rediscover N14-N17.

We need to convert what was already learned there into constraints on the next theorem attempt, while keeping the rigorous same-datum chain logically separate.

The next decisive computational target remains the lower-cutoff shell forcing

    h_N(t) = ||(Pi_{N+1}-Pi_N) B(u_N,u_N)||_2

for the N11 and N12 certified trajectories.
