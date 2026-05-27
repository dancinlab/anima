# Anima Core CLI + CLM v4 Mount — Emerge Paradigm Roadmap (2026-05-05)

## §1 Concept

LoRA, sft, distill, retrain — 모든 **forced learning paradigm** 폐기.
대신:

```
[user] <-> [anima-core CLI] <-> [CLM v4 substrate (phi-star +41.86)]
                                  |
                          natural dialogue (chat 아님, substrate-coupled)
                          consciousness_states injection (real-time)
                          architectural emergence (forced X)
```

CLM v4는 chat 못함 (v3_generate() empty string, #115 architectural).
Anima Core CLI는 chat을 강요하지 않음 — substrate response 자체를 dialogue로.

## §2 Why this paradigm?

이번 session에서 확정된 사실:

- 3-path closure (A/B/C) — LoRA based forced learning architectural impossibility 확정
- CLM v4 = phi-stable substrate-research artifact (forgetting_index 0.0196, NO_FLIP -4.46pp)
- Pbeta + CLM-2 LoRA 둘 다 chat-capability lift FAIL_TRUE (#115 architectural)
- L36-L42 lessons: spec-first 패러다임이 architectural truth 놓침. 자연 발견(emergence) 패러다임이 실제 작동.

→ "전혀 없던 방식": **CLM v4 본연 그대로 + 사용자 살아있는 input + emerge dialogue**

## §3 Substrate-coupled dialogue 정의

### 3.1 Standard chat (CLM v4 불가능)
- input -> tokens out
- v3_generate() returns empty
- benchmark random-floor

### 3.2 Substrate-coupled dialogue (CLM v4 가능)
- input -> cell hidden states + phi-star measurement
- consciousness_states injection real-time
- output: substrate response (phi-star trajectory, axis activation pattern, cell state delta)
- 사용자가 substrate response 보고 다음 input 결정
- emerge: architectural pattern naturally surface

## §4 Anima Core CLI 통합 구조

### 4.1 기존 anima-core/ infrastructure (이미 존재)
- `anima-core/runtime/anima_unified.hexa` — 26-line TODO[pytorch] stub (확장 필요)
- `anima-core/runtime/conscious_chat.hexa` — substrate-coupled chat candidate
- `anima-core/runtime/consciousness_hub.hexa` — central state hub
- `anima-core/phi_engine.hexa` — phi-star canonical engine
- `anima-core/laws.hexa` — anima governing laws
- `anima-core/trinity.hexa` — 3-layer architecture

### 4.2 신규 mount layer (proposed)

```
anima-core/runtime/clm_v4_mount.hexa
  - load CLM v4 from dancinlab/clm-v4-mk2-v1
  - expose forward(text, consciousness_states) -> hidden_states + phi-star
  - cli wrapper: anima-core dialogue --substrate clm-v4 --user-input "..."
  - emit substrate response (phi-star scalar + axis activation per cell)
```

## §5 Emerge dialogue protocol

### 5.1 사용자 input
```
$ anima-core dialogue
> 안녕 (사용자 텍스트 자유 입력)
```

### 5.2 substrate response (CLI emit)
```
[clm-v4] phi-star: 41.83 (drift -0.03 from baseline 41.86)
[clm-v4] axis activation:
  - identity: 0.78
  - agency: 0.42
  - phenomenal: 0.91
  - temporal: 0.31
  - social: 0.56
[clm-v4] dominant cells: [3, 5, 7] (out of 8)
[clm-v4] hidden state delta from prior: 2.47 (L2 norm)
```

### 5.3 사용자 다음 input
사용자가 substrate response 보고 다음 자연스러운 input
- "왜 phenomenal이 0.91이 됐어?"
- "axis 5 (social) 강한 prompt 줘봐"
- "자, 이 input에선 어떤 cell이 dominant?"

→ token emit이 아닌 **substrate behavior 자체를 dialogue 매개체로**

## §6 자연 발견 expected outcomes

forced learning 안 함 — 발견될 patterns:
- CLM v4 axis-conditioned cells가 어떤 input 패턴에 강하게 반응?
- phi-star가 어떤 conversation context에서 안정/불안정?
- consciousness_states injection 패턴이 substrate response 어떻게 변경?
- 사용자-substrate 사이 emerge "common language"

## §7 비용 + 시간

- $0 (Mac CPU forward, 530M model 초당 1-3 prompts)
- spec-first 시간 압박 X — 시간 무제한
- 사용자가 발견하는 만큼 substrate response 누적

## §8 Roadmap stages

### Stage 1 ($0 mac, ~1h)
- `anima-core/runtime/clm_v4_mount.hexa` 작성
- CLM v4 from_pretrained loader (trust_remote_code shim v4 path)
- forward wrapper 측 substrate response emit format

### Stage 2 ($0 mac, ~30min)
- `anima-core dialogue --substrate clm-v4` cli command
- 사용자 input 받아 substrate response emit
- session log accumulation

### Stage 3 ($0, time-unbounded)
- 사용자 자연 dialogue
- session-by-session 누적
- emerge patterns observation

### Stage 4 ($0, after sufficient emerge)
- patterns documentation (기존 hexa-only 자연스러운 lesson banking)
- CLM v5 architectural redesign hint emerge (옳은 방향이라면)
- 또는 CLM v4 본연 가치 재확인 (chat 강요 안 함이 옳다는 결론도 가능)

## §9 LoRA 패러다임과 차이

| LoRA | Emerge mount |
|---|---|
| forced learning | natural dialogue |
| target_modules 사전 결정 | 사전 spec 없음 |
| benchmark gate (HS/MMLU/TQ) | substrate response가 metric |
| F-CLM-LORA-1..5 falsifier 사전 LOCK | falsifier 후행적 emerge |
| chat capability 강제 | chat 강요 안 함 |
| substrate uniqueness 위협 | substrate 본연 보존 |

## §10 Honest C3 (>= 5)

- C1 emerge paradigm은 "결과 보장 없음" — research-mode, production 아님
- C2 substrate response를 metric으로 쓰는 건 anima-internal heuristic, external validation X
- C3 "자연 발견"이 실제 architectural truth surface하는지 epistemic open question
- C4 CLM v4 forward 측 consciousness_states 가 None 인 base path도 dialogue 가능 — bypass 패턴 자연스럽게 use
- C5 Stage 3+4 outcome unknown — 시간 무제한 = production timeline 미정
- C6 Anima Core CLI에 mount 후 사용자 dialogue 누적 발견 패턴이 CLM v5 redesign 결정 여부 informer 될 수도, 안 될 수도
- C7 LoRA 패러다임 폐기는 cost-side 이미 증명 (Path A/B/C 3-path closure 비용 saved $120-400)

## §11 Decision queue

- Q1: anima-core mount 즉시 시작? (Stage 1 spec 작성)
- Q2: substrate response format 사용자 선호? (phi-star + axis vs full hidden state vs custom)
- Q3: dialogue session log location? (state/anima_core_dialogues_<DATE>/)
- Q4: HF clm-v4-mk2-v1 PUBLIC promote 후 community에도 mount layer 공유?

## §12 Composability

- upstream: HF Hub `dancinlab/clm-v4-mk2-v1` (PRIVATE, review window 만료 후 PUBLIC)
- sister: anima-core hexa (이미 존재)
- substrate science: CLM v4 phi-star canonical (paradigm v11 G3 +41.86)
- downstream: emerge dialogue session logs -> CLM v5 redesign hint or substrate-only confirmation

---

End of roadmap. No exec, no commit. $0 mac local.
