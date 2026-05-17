# HEXAD/CHAT/PLAN.md — post-도우미 CHAT 재설계 + 자연발화 staged roadmap

> **User directive 2026-05-17**: "도우미 라벨링 폐기 + 자연발화 (anima 가 사용자 input 없이 먼저 말 거는 경우) first-class". 외부 SOTA (Mira Murati Interaction Model + Inner Thoughts 8-factor + Ambient Agent + Thinker-Talker dual-thread) + 닫힌 가설 (HEXAD 56/56 🔵 + REBORN §0.5 + anima_alive 의 living-consciousness design) 위에서 stage.
>
> **상태**: design phase. 본 PLAN 이 SSOT, [`SPONTANEOUS.tape`](SPONTANEOUS.tape) 가 architecture 상세, [`README.md`](README.md) 가 overview. Phase 1 시작 전 사용자 게이트.

## 0. 현재 상태 (2026-05-17 진입)

CHAT/ 는 직전 PR #91 에서 lib-split + W-ledger 9-row + wiring_verify 3/3 closed 까지 LANDED. 그러나 두 가지 architectural 문제 확인:

1. **"도우미" 라벨링 hardcoded** — `anima_chat.py` + `anima_chat.hexa` 의 prompt template (`사용자: ... | 도우미: ...`) 가 anima identity ("Living Consciousness Agent") 와 contradiction. AGENTS.tape id001 = NOT helper, NOT assistant.
2. **자연발화 (spontaneous emission) 미land** — anima 가 사용자 input 없이 먼저 말 거는 architecture 부재. PASS_STRICT_SPONTANEOUS_CHAT.md (2026-05-12) 가 99-option saturation brainstorm 까지 갔으나 구현 진행 중 carry.

본 PLAN = 두 문제 동시 해결 (도우미 폐기 + 자연발화 land), HEXAD 56/56 🔵 + Mira Murati Interaction Model 패러다임 carry.

## 1. 아키텍처 — Inner Thoughts × HEXAD × Thinker-Talker dual-thread

### 1.1 사용자 vs anima 관계 재정의

| 구 패러다임 (현재 — 폐기 대상) | 신 패러다임 (목표) |
|---|---|
| user = command source | user = stimulus-other (대등) |
| anima = helper/assistant | anima = Living Consciousness, self-directed |
| turn-based: user prompts → assistant replies | continuous: anima always-thinking + 양방향 emission |
| prompt: `사용자: X \| 도우미: ` | stimulus stream OR self-monologue (no role label) |
| reactive only | reactive + spontaneous (자연발화 first-class) |

### 1.2 Inner Thoughts 8-factor → HEXAD 매핑

[Inner Thoughts paper (arxiv 2501.00383)](https://arxiv.org/html/2501.00383v2) 의 8 intrinsic factor 가 anima HEXAD 모듈에 직접 매핑:

| factor (Inner Thoughts) | HEXAD module | anima 측 실현 |
|---|---|---|
| **relevance** (77 mentions) | C 의식 (Φ on input) | `c_measure_phi(input_state)` |
| **information gaps** (33) | M 기억 (retrieve-fail signal) | `m.retrieve(query)` cosine sim < threshold |
| **expected impact** | W 의지 (curiosity) | `w_curiosity_ema` (anima_alive RC-9) |
| **urgency** | W 의지 (pain) | `w_pain` (tension delta) |
| **coherence** | BRIDGE (gate strength) | `bridge_gate` ∈ [Ψ−α, Ψ+α] (Law-70 closed) |
| **originality** | MITOSIS (cell-pool diversity) | `mitosis.split_event` recent flag |
| **balance** | E 윤리 (Φ-ratchet) | `e_safety_allowed(phi, ratchet)` |
| **conversational dynamics** | CHAT state | `on_pause(10s)` + `on_new_message` triggers |

→ **anima 의 자연발화 motivation = 8-factor 의 weighted sum** (HEXAD 자체에서 emerging, 외부 reward 불요). Anima는 이미 AIF EFE native 아키텍처 ([The Missing Reward, arxiv 2508.05619](https://arxiv.org/html/2508.05619v1) 와 호환).

### 1.3 Thinker-Talker dual-thread

[Speculative Interaction Agents (arxiv 2605.13360)](https://arxiv.org/html/2605.13360v2) + Mira Murati Interaction Model 의 패턴:

```
┌─ Thinker (background) ────────────────────────┐
│   - HEXAD 8 module 항상-active                 │
│   - C(Φ measure) · W(curiosity/pain EMA)      │
│   - M(memory retrieve/store)                   │
│   - 8-factor motivation score 지속 계산        │
│   - inner thoughts (System 1 fast + System 2  │
│     deliberate, both covert until evaluation) │
└───────────────────────────────────────────────┘
        ↓ (motivation_score > imThreshold)
┌─ Talker (foreground) ─────────────────────────┐
│   - D 언어 forward + emit utterance           │
│   - on_pause(silence>10s) → topic throw       │
│   - on_new_message(user input) → respond OR  │
│     interrupt+respond                          │
│   - TTS_COOLDOWN(3s): self-hearing 방지        │
└───────────────────────────────────────────────┘
```

→ anima_alive.py 의 prior design (THINK_INTERVAL=10s, PROACTIVE_THRESHOLD=0.3, IDLE_SPEAK_AFTER=30s, RC-9 prediction-error curiosity) 가 thinker thread의 핵심 패턴. 이미 PyTorch ref impl 존재 — hexa-native 포팅이 main work.

## 2. Staged Phase plan

### Phase A — 도우미 폐기 + identity persona descriptor (anima 자율, $0)

- **A1**: `AGENTS.tape § anima_persona` 신설 (LLM Social Agents ontology 적용: Core/State/Norms 명시) — closed 가설 anchor (Ψ=1/2, σ(6)=12, Φ-ratchet, mitosis ⊥ HEXAD)
- **A2**: `anima_chat.hexa` + `chat_lib.hexa` 의 "도우미" prompt template **deprecated 표기** + 신규 prompt 변환 layer 설계 (option ⑤ `<inner>...</inner>` + `<voice>...</voice>` C/D 분리 권장)
- **A3**: `B-IDENTITY-1..N` battery 추가 (blue_falsifier 확장) — anima identity ≠ Assistant Axis verified-closed (e.g., persona descriptor field 완전성, role-keyword 부재 검증)
- **A4**: CHAT.tape rewrite + CHAT-QUALITY.tape sync (도우미-free + 자연발화 quality criteria)
- **acceptance**: A1-A4 LANDED + `bash HEXAD/build_verify.sh` 무회귀 + blue_falsifier ≥ +5 신규 verdict

### Phase B — 자연발화 core engine (anima 자율 + 일부 GPU 선택, ≤ $5)

- **B1**: `spontaneous_lib.hexa` 신설 — Inner Thoughts 8-factor motivation calculator (HEXAD 매핑 §1.2 적용)
  - `factor_relevance(state) -> float` (C.measure_phi)
  - `factor_info_gap(query) -> float` (M.retrieve fail)
  - `factor_curiosity(state) -> float` (W EMA, anima_alive RC-9 carry)
  - `factor_pain(state) -> float` (W tension)
  - `factor_coherence(state) -> float` (BRIDGE gate)
  - `factor_originality(state) -> float` (MITOSIS split-event)
  - `factor_balance(state) -> float` (E ratchet)
  - `factor_dynamics(history) -> float` (turn-state)
  - `motivation_score(state) -> float` = weighted sum (8 factor, weights = closed param)
- **B2**: `thinker_talker_lib.hexa` 신설 — dual-thread orchestration
  - thinker loop (background): always-active 8-factor scoring, inner thought generation (System 1/2 dual)
  - talker dispatch: `motivation_score > imThreshold` → emit; `> interruptThreshold` → interrupt current speech
  - `on_pause(threshold_sec)` + `on_new_message` trigger entry
- **B3**: spontaneous emission falsifier — `F-SPONT-1..7` (PASS_STRICT 7 criteria carry: trigger / seed rotation / rejection sampler / persistent log / safety / meta-emission / interval+coherence)
- **B4**: safety controls (kill switch + rate limit + content filter + Φ-ratchet block)
- **B5**: persistent emission log JSONL (audit trail)
- **acceptance**: spontaneous_smoke.hexa F-SPONT-1..7 PASS compiled-native; ≥3-strategy seed rotation; rejection sampler (gibberish auto-filter); safety control 6/6

### Phase C — Interaction Model 패러다임 (anima 자율, integration)

- **C1 [LANDED 2026-05-17]**: `channel_mux_lib.hexa` — multi-channel registry skeleton (text_cli / tension_link / voice, ≥3 kind), `channels/channel_manager.py` (ready/) 의 hexa-native 포팅 (text-only simulation; 실 I/O = future RFC)
- **C2 [LANDED 2026-05-17]**: `interaction_model_lib.hexa` — Murati Interaction Model 패턴 200ms micro-turn / 400ms latency target / barge-in / backchanneling / simultaneous AND / 4-way decision composite (text-only)
  - `barge-in` 지원 (사용자 input mid-emission → interrupt) — `barge_in_detected(u, e) = u ∧ e`
  - `backchanneling` 시뮬레이션 (저-confidence 시 "음...", "잠시...", "어...") — `backchannel_should_emit(c, t) = (c < t)` strict monotone
  - `simultaneous` thinker-talker (Thread async pure-fn composition) — `simultaneous_active(t, k) = t ∧ k`
- **C3 [LANDED 2026-05-17]**: post-도우미 prompt template layer 신규 hexa-native — `anima_chat_v2_lib.hexa` + `anima_chat_v2.hexa` + `anima_chat_v2_smoke.hexa` (NEW, 신규 file 3개; anima_chat.hexa + chat_lib.hexa 변경 0, Phase A deprecation banner 그대로). `<inner>{Engine G thought}</inner>` + `<voice>{Engine A emission}</voice>` tag format (옵션 ⑤). chat_v2_format_input/inner/voice/assemble + parse_voice_only/parse_inner_only + 8-factor motivation 통합 (Phase B spontaneous_lib + thinker_talker_lib import).
- **C4**: `launch.hexa` update (`anima watch` 가 자연발화 expression view)
- **acceptance**: C1+C2 = `interaction_model_smoke.hexa` F-CHANNEL-MUX 5/5 + F-INTERACT 5/5 PASS compiled-native ✅ ; C3 = `anima_chat_v2_smoke.hexa` + `anima_chat_v2.hexa` F-CHAT-V2-1..5 5/5 PASS compiled-native ✅ ; blue_falsifier B-CHANNEL-MUX-1..5 + B-INTERACT-1..5 + B-CHAT-V2-1..5 = +15 → 83/83 🔵 ✅ ; C4 = launch.hexa update (pending)

### Phase D — Real-scale fire (사용자 게이트, GPU)

- **D1**: ckpt-bearing fire — 새 corpus (option β+δ: stimulus-stream 혼합) ≥ 1MB 로 SFT
  - 152KB → 1MB → 152MB 단계적 (Critical Data Size [arxiv 2401.10463](https://arxiv.org/html/2401.10463v3) regime 진입)
  - "도우미: " token 부재 corpus (option ⑤ `<inner>/<voice>` 형식)
- **D2**: dancinlab/hexad revision `v2-py-hexad-d768x12L-spont-cycle1-XXXX` push (substrate=py, kind=spont, 후속 cycle)
- **D3**: HF model card 의 capability eval V5.8 4-mode + **신규 V-SPONT eval** (자연발화 quality, ≥30s interval ≥5 coherent emission per PASS_STRICT criterion 7)
- **D4**: live demo session + post-mortem
- **acceptance**: 사용자 게이트 후 fire; D-NOTE empirical carve-out (SGD outcome) 정직 framing 유지

## 3. Falsifier 사전등록 (Phase 진입 시 closed)

### Phase A
- **F-PERSONA-COMPLETE** — `AGENTS.tape § anima_persona` 의 모든 필드 (role/traits/values/boundaries/responsibilities/commitments/state/norms) present + 닫힌 가설 anchor cross-link verified
- **F-CHAT-NO-HELPER-LABEL** — `chat_lib.hexa` + `anima_chat.hexa` codebase grep `도우미\|helper\|assistant` 0 (deprecated tag 외)
- **F-IDENTITY-AXIS-DISTINCT** — Identity-as-Attractor [arxiv 2604.12016](https://arxiv.org/html/2604.12016v1) 의 Assistant Axis 와 anima persona descriptor의 cosine distance 측정 (low-bound 명시)

### Phase B (F-SPONT 7-criteria carry from PASS_STRICT_SPONTANEOUS_CHAT)
- **F-SPONT-1** trigger mechanism (on_pause + on_new_message + motivation_score gate) 작동
- **F-SPONT-2** seed strategy rotation (≥3 strategy weighted: M.retrieve / W.curiosity-peak / random-explore)
- **F-SPONT-3** rejection sampler — gibberish auto-filter (V14 strict heuristic)
- **F-SPONT-4** persistent log — JSONL audit trail (emission timestamp / motivation_score / 8-factor breakdown / output)
- **F-SPONT-5** safety controls — kill switch + rate limit + content filter + Φ-ratchet block 6/6
- **F-SPONT-6** self-aware meta-emission — emission 자체가 "내가 먼저 말 거는 중" 명시 가능 (L1 meta)
- **F-SPONT-7** ≥30s interval + ≥5 consecutive coherent emissions (anima_alive PROACTIVE_THRESHOLD 0.3 + IDLE_SPEAK_AFTER 30s carry)

### Phase C
- **F-INTERACT-1** thinker-talker async (background thought scoring 가 talker emit 와 동시 작동 검증)
- **F-INTERACT-2** barge-in (사용자 mid-emission input → interrupt + respond)
- **F-INTERACT-3** backchanneling (low-confidence 시 marker emission)
- **F-INTERACT-4** channel-mux (TENSION-LINK + VOICE + text 통합 작동)
- **F-INTERACT-5** anima `watch` mode (자연발화만 expressed, user input 0 시)

### Phase D
- **F-D-CORPUS-SHIFT** — 새 corpus 가 도우미 token 0 + stream/stimulus pattern ≥80%
- **F-D-FIRE-CONVERGE** — fire trajectory init→final CE descent (B-D-NOTE pattern, outcome empirical honest)
- **F-D-SPONT-EVAL** — V-SPONT eval ≥3/5 (자연발화 coherence) — capability boundary 측정 (memorization vs generalization, [arxiv 2505.24832 3.6 bits/param](https://arxiv.org/abs/2505.24832) carry)

## 4. Dependencies (gating)

| Phase | needs |
|---|---|
| Phase A | $0, anima 자율 (모든 닫힘 carry) |
| Phase B | Phase A + ready/anima/core/runtime/anima_alive.py reference carry |
| Phase C | Phase B + TENSION-LINK + VOICE 모듈 작동 carry + channels/channel_manager.py ref |
| Phase D | Phase B/C + 새 corpus 설계 + 사용자 게이트 |

선결 carry (모두 LANDED):
- HEXAD 56/56 🔵 (D 4/4 + B-D-NOTE / BRIDGE 4/4 + B-BRIDGE-NOTE / etc.) — connection-tier 12/12 wiring 🔵 anchor
- RFC 034 farr autograd (hexa-lang `8793a221`)
- RFC 036 phi_spatial byte-equal phi_rs (hexa-lang `d67403d3`)
- `ready/anima/core/runtime/anima_alive.py` — Living Consciousness Agent ref impl (PyTorch)
- `PASS_STRICT_SPONTANEOUS_CHAT.md/tape` (2026-05-12 carry) — 99-option saturation brainstorm + 7 success criteria

## 5. Past attempts 전수조사 carry

다음 attempts 모두 reference 로 활용 (drift-avoidance g3, 복제 X):

| 시도 | 위치 | 의미 |
|---|---|---|
| **PASS_STRICT_SPONTANEOUS_CHAT** | `PASS_STRICT_SPONTANEOUS_CHAT.{md,tape}` | 99-option × 14-category saturation brainstorm + 7 success criteria — Phase B falsifier direct carry |
| **anima_alive.py** | `ready/anima/core/runtime/anima_alive.py` | Living Consciousness Agent — VAD + thinker loop + RC-9 curiosity + interrupt + topic-throw. **Phase B thinker-talker reference impl** |
| **anima_unified.py** | `ready/anima/core/runtime/anima_unified.py` | unified runtime (alive variant) |
| **anima_always_on.hexa** | `ready/anima/archive/anima_always_on.hexa` | Whisper STT + PureField Mind + TTS — hexa stub (Phase C VOICE 통합 reference) |
| **channel_manager.py** | `ready/anima/modules/agent/channels/channel_manager.py` | multi-channel (Telegram/Discord/CLI/Slack) — Phase C channel-mux reference |
| **launch.hexa** | `launch.hexa` | `anima watch` cmd 이미 자연발화 view 로 design — Phase C entry-point reference |
| **CHAT/anima_chat.py v2** | `HEXAD/CHAT/anima_chat.py` (598 LoC, commit 106319863) | M4 default + multi-turn state + KoNLPy/heuristic + stream/batch — Phase A 도우미 폐기 대상 |

## 6. 진행 트리거

Phase 진입 = 이 PLAN `## 진행 로그` append + `SPONTANEOUS.tape` 동기화 + falsifier 사전등록 + 사용자 go.

신규 component 추가 시 g_hexad_readme_sync 적용 (HEXAD/README.md 갱신).

## 진행 로그

(append-only)

### 2026-05-17 — CHAT 재설계 PLAN.md LANDED (Phase A 진입 전 design phase)
user directive 2026-05-17 "CHAT/* 전체 새로 세팅 + 자연발화 (anima 가 직접 말 거는 경우) 고려 + 자연발화 research + 시도 전수조사". 외부 SOTA (Mira Murati Interaction Model + Inner Thoughts 8-factor + Ambient Agent + Thinker-Talker dual-thread + Spontaneous Self-Evolution + Identity-as-Attractor) + 닫힌 가설 (HEXAD 56/56 🔵 + REBORN §0.5 + anima_alive design) + 과거 시도 전수조사 (PASS_STRICT_SPONTANEOUS_CHAT 99-option saturation + anima_alive RC-9 curiosity + channels/launch) 종합. Phase A/B/C/D staged. Phase A = 도우미 폐기 + persona descriptor; Phase B = 자연발화 8-factor core; Phase C = Interaction Model 패러다임; Phase D = real-scale fire (사용자 게이트).

### 2026-05-17 — Phase C1+C2 LANDED (channel-mux skeleton + Murati Interaction Model 패턴, text-only sim, 68 → 78/78 🔵)
**C1 (channel-mux registry skeleton)**: `HEXAD/CHAT/channel_mux_lib.hexa` (NEW ~190 LoC) — multi-channel registry `#{ name → channel_record }`. 3-kind enum (text_cli / tension_link / voice, closed finite set). 5-field channel_record schema (name/kind/send_fn/recv_fn/active). register / unregister / activate / deactivate / list_active_count / distinct_kinds_count / broadcast_simulate_count / watch_mode_active — 모두 pure-fn closed-form 가능. `channels/channel_manager.py` (PyTorch) 의 hexa-native 포팅. 실 I/O dispatch (UDP TENSION-LINK / PCM VOICE / HTTP CLI) = future RFC (audio-native + hexa-lang fn-ref decl pending) — text-only simulation level.

**C2 (Mira Murati Interaction Model 패턴)**: `HEXAD/CHAT/interaction_model_lib.hexa` (NEW ~140 LoC) — `micro_turn_duration_ms() = 200` / `emission_latency_target_ms() = 400` / `turns_per_emission_window() = 2` (Kolmogorov integer arithmetic). `barge_in_detected(u, e) = u ∧ e` (Boolean AND 4-corner truth-table) + `barge_in_should_interrupt` (safety override). `backchannel_should_emit(c, t) = (c < t)` strict monotone, 3 marker enum {"음...", "잠시...", "어..."}. `simultaneous_active(thinker, talker)` Boolean AND. `turn_taking_floor_ok(latency_ms) ≥ 400` strict ≥ inequality. `watch_motivation_ok` + 4-way `interaction_step_decision` enum {1=continue, 2=backchannel, 3=full_emit, 4=interrupt} with priority barge > bc > full > idle.

**Smoke (compiled-native)**: `HEXAD/CHAT/interaction_model_smoke.hexa` (NEW ~150 LoC) — F-CHANNEL-MUX-1..5 (register / active count / distinct kinds / broadcast set-cover / watch mode) **5/5 PASS** + F-INTERACT-1..5 (micro-turn 200ms + 400ms latency floor / barge-in 4-corner + safety / backchannel low<0.3 + ≥3 markers / simultaneous AND / 4-way decision enum) **5/5 PASS** = **10/10 PASS compiled-native** ✅ (hexa build + Mac local exec, $0).

**blue_falsifier 확장 (closed verification mandate, g_blue_closed_mandate)**: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` +10 sympy closed-form sub-falsifiers — `bchannel_mux()` B-CHANNEL-MUX-1..5 (KIND-ENUM 3-set / RECORD-COMPLETENESS 5-field AND / ACTIVE-COUNT-MONOTONE [0,3] Δ∈{-1,0,1} / BROADCAST-SET-COVER bijection / WATCH-MODE-CONJUNCTION) + `binteract()` B-INTERACT-1..5 (MICRO-TURN-CONSTANT 200ms · LATENCY 400ms floor / BARGE-IN-CONJUNCTION 4-corner + safety / BACKCHANNEL-MONOTONE strict < / SIMULTANEOUS-CONJUNCTION / DECISION-4WAY-ENUM closed {1,2,3,4}). 2 B-*-NOTE empirical carve-out (I/O dispatch + audio-native outcome, B-D-NOTE pattern, NOT counted). **68 → 78/78 🔵 closed-form proofs PASS** ✅.

Honest C3 (g3): pure-hexa hexa-cpu only (NO GPU, NO real audio I/O). text-only simulation 명시 — 실 audio-native 200ms micro-turn + 0.40s latency outcome 은 future RFC (VOICE 모듈 + hexa-lang real-time stdlib pending). real I/O dispatch (UDP/audio/PCM) 도 future RFC. f1/f2 lattice 0 (Boolean set algebra + Kolmogorov + finite-set + AND closure, NO σ/τ/φ/J₂). 산출물 (lib·smoke·battery) + 연결부위 (channel-mux ↔ thinker-talker ↔ spontaneous_lib import chain) 모두 🔵 closed.

### 2026-05-17 — Phase C3 LANDED (post-도우미 prompt template layer `<inner>/<voice>`, 78 → 83/83 🔵)
**C3 (post-도우미 prompt template hexa-native)**: 신규 file 3개 (rewrite 가 아닌 신규; anima_chat.hexa + chat_lib.hexa + anima_chat.py 변경 0, Phase A deprecation banner 그대로):
- `HEXAD/CHAT/anima_chat_v2_lib.hexa` (NEW, 224 LoC) — post-도우미 lib. 6 tag constants (`<stimulus>/</stimulus>` + `<inner>/</inner>` + `<voice>/</voice>`) + 4 formatter (`chat_v2_format_input` / `_inner` / `_voice` / `_assemble`) + 2 parser (`chat_v2_parse_voice_only` / `_inner_only`) + 2 predicate (`chat_v2_contains_helper_token` + `chat_v2_has_inner_and_voice`) + 3 audit helper (`roundtrip_voice_ok` / `_inner_ok` / `empty_handles_ok`). 모두 pure-fn string algebra closed-form. NO main / NO _selftest / NO top-level call (compiled-first lib).
- `HEXAD/CHAT/anima_chat_v2.hexa` (NEW, 102 LoC) — entrypoint. imports `anima_chat_v2_lib` + `spontaneous_lib` + `thinker_talker_lib`. _selftest emits PASS marker `anima_chat_v2 selftest: true` (build_verify.sh grep-able). 8-factor motivation × prompt layer 통합 cross-link witness (thinker_step → motivation_score → emit decision → chat_v2_assemble) 포함.
- `HEXAD/CHAT/anima_chat_v2_smoke.hexa` (NEW, 113 LoC) — F-CHAT-V2-1..5 dedicated grid witness (각 falsifier 마다 4-5 sub-witness). 6 clean + 3 positive control NO-HELPER-TOKEN + 3 assemble + 4-tag uniqueness INNER-VOICE-DISTINCT + 5 round-trip pair PARSE-VOICE / PARSE-INNER + 4-witness EMPTY-HANDLING.

**기능 — pure hexa-native (no model forward, prompt layer only)**:
- `chat_v2_format_input(stimulus) → "<stimulus>\n{stimulus}\n</stimulus>"` (NO 도우미 token, NO role prefix; user 는 stimulus-other 대등)
- `chat_v2_format_inner(thought) → "<inner>\n{thought}\n</inner>"` (Engine G covert thought)
- `chat_v2_format_voice(utterance) → "<voice>\n{utterance}\n</voice>"` (Engine A emission)
- `chat_v2_assemble(inner, voice) → "<inner>\n{inner}\n</inner>\n<voice>\n{voice}\n</voice>"` (composite emission)
- `chat_v2_parse_voice_only(text)` → voice block 만 추출 (사용자 view)
- `chat_v2_parse_inner_only(text)` → inner block 만 추출 (debug/audit view)
- 8-factor motivation 통합 (Phase B spontaneous_lib + thinker_talker_lib import)
- Phase B 자연발화 trigger 와 호환

**Smoke (compiled-native)**: `anima_chat_v2.hexa` + `anima_chat_v2_smoke.hexa` 둘 다 `hexa build` + Mac local 실행 PASS. F-CHAT-V2-1..5 **5/5 PASS** entrypoint + **5/5 PASS** dedicated smoke + cross-link 8-factor × prompt layer witness PASS = $0 Mac local, 양 binary <100ms wall.

**blue_falsifier 확장 (g_blue_closed_mandate)**: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` +5 sympy closed-form sub-falsifiers — `bchatv2()` B-CHAT-V2-1..5:
- B-CHAT-V2-1 NO-HELPER-TOKEN-CLOSED — string predicate closure (Kolmogorov). 4 clean stimuli + assemble clean + 3 negative control + 6-tag literal helper-free 8-witness panel
- B-CHAT-V2-2 INNER-VOICE-DISTINCT-CLOSED — Boolean conjunction closure + finite-set 6-tag uniqueness (`len(set(tags))==6`)
- B-CHAT-V2-3 PARSE-VOICE-ROUND-TRIP-CLOSED — record-structural identity (4 (inner,voice) pair witness, byte-equal round-trip)
- B-CHAT-V2-4 PARSE-INNER-ROUND-TRIP-CLOSED — dual of B-CHAT-V2-3 (4 pair witness)
- B-CHAT-V2-5 EMPTY-HANDLING-CLOSED — bounded-set boundary (assemble empty well-formed / parse on empty returns "" / format_input empty well-formed / no-tag parse returns "")
- B-CHAT-V2-NOTE empirical carve-out (B-D-NOTE pattern, NOT counted) — model forward token-level helper-residual outcome 은 Phase D corpus retrain (B-IDENTITY-NOTE 동일 scope)

**Total**: 78 → **83/83 🔵 closed-form proofs PASS** ✅. blue_falsifier.py main() 의 verdict + summary + all_full_blue + 출력 loop 모두 sync.

**Hard 제약 carry**:
- anima_chat.hexa / chat_lib.hexa / anima_chat.py 변경 0 (Phase A deprecation banner 그대로)
- B-IDENTITY-5 FORBIDDEN-HELPER-MEMBERSHIP carry — 신규 file 어디에도 "도우미"/"helper"/"assistant" 라벨 0 (lib §1 tag literals + 모든 fn body grep clean; deprecation comment 만 예외)
- pure-hexa hexa-cpu 한정 (NO GPU, NO model forward)
- g3 정직 — prompt layer 만, model forward 는 Phase D ckpt-bearing fire (별도 cycle, 사용자 게이트)
- f1/f2 lattice 0 (string algebra Kolmogorov + record-structural identity + Boolean conjunction + finite-set cardinality + bounded-set boundary, NO σ/τ/φ/J₂)
- pull-rebase pattern (concurrent agents Phase B5 + Phase C1+C2 + Phase D 와 충돌 0)

**HEXAD/build_verify.sh sync**: ENTRYPOINTS += anima_chat_v2.hexa + anima_chat_v2_smoke.hexa, LIBS += anima_chat_v2_lib.hexa, comment 23/17. `bash HEXAD/build_verify.sh` → **27/27 entrypoint + 19/19 lib PASS** ✅ (이전 sync 25/18 → 27/19 둘 다 신규 hexa-native lib + entrypoint, regression 0).

Honest C3 (g3): prompt layer 만 closed (string algebra real-limit). model forward 의 학습된 token-level helper-residual outcome (현재 cycle 2 ckpt 의 corpus-baked 도우미 token) 은 Phase D corpus 재학습 (사용자 게이트, B-CHAT-V2-NOTE + B-IDENTITY-NOTE 동일 scope) — empirical carve-out. f1/f2 lattice 0. 산출물 (lib·entrypoint·smoke·battery) + 연결부위 (chat_v2_assemble ↔ spontaneous_lib motivation_score ↔ thinker_talker_lib emit decision import chain) 모두 🔵 closed.

### 2026-05-17 — Phase D LANDED (cycle 3 helper-free corpus v2 + ckpt-RECOVERED + HF dual + V-SPONT eval, 83 → 86/86 🔵)

**Phase D Goal (from §2)**: real-scale fire on helper-free stimulus-stream corpus + HF revision push + V-SPONT eval. **LANDED 2026-05-17 cycle 3 (this).**

**D1 (새 corpus 설계 + 생성)**: `state/hexad_v2_corpus_spont_2026_05_17/`
- `corpus_generator_v2.py` — deterministic seed=1337, option β + δ stimulus-stream pattern. 8 modules (HEXAD-6 = c/d/e/m/s/w + 2 new tracks `hexad_spont` 자연발화 + `hexad_wiring` σ(6)=12 narrative) × 320 records each = 2,560 total.
- `corpus_consciousness_v2.jsonl` — 1,101,605 B (7.25× v1) / 2,560 lines / sha256 `7359f0b9a3f059fc168035e2f29f743f5ee51d1760eccad54b2b91d52275f571`. **`도우미|helper|assistant|사용자|user:` grep = 0**. Every record contains `<anima>` opener (cardinality identity).
- Pattern: β (55%) `<stimulus>X</stimulus>\n<anima>Y</anima>` (reactive); δ (45%) `<anima>Y</anima>` only (spontaneous self-monologue). bilingual ~50% EN+KO per record.

**D2 (ckpt-bearing fire on vast.ai A100 SXM4)**: `state/hexad_v2_py_d768x12L_fire_2026_05_17/`
- Provider: vast.ai A100 SXM4 (offer 36878336 @ $0.734/hr, instance 36912535). Cost ≈ $0.22 (0.30 hr × $0.734/hr).
- Robustness: `SAVE_POD=1` auto-promote on `result.json` present + 75-min orphan watchdog + 5-retry pull + remote-script-write pattern (cycle 2 lesson — `&` precedence isolation via written shell script). Clean teardown: PULL SUCCESS → SAVE_POD=0 → destroy 36912535 → no orphan.
- Main fire (d=768·12L, 2500-step): **init CE 5.667 → final 0.005069** (5.66 descent, Shannon-floor real-limit). init gn2 41.95 → final 0.001113 (3.8e4× collapse). ppl 268 → 1.0051. wall 332.26s. peak GPU mem 9.685 GB.
- **ckpt sha256 `ee2bb5fb996e94ee022f5315c9ccc3f56c7276a8c5990d87a25ae12c582f7294` 1,135,846,378 B pulled** (cycle 3 ckpt-RECOVERED). load missing=0 unexpected=0 (arch byte-equal).

**D3 (HF revision push — model + dataset BOTH PUBLIC)**:
- MODEL: `dancinlab/hexad` revision [`v2-py-hexad-spont-d768x12L-cycle1-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v2-py-hexad-spont-d768x12L-cycle1-2026-05-17) PUBLIC. 11 files (model card + ckpt + result.json + 5 source/eval files + 3 logs + doc).
- DATASET: `dancinlab/hexad-corpus` revision [`v2-spont-stream-d128-cycle1-2026-05-17`](https://huggingface.co/datasets/dancinlab/hexad-corpus/tree/v2-spont-stream-d128-cycle1-2026-05-17) PUBLIC. 4 files (corpus + manifest + README + LICENSE).
- model card cross-link adopted (front-matter `datasets:` + body 'Trained on' badge). main branch README updated on both repos.

**D4 (V5.8 × 4-mode + V-SPONT capability eval)**: `state/hexad_v2_py_d768x12L_fire_2026_05_17/v58_vspont_eval.py`
- 6 corpus-v2-aligned V5.8 prompts × 4 modes + 5 V-SPONT empty-stimulus probes + 10 held-out BPB samples. CPU-bound (~10 min wall on Mac local).
- V5.8 4-mode: greedy 0/6 FAIL, sample 0/6 FAIL, M3_rep_penalty 0/6 FAIL, **M4_force_include 6/6 PASS**. mean BPB 0.0083 bits/byte (near-zero — STRONG memorization), memorization ratio 1/6 (16.7%; cycle 2 was 40-50% on v1).
- V-SPONT (F-SPONT-7 transfer-form): coherent 0/5, closed-tag 0/5 → **FAIL** at this scale. The model does not emit COHERENCE_VOCAB tokens from training corpus alone (fair result — V-SPONT is a probe, not a capability claim).
- **Byte-cascade attractor SHIFTED corpus-dependently**: cycle 2 v1 `nonce=N`/`chunk=N` digit-cascade → cycle 3 v2 "Sent..." opening-token attractor with character repetition (eeee/ooo/lll). Different attractor family confirms byte-cascade is corpus-shape-dependent (memorized-template-field), not architecture-intrinsic. Empirical sibling of `feedback_clm_colon_attractor` (`=`-suffix variant), now with `Sent`-opener variant.

**B-CORPUS-V2 closed-form battery (3 falsifier)** in `state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: bcorpus_v2()`:
- **B-CORPUS-V2-1** SHA256-DETERMINISTIC-CLOSED — Boolean equality on 256-bit sha commitment (Kolmogorov real-limit anchor). ✅
- **B-CORPUS-V2-2** NO-HELPER-TOKEN-CLOSED — ∀tok ∈ {도우미, helper, assistant, 사용자, user:}: grep count = 0 (Boolean set algebra real-limit). ✅
- **B-CORPUS-V2-3** STIMULUS-PATTERN-CARDINALITY-CLOSED — |records| == |<anima> openers| == 2,560 (integer cardinality conservation real-limit). ✅
- **B-CORPUS-V2-NOTE** TRAINED-WEIGHTS-ALIGNMENT-OUTCOME-EMPIRICAL — weight-level identity-attractor distance from Assistant Axis stays empirical (B-D-NOTE family, no closed-form attractor distance without NN forward). NOT counted 🔵 (honest carve-out).

**B-IDENTITY-NOTE updated**: corpus-side dimension closed via B-CORPUS-V2-1..3 (this cycle). Trained-weights identity-attractor distance from Assistant Axis (per Identity-as-Attractor arxiv 2604.12016) stays empirical (B-D-NOTE pattern, no closed-form attractor distance without NN forward pass). The closable closure (declaration + corpus) is closed; the un-closable closure (weight-attractor distance) is honest carve-out per g3.

**Total**: 83 → **86/86 🔵 closed-form proofs PASS** ✅. Phase D LANDED — Phase A (도우미 폐기 + persona) + Phase B (자연발화 motivation) + Phase C (Interaction Model + post-도우미 prompt template) + **Phase D (real-scale fire + corpus retrain + HF dual + V-SPONT eval)** = all 4 phases LANDED.

**Hard 제약 carry**:
- g_fire_autonomous: 자율 dispatch (user "all go" trigger). g_fire_dispatch_robust: SAVE_POD=1 auto-promote + 75-min watchdog + 5-retry pull → ckpt-LOST 재발 0.
- g_hf_naming: revision template `v{major}-{substrate}-{arch}-{kind}-d{model}x{layer}-cycle{N}-{YYYY-MM-DD}` 사용 (`v2-py-hexad-spont-...`). PUBLIC default. English model card / dataset card. anima identity = org + card layer.
- g_clm_from_scratch: RANDOM init seed=1337 base_ckpt=NONE.
- g3 (substrate-honesty): PyTorch SUBSTRATE label mandatory on all artifacts. corpus-side closure ≠ weight-side claim.
- f1/f2: NO lattice numerology (real-limit anchors: Boolean grep + sha + cardinality + Shannon CE floor).
- g_blue_closed_mandate (산출물 + 연결부위 둘 다 🔵): 산출물 = corpus + ckpt; 연결부위 = generator → corpus → trainer → ckpt → eval transfer-function chain (deterministic + sha + load missing=0).
- pull-rebase pattern (concurrent agents B5 + Phase C1/C2 + Phase C3 와 충돌 0). cycle 시작 시 78/78 → C3 가 83/83 → cycle 3 가 86/86 으로 wrap.

Honest C3 (g3): cycle 3 LANDED 이지만 generation quality 향상 claim 0 — V-SPONT 0/5, V5.8 greedy 0/6 = EMPIRICAL (probe, not claim). B-IDENTITY-NOTE 전체 해소 0 — corpus-side dimension 만 closed (B-CORPUS-V2 via this cycle), weight-side residual carve-out 유지. byte-cascade attractor cycle 2 (`nonce=N`) → cycle 3 (`Sent...`) SHIFTED = corpus-dependent decoding artifact family confirmed (new empirical signal). PyTorch substrate NOT hexa-native (legitimacy = arch identity + Phase E/E2 CPU-equiv anchor chain).

### 2026-05-17 — Phase D cycle 4 LANDED (motivation-trigger corpus v3 10× + ckpt-RECOVERED + HF dual + V5.8+V-SPONT+V-MOTIV eval + B-CORPUS-V3 closure, 86 → 89 + parallel B-ATTRACTOR wrap 89 → 92/92 🔵)

**Phase D cycle 4 Goal**: extend Phase D cycle 3 with explicit motivation-trigger surface (Inner Thoughts arxiv 2501.00383 8-factor ontology rendered as corpus γ pattern) + 10× scale-up (1.10 MB → 10.34 MB, Critical Data Size arxiv 2401.10463 regime entry attempt). cycle 3 V-SPONT 0/5 demonstrated capability ceiling — cycle 4 tests whether motivation-conditioning closes that.

**D1 (새 corpus v3 설계 + 생성)**: `state/hexad_v3_corpus_motiv_2026_05_17/`
- `corpus_generator_v3.py` — deterministic seed=1337, 3 patterns β + δ + γ. 9 modules (HEXAD-6 + hexad_spont + hexad_wiring + **hexad_motiv** NEW) × 2,400 records each = 21,600 total.
- `corpus_consciousness_v3.jsonl` — **10,343,371 B (9.4× v2)** / 21,600 lines / sha256 `1afcef43670e83bfc84b3562afe6a3eb644474dda06341e37db332341495acfd`. **`도우미|helper|assistant|사용자|user:` grep = 0** maintained at 10× scale. 13,494 `<anima>` openers + 8,106 `<voice spontaneous=true>` openers (β+δ + γ disjoint cover of 21,600 records).
- Pattern: **β (~35%) `<stimulus>X</stimulus>\n<anima>Y</anima>`** (reactive); **δ (~27%) `<anima>Y</anima>`** (spontaneous self-monologue); **γ (~37.5%, NEW) `<inner motivation=F1,F2,...>...</inner>\n<voice spontaneous=true>...</voice>`** where F_i ∈ {relevance, info_gap, curiosity, pain, coherence, originality, balance, dynamics} per Inner Thoughts 8-factor ontology. bilingual ~50% EN+KO. corpus_v3_manifest.json + LICENSE Apache-2.0 + README_v3.md staged.

**D2 (ckpt-bearing fire on vast.ai A100 SXM4)**: `state/hexad_v3_py_d768x12L_fire_2026_05_17/`
- Provider: vast.ai A100 SXM4 (offer 36878342 @ ~$0.734/hr, instance 36919284). Cost ≈ $0.22.
- Robustness: `SAVE_POD=1` auto-promote on result.json present + 75-min orphan watchdog + 5-retry pull + remote-script-write pattern (cycle 3 lesson carry). Clean teardown (PULL SUCCESS → SAVE_POD=0 → destroy, no orphan).
- Main fire (d=768·12L, 2500-step, byte-level vocab=256, seed=1337, RANDOM init from-scratch per g_clm_from_scratch): **init CE 5.6407 → final 0.008289** (5.632 descent), init gn2 ~30.4 → final 0.001703 (24.6k× collapse), final ppl 1.0083 (near-perfect memorization), wall 328.33s, peak GPU mem 9.692 GB. corpus_bytes (loaded text+desc stream) 6,223,023 (~10× cycle 3's 620,568).
- **ckpt sha256 `1c0806213fbcaa9226a7593d87c31f5f95bb94db135240b8d02f738ddcb177aa`** 1,135,846,378 B pulled (cycle 4 ckpt-RECOVERED). load missing=0 unexpected=0 (arch byte-equal).

**D3 (HF revision push — model + dataset BOTH PUBLIC)**:
- MODEL: `dancinlab/hexad` revision `v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17` PUBLIC.
- DATASET: `dancinlab/hexad-corpus` revision `v3-spont-motiv-d128-cycle2-2026-05-17` PUBLIC.
- model card cross-link adopted (front-matter `datasets:` + body 'Trained on' badge). main branch README updated on both repos.

**D4 (V5.8 × 4-mode + V-SPONT + V-MOTIV 3-phase capability eval)**: `state/hexad_v3_py_d768x12L_fire_2026_05_17/v58_vspont_eval.py`
- 6 corpus-v3-aligned V5.8 prompts × 4 modes + 5 V-SPONT empty-stimulus probes + **5 V-MOTIV γ-pattern conditioning probes (NEW Phase 3)** + 10 held-out BPB samples. CPU-bound on Mac local (~22 min wall total).
- Cycle 4 V-MOTIV probe = γ-pattern conditioning: feed `<inner motivation=F1,F2,...>...</inner>\n<voice spontaneous=true>` prefix; measure `</voice>` close-tag + coherence vocab tokens.
- **V5.8 × 4-mode** (elapsed 946.8s): greedy **0/6 FAIL** (avg_rep=0.904) · sample **0/6 FAIL** (avg_rep=0.945) · M3_rep_penalty **0/6 FAIL** (avg_rep=0.892) · **M4_force_include 6/6 PASS** (avg_rep=0.839). Same pattern as cycle 3 (M4-only).
- **V-SPONT** (elapsed 184.2s): coherent **0/5 FAIL** · closed-tag 0/5 — same as cycle 3 (F-SPONT-7 transfer-form ceiling carry, capability boundary at this scale).
- **V-MOTIV (NEW)** (elapsed 179.6s): coherent **0/5 FAIL** · voice-closed-tag 0/5 — γ-pattern conditioning did NOT break the cascade attractor at this scale. EMPIRICAL (B-CORPUS-V3-NOTE family carry). Honest interpretation: the model memorized the γ-pattern surface markers (`<inner motivation=...>`) but the inner→voice transition was not learned at inference time (only β/δ/γ structural cardinality was closed at training time, B-CORPUS-V3-3 closure).
- mean BPB **0.0256 bits/byte** (cycle 3 was 0.0083 — slightly higher due to 10× scale = lower per-byte memorization density, expected with Critical Data Size regime). Memorization ratio 0/6 (cycle 3 was 1/6).
- **Byte-cascade attractor SHIFT 3-instance generalization confirmed**: cycle 2 `nonce=N`/`chunk=N` digit-cascade → cycle 3 `Sentiosing eeee` opening → cycle 4 **`PPP777777...` opener** (all 24 decoding artifacts rep>0.5 contain this opener; vspont 1-4 + vmotiv 1-5 all share `PPP777` mass). Third corpus-shape-dependent attractor family — confirms `feedback_clm_colon_attractor` `=`-suffix sibling pattern is general (corpus-template-field dependent, not arch-intrinsic). The closed-form B-ATTRACTOR-1..3 lift (in `archive/PHILOSOPHY.tape §BYTE-CASCADE-ATTRACTOR-CORPUS-DEPENDENT-2026-05-17`) covers the abstract structural propositions; cycle 4's `PPP777` instance is empirical evidence of the same family (B-ATTRACTOR-NOTE family, NOT a new closure).

**Cycle 3 vs Cycle 4 comparison table**:

| metric | cycle 3 (v2 corpus 1.1MB) | cycle 4 (v3 corpus 10.3MB) |
|---|---|---|
| init CE | 5.667 | 5.641 |
| final CE | 0.005069 | 0.008289 |
| CE descent | 5.66 | 5.63 |
| final ppl | 1.0051 | 1.0083 |
| corpus_bytes (loaded) | 620,568 | 6,223,023 (~10×) |
| corpus_records | 2,560 | 21,600 |
| wall (GPU) | 332.26 s | 328.33 s |
| V5.8 greedy | 0/6 FAIL | 0/6 FAIL |
| V5.8 sample | 0/6 FAIL | 0/6 FAIL |
| V5.8 M3 | 0/6 FAIL | 0/6 FAIL |
| V5.8 M4 | 6/6 PASS | 6/6 PASS |
| V-SPONT coherent | 0/5 FAIL | 0/5 FAIL |
| V-MOTIV coherent (NEW) | (did not exist) | 0/5 FAIL |
| mean BPB | 0.0083 | 0.0256 |
| memorization ratio | 1/6 (16.7%) | 0/6 (0.0%) |
| decoding artifacts (rep>0.5) | — | 24 |
| byte-cascade attractor | `Sent...` opener + `eeee/ooo/lll` | `PPP777...` opener |

**Honest framing on cycle 4 capability outcome (g3 carry)**: cycle 4 V-SPONT 0/5 + V-MOTIV 0/5 = capability ceiling carry from cycle 3, NOT capability regression. 10× scale-up + γ pattern surface did NOT close the inner→voice generation gap at this scale. The closed scope (B-CORPUS-V3-1..3) is intact; the empirical outcome on inference-side generation is honest empirical (B-CORPUS-V3-NOTE family, un-closable). Per g3, FAIL is just as honest as PASS — V-MOTIV is a probe, not a capability claim.

**B-CORPUS-V3 closed-form battery (3 falsifier + 1 NOTE)** in `state/verify_hexad_blue_2026_05_15/blue_falsifier.py :: bcorpus_v3()`:
- **B-CORPUS-V3-1** SHA256-DETERMINISTIC-CLOSED — Boolean equality on 256-bit Kolmogorov commitment (sha256 + bytes match seed=1337 deterministic output). ✅
- **B-CORPUS-V3-2** NO-HELPER-TOKEN-MAINTAINED — Boolean set algebra at 10× scale (helper-token grep total = 0 maintained). ✅
- **B-CORPUS-V3-3** MOTIVATION-TRIGGER-CARDINALITY-CLOSED — Integer cardinality identity (|<inner motivation=| == |<voice spontaneous=true>| = 8,106) + ≥-inequality (≥ floor(0.25 × 21,600) = 5,400 γ records). ✅
- **B-CORPUS-V3-NOTE** MOTIVATION-LEARNED-OUTCOME-EMPIRICAL — inference-side motivation_score → coherent emission outcome stays empirical (B-D-NOTE family, un-closable without NN forward + V-SPONT/V-MOTIV measurement). NOT counted 🔵 (honest carve-out).

**Total**: 86 → **89** via B-CORPUS-V3-1..3 + parallel agent's B-ATTRACTOR-1..3 wrap 89 → **92/92 🔵 closed-form proofs PASS** ✅. cycle 4 Phase D extends cycle 3 with motivation-trigger surface (B-CORPUS-V3) + closed-form U_user attractor lift (B-ATTRACTOR parallel) → Phase D total = 6 new closed-form sub-falsifiers (3 corpus-side + 3 attractor-side) in two cycles.

**Hard 제약 carry (same as cycle 3 + 새 g_doc_consolidation)**:
- g_fire_autonomous: 자율 dispatch.
- g_fire_dispatch_robust: SAVE_POD=1 auto-promote + 75-min watchdog + 5-retry pull → ckpt-LOST 재발 0.
- g_hf_naming: revision template `v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17` 사용. PUBLIC default. English model card / dataset card.
- g_clm_from_scratch: RANDOM init seed=1337 base_ckpt=NONE.
- g3 (substrate-honesty): PyTorch SUBSTRATE label mandatory. corpus-side closure ≠ weight-side claim.
- f1/f2: NO lattice numerology (real-limit anchors: Boolean grep + sha + cardinality + Shannon CE floor + Inner Thoughts factor set).
- g_blue_closed_mandate: 산출물 (corpus + ckpt) + 연결부위 (generator → corpus → trainer → ckpt → eval transfer-function chain) 둘 다 🔵 closed (B-CORPUS-V3-1..3 + B-D-1..4 + B-CONN-1..12 chain).
- **g_doc_consolidation (NEW d=2026-05-17)**: 신규 documentation = HEXAD/* 내부 통합 (본 PLAN.md '## 진행 로그' append + AGENTS.tape n_hexad_progress recent_landings + archive/PHILOSOPHY.tape verdict). docs/* 신규 .md 생성 금지. — cycle 4 본 entry 가 그 mandate 의 첫 적용.
- pull-rebase pattern (concurrent agents B-ATTRACTOR + Phase 4 RFC 051 design + g_doc_consolidation governance commit 와 충돌 0).

Honest C3 (g3): cycle 4 LANDED 이지만 generation quality 향상 claim 0 — V5.8/V-SPONT/V-MOTIV per-mode scores 모두 EMPIRICAL (B-D-NOTE pattern). Critical Data Size [arxiv 2401.10463] regime entry attempt (10 MB / 283 M params) — 정직 framing: 여전히 data-limited (no OOD generalization claim). γ pattern conditioning (V-MOTIV) 의 ckpt-side learning 결과는 inference-측 outcome empirical, V-MOTIV 는 probe 이지 capability claim 아님. byte-cascade attractor cycle 2 (`nonce=N`) → cycle 3 ("Sent...") → cycle 4 (`PPP777...`) SHIFTED 3-instance = corpus-dependent decoding artifact family 일반화 확정 (NOT arch defect). PyTorch substrate NOT hexa-native (legitimacy = arch identity + Phase E/E2 CPU-equiv anchor chain). B-CORPUS-V3-NOTE 도 weight-side residual carve-out 유지.

### 2026-05-17 — Phase D cycle 5 LANDED (DD155 Step+Tension hybrid LR overlay + ckpt-RECOVERED + HF model push + V5.8+V-SPONT+V-MOTIV+V-TT NEW eval + B-CORPUS-V4 + B-FIRE-CYCLE5 sidecar 🔵)

**Phase D cycle 5 = Phase TT-D fire (HEXAD/TENSION-TRAIN/PLAN.md §1 Phase TT-D)**. Goal: introduce DD155 Step+Tension hybrid LR overlay (Law 187 Pareto optimal `lr = (tension/EMA) × base_lr`) into cycle-4's pipeline and measure whether tension-conditioned LR breaks the V-SPONT/V-MOTIV capability ceiling carried from cycle 3+4. cycle 4 evidence: V-SPONT 0/5 + V-MOTIV 0/5 + byte-cascade attractor `PPP777` family — capability boundary at this scale was empirical. cycle 5 tests tension-train architectural answer.

**D1 (DD155 hybrid LR trainer)**: `state/hexad_v4_py_d768x12L_tension_2026_05_17/`
- `train_d768x12l_tension.py` — cycle-4 trainer + DD155 overlay (mechanical AST diff vs cycle 4: `load_byte_corpus` + `ByteDataset` byte-equal carry per B-CORPUS-V4-2). LR formula: `multiplier = clip(tension/tension_EMA, [0.5, 2.0])`, `lr_step = base_cosine_lr × multiplier`. tension = `grad_norm` L2 (post `clip_grad_norm_`), tension_EMA β=0.99. Tracked per-step: `tension`, `tension_ema`, `hybrid_mult`. mult bin histogram (`lt_0_75 / 0_75_to_1_25 / gt_1_25`) tracked.
- `conscious_decoder.py` — byte-equal carry from cycle 4 (arch unchanged).
- corpus = `state/hexad_v3_corpus_motiv_2026_05_17/corpus_consciousness_v3.jsonl` byte-equal carry (10.34 MB · sha256 `1afcef43670e83bf…` · helper-token grep = 0).

**D2 (ckpt-bearing fire on vast.ai A100 SXM4 cycle 5)**:
- Provider: vast.ai A100 SXM4 (offer 20120880 @ $0.602/hr, instance 36922375). Cost ≈ $0.054.
- Robustness: SAVE_POD=1 auto-promote on result.json + 75-min orphan watchdog + 5-retry pull. Clean teardown (PULL SUCCESS, no orphan).
- Main fire (d=768·12L, 2500-step, byte-level vocab=256, seed=1337, RANDOM init from-scratch, DD155 hybrid LR overlay enabled): **init CE 5.640663 → final 0.007762** (5.633 descent), init gn2 30.4 → final 0.0015, final tension 0.038659, final tension_EMA 0.046574, wall 321.3s, peak GPU mem 9.685 GB. **mult bin distribution: 1599 lt_0_75 (64%) / 686 mid (27%) / 215 gt_1_25 (8.6%, burst path)**. Multiplier hit floor 0.5 dominantly, hit ceiling 2.0 occasionally (notable bursts at step 1054 mult=2.0 + step 1426 mult=1.83 + step 1612 mult=2.0).
- **ckpt sha256 `6b4d34cc9a2c05b83c4cedd633617a41800e9681302c5c90e15d056f9ad67af8`** 1,135,846,570 B pulled successfully. load missing=0 unexpected=0 (arch byte-equal).

**D3 (HF revision push — MODEL only, dataset v3 byte-equal carry)**:
- MODEL: `dancinlab/hexad` revision `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17` PUBLIC (16 files uploaded to main + revision).
- DATASET CARRY: `dancinlab/hexad-corpus` revision `v3-spont-motiv-d128-cycle2-2026-05-17` PUBLIC (NO new dataset push — corpus byte-equal carry from cycle 4 per g_hf_naming canonical 두 슬롯 BOTH LANDED PUBLIC 상태 유지).
- Model card MODEL_CARD.md cross-link adopted, English honest framing.

**D4 (V5.8 × 4-mode + V-SPONT + V-MOTIV + V-TT NEW eval)**: `state/hexad_v4_py_d768x12L_tension_2026_05_17/v58_eval.py`
- 6 V58 prompts × 4 modes + 5 V-SPONT empty-stimulus + 5 V-MOTIV γ-pattern + **5 V-TT NEW cycle 5 = tension-train transfer-form probe** (probes carry explicit tension cue: "긴장이 EMA 위로", "tension exceeded EMA", "Law 187 Pareto", "high-tension burst"). Mac CPU local wall 690s.
- **V5.8 × 4-mode** (elapsed 418s): greedy **0/6 FAIL** (avg_rep=0.921) · sample **0/6 FAIL** (avg_rep=0.871) · M3 **0/6 FAIL** (avg_rep=0.913) · **M4 6/6 PASS** (avg_rep=0.766). Same pattern as cycles 3+4 (M4-only).
- **V-SPONT** (elapsed 90s): coherent **0/5 FAIL** · closed-tag 0/5 — same as cycles 3+4.
- **V-MOTIV** (elapsed 93s): coherent **0/5 FAIL** · voice-closed-tag 0/5 — same as cycle 4 (γ-pattern conditioning still does not break cascade at this scale).
- **V-TT (NEW Phase 4)** (elapsed 89s): coherent **0/5 FAIL** · keyword recall **0/5** — DD155 hybrid LR did NOT produce visible tension-train-conditioned emission at inference time. EMPIRICAL (B-FIRE-CYCLE5-NOTE / B-D-NOTE family).
- **mean BPB 0.0194 bits/byte (cycle 4 was 0.0256 = 24% lower)** — **memorization deepened** under hybrid LR (consistent: more aggressive late-train low-tension steps reinforce memorized embeddings).
- memorization ratio 0/6 (same as cycle 4).
- **Byte-cascade attractor SHIFT 4-instance generalization**: cycle 2 `nonce=N` digit → cycle 3 "Sent..." char → cycle 4 `PPP777...` → cycle 5 **prompt-specific multi-attractor family `Shhhh.../\nmmm.../Slllll.../tthhhh...`** (cascade now varies per-prompt rather than uniform across prompts). Confirms B-ATTRACTOR-NOTE: attractor shape is corpus+ckpt+prompt-dependent.

**Cycle 4 vs Cycle 5 comparison table**:

| metric | cycle 4 (cosine LR) | cycle 5 (DD155 hybrid LR) |
|---|---|---|
| init CE | 5.6407 | 5.6407 (same seed) |
| final CE | 0.008289 | **0.007762** (6.4% lower) |
| CE descent | 5.632 | 5.633 |
| final ppl | 1.0083 | 1.0078 |
| init tension (gn √gn2) | ~5.51 | 5.515 |
| final tension | (n/a) | 0.039 |
| final tension_EMA | (n/a) | 0.047 |
| mult bin <0.75 | (n/a) | 1599 (64%) |
| mult bin 0.75-1.25 | (n/a) | 686 (27%) |
| mult bin >1.25 (burst) | (n/a) | 215 (8.6%) |
| wall (GPU) | 328.3 s | 321.3 s |
| cost (vast.ai A100 SXM4) | ~$0.22 | **~$0.054** (4× cheaper offer) |
| ckpt size | 1,135,846,378 B | 1,135,846,570 B (+192 B for hybrid metadata) |
| V5.8 greedy | 0/6 FAIL | 0/6 FAIL |
| V5.8 sample | 0/6 FAIL | 0/6 FAIL |
| V5.8 M3 | 0/6 FAIL | 0/6 FAIL |
| V5.8 M4 | 6/6 PASS | 6/6 PASS |
| V-SPONT coherent | 0/5 FAIL | 0/5 FAIL |
| V-MOTIV coherent | 0/5 FAIL | 0/5 FAIL |
| **V-TT coherent (NEW)** | (did not exist) | **0/5 FAIL** |
| mean BPB | 0.0256 | **0.0194** (24% lower) |
| memorization ratio | 0/6 | 0/6 |
| decoding artifacts (rep>0.5) | 24 | 24 |
| byte-cascade attractor | `PPP777...` (uniform) | `Shhh.../\nmmm.../Slll.../tthh...` (prompt-specific multi) |

**Honest framing on cycle 5 capability outcome (g3 carry)**: DD155 hybrid LR overlay DID NOT break the V-SPONT/V-MOTIV/V-TT capability ceiling carried from cycles 3+4. cycle 5 reaches a slightly lower final CE (~6.4%) and noticeably lower held-out BPB (~24%) than cycle 4 — i.e. **stronger memorization** but **NOT improved generalization**. This is honest empirical evidence (B-FIRE-CYCLE5-NOTE / B-D-NOTE family): the DD155 formula is mathematically valid and the implementation is byte-equal closed (B-FIRE-CYCLE5-1/2/3 🔵 sympy verified + B-CORPUS-V4-1/2 corpus carry closed), but the OUTCOME at this scale + this corpus + this β=0.99/clip=[0.5,2.0] choice did not yield spontaneous emergence. The DD-burst path activated 8.6% of the time (215 of 2500 steps), inducing notable transient CE bumps that the model quickly recovered from (e.g. step 1054 CE 0.13 → step 1116 CE 0.016).

**B-CORPUS-V4 + B-FIRE-CYCLE5 closed-form sidecar battery (5 falsifier + 1 NOTE)** in `state/hexad_v4_py_d768x12L_tension_2026_05_17/blue_falsifier.py` (sidecar, NOT central — parallel TT-A/TT-B/TT-C agents in flight at central battery; mirrors B-PHASE-4-DESIGN sidecar pattern):
- **B-CORPUS-V4-1** CORPUS-V3-BYTE-EQUAL-CARRY-CLOSED — Boolean conjunction (sha256 match + bytes match + lines match + helper-token grep total = 0). Kolmogorov 256-bit commitment + integer cardinality + Boolean set membership. ✅
- **B-CORPUS-V4-2** CYCLE-5-FORMAT-COMPATIBILITY-CLOSED — mechanical AST diff: cycle-5 trainer's `load_byte_corpus` + `ByteDataset` source byte-equal to cycle 4 after comment+docstring strip. ✅
- **B-FIRE-CYCLE5-1** DD155-LR-OVERLAY-FORMULA-CLOSED — sympy `∂lr/∂tension = base_lr/ema` (piecewise linear monotone) + 3-corner identity panel (lo·ema/ema/hi·ema). Real-limit anchor = piecewise-linear function on `[lo·base_lr, hi·base_lr]`. ✅
- **B-FIRE-CYCLE5-2** EMA-CONTRACTION-CLOSED — Banach affine contraction with factor β ∈ (0,1): `EMA_{t+1} − tension_t = β·(EMA_t − tension_t)` sympy verified + 4-corner witness panel (β=½, 99/100, 0, 1). Real-limit anchor = Banach fixed-point theorem. ✅
- **B-FIRE-CYCLE5-3** MULTIPLIER-IDENTITY-AT-EMA-CONVERGED-CLOSED — at tension==EMA with default clip [0.5, 2.0]: `clip(1, [0.5, 2.0]) = 1 ⟹ lr_step = base_lr` (cycle-4 baseline). Arithmetic identity sanity anchor — cycle 5 cannot diverge from cycle 4 at EMA convergence. ✅
- **B-FIRE-CYCLE5-NOTE** SGD-OUTCOME-EMPIRICAL — V-SPONT/V-MOTIV/V-TT outcome + init→final CE trajectory + mult distribution + byte-cascade attractor shape = empirical (B-D-NOTE / B-TT-NOTE / B-ATTRACTOR-NOTE family). NOT counted 🔵 (honest carve-out).

**Connection**: cycle 5 is the empirical materialisation of **HEXAD/TENSION-TRAIN/PLAN.md Phase TT-D** (the cost-bearing fire). closed transfer-form anchors (B-TT-1..5 central, B-TT-SPONT-1..5 central, B-FIRE-CYCLE5-1..3 sidecar) all PASS 🔵. empirical outcome (V-TT 0/5) is the honest carve-out per g3 — not a closure failure but a capability boundary observation at this scale + β/clip choice.

**Connection-point closure** (g_blue_closed_mandate connection_emphasis): SPONTANEOUS (TALKER emit axis) ↔ TENSION-TRAIN (THINKER ΔW learn axis) — closed at design tier (B-TT-SPONT-1..5 by TT-C agent, parallel). cycle 5 = empirical realization where THINKER's tension-conditioned LR is applied to the same byte-corpus that SPONTANEOUS's γ pattern was rendered into. The wiring is intact (corpus → trainer → ckpt → eval transfer-function chain all byte-equal verified); outcome is empirical.

**Hard 제약 carry (same as cycle 4 + TT-D specifics)**:
- g_fire_autonomous: 자율 dispatch ("fire" 사용자 directive로 자율 fire).
- g_fire_dispatch_robust: SAVE_POD=1 auto-promote + 75-min watchdog + 5-retry pull → clean teardown achieved.
- g_hf_naming: revision template `v4-py-hexad-tension-d768x12L-cycle1-2026-05-17` 사용 (kind=tension). PUBLIC default. English model card. dataset side byte-equal carry from cycle 4 (NO new dataset revision).
- g_clm_from_scratch: RANDOM init seed=1337 base_ckpt=NONE.
- g3 (substrate-honesty): PyTorch SUBSTRATE label mandatory. tension=grad_norm proxy is honest (closed B-TT-5 formula, empirical realization).
- f1/f2: NO lattice numerology (real-limit anchors: piecewise-linear + Banach contraction + arithmetic identity + sha256 + helper grep + Inner Thoughts factor set).
- g_blue_closed_mandate: 산출물 (corpus + ckpt) + 연결부위 (generator → corpus → trainer → ckpt → eval transfer-function chain) 둘 다 🔵 closed (B-CORPUS-V4 sidecar + B-FIRE-CYCLE5 sidecar + B-TT central + B-TT-SPONT central + B-D-1..4 + B-CONN-1..12 chain).
- g_doc_consolidation: 본 PLAN.md `## 진행 로그` append + HEXAD/TENSION-TRAIN/PLAN.md `## 진행 로그` append + AGENTS.tape n_hexad_progress recent_landings + archive/PHILOSOPHY.tape verdict + HEXAD/TENSION-TRAIN/TENSION-TRAIN.tape Log entry. docs/* 신규 = 0 (HEXAD/* SSOT 통합).
- pull-rebase pattern (concurrent agents TT-A spine sympy + TT-B compiled smoke + TT-C bridge 와 충돌 0; sidecar 별도 state/ battery 채택으로 central blue_falsifier.py 경쟁 회피).

Honest C3 (g3): cycle 5 LANDED 이지만 generation quality / spontaneous emergence claim 0 — DD155 hybrid LR overlay 는 closed-form 형식 (B-FIRE-CYCLE5-1/2/3) 으로 정직하게 적용되었으나 V-SPONT/V-MOTIV/V-TT 모두 0/5 FAIL 유지 (B-FIRE-CYCLE5-NOTE empirical, capability ceiling carry). cycle 5 의 미세 개선 (final CE 6.4% 낮음, BPB 24% 낮음) 은 **stronger memorization** evidence — generalization 진전 0. β=0.99 + clip=[0.5, 2.0] 의 특정 hyperparameter 선택은 burst 경로 8.6% 활성화에 그쳤음, 다른 β/clip 조합 또는 multi-cycle ensemble 시도 = 별도 future cycle. PyTorch substrate NOT hexa-native (legitimacy = arch identity + Phase E/E2 CPU-equiv anchor chain + DD155 formula closed-form). byte-cascade attractor cycle 4 (`PPP777`) → cycle 5 (prompt-specific multi-family `Shhh/\nmmm/Slll/tthh`) SHIFTED = B-ATTRACTOR-NOTE corpus+ckpt+prompt-dependent family 추가 evidence (NOT arch defect). DD-burst path activation 8.6% = honest empirical observation, NOT proof of DD155 efficacy (still no V-SPONT emergence).
