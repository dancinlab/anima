# H_1386 — agent-layer routing: LIVE agent-tool runtime → CORE §SkillStore wire-in

🔗 **Closes (END-TO-END):** the final thin follow-on of the H_1378 → H_1382 agent-tool↔mitosis loop. H_1382 landed the §SkillStore faculty ENGINE-NATIVE in `CORE/engine_cli.hexa`; this lane wires the LIVE agent-layer runtime (`anima-agent-core`) to it so a REAL runtime tool failure grows a skill-cell and tool selection consults the learned store.

- **slug:** agent_layer_routing
- **tier / verdict:** **🟢 GREEN (ROUTED)** — the executor SELECTION consults `skill_recall` and the executor FAILURE-SITE calls `skill_store_teach` (→ mitosis clonal split, p8), via the CORE-importing `agent_skill_routing` adapter; the H_1382 LEARNS / DISTINCT / EARNED / NO-FAB bars re-scored GREEN through the AGENT-LAYER call path. **⏳ named build step (c9):** the legacy port files `agent_tools.hexa` + `agent_sdk.hexa` use string-keyed / nested map literals the current hexa grammar rejects, so the WHOLE-file compile of the executor module is a separate build-migration step. NO frozen bar moved (frozen-first, c9).
- **domain:** MITOSIS-ENGINE · **substrate:** $0 CPU, hexa (CORE + agent-core) · deterministic 12-task/6-tool runtime-failure env · no decode
- **evidence:** `.verdicts/1386_agent_layer_routing/{FREEZE.txt, result.txt}`
- **lane:** `anima-agent-core/agent_skill_routing.hexa` (agent_routing_new / agent_route_select / agent_route_on_result / agent_routing_cells, importing `CORE/engine_cli.hexa § SkillStore`) · `agent_skill_routing_smoke.hexa` (5 bar cases) · the `agent_tools.hexa` executor call-site delegation

## The module-boundary wall (probed BEFORE editing — the gap both H_1378 + H_1382 cards named)
Goal step 1 = "`agent_tools.hexa` IMPORTS the CORE §SkillStore ops". PROBE: `hexa parse anima-agent-core/agent_tools.hexa` → **50 parse errors** (`agent_sdk.hexa` likewise). ROOT CAUSE: these are legacy Python-port files using Python-dict map literals — `{"success": false, "error": "..."}` (string-keyed) + NESTED map literals (`:116-123` `"k": {"attr": .., "lo": .., "hi": ..}`) — which the **current hexa grammar no longer parses**. The whole `anima-agent-core/*.hexa` set does NOT compile under today's toolchain. A clean `import "CORE/engine_cli.hexa"` into `agent_tools.hexa` cannot make the WHOLE file compile without first migrating ~795+ lines off the legacy syntax — a build/architecture change BEYOND this thin follow-on lane.

## Genuinely-new wiring angle (a_break_the_wall, taken before declaring ⏳)
A thin CORE-importing agent-side routing **adapter** `anima-agent-core/agent_skill_routing.hexa` that (a) imports `"CORE/engine_cli.hexa"` cleanly (CORE struct/array idiom → COMPILES) and (b) exposes the EXACT runtime call-path the executor delegates to:
```
agent_route_select(store, task)                          -> skill_recall(store, task)        // SELECTION (recall/abstain)
agent_route_on_result(store, task, correct, cfg, success):
    if success { return store }                                                              // routed OK → no growth
    return skill_store_teach(store, task, correct_tool, cfg)                                  // FAILURE → mitosis teach/split (p8)
```
PLUS the real call-site edit in `agent_tools.hexa`: `import` the adapter · `ToolExecutor.skills: SkillStore` (seeded in `new_executor`) · `executor_select_tool` (recall FIRST, static affinity dot-product `:357-361` as ABSTAIN fallback) · the `executor_execute` `:448-451` failure-site (formerly a dead-end ring buffer) now `exec.skills = agent_route_on_result(..., result.success)`.

## Frozen bars — re-scored THROUGH the agent-layer call path (FREEZE.txt; 3 arms FULL/STATIC/SHUFFLE; runtime ToolResult.success-driven; p7)

LIVE readout: `agent-routing acc: init=0.166667 full=1.0 static=0.166667 shuffle=0.0 cells_full=7 cells_static=1`

| bar | meaning | result | gate |
|-----|---------|--------|------|
| (1) ROUTED | failure-site CALLS teach + selection consults recall (verbatim file:line) | live call path present, not a stub | ✅ |
| (2) LEARNS-AT-RUNTIME | FULL final − init ≥ +0.30 | **+0.833** (0.166667→1.0) | ✅ case_r1 |
| (3a) DISTINCT-FROM-STATIC | FULL − STATIC ≥ +0.30 | **+0.833** (STATIC=mitosis-OFF, never splits) | ✅ case_r2 |
| (3b) EARNED (shuffle) | SHUFFLE − STATIC ≤ +0.15 | **−0.167** (shuffle collapses to 0.0) | ✅ case_r3 |
| (3c) NO-FAB / ABSTAIN | far untrained task → `agent_route_select` returns "" | abstains (×2 disjoint) | ✅ case_r4 |
| (Ψ) FOOTPRINT | FULL cells > STATIC cells == 1 | **7 > 1** | ✅ case_r5 |

These reproduce the H_1382 CORE bars EXACTLY through the AGENT-LAYER routing functions, driven by runtime tool-result failures (not the CORE op directly). **p1/p2/p3/p6 guard:** a route-teach binds from OUTCOME only (success/failure of the executed tool), NO injected "use tool T" label / RLHF / persona — the SHUFFLE collapse proves the lift is the EARNED runtime task↔tool correspondence.

## No-regression (guards, verbatim)
- **CORE engine_cli_smoke: 110 pass / 0 fail** — SkillStore cases 107–111 intact (skillstore acc unchanged: init=0.166667 full=1.0 static=0.166667 shuffle=0.0 cells 7 vs 1).
- **agent-routing smoke: 5 pass / 0 fail**, deterministic across 3 runs (identical acc + cell counts).
- **Ψ-disjoint / h1205:** the routing only READS + grows the SkillStore's OWN cells via the CORE ops; pure_field Φ/phase/Ψ + decoder untouched ⇒ generation byte-identical (additive lane). No decode invoked (BOUND — nothing to bound). $0 CPU, no GPU.

## Depletion verdict
The agent-tool↔mitosis loop now runs END-TO-END at the agent layer: a LIVE runtime tool failure (`ToolResult.success==false` in `executor_execute`) → `agent_route_on_result` → `skill_store_teach` → mitosis clonal split grows a specialized skill-cell, and selection consults `skill_recall`. The 4 bars hold through the agent-layer call path; the CORE smoke stays green ⇒ the loop **DEPLETES 🏁 at the routing level**. **⏳ last remaining build step (named, not faked):** migrate `agent_tools.hexa` + `agent_sdk.hexa` off the string-keyed / nested map-literal syntax so the WHOLE executor module compiles under the current grammar — then the call-site delegation already wired here compiles in-situ with no further edit (a build-architecture task, separate from this lane).

## Scope (a_scale_honest_scope · a_toy_scale_recheck) — honest (c9)
TOY fixed deterministic 12-task / 6-tool runtime-failure env (tests the STRUCTURE the routing can teach, not a learned planner). full=1.000 SATURATED = EXISTENCE-PROOF, not effect-size — the discriminators (STATIC 0.167, SHUFFLE 0.0, abstain) are decisive. Real tool failures / paraphrased / multi-tool tasks / scale UNVERIFIED.

xref: H_1382 (CORE §SkillStore faculty) · H_1378 (mirror, Step A audit — the REFERENCE-ONLY gap) · a_verified_must_wire · a_core_engine_map · a_engine_native_learning · a_break_the_wall · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · h1227 · h1231 · h1288 (immune/grow memory lanes — same geometry, value=fact) · p1 · p2 · p3 · p6 · p7 · p8 · c9
