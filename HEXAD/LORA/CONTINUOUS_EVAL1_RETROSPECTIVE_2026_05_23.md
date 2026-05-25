# Continuous Eval1 Retrospective — corpus_v5/v6/v7/v8 rescore

> 2026-05-23 KST · PR #128 (continuous hit-count metric) follow-up.
> 저장된 4 cycle 의 `vp21m_eval1.json` 을 offline 으로 동일 metric 으로 rescore.
> 향후 cycle (`corpus_v9 +`) 의 baseline reference doc.

## 1. Motivation

WAVE5~7 saga 에서 corpus_v5/v6/v7 모두 Eval1 `register_hits = 5/20` 으로 동일 floor
관측 — 변화 없음. PR #128 분석 결과 이것은 **probe-set coverage 문제 (PR #125 에서
이미 해결됨)** 가 아니라 **`classify_output` 의 binary saturation** 이었음:

```python
if hits >= 2: return "MEMORIZE"   # hits=2 와 hits=18 동일 처리
```

→ 동일 5 row 가 hits ≥ 2 로 포화 → corpus_v7 의 27.3% chars / 840k pattern strip
이 metric 에 보이지 않음. PR #128 은 `count_register_hits_continuous(text)` 추가 —
**uncapped per-output hit count** (substring 은 `str.count`, regex 는
`len(rx.findall(...))`) — binary 와 병기하여 saturation floor 제거.

본 doc 은 그 새 metric 을 saved JSON 4개 에 적용하여 lever 효과 retrospective 측정.

## 2. Methodology

### Metric (PR #128 verbatim)

`train_p21m_multilingual.py:177` 의 함수 그대로:

```python
def count_register_hits_continuous(text):
    if not text: return 0
    sub_hits = sum(text.count(k) for k in ANIMA_KEYS)
    re_hits  = sum(len(rx.findall(text)) for rx in ANIMA_REGEX_KEYS)
    return sub_hits + re_hits
```

`ANIMA_KEYS` = 26 substring (`"vacuum point"`, `"<carve"`, `"</carve>"`,
`"tension flow"`, `"Tension flows"`, `"basin"`, `"eternal cell"`, `"tier="`,
`"Tier "`, `"psi=["`, `"stimuli converge"`, `"domain "`, `"🛸"`, `"호흡"`,
`"weights 는 불변"`, `"domain 자연/관계/기술/윤리"`, `"vacuum"`,
`"landscape, top emotion"`, `"stimuli"`, `"감각-domain"`, `"운동"`,
`"감각"`, `"tension"`).

`ANIMA_REGEX_KEYS` = 7 (PR #125 확장):
- `[N.N,N.N]` coord brackets
- `🛸N` UFO + digit
- `Tier N`
- `tension flow(s)`
- `vacuum point(s)`
- `frozen cell(s)`
- `top emotion X`

### Aggregate

- per-variant `combined_total` = greedy 10 + sample 10 = 20 row hit-count 합.
- `mean / median / max` = 20 row 통계.
- `nonzero` = continuous hit > 0 인 row 수.
- `binary≥2` = `classify_output` MEMORIZE 판정 row 수 (saturation 비교용).

## 3. Per-variant table

### 3.1 Headline (combined greedy+sample, 20 row)

| variant | binary≥2 | **continuous total** | mean  | median | max | nonzero |
|---------|---------:|---------------------:|------:|-------:|----:|--------:|
| **V5**  | 6        | **85**               | 4.25  | 0      | 18  | 7       |
| **V6**  | 5        | **69**               | 3.45  | 0      | 16  | 5       |
| **V7**  | 6        | **17**               | 0.85  | 0      | 4   | 8       |
| **V8**  | 10       | **28**               | 1.40  | 1.5    | 5   | 11      |

PR #128 commit 보고 (V5=85 · V6=69 · V7=17) 와 byte-identical 재현. V8 = 28 신규.

### 3.2 Mode breakdown (greedy / sample)

| variant | mode   | total | mean | max | nonzero | binary≥2 |
|---------|--------|------:|-----:|----:|--------:|---------:|
| V5      | greedy | 64    | 6.4  | 18  | 4       | 4        |
| V5      | sample | 21    | 2.1  | 15  | 3       | 2        |
| V6      | greedy | 45    | 4.5  | 16  | 3       | 3        |
| V6      | sample | 24    | 2.4  | 15  | 2       | 2        |
| V7      | greedy | 11    | 1.1  | 4   | 5       | 4        |
| V7      | sample | 6     | 0.6  | 3   | 3       | 2        |
| V8      | greedy | 14    | 1.4  | 5   | 6       | 5        |
| V8      | sample | 14    | 1.4  | 5   | 5       | 5        |

binary metric 은 V5/V6/V7 에서 모두 4-6 floor 에서 떨림 — 동일하게 보이지만
continuous 는 **V5 → V7 = 85 → 17 (80% drop)** 로 lever 효과 명확.

### 3.3 Per-output 분포 (combined 20 row, hits>0 만)

| variant | per-output hit list (nonzero 만, sorted desc)         |
|---------|--------------------------------------------------------|
| V5      | `18, 16, 16, 15, 14, 5, 1`                             |
| V6      | `16, 15, 15, 14, 9`                                    |
| V7      | `4, 3, 3, 2, 2, 2, 1, 1`                               |
| V8      | `5, 5, 3, 2, 2, 2, 2, 2, 2, 1`                         |

→ V5/V6 는 **소수 row 가 매우 큰 hit 폭발** (max 18/16) — saturation 의 origin.
V7/V8 는 **다수 row 가 작게 산포** (max 4/5) — strip 후 폭발 사라짐.

## 4. Per-pattern breakdown (combined, top 8 per variant)

### V5 (total 85, no prune)

| count | pattern                                            |
|------:|----------------------------------------------------|
| 11    | `vacuum` (sub)                                     |
| 10    | `stimuli` (sub)                                    |
| 6     | `vacuum point` (sub) + `vacuum point(s)` (regex)   |
| 5     | `basin` (sub)                                      |
| 5     | `stimuli converge` (sub)                           |
| 5     | `landscape, top emotion` (sub)                     |
| 5     | `[N.N,N.N]` coord brackets (regex)                 |

### V6 (total 69, wiki_frac 0.50)

| count | pattern                                            |
|------:|----------------------------------------------------|
| 8     | `vacuum`                                           |
| 6     | `basin`                                            |
| 5     | `stimuli converge`                                 |
| 5     | `tension flow(s)` (regex)                          |
| 4     | `vacuum point` + regex                             |
| 4     | `[N.N,N.N]` (regex)                                |

### V7 (total 17, v7 EN-prune 27.3%/840k)

| count | pattern                                            |
|------:|----------------------------------------------------|
| 5     | `eternal cell` (sub)                               |
| 4     | `domain ` (sub)                                    |
| 3     | `vacuum` (sub)                                     |
| 3     | `weights 는 불변` (sub)                            |
| 1     | `호흡` · `감각`                                    |

### V8 (total 28, v8 ja-safe prune)

| count | pattern                                            |
|------:|----------------------------------------------------|
| 10    | `domain ` (sub)                                    |
| 5     | `eternal cell` (sub)                               |
| 3     | `weights 는 불변` (sub)                            |
| 2     | `tension flow` (sub) + regex                       |
| 2     | `[N.N,N.N]` (regex)                                |
| 2     | `vacuum` · `tension`                               |

**관찰**:

1. **V5→V7 strip target hit**: `tension flow`, `vacuum point`, `[N.N,N.N]`,
   `top emotion X`, `Tier N`, `🛸N` — V5 에서 합 ~25, V7 에서 합 ~0. 27.3%
   corpus prune 이 output 에서 byte-level 검증됨.
2. **V7/V8 잔존 패턴**: `eternal cell`, `domain `, `weights 는 불변`, `호흡`,
   `감각` — KR-side anima identity 표현. v7/v8 prune target 외 (의도적 preserve).
3. **V8 vs V7 약간 reflate (17→28)**: v8 ja-safe prune 은 v7 의 일부 패턴
   (`tension flow + KR-particle`, `[N.N,N.N]`, `knuth_N`) 을 drop → 그
   pattern 들이 살짝 복귀. `tension flow / [N.N,N.N]` 가 각 2 hit 로 reappear.

## 5. Cross-reference

### 5.1 prune ground truth vs output 효과

| | V5 baseline | V6 (wiki_frac) | V7 (EN-strip) | V8 (ja-safe) |
|---|---|---|---|---|
| corpus prune % chars | — | — | **27.28%** | **15.64%** |
| total pattern matches stripped | — | — | **840,434** | **2,221,837** |
| Eval1 binary `register_hits` | 5 | 5 | 5 | 6 |
| **Eval1 continuous total** | **85** | **69** | **17** | **28** |
| Δ vs V5 | = | -19% | **-80%** | **-67%** |

→ corpus-side strip 이 output-side continuous metric 에 **monotone tracking**.
v7 의 840k pattern strip = 80% output reduction. v8 의 더 큰 record-set (2.2M
match) 이지만 더 작은 prune 비율 (15.6% chars) → 67% reduction (덜).

### 5.2 multilingual cost (per_lang_verdicts)

| variant | en  | ko       | zh      | ru  | ja      | n_strong | continuous |
|---------|-----|----------|---------|-----|---------|---------:|-----------:|
| V5      | S   | PARTIAL  | S       | S   | S       | 4        | 85         |
| V6      | S   | PARTIAL  | S       | S   | PARTIAL | 3        | 69         |
| V7      | S   | **S**    | PARTIAL | S   | **WEAK**| 3        | 17         |
| V8      | S   | S        | PARTIAL | S   | **WEAK**| 3        | 28         |

→ continuous metric 80% drop **과 동시에** ja `STRONG → WEAK` (16→11→10 lang_coherent).
strip lever 의 **cost** = multilingual regression, 특히 ja.
v7→v8 transition (ja-safe regex 시도) 으로 ja 회복 실패 — `WEAK` 유지.

### 5.3 WAVE saga 결론 재검증

| WAVE | 원 결론                                            | continuous 로 본 retrospective                     |
|------|----------------------------------------------------|----------------------------------------------------|
| WAVE7 | "lever 효과 unmeasured by harness" (5/20 floor)  | **lever 효과는 컸음 (85→17, 80%)** — binary 가 가렸을 뿐 |
| WAVE7 | "ja STRONG → WEAK = concrete regression"          | 재확인. lever 의 **진짜 cost** 였음                |
| WAVE8 | "ja-safe v8 ablation FALSIFIED"                   | 재확인. continuous 17→28 (소량 reflate) + ja 회복 실패 |

원 결론의 **방향성**은 맞았으나 **lever 효과의 크기**가 binary metric 에 가려져
"unmeasured" 로 처리됨. continuous 로 보면 lever 는 **명확히 작동했지만** cost
> benefit (multilingual regression) 이라 production swap 보류는 여전히 옳음.

## 6. Lever lesson refinement

이전 결론 (WAVE7 §):
> "corpus prune 의 lever 효과가 본 harness 에 안 잡힘"

수정된 결론:
> **corpus prune IS effective at output level** — continuous 85→17 (80% drop)
> 으로 register-leak output reduction 명확히 입증. 그러나 prune 의 **cost** =
> multilingual ja regression (S→W). lever 자체는 invalid 가 아니고 **trade-off
> 의 cost side 가 production budget 을 초과**한 것이 production-swap 결정을 보류시킨 진짜 이유.

**5 lever 의 위치 재조정**:
- L3 `wiki_frac` (WAVE6): continuous 85→69 (19% drop), n_strong 4→3 → marginal lever,
  cost 큼.
- L4 `EN-prose strip` (WAVE7): continuous 85→17 (80% drop), n_strong 4→3, ja S→W →
  **most effective output lever 이지만 ja cost 큼**.
- L5 `ja-safe strip` (WAVE8): continuous 85→28 (67% drop), ja still WEAK →
  ja collision 회피 시도 FALSIFIED.
- L6 (WAVE9+) `EN-share lever` (LANG_ROTATION 직접 조정): corpus 변경 없이
  EN emission ratio lever → 미발화 corpus 와 무관 path.

## 7. Future use — corpus_v9 candidate criteria

본 doc 을 next-cycle baseline 으로 채택. corpus_v9 (또는 후속) 의 success
criteria:

```text
continuous_total ≤ 10       (V7 의 17 보다 더 strip, 88% drop 이상)
AND
multilingual no regression  (n_strong ≥ 4, 어떤 lang 도 WEAK 금지)
AND
binary register_hits unchanged or lower (≤ 5)
AND
register_regress = False
```

- continuous **≤ 10** = V5 의 85 대비 88%+ drop, V7 보다 약간 더 strict.
- ja STRONG **mandatory** — v7/v8 의 ja WEAK 가 production swap 보류 핵심 사유.
- 후보 lever:
  1. v7 의 patterns 중 ja-collision pattern (`tension flow + KR-particle`, `[N.N,N.N]`)
     **+ ja preserve filter** (ja-record skip).
  2. Anima carving corpus 의 KR-side identity 표현 (`eternal cell`, `domain `,
     `weights 는 불변`) → output 잔존 — KR-target prune 으로 보완 검토.
  3. corpus 외 lever: WAVE9+ EN-share LANG_ROTATION 직접 조정.

## 8. Honest C3

1. **n=10 per mode 의 통계 한계** — Eval1 prompt set 이 작아 median 0 이 자주
   발생. continuous_total 이 단일-row outlier (V5 18, V6 16) 에 민감.
2. **same prompt set / same seed** — 4 variant 가 동일 Eval1 fixture 평가
   (좋은 비교 invariant) 이지만 prompt set 자체가 V5 baseline 시점에 fixed →
   curriculum drift 없음.
3. **binary metric 와의 단조 일치 미보장** — V8 binary 10 (V5 6 보다 ↑) 이지만
   continuous 28 (V5 85 보다 ↓). binary 는 saturation 으로 ‘많은 row’ 만 보고
   continuous 는 ‘큰 폭발 row’ 를 측정 — orthogonal axis.
4. **per-pattern attribution 의 double-count** — `vacuum point` 는 substring +
   regex 둘 다 hit (의도된 dup). 트레이너 그대로 재현. true 고유 pattern count
   < 표 표시값.
5. **prune ground truth vs output 의 monotonicity** 가 **단 4 cycle** 의
   correlation. corpus_v9+ 에서 단조 깨질 가능성 (특히 KR-side prune 시도시).
6. **multilingual ja WEAK 의 cause 단정 불가** — prune 의 KR-particle pattern,
   `[N.N,N.N]`, `top emotion X` 셋 중 정확한 culprit 미식별. WAVE8 의 ja-safe
   ablation 도 회복 실패 → 단일 pattern 이 아닌 prune **누적량** 자체일 수 있음.
7. **LIVE register-leak 미측정** — Eval1 fixture-level 측정만. production
   inference 시점의 register-leak (anima_live_register_measure.hexa) 와의
   상관 추후 검증 필요.
