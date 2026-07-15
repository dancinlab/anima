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

## 🧱 VERDICT — FILLER-OOD-BLOCKED (reading 1) · Δ-INJECT 이 ckpt서 종결 (natem_n2_main_s7 · aiden GPU · 2026-07-16)

**sequential 게이트가 두 단계서 발사·중단** (frozen-first · 제 역할):

**stage-1 행동 pre-gate = 🔴 FAIL 0/20** (`--delta-pregate`): carrier `지 않다` vs 신규필러 `고 있다` 전 어간
**같은 부호**(pol1→둘다 부정·pol0→둘다 긍정), carrier magnitude만 증폭(|m_c|>|m_f| 20/20 · median gap 6.89nat).
두 해석 미결: ① 필러 OOD vs ② 답이 어간-결정. Fable: 훈련된 flip0 carrier 부호만 가름.

**stage-2 결정적 통제 = arm B `고`(훈련 declarative 3B · `--delta-control`)**:

| arm | 결과 | 판독 |
|---|---|---|
| A 양성통제 `지 않다` | **20/20 sign-correct** | pipeline 신뢰(esign/frame 안 미끄러짐 · Fable caveat 3) |
| B 결정 `고` | **UN-flipped 20/20 · FLIPPED 0/20** | 훈련 `고`=어간극성(un-flip), `지 않다`=반대부호(참 +5.27 vs 고 −0.44·훌륭하 −14.3 vs +11.7·전 어간 반전) |

**⟹ VERDICT = FILLER-OOD-BLOCKED (reading 1)**:
- **carrier 는 인과적으로 소비된다** — 훈련 `고`(declarative)와 `지 않다`(negation)가 같은 어간에 **정반대** 답 ⟹ 연산자는 **실재**(stem-determined 반증). H_9327 "연산자 alive" **재확인·국소화**(carrier 바이트가 답 방향 결정).
- **`고 있다`는 OOD** — 미훈련 10B 필러가 dominant-frame(부정 basin)으로 default → pre-gate 의 same-sign 은 stem-결정 아니라 **OOD 아티팩트**. corpus-py-1⑧ carrier-census 벽 실증: 이 CPT 모델의 훈련 carrier = `지 않다`(10B)·`고`(3B) 뿐, byte-정합 비부정 carrier **없음**(H_9361 "option B unbuildable" 확증).
- **Δ-INJECT 이 ckpt서 종결**(Fable branch 1): 유일 대안인 `고`-vs-`지않다` Δ 는 **answer-row tautology**(두 arm이 구성상 반대답 → 주입=자명한 flip · H_9391 score-gate 공허형) + carrier-row Δ 는 carrier 바이트 정체성으로 교란. **비공허 Δ 는 byte-정합 훈련 carrier 쌍(연산자 의미만 다른)이 필요한데 이 ckpt 인벤토리엔 없다.**

**함의 (frontier)**: 벽은 **stem-lookup 으로 통합되지 않는다**(reading 2 반증) — SEEN 연산자는 실재하고 carrier-구동. 벽은 여전히 **held-out 전이 실패**(two-lane bridge 부재)이지 "연산자 부재" 아님. **NEXT rescue = H_9267 합성 XBIND corpus**(byte-정합 flip0/flip1 carrier 쌍을 구성상 훈련) — 이건 **측정(measure)을 재는 것이지 이 substrate 아님**(자연 자발창발 아님 · a_scale_honest_scope). 계기 전부 engine-native(`corpus deltainj` · `evaluate --delta-pregate`/`--delta-control`).

## 🔀 교차세션 기여 — H_9389 XBIND-BRIDGE prereg addendum (from H_9397 2-입력 기전 · a_parallel_session_compare)

H_9397 의 rescue(byte-정합 flip0/flip1 carrier 쌍 훈련)는 **병렬 H_9389 XBIND-BRIDGE 시간분리**(⭐Fable#1 레버 ·
`corpus xbind --bridge-split` 이 S_op 서 flip0+flip1 **둘 다 byte-정합 훈련** · phase-A CONFIRMED)와 **동일** ⟹
내 OOD 벽은 H_9389 설계에 **구조적으로 배제됨**(carrier-inventory 요건 충족). 중복 금지. **대신** 내 **2-입력 연산자**
발견(carrier=flip결정 × 어간=극성 · H_9388 어간읽음 + H_9397 carrier소비)이 H_9389 frozen 표의 **3개 구멍**을 드러낸다
— 그들 gate 소각 前 사전등록해야(실런은 EN-atoms 마이닝 대기 = 아직 안 소각 · burned-gate 회피). **그들 카드 편집 안 함**
— 내 surface 로 전달, 병렬 세션이 채택 결정:

1. **KILL 셀이 두 기전을 혼동한다.** "S_decl flip1 우연≤ ⟹ 다리부재 KILL" 인데, carrier×stem 상 **우연 이하**는 다리부재
   아니라 **어간-입력 전이 O · carrier-게이팅 held-out 미적용** = 모델이 훈련된 선언을 꺼내 **un-flip 극성**을 뱉어 계통적
   오답(=**half-bridge**: 선언→답 경로 O, carrier 게이팅 미일반화). 우연(=아무것도 전이X)과 **다른 발견·다른 후속**.
   측정 **후** 재독 = burned-gate ⟹ 지금 분리.
2. **짝 retention 통제 부재.** `sdecl_flip1.json` 만 emit. **S_decl flip0**(같은 게이트 어간의 훈련-선언 정확도) 없으면
   우연 flip1 이 판독불가(다리부재 vs 그 step 예산서 선언 자체 미보존). 매니페스트 1개 추가 · $0.
3. **CPT후 operator-alive arm 부재.** G-ALIVE(S_op flip1≥0.90)는 phase-A 한정. `cpt-destroys-what-corpus-omits`:
   선언전용 phase-B CPT 가 연산자를 전역 lobotomize 가능 → 그러면 "S_cpt flip1 미동"이 **죽은 계기 위에** 🔴 W_wt
   terminal 을 못박음(위조). **각 CPT arm 후 S_op flip1 재측정을 🔴 행 validity 게이트로 사전등록.**

세 구멍 다 측정면·$0·그들이 이미 emit 하는 매니페스트(+1개). 학습런이 낼 수 있는 **두 거짓 verdict(오독 KILL · 거짓
terminal)**를 정확히 de-risk. **arc 종결 후 STOP**(read-side 소진 · 활성 레버는 병렬 소유 · 3번째 계기 = proliferation ·
read-side-exhausted 교훈). 설계 Fable 5.
