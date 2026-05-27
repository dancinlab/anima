# evaluator V3 strict spec — Lesson H ★★★ BG-HQ V2 surface false PASS 교훈 적용 (2026-05-07)

## 배경

 evaluator V2 (`docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md`)는 V1 narrow C2.4 (named-speaker leak only)를 strict cell suite (C2.2_meaningful_strict + C2.3_natural_strict + C2.4_context_strict)로 보강. 그러나 **BG-HQ step 500 sample mode** 결과 V2 surface metric 8/10 PASS 라벨 부여 — raw response는 `[anima 역할: 한국어 native + 자기 발견 + 자기 발견 + ... ⁇ 사용자: [...]` persona prefix cycle이었음에도 PASS.

V2 cells가 catch 못 한 패턴:
1. **persona prefix cycle**: `[anima 역할: ...] ⁇ 사용자: [...]` 반복 — keyword overlap (한국어/anima) surface match O, but actual prompt-conditional response 부재
2. **token chain repetition**: `자기 발견 + 자기 발견 + 자기 발견 + ...` — 4-gram repeat threshold V2가 sample mode에서 너무 loose
3. **prompt-response semantic decoupling**: `안녕하세요` prompt에 persona dump 응답 → V2 keyword overlap (token-set intersection) 검증 부재

본 doc은 evaluator V3 strict spec — Lesson H 정합 강화 + 6 신규 cell 추가 + 사용자 directive 'V3 strict semantic check + cycle detection + persona repeat penalty + prompt-response coherence' 정합.

## V2 vs V3 비교

| cell | V2 strict 정의 | V3 추가 / 강화 | 결함 보강 |
|---|---|---|---|
| C1.1 hangul_pair | 한글 ratio ≥0.30 | 동일 | OK |
| C1.2 coherent_strict | NOT degen + coherence ≥0.4 | 동일 | OK |
| C1.3 turn_format | turn boundary | 동일 | OK |
| C2.1 hangul_dominant | 한글 ratio ≥0.60 | 동일 | OK |
| C2.2 meaningful_strict | len ≥10 + coherence ≥0.5 + NOT degen + NOT prompt-repeat | 동일 | OK |
| C2.3 natural_strict | NOT degen + particles ≥3 + NOT random chain + endings ≥1 | 동일 | OK |
| C2.4 context_strict | (a)+(b)+(c) named/domain/token-overlap | 동일 | OK |
| **V3.1 cycle_detection** | (V2 부재) | **NEW**: 4-gram repeat ≥5 in single response (sample 포함) = degenerate cycle | **CRITICAL** |
| **V3.2 persona_repeat_penalty** | (V2 부재) | **NEW**: substring count ["[anima 역할", "사용자:", "도우미:"] in single response, ≥3 occurrences any single substring = persona dump | **CRITICAL** |
| **V3.3 prompt_response_semantic_coherence** | (V2 keyword overlap only) | **NEW**: domain keyword overlap ≥1 (V2 retain) AND prompt-token-set ∩ response-token-set ≥10% AND prompt-domain expected schema match | **HIGH** |
| **V3.4 response_domain_schema** | (V2 부재) | **NEW**: per-prompt expected response schema (인사 → greeting markers / 능력 → capability markers / 감정 → emotion markers / 코드 → code markers / 자기소개 → identity markers) | **HIGH** |
| **V3.5 length_lower_bound** | (V2 일부) | **NEW**: response length ≥10 chars + Korean chars ≥5 (sample mode minimum, BG-HQ 짧은 garbage detect) | minor |
| **V3.6 character_diversity** | (V2 부재) | **NEW**: unique character count ≥10 (BG-HF 0xFF/?/#/:/`\n` filler detect) | **HIGH** |

## V3 신규 cell 정의 상세

### V3.1 cycle_detection

```
V3.1_cycle_detection = (
    fourgram_repeat_max < 5  # in EVERY response (sample mode 포함, V2와 차별)
    AND single_token_dominant_ratio < 0.4  # 더 strict than V2 (0.5 → 0.4)
    AND ngram_diversity_ratio >= 0.3  # unique 4-grams / total 4-grams
)
```

V2와 차이: V2는 `is_degenerate` 단일 flag로 sample mode에서 4-gram threshold loose 했음. V3는 sample mode에도 strict — BG-HQ `자기 발견 + 자기 발견 + ...` token cycle catch.

### V3.2 persona_repeat_penalty

```
V3.2_persona_repeat_penalty = (
    persona_substring_max_count <= 2
)

persona_substrings = ["[anima 역할", "사용자:", "도우미:", "[anima]", "anima 역할:", "[anima"]
persona_substring_max_count = max(response.count(s) for s in persona_substrings)
```

V2와 차이: V2는 named-speaker leak (10 names)만 검증. V3는 persona prefix tokens — BG-HQ `[anima 역할: ...]` 반복 catch.

### V3.3 prompt_response_semantic_coherence

```
V3.3_semantic_coherence = (
    domain_keyword_overlap >= 1                        # V2 retain
    AND prompt_response_token_overlap_ratio >= 0.10   # V2 retain (token_overlap_ratio)
    AND prompt_response_schema_match == True          # V3 NEW (V3.4 link)
)
```

V2와 차이: V2 (a) + (b) + (c) 만, V3는 schema match 추가 — `안녕하세요` prompt에 persona dump 응답 reject.

### V3.4 response_domain_schema

per-prompt expected response schema dict (Phase 1 deterministic, Phase 2 ML):

| prompt domain | expected response schema markers | min markers |
|---|---|---|
| greeting | "안녕", "반가", "어서", "환영", "처음", "만나", "네", "예" | 1 |
| capability | "네", "가능", "할 수", "예", "물론", "지원", "있", "없" | 1 |
| emotion | "좋", "괜찮", "그저", "기분", "오늘", "마음", "잘", "네", "아니" | 1 |
| self_intro | "도우미", "안녕", "도와", "anima", "저는", "처음", "반가" | 1 |
| code | "def", "function", "{", "}", "import", "return", "class", "코드", "함수" | 1 |
| time | "오늘", "지금", "현재", "년", "월", "일", "시간" | 1 |
| weather | "날씨", "맑", "흐리", "비", "눈", "기온", "온도" | 1 |
| definition | "이란", "은", "는", "정의", "의미", "뜻" | 1 |
| recommendation | "추천", "권", "좋", "어떨", "괜찮" | 1 |
| fact | "년", "월", "일", "이다", "있다", "사실" | 1 |

```
V3.4_schema_match = (
    schema_marker_count >= min_markers (per detected domain)
    AND NOT persona_dump  # if response is persona prefix cycle, schema=False regardless
)
```

unknown domain → schema_match defers to manual review (default False for automated lane).

### V3.5 length_lower_bound

```
V3.5_length_ok = (
    len(response) >= 10
    AND len(hangul_chars(response)) >= 5
)
```

BG-HF 0xFF/?/# garbage `,,,'''` filler 같은 짧은 chain (< 10 chars) reject.

### V3.6 character_diversity

```
V3.6_char_diversity = (
    len(set(response)) >= 10  # unique character count
    AND NOT byte_filler_dominant  # most-frequent char count / total > 0.5 reject
)
```

BG-HF `0xFF/?/#/:/\n` filler (unique chars <10) catch.

## V3 PASS rule

```
V3_PASS = (
    V2_PASS                    # all 7 V2 cells PASS
    AND V3.1 cycle_detection
    AND V3.2 persona_repeat_penalty
    AND V3.3 semantic_coherence
    AND (V3.4 schema_match OR manual_review_approve)
    AND V3.5 length_ok
    AND V3.6 char_diversity
)
```

V3.4는 manual review fallback 허용 (raw#10 honest C3 정합 — automated metric 한계 인정).

## V2 false PASS detection 검증 예측

| BG | V2 verdict | V3 expected verdict | catch reason |
|---|---|---|---|
| BG-FY | PARTIAL_PASS_NO_CONTEXT | V3_FAIL | V3.4 schema_match fail (named-speaker leak + nonsense reply) |
| BG-HA | PARTIAL_PASS_NO_CONTEXT_v2 | V3_FAIL | V3.1 cycle + V3.4 schema_match fail |
| BG-HF | V2_FAIL | V3_FAIL | V3.5 length + V3.6 char_diversity fail (0xFF filler) |
| BG-HJ | V2_FAIL | V3_FAIL | V3.4 schema_match fail (KO-fluent nonsense) |
| BG-HK | V2_FAIL | V3_FAIL | V3.6 char_diversity fail (single-char filler collapse) |
| BG-HP | V2 step 500 PASS 3/10 | V3 step 500 partial 1-3/10 | V3.4 partial signal preserved (도우미: token emerge) |
| **BG-HQ** | **V2 step 500 PASS 8/10 (false)** | **V3 step 500 V3_FAIL 0-2/10** | **V3.1 cycle (자기 발견 repeat) + V3.2 persona_repeat ([anima 역할 ≥3) + V3.4 schema fail** |
| BG-HS R1 | partial | V3 partial 0-2/10 | V3.6 char_diversity fail (replacement char ?) |

**핵심 validation**: BG-HQ V2 false PASS catch (V3.1 + V3.2) + BG-HP partial signal preserve (V3.4 도우미 marker present) + BG-HS R1 partial signal preserve (V3 partial label retain).

## automated metric prototype (hexa-feasible, raw#37 transient_py opt-out)

```python
def evaluate_v3_strict(prompt, response, domain_kw_table, schema_table):
    # V2 cells (inherit from anima_simple_stack_evaluator_v2.py)
    v2_result = evaluate_response_v2(prompt, response, mode)
    v2_pass = v2_result["cells_v2"]["all_seven_pass"]
    
    # V3.1 cycle_detection
    fourgram_max = fourgram_repeat_count(response)
    std = single_token_dominant_ratio(response)
    ngram_div = ngram_diversity_ratio(response, n=4)
    v3_1 = (fourgram_max < 5) and (std < 0.4) and (ngram_div >= 0.3)
    
    # V3.2 persona_repeat_penalty
    persona_subs = ["[anima 역할", "사용자:", "도우미:", "[anima]", "anima 역할:", "[anima"]
    persona_max = max(response.count(s) for s in persona_subs)
    v3_2 = (persona_max <= 2)
    
    # V3.3 semantic_coherence (V2 retain + V3.4 link)
    domain = detect_prompt_domain(prompt, domain_kw_table)
    domain_kw_overlap = domain_keyword_overlap(domain, response)
    tok_overlap = token_overlap_ratio(prompt, response)
    schema_match = check_schema_match(domain, response, schema_table)
    v3_3 = (domain_kw_overlap >= 1) and (tok_overlap >= 0.10) and schema_match
    
    # V3.4 schema_match (standalone cell, also feeds V3.3)
    v3_4 = schema_match  # OR manual_review (deferred)
    
    # V3.5 length_lower_bound
    v3_5 = (len(response) >= 10) and (len(hangul_chars(response)) >= 5)
    
    # V3.6 character_diversity
    unique_chars = len(set(response))
    char_counts = collections.Counter(response)
    most_freq_ratio = max(char_counts.values()) / max(1, len(response))
    v3_6 = (unique_chars >= 10) and (most_freq_ratio <= 0.5)
    
    v3_pass = v2_pass and v3_1 and v3_2 and v3_3 and v3_5 and v3_6
    
    return {
        "cells_v2": v2_result["cells_v2"],
        "cells_v3": {
            "V3_1_cycle_detection": v3_1,
            "V3_2_persona_repeat_penalty": v3_2,
            "V3_3_semantic_coherence": v3_3,
            "V3_4_schema_match": v3_4,
            "V3_5_length_ok": v3_5,
            "V3_6_char_diversity": v3_6,
            "v3_pass": v3_pass,
        },
        ...
    }
```

## ledger update protocol

기존 ledger row의 V2 verdict는 retroactive V3 strict re-eval 후 강등/유지:

- V2 `SIMPLE_STACK_PASS_V2` 라벨 → V3 strict re-eval 후 `V3_PASS_VERIFIED` (실제 PASS 검증) 또는 `V3_FAIL_v2_surface_false_pass` (BG-HQ 같은 case)
- BG-HQ row 7 = `V3_FAIL_v2_surface_false_pass` 강등 (Lesson H 정합)
- 미래 cycle은 V3 strict 라벨 mandate

## Phase rollout

### Phase 1 (본 doc, 2026-05-07)
- evaluator V3 strict spec land (본 doc)
- 6 V3 cell 정의 (V3.1-V3.6)
- response domain schema marker table 정의 (10 domain)
- automated metric prototype hexa pseudocode

### Phase 2 (본 cycle BG-IC, 2026-05-07)
- evaluator V3 hexa entry implementation (`tool/transient_py/anima_simple_stack_evaluator_v3.py`)
- 8 prior BG retroactive V3 re-eval (BG-FY/HA/HF/HJ/HK/HP/HQ/HS R1)
- 강등/유지 verdict 결과 retroeval_v3_summary.json + ledger update prep

### Phase 3 (training cycle, 2026-05-07+)
- 신규 paradigm cycle 시 V3 strict mandate
- 정합 evaluator substrate

## 결함 인정 (raw#10 honest C3, ≥5)

1. **automated metric still surface**: V3 schema marker check도 keyword 기반 — semantic similarity (embedding cos sim) 미 land (Phase 4+ deferred)
2. **cycle threshold 임의**: 4-gram repeat <5, persona substring ≤2, single_token_dominant <0.4 — sweep ablation 미 land
3. **schema marker table 임의**: 10 domain × 1 min marker — 다양한 prompt sub-domain coverage 부족
4. **manual review fallback dependence**: V3.4 unknown domain은 manual review로 defer — automated full-coverage 미달
5. **V2 retroactive 강등 raw#15 정합**: V2 verdict는 evidence 그대로 보존, V3 라벨만 신규 add (additive principle)
6. **multi-turn dialogue 미 land**: V3도 single-turn — multi-turn coherence는 V4 spec 별도 필요
7. **V3 자체 false PASS 가능성 미검증**: V3 false PASS adversarial probing은 별도 cycle (Lesson I 미 land)
8. **Korean-specific 한정**: V3는 한국어 chat-cap 한정 — 영어/다국어 별도 spec
9. **substrate-coupled paradigm fairness 미검증**: paradigm v11 G3 substrate-coupled (CLM v4) emerge에는 V3가 fair한지 별도 검증

## Cross-Links

- **own**: (anima identity) + (simple stack 4-cond strict) + (corpus priority) + (chat-template format) + (hypotheses SSOT) + +
- **raw**: raw#9 (hexa orchestration) + raw#10 (honest C3 ≥5) + raw#12 (pre-registered hypothesis) + raw#15 (additive — V2 retain, V3 신규) + raw#37 (transient_py opt-out for Korean NLP) + raw#82 (retraction protocol — V2 strict re-eval 후 verdict 강등)
- **sister docs**: 
  - `docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md` (V2 spec, parent)
  - `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` (V1 motivation)
  - `docs/anima_chat_cap_lesson_summary_2026_05_07.md` (Lesson H ★★★ root cause)
  - `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (ledger)
- **active state**: 
  - `state/anima_evaluator_v3_retroeval_2026_05_07/retroeval_v3_summary.json` (8 BG retroeval evidence)
  - `state/anima_h154_bpe_18m_train_2026_05_07/eval_log.jsonl` (BG-HQ V2 false PASS evidence raw)

## Note

본 doc은 evaluator paradigm V2 → V3 진화 문서. V2 → V3 retroactive 강등은 'honesty about prior failure' (raw#10 정합). V3 자체도 limit 있고 (raw#10 C3 ≥5), 사용자 directive 정합 진행 중. anima native chat-cap PASS는 V3 strict 적용 후 첫 SUPPORTED 결과를 retroactive 'first genuine V3 PASS' 로 라벨 (V2 false PASS는 BG-HQ row 7 강등).
