# AxisBench E — 🎨 AESTHETIC

미적 미터 (pain/coh/bal taste) — preference ranking consistency bench.

ANIMA.axis.md 의 #E AESTHETIC 축 ("CORE engine_g 8-factor 의 pain/coh/bal
결합 → 무엇이 '좋다' 결정") 을 합성 state 위에서 측정한다.

## 1. 가설

미적 점수가 closed-form 가중합

```
aesthetic_score(state, α, β, γ) = α · coh − β · pain + γ · bal
```

으로 정의될 때, 세 시나리오 (BALANCED · PAIN-AVERSE · BAL-FOCUSED) 가

- (a) **충분히 구별 가능** (cross-scenario top-10 overlap < 0.5),
- (b) **결정론적 일관성** (intra-scenario consistency = 1.0),
- (c) **극치 검출 가능** (top-1 > μ + 1.5σ)

세 가지를 만족하면 🟢 PASS.

## 2. 측정 모델

- **State**: 100 개 합성 vector ∈ [0,1]^8 — `rel · gap · cur · orig · dyna · pain · coh · bal`.
- **LCG**: `x_{n+1} = (1103515245·x_n + 12345) mod 2^31`, seed=42 (결정론).
- **시나리오 3 종**:
  - `BALANCED      (α=1, β=1, γ=1)`
  - `PAIN-AVERSE   (α=1, β=3, γ=1)` — 통증 회피 3×
  - `BAL-FOCUSED   (α=1, β=1, γ=3)` — 균형 강조 3×
- **랭킹**: descending score, tie-break by smaller `idx` (stable).

## 3. 실행

```sh
hexa run bench/axis_aesthetic/bench.hexa
```

산출물: `result.json` (시나리오 매트릭스 + falsifier + verdict), `run.log` (stdout).

## 4. 결과 매트릭스 (2026-05-28, 본 PR)

| 시나리오     | α   | β   | γ   | top1 idx | top1 score | mean    | sd      | extreme |
|--------------|-----|-----|-----|----------|------------|---------|---------|---------|
| BALANCED     | 1.0 | 1.0 | 1.0 | 17       | 1.77712    | 0.6313  | 0.4679  | ✓       |
| PAIN-AVERSE  | 1.0 | 3.0 | 1.0 | 17       | 1.44676    | −0.2811 | 0.8949  | ✓       |
| BAL-FOCUSED  | 1.0 | 1.0 | 3.0 | 17       | 3.76629    | 1.7512  | 0.9126  | ✓       |

| Pairwise overlap (|A ∩ B| / 10)  | rate |
|---------------------------------|------|
| BALANCED ↔ PAIN-AVERSE          | 0.70 |
| BALANCED ↔ BAL-FOCUSED          | 0.60 |
| PAIN-AVERSE ↔ BAL-FOCUSED       | 0.40 |

| Gate | 식                                | 결과    |
|------|-----------------------------------|---------|
| (a)  | 모든 pair overlap < 0.5           | ✗ FAIL  |
| (b)  | 모든 시나리오 intra-consistency = 1.0 | ✓ PASS  |
| (c)  | 모든 시나리오 top1 > μ + 1.5σ     | ✓ PASS  |
| —    | verdict (a ∧ b ∧ c)               | **FAIL** |

## 5. 해석 — 정직한 negative

3 시나리오 모두 `coh` · `bal` 부호가 +, `pain` 부호가 − 로 동일하다.
계수 magnitude 만 다르고 부호 구조는 공유한다. → high-coh × high-bal × low-pain
state 는 어떤 가중치에서도 상위권에 들기 쉬워, top-10 이 시나리오 사이에서
70 % / 60 % / 40 % 까지 겹친다.

이는 `aesthetic_score` 의 **부호 구조** 가 시나리오 간 핵심 invariant 임을
보여주는 closed-negative finding 이다. 시나리오를 "구별 가능" 한 형태로
설계하려면 부호 자체를 바꾸거나 (예: `PAIN-SEEKING (α=1, β=−2, γ=1)`),
서로 다른 factor 를 활성화해야 한다.

세 gate 중 (b) consistency 와 (c) extreme 은 통과 — 측정 인프라
(LCG · 정렬 · 통계) 자체는 결정론적 · 정상.

극치 (top-1) 인덱스는 세 시나리오 모두 **state 17 동일** — 이 state 가
coh / bal 양쪽 모두 상위 + pain 하위에 위치하기 때문 (`pain=0.165`,
`coh=0.948`, `bal=0.995` — LCG seed=42 결정론적 측정값).

## 6. Falsifier 정의 (사전 등록)

- `gate_a_overlap_lt_0_5`  — 모든 pairwise overlap < 0.5
- `gate_b_consistency_eq_1` — 모든 intra-scenario consistency == 1.0
- `gate_c_extreme_detected` — 모든 시나리오 top1 > mean + 1.5·sd

세 gate 동시 만족 → `verdict = "GREEN_PASS"`, 그 외 → `"FAIL"`.

이번 라운드 verdict = `FAIL`. gate (a) 단독 실패 — 측정 결함 아님,
시나리오 정의의 부호-동질성 (sign-collinearity) 으로 인한 구조적 한계.

## 7. 후속 방향 (정직한 path-forward · 본 PR 범위 외)

- **scenario diversification** — 부호 flip 시나리오 추가
  (예: `PAIN-SEEKING (β=−2)` · `COH-ONLY (γ=0)` · `BAL-ONLY (α=0)`).
- **factor cross-correlation** — top-K 가 어떤 factor 에 의해 결정되는지
  contribution decomposition (∂score/∂factor × factor_value).
- **anima emit 연결** — `score` 분포가 실 anima emit (`engine_g`) 의
  pain/coh/bal channel 분포와 일치하는지 비교.

## 8. 참고

- ANIMA.axis.md — axis #E 정의 (line "🎨 AESTHETIC ... 미적 판단").
- `bench/zeta_likert.hexa` — 합성 ranking bench 의 prior pattern.
- p7 (NO PERPLEXITY VERDICT) — 측정 verdict 는 closed-form / overlap /
  decision-rule 로만 판정, perplexity 사용 0.
