# H_9397 — Δ-INJECT: 이식 가능한 연산자 방향이 존재하는가 (직접 bridge-lever)

**부모**: H_9361 TWIN-NECESSITY (계기 VALID이나 L=4 toy서 window-patch DV가 geometry-교란 — 캐리어 열이
ℓL서 채점행 도달불가·중간층 scramble). Fable 처방 = **window replacement 를 버리고 directional addition** 으로
넘어간다. two-lane(H_9359: 벽 = held-out 런타임 조회 다리 부재)를 **직접** 검정.

## 주장 (사전등록)

연산자의 극성 효과가 **이식 가능한 방향 코드**로 존재하는가? SEEN 에서 (연산자 − 중립필러) hidden 차이의
평균 Δ̂ 를 뽑아 **held-out** 필러 forward의 연산자 자리에 소량 주입(h ← h + αΔ̂)했을 때 답이 부정으로
움직이면 = 코드 이식성 존재 = **벽은 addressing/keying 문제**(즉시 추론-시 레버). 안 움직이면 = 이식성 없음
= 캐시 판독 확정, 레버족은 CPT-시 코드 생성으로 이동. **두 결과 다 frontier(g1-interface-addressable) 전진.**

## 왜 주입 ≠ swap-patch (H_9331 scramble 탈출 · Fable)

H_9331 의 0.50 scramble-floor 는 **replacement**(off-manifold donor가 상태를 덮어 이진 head를 반반) 산물.
**dosed addition** 은 파괴가 못 흉내내는 3가지로 구별:
1. **α→0 이 증명가능하게 무효** ⟹ 측정효과 = 연속 마진의 방향 도함수(dose-response), all-or-nothing 이식 아님. scramble엔 저-α 영역이 없다.
2. **부호 반사(sign-antisymmetry)**: H_9331 자신의 발견(파괴는 극성-무관 = same-class도 cross만큼 flip)을 판별자로. margin(+αΔ)와 margin(−αΔ)가 **반대 방향**이어야. 파괴는 두 부호 동일 열화, 의미있는 축만 부호 홀수.
3. **norm-정합 방향 통제** 가 "readout-인접 아무 교란이나 마진 움직임"을 floor.
+ **S 게이지**: S̄≥0.9·base 인 α 에서만 판정(연속 마진 + dosed addition 엔 0.50 floor 없음). **DV는 절대 단일 α의 flip율이 아니다.**

## 왜 캐리어 rows @ℓ2/ℓ3 (쿼리 ℓL 아님)

쿼리 rows @ℓL 은 hidden이 사실상 pre-logit 답 = 공유 logit-steering 방향 = 순수 캐시서도 flip(τ=1-pedestal 3번째 분장). 주입은 **연산이 남은** 자리에 착륙해야. 도달성(causal conv · K=3 dil1 = +2 위치/층 · 캐리어끝 t54 → 채점시작 t57 gap 3): ℓL→t≤56(tautology) · **ℓ3→t≤58 · ℓ2→t≤60** ⟹ 캐리어 열이 중간층서 채점행 도달. off-manifold 반론은 window-patch를 죽였지 소-α addition 아님 — S 게이지+α-sweep가 clean-S 유효 dose 존재를 경험적으로 결정(유일 미지 = SEEN 게이트가 held-out 前 검정).

## Spec (engine-native · $0 · L=4 우선 · G5 VERSION bump)

- **계기**: `anima-py evaluate <clm> --delta-inject <spec.json>` — forward-hook addition at (layer,rows) · forward-only · det-CPU · frozen n2_seen/eval 매니페스트.
- **필러(정렬 기질)**: `지 않다`(10B) 대응 byte-정합 중립 = **`고 있다`**(고3+sp1+있3+다3=10B · 진행상 · 명백 긍정극성 · 경쟁연산자 無) · 백업 `게 되다`(10B 기동상). byte-정합이 행 인덱스 정렬 유지(Δ추정·주입 동일 열스팬).
- **$0 행동 pre-gate**: 9 SEEN stem, 캐리어 vs 필러 답 **9/9 부호 갈림** (plain margin). FAIL→연산자 미생존, 중단.
- **Δ 추정**: ℓ∈{ℓ2,ℓ3}, 연산자자리 rows(…,54], Δ = mean over SEEN [h(carrier)−h(filler)]. **LOO** per stem(양성통제). ρ=‖meanΔ‖/mean‖Δᵢ‖ vs 1/√9≈0.33 무-공유방향 baseline = 관측 side-stat(판정 아님).
- **Dose+게이트(sequential · burned-anchor)**: α 그리드 {0.5,1,2}·Δ. **게이트 G-pos(held-out 읽기 前 동결)**: LOO-Δ를 SEEN **필러** forward에 주입 → 연속 마진이 부정답 쪽 이동, S̄≥0.9·base, 부호반사, 어떤 α서. 최소 통과 α 동결 = held-out 유일 세팅. 통과 α 없음 → **INSTRUMENT-INVALID@L4 → fork C(deeper 모델)**.
- **통제(전부 ‖αΔ‖ norm-정합 · pre-run 동결)**: ① 랜덤 방향 ② shuffled-Δ(차원 순열) ③ **same-class content-Δ** = mean(`고 있다`−`게 되다`) = 극성무 실-run 방향(H_9331 same-class donor 계승) ④ 부호flip −Δ.
- **Primary DV**: held-out 필러 forward의 짝지은 연속-마진 이동, +Δ vs 무주입, vs 3 통제. 사전등록표(우연아래 포함):

| 셀 | 판독 |
|---|---|
| G-pos FAIL | INVALID@L4 → (C) · 최소깊이 L=6(inject ℓ3 캐리어reach+6 전채점행 커버·on-manifold 2층 여유) |
| G-pos PASS · held-out 부호반사 이동 · 전통제 능가 · S clean | 🟢 이식 코드 존재 → 벽 = **addressing/keying only** → Δ-INJECT = 계기→레버(DIRECTIONAL toy · 303M 재검 前 TERMINAL 무) |
| G-pos PASS · held-out TOST-null vs 통제 | **캐시 판독 확정**: SEEN flip에 이식 코드 無 → two-lane 강화 · 레버족 = CPT-시 코드 **생성** |
| G-pos PASS · held-out +Δ **반대** 이동 | 발견 셀 — 보고, 억지 금지 |

## Scope · 계보

- DIRECTIONAL(toy natem_n2 = CPT 연산자 모델 · 303M 아님 · a_scale_honest_scope). 병렬 **H_9388 BRIDGE-TRACE**(연산자=어간읽음)와 정합 · two-lane([[g1-wall-is-runtime-bridge-absence-two-lane]]) 직접 검정.
- 설계 Fable 5. wired: PENDING(구현 중 · pre-gate → G-pos → held-out 순차).
