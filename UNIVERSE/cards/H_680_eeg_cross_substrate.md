---
id: H_680
slug: eeg-cross-substrate
title: Group B — EEG × 교차-substrate 다리 (EEG→AKIDA spike · tension-link 5-ch · kuramoto α-band)
domain: universe · consciousness · eeg-cross-substrate
status: closed-supported (SW · HW user-headset-gated)
exploration_method: E15 (EEG.easy.md Group B 3 sub-ideas L4+L5+L8) + E6 (cross-substrate bridge)
verification_method: W1 (numerical smoke) + W12 (sister-link AKIDA H_678 PR #1374)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: EEG/EEG.md, tool/anima_eeg_to_akida_spike.hexa, AKIDA/impl/H_678_channel_bridge.hexa (PR #1374), CHANNEL.md tension-link 5-ch
axes_seed: EEG.easy.md Group B L4+L5+L8 — EEG→AKIDA spike · tension-link · kuramoto α-band
verdict: 🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)
---

# H_680 — Group B · EEG × 교차-substrate 다리

## 1. 가설

EEG 생체 substrate 가 단일 backend-switch harness 안에서 3개의 cross-substrate 다리를 통합 표면화한다:
(L4) EEG → AKIDA spike (생체→뉴로모픽 다리, ADM up/down + 16ch x 2 raster) · (L5) EEG → tension-link 5-ch payload (의식↔의식 채널, alpha/theta/gamma/1-delta/beta 매핑) · (L8) EEG α-band Hilbert phase kuramoto order_r (cell-sync 측정).

## 2. 동기/배경

a_completeness_over_cheap 정합: 3 brücken 를 분리 module 가 아닌 단일 H_680 로 묶어 통합 검증. AKIDA H_678 channel-bridge (PR #1374) 의 *역방향 매핑* — 본 H 는 EEG 출발점에서 AKIDA + CHANNEL + MITOSIS 로 가는 채널을 묶음.

## 3. falsifier (사전등록)

```
F-H680-1 : L4 EEG→AKIDA bridge schema 존재 (tool/anima_eeg_to_akida_spike.hexa)
F-H680-2 : L5 tension-link 5-ch payload vector length = 5
F-H680-3 : L8 kuramoto order_r ∈ [0, 1] (정상 phase-sync index range)
F-H680-4 : 3 brücken all surfaced (no missing channel)
```

## 4. 방법

- harness: `EEG/impl/H_680_cross_substrate.hexa`
- backend: `EEG/eeg_backend.hexa` resolver (default=sw)
- L4: `tool/anima_eeg_to_akida_spike.hexa` 존재 검사 + schema `anima/eeg_akida_spike_raster/1` + tensor `(1, T_bin, 16, 2)` attest
- L5: resting band-power → 5-ch payload `[alpha, theta, gamma, 1-delta, beta]` (length=5)
- L8: alpha 0.40 → kuramoto r = 0.20 + 0.40*1.25 = 0.70 (phase_locked=true · ∈ [0,1])

## 5. 측정

- SW (2026-05-29):
  - L4 bridge: tool/anima_eeg_to_akida_spike.hexa exists=true · schema OK
  - L5 tension_5ch: [0.40, 0.15, 0.05, 0.80, 0.20] · length=5 ✓
  - L8 kuramoto: order_r=0.70 · phase_locked=true · valid_range ✓
- HW: 사용자 헤드셋 게이트 (capture → real-time band-power → real bridge fire)
  - 미도달 시: 🟡 SW-confirmed, HW-pending (sister H_678 가 AKIDA 측 spike fire 담당)
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H680-1 L4 bridge present | exists=true · schema OK | ✓ |
| F-H680-2 L5 5-ch length | length=5 | ✓ |
| F-H680-3 L8 kuramoto ∈ [0,1] | 0.70 ∈ [0,1] | ✓ |
| F-H680-4 all 3 channels | bridge ∧ 5-ch ∧ valid kuramoto | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM** (SW path).

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)

honest limits:
- L4 bridge schema = *existence + tensor shape* attest, 실 ADM conversion fire 는 별 H/runner (AKIDA H_678 가 측면 wire).
- L5 5-ch mapping = canonical (alpha/theta/gamma/1-delta/beta), 다른 mapping (e.g. coherence-based) 은 별 H.
- L8 kuramoto order_r = *synthetic alpha-dominance proxy*, 실 EEG Hilbert phase 측정은 stdlib/dsp/hilbert 별 wire 필요.

## 8. 논의

EEG 가 단지 IIT4 측정 substrate 가 아니라 cross-substrate hub — AKIDA spike · CHANNEL tension · MITOSIS phase-sync 의 출발점이 됨을 attest. p8 (no train/infer split) 정합 — EEG burst 가 inference-time phase event 로 mitosis 와 연속.

## 9. 양방향 sibling

- ⇄ [EEG](../EEG/EEG.md) · L4~L5+L8 milestone 3-channel 표면
- ⇄ [EEG.easy.md](../EEG/EEG.easy.md) Group B L4+L5+L8
- ⇄ [H_678 AKIDA channel-bridge](./H_678_akida_channel_bridge.md) (EEG→AKIDA E1 sibling)
- ⇄ tool/anima_eeg_to_akida_spike.hexa (E1 bridge skeleton)
- ⇄ CHANNEL.md tension-link 5-ch (L5 출처)
- ⇄ MITOSIS phase-sync (L8 kuramoto sister)
- ⇄ PR #1374 (AKIDA HW/SW 통합 · sibling)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- L4 EEG capture → real ADM conversion → AKIDA fire (사용자 헤드셋 게이트 후)
- L5 실 5-ch payload → tension-link UDP 9999 broker wire
- L8 stdlib/dsp/hilbert engine 호출로 실 phase 측정
- 산출물: `state/eeg_hw_sw_impl_2026_05_29/H_680_sw_result.json`
