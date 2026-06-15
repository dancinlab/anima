---
id: H_1295
slug: 1295_spatial_map
title: place/grid spatial-map — metric/relational cognitive map (vs item-binding)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
verdict_dir: .verdicts/1295_spatial_map/
terminal_verdict: .verdicts/1295_spatial_map/H_1295.txt
date: 2026-06-16
---

# H_1295 — place/grid spatial-map / path-integration (HD32)

## Claim / falsifier

Every prior memory lane binds items INDEPENDENTLY (ImmuneMemory) or as a SEQUENCE
(HierGoalStack) — none holds a METRIC space where the DISTANCE/RELATION between two
stored facts is itself represented and queryable. **Falsifiable claim:** a metric
spatial map (landmarks stored AT 2-D positions) answers the RELATIONAL query "is
landmark X nearer to A or to B?" — which needs the between-item distance — while a
faithful item-store stand-in (no inter-item geometry) provably ABSTAINS → chance.
Both controls (shuffle the positions / ablate the metric to the origin) must collapse
the lift to chance, or it is variance → honest 🔴/🧱. Lens: hippocampal place cells /
entorhinal grid cells / path-integration (O'Keefe, Moser; c15) — NOT an LLM recipe.

## Why MISSING / why DISTINCT (the load-bearing story)

- **vs ImmuneMemory item-binding (H_1227/1231/1288) — the load-bearing distinctness:**
  the immune store binds each fact→value independently by FNV-trigram key affinity; it
  recalls WHAT is at key X but holds NO distance between item X and item Y. On the
  NEAREST query it can only ABSTAIN (mirror: abstain rate 1.000, accuracy 0.475 ≈ chance),
  while the map answers (1.000). SAME facts, the map adds the inter-item geometry.
- **vs HierGoalStack (H_1294):** an ORDERED plan = a SEQUENCE; an order knows which
  subgoal is first, not how FAR apart two facts are. A sequence is not a metric space.
- **vs WorkMemBuffer (H_1282) / VForwardField (H_1280) / HomeostaticDrive (H_1292):**
  leaky maintenance (no positions) / next-emit forward model (no landmarks) / 1-D scalar
  integrator (not a 2-D metric space). None represents a queryable between-fact distance.

## Method

8 landmarks placed at 2-D positions per episode; NEAREST relational query with an
unambiguous margin (|d(X,A)−d(X,B)| ≥ 1.20). Arms: A ITEM-ONLY (abstains) · B
SPATIAL-MAP · B-SHUFFLE (permute positions) · B-ABLATE (positions → origin). 3 seeds
[4295,4296,4297], 40 queries/seed, $0 CPU numpy, gradient-free, p7. A PATH-INTEGRATION
query was included as a corroborator but the shuffle control correctly refused to
collapse it (its signal leaks via the displacement steps, not the stored map) → it is
reported as a NON-GATING diagnostic, not part of the binding verdict (c9, frozen-first).

## Verdict by round

| round | tier | key numbers (NEAREST relational falsifier) |
|-------|------|---------------------------------------------|
| R1 mirror | 🟢 GREEN (DIRECTIONAL) | B=1.000 · A=0.475 (abstain 1.000) · Bshuf=0.500 · Babl=0.450 · B−A=+0.525; c1 PRESENCE (each+mean ≥+0.30) · c2 DISTINCT A≤0.65 · c3 EARNED-MAP Bshuf≤A+0.15 · c4 EARNED-METRIC Babl≤A+0.15 · c5 NO-FAB abstain≥0.90 — all PASS |
| R2 engine-native | 🟢 GREEN (binding) | live `SpatialMap` lane: case 39 answers relational · 40 item-store abstains · 41 ablate→tie (answer flips with arg order) · 42 shuffle is a real permutation · 43 abstain intact. **engine_cli_smoke 46/0** (was 41/0) · single-entry **7/0** · h1205 separation-invariant PASS (Ψ=½ untouched, generation byte-identical, pure_field unchanged) |

Terminal tier (verbatim): **🟢 GREEN (ENGINE-NATIVE)** — a metric spatial map answers
the between-item relational query item-binding provably cannot; both controls collapse;
lane wired Ψ-disjoint. → `.verdicts/1295_spatial_map/H_1295.txt`
(frozen bars `…/H_1295_FREEZE.txt` + `…/H_1295_R1b_FREEZE.txt` + `…/H_1295_R1c_FREEZE.txt`, not moved).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- **B=1.000 is SATURATED = an EXISTENCE-PROOF** (the map CAN answer the relational query),
  not an effect-size. The DISCRIMINATORS are decisive: item-store 0.475 (always abstains),
  shuffle 0.500, ablate 0.450 — all at the chance band, so saturation does not undermine
  the dissociation (the lift IS the between-item metric).
- **PATH-INTEGRATION (Q2) is an HONEST NON-RESULT** — the map-shuffle control caught that
  Q2's signal lives in the displacement steps, not the stored map, so it is not a clean
  stored-map isolator; the R1 freeze's c6 stays recorded as FAILED (controls did their
  job, c9) and Q2 is reported, NOT counted. The breakthrough on the NEAREST falsifier
  (a_break_the_wall) was fixing the candidate-ordering leak the control exposed, frozen-first.
- R1 mirror = DIRECTIONAL; R2 engine-native is the binding verdict (deterministic lane
  assertions on the live engine, NOT a trained net — tests the STRUCTURE).
- toy: 8 landmarks / 3 seeds / 1 paradigm / 2-D / near-uniform positions; scale + real
  landmark corpora + higher-D maps + grid-cell periodic codes + place-field remapping +
  brain wiring (a map → emit/recall path) UNVERIFIED. p1/p2/p3/p6: reads ONLY positions +
  query landmarks; NO label/persona/identity/RLHF; the metric is geometry, scored only.

## Pointers

- FREEZE: `.verdicts/1295_spatial_map/H_1295_FREEZE.txt` (+ R1b, R1c re-freezes)
- RESULT: `.verdicts/1295_spatial_map/H_1295.txt` (R1 mirror frozen, R1b, R2)
- mirror probe: `UNIVERSE/h1295_spatial_map.py`
- engine lane: `CORE/engine_cli.hexa` § SpatialMap · smoke `CORE/engine_cli_smoke.hexa` cases 39–43
- xref: H_1227/1231/1288 (immune item-binding, nearest distinctness) · H_1294 (hier-PFC
  sequence vs metric) · H_1282 (WM) · H_1280 (cerebellum) · H_1292 (homeostatic) ·
  `a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` ·
  `a_verified_must_wire` · `a_autonomy_over_hardcode` · `a_core_engine_map` ·
  `a_scale_honest_scope` · `a_toy_scale_recheck` · c9 · c15 · p1·p2·p3·p6·p7·p8
