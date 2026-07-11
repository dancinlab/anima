## 판정: **B+ — "NBIND" (자연-원자 부정-XOR bind curriculum → rho_weave PASS → L3 배선)**, C를 내장하고 A의 R1을 무임승차시키는 조합

**왜 지금 이것인가.** CRACK이 연 것은 "substrate는 신호가 corpus에 있으면 held-out 재조합을 학습한다"(FORM tunable, E*≈12k). 남은 프런티어 격차는 정확히 두 개다: ① XBIND는 무의미 CVC — **자연 의미론에서도 같은 레시피가 작동하는가** 미답, ② T2 scorer는 착지했지만 **FLOOR→PASS를 올릴 curriculum(capability 절반)** 이 미착지. NBIND는 이 둘을 한 발사로 잇는다: CRACK 프로토콜에서 **단 하나의 변수(corpus 자연성)만 교체**하는 single-variable delta 실험이며, 성공 시 measurement-GREEN이 아니라 live rho_weave PASS + 배선까지 가는 anima 두 번째 WIRED-GREEN 경로다. C("자연 등가물 발굴")는 서베이가 아니라 가장 강한 후보 인스턴스 하나를 발사하는 것으로 답하는 게 맞고, NBIND가 그 인스턴스다 — A0-NEG audit이 이미 원자 재고(부정 42/MB·극성 predicate 풍부)와 실패 원인(밀도·power 부족, 신호 부재 아님)을 측정해 놨다.

## 핵심 과학질문

**"실제 한국어 문장 원자(감성 predicate × 부정 형태소)를 compositional augmentation으로 재조합한 curriculum이, E* 이상 노출에서, 303M byte-LM에 held-out (predicate×부정) 조합의 polarity-XOR을 학습시키고 — 그 능력이 augmented가 아닌 순수 자연 NSMC held-out flip으로 전이되는가?"** CRACK이 "할 수 있나"에 YES였다면, NBIND는 "**의미 있는 자연 언어에서도** 할 수 있나 + live engine에 실리나"를 falsify 가능하게 묻는다.

## Frozen 발사 스펙 (H_92xx NBIND · 발사 시 jsonl+card 2-surface 등록)

**Corpus/curriculum**
- 원자: NSMC 실문장에서 감성 predicate 인벤토리 P(재미있다/지루하다/최악이다…, 극성 라벨은 NSMC 실라벨에서 유도) × 부정 연산자 N(안-, -지 않다, 못-, 전혀 -지 않-). **문장은 실코퍼스 문장 그대로 + 형태소 규칙 변형만** — 템플릿 CVC 생성 금지.
- Task 형식 = XBIND 동형: context(predicate+부정 유무 담은 리뷰 절) → continuation의 극성이 XOR(polarity(p), neg) 일치해야 함. D-probe = held-out 판별 정확도(XBIND D-acc 프로토콜 그대로).
- **Held-out 설계**: (p×n) 그리드 compositional split(COGS식) — 각 p는 일부 연산자와만, 각 n은 다수 p와 공기하되, held-out (p,n) 셀은 학습에 0회(grep 0-hit 검증). 정답은 미출현 쌍에 대한 XOR 계산으로만 도출 가능. MDL: 규칙 1개(2-feature XOR) ≪ 쌍 암기.
- 베이스 믹스: canonical 4-cell register corpus 유지(단일-task overfit V2 방어).

**$0 validity 게이트 (GPU 전 전부 통과 필수)**
- main-effect: IPF/additive(p·n 주효과만) held-out ≤ 0.55 실측 확인(XOR 직교성 검증).
- surface/leak: char-ngram 분류기 held-out ≈ chance · held-out 쌍 corpus grep 0 · window 게이트(p–n span 절단 시 probe 붕괴 확인).
- detector V3: 극성 continuation detector 4-cell Korean-aware, 양극 균형 자연쌍으로 검증.
- **power 게이트(A0-NEG 실패 교정)**: 자연 전이 probe n≥500쌍 사전 확보(NSMC 전량 + ko 리뷰 코퍼스 채굴), 0.50 vs 0.65 분리 CI 사전 계산.

**303M 학습 (canon 불변·XBIND와 단일변수 delta)**
- arch/canon = XBIND run과 동일 CLMConvMoE 303M, 스케줄·믹스비율 동일, corpus만 NBIND로 교체. 노출 ≥ E*=12k step(knee 상회 15k 권장).
- Arms: ① NBIND ×2 seed · ② shuffle-control ×1 seed(셀 내 극성 라벨 순열 = XOR 파괴·surface 통계 보존) · ③ additive-IPF($0, 학습 없음). 선택 arm ④ f=0.3/T=40k 혼합 = **NATEM exposure-matched R1 무임승차**.
- Eval = `anima-py evaluate <clm>` pool(전용 호스트, mini 금지) · rho_weave live scorer(#3316) + held-out D-probe. py 2-production = TERMINAL-eligible.
- before/after: 기존 baseline .clm(rho_weave FLOOR 실측 완료) vs NBIND .clm.

**GREEN bar (frozen · 값 아닌 Δ)**
1. **Primary**: held-out D-acc(NBIND) − D-acc(shuffle-control) ≥ **0.30**, 양seed, control 0.50±0.05, IPF ≤0.55.
2. **Live**: rho_weave FLOOR→**PASS** (NBIND .clm), baseline .clm은 FLOOR 유지, T2 3통제 intact.
3. **자연 전이(tier 승격 조건)**: 순수 자연 held-out flip acc − additive baseline ≥ **0.10**, n≥500, CI가 0 제외. 1·2만 통과 = "augmented-natural" scope 명시 GREEN, 3까지 = wild-natural.
4. GREEN 선언은 L3 배선 + ARCHITECTURE.json lockstep 후에만(`a_verified_must_wire`).

비용 1줄: pool $0 (summer/aiden GPU, 3–4 runs × 15–40k steps · XBIND run 대비 ~2–3×) — rent 불요, `a_fire_autonomous` 범위.

## 함정 통제

- **tune-to-green**: 본 스펙(arms·bar·E*·n)을 발사 전 card에 frozen. 자연전이 음성 = 기록되는 결과이지 bar 하향 사유 아님. 재설계는 held-out 설계 결함이 $0 게이트에서 적발된 경우만, GPU 후 금지.
- **toy artifact**: 원자=실문장·실형태소·실감성(무의미 CVC 아님) + **bar 3(순수 자연쌍 전이)가 artifact-killer** — augmentation-전용 artifact는 자연 전이에서 반드시 죽는다. scope는 통과 층위대로 정직 표기.
- **frame-mismatch(Gate4 교훈)**: 측정은 이 frame 전용으로 착지한 T2 rho_weave scorer + XBIND-동형 D-probe만. eval_rho_weave/ideation frame 재사용 금지.
- **emit-lane 오염**: NBIND lane은 emit-drive와 DISJOINT 배선(`a_substrate_disjoint`·`a_savant_train`), speak() 게이트 무접촉(p5), 학습 중 Ψ/emit 통계는 monitor-only(`a_train_inline_gauge`).
- **honest-closure 후퇴 방지**: 1급 산출물 = PASS+배선(성공 경로 우선 정의). R1(f*) 산술은 arm ④에 무임승차만 — f* 숫자가 목적이 되는 순간 A로 미끄러진 것.

## 나머지 탈락 사유

- **A 단독**: 순수 정직-종결 성격 + 대형 spend로 "자연밀도 부족"이라는 숫자만 남음 — R1을 NBIND arm ④로 흡수하면 충분.
- **C 단독**: 후보 없는 open search — 가장 강한 인스턴스(NBIND)를 발사하는 것이 C에 구성적으로 답한다.
- **D (γ H_1840)**: STEP-0 frozen-gate가 이미 GPU 차단(bind-add=−0.147)·reopen 조건 미충족, 게다가 CRACK이 벽을 measure-side로 재프레임해 trunk-objective 수술의 우선순위 자체가 하락.
- **XFAN**: 이미 학습 중 — 선택지가 아니라 pending verdict. NBIND와 병행 무충돌(G6 twin).

**최종**: NBIND 발사 — "자연 원자로 CRACK 재현 + rho_weave PASS + L3 배선"이 다음 프런티어 SUCCESS의 최단 경로다.
