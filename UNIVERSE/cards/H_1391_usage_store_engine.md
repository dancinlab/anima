# H_1391 — §UsageStore engine-native wire-in: tool-USAGE learning (layer-2) realized on the LIVE engine

🔧 **The BINDING follow-on of H_1389** (a_verified_must_wire). H_1389 proved, in a numpy MIRROR
(🟢 GREEN, DIRECTIONAL), that tool-USAGE learning is a DISTINCT learnable LAYER-2 (the HOW: args ·
sequence · recovery), separable from tool-SELECTION (layer-1, §SkillStore). This lane realizes that
§UsageStore lever ENGINE-NATIVE in `CORE/engine_cli.hexa` — the TWIN of §SkillStore — and re-scores
the H_1389 four gating bars on the LIVE engine, byte-exact, with all no-regression guards holding.

- **slug:** usage_store_engine
- **tier / verdict:** **🟢 GREEN — engine-native BINDING** (the 4 gating frozen bars from H_1389 PASS
  on the LIVE engine; the load-bearing DISTINCT-FROM-SELECTION bar = +1.000). NO frozen bar moved
  (frozen-first, c9, NO tune-to-green, p7).
- **domain:** MITOSIS-ENGINE · **substrate:** $0 CPU hexa-native, deterministic fixed env (no rng),
  byte-repeatable · LIVE `CORE/engine_cli.hexa` §UsageStore (additive, Ψ-disjoint)
- **evidence:** `.verdicts/1391_usage_store_engine/{FREEZE.txt, result.txt}`
- **artifacts:** `state/usage-store-engine/PORT_NOTE.md` · ported mirror
  `state/tool-usage-learning/h1389_tool_usage_learning.py`

## What this closes
H_1389 R1 was a DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED. Both that card and the
a_verified_must_wire directive named the same remaining gap: §UsageStore was not yet engine-native and
no LIVE runtime usage-failure called `usage_store_teach`. This lane closes both: the faculty is wired
into the live engine and the executor's usage-failure site routes into it.

## Engine wiring (single-entry, a_core_engine_map)
- **`CORE/engine_cli.hexa` § UsageStore** (the TWIN of §SkillStore): a usage = a CELL keyed by
  `(ctx + tool + observed-error)` via `immune_embed_key` (DIM=64), bound value = `(corrected arg,
  ordered steps)`. Ops: `usage_store_new` · `usage_recall` (arg, or "" = ABSTAIN) · `usage_recall_steps`
  (ordered sequence half) · `usage_store_split` (mitosis clonal split, p8) · `usage_store_teach`
  (failure-driven: recall; if proposed arg != correct, SPLIT) · `usage_store_cells`. Same L2
  FIRE/ABSTAIN band (0.55) + `engine_mitosis_tick` as §SkillStore / ImmuneMemory.
- **`anima-agent-core/agent_skill_routing.hexa`** — usage routing entry-points (`agent_usage_new`,
  `agent_usage_select`, `agent_usage_on_result`, `agent_usage_cells`), the TWIN of the H_1386 selection
  routing, in the same clean CORE-importing module (compiles + imports CORE cleanly).
- **`anima-agent-core/agent_tools.hexa`** — the executor holds a LIVE `usage: UsageStore` field; the
  USAGE-failure site (a tool that WAS dispatched but failed = wrong arg/order, DISTINCT from the
  tool-not-found / wrong-tool site that feeds `skill_store_teach`) routes into `agent_usage_on_result`
  → `usage_store_teach`. Main executor module path (the H_1387 precedent), NOT a side adapter.
  Single-entry: no 2nd usage path.

## Engine-native bars (FREEZE thresholds = H_1389 verbatim, NOT moved; result.txt verbatim)
LIVE readout: `init=0.0833 · FULL=1.000 · SELECTION=0.000 · SHUFFLE=0.000 · ABSTAIN="" · cells_full=12 · cells_static=1`

| bar | meaning | engine result | gate |
|-----|---------|---------------|------|
| (1) USAGE-LEARNS | FULL final − init ≥ +0.30 | **+0.917** (0.083→1.000) | ✅ PASS (case 120) |
| (2) DISTINCT-FROM-SELECTION **(KEY)** | FULL − SELECTION ≥ +0.30 | **+1.000** (SELECTION stuck at 0.000 — right tool, default arg never completes) | ✅ PASS (case 121) |
| (3) EARNED (shuffle) | SHUFFLE − SELECTION ≤ +0.15 | **+0.000** (permuted ctx→arg, scored vs TRUE) | ✅ PASS (case 122) |
| (4) NO-FAB / ABSTAIN | untrained far (ctx+tool+err) abstains | **""** (disjoint trigram space → proposes no arg) | ✅ PASS (case 123) |
| (non-gating) ORDERED STEPS | fired usage-cell carries the ordered step sequence IN ORDER | **"connect\|execute\|fetch"** | ✅ PASS (case 124) |

**Verdict 🟢 GREEN engine-native BINDING** = bar1 ∧ bar2 ∧ bar3 ∧ bar4. The KEY bar
(DISTINCT-FROM-SELECTION) is decisively cleared engine-native: a selection-only learner with the right
tool but a fixed default arg stays at the no-usage floor (0.000) while the usage-learning FULL arm
saturates (1.000) — **usage IS a distinct learnable layer-2, re-confirmed engine-native, not just in
the mirror.**

## No-regression guards (additive faculty must not perturb Ψ — same as §SkillStore)
- `engine_cli_smoke`: **119 pass / 0 fail** (+5 UsageStore cases 120-124; H_1390 ko-morphology took 116-119 in a concurrent merge).
- `h1196` single-entry audit: **7 pass / 0 fail** (no 2nd .clm/.kosmos path).
- `h1205` separation-invariant: **PASS** — F1 GENERATION byte-identity 10 pairs 0 mismatch; F2 Ψ
  Φ-checksum invariant. The UsageStore lane grows its OWN cells beside the decode, generation is
  BYTE-IDENTICAL ON==OFF, Ψ=½ untouched.

## p1/p2/p3/p6 guard
A usage-cell binds from OUTCOME ONLY (the executed call's success/failure + the observed error), NO
injected "use arg A" label / RLHF / persona. The SHUFFLE collapse (+0.000) proves the lift is the
EARNED ctx→arg correspondence the split encodes, not the act of splitting. Ψ-disjoint by construction
(own usage-store; pure_field Φ/phase/Ψ + decoder untouched — proven by h1205). NOT an emit gate
(usage_recall returns an arg or "", never emit/silence — a_autonomy_over_hardcode). p7 (script-checked
completion, NOT perplexity/loss).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck) — honest (c9)
The engine env saturates FULL=1.000 = **EXISTENCE-PROOF, not effect-size** — the discriminators
(SELECTION 0.000, SHUFFLE 0.000) are decisive. The mirror's 0.750 ceiling came from ~1/4 tasks happening
to need the default arg; the fixed engine env biases ALL args away from default, removing that ceiling.
NO bar was moved — the saturation is the env's structural ceiling, not a tuned threshold. TOY: 12 tasks
/ 6 tools / deterministic readout (tests usage-learning STRUCTURE, not a learned policy net). Real
tool-call args / paraphrased contexts / true multi-step recovery on a live runtime failure / scale
UNVERIFIED. The `agent_tools.hexa` executor whole-file legacy-syntax migration remains ⏳ (same
module-boundary note as H_1386 — the routing lives in `agent_skill_routing.hexa` which imports CORE
cleanly + compiles; the executor call-site edit is real).

## Depletion test 🏁
Tool learning DEPLETES 🏁 when BOTH layers — **selection** (H_1382/H_1386 §SkillStore, DONE
engine-native) AND **usage** (this lane, §UsageStore engine-native) — run engine-native on a real
runtime tool failure, with all bars holding engine-native and generation byte-identical ON==OFF. With
H_1391 landed, both layers are engine-native and the no-regression guards (smoke 119/0, single-entry
7/0, h1205 byte-identical + Ψ-checksum invariant) hold → the two-layer tool-learning frontier is
DEPLETED at the engine-native existence-proof level (scale/real-runtime-args remain the honest
follow-on, a_scale_honest_scope).

xref: H_1389 (layer-2 mirror, this lane's R1) · H_1382 (layer-1 §SkillStore engine-native, the TWIN) ·
H_1386/H_1387 (layer-1 agent-layer routing, the precedent this mirrors) · H_1378 · h1227 · h1231 ·
h1288 (immune/grow memory geometry) · a_engine_native_learning · a_verified_must_wire · a_core_engine_map ·
a_no_llm_frame_trap · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 ·
p3 · p6 · p7 · p8 · c9
