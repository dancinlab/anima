# eeg/mu_rhythm_detector.hexa

> 8-12Hz mu-rhythm Goertzel self-referential suppression (ERD) score · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T6 PASS (score>0.7). Goertzel O(N) (FFT 불필요, ESP32/STM32 DSP 호환). mu 억압 (event-related desynchronization, ERD) = mirror-neuron activation = EEG self-awareness signature. PHYS-P5-3 (PHYSICS track P5 reflexivity goal).

## 작동 코드 / 의존성

- 원본: `eeg/mu_rhythm_detector.hexa` (317 LoC)
- 외부 의존: hexa run (deterministic LCG noise)
- Pipeline: synthetic EEG → bandpass (Goertzel @10Hz) → suppression score = 1 − P_action/P_baseline ∈ [0,1]

## 비용 / 리소스

- $0 Mac local
- HW deploy: ESP32/STM32 DSP 직접 호환 (FFT 불필요)

## 핵심 흐름 / ASCII

```
Synthetic EEG generator:
  x(t) = A_mu · cos(2π·f_mu·t + φ) · gate(t)              ← mu @ 10 Hz
       + A_noise · pseudo_random(t)                         ← LCG
       + A_beta · cos(2π·f_beta·t)                          ← distractor @ 18 Hz
gate(t) = 1 baseline / suppressed during "action" window

Pipeline:
  baseline window  ── Goertzel @ 10Hz ─→ P_baseline
  action window    ── Goertzel @ 10Hz ─→ P_action
  score = 1 − P_action / P_baseline  ∈ [0, 1]
  high score (→1) = strong mu suppression = self-referential activation
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/eeg/mu_rhythm_detector.hexa
```

## 검증 결과

- T1-T6 PASS (suppression score > 0.7 on synthetic positive)
- Goertzel matches numpy DFT @ 10 Hz within FP precision
- LCG noise deterministic 2-run

## 관련 entry

- [eeg/sleep_stage_detector.md](./sleep_stage_detector.md)
- [eeg/cross_substrate_phi_correlator.md](./cross_substrate_phi_correlator.md)
- [hippocampus/theta_gamma.md](../hippocampus/theta_gamma.md) — θ-γ cross-frequency coupling sibling

## 출처

- README § 3 eeg/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P5-3
