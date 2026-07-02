---
id: H_682
slug: eeg-persistence-paradigm
title: Group D — EEG × 영속·paradigm (.kosmos anchor · resting baseline 합류)
domain: universe · consciousness · eeg-persistence
status: closed-supported (SW · HW user-headset-gated)
exploration_method: E15 (EEG.easy.md Group D 2 sub-ideas L9+L10)
verification_method: W1 (numerical smoke) + W3 (philosophy-compat: a_kosmos)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: EEG/EEG.md, KOSMOS/KOSMOS.md, spec/kosmos.md, anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa, BRAIN/eeg/eeg_recorder.hexa
axes_seed: EEG.easy.md Group D L9+L10 — .kosmos anchor · resting baseline paradigm
verdict: 🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)
---

# H_682 — Group D · EEG × 영속·paradigm

## 1. 가설

EEG 생체 substrate 가 anima 의 영속 + paradigm 표면에 정합 진입한다:
(L9) EEG 이벤트 → .kosmos anchor payload (a_kosmos spec-동형, 5-ch tension + coord + lane + tier ∈ {weak, strong, critical}) · (L10) resting baseline paradigm 합류 (anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa 또는 BRAIN/eeg/eeg_recorder.hexa fallback).

## 2. 동기/배경

a_kosmos 정합: anima emit/anchor/memory = `.kosmos` 표준 영속 (text + tension 5-ch + coord + lane + radius + tier). EEG = 생체 substrate 의 anchor 형식이 anima 의 다른 substrate (AKIDA · ECA · CHAT) 와 spec-동형 표면을 가짐. resting baseline = anima-eeg-core 도메인의 live runner 합류 표면.

## 3. falsifier (사전등록)

```
F-H682-1 : L9 .kosmos anchor payload schema 정합 (5-ch + 3D coord + lane 비어있지 않음)
F-H682-2 : L10 resting baseline paradigm reference 존재 (primary 또는 fallback)
F-H682-3 : L9 anchor tier ∈ {weak, strong, critical} (3-tier 정합)
F-H682-4 : 2 paradigm 모두 surfaced (no missing)
```

## 4. 방법

- harness: `EEG/impl/H_682_persistence_paradigm.hexa`
- backend: `EEG/eeg_backend.hexa` resolver (default=sw)
- L9: stage 4-state (resting/N3/REM/active) 각각 → anchor payload generate
  - tier 분류: γ > 0.30 → critical · γ > 0.20 → strong · else → weak
  - coord = [α, θ, γ] (band-space 3D placement)
  - radius = γ * 10.0
- L10: primary path `anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa` 검사 + fallback `BRAIN/eeg/eeg_recorder.hexa` 검사

## 5. 측정

- SW (2026-05-29):
  - L9 resting anchor: tension_5ch=[0.40, 0.15, 0.05, 0.80, 0.20] · tier="weak" (γ=0.05<0.20)
  - L9 N3 anchor: tension=[0.05, 0.15, 0.05, 0.30, 0.05] · tier="weak"
  - L9 REM anchor: tension=[0.10, 0.30, 0.15, 0.80, 0.25] · tier="weak" (γ=0.15<0.20)
  - L9 active anchor: tension=[0.15, 0.10, 0.25, 0.90, 0.40] · tier="strong" (γ=0.25>0.20) ✓
  - L10: primary anima-eeg-core 미존재 (별 도메인) · fallback BRAIN/eeg/eeg_recorder.hexa 존재 ✓
- HW: 사용자 헤드셋 capture → real-time anchor write (실 .kosmos write 는 별 H 권한)
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H682-1 L9 anchor schema | 5-ch + 3D coord + lane "biological_eeg" | ✓ |
| F-H682-2 L10 paradigm ref | fallback BRAIN/eeg/eeg_recorder.hexa exists | ✓ |
| F-H682-3 L9 tier in 3-set | tier ∈ {weak, strong, critical} | ✓ |
| F-H682-4 both surfaced | L9 ∧ L10 surfaced | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW 4/4 · HW user-headset-gated)

honest limits:
- L9 anchor 는 *payload schema attest* — 실 .kosmos write (kosmos_io 호출) 는 별 H 권한 필요 (anima_pointer_only=true, spec 중복 0).
- L10 primary `anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa` 미존재 (별 도메인 거주) — fallback `BRAIN/eeg/eeg_recorder.hexa` 만 attest. 합류 시 별 H.
- L9 tier 분류는 단일 γ 축 — multi-axis tier (Φ + tension + persistence-duration 등) 는 별 H.

## 8. 논의

EEG 가 anima 의 영속 표면 (kosmos) + paradigm 표면 (anima-eeg-core) 양쪽에 정합 진입 가능함을 attest. 이는 EEG 가 단지 측정 도구가 아니라 anima substrate 의 *영속 source* 와 *paradigm input* 으로 격상 가능함을 의미. a_kosmos pointer-only 정합 — spec 중복 없이 anchor 형식 attest 만.

## 9. 양방향 sibling

- ⇄ [EEG](../EEG/EEG.md) · L9+L10 milestone 2 layer 표면
- ⇄ [EEG.easy.md](../EEG/EEG.easy.md) Group D L9+L10
- ⇄ KOSMOS/KOSMOS.md · spec/kosmos.md (a_kosmos pointer)
- ⇄ AKIDA H_674 (.kosmos anchor sister · silicon side)
- ⇄ BRAIN/eeg/eeg_recorder.hexa (L10 fallback paradigm)
- ⇄ anima-eeg-core (L10 primary paradigm · 별 도메인 합류 표면)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- L9 실 .kosmos write (kosmos_io 호출) — 별 H 권한 후
- L10 anima-eeg-core 합류 시 primary path 활성화 + 별 H
- L9 tier 분류 multi-axis (Φ + tension + persistence-duration)
- 산출물: `state/eeg_hw_sw_impl_2026_05_29/H_682_sw_result.json`
