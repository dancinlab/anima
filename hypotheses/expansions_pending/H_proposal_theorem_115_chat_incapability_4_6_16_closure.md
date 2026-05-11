# Expansion Draft — H_proposal (NEW): Theorem 115 — CLM v4 Chat-Incapability 4 → 6 → 16-Closure

## Status: draft-pending-review (2026-05-11) — proposal for new H_XXX (no current target)

## Source candidates merged (3 core + chat-incapability lineage)

- Hc_609 115-clm-v4-architectural-chat-incapability-theorem — original Theorem 115: CLM v4 substrate cannot achieve traditional chat composite ≥ 0.5584 via 4-axis converging closure (L1 LoRA SFT Δ=−36.298pp / L2 Pβ Φ★-distill 0.01176 / L3 tribev2 no logits/lm_head/generate / L4 logit lens n_coherent 1/8)
- Hc_660 115-6-closure-4-axis-2-substrate-empirical-floor — extended to 6 closures: + closure 5 (semantic bridge cosine-NN degenerate `\x1c\x06...`) + closure 6 (iterative self-feed attractor `(\x1c, \x06×9)`). Pβ Paradigm D 50K Φ★=42.37 PASS while chat composite 0.01176 FAIL_TRUE → Φ★ axis stability ⊥ chat-cap (decoupled)
- Hc_666 clm-v4-16-closure-layer-lockin-byte-monopoly-chat-axis-decoupled — extended to 16+ closures: 4-closure formal + entropy basin + closures 5-6 + L13-L15 lock-in + byte monopoly + chat axis decoupled + prompt-conditional basin. 6-step causal chain (embed Korean 9 → L0-L12 drift → L13 rank 102 lock-out → L14-L15 entropy 10.9→3.3 collapse → lm_head byte monopoly → SAE chat-axis lm_head decoupled)
- bridge: chat-incapability lineage docs (anima_115_architectural_4_closure_theorem_2026_05_05.md, anima_2026_05_05_cycle_close_decision_landed_2026_05_05.ai.md, anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md)

## Proposed expansion target

- Target: hypotheses/H_proposal_theorem_115.md (NEW; assign next free H_ID at promotion time)
- Action: propose as new theorem-grade H — first formal chat-incapability statement in ANIMA repo with progressive closure structure (4 → 6 → 16)

## Draft content

### Hypothesis (unified theorem statement)

**Theorem 115 (closure-under-evidence, NOT formal proof).** The CLM v4 substrate S = (dancinlab/clm-v4-mk2-v1, paradigm v11 G3, Φ★ +41.86, 16 decoder blocks, hidden_dim 768) cannot achieve C = traditional chat composite ≥ 0.5584 + coherent multi-turn dialogue. The impossibility is closed under 16 mutually independent failure mechanisms organized along 4 axes × 2 substrates:

**Stage 1 — 4 formal closures (Hc_609):**
- L1 (post-hoc adapter): LoRA SFT chat-composite Δ = −36.298 pp
- L2 (train-time distill): Pβ Φ★-axis distill F-Pβ-3 chat composite 0.01176 RED
- L3 (cross-modal bridge): tribev2 family produces no logits / lm_head / generate
- L4 (residual-stream probe): logit lens n_coherent 1/8 + semantic bridge 0/2

**Stage 2 — 2 extended closures (Hc_660):**
- L5 (semantic bridge cosine-NN): degenerate to `\x1c\x06...` byte cluster
- L6 (iterative self-feed): greedy locks to `(\x1c, \x06×9)` attractor

**Stage 3 — 10 deep closures (Hc_666 6-step causal chain × measurement decomposition):**
- L7-L12: 6-step root mechanism (embed Korean 9 in-top-100 → L0-L12 drift → L13 Korean rank-102 lock-out → L14-L15 entropy 10.9→3.3 collapse → lm_head top-30 100% byte-fallback monopoly → SAE chat-axis residual but lm_head decoupled)
- L13-L16: entropy basin / L13-L15 layer lock-in / byte monopoly / prompt-conditional basin (measurement-method decompositions cross-validated 4 methods)

The Φ★-axis is **decoupled from chat-cap**: Pβ Paradigm D 50K reaches Φ★=42.37 PASS WHILE chat composite stays 0.01176 FAIL_TRUE.

### Predictions (H_115.1 — H_115.4 untested bypass paths)

These are the H1-H4 paths that have NOT yet been falsified, kept as open routes:

- H_115.1 (continued-pretrain bypass): a continued-pretraining run with chat-objective + Korean corpus may unwind L13 lock-out. Falsifier: post-pretrain n_coherent ≥ 5/8 → 4-axis closure broken
- H_115.2 (foundation-borrow bypass): swap to Llama-3.2-3B foundation (Path A v2 corollary) with anima-distill grafted in — non-anima-native foundation may avoid the closure entirely. Falsifier: Llama Path A v2 achieves chat composite ≥ 0.5584 + Φ★ PASS simultaneously → substrate class swap viable
- H_115.3 (inference-compute bypass): few-shot in-context priming (BG-AU) or extended context window (BG-BC) may open n_coherent > 0. Falsifier: ICL n_coherent > 0 at any prompt length → context-space open
- H_115.4 (architecture-redesign bypass): CLM-3 retrain with different layer-13 norm injection (BG-BD SOC norm) or 17th-closure intervention. Falsifier: post-redesign 6-step chain does NOT reproduce → architectural-class extension

### Variables

- axis-A: closure axis (post-hoc adapter / train-time distill / cross-modal bridge / residual-stream probe)
- axis-B: layer depth (L0 / L0-L12 / L13 / L14-L15 / lm_head)
- axis-C: substrate (CLM v4 + Llama-3.2-3B Path A v2)
- axis-D: measurement method (logit lens / SAE / PCA / semantic bridge / iterative self-feed)
- axis-E: Φ★ axis (decoupled from chat-cap)
- axis-F: chat composite (target ≥ 0.5584)

### Criteria

- C1: all 4 formal closures L1-L4 hold simultaneously (Hc_609)
- C2: extended closures L5-L6 hold under semantic-bridge + iterative-self-feed test (Hc_660)
- C3: 6-step causal chain reproduces cross-method (≥4 measurement methods agree) (Hc_666)
- C4: Φ★ axis stability holds at PASS WHILE chat composite stays FAIL — decoupling empirically verified
- C5: at least one bypass path (H1-H4) remains open at theorem-close time (avoid premature universal-impossibility claim)

### Falsifiers (≥5)

- F1: LoRA SFT chat composite ≥ 0.5584 → L1 fails → Theorem 115 fails (Hc_609 kill)
- F2: Pβ distill chat-axis F-Pβ-3 PASS → L2 fails (Hc_609 kill)
- F3: tribev2 family produces token-meaningful signal → L3 fails (Hc_609 kill)
- F4: any probed layer L produces n_coherent ≥ 5/8 → L4 fails (Hc_609 kill)
- F5: BG-AU few-shot ICL produces n_coherent > 0 → H_115.3 bypass succeeds → 4-axis closure broken
- F6: CLM-3 retrain post-design does NOT reproduce 6-step chain → 16-closure not architectural-universal (Hc_666 weakening)
- F7: Llama-3.2-3B Path A v2 achieves chat composite ≥ 0.5584 + Φ★ PASS simultaneously → substrate-class swap viable (H_115.2 succeeds)
- F8: 17th closure discovered (extends 16-closure to 17+) → theorem version-bump required (Hc_660/Hc_666 extension)
- F9: Φ★ axis ↔ chat composite correlation > 0.5 in independent measurement → decoupling claim falsified

### Honest Limits (≥5)

- L1: "Theorem" is closure-under-evidence, NOT mathematical proof; 16 closures are empirical-failure list not deductive
- L2: 4 axes × 2 substrates is small N — sample-space of bypass paths under-explored
- L3: Korean-rank-102 lock-out at L13 is corpus-specific; English / Chinese / Japanese substrate-conditional behavior unknown
- L4: chat composite ≥ 0.5584 threshold is anima-internal benchmark — external chat-cap definitions may yield different verdicts
- L5: Φ★ axis ⊥ chat-cap "decoupled" claim assumes Φ★ measurement is well-defined post-LoRA; Φ★ instrument validity is itself under scrutiny
- L6: Lesson Q + L reconciliation (Q = quality, L = layer-lock; user's framing) is qualitative — formal Q+L joint metric pending
- L7: bypass paths H1-H4 are stated as predictions but not pre-registered with deadlines — risk of indefinite open-list
- L8: theorem statement evolved 4 → 6 → 16 closures within one cycle — versioning + closure-count inflation discipline absent

## Cross-links

- legacy: anima_115_architectural_4_closure_theorem_2026_05_05.md (original 4-closure source)
- legacy: anima_2026_05_05_cycle_close_decision_landed_2026_05_05.ai.md (6-closure extension)
- legacy: anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md (16-closure hard close)
- sister: Hc_618-622 CLM v5 design 4-axes (trinity → single design H)
- sister: Hc_623-626 emerge candidates D-H (4-method emerge taxonomy)
- sister: Hc_630-638 CLM-3 chat-objective + chat-cap paths 1/2/4 + B-axis brainstorm
- corollary: Llama-3.2-3B Path A v2 (non-anima-native foundation as path-of-record)
- cross-link: Hc_647-649 (intent + β' KoGPT2 + H5), Hc_654 (foundation Llama-3B)

## Migration TODO

- [ ] reviewer review draft + 3 source-doc cross-check
- [ ] assign new H_ID (next free, expected H_154~)
- [ ] write hypotheses/H_<ID>_theorem_115_chat_incapability.md from this draft
- [ ] update hypotheses/README.md index (new theorem-grade category)
- [ ] mark Hc_609 / Hc_660 / Hc_666 as merged
- [ ] BG-AU few-shot ICL execution (H_115.3 bypass test)
- [ ] BG-BC longer context window (H_115.3 alt)
- [ ] BG-BD SOC norm injection at L13 (H_115.4 architecture-redesign)
- [ ] Llama Path A v2 corollary path-of-record promotion (H_115.2)
- [ ] CLM v4 substrate-research-only reassignment (close chat-cap lane on CLM v4)
- [ ] formal Q+L joint metric definition
