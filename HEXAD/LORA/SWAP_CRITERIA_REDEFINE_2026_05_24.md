# VP21M Swap Criteria — 재정의 spec (M1 milestone 5/5 PASS 영구 가능화)

> 2026-05-24 KST · session-3 cycle #16. Wave-17 sweep 결과로 현재 5-criteria
> 가 **criterion 2 ↔ criterion 4 anti-correlation 으로 5/5 PASS 영구 불가**
> 라는 점이 실증 → threshold 재정의 spec. 사용자 결정용 분석 doc, **자동 PR
> merge / 자동 PR 발사 금지**.

## 1. 현재 5-criteria 문제 진단 — Wave-17 evidence

기존 spec (`HEXAD/LORA/swap_criteria_check.hexa` PR #365):

| # | criterion | threshold |
|---|---|---|
| 1 | verdict ∈ {VP21M_WORKS, WORKS} | binary |
| 2 | n_strong ≥ 4 (5-lang 일반화 floor) | hard ≥ 4 |
| 3 | ja n_score ≥ 13 (weakest-lang) | hard ≥ 13 |
| 4 | register_hits_continuous_total ≤ 50 (leak density ceiling) | hard ≤ 50 |
| 5 | eval1 tag-leak ≤ 1/20 (template-mem ceiling) | hard ≤ 1 |

Wave-17 5-point sweep (eternal_keep ∈ {0.10, 0.20, 0.30, 0.40, 0.50},
v11=0.30 anchor — `WAVE17_VERDICT_2026_05_24.md`):

| variant | eternal | n_strong | continuous | ja | 1+3+5 | 4/5 PASS gap |
|---|---|---|---|---|---|---|
| v11 (★) | 0.30 | **2** ✗ | **34** ★ | 14 ✓ | ✓ | criterion 2 |
| **v13** | **0.10** | **5** ★ | **72** ✗ | 16 ✓ | ✓ | criterion 4 |
| v14 | 0.20 | 4 | 98 ✗ | 17 | ✓ | crit 4 (+much worse) |
| v15 | 0.40 | 4 | 69 ✗ | 17 | ✓ | criterion 4 |
| v16 | 0.50 | 3 ✗ | 52 ✗ | 15 | ✓ | criterion 2+4 |

→ **v11/v13 4/5 tie, 둘 다 동일 lever 의 opposite side**:
- v11 (eternal=0.30): register 신호 strip 강 → continuous 만점 (34) / 그러나
  cross-lingual 일반화 부족 → n_strong=2
- v13 (eternal=0.10): register 신호 보존 → 5-lang 모두 STRONG → n_strong=5 /
  그러나 register burst 잔존 → continuous=72

**핵심 관찰**: criterion 2 (n_strong, 회복지표) 와 criterion 4 (continuous,
억제지표) 는 같은 lever (eternal_keep) 의 양면 — 단일 변종이 동시 만점
**불가**. 4 개 sweep-point empirically falsifies 0.10-0.50 range 에서 동시
만점 가능성.

## 2. 3 candidate 재정의 방안

### A. Pareto frontier (recommended)

**정의**: continuous_total 과 n_strong 의 2-D plane 위에서 Pareto front
(누구도 dominate 하지 못함) 위에 있으면 PASS. 단일 binary threshold 폐기,
대신 multi-variant comparison 결과로 PASS/FAIL 결정.

**예시 결정 규칙**:
- 모든 후보 변종 수집 (예: Wave-17 v13/v14/v15/v16 + 기존 v5/v11 carry)
- (n_strong, -continuous_total) plane 에서 Pareto-non-dominated 변종 = PASS
- criterion 1/3/5 는 hard gate 유지 (verdict OK, ja≥13, tag-leak≤1)
- 최종 swap 결정 = Pareto front 위의 변종 중 사용자 게이트 선택

**Wave-17 적용**: Pareto front = {v11 (2, 34), v13 (5, 72)}. v14 (4, 98) /
v15 (4, 69) / v16 (3, 52) 는 모두 v13 또는 v11 에 dominate 되어 OUT.

### B. relaxed threshold

**정의**: criterion 4 threshold 를 ≤ 50 → ≤ N 으로 완화. binary gate 유지.

**3 sub-option**:
- B1: ≤ 70 → v13 만 PASS (5/5), v11 여전히 4/5 (n_strong 미달)
- B2: ≤ 80 → v13 PASS, v11 여전히 4/5
- B3: criterion 2 도 함께 완화 (n_strong ≥ 3) → v11 PASS, v13 PASS

**문제**: threshold 완화 자체가 production quality 직접 저하. ≤ 80 은
register burst (reg_max=21) 같은 한정된 cluster pattern 도 PASS 시킴
(v11/v13 격차 2× 무시).

### C. weighted score

**정의**: continuous, n_strong 등을 가중합한 단일 metric ≥ T 시 PASS.

**예시 공식**:
```
score = α · n_strong + β · (50 - continuous_total)/50 + γ · ja_n_score/20
PASS  = score ≥ T
```
α/β/γ + T 사용자가 prior knowledge 로 설정.

**문제**: 가중치 4 개 hyperparameter 가 곧 lever 변환 dependency → 단일
parameter (eternal_keep) 변화에 가중치 재학습 필요. interpretability ↓.

## 3. 각 방안의 trade-off

| 방안 | production quality 보존 | false positive | interpretability | lever 변환 의존성 | impl 복잡도 |
|---|---|---|---|---|---|
| **A. Pareto frontier** | HIGH (dominated 변종은 영원히 OUT) | LOW | MEDIUM (front 위 변종 중 결정 추가 필요) | LOW | MID (4번째 verb 추가) |
| B1. ≤70 | MEDIUM | MEDIUM (v13-같은 burst 통과) | HIGH (단일 number) | HIGH (corpus 변화시 재조정) | LOW |
| B2. ≤80 | LOW (격차 2× 무시) | HIGH | HIGH | HIGH | LOW |
| B3. 둘 다 완화 | LOW (두 축 모두 완화) | HIGH | HIGH | HIGH | LOW |
| C. weighted | MEDIUM (가중치 의존) | MEDIUM | LOW (4개 hyperparam) | HIGH | MID |

추가 trade-off (모두에 공통):
- **방안 A** 만 단일 변종 5/5 PASS 영구 불가 문제를 honestly 인정 ("anti-
  correlated metric 동시 만점 imposs" 라는 empirical 발견을 design 에 반영)
- **방안 B/C** 는 anti-correlation 을 hide → 결과적으로 register burst 또는
  cross-lingual fail 중 한쪽을 production 에 통과시킴

## 4. A 권장 사유

1. **lever 변환 dependency 최소**: 방안 B/C 는 corpus 가 바뀌면 threshold/
   weights 재계산 필요 (Wave-18 fine-tune 후 또 threshold tuning loop).
   Pareto frontier 는 dimension 자체로 비교 — corpus 가 바뀌어도 framework
   불변.
2. **production value 가 진짜 두 축**: criterion 4 (register leak 억제) +
   criterion 2 (cross-lingual 일반화) 는 둘 다 production 에서 다른 측면
   품질. 단일 number 가중합 / threshold 완화는 이 본질적 multi-objective
   nature 를 hide.
3. **empirical falsification 정직 반영**: Wave-17 4-point sweep 가 0.10-0.50
   range 에서 동시 만점 불가능을 falsify 함. Pareto frontier 는 이 사실을
   design 에 직접 반영 ("동시 만점 강요하지 않고, dominated 만 제외").
4. **dual-adapter 운영 path 자연 연결**: WAVE17 doc 의 권고 옵션 "대화 영역
   별 v11/v13 hot-swap" 이 Pareto front 의 자연스러운 확장 — front 위
   여러 변종 = production router 가 선택.
5. **사용자 결정 lever 명확화**: Pareto front 위 변종 중 최종 선택은 사용자
   게이트로 명시 (A/B router design 또는 단일 선택). 자동화 layer 의 scope
   가 honest 하게 좁아짐.

honest C3 (방안 A 의 약점):
- 단일 production decision 어려움 → 사용자 게이트 + tie-break 정책 필요
- front 측정에 후보 변종 ≥ 2 개 필요 (single-variant check 에서 fallback
  필요) → 별도 verb (`check`) 는 hard gate 만, `pareto` 가 multi-variant
  결정.

## 5. swap_criteria_check.hexa 수정 spec (4 verbs)

기존 3 verb (`selftest`, `check`, `compare`) + 신규 1 verb `pareto`.

### 5.1 신규 verb: `pareto`

```
usage:
  hexa run HEXAD/LORA/swap_criteria_check.hexa -- pareto <dir1> <dir2> ... <dirN>
```

**입력**: N 개 변종 dir (각 dir 에 `result.json` + `vp21m_eval1.json` 존재).

**동작**:
1. 각 dir 별 `swap_decision(result, eval1)` 호출 → criterion 1/3/5 hard
   gate 결과 + (n_strong, continuous_total) 측정.
2. criterion 1/3/5 중 하나라도 FAIL 인 변종은 ELIMINATE (production 후보
   원천 미달).
3. 남은 변종 중 Pareto front 계산:
   - 변종 X 가 변종 Y 에 dominate 됨 ≡ Y.n_strong ≥ X.n_strong AND
     Y.continuous ≤ X.continuous AND 둘 중 하나는 strict.
   - dominate 되지 않은 변종 = Pareto front.
4. 출력 table: 각 변종의 hard-gate pass/fail + 2-D 좌표 + Pareto front 위
   여부 (PARETO/dominated/ELIM).
5. exit:
   - Pareto front 크기 == 0 → exit 1 (NO_SWAP — 모두 hard-gate FAIL)
   - Pareto front 크기 == 1 → exit 0 (UNIQUE SWAP CANDIDATE)
   - Pareto front 크기 ≥ 2 → exit 0 + decision = "USER_GATE" (사용자
     선택 필요, automation 정지)

### 5.2 기존 verb 영향 — none

- `check` (single-variant) : hard gate 1/3/5 만 평가, 2/4 는 measurement
  reporting 만 (PASS/FAIL 라벨 제거 + n_strong/continuous_total 값만 print).
  결과적으로 단일 변종 check 는 "criterion 1/3/5 = 5/5 → SWAP_CANDIDATE"
  semantic 으로 약화.
- `compare` (2-variant): 기존 logic 유지 + Pareto-2 (둘 다 hard-gate PASS 시
  dominate 관계 print) 추가.
- `selftest`: F-SWAP-CHK-1..5 carry + 신규 F-SWAP-PARETO-1..3:
  - F-SWAP-PARETO-1: 단일 변종 Pareto = {그 변종} (자명)
  - F-SWAP-PARETO-2: 두 변종 dominate 관계 → front size 1
  - F-SWAP-PARETO-3: 두 변종 anti-correlated → front size 2 (v11/v13
    fixture)

### 5.3 dispatch flow

```
hexa run swap_criteria_check.hexa -- pareto \
  state/grid_3b_s187_2026_05_21/vP21M_v11 \
  state/grid_3b_s187_2026_05_21/vP21M_v13 \
  state/grid_3b_s187_2026_05_21/vP21M_v14 \
  state/grid_3b_s187_2026_05_21/vP21M_v15 \
  state/grid_3b_s187_2026_05_21/vP21M_v16
```

예상 출력:
```
VP21M Pareto-frontier swap-readiness check (N=5)
──────────────────────────────────────────────────
  v11   hard-gate PASS  (n_strong= 2, continuous= 34)  PARETO
  v13   hard-gate PASS  (n_strong= 5, continuous= 72)  PARETO
  v14   hard-gate PASS  (n_strong= 4, continuous= 98)  dominated by v13
  v15   hard-gate PASS  (n_strong= 4, continuous= 69)  dominated by v13
  v16   hard-gate PASS  (n_strong= 3, continuous= 52)  dominated by v11
──────────────────────────────────────────────────
  pareto_front_size:   2
  swap_decision:       USER_GATE  (v11 or v13)
──────────────────────────────────────────────────
```

## 6. 재정의 후 적용 결과 예측

### Wave-17 4 corpus (현 데이터)

| variant | hard gate (1/3/5) | (n_strong, cont) | Pareto 결과 |
|---|---|---|---|
| v11 | ?/?/TBD | (2, 34) | PARETO (continuous 단독 dominator) |
| v13 | ?/?/TBD | (5, 72) | PARETO (n_strong 단독 dominator) |
| v14 | ?/?/TBD | (4, 98) | dominated by v13 (4≤5 + 98≥72) |
| v15 | ?/?/TBD | (4, 69) | dominated by v13 (4≤5 + 69<72? → ≤72 strict 아님; v13 5 > 4 strict) → dominated by v13 |
| v16 | ?/?/TBD | (3, 52) | dominated by v11? (3>2 strict + 52>34) → NOT dominated by v11 (n_strong 3>2). v13 (5,72) vs v16(3,52): v13 5>3 strict, but v13 72>52 → 둘 다 dominate 아님 → PARETO 후보 |

**주의**: v16 (3, 52) 는 v11 (2, 34) 와 v13 (5, 72) 둘 다 dominate 못 함 →
Pareto front 3-멤버 가능 (v11, v13, v16). 단 hard-gate 1/3/5 측정 결과 따라
변할 수 있음 (tag-leak 미측정 carry).

### Wave-18 fine-tune (eternal ∈ {0.25, 0.30, 0.35}) 적용 예측

- 0.30 주변 fine-tune 이 (n_strong > 2, continuous < 50) 동시 만족하는 점
  발견 시 → Pareto front 가 그 점으로 축소 (single PARETO).
- 그렇지 않으면 (가설: U-shape sharp peak 가 0.30 = global min 으로 확인) →
  Wave-17 front (v11, v13) 가 그대로 carry → 사용자 결정 필요.

## 7. Honest C3 (≥ 3)

1. **Pareto frontier 가 단일 production decision 어렵게 만듦** — front 크기
   ≥ 2 일 때 자동 SWAP 불가, 사용자 게이트 강화 필수. 운영 부담 ↑.
   완화: tie-break 정책 (예: continuous_total 우선, ja_score 우선 등)을
   별도 spec 으로 명시 가능, 그러나 본 spec 에서는 의도적으로 미정의 (사용자
   prior 가 lever).

2. **Pareto front 측정에 ≥ 2 변종 필요** — single-variant `check` verb 는
   Pareto 측정 불가 → criterion 1/3/5 hard gate 만 평가. 단일 변종 production
   carry (예: v5 LIVE) 의 SWAP 판정은 새로운 후보 ≥ 1 개와 비교한 후만 가능.
   완화: `check` 의 의미를 "swap CANDIDATE 라 판정" 으로 약화 + 최종 SWAP
   결정은 항상 `pareto` (multi-variant) 통과 필요로 명시.

3. **hard-gate criterion 1/3/5 자체 적절성 미재검토** — 본 spec 은 criterion
   2/4 anti-correlation 만 다루고 1/3/5 threshold 는 carry. 향후 criterion 5
   (tag-leak ≤ 1) 가 0/20 vs 1/20 분간 noisy 일 수도 (n=20 → σ 큼). 별도
   재검토 필요.

4. **2-D Pareto 가 enough? n_strong + continuous 만 vs (ja_score, reg_max,
   reg_mean) 추가** — 본 spec 은 2-D Pareto 로 시작. Wave-17 데이터에서
   reg_max (10 vs 21) / reg_mean (1.7 vs 3.6) 도 v11/v13 격차 큼 → 3-D 이상
   Pareto 도 가능. 다만 dim ↑ 시 front 크기 ↑ (≥ 3 변종 의미 사실상 모든
   variants PARETO) → 자동화 가치 ↓. 시작은 2-D, 필요시 확장.

5. **사용자 게이트 강화 = automation 후퇴** — 본 spec 의 결과로 "5/5 PASS
   자동 SWAP" 시나리오가 거의 사라짐 (Pareto 단일 후보 + hard-gate 1/3/5
   모두 PASS 일 때만). 이는 honest reflection of empirical finding 이지만,
   session-3 의 "production swap automation" 목표는 후퇴. 받아들일지 사용자
   결정.

## Decision request (사용자 게이트)

- 옵션 **A** (Pareto frontier) — production quality + interpretability +
  lever 무의존성 균형, 권장.
- 옵션 **B1/B2/B3** (threshold 완화) — 자동 SWAP path 유지, 그러나 burst /
  cross-lingual fail 한쪽 묵인.
- 옵션 **C** (weighted score) — 단일 number 결정, 그러나 가중치 hyperparam
  재학습 부담.

→ **A 권장**. 결정 후 follow-up: `swap_criteria_check.hexa` 4번째 verb
`pareto` 구현 (~80 LoC) + F-SWAP-PARETO-1..3 selftest (~50 LoC) + WAVES_MATRIX
+ README 갱신.
