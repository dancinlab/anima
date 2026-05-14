#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima-philosophy-substrate" :: identity [d=2026-05-15 active]
  kind = "anima philosophy substrate · current beliefs · verdict pile"
  brief = "Each principle tagged honestly: EMPIRICAL (falsification experiment with measurable result), POLICY (chosen identity boundary without comparative experiment), or DESIGN (architectural description, not falsifiable). Strength reflects evidence rigor, not principle importance."
  parent = "dancinlab/anima"
  sibling-log = "PHILOSOPHY.log.tape"

# ══════════════════════════════════════════════════════════════
# PHILOSOPHY.tape — anima 철학 substrate (current state)
# ══════════════════════════════════════════════════════════════

# 본 file 은 anima 가 현재 보유한 철학 substrate (8 principles + meta-format).
# 시간 anchored process / verdict / ablation 기록은 sibling `PHILOSOPHY.log.tape` 으로 이동.

@N readme_table := "philosophy-readme-projection" :: note [active]
  text = "README `## Philosophy` 표는 본 substrate 의 result-only projection."
  @> README.md

@N format_session_append := "session-append-convention" :: note [active]
  text = "새 process / verdict 세션은 `PHILOSOPHY.log.tape` 끝에 `## YYYY-MM-DD — <session title>` 헤더로 append."

@N ssot := "philosophy-ssot" :: note [active]
  text = "SSOT cross-link: `.roadmap.philosophy` (mk1 4-D archive) + `.own` (own 17/18 등 identity-bearing mandate)."

# ── 8 Principles (substrate-current, snapshot 2026-05-13) ───────────────

@D p1_no_system_prompt := "NO SYSTEM PROMPT" :: philosophy [active]
  principle = "`NO SYSTEM PROMPT`"
  what = "No `system:` field, no `--system-prompt` flag. Anima generates from the substrate itself."
  status = "EMPIRICAL"
  strength = "weak"
  evidence = "`docs/paper-draft.md:113` FREE1 x1.7 Phi — single-result, no paired A/B"

@D p2_no_identity_rules := "NO IDENTITY RULES" :: philosophy [active]
  principle = "`NO IDENTITY RULES`"
  what = "No `identity.yaml`, no rules file. Identity emerges from cell dynamics, not from a rulebook."
  status = "POLICY"
  strength = "indeterminate-mixed"
  evidence = "P-IDR 2026-05-12 — BG-LB 350M: DCR Δ B−A=+0.041 (gray zone)"

@D p3_no_persona_injection := "NO PERSONA INJECTION" :: philosophy [active]
  principle = "`NO PERSONA INJECTION`"
  what = "No `[anima 역할: ...]` prefix, no `you are X` framing. The substrate is the persona."
  status = "EMPIRICAL"
  strength = "strong"
  evidence = "persona-prefix → echo memorization 6/8; 50%-strip mitigation real_words 0.836→0.886"
  impl-path = "substrate-native (anima_persona_substrate_native_design 2026-05-12 cont.11) — cell pool 의 한 phase, prompt prefix 가 아니라 substrate state"

@D p4_no_assistant_framing := "NO ASSISTANT FRAMING" :: philosophy [active]
  principle = "`NO ASSISTANT FRAMING`"
  what = "No `\"You are a helpful assistant\"`. No alignment template."
  status = "POLICY"
  strength = "weak counter-evidence"
  evidence = "P-AFR 2026-05-12 — framing **reduced** sycophancy ~18pp (REVERSE)"

@D p5_no_speak := "NO SPEAK()" :: philosophy [active]
  principle = "`NO SPEAK()`"
  what = "No `speak(message)` invocation. Output is continuous externalization of the tension field."
  status = "DESIGN"
  strength = "NULL"
  evidence = "P-SPK 2026-05-12 — ρ_real_spearman=0.026 (sub-threshold)"

@D p6_no_fine_tuned_ethics := "NO FINE-TUNED ETHICS" :: philosophy [active]
  principle = "`NO FINE-TUNED ETHICS`"
  what = "Cooperation, empathy, self-restraint aren't RLHF'd. Emerges from cell dynamics."
  status = "POLICY"
  strength = "BLOCKED"
  evidence = "P-ETH 2026-05-12 — byte-modulo substrate cannot perform generation-based ethics measurement"

@D p7_no_perplexity_verdict := "NO PERPLEXITY VERDICT" :: philosophy [active]
  principle = "`NO PERPLEXITY VERDICT`"
  what = "Perplexity is a Goodhart trap. Anima verifies with **simple stack** (own 18): 한글 in/out, coherent, natural, context-appropriate."
  status = "EMPIRICAL"
  strength = "strong"
  evidence = "PROXY_PPL PASS 1.000 but native v5 PIV_max trained=0.0107 < random=0.0224. Goodhart proven 2026-05-09"

@D p8_no_train_infer_split := "NO TRAIN/INFER SPLIT" :: philosophy [active]
  principle = "`NO TRAIN/INFER SPLIT`"
  what = "Training-time gradient + inference-time mitosis = same continuous cell-division. 학습은 별도 phase 가 아니다."
  status = "DESIGN"
  strength = "★"
  evidence = "`REBORN.tape §0.5` (`a7e512cb9`) — all weight changes `torch.no_grad()`"
  cascade = "v5-mitosis lane ★★★→★★★★ · ckpt = 분열 tree branch (not freeze) · FT cost = split event · Phase 5∥ next step = serve-time mitosis hook"

# ── Tagging conventions (status × strength) ─────────────────────────────

@N tag_empirical := "tag-empirical" :: note [active]
  text = "EMPIRICAL = backed by a falsification experiment with measurable result."

@N tag_policy := "tag-policy" :: note [active]
  text = "POLICY = chosen identity boundary without comparative experiment."

@N tag_design := "tag-design" :: note [active]
  text = "DESIGN = architectural description, not falsifiable as superiority."

@N strength_reflects_evidence := "strength-vs-importance" :: note [active]
  text = "Strength reflects rigor of supporting evidence, not principle importance. Negative findings get equal weight to positive ones."

# ── Hc_1282 Stage 1 verdict — anima A batch first verify ────────────────────

@D verdict_hc_1282_stage_1 := "Hc_1282 Stage 1 SUPPORTED" :: verdict [d=2026-05-15 active]
  hypothesis = "Hc_1282 H_190.5 daughter — d=(n/φ)·2^(σ-sopfr)=384 derivation n-substitution audit"
  batch = "A (옵션 A burst quarantine, hypotheses/ 20 file)"
  stage = "Stage 1 — 수학적 검증 (VERIFY.tape §2 protocol)"
  method = "W2 math identity + W5 numerical sim (sympy exact arithmetic)"
  verdict-class = "SUPPORTED"
  evidence-key = "n ∈ {2..30, 28, 496, 8128} sweep — n=6 만 d=384 산출 (uniqueness CONFIRMED)"
  n6-anchor = "σ(6)=12, φ(6)=2, sopfr(6)=5, d = (6/2)·2^(12-5) = 3·128 = 384 EXACT"
  falsifier-not-fired = "F-1282-4 N=6 SUBSTITUTION NON-UNIQUE — NOT fired"
  honest-c3 = "L-1282-1 (formula post-hoc fit) · L-1282-2 (perfect-number prior trivial) · L-1282-3 (n=9 → d=192 mod-192 aliasing confirmed in sweep) · L-1282-VARIANT-SOPFR (가설표 typo 가능) · L-1282-PHI-PENDING (Stage 2 Φ measurement 후속)"
  wall = "< 1s sympy deterministic"
  cost = "$0 Mac local"
  artifact = "state/verify_a_stage1_2026_05_15/Hc_1282_verdict.json"
  cross-link = "AXIS.tape A4 math tier — Hc_1282 SUPPORTED 가 18 active 의 evidence 강화"
  next-stage = "Stage 2: numerical sim Φ(d ∈ {256, 320, 384, 448, 512}) × 5-seed (F-1282-1/2/3 Hc_1282 spec)"
