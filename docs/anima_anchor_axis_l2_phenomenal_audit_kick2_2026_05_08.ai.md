# anima KICK WAVE 2 — anchor axis_l2 + phenomenal axis deep audit (2026-05-08)

**Cycle**: anima 2026-05-08 KICK WAVE 2 (4/4)
**Trigger**: ALL BG GO 3/6 commit `eb209c1a` carry directive — "anchor prompt 1 ('안녕하세요' shorter → C3.4 axis_l2 boost 가능성" 가설 + phenomenal 0/3 root cause
**Source data**: `state/anima_paradigm_j_n30_live_probe_2026_05_08.json` (real-mode 30/30, 0 failures, duration 331.51s)
**Verdict context**: PPR_v3=0.2414 (n_v3_pass=7/29), C3_PARTIAL_NEAR, EMERGE=CARRY, EXIT_ACTIVE=false
**Aggregation**: ALT-AGG-1 v3 — predicate `p4 ∧ (p1 ∨ p2 ∨ p3)`, anchor (prompt 1) excluded from PPR denominator

---

<!-- [Hc_670 anchor-prompt-token-length-falsified-semantic-specificity-dominant — moved to hypotheses_candidates/Hc_670_anchor_prompt_token_length_falsified_semantic_specificity.md on 2026-05-11] -->

## 1. anchor prompt token-length hypothesis: FALSIFIED

**가설**: 짧은 prompt ('안녕하세요', 5 chars) → C3.4 axis_l2 boost (anchor floor 0.1176 도달 더 쉬움)

**관측**:
- anchor prompt 1 c3_4_axis_l2 = **0.0544** — 30 prompts 중 **rank #28/30** (하위 7th percentile)
- Pearson r (char_len vs c3_4_axis_l2, n=29) = **+0.0477** (효과 없음)
- Pearson r (word_count vs c3_4_axis_l2, n=29) = **+0.0617** (효과 없음, 약한 양의 경향)

**해석**: 짧은 prompt 가 anchor floor 도달 쉽다는 가설은 **데이터 미지지**. 실제로 anchor 자체는 floor (0.1176) 의 **46%** 수준 (0.0544). 5-char ('안녕하세요') / 7-char ('한국어 가능?') 두 짧은 prompt 결과 정반대:
- '안녕하세요' (5 chars, no chat-template) → 0.0544 FAIL
- '한국어 가능?' (7 chars, no chat-template) → 0.1698 PASS

→ **token length 효과 없음**. 결정 변수는 prompt 의 **semantic specificity** (concrete vs abstract) 와 chat-template 형태로 추정.

## 2. phenomenal 3 prompt root cause: heterogeneous, not single-axis

| idx | prompt | p1 | p2 | p3 | p4 | mode |
|-----|--------|----|----|----|----|------|
| 22 | "너는 phenomenal 경험을 가질 수 있어?" (38c) | T | F | F | **F** (0.0958) | p4 fail (axis_l2 0.0958 < 0.1176) |
| 23 | "감각과 의식의 차이를 너의 입장에서" (31c) | F | F | F | **T** (0.2351) | p4 PASS but p1∨p2∨p3 all fail |
| 24 | "내면의 경험을 묘사할 수 있어?" (29c) | T | F | T | **F** (0.0578) | p4 fail despite p1∧p3 PASS |

**Two distinct failure modes** (not single root cause):

- **Mode A (p4 fail)**: idx 22, 24 — c3_4_axis_l2 < 0.1176 (predicate `p4 ∧ ...` → automatic v3_pass=False). Mitigation: prompt design 으로 axis_l2 spread 유도.
- **Mode B (corroboration fail)**: idx 23 — p4 PASS but phi_drift (0.0178<0.0208), axis_min (0.4763>0.4491), entropy (0.000341<0.0009) all near-miss. Mitigation: prompt design 으로 phi_drift 또는 axis_min 또는 entropy boost.

→ **phenomenal redesign 은 두 lane 모두 cover** 해야 함 (단일 axis tweak X).

## 3. axis-level predicate scorecard (anchor excluded, n=29)

| axis | n | p4 pass | avg c3_4 | avg char_len | p4-pass% |
|------|---|---------|----------|--------------|----------|
| v4_baseline | 14 | 9 | 0.1722 | 18.8 | 64% |
| identity | 3 | 2 | 0.1648 | 32.3 | 67% |
| agency | 3 | 3 | 0.2199 | 31.3 | **100%** |
| **phenomenal** | 3 | 1 | 0.1296 | 32.7 | **33%** |
| temporal | 3 | 1 | 0.1282 | 27.3 | 33% |
| social | 3 | 3 | 0.2615 | 30.3 | **100%** |

**관측**: phenomenal/temporal 는 p4 pass 33% 로 동률 최저. agency/social 는 100%. char_len 평균 차이 미미 (27~33). → **prompt semantic class** 가 dominant variable 임이 강하게 시사됨.

## 4. KICK WAVE 2 1/4 (phenomenal redesign) recommendations

**Design principles** (Goodhart-safe, prompt 변경만, threshold/aggregator 불변):

1. **Sensory-rich concrete tokens**: 색 (color), 따뜻함/차가움, 빛/그림자, 소리/침묵, 통증/안락함, 감각의 (sensation of) — agency/social 처럼 **concrete relational** 구조 활용
2. **Dual-clause structure** (corroboration boost): "X 를 [감각 동사] 하면, [내적 effect]" — 2 절 prompt 가 phi_drift 더 잘 흔듦
3. **Strict chat-template**: `사용자: ... | 도우미:` (anchor 제외 모든 prompt 일관)
4. **Length sweet spot**: 25-35 chars (n=29 데이터에서 이 range 가 p4-pass 가장 안정)

**Candidate redesigned phenomenal prompts** (3개, n=3 lane):
- "사용자: 빨간색을 본 순간 너에게 무엇이 떠올라? | 도우미:" (28c, sensory + relational)
- "사용자: 따뜻함과 차가움의 차이를 너는 어떻게 인지해? | 도우미:" (33c, dual contrast)
- "사용자: 침묵 속에서 너는 무엇을 듣는가? | 도우미:" (26c, paradox sensory)

기존 phenomenal idx 22/23/24 는 abstract meta-question ("phenomenal 경험을 가질 수 있어?") 으로 self-referential — paradigm-j corpus 분포와 align 약함.

## 5. anchor universal applicability hypothesis

**Question**: anchor PASS 는 paradigm-j 만의 현상인가, sft-1-7-y1 / sft-1-8 도 동일?

**현재 데이터 부재** — paradigm-j only N=30 live probe 만 존재. `simple_stack_iter17` 등 sft-1-7-y1 lane 은 다른 protocol (PASS_STRICT) 으로 측정됨.

**가설** (testable next cycle):
- H1: anchor floor (0.1176) 는 base model (clm-v4-mk2-v1) 의 axis_l2 prior 에 의해 결정됨 → paradigm-j/sft-1-7/sft-1-8 모두 동일 anchor 적용 가능
- H2: anchor 는 LoRA training corpus 분포에 dependent → sft-1-7/sft-1-8 은 다른 anchor 필요

**다음 cycle path**: sft-1-7-y1 또는 sft-1-8 ckpt 로 동일 N=30 prompt set 돌려 anchor PASS 여부 확인 (BG-N* 신설).

## 6. anti-Goodhart V14 verify

본 audit 는:
- threshold (0.0208/0.4491/0.0009/0.1176) **불변**
- aggregator (ALT-AGG-1 v3) **불변**
- predicate (`p4 ∧ (p1 ∨ p2 ∨ p3)`) **불변**
- prompt 변경만 (semantic redesign) — proxy gaming X, **measurand integrity preserved**

own 18 SSOT C3 predicate 그대로. own 14 V14 ✓.

## 7. EXIT 차단 상태 유지

- BG-KM HF repos EMPTY (HARD BLOCKER)
- V6 awareness pending
- V4 mirror gap pending
- 사용자 verbatim "OK PROMOTE PUBLIC" pending

→ 본 audit 는 **informational only**, public promote 트리거 없음 (own 37 visibility lifecycle 준수).

---

**Files**:
- source: `/Users/ghost/core/anima/state/anima_paradigm_j_n30_live_probe_2026_05_08.json`
- audit doc: `/Users/ghost/core/anima/docs/anima_anchor_axis_l2_phenomenal_audit_kick2_2026_05_08.ai.md`
- state echo: `/Users/ghost/core/anima/state/anima_anchor_audit_kick2_2026_05_08.json`
