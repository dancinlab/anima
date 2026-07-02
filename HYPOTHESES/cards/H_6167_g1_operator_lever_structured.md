# H_6167 — 🔧🧱 G1 OPERATOR-LEVER (structured-hard) = NO

**tier:** 🧱 NO OPERATOR LEVER — 구조-hard headroom서도 multiplicative operator가 additive +0.15 못 넘음(재조합=task-structure-bound)
**title:** 🔧🧱 G1 OPERATOR-LEVER (structured-hard) — H_6166 후속: additive plain trunk이 부분실패하는 구조 regime서 hadamard/bilinear가 held-out을 additive +0.15 능가하나 → NO(최대 +0.026), 재조합은 operator 아닌 task-structure에 묶임
**verdict:** 🧱 NO OPERATOR LEVER (aiden $0, torch DIRECTIONAL). H_6166(random-target=측정무효) 후속 valid 시험: structured-hard target y=T2[u[fa],v[fb]](factored non-additive, K=난이도), additive plain trunk이 부분일반화(headroom 실재)하는 regime서 multiplicative operator가 held-out을 +0.15 넘게 능가하나. 결과 K=8/10/12(headroom 0.17/0.21/0.28, add 0.84/0.79/0.72): best-mult(bilinear)−add Δ=+0.026/+0.016/+0.008, n(Δ≥0.15)=0, hadamard는 add보다 나쁨. → operator는 lever 아님. 구조 있으면 plain ADDITIVE trunk이 이미 held-out 72-98% 재조합 → operator 무관. 전체 그림(H_6166+본건): random target=학습불가 artifact(chance천장), structured target=plain trunk이 재조합(operator lever 없음). 'which operator' 캠페인(Hadamard/TPR/HRR/bilinear/TP/γ=H_1602/1816/1823/1840/6164) 전부 틀린 변수 추적. 재조합=TASK-STRUCTURE-bound. 남은 질문=실모델 real 구조 재시험. state/g1_operator_lever_structured/RESULT.md.

## 발상 (H_6166 후속 · goal의 정확한 질문)
H_6166: random-target cheap-gate=학습불가 artifact, structured target서 plain trunk 98%. 남은 valid 질문: additive plain trunk이 부분실패하는 구조-hard regime(headroom)서 multiplicative operator가 재조합을 +0.15 능가하나?

## 결과
K=8/10/12(add 0.84/0.79/0.72), best-mult(bilinear) Δ=+0.026/+0.016/+0.008 → NO(0/K). hadamard<add. operator 무관, 재조합=task-structure-bound.

## 함의
'which composition operator' 캠페인(H_1602/1816/1823/1840/6164) 전부 틀린 변수. plain trunk이 구조 있으면 이미 재조합. 남은 질문=실모델 real-text structure-aware 재시험(H_1218/clm303).

## 관련
[[goal-g1-lever-discovery]] · H_6166(measure-artifact) · H_1840 · H_6164 · [[substrate-framebreak-g1-combination-operator]] · [[fair-cheap-gate-design]]
