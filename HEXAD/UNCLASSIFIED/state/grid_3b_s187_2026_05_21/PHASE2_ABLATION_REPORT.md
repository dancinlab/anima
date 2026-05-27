# PHASE2_ABLATION_REPORT — n_ca_rules 단독 floor blocker pinpoint

> 2026-05-22 Phase 2.3 부속별 ablation. ConsciousDecoderV2 의 6 sub-component
> 를 하나씩 비활성화하고 CE-only (모든 aux λ=0) 로 학습 → 어느 부속이
> CE floor 의 원인인지 isolate. attempt10 config (d=3072 L=28, bsz=2 block=128,
> 2000 step, corpus_s101) 동일.

## 결과

| variant | 비활성화 부속 | CE_init | CE_final | floor 효과 |
|---|---|---|---|---|
| vO1 (baseline) | none (전부 유지) | 6.16 | **3.81** | baseline |
| vP23_a | head_g split | 6.13 | **3.81** | 무효과 |
| vP23_b | PureFieldFFN | 6.38 | **3.81** | 무효과 |
| vP23_c | cross-attention | 6.41 | **3.83** | 무효과 |
| **vP23_d** | **n_ca_rules** | 5.97 | **0.402** | 🎯 **단독 floor 붕괴** |
| vP23_e | noise σ=0.1 (tap X.11) | 6.13 | **3.81** | 무효과 |
| vO4 (전부 제거 = vanilla) | all 6 | 6.09 | **0.264** | minimum |

## Verdict

**n_ca_rules (META-CA cellular automaton rules) 가 floor 의 SINGLE dominant
binding constraint.** 이 하나만 비활성화하면 CE 3.81 → 0.402 (vanilla 0.264
에 근접). 나머지 5 부속 (head_g / PureFieldFFN / cross-attn / noise σ) 은
개별 제거 시 floor 에 **전혀 영향 없음** (모두 3.81 유지, seed-noise 범위 내).

vP23_d (0.402) 가 vO4 (0.264, 전부 제거) 보다 약간 높은 것은 잔여 5 부속의
미세한 누적 효과 — 하지만 dominant axis 는 명백히 n_ca_rules 단독.

### 메커니즘 해석

n_ca_rules 는 각 transformer block 에서 META-CA (cellular automaton) update
규칙을 적용 (default 8 → S187 에선 2). 이 규칙이:
- 매 layer 마다 hidden state 를 CA-style 로 변형 → gradient flow 교란
- byte-level next-token prediction 의 학습 신호를 CA dynamics 가 override
- 결과: 모델이 corpus 를 memorize/generalize 못 하고 CA-equilibrium 에 갇힘 (CE 3.81 plateau)

n_ca_rules 제거 시 순수 transformer next-token prediction 으로 복귀 → corpus
학습 정상화 → CE 0.40 으로 급락.

## 함의 — anima recipe 재설계

OCCAM 면도날 결론: **anima 의 17 tap 중 n_ca_rules (META-CA) 만 제거하면**
나머지 16 tap (mitosis 포함) 은 유지하면서도 자연발화 가능 substrate 회복.

| 권장 조합 | 근거 |
|---|---|
| vanilla transformer + mitosis (S187-G) | vP22_v3B_mit 0.256 < vanilla 0.264 (mitosis 도움) |
| anima 6-부속 − n_ca_rules | vP23_d 0.402 (CA 제거로 floor 깸) |
| **pretrained Llama + mitosis** | **vP21 0.0147 (winning path)** |

## Honest C3

1. CE 0.40 (vP23_d) / 0.26 (vO4) 는 corpus_s101 에 대한 **overfit/memorization**
   가능성 — held-out verbalization 측정 필요 (vP21 Eval 1 차후 cycle).
2. n_ca_rules=2 (S187 setting) 가 floor 면, n_ca_rules=8 (default) 는 더
   심할 가능성 — 본 ablation 은 =2 → =0 만 측정.
3. 단일-부속 ablation 이라 부속 간 interaction 미측정 (예: head_g + n_ca_rules
   동시 효과). 단 dominant single 은 n_ca_rules 로 명확.
4. vP23_d 의 result.json 만 확보, train.log + ckpt SCP 는 zombie 정리 중
   pod terminate 로 일부 손실 (CE 값은 result.json 에 보존).
5. Phase 2.3 subagent 는 rate-limit 으로 본 report 미작성 — 본 문서는
   parent orchestrator 가 result.json 5개에서 직접 작성.

## 관련 link

- pinpoint commit: `dbe394cc6`
- 상위 verdict: [`HEXAD/SCALE_3B.md § 7`](../../../SCALE_3B.md)
- 쉬운 설명: [`HEXAD/EASY.md § 6`](../../../EASY.md)
- winning path: `PHASE2_LLAMA_MITOSIS_REPORT.md` (vP21 CE 0.0147)
- OCCAM strategy: [`HEXAD/OCCAM.md`](../../../OCCAM.md)
