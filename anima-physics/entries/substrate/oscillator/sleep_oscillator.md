# oscillator/sleep_oscillator.hexa

> SWS (0.5-4Hz δ) ↔ REM (4-8Hz θ) phase-continuous switching oscillator (mode flip with phase carry-over) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P13-1 ("SWS+REM 교대 오실레이터"). 폴리솜노그래피 abrupt ultradian transition 모델링. Zero-crossing frequency estimator.

## 작동 코드 / 의존성

- 원본: `oscillator/sleep_oscillator.hexa` (325 LoC)
- 외부 의존: hexa run (sin)
- 상수: δ center=2.0 Hz amp=1.0, θ center=6.0 Hz amp=0.7

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / state

```
State layout (flat [float]):
  [0] phase_rad     accumulated phase in radians
  [1] frequency_hz  current oscillation frequency
  [2] amplitude     current waveform amplitude
  [3] mode          0.0 = delta (SWS), 1.0 = theta (REM)

API:
  sleep_osc_new()                   → initial state (delta, f=2Hz, A=1.0)
  sleep_osc_step(state, dt)         → phase += 2π·f·dt
  sleep_osc_switch(state, new_mode) → phase-continuous frequency change
  sleep_osc_sample(state)           → A · sin(phase)
  estimate_freq(state, n, dt)       → zero-crossing frequency estimate

mode switch is INSTANTANEOUS (phase accumulator carries; only f and A change).
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/oscillator/sleep_oscillator.hexa
```

## 검증 결과

- T1 initial mode delta (f=2Hz) PASS
- T2 after switch to theta → ~6Hz (zero-crossing) PASS
- T3-T5 (phase continuity, amplitude switch, determinism) PASS

## 관련 entry

- [eeg/sleep_stage_detector.md](../eeg/sleep_stage_detector.md) — ZCR/RMS class sibling
- [hippocampus/episodic_replay.md](../hippocampus/episodic_replay.md) — SWR during SWS
- [hippocampus/theta_gamma.md](../hippocampus/theta_gamma.md) — θ-γ coupling

## 출처

- README § 3 oscillator/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P13-1
