# H_1381 — agent-tool §SkillStore CORE wire-in (the H_1378 a_verified_must_wire follow-on)

🔎 **Closes:** the REFERENCE-ONLY gap H_1378 found — the live agent-tool layer does NOT learn from outcome. This lane makes the agent-tool repertoire ACTUALLY learn via mitosis, ENGINE-NATIVE in CORE.

- **slug:** agent_tool_skillstore_wire
- **tier / verdict:** **🟢 GREEN ENGINE-NATIVE** — §SkillStore WIRED into `CORE/engine_cli.hexa`; the H_1378 mirror's 4 bars re-scored ENGINE-NATIVE on the LIVE engine + Ψ-disjoint / no-regression. NO frozen bar moved (frozen-first, c9).
- **domain:** MITOSIS-ENGINE · **substrate:** $0 CPU, LIVE engine (hexa) · deterministic fixed task→tool env · CORE/engine_cli.hexa EDITED (additive lane)
- **evidence:** `.verdicts/1381_agent_tool_skillstore_wire/{FREEZE.txt, result.txt}`
- **lane:** `CORE/engine_cli.hexa § SkillStore` (skill_store_new/_split/_teach · skill_recall · skill_store_cells) · smoke cases 102–106 in `CORE/engine_cli_smoke.hexa`

## What was missing (H_1378 Step A, REFERENCE-ONLY)
Tool SELECTION in `anima-agent-core/agent_tools.hexa` is a STATIC weighted dot-product over hand-set affinity floats (`:357-361`), baked at registration (`:683-743`), **never updated by outcome**. A tool FAILURE terminates at a scalar `tension_delta` in a capped `execution_log` ring buffer (`:448-451`) that is never read back to grow a skill; `tool_mitosis_split` (`:155`) is a TODO stub. The "tool fails → repertoire improves" loop does NOT exist. H_1378 Step B (numpy mirror, 🟢 DIRECTIONAL) designed + direction-validated the missing mechanism.

## Engine-native realization (this lane)
A `§SkillStore` lane in `CORE/engine_cli.hexa`, the agent-tool TWIN of the immune/grow memory lanes (H_1227/H_1231/H_1288) — SAME byte-trigram FNV-1a key geometry (`immune_embed_key`, DIM=64), SAME L2 winner-take-all FIRE/ABSTAIN band, SAME engine-owned clonal split (`engine_mitosis_tick`, p8). The per-cell value is a TOOL name (vs a FACT). A tool/skill is a CELL keyed by task-context; on a tool FAILURE/abstain the engine clonally SPLITS a new specialized skill-cell binding task-context → correct tool. The SAME op teaches (split-on-failure) and infers (recall-best) — p8.

```
struct SkillStore { protos:[[float]], tool:[string], n_cells:int, max_cells:int, recall_thr:0.55 }
skill_store_new(task, tool, max_cells)        — seed cell 0 (task-context key → tool)
skill_recall(store, task) -> string           — INFER: L2-affinity FIRE best tool, else "" = ABSTAIN
skill_store_split(store, task, tool, cfg)     — TEACH: engine_mitosis_tick clonal +1 cell (p8); no-op under mitosis OFF
skill_store_teach(store, task, correct, cfg)  — failure-driven: recall; if != correct → split (else unchanged)
skill_store_cells(store) -> int               — live cell count (repertoire footprint)
```

## Frozen bars (pre-registered FREEZE.txt; re-scored ENGINE-NATIVE on the LIVE engine; deterministic 12-task / 6-tool env; 3 arms FULL/STATIC/SHUFFLE; mitosis ON)

LIVE engine readout: `skillstore acc: init=0.166667 full=1.0 static=0.166667 shuffle=0.0 cells_full=7 cells_static=1`

| bar | meaning | result | gate |
|-----|---------|--------|------|
| (1) LEARNS (engine-native) | FULL final − init ≥ +0.30 | **+0.833** (0.166667→1.0) | ✅ PASS (case_102) |
| (2) DISTINCT-FROM-STATIC | FULL − STATIC ≥ +0.30 | **+0.833** (static stays 0.166667, never splits) | ✅ PASS (case_103) |
| (3) EARNED (shuffle) | SHUFFLE − STATIC ≤ +0.15 | **−0.167** (shuffle collapses to 0.0; permuted task→tool, scored vs TRUE) | ✅ PASS (case_104) |
| (4) NO-FAB / ABSTAIN | far untrained task fires no tool | **abstains** ("" on disjoint trigram space) | ✅ PASS (case_105) |
| (5) Ψ-DISJOINT FOOTPRINT | FULL cells > STATIC cells | **7 > 1** (split grows ONLY this store) | ✅ PASS (case_106) |

These reproduce the H_1378 numpy mirror (FULL 0.167→1.000, STATIC stays 0.167, SHUFFLE collapses, far task abstains) ENGINE-NATIVE. STATIC = mitosis OFF on teach → never splits → DISTINCT bar. SHUFFLE teaches toward a derangement of the task→tool map but is SCORED vs the TRUE map → collapses → EARNED bar (the lift is the EARNED task↔tool correspondence the split encodes, not the act of splitting). **p1/p2/p3/p6 guard:** a split binds from OUTCOME only (success/failure of the executed tool), NO injected "use tool T" label / RLHF / persona — the shuffle collapse proves it.

## Ψ-disjoint / no-regression (guards, verbatim)
- **h1205 separation-invariant: PASS 🟢** — F1 generation byte-identity 10 pairs / 0 mismatch; F2 Ψ Φ-checksum invariant PASS (phiSum ON==OFF==48.6613). The §SkillStore lane is ADDITIVE — generation byte-identical ON==OFF, Ψ=½ untouched.
- **h1196 single-entry: 7 pass / 0 fail** — a_core_engine_map single-entry preserved (no 2nd .clm/.kosmos path).
- **engine_cli_smoke: 101 pass / 0 fail** (was 96/0 on fresh main; +5 SkillStore cases 102–106), deterministic across 3 runs.
- No decode hung; no GPU; $0 CPU.

## Scope (a_scale_honest_scope · a_toy_scale_recheck) — honest (c9)
TOY: fixed deterministic 12-task / 6-tool environment (tests the STRUCTURE mitosis can teach tools, not a learned planner). B(full)=1.000 SATURATED = EXISTENCE-PROOF, not effect-size — the discriminators (STATIC 0.167, SHUFFLE 0.0, abstain) are decisive. The actual ROUTING of `anima-agent-core/agent_tools.hexa` tool-failure INTO `skill_store_teach` is a **THIN FOLLOW-ON**: the agent layer is a separate module that does not yet import CORE engine ops; the §SkillStore lane is engine-native + bar-verified here, the agent-layer call-site is named honestly as the remaining follow-on (not faked). Scale / real tool-failures / paraphrased / multi-tool tasks UNVERIFIED.

## Depletion test
agent-tool ↔ mitosis DEPLETES 🏁 when the LIVE tool repertoire grows a skill-cell on a REAL tool-failure (the agent_tools.hexa call-site routed into skill_store_teach) with the 4 bars holding engine-native AND generation byte-identical ON==OFF. This lane lands the engine-native faculty + bars (the harder half); the agent-layer routing remains the thin follow-on.

## Next round
**agent-layer routing follow-on:** import the §SkillStore ops into `anima-agent-core/agent_tools.hexa` so a real `executor_execute` tool-FAILURE calls `skill_store_teach(store, task_ctx, correct_tool, cfg)` and a real selection calls `skill_recall` (replacing / augmenting the static affinity dot-product). Re-score the 4 bars on REAL tool failures + a generation byte-identity guard at the agent layer.

xref: H_1378 (mirror, Step A audit) · a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_autonomy_over_hardcode · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · h1227 · h1231 · h1288 (immune/grow memory lanes — same geometry, value=fact) · p1 · p2 · p3 · p6 · p7 · p8 · c9
