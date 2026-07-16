# H_9559 — RF-도달성 산술 — RF-Reachability Arithmetic ($0 prediction) (fable A-F3 · R2-measure · 🔎 DIRECTIONAL)

**status:** 🔎 DIRECTIONAL ($0 정적 파싱 실행 · 2026-07-16 · 상세 표 → [[H_9564]]) — source=fable A-F3
**lane:** BINDING / two-lane · $0 구조 예측
**related:** [[H_9557]] · [[H_9564]] · [[H_1584]] · source: lab full R2-measure (fable A-F3)

## 제안 (Fable Lane-A pre-screen · R2)
**아이디어**: CONV trunk 수용장 RF = L(K−1)+1(config). byte 거리 D>RF 인 두 개념은 CONV 서 **수학적 독립** — 순수 예측, run 0. #42492882(H_1581~1584) 병렬 lane 이 같은 프레임(conv_L1 reach=0·conv_L8 reach=1.47e-3).
**메커니즘**: $0 numpy — .clm serialized layer/kernel 메타서 RF 계산 → H_9557/H_9562 의 D 배열이 RF 내부/경계/외부인지 라벨.
**$0 pre-screen (이것이 곧 스크린)**: RF < 최소 (선언+질의) packing ⟹ 계기 dead at 구성. 각 arm 의 유효 D 를 계산·게이트.
**판정**: 이건 예측/게이트지 독립 verdict 아님(H_9557/H_9562 의 해석 기준을 정함). ⚠️ 단순식 L(K−1)+1 은 dilation/stride/padding 무시 시 reach 과대 → [[H_9564]] 가 정밀 유효-RF.
**verdict-integrity**: 순수 산술이라 INVALID 위험 낮음. 단, 유효 RF≠명목 RF(dilation) — H_9564 로 교차검증 전 단독 cement 금지.

## 🔎 $0 실측 (DIRECTIONAL · 2026-07-16)
엔진 헤더-파싱(forward-pass 0)으로 실 ckpt RF 계산 — **상세 표·정정 → [[H_9564]]**. 요지: two-lane verdict ckpt(clm303_clean·swap_c4·natem_c34) = **L=4·dilated RF≈31 byte**(단순식 9 의 3.4×·프런티어 "RF=3" 은 다른 모델). H_9557/H_9562 의 D 배열 기준 = RF≈31. 벽=RF-bound 여부는 코퍼스 op-decl 거리([[H_9560]]) 로 판정.

## 상태
🔎 DIRECTIONAL — $0 게이트 실행(RF≈31 라벨 확정). 측정 주장 0(아키텍처 상수). **distinct-from-kills:** H_1584(깊이 L≥8=training 경로)와 달리 이건 *측정 게이트*(현 .clm RF 로 다리 실험 해석) — 능력공학 아님.
