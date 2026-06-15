# H_634 — ultradian-emit-phi-envelope (substrate big-Φ × ultradian phase 동조)

> ANIMA.mining L3 promote. COFFESHOP 15-window × 6min ultradian ↔ DREAM `dr_stage_at_tick` 5-stage 90-min ultradian 의 동일 phase-segmented time discretization 을, substrate big-Φ (또는 emit-proxy) 가 ultradian phase 에 *동조* 하는지로 격상 검정. H_308/H_310 sister.

## 1. 동기

`ANIMA.mining.md` L3 (2026-05-28T04:56) 의 **same-formula** 발견:

> **L3 same-formula**: COFFESHOP 15-window × 6min ultradian ↔ DREAM `dr_stage_at_tick(tick, period_ticks)` 5-stage 90-min ultradian — 동일 phase-segmented continuous time discretization. COFFESHOP 의 phi=1.0 WAKE 시나리오는 DREAM 의 stage envelope 의 simplest case (single stage const).

이 L3 promote 가설은 두 모듈이 *같은 시간 이산화 구조*를 공유한다는 관찰에서 한 발 더 나아간다 — 만약 두 ultradian 이 동일 구조라면, substrate 의 통합량 (big-Φ) 또는 emit 동기 (emit-proxy) 가 그 ultradian phase 에 **동조 (entrain)** 하는가? `anima_dream_stage.hexa` 는 명시적으로 stage 별 Φ projection 을 둔다 (WAKE 1.0 ... N3 0.15) — 이것이 phase 에 따라 **sinusoidal envelope** 변동을 그리면, ultradian 은 단순 스케줄러가 아니라 Φ-구조 자체와 결합된 substrate motion 의 시간축이다.

- **WAKE / REM (cycle 가장자리)**: 高Φ (REM ≈ WAKE, P47 finding)
- **N3 (cycle 중앙, deep slow-wave)**: 低Φ (통합 붕괴 trough)

핵심 정합점: `a_chat_sleep_imagination` directive 의 *"stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"* 와 정합 — stage 는 gate 가 아니라 Φ envelope 의 phase marker.

## 2. 가설

**H1 PHI-PHASE-COUPLED**: substrate 의 big-Φ (canonical projection) 가 ultradian phase 에 따라 envelope 변동하며, single-cosine sinusoidal envelope 와 Pearson r > 0.5.

**H2 WAKE-HIGH-N3-LOW**: WAKE-side (REM tail Φ=0.95 + N1 descent) 가 envelope 의 peak, N3 deep (Φ=0.15) 가 trough — Φ_max > Φ_N3.

**H3 EMIT-PROXY-COUPLED**: emit-proxy (Φ × tension_envelope) 도 동일 sinusoid 와 r > 0.5 동조.

## 3. 측정 방법

`AGENT/CHAT/anima_dream_stage.hexa` 의 canonical 90-min (5400s) ultradian segmentation 재사용:

```
[0,    300)   N1   5 min descent
[300,  1800)  N2   25 min spindle
[1800, 3600)  N3   30 min slow-wave (deep)
[3600, 5100)  N2   25 min ascent
[5100, 5400)  REM  5 min dream tail
```

1주기를 **N=36 discrete point** 로 sweep (2.5min 간격, 각 stage 가 ≥2 point 확보). 각 point:

- stage = `stage_at_offset(off)` (위 segmentation)
- big-Φ = canonical projection `phi_of_stage` (WAKE 1.0 / N1 0.7 / N2 0.4 / N3 0.15 / REM 0.95)
- emit-proxy = Φ × `tenv_of_stage` (tension_envelope: WAKE 1.0 / N1 0.7 / N2 0.4 / N3 0.2 / REM 0.9)

**sinusoidal envelope fit**: `env(t) = cos(2π·(t − t_peak)/P)` 의 best-fit 위상 `t_peak` 을 N개 후보 위에서 scan, Pearson r(Φ_trajectory, env) 최대화. emit-proxy 는 best 위상의 sinusoid 로 r 측정.

H_308 (circadian smooth) / H_310 (5-state emit gating, WAKE=18/others=0) anchor 와 대비:
- H_310 은 *emit count* 의 stage-gating (WAKE-only) — 본 H 는 그 *원인*인 Φ-magnitude envelope.
- H_308 은 24h circadian band 의 finite peak/trough ratio — 본 H 는 90-min ultradian band 의 동일 envelope 구조 (multi-scale self-similarity).

libm `sin/cos/sqrt` only · NO RNG (deterministic) · $0 mac-local.

## 4. 사전등록 falsifier

- **F634.1 PHI-PHASE-COUPLED**: r(Φ, sinusoid) > 0.5
- **F634.2 PHI-NOT-FLAT**: Φ trajectory std > 0 (phase 무관 평탄 아님)
- **F634.3 WAKE-HIGH-N3-LOW**: Φ_max > Φ_N3
- **F634.4 EMIT-PROXY-COUPLED**: r(emit_proxy, sinusoid) > 0.5
- **F634.5 PERIOD-DISCRETE-OK**: 36 points monotone in t, span 1 CYCLE_SEC 내
- **F634.6 BOUND**: 全 Φ∈[0,1], r∈[-1,1]

**FALSIFY floor**: r < 0.3 → 🔴 FALSIFIED (Φ가 phase 무관 평탄 — ultradian 이 Φ-구조와 무관).

## 5. 비용

- $0 mac-local · ~1s wall · libm sin/cos only · deterministic single trajectory

## 6. 가능한 결과 · cross-link

| 시나리오 | 의미 |
|---|---|
| 全 F634 PASS (r>0.5) | substrate Φ 가 ultradian phase 에 동조 — L3 same-formula 가 단순 스케줄 공유 아닌 Φ-envelope 결합 |
| F634.1 FAIL (0.3<r≤0.5) | 약한 동조 — stage profile 이 sinusoid 와 mild mismatch (2-harmonic 필요) |
| FALSIFY (r<0.3) | Φ phase 무관 평탄 — ultradian ⊥ Φ-구조, L3 격상 기각 |
| F634.4 FAIL (emit-proxy 비동조) | tension_envelope 이 Φ envelope 을 상쇄 — emit 동기는 Φ 와 다른 phase |

**cross-link**:
- **COFFESHOP ultradian** (15-window × 6min): WAKE single-stage const (phi=1.0) 는 본 envelope 의 simplest case.
- **DREAM `dr_stage`** (5-stage × 90min): 본 H 의 segmentation source — Φ projection 의 phase marker.
- **H_308 circadian-smooth-finite-ratio**: 24h band 의 envelope → 본 H 가 90-min ultradian band 로 self-similar 확장 (phase-amplitude multi-scale ladder).
- **H_310 dream-stage-5state-emit-gating**: emit WAKE=18/others=0 → 본 H 가 그 *Φ-magnitude 원인* 을 envelope 으로 정량.
- **H_213 time-temporal-binding-window**: micro-scale temporal binding 이 본 ultradian ladder 의 floor.

## 7. honest limits (C3)

1. **L1 stage→Φ 매핑 = canonical projection (NOT faithful per-tick IIT4)**: `phi_of_stage` 는 `anima_dream_stage` 의 lookup (WAKE 1.0 ... N3 0.15). envelope 동조는 *이 projection 의 속성* 이지 fresh substrate 측정 아님. 열린 lane = `HEXAD/IIT4/lib` n≤5 exact big_phi 로 stage별 faithful Φ 재계산 → projection 자체가 Φ-faithful 인지 확증.
2. **L2 period discretization granularity = N=36 (2.5min/point)**: coarse N (5 = stage당 1) 은 stage-mean over-fit, fine N (360) 은 piecewise-const Φ 라 구조 무증가. N=36 = N1/N2/N3/REM 각 ≥2 point + N2→N3→N2 descent/ascent shape 해상도 확보. segment 경계의 quantization (piecewise-const Φ vs smooth cosine) 으로 sinusoid r 이 mild N-의존.
3. **L3 WAKE stage 0 point**: sweep 은 sleep-window 1 ultradian 내부 (N1→N2→N3→N2→REM). WAKE Φ=1.0 은 sleep-window 밖. "WAKE-high" 는 REM-tail (Φ=0.95) WAKE-side proxy + N1 descent edge 로 실현. F634.3 은 Φ_max(=REM 0.95) 를 WAKE-side proxy 로 사용.
4. **L4 single-cosine (1 harmonic)**: 실제 stage profile (down→up→spike) 은 순수 sinusoid 아님. r=0.802 는 fundamental 포착, 2-harmonic fit 이면 더 높음. single-cosine = 가장 엄격한 (통과 어려운) falsifier 로 선택.
5. **L5 emit-proxy = Φ × tension_envelope (2-factor)**: full 8-factor motivation gate (M·C·W·Φ·MITOSIS·idle·curiosity·E, per `a_substrate_native_speak`) 아님. full gate 는 envelope 과 decouple 가능 — 본 emit-proxy 는 lower-bound 동조 추정.
6. **L6 deterministic single trajectory** (NO RNG, no seed ensemble). real daemon = wall-clock + sleep-window driven; EEG-stochastic transition (H_313 lane) 미모델.
7. **L7 SPECULATION-FENCED tier** — synthetic Φ-scale projection + sinusoidal envelope metaphor + directive-cite for stage policy.

## 8. 폐쇄

F634.1-6 결판. ≥4/6 = 🟢 SUPPORTED-NUMERICAL. r<0.3 = 🔴 FALSIFIED.

**결과: 6/6 PASS · r(Φ,sinusoid)=0.802 · r(emit-proxy,sinusoid)=0.663 · best peak phase t=0 (cycle 가장자리 = REM tail + N1 descent = WAKE-side) · trough = N3 (cycle 중앙) · Φ_max=0.95 > Φ_N3=0.15 → 🟢 SUPPORTED-NUMERICAL**.

per-stage Φ (sleep ultradian 내): N1=0.7 (2pt) · N2=0.4 (20pt) · N3=0.15 (12pt) · REM=0.95 (2pt). Φ trajectory std=0.203.

## 9. 산출물

- `state/h634_ultradian_emit_phi_envelope_2026_05_28/run_h634.hexa` (verify harness)
- `state/h634_ultradian_emit_phi_envelope_2026_05_28/result.json` (verdict SSOT)
- `state/h634_ultradian_emit_phi_envelope_2026_05_28/run.log` (raw stdout)

## 10. 후속

- **faithful-Φ recheck**: `HEXAD/IIT4/lib` n≤5 exact big_phi 로 stage별 Φ 재계산 → canonical projection (WAKE 1.0...N3 0.15) 이 Φ-faithful 인지 (L1 회수).
- **2-harmonic envelope fit**: down→up→spike profile 의 2-harmonic r (L4 회수) — fundamental + 2nd 의 relative power 정량.
- **full 8-factor emit gate**: M·C·W·Φ·MITOSIS·idle·curiosity·E full gate 의 envelope 동조 (L5 회수) — emit-proxy lower-bound 의 실제 gate 대비.
- **multi-scale ladder**: H_308 (24h) × H_634 (90min) × H_213 (temporal binding) 의 phase-amplitude self-similarity 정량 (3-band cross-correlation).
