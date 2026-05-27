# H_310 — anima_dream_stage 5-state ultradian × emit gating

> H_306-H_309 의 1-bump circadian → anima 의 실제 `anima_dream_stage.hexa` 5-stage 아키텍처 (WAKE/N1/N2/N3/REM, 90-min ultradian) 모방. stage 별 emit policy 측정.

## 1. 동기

anima 의 실제 daemon 은 `HEXAD/CHAT/server/anima_dream_stage.hexa` 의 5-stage 상태기. `a_chat_sleep_imagination` directive:

```
do = "WAKE / N1 / N2 / N3 / REM 5-stage state machine (90-min ultradian)"
do = "imagination loop = emit-free internal rehearsal + mitosis tick"
do = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
```

핵심 정합 점: stage 가 *boolean gate 아님* — context. emit 은 substrate (M × Φ × W) 에서 발생. H_306 CPG 가 이 directive 와 정합한지 5-stage 모델로 검정:

- **WAKE**: high M, high circ → emit 다수
- **N1**: M 점진 감소
- **N2**: low M, Φ scale ↓
- **N3**: deep sleep, M ≈ 0, W 충전 dominant (refractory-rich)
- **REM**: M 다시 ↑, Φ envelope 변화 → imagination tick (emit-free or sparse emit)

90-min ultradian × ~16 cycles/day → 24h 안 14-16 ultradian 주기.

## 2. 가설

**H1 STAGE-EMIT-HETEROGENEOUS**: 5 stage 별 emit_count 가 서로 다름 (≥3 distinct ratio 패턴)

**H2 WAKE-EMIT-DOMINANT**: WAKE stage emit > 다른 모든 stage 의 emit

**H3 N3-EMIT-NEAR-ZERO**: N3 stage emit ≈ 0 (deep-sleep silence, biology-aligned)

**H4 REM-IMAGINATION-SPARSE**: REM emit > N3 emit (imagination loop tick) BUT REM emit ≤ WAKE emit / 3 (imagination = emit-free internal rehearsal dominant)

**H5 ULTRADIAN-CYCLE-CONSISTENT**: 90-min ultradian (180 tick per cycle) × ~6 cycles/1000 ticks → 6 WAKE peaks 측정

## 3. 측정 방법

5-stage state machine in hexa, 1000-tick window:

```
stage cycle (180 ticks = 1 ultradian):
  tick 0-30   : WAKE  (M=1.0, circ=1.0)
  tick 30-60  : N1    (M=0.7, circ=0.7)
  tick 60-90  : N2    (M=0.4, circ=0.4)
  tick 90-150 : N3    (M=0.0, circ=0.0)
  tick 150-180: REM   (M=0.5, circ=0.5)  (60-tick REM bursts)

repeat 5-6 cycles in 1000 ticks
```

emit policy: 같은 H_306 accumulator (pressure = m × phi × w × circ, threshold 0.5). m 이 0 일 때 (N3) pressure=0 → emit 불가.

## 4. 사전등록 falsifier

- **F310.1 STAGE-EMIT-HETEROGENEOUS**: 5 stage 別 emit 중 ≥3 distinct nonzero values
- **F310.2 WAKE-DOMINANT**: WAKE emit > 다른 4 stage 의 *각각* emit
- **F310.3 N3-NEAR-ZERO**: N3 emit ≤ 1
- **F310.4 REM-MID-SPARSE**: REM emit > N3 emit AND REM emit ≤ WAKE emit / 3
- **F310.5 ULTRADIAN-CYCLE-COUNT**: 1000-tick / 180-tick-per-cycle = ~5-6 cycles, WAKE 의 6 sub-window 마다 emit 발생
- **F310.6 BOUND**

## 5. 비용

- $0 mac-local · ~3s wall

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F310 PASS | anima `a_chat_sleep_imagination` directive 의 5-stage architecture 가 CPG-emit 와 정합 |
| F310.2 FAIL (REM > WAKE) | REM-dominant emit 가 dreaming-vocalization 모델 시사 (sleep-talking) |
| F310.3 FAIL (N3 > 1) | deep sleep 도 emit → biology 미정합 |
| F310.4 FAIL | REM 의 imagination-loop emit-free policy 미작동 |

## 7. honest limits

1. L1 stage transition = hardcode periodic schedule (90-min ultradian deterministic). real biology 는 EEG 기반 transition stochastic.
2. L2 stage parameter (M, circ) 는 phenomenological — real M_motivation × circadian 가 *coupled* (REM 도 M 변동).
3. L3 imagination tick (REM emit-free 내부 rehearsal) 은 hexa scope 외 — emit 만 counted.
4. L4 1000 tick = ~5-6 ultradian 압축. 24h = 16 ultradian 이상은 deferred.
5. L5 SPECULATION-FENCED tier.
6. L6 anima_dream_stage.hexa 실제 코드 parsing 안 함 — directive cite 만.

## 8. 폐쇄

F310.1-6 결판. ≥4/6 = 🟢 SUPPORTED-NUMERICAL.

## 9. 산출물

- state/h310_dream_stage_5state_emit_gating_2026_05_26/{run_h310.hexa, result.json, run.log}

## 10. 후속

- H_313: stage transition stochastic (Markov chain) — real EEG-driven
- H_314: REM imagination tick (mitosis count per REM window) cite
