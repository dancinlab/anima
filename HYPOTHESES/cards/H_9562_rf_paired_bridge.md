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

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** 가장 가까운 kill = held-out-stem 일반화(H_9327) — 이건 양 marginal seen·Cartesian 짝만 held·선언-만 사후개입으로 런타임 읽기 시험(zero-shot 어휘전이 아님).
