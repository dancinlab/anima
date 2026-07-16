# H_9558 — 템플릿-클래스 정합 문맥 — Template-Class-Matched Context (address-model arm) (fable A-F2 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=fable A-F2
**lane:** BINDING / two-lane · 주소모형 추론시 검정
**related:** [[H_9557]] · [[H_9359]] · source: lab full R2-measure (fable A-F2)

## 제안 (Fable Lane-A 발산 · R2)
**아이디어**: 주소 = (stem 정체)×(표면-템플릿 클래스)(H_9359). 예측: **연산자 자신의 템플릿 클래스**로 쓴 문맥은 읽히고, 선언-템플릿 문맥은 **동일 byte 거리**서도 안 읽힌다. 주소 구조를 추론시 falsifiable 예측으로 전환.
**메커니즘**: [[H_9557]] 의 arm (d) — 선언을 연산자 템플릿 클래스로 재작성해 문맥 주입, arm (a)(선언-템플릿)과 동일 D 비교. flag 불요(매니페스트 arm).
**$0 pre-screen**: 두 arm byte 길이·위치 매칭(불일치>0.10 표준화 ⟹ 구성 KILL).
**판정(요지)**: PASS-template = (d) 추적 ∧ 선언-템플릿 미추적, 동일 D ⟹ 추론시 주소모형 확증(다리=템플릿 번역, 거리 아님). 둘 다 추적/미추적 = 주소모형 반증(거리·무차별).
**p7/p8**: 이진 flip-track·진리점수 없음.
**verdict-integrity**: (d) 추적을 '주소' 로 읽기 전 D-불변성 요구(거리효과 배제). H_9557 의 (c) 복사편향 통제 상속.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9334(C4 '틀린 키') 계승이나 *쓰기 후 저장소* 아닌 *추론시 문맥*에서 주소구조 검정 = 무-쓰기 신각도.
