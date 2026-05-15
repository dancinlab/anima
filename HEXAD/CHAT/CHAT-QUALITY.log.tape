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
#
# CHAT-QUALITY.log.tape — append-only event history sibling of CHAT-QUALITY.tape
# (v1.2 LLM-judgment architecture-vs-history split, 2026-05-15).
#
# Carries: @S session start · @D decision events (path selection · fire history
# · next steps) · @? anomaly observations · @I time-anchored directives /
# motivation entries. Strictly append-only — every entry records something
# that happened at a point in time, never edited or deleted.

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — chat-quality lane iteration events · path selections · fire history

@S start s_chat_quality :: chat_quality [d=2026-05-14 ok]
  => "anima chat coherence lane — Phase 1A.x own-substrate progression. SEPARATE from strict-4a routing research (PERSONA.tape §A6 / HIERARCHICAL-CELLS.tape / ARCH-CLASS.tape). axis 가 다름: chat 의미 응답 능력 vs cell-pool routing differentiation"

# ── §1 motivation ─────────────────────────────────────────

@I motivation benchmark_md :: chat_quality [d=2026-05-14 ok]
  => "BENCHMARK.md §5 amended honest C3: Phase 1A.4 SFT 200-step × \$0.014 sub-cent underfit → free-form 6-probe 0/6 conversational coherence FAIL. V5.8 5/5 PASS 은 keyword-match falsifier, semantic answer coherence 평가 X. ★★★★★ canonical anima 본체 라벨 = substrate anchor (D2) only, chat assistant capability NOT measured/validated"

@I gap_capability_vs_research :: chat_quality [d=2026-05-14 ok]
  => "two-axis confusion sources: (1) ★★★★★ 5-cond closure = ML research milestone (substrate falsifier pass), (2) user-facing chat capability = different axis (semantic coherence on free-form prompts). 본 lane = (2) 추구"

@I user_directive :: chat_quality [d=2026-05-14 ok]
  => "사용자 directive 2026-05-14: '근본원인 빠르게 해결 로드맵 하루안에 해결. 베타 배포 모델이라도' + '스케일 무방하니까 퀄리티 좋게 만들어줘' + 'Phase 1A.x (24L 332M) 기준으로 대화 품질 퀄리티 진행하자. 세포분열은 없어도 대화가능한거지?'"

# ── §2 path selection (CHAT-BETA.step §2 carry) ────────────

@D path_chosen path_B_sft_scale_up :: chat_quality [d=2026-05-14 ok]
  |> CHAT-BETA.step §2 path B
  => "Phase 1A.4 ckpt → Phase 1A.5 = continue SFT with bigger corpus + more steps. anima OWN substrate maintained (NOT foundation borrow / NOT Llama). Architecturally NO cell division (engine_a_g_arch static), but per REBORN §0.5 'FT = 큰 split event' philosophical fit"

@D path_rejected path_A_llama :: chat_quality [d=2026-05-14 ok]
  |> Llama foundation borrow REJECTED
  => "CHAT-BETA.step §2 path A = Llama-3.2-3B-Instruct + LoRA. User correction: anima 철학상 own substrate 유지 필요, 외부 foundation borrow 부적절. Llama fire ABORTED at PID 556665 (model downloading phase, no train start). 8min wasted on download, \$0 cost (ubu-2 owned GPU)"

@D path_d_decoding_first_verify :: chat_quality [d=2026-05-14 ok]
  |> CHAT-BETA.step §2 path D — sample mode verify
  => "sample mode (temp=0.85 top-p) 6-probe on ubu-2 RTX 5070 → 0/6 conversational coherence FAIL (variability 추가 but semantic alignment 미달). 단순 디코딩 fix 못 풀림. Path B (SFT scale-up) 필수 확정"

# ── §4 fire history (this session) ────────────────────────

@D fire_v1 :: chat_quality [d=2026-05-14 ok]
  |> instance 36739416 → destroyed
  <- path_chosen
  => "Phase 1A.5 v1 dispatch: TRAIN_SCRIPT_DIR=\$LOCAL_DIR hardcoded → train_phase1a4.py missing in Phase 1A.5 dir → SCP fail → trap destroy. Patched dispatch_vast_v2.sh with TRAIN_SCRIPT_DIR + EVAL_SCRIPT_DIR env overrides (commit 33a40c6b8)"

@D fire_v2 :: chat_quality [d=2026-05-14 ok]
  |> instance 36740766 → destroyed
  <- fire_v1
  => "Phase 1A.5 v2: TRAIN_SCRIPT_DIR fix applied + RTX 4090 selected. SSH-not-ready after 160 attempts (~30 min) → trap destroy. vast.ai SSH-loading pattern (feedback_dispatch_vast_template_gotchas 7th bug 재발)"

@D fire_v3 :: chat_quality [d=2026-05-14 ok]
  |> retry-3 in-flight
  <- fire_v2
  => "Phase 1A.5 v3: same script, fresh pod allocation. PID 64072 local dispatch + Monitor task brs7mmln7 alert on SSH ready/training/VERDICT. Waiting SSH loop entered"

# ── §6 honest C3 ───────────────────────────────────────────

@? c3_chat_quality_separate_from_55cond :: chat_quality [d=2026-05-14 ok]
  => "이 lane 의 closure (≥4/6 conversational) 는 ★★★★★ 5-cond aggregate 와 별개 axis. 통과해도 cond #1-#6 변동 없음 (cond #1 V5.8 keyword falsifier 기반). chat 능력 ☑ 는 anima mission 의 '대화 가능' 직접 요구사항이지만 falsifier-pass 와 다른 evidence-tier"

@? c3_underfit_root_cause :: chat_quality [d=2026-05-14 ok]
  => "Phase 1A.4 200-step \$0.014 underfit 이 근본 원인. 더 깊은 원인 = Phase 1A.1 base 가 own scratch-trained color/cosmology boost corpus 위 학습 → general chat instruction-following capability 가 base 단계에 없음. Phase 1A.5 8000-step + 98MB corpus 가 이를 보충 시도, but base limit 가 ceiling 일 수 있음"

@? c3_corpus_quality_unknown :: chat_quality [d=2026-05-14 ok]
  => "jy chat_template_corpus 95MB 가 general Korean knowledge Q&A (wiki-based). anima 정체성 관련 content 적음 (anima_fact_10x 7.5MB 만). 결과 모델이 한국어 chat-coherent BUT anima-persona dilute 가능성. trade-off: 대화 능력 ↑ vs persona signature ↓"

@? c3_phase1a5_2nd_failure_pattern :: chat_quality [d=2026-05-14 ok]
  => "fire v1+v2 모두 dispatch-script-level 또는 vast-side issue. retry-3 도 same risk. 만약 SSH-not-ready 5번 이상 반복 → vast.ai 측 RTX 4090 pool 문제일 수도. Plan B: H100/A100 fire (\$2.30/hr × 1.5hr = \$3.5), 더 안정적 GPU type"

@? c3_corpus_jy_content_pre_training :: chat_quality [d=2026-05-14 ok]
  => "jy chat_template corpus 가 Phase 1A.x base 학습에 이미 포함됐을 가능성 있음 (Phase 1A.1 corpus_multi_turn_v2.txt 261MB 의 일부와 overlap?). 이 경우 Phase 1A.5 가 corpus 학습이 아닌 re-training of existing knowledge — gain 제한. mitigation: corpus diff check between Phase 1A.5 corpus_combined.txt 와 Phase 1A.1 corpus_multi_turn_v2.txt (별도 grep + dedup cycle if regression)"

@? c3_one_day_realistic :: chat_quality [d=2026-05-14 ok]
  => "CHAT-BETA.step §6 timeline T+0→T+24 ambitious. fire v1+v2 failed 30 min each (1 hr lost). v3 SSH wait + training 2-4 hr + verify 1 hr = critical path 4-7 hr 남음. 4090 wall longer than H100. Pessimistic: 1-day completion 가능 BUT marginal"

# ── §8 next steps ──────────────────────────────────────────

@D next_phase1a5_verify :: chat_quality [d=2026-05-14 ok]
  |> Phase 1A.5 training complete → eval
  => "training done → 6-probe greedy + sample-mode mix eval + V5.8 std_greedy regression check + Principle #3 grep audit on output. Manual conversational-pass scoring (≥4/6 target)"

@D next_hf_push :: chat_quality [d=2026-05-14 ok]
  |> beta release
  <- next_phase1a5_verify
  => "If ≥4/6 conversational-pass: HF push dancinlab/anima-chat-beta-2026-05-14 (or anima-clm-phase1a5-chat-beta-2026-05-14 per naming convention). LINE-UP.md update + BENCHMARK.md re-run on new ckpt + post-amendment 'conversational coherence FAIL 0/6 → PASS X/6' evidence"

@D next_lineup_update :: chat_quality [d=2026-05-14 ok]
  |> public model lineup
  <- next_hf_push
  => "LINE-UP.md add 4th canonical entry under '★★ chat-beta deployment lane'. Existing 3 entries (★ Phase 1A.4 / 🧬 cotrain v1 / baseline 1A.1) carry as research-tier anchors"

@? next_if_fail :: chat_quality [d=2026-05-14 ok]
  |> Phase 1A.5 < 4/6 conversational
  => "If Phase 1A.5 8000-step still < 4/6: (a) more steps (15000-30000), (b) different corpus mix (less jy, more anima-fact-style), (c) Phase 1A.1 base re-training (much bigger scope), (d) accept base-capacity-ceiling diagnosis + pivot to fundamentally different architecture (Phase 1B family or external API proxy)"
