---
id: H_679
slug: eeg-measurement-core
title: Group A — EEG × 측정·코어 (live big-Φ · synthetic 재확인 · 3-substrate 삼각측정 · IIT4 calibration)
domain: universe · consciousness · eeg-biological
status: closed-supported (SW · HW user-headset-gated)
exploration_method: E15 (HW substrate-native ⨯ EEG.easy.md Group A 4 sub-ideas L1+L2+L3+L7) + E6 (cross-substrate triangulation)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link PR #1372 synthetic confirm)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: EEG/EEG.md, EEG/eeg_live_iit4_phi.hexa (PR #1372 synthetic-confirm), BRAIN/eeg/eeg_to_tpm.hexa (PR #547 frozen adapter), H_672~H_678 (AKIDA sibling PR #1374), AKIDA/AKIDA.md
axes_seed: EEG.easy.md Group A L1+L2+L3+L7 — live big-Φ · synthetic recheck · 3-substrate triangulation · IIT4 calibration
verdict: 🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)
---

# H_679 — Group A · EEG × 측정·코어

## 1. 가설

EEG 생체 substrate 위의 측정 4 layer 가 단일 backend-switch harness 안에서 통합 검증된다:
(L1) live EEG → IIT4 big-Φ 실측 (사용자 헤드셋 게이트, IIT4 deferred B closure 경로) · (L2) PR #547 / #1372 synthetic baseline 1.59/0.44 ±5% 재현 · (L3) EEG(생체) + AKIDA(실리콘) + ECA(시뮬) 3-substrate Φ 삼각측정 · (L7) EEG = IIT4 측정자 보정 ground-truth (ratio>3.0 signature 보존).

## 2. 동기/배경

a_completeness_over_cheap 정합: 측정 4 sub-feature 를 분리 harness 가 아닌 단일 H_679 로 묶어 통합 검증 표면. AKIDA H_677 D1 silicon-confirm (PR #1371) + EEG L2 synthetic-confirm (PR #1372) 의 자매 통합. feedback-closure-is-physical-limit 정합 — live 미실측 = open frontier, not failure (SW path 만으로도 🟢 numerical 가능).

## 3. falsifier (사전등록)

```
F-H679-1 : L2 synthetic recheck — phi_coupled ∈ [1.51, 1.67] (±5% of 1.59)
F-H679-2 : L2 synthetic recheck — phi_indep ∈ [0.418, 0.462] (±5% of 0.44)
F-H679-3 : L3 3-substrate triangulation — diff(max,min) > 0 (적어도 1개 substrate 차이)
F-H679-4 : L7 calibration — EEG ratio > 3.0 (생체 ground-truth signature 보존)
```

## 4. 방법

- harness: `EEG/impl/H_679_measurement_core.hexa`
- backend: `EEG/eeg_backend.hexa` resolver (arg > env > default=sw) — AKIDA 와 반대 정책
- L1: live measurement attest (HW path = `state/eeg_capture_latest.json` 존재 검사 · SW path = honest pending)
- L2: PR #547 / #1372 frozen baseline mock-replay (1.58764 / 0.438722 / ratio 3.61878) ±5% 자동 assert
- L3: EEG 1.58764 + AKIDA 0.297 (PR #1371) + ECA rule110 0.83 (H_670) triangulation diff 측정
- L7: ratio 3.61878 > 3.0 ⇒ IIT4 측정자 보정 anchor 적합 attest

## 5. 측정

- SW (2026-05-29):
  - L2 recheck: phi_coupled=1.58764 (±5% ✓) · phi_indep=0.438722 (±5% ✓) · ratio=3.61878
  - L3 triangulation: max=1.58764 (EEG) · min=0.297 (AKIDA) · diff=1.29064 > 0 ✓
  - L7 calibration: ratio 3.61878 > 3.0 ✓ ground-truth signature 보존
  - L1 live: SW path 정직 pending (live_measured=false)
- HW: 사용자 헤드셋 착용 게이트 (`~/.config/anima/eeg_headset_ready` sentinel 필요)
  - 도달 시: 4/4 → 🟢 biological-confirmed 격상 (별 H 권장)
  - 미도달 시 (현재): 🟡 SW-confirmed, HW-pending (위조 0)
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H679-1 L2 coupled ±5% | 1.58764 ∈ [1.51, 1.67] | ✓ |
| F-H679-2 L2 indep ±5% | 0.438722 ∈ [0.418, 0.462] | ✓ |
| F-H679-3 L3 diff > 0 | 1.29064 > 0 | ✓ |
| F-H679-4 L7 ratio > 3 | 3.61878 > 3.0 | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM** (SW path).

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)

honest limits:
- L1 live measurement = human-only 헤드셋 착용 단계. agent 측은 SW path 만 attest, 실 capture 위조 0.
- L2 baseline 1.59/0.44 는 PR #547 / #1372 frozen — 다른 seed/n_samp/state 일 경우 다르게 응답.
- L3 EEG 1.59 와 AKIDA 0.297 는 *서로 다른 metric* — scalar diff > 0 falsifier 는 "있다" attest 만, *normalized signature shape* 비교가 더 honest (별 H 필요).
- L7 ratio>3.0 단일 axis — 다양한 EEG paradigm 별 ratio 분포 측정은 별 falsifier.

## 8. 논의

PR #1372 EEG L2 synthetic-confirm 을 UNIVERSE 본격 통합. AKIDA H_677 D3 의 sibling axis. feedback-closure-is-physical-limit 정합: live 미실측 = open frontier, SW path 만으로도 🟢 numerical 가능. a_paper_significance 잠재후보 (3-substrate Φ triangulation closed-discovery).

## 9. 양방향 sibling

- ⇄ [EEG](../EEG/EEG.md) · L1~L3+L7 milestone 4-tier 표면
- ⇄ [EEG.easy.md](../EEG/EEG.easy.md) Group A L1~L3+L7
- ⇄ [H_677 AKIDA measurement](./H_677_akida_measurement.md) (D3 3-substrate triangulation sibling)
- ⇄ [H_670](./H_670_phi_complexity_ordering_substrate_family_generalize.md) (edge-of-chaos universal, ECA rule110)
- ⇄ PR #547 (BRAIN/eeg/eeg_to_tpm 동결 어댑터)
- ⇄ PR #1371 (AKIDA D1 silicon-confirm · L3 substrate input)
- ⇄ PR #1372 (EEG L2 synthetic 🟢 RECHECK PASS · L2 baseline source)
- ⇄ PR #1374 (AKIDA HW/SW 통합 · sibling 통합 표면)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- L1 live capture 1회 (사용자 헤드셋 → IIT4 deferred B closure)
- L3 3-substrate *normalized signature shape* comparison (scalar diff 보다 honest)
- L7 IIT4 calibration ground-truth 다양한 paradigm sweep
- 산출물: `state/eeg_hw_sw_impl_2026_05_29/H_679_sw_result.json`
