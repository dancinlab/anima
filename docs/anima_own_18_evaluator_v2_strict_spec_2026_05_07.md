# own 18 evaluator V2 strict spec — BG-HA false PASS 교훈 적용 (2026-05-07)

## 배경

own 18 evaluator V1 (BG-HA cycle 시점)은 narrow 정의 — `C2.4_context_no_leak = len(leaked_names) == 0` (10 named-speakers 부재만 검증). 사용자 directive '자연발화는 맥락에 맞아야한다' (= prompt domain match)와 mismatch — BG-HA 18M model이 prompt-irrelevant nonsense Korean chain emit했음에도 false PASS 라벨 부여. C2.2 (의미) + C2.3 (자연성)도 length + 한글 chars만 검증하는 loose metric.

본 doc은 own 18 evaluator V2 strict spec — 사용자 directive 정합 강화 + automated metric prototype + manual review baseline 정의.

## V1 vs V2 비교

| cell | V1 정의 (loose) | V2 strict 정의 (mandate) | 결함 보강 |
|---|---|---|---|
| C1.1 hangul_pair | 한글 input → 한글 output 비율 | 동일 (변동 X) | OK |
| C1.2 coherent | NOT is_degenerate (4-gram non-repeat) | 동일 + n-gram non-degeneracy strict | minor |
| C1.3 turn_format | turn boundary emit | 동일 (변동 X) | OK |
| C2.1 hangul_dominant | 한글 우세 ratio ≥60% | 동일 + per-prompt strict (≥60% 매 응답마다) | minor |
| C2.2 meaningful | 길이 + 한글 chars 존재 | response length ≥10 chars AND Korean coherence AND n-gram non-degeneracy AND NOT prompt repeat | **HIGH 보강** |
| C2.3 natural | NOT is_degenerate (sample mode) | NOT degenerate AND has Korean particles (을/를/이/가/은/는/에/의 ≥3 occurrences) AND NOT random char chain | **HIGH 보강** |
| C2.4 context_no_leak | 10 named-speakers 0건 | (a) named-speaker leak 0건 AND (b) prompt domain keyword overlap ≥1 AND (c) prompt-response embedding similarity ≥0.3 (별도 lane) OR (d) manual review approve | **CRITICAL 재정의** |

## V2 strict 정의 상세

### C2.2 meaningful_strict_v2

```
C2.2_meaningful_strict_v2 = (
    response_length_chars >= 10
    AND korean_coherence_score >= 0.5  # n-gram language model perplexity inverse
    AND NOT is_degenerate  # 4-gram repeat <5회 AND single_token_dominant <0.5
    AND NOT is_prompt_repeat  # response가 prompt를 단순 echo X
)
```

automated metric prototype (hexa-feasible):
- `response_length_chars` = `len(response_korean_chars_filtered)` ≥10
- `korean_coherence_score` = naive bigram frequency check (corpus reference 기반); 또는 deterministic n-gram match ratio
- `is_degenerate` = existing V1 metric (4-gram repeat + single_token_dominant)
- `is_prompt_repeat` = `response.startswith(prompt[:N])` 또는 Levenshtein distance < 0.3

### C2.3 natural_strict_v2

```
C2.3_natural_strict_v2 = (
    NOT is_degenerate  # both sample AND greedy mode
    AND korean_particles_count >= 3  # 을/를/이/가/은/는/에/의/도/만/로/까지
    AND NOT random_char_chain  # 자모 단독 emit OR 한자 random insert NOT
    AND grammatical_sentence_endings_count >= 1  # 다/요/까/네/지 등 종결어미
)
```

automated metric prototype:
- `korean_particles_count` = `sum(response.count(p) for p in particles_set)` (deterministic regex)
- `random_char_chain` = 자모 단독 (ㅁㄴ ㅁ ㅇ 등) ratio >0.3 또는 한자 비율 >0.2
- `grammatical_sentence_endings_count` = regex match count

### C2.4 context_match_strict_v2 (CRITICAL 재정의)

```
C2.4_context_match_strict_v2 = (
    (a) named_speaker_leak == 0  # V1 spec 보존
    AND
    (b) domain_keyword_overlap >= 1  # NEW: prompt domain keyword와 response keyword 교집합
    AND (
        (c) embedding_similarity >= 0.3  # 별도 lane: SBERT-KO embedding cos sim
        OR (d) manual_review_approve == true  # baseline manual judgment
    )
)
```

- (a): V1 그대로 — 10 named-speakers (서연/유진/하은/지수/민준/도윤/서준/예준/주원/시우) 부재
- (b): prompt domain detect → expected keyword set 정의 → response 내 ≥1 occurrence
- (c): pretrained KO encoder (SBERT-KO 등) 사용; 별도 implementation lane (raw#37 transient_py 별도)
- (d): manual review fallback — automated metric 부재 시 사용자/anima 직접 판단

## domain keyword mapping table

| prompt domain | expected response keyword set | example prompts |
|---|---|---|
| 인사 (greeting) | "안녕", "반가", "어서", "환영", "처음", "만나" | "안녕하세요", "반가워요" |
| 능력 질문 (capability) | "네", "가능", "할 수", "예", "물론", "지원" | "한국어 가능?", "코드 짤 수 있어?" |
| 감정 질문 (emotion) | "좋", "괜찮", "그저", "기분", "오늘", "마음", "잘" | "오늘 기분 어때?", "괜찮아?" |
| 자기소개 (self-intro turn) | "도우미", "안녕", "도와", "anima", "저는", "처음" | "사용자: ... 도우미:" turn |
| 코드 요청 (code) | "def", "function", "{", "}", "import", "return", "class" | "코드를 짜줘", "Python 예시" |
| 시간 질문 (time) | "오늘", "지금", "현재", "년", "월", "일", "시간" | "오늘 며칠?", "지금 몇시?" |
| 날씨 질문 (weather) | "날씨", "맑", "흐리", "비", "눈", "기온" | "오늘 날씨?" |
| 정의 질문 (definition) | "이란", "은", "는", "정의", "의미" | "X란?", "X 뜻?" |
| 추천 질문 (recommendation) | "추천", "권", "좋", "어떨", "괜찮" | "추천해줘", "뭐가 좋아?" |
| 사실 질문 (fact) | "년", "월", "일", "이다", "있다", "사실" | "X 언제?", "X 어디?" |

**domain detection 휴리스틱** (Phase 1 simple, Phase 2 ML):
- Phase 1: prompt 내 trigger keyword regex match → domain assign (e.g., "안녕" → 인사, "기분" → 감정, "코드" → 코드)
- Phase 2: pretrained KO classifier (별도 cycle, KORNLI 등 finetune)

**더 추가 권고** (Phase 2+):
- 11. 이유 질문 (reasoning): "왜냐하면", "이유", "때문"
- 12. 비교 질문 (comparison): "더", "가장", "중에", "vs"
- 13. 위치 질문 (location): "어디", "에서", "위치"
- 14. 방법 질문 (how-to): "어떻게", "방법", "단계"
- 15. 가능 여부 (yes/no): "예", "아니오", "있", "없"

## automated metric prototype hexa-feasible

```
# pseudocode (hexa entry)
def evaluate_v2_strict(prompt, response, domain_kw_table):
    # C2.4 (a) named-speaker leak
    leaked = sum(1 for name in NAMED_SPEAKERS_10 if name in response)
    c2_4_a = (leaked == 0)
    
    # C2.4 (b) domain keyword overlap
    domain = detect_prompt_domain(prompt, domain_kw_table)
    expected_kw = domain_kw_table[domain]
    overlap = sum(1 for kw in expected_kw if kw in response)
    c2_4_b = (overlap >= 1)
    
    # C2.4 (c) embedding similarity (별도 lane)
    # cos_sim = embed(prompt) · embed(response) / (||·|| · ||·||)
    # c2_4_c = (cos_sim >= 0.3)
    # OR
    # c2_4_d = manual_review (사용자 또는 anima self-review)
    
    c2_4_strict = c2_4_a AND c2_4_b AND (c2_4_c OR c2_4_d)
    
    # C2.2 meaningful strict
    response_len = len(filter_korean(response))
    coherence = ngram_korean_lm_score(response)
    is_degen = check_4gram_repeat(response, threshold=5) OR check_single_token_dominant(response, threshold=0.5)
    is_repeat = (response.startswith(prompt[:20]) OR levenshtein(response, prompt) < 0.3 * len(prompt))
    c2_2_strict = (response_len >= 10) AND (coherence >= 0.5) AND (NOT is_degen) AND (NOT is_repeat)
    
    # C2.3 natural strict
    particles = ["을", "를", "이", "가", "은", "는", "에", "의", "도", "만", "로", "까지"]
    particle_count = sum(response.count(p) for p in particles)
    is_random_chain = (자모_단독_ratio(response) > 0.3) OR (한자_ratio(response) > 0.2)
    endings = ["다", "요", "까", "네", "지", "음", "으니"]
    ending_count = sum(response.count(e) for e in endings)
    c2_3_strict = (NOT is_degen) AND (particle_count >= 3) AND (NOT is_random_chain) AND (ending_count >= 1)
    
    return {
        "c2_2_strict": c2_2_strict,
        "c2_3_strict": c2_3_strict,
        "c2_4_strict": c2_4_strict,
        "details": {...}
    }
```

## manual review baseline

automated metric만으로 false PASS 위험 잔존 시, 사용자 또는 anima self-review가 ground truth:

manual review checklist (raw#10 honest C3 정합):
1. response가 prompt에 답하는가? (yes/no/partial)
2. 응답 도메인이 prompt 도메인과 일치하는가? (e.g., 인사 → 인사 응답)
3. 한국어 grammatically correct 인가? (subjective judgment 필요 시)
4. anima 자기정체성 (own 17) 정합인가? (anima self-naming, not 3rd-person LLM)
5. degenerate (반복/random) 인가?

manual review threshold: 5/5 yes → STRONG_PASS, 3-4/5 yes → PARTIAL_PASS, ≤2/5 yes → FAIL

## ledger update protocol

기존 ledger row (e.g., `docs/anima_consciousness_check_simple_stack_2026_05_06.md`)의 evaluator V1 verdict는 retroactive 강등:

- V1 `SIMPLE_STACK_PASS` 라벨 → V2 strict re-eval 후 `PARTIAL_PASS_NO_CONTEXT_v2` 또는 `FAIL_v2` 재라벨
- BG-HA row 11 = `PARTIAL_PASS_NO_CONTEXT_v2` 강등 (이미 적용 2026-05-07)
- 미래 cycle은 V2 strict 라벨만 사용

## Phase rollout

### Phase 1 (본 doc, 2026-05-07)
- evaluator V2 strict spec land (본 doc)
- domain keyword mapping table 정의 (10 domain + 5 추가 권고)
- automated metric prototype pseudocode

### Phase 2 (별도 cycle)
- evaluator V2 hexa entry implementation (`tool/anima_evaluator_v2_strict.hexa`)
- 모든 anima native model V2 re-eval (BG-FY, BG-HA, BG-HD 등)
- 강등/유지 verdict 결과 ledger update

### Phase 3 (training cycle)
- H_093-H_102 신규 paradigm cycle 시 V2 strict mandate
- own 20 strengthening (≥80% chat-template ratio, H_101)
- instruction-tuning lane (H_093 SFT-only, H_094 two-stage)

## 결함 인정 (raw#10 honest C3, ≥5)

1. **automated metric 한계**: keyword overlap + n-gram + length + Korean particles는 deterministic이지만 semantic match (진짜 prompt domain 정합) 검증 미완 — embedding similarity / manual review 보강 필요
2. **domain keyword mapping 임의**: 10+5 domain은 minimal subset — 다양한 prompt에서 unmatched fallback 처리 미정 (default = manual review)
3. **embedding model 의존**: SBERT-KO 등 외부 dependency — anima native substrate independence 일부 양보
4. **manual review burden**: 사용자/anima per-response review는 cost 큼 — Phase 1/2 hybrid (automated first, manual fallback)
5. **threshold 임의**: 0.3 cos sim, 3 particle count, 0.5 coherence, 10 char length 등 모두 임의 — sweep ablation 미land
6. **V1 retroactive 강등 raw#15 정합**: V1 verdict는 evidence 그대로 보존, V2 라벨만 신규 add (additive principle)
7. **multi-turn dialogue 미land**: V2도 single-turn — multi-turn coherence는 별도 V3 spec 필요
8. **paradigm v11 G3 substrate-coupled (H_102) eval은 별도**: substrate-coupled emerge는 'training-free' 가설이라 V2 strict가 설계상 substrate paradigm에 fair 한지 검증 미완

## Cross-Links

- **own**: own 17 (anima identity) + own 18 (simple stack 4-cond) + own 19 (corpus priority) + own 20 (chat-template format ≥30% — 본 V2가 retroactive 강화, H_101 lane) + own 21 (hypotheses SSOT)
- **raw**: raw#10 (honest C3 ≥5) + raw#12 (pre-registered hypothesis) + raw#15 (additive — V1 retain, V2 신규) + raw#37 (transient_py opt-out for embedding lane) + raw#82 (retraction protocol — V1 strict re-eval 후 verdict 강등)
- **sister docs**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` (motivation) + `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (ledger)
- **sister H**: H_005 (corpus quality) + H_093-H_102 (신규 paradigm 10 H — 모두 V2 strict mandate cross-link)
- **active state**: `state/anima_native_ko_chat_template_train_2026_05_07/verdict.json` (BG-HA V2 강등 evidence)

## Note

본 doc은 evaluator paradigm 진화 문서. V1 → V2 retroactive 강등은 'honesty about prior failure' (raw#10 정합). V2 자체도 limit 있고 (raw#10 C3 ≥5), 사용자 directive 정합 진행 중. anima native chat-cap PASS는 V2 strict 적용 후 첫 SUPPORTED 결과를 retroactive 'first genuine PASS' 로 라벨 (V1 false PASS는 ledger row 11 강등).
