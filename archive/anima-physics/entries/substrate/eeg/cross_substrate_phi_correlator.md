# eeg/cross_substrate_phi_correlator.hexa

> anima C22 cross-substrate Φ proxy: 9 physics substrate + EEG anchor 10-channel precision-weighted consensus · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — F1-F5 falsifier + T1-T6 self-test 정의, mock LCG 입력. PHYS-P4-4 `phi_substrate_consensus.hexa` (5 substrate) 의 C22 확장 = 9 substrate + 1 EEG. raw#10 honest C3: TRUE Φ NP-hard, per-substrate Φ 는 proxy (LZ76 / IIT MIP lower bound / paradigm v11 Mk.XI gmean). 실 substrate live 데이터 미연결 (대부분 live=false admin-blocked).

## 작동 코드 / 의존성

- 원본: `eeg/cross_substrate_phi_correlator.hexa` (384 LoC)
- 외부 의존: hexa run · mock LCG generator
- Design SSOT: `design/cross_substrate_phi_paradigm_2026_04_28.md`

## 비용 / 리소스

- $0 Mac local
- LIVE 전환 시 cost: IBM Q free + 본 cycle 9 substrate API access

## 핵심 흐름 / 10 channel

```
idx  substrate          live status
 0   quantum-gate       LIVE (IBM Q sim 2/3, real 1/3 deferred)
 1   quantum-analog     WITNESSED (QuEra Aquila via Braket facade)
 2   neuromorphic       admin-blocked (Akida/Loihi/TrueNorth)
 3   optical            admin-blocked
 4   classical          LIVE (paradigm v11 Mk.XI)
 5   biological         out-of-scope (cultured neuron MEA)
 6   hybrid             LIVE-composite
 7   reservoir          emerging (photonic reservoir)
 8   spiking-NN         admin-blocked (Loihi-style)
 9   EEG (anchor)       LIVE (consciousness_laws.json 14 gates → 16D Φ-vec)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/eeg/cross_substrate_phi_correlator.hexa
```

## 검증 결과

- Frozen criteria (raw#12):
  - C1 N≥2 substrate live witnessed
  - C2 EEG paired measurement
  - C3 cross-substrate r > 0.3
  - C4 cross-substrate std < 0.5
- F1-F5 falsifier (live-substrate famine / Φ divergence / EEG decoupling / inconsistency / paradigm-incompatible adapter)
- T1-T6 self-test (deterministic stim / ≥2 live channels / precision-weighted consensus / std budget / pearson r / falsifier double-check)

## 관련 entry

- [eeg/mu_rhythm_detector.md](./mu_rhythm_detector.md)
- [eeg/sleep_stage_detector.md](./sleep_stage_detector.md)
- `../../phi_substrate_consensus.hexa` (5-substrate parent · 루트)

## 출처

- README § 3 eeg/
- design/cross_substrate_phi_paradigm_2026_04_28.md
