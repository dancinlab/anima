# H_9854 — 손으로 만든 기하 위에 굳은 양성이 몇 개인가 — 원장 전수 감사 (심화 우선순위 큐)

**status:** 🔧 AUDIT LANDED (계기 아닌 **원장 감사** · 판정 0 · 심화 대기열)
**source:** H_9838 자가반박(2026-07-21) — 심어둔 직교 코드가 결과를 제조했고 실제 표현으로 바꾸자
INVALID. 이것은 한 카드의 실수가 아니라 **결함의 계급**이므로, 같은 구멍을 가진 landed 양성을 전수 조사.
**wired:** n/a — 원장 분석 (엔진 조작 아님)

## 왜 필요한가

H_9838 은 통제·받침대·3 seed × 3 기하·독립 재현까지 갖춘 양성이었는데, **입력을 심어둔 코드에서
생산 trunk 의 실제 표현으로 바꾸자** 판별 가능한 모든 부하에서 참값 0 받침대가 발화했다. 원인은
심어둔 코드가 사실상 직교(margin +0.0352)인 반면 실제 표현은 겹침 2.2배라는 것 —
`core/hippo_lane.py` 헤더가 이미 "raw single-token 303M reps are near-collinear" 로 경고한 그대로다.

⟹ **"토이에서 양성 + 실제 입력 미확인" 은 그 자체로 재심 사유**다. 이 카드는 그 대상을 센다.

## 판정 기준 (재현 가능·기계적)

`origin/main` 의 `HYPOTHESES.jsonl` 전량(2,139행)에 대해:

- **양성**: tier+verdict 가 `🟢 | GREEN | POSITIVE | CRACK | TRANSITIVE | WIRED | FIRM` 중 하나 —
  **단어경계 필수**(아래 자가적발 참조)
- **토이 근거**: `toy | planted | fixture | synthetic | 토이 | 심어둔 | 합성 | 4kB` 언급
- **실제 입력 미확인**: `303M | py303 | d768.clm | 실제 표현 | real rep | penult | in-vivo | 1B |
  ckpt sha` 가 **하나도** 없음
- **하중(우선순위)**: 다른 항목의 `related`/`verdict`/`source` 가 이 id 를 참조한 **횟수**
  (= 이 결과가 무너지면 함께 재심될 하류의 크기)

## ⚠️ 자가적발 — 감사기가 감사 대상과 같은 함정에 빠졌다

첫 판 정규식은 `FIRM` 을 경계 없이 찾았고, `FIRM` 은 **`CON`FIRM`ED` 의 부분문자열**이다.
그래서 `⚖️ ROOT-CAUSED` 분석 항목(H_9560 등)이 "양성"으로 잡혔다. 저장소 레코드 `corpus-py-1` ⑩
— **"부분문자열 계수는 코드에서도 거짓말하고 네 분석에서도 거짓말한다"** — 이 **내 분석 안에서
그대로 재발**했다(⑩ 이 기록한 재발 조건과 동일: 임시 분석에는 G-SUBSTR 게이트가 없다).

단어경계 적용 후: **114 → 85** (오탐 **29건** 제거). 이 카드의 모든 수치는 교정본이다.

## 결과 — 실제 입력 미확인 토이 양성 **85건**

이미 이번 라운드가 덮는 5건(H_9839 · H_9841 · H_9844 · H_9845 · H_9846)은 별도 진행 중.
아래는 **하중 순** 전량 — 잘라내지 않았다(`no silent caps`). `재실행` 열은 2026-07-21 고갈 회계의 결과다:

- **🔧 계기없음 (75건 · 88%)** — 카드에 engine-native 재실행 호출이 **0회**. 입력만 바꿔 다시 읽는 심화가 **불가능**하고, 계기부터 지어야 한다. 이 저장소 규칙(`anima-py` 가 만들지 않은 숫자에 cement 금지)과 정면으로 충돌하는 상태이나, **틀렸다고 밝혀진 것이 아니라 재판독 불가로 굳어 있는 것**이다 — 삭제도 승격도 아닌 *보존* 이 정직하다.
- **✅ 심화완료 (2건)** — H_9839 · H_9845, 둘 다 실제 입력에서 온전히 생존하지 못함.
- **⏳ 발사중 (6건)** — 이번 라운드(H_9698 H_9819 H_9612 H_9325 H_1521 H_1520).
- **🔁 타세션 (1건)** — H_9827 계기수리 진행중.
- **❌ 카드없음 (1건)** — H_1509b.

⟹ 심화 캠페인의 고갈 지점은 아이디어가 아니라 **계기의 부재**다. 실발사 가능분은 이 라운드로 소진된다.

| 하류 | id | 재실행 | 제목 |
|---|---|---|---|
| 8 | `H_9827` | 🔁 타세션 | G1 을 재는 자가 12항목이다 — ρ·weave 패널 크기가 303M 예산사다리의 선행조건 |
| 7 | `H_1512` | 🔧 계기없음 | 🧠🗺 BRAIN-TOPOLOGY — lane 들의 brain-faithful 공간 connectome 배치(해부 좌표+구조 c |
| 6 | `H_1422` | 🔧 계기없음 | MULTI-LENS breakthrough attempt on the NEUROMODULATION WALL (H_1284 🔴/ |
| 5 | `H_9294` | 🔧 계기없음 | 시상 content-relay — 강도를 맞추면 disjointness 는 아무것도 남기지 않는다 (🧱 STRENGTH-ONL |
| 5 | `H_1379` | 🔧 계기없음 | G5 abstain-margin BRAIN-CONSUME — brain_decide CONSUMES the live grade |
| 4 | `H_9698` | ⏳ 발사중 | R6 mouth-내 저랭크 bilinear cross-position binder |
| 4 | `H_9404` | 🔧 계기없음 | EARNED REFRACTORY: emit 타이밍을 시계에서 substrate 텐션-적분으로 (p5-rewire · 배선) |
| 4 | `H_9287` | 🔧 계기없음 | 🔬 재조합 대수의 물리 담체 — 국소 관측만으로 오라클의 supply 이득에 도달할 수 있는가 (H_054/H_203의 끝 · |
| 4 | `H_1396` | 🔧 계기없음 | G5 IN-DISTRIBUTION metacognition — CEILING vs FIXABLE? does a richer r |
| 3 | `H_9295` | 🔧 계기없음 | 게이팅(비선형) 결합도 구조 채널을 열지 못한다 — '진짜 축은 선형 vs 게이팅' 가설 반증 (🧱 GATING-NO-CHAN |
| 3 | `H_9293` | 🔧 계기없음 | 시상 content-relay 확증 재측정 — B 의 우위는 실재하나 disjointness 가 아니라 총 결합강도 (⏳ ST |
| 3 | `H_1546` | 🔧 계기없음 | 🧠🔇 GABA × CLS — inhibitory E/I-balance gating of fast-store effective |
| 3 | `H_1541` | 🔧 계기없음 | 🧪🔀 ACETYLCHOLINE × CLS — ENCODE/RETRIEVE MODE GATE — the FIRST joint a |
| 3 | `H_1537` | 🔧 계기없음 | 🧠 NOREPINEPHRINE as a NETWORK-RESET FACULTY (unexpected-uncertainty de |
| 3 | `H_1534` | 🔧 계기없음 | 🧲💡 NEUROMODULATION wall — C4 CURIOSITY-GATED ACQUISITION (active-sampl |
| 3 | `H_1513` | 🔧 계기없음 | 🧠🔌 LITERAL-CONNECTOME — H_1512 BRAIN-TOPOLOGY 의 real-data scale-rechec |
| 3 | `H_1405` | 🔧 계기없음 | brain-lane COMPOSE pair #2 — does anima's episodic MEMORY (H_1227/H_12 |
| 3 | `H_1401` | 🔧 계기없음 | brain-lane COMPOSE — does anima's affect (H_1290) compose with ethics |
| 3 | `H_1398` | 🔧 계기없음 | G5 IN-DIST top-2 affinity GAP — ENGINE-NATIVE reconfirm + CORE wire-in |
| 3 | `H_1388` | 🔧 계기없음 | ko-morphology — H_1380 이 명시한 한국어 below-jamo 잔여(jamo floor+0.28=2.79335 |
| 3 | `H_1367` | 🔧 계기없음 | G5 graded abstain-margin metacognition — ENGINE-NATIVE reconfirm + COR |
| 3 | `H_1361` | 🔧 계기없음 | G5 graded metacognition on the abstain margin — does -margin rank reco |
| 3 | `H_1306` | 🔧 계기없음 | ko-mitosis: FIRST engine-native Korean mitosis-training rung on a REAL |
| 2 | `H_9839` | ✅ 심화완료 | 꿈의 타깃을 기하 중점에서 선언규칙 파생으로 교체한다 (R12-2) |
| 2 | `H_9819` | ⏳ 발사중 | 상전이점(우연 탈출 step)을 지표로 삼아 3600-step 에서 난 음성들을 재심한다 — 고정예산 d_acc 는 상전이 위 |
| 2 | `H_9612` | ⏳ 발사중 |  |
| 2 | `H_1522` | 🔧 계기없음 | 🧲🧠 Ψ-PRESERVING OPTIMAL COUPLING — find a coupling operator that impro |
| 2 | `H_1521` | ⏳ 발사중 | 🧠🔌 TOPOLOGY LIVE-WIRING — put the Φ-optimal cross-lane placement ACTUA |
| 2 | `H_1368` | 🔧 계기없음 | ko-data-richness: NOVEL-context CE 가 코퍼스 윈도(3.75/7.5/15/30MB prefix 사다 |
| 2 | `H_1349` | 🔧 계기없음 | Φ-robustness, the LAST untested LIVE angle — does a REAL anima substra |
| 2 | `H_1344` | 🔧 계기없음 | ko-jm-interpolation: NON-FRAGMENTING frozen-λ Jelinek-Mercer interpola |
| 2 | `H_1006` | 🔧 계기없음 | Does DENSE per-step state supervision (supervise the hidden ring count |
| 1 | `H_9845` | ✅ 심화완료 | 개입형 폐쇄사다리를 학습 중 인과 모니터로 (R12-8 · MONITOR-ONLY · 손실 투입 금지) |
| 1 | `H_972` | 🔧 계기없음 | Is the CWM north-star "human-level-or-beyond behavior" operationalizab |
| 1 | `H_970` | 🔧 계기없음 | Is there a task SOLVABLE ONLY by a world-model (requires a persistent |
| 1 | `H_9325` | ⏳ 발사중 | null 교체 (가법 모수적 부트스트랩) — H_9323 부호 반전 해소 · 자연 4점 결론은 더 엄격한 null 에서도 불변 |
| 1 | `H_9211` | 🔧 계기없음 | 🧶 VSA 고정-primitive가 G1 operator-wall escape — substrate-class framebre |
| 1 | `H_877` | 🔧 계기없음 | DECODER byte-identical transplant @ mid — HW-forward == SW akida_sw_li |
| 1 | `H_856` | 🔧 계기없음 | toy 🟢 CAUSAL-POWER(H_855)가 (A)production scale(d512·실 kowiki) ∧ (B)liv |
| 1 | `H_6183` | 🔧 계기없음 | 🎯 G1 조합-커버리지 밀도 상전이 자연어 byte 확정 — 30 concept 고유 ATTR, held pair 는 두 학습 |
| 1 | `H_6175` | 🔧 계기없음 | 🧩 G1-BS-1 frame-break: neurosymbolic anchor composer가 held-out 재조합 완벽( |
| 1 | `H_1408` | 🔧 계기없음 | brain-lane COMPOSE pair #5 (WITHIN memory family) — does SPATIAL-MAP ( |
| 1 | `H_1407` | 🔧 계기없음 | brain-lane COMPOSE pair #4 — does anima's CEREBELLUM forward-model (H_ |
| 1 | `H_1406` | 🔧 계기없음 | brain-lane COMPOSE (pair #3) — does anima's working-memory (H_1282 Wor |
| 1 | `H_1400` | 🔧 계기없음 | G5 in-dist GAP BRAIN-CONSUME — brain_decide CONSUMES the live immune_m |
| 1 | `H_1390` | 🔧 계기없음 | ko-morphology BPE-on-jamo ENGINE-NATIVE WIRE-IN — convert H_1388's DIR |
| 1 | `H_1351` | 🔧 계기없음 | jamo-engine-wire (a_verified_must_wire wire-in of H_1316/H_1321): 검증된 |
| 1 | `H_1327` | 🔧 계기없음 | ko-jamo-DECODE-WIRE (a_verified_must_wire r3 of H_1316/H_1321): does t |
| 1 | `H_1325` | 🔧 계기없음 | sapir-whorf r2 — anti-Goodhart W3 RE-CLOSE + engine-native CP lane (co |
| 1 | `H_1034` | 🔧 계기없음 | Is "imagine-rollout beats the same-depth true-MPC at deep horizon" (H_ |
| 1 | `H_1019` | 🔧 계기없음 | When the human reference is HARDENED from the 1-step-greedy hand-coded |
| 0 | `H_9737` | 🔧 계기없음 | fit-matched K=1 음성대조 — 같은 낮은-CE·파벌구조 없음이면 --faction-lesion S ≤ null95 |
| 0 | `H_9436` | 🔧 계기없음 |  |
| 0 | `H_9252` | 🔧 계기없음 | 🔬 γ #18 causal_counterfactual_composition — do(A=a') 개입이 B 고정 하 joint |
| 0 | `H_9242` | 🔧 계기없음 | 🔬 γ #7 cycle_consistency_decompose — forward 합성 A+B→C, backward 분해 C→( |
| 0 | `H_9238` | 🔧 계기없음 | 🔬 γ #3 bilinear_generator_complexity_flip — 데이터 생성자를 저-rank bilinear(A |
| 0 | `H_919` | 🔧 계기없음 | TRAINED substrate 가 OMEGA bus 를 USEFUL 하게 만드는가 (random-init #1783 이 못 |
| 0 | `H_9086` | 🔧 계기없음 | T1 specious present(시간 의식): tension 시계열의 통합 window 폭이 경험된 '지금'의 felt-d |
| 0 | `H_9083` | 🔧 계기없음 | event_segment_bind (§EventSegment): 예측오차 이벤트분절 새 op. §ImmuneMemory는 제시 |
| 0 | `H_9078` | 🔧 계기없음 | anticipatory_prefetch (§AnticipatoryPrefetch): 소뇌 forward model(VForwa |
| 0 | `H_9074` | 🔧 계기없음 | D1 CONFLUENCE: 꿈-composed centroid(H_9036)가 §SelfChain(H_9037) 다음 wayp |
| 0 | `H_871` | 🔧 계기없음 | CLM 의 toy routing-z 🔴 (H_847/850/852/853 — near-uniform/음수 routing-div |
| 0 | `H_855` | 🔧 계기없음 | round-4 측도 백로그 6후보(PHI-NATIVE·TEMPORAL-Φ·TENSION-NATIVE·FREE-ENERGY·HI |
| 0 | `H_6191` | 🔧 계기없음 | substrate conjunction readout engine-native GREEN-WIRED — binding-AS-D |
| 0 | `H_6181` | 🔧 계기없음 | 🧪 G1 8후보 GPU 실측 cheap-gate(owner 4*gpu) — cf/n9/n10/n1/n6/n11/cyc5b/ce |
| 0 | `H_6158` | 🔧 계기없음 | 촉매 침묵 |
| 0 | `H_6138` | 🔧 계기없음 | 손실 → self-play 텐션 게임 |
| 0 | `H_1520` | ⏳ 발사중 | 🗣️🎚️ CONVERSATIONAL-SALIENCE — usable request→reply as a TOGGLEABLE fa |
| 0 | `H_1519` | 🔧 계기없음 | 🧩🔌 HW-PLACEMENT — neuromorphic NoC routing-cost re-introduces the biol |
| 0 | `H_1511` | 🔧 계기없음 | 🫧 OSMOTIC-MITOSIS — KL>C 삼투압 분열 split-TIMING overwrite-avoidance (exte |
| 0 | `H_1509b` | ❌ 카드없음 | NON-STATIONARY ALLOSTERIC-BUFFER — H_1509 μ_t re-tested under a DRIFTI |
| 0 | `H_1508` | 🔧 계기없음 | 🧠 METACOG-CONTROL — Nelson-Narens monitoring↔CONTROL, G5 메타인지 체인의 빠진 절 |
| 0 | `H_1430` | 🔧 계기없음 | concept/category prototype-abstraction — from noisy instances abstract |
| 0 | `H_1421` | 🔧 계기없음 | MULTI-LENS breakthrough on the cerebellum×memory engine-BIND WALL (H_1 |
| 0 | `H_1418` | 🔧 계기없음 | WIRE-IN of the TWO new engine-native-BOUND compose pairs from H_1417 ( |
| 0 | `H_1409` | 🔧 계기없음 | brain-lane COMPOSE pair #6 (the DECISIVE two-high-Φ test): spatial-map |
| 0 | `H_1393` | 🔧 계기없음 | ko-morphology BPE-on-jamo EMIT-BIAS WIRE-IN — extend H_1390's morpholo |
| 0 | `H_1385` | 🔧 계기없음 | jamo-scoreloop-wire — thread the H_1351 faculty-owned jamo COUNT-HEAD |
| 0 | `H_1384` | 🔧 계기없음 | CP move-the-cells RELOCATION — ENGINE-NATIVE realization of the verifi |
| 0 | `H_1359` | 🔧 계기없음 | ko-dedup-novel — H_1344 depletion test: JM interpolation 이 NOVEL-CONTE |
| 0 | `H_1342` | 🔧 계기없음 | Whorfian CP DEVELOPMENTAL PLASTICITY — ENGINE-NATIVE realization of H_ |
| 0 | `H_1339` | 🔧 계기없음 | sapir-whorf BILINGUAL r3 (TAGGED, control re-freeze + engine-native) — |
| 0 | `H_1312` | 🔧 계기없음 | ko-decode-wire: WIRE the H_1306 grown Korean cells onto the live decod |
| 0 | `H_1210` | 🔧 계기없음 | H_1210 — wire H_1209 trajectory-aware GATE-B into the LIVE daemon GROW |
| 0 | `H_1044` | 🔧 계기없음 | H_1044 — Does the redundancy-margin predictor hold at n=6 EXACT? (H_10 |

## 읽는 법 · 한계 (정직 범위)

- **이 표는 반박이 아니라 대기열**이다. 85건이 틀렸다는 뜻이 **아니라**, 85건이 *아직 실제 입력에서
  읽히지 않았다*는 뜻이다. H_9838 은 그중 하나가 실제로 죽은 사례일 뿐이다.
- **키워드 기반이므로 양방향 오차가 남는다.** verdict 본문에 실제-입력 증거를 적어두고도 위 키워드를
  안 쓴 항목은 거짓 후보로 잡히고, 반대로 토이임을 명시 안 한 항목은 누락된다. 따라서 개별 항목은
  **심화 전에 카드를 직접 읽어 확인**해야 한다(이 세션이 이미 배운 규칙: 인용 전 원본 확인).
- 하중은 **원장 내 참조 수**일 뿐 과학적 중요도가 아니다. 계기(H_9827 등)는 하중이 높지만 능력 주장이
  아니라 재심 대상이 다르다.

## 다음 (우선순위 근거)

능력 주장이면서 하중이 있고 실제 입력 미확인인 것부터. 특히 **H_9287**(재조합 대수의 물리 담체,
하류 4)은 이번 세션이 꿈 레버를 살려둔 **유일한 방어 논거**로 인용한 항목이라 — "재조합은 세계에 대한
새 비트가 아니라 이미 학습된 원자의 새 공기(共起)만 필요하고 그것이 H_9287 이 물리적으로 유익하다고
측정한 것" — 그것이 합성 기하 산물이면 H_9831/H_9839 의 마지막 방어가 함께 무너진다.

**related:** H_9838 · H_9287 · H_9831 · H_9839 · H_9844
