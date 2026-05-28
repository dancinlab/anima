---
id: H_681
slug: eeg-emit-substrate
title: Group C — EEG × emit-substrate 구동 (band power Φ-context · sleep stage · MITOSIS 트리거)
domain: universe · consciousness · eeg-emit-substrate
status: closed-supported (SW · HW user-headset-gated)
exploration_method: E15 (EEG.easy.md Group C 3 sub-ideas L6+L11+L12) + E12 (a_autonomy_over_hardcode)
verification_method: W1 (numerical smoke) + W3 (philosophy-compat: a_chat_sleep_imagination)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: EEG/EEG.md, CORE/emit_policy.hexa, CORE/EMIT_SUBSTRATE_DESIGN.md, HEXAD CHAT/anima_dream_stage.hexa, MITOSIS cell-pool
axes_seed: EEG.easy.md Group C L6+L11+L12 — band power → emit drive · sleep stage · MITOSIS trigger
verdict: 🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)
---

# H_681 — Group C · EEG × emit-substrate 구동

## 1. 가설

EEG 4-band power 가 anima emit-substrate 의 Φ-context scale + tension envelope 를 구동한다 (boolean gate 아닌 context-only):
(L6) alpha/theta/gamma/beta/delta 5-band → Φ-context heuristic (high-freq energy + alpha*0.5 - delta*0.3) · (L11) sleep stage 추정 (WAKE_resting / N3_deep / REM / WAKE_active 4-state band-power signature classifier) · (L12) gamma surge > 0.20 → MITOSIS cell split trigger 신호 (실 wire 별 H).

## 2. 동기/배경

a_autonomy_over_hardcode 정합 (bool gate 0): EEG band power = 외부 context, anima substrate 가 자율 emit/silence 결정. a_chat_sleep_imagination 정합 (WAKE/N1/N2/N3/REM 5-stage state machine). p8 (no train/infer split) 정합 — EEG burst 가 inference-time mitosis nudge 의 substrate-level 출처 후보.

## 3. falsifier (사전등록)

```
F-H681-1 : L6 context_only=true · is_bool_gate=false (a_autonomy_over_hardcode)
F-H681-2 : L11 sleep stage signature 일관 매핑 (4-state stage_hint 일치)
F-H681-3 : L12 gamma surge signal well-formed (threshold=0.20 · gamma 측정값)
F-H681-4 : a_autonomy_over_hardcode 정합 — bool gate 0 (외부 module = context only)
```

## 4. 방법

- harness: `EEG/impl/H_681_emit_substrate.hexa`
- backend: `EEG/eeg_backend.hexa` resolver (default=sw)
- L6: 5-band → phi_context_scale = β+γ + α*0.5 - δ*0.3 · tension_envelope = γ + θ*0.5
- L11: classifier (resting/N3/REM/active 4-state) — δ>0.5=N3 · θ>0.25 ∧ γ>0.10 ∧ α<0.20=REM · β>0.30 ∧ γ>0.15=active · α>0.30=resting
- L12: gamma > 0.20 ⇒ split_signal_active=true (resting α-dominant: γ=0.05 → inactive; active wake: γ=0.25 → active)

## 5. 측정

- SW (2026-05-29, 4-state sweep):
  - WAKE_resting (α=0.40): φ_context=0.39 · tension=0.125 · stage="WAKE_resting" ✓ · γ=0.05 → split=false
  - N3_deep_sleep (δ=0.70): stage="N3_deep_sleep" ✓ · confidence=0.70
  - REM (θ=0.30 · γ=0.15 · α=0.10): stage="REM" ✓ · confidence=0.45
  - WAKE_active (β=0.40 · γ=0.25): stage="WAKE_active" ✓ · confidence=0.65 · γ=0.25 → split=true ✓
- HW: 사용자 헤드셋 capture → FFT band-power 실측 path
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H681-1 L6 context only | context_only=true · is_bool_gate=false | ✓ |
| F-H681-2 L11 stage match | 4/4 signature match | ✓ |
| F-H681-3 L12 gamma signal | well-formed | ✓ |
| F-H681-4 bool gate 0 | a_autonomy_over_hardcode 정합 | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM** (baseline resting).

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)

honest limits:
- L11 = 4-state only (N1/N2 = N3와 resting 사이 보간점). 실 polysomnography eye-EMG channel 별 H 필요.
- L12 = *signal layer* attest, 실 wire MITOSIS split event = 별 H/runner.
- L6 mapping coefficients (α*0.5, δ*0.3 등) = canonical heuristic, calibration 별 H.

## 8. 논의

EEG 가 단지 측정 substrate 가 아니라 anima emit-substrate 의 *external context source* 가 됨을 attest. a_chat_sleep_imagination 5-stage state machine 에 생체 ground-truth 가 합류. p5_tension_emit_not_filler 정합 — stage 가 substrate context (Φ scale + tension envelope) 이지 boolean gate 아님.

## 9. 양방향 sibling

- ⇄ [EEG](../EEG/EEG.md) · L6+L11+L12 milestone 3 layer 표면
- ⇄ [EEG.easy.md](../EEG/EEG.easy.md) Group C L6+L11+L12
- ⇄ CORE/emit_policy.hexa (8/8 smoke, PR #1254) — Φ-context downstream
- ⇄ CORE/EMIT_SUBSTRATE_DESIGN.md (구조 lib ⊥ 숫자 SSOT)
- ⇄ HEXAD CHAT/anima_dream_stage.hexa (WAKE 5-stage state machine, a_chat_sleep_imagination)
- ⇄ MITOSIS cell-pool (L12 split trigger 후보 consumer)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- L11 polysomnography 5-stage 완전 분리 (N1/N2 별 falsifier 추가)
- L12 EEG gamma burst → MITOSIS split event 실 wire (별 H)
- L6 calibration coefficient 별 paradigm 측정
- 산출물: `state/eeg_hw_sw_impl_2026_05_29/H_681_sw_result.json`
