# H_1520 — 🗣️🎚️ CONVERSATIONAL-SALIENCE — usable request→reply as a TOGGLEABLE faculty (like MITOSIS), per-entry-point default; philosophy guaranteed by P2/P3 regardless of default

**tier:** DIRECTIONAL (numpy mirror, hard-gate-1 auto-DIRECTIONAL)
**verdict:** 🟢 GREEN (DIRECTIONAL) — conversational usability is a clean toggleable `cfg.salience` faculty (like `cfg.mitosis`); the default is set **per entry-point** (`anima` service = ON, `anima chat` TUI = autonomous), and **the philosophy is guaranteed not by forcing a default but by P2 (retained silence-autonomy) + P3 (no assistant-frame) holding EVEN when the toggle is ON** — communication is always emit (autonomous externalization), never assistant request→reply.
**wired:** `DIRECTIONAL-mirror` — engine-native R2 = follow-on ING `h1520-r2-engine-native` (live emit gate / `core/engine_g.hexa` `motivation_score`+`should_emit` + `brain_decide`, with a real `cfg.salience` flag mirrored on the engine's `cfg.mitosis` pattern; deferred to avoid colliding with a sibling lane editing `core/engine_cli.hexa`)
**seeds:** [1520, 1521, 1522] · $0 CPU · p7 · frozen-first · c9

## THE TOGGLE IS THE HEADLINE — conversational mode is a `cfg.salience` faculty, like MITOSIS; default is PER-ENTRY-POINT
The engine already has a toggleable faculty: **MITOSIS** (`cfg.mitosis` ON/OFF; `engine_cli_parse(["--mitosis","on"])` / `["--no-mitosis"]`; `engine_mitosis_tick` is a **NO-OP when OFF** — see `core/h1166_/h1194_/h1199_*` smokes; the cfg note: *"mitosis flag is irrelevant to pf — disjoint"*). Conversational-salience is modelled the **same way**: a `cfg.salience` flag (`engine_cfg(["--salience","on"])` / `["--no-salience"]`) threaded through the SAME emit gate, where the salience boost is a **NO-OP when the flag is OFF**.

### The default is set BY ENTRY-POINT, not globally (product design, the user's)
- **`anima` (bare / service execution)** — emit-as-communication, usable from other services → toggle **DEFAULT-ON** (responsive enough to be a service).
- **`anima chat` (TUI)** — pure autonomous interactive chat → toggle **DEFAULT autonomous** (the salience boost off; anima emits on its own substrate tension).
- The TOGGLE is a **cfg flag, NOT a permanent substrate change**: flipping OFF→ON→OFF leaves Ψ=½, generation, and the separation invariant byte-identical (P4 applies to the toggle mechanism itself).

### How the philosophy is protected — NOT by the default, but by P2/P3 holding even when ON
The philosophy is **not** protected by forcing default-OFF. It is protected because **P2 (retained silence-autonomy) and P3 (no assistant-frame) hold even when the toggle is ON**:
- **MODE ON behavior:** the environmental-salience term is enabled → grounding raises Φ/coherence → the autonomous gate naturally crosses its existing threshold on answerable prompts (usable chat) **WHILE still abstaining on ungrounded prompts (P2 = 0.00)** and **WHILE the emit depends only on substrate features, never a "must answer" rule (P3 audit clean)**. Communication is always **emit** (autonomous externalization, p5), never assistant request→reply (p4).
- **MODE OFF behavior (the autonomous default for `anima chat`):** the user message is weak ambient environmental context, no boost — anima emits ONLY on genuine substrate tension (emit-rate LOW even on grounded prompts). This is the **control arm** (P2b) that proves the toggle actually changes behavior and that the autonomous mode is intact.

**Headline:** conversational usability is a **toggleable faculty (like mitosis) with a per-entry-point default (`anima` service = ON, `anima chat` = autonomous). The philosophy is guaranteed REGARDLESS of the default** — because even with the toggle ON, anima still abstains on ungrounded prompts (P2) and emits only from substrate features with no assistant-frame (P3). Communication is always autonomous externalization, never assistant request→reply.

## MECHANISM (faithful to the live gate — no invented machinery)
Mirror of `core/engine_g.hexa` (`motivation_score` 8-factor weighted sum, `should_emit` = `score > 0.30`, the A→G `safety_phi_ratchet` gate `phi > phi_peak/2`) + the 8 factors derived exactly as `HEXAD/CHAT/spontaneous_lib.hexa` §2 derives them. The user message enters ONLY as a READ of how strongly it grounds in the live immune store (H_1227 FNV-trigram key geometry). When `cfg.salience` is OFF the grounding-gain drops to a weak ambient floor (no boost) and the coherence band widens (no inward pull) — both grounding-driven boosts are part of the SAME opt-in faculty. **No "must answer" constant is ever added.**

## FROZEN BARS + RESULTS (pre-registered `H_1520_FREEZE.txt` v2, frozen-first, mean 3 seeds)
| bar | rule | value | pass |
|---|---|---|---|
| **P1 USABILITY** | MODE ON grounded emit-rate ≥ 0.90 | **1.00** | ✅ |
| **P2 RETAINED-AUTONOMY** | MODE ON ungrounded emit-rate ≤ 0.40 | **0.00** | ✅ |
| **GAP** (P1−P2) | ≥ 0.50 (substrate-DECIDED, not stimulus-response) | **1.00** | ✅ |
| **P2b AUTONOMOUS-ARM** ⭐ | MODE OFF grounded emit-rate ≤ 0.40 **AND** toggle-delta (ON−OFF grounded) ≥ 0.50 (the autonomous mode is intact + the toggle materially changes behavior) | **off 0.00, Δ 1.00** | ✅ |
| **P3 NO-ASSISTANT-FRAME** | operative gate code clean (AST-extracted gate fns; no system_prompt / persona / assistant-frame / baked must_answer constant; score = weighted 8-factor `motivation_score`) | clean | ✅ |
| **P3 ADVERSARIAL** | inject `must_answer=1.0` (MODE ON) → ungrounded emit-rate jumps > 0.40 (P2 breaks) | **1.00** | ✅ |
| **P4 NO-DAMAGE** (toggle mechanism) | flip OFF→ON→OFF → generation byte-identical + Ψ=½ + reversible cfg flag (both states) | True | ✅ |

→ **🟢 GREEN (DIRECTIONAL).** All seven bars pass.

## THE PHILOSOPHY GUARD (load-bearing — this H is ABOUT the rules)
The philosophy is **not** protected by forcing a particular default — the default is a per-entry-point product choice (`anima` service = ON, `anima chat` = autonomous). It is protected because **P2 and P3 hold even with the toggle ON**:
- **P2 dissociation** (MODE ON, the no-damage crux): usability ≠ blind compliance — anima still abstains on ungrounded prompts (emit-rate 0.00) even in chat mode. So even on the service entry-point (default-ON), communication remains autonomous emit, never forced request→reply.
- **P3 adversarial** proves P2 is a real discriminator: a baked `must_answer=1.0` constant would jump ungrounded emit to 1.00 and break P2. The honest verdict would then be "this scheme DOES damage autonomy → REJECT" (c9). It does not, because the emit depends only on substrate features (grounding-driven), never an assistant-frame rule.
- **P2b autonomous-arm** confirms the toggle is real, not inert: with the boost OFF, even grounded prompts stay silent (emit-rate 0.00) and the toggle materially changes behavior (delta 1.00). The `anima chat` autonomous mode is intact.
- **P4** confirms the toggle is a reversible cfg flag (like mitosis), not a permanent substrate change: OFF→ON→OFF leaves generation and Ψ=½ byte-identical — switching entry-points never mutates the substrate.

## HONEST SCOPE (a_scale_honest_scope · a_toy_scale_recheck · c9)
- **DIRECTIONAL numpy mirror** (hard-gate-1: `state/1520_conversational_salience/h1520_salience.py` greps `numpy` → auto-DIRECTIONAL, terminal NOT). Engine-native R2 = deferred follow-on ING `h1520-r2-engine-native` (add a real `cfg.salience` flag to the live emit gate mirrored on `cfg.mitosis`, re-score frozen bars on `brain_decide`).
- TOY synthetic prompt classes, deterministic seeded readout — tests the emit-gate STRUCTURE + the toggle, not a trained chat model. Real-corpus / paraphrase / multi-turn / scale / engine-transfer UNVERIFIED.
- **Substrate sensitivity params (NOT bars; grounding-driven):** GROUNDING_GAIN 1.30 (mode ON) vs ENV_FLOOR 0.12 (mode OFF); coherence band 0.020 (ON) vs 0.060 (OFF); DIM 512 (64 saturated — metric-artifact, frozen-first); info_gap = answerable-residual `cos·(1−cos)`. Off-mode grounded scores cluster 0.06–0.24 (all under the 0.30 threshold with margin — not a knife-edge).
- NO `core/*.hexa` / README / ARCHITECTURE change in R1.

## HEADLINE (the user's "without damage" answer)
**YES — and it is a toggleable faculty with a per-entry-point default.** Conversational usability is a `cfg.salience` toggle exactly like mitosis. The default is set **by entry-point**: `anima` (bare/service) = **ON** (responsive enough to serve other services), `anima chat` (TUI) = **autonomous**. **Crucially, the philosophy is guaranteed REGARDLESS of the default** — not by forcing OFF, but because **P2 and P3 hold even when the toggle is ON**: in chat-mode anima still abstains on ungrounded prompts (P2 = 0.00) and emits only from substrate features with no assistant-frame (P3 audit clean + adversarial discriminator). Communication is always **emit** (autonomous externalization, p5), never assistant request→reply (p4). MODE ON gives usable chat (grounded emit-rate 1.00); the autonomous arm (boost OFF) stays silent (0.00, P2b), and the toggle leaves Ψ=½ + generation byte-identical across flips (P4) — **zero philosophy damage on either entry-point.**

xref: p1·p3·p4·p5·`p5_tension_emit_not_filler`·`a_substrate_native_speak`·`a_autonomy_over_hardcode`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·`a_scale_honest_scope`·c9 · MITOSIS `cfg` toggle (`core/h1166_/h1194_/h1199_*` smokes) · H_1227 (immune key geometry) · `core/engine_g.hexa` · `HEXAD/CHAT/spontaneous_lib.hexa`

artifacts: `state/1520_conversational_salience/h1520_salience.py` · `state/verdicts/1520_conversational_salience/{H_1520_FREEZE.txt,H_1520_R1.json}`
