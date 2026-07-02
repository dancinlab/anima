# H_6166 — 🚨🔬 G1 MEASURE-ARTIFACT (random-target cheap-gate 무효)

**tier:** 🟠 MEASURE-ARTIFACT — random-target cheap-gate 무효; plain trunk이 STRUCTURED 재조합 98% (별도 lever 불요)
**title:** 🚨🔬 G1 MEASURE-ARTIFACT — 캠페인 random-target cheap-gate는 정보이론적 학습불가 과제였음; 동일 plain trunk이 STRUCTURED(factored-rule) held-out 재조합 98%, RANDOM은 chance floor → 최근 FLOOR(H_1840/6164/6162/6161/1824) 측정무효, 재조합능력은 존재
**verdict:** 🟠 MEASURE-ARTIFACT CONFIRMED (aiden $0, torch DIRECTIONAL, 5-seed). 동일 plain concat-embed MLP trunk이: random T[fa,fb] held-out 0.092(≈chance 0.125=floor) · struct_add(y=(u[fa]+v[fb])%C) 0.80 · struct_nonadd(y=T2[u[fa],v[fb]], factored K=4 shared latent, NON-additive) **0.978**. 해석: random full-rank table은 held-out이 seen과 정보이론적 독립 → 어떤 메커니즘(additive/HRR/TP/γ/slot/neurosymbolic)도 불가, chance가 천장. rigging 방지용 operator-agnostic random target(H_1840 교훈)이 과교정돼 학습불가 극단이 됨. 구조 있으면 plain trunk이 lever 없이 98% 재조합 → trunk은 재조합 불능 아님. ⇒ 최근 random-target FLOOR(H_1840 γ GPU 미인가·H_6164·H_6162·H_6161·H_1824)는 lever 부재 증거 아님=측정무효, STRUCTURED 재측정 필요. ⚠️범위(a_toy_scale_recheck): 합성 random-target 방법론만 무효화, 실모델 real-text G1=0(H_1218/clm303)은 별도 structure-aware 재시험 대상(뒤집힘 아님). state/g1_measure_artifact_random_target/RESULT.md.

## 발상 (break-walls: measure-artifact 의심 · verdict-integrity)
캠페인 cheap-gate들이 전부 RANDOM T[fa,fb] target을 씀(operator-agnostic, rigging 방지). random table은 held-out이 정보이론적으로 seen과 독립 = 학습불가 → chance가 천장. 진짜 재조합(SCAN)은 규칙 구조가 있어 부분→전체 예측가능.

## 측정 (동일 plain trunk, 3 target, 5 seed)
random 0.092(≈chance) · struct_add 0.80 · struct_nonadd 0.978. → 구조 있으면 plain trunk이 lever 없이 재조합.

## 함의
최근 random-target FLOOR(H_1840 γ·H_6164·H_6162·H_6161·H_1824) = 측정무효(lever 부재 증거 아님). trunk 재조합능력 존재. 실모델 real-text G1(H_1218/clm303)은 별도 structure-aware 재시험(범위 한정, a_toy_scale_recheck).

## 관련
[[goal-g1-lever-discovery]] · [[fair-cheap-gate-design]] · H_1840 · H_6164 · H_6162 · H_6161 · H_1824 · [[substrate-framebreak-g1-combination-operator]]
