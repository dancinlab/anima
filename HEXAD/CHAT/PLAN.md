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

- **C1**: TENSION-LINK + VOICE + (future) CLI/Telegram channels 통합 — `channels/channel_manager.py` (ready/ 참조) 의 hexa-native 포팅
- **C2**: Murati Interaction Model 패턴 — 200ms micro-turn 시뮬레이션 (text-only 한정, audio-native 는 future RFC)
  - `barge-in` 지원 (사용자 input mid-emission → interrupt)
  - `backchanneling` 시뮬레이션 (저-confidence 시 "음...", "잠시...")
  - `simultaneous` thinker-talker (Thread async)
- **C3**: anima_chat.hexa rewrite — `chat_alive()` 통합 entry (thinker-talker dual-thread launcher)
- **C4**: `launch.hexa` update (`anima watch` 가 자연발화 expression view)
- **acceptance**: chat_alive demo + interaction model 패턴 5/5 + integration test PASS

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
