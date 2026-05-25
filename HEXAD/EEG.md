# HEXAD/EEG.md — EEG 가설 보류 ledger (나중에 체크)

> User directive 2026-05-16: "HEXAD/EEG.md 로 남겨놔줘 EEG 는 나중에 체크하자".
> EEG-dependent 가설은 anima-eeg-core **하드웨어 의존** — $ 으로 해결 불가
> (cloud GPU 와 다름; 실제 EEG 측정 장비 + 피험자 필요). 보류, 추후 체크.

## 보류 대상 (DEFERRED — hardware blocker)

| ID | 한 줄 | blocker | 파일 |
|----|-------|---------|------|
| **H_013** | longitudinal EEG 5-axis (장기 EEG 추적, anima 5-axis ↔ EEG 정합) | anima-eeg-core 하드웨어 + 장기 피험자 recording | `hypotheses_legacy_2026_05_15/H_013_longitudinal_eeg_5axis.md` |
| **H_014** | CLM EEG LZ76 (Lempel-Ziv 복잡도 ↔ CLM 의식 proxy) | anima-eeg-core 하드웨어 EEG | `hypotheses_legacy_2026_05_15/H_014_clm_eeg_lz76.md` |
| **H_015** | CLM EEG gamma-theta (감마-세타 결합 ↔ CLM) | anima-eeg-core 하드웨어 EEG | `hypotheses_legacy_2026_05_15/H_015_clm_eeg_gamma_theta.md` |

## 왜 $ 으로 안 되나 (honest)

GPU sweep ($200-600) 와 **근본적으로 다름**: EEG 가설은 cloud compute 가 아니라
**물리적 EEG 측정 장비 (anima-eeg-core) + 인간/생체 피험자 + 시간(longitudinal)**
이 필요. AGENTS.tape g3 — 측정 없이 verdict 날조 금지. faking 불가.

## 부분 $0 path (추후 체크 시 고려 — anima-internal surrogate)

EEG 가설 자체는 hardware-blocked 이나, 일부 *알고리즘* 은 anima 자체 substrate
에 적용 가능 ($0, anima-internal — 외부 데이터 불요):

- **LZ76 (H_014)**: Lempel-Ziv 76 복잡도는 anima substrate 의 perturbation
  response 시퀀스에 직접 계산 가능 (deterministic, $0). 단 이는 "anima-internal
  LZ proxy" 이지 "EEG cross-validation" 이 아님 — H_014 의 EEG anchor 는 여전히
  hardware-blocked. surrogate ≠ 가설 본 claim (정직 분리).
- **gamma-theta (H_015)**: anima cell-pool oscillation 의 spectral 분석은 $0
  가능하나, 동일하게 "EEG cross-validation" 부분은 hardware 필요.

→ 추후 EEG 체크 시: (a) anima-internal surrogate ($0, 가능) 와 (b) 실제 EEG
hardware cross-validation (anima-eeg-core 필요, blocked) 을 **정직하게 분리**
하여 (a) 만 closed-form/formal 산입, (b) 는 DEFERRED 유지.

## cross-link

- `HEXAD/INDEX.md` §DEFERRED entries (H_013/014/015) — 이 파일이 상세 ledger
- `state/verify_hypotheses_pending_2026_05_16/hypo_coverage.json` — `type: hardware`
- AGENTS.tape g3 (real-limit anchor — 측정 없이 verdict 금지)
- 관련: H_188 PCI clinical (external clinical data — 별개 blocker, `HEXAD/INDEX.md`)

> **상태**: 보류 (deferred). EEG 하드웨어 cycle 은 나중에. 이 파일이 추적 anchor.
