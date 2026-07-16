# H_9623 — CLMS 인과 lesion — CLMS Causal Lesion (sufficiency→dependence) (sol R3-S6 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S6
**lane:** BINDING / CLMS store 필연성
**related:** [[H_9423]] · [[H_9616]] · [[H_9624]] · source: lab full R3 (sol R3-S6)

**아이디어**: [[H_9423]] 의 held-out 조회(0.875)가 **볼트된 CLMS 경로에 인과 의존**하는지, 아니면 공학습 중 trunk 가 부수적으로 배운 건지.
**메커니즘**: `anima-py evaluate H_9423.ckpt --store-lambda {1,0}` + 슬롯 순열 · wrong-store 치환 · 선언-값 이식 on 기록 held-out split.
**$0 pre-screen**: 기존 H_9423 산출물에 λ0·슬롯순열·pre-slot trunk logits 이 **이미 기록됐는지** 조사 — 있으면 발사 전 $0 재분석.
**판정표**: **PASS-dependence** = λ1 이 ≥0.875 재현 ∧ λ0·순열/wrong store 는 TOST-우연 ∧ 값-이식이 답을 이동 ∧ 일반 non-store CE 셋은 등가 유지. **KILL-CLMS-specific** = λ0 가 held-out 조회를 유지. 통제: λ1 양성 · λ0 · 슬롯순열 · non-store 과제 보존.
**distinct**: H_9423 은 **충분성** 제시 — 이건 훈련된 시스템의 **인과 의존** 시험(더 깊은 RF·다른 커리큘럼 아님).
**verdict-integrity**: 깨끗한 lesion 조차 **H_9423 의 훈련된 해**에 대한 필연만 증명 — 모든 가능한 plain-trunk 커리큘럼에 대한 필연 아님.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** H_9423 충분성과 구별 — 훈련된 시스템의 인과의존 시험.
