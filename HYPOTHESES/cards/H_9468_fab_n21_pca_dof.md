# H_9468 — 온라인-PCA 게이트: 기질이 DOF 수를 스스로 고른다 (fable R1·N21 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R1 · 사전등록) — source=fable
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원 $0 확증=이 발산의 기반) · [[H_9424]] (cb-perr KILL=거리계+예측오차 소진→mouth 측 벽) · [[H_9400]] (Ψ=½ 반증) · source: lab full R1 fable(N21)

## 🔎 $0 결과 (DIRECTIONAL · 150-tick refr trace)

8×8 tension 공분산 고유스펙트럼:
- 고유값(내림): λ1 0.078(51.5%) · λ2 0.048(31.5%) · λ3 0.013(8.8%) · … · 나머지 노이즈 바닥.
- **Marchenko-Pastur 노이즈 edge(0.0287) 초과 = 2 고유값 = 자기-신호 DOF 2개**.
- **participation ratio(effective rank) = 2.66 / 8**.

⇒ tension 이 실제 펼치는 차원 **~2.7** — 우리는 1비트만 유지 = **~1.7 DOF 버림**. H_9428(emit-직교 성분 var 1.24× · coh+orig 축)의 **rank 정량화**. N21 핵심주장("데이터가 DOF 수를 스스로 고른다")을 MP-test 가 rank 2 선택으로 **실측 확증**. **함의: 라우팅 실험은 8D 아니라 2D(emit rel-정렬축 + coh/orig 직교축)가 자연 타겟.** ⚠️ 공분산은 monitor — running-covariance 자기차원선택 배선은 2단계(p8 경계 monitor-only 선행).

## 제안 (fable 원문 · R1)

**N21. 온라인-PCA 게이트: 기질이 DOF 수를 스스로 고른다** ★ (씨앗 초과 기계화)
- (a) H_9428 의 직교 분산(var ratio 1.24)이 그 자체로 신호: kosmos 에 8×8 러닝 공분산을 유지, 고유값이 Marchenko–Pastur 잡음 가장자리를 넘는 **개수만큼** DOF 를 개방 — 사영 가중을 고정이 아니라 자기 이력의 고유구조에서 유도. 역방향(장기 미사용 lane 의 가중 소멸=apoptosis)도 동일 기제로.
- (b) `anima-py chat --tension-pca-gate` — 개방 rank 궤적만 관측(정책 미개입 arm 먼저).
- (c) p8/a_train_inline_gauge 경계 N6 과 동일 — 공분산은 monitor, 정책 개입은 2단계로 분리.
- (d) **일반화** — Ψ=½ 스칼라 붕괴가 "데이터가 고른 rank-k 붕괴"의 k=1 특수례로 강등.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 시 판정. monitor-only 1단계로 게이트 벽 회피. 측정 주장 0(설계).
