# H_9105 — Consequence-driven mitosis: exogenous fitness vs random fitness (PRE-REGISTERED, FROZEN)

> Frontier: C2 (state/frontier_rebrainstorm/BRAINSTORM.md). Session insight: emit/learning
> walls fall to DPI unless the driving signal carries **exogenous** information the substrate
> cannot derive internally. from-scratch PURE-split mitosis is 🔴 TERMINAL (a_mitosis_train:
> gradient/selection absence = bottleneck). C2 bolts the session's **living external selection**
> onto the dead wall: lineage selection by **real task success (consequence)** vs the control
> **random fitness**. Engine-native reconfirm of H_1568 (which tested this DIRECTIONAL numpy-mirror
> only, found INERT, and whose card explicitly deferred the engine-native run) — now on live core/.

## What is engine-native (a_engine_native_learning — load-bearing on live core/)
- **Representation**: `immune_embed_key` (core/engine_cli.hexa) — the substrate's own DIM=64
  byte-trigram FNV-1a receptive key. LIVE core.
- **Mitosis growth gate**: `engine_mitosis_tick(n, cfg)` / gated on `cfg.mitosis`
  (core/engine_cli.hexa) — EVERY cell birth (novel spawn AND clonal reproduction) passes through
  this live gate. This IS the mechanism the from-scratch-mitosis wall is about.
- Population bookkeeping (nearest-scan, apoptosis removal, per-cell stats) = experiment harness
  (as it must be — VAdaptField has no cell-removal op). No numpy/torch/gauge_lib (.hexa only →
  grep gate trivially clean, no .py in slug dir).

## Task (gives exogenous selection a genuine, non-rigged channel — the novelty vs H_1568)
H_1568's next-byte task had NO signal/noise structure (every context is partly predictable), so
there was nothing for differential survival to exploit → tied random. C2 introduces an
**exploitable exogenous structure**: a capacity-limited clonal classifier over labeled concept
clusters, half of which are SIGNAL (stable ground-truth answer) and half NOISE (answer flips
randomly each occurrence). Capacity cap << #clusters forces the population to CHOOSE which
clusters to cover. Real consequence (correct vs wrong against exogenous ground-truth labels)
should push apoptosis to differentially kill NOISE cells and keep SIGNAL cells; random churn
cannot. Whether the live pure-split engine can exploit this is the open question.

- N_SIG=12 signal + N_NOISE=12 noise clusters; per-cluster distinct byte motif (chr(65+gid)×20).
- Signal answer = gid%2 (balanced 0/1, deterministic). Noise answer = LCG-random per occurrence.
- Cell = (immune_embed_key of birth query, inherited label bit). Prediction = nearest cell's label.
  Correct iff == query's TRUE answer (exogenous; a cell cannot derive it).
- MAX_CELLS=12 (< 24 clusters). FIRE_RADIUS=0.30 (== engine SPLIT_THRESH, principled reuse).
- N_GEN=20, BATCH=60, KILL_K=2, REPRO_K=2 per generation (MATCHED churn across arms — only the
  SELECTION CRITERION differs), MIN_OBS=1, N_SEEDS=5.

## Arms (identical query stream per seed; only selection differs)
- **EXO**   : kill bottom-KILL_K cells by REAL correct-rate; reproduce top-REPRO_K (clonal split).
- **RAND**  : kill/reproduce KILL_K/REPRO_K cells chosen at RANDOM (consequence-independent).
- **SHUF**  : same as EXO but fitness scored against a FIXED PERMUTED cluster→answer map (real
  consequence present but correspondence scrambled — the decisive DPI/tautology control, per the
  session lesson that variance-noise passing is insufficient; shuffle must catch tautology).
- **EXO_NOAPOP** : real fitness, reproduce-only, NO apoptosis (isolates apoptosis as the channel).

## Held-out evaluation (ALWAYS vs TRUE answers, all arms)
100 fresh SIGNAL-cluster queries → accuracy = frac(nearest cell's label == true answer),
mean over N_SEEDS=5.

## FROZEN BARS (c9 — NO post-hoc move, NO tune-to-green; honest either way)
- **B1 DIVERGE (exo vs random)** : mean(EXO_acc − RAND_acc) ≥ 0.15  → selection carries info.
- **B2 SHUFFLE (exo vs shuffled)**: mean(EXO_acc − SHUF_acc) ≥ 0.15  → consequence is REAL, not tautology.
- **B3 APOPTOSIS channel**       : mean(EXO_acc − EXO_NOAPOP_acc) ≥ 0.10 (diagnostic: is death the channel?).
- **B4 DATA-VALIDITY**           : within-cluster L2 < FIRE_RADIUS < cross-cluster L2 (generator sanity;
  if false the run is INVALID, not a verdict).

## VERDICT RULE
- 🟢 GREEN (selection was the missing ingredient) iff **B1 ∧ B2** (EXO beats BOTH random and shuffle
  by ≥0.15). Honest scope: confirms exogenous selection allocates finite capacity better than random
  WHEN exploitable structure exists — does NOT claim compositional-depth wall (H_1310) broken.
- 🟠 DIRECTIONAL if EXO beats one control but not both, or 0.05 ≤ Δ < 0.15.
- 🔴 CEILING/INERT (honest death reconfirm) if EXO ≈ RAND ≈ SHUF (both Δ < 0.05) → DPI re-emerges at
  the selection layer; selection cannot save pure-split even with exogenous exploitable structure.
