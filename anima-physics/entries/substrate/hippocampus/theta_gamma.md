# hippocampus/theta_gamma.hexa

> Tort 2010 modulation index for hippocampal θ-γ phase-amplitude coupling (6Hz θ × 40Hz γ, N_BINS=18, MI=(log N − H(P))/log N) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P6-2 ("theta-gamma coupling — 해마 scale-free 시간 코딩"). Buzsáki 2010 + Lisman & Jensen 2013 + Tort et al. 2010 reference. Husserlian retention/protention substrate (specious-present ~150ms).

## 작동 코드 / 의존성

- 원본: `hippocampus/theta_gamma.hexa` (527 LoC)
- 외부 의존: hexa run (cos/sin, log 내장)
- API: `compute_pac(lfp: [float], sr: float) -> float` → MI ∈ [0, 1]
- 상수: N_BINS=18 (Tort standard)

## 비용 / 리소스

- $0 Mac local · ESP32/STM32 호환 (no FFT, Hilbert single-freq quadrature)

## 핵심 흐름 / ASCII

```
Synthetic LFP generator:
  x(t) = A_θ · cos(2π·f_θ·t)                                 (theta carrier @ 6 Hz)
       + A_γ · (1 + m · cos(2π·f_θ·t)) · cos(2π·f_γ·t)       (amp-mod gamma @ 40 Hz)
       + A_noise · pseudo_random(t)                          (broadband)
  m ∈ [0, 1] = modulation depth (0=no coupling, 1=full PAC)

Modulation Index (Tort 2010):
  1. Split theta phase into N_BINS=18 uniform bins
  2. For each bin: mean gamma-band amplitude envelope
  3. Normalize N_BINS means to probability P
  4. MI = (log(N) − H(P)) / log(N)        ∈ [0, 1]
     0 = uniform (no coupling)
     1 = perfectly locked
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/hippocampus/theta_gamma.hexa
```

## 검증 결과

- T1 fully-coupled LFP (m=1) → MI > 0.2 PASS
- T2 uncoupled LFP (m=0) → MI < 0.05 PASS
- T3-T5 (deterministic / N_BINS=18 standard / monotonicity in m) PASS

## 관련 entry

- [hippocampus/episodic_replay.md](./episodic_replay.md)
- [eeg/mu_rhythm_detector.md](../eeg/mu_rhythm_detector.md) — sibling EEG signal detector (Goertzel)
- [oscillator/sleep_oscillator.md](../oscillator/sleep_oscillator.md) — δ/θ phase oscillator

## 출처

- README § 3 hippocampus/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P6-2
