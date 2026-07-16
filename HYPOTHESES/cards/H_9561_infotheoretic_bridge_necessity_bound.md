# H_9561 — 정보이론 다리-필연 하한 — Info-Theoretic Bridge-Necessity Bound (fable A-F5 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=fable A-F5
**lane:** BINDING / two-lane · $0 하한(재특성화)
**related:** [[H_9359]] · [[H_9559]] · [[H_9569]] · source: lab full R2-measure (fable A-F5)

## 제안 (Fable Lane-A $0 하한 · R2)
**아이디어**: corpus MI(연산자-답 ; 선언-극성 | ≤RF window) ≈0 이면 다리 부재는 *훈련 사고*가 아니라 CONV+corpus 가 **강제**한 것 = 재특성화(다리 강제는 못 함).
**메커니즘**: $0 — corpus 통계 MI 를 ≤RF window 로 제한 계산. [[H_9569]](min-cut) 과 자매.
**판정**: MI≈0 (사전등록 TOST 등가) ⟹ 절대 부재는 아키텍처-강제(음성을 *설명*). MI>0 인데 벽 존재 ⟹ 정보는 있으나 CONV 가 못 씀 = 다른 벽.
**한계**: 이건 벽을 *재특성화*할 뿐 다리를 *강제*하지 않음 → 단독 solution 아님(H_9557/H_9562 가 강제 시험).
**verdict-integrity**: MI 추정기 참값-0 pedestal 필수([[phi-estimator-needs-zero-truth-pedestal]]). 음성=TOST, 'ns' 금지([[negative-claims-need-tost-not-ns]]).

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9304(data-wall) 계열이나 *≤RF window 제한* MI = 국소성 조건부 신 하한(전역 MI 아님).
