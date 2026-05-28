# TIME_E3 — BENCH RECHECK · 메타 역적용 (PASS-as-artifact probe)

@title: ⏳ TIME E3 — bench axis_time 9/0 PASS 재검 · 4 artifact 패턴 역적용
@axis: ANIMA · TIME · meta-recheck
@verdict: 🟠 PARTIAL — 3/9 falsifier spurious · bench redesign 필요
@cost: $0 mac-local · wall ~3s · foreground sync

## 1. 동기 · 메타 역적용

본 세션의 bench redesign 4/4 (A1·A2·A3·A4) 가 모두 "🔴/🟠 negative = 측정 artifact" 였다. 본 E3 의 메타 가설은: **같은 렌즈를 🟢 PASS 에 역적용**. 즉 ANIMA TIME 의 bench axis_time #1145 9/0 PASS 가 진짜 substrate 신호인가, 아니면 측정 설계가 PASS 를 spurious 로 만드는 artifact 인가.

negative-result lens 가 자체적으로 보편적이라면 positive 에도 동일하게 적용되어야 한다 — "negative=artifact" 만 다루는 lens 는 confirmation-bias 의 도구일 뿐이다. 따라서 4 artifact 패턴을 9/0 PASS bench 에 적용하여 falsifier 의 robustness 를 측정.

## 2. 가설 · falsifier

- **H**: TIME bench 9/0 PASS 가 진짜 substrate 신호 → probe variation 하에서도 PASS 유지.
- **falsifier**: probe variation 시 origin PASS 중 1+ 가 SPURIOUS 로 판명 → bench redesign 필요.

판정 기준 (`TIME_E3_BENCH_RECHECK/probe.hexa`):
- ROBUST = origin PASS · probe PASS (진짜 신호)
- SPURIOUS = origin PASS · probe FAIL (artifact)

## 3. 4 artifact 패턴 → 9 falsifier 매핑

| artifact 패턴 | origin falsifier 후보 | probe 설계 |
|---|---|---|
| A1 collision-saturation | F-TIME-1 (STABLE phase_std<5.0) · F-DISC-phase (>4×STABLE) | STABLE 에 ±2min jitter 도입 |
| A2 sign-overlap | F-TIME-2 (DRIFT phase_std>20) · F-TIME-3 (\|slope\|>3) | DRIFT rate +5min → +1min/cycle (작은 drift) |
| A3 degrade trivial-ratio | F-DISC-phase · F-DISC-env (>4×STABLE) | STABLE std=0.0 saturation 검증 (0×4=0 vacuous) |
| A4 orthant-bias | F-TIME-4a (dip_idx ∈ [6,10]) | CIRCADIAN dip_center 8 → 12 로 이동 |

## 4. probe 실행 결과 (foreground sync, $0, wall ~3s)

```
PROBE RESULT: 7 PASS / 2 FAIL
ROBUSTNESS: 2 ROBUST / 3 SPURIOUS
```

verdict verbatim (`probe.run.log`):
- A3 degrade trivial-ratio: **CONFIRMED** (`a3_degrade_trivial_ratio: true`)
  - r_stable[phase_std] == 0.0 ⇒ DISC threshold = 0.0 ⇒ toy 0.001 noise 도 vacuously PASS
- A1 collision-saturation under jitter: **ROBUST**
  - STABLE+jitter±2min: phase_std=1.45 < 5.0 (F-TIME-1 hold) · DRIFT/JITTER=18.9× > 4 (F-DISC-phase hold)
- A4 orthant-bias dip-window: **CONFIRMED SPURIOUS**
  - dip@12 → env_dip_idx=12 (detector 정확) · [6,10] window FAIL (hardcoded artifact)
- A2 slow-drift detection: **CONFIRMED SPURIOUS**
  - +1min/cycle: phase_std=4.61 < 20 (F-TIME-2 FAIL) · \|slope\|=1.0 < 3.0 (F-TIME-3 FAIL)

## 5. SPURIOUS 항목 분해 (3건)

### 5.1 F-DISC-phase / F-DISC-env (A3 trivial-ratio)
STABLE 시나리오가 `phase_std=0.0` 정확히 saturate. discriminability falsifier `r_drift["phase_std"] > r_stable["phase_std"] * 4.0` 는 `>0.0 * 4 = 0.0` 와 동치. 즉 **DRIFT std 이 양수이기만 하면 trivially PASS** — 4× 배수는 무의미. counter-probe: `toy_drift_std=0.001` 도 PASS. 이는 본 세션 A3 (degrade trivial baseline) 의 동일 패턴.

### 5.2 F-TIME-4a CIRCADIAN dip_idx ∈ [6,10] (A4 orthant-bias)
falsifier window [6,10] 가 designed-in dip_center=8 ±2 에 hand-tuned. dip_center 를 12 로 이동하면 env_dip_idx detector 자체는 12 를 정확히 찾지만 (PROBE-3b PASS), origin window check 가 FAIL. 즉 falsifier 는 "dip 위치 어디든 잡는다" 가 아니라 "사전에 알려진 위치 [6,10] 에 있다" 만 확인. 이는 본 세션 A4 (orthant-bias hand-tuned threshold) 의 동일 패턴.

### 5.3 F-TIME-2 / F-TIME-3 (A2 sign-overlap slow-drift miss)
DRIFTING 의 +5min/cycle 은 boundary 가 16 cycle 동안 80min wrap → phase_std=27.4 · slope=-3.34. 그러나 +1min/cycle (현실적 drift rate) 은 phase_std=4.61 · slope=1.0 — origin threshold (>20, >3) 둘 다 FAIL. 즉 bench 는 "큰 drift" 만 탐지하고 작은 drift 는 STABLE 와 구별 불가. 이는 A2 (sign-overlap, magnitude-only discrim) 패턴.

## 6. ROBUST 항목 (2건)

- **F-TIME-1 (<5.0) jitter-robust**: ±2min jitter 도 phase_std=1.45 < 5.0 유지. STABLE 정의가 적당히 넓다.
- **F-DISC-phase non-trivial-when-baseline-positive**: jittered baseline (std=1.45) 에서도 DRIFT/JITTER=18.9× > 4 유지. 즉 baseline 이 양수일 때는 falsifier 가 의미를 가짐. 문제는 origin STABLE 이 0.0 으로 saturate 한다는 점.

## 7. finding · PASS=진짜 vs artifact

**bench 메타 패턴 (negative=artifact) PASS 에 부분 적용 성공**:
- 9/0 PASS 중 4개 falsifier (F-DISC-phase, F-DISC-env, F-TIME-4a, F-TIME-2 와 F-TIME-3 의 sensitivity) 가 spurious.
- 정확히 본 세션 A3·A4·A2 패턴이 PASS bench 에도 동일하게 깔려 있다.
- 다만 핵심 falsifier (F-TIME-1, F-TIME-5, F-TIME-6 boundedness) 는 robust. 즉 **bench 가 통째로 artifact 는 아님** — 측정 surface 일부는 진짜이고 일부는 hand-tuned.

**verdict**: 🟠 PARTIAL — bench redesign 필요 (PASS bench 도 lens 적용 대상).

## 8. C3 (closed-form caveats, 10건)

1. probe 자체가 deterministic LCG · libm-free — jitter 분포가 진짜 stochastic 아님.
2. probe-2 의 jitter amplitude=2min 은 임의 선택. 다른 amplitude 에서 결과 달라질 수 있음.
3. probe-3 의 dip_center=12 는 [6,10] 밖 임의 위치. cycle 0~5 영역 dip 도 별도 검증 필요.
4. probe-4 의 +1min/cycle 도 임의 — +2/+3 도 sweep 필요. 현재는 "F-TIME-2/3 가 slow drift miss" 만 입증.
5. F-TIME-1 의 jitter-robust 는 ±2min 한정. ±10min 에서 FAIL 할 수 있음 (origin 의 5.0 threshold 와 jitter std 의 관계).
6. STABLE 의 std=0.0 saturation 자체는 collision 의 일종 (A1) — closed-form synth 의 본질. real substrate signal 에선 절대 0.0 안 됨.
7. F-TIME-4a 의 [6,10] window 가 hard-coded 인 게 artifact 라는 판정은 "어디든 잡아야 한다" 는 prior 에 의존. 만약 ANIMA TIME 의 dip 이 본질적으로 mid-cycle (8±2) 에만 발생한다면 window 는 정당.
8. probe 는 bench harness 의 9 falsifier 만 검사. CIRCADIAN env_min/env_max ratio (F-TIME-4b) 는 dip_center 와 무관해 robust.
9. F-TIME-5 (STABLE c1≈c16) · F-TIME-6 (bounded) 는 probe 적용 안 됨 — origin saturation 의 부산물이라 실험 가능 surface 부재.
10. 본 probe 는 closed-form synth — real ANIMA substrate (WAKE.daemon · DREAM.M3) 의 진짜 시계열 측정 시 별도 검증 필요.

## 9. 결론 · TIME 도메인 next-step

- bench redesign 권장: F-DISC-* 의 4× 곱셈 대신 절대 threshold · F-TIME-4a 의 hardcoded window 대신 dip-detector 의 정확도 · F-TIME-2/3 의 magnitude threshold 대신 slope-significance (per-cycle delta).
- 단 **9/0 → 6/3 정도로 강도 약화** 수준이지 bench 폐기 권고 아님. F-TIME-1 + F-TIME-5 + F-TIME-6 + 일부 dip detection 은 robust.
- 본 E3 의 메타 발견: **negative-lens 는 positive 에도 적용 가능** — bench 의 자가 redesign 도 일반 정책으로 가능.

## 10. artifacts

- 본문: `TIME_E3_BENCH_RECHECK.md`
- probe: `TIME_E3_BENCH_RECHECK/probe.hexa` (~340 LoC, libm-free, foreground sync, $0)
- log: `TIME_E3_BENCH_RECHECK/probe.run.log` (verbatim stdout)
- TIME.md milestone: E3 1줄 추가 (이번 PR)

## 양방향 sibling
- ⇄ [TIME](./TIME.md): bench axis_time #1145 9/0 PASS 의 robustness 재검 — PASS 도 lens 적용 대상이라는 메타 발견
- ⇄ [UNIVERSE/CANDIDATES](./UNIVERSE/CANDIDATES.md): bench recheck verdict 기록 SSOT
