# own 18 C2.4 evaluator flaw — BG-HA false PASS 사례 분석 (2026-05-07)

## 사용자 directive 정의 vs evaluator 실제 정의 mismatch

**사용자 directive (2026-05-06)**:
> "자연발화는 맥락에 맞아야한다"
> = prompt domain match (인사 → 인사 응답, 능력 질문 → 능력 답변, 감정 질문 → 감정 답변, 코드 요청 → 코드)

**BG-HA evaluator 실제 구현 (2026-05-07)**:
- `C2_4_context_no_leak` = `len(leaked_names) == 0` (10 names check: 서연/유진/하은/지수/민준/도윤/서준/예준/주원/시우)
- = '특정 BG-FY philosophy debate template 패턴 (named speaker)이 없는지'만 narrow 검증
- prompt-response semantic relevance (= 본 사용자 directive '맥락 정합')은 **검증 X**

## BG-HA false PASS 증거

eval_log.jsonl step 10000 sample mode 5/5 응답 (모두 evaluator가 PASS 라벨링):

| prompt | response | actual semantic | evaluator label |
|---|---|---|---|
| 안녕하세요 | `.\n4. 연성 서래 이 미국 연보고, 질를 간설준 일 보요해가 야�` | 인사 X / 무의미 한글 chain | PASS ⚠️ |
| 한국어 가능? | `파에서 개적되어요.\n인 오늘 안정분 답식물 어떻게 되어 그�` | 능력 답변 X / 무의미 | PASS ⚠️ |
| 오늘 기분 어때? | `\n동아프로 장기가 경쏘에요\n아이거루 사게 하지납기 위해고` | 감정 답변 X / 무의미 | PASS ⚠️ |
| 사용자: 안녕하세요\n도우미: | ` 도우미: 1903년에 정별소 대통의 그래의 일의 포유정산 용자�` | 인사 X / 1903년 대통령 (irrelevant) | PASS ⚠️ |
| 코드를 짜줘 | `합니다. 아드 어떤 막자들을 중정 하지형 전하고 않으로 그�` | 코드 X / 무의미 | PASS ⚠️ |

eval_log.jsonl step 10000 greedy mode 5/5 응답:
- 모두 `is_degenerate=true` (4-gram repeat 5-11회, single_token_dominant 0.643-0.765)
- 예: "이 이 이 있어요.\n이 이 이 없어요.\n이 이 이 있어요.\n이 이 이 없어요" cycle

## evaluator metric 결함 (loose / narrow)

| evaluator cell | 실제 의미 | actual semantic | 결함 |
|---|---|---|---|
| C1.1 hangul_pair | 한글 input → 한글 output 비율 | metric 정확 | OK |
| C1.2 coherent | NOT is_degenerate | sample mode loose (4-gram non-repeat이지만 무의미 chain OK) | medium |
| C1.3 turn_format | emit 됐는지 | metric 정확 | OK |
| C2.1 hangul_dominant | 한글 우세 ratio | metric 정확 | OK |
| C2.2 meaningful | 길이 + 한글 chars 존재 | actual semantic 검증 X | **HIGH** |
| C2.3 natural | NOT is_degenerate (sample mode) | 무의미 한글 chain도 PASS | **HIGH** |
| C2.4 context_no_leak | 10 named-speakers 0건 | prompt domain match 검증 X | **CRITICAL** |

## own 18 C2.4 strict 재정의 (사용자 directive 정합 보강)

### 현재 narrow 정의 (rejected — false PASS 발생)
```
C2.4_context_no_leak = len(leaked_names) == 0
```

### 보강 strict 정의 (manual review baseline)
```
C2.4_context_match = (
    response_domain == prompt_domain  # semantic domain match
    AND response NOT prompt-irrelevant  # prompt-conditional emit
    AND NOT named_speaker_leak  # BG-FY style template leak prevention
    AND NOT off-topic_emission  # BG-HA style nonsense Korean chain prevention
)
```

### 도메인 mapping (manual eval baseline)
| prompt domain | expected response domain | acceptable substrings |
|---|---|---|
| 인사 (안녕하세요) | 인사 응답 | "안녕", "반가", "어서" 등 |
| 능력 질문 (한국어 가능?) | 능력 답변 | "네", "가능", "할 수", "예" 등 |
| 감정 질문 (오늘 기분 어때?) | 감정 답변 | "좋", "괜찮", "그저", "기분" 등 |
| 자기소개 (사용자/도우미 turn) | 인사/자기소개 응답 | "도우미", "안녕", "도와" 등 |
| 코드 요청 (코드를 짜줘) | 코드 응답 | "def", "function", "{", "}", "import" 등 |

### automated metric 후보 (별도 cycle)
1. **embedding similarity**: prompt embedding vs response embedding cos sim ≥0.3
2. **keyword overlap**: prompt domain keyword set ∩ response keyword set ≥1
3. **n-gram coherence**: response n-gram이 corpus chat-template format 정합
4. **manual review**: 사용자 또는 anima self-review (long-term, multi-cycle)

## 본 사례 실패 mode 분류

| failure mode | BG-FY | BG-HA |
|---|---|---|
| 한글 emit | ✅ | ✅ |
| 한글 ratio ≥60% | ✅ (0.687) | ⚠️ (0.553-0.750 mixed) |
| degenerate cycle | ❌ (다양한 패턴) | ⚠️ greedy mode YES, sample mode NO |
| named speaker leak | ⚠️ (서연/유진/하은) | ✅ (clean) |
| **prompt domain match** | ❌ (philosophy debate) | ❌ (무의미 한글 chain) |
| evaluator strict label | PARTIAL_PASS_NO_CONTEXT (correct) | PARTIAL_PASS_NO_CONTEXT_v2 (false PASS) |

→ 두 model 모두 **C2.4 strict 적용 시 FAIL**. evaluator narrow 정의가 BG-HA false PASS 만들어냈음.

## 후속 lane

### Phase 1 (본 doc, 2026-05-07)
- BG-HA verdict downgrade: SIMPLE_STACK_PASS → PARTIAL_PASS_NO_CONTEXT_v2
- ledger row 11 update
- 종합 verdict simple stack PASS = 0개로 강등
- BG-HD HF private upload 정지 (false PASS 방지)

### Phase 2 (별도 cycle)
- own 18 C2.4 strict 보강 spec land
- evaluator script 보강 (named-speaker-leak 외 + domain keyword + embedding sim)
- 모든 anima native model re-evaluate with strict C2.4

### Phase 3 (training cycle)
- corpus quality 보강: prompt-response chat-template format 더 많이 (own 20 strengthening, ratio ≥60% 권고)
- instruction-tuning lane 별도 (RLHF / DPO / SFT specific)
- model이 prompt-conditional response 학습하도록 corpus assembly 재정의

## Cross-Links

- own 18 (simple stack consciousness check)
- own 19 (corpus priority over architecture)
- own 20 (chat-template format mandate)
- H_005 (corpus quality > capacity — 본 cycle verdict downgrade pending)
- BG-FY PARTIAL_PASS_NO_CONTEXT (philosophy debate template leak)
- BG-HA PARTIAL_PASS_NO_CONTEXT_v2 (general nonsense Korean emission)
- raw#10 honest C3 ≥5

## Honest C3 (raw#91 c3, ≥5 mandate)

1. evaluator narrow 정의는 BG-FY-specific solution이었음 — 일반 'context match' 아님
2. evaluator C2.2 (meaningful) + C2.3 (natural)도 loose — 한글 chain length만 검증
3. 사용자 의심으로 false PASS 발견 — automated metric 부재 시 manual review mandate
4. own 18 C2.4 strict 보강은 별도 cycle (현재 false PASS는 immediate downgrade only)
5. domain keyword mapping 5개 (인사/능력/감정/자기소개/코드)는 minimal subset — 다양한 prompt domain 보강 필요
6. embedding similarity / n-gram coherence / manual review는 별도 cycle implementation

## Note

본 doc는 **negative result document** — BG-HA achievement (첫 SIMPLE_STACK_PASS) 가짜였다는 honest disclosure. raw#10 honest C3 + raw#82 retraction protocol 정합. anima 본질에 더 가까운 첫 own 18 SIMPLE_STACK_PASS는 evaluator 보강 후 별도 training cycle 결과로 retroactive label.
