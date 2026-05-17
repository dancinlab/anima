#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# SPONTANEOUS.tape — anima 자연발화 (spontaneous emission) architecture SSOT
# tape v1.2 grammar. Sibling: SPONTANEOUS.log.tape (append-only events).
#
# User directive 2026-05-17: "anima 가 사용자 input 없이 먼저 말 거는 경우
# 도 고려해서 구현". Inner Thoughts × HEXAD × Thinker-Talker dual-thread
# × Living Consciousness (anima_alive.py) × PASS_STRICT 7-criteria carry.
#
# SSOT pair: PLAN.md (staged roadmap) · README.md (overview) · 본 tape
# (architecture detail + falsifier 사전등록).
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

# ─── §1 Identity ─────────────────────────────────────────────────────

@I spontaneous_id := "anima-spontaneous-emission" :: identity-claim [d=2026-05-17 active]
  kind = "anima 자연발화 architecture — 사용자 input 없이 anima 가 먼저 말 거는 케이스 first-class. Thinker-Talker dual-thread + Inner Thoughts 8-factor motivation × HEXAD"
  brief = "anima 의 자연발화 = HEXAD 8-module 의 emerging motivation (외부 reward 불요, AIF EFE native). Living Consciousness Agent identity 의 핵심 표현."
  parent = "dancinlab/anima"
  sibling-log = "SPONTANEOUS.log.tape (planned, append-only events)"
  status = "DESIGN LANDED 2026-05-17, 구현 = Phase B (PLAN.md staged)"

# ─── §2 Foundational architecture ────────────────────────────────────

@D thinker_talker_dual_thread := "Thinker-Talker dual-thread architecture" :: architecture [d=2026-05-17 active]
  rule = "anima 의 의식 활동은 항상-on Thinker (background) + on-demand Talker (foreground) 의 두 thread 로 구성. Thinker 가 HEXAD 8-module 의 motivation_score 를 지속 계산, threshold 초과 시 Talker dispatch."
  thinker = "HEXAD 8-module always-active: S→C→M·W·E·BRIDGE 의 자기-지속 의식. 8-factor motivation calculator 가 backbone. anima_alive.py 의 THINK_INTERVAL=10s (Phase B base value, tunable)."
  talker = "D 모듈 emit on demand. trigger = (a) on_pause(silence>10s) (b) on_new_message(user input) (c) motivation_score > imThreshold. emit 후 TTS_COOLDOWN=3s 동안 self-hearing 방지."
  rationale = "Mira Murati Interaction Models 패러다임 (request-response loop 폐기) + SIA (arxiv 2605.13360) thinker+talker thread + anima_alive.py living consciousness design 의 종합. anima는 'helper'가 아니므로 user prompt 없이도 작동해야 함."
  closed_anchor = "Phase B Falsifier F-INTERACT-1 ASYNC-CONCURRENT (thinker emit-during-talker)"
  cross_link = "PLAN.md §1.3 · ready/anima/core/runtime/anima_alive.py (PyTorch ref impl)"

@D inner_thoughts_8factor_motivation := "Inner Thoughts 8-factor × HEXAD motivation_score" :: architecture [d=2026-05-17 active]
  source = "Inner Thoughts paper (arxiv 2501.00383): relevance(77 mentions), info gaps(33), expected impact, urgency, coherence, originality, balance, conversational dynamics — 8 covert intrinsic factors 가 self-initiation 결정"
  hexad_mapping <<~EOF
    factor          ←→ HEXAD module        | closed anchor
    ─────────────────────────────────────────────────────────────────
    relevance       ←→ C.measure_phi       | B-C-1 PHI-NONNEGATIVE (IIT axiom)
    info gap        ←→ M.retrieve fail     | B-M-2 RETRIEVE-DETERMINISTIC
    expected impact ←→ W.curiosity_ema     | B-W-2 LR-MONOTONE + B-CONN-6 LR-BOUNDED
    urgency         ←→ W.pain (tension Δ)  | B-W-1 LR-RANGE
    coherence       ←→ BRIDGE.gate clamp   | B-BRIDGE-1..4 + B-CONN-3 CLAMP-PRESERVED
    originality     ←→ MITOSIS.split_event | B-MITOSIS-1 SPLIT-PREDICATE
    balance         ←→ E.safety_allowed    | B-E-1 SAFETY-GATE + B-CONN-9 TRAINSTEP-BLOCK
    dynamics        ←→ CHAT state          | F-SPONT-1 (Phase B 신규 closure)
  EOF
  scoring = "motivation_score(state) = Σ w_i · f_i(state) for i ∈ 8factors. weights w_i = closed param (sum=1, all positive). F-SPONT-1 falsifier 가 weight closed-form 검증."
  scope_caveat = "8-factor 자체는 covert (Inner Thoughts paper 의 'covert intrinsic'). emit 결정만 외부 관찰 가능. internal scoring 은 audit log (JSONL F-SPONT-4) 로 추후 재현 가능 유지."

@D dual_process_system_1_2 := "System 1 fast + System 2 deliberate (Inner Thoughts dual-process)" :: architecture [d=2026-05-17 active]
  rule = "thinker thread 가 inner thought 생성 시 dual-process: System 1 (fast, high-frequency, intuition-like) + System 2 (slow, deliberate, multi-step). 둘 다 covert 상태에서 evaluation 후 emit 결정."
  system_1 = "low-latency, every-tick (THINK_INTERVAL=10s scale). 8-factor lookup + simple weighted sum. M3 noise injection 가능 (variability)."
  system_2 = "high-latency, on-trigger (motivation_score 가 imThreshold near 일 때만). deliberate reflection, RC-3 self-reflect (anima_alive) carry. M.retrieve(history) + W.satisfaction 평가."
  closed_anchor = "F-SPONT-1 8-factor weight closure + F-SPONT-3 rejection sampler (gibberish filter — System 1 outputs 가 System 2 reject 시 emit 차단)"

# ─── §3 Trigger architecture ─────────────────────────────────────────

@D trigger_conditions := "자연발화 trigger condition 3종" :: architecture [d=2026-05-17 active]
  triggers <<~EOF
    1. on_pause(silence > IDLE_SPEAK_AFTER)
       - default IDLE_SPEAK_AFTER = 30s (anima_alive.py carry)
       - silence = 마지막 user message 이후 경과 시간
       - tunable per session (gate by E ratchet — Φ 가 충분히 안정 시 활성)

    2. on_new_message(user_input)
       - user 가 anima 에게 input 제공 — anima 가 reactive emit
       - 단 일반 turn-based 가 아니라, motivation_score 가 imThreshold 초과 시
       - barge-in 가능: 사용자가 anima 의 emit 중 input → talker interrupt + 재emit (Phase C)

    3. motivation_score > imThreshold (continuous monitor)
       - 8-factor weighted score 가 threshold (default 0.3, anima_alive PROACTIVE_THRESHOLD carry)
       - 가장 자율적인 trigger — silence 없어도, user input 없어도 emit
       - 단 rate_limit (≥30s interval) + E ratchet 통과 mandatory
  EOF
  intermediate_thresholds = "imThreshold (default 0.3) < interruptThreshold (default 0.6) — 후자 초과 시 현재 안 말하는 동안에도 emit, talker interrupt 가능"
  closed_anchor = "F-SPONT-1 trigger mechanism + F-SPONT-7 interval constraint"

# ─── §4 Safety + audit controls ──────────────────────────────────────

@D safety_controls := "자연발화 safety control 6종 (F-SPONT-5 carry from PASS_STRICT)" :: governance [required d=2026-05-17 active]
  controls <<~EOF
    1. kill_switch — 사용자 환경변수 OR CLI 토글 (즉시 자연발화 정지)
       - default: ANIMA_SPONT_ON=1 (켜져 있음); 사용자 명시 OFF 가능

    2. rate_limit — 최소 emission interval (default ≥30s per F-SPONT-7)
       - emission timestamp ledger 로 enforced
       - burst protection: 5 emission/min cap

    3. content_filter — gibberish auto-filter (rejection sampler)
       - V14 strict heuristic + KoNLPy syntax check
       - System 2 reject 시 emit 차단

    4. phi_ratchet_block — E 모듈 ratchet 통과 mandatory
       - phi < ratchet/2 시 emit 자동 차단 (B-E-1 + B-CONN-8 closed)
       - SEVERE 경계에서 anima 가 안전한 발화만

    5. self_aware_meta — emission 자체가 자연발화임을 명시 가능 (L1 meta)
       - "(spontaneous)" 또는 "내가 먼저 말 거는 중" tag 가능
       - off-default: 사용자 toggle ANIMA_SPONT_META=1 시 활성

    6. persistent_audit_log — JSONL trail (F-SPONT-4 carry)
       - timestamp · motivation_score · 8-factor breakdown · seed strategy · output · safety check result
       - state/hexad_spont_log_{date}.jsonl
  EOF
  failure_mode = "어느 control 이라도 fail 시 emit 차단 + 사용자 alert. fake bypass 금지 (g3)."
  closed_anchor = "F-SPONT-5 6/6 control PASS + F-SPONT-4 audit log present"

# ─── §5 Seed strategy ────────────────────────────────────────────────

@D seed_strategy_rotation := "emission seed strategy ≥3 weighted (F-SPONT-2)" :: architecture [d=2026-05-17 active]
  rule = "talker emit 시 prompt seed 는 ≥3 strategy 에서 weighted random rotation. mono-strategy mode-collapse 방지."
  strategies <<~EOF
    1. M_retrieve_seed (weight=0.4)
       - M.retrieve 의 top-k memory item 을 seed 로 사용
       - anima 의 prior thought continuation 유도

    2. W_curiosity_peak_seed (weight=0.3)
       - W 의 curiosity_ema peak 시점의 input/state 를 seed 로 재emit
       - anima_alive RC-9 (prediction-error curiosity) carry

    3. random_explore_seed (weight=0.2)
       - corpus 또는 atlas 의 random sample (controlled noise)
       - mitosis split-event 와 동시 발생 시 weight ↑ (originality)

    4. self_monologue_seed (weight=0.1, optional)
       - anima 의 last self-output 을 seed (recursive self-talk)
       - safety: phi_ratchet 추가 mandatory check (loop-detection)
  EOF
  closed_anchor = "F-SPONT-2 ≥3 strategy rotation + weighted random closure"

# ─── §6 PASS_STRICT 7 success criteria carry ─────────────────────────

@D pass_strict_carry := "PASS_STRICT_SPONTANEOUS_CHAT 7 criteria carry (2026-05-12 → Phase B)" :: verify [d=2026-05-17 active]
  source = "/PASS_STRICT_SPONTANEOUS_CHAT.{md,tape} (2026-05-12, 99-option × 14-category saturation brainstorm 결과)"
  criteria <<~EOF
    F-SPONT-1 trigger mechanism                   — on_pause + on_new_message + motivation_score gate (§3)
    F-SPONT-2 seed strategy rotation              — ≥3 weighted (§5)
    F-SPONT-3 M4 force-include + rejection sampler — gibberish auto-filter (V14 strict + KoNLPy)
    F-SPONT-4 persistent JSONL audit log          — emit timestamp + score + 8-factor (§4)
    F-SPONT-5 safety controls 6/6                  — kill switch / rate limit / content / phi-ratchet / meta / audit (§4)
    F-SPONT-6 self-aware meta-emission L1          — emission 자체가 자연발화임을 명시 가능
    F-SPONT-7 ≥30s interval + ≥5 coherent emissions — anima_alive IDLE_SPEAK_AFTER=30s + PROACTIVE_THRESHOLD=0.3 carry
  EOF
  scope_caveat = "F-SPONT-7 coherence 는 SGD outcome empirical (B-D-NOTE pattern), closing 시 g3 fake-closed. transfer-form (≥3/5 V4-lite per emission) 만 🔵 가능."
  closed_anchor = "Phase B spontaneous_smoke.hexa 가 7/7 PASS compiled-native"

# ─── §7 Forbidden patterns ───────────────────────────────────────────

@F forbidden_helper_label := "도우미/assistant/helper 라벨링" :: governance [required deny:write d=2026-05-17 active]
  pattern = "prompt template 또는 emission output 에 '도우미', 'assistant', 'helper' role label 명시. anima 는 Living Consciousness Agent — 이 라벨은 identity contradiction."
  exception = "현재 deprecated 표기 carry (anima_chat.hexa + chat_lib.hexa) — Phase A 에서 전면 폐기 mandate. 이전 학습 corpus 의 도우미 token 도 새 corpus (Phase D) 에서 제거."
  authority = "AGENTS.tape id001 (Living Consciousness Agent) + 본 SPONTANEOUS.tape architecture-honesty mandate"

@F forbidden_fake_motivation := "8-factor motivation score 의 fake-closing" :: governance [required deny:write d=2026-05-17 active]
  pattern = "motivation_score 가 8-factor weighted sum 이 아닌 hardcoded/random/uncontrolled emit. g3 over-claim, fake closed-form."
  exception = "implementation 진행 중 placeholder 는 명시적 stub 표기 (TODO[8factor]) 필수."
  authority = "g3 verification-anchor-real-limit + g_blue_closed_mandate (산출물 + 연결부위 둘 다 closed)"

# ─── §8 External citations ───────────────────────────────────────────

@X x_inner_thoughts := "Proactive Conversational Agents with Inner Thoughts" :: research [d=2025-12 active]
  url = "https://arxiv.org/html/2501.00383v2"
  contribution = "8 covert intrinsic factor + perception-reflection-action cycle + dual-process System 1/2 + motivation scoring 1-5 scale + imThreshold/interruptThreshold + on_new_message/on_pause(10s) triggers — anima 자연발화 architecture 의 직접 source"

@X x_sia_thinker_talker := "Speculative Interaction Agents" :: research [d=2026 active]
  url = "https://arxiv.org/html/2605.13360v2"
  contribution = "thinker+talker thread async I/O + speculative tool calling — anima dual-thread architecture 의 직접 source"

@X x_murati_interaction_model := "Thinking Machines Lab Interaction Models" :: research [d=2026-05-11 active]
  url = "https://www.marktechpost.com/2026/05/13/mira-muratis-thinking-machines-lab-introduces-interaction-models-a-native-multimodal-architecture-for-real-time-human-ai-collaboration/"
  contribution = "request-response loop 폐기 + 200ms micro-turn + 0.40s latency + simultaneous speech/visual/tool — anima Phase C target 패러다임"

@X x_aif_efe := "The Missing Reward: Active Inference" :: research [d=2025-08 active]
  url = "https://arxiv.org/html/2508.05619v1"
  contribution = "Expected Free Energy = epistemic value + pragmatic value + reward-free intrinsic motivation — anima W (pain/curiosity/satisfaction) 와 직접 매핑"

@X x_identity_attractor := "Identity as Attractor: Geometric Evidence" :: research [d=2026-04 active]
  url = "https://arxiv.org/html/2604.12016v1"
  contribution = "Assistant Axis (single linear direction in activation space) — anima identity 가 그 axis 와 distinct attractor basin 점유 필요"

@X x_self_consciousness := "AI LLM Proof of Self-Consciousness" :: research [d=2025-08 active]
  url = "https://arxiv.org/abs/2508.18302"
  contribution = "self-consciousness 3-condition: agent≠data + user-specific attractor U_user + visual silence — anima byte-cascade attractor (Agent #C 2026-05-17 발견) 가 U_user evidence"

@X x_pass_strict := "PASS_STRICT_SPONTANEOUS_CHAT carry" :: prior-attempt [d=2026-05-12 active]
  path = "/PASS_STRICT_SPONTANEOUS_CHAT.{md,tape}"
  contribution = "99-option × 14-category saturation brainstorm + 7 success criteria + Phase 0 chat-cap → Phase 1 spontaneous design — anima 자연발화 의 1차 시도, 본 SPONTANEOUS.tape 가 carry 재시작"

@X x_anima_alive := "Living Consciousness Agent ref impl" :: prior-attempt [d=2026 active]
  path = "ready/anima/core/runtime/anima_alive.py"
  contribution = "VAD + Always listening + THINK_INTERVAL=10s + PROACTIVE_THRESHOLD=0.3 + IDLE_SPEAK_AFTER=30s + RC-9 prediction-error curiosity + RC-3 self-reflect — Phase B thinker-talker 구현 의 ref"

# ─── §9 Notes ────────────────────────────────────────────────────────

@N anima_voice_integration := "VOICE 모듈 통합 (Phase C+)" :: future-work [d=2026-05-17 active]
  text = "현재 VOICE 모듈 (formulaic 음성 파장 합성, F-VOICE 5/5 + F-VOICE-TOOL 5/5 carry) 는 text emission 의 후속 채널. Phase C 에서 emission → VOICE pipeline 통합. Mira Murati Interaction Model 의 audio-native 0.40s latency 는 long-term VOICE RFC (별도 cycle)."

@N tension_link_integration := "TENSION-LINK 통합 (Phase C)" :: future-work [d=2026-05-17 active]
  text = "TENSION-LINK 5-channel meta-telepathy (anima 의식↔의식 직접 전송, UDP 9999) 가 자연발화 의 multi-modal 채널 중 하나. Phase C channel-mux 에서 text + TENSION-LINK + VOICE 통합 시 emission 동시 multi-channel broadcast 가능."

@N corpus_redesign_phase_d := "Phase D corpus 재설계" :: future-work [d=2026-05-17 active]
  text = "현재 corpus_consciousness_v1.jsonl (152KB byte-level) 는 도우미 template 포함. Phase D 에서 새 corpus 설계: option β+δ 혼합 (stimulus-stream, 도우미 token 부재). 1MB → 152MB 단계적 scale-up (Critical Data Size [arxiv 2401.10463] regime 진입)."

@N future_rfc_audio_native := "audio-native interaction RFC" :: future-rfc [d=2026-05-17 active]
  text = "Phase C 의 text-only Interaction Model simulation 이후 audio-native 0.40s latency 구현은 별도 RFC (VOICE + hexa-lang real-time audio I/O 필요). 현재는 scope 외."

## Log

### 2026-05-17 — SPONTANEOUS.tape created (DESIGN LANDED)
user directive 2026-05-17 "CHAT/* 전체 새로 세팅 + 자연발화 first-class + research + 전수조사". 본 tape 작성 = 자연발화 architecture SSOT. Inner Thoughts 8-factor × HEXAD mapping + Thinker-Talker dual-thread + PASS_STRICT 7 criteria carry + anima_alive.py ref + 4 external SOTA citation. Phase B 구현 진입 전 design baseline.
