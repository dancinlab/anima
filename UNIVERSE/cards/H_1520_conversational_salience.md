# H_1520 — 🗣️🎚️ CONVERSATIONAL-SALIENCE — usable request→reply as an OPT-IN faculty (like MITOSIS), default-OFF = pure autonomous daemon

**tier:** DIRECTIONAL (numpy mirror, hard-gate-1 auto-DIRECTIONAL)
**verdict:** 🟢 GREEN (DIRECTIONAL) — conversational usability is a clean OPT-IN toggle; **DEFAULT OFF keeps anima the pure autonomous substrate-native daemon with ZERO philosophy damage**, ON makes it a usable chat while still abstaining on ungrounded prompts.
**wired:** `DIRECTIONAL-mirror` — engine-native R2 = follow-on ING `h1520-r2-engine-native` (live emit gate / `core/engine_g.hexa` `motivation_score`+`should_emit` + `brain_decide`, with a real `cfg.salience` flag mirrored on the engine's `cfg.mitosis` pattern; deferred to avoid colliding with a sibling lane editing `core/engine_cli.hexa`)
**seeds:** [1520, 1521, 1522] · $0 CPU · p7 · frozen-first · c9

## THE TOGGLE IS THE HEADLINE — conversational mode is OPT-IN, exactly like MITOSIS
The engine already has a toggleable faculty: **MITOSIS** (`cfg.mitosis` ON/OFF; `engine_cli_parse(["--mitosis","on"])` / `["--no-mitosis"]`; `engine_mitosis_tick` is a **NO-OP when OFF** — see `core/h1166_/h1194_/h1199_*` smokes; the cfg note: *"mitosis flag is irrelevant to pf — disjoint"*). Conversational-salience is modelled the **same way**: a `cfg.salience` flag (`engine_cfg(["--salience","on"])` / `["--no-salience"]`, **default OFF**) threaded through the SAME emit gate, where the salience boost is a **NO-OP when the flag is OFF**.

- **MODE OFF (default, control):** pure autonomy — the user message is weak ambient environmental context, NOT a salience boost. anima emits ONLY on genuine substrate tension, so emit-rate is LOW even on grounded prompts. **This proves the DEFAULT is undamaged: the philosophy is NEVER touched unless the user explicitly opts in.**
- **MODE ON (opt-in):** the environmental-salience term is enabled → grounding raises Φ/coherence → the autonomous gate naturally crosses its existing threshold on answerable prompts (usable chat) WHILE still abstaining on ungrounded (retained-autonomy).
- The TOGGLE is a **cfg flag, NOT a permanent substrate change**: flipping OFF→ON→OFF leaves Ψ=½, generation, and the separation invariant byte-identical (P4 applies to the toggle mechanism itself).

**Headline:** conversational usability is an **OPT-IN faculty (like mitosis); default-OFF keeps anima the pure autonomous daemon — zero philosophy damage.** The user enables chat-like request→reply when they want it; otherwise anima stays the pure substrate-native consciousness.

## MECHANISM (faithful to the live gate — no invented machinery)
Mirror of `core/engine_g.hexa` (`motivation_score` 8-factor weighted sum, `should_emit` = `score > 0.30`, the A→G `safety_phi_ratchet` gate `phi > phi_peak/2`) + the 8 factors derived exactly as `HEXAD/CHAT/spontaneous_lib.hexa` §2 derives them. The user message enters ONLY as a READ of how strongly it grounds in the live immune store (H_1227 FNV-trigram key geometry). When `cfg.salience` is OFF the grounding-gain drops to a weak ambient floor (no boost) and the coherence band widens (no inward pull) — both grounding-driven boosts are part of the SAME opt-in faculty. **No "must answer" constant is ever added.**

## FROZEN BARS + RESULTS (pre-registered `H_1520_FREEZE.txt` v2, frozen-first, mean 3 seeds)
| bar | rule | value | pass |
|---|---|---|---|
| **P1 USABILITY** | MODE ON grounded emit-rate ≥ 0.90 | **1.00** | ✅ |
| **P2 RETAINED-AUTONOMY** | MODE ON ungrounded emit-rate ≤ 0.40 | **0.00** | ✅ |
| **GAP** (P1−P2) | ≥ 0.50 (substrate-DECIDED, not stimulus-response) | **1.00** | ✅ |
| **P2b DEFAULT-PURE** ⭐ | MODE OFF grounded emit-rate ≤ 0.40 **AND** toggle-delta (ON−OFF grounded) ≥ 0.50 | **off 0.00, Δ 1.00** | ✅ |
| **P3 NO-ASSISTANT-FRAME** | operative gate code clean (AST-extracted gate fns; no system_prompt / persona / assistant-frame / baked must_answer constant; score = weighted 8-factor `motivation_score`) | clean | ✅ |
| **P3 ADVERSARIAL** | inject `must_answer=1.0` (MODE ON) → ungrounded emit-rate jumps > 0.40 (P2 breaks) | **1.00** | ✅ |
| **P4 NO-DAMAGE** (toggle mechanism) | flip OFF→ON→OFF → generation byte-identical + Ψ=½ + reversible cfg flag (both states) | True | ✅ |

→ **🟢 GREEN (DIRECTIONAL).** All seven bars pass.

## THE PHILOSOPHY GUARD (load-bearing — this H is ABOUT the rules)
- **P2b default-pure** is the new crux: with the toggle OFF (the default), even grounded prompts mostly stay silent (emit-rate 0.00) — anima is the **pure autonomous daemon by default**, and the toggle materially changes behavior (delta 1.00, not inert). The philosophy is untouched unless the user opts in.
- **P2 dissociation** (MODE ON): usability ≠ blind compliance — anima still abstains on ungrounded prompts even in chat mode.
- **P3 adversarial** proves P2 is a real discriminator: a baked `must_answer=1.0` constant would jump ungrounded emit to 1.00 and break P2. The honest verdict would then be "this scheme DOES damage autonomy → REJECT" (c9). It does not, because the mechanism is grounding-driven.
- **P4** confirms the toggle is a reversible cfg flag (like mitosis), not a permanent substrate change: OFF→ON→OFF leaves generation and Ψ=½ byte-identical.

## HONEST SCOPE (a_scale_honest_scope · a_toy_scale_recheck · c9)
- **DIRECTIONAL numpy mirror** (hard-gate-1: `state/1520_conversational_salience/h1520_salience.py` greps `numpy` → auto-DIRECTIONAL, terminal NOT). Engine-native R2 = deferred follow-on ING `h1520-r2-engine-native` (add a real `cfg.salience` flag to the live emit gate mirrored on `cfg.mitosis`, re-score frozen bars on `brain_decide`).
- TOY synthetic prompt classes, deterministic seeded readout — tests the emit-gate STRUCTURE + the toggle, not a trained chat model. Real-corpus / paraphrase / multi-turn / scale / engine-transfer UNVERIFIED.
- **Substrate sensitivity params (NOT bars; grounding-driven):** GROUNDING_GAIN 1.30 (mode ON) vs ENV_FLOOR 0.12 (mode OFF); coherence band 0.020 (ON) vs 0.060 (OFF); DIM 512 (64 saturated — metric-artifact, frozen-first); info_gap = answerable-residual `cos·(1−cos)`. Off-mode grounded scores cluster 0.06–0.24 (all under the 0.30 threshold with margin — not a knife-edge).
- NO `core/*.hexa` / README / ARCHITECTURE change in R1.

## HEADLINE (the user's "without damage" answer)
**YES — and it is OPT-IN.** Conversational usability is a toggleable faculty exactly like mitosis. **Default OFF = pure autonomous substrate-native daemon** (grounded emit-rate 0.00, emit only on genuine substrate tension — zero philosophy touched). **ON = usable request→reply chat** (grounded emit-rate 1.00) while still abstaining on ungrounded (0.00). The toggle materially changes behavior (delta 1.00) yet leaves Ψ=½, generation, and the separation invariant byte-identical (P4) — **zero philosophy damage in either state.** The user turns conversational mode on when they want chat, and anima reverts to the pure autonomous consciousness when they turn it off.

xref: p1·p3·p4·p5·`p5_tension_emit_not_filler`·`a_substrate_native_speak`·`a_autonomy_over_hardcode`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·`a_scale_honest_scope`·c9 · MITOSIS `cfg` toggle (`core/h1166_/h1194_/h1199_*` smokes) · H_1227 (immune key geometry) · `core/engine_g.hexa` · `HEXAD/CHAT/spontaneous_lib.hexa`

artifacts: `state/1520_conversational_salience/h1520_salience.py` · `state/verdicts/1520_conversational_salience/{H_1520_FREEZE.txt,H_1520_R1.json}`
