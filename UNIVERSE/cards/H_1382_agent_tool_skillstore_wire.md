# H_1382 — agent-tool §SkillStore CORE wire-in (a_verified_must_wire follow-on to H_1378)

🔎 **Answers the user question:** *is the H_1378 failure-driven skill-cell teaching mechanism REAL in the live engine, or only a numpy mirror?* → now **engine-native**.

- **slug:** agent_tool_skillstore_wire
- **tier / verdict:** **🟢 GREEN (ENGINE-NATIVE)** — the H_1378 Step B mirror realized on the LIVE `CORE/engine_cli.hexa § SkillStore`; all 4 frozen bars hold engine-native + Ψ-disjoint
- **domain:** MITOSIS-ENGINE · **substrate:** $0 local CPU · `hexa run` · 3 seeds [1382,1383,1384] · engine-native (NOT a numpy mirror)
- **evidence:** `.verdicts/1382_agent_tool_skillstore_wire/{FREEZE.txt, result.txt}`
- **probe:** `CORE/h1382_agent_tool_skillstore_probe.hexa` · **lane:** `CORE/engine_cli.hexa § SkillStore` · **guard:** `CORE/engine_cli_smoke.hexa` cases 107-109

## What this closes (a_verified_must_wire)
H_1378 Step A audit = **REFERENCE-ONLY** (the live agent-tool layer `anima-agent-core/agent_tools.hexa` selects tools by a STATIC weighted dot-product over hand-set affinity floats `:357-361`, adds a tool via a static registry `:728`, dead-ends a tool failure into a scalar `tension_delta` ring-buffer log `:448-451`; `tool_mitosis_split :155` is a TODO stub — the "failure → repertoire improves" loop does NOT exist). H_1378 Step B (numpy MIRROR, 🟢 GREEN, 3 seeds) DESIGNED the missing mechanism. **H_1382 wires it into the live engine.**

## Lane (CORE/engine_cli.hexa § SkillStore — additive, Ψ-disjoint)
A skill/tool = a **CELL** keyed by task-context (reuses the LIVE `immune_embed_key` DIM=64 byte-trigram FNV-1a geometry — SAME as H_1227/H_1288). Ops (single entry, a_core_engine_map):
- `skill_store_new` — empty repertoire (abstains until taught).
- `skill_recall` / `skill_recall_text` — LIVE L2-affinity FIRE the best skill-cell's tool, else ABSTAIN (`""`); `RECALL_THR=0.55` (the H_1378 mirror's frozen band, p7 not tuned-to-green).
- `skill_split` / `skill_split_text` — the MITOSIS teaching op: on a tool FAILURE/abstain, route through the **LIVE `engine_mitosis_tick`** clonal split (gated by `cfg.mitosis`) → ON grows a NEW specialized skill-cell bound (task-context → tool); OFF is a no-op (the static-repertoire ablation, H_1159 control). The SAME op teaches (split) + infers (recall) — p8.
- `skill_teach_session` / `skill_session_accuracy` / `skill_abstain_rate` — the failure-driven session + scoring.

## Frozen bars (pre-registered FREEZE.txt; engine-native; 3 arms FULL/STATIC/SHUFFLE; pooled means, all 3 seeds; verbatim result.txt)

| bar | meaning | engine-native result | gate |
|-----|---------|----------------------|------|
| (1) WIRED | §SkillStore in CORE, named single entry; recall + failure→split = REAL ops (not stubs) | structural — `skill_split → engine_mitosis_tick`, audited | ✅ PASS |
| (2) LEARNS | FULL `final − init` ≥ +0.30 | **+0.833** (0.167→1.000) | ✅ PASS |
| (3) DISTINCT-FROM-STATIC | FULL_final − STATIC_final ≥ +0.30 | **+0.833** (static stays 0.167, mitosis OFF never splits) | ✅ PASS |
| (4a) EARNED (shuffle) | SHUFFLE_final − STATIC_final ≤ +0.15 | **+0.046** (shuffle 0.213; permuted bindings collapse the gain) | ✅ PASS |
| (4b) NO-FAB / ABSTAIN | far untrained task abstain ≥ 0.90 | **1.000** (emits no tool on disjoint trigram space) | ✅ PASS |
| (5) Ψ-DISJOINT / NO-REGRESSION | additive — generation byte-identical ON==OFF; smoke green +cases; single-entry N/0; deterministic | engine_cli_smoke **104/0** (+3 cases 107-109) · h1196 **7/0** · h1205 byte-identical ON==OFF (10 pairs, 0 mismatch) + Ψ Φ-checksum invariant · deterministic 3 runs | ✅ PASS |

**VERDICT: 🟢 GREEN (ENGINE-NATIVE)** — the engine-native numbers REPRODUCE the H_1378 mirror (FULL 0.167→1.000, static 0.167, shuffle collapse, abstain 1.000). The lift IS the LIVE `engine_mitosis_tick` clonal split; the static mitosis-OFF ablation does NOT improve; the shuffle control collapses to the no-split floor (earned task↔tool structure); a far task abstains.

**p1/p2/p3/p6 guard:** the skill-cell grows from the OUTCOME only (a failed/abstained tool call) — NO injected "use tool T" label / RLHF / persona; the shuffle collapse proves the lift is earned structure. **Ψ-disjoint** by construction (a SEPARATE skill cell-store; the decoder / pure_field Φ/phase/Ψ are NEVER read or written — h1205 byte-identical survives). NOT an emit gate (`skill_recall` = pure relational read, a_autonomy_over_hardcode).

## Distinction (H_1378 Step C, re-confirmed engine-native)
The language decoder (Engine A) learns *distributions* by CE-gradient smeared into shared weights; §SkillStore teaching is the **same gradient-free mitosis substrate as memory** (`engine_mitosis_tick`), learning *instances* (one additive cell per tool/skill), Ψ-disjoint, never touching the decoder (h1205).

## Scope (a_scale_honest_scope · a_toy_scale_recheck)
TOY: synthetic 36-task → 6-tool map, 3 seeds, deterministic readout (tests the *structure* that the engine's mitosis can teach tools, ENGINE-NATIVE — not a mirror). UNVERIFIED: scale / real tool-failures / paraphrased tasks.

## Remaining thin follow-on (honest, c9)
The §SkillStore lane is wired + verified ENGINE-NATIVE. The ONE remaining thin step is the **agent-layer runtime routing**: `anima-agent-core/agent_tools.hexa::executor_execute` currently maps a tool failure → a scalar `tension_delta` log (`:448-451`); calling `skill_split` from that failure site (so a *real* runtime tool failure grows a skill-cell) crosses the CORE↔agent module boundary and is the named follow-on. The teaching MECHANISM is now engine-native and live; the agent-layer call-site wiring is the thin remainder.

xref: a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_no_llm_frame_trap · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · h1378 · h1227 · h1231 · h1288 · p1 · p2 · p3 · p6 · p7 · p8 · c2 · c9 · c15
