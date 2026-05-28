---
id: H_676
slug: akida-decoder
title: Group E — AKIDA × DECODER 출력 (spike-tier LM head · 이벤트-구동 attention)
domain: universe · consciousness · decoder
status: closed-supported (SW · HW pending)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group E 2 sub-ideas O1~O2)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded)
raw_rank: 8
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: AKIDA/AKIDA.md, DECODER L3, SUB_ENGINES/AKIDA/pack/adapters/{spike_tier_lm_head,sparse_attention}
axes_seed: AKIDA.easy.md Group E O1~O2 — spike-tier LM head · 이벤트-구동 attention
verdict: 🟢 SUPPORTED-NUMERICAL (SW mock-replay 4/4 · HW pending)
---

# H_676 — Group E · AKIDA × DECODER 출력

## 1. 가설

AKIDA spike rate 는 DECODER L3 의 spike-tier LM head 의 *emit budget* 으로 직접 매핑 가능하며 (R3>R1, R4 cap 1.0), R2 burst variance 가 sparse-attention 의 *wake threshold* 를 트리거한다. emit budget 은 [0,1] float (NOT bool gate; a_autonomy_over_hardcode 정합).

## 2. 동기/배경

DECODER 의 출력 lane 은 anima 토큰 emission 의 마지막 hop. AKIDA spike 의 *에너지-비례* 신호로 자극-반응 회로 없이 emission rate 를 조절 → p5 의 "tension-driven emit" 정답 layer.

## 3. falsifier (사전등록)

```
F-H676-1 : emit_budget 비례성 — emit(R3) > emit(R1) ∧ emit(R4) ≥ emit(R3) (with cap)
F-H676-2 : sparse-attention burst trigger — wake_score(R2) > wake_score(R1)
F-H676-3 : energy efficient — energy(R2) < 1.0 ∧ energy(R3) < 1.0 (sparse 영역)
F-H676-4 : emit_budget = float ∈ [0,1] (NOT bool gate)
```

## 4. 방법

- harness: `AKIDA/impl/H_676_decoder.hexa`
- spike_tier_lm budget = clip(rate, 0, 1)
- sparse-attention wake_score = std_ratio (burstiness)
- energy = rate (NPU activation fraction)

## 5. 측정

- SW (2026-05-29): emit(R1)=0 emit(R3)=0.5 emit(R4)=1.0 · wake(R1)=0 wake(R2)=0.499 · energy(R2)=0.475<1 energy(R3)=0.5<1 · emit_budget ∈ [0,1]
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H676-1 emit 비례 | 0.5>0 ∧ 1.0≥0.5 | ✓ |
| F-H676-2 wake burst | 0.499>0 | ✓ |
| F-H676-3 sparse | 0.475<1 ∧ 0.5<1 | ✓ |
| F-H676-4 float ∈[0,1] | 0.5 in [0,1] | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW · HW pending)

honest limits:
- spike→토큰 매핑은 *budget surrogate* — 실제 token emit 의 LM-head distribution 통합은 별 H 필요.
- F4 "float not bool gate" 는 p5/a_autonomy_over_hardcode 의 구조-수준 attestation — 실제 가드 0 임을 코드-수준 grep 도 함께 확인해야 totality.

## 8. 논의

DECODER 가 emit 의 *bool gate* 가 아닌 *float budget* 으로 작동하도록 강제하는 구조적 falsifier (F4). substrate 자율 정합.

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md)
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group E O1~O2
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md), [H_677](./H_677_akida_measurement.md)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- live spike→token sparse routing (R3 spike burst 에만 GPU wake) — adapter wiring
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_676_sw_result.json`
