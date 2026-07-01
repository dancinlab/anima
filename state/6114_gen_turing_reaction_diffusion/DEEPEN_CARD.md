## 심화 (adversarial multi-lens)

**목표:** DIRECTIONAL REACHABLE(ADD=0.000 → RD-TURING=1.000)이 진짜 조합 신호인지, 아니면 metric artifact 인지 3-control 로 REFUTE 시도. (a_break_the_wall · H_6112 전례: numpy 0→1.0 이 실 CLMConvMoE trunk 서 0→0.022 붕괴 = numpy 과대평가.)

**FROZEN BAR (실행 전 고정):** RD 연산자 SURVIVE(→CONFIRMED) iff (S1)어떤 generic 비선형도 RD held-out 의 0.15 이내에 못 옴 ∧ (S2)RD bind-recoverability 가 additive 를 +0.20 초과 ∧ (S3)ablation 붕괴. 아니면 ARTIFACT.

**결과 (numpy, `state/6114_gen_turing_reaction_diffusion/deepen.py`·DEEPEN_RESULT.txt):**

| control | 수치 | 판정 |
|---|---|---|
| (C0) split-fragility | RD held-out = **0.600** (신split) vs **1.000** (원split) | 원 0.70 bar 미달 · REACHABLE 이 split 의존 |
| (C1) generic-비선형 | RD=0.600 · prod=0.200 · sqsum=0.000 · mlp=0.000 | **S1=True** (RD 는 generic 곱/MLP 보다 우위) |
| (C2) bind-recoverability | RD recov=**0.000** (A=0,B=0) · ADD recov=**1.000** (A=1,B=1) | **S2=False** (결정적) |
| (C3) ablation | eqdiff=0.000 · noreact(반응항 OFF)=0.000 | S3=True |

**정직한 결론 — ARTIFACT.** C1(generic 비선형과 구별)·C3(ablation 붕괴)는 통과하나 **C2 bind-recoverability 에서 결정적으로 실패**. RD 합성장(C)에서 부모 A·B 를 선형 복원 = **0.000** (additive 는 1.000). 즉 RD 는 부모 정보를 *파괴*함으로써 "부모와의 distinctness"(원 metric)를 trivially 달성 — 이는 조합 결합(compositional binding)의 정반대다. distinctness-from-parents 는 **necessary-not-sufficient**: 진짜 결합은 두 부모가 C 에서 복원돼야 하는데 RD 는 chaotic scramble 으로 이를 파괴. 게다가 XOR acc 는 split 에 취약(1.000→0.600, 원 0.70 bar 미달)해 REACHABLE 자체가 robust 하지 않음.

**H_6112 transfer caveat:** numpy = DIRECTIONAL by construction, terminal 아님. 그러나 이 심화는 실-trunk 재측정 *이전*에 이미 조합 신호가 없음을 보임 — RD 의 작동 성분(u·v² cross-term)은 census 상 실 additive trunk 서 collapse 확정된 multiplicative-readout 계열(H_1617 Hadamard⊙·H_1823 circconv·H_6104 constraint-intersect INERT). H_6112 처럼 실 CLMConvMoE 서도 falsify 될 것으로 예상. terminal 박제 전 실-trunk rung 불필요 — bind-recoverability=0 이 numpy 단계에서 이미 조합-결합 부재를 증명. **DIRECTIONAL → ARTIFACT.**
