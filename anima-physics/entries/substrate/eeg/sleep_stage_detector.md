# eeg/sleep_stage_detector.hexa

> ZCR + RMS feature → Awake / SWS / REM 3-class sleep stage classifier · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T4 PASS (accuracy >0.8 on 30 mixed synthetic trials). 단순 ZCR (zero-crossing rate) + RMS (amplitude) rule-based. PHYS-P13-2 (K-complex / spindle 추가는 별 cycle).

## 작동 코드 / 의존성

- 원본: `eeg/sleep_stage_detector.hexa` (365 LoC)
- 외부 의존: hexa run (deterministic LCG)
- Pipeline: synthetic EEG → ZCR + RMS per window → rule-based class

## 비용 / 리소스

- $0 Mac local · ESP32 호환 (no FFT)

## 핵심 흐름 / ASCII

```
Synthetic EEG (deterministic LCG noise):
  Awake: 15 Hz + noise (beta/alpha)        moderate amplitude
  SWS:    2 Hz + noise (delta band)        HIGH amplitude
  REM:    6 Hz + noise (theta band)        LOW amplitude

Feature per window:
  f1 = ZCR (zero-crossing rate) — proxy for dominant freq
  f2 = RMS (root-mean-square)   — amplitude

Rules:
  Awake : ZCR > threshold_high · moderate amp
  SWS   : ZCR < threshold_low  · HIGH amp (delta)
  REM   : medium ZCR           · LOW amp (theta + desync)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/eeg/sleep_stage_detector.hexa
```

## 검증 결과

- T1 Awake → stage 0 PASS
- T2 SWS → stage 1 PASS
- T3 REM → stage 2 PASS
- T4 Accuracy > 0.8 on 30 mixed trials (10 per stage) PASS
- T5 Determinism 2-call same output PASS

## 관련 entry

- [oscillator/sleep_oscillator.md](../oscillator/sleep_oscillator.md) — SWS↔REM phase-continuous oscillator
- [eeg/mu_rhythm_detector.md](./mu_rhythm_detector.md) — sibling EEG signal detector

## 출처

- README § 3 eeg/
- shared/roadmaps/anima.json PHYS-P13-2
