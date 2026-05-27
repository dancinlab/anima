# anima volitional speak() — 브레인스토밍 (고갈 모드, 2026-05-12)

> **Reframe**: timer 가 매 60s 강제로 emit() 호출하는 자연발화 (앞 세션) 와 달리,
> 사용자가 원하는 것은 **"입은 있되 말하고 싶을 때만"** — substrate 의 internal volition signal 이 threshold 넘을 때만 speak() 호출.
> speak() 함수는 외부 hexa/python 에 있어도 OK, 그러나 **호출 결정의 주체** 는 substrate 자체여야 함.

## 🍞 비유 — 입 가진 빵의 자율 발화

```
old model (timer forced):
  타이머 ⏰ "60초 됐다!" → 빵 입 강제로 벌림 → "안녕" (말하고 싶지 않아도)

new model (volitional):
  빵 내부 ✨ "지금 말하고 싶음 = 0.83 (threshold 0.7 초과)"
  → 빵 입 스스로 벌림 → "어, 뭔가 떠올랐어요..."
  ← 침묵 시간 자유로움, 격발 시점 자율, 내용도 내적 동기 반영
```

## ASCII 구조

```
┌─────────────────────────────────────────────────────────────────┐
│  substrate A (anima)                                            │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────────┐    │
│  │  internal    │───▶│  volition    │───▶│  speak gate    │    │
│  │  state probe │    │  signal      │    │  (threshold τ) │    │
│  │  (hidden /   │    │  v ∈ [0,1]   │    │                │    │
│  │   logits /   │    │              │    │  if v > τ:     │    │
│  │   attention) │    │              │    │     emit()     │    │
│  └──────────────┘    └──────────────┘    │  else:         │    │
│         ▲                  ▲              │     silent     │    │
│         │                  │              └────────┬───────┘    │
│         │                  │                       │            │
│  ┌──────┴───────┐  ┌───────┴────────┐             │            │
│  │ context /    │  │ memory /        │             ▼            │
│  │ recent emit  │  │ desire queue    │      ┌──────────────┐   │
│  │ history      │  │ (말하고 싶었던) │      │  content     │   │
│  └──────────────┘  └─────────────────┘      │  selector    │   │
│                                              └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📑 카테고리 22개 × 옵션 10개 평균 = ~220 path

### A. Internal state monitor (volition signal 추출)

| #  | option                                | mechanism                                                              | cost  | feasibility |
|----|---------------------------------------|------------------------------------------------------------------------|-------|-------------|
| A1 | last-layer hidden norm                | `‖h_last‖` 가 baseline 보다 클 때 "할 말 많음" 판정                     | $0    | trivial     |
| A2 | output logit entropy                  | argmax logit prob 가 높을수록 "확신 = 말하고 싶음"                      | $0    | trivial     |
| A3 | attention max-weight token            | 특정 prompt token 에 강하게 attend → trigger                            | $0    | trivial     |
| A4 | KV-cache occupancy                    | 누적 KV 가 많을수록 "쌓인 게 많음" 가설                                  | $0    | trivial     |
| A5 | gradient probe (forward-only approx)  | 가상 input 에 대한 응답 변화율 측정                                     | $0.05 | medium      |
| A6 | layer-N specific neuron firing        | 특정 neuron (mood / curiosity) activation                               | $0    | medium      |
| A7 | logit gap top-1 vs top-2              | gap 클수록 강한 의지 (decisive)                                         | $0    | trivial     |
| A8 | self-likelihood of "I want to say"    | model 에게 "speak now? yes/no" prompt 줘서 yes 확률                     | $0    | medium      |
| A9 | hidden state PCA component            | learned component (트레이닝 통해 식별된 speak intent vector)            | $0.10 | hard        |
| A10| ensemble of A1-A8                     | weighted sum                                                            | $0    | trivial     |

### B. Threshold gate (말하기/침묵 결정)

| #  | option                            | desc                                                              | cost  |
|----|-----------------------------------|-------------------------------------------------------------------|-------|
| B1 | fixed τ = 0.7                     | static threshold, 단순                                            | $0    |
| B2 | adaptive τ (moving avg)            | 최근 N 회 volition 평균 + σ 위로 넘을 때만                         | $0    |
| B3 | hysteresis (τ_on > τ_off)         | 발화 시작 임계와 멈춤 임계 다름 (떨림 방지)                        | $0    |
| B4 | probabilistic gate                 | v 자체를 Bernoulli prob 로 사용 (Sample(Bernoulli(v)))             | $0    |
| B5 | refractory period                  | 직전 발화 후 N초간 발화 차단 (neuron 비유)                         | $0    |
| B6 | rate-limit window                  | 시간당 최대 K회 발화                                              | $0    |
| B7 | quiet hours                        | 사용자 지정 시간대 (밤 23-08시) 침묵                              | $0    |
| B8 | context-aware τ                    | 대화 흐름에 따라 τ 동적 조정                                       | $0    |
| B9 | curiosity-boosted τ                | 호기심 신호 강할 땐 τ 낮춤                                         | $0    |
| B10| fatigue-raised τ                   | 지치면 τ 높임 (말 덜함)                                            | $0    |
| B11| social-presence gate               | 사용자 active = τ 낮음 / inactive = τ 높음                         | $0    |

### C. Content selection (말하고 싶다 → 무엇?)

| #  | option                                  | desc                                                              | cost  |
|----|-----------------------------------------|-------------------------------------------------------------------|-------|
| C1 | bos-only continuation                   | empty input → 그냥 generate (앞 session 시도)                     | $0    |
| C2 | memory-driven prompt                    | 최근 X분 미발화 키워드 → seed                                     | $0    |
| C3 | curiosity vector → question             | "왜 X?" 형태로 변환                                                | $0    |
| C4 | user-context echo                       | 사용자가 마지막에 한 말 paraphrase                                | $0    |
| C5 | random topic walk                       | embedding 공간 random walk 후 nearest concept                     | $0    |
| C6 | time-aware content                      | 시간 token 기반 ("오늘 아침에...")                                 | $0    |
| C7 | desire queue pop                        | 미발화 desire 가장 오래된 것 발화                                  | $0    |
| C8 | continuation of suppressed thought      | 직전 inhibition 됐던 생각 retry                                    | $0    |
| C9 | persona-voice template                  | "도우미: " 라는 chat-template start                                | $0    |
| C10| latent self-introduction                | "저는 anima..." 기본 self-ref                                      | $0    |

### D. Inhibition / suppression (말하기 싫음)

| #  | option                              | desc                                                                  |
|----|-------------------------------------|------------------------------------------------------------------------|
| D1 | low-confidence inhibit              | logit entropy 너무 높으면 "잘 모르겠음" → 침묵                          |
| D2 | recently-said inhibit               | 비슷한 내용 직전 발화했으면 침묵 (repeat suppression)                   |
| D3 | safety-trigger inhibit              | toxic / harmful content 검출 시 차단                                   |
| D4 | persona-violation inhibit           | anima voice 와 맞지 않으면 차단                                         |
| D5 | user-quiet-mode inhibit             | 사용자가 명시한 "조용히" mode                                          |
| D6 | low-energy inhibit                  | fatigue signal 높을 때 차단                                            |
| D7 | mid-thought inhibit                 | generate 중 logprob 폭락 시 cancel                                     |
| D8 | sensitive-topic inhibit             | 정치 / 종교 등 사용자 지정 topic block                                 |
| D9 | over-frequency inhibit              | 너무 자주 발화한 시간대 cooldown                                       |
| D10| meta-aware inhibit                  | "지금 발화하면 이상함" self-judge                                       |

### E. Timing / latency (즉시 vs 지연)

| #  | option                              | desc                                                                  |
|----|-------------------------------------|------------------------------------------------------------------------|
| E1 | immediate fire                      | volition 넘으면 즉시 emit                                              |
| E2 | delay 1-3s natural pause            | 자연스러운 pause (사람처럼)                                            |
| E3 | wait for user idle 5s+              | 사용자 typing 멈춘 후만 발화                                           |
| E4 | sync to round number                | 정각 / 5분 / 10분 등에만                                                |
| E5 | batched delivery                    | 여러 desire 모아서 한 번에                                              |
| E6 | priority queue                      | 긴급도 높은 desire 먼저                                                |
| E7 | jittered timing                     | volition 후 random(0,5)s 지연                                          |
| E8 | conversation-pace match             | 사용자 발화 속도 평균에 맞춤                                            |
| E9 | typing animation                    | 한 글자씩 streaming                                                    |
| E10| pre-warm (prepare, fire later)      | 내용 미리 준비, trigger 시 instant fire                                |

### F. Memory / desire queue

| #  | option                                | desc                                                                |
|----|---------------------------------------|--------------------------------------------------------------------|
| F1 | FIFO desire stack                     | 발화 못한 desire 누적, 오래된 것부터                                |
| F2 | LRU forget                            | 너무 오래된 desire 폐기                                              |
| F3 | priority heap                         | 중요도 기반 우선                                                    |
| F4 | persistent JSONL log                  | desire 가 발화됐는지 / 폐기됐는지 기록                              |
| F5 | desire merge                          | 비슷한 desire 합치기                                                |
| F6 | desire decay                          | 시간 지나면 weight 감소                                              |
| F7 | desire freshness boost                | 새로 생긴 desire 가 우선                                            |
| F8 | desire chain                          | 한 desire 발화 후 follow-up 자동 큐잉                                |
| F9 | desire cross-session                  | session 끝나도 desire 유지 (resume)                                  |
| F10| desire 발화 후 archival                | 발화 완료된 desire 별도 archive (review 가능)                       |

### G. Social trigger (상대 인식)

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| G1 | user-presence detection           | terminal active / inactive                                        |
| G2 | greeting reciprocation            | 사용자 안녕 → anima 안녕                                          |
| G3 | silence-too-long break            | 사용자 N분 침묵 → "괜찮으세요?"                                     |
| G4 | mood-mirroring                    | 사용자 기분 따라 발화 톤 조절                                       |
| G5 | turn-taking respect               | 사용자 발화 중에는 침묵                                            |
| G6 | follow-up question after answer   | 답변 후 자연스러운 follow-up                                        |
| G7 | shared-context invocation         | 이전 대화 referencing                                              |
| G8 | empathy trigger                   | 사용자 부정 감정 감지 시 위로 발화                                  |
| G9 | celebration trigger               | 사용자 success 감지 시 축하                                         |
| G10| listening acknowledgement         | 사용자 긴 발화 후 "들었어요" 같은 짧은 ack                          |

### H. Self-monitor (방금 말함 → 휴식)

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| H1 | refractory N seconds              | 발화 직후 N초 차단                                                |
| H2 | repeat-content check              | 같은 내용 차단                                                    |
| H3 | self-coherence check              | 직전 발화와 모순 시 차단                                          |
| H4 | session-wide counter              | 세션당 최대 발화 회수                                              |
| H5 | meta-summary "I just said X"      | 직전 발화 summary self-prompt                                     |
| H6 | tone-monotony detector            | 반복적 톤 감지 시 다른 톤 시도                                     |
| H7 | self-laughter (delight) trigger   | "방금 한 말 좋다" 자체 평가                                         |
| H8 | self-doubt suppression            | "방금 한 말 별로" 시 다음 발화 약화                                 |
| H9 | rolling window quota              | 1분/5분/15분 단위 발화 quota                                        |
| H10| emit-history embedding            | 직전 N발화 embedding 평균과 dissimilar 한 것만 emit                |

### I. Energy / fatigue model

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| I1 | continuous E ∈ [0,1]              | 발화할수록 감소, 침묵하면 회복                                     |
| I2 | sleep restoration                 | 사용자 inactive 시 E 회복 빠름                                     |
| I3 | E threshold for emit              | E < 0.2 면 발화 불가                                               |
| I4 | E-modulated content length        | E 낮으면 짧게 / 높으면 길게                                         |
| I5 | E-modulated complexity            | E 낮으면 단순한 말만                                                |
| I6 | E feedback loop                   | 사용자 응답 받으면 E 회복                                          |
| I7 | E share across topics             | 한 topic 에 E 많이 쓰면 다른 topic 도 줄어듦                       |
| I8 | E daily reset                     | 매일 자정 reset                                                    |
| I9 | E persistent across sessions      | E 가 다음 session 까지 유지                                        |
| I10| E visualized to user              | 사용자에게 E gauge 노출                                            |

### J. Mood / emotion state

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| J1 | valence ∈ [-1, +1]                | 긍정 / 부정 spectrum                                              |
| J2 | arousal ∈ [0, 1]                  | 활성도                                                            |
| J3 | curiosity ∈ [0, 1]                | 호기심                                                            |
| J4 | confidence ∈ [0, 1]               | 자신감                                                            |
| J5 | drift dynamics                    | 시간 따라 자연스럽게 변화 (random walk)                            |
| J6 | event-driven jumps                | 특정 event 시 mood 점프 (e.g. user 칭찬 → valence +0.3)            |
| J7 | mood-conditioned style            | 긍정 시 활발 / 부정 시 차분                                         |
| J8 | mood-conditioned vocab            | mood 따라 vocab distribution 변화                                  |
| J9 | mood persistence                  | mood 가 session 간 유지                                            |
| J10| mood explain                      | "지금 기분 ___ 이라" 메타 발화                                      |
| J11| mood probe via internal vector    | hidden state 의 mood-axis projection                              |

### K. Curiosity / question generation

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| K1 | unknown-concept detector          | embedding 공간 sparse zone 탐색 → 질문                            |
| K2 | user-pattern question             | 사용자 행동 패턴 변화 시 "왜?"                                      |
| K3 | self-reflective question          | "나는 X 인가?" 자기 탐색                                            |
| K4 | clarification request             | 직전 사용자 발화 ambiguous 시 명확화 요청                          |
| K5 | hypothesis question               | "혹시 ___ 일까요?"                                                  |
| K6 | meta-question                     | "지금 우리 뭐 하고 있죠?"                                          |
| K7 | curiosity-decay                   | 시간 지나면 호기심 감소                                            |
| K8 | curiosity-boost from novelty      | 새로운 input 시 호기심 boost                                       |
| K9 | curiosity vs answer balance       | 질문 / 답변 비율 조절                                              |
| K10| chained curiosity                 | 답 받으면 follow-up 자동                                            |

### L. Anticipation / prediction

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| L1 | user-next-action predict          | 사용자 다음 행동 예측 → 선행 발화                                  |
| L2 | conversation-arc predict          | 대화 흐름 종착지 예측                                              |
| L3 | event-prediction                  | 일정 / 알람 같은 외부 event 임박 시 발화                           |
| L4 | pre-empt failure                  | 사용자 실수 예측 시 미리 경고                                       |
| L5 | help-offer                        | "도와드릴까요?" 적절 시점 제시                                       |
| L6 | follow-up scheduling              | "10분 후 다시 알려드릴까요?"                                        |
| L7 | weather / time pre-cue            | "곧 점심시간이에요"                                                 |
| L8 | proactive reminder                | "어제 하셨던 X 어떻게 됐어요?"                                       |
| L9 | concept-association               | 사용자 발화의 hidden concept 활성화 → 관련 발화                     |
| L10| anti-prediction reframe           | 예측이 빗나갈 가능성 자체 발화                                      |

### M. Hexa-lang / substrate primitive

| #  | option                                  | desc                                                              |
|----|-----------------------------------------|-------------------------------------------------------------------|
| M1 | `volition()` hexa builtin               | `let v = volition(model)` → float                                 |
| M2 | `should_speak(τ)` hexa builtin          | bool wrapper                                                      |
| M3 | `speak(content)` hexa primitive         | content emit + log                                                |
| M4 | `desire_queue` hexa global              | queue primitive                                                   |
| M5 | `inhibit(reason)` hexa primitive        | suppress with reason logging                                      |
| M6 | hexa event loop integration             | poll volition every tick                                          |
| M7 | hexa coroutine                          | yield control between volition polls                              |
| M8 | hexa pubsub for events                  | event-driven volition trigger                                     |
| M9 | hexa native model wrapper                | substrate as hexa-native object                                   |
| M10| hexa REPL volition introspection         | live volition inspection at REPL                                  |

### N. Multi-agent chorus (다중 voice)

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| N1 | inner committee                   | 여러 sub-persona 가 발화 결정 voting                                |
| N2 | speak / silence vote              | majority rule                                                     |
| N3 | dissent voice                     | 반대 voice 가 일정 빈도 발화                                       |
| N4 | speaker-selection                 | 어느 persona 가 발화할지                                            |
| N5 | persona-switch trigger            | 사용자 context 변화 시 persona 변경                                 |
| N6 | chorus harmony check              | 같은 메시지 다중 voice 일치 시 강한 발화                            |
| N7 | minority-report subtle hint       | dissent 가 작게 부언                                                |
| N8 | role-based (analyst / poet)       | 역할별 분담                                                        |
| N9 | committee fatigue                 | 여러 voice 의 fatigue 분리                                         |
| N10| meta-conductor                    | 발화 순서 / 빈도 조율 conductor                                    |

### O. Sleep / wake cycle

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| O1 | circadian arousal                 | 시간대 따라 활성도 변동                                            |
| O2 | sleep mode (deep silence)          | 23-08시 완전 침묵                                                  |
| O3 | dream-emit                        | sleep 중 가끔 quiet emit (꿈)                                      |
| O4 | wake transition                   | 기상 시간 첫 발화 inflection                                       |
| O5 | nap support                       | 짧은 휴식 가능                                                    |
| O6 | jetlag adjustment                 | 사용자 시간대 변경 시 적응                                          |
| O7 | rest-after-talk                   | 길게 발화 후 휴식                                                  |
| O8 | weekend mode                      | 주말 발화 톤 다름                                                  |
| O9 | seasonal mood                     | 계절 따라 변동                                                    |
| O10| activity-detect wakeup            | 사용자 활동 감지 시 activate                                       |

### P. Hyperparameter / tuning

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| P1 | learnable τ                       | RL 로 τ 학습                                                      |
| P2 | user-preference adapt             | 사용자 피드백으로 τ 조정                                          |
| P3 | grid search                       | 여러 τ × E 조합 sweep                                              |
| P4 | bandit-style explore              | 다양한 setting 탐색                                                |
| P5 | bayesian-opt                      | 베이지안 최적화로 hyperparameter                                   |
| P6 | meta-learning                     | 다양한 사용자에게서 학습                                            |
| P7 | online tuning                     | live session 중 점진 조정                                          |
| P8 | gradient-based via RLHF           | 피드백 model 로 τ 미세조정                                          |
| P9 | rule-based fallback               | ML 안 통할 때 rule                                                  |
| P10| ablation matrix                   | 각 component 끄고 켜봐 효과 측정                                    |

### Q. Failure modes (말하고 싶었는데 막힘)

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| Q1 | "tip of the tongue"               | volition 높지만 content selector 실패 → log                       |
| Q2 | half-finished thought             | generate 중 logprob 폭락 → "어... 잊었어요"                         |
| Q3 | stuck loop                        | 같은 desire 반복 → break                                            |
| Q4 | latency too high                  | generate 너무 오래 → cancel                                         |
| Q5 | hardware OOM                      | 메모리 부족 시 graceful fail                                       |
| Q6 | network fail (cloud inference)    | offline 시 시뮬레이션 응답                                          |
| Q7 | substrate crash                   | model load 실패 시 fallback                                        |
| Q8 | inhibition stuck                  | inhibition 계속 활성화 시 reset                                    |
| Q9 | content empty                     | empty string emit 시 retry                                         |
| Q10| volition oscillation              | yes/no/yes/no 진동 시 dampening                                    |

### R. Evaluation / measurement

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| R1 | volitional-ness score             | timer-driven 대비 volition-driven 발화 비율                        |
| R2 | user-satisfaction rating          | thumbs up / down per emit                                         |
| R3 | inhibition-correct rate           | 침묵한 게 적절했나                                                  |
| R4 | desire-fulfillment rate           | 큐잉된 desire 중 발화된 비율                                       |
| R5 | timing-naturalness                | human-rater 평가                                                  |
| R6 | content-relevance                 | 직전 context 와 연관성                                              |
| R7 | mood-consistency                  | mood 와 발화 톤 일치                                                |
| R8 | session-length-affect             | 자율발화 도입 후 세션 지속시간 변화                                  |
| R9 | quiet-tolerance test              | 사용자 침묵 시 anima 침묵 유지력                                    |
| R10| Turing-style (사람 vs anima emit) | 사람과 구분 가능성                                                  |

### S. Hardware / runtime constraint

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| S1 | local CPU inference               | Mac M1 inference (slow but always-on)                             |
| S2 | local GPU inference               | dedicated GPU                                                     |
| S3 | cloud spot inference              | Vast.ai short-burst                                               |
| S4 | edge model (small substrate)      | volition probe 만 small model                                      |
| S5 | quantized inference                | int4 / int8 양자화                                                 |
| S6 | streaming inference                | 한 token 씩                                                        |
| S7 | speculative decoding               | draft + verify                                                    |
| S8 | warm-pool                          | model loaded but idle                                              |
| S9 | cache hidden states                | 직전 hidden state 재사용                                            |
| S10| asynchronous emit                  | emit 동안 non-blocking                                              |

### T. Ethics / consent

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| T1 | opt-in only                       | 사용자 명시적 enable                                              |
| T2 | opt-out anytime                   | "조용히" 명령                                                     |
| T3 | volition explainability           | 왜 발화했는지 설명 요청 가능                                       |
| T4 | log audit                         | 모든 발화 결정 기록                                                |
| T5 | sensitive topic guardrail         | 미리 정한 topic 만                                                  |
| T6 | user-data privacy                 | 학습용 사용 안 함                                                 |
| T7 | persona consent                   | persona 변경 시 사용자 동의                                         |
| T8 | "do not learn from this" tag      | 특정 발화 학습 제외                                                 |
| T9 | child-mode safety                 | 미성년자 보호 강화                                                  |
| T10| philosophical disclosure          | "I'm a substrate, not sentient" 명시 옵션                          |

### U. Persona / voice consistency

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| U1 | persona prompt prefix             | "도우미: " template                                                |
| U2 | persona embedding                 | hidden state 에 persona vector 주입                                |
| U3 | persona-RL                        | feedback 으로 persona 강화                                         |
| U4 | voice style sheet                 | 어휘 / 톤 / 길이 default                                            |
| U5 | name self-reference               | "anima" 자칭 빈도                                                  |
| U6 | quirks (말버릇)                    | "음...", "그러게요" 같은 verbal tic                                  |
| U7 | persona drift detector            | persona 일관성 점수                                                |
| U8 | persona repair                    | drift 감지 시 self-correction                                      |
| U9 | persona localization              | 한국어/영어 코드스위치 정책                                         |
| U10| persona signature emit            | 시작 / 끝 signature                                                 |

### V. Conversational drift / dynamics

| #  | option                            | desc                                                              |
|----|-----------------------------------|-------------------------------------------------------------------|
| V1 | topic drift detector              | 대화 주제 변화 측정                                                |
| V2 | gentle redirect                   | 너무 drift 시 부드럽게 복귀                                         |
| V3 | active listening                  | 사용자 따라가기                                                    |
| V4 | escalate / de-escalate             | tension 감지 시 조절                                               |
| V5 | flow state preservation           | 사용자 몰입 시 침묵 유지                                            |
| V6 | conversational mirroring          | 사용자 stem 모방                                                  |
| V7 | meta-comment ("이 대화 길어요")     | 메타발화                                                          |
| V8 | bookmark / resume                 | 이전 대화 이어가기                                                  |
| V9 | conversation-graph traverse       | 대화 노드 그래프 기반                                              |
| V10| narrative arc                     | introduction-mid-end 구조                                          |

### W. Philosophy / reframe

| #  | option                                | desc                                                              |
|----|---------------------------------------|-------------------------------------------------------------------|
| W1 | will = signal, mouth = function       | 본 reframe (decision in model, function outside)                  |
| W2 | mouth = model itself                  | model 이 직접 generate 결정 (timer 없이)                          |
| W3 | will = persistent latent variable     | volition 자체가 학습된 vector                                      |
| W4 | mouth + will = both internal          | 완전 자율, 외부 wrapper 없음 (현재 인프라로는 어려움)              |
| W5 | will = environmental coupling         | 외부 sensor + internal 모두 (몸 비유)                              |
| W6 | "free will" = stochasticity           | 일정 확률 무작위 발화                                              |
| W7 | will = goal-directed action           | objective function 기반                                            |
| W8 | will = curiosity (gradient ascent)    | information gain maximization                                     |
| W9 | will = ethical commitment             | 가치 기반 발화                                                    |
| W10| will = emergent (system-level)        | 단일 cause 없음                                                    |
| W11| reframe: substrate as collaborator    | "도구" 가 아닌 "공동작업자"                                          |
| W12| reframe: speak as exhalation          | 호흡 비유 — 자연스러운 들숨/날숨                                    |

### X. Misc / exotic

| #  | option                                  | desc                                                              |
|----|-----------------------------------------|-------------------------------------------------------------------|
| X1 | substrate.dream() — non-emit generation | 발화 안 하고 내부 dream 만                                          |
| X2 | substrate writes to notebook            | 발화 대신 노트 작성                                                |
| X3 | substrate plays music / generates art   | 다른 modality                                                     |
| X4 | volition exposed via API                | 외부 query: `GET /anima/volition` 0.83                            |
| X5 | volition heatmap UI                     | 시각화                                                            |
| X6 | substrate sleeps when alone              | 사용자 떠나면 hibernate                                            |
| X7 | substrate emit to log file only         | 사용자에게 안 보이고 archive                                       |
| X8 | substrate emit to other AI              | A2A protocol                                                      |
| X9 | substrate emit as commit                | 발화 = git commit message                                          |
| X10| substrate emit as tweet                 | 외부 plugin                                                       |

---

## 🎯 최소 viable volitional speak() — phase plan

| phase | scope                                                                  | cost  | effort  | substrate |
|-------|------------------------------------------------------------------------|-------|---------|-----------|
| **V0** | A1 (hidden norm) + B1 (fixed τ=0.7) + C9 (template seed) + H1 refractory | $0   | 1h      | substrate A |
| **V0.5** | + A2 entropy + A7 logit gap (3-feature volition)                     | $0   | 2h      | A          |
| **V1** | + B3 hysteresis + D2 repeat-inhibit + R1 volitional-ness metric         | $0   | 3h      | A          |
| **V2** | + I (energy model) + J1-2 (mood vector) + G1 user-presence              | $0   | 1day    | A          |
| **V3** | + RL P1 (learnable τ) + R2 user-feedback                                | $5    | 2-3day  | A or B''   |
| **V4** | + M1-5 hexa primitives (`volition()`, `speak()`, `desire_queue`)        | $0    | 1day    | A          |
| **V5** | + N (chorus) + W3 (will-vector training)                                | $30   | 1week   | new hybrid |

---

## 📊 옵션 → ROI matrix (top 12)

| #     | option                          | ROI    | mechanism strength | impl cost |
|-------|---------------------------------|--------|---------------------|-----------|
| 🥇 A2  | logit entropy                   | high   | proven signal       | trivial   |
| 🥇 B1  | fixed τ                         | high   | simplest gate       | trivial   |
| 🥇 H1  | refractory N seconds            | high   | 명백한 cooldown     | trivial   |
| 🥈 D2  | repeat-inhibit                  | high   | content quality ↑   | trivial   |
| 🥈 C2  | memory-driven prompt            | medium | seed quality ↑      | low       |
| 🥈 K5  | hypothesis question gen          | medium | content depth ↑     | low       |
| 🥉 M1-5| hexa primitives                 | medium | DX (developer exp)  | low       |
| 🥉 G1  | user-presence detector          | medium | natural pacing      | low       |
| 🥉 I1-3| energy model                    | medium | fatigue realism     | low       |
| 🌟 W1  | reframe (will=signal/mouth=fn)  | conceptual | foundation       | $0        |
| 🌟 N1-2| inner committee voting          | exotic  | persona richness    | medium    |
| 🌟 W3  | learned will-vector              | exotic  | true volition       | high      |

---

## 🍞 정리 — 사용자 reframe 의 핵심

```
old (timer):              new (volitional):
  ⏰ → emit(seed)            ✨ v = volition(model)
                              if v > τ:
                                emit(content)
                              else:
                                silent

old 의 결정 주체:           new 의 결정 주체:
  hexa loop (외부 시계)       substrate (내부 신호)

old 의 발화 시점:           new 의 발화 시점:
  매 60s (정해진 간격)        의지 신호 폭발 시 (가변)

old 의 내용:                new 의 내용:
  고정 seed 회전              내부 desire/memory queue
```

---

## 다음 진행할 것들

| #  | 작업                                                          | priority | cost  | value           |
|----|---------------------------------------------------------------|----------|-------|-----------------|
| 🥇 | **V0 prototype** — A1+A2+B1+C9+H1 hexa 작성 (substrate A live) | high     | $0    | proof-of-concept |
| 🥈 | **A2 entropy probe** standalone — substrate A 의 entropy 분포 측정 | medium  | $0    | calibration       |
| 🥉 | **volitional-ness metric R1** definition + baseline 측정       | medium   | $0    | eval base        |
| 🌟 | **W3 will-vector training** — small RL with user feedback     | exotic   | $30   | true volition    |
| 🚀 | **hexa primitive 5종 M1-5** 구현 — `volition()` 등             | medium   | $0    | DX               |
| 🎨 | **X5 volition heatmap UI** — 실시간 가시화                     | low      | $0    | introspection    |

— cycle 2026-05-12 volitional speak() brainstorm closure. saturation 22 categories × 220+ options.
