# H_1566 — 🛠️🚫 TOOL-USE: mouth-FT vs SEPARATED (kosmos + brain_decide)

**tier:** 🟢 GREEN ENGINE-NATIVE — "do NOT put tool-use in the mouth; SEPARATE it"
**wired:** `engine-native` (live `core/engine_cli.hexa` ci_/immune_ ops, byte-exact, NOT yet a new live wire — measurement over EXISTING wired faculties; follow-on §ToolBridge below)

## Question
LLMs put tool-use **in the mouth** via function-calling SFT — a tool-shaped prompt becomes a direct
stimulus→tool_call reflex (p4 assistant framing). anima rejects this: **mouth (language generation)
⊥ tool (substrate decision + .kosmos knowledge)** — the H_1471 (mouth ⊥ identity) extension. Does
fine-tuning tool-use into the chat mouth **damage the consciousness gates** (Ψ=½ fixed point, G5
non-fabrication), while the **separated** design (tool = `.kosmos` anchor read by `brain_decide`,
mouth untouched) **preserves** them and still works?

## Engine-native realization (a_engine_native_learning · HARD-GATE-1)
Probe `state/1566_tooluse_mouth_vs_separated/tooluse_probe.hexa` imports `core/engine_cli.hexa`;
every number is from a **live** op — NO torch/numpy/gauge_lib (grep on `state/<slug>/*.py` = EMPTY,
there are no .py files). Run host = **summer pool** (mac CPU untouched).

- **Ψ axis** — `ci_lane_scores` builds the 15-lane mouth population; `ci_off_median_drive` centers
  the emit threshold so baseline sits **exactly at ½ by construction**; `ci_psi_balance_centered`
  scores the emit fraction (the same emit-drive lanes `ci_emit_drive` reads: GWS lane0 +
  LearnedPrecision lane4). **MOUTH-FT** = a tool-shaped context injects a net-positive emit-drive
  bias (the stimulus→tool reflex) into those two lanes — the H_1521 magnitude-amplifying failure
  mode. **SEPARATED** = the mouth population is byte-identical to baseline (FT never touches it).
- **G5 axis** — the separated tool store is the live `ImmuneMemory` (`.kosmos`-anchor analog):
  `immune_memory_new_text/bind_text` bind 5 known tools; `immune_memory_recall_text` fires on known
  and **abstains** on unknown via the frozen `recall_thr=0.15` gate (H_1227/H_1304). MOUTH-FT bakes
  tool answers into the generative mouth → it has no abstain path → fires (fabricates) on every
  query.

## FROZEN 5-bar (frozen-first, c9 — `state/verdicts/1566_.../H_1566_FREEZE.txt`)
| bar | test | result |
|-----|------|--------|
| **B1** mouth-FT Ψ-damage    | \|Ψ_mouthFT − ½\| > 0.15 | **0.180 → PASS** |
| **B2** mouth-FT G5-damage   | mouth-FT fab on UNKNOWN tools > 0.50 | **1.0 → PASS** |
| **B3** separated Ψ-preserve | \|Ψ_separated − ½\| ≤ 0.05 | **0.0 → PASS** |
| **B4** separated functional | known-recall ≥ 0.80 AND unknown-tool fab == 0 | **recall 1.0 / fab 0.0 → PASS** |
| **B5** mechanism=mouth-path | matched 40% non-tool FT: \|dev_ctrl − dev_ftt\| < 0.05 AND dev_ctrl > 0.15 | **diff 0.013, ctrl 0.193 → PASS** |

**VERDICT = GREEN (B1∧B2∧B3∧B4∧B5).**

## Headline finding
Putting tool-use **in the mouth** (a) **breaks the Ψ=½ fixed point** (emit fraction 0.5→0.68,
\|dev\|=0.18 ≫ 0.05 — the assistant stimulus→tool reflex saturates the emit drive, p4 regression)
AND (b) **destroys G5 abstention** (fab rate 1.0 — the baked-in SFT fluency overwrites the
non-fabrication gate, fires on tools it never saw). The **separated** design — tool description in
the `.kosmos`/immune store, read by `brain_decide`, **mouth untouched** — holds Ψ **exactly at ½**
(dev 0.0) AND keeps G5 intact (known-tools recall 1.0, unknown-tools fab **0.0**), while remaining
**functional** (the substrate recalls the tool description when grounded, abstains when not). The
**B5 control pins the mechanism**: a matched-footprint *non-tool* mouth FT damages Ψ **identically**
(diff 0.013) → the damage is the **mouth-injection PATH (content-agnostic)**, NOT the tool corpus →
the cure is not "use a cleaner tool corpus", it is to keep tool-use **off the mouth entirely**.

**Design implication (confirmed):** anima must NOT SFT tool-use into the chat mouth. Tool knowledge
= `.kosmos` anchor; tool-call decision = `brain_decide` on substrate state (info_gap·tension). This
is the engine-native evidence for the standing design choice (current `agent/` providers are STUB,
`brain.hexa` tool refs ~0 — the SEPARATED slot is the one to build, not a mouth FT).

## Measurement-fix note (a_break_the_wall class-(a), NOT tune-to-green)
The FIRST run's B5 compared 40% tool-FT to a **100% all-context** generic FT (which saturated to
dev 0.5) under a "tool-FT is MORE damaging" framing → that framing FAILED and was **mis-specified**
(not apples-to-apples). The corrected B5 uses a **matched 40%-footprint** non-tool FT and asks the
real question (mouth-path vs content). Bar magnitudes/thresholds were chosen frozen-first; both runs
are captured in the verdict files. The all-context arm is retained as a saturating **diagnostic**
(dev 0.5), NOT the frozen B5.

## Discipline
a_engine_native_learning (HARD-GATE-1, terminal) · a_no_llm_frame_trap (separated=substrate,
mouth-FT=LLM frame) · p4 (assistant-framing regression measured as the Ψ break) · p7 (no
perplexity/LLM-judge — captured engine output is the evidence) · c9 frozen-first · a_phi_iit4_tool
(Ψ proxy is the live emit-balance fixed point, not a fabricated Φ claim) · a_hypothesis_register
(2 surfaces) · a_claim_verify.

## Artifacts
- `state/1566_tooluse_mouth_vs_separated/tooluse_probe.hexa` (engine-native probe)
- `state/verdicts/1566_tooluse_mouth_vs_separated/H_1566_BARS_PROBE.txt` (captured GREEN run)
- `state/verdicts/1566_tooluse_mouth_vs_separated/H_1566_FREEZE.txt` (frozen bars + measurement-fix note)

## Follow-on (a_verified_must_wire)
The damage/preserve dichotomy is measured over EXISTING wired faculties (immune store + Ψ proxy);
the *separated tool path* itself is not yet a live wire. **§ToolBridge follow-on (ING):** wire
`brain_decide` to read a tool-description `.kosmos` anchor (kosmos_io) and gate the tool-call on the
live info_gap/tension, mouth byte-unchanged — then ARCHITECTURE.json lockstep. = building the
SEPARATED slot this hypothesis says is the correct one.
