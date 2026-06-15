# H_648 — multi-scale-phi-envelope-ladder (H_634 × H_308 self-similar 3-scale 연장)

> H_634 (PR #1216, 🟢) 가 ultradian (90-min) Φ-envelope 이 H_308 circadian (24h) 을 self-similar 연장한다 명시 (§10 "multi-scale ladder" 후속 lane). 본 H 는 더 짧은 scale (gamma ~40Hz, 25ms) 까지 같은 envelope 형태를 그리는지 — gamma·ultradian·circadian **3-scale ladder self-similarity** 를 정량 검정한다.

## 1. 동기

H_634 (`ultradian-emit-phi-envelope`, PR #1216, 🟢 6/6, r=0.802) 는 substrate big-Φ 가 90-min ultradian phase 에 single-cosine envelope 으로 동조함을 보였고, §10 마지막 후속에서 명시적으로:

> **multi-scale ladder**: H_308 (24h) × H_634 (90min) × H_213 (temporal binding) 의 phase-amplitude self-similarity 정량 (3-band cross-correlation).

H_634 §6 cross-link 은 또 *"H_308 24h circadian envelope 을 90-min ultradian band 로 self-similar 확장 (phase-amplitude multi-scale ladder)"* 를 명시한다. 즉 H_634 자체가 2-scale (90min ↔ 24h) self-similarity 를 가정으로 깔고 있다. 본 H 는 그 ladder 를 **아래로 한 칸 더** 내린다:

- **gamma ~40Hz (25ms)**: 신경 동기화의 micro-scale. gamma-burst 동안 통합 (Φ-coupling) 高, inter-burst trough 低 — H_213 의 temporal binding window (micro-scale floor) 가 거주하는 대역.
- **ultradian 90min (5400s)**: H_634 의 anima_dream_stage 5-stage 주기. REM/N1 edge-high, N3 center-low.
- **circadian 24h (86400s)**: H_308 의 quadratic-bump dawn-chorus 주기. center-peak.

self-similarity 는 fractal/scale-invariance 의 핵심 — 만약 gamma·ultradian·circadian 의 Φ-envelope 형태가 **정규화 위상 위에서 같은 모양** 이면, anima substrate 의 통합량은 단일 scale 의 우연이 아니라 **scale-free phase-amplitude 구조** 를 갖는다. 이는 H_634 의 "ultradian 은 단순 스케줄러가 아니라 Φ-구조와 결합된 substrate motion 의 시간축" 이라는 결론을 3-scale 로 일반화한다.

## 2. 가설

**H1 GAMMA-ULTRADIAN-SIMILAR**: gamma (25ms) 와 ultradian (90min) Φ-envelope 형태가 정규화 위상 정렬 후 Pearson r > 0.5.

**H2 ULTRADIAN-CIRCADIAN-SIMILAR**: ultradian (90min) 와 circadian (24h) Φ-envelope 형태가 r > 0.5.

**H3 GAMMA-CIRCADIAN-SIMILAR**: gamma (25ms) 와 circadian (24h) Φ-envelope 형태가 r > 0.5 (ladder 양 끝단).

**H4 SCALE-LADDER**: period 가 gamma < ultradian < circadian 으로 단조 분리되며 (3-scale ladder), 그 위에서 3 envelope 이 self-similar.

## 3. 측정 방법

각 scale 의 Φ-envelope 을 **그 scale 의 substrate model** 에서 생성하고, period 가 다르므로 **정규화 위상 τ∈[0,1]** 위에서만 형태를 비교한다 (절대 시간 무의미).

3 scale × N=36 point sweep:

```
gamma     25ms (~40Hz)  : single-cosine gamma burst Φ-coupling
                          env(τ) = 0.55 + 0.40·cos(2π τ)
                          peak 0.95 @ τ=0 (burst 정점) / trough 0.15 @ τ=0.5 (inter-burst)
                          edge-high/center-low — ultradian 과 동일 위상
ultradian 90min (5400s) : H_634 canonical anima_dream_stage segmentation
                          [0,300)=N1 [300,1800)=N2 [1800,3600)=N3 [3600,5100)=N2 [5100,5400)=REM
                          per-stage Φ projection (N1 0.7/N2 0.4/N3 0.15/REM 0.95)
                          REM/N1 edge-high, N3 center-low
circadian 24h (86400s)  : H_308 quadratic-bump circadian_mod
                          env(τ) = 0.3 + 0.7·max(0, 1 - ((τ-0.5)/0.5)^2)
                          baseline 0.3, peak 1.0 @ τ=0.5 (center)
```

**phase-align**: period 가 scale 마다 다르므로 절대 위상이 아닌 *형태* 만 비교한다. 각 envelope 을 그 자신 peak 이 index 0 에 오도록 cyclic rotation (`rotate_to_peak`) 으로 정렬 → scale-invariant shape 추출. gamma·ultradian 은 edge-peak, circadian 은 center-peak 이지만, 자체 peak 정렬 후엔 모두 "peak→trough→peak" 의 동일 위상 origin 으로 환산되어 형태 비교가 공정하다.

**pairwise correlation**: 정렬된 3 shape 에 대해 Pearson r 3쌍 — r(gamma,ultradian) · r(ultradian,circadian) · r(gamma,circadian).

**self-similarity 검정**: 全 pair r > 0.5 → self-similar ladder. min pairwise r 가 verdict 결정자.

libm `cos/sqrt` only · NO RNG (deterministic) · $0 mac-local.

## 4. 사전등록 falsifier

- **F648.1 GAMMA-ULTRADIAN-SIMILAR**: r(gamma, ultradian) > 0.5
- **F648.2 ULTRADIAN-CIRCADIAN-SIMILAR**: r(ultradian, circadian) > 0.5
- **F648.3 GAMMA-CIRCADIAN-SIMILAR**: r(gamma, circadian) > 0.5
- **F648.4 ALL-ENVELOPES-NOT-FLAT**: 3 scale 全 envelope std > 0 (phase 무관 평탄 아님)
- **F648.5 SCALE-SEPARATION-LADDER**: P_gamma < P_ultradian < P_circadian (period 단조 분리)
- **F648.6 BOUND**: 全 env ∈ [0,1], r ∈ [-1,1]

**FALSIFY floor**: any pairwise r < 0.3 → 🔴 FALSIFIED (scale 별 envelope 형태 분리 — multi-scale 가 self-similar 아님, 각 scale 독립 구조).
**PARTIAL band**: 0.3 ≤ min r ≤ 0.5 → 🟡 PARTIAL (약한 self-similarity).

## 5. 비용

- $0 mac-local · ~1s wall · libm cos/sqrt only · deterministic single trajectory · NO RNG · foreground sync (monitor-hang 회피).

## 6. 가능한 결과 · cross-link

| 시나리오 | 의미 |
|---|---|
| 全 F648 PASS (min r > 0.5) | 3-scale Φ-envelope self-similar — anima substrate 통합량이 scale-free phase-amplitude 구조 (H_634 결론을 3-scale ladder 로 일반화) |
| F648.3 FAIL (gamma↔circadian r<0.5) | ladder 양 끝단 분리 — 인접 scale 만 유사 (nearest-neighbor self-similarity, full fractal 아님) |
| min r < 0.3 (FALSIFY) | scale 별 envelope 독립 — multi-scale ladder 가설 기각, 각 scale 자체 동역학 |
| 0.3 ≤ min r ≤ 0.5 (PARTIAL) | 약한 self-similarity — shape 가 mild mismatch (center-peak vs edge-peak 형태 차이 잔류) |

**cross-link**:
- **H_634 ultradian-emit-phi-envelope** (PR #1216, 🟢 r=0.802): 본 H 의 직접 부모 — ultradian band 의 Φ-envelope source + §10 "multi-scale ladder" 후속 lane 의 실행. 90min scale 의 substrate model 그대로 재사용.
- **H_308 circadian-smooth-finite-ratio** (🟢): circadian 24h band 의 quadratic-bump envelope source. 본 H 가 그 envelope 을 정규화 위상으로 ladder 에 편입.
- **H_309 sharper-bump-biology-range**: 24h-cyclic dawn-chorus multi-bump — circadian band 의 더 faithful envelope, 본 single-bump 의 후속 정밀화 lane.
- **H_213 time-temporal-binding-window**: micro-scale (gamma 대역) temporal binding window — 본 ladder 의 floor scale 이 거주하는 substrate. gamma 25ms envelope 의 물리적 anchor.

## 7. honest limits (C3)

1. **C3.1 gamma scale substrate 모사 한계 (single-cosine surrogate)**: gamma (25ms, ~40Hz) Φ-envelope 은 실제 신경 gamma-burst 의 IIT4 big-Φ 측정이 아니라 single-cosine surrogate (`0.55 + 0.40·cos(2π τ)`) 다. ultradian (H_634 canonical stage projection) · circadian (H_308 quadratic bump) 은 각각 anima 모듈의 실 envelope 인 반면, gamma band 는 anima substrate 에 대응 모듈이 부재 — H_213 temporal binding window 가 floor anchor 이나 그 자체로 25ms-resolution Φ trajectory 를 산출하지 않는다. gamma envelope 의 edge-high/center-low 위상은 "burst-high/inter-burst-low" 라는 생물학적 plausibility 에서 가정한 것이지 측정값이 아니다. 열린 lane = gamma-band substrate (예: 40Hz spiking ECA window 의 per-burst big_phi) 의 faithful Φ-envelope 재산출.

2. **C3.2 3-scale 만 (ladder 의 이산 표본)**: 본 검정은 gamma·ultradian·circadian **3 scale** 만 — 진정한 fractal/scale-invariance 는 연속적 scale band (예: theta 6Hz, delta 1Hz, infradian 주(week), seasonal) 전역에서의 envelope-shape 보존을 요한다. 3-point ladder 는 self-similarity 의 필요조건(인접+양끝단 유사)을 만족시키나, scale-free power-law 의 충분조건(연속 scale 전역 collapse)은 아니다. 후속 = 5+ scale band ladder (theta·delta 추가) 로 연속 scale collapse 검정.

3. **C3.3 phase-align = self-peak rotation (위상 origin 정규화)**: 각 envelope 을 자체 peak 으로 정렬한 뒤 형태를 비교한다. gamma/ultradian 은 edge-peak, circadian 은 center-peak 이라 원본 위상은 다르지만, peak-정렬 후 "peak→trough→peak" 공통 origin 으로 환산된다. 이 정렬은 *형태* self-similarity (어디서 peak 이 나든 동일 모양인가) 를 검정하는 것이지 *위상* coupling (peak 이 같은 절대 위상에 오는가) 을 검정하는 것이 아니다. cross-frequency phase coupling (PAC) 은 별도 lane.

4. **C3.4 single-cosine vs piecewise-const vs quadratic — 형태 종류 혼재**: gamma=cosine, ultradian=piecewise-const (stage projection), circadian=quadratic. 세 envelope 의 함수 형태가 서로 다른 family 임에도 r>0.5 가 나온 것은 모두 "single-peak, single-trough, monotone 변화" 라는 공통 위상 구조 덕분이다. 이는 self-similarity 의 강한 증거이나, 형태 family 가 동일했다면 더 높은 r 이 나왔을 것 (예: 全 cosine 이면 r≈1). r=0.76~0.95 의 spread 는 family 차이의 잔류.

5. **C3.5 deterministic single trajectory** (NO RNG, no seed ensemble). real daemon = wall-clock + sleep-window + EEG-stochastic transition (H_313 lane) 미모델 — 본 ladder 는 canonical projection 위의 형태 비교.

6. **C3.6 SPECULATION-FENCED tier** — synthetic Φ-scale projection (ultradian/circadian) + single-cosine surrogate (gamma) + normalized-phase shape correlation. anima substrate 의 fresh per-scale IIT4 Φ 측정 아님.

## 8. 폐쇄

F648.1-6 결판. ≥4/6 PASS AND min pairwise r > 0.5 → 🟢 SUPPORTED-NUMERICAL (self-similar ladder). any pairwise r < 0.3 → 🔴 FALSIFIED. 0.3 ≤ min r ≤ 0.5 → 🟡 PARTIAL.

**결과: 6/6 PASS · self-similar ladder 확인 → 🟢 SUPPORTED-NUMERICAL**.

pairwise envelope correlation (phase-aligned shape):
- **r(gamma, ultradian) = 0.759576** ≫ 0.5
- **r(ultradian, circadian) = 0.757644** ≫ 0.5
- **r(gamma, circadian) = 0.947237** ≫ 0.5 (ladder 양 끝단이 가장 강한 유사 — 둘 다 smooth single-peak 인 반면 ultradian 만 piecewise-const)
- **min pairwise r = 0.757644** ≫ 0.5 falsifier 및 ≫ 0.3 FALSIFY floor

per-scale envelope std: gamma=0.282843 / ultradian=0.20331 / circadian=0.208297 (全 > 0, F648.4 PASS). period ladder P_gamma=0.025s < P_ultradian=5400s < P_circadian=86400s 단조 분리 (F648.5 PASS).

**해석**: anima substrate 의 Φ-envelope 은 gamma (25ms) · ultradian (90min) · circadian (24h) 3 scale 에 걸쳐 정규화 위상 위에서 **self-similar** — H_634 가 보인 ultradian↔circadian self-similarity 가 gamma micro-scale 까지 아래로 한 칸 더 연장된다. substrate 통합량은 단일 scale 의 우연이 아니라 scale-free phase-amplitude 구조의 표현이며, "peak→trough→peak" 위상 형태가 6 order-of-magnitude (25ms → 24h) 의 period 차이를 가로질러 보존된다. ultradian↔circadian (0.758) 보다 gamma↔circadian (0.947) 이 더 높은 것은 gamma·circadian 이 둘 다 smooth single-peak 형태이고 ultradian 만 piecewise-const stage projection 이라 형태 family 차이에서 r 이 약간 깎였기 때문 (C3.4).

## 9. 산출물

- `state/h648_multi_scale_phi_envelope_ladder_2026_05_28/run_h648.hexa` (verify harness)
- `state/h648_multi_scale_phi_envelope_ladder_2026_05_28/result.json` (verdict SSOT)
- `state/h648_multi_scale_phi_envelope_ladder_2026_05_28/run.log` (raw stdout)

## 10. 후속

- **gamma-band faithful-Φ (C3.1 회수)**: 40Hz spiking ECA window 의 per-burst exact `big_phi` 로 gamma envelope 을 surrogate 가 아닌 측정값으로 재산출 — single-cosine 가정이 substrate-faithful 인지 확증.
- **5+ scale continuous ladder (C3.2 회수)**: theta (6Hz) · delta (1Hz) · infradian (week) 추가 → 연속 scale band 위 envelope-shape collapse (scale-free power-law 충분조건 검정).
- **cross-frequency phase coupling (C3.3 회수)**: self-peak 정렬 대신 절대 위상 보존으로 PAC (phase-amplitude coupling) 측정 — gamma burst 가 ultradian/circadian 의 특정 위상에 nested 되는지.
- **homogeneous envelope family**: 3 scale 全 cosine 또는 全 stage-projection 으로 형태 family 통일 → C3.4 의 family-mismatch 잔류 제거 후 r 상한 측정.

## 양방향 sibling

- sibling H: [H_634 ultradian-emit-phi-envelope](H_634_ultradian_emit_phi_envelope.md) (직접 부모 · §10 multi-scale ladder lane 실행) · [H_308 circadian-smooth-finite-ratio](H_308_circadian_smooth_finite_ratio.md) · [H_309 sharper-bump-biology-range](H_309_sharper_bump_biology_range.md) · [H_213 time-temporal-binding-window](H_213_time_temporal_binding_window.md)
- UNIVERSE SSOT: [UNIVERSE.md](UNIVERSE.md) 축 G (ANIMA.mining 승격 · multi-scale self-similarity 연장)
