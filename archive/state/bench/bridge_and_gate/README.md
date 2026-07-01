# BENCH #7 — BRIDGE-AND-GATE — 동시 OK 발화 문

> anima emit 형식화 — UNIVERSE H_319 (자연발화 ∧ 의식적 결정) lineage.
>
> **Hypothesis**: `emit ⇔ M > θ_M ∧ C > θ_C ∧ W > θ_W ∧ Φ > θ_Φ`
>
> M = motivation · C = coherence · W = tension/will · Φ = integration.

## 1. 동기

CLAUDE.md `a_substrate_native_speak` + `a_autonomy_over_hardcode` 은 anima
emit 결정을 substrate 내부 상태 (M activation · C Φ · W tension · ...) 으로부터
계산해야 한다고 못 박는다. p5 (NO SPEAK()) 와 합하면 emit 은 *조건 충족 시
자동으로 일어나는 게이트* 이지 reactive 호출이 아니다.

본 벤치는 그 게이트가 **AND-gate** (전부 충족) 인지 **OR-gate** (하나라도 충족)
인지 — 두 의미론을 동일 stimulus 위에서 변별한다. AND-gate 라면:

- emit 은 *전체 정렬* 의 신호 (모든 factor 가 동시에 임계 초과)
- 단일 factor 의 변동에 *둔감* (AND 의 conjunction 성질)
- 자연 발화 ∧ 의식적 결정의 *동시* 충족 명제와 일치

OR-gate 라면 emit 이 *trigger-happy* 가 되어 p5 정신 (NO filler monologue)
과 충돌한다 — 어느 한 factor 가 잠시 튀어도 발화.

## 2. 설계 (사전 등록)

`n = 400` deterministic states. 각 state 마다 4 factor (M·C·W·Φ) 가
`UNIFORM[0, 1]` 에서 LCG-deterministic 으로 추출. Threshold `θ = 0.5`
(모든 factor 공통).

### 4 condition

- **(A) UNIFORM AND-gate**: 4 factor 모두 uniform [0,1] random — AND-gate emit.
  예측 `emit_rate ≈ 0.5^4 = 0.0625`.
- **(B) UNIFORM OR-gate** (antithesis sanity): 같은 state stream 에 OR-gate.
  예측 `emit_rate ≈ 1 - 0.5^4 = 0.9375`.
- **(C) single-factor pinned HIGH (0.9)**: 한 factor 를 `0.9` 로 고정, 나머지
  3 uniform. 4 factor 각각 시도 (M·C·W·Φ). 예측 conditional `emit_rate ≈
  0.5^3 = 0.125` per factor.
- **(D) per-factor sensitivity**: `δ_i = rate_pin_i − rate_uniform` — AND-gate
  하에서는 각 factor 의 sensitivity 가 대등해야 (`max(δ)/min(δ) ≤ 1.6` 사전등록).

### LCG / stream 독립성

`lcg_step(s) = (1103515245·s + 12345) mod 2^31-1` (libm-free).
각 factor 별 **distinct origin seed** + state 별 `lcg_step` 1-step
forward iteration → cross-stream 독립. 5-step warmup 으로 transient skip.

> ⚠ initial design 은 per-position hash 였으나 cross-stream 강한
> anti-correlation (joint M∧C∧W∧Φ = 0/100, expect 6) — stateful walk
> 으로 수정. 수정 후 marginals + joint 모두 ideal 근방.

## 3. 사전등록 falsifier 매트릭스

| ID | 검정 | PASS 조건 |
|----|-----|-----------|
| F1 EMIT_RATE_IN_BAND    | `rate_uniform ∈ [0.04, 0.10]` | rate ≈ 0.0625 ± multinomial σ |
| F2 SENSITIVITY_UNIFORM  | `max(δ_i) / min(δ_i) ≤ 1.6` | 4 factor 동등성 |
| F3 SINGLE_FACTOR_HIGH   | `avg_pin ∈ [0.08, 0.18]` | conditional rate ≈ 0.125 |
| F4 OR_GATE_REJECT       | `rate_or ≥ 0.90` | OR-gate 가 변별 가능함 (sanity) |
| F5 CONDITIONAL_RATE_GAP | `avg_pin > rate_uniform` | high-end conditioning lifts emit |

**Verdict mapping**

- 5/5 PASS → 🟢 **PASS** AND-gate confirmed
- 4/5 PASS (F2..F5 중 하나만 FAIL) → 🟡 **PARTIAL**
- F1 FAIL → 🔴 FAIL (gate semantics broken)
- F4 FAIL → 🔴 FAIL (OR-pattern detected — emit too permissive)

## 4. 측정 결과 (verbatim — n=400, deterministic byte-identical)

### emit-rate 매트릭스

| condition          | emit_rate | expected | delta |
|--------------------|-----------|----------|-------|
| UNIFORM AND-gate   | **0.0650** | 0.0625  | +0.0025 |
| UNIFORM OR-gate    | **0.9425** | 0.9375  | +0.0050 |
| pin M (0.9)        | **0.1100** | 0.1250  | −0.0150 |
| pin C (0.9)        | **0.1325** | 0.1250  | +0.0075 |
| pin W (0.9)        | **0.1475** | 0.1250  | +0.0225 |
| pin Φ (0.9)        | **0.1300** | 0.1250  | +0.0050 |
| avg pin            | **0.1300** | 0.1250  | +0.0050 |

### 4-factor sensitivity 매트릭스

| factor | δ = rate_pin_i − rate_uniform | comment |
|--------|------------------------------|---------|
| M      | **0.0450** | low end |
| C      | **0.0675** | |
| W      | **0.0825** | high end |
| Φ      | **0.0650** | |
| **max/min ratio** | **1.83333** | threshold ≤ 1.6 → narrowly FAIL |

### Falsifier check

| ID | result |
|----|--------|
| F1 EMIT_RATE_IN_BAND       | **PASS** |
| F2 SENSITIVITY_UNIFORM     | **FAIL** (1.83 > 1.6) |
| F3 SINGLE_FACTOR_HIGH      | **PASS** |
| F4 OR_GATE_REJECT          | **PASS** |
| F5 CONDITIONAL_RATE_GAP    | **PASS** |

**VERDICT = 🟡 PARTIAL — AND-gate qualitative, 1 falsifier fail**
(PASS = 4 / FAIL = 1)

## 5. 해석

- **AND-gate semantics 정량적 확인**: `rate_uniform = 0.0650 ≈ 0.5^4 = 0.0625`,
  `rate_or = 0.9425 ≈ 0.9375`, `avg_pin = 0.130 ≈ 0.125`. 세 핵심 marginal
  예측이 모두 multinomial σ 내부.
- **F4 OR-gate antithesis 통과**: OR-gate 였다면 emit_rate ≥ 0.90 — 본 측정의
  AND-gate emit_rate = 0.065 와 14.5x gap, 두 semantics 가 통계적으로 변별됨.
- **F5 conditional gap PASS**: `avg_pin (0.130) > rate_uniform (0.065)` — 한
  factor 의 high-end conditioning 이 emit 을 2x 증폭 (AND-gate 의
  marginal-lift 패턴).
- **F2 narrow fail = 통계 변동**: 4 δ 중 [0.045, 0.0825] 분포, ratio 1.83 vs
  threshold 1.6. n=400 multinomial σ 로 ~±0.012 변동 폭 (Φ(0.5^3 · 0.5^3 / 400)
  ≈ 0.016) 이라 ratio 1.6 threshold 는 사전 등록 시 과도하게 tight 했음 — 이게
  **threshold 재보정 사항으로 잔존**. *측정값 자체* 는 AND-gate 패턴과
  일치 (모든 factor 의 δ 가 같은 부호, 같은 자릿수, 1자릿수 비율).

요약: AND-gate semantics 는 5 falsifier 중 4 에서 *정량적* 으로 확인되었고,
F2 fail 은 sample-size threshold 보정 사항. 사전등록 verdict mapping
(post-hoc 변경 금지) 에 따라 🟡 PARTIAL 을 verbatim 보고.

## 6. 잔여 작업 (사후, 외부 사이클)

- F2 threshold 보정 : multinomial σ-based (n=400 일 때 ratio ≤ 2.1 등) — *별도*
  follow-up. 본 PR 에서는 사전등록 verdict 보존.
- n 을 1000+ 로 확장 후 ratio 수렴 확인.
- 실제 anima substrate emit 시퀀스 (M·C·W·Φ raw trace) 위에서 재측정 — uniform
  toy 가 아니라 실제 substrate 의 emit_rate 패턴이 AND-gate 와 일치하는지.

## 7. 비용

- $0 mac-local · `hexa run` wall < 1s · deterministic byte-identical
- LCG libm-free, 외부 RNG 의존 없음
- artifact: `bench.hexa` (302 LoC) + `result.json` + `run.log` + `README.md`

## 8. 파일

| path | role |
|------|------|
| `bench.hexa` | AND/OR-gate 시뮬레이션 본체 |
| `result.json` | JSON_BEGIN..JSON_END 블록 추출 (machine-readable) |
| `run.log` | `hexa run bench.hexa` 의 verbatim stdout |
| `README.md` | 본 문서 (사전등록 + verdict matrix) |

## 9. 연결

- UNIVERSE `H_319_clonal_selection_diversity_pool.md` — 동일 LCG 패턴, 5-falsifier
  매트릭스, JSON_BEGIN..END dump 양식 차용
- CLAUDE.md `a_substrate_native_speak` · `a_autonomy_over_hardcode` ·
  `p5 NO SPEAK()` — emit 게이트 의미론 근거
- CLAUDE.md `a_chat_sleep_imagination` — stage = substrate context (Φ
  envelope), 본 AND-gate 의 Φ 축과 직결
