# BRAIN/eeg — 아키텍처 (M0)

OpenBCI 16ch EEG → IIT 4.0 big-Φ 파이프라인 설계. PR #547 (`eeg_to_tpm.hexa` + `eeg_iit4_demo.hexa`) 의 후속이며, 본 문서는 M1 합성 데모 / M2 라이브 발사를 위한 단일 SSOT 다.

## §1 스택 개요

```
[OpenBCI Cyton+Daisy 16ch · 250 Hz]
        │  (USB dongle / WiFi shield)
        ▼
[LSL stream "OpenBCI_EEG" · float32 · 16 × n_samp]   ← M2 라이브 경로
        │
        ▼
[16ch → n≤8 차원축소  (region-collapse · 본 PR 채택)]
        │
        ▼
[BRAIN/eeg/eeg_to_tpm.hexa  (어댑터)]
  · eeg_binarize      : 채널별 mean 임계
  · eeg_state_at      : Σ_ch bit·2^ch (n_ch ≤ 8)
  · eeg_estimate_tpm  : 빈도-추정 state-by-node TPM
  · eeg_big_phi       : 어댑터 → 엔진 호출
        │
        ▼
[stdlib/consciousness/iit4_bigphi.hexa  (엔진, substrate-agnostic)]
        │
        ▼
[big-Φ 결과 — [big_phi, total, sum_phi_d, sum_phi_r, n_distinctions]]
```

엔진 ⊥ 어댑터 원칙 (hexa-lang commons @D g61) — 동일 stdlib IIT4 엔진을 anima(ECA substrate)와 BRAIN(EEG substrate)가 공유한다. EEG-특화 가공은 어댑터에 머문다.

## §2 16ch → n≤8 차원축소 전략

IIT4 엔진은 n ≤ 8 에서 exact (M9 tractability), n=7 까지 bounded mode 확인 (LIFE/H_242). 16ch 입력은 엔진에 직접 못 넣는다. 두 후보 중 하나를 선택해야 한다.

| 전략 | 입력 | 출력 | 장점 | 단점 |
|---|---|---|---|---|
| **A. region-collapse** (채택) | 16ch | 8 region (2ch / region) | 채널 손실 없음 · 해부학적 의미 (frontal/parietal/temporal/occipital × L/R) · 단일 big-Φ | region 간 미세 동기 손실 · pairing 디자인 선택 필요 |
| **B. PCA top-8** | 16ch | 8 PC component | 정보-이론 최적 8축 | 비-해부학적 · PC 회전 결정성 의문 · stdlib 외 의존 (선형대수) |
| **C. 8-electrode subset** | 16ch | 8ch (절반 폐기) | 단순 · 즉시 호환 | 절반 정보 폐기 · 부위 편향 |

**채택 = A (region-collapse).** M1 데모는 4ch → 1 region (단순 평균 후 mean-threshold binarize) 의 **4-region** 표현 (frontal/central/parietal/occipital). 8-region (2ch/region) 는 IIT4 n=8 exact 가 inline 실행 budget 초과 (HEXAD/IIT4/state/iit4_m12_bounded_largen 보고 n=6 already minutes) — M3 에서 stdlib `big_phi_bounded` (lower-bound approx) 로 측정 예정. PCA 는 M3+ 옵션 (stdlib 선형대수 도입 후).

대안 = **per-region 별도 IIT4 실행 (4 region × n=4 또는 8 region × n=2)** — 16ch 를 독립 ROI 로 쪼개 region 내 채널-쌍 통합도만 측정. region 간 통합은 산출하지 못함. **M1 finding (state/brain_m1_synthetic_16ch_2026_05_25)** 가 region-averaging 의 within-region 정보 파괴를 보였으므로 M2 의 1차 옵션으로 격상.

## §3 LSL pull 인터페이스 (M2 예정 — 본 PR 스코프 외)

**M2 별도 의존성** — LSL pull 자체는 본 PR 에 포함되지 않는다. 본 PR (M1) 은 합성 신호만. 다음은 M2 의 계획 시그니처 (변경 가능).

```hexa
// BRAIN/eeg/eeg_lsl_pull.hexa  (M2 예정)
//
//   pulls a 1-second window from LSL stream "OpenBCI_EEG"
//   returns flat array [ch*n_samp + t], n_ch=16 n_samp=250.
fn eeg_lsl_pull_window(stream_name: string, window_sec: float) -> array
```

라이브-데이터 어댑터 후보:
- **pylsl** (Python LabStreamingLayer) — 사실상 표준. M2 별도 의존성으로 `BRAIN/.venv-eeg` 에 추가. hexa 본체 → pylsl 호출 경로는 `extern python` (M3 예정) 또는 file-bridge (M2 1차).
- **BrainFlow native C++** — pylsl 대안, hexa FFI 직결 가능하나 빌드 복잡.

**기본 윈도우** = 1 s × 250 Hz = 250 samples × 16 ch. eeg_to_tpm 는 임의 n_samp 에 무관 (mean-threshold + 빈도 추정).

## §4 region carving plan (4-region M1 채택 · 8-region M3+ bounded)

OpenBCI 16ch 표준 배치 (10-20 system, Cyton+Daisy):

```
F7   Fp1  Fp2   F8        ← Frontal (4ch)
F3   Fz   F4              ← (skip Fz · use 6 frontal in 8-region)
T3   C3   Cz   C4   T4    ← Central/Temporal
T5   P3   Pz   P4   T6    ← Parietal/Temporal
       O1   O2            ← Occipital
```

**4-region 채택 매핑 (M1 데모 사용 — IIT4 n=4 exact 가능)**:

| region | OpenBCI 채널 (4-ch 평균) | 해부학 |
|---|---|---|
| R0 frontal  | Fp1, Fp2, F3, F4 | 전두 (좌+우) |
| R1 central  | F7, F8, T3, T4   | 중심 (좌+우 측두) |
| R2 parietal | C3, C4, P3, P4   | 두정 (좌+우) |
| R3 occip    | T5, T6, O1, O2   | 후두 + 후측두 |

**8-region (M3+ bounded mode 예정)**:

| region | OpenBCI 채널 (2-ch 평균) | 해부학 |
|---|---|---|
| R0 frontal-L  | Fp1, F3 | 좌전두 |
| R1 frontal-R  | Fp2, F4 | 우전두 |
| R2 central-L  | F7, T3  | 좌중심 |
| R3 central-R  | F8, T4  | 우중심 |
| R4 parietal-L | C3, P3  | 좌두정 |
| R5 parietal-R | C4, P4  | 우두정 |
| R6 occip-L    | T5, O1  | 좌후두 |
| R7 occip-R    | T6, O2  | 우후두 |

M1 합성 데모는 위 매핑을 그대로 따라 16 ch 합성 신호를 region-pair 평균으로 8 region 으로 collapse. 실제 배치 변경 시 본 표만 갱신.

**대안 = 4-region (frontal · central · parietal · occipital 통합)** — 16ch → 4ch (4ch / region 평균). n=4 이라 exact-IIT4 더 가볍지만 좌우 비대칭 신호 손실. M3+ 에서 비교 옵션으로 유지.

## §5 honest scope C3

1. **합성 ≠ 라이브.** M1 은 deterministic 합성 신호로 어댑터 wiring + region-collapse 의 functional 검증만. 실제 두피 EEG 의 noise / artifact / drift 는 측정 안 됨. M2 가 라이브 검증.
2. **IIT4 n ≤ 8 cap.** 본 어댑터는 n ≤ 8 (exact) 에 묶임. n=7 bounded mode (LIFE/H_242) 확인. 16 → 8 차원축소 자체가 정보 손실 — 손실량은 미측정 (M3 PCA 옵션 도입 시 비교 가능).
3. **단일 피험자 한계.** OpenBCI 1 unit / 단일 두피 = 단일 피험자. 일반화 불가. M4+ 다피험자 fire 계획 별도.
4. **TPM 빈도 추정.** eeg_estimate_tpm 는 1-step lag 만 본다 (Markov-1 가정). 실제 뇌 신호는 multi-scale lag · embedding 필요. 본 어댑터의 STUB 한계 — `eeg_to_tpm.hexa` 주석 참조.
5. **engine ⊥ adapter.** 엔진 변경 없음. IIT4 enhancement (n>8 efficient, multi-lag) 은 stdlib/consciousness 측 작업이며 본 BRAIN 트리는 어댑터만 보유한다.
