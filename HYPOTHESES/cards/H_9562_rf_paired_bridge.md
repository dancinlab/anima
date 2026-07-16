# H_9562 — RF-내 짝 커리큘럼 다리 — RF-Paired Bridge (cheap-CPT + declaration transplant) (sol A-S1 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S1
**lane:** BINDING / two-lane · 저비용 훈련 + 이식 판독
**related:** [[H_9359]] · [[H_9358]] · [[H_9559]] · [[H_9565]] · source: lab full R2-measure (sol A-S1)

## 제안 (Sol Lane-A 수렴안 · R2)
**아이디어**: 짝 커리큘럼이 연산자↔선언 다리(reader)를 **RF 내 공동도달** 시에만 벌 수 있다. 그 뒤 **선언-만 극성 이식**이 *건드리지 않은* 연산자 판독을 인과 이동시키면 = 다리 획득.
**메커니즘 (저비용 훈련)**:
```
anima-py corpus atoms --rf-paired-bridge --rf-distance {inside,outside,postquery} \
  --pair-split cartesian-heldout --polarity-counterbalance <seed> --out <corpus>
anima-py train <base.clm> --continued-pretrain <corpus> --rf-paired-bridge --out <bridge.clm>
anima-py evaluate <bridge.clm> --xbind --rf-bridge-readout <manifest> --declaration-transplant <flip-corpus>
```
`inside`=D≤RF−δ · `outside`=D≥RF+δ · `postquery`=선언 후치. 정확 RF 는 serialized 메타서. counterbalanced stem×클래스 훈련·Cartesian stem×템플릿 held-out → 2차 CPT(선언 라인만). 주 DV = held-out 짝서 연산자 극성의 짝지은 변화.
**$0 pre-screen**: 정적 numpy(모델 forward 0) — 각 행 유효 방향 의존구간 계산: inside 는 선언값 byte·연산자 결정위치가 최소 1 공통 조상 공유 · outside/postquery 는 무공유 · 답byte·stem·극성·템플릿·길이·노출 매칭 · held-out 짝 부재∧양 marginal seen. 인과분류 100% 아니거나 leak 또는 표준화 불균형>0.10 ⟹ **훈련 전 KILL**.
**판정표**: PASS = inside 선언-이식이 ≥10/12 stem/seed 이동(≥2 seed·pooled perm p≤.01) ∧ outside/postquery ≤6/12·(inside−ctrl)≥4/12 ∧ 양성통제(훈련짝 readback ≥10/12). KILL = 어느 seed<10/12 or p>.01 or Cartesian-held 실패. INVALID = 연산자-포함 라인이 이식 CPT 진입·짝 leak·RF-arm 불일치·양성통제 실패·음성통제 ≥10/12.
**p7/p8**: 진리점수 없음. 학습된 reader 는 국소-조건부(공유저장소 획득 아님).
**verdict-integrity**: inside 우위인데 선언-이식 민감성 없으면 = 짝-캐시/FORM(다리 아님). 음성이 모든 CONV 다리 불가 증명 안 함(이 커리큘럼·RF 기하 한정).

## 🎨 FABLE 판정 — 이 카드가 **fork 결정 테스트** (2026-07-16 · [[H_9560]] ruling)
Fable 판정: two-lane 벽이 **(a) RF-formation-bound**(훈련 co-location 부재=DATA 벽·H_9304 정합) 인지 **(b) store-separation**(RF 내 공기해도 다리 없음) 인지를 가르는 **유일 결정 테스트 = 이 H_9562**. 이유: (a)vs(b)는 *훈련 co-location 반사실*로만 갈리고, 기록-재분석/추론시-문맥주입은 그 반사실을 실현 못 함 — **훈련 개입만** 가능.
- **D-arm 재anchor**: inside=D≤20(RF31 안전 밑)·outside=D≥64·postquery. ⚠️ **RF=9 아니라 측정 RF([[H_9560]] Step0 경험적 RF) 기준**([[H_9564]] #3793 파싱=31 을 Step0 가 engine-measured 로 확정한 뒤 fire).
- **게이트**: Step0(경험 RF)+Step1(H_9560 co-occurrence census) 통과 후 fire. 정적 RF=31 은 mirror-claim(미검)→Step0 없이 anchor 금지.
- **판정표(측정 RF anchor)**: inside 이식 ≥10/12·≥2seed·pooled perm p≤.01 ∧ outside ≤6/12 ∧ (inside−unpaired)≥4/12 ∧ 양성통제(훈련짝 readback)≥10/12 ⟹ **(a) RF-formation-bound**(co-location 커리큘럼=오프닝) · inside ≤6/12 ∧ 양성통제≥10/12 ∧ C0(선언-표면≥0.75) ⟹ **(b) store-separation**(RF 프레임 이 벽엔 死) · 양성통제<10/12 or C0<0.75 or Step0 RF≠파싱 or leak ⟹ **INVALID**(셀 읽지마·V2_1) · inside readback 우위인데 이식-둔감 ⟹ FORM/짝-캐시(다리 아님).
- **AGREES**: 병렬 [[H_9423]] S1(#3795) = 공학습 CLMS store-bridge 가 부모 conv 서 held-out 0.875(다리를 *모듈추가*로 설치) — 이 카드는 *plain conv 가 RF 내 짝으로 reader 스스로 학습하나*(모듈 없이) = 상보.
- **over-claim 방지**: inside-PASS = 커리큘럼 결과지 "재조합 열림" 아님(H_1584=건강한 훈련·정보흐름 존재 ≠ 정보 *사용*). EN=SCREENER/DIRECTIONAL.

## 상태
🔵 PROPOSED(🎨 fork-decider 승격) — 미실행. Step0/Step1 게이트 후 summer fire(a_fire_autonomous·cheap-CPT). **distinct-from-kills:** 가장 가까운 kill = held-out-stem 일반화(H_9327) — 이건 양 marginal seen·Cartesian 짝만 held·선언-만 사후개입으로 런타임 읽기 시험(zero-shot 어휘전이 아님).
