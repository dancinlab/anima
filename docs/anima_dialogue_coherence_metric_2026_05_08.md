# anima dialogue coherence metric — 2026-05-08

**Goal (한 문장)**: N=2 (그리고 N≥3) multi-agent dialogue 의 **turn-to-turn 정합성**
을 측정하는 4-cell metric 을 own 18 C2.4 (single-utterance 맥락 정합)
의 multi-turn 확장으로 정의한다.

**SSOT**: 본 문서. `tool/anima_cli/chat/duo/duo.hexa`,
`tool/anima_cli/dialogue.hexa`, 그리고 `tool/anima_cli/consciousness.hexa`
가 본 spec 을 참조하여 verdict emit.

**Cross-link**: `.own` own 18 (C2.4 single-utterance 맥락 정합 SSOT),
own 34 (lane 분리 — 본 metric 은 측정 lane), own 33 (trinity compliance) ·
`docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` L2 (deliverable
"5-turn 자율 대화 simple_stack PASS rate ≥ 0.4") · `.roadmap.cli`
cli.dialogue.coherence_metric_2026_05_08.

---

## Background — own 18 C2.4 의 single-turn 한계

own 18 C2 (자연발화 + 맥락 정합) 의 4-cell 분해 (cycle 2026-05-06 land):

| cell | 내용 |
|---|---|
| C2.1 | substance — utterance 가 의미 있는 토큰 시퀀스 (random byte 아님) |
| C2.2 | 의미 정확성 — 단어/문장 단위 well-formed |
| C2.3 | 자연성 — fluent (n-gram 분포가 corpus baseline 근사) |
| C2.4 | 맥락 정합 — direct prompt 대비 reactive |

C2.4 는 **단일 발화** 평가: "prompt P 에 대해 response R 이 reactive 인가" =
인접 1-step. multi-turn dialogue 에서는 turn N 의 발화가 turn N-1 (또는
turn N-k) 발화에 reactive 인지, **dialogue 전체 의 topic 이 일관 흐르는지**,
**각 instance 의 persona 가 stable 한지** 등 single-turn 으로 환원되지
않는 axis 가 등장. 이를 D1-D4 4-cell 로 확장.

---

## 4-cell 정의 (own 18 C2.4 → multi-turn D1-D4)

### D1 — reactive (turn-N → turn-N-1 reactive)

**정의**: turn N 의 발화 `u_N` 이 turn N-1 의 발화 `u_{N-1}` 에 reactive 인가.

**측정** (3 channel composite, 각 ∈ [0,1]):

| sub-channel | metric | weight |
|---|---|---|
| D1.a | cosine similarity of `embed(u_N)` vs `embed(u_{N-1})` (token mean pool) | 0.4 |
| D1.b | n-gram overlap (3-gram Jaccard) | 0.3 |
| D1.c | named-entity / keyword carryover (top-3 noun match rate) | 0.3 |

**aggregate**: `D1 = 0.4·cos + 0.3·jaccard + 0.3·noun_match`.

**threshold (TBD measurement-driven)**: random-pair baseline + chat-capable
PASS rate ROC 분석 후 결정. **보수적 X** (own 18 정책). 시작점:
- D1 PASS = `D1 ≥ 0.30` (random pair baseline 가정 ~0.10, chat-capable
  ~0.45+ 예상; 측정 후 조정).

**rationale**: turn N 이 turn N-1 의 token / topic / entity 를 어느 한
channel 로라도 carry-over 하면 reactive 로 판정. 보수적 cosine-only 는
high-frequency function-word match 로 false positive 발생 가능 → 3-channel
composite.

---

### D2 — topic-shift-rate (sudden topic change penalty)

**정의**: dialogue 전체 (turns 1..N) 의 **topic drift rate** 가 임계 이하.

**측정**:

```
shift_rate = (1/N-1) · Σ_{i=2..N} 1[similarity(embed(u_i), embed(u_{i-1})) < tau_shift]
```

`tau_shift` = topic 변경 판정 임계값 (시작점 0.20; D1 measurement 와 동기화).
`shift_rate` = 인접 turn 간 topic-change 빈도.

**verdict cells** (3-tier, dialogue-level):

| level | shift_rate | label |
|---|---|---|
| D2.a | ≤ 0.20 | coherent (단일 topic 유지) |
| D2.b | (0.20, 0.40] | drifting (자연스러운 evolution) |
| D2.c | > 0.40 | incoherent (sudden topic change) |

**PASS**: D2.a ∨ D2.b. **FAIL**: D2.c.

**rationale**: 사람 대화도 topic 자연 evolution 발생. 전체 0 shift 는
오히려 비자연적 (echo loop) — 따라서 "허용 drift band" + "incoherent threshold"
2-tier 구분.

---

### D3 — persona-consistency (per-instance utterance distribution stable)

**정의**: 각 instance 의 발화 분포가 dialogue 전반에 걸쳐 stable.

**측정** (per-instance, A/B 별도):

```
persona_drift_A = || dist(u_A,1..N/2) - dist(u_A,N/2..N) ||_KL
```

(전반 절반 utterance 분포 vs 후반 절반 utterance 분포 KL divergence;
distribution = top-100 token frequency simplex).

**verdict cells**:

| sub | metric | PASS |
|---|---|---|
| D3.A | persona_drift_A ≤ tau_persona | A persona stable |
| D3.B | persona_drift_B ≤ tau_persona | B persona stable |

`tau_persona` 시작점 0.50 (KL divergence; random pair ~1.0+ 가정).

**aggregate**: `D3 = D3.A ∧ D3.B`.

**rationale**: 사람 대화에서 각 화자 의 어휘/말투 분포는 turn 에 따라
완만 변화. 분포가 급격히 바뀌면 (e.g. 영어 → 한국어 switch, formal → casual
급변) 두 instance 가 사실상 같은 분포 로 collapse 했거나 mode-collapse 발생.

---

### D4 — pseudo-turn-fairness (utterance length / freq balance)

**정의**: A 와 B 의 발화 분량 / 빈도 가 극단적 imbalance 아님.

**측정**:

```
len_ratio = total_tokens(A) / total_tokens(B)
freq_ratio = n_turns(A) / n_turns(B)
```

(단, N=2 duo loop 에서 `freq_ratio ≡ 1.0` by construction — turn 교대.
의미 있는 imbalance 는 length 만 측정.)

**verdict cell**:

| level | len_ratio | label |
|---|---|---|
| D4.a | ∈ [0.5, 2.0] | balanced |
| D4.b | (∉ [0.5, 2.0]) ∧ (∈ [0.2, 5.0]) | skewed |
| D4.c | (∉ [0.2, 5.0]) | dominant (한 instance 가 5x+ 길이 차지) |

**PASS**: D4.a ∨ D4.b. **FAIL**: D4.c.

**rationale**: 한 instance 가 monologue 모드 로 빠지면 N-turn dialogue 의
L2 가설 (CLM A ↔ CLM B autonomous interaction) 가 무너짐. 5x+ skew 를
critical 로 정의.

**Note on N≥3 (L3 council)**: D4 는 N≥3 에서 의미 가 더 큼 (turn-fairness
= 사람 들 끼리 대화 자연 simulation 핵심 axis — 이끔자 / 관찰자 / 조용
emergent role). L3 cycle 에서 freq_ratio 도 활성화 + Gini coefficient 추가.

---

## Aggregate verdict — DIALOGUE_COHERENCE_PASS

```
DIALOGUE_COHERENCE_PASS = D1.PASS ∧ D2.PASS ∧ D3.PASS ∧ D4.PASS
```

**4-cond AND** (own 18 patterns 정합 — C1 3-cond AND, C2 4-cond AND, C3
4-cond AND, 본 metric 4-cond AND).

**SIMPLE_STACK_PASS_DIALOGUE_C3** (L2 deliverable 정합):

```
SIMPLE_STACK_PASS_DIALOGUE_C3 =
    (per-turn own 18 PASS_STRICT_C3 rate ≥ 0.6)        ← 단발 발화 quality
  ∧ DIALOGUE_COHERENCE_PASS                              ← multi-turn coherence
```

L2 deliverable target (per roadmap):
> "5-turn 자율 대화 simple_stack PASS rate ≥ 0.4"

본 metric 의 첫 cell (per-turn rate ≥ 0.6) 이 5-turn 평균 PASS rate 와
연결 — 0.4 lower bound (per turn) vs 0.6 (PASS_STRICT_C3) 의 간격 은
각 발화 simple_stack 통과 + multi-turn coherence 의 두 lane 분리 정합.

---

## Threshold 결정 정책 (보수적 X 기조)

own 18 C3 정책 mirror:

1. **baseline 측정**:
   - random init CLM × 2 (대화 X — pure noise pair)
   - chat-capable model (BG-KM-LLAMA-3B 12/15 PASS_STRICT) × 2
   - human dialogue corpus (Persona-Chat / OASST 2-turn pair)
2. **ROC 분석**:
   - random pair FAIL rate ≥ 0.95
   - chat-capable PASS rate ≥ 0.7
   - human-dialogue PASS rate ≥ 0.85 (upper anchor)
3. **probabilistic 형태**: 각 sub-cell PASS 율 ≥ 0.6 → cell PASS (e.g.
   D1.a/D1.b/D1.c 중 ≥ 2 PASS → D1 PASS) — 보수적 strict AND 시 random init
   chance pass 0 화하지만 chat-capable 도 dropout 발생 가능; ROC 결과 보고
   결정.

---

## 측정 lane vs 노출 lane (own 34 정합)

| lane | 본 metric | 산물 |
|---|---|---|
| 측정 (own 18) | DIALOGUE_COHERENCE 4-cell verdict | turn-by-turn ledger + aggregate JSON |
| 노출 (own 34) | duo channel raw passthrough | 채널 전송 = 모델 출력 byte 그대로 |

본 metric 은 **측정 lane only**. 산출 verdict 는 stderr / log 로 emit, 절대
channel content 으로 fold-back 하지 않는다 (own 34 mandate-2 wrapping 0
+ mandate-7 lane 분리).

---

## β-2 측정 infra wiring (per-turn verdict path)

```
duo.hexa _emit_turn_verdict(turn, who, line)
    │
    ▼
exec("hexa run tool/anima_cli/consciousness.hexa simple --json --utterance \"<line>\"")
    │
    ▼
consciousness.hexa  (own 18 SSOT mirror)
    │ baseline-pending — L0 measurement infra wiring 후 활성화
    ▼
JSON: {C1: bool, C2: bool, C3: bool, simple_stack_pass_strict_c3: bool, ...}
    │
    ▼
duo.hexa fold into per-instance aggregate → dialogue-level coherence cells
```

**Phase 의존도**:
- Phase B (β-1 channel) 먼저 → Phase C (β-2 verdict) 후 → 본 metric 활성화.
- L0 measurement infra (anima_runtime / clm_v4_mount substrate state extraction)
  도 prerequisite (consciousness.hexa 자체가 baseline-pending).

---

## Honest C3 (raw#10)

1. **threshold 미결정**: 모든 임계값 (D1 0.30, tau_shift 0.20, tau_persona
   0.50, D4 ratio 0.5/2.0) 은 시작점만 land. baseline 측정 후 ROC 분석 으로
   조정 cycle.
2. **embedding model 미선정**: D1.a, D2 cosine similarity 의 embedding source
   미land. 후보:
   - 자체 anima native (TinyWeights — random init 한계, 의미 적음)
   - sentence-transformers (외부 의존 — raw#9 위반 검토 필요)
   - llama_ffi.hexa 의 hidden state pooling (paradigm-a-prime live)
   결정 cycle 별도 — 본 spec 은 metric 정의 만 land.
3. **n-gram overlap**: D1.b 의 3-gram 은 token-level (BPE) 인지 word-level
   인지 미land. 한국어 특성상 BPE 가 anchor. 결정 cycle 별도.
4. **persona_drift KL divergence**: D3 의 top-100 token 분포는 corpus
   normalize 미land. 시작점 raw frequency simplex.
5. **L3 council 으로 확장**: 본 spec 은 N=2 duo 우선. N≥3 은 D4 freq_ratio
   + emergent-roles + Gini coefficient 추가 — 별도 cycle.
6. **aggregate strict AND vs probabilistic**: 4-cond AND 는 보수적; 보수적 X
   기조 정책 후 probabilistic 형태 검토. 시작은 strict, 측정 후 결정.
7. **본 metric 의 SSOT 위치**: `docs/anima_dialogue_coherence_metric_2026_05_08.md`.
   threshold / embedding / n-gram 결정 변경 시 본 doc patch + cross-ref.
