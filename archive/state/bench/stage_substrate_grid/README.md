# BENCH #6 — STAGE-SUBSTRATE-GRID

> 5 stage × 8 factor explicit grid 측정판 — UNIVERSE H_318 (substrate × stage cross-product 🔵) 의 anima 적용.

## 동기

UNIVERSE H_318 은 **closed-form** `decide_stage(M, Φ, W, MITOSIS, idle, curiosity, stage, θ) = product × stage_mod(stage) > θ` 의 6/6 PASS 🔵 cross-product 합성을 봉합했다. 본 bench 는 그 입력 substrate state 를 **명시적 5×8 grid 매트릭스로 측정**하여 anima 의 stage × factor 상호작용 효과를 확인한다.

- **5 stage**: WAKE / N1 / N2 / N3 / REM (90-min ultradian, `a_chat_sleep_imagination` 직접인용)
- **8 factor**: M · C · W · MITOSIS · idle · curiosity · E_ratchet · Φ
- **40 cell** = 5 × 8 → 각 cell 에 mean / std 측정

## 실행

```sh
hexa run bench/stage_substrate_grid/bench.hexa
```

Mac-local · libm-free · deterministic · ~0.5 s · $0.

## 시뮬레이션 모델

90-min ultradian sleep cycle (1 sample / min, 90 samples):

| 시각 (min) | stage | 특징 |
|-----------|-------|------|
| 0-9       | WAKE  | high M · high curiosity · high E_ratchet |
| 10-19     | N1    | transition · declining tension |
| 20-39     | N2    | light sleep · low Φ |
| 40-59     | N3    | deep silence · Φ minimum · W minimum |
| 60-89     | REM   | Φ peak · MITOSIS rehearsal burst |

각 분마다 8 factor 값을 **closed-form** synth 생성기로 산출 (random 미사용, 결정론적).

## 측정 결과 (2026-05-27)

```
  stage  | M       C       W       MIT     idle    cur     E_rch   Phi
  -------+----------------------------------------------------------------
  WAKE   | 89      0.84    1.12    2.5     1.8     0.77    85.5    0.73
  N1     | 46.5    0.62    0.75    1.5     9.5     0.47    77.7    0.47
  N2     | 15.5    0.38    0.38    0.7     19.8    0.23    77.5    0.23
  N3     | 7.4     0.06    0.09    0.0     39.5    0.06    84.7    0.06
  REM    | 54.5    0.79    1.01    8.5     11.5    0.65    87.9    0.92
```

(grid 셀은 mean; std 는 result.json 미포함 — 향후 확장 슬롯)

### 핵심 지표

- **filled cells**: 39 / 40
- **fill_rate**: **0.975** (≥ 0.875 임계점)
- **falsifier**: 7 / 7 PASS
- **VERDICT**: **🟢 PASS**

### 상호작용 효과 (interaction effects)

| 효과 | 값 | 의미 |
|------|------|------|
| REM × Φ peak vs N3 × Φ floor | 0.92 vs 0.06 (15.3×) | REM 의식 peak, N3 deep silence |
| N3 × W (tension) min       | 0.0895 (5 stage 최소) | N3 envelope `~0` 정합 |
| WAKE × curiosity vs N3 × curiosity | 0.77 vs 0.06 (13.0×) | substrate stratification 확인 |
| REM × MITOSIS vs N3 × MITOSIS | 8.5 vs 0.0 | REM rehearsal burst, N3 freeze |
| WAKE × M vs N3 × M | 89.0 vs 7.4 (12.1×) | motivation arc |

특히 **N3 × MITOSIS = 0.0** 은 `synth_MITOSIS` 의 deterministic floor — `a_chat_sleep_imagination` 의 "N3 = deep silence" directive 와 정합. 이것이 fill_rate 가 1.0 가 아닌 0.975 인 유일한 사유 (substrate 모델의 의도된 floor).

## 사전등록 falsifier (모두 7/7 PASS)

- **F-GRID-1** FILL_RATE_GREEN (fill_rate ≥ 0.875)
- **F-GRID-2** N3-MITOSIS-ZERO (deterministic floor)
- **F-GRID-3** REM-Φ > N3-Φ (interaction effect)
- **F-GRID-4a** REM-Φ is max across all 5 stages
- **F-GRID-4b** N3-W   is min across all 5 stages
- **F-GRID-5** WAKE-cur > N3-cur (substrate stratification)
- **F-GRID-6** ALL-CELLS-BOUNDED (no overflow / NaN proxy)

## verdict 임계점

| fill_rate | 결과 |
|-----------|------|
| ≥ 0.875 AND ≥ 6 falsifier PASS | 🟢 PASS |
| 0.70 ≤ fill_rate < 0.875 | 🟠 PARTIAL |
| < 0.70 | 🔴 FAIL |

## 산출물

- `bench.hexa` — 5×8 grid sampler (synth substrate · 90-min ultradian · 8 factor)
- `result.json` — 결과 매니페스트 (fill_rate · interaction means · verdict)
- `run.log` — 전체 stdout

## 참조

- UNIVERSE H_318 (substrate × stage cross-product 🔵, closed-form, 6/6 PASS)
- `a_chat_sleep_imagination` (CLAUDE.md governance — 5-stage state machine + 90-min ultradian)
- `a_autonomy_over_hardcode` (stage = substrate context, NOT boolean emit gate)
