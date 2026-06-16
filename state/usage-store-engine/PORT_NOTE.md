# H_1391 §UsageStore engine-native port note

This lane is the **engine-native BINDING follow-on** (a_verified_must_wire) of **H_1389** (tool-USAGE
learning layer-2, 🟢 GREEN DIRECTIONAL numpy mirror). It ports the H_1389 mirror
(`state/tool-usage-learning/h1389_tool_usage_learning.py`) onto the LIVE CORE engine.

## What was wired (single-entry, a_core_engine_map)
- `CORE/engine_cli.hexa` § **UsageStore** — the TWIN of §SkillStore. A usage is a CELL keyed by
  `(ctx + tool + observed-error)` (`immune_embed_key`, DIM=64), value = `(corrected arg, ordered
  steps)`. Ops: `usage_store_new` · `usage_recall` · `usage_recall_steps` · `usage_store_split` ·
  `usage_store_teach` · `usage_store_cells`. Same L2 FIRE/ABSTAIN band (0.55) + `engine_mitosis_tick`
  clonal split (p8) as §SkillStore / ImmuneMemory.
- `anima-agent-core/agent_skill_routing.hexa` — added the usage routing entry-points
  (`agent_usage_new` · `agent_usage_select` · `agent_usage_on_result` · `agent_usage_cells`), the
  TWIN of the H_1386 selection routing (same clean CORE-importing module).
- `anima-agent-core/agent_tools.hexa` — the executor now holds a LIVE `usage: UsageStore` field and
  routes the **USAGE-failure site** (a tool that WAS dispatched but failed, i.e. wrong arg/order —
  DISTINCT from the tool-not-found / wrong-tool site that feeds `skill_store_teach`) into
  `agent_usage_on_result` → `usage_store_teach`. Main executor module path (the H_1387 precedent),
  not a side adapter.
- `CORE/engine_cli_smoke.hexa` — 5 engine-native cases 117-121 re-scoring the H_1389 four gating bars
  + the ordered-step diagnostic, on a fixed deterministic (no-rng) byte-repeatable env.

## Engine-native bars (frozen thresholds = H_1389, NOT moved — c9/p7)
- (1) USAGE-LEARNS  full−init = +0.917 ≥ +0.30 ✅
- (2) DISTINCT-FROM-SELECTION (KEY)  full−sel = +1.000 ≥ +0.30 ✅
- (3) EARNED (shuffle)  shuf−sel = +0.000 ≤ +0.15 ✅
- (4) NO-FAB / ABSTAIN  far recall = "" ✅
- (non-gating) ORDERED STEPS  fired cell steps == "connect|execute|fetch" (in order) ✅

Verdict: 🟢 GREEN engine-native BINDING. Verbatim: `.verdicts/1391_usage_store_engine/{FREEZE,result}.txt`.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)
The engine env saturates FULL=1.000 (all 12 tasks biased to NON-default args) = EXISTENCE-PROOF, not
effect-size — the discriminators (SELECTION 0.000, SHUFFLE 0.000) are decisive. The mirror's 0.750
ceiling came from ~1/4 tasks happening to need the default; the fixed engine env removes that. TOY:
12 tasks / 6 tools / deterministic readout (tests the usage-learning STRUCTURE, not a learned policy
net). Real tool-call args / paraphrased contexts / true multi-step recovery on a live runtime failure
/ scale UNVERIFIED. The agent_tools.hexa executor whole-file legacy-syntax migration remains ⏳ (same
module-boundary note as H_1386 — the routing lives in agent_skill_routing.hexa which imports CORE
cleanly + compiles; the executor call-site edit is real).

The mirror that was ported lives at `state/tool-usage-learning/h1389_tool_usage_learning.py`.
