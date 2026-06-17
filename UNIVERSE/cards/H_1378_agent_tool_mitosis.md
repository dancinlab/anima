# H_1378 — agent-tool ↔ mitosis teaching (REFERENCE-ONLY wiring → mirror-GREEN teaching mechanism)

🔎 **Answers the user question:** *how is the AGENT TOOL taught via mitosis, does it learn, and how does it differ from the language decoder?*

- **slug:** agent_tool_mitosis
- **tier / verdict:** Step A = **REFERENCE-ONLY** (agent-tool layer does NOT learn via mitosis today) · Step B = **🟢 GREEN (numpy MIRROR, DIRECTIONAL — engine-transfer UNVERIFIED)** designs+validates the missing mechanism
- **wired:** **engine-native (twin-confirm)** — re-confirmed 2026-06-17 (aiden): the Step-B designed skill-cell SPLIT mechanism is realized engine-native as its TWIN **H_1382 §SkillStore**; `CORE/engine_cli_smoke.hexa` cases 107–111 PASS (init=0.167 full=1.0 static=0.167 shuffle=0.0): LEARNS/DISTINCT-FROM-STATIC/EARNED(shuffle→0.0)/NO-FAB. Step-A REFERENCE-ONLY audit unchanged. CONFIRMS the Step-B 🟢 on the live engine (via the twin, not this probe's own `.hexa`). Evidence `state/_engine_native_audit/dfree_other/`.
- **domain:** MITOSIS-ENGINE · **substrate:** $0 CPU numpy mirror · 3 seeds [1378,1379,1380] · CORE/*.hexa UNTOUCHED (wire-in = follow-on, a_verified_must_wire)
- **evidence:** `.verdicts/1378_agent_tool_mitosis/{wiring_audit.txt, FREEZE.txt, result.txt}`
- **probe:** `state/agent-tool-mitosis/h1378_agent_tool_mitosis.py`

## Step A — WIRING AUDIT (read-only) → **REFERENCE-ONLY**
The live agent-tool layer references mitosis but does **not** learn through it end-to-end. Verbatim (file:line):

1. **Selection is a STATIC weighted dot-product over hand-set affinity floats** — `anima-agent-core/agent_tools.hexa:357-361` (`score = curiosity_affinity*curiosity + pe_affinity*pe + …`). The `*_affinity` weights are CONSTANTS baked at registration (`agent_tools.hexa:683-743`); never updated by outcome. No cell store, no affinity recall, no clonal split.
2. **A new tool is added via a STATIC registry**, not a mitosis split — hardcoded `registry_register(reg, ToolDef{…})` calls (e.g. `agent_tools.hexa:728`); `registry_get` is a plain map lookup (`agent_tools.hexa:340`). The repertoire is frozen at source-authored set.
3. **Data path terminates at a log:** `executor_execute` maps success/failure → a scalar `tension_delta` (`agent_tools.hexa:437`) appended to a capped `execution_log` ring buffer (`agent_tools.hexa:448-451`). That log is NEVER read back to grow/split a skill cell. The "failure → repertoire improves" loop does **not exist**.
4. The mitosis references are **stubs / the inverse direction:** `tool_mitosis_split` (`agent_tools.hexa:155`, TODO) EXPOSES engine mitosis *as a callable tool*; `tools.hexa:39` is an opcode tag; `consciousness_features.hexa:15` prints `"mitosis stub"`. The real teaching ops (`engine_mitosis_tick` `CORE/engine_cli.hexa:263`, `immune_embed_key` L774, `immune_memory_bind` L830, `immune_memory_recall` L858) live ONLY in CORE and are never imported by the tool layer.

**Verdict: REFERENCE-ONLY.** Tools today are a static registry; they do not learn via mitosis.

## Step B — DESIGNED MECHANISM + DIRECTIONAL MIRROR (🟢 GREEN)
**Mechanism:** a skill/tool = a CELL keyed by task-context (byte-trigram FNV-1a, **same geometry** as `immune_embed_key`, DIM=64). Tool call → recall best-affinity skill-cell (L2 affinity, abstain band `RECALL_THR`); if best affinity ABSTAINS **or** the selected tool FAILS → **MITOSIS-SPLIT** a new specialized skill-cell binding `task-context → correct tool`. The SAME op teaches (split-on-failure) and infers (recall-best) — p8, no train/infer split. Mirrors H_1227 (value-bind) / H_1288 (grow) onto agent-tools.

**Frozen bars (pre-registered FREEZE.txt; 3 arms FULL/STATIC/SHUFFLE; pooled means, all 3 seeds):**

| bar | meaning | result | gate |
|-----|---------|--------|------|
| (1) LEARNS | FULL `acc_final − acc_init` ≥ +0.30 | **+0.833** (0.167→1.000) | ✅ PASS |
| (2) DISTINCT-FROM-STATIC | FULL_final − STATIC_final ≥ +0.30 | **+0.833** (static stays 0.167, never splits) | ✅ PASS |
| (3) EARNED (shuffle) | SHUFFLE_final − STATIC_final ≤ +0.15 | **−0.046** (shuffle 0.120; training permuted bindings collapses gain) | ✅ PASS |
| (4) NO-FAB / ABSTAIN | far untrained task abstain ≥ 0.90 | **1.000** (emits no tool on disjoint trigram space) | ✅ PASS |

**VERDICT: 🟢 GREEN** (all 4 bars, all 3 seeds). The static fixed-repertoire control does NOT improve (0.167) → the lift is the mitosis split op; the shuffle control collapses → the gain is the *earned* task↔tool correspondence, not variance. **p1/p2/p3/p6 guard:** the split binds from OUTCOME only (success/failure of the executed tool), no injected "use tool T" label / RLHF / persona — the shuffle collapse proves the lift is earned structure. **Ψ-disjoint** by construction (a separate skill cell-store; decoder/pure_field untouched).

**HONEST note (c9):** the EARNED bar first FAILED because the shuffle control trained AND scored on the same permuted map (so it "learned" the wrong map equally well). Fixed the *control* — train on permuted labels but always score vs the TRUE map — a flaw the bar correctly caught; **no frozen bar was moved** (frozen-first).

## Step C — LANGUAGE DECODER vs AGENT-TOOL/MEMORY MITOSIS (the distinction)
| | **Language decoder (Engine A)** | **Agent-tool / memory MITOSIS** |
|---|---|---|
| learning rule | CE **gradient descent** (byte-LM) | **gradient-free cell SPLIT** |
| what it learns | **DISTRIBUTIONS** smeared into shared weights | **INSTANCES** — one cell per tool/skill |
| update | overwrites weights (interferes) | **ADDITIVE** — a new cell, prior cells intact |
| effect on generation | changes the decoder | **Ψ-disjoint** — NEVER touches the decoder → generation byte-identical |
| abstain | n/a (always emits a distribution) | **abstains** on far task (no fabricated tool) |

**One line:** the language decoder learns *distributions* by CE gradient smeared into weights; agent-tool teaching is the **same gradient-free mitosis substrate as memory**, learning *instances* (one additive cell per tool/skill), Ψ-disjoint, never touching the decoder.

## Scope (a_scale_honest_scope · a_toy_scale_recheck)
TOY: synthetic task→tool map, 3 seeds, deterministic readout (tests the *structure* that mitosis can teach tools, not a learned planner). DIRECTIONAL numpy mirror — **engine-transfer UNVERIFIED**. Scale / real tool-failures / paraphrased tasks / the live CORE wire-in are UNVERIFIED.

## Next round (a_verified_must_wire follow-on)
**CORE wire-in:** add a `§SkillStore` lane in `CORE/engine_cli.hexa` (reuse `immune_embed_key` + `vadapt_field_step` clonal split + `immune_memory_recall` abstain) and route `agent_tools.hexa` tool-failure → `engine_mitosis_tick`-driven skill-cell split, re-score these 4 bars engine-native + regression guard (engine_cli_smoke, single-entry, Ψ-checksum). Waits for a CORE slot. **Depletion test:** the wire-in is done only when the live tool repertoire grows a cell on a real tool failure AND the 4 frozen bars hold engine-native byte-exact with generation byte-identical ON==OFF.

xref: a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · h1227 · h1231 · h1288 · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
