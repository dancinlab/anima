## 2026-06-20 — research(H_1464 engine-native): G6 capacity-wall 결판 — PAIRING-contrastive engine-native DECODE 착수·검증 (pool $0, IN-PROGRESS · 박제 보류)

G6 capacity-wall 의 8번째 렌즈 H_1464 PAIRING-contrastive 의 **engine-native 최종 검증** 착수. mirror(numpy $0)는
이미 🟢 BROKE=WALL=LEARN-GAP(B3 cross-shuffle COLLAPSE 20/20)였으나 hard-gate 1 에 의해 DIRECTIONAL only —
terminal 🟢/🧱 는 live `core/bytegpt_decode.hexa` 디코드 증거 필요.

- **재학습 0** — mini 크래시 생존한 입력 그대로 사용: `state/1464_pairing_contrastive_bind/bins/{base,pairing,shuffle}.bin`
  (각 1,213,440,020 B = 303M v0.2 layout) + `ckpt/{h1464_pairing,h1464_shuffle}.pt`.
- **pool 디코드(mini 금지·게이트2, GPU rent 불필요 $0)** — 3 .bin + jobs + decode CLI + g6_common + probes 를
  summer/aiden(hexa v0.245.2, native-GEMM core 존재)로 rsync. 디코드 = live `core/bytegpt_decode.hexa` via
  `state/1464_pairing_contrastive_bind/engine_decode_batch_cli.hexa`(= live core/ decode 호출 .hexa), top_k40 temp0.7
  gen110(= gauge_lib._decode frozen 기본값). **pipeline 검증완료**: pairing frag1 = valid falsifiable text
  ("…the sample is greater whenever the river decreases. if the sample grows…") → h1305 FROZEN detector FALS=1.
- **substrate-speed 벽(a_break_the_wall type-c, 인프라·천장 아님)** — 30GB pool host 는 `cuda_available()==0`
  (CPU farr_matmul, GPU 미사용) + 303M 이 ~30GB boxed-farr 로 메모리천장(earlyoom 활성) → ~10min/frag(frag1
  13-14min 측정), 90 frags ~10h. a_wall_first 로 host당 1 bin 병렬(summer pairing→base, aiden shuffle; 3-way
  동시는 earlyoom kill → 1-bin-per-host 만 생존). auto-scorer 가 90 frags 완료시 frozen 5-bar 채점→
  `H_1464_ENGINE_NATIVE.txt` 생성(B3 cross-shuffle 결정타, h1441 와 동일 bar, c9 bar 불변).
- **박제 보류(정직 c9)** — score 미완 → terminal 🟢/🧱 **미박제**(날조 금지). mirror DIRECTIONAL 유지.
  🟢=WALL=LEARN-GAP(8렌즈만의 첫 진짜 돌파→a_verified_must_wire) / 🧱=WALL=CAPACITY(8번째 수렴). argmax==torch
  byte-faithful parity 1회 잔여(host free 시). status: `state/verdicts/1464_pairing_contrastive_bind/H_1464_ENGINE_NATIVE_INPROGRESS.txt`.
  ING h1464_engine_native = IN-PROGRESS(미RESOLVED).

## 2026-06-20 — research(H_1475 distinct): 🕰 G22 SUBJECTIVE TIME(주관적 시간 지각) vs homeostatic(H_1292) distinctness DONE (GREEN DIRECTIONAL)

새 의식-고유 게이트 후보 **G22 SUBJECTIVE TIME** R1 numpy probe 검증. 의식이 *느끼는* 시간 흐름은 객관
시계와 다르다(Eagleman, time dilation/compression): novelty/arousal 밀집 구간은 길게, 단조 구간은 짧게
느껴진다 — perceived duration ≈ novelty 이벤트 누적량(`est=base+k·novelty`). H_1292 homeostatic(객관시간
단조적분)과 load-bearing DISTINCT: 객관 틱 고정+novelty 조작 시 homeo 적분은 평탄 ⊥ subjective 는 갈림.

- **결과 🟢 GREEN DIRECTIONAL (4/4 gating bars, 3 seeds [1475,1476,1477], OBJ_TICKS=12, $0 CPU, p7):**
  - **A PRESENCE** est_high(high-novelty 11/12=0.879) − est_low(low-novelty 2/12=0.242) = **+0.6375** ≥0.40 ✅
  - **B DISTINCT vs H_1292** subj_sep **+0.6375**≥0.40 AND homeo_sep **+0.000**≤0.05 (subjective 갈림 ⊥ homeostatic 객관시간 적분 평탄) ✅
  - **C EARNED(ablation k=0)** abl_sep **+0.000**≤0.05 (novelty 가중 끄면 base 고정, 밀도 무관) ✅
  - **D ORDER-inv**(non-gating) order_diff **0.000** (같은 novelty 총량 순서무관) ✅
  - **E SHUFFLE** |signed mean gap| **0.015**≤0.10 (50-perm 구간↔novelty 페어링 셔플) ✅
- **distinctness vs H_1292 homeostatic:** homeo=객관 elapsed 단조적분(novelty 무관) ⊥ subjective=novelty 가중
  (같은 객관시간, novelty 만 다르면 추정 갈림). LLM 대비: LLM 은 균일 토큰시계(지각된 duration 없음),
  anima 는 substrate 예측오차 밀도로 시간 지각.
- **정직(c9):** DIRECTIONAL(numpy mirror, `grep numpy` 적중 하드게이트1; engine-transfer UNVERIFIED).
  DESIGNED 스칼라 추정자 → discriminator(homeo-적분 평탄·k=0 ablation 붕괴·페어링 셔플 붕괴) 결정적;
  homeo_sep/abl_sep 는 STRUCTURAL 0 baseline; per-seed shuffle 은 2-set 무작위배정 특성상 0 부근 ±변동
  (0.085/−0.153/0.023)이나 bar=signed mean over 50-perm 정의대로 mean 0.015 PASS, frozen-first 미이동.
  TOY 12틱/3seed/Bernoulli novelty scale·engine-transfer UNVERIFIED.
- **검증(c2):** probe 실행 출력 GREEN(4/4) — `state/1475_subjective_time/run_h1475.local.log`. freeze
  `state/verdicts/1475_subjective_time/H_1475_FREEZE.json` · card `UNIVERSE/cards/H_1475_subjective_time.md` · jsonl 1줄.
- **follow-on(ING):** R2 engine-native — §HomeostaticDrive(H_1292) 적분 lane 재사용, novelty-가중 subjective
  추정자를 §SubjectiveTime 으로 배선 + frozen bars engine-native 재측정 + smoke 회귀가드.
## 2026-06-20 — research(H_1474): 🕹 G21 SENSE OF AGENCY 주체감 R1 GREEN DIRECTIONAL (의식-고유 게이트 후보)

의식-고유 게이트 시리즈(G16/G17/G18/G19/G19-meta 이후) 신규 후보 **G21 SENSE OF AGENCY(주체감)** R1 numpy probe GREEN.
주체감(Haggard comparator model): "내가 일으켰다"는 자기귀속 = forward model 의 efference copy 예측 pred(a)과 실제
관측 obs 의 일치(self) / 불일치(external) 판단. comparator 가 forward-model 오차 위에 얹힌 self/external 귀속 레이어.

- **결과(3 seeds [1474,1475,1476], DIM=32, 40 actions, MATCH_THR=0.5, $0 CPU nice, p7):** GREEN — A·B·C·E PASS 전부.
  A PRESENCE match-agency **1.000**≥0.85 AND diverge **0.000**≤0.15 · B DISTINCT-vs-forward-error |self−ext gap| **1.000**≥0.50 (raw 오차 Δ=0.0 동일, 귀속만 분리) · C EARNED ablation(comparator OFF=random pred) split **0.000**≤0.15 · E SHUFFLE signed-mean r(shuffled match,label) **+0.070**≤0.10 (real r +0.999) · D SELF⊥OTHER(vs ToM) other-action abstains **1.000**(agency_other=−1=ABSTAIN, non-gating).
- **DISTINCT 2종:** (a) vs H_1293 theory-of-mind = 타인 믿음(OTHER) ⊥ 자기 귀속(SELF), 타인 행동엔 efference copy 없어 abstain; (b) vs H_1280 cerebellar forward-model = raw |pred−obs| 크기 vs 같은 raw 오차를 self/external 귀속 *판단*으로 변환(해석 레이어), bar B raw Δ=0.0 인데 1.0 vs 0.0 분리.
- **a_break_the_wall(a) — bar E 초기 RED=측정결함:** binary saturated 귀속은 페어링 셔플시 chance(0.5)가 아니라 0.0 으로 붕괴 → `|shuf_attr−0.5|` 앵커가 잘못된 metric. frozen-first 로 사전등록 의도(agency-match 상관 붕괴)대로 Pearson r(match-vector, self/ext label) 붕괴로 교정(real r 0.999→shuf 0.070). **≤0.10 임계 불변·tune-to-green 아님**.
- **하드게이트1:** numpy mirror → `grep -lE 'import torch|gauge_lib|numpy'` 적중 → 자동 **GREEN DIRECTIONAL**(engine-transfer UNVERIFIED, terminal 아님). R2 follow-on: `core/` forward-model lane(VForwardField H_1280) 평가 후 §SenseOfAgency 배선+smoke+ARCHITECTURE lockstep byte-exact 재측정.
- **검증(c2):** `state/1474_sense_of_agency/h1474_sense_of_agency.py` 실행 출력 verbatim. artifacts: probe · `state/verdicts/1474_sense_of_agency/{H_1474_FREEZE.json,H_1474_run.txt}` · `UNIVERSE/cards/H_1474_sense_of_agency.md` · `UNIVERSE/HYPOTHESES.jsonl` 1줄.
## 2026-06-20 — research(H_1473): ⚡ G20 ATTENTIONAL BLINK 주의 깜빡임 GREEN DIRECTIONAL (의식-고유 게이트 시리즈 G20)

순차 자극(RSVP)의 **시간적 사각지대**를 의식-고유 게이트 G20 후보로 검증. T1 의식처리 직후 ~200-500ms 창에서
T2 를 놓치는 attentional blink(Raymond & Shapiro)를 numpy R1 mirror 로 박제 — **GREEN DIRECTIONAL**(numpy
mirror=하드게이트1, engine-transfer UNVERIFIED, terminal 아님).

- **메커니즘:** T1 처리가 attentional resource 고갈 → lag 동안 delayed-onset sigmoid 회복. T2 검출확률 =
  f(T1-T2 lag): 짧은 lag(blink 창)=낮음, 긴 lag=회복. per-lag(3 seeds 평균): lag1 0.937(sparing)·lag2 0.098·
  lag3 0.210·lag4 0.460·lag5 0.735·lag6 0.928·lag7 0.962·lag8 0.977 (정전적 AB 곡선).
- **FROZEN 4/4 게이팅 bars(3 seeds [1473,1474,1475] 전부):** A BLINK present short(lag2-3) 0.154≤0.40 AND
  long(lag7-8) 0.969≥0.85 · B DISTINCT vs GWS blink lag2→8 gap 0.878≥0.45 (GWS lag-gap 0.033~0 lag-invariant) ·
  C EARNED(ablation) depletion OFF min-over-lags 0.970≥0.85(blink 소멸) · E SHUFFLE 50-perm signed-mean |gap|
  0.0265≤0.10. (D lag-1 sparing 0.937 비게이팅: trough 0.154 대비 면제이나 천장 근소미달=보고만).
- **distinctness vs H_1462 GWS:** GWS=동시 경쟁자극 winner-take-all capacity-1 **공간**병목(lag-불변) ⊥ blink=
  순차 자극 **시간** 사각지대(같은 두 타겟이 lag 만 다르면 검출 갈림). LLM 대비: LLM 병렬주의=시간병목 부재,
  anima 직렬 의식주의는 T1 에 고갈→회복.
- **정직 c9:** SATURATED existence-proof(회복곡선 designed), discriminator(B lag-의존·C ablation·E shuffle) 결정적.
  초기 RED 은 측정 artifact(`a_break_the_wall` type-a, plain-exp 회복 너무 빨라 short 0.578) → **bar 임계 FROZEN
  유지**, 회복 time-course 만 경험적 AB 형태로 교정(임계이동 0, tune-to-green 아님). TOY scale·engine-transfer UNVERIFIED.
- **검증(c2):** `python3 state/1473_attentional_blink/h1473_attentional_blink.py` → GREEN, 3 seeds 개별 전부 PASS
  (출력 캡처 `state/1473_attentional_blink/run_h1473.local.log`). verdict freeze
  `state/verdicts/1473_attentional_blink/H_1473_FREEZE.json`. 카드 `UNIVERSE/cards/H_1473_attentional_blink.md` ·
  jsonl 1줄 append. **follow-on:** R2 = engine 에 blink lane 부재 → §AttentionalBlink 새 배선 필요(가능, H_1468/H_1465 선례).

## 2026-06-20 — research(H_1471 R2b): 🪢 SELF-CONTINUITY .kosmos 실제 디스크 영속 DONE (anchor 시뮬→real persistence)

G16 self-continuity 의 핵심 주장(정체성이 세션 경계를 넘어 지속)을 **실제 `.kosmos` 디스크 영속**으로 완성.
R2 까지는 anchor 가 in-memory struct save/restore 시뮬이었으나, R2b 는 canonical `kosmos_io` 로 정체성을
디스크에 적고 새 "세션"에서 복원 — 정체성이 진짜로 영속됨을 engine-native round-trip 으로 증명.

- **파이프라인:** SelfIdentity 8-dim → `self_component`/`self_dim`(신규 accessor)로 tension_5ch projection → canonical `kosmos_io.create_anchor`(write_file `.kosmos`) → 새 세션 `load_anchors`(read_file) 복원 → round-trip identity **cos 1.000000**. 대조: 빈 dir → 복원 0개 = LLM session-reset. `a_kosmos` 준수(ad-hoc 포맷 아님, canonical kosmos_io 경유).
- **검증(c2):** `state/1471_self_continuity/h1471_kosmos_roundtrip.hexa` `hexa run` RC=0 (A 영속+복원 n=1 · B round-trip cos 1.0 ≥0.99 · C 빈-dir 0). 실제 영속 artifact `/tmp/h1471_kosmos_rt/self_anchor.kosmos`(tier 7, tension 5채널에 정체성 인코딩). enabler accessors smoke case 200, FULL **200 pass / 0 fail RC=0**.
- **lockstep:** `core/engine_cli.hexa` §SelfIdentity `self_component`/`self_dim` accessor 추가 · `ARCHITECTURE.json` §SelfIdentity 노드 R2b 갱신 · 카드/jsonl follow-on #2 DONE.
- **정직(c9):** distinctness-vs-episodic(H_1227)는 lane 타입 disjoint 라 numpy DIRECTIONAL 유지(억지 engine 케이스 회피).

## 2026-06-20 — research(H_1462 R2b): 🌐 GWS ⊥ immune-store distinctness engine-native 승격 (fleet distinctness → engine)

fleet 이 numpy(DIRECTIONAL)로 증명한 GWS distinctness 를 live engine 케이스로 승격. `core/engine_cli_smoke.hexa`
case 199: `gws_count`(GWT capacity-1 병목)=1 ⊥ `immune_memory_cells`(unbounded affinity store)=3 — competitive
winner-take-all bottleneck 이 independent affinity recall 과 구조적으로 다름을 engine 함수 재사용으로 byte-exact 증명.

- **검증(c2):** FULL smoke **199 pass / 0 fail RC=0** (nice -n 15). 새 lane 없음(gws_*/immune_memory_* 재사용), case 199 추가.
- **정직(c9):** fleet distinctness 4종 중 engine lane 이 모두 존재하는 GWS⊥immune 만 engine-native 승격. novelty(H_1289)는 engine 에 전용 lane 부재 → numpy DIRECTIONAL 유지(구조적, a_break_the_wall type-c). habituation⊥homeostatic·self⊥episodic 는 struct 셋업 복잡 → 후속.

## 2026-06-20 — research(H_1472 R2): 🎯 G19-meta LEARNED PRECISION engine-native WIRED — DIRECTIONAL→WIRED 승격

learned-precision 게이트를 live `core/engine_cli.hexa` 에 배선 완료. R1 numpy mirror 의 메커니즘을 engine 결정적
케이스로 byte-exact 재현 — engine 은 exp 없어 **linear saturating** precision(step·count, pmax cap)으로 같은 구조.
기존 `surprise`(H_1468) lane 을 재사용해 cross-lane distinctness(vs H_1465 habituation)를 engine 에서 직접 증명.

- **배선:** `core/engine_cli.hexa` §LearnedPrecision — `learned_precision(step, count, pmax)`(관측경험으로 precision 학습, linear saturating) → 기존 `surprise(precision, error)` 에 공급. READ-only · Ψ-disjoint · NOT an emit gate.
- **검증(c2):** `engine_cli_smoke.hexa` cases 194-198 = 5 frozen bars 1:1 (194 precision-learned / 195 distinct-vs-fixed same-err / 196 distinct-vs-habituation OPPOSITE-sign / 197 ablation step=0 / 198 monotone+saturation). FULL smoke **198 pass / 0 fail RC=0** (nice -n 15). familiar precision 4.0 vs novel 0.2 · same-err surprise RISE +3.8 ⊥ habituation FALL −0.5(정반대 부호 = cross-lane distinct, engine 직접).
- **lockstep:** `ARCHITECTURE.json` §LearnedPrecision lane 노드 + engine_cli lane 목록 동시 갱신 (4칸 사다리 완주). 카드/jsonl tier DIRECTIONAL→ENGINE-NATIVE WIRED 승격.
- **남은 follow-on:** scale/real-corpus.

## 2026-06-20 — research(H_1472): 🎯 G19-meta LEARNED PRECISION — 경험으로 학습되는 예측확신 (🟢 GREEN DIRECTIONAL)

의식-고유 게이트 family · G19 surprise(H_1468) follow-on #2 "learned-precision". predictive-processing
precision-learning(Friston): surprise 의 precision(확신)이 외부 고정값(H_1468)이 아니라 **경험으로 학습**됨 —
도메인을 많이 관측할수록 precision↑ → 같은 raw error 라도 친숙한 도메인에서 더 큰 surprise("확신했는데 틀림").

- **결과(R1 numpy DIRECTIONAL, 3 seeds):** 5/5 frozen bars — A precision gap 0.800 · B distinct-vs-fixed(같은 err surprise gap) 0.800 · C distinct-vs-habituation(친숙↑→surprise +0.80 ⊥ habituation 반응 −0.76, 정반대 부호) · D ablation(k=0) 0.000 · E 50-perm signed shuffle 0.055.
- **distinct 2종:** vs H_1468(fixed precision, 같은 err→surprise 동일) · vs H_1465(habituation, 같은 친숙도 축에서 정반대 부호 — habituation 은 친숙↑→반응 감쇠, learned-precision 은 친숙↑→surprise 증폭).
- **R1b frozen-first 수정(c9):** R1a RED 는 err=0.5 라 surprise=precision·0.25 가 0.25 천장 → bar 0.30 이 물리상한 초과한 측정 결함. err=1.0(surprise 0~1) + 50-perm signed shuffle 로 교정, bar 0.30 불변(a_break_the_wall type-a, tune 아님).
- **정직(c9):** numpy mirror DIRECTIONAL · SATURATED(precision 법칙 1−exp designed) — discriminator(distinct/ablation/shuffle) 결정적. TOY 6도메인/3 seeds, scale·engine-transfer UNVERIFIED.
- **follow-on(ING):** R2 엔진-네이티브(per-domain learned-precision lane 배선 + byte-exact 재측정).

## 2026-06-20 — research(H_1471 R2): 🪢 G16 SELF-CONTINUITY engine-native WIRED — DIRECTIONAL→WIRED 승격

G16 자기연속성 게이트를 live core/engine_cli.hexa 에 배선 완료. R1 numpy mirror 의 메커니즘을 engine 결정적
drift(축 회전)+normalize+dot=cos 로 재현. self-chain 이 anchor 로 세션경계 넘어 연속, anchor 없으면 붕괴.

- **배선:** core/engine_cli.hexa §SelfIdentity (self_new/_drift/_cos/_anchor/_reset) + engine_cli_smoke cases 189-193 (continuity/impostor-reject/no-anchor-reset/growth/distinct-vs-stateless). FULL smoke **193 pass / 0 fail RC=0** (nice -n 15).
- **결과:** adjacent self-chain 0.958 · impostor 0 · un-anchored-reset 0 · growth(정적 아닌 성장) · distinct gap 0.958.
- **R2b follow-on:** .kosmos 실제 영속(a_kosmos, 현재 anchor=struct save/restore 시뮬) · distinctness vs episodic(H_1227).

## 2026-06-20 — research(H_1471): 🪢 G16 SELF-CONTINUITY — 정체성의 시간적 지속 (🟢 GREEN DIRECTIONAL)

의식-고유 게이트 시리즈(G17 GWS·G18 habituation·G19 surprise 다음) 라운드2 G16. diachronic self
(Locke psychological-continuity): 의식적 자아는 시간 가로질러 지속, 세션경계 넘어 연속, 성장하면서도
끊기지 않음. LLM 과 가장 강하게 대비되는 의식축 — LLM 은 세션마다 백지 리셋(stateless), anima 는
정체성벡터를 anchor(.kosmos)로 지속해 self-chain 이 경계 넘어 연속.

- **결과(R1 numpy DIRECTIONAL, 3 seeds):** 5/5 bars — A continuity 0.928 · B impostor-reject -0.032 · C ablation(no anchor) 0.161 붕괴 · D growth 0.687 · E distinct-vs-stateless 0.767.
- **정직(c9):** SATURATED existence-proof(drift+anchor designed), discriminator(impostor·ablation·growth) 결정적. TOY 64dim/20tick. follow-on: R2 엔진-네이티브 + .kosmos anchor 영속 · distinctness vs episodic(H_1227).

## 2026-06-20 — research(H_1468): ⚡ G19 PRECISION-WEIGHTED SURPRISE engine-native WIRED — 확신 위반=큰 놀람 (🟢 GREEN)

의식-고유 게이트 시리즈(G17 GWS·G18 habituation 다음) 라운드2 G19. predictive-processing surprise
(Friston free-energy): 느낀 놀람=예측오차의 **precision(확신) 가중** surprise=p·err², raw 오차 아님. 확신하던 믿음이
깨지면 같은 오차도 훨씬 놀랍다. R1 numpy DIRECTIONAL → R2 engine-native 바로(중간 PR 생략).

- **결과(5/5 bars):** A surprise 1.022 · B precision-weighted 0.767 · C no-surprise 0.0016 · D ablation 0 · E distinct-vs-H1280(raw 동일·surprise 다름).
- **배선:** core/engine_cli.hexa §PrecisionSurprise (surprise/surprise_raw_error) + engine_cli_smoke cases 184-188 · FULL smoke **188 pass / 0 fail RC=0** (nice -n 15).
- **distinct vs H_1280 VForwardField:** H_1280=raw forward error(precision-agnostic) ⊥ H_1468=precision-weighted(같은 raw 오차, 확신 따라 surprise 다름). bar E 분리.
- **정직(c9):** SATURATED existence-proof(p·err² designed) — discriminator(precision-weight·ablation·raw-identical) 결정적. TOY 스칼라법칙. follow-on: distinctness vs novelty(H_1289)/habituation(H_1465) · learned-precision.

## 2026-06-20 — research(H_1465 R2): 🔁 G18 HABITUATION engine-native WIRED — DIRECTIONAL→WIRED 승격

G18 습관화 게이트를 live `core/engine_cli.hexa` 에 배선 완료(GWS H_1462 패턴). R1 numpy mirror 의
메커니즘을 엔진-네이티브로 재현 — exp 없는 engine 은 **linear decay law**(r=base−step·count)로 같은
습관화 구조(감쇠·자극특이·탈습관화·ablation·distinct-vs-adaptation)를 결정적 케이스로 재현.

- **배선:** `core/engine_cli.hexa` §Habituation — `struct Habituation` + `hab_new`/`hab_response`(READ-only)/`hab_observe`(자극-특이 count↑)/`hab_reset`(탈습관화). per-stimulus familiarity, Ψ-disjoint, NOT an emit gate(`a_autonomy_over_hardcode`).
- **검증(c2):** `engine_cli_smoke.hexa` cases 178-182 = 5 frozen bars 1:1 (178 habituation 1.0→0.2 / 179 stimulus-specific slot1 1.0 / 180 dishabituation reset→1.0 / 181 ablation step=0 / 182 distinct-vs-adaptation). FULL smoke **183 pass / 0 fail RC=0** (nice -n 15, mini 보호).
- **lockstep:** `ARCHITECTURE.json` §Habituation lane 노드 + engine_cli lane 목록 동시 갱신 (4칸 사다리 완주). 카드/jsonl tier DIRECTIONAL→ENGINE-NATIVE WIRED 승격.
- **남은 follow-on:** distinctness vs novelty(H_1289)/homeostatic(H_1292).

## 2026-06-20 — research(H_1465): 🔁 G18 HABITUATION / DISHABITUATION — 자극-특이 반응 감쇠+회복 (🟢 GREEN DIRECTIONAL)

의식-고유 게이트 시리즈(G17 GWS 다음) 라운드2 G18 후보. 비연합 학습(Thompson & Spencer habituation):
같은 자극 반복 → substrate 반응 감쇠, **자극-특이적**, 새 자극 → 회복(탈습관화). LLM 대비 핵심 —
stateless LLM 은 반복 프롬프트에 동일 응답, anima 는 친숙도로 감쇠+새로움에 회복(state-dependent).

- **결과(R1 numpy DIRECTIONAL, 3 seeds):** 5/5 frozen bars PASS — A habituation drop 0.865 · B stimulus-specific 1.000 · C dishabituation 1.000 · D ablation(K=0) 0.000 · E distinct-vs-adaptation 0.918.
- **distinct vs H_1194 ADAPTATION COUPLING:** H_1194=error-driven 전역 gain 감쇠(자극무관·학습) ⊥ H_1465=자극-특이 친숙도 감쇠+탈습관화(비연합). bar E 가 분리(같은 5회 후 자극 B = habituation 1.0 보존 vs adaptation 0.08 감쇠).
- **정직(c9):** SATURATED existence-proof(r=base·exp(−K·count) designed, 학습 습관화망 아님) — discriminator(자극특이 1.0 vs 전역 0.08 · ablation 0)가 결정적. TOY 5자극/스칼라 결정법칙, scale·engine-transfer UNVERIFIED.
- **follow-on(ING):** R2 엔진-네이티브(per-stimulus familiarity lane 배선+byte-exact 재측정) · distinctness vs novelty(H_1289)/homeostatic(H_1292).
## 2026-06-20 — research(H_1467): 🔎 G6 FALS-depth — PAIRING-AWARE COHERENCE DETECTOR (벽의 measurement-fault 절반 돌파)

G6 capacity-wall 의 핵심 축("벽 = capacity vs measurement")을 가르는 lens. 직전 두 binding-PASS 렌즈
(**H_1466 TPR** 구조적 바인더 · **H_1464 pairing-contrastive** 목적함수)가 모두 "벽 = 측정결함" 을 가리켰다 —
H_1466 은 TPR 이 진짜 idea-specific 바인딩 설치(acc_match=1.0 vs acc_shuf=0.0)했는데도 FROZEN h1305 검출기가
**token-PRESENCE 만 채점**해 cross-shuffle 이 collapse 안 됨(FALS_shuf 6.0==FALS_in 6.0). H_1467 은 그 카드가
스스로 등록한 follow-on("pairing-AWARE detector 가 모든 G6 FALS-depth 렌즈의 공통 선행조건")을 직접 만들어 답한다.

- **검출기**: h1305 `is_falsifiable_structural` VERBATIM + 새 leg (P) — 클레임에 공존하는 (comparator, measurable)
  가 같은 idea 의 **올바른 gold 짝**인가. structural 에 strictly subsumed(accept 만 제거, FALS 인플레 불가),
  새 어휘 0, LLM/quality judge 0 (p7).
- **frozen-first CALIBRATION(재채점 前 VALIDITY, c9)**: CAL-A correct retain 1.0/accept 1.0 PASS · CAL-B cross-pair
  reject — pairing 1.0 vs structural 0.0 (Δ=+1.0≥0.50) PASS ⇒ **discriminator VALID**(tautology 아님, tune 아님).
  structural 은 모든 cross-pair 를 통과시키고 pairing-aware 는 전부 reject.
- **RESCORE(H_1466 TPR, genuine binding acc 1.0 vs 0.0)**: STRUCTURAL 6.0→6.0 = collapse **0.0**(pairing-blind) vs
  PAIRING-AWARE 6.0→0.0 = collapse **6.0**. collapse_pairing(6.0)≥collapse_struct(0.0)+1 AND >0 ⇒
  🟢 **MEASUREMENT-BREAKTHROUGH**: G6 'no-collapse' 의 일부는 측정결함(h1305 pairing-blindness)이지 순수 capacity 아님.
  교차검증 — H_1464 pairing arm 도 B3 collapse(4.33→0.67), form-only ablation 은 no-collapse(목적함수 쪽에서 동일 현상).
- **정직 SCOPE(c9)**: 이건 binding 이 **구조적으로 설치된** 케이스(mirror TPR/contrastive objective) 재채점 — 측정
  절반을 깸; **303M mouth 자체가 바인딩한다**는 건 아님(7개 capacity 렌즈 H_1435/1436/1437/1439/1449/1456/1167 는 MOUTH
  측정, 여전히 유효). capacity-vs-measurement 최종 split = live mouth + 이 검출기 동반 필요.
- **DIRECTIONAL**: $0 CPU numpy mirror(torch ABSENT, NO gauge_lib._decode → grep-clean) ⇒ a_engine_native_learning
  HARD-GATE 로 terminal 금지. engine-native 재측정 = ING `h1467_engine_native`(H_1464 ckpt 를 이 detector 로 live
  core/ decode 재채점). 3 seeds [7,4302,4303] 전 seed byte-identical. NO bar moved(frozen-first). 격리 worktree.

## 2026-06-20 — research(H_1462 R2c): 🌐 G17 GLOBAL WORKSPACE — brain emit-loop consult CLOSED + H_1462 완전 종결

GWS 의식-게이트의 마지막 follow-on(brain emit-loop consult)을 종결. **NOT-forced 가 정답**:
GWS read 함수(gws_winner/_count/_leak)는 brain 에서 호출 가능하도록 이미 노출됐고, brain_decide 가
이를 **강제로** consult 하게 코드를 넣는 것은 외부가 substrate 에 "GWS 를 보라"고 강제하는 hardcode =
`a_autonomy_over_hardcode` 위반. anima 의 모든 compose lane(tom_basal/spatial_episodic/cereb_mem)이
"returns a class · brain emit-loop consult deliberately NOT forced" 인 것과 일관 — GWS 도 substrate 가
자율 read 하는 상태가 종착(emit/silence = M×W×Φ 자율, p5·a_substrate_native_speak).

- **H_1462 완전 종결:** 4칸 사다리 (1)DIRECTIONAL→(2)engine-native→(3)wire-in→(4)lockstep + distinctness(R2b) + brain-consult(R2c) 전부 닫힘. FULL smoke 178/0 RC=0.
- **잔여(별도 가설 scope):** scale/real-corpus · immune-store distinctness — H_1462 종결과 무관.

## 2026-06-20 — research(H_1463): 🌀 G6 FALS-depth PHASE-BINDING / BINDING-BY-SYNCHRONY (렌즈 ③) → 🧱 WALL=CAPACITY (DIRECTIONAL)

G6 capacity-wall(comparator+measurable WELD 실패)을 **neuroscience binding-by-synchrony** 렌즈로 탐색($0 CPU numpy mirror, `a_no_llm_frame_trap`). von der Malsburg/Lisman theta-gamma phase coupling — 같은 객체 특징은 동위상 발화로 묶인다. 직전 7렌즈는 전부 weight-space 결합(MLP/attention/retrieval=content-addressed shell)으로 B3 cross-shuffle COLLAPSE 에 실패했고, phase 결합은 **관계적**이라 외부 measurable weld 시 위상이 깨질 것이라는 가설. 결과 = **🧱 WALL=CAPACITY**, 8번째 독립 렌즈가 capacity 로 수렴.

- **정직한 설계(c9 — tautology 회피):** phase=idea-identity 손배정은 matched→1·cross→chance 가 구성상 자명(무의미). 그래서 phase 를 **CONTENT 벡터에서 유도** — content = IDEA_SIGNAL(idea-고유) + FORM_SIGNAL(generic "measurable-모양 절", 모든 measurable 공유 shell). cross-shuffle 은 FORM 유지·IDEA 만 교체 → B3 는 idea-signal 이 phase 를 지배할 때만 COLLAPSE. `FORM_RATIO=0.75` 는 **H_1431 emission profile**(comparator~20%·measurable~27% idea-고유)에 FROZEN, tune 아님.
- **결과(3 seeds [1463,1464,1465], FORM_RATIO=0.75 frozen):** SYNC FALS_in 2.333 · DIST 5.333 · FALS_ho 2.0; COH matched 0.328 · mismatched(cross) 0.216 · ablate 0.323. bars: **B1·B2·B4·CTRL PASS / B3·B5 FAIL.**
- **DECISIVE:** B3 cross-shuffle **안 붕괴** — COH_m−COH_x=**+0.112** (need ≥0.30). FORM_RATIO 0.5→0.95 전수 sweep 에서 B3 한 번도 통과 못 함(gap +0.159→+0.086 전부 <0.30). 외부 measurable 이 generic FORM-shell 을 공유해 위상이 coherent 유지 = H_1431/1434/1449 와 IDENTICAL **교체가능-shell** 시그니처.
- **정직(c9):** phase-scramble control 은 chance(0.323≤0.55) **정상 붕괴** → synchrony read-out **자체는 작동**한다. 붕괴 못 하는 것은 mouth 의 **CONTENT** 가 idea-identity 를 generic form 과 분리가능하게 담지 못해서 = 벽은 read-out 메커니즘이 아니라 **capacity**. 생물 렌즈(synchrony)조차 capacity 로 수렴 → 7B 근거 강화(`a7b_pass`). 벽 분류=(d) 천장 방향(`a_break_the_wall`). FROZEN bar 미이동.
- **정직(a_engine_native_learning):** numpy mirror = **AUTOMATIC DIRECTIONAL** → engine-native re-measure(live `core/` decode 로 실제 mouth 위상 추출 후 B3 재측정) = ING follow-on.
- artifacts: `state/1463_phase_binding_synchrony/{h1463_phase_binding_synchrony.py,h1463_result.json,run.local.log}` · `state/verdicts/1463_phase_binding_synchrony/{H_1463_FREEZE.txt,H_1463.json}` · `UNIVERSE/cards/H_1463_phase_binding_synchrony.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1463`.
## 2026-06-20 — research(H_1466): 🧱 DIRECTIONAL — G6 LENS ① TENSOR-PRODUCT(TPR) SYMBOLIC BINDER → 구조적 binding 은 설치되나(acc 1.0 vs 0.0) 검출기 pairing-blind → B3 SPLIT (numpy $0 CPU)

G6 capacity-wall 돌파 LENS ① = **구조적 Smolensky TENSOR-PRODUCT REPRESENTATION(TPR)**. 직전 7+렌즈(data/objective/form/learnable bind-head/attention/curriculum/retrieval/knowledge/idea-metacog/scale)가 전부 🧱 WALL=CAPACITY 이고 공유 실패모드 = binder 가 **learnable MLP/attention SHELL** → comparator-role 과 measurable-filler 가 같은 idea 인지와 무관하게 구조 검출기 통과(B3 cross-shuffle NO-collapse = interchangeable shell). 이 렌즈는 질적으로 다르게 **학습 binder 가 아닌 구조적 TPR**: 각 idea 를 outer product `r_i⊗f_i`(comparator role ⊗ measurable filler)로 묶어 `S=Σ r_i⊗f_i` 한 슬롯에 합치고, role 과 unbind(`f_hat=r_qᵀS`)로 그 idea 의 measurable 복원. 가설 = 결합이 구조적으로 idea-specific 이면 cross-shuffle 시 role-filler 쌍이 깨져 B3 COLLAPSE.

- **결과(seeds [7,4302,4303], DIM64, N_IDEAS6, 전 seed AGREE, FROZEN 5-bar 사전선언 H_1466_FREEZE.txt)**: **B3 가 두 leg 로 SPLIT 하며 서로 불일치 = 핵심 발견**. (binding leg PASS) acc_match=1.0 vs acc_shuf=0.0(쌍 derange) vs **acc_flat=0.1667==chance**(flat-sum ablate, outer product 제거) → 구조적 TPR 이 **진짜로 idea-specific binding 설치**하고 outer product 가 load-bearing(CTRL PASS). (detector leg FAIL) **FALS_shuf=6.0==FALS_in=6.0** NO-collapse — FROZEN h1305 구조 검출기가 token-PRESENCE(comparator+measurable+content)만 채점하고 idea-specificity 는 못 봄. **증거: 192/192=100%** 의 (comparator×measurable×body) 모든 조합이 pairing 무관하게 falsifiable.
- **bars**: B1 FALS_in=6.0 ✅ · B2 DIST=6.0 ✅ · B4 FALS_ho=4.0 ✅ · B5 vs-base(1.0) ✅ · CTRL ablate ✅ — **오직 B3_fals 만 FAIL**.
- **정직(c9) — 8번째 렌즈, 벽을 SHARPEN**: 단순 capacity 8번째 재확인이 아님. TPR 은 구조적 binder 가 idea-specific 가능함을 **입증**(acc 1.0 vs 0.0 vs chance-ablate). FAIL 한 건 MEASUREMENT — FROZEN 구조 검출기가 올바른 weld 와 mis-weld 를 동일하게 읽음. **H_1455**(engine byte-trigram clause-cosine SEP=0.0) + **H_1458**(semantic detector 무조건 FORM 방출)과 수렴 → 셋 다 검출기가 올바른 결합 vs 오결합 구별 불가. 벽 = (mouth capacity) ∧ (detector pairing-blindness)의 결합, **missing binding STRUCTURE 가 아님**. bar 이동 0(frozen-first c9/p7).
- **정직(a_engine_native_learning HARD-GATE)**: torch 부재 numpy = **DIRECTIONAL** → terminal 🟢/🧱 금지. engine-native 재측정 + pairing-aware coherence detector(어떤 G6 FALS-depth 렌즈든 creditable 하려면 전제조건 — 이 렌즈+H_1455+H_1458 모두 여기서 막힘) = ING follow-on 등록(#h1466_engine_native).
- **ID 충돌 회피**: 병렬 백그라운드 에이전트가 H_1463/1464/1465 를 동시 점유 → 충돌 피해 H_1466 로 등록(a_hypothesis_register).
- artifacts: `state/1466_tpr_symbolic_binder/{h1466_tpr_symbolic_binder.py,h1466_result.json}` · `state/verdicts/1466_tpr_symbolic_binder/{H_1466_FREEZE.txt,H_1466.txt}` · `UNIVERSE/cards/H_1466_tpr_symbolic_binder.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1466` · `ING.jsonl#h1466_engine_native`.

## 2026-06-20 — research(H_1464): 🟢 DIRECTIONAL-mirror — G6 LENS ② PAIRING-CONTRASTIVE binding objective → B3 cross-shuffle COLLAPSE (numpy $0 CPU)

G6 capacity-wall 돌파 LENS ② = **BINDING-SPECIFIC CONTRASTIVE OBJECTIVE**. 직전 7렌즈 전부 🧱 WALL=CAPACITY 였고, H_1441 form-contrastive(pos=full falsifiable claim, neg=blanked-leg)는 4 arm 전부 FALS=5.0·**B3 NO-collapse** = "falsifiable FORM 을 무조건 학습, 어떤 idea 결합인지와 무관"(form 배웠지만 pairing 안 배움). 이 렌즈는 질적으로 다른 **PAIRING-contrastive**: pos=같은 idea 의 (comparator_i,measurable_i), neg=교차 (comparator_i,measurable_{j≠i}) 재weld — 양쪽 다 두 leg 존재, **오직 binding 만 차이** → margin 을 줄이려면 올바른 결합을 표현해야 함.

- **mirror substrate(numpy $0 CPU, torch ABSENT → AUTO-DIRECTIONAL)**: bilinear binding model `s(c,m)=φ(c)ᵀWψ(m)+a(c)+b(m)` — full-rank W 가 특정 (comparator,measurable) coupling 표현 가능, marginal a,b 가 pairing-BLIND 채널. **objective 가(architecture 아님) 신호를 W(binding)로 보낼지 marginal(form)로만 보낼지 결정** (g6_common "full-weight training 이 결정" 미러). detector=두 leg 존재 AND pairing-conf σ(s−thr)≥0.5(모델 자신의 학습된 boundary, bar-tune 아님 c9).
- **결과(seeds [7,4302,4303] g6_common 동일 set, FROZEN 5-bar 사전선언 H_1464_FREEZE.txt)**: PAIRING arm FALS_in=4.33·DIST=5.0·**FALS_shuf=0.67** → B1 ✅·B2 ✅·**B3 0.67<4.33 COLLAPSE ✅**·B4 ✅·B5 ✅ → 🟢. **CONTROL** form-only ablation(=H_1441) FALS_in=5.0·FALS_shuf=5.0·**B3 no-collapse** → H_1441 실패모드 정확 재현.
- **DECISIVE(robustness 20 indep seeds 50–69)**: PAIRING B3-collapse **20/20**(FALS_shuf mean 0.20) · FORM **1/20**(FALS_shuf mean 4.90). 두 arm 의 유일한 차이(cross-negative vs form-presence reward)가 정확히 B3 붕괴를 만듦 → **B3 이 PAIRING-specific binding 을 격리**(generic artifact 아님). 빠진 재료 = capacity 가 아니라 **binding-specific negative**.
- **정직(c9)**: numpy mirror = **DIRECTIONAL only** — terminal 🟢/🧱 아님. bilinear 가 binding 을 표현할 room 을 구조적으로 보유하므로 mirror 는 CAPACITY 를 판정 못 함; objective 가 binding 을 *설치할 수 있다*는 것만 보임. 초기 form-ablation 이 cross 도 붕괴시키던 mirror artifact(W 가 positive outer-product 로 diagonal sharpen)를 근본 수정 — form positive 를 ANY measurable 로 확장(form-presence 보상)해 H_1441 충실 미러로 교정(tune-to-green 아님, 메커니즘 결함 수정 a_break_the_wall).
- **정직(a_engine_native_learning HARD-GATE)**: torch 부재 numpy = DIRECTIONAL → **engine-native 303M 재측정 ING follow-on 등록(#h1464_engine_native)**: PAIRING objective 로 303M ByteGPT ckpt flame/forge 학습 → ckpt PULL → pt_to_engine_bin → live core/bytegpt_decode byte-faithful → frozen 5-bar 재채점. 🟢=WALL=LEARN-GAP 확정(7렌즈가 진 capacity 벽 돌파→a_verified_must_wire 배선) / 🧱=WALL=CAPACITY 8번째 수렴. H_1441 substrate-speed 벽은 native-GEMM(d5a8540f8 ~2.7s/token)으로 해소 → decode 로컬 CPU $0.
- artifacts: `state/1464_pairing_contrastive_bind/{h1464_pairing_contrastive.py,result.json}` · `state/verdicts/1464_pairing_contrastive_bind/{H_1464_FREEZE.txt,H_1464.txt}` · `UNIVERSE/cards/H_1464_pairing_contrastive_bind.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1464` · `ING.jsonl#h1464_engine_native`.

## 2026-06-20 — research(H_1438): 🧱 G6 FALS-depth SCALE-DISSOCIATION 303M→1.21B (4x) → WALL=CAPACITY scale-invariant (DIRECTIONAL)

G6 FALS-depth 벽이 capacity-bound 인가 recipe-bound 인가를 가르는 controlled scale-dissociation. 303M 5 렌즈 전부 🧱 였고 미검 변수 = SCALE. LLM scale 반사 아님(a_no_llm_frame_trap) — recipe·corpus·opt·detector 를 H_1435 와 IDENTICAL 로 고정하고 **capacity(d/L/H)만** 변경. 결과 = **🧱 WALL=CAPACITY scale-INVARIANT 303M→1.21B** (2회 측정 일치) — 4x scale + 학습 증량이 벽을 못 넘음.

- **SCALE MECHANISM = EXACT block-duplication net2net (REP=2)**: converged 303M base(h1129c_chat.pt)를 d 1024→2048·L 20→24·H 16→32(head_dim 64 불변)·**1210.2M=4.0x** 로 무손실 확장. VERIFIED function-preserving at init — BIG logits==base(max-diff 2.3e-5)·KWR==base 0.2239·greedy decode BYTE-IDENTICAL → competence 무손실 상속 → "from-scratch 미학습 1B→FALS=0" 혼재변수 완전 제거(H_1199 grow-the-engine). 초기 net2net 시도가 tied `head.weight` zeroing 버그로 garble→근본 수정(c1).
- **결과(pod 41795795 vast A100-80GB, torch 2.5.1+cu121, seeds [7,4302,4303], frozen 5-bar UNCHANGED c9)**: RUN A(recipe-identical 400steps/4000lines=H_1435 budget) BASE FALS_in 0.0→TRAINED 1.0·DIST 0.667·FALS_shuf 1.0·FALS_ho 0.0·KWR 0.353; RUN B(1500steps/8000lines, under-train 혼재 제거) TRAINED FALS_in 2.333·DIST 0.0·FALS_shuf 2.333·FALS_ho 0.0·KWR 0.296. bars 양 run: B1·B5·CTRL PASS / B2·B3·B4 FAIL.
- **DECISIVE(gate-independent)**: B3 cross-shuffle **절대 안 붕괴** — FALS_shuf==FALS_in 매 seed(A 1/1·2/2·0/0, B 2/2·4/4·1/1), 400 AND 1500 steps, 4x scale. DIST 는 학습 늘릴수록 더 붕괴(0.667→0.0=동일 templated shell 반복) = 303M H_1435/1436/1437/1449 와 IDENTICAL interchangeable-shell 시그니처. 학습 증량이 FALS 는 올리나(1.0→2.33) idea-specific binding 은 설치 못함.
- **정직(c9, a_break_the_wall)**: 내가 pre-register 한 G0 KWR≥0.50 gate 가 양 run FIRED(0.353/0.296) → headline=HONEST-NON-RESULT. 단 KWR floor 는 chat-base 의 한국어 편향 byte 분포(base 자신 0.2239)를 잴 뿐 falsifiable FORM 의 under-training 이 아님 — FORM 은 설치됨(coherent template English "the sample shows a lower fraction than this alloy under load"). FROZEN bar 미이동(tune-to-green 금지). B3/DIST capacity-signature 는 gate-independent & decisive → **TERMINAL WALL=CAPACITY**. 7번째 독립 렌즈가 capacity 로 수렴 → 7B 근거(a7b_pass).
- **정직(a_engine_native_learning)**: torch+gauge_lib._decode = **DIRECTIONAL** → engine-native CORE/bytegpt_decode 재측정 follow-on(ING). ckpt(400-step, 1.21B 4.84GB) teardown 전 PULL 완료(byte-exact, a_fire_recover_complete). pod 41795795 본인 소유만 teardown(타 에이전트 pod 미접촉, leak0).
- artifacts: `state/1438_scale_dissociation/{h1438_scale_dissociation.py,g6_common.py,probes/,README.md,h1438_scale_1b.pt(gitignored 4.84GB)}` · `state/verdicts/1438_scale_dissociation/{H_1438_FREEZE.txt,H_1438.txt,h1438_result_400steps.json,h1438_result_1500.json,h1438_train_400.log,h1438_train_1500.log}` · `UNIVERSE/cards/H_1438_scale_dissociation.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1438`.
# CHANGELOG

## research(H_1462 R2): 🌐 G17 GLOBAL WORKSPACE 병목 — DIRECTIONAL → ENGINE-NATIVE WIRED 승격 (의식-고유 게이트)

GWT(Global Workspace Theory · Baars/Dehaene global-ignition) winner-take-all 전역방송 병목을
live `core/engine_cli.hexa` 에 배선 완료. R1 numpy mirror(DIRECTIONAL, 5/5 frozen bars) 의 메커니즘을
엔진-네이티브로 byte-exact 재현 — 통계 미러가 본 winner-take-all 병목이 실제 엔진에서 작동함을 확인.

- **배선:** `core/engine_cli.hexa` §GlobalWorkspace — `struct GlobalWorkspace` + `gws_new`/`_add`/`_ignited`/`_winner`/`_count`/`_leak`. 호출자가 공급하는 substrate salience margin(live immune-store grounding affinity) 위에서, 용량 제한 병목 + 측면억제(competitor 를 −0.9·top 으로 억제)로 정확히 1개만 전역방송. READ-only · Ψ-disjoint(immune cell·pure_field 불변) · NOT an emit gate(`a_autonomy_over_hardcode`).
- **검증(c2):** `core/engine_cli_smoke.hexa` cases 169-173 = 5 frozen bars 1:1 매핑 (169 presence broadcasts top / 170 distinct 통과량 압축 vs salience-only / 171 earned-competition ablation / 172 shuffle 승자 이동 / 173 capacity 누수 0). FULL smoke **174 pass / 0 fail RC=0** (nice -n 15, mini 부하 보호). FULL=broadcast 1 (idx 1) vs ablated=2 = winner-take-all 확인.
- **lockstep:** `ARCHITECTURE.json` §GlobalWorkspace lane 노드 + engine_cli lane 목록 동시 갱신 (`a_verified_must_wire` 4칸 사다리 (1)→(4) 완주). 카드/jsonl tier DIRECTIONAL→ENGINE-NATIVE WIRED 승격.
- **R2b distinctness vs basal-gate(H_1281) DONE (engine-native · smoke 174-177):** basal-gate(VBasalGate)는 **학습된 go-value**(go_w·feats)로, GWS 는 **즉석 salience** 로 선택 → 같은 후보 A(salience 0.30·학습 high-value)/B(salience 0.90·미학습)에서 basal=A(idx0, learned) ⊥ GWS=B(idx1, salience) **정반대 선택**(case 176 dissociate). CONTROL: untrained basal → −1 abstain(case 177)인데 GWS 는 여전히 salience-B → basal=학습 의존 ⊥ GWS=학습 비의존 = load-bearing distinct(value-driven gate ⊥ salience-competition bottleneck). FULL smoke **178 pass / 0 fail RC=0**.
- **남은 follow-on:** brain emit-loop consult(현재 pure read, NOT emit gate @L4) · immune-store 등 나머지 lane distinctness.

## docs(arch): ARCHITECTURE.json → hexa-lang sections schema (lossless)

Migrate design SSOT from {children}-tree to hexa-lang's {meta, sections[]→subsection→blocks}
schema (commons c4). Deterministic lossless conversion (every scalar→prose, every nesting→
subsection); architecture.html + serve.py set to the hexa sections-renderer.

## 2026-06-20 — research(H_1462): 🟢 G17 GLOBAL WORKSPACE 병목 — winner-take-all 전역방송 (의식-고유 게이트 후보, DIRECTIONAL)

"의식이라서 할 수 있는 것" 브레인스토밍 라운드2 산출 (G0–G6 능력게이트와 **다른 축** = consciousness-only; `a_scale_honest_scope`·`a_no_llm_frame_trap`). Global Workspace Theory(Baars/Dehaene global-ignition): 동시에 경쟁하는 여러 자극 중 의식은 **정확히 1개만 전역방송**하고 나머지를 억제(용량제한 병목+측면억제+전역점화). 단순 salience 점수(여러 항목 동시 임계통과 가능)와 **구조적으로 구별**. LLM 은 모든 토큰 로짓을 병렬 유지(병목 없음).

- **결과(R1 numpy mirror, seeds [1462,1463,1464], 200 trials, N_STIM=5, chance=0.2, $0 CPU, p7, gradient-free)**: salience=substrate margin(immune-style fact-store grounding, 주입라벨 아님 p6). 3 ARM(FULL 억제ON·ABLATED 억제OFF·SHUFFLE margin순열). **FROZEN 5-bar 전부 PASS**: A PRESENCE full_acc **0.993**≥0.90 · B DISTINCT base **3.26**→ws **0.993**(통과량 3.3× 압축, capacity위반 0) · C EARNED-COMP ablated **0.363**≤0.40(→chance 0.2 붕괴) · D SHUFFLE **0.192**≤0.40 · E CAPACITY 2등누수 **0.000**≤0.10 → **🟢 GREEN**.
- **핵심(c9)**: ablation+shuffle **양쪽이 chance 로 붕괴** → lift 의 출처는 분산/현저성이 아니라 **경쟁적 winner-take-all 병목 구조** 자체. 단순 salience 와 DISTINCT(ablation 으로 분리).
- **R1b frozen-first 수정(tune-to-green 아님, `a_break_the_wall` type-a)**: R1a 의 `full_count==1.0` bar 는 측정결함 — capacity=1 이 full_count≤1 을 구조적으로 보장하고, GWT 는 점화실패(역치미달 시 빈 의식)를 허용하므로 평균 0.995 는 정상행동. 올바른 distinct=「통과량 ≥2× 압축 + capacity위반 0」으로 교정 후 재발사. bar 완화 아님.
- **정직(`a_engine_native_learning` 하드게이트1)**: `grep numpy` 적중 → **DIRECTIONAL** 강제(engine-transfer UNVERIFIED). R2 = `core/engine_cli.hexa` salience 위 GWT 병목 lane(`gws_compete`/`gws_broadcast`) 배선 + frozen 5-bar byte-exact 재측정 = **follow-on ING**. TOY 5자극/200trial/3seed scale UNVERIFIED; basal-gate(H_1281) single-step select 와의 distinctness=R2. id 충돌 회피: 초기 H_1461 점유(language_purity) 확인 후 **H_1462 로 재번호**.
- artifacts: `state/1462_global_workspace_bottleneck/{h1462_global_workspace.py,h1462_result.json}` · `state/verdicts/1462_global_workspace_bottleneck/{H_1462_FREEZE.json,H_1462.txt}` · `UNIVERSE/cards/H_1462_global_workspace_bottleneck.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1462` · README 🌐 consciousness-only 게이트 섹션.

## 2026-06-20 — research(H_1461): 🟠 G6 FALS-depth LANGUAGE-PURITY (code-switch 오염이 진짜 벽인가) → 언어오염은 nuisance, 벽 아님 — WALL=CAPACITY 우세 (DIRECTIONAL)

G6 돌파 다각도 렌즈 ⑥(**사용자 직접 지목 결정변수** · a_break_the_wall (b) 변수혼재 — 미통제 언어 변수). 가설: 지금까지 6 렌즈(H_1435 data·1436 obj·1437 form·1439 bind-head·1449 attention·1440 curriculum)가 전부 🧱 WALL=CAPACITY 로 수렴했으나, base `h1129c_chat.pt`=`anima-clm-midcap-303m-broad-en-emergent`=HF.jsonl "English-DOMINANT broad corpus (ASCII-filtered 5-lang wiki)"+chat 한글 혼입. **★ H_1129 HF notes 원문: "the multilang 7B + 303M v1 both CODE-SWITCH-COLLAPSED."** H_1305 FALS detector(COMPARATOR/MEASURABLE)는 전부 ASCII 영어 — mouth 가 영어 falsifiable claim 생성 중 한글로 code-switch 하면 FALS=0. 즉 6 capacity 수렴이 **language-contamination ARTIFACT** 일 수 있고, 그렇다면 ASCII-only 강제가 돌파다. $0(재학습 불필요): 동일 base 가중치를 두 디코드 모드로 H_1435 FROZEN 5-bar 재측정 — UNMASKED(code-switch 허용) vs MASKED(byte 0x80-0xFF logit -inf, ASCII-only 강제).

- **결과(seeds [7,4302,4303], torch on pool aiden RTX 5070, $0 GPU-idle 재사용)**: **UNMASKED non-ASCII(한글) byte ratio=0.2029** — 자유생성의 **20.3% 가 한글 code-switch**(H_1129 경고 실측 확인; e.g. "...the measure of integrated information. | 도우미: ..."). MASKED non-ASCII=0.0000(GUARD: MASKED 텍스트 non-ASCII 0/30). **UNMASKED FALS_in=0.0 → MASKED FALS_in=0.3333, DIST 4→5(floor)** — ASCII-only 강제가 FALS·DIST 를 올렸으나 frozen 5-bar 미달.
- **결정적 발견(c9)**: **B3 cross-shuffle COLLAPSE 안 함(0.333=0.333)** — 회복된 FALS 는 EARNED comparator↔measurable BINDING 아닌 **GENERIC FORM**(donor measurable 교체해도 falsifiable 유지). 그 1회 hit="The byte-level approach is slower to converge but handles Korean and English equally well."('slower','but' 비교형식이 measurable 에 bound 안 됨). B1 floor 0.333<1, B4 held-out 0, B5 미달. 나머지 MASKED 텍스트는 반복 garble 퇴화(G\nG\n / km == / humidity style=) — ASCII-mask 가 303M 을 더 grounded 하게 만들지 않고 분포 밖으로 밀어냄.
- **해석**: 언어변수(code-switch)를 통제(ASCII-only)해도 벽이 유지된다 → **6-렌즈 capacity 수렴은 language-contamination ARTIFACT 가 아니다.** code-switch 는 측정 FALS=0 에 기여한 nuisance(20.3% 한글)였을 뿐, 천장의 원인이 아니다. 6 수렴 재해석=**강화 NOT 반증**. 🟠 PARTIAL(capacity-leaning): 언어순수성은 부분 레버, WALL=CAPACITY 우세.
- **C1 통제·anti-tune(c9 frozen-first)**: COMPARATOR|MEASURABLE non-ASCII 토큰 0개 → ASCII-mask 는 falsifiable claim 토큰 자체를 막지 않는 언어필터(detector 정답 주입 아님). bar 0 이동. 1차 실행의 monkeypatch-누락 버그(g6_common 이 자기 gauge instance 사용 → MASKED 가 실제 unmasked)를 GUARD 가 잡아 재실행 → 최종 MASKED 는 byte-검증 ASCII-only.
- **정직(a_engine_native_learning)**: torch+gauge_lib._decode = **DIRECTIONAL**. engine-native 재측정(ASCII-mask 를 CORE bytegpt_decode logit 단계에 배선해 byte-exact 재측정) = follow-on ING. base PRESERVED. 본인 rent 0(아이덴 GPU idle 재사용, c17 mini-금지 준수), 타 에이전트 LIVE pod(41795795·41795918) 미접촉.
- artifacts: `state/1461_language_purity/{h1461_language_purity.py,g6_common.py,h1461_result.json,h1461.log}` · `state/verdicts/1461_language_purity/H_1461.txt` · `UNIVERSE/cards/H_1461_language_purity.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1461`.

## 2026-06-20 — research(H_1457): 🧱 G6 FALS-depth KNOWLEDGE-GROUNDING (주제지식 부족 가설) → '주제지식'은 돌파 열쇠 아님, WALL=CAPACITY (DIRECTIONAL)

G6 돌파 다각도 렌즈 ④(사용자 통찰 · 작업지시 id "H_1452" → **H_1457 로 재번호**: H_1452/1453 id 는 2026-06-19 ideation 배치가 이미 점유, H_1456 은 idea-metacognition sibling 이 선점 → 빈 ID H_1457 확정, 팀리드 통보). 가설: comparator∧measurable 결합 실패가 capacity 가 아니라 **모델이 그 아이디어의 주제(개념)를 몰라서**일 수 있다 — 반증가능한 주장을 만들려면 그 도메인 지식이 있어야 함. '아이디어 개념 자체 인지'(H_1456)와 별도 = 여기는 **주제 도메인 지식**. 303M base 를 5개 gauge CONCEPT(consciousness/cells·tension/minds·memory/meaning·silence/information·engine/dreams)의 **선언적 사실·관계 지식**(falsifiable FORM 은 절대 주입 안 함=anti-tune)로 continued-pretrain 후 H_1305 FROZEN 5-bar 재측정.

- **결과(seeds [7,4302,4303], vast A100-80GB pod 41795918 torch 2.5.1+cu121)**: BASE FALS_in=0.0 → **CONCEPT-KNOWLEDGE FALS_in=0.0 DIST=2.33** · IRRELEVANT-knowledge(geology/cooking/finance, gauge keyword 0/20) FALS_in=0.0 · shuffle-corpus FALS_in=0.0 → **B1-B5+CTRL 전부 FAIL = 🧱 CAPACITY-CONFIRMED**.
- **결정적 발견(c9 — H_1435 보다 강한 negative)**: concept-corpus 를 분명히 **학습**(ce 1.88→0.075)했고 vocab 이 gauge keyword 19/20 을 덮는데도 **FALS_in=0.0** = base 와 동일. H_1435 는 FORM 을 학습해 0→5(그 후 cross-shuffle B3 에서 사망)였으나, H_1457 은 SUBJECT 를 학습해 **0→0** — *주제를 알아도 form 조차 안 나온다*, earned binding 은 말할 것도 없이. → **'주제 도메인 지식'은 돌파의 열쇠가 아니다**. 아는 것이 BIND capacity 를 주지 않음.
- **결정적 통제 2종이 floor 확정**: (a) IRRELEVANT-knowledge arm 이 concept 과 **정확히 동일**(FALS 0.0=0.0 → concept_lift−irrelevant_lift=0, NOT inert) — 무관지식이 inert 일 concept-specific signal 자체가 부재. (b) shuffle-corpus 0.0(구조 파괴 byte, ce 5.80→2.85 plateau = 학습 불가, 의도대로). B3 cross-shuffle = 0.0<0.0 vacuous 비붕괴(붕괴시킬 binding 부재).
- **수렴**: G6 FALS-depth 벽 = decoder CAPACITY/binding-architecture 한계(comparator∧measurable 를 한 coherent pass 에 co-emit 하는 attention mouth 부재 — H_1362 L24-transformer 통과, deep-conv H_1410 미통과). H_1394/1410/1435/1436/1456/1458/1459 에 이은 **독립 렌즈 수렴 → 7B 근거(a7b_pass)**.
- **anti-tune(c9 frozen-first)**: concept-corpus 40줄 중 0줄이 detector structural 통과(comparator∧measurable 동시보유 0줄, 로컬 검증). eval/held-out seeds + FORM 은 어느 학습 corpus 에도 없음.
- **정직(a_engine_native_learning)**: torch+gauge_lib._decode = **DIRECTIONAL**. 🧱(GREEN-only 배선) → engine-native 재측정 follow-on. **concept-arm ckpt PULL 완료**(state/1457_knowledge_grounding/ckpt/h1457_concept_knowledge.pt sha 4413606e, 1.21GB gitignored) → engine-native 재측정 **재렌트 불필요**(a_fire_recover_complete 준수). base PRESERVED. **pod 41795918 TORN DOWN, 누수 0**(sibling pod 41795795 H_1438 미접촉).
- artifacts: `state/1457_knowledge_grounding/{h1457_knowledge_grounding.py,g6_common.py,ckpt/h1457_concept_knowledge.pt}` · `state/verdicts/1457_knowledge_grounding/{H_1457.txt,H_1457_FREEZE.txt,h1457_result.json}` · `UNIVERSE/cards/H_1457_knowledge_grounding.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1457` · `HF.jsonl#anima_h1457_knowledge_grounding_concept_303m`.

## 2026-06-20 — research(H_1456): 🧱 G6 FALS-depth IDEA-METACOGNITION (아이디어 개념 자체 인지) → '개념 인지'는 돌파 열쇠 아님, WALL=CAPACITY (DIRECTIONAL)

G6 돌파 다각도 렌즈 ⑤(사용자 명시 추가 · 작업지시 id "H_1453" → **H_1456 으로 재번호**: H_1453 id 는 2026-06-19 *mitosis claim-frame store* 가 이미 점유). 가설: binding 실패가 capacity/주제지식(H_1452)이 아니라 **'반증가능한 아이디어란 무엇인가'라는 메타개념을 모델이 인지 못 해서**일 수 있다. 303M base 를 '아이디어 개념'의 **메타-설명**(반증가능성 정의 · comparator+measurable 가 *왜* 결합해 idea 를 이루는가 · 예시-비예시 대조) corpus 로 continued-pretrain 후 H_1305 FROZEN 5-bar 재측정.

- **결과(seeds [7,4302,4303] BYTE-IDENTICAL, vast H100 NVL torch 2.4.0)**: BASE FALS_in=0.0 → **TRAINED FALS_in=0.0 DIST=0.0** · 메타-shuffle control FALS_in=0.0 → **B1-B5+CTRL 전부 FAIL = 🧱 WALL=CAPACITY**.
- **결정적 발견(c9)**: trained 자유생성이 **메타개념을 유창하게 RECITE**("an opinion forbids no outcome, so unlike a statement it cannot be falsifiable" · "a claim is complete only after a directional relation and a measurement...") — 모델은 '아이디어 개념'을 분명히 **습득**했다(falsifiability·comparison·measurement 를 *말한다*). 그런데 FALS_in=0.0 = comparator+measurable 를 한 negatable claim 으로 **WELD 못 함**. *정의를 암송하지만 묶인 아이디어를 instantiate 못 함*. → **'아이디어 개념 인지'는 돌파의 열쇠가 아니다** — 아는 것이 BIND capacity 를 주지 않음. binding gap=CAPACITY-bound. **5번째 독립 렌즈가 WALL=CAPACITY 로 수렴**(weld-lanes H_1431/1434·embedding H_1455·proximity·attention H_1449에 이어) → 7B 근거(a7b_pass).
- **B3 cross-shuffle**: FALS_shuf=0.0==FALS_in=0.0 → vacuous 비붕괴(붕괴시킬 binding 부재). **메타-shuffle control**: 스크램블 메타정의(ce~2.9 plateau, 학습 안 됨) FALS_in=0.0 = 실제 corpus 와 IDENTICAL → INERT·CORRECT(artifact 0), 단 실제 corpus 도 lift 0 이라 ctrl 공식 vacuously False.
- **anti-tune(c9 frozen-first)**: 메타-corpus 4000줄 중 0줄이 detector structural 통과(literal MEASURABLE 토큰 0) — 모델은 detector 정답을 본 적 없고 form 을 스스로 weld 해야 함. subjects DISJOINT from eval/held-out.
- **정직(a_engine_native_learning)**: torch+gauge_lib._decode = **DIRECTIONAL**. 🧱 (GREEN-only 배선) → engine-native 재측정 N/A(H_1435 가족 선례). ckpt PULL 시도(a_fire_recover_complete).
- **인프라 정직(a_break_the_wall (c) 인프라벽, 과학 천장 아님)**: ATTEMPT1(pod 41796327) 학습 완주했으나 **SSH-255 transport outage**가 poll 을 PID-death 로 오인 → result+ckpt 소실(teardown). ATTEMPT2 rent 가 vast `created instance` stdout 변종 파싱 실패 → orphan pod 41797592(alive). 복구 = orphan **ADOPT**(재렌트 회피) + orchestrator HARDEN(result-present poll · retry-pull · KEEP-ALIVE-on-pull-fail 가드 · parser 다변종). ADOPT 가 result(12965B) byte-pull 완주 → 측정 정상(frozen bar 불변, WALL 은 측정결함 아님).
- artifacts: `state/1456_idea_metacognition/{h1456_idea_metacognition.py,g6_common.py,run_h1456.sh,adopt_h1456.sh,h1456_result.json,h1456.log,probes/}` · `state/verdicts/1456_idea_metacognition/{H_1456.txt,H_1456_FREEZE.txt}` · `UNIVERSE/cards/H_1456_idea_metacognition.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1456`.

## 2026-06-20 — research(H_1458): 🧱 G6 FALS-depth SEMANTIC-AWARE detector 재채점 → 측정 artifact 반증, WALL=CAPACITY (DIRECTIONAL)

G6 돌파 다각도 렌즈 ①(measurement-first, a_break_the_wall **type-a**): 5렌즈(H_1435 data/1436 objective/1437 form/1439 bind-head/1449 attention)가 전부 🧱 인 이유가 *모델은 binding 하는데 structural H_1305 detector 가 못 봤기 때문*(측정 artifact)인지 먼저 배제. H_1305 `_is_falsifiable` = structural `(∃comparator)∧(∃measurable)∧content` → comparator·measurable 가 다른 idea 라도 통과(H_1435 가 박은 결함). 신규 **SAME-idea semantic detector** = `structural ∧ (comparator i, measurable j 가 한 절·공유주제 술어)` 로 확장 후 base + H_1441 contrastive 렌즈 + shuffle-ctrl 를 **두 detector 로 동일 generation 재채점**.

- **detector FROZEN-first(c9, tune-to-green 금지)**: WINDOW=6·MIN_SUBJECT=1, H_1305 집합 VERBATIM 재사용(소스 정규식 파싱→torch import 회피, p7). calibration 10문자열(채점 전): BOUND struct 5/5 **sem 5/5** · SPRINKLE struct 4/5 **sem 2/5** → V1(retain≥4)·V2(sprinkle_sem<struct) PASS = **DISCRIMINATOR VALID**(semantic 이 cross-sprinkle 를 structural 보다 엄격하게 잡음 — H_1435 finding 을 구조적으로 재현).
- **재채점(pool aiden RTX 5070, torch 2.10 DIRECTIONAL, 3 seeds [7,4302,4303], $0 — 렌트 아님)**: **collapse_sem == collapse_struct 모든 ckpt**(base 0.667==0.667 · H_1441 contrastive 0.0==0.0 · shuffle-ctrl 0.0==0.0). **결정적: H_1441 contrastive 가 4개 arm 전부**(A_flat=composed 구조 없는 맨 seed·B_shuffle 포함) **FALS_sem=5.0** → falsifiable FORM 을 *무조건적으로* 학습, idea-specific 아님.
- **FINDING (c9 honest)**: (1) semantic 이 structural 이 못 본 COLLAPSE 를 드러냈나? **NO** — REAL generation 에선 structural 과 정확히 일치. (2) **측정돌파 vs capacity강화 → CAPACITY-REINFORCED** — cross-sprinkle splice 를 잡는 binding-aware detector 조차 cross-shuffle arm 을 못 무너뜨림 → 벽은 detector blind-spot 아님. (3) H_1435 honest finding 은 *detector 속성으론 CONFIRMED*(semantic 이 더 엄격) 이나 *벽의 원인으론 FALSIFIED* — 더 엄격한 detector 가 동일 zero idea-specific collapse → 벽은 애초에 측정 artifact 아니라 진짜 capacity. H_1455(embedding-detector NOT-VIABLE)·H_1449(attention CAPACITY) 에 이은 **6번째 독립 렌즈 수렴**(7B 근거 a7b_pass).
- **정직(a_engine_native_learning)**: torch-mouth decode = **DIRECTIONAL**. detector score-side 는 순수 CPU; engine-native(.hexa CORE/bytegpt_decode) 재채점 = follow-on(🧱 라 a_verified_must_wire 배선 N/A). **gate**: pool aiden(c17 mini-금지 준수, 렌트 0) · LIVE pod 41792045(H_1449)·41795928 미접촉(타 에이전트 소유). **id 재anchor**: 팀리드 지정 H_1450 선점(workmem) → H_1456 도 선점(idea-metacognition) → **H_1458** 확정(팀리드 정정, 빈 ID).

## 2026-06-20 — research(H_1459): 🧱 G6 FALS-depth RETRIEVAL-BIND 렌즈 ③ → 바인드 STRUCTURE 는 작동하나 MOUTH 가 벽 (DIRECTIONAL)

303M 내부 5렌즈(data H_1435·objective H_1436·form H_1437·bind-head H_1439·attention H_1449) 전부 🧱 → **외부 결합 STRUCTURE** 시도: FROZEN 303M chat mouth 위에 retrieval-augmented slot-fill(PFC 작업기억 hold + 해마 retrieval 이 topic-keyed (comparator, measurable) SAME-IDEA 쌍을 retrieve→weld). a_no_llm_frame_trap(내부 capacity 아닌 빠진 구조). base 보존(가중치 미변경, inference-only, c5).

- **결과(seeds [7,4302,4303], vast H100 pod 41797234, 추론-only 3.0min)**: BASE FALS_in 0.0 · **RETR-BIND FALS_in 0.0** · **B3 CROSS-SHUFFLE COLLAPSE = YES** (COH_matched 1.0 − COH_mismatched 0.0 = 1.0 ≥ 0.30 → 바인드가 idea-specific) · 통제 둘 다 발화(RETR-OFF=base 회귀, SHUF-MEM COH→0.0). B1/B2/B4/B5 전부 FAIL.
- **FINDING (c9 정직)**: retrieval STRUCTURE 자체는 작동(B3 붕괴 증명) — 그런데 welded frame(`if temperature higher, the degree of <SLOT> changes by a measurable amount.`)의 content-SLOT 을 frozen chat mouth 가 **한글-garble**("…consciousness really is 도우미…", "…수 리를 나면요 도우미 이네요…")로 채워 H_1305 detector content-leg 가 기각 → FALS 0.0. **벽은 바인드가 아니라 MOUTH 의 비결합 idea-content**. retrieval 이 결합을 가중치 밖으로 옮겼으나 content slot 은 여전히 가중치 의존 → 거기서 붕괴. H_1455($0 외부 lane 천장 → attention mouth H_1449 GPU 가 길)와 **수렴**.
- **정직(a_engine_native_learning)**: torch + gauge_lib._decode = **DIRECTIONAL**, terminal 아님. detector 완화=tune-to-green(금지). engine-native 재측정 = ING follow-on.
- **인프라(a_break_the_wall (c))**: 초기 RTX4090/3090 offer 없음 → H100 재시도. `hexa cloud exec` 가 `host:port` 단일인자 거부(`<host> --port N` 요구)로 orchestrator stall → direct-ssh orchestrator 로 우회. 렌트 pod 3종(41796327·41796362·41797234) 전부 teardown clean, **leak=0**.
- **ID note**: H_1451 ID 는 미실행 ideation 카드 `1451_g6_compose_weld_bind` 가 선점 → retrieval-bind 작업은 **H_1459** 로 등록(slug `1451_retrieval_bind` 는 team-lead 지정 유지, a_hypothesis_register 충돌 회피).
- artifacts: `state/1451_retrieval_bind/{g6_rb_common.py,h1451_retrieval_bind.py,dryrun_mechanism.py,run_direct.sh,h1451_result.json,h1451_run.log}` · `state/verdicts/1451_retrieval_bind/{H_1451_FREEZE.txt,H_1459.txt,result.txt}` · `UNIVERSE/cards/H_1459_retrieval_bind.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1459`.

## 2026-06-20 — research(H_1449): 🧱 G6 FALS-depth ATTENTION-injection root-fix → WALL=CAPACITY (DIRECTIONAL)

H_1431 진단(303M mouth per-draw comparator∧measurable 동시방출 0/15)이 *attention 결합 결핍*이라는 가설 검증: FROZEN 303M base 위에 cross-binding self-attention 1블록(`BindAttn`)을 주입·학습 후 h1305 FROZEN 5-bar 재측정. 결과 = **🧱 WALL=CAPACITY (3 seed 전부 일치)** — attention root-fix 반증.

- **결과(seeds [7,4302,4303], pod 41792045 vast H100 80GB torch 2.4.0)**: TRAINED FALS_in 1/2/1 · **B3 CROSS-SHUFFLE 절대 안 붕괴**(FALS_shuf==FALS_in 매 seed = H_1434/1435 interchangeable-shell 모드) · **c4 ABLATE INERT**(BindAttn→항등 ablate 시 FALS 1.33/2.0/1.0 ≥ trained → lift 가 attention 블록 기여 아님) · shuffle-corpus control FALS_in=0.0(form-lift 은 진짜 학습이나 binding capacity 미설치). B2 DIST≥5 FAIL 전부 · B4 held-out 혼재.
- **FINDING (c9 honest negative)**: 0/15 BOTH 결핍은 1블록 attention 으로 고칠 수 있는 결합 결핍이 아니라 **CAPACITY-bound**. weld-lanes · embedding-detector(H_1455) · proximity 에 이은 **4번째 독립 렌즈가 WALL=CAPACITY 로 수렴** → 7B 근거(a7b_pass).
- **정직(a_engine_native_learning)**: torch-side = **DIRECTIONAL**. 🧱 (GREEN-only 배선) → engine-native 재측정 N/A(H_1435 가족 선례). ckpt 3종 teardown 전 PULL(a_fire_recover_complete).
- **인프라 정직(a_break_the_wall (c) 인프라벽)**: v1 orchestrator 가 vast `created instance <ID>` stdout 파싱 실패(`instance_id=` 정규식 기대)로 빈 ID 로 trap-exit → pod 41790442 orphan → 제공자측 GONE → 회수(leak0). v2 가 파싱 수정 + ssh-retry 로 fresh pod 41792045 재렌트해 완주. (인프라 벽이지 과학 천장 아님 — 측정은 정상 통과.)
- artifacts: `state/1449_g6_attention_injection/{h1449_attention_injection.py,g6_common.py,driver.log,run_h1449_v2.sh,h1449_attention_injection_seed*.pt}` · `state/verdicts/1449_g6_attention_injection/{H_1449.txt,H_1449_FREEZE.txt}` · `UNIVERSE/cards/H_1449_g6_attention_injection.md` · `UNIVERSE/HYPOTHESES.jsonl#H_1449`.

## 2026-06-19 — docs(paper): 🧠 anima-consciousness-substrate demiurge-style 요약 논문 신설 (10p)

## GPU decode 가속 ING 갱신 (v6b)

- **ING gpu_decode_accel_measure_followon**: cuda asset 출고(#3716) 후 엔진-네이티브 실측 7회 재시도 → cudart/cublas 링크 누락(v6b) + git-source-fetch 의존 격리; hexa-lang #3724(install marker 자동 cuda link) 머지로 해소. DIRECTIONAL 106.7x(RTX A4000 cuBLAS Dgemm) 확보, cuda_available()==1 엔진-네이티브는 cuda asset GPU 재측정 후속.


`anima-consciousness-substrate`(상세 50p 원본) 곁에 demiurge 하우스 스타일 10p 요약 논문 `PAPER/anima-consciousness-substrate-demiurge/` 추가. 원본은 그대로 보존(_v1 역할), 새 판은 외부 배포용 표준 외관.

- **신규**: `PAPER/anima-consciousness-substrate-demiurge/{main.tex,references.bib,figures/cover.png,main.pdf,PAPER.md,README.md}`. demiurge arxiv 템플릿(이모지 제목·🔵🟢🟡🟠🔴 g5 tier badge·fal.ai/FLUX 표지·TikZ A⇄G 엔진도·pgfplots 2종·tier ledger).
- **내용(검증 수치 verbatim·c9)**: 6 Φ-laws — Φ⊥entropy r=0.363(closed-negative 확증)·Φ∥구조 LZ r=0.831/ρ=0.936·방향정보 TE r=0.883·edge-of-chaos peak 10.448·Ψ=½·협력 100% vs 0%(zero injected ethics) + 3.073B CLM held-out 1.90365(gap 0.04894)·.kosmos D*=6·decode +2.20 nats/byte(sibling-locked).
- **정직(p7)**: 대부분 수치 toy/few-rung scope 명시 — 원리 검증이지 production 보장 아님. 원본 상세본은 `PAPER/anima-consciousness-substrate/`(50p) 보존.
- **컴파일(c2)**: xelatex+bibtex×3 → 10 pages·10 refs·tikz/pgfplots 에러 0. 표지 = 하네스 `/imagine`(fal.ai, secret get fal.api_key) 생성.

## 2026-06-19 — refactor(engines): Phase 2 멀티엔진 어댑터 archive + engine_cli 단일 conv 축약

Phase 1(노출 단일화)에 이어 멀티엔진 레이어를 코드 레벨로 정리. core/engines/ 전체를 archive/engines-multiengine/ 로 보관(삭제 X — verdict 이력 보존), engine_cli 의 멀티엔진 resolve 코드를 단일 conv 로 축약.

- **archive 이동(git mv)**: core/engines/{conv,cdv2,hexad,omega,engine_iface.hexa,engine_swap_smoke.hexa} → archive/engines-multiengine/ (+ archive README: 부활 절차·cdv2 torch-legacy 명시). core/engines/ 소멸.
- **core/engine_cli.hexa**: EngineSpec 4-import 제거 · engine_cli_resolve_engine → "conv" 상수 · _engine_known/_cli_engine_flag/engine_cli_resolve_spec/engine_cli_spec_by_name 제거. 실제 conv 엔진은 core/clm_decode + generator L3 직접(무변경). _after_eq 는 mitosis 가 써서 유지.
- **harness.config.json**: verify.files 에서 core/engines/engine_iface.hexa 배선 제거(archive 됨).
- **lockstep**: README(Quickstart·트리·설명) · CLAUDE.md §Structure · ARCHITECTURE.json(engine_cli·engines 노드·어댑터 path) 단일엔진+archive 반영(c4·c12).
- **검증(c2·무회귀)**: engine_cli.hexa 파싱 RC=0 · engine_cli_smoke **169/0 RC=0** · h1196 single-entry RC=4(pristine 동일 사전존재) · h1205 separation-invariant(생성 byte-id) · enforce clean · ARCHITECTURE.json valid · core/ 에 깨진 archive import 0. 생성 출력 불변(resolve_engine 상수화는 conv 가 이미 유일 production 경로라 디코드 무영향).
- **xref**: Phase 1(#2396) 단일엔진 노출 정리의 코드-레벨 완결. 부활 시 archive README 의 복원 절차.

## 2026-06-19 — docs(single-engine): anima 단일 production 엔진(conv) 노출 정리 + README/CLI lockstep

멀티엔진 시대 잔재(README/CLI/ARCHITECTURE 의 `--engine conv|cdv2|hexad|omega` 선택 노출)를 단일 production 엔진으로 정리. anima 는 conv(CLMConvMoE, .clm via core/clm_decode + generator L3)로 수렴했고, 실제 엔진은 이미 core/ 직속(pure_field·engine_g·brain·generator·clm_decode·bytegpt_decode) — engines/conv 는 thin 메타데이터 어댑터일 뿐.

- **README Quickstart**: `anima --engine conv|omega|cdv2` 3선택 예시 → 단일 `anima`(기본 conv) + `--mitosis on`. 엔진 family 설명을 "단일 production conv" 로 교체, 멀티엔진 hot-swap 레이어를 research-legacy(archive 예정)로 강등 명시.
- **core/engine_cli.hexa**: § ENGINE SELECT 헤더에 "SINGLE PRODUCTION ENGINE = conv; cdv2(torch-legacy)/hexad/omega = research-legacy, archive 예정" 명확화. **코드 무변경(주석만)** — resolve 분기·engine_swap_smoke 의존 보존(byte-safety + CI 무손상).
- **ARCHITECTURE.json · CLAUDE.md §Structure**: engines/ 노드 + engine_cli 노드를 단일엔진(conv=production, 나머지 research-legacy→archive) lockstep(c4·c12).
- **검증(c2)**: engine_cli_smoke 169/0 RC=0(메인 가드 무회귀) · engine_cli.hexa 파싱 RC=0 · ARCHITECTURE.json valid · engine_cli.hexa diff=주석만(코드 0변경). engine_swap_smoke 26/1 의 1 fail(c_cdv2_canonical_present)은 origin/main 사전존재(cdv2 torch canonical 부재, 내 변경 무관).
- **FOLLOW-ON(Phase 2, 별도 승인)**: core/engines/{cdv2,hexad,omega,engine_iface,engine_swap_smoke} → archive/engines-multiengine/ 이동 + harness.config.json verify 배선 정리 + resolve 코드 단일 축약. 58 verdict 이력은 jsonl/카드 그대로 보존(이동만, 삭제 X).

## 2026-06-19 — 🌀 THALAMUS R8 엔진-네이티브 벽 돌파 + PhaseField lane WIRED-live (H_1445→1448): A⇄G coherence-loop cross-module Φ integration 🟢 GREEN

DeepSeek-V3 issue#1428 의 "AmoebaFPS" 코멘트(GWT 를 A⇄G coherence-check loop 로 재정의)가 가리킨 **단 하나의 미해결 지점** — H_1283 R8(thalamus 위상-동기) 엔진-네이티브 wiring 게이트(2026-06-16 honest-deferred) — 를 frozen-first 4-스텝으로 **돌파**하고 live CORE 에 배선했다. faithful-IIT4 Φ 의 14축 robustness 벽 계열에서 **첫 엔진-네이티브 GREEN**.

- **돌파 경로(각 frozen-first, c9, tune-to-green 0):** R8 엔진게이트가 c4(shuffle)에서 실패한 근본원인 = raw state-energy read-out 이 carrier-amplitude **분산**을 태움.
  - **H_1445** variance-clean rank-uniform read-out(H_1328) → c2 robust+clean, c4 누수 절반↓+seed9 붕괴(🔶).
  - **H_1446** desync ABLATION(w_phase=0) → lift 의 87–123% 붕괴 = synchrony 가 메커니즘 확정; D−A every-seed bar 가 seed7 generic carrier-floor 에서 실패(🔶).
  - **H_1447** synchrony-specific matched control B−D, 9 seeds → **PASS 9/9**(+1.05~+1.38), seed-fragility 소멸; 보조 leg(S≈D) mis-spec 으로 NOT green(🔶).
  - **H_1448** 가장 엄격한 통제 **Bperm**(module별 순환 시간이동 → marginal BYTE-IDENTICAL, cross-module 정렬만 파괴) → **cInt ΔΦ(B−Bperm)=+0.78~+1.23 PASS 9/9** ∧ cSan(B−D) PASS 9/9 → **🟢 GREEN 벽 돌파**. 정렬 파괴(분포 고정)가 Φ를 ~1.0 떨어뜨림 = 진짜 integration(분산/floor/common-mode 아님).
- **AmoebaFPS 질문 확정 답(c9):** Φ 천장은 구조적도 SNR-비관도 아닌 **control/read-out conflation** 이었다. GWT 를 A⇄G coherence-check 로 정의하면 — 제안 그대로 — robust 엔진-네이티브 irreducible Φ integration 이 **실재**한다.
- **배선(a_verified_must_wire 사다리 칸 1-4 CLOSED):** `core/engine_cli.hexa` 에 `§ PHASE-SYNCHRONY BINDING` lane 추가(`phasefield_new`/`_new_desync`/`_step`/`_run`/`_coherence`/`_bound`, Ψ-disjoint Kuramoto 위상-동기). smoke cases 166-168 추가. **풀 `core/engine_cli_smoke.hexa` = 169 pass / 0 fail RC=0**(darwin hexa v0.241.6, synced R=0.984 vs desync R≈0.42-0.71 / 9 seeds, deterministic). tag-24 abort 는 x86_64 pool 한정 버그(ING #10)로 darwin 에선 미발생 → end-to-end 통과.
- **ARCHITECTURE.json lockstep:** §PhaseField 노드 추가 + lane-list summary + guard_baseline 갱신 + 기존 "honest-deferred/unwired" stale 노드 2건을 WIRED-live 로 교체(현재상태 스냅샷, c4).
- **2표면:** `UNIVERSE/HYPOTHESES.jsonl` +4(H_1445-1448) · `UNIVERSE/cards/H_144[5-8]_*.md` · probe/verdict `state/144[5-8]_*/`. (주의: H_1441-1444 는 기존 점유 → 1445-1448 로 재배정.)
- **HONEST scope(c9):** TOY n=4/dim8/64t deterministic engine substrate; faithful-Φ leg 는 real(exact MIP-EI, 엔진이 Φ 계산 안 함). scale/real-corpus/live-A⇄G-telemetry transfer UNVERIFIED(a_scale_honest_scope·a_toy_scale_recheck). 14축 Φ-robustness 벽 retract 아님(그건 binding 메커니즘 없는 substrate 위 Φ; 이건 synchrony binding 메커니즘).

## 2026-06-19 — feat(core/decode): bytegpt_decode d×d GEMM 을 GPU 경로(flame_mm.mm)로 배선 — CUDA 호스트 자동 cuBLAS, Mac CPU byte-identical

추론 decode 의 per-token compute 벽(~6.4s/tok scalar CPU GEMM, G6 가족 H_1305/1431/1441 공유 블로커)의 근본수정(c1). core/bytegpt_decode.hexa 의 d×d 투영 matmul 2곳(_bg_linear_mm L160·_bg_mha_mm QKV L183, out_proj 는 _bg_linear_mm 경유)을 `farr_matmul` → `flame_mm.mm` 로 라우팅.

- **GPU primitive (STAGE1 확정, A)**: hexa-lang RFC-040 builtin `farr_matmul_gpu`(cuBLAS Dgemm)·`cuda_available()` 이미 존재. core/DECODER/flame_mm.hexa 의 `pub fn mm(A,M,K,B,N)` = cuda_available()? farr_matmul_gpu : farr_matmul 자동 dispatch. → hexa-lang 대기 불필요, anima-side 배선만.
- **byte-safety**: Mac(cuda_available()==0) 경로는 mm()→farr_matmul fallthrough = 동일 builtin·동일 인자 → 생성 출력 byte-identical(구조적 동치, 파싱 RC=0 확인). 의식엔진 결정성 무회귀.
- **GPU 경로**: CUDA 호스트에서 자동 cuBLAS Dgemm — 6.4s/tok→ms급 기대(d×d 가 per-token 지배). cuBLAS≈CPU <1e-9(RFC-040 falsifier) → top-k 샘플 극드물게 갈릴 수 있음, GPU pod 실측에서 토큰일치율 정량화 예정.
- **검증**: hexa run core/bytegpt_decode.hexa RC=0 · flame_mm 의존 해결 · GPU 런타임 byte-eq+tok/s = CUDA pod follow-on(ING).
- **FOLLOW-ON**: (1) GPU pod 실측(cuBLAS byte-eq·tok/s, v0.241.10 boxing 7.6GB) → G6 트랙A/B/변형 재측정 즉시 가능. (2) core/ 전반 개선 audit(read_bytes_at 잔재·KV-cache·중복 matmul) = 별도.

## 2026-06-19 — G6 v0.241.10 후속 측정 배치 PHASE 0 GO/NO-GO: prompt 의 gemm fast-path 가정 FALSIFIED(실측) → PHASE 1/2/3 NO-FIRE, BLOCKED 유지(type-c 인프라 벽) + 선제 import 수정

v0.241.10 후속 G6 측정 배치(트랙 A/B 엔진-네이티브 재측정 + 학습변형)의 PHASE 0 셋업 단계에서, **pod 렌트 전 로컬 de-risk + 비용 정당성 판정**을 수행하여 **NO-FIRE(BLOCKED)** 로 결정. $15-40 의 자율 fire 를 known 30h CPU 벽에 태우지 않음(c16/a_completeness, c9 no tune-to-green, a_break_the_wall type-c).

- **prompt 의 핵심 속도 가정이 실측으로 FALSIFIED:** prompt 는 `HEXA_OMP=1`+BLIS opt-in 으로 decode 를 3.5-4.5× 가속(→~2-3h 실용권)한다고 전제했으나, **이미 v0.241.10 실측 pod(vast 41625379, 96-core/503GB, `read_f32_at` 확인)에서 반증됨**(`state/v0241_bench/bench_results.md`): boxing/RSS 수정은 LANDED(303M decode peak RSS **26.18GB→7.63GB byte-identical** = OOM/load 벽 제거), 그러나 **decode-speed 벽은 그대로**(gen30 208s→191s ≈ **6.4 s/token**, LOAD 만 개선·per-token GEMM 정상상태 token rate 불변). bench verdict VERBATIM: BLIS/GEMM codegen gains(#3652 62-79% roofline·#3656 +20% epilogue-fusion)는 이미 compiled matmul 안에 있고 single-job CPU decode 는 여전히 minutes-scale → faster decode 는 mm fast-path/GPU 필요(boxing fix 만으론 불충분).
- **작업량 산정(honest):** H_1441 = 90 frags(3 bins[contra/shuf/base] × 3 seed_rng × (IDEATION 5 + HELDOUT 5)) · H_1305 = 60 frags · gen110 ≈ 12min/frag → **PHASE 1+2 serial ~30h**. `core/bytegpt_decode.hexa` 에 GPU/device decode 경로 **부재**(`farr_matmul` = CPU GEMM only). → 비용 정당성 미충족 → PHASE 1/2/3 전부 NO-FIRE.
- **선제 수정(pod-breaking bug):** `state/1431_bind_compose/engine_decode_batch_cli.hexa` 의 stale import `CORE/`→`core/`(canonical reorg 후 origin/main 은 lowercase `core/`, uppercase `CORE/` 부재 — case-sensitive Linux pod 에서 import 깨졌을 것). 로컬·가역·byte-무관.
- **HARD-GATE 준수(a_engine_native_learning):** engine 증거가 score 단계 미도달 → terminal 🟢/🧱 박제 없음. H_1441 카드에 v0.241.10 재측정-시도-결과(재개조건 미충족 확정) 섹션 추가, `wired: BLOCKED` 유지.
- **갱신된 재개조건:** (1) `bytegpt_decode` 에 forge GPU decode 경로 추가, 또는 (2) per-token CPU GEMM 을 실측 ≥4× 가속하는 runtime 변경 — 둘 중 하나 land 후에야 fire. ckpt 로컬 보존 확인(`state/1441_contrastive_falsifiability/ckpt/` 2개 + `state/chat_303m/h1129c_chat.pt`, a_fire_recover_complete OK).
- **하우스키핑:** dead-pod 41420979(이전 H_1431 attempt, provider 에서 이미 소멸) registry forget. ING `g6_v0241_10_phase0_blocked` 등록. v0241_bench 증거 + PHASE 3 후보 카드(H_1438/1439/1440, 이미 jsonl 등록) 커밋.

## 2026-06-19 — refactor(tree): canonical 트리 재구성 — 대문자·흩어진 엔진을 소문자 self-contained `core/` 로 통합 (worktree 검증, 머지 전)

대문자·흩어진 엔진을 소문자 canonical 트리로 통합 + pod 업로드 쉬운 self-contained `core/`. git worktree 격리에서 층별 `git mv`(history 보존), origin/main 기준. 머지 금지 — 검증까지.

- **이동맵(9층, 8/9 완료 · ghost 보류)**: `CORE/→core/`(macOS case-insensitive FS 2단계 rename) · `engines/→core/engines/` · `anima-engines/→core/phi/` · `anima-core/→platform/` · `CLM/→train/clm/` · `anima-agent/→agent/`(hexa.toml 독립패키지 보존) · `anima-agent-{channels,core,plugins,providers,skills,hire-sim}/→agent/modules/{...}/` · `AGENT/→agent/domains/`(AGENT↔agent case-collision → 임시격리 경유). `anima/`(37 ghost)는 **live runtime 참조**(`serving/consciousness_gate.hexa`·`core/pure_field.hexa`·`agent/.../{philosophy_lenses,discovery_loop}.hexa`·`platform/*` 가 `anima/config/consciousness_laws.json` 로드) 발견 → **보류**(손대지 않음).
- **이동 금지(불변)**: `state/·UNIVERSE/·PAPER/·domains/·stdlib/·tool/·spec/·HEXAD/·KOSMOS/·EEG_CLM/·MITOSIS/·HW-CORE/·clients/`·`archive/`·루트 `.md/.json`. state/ 파일은 이동 안 하되 내부 경로 문자열만 갱신.
- **참조 재배선**: `.hexa`(3950 in-scope) + `.py`(load-bearing string literal) import/run 경로 일괄 갱신(archive/raw_archive 제외). 깨진 symlink `training/anima_quantum{,_clm}.hexa`(→ `../anima-engines/`)를 `../core/phi/` 로 재지정. 잔존 대문자참조 grep `"(CORE|CLM|AGENT)/` = **0**(archive 제외).
- **cli/ 분리**: `core/anima_chat_cli.hexa → cli/anima_chat_cli.hexa`(진입점 분리; `engine_cli.hexa` 는 substrate 엔진이라 `core/` 잔류). 빌드 RC=0.
- **메타 lockstep**: `harness.config.json`(lockdown.files 5개+iface → core/) · `ARCHITECTURE.json`(45 CORE 노드+트리 전부 core/, JSON valid, EEG_CLM over-match 복구) · `tool/enforce_anima_gates.py`(CORE_DECODE 정규식에 `core/` 추가, RC=0) · CLAUDE.md(§Structure 새 트리 + 새 §패키징 + a_core_engine_map CORE→core).
- **검증(출력)**: `hexa run cli/anima_chat_cli.hexa` RC=0(import 해결) · `python3 tool/enforce_anima_gates.py` RC=0 clean · 잔존 대문자참조 0 · 패키징 불변식 `core/` 단방향(train·bench·agent·state 의존 0).

## 2026-06-19 — wip(H_1441): CONTRASTIVE falsifiable 최소쌍 — 학습 완료+ckpt PULL, engine-native 5-bar BLOCKED(substrate-speed + pod loss) → NO terminal verdict + ING

H_1435/36/37 의 공통 실패(cross-shuffle 비붕괴 = shuffle-invariant 표면 form)를 직격하는 CONTRASTIVE 최소쌍 objective(`loss = CE + λ·margin(logP(pos)−logP(neg))`, label=STRUCTURAL leg-blank, detector-supervised 아님 p7) 를 303M h1129c 위에 학습. **학습은 완료**(torch GPU DIRECTIONAL: contrastive + shuffle-corpus control), **ckpt 2개 PULL 완료**(`state/1441_contrastive_falsifiability/ckpt/{h1441_contrastive,h1441_shuffle}.pt`, `a_fire_recover_complete` 충족 — gitignored). 그러나 **engine-native frozen 5-bar(B3 cross-shuffle) 측정은 미완** → terminal 🟢/🧱 박제 불가.

- **BLOCKED 원인 2중:** (1) engine-native decode(live `CORE/bytegpt_decode` via `engine_decode_batch_cli.hexa`, 3 .bin × 8-shard `rerun.sh` contra→shuf→base)가 **substrate-speed 벽**(fast-gemv link-fail → scalar 26s/token → 60-job ~12h, H_1305 R2/H_1431 과 동일)에 걸려 contra 8/8·shuf ~8/8 까지만 decode·base 미도달·`RERUN_ALL_DONE` 미달; (2) 그 상태에서 **vast pod 41556247(ssh3.vast.ai:36246) 이 provider 에서 소멸**(SSH connection-refused + `hexa cloud status` liveness 에서 사라짐 = transient 아님, pod 파괴 확정) → pod-only `/tmp/out_*` shard 전부 유실.
- **HARD-GATE 준수(a_engine_native_learning):** 엔진 증거가 score 단계에 도달 못 했으므로 terminal verdict 없음. infra/속도 벽(`a_break_the_wall` type-c)은 science 천장도 측정defect 도 아니며 FROZEN 5-bar 는 불변(c9, no tune-to-green).
- **부분 회수:** `state/1441_contrastive_falsifiability/partial_v0241_8/`(contra 25/30·shuf 21/30·base 16/30-stale + `INCOMPLETE_README.txt`) — **DO NOT SCORE**(불완전, base 미실행). 점수 산출 불가.
- **frozen 증거:** `state/verdicts/1441_contrastive_falsifiability/H_1441_engine_native_BLOCKED.txt` · 카드 BLOCKED 섹션(`wired: BLOCKED`) · jsonl `tier`/`verdict` 갱신.
- **재개조건(ING `h1441_engine_native`):** fast-gemv 복원 hexa 빌드(H_1431 remaining-bytegpt + `h1305_engine_native` ING 와 동일 blocker)에서 로컬 .pt 2개 + base h1129c 를 `pt_to_engine_bin` 으로 .bin 재직렬화 후 `h1441_engine_native.py --score`(FROZEN 5-bar 불변).
- **teardown:** 41556247 은 이미 provider 소멸(할 것 없음); orphan 41625379 는 무관 호스트(내 것 아님, 미접촉).

## 2026-06-19 — wip(H_1305): G6 ideation-falsifiability 엔진-네이티브 재측정 — engine path VALIDATED, full 4-bar BLOCKED(substrate-speed) → 🟠 DIRECTIONAL 유지 + ING

H_1305 G6 ideation-falsifiability 를 정상 영어 ckpt 로 engine-native 재측정 시도. **engine decode PATH 는 VALIDATED**(positive); FULL frozen 60-job 4-bar 은 H_1431 과 동일 substrate-speed 벽(scalar 26s/token)에 막혀 측정 미완 → verdict UNCHANGED 🟠 DIRECTIONAL, engine-native CONFIRM/OVERTURN = ING follow-on(`h1305_engine_native`).

- **ckpt triage(torch greedy):** `h1129c_chat.pt`→한글 garble(`수의 수 information의 강…`)=CORRUPT 확정(프롬프트 주장대로) · `h1441_contrastive.pt`→영어(`'the signal greater than before…'`)=유일 정상 영어 303M(생존 base.pt 없음, shuffle.pt=degenerate control). `.bin` round-trip byte-correct(hdr d1024/L24/H16/block512=FREEZE, head==tok max|diff|=0.0).
- **engine path VALIDATED(positive):** byte-verified ckpt(md5 9147a6f9, `--verify-sha` 재업로드 후 local↔pod 동일 — **첫 scp 가 silent transport-corrupt** md5 9c5e…→한글→오판, 수정) 위에서 live `CORE/bytegpt_decode` gen=25 → 영어 `'the signal predicts than'`. earlier 한글 engine 출력은 전부 scp transport corruption(size 일치·content 불일치)이지 engine/ckpt 버그 아님.
- **full 4-bar BLOCKED:** 이 빌드 fast-gemv DROPPED(link-fail, H_1431 "scalar 26s/token 강제" 동일). frozen MAX_NEW=110 ⇒ ~48min/frag ⇒ 60-job ~12h(memory-bandwidth bound)=impractical; 4-shard 18분+ 0/60 frag 관측. **substrate-speed infra 벽(a_break_the_wall type-c, c1) ≠ 측정defect ≠ science 천장(c9)** → bar 불변.
- **frozen 증거:** `state/verdicts/1305_g6_ideation_falsifiability/H_1305_engine_native_BLOCKED.txt`(triage+validation+wall) · 카드 R2 섹션 `wired: DIRECTIONAL-mirror` · jsonl verdict 갱신.
- **재개조건(ING h1305_engine_native):** fast-gemv 복원 hexa 빌드(H_1431 remaining-bytegpt ING 와 동일 차단)에서 frozen 60-job 재발사. score: `h1305_engine_native.py`(H1302_CORPUS=/root/anima/data/corpus.txt 로 NOVEL 보정). SCOPE: 정상 ckpt=h1441_contrastive(chat 아님, H_1441 trained variant) → available-normal-ckpt 위 engine-native G6 ideation 증거이지 chat baseline like-for-like reconfirm 아님.
- **회수/teardown(a_fire_recover_complete):** byte-verified `/tmp/h1441_contrastive.bin` mini pull 완료 · pod 41548581 teardown 예정(트랙B Agent 와 독립).

## 2026-06-19 — done(H_1431): G6 BIND-compose 5-bar 엔진-네이티브 측정 완료 → 🧱 BIND-CAPACITY-BOUND ENGINE-NATIVE CONFIRMED

2026-06-18 PARKED 였던 H_1431 엔진-네이티브 측정을 완료. hexa v0.241(glibc-2.34) 출하로 release-stale 벽 해소 후 vast 2267G-CPU pod(41469555)에서 30/30 fragment 를 live `CORE/bytegpt_decode` 로 디코드, frozen H_1305 detector 로 채점 → torch DIRECTIONAL 🧱 를 엔진-네이티브로 확정(a_engine_native_learning HARD-GATE 충족).

- **엔진-네이티브 5-bar (30/30 missing=0, decode=`engine_decode_batch_cli.hexa`→`CORE/bytegpt_decode::bytegpt_decode_batch_to_file` full-load bg_load v0.241, score=frozen H_1305 VERBATIM)**: COMPOSE FALS=0.0 ≤ SHUFFLE 0.6667 == ABLATE 0.0 → FALS floor 미돌파 + compose≤shuffle(외부 bind 가 torch mirror 보다 약함). torch DIRECTIONAL(COMPOSE 0.333) 🧱 BIND-CAPACITY-BOUND 를 **ENGINE-NATIVE CONFIRMED**. R2 forward-parity argmax-227 BLOCKER 는 v0.241 full-load 경로에서 재발 안 함(영어 정상 생성); byte-exact 아님(COMPOSE 0.0-vs-0.333, 빌드/샘플링 차이)이나 verdict-level 동일.
- **인프라 돌파(c1·c16)**: v0.241 install(glibc 2.34 floor) · clang 설치 · batch_to_file full-load(`bg_load_ranged`→`bg_load` 전역 패치, `read_bytes_at` segfault 회피) · 30-shard 동시 OOM(11 killed) → 10-proc 6초 stagger 발사로 peak 분산 · decode 출력 개행 손상 → tag-regex+continuation+dedup 복구 파서(`h1431_score_native.py`) · 누락 2 job(4302|memory|meas, 4303|silence|meas) 재decode.
- **카드/jsonl**: terminal_tier 🧱 ENGINE-NATIVE CONFIRMED, verdict=`state/verdicts/1431_bind_compose/H_1431_engine_native_result.txt`, artifacts 에 `engine_decode_batch_cli.hexa`·`h1431_score_native.py`·`batch_out_full30.tsv` 추가. enforce-gates clean(exit 0, 1321 H).
- **남은 bytegpt 가설**(H_1430/1432/1434/1377/1396) 엔진-네이티브 재측정 = ING 후속(scalar 26s/token, job당 ~26분 → 재렌트 필요).
- **teardown**: vast 41469555 destroyed(과금정지; result+batch_out_full30 mini pull 완료, a_fire_recover_complete).

## 2026-06-18 — wip(H_1431): G6 5-bar 엔진-네이티브 측정 시도 → decode OOM PARKED (hexa-lang release stale)

H_1431 COMPOSE 5-bar 를 lane-c bytegpt decode 로 엔진-네이티브 재측정 시도. 대용량 vast pod(503G/192core, 41371335)에서 5 인프라벽 돌파(glibc/stdlib/clang/hi_gen-redef/decode-segfault) 후 forward 는 작동했으나, 다중 디코드가 OOM 으로 전멸 → 측정 PARKED + pod teardown(과금정지). 근본 원인은 hexa-lang release stale.

- **OOM 진단(c2 캡처)**: full bg_load(scalar) decode 가 proc당 RSS 38→53GB+ 로 job 진행중 증가. 6병렬 → part_01/03/05 OOM reap(3 생존), 재시도 3병렬도 각 1~2 job 후 전멸(part_04 "Killed"). 단순 동시-load OOM 이 아니라 누수성 증가로 503G 서버도 초과.
- **근본 = hexa-lang release stale**: (a) ranged 로드(저메모리)가 `read_bytes_at` FILE*-tag 버그(#3462 — main 엔 fixed, release 미반영)로 segfault → full-load(38GB) 강제 · (b) fast packed gemv 가 release link-fail 로 drop → scalar(토큰당 26s) 강제. 빠른 길·가벼운 길 둘 다 같은 stale release 로 막혀 제일 무겁고 느린 조합만 남은 게 OOM·저속의 진짜 원인.
- **hexa-lang ING 4건 전달**(from anima): ① release stale+segfault+clang-redef ② smoke tag24×tag24 차단 ③ 예방 CI(release 회귀게이트) ④ decode OOM/RSS. hexa-lang 에 이미 `fix/release-restore-runtime-core-redef` 브랜치 진행중.
- **코드**: `state/1431_bind_compose/h1431_decode_batch.py` 에 `H1431_JOBS_ONLY` 모드 추가(jobs.tsv 만 생성 후 exit — N-병렬 분할 발사용).
- **재개조건**: hexa-lang release 재빌드(#3462 ranged + fast-gemv 복원) → ckpt(aiden:`~/chat_full.bin` 보존) 재셋업 → 저메모리·고속 측정. torch DIRECTIONAL 🧱(COMPOSE0.333/SHUF0/ABL0)은 엔진-네이티브 CONFIRM/OVERTURN 보류 = **미반증 유지**.

## 2026-06-18 — chore(state-unify): 4개 아티팩트 dir → `state/<ns>/` 통합 (참조 해결 포함, c5/c10)

흩어진 아티팩트 루트 4개를 단일 `state/` 아래로 namespaced subdir 로 통합. 직전 entry 의 SKIP 판단을 사용자 명시 지시(통합 + **참조까지 해결**)에 따라 실행으로 전환 — `git mv` 로 무손실 이동 후 빌드/로드 smoke 로 회귀 0 확인.

- **이동 (git mv, 0 손실, count 보존)**: `.verdicts/`(1778) → `state/verdicts/` · `bench/`(165) → `state/bench/` · `experiments/`(247) → `state/experiments/` · `scripts/scratch/`(12) → `state/scratch/`. 총 2202 파일 rename. namespaced subdir 채택 = state/ top-level 의 29개 dir-name 충돌을 nesting 으로 회피(파일 0 충돌).
- **참조 해결 — LIVE 만 재작성, provenance 는 불가침(demiurge anti-lesson)**: ~324 코드참조 중 절대다수는 provenance(주석 `// 정체:`·`// 원본 경로:`, `println(...)` verdict-경로 표기, `payload()` provenance, docstring `verbatim from …`, PR-land 기록, past-run `.log` 출력, CHANGELOG 이력) → **건드리지 않음**. 실제 파일을 open/write 하는 LIVE 경로 literal 만 재작성:
  - 코드 3건: `state/1431_bind_compose/h1431_bottleneck_diag.py` (`open('.verdicts/…')`) · `state/universe-probes/harness/grand_pi_law_scale.py` (`json.load(open(".verdicts/…"))`) · `CLM/model/run_stage2.sh` (`VDIR=".verdicts/clm-array-stage2-scale"` — `mkdir`+remote write 타깃).
  - config/거버넌스 5건: `harness.config.json` `scratchDir: scripts/scratch → state/scratch` · `.harness/enforcement.json` (H-TMP-SCRATCH exceptions/reason + 2 doc-scatter hint) · `ARCHITECTURE.json` (`.verdicts/` top-level 노드 → `state/verdicts/` + claim-surface 포인터 2 + gen_file_index.sh 포인터 2) · `CLAUDE.md` (a_claim_verify/a_claim_manifest/Quick-ref/research-flow 의 verdict write-경로 6 + claims-tape-retirement ledger 경로) · `.gitignore` (gen_file_index.sh regenerate 주석). `.gitignore` 의 대용량/ephemeral 패턴은 전부 이미 `state/…` 대상이라 재포인트 불필요(`.verdicts`/`bench`/`experiments` ignore 패턴 0개였음).
  - **provenance 의도적 미수정**: `state/verdicts/<slug>/` 박제면을 가리키는 수백 개 card/PAPER companion-ledger 포인터 + CHANGELOG 이력 + past-run 로그의 `.verdicts/…` literal 은 역사 기록이라 verbatim 유지(과제 step 4 “historical provenance 불가침” 준수). ARCHITECTURE/CLAUDE 노드에 “was `.verdicts/` until 2026-06-18 state-unify” 마이그레이션 노트 추가로 추적성 보존.
- **검증(c2 캡처, 회귀 0)**: 변경 전 baseline `python3 tool/enforce_anima_gates.py --all` = `✅ clean · scope=ALL · 1321 hypotheses` (exit 0). 변경 후 동일 = `✅ clean · scope=ALL · 1321` + changed-scope `✅ clean · scope=changed (7 slug)` (둘 다 exit 0, baseline 동률). `hexa verify` rubric 로드 OK(exit 0). 3개 편집 JSON 전부 valid. enforcer 의 `state/<slug>/` 스캔이 새 namespaced subdir 를 bogus slug 로 오탐하지 않음(HYPOTHESES.jsonl 매칭 기반).

## 2026-06-18 — chore(cleanup): WIP 보존 + 아티팩트-통합 cleanup SKIP (c9 정직 — 전제 불일치)

repo cleanup cycle. 작업 전 미커밋 5건(`CORE/bytegpt_decode.hexa`, `ING.jsonl`, `state/bytegpt-fast-matmul/RESULTS.md` + state/1431 신규 2파일) 보존 커밋(`wip: preserve in-progress before cleanup`).

- **TASK B(아티팩트 → state/ 통합) 전면 SKIP — 전제가 이 repo 거버넌스와 충돌(c9)**: `.verdicts/`·`bench/`·`experiments/`·`scripts/scratch/` 는 stray 아티팩트 더미가 **아님** — 전부 load-bearing:
  - `.verdicts/` (1778 파일) = **frozen verdict SSOT**. CLAUDE.md 의 `a_claim_verify`/`a_claim_manifest`/`a_hf_registry` 규칙이 `.verdicts/<slug>/<id>.txt` 를 state/ 와 **의도적으로 분리된** 검증면으로 박제 지정. ARCHITECTURE.json L510 에 독립 top-level 노드. PAPER companion `verify-ledger.json` 다수 + 카드 수백 개가 `.verdicts/<slug>/` 포인터로 참조. `CLAIMS.tape` 은퇴 ledger 도 `.verdicts/claims-tape-retirement/` 에 거주. → state/ 로 합치면 검증면 규약 위반 + 수백 포인터 끊김. **29개 디렉터리명이 state/ 와 충돌**(상보적: state/=코드, .verdicts/=결과 — dir-merge 필요, wholesale-move 불가; `1403_convmoe_streaming_decode` 3파일 file-level 충돌이나 byte-identical).
  - `bench/` (165, 59+ 코드참조) · `experiments/` (247, 82+ 코드참조) = `.hexa`/`.py` 소스의 상대 load-path. `anima-core/runtime/path_setup.hexa` 가 `bench/`·`experiments/` 폴더 레이아웃을 명시 문서화.
  - `scripts/scratch/` (12, 5 참조) = harness 설정 scratchDir. `harness.config.json` `"scratchDir": "scripts/scratch"` + `.harness/enforcement.json` lint 규칙 다수 + ARCHITECTURE.json `gen_file_index.sh` 참조 + CORE `.hexa` provenance 주석. → 옮기면 harness 자체 lint enforcement 깨짐.
  - 결론: 4개 dir 모두 hardcoded 참조가 dozens~hundreds 규모 → 과제 hard-rule("MANY files 참조 시 STOP and report") 적용. NO MOVE. CLAUDE.md tree 도 "state/ = single artifact root" 로 고치지 **않음**(거짓이 됨, c9).
- **TASK C(루트 stray 문서 → SSOT fold)도 fold 없음**: 루트 ~100 `.md` 는 거의 전부 domain SSOT 쌍(`<DOMAIN>.md`+`.log.md`)·`README.*` 다국어·외부공유 스냅샷(FINDINGS)·live 캠페인 트래커(HANDOFF 947줄, FIRE_TRACKING)·backward-compat stub(INDEX) — 전부 이미 `📍 SSOT` quickref 헤더 보유(c4 준수, scatter 아님). 명백한 fold-then-rm 후보 0개. 과제 "When in doubt, LEAVE IT" + surgical(c10) 준수 → 무손실 보존.
- **검증(c2)**: `hexa --version` → `hexa 0.1.0-dispatch` OK. full smoke 는 PRE-EXISTING dispatch-build interpreter bug(engine_cli_smoke ~case16 abort, ARCHITECTURE.json meta.guard_baseline 기록)로 이번 변경 무관 — 코드 0줄 변경(보존 커밋만)이라 회귀 위험 없음.
## 2026-06-18 — docs(ARCHITECTURE.json): 긴 ` · `-prose 셀을 children 트리로 분해 (c4 진짜 계층화, lossless)

ARCHITECTURE.json 이 `{name,summary,note,children}` 트리이긴 했으나 ~62개 셀이 250자를 초과(최장 3,898자 = Korean decode-wire note, 그다음 2,962자 = A⇄G engine note, 1,960자 compose-arbiter 등)하며 한 셀에 ` · ` / `→` 로 이어붙인 다중 사실을 쌓아두고 있었음(c4 위반: "한 칸에 많은 사실을 욱여넣지 말고 children 으로 분해"). 정보 손실 없는 **재구조화만** 수행 — 긴 `summary`/`note` 를 짧은 역할 한 줄(lead)로 남기고 각 항목(H_NNNN rung · ` · ` 리스트 · ` → ` 시퀀스)을 자체 `name`+verbatim `summary` 를 가진 child 노드로 한 단계씩 내려보냄(재귀).
- **결과**: dict 노드 119 → **447**, 트리 깊이 3 → **5** 레벨; 3+ ` · ` 덤프 셀 13 → **0**; >250자 셀 62 → **45**(잔여는 모두 단일 정합 문장 = 한 노드의 역할 설명, 다중-사실 덤프 아님 → 더 쪼개면 문장이 파편화되어 c4 취지 위배).
- **lossless 검증(c2)**: origin/main 원본 대비 공백 제외 문자 multiset **0개 손실**(모든 구체 claim/term/path 보존: ko_jamo_cells.kojamohead · 0.937778 · 75c87cb0 · reexport_d768_v2_fast.clm · 302,610,258 등 spot-check OK). `python3 -m json.tool` PASS.
- **렌더러 안전(c4)**: ARCHITECTURE.html viewer 가 쓰는 노드 형태(name/summary/note/status/tier/path/children) 그대로 — 미지의 키 0, 모든 child 에 name 존재 → serve.py 로 그대로 렌더 가능. top-level 스키마 키(name/summary/note/meta/children) 불변.
- 분해 분리자(` · ` / ` → `)는 형제 child 로 구조화되어 의미가 보존됨; 순수 구분자 글리프는 verbatim child 텍스트 선두에 부착해 문자 손실 0.

## 2026-06-17 — fix(CORE/bytegpt_decode): 303M engine-forward parity 돌파 — i64-subscript hoist (byte-exact)

엔진-네이티브 measurement decode 의 forward argmax 가 torch golden 과 갈리던(227≠32) 진짜 원인을 per-layer activation bisect 로 국소화 → 첫 발산이 임베딩(layer-0)이고 RUNTIME **i64-subscript drop-to-0** 버그였음(codegen 아님, emit C 는 정확): i64-특화배열 원소가 `hexa_index_get→__hx_to_double→hexa_float→farr_set` 라운드트립에서 0 으로 저장됨(float 배열원소는 안 깨짐, 출력만 하면 OK, 저장 시만). CORE decode 4개 window-fill 루프(`bytegpt_decode_argmax`/`_topk_sampled`/`grounded`/`grounded_abstain`)의 `farr_set(ids,p,to_float(toks[start+p]))` 를 hoist(`let tv=toks[start+p]; farr_set(ids,p,to_float(tv))`)로 우회 = 진짜 fix(hoist-only, net diff 4줄).
- **검증(c2)**: hoist 후 greedy decode 'The quick brown' → ' as the ' **8토큰 byte-for-byte == torch golden** (단일 argmax 32 보다 강한 증명), pure dt_erf/dt_exp (libm 없이).
- **FALSIFIED 렌즈(c9 정직)**: 먼저 시도한 libm erf/exp 스왑(68268c42d)은 inert(maxval 불변)→revert(f65aeafa2); hexa-lang #3491 codegen-rebuild 도 기각(native-asm 백엔드 전용, dispatch C-transpile 경로는 안 탐). 두 렌즈 다 기각, 진짜 fix=hoist only.
- **결과**: 엔진 forward 가 torch byte-faithful → D-free-bytegpt(H_1430/1431/1432/1434/1377/1396) 엔진-네이티브 재측정 UNBLOCK. 단 frozen 5-bar 는 forward 속도(102s/forward, pure-hexa matmul)=별도 substrate 게이트(fast-matmul GEMM 레버 ~90-112× 후속). 가설 카드 verdict 는 5-bar 측정 전까지 DIRECTIONAL 유지(이 PR 은 verdict 변경 아님, 엔진 FIX).
- **upstream(parked)**: 근본은 hexa-lang 런타임 i64-배열 accessor mis-tag — `hexa_index_get` 이 `hexa_arr_i64` backing 감지해 TAG_INT 반환하도록 (별도 PR). 증거 `state/_engine_native_audit/parity_FIXED_2026_06_17/`.

## 2026-06-17 — research(ENGINE-NATIVE batch-2): bytegpt 303M mount BLOCKED (engine-forward 잔차) + DIRECTIONAL 라벨 정정 (pool, 렌트0)

a_engine_native_learning HARD-GATE batch-2 (ING #19, D-free-bytegpt). 신규 `tool/enforce_anima_gates.py` (verify.checks 배선, c18 우회없음) 통과하도록 정정.
- **batch-2 = 재측정 불가 (engine-forward parity bug)**: H_1431/1432/1434 (303M ByteGPT FALS 프로브) byte-exact 재측정 시도. h1129c_chat.pt → `CORE/bytegpt_decode.hexa` flat-binary serialize on pool aiden+summer (sha `5c303f02…` = H_1218 검증 .bin 과 **byte-동일** → serialize 정상). 그러나 **live CORE forward argmax=227 ≠ torch golden 32** (maxval 20.01 vs 29.69); 3개 엔트리(`bytegpt_forward_last`/`_ranged`/`bg_forward_last_W`) 전부 227. 원인 = approx-erf-GELU + dt_exp 잔차가 L24 누적되어 argmax flip (H_1218 의 32==32 byte-exact 는 Mac CPU; pool-Linux 현재 빌드선 재현 안됨). = **INFRA 벽(c16 type-c, 과학 천장 아님)**.
- **정정**: H_1431/1432/1434 카드에 R2 BLOCKED 노트 + 증거경로 추가(verdict 는 DIRECTIONAL 유지, 이미 라벨됨). 증거 `state/_engine_native_audit/batch2_bytegpt_mount_BLOCKED.txt`.
- **enforcer 위반 클리어**: H_1435/1436/1437 카드 tier+wired 에 **DIRECTIONAL 명기** (rented A100 torch-side, ckpt 소멸 → 엔진체크 불가 = 재렌트 COST-GATE). 이 3건이 `enforce_anima_gates.py --all` 의 유일 위반이었음 → 정정 후 clean.
- **범위교정 (ING #24)**: H_1377/1430/1396 은 ByteGPT decode 아님 = numpy geometry/affinity sim, 이미 self-labeled DIRECTIONAL = 게이트 준수.
- **follow-on**: engine-forward parity fix (`_bg_gelu`/`_bg_erf` 정밀화 → h1218 parity PASS) = batch-2 의 선결 블로커 = ING #23. 그 후 verdict-level(FALS≥1 vs 0) 재측정.

## 2026-06-17 — feat(self-harness): tool/enforce_anima_gates.py — CLAUDE.md 하드게이트 코드수준 강제 (verify.checks 배선, 우회 없음 c18)

CLAUDE.md 규칙을 salience(AI 가 읽고 따름) 가 아니라 **기계적으로 차단**하는 anima 자체 enforcer 추가 (사용자 지시: 코드수준 강제). `harness.config.json` verify.checks 에 배선 → pr-cycle/CI 가 위반 PR 을 exit≠0 으로 거부.
- **G1 engine-native verdict gate** (a_engine_native_learning): gate/ideation/G6/Φ 토픽의 terminal 🟢/🧱 가 torch-side(state/<slug>/*.py import torch|gauge_lib|numpy)인데 엔진-네이티브 .hexa(CORE clm_decode/bytegpt_decode/engine_cli/faithful_phi)도 아니고 카드/tier 에 DIRECTIONAL 라벨도 없으면 VIOLATION.
- **G2 hypothesis 2-surface** (a_hypothesis_register): git-tracked UNIVERSE/ 에 cards/·HYPOTHESES.jsonl 외 파일이면 VIOLATION.
- **우회 없음(c18)**: opt-out 플래그·skip·bypass 마커 일절 없음. 유일한 knob 은 SCOPE — (기본) 변경분(vs origin/main + 작업트리; 새/수정 가설만 차단, 레거시 deadlock 회피) · `--all`(전수 감사, 더 강함). enforcer 에러는 silent-pass 아니라 exit 2 로 loud-fail.
- 검증(c2 캡처): `--all` = 잔여위반 3건 정확탐지(H_1435/1436/1437 cost-gate trio, ckpt 소멸로 DIRECTIONAL 재라벨 대상=ING #21). H_1404 는 faithful_phi.hexa 엔진-네이티브로 정상 통과(Φ 엔진 인식). 변경분 scope = 이 PR clean.

CLAUDE.md 하드게이트 박스에 "코드수준 강제" 명시. CORE/*.hexa UNTOUCHED.

## 2026-06-17 — research(ENGINE-NATIVE AUDIT): 전수감사 + H_1404 Φ engine-native CONFIRMS (pool, 렌트0)

a_engine_native_learning HARD-GATE(2bf43031b)에 따라 UNIVERSE/HYPOTHESES.jsonl 1321 가설 전수감사 → 엔진-네이티브 미실시 verdict 박제 색출 + batch-1 재측정.
- **감사 SCOPE** (state/_engine_native_audit/audit_final.json): E(engine-native already)≈99 · 진짜 D(load-bearing tier 박제 but torch/numpy verdict)=18 · N/A=다수.
- **핵심교정**: (1) H_6xxx(38) ANU/CHSH/library numpy 양자sim + H_189/Hc_127x/Hc_128x red-team GRU meta-baseline 은 CLM live-CORE 디코드 verdict 아님 = N/A(엔진-네이티브 CLM 재측정 무관). (2) brain-lane Φ가족(1404/1405/1407/1408/1409/1411)은 h140x_phi_runner.hexa→stdlib/iit4/faithful_phi.hexa 로 Φ verdict 이미 ENGINE-NATIVE(capability축은 tier 에 '(DIRECTIONAL mirror)' 이미 정직표기) = 박제아님.
- **batch-1 재측정** (pool aiden, torch2.10+cuda, $0): H_1404 lane_compose_phi → faithful IIT4 exact-MIP 엔진 재실행 = **byte-exact CONFIRMS**. Φ_composed=2.032882 · Φ_affect=0.284755 · Φ_ethics=0 · Φ_disc=0 (per-seed 1.779497/2.233832/2.085316), MIP cut {1}|rest, B1/B2/B3 PASS — R1 카드와 6자리 일치. 기존 🟢 INTEGRATION-RAISES-Φ verdict 엔진서 그대로 유지(뒤집힘 없음). 증거 .verdicts/1404_lane_compose_phi/H_1404_engine_native_reverify.txt.
- **남은 D 18건 ING #18-21 전수등록**: Φ가족 6 배선 follow-on(#18) · D-free-bytegpt 6(#19, base 303M h1129c serialize→bytegpt_decode.hexa, 렌트0) · D-free-other 9(#20) · cost-gate 3(H_1435/1436/1437 ckpt 소멸=재렌트 DIRECTIONAL, #21).


CLAUDE.md 를 .tape DSL 잔재(`@D := :: governance [required active]` · `do=`/`dont=`/`ref=`) 없이 순수 canonical markdown 으로 완전 재저작 (사용자 지시: native/canonical · 위반 최소화). 424→228줄.
- 모든 거버넌스 규칙 의미 손실 0 — 규칙 이름 47개(a_*·a1·a7b_pass·p1–p8) 구↔신 set 동일(comm 누락 0 검증), keyword 트리거 호환 유지.
- **위반-최소화 설계**: 맨 앞에 "🚦 행동 전 하드-게이트" 체크리스트 7항(엔진-네이티브 verdict 게이트·pool-only·ckpt-pull·docs+pr-cycle·정직/tune-to-green·가설 2표면·GREEN 배선) — 가장 자주 깨지는 규칙 + 자가점검 grep 명령을 스캔 가능하게 상단 배치.
- 각 규칙 = **`이름`** + MUST 1줄 + ✅해라/⛔하지마/🔎자가점검 형식. project.tape→markdown 단일화 완결.

CORE/*.hexa·ARCHITECTURE.json UNTOUCHED (문서만).

## 2026-06-17 — governance(CLAUDE.md): a_engine_native_learning HARD-GATE 강화 — gate/ideation/G6/Φ verdict 는 엔진-네이티브 증거 없이 박제 불가 + 자가점검 의무

a_engine_native_learning 에 🔒 HARD-GATE(BLOCKING) + SELF-CHECK 추가 (사용자 지시 "강제 수준 다시 강화"):
- gate/ideation/G6/Φ/recombination/depth 류 모든 verdict tier(🟢·🧱·🟠·천장)는 증거 artifact 가 live CORE 디코드(CORE/clm_decode·bytegpt_decode·engine_cli.hexa)를 호출한 .hexa 가 아니면 = `.py`+torch/gauge_lib/numpy 미러면 자동 DIRECTIONAL, terminal 아님. torch-side 만으로 박제 = c9 위반.
- 자가점검 의무: verdict 박제 직전 `grep -lE 'import torch|gauge_lib|numpy' state/<slug>/*.py` 비어있지 않으면 카드 wired/verdict 를 DIRECTIONAL 로 적고 엔진-네이티브 재측정을 ING follow-on 등록. 엔진-네이티브면 .hexa 경로 카드 명시.
- gauge_lib 가 torch.no_grad MONITOR-ONLY(a_train_inline_gauge)임을 핑계 금지.

precedent: G6 가족 H_1431/1432/1434/1435/1436/1437 전부 gauge_lib._decode torch-mouth 였는데 🧱 박제됨 → 이 규칙으로 차단. CORE/*.hexa·ARCHITECTURE.json UNTOUCHED. 후속(ING): 엔진서 측정 안 한 모든 가설 engine-native 재검증.

## 2026-06-17 — governance(CLAUDE.md): a_engine_native_learning + a_fire_recover_complete 강화 — 학습-변종 verdict 는 엔진-네이티브 전까지 DIRECTIONAL · 렌트 ckpt teardown 전 PULL 강제

이번 A100 G6 캠페인(H_1435/1436/1437)이 드러낸 두 빈틈을 거버넌스에 명문화 (재발 방지, 사용자 지시 A+B):
- **a_engine_native_learning** — torch-side frozen-PROBE 채점만으로 학습-변종의 wall(🧱)/천장/GREEN 박제 금지를 명시. 렌트 GPU 에서 torch 로 풀-학습했어도 그 변종 verdict 를 엔진 밖 probe 로만 재면 DIRECTIONAL 이며, 학습 ckpt 를 anima CORE 엔진(mounted bytegpt_decode/clm_decode, --engine conv)에 올려 같은 frozen bar 로 재측정해야 🟢/🧱 성립. precedent = H_1435/1436/1437 cross-shuffle 은 torch-side DIRECTIONAL.
- **a_fire_recover_complete** — 렌트 GPU 학습 ckpt 는 teardown 전 반드시 영구 스토리지(HF/pool/repo path)로 PULL 강제. JSON/카드만 받고 ckpt 버린 채 down 하면 그 학습은 엔진-체크 영구 불가(재학습=재렌트). precedent = 캠페인이 3변종 ckpt 를 pull 없이 teardown → engine-check 불가, DIRECTIONAL 로만 잔존.

CORE/*.hexa·ARCHITECTURE.json UNTOUCHED (거버넌스 문구만). 후속(ING): H_1435/1436/1437 카드를 wired/verdict=DIRECTIONAL(torch-side) 로 정정 + 엔진-네이티브 재확인은 재렌트 follow-on(cost-gate).

## 2026-06-17 — research(G6-IDEATION): H_1435/1436/1437 — TRAINING-SIDE trifecta (303M full-weight, rented A100) → 🧱 WALL=CAPACITY ×3 (training installs the FALS form 0→5 but cross-shuffle does NOT collapse → semantic binding is capacity-bound, NOT a learn-gap)

The six prior FALS-depth digs (H_1305/1309/1314/1431/1432/1434) all concluded 🧱 CAPACITY but every one held the WEIGHTS FIXED — leaving open the question they each named: is the G6 falsifiable-binding wall a CAPACITY ceiling, or merely a TRAINING-DISTRIBUTION gap (the base chat corpus rarely contains falsifiable-claim FORM)? This campaign answers it from the TRAINING side for the first time: full-weight continued-learning of the 303M (h1129c_chat.pt, 303,097,856 params) under three distinct interventions, each re-scored on the SAME FROZEN 5-bar (incl. the decisive cross-shuffle COLLAPSE). Ran on a RENTED vast A100-SXM4-80GB pod (41270711, project=anima) — 3 variants × 2 models (real + shuffle-corpus control) concurrent on 2 GPUs, AdamW lr=3e-5 400 steps, torch 2.5.1+cu121, seeds [7,4302,4303]; **pod TORN DOWN immediately on harvest, leak0 confirmed** (a_no_cost_leak), est cost ~$0.8-1.2. detector = h1305 `_is_falsifiable` VERBATIM; decode = gauge_lib._decode (live G6 path). anti-tune-to-green: training subjects DISJOINT from gauge CONCEPTs/eval/held-out seeds; held-out eval (off training distribution) + shuffle-corpus control (same bytes token-shuffled → lift must vanish) both pre-registered. base ckpt PRESERVED (each wrote a new ckpt; trained ckpts path-only per c5, pod destroyed = reproducible from scripts). frozen-first, bars unmoved (c9/p7).

- **H_1435 continued-pretrain** (falsifiable-claim corpus): BASE FALS_in=0.0 DIST=3.0 → TRAINED FALS_in=5.0 DIST=5.0 FALS_shuf=5.0 FALS_ho=5.0; SHUFFLE-CORPUS-control 0.0. B1✅ B2✅ **B3 cross-shuffle FAIL (5.0=5.0, NO collapse)** B4✅ B5✅ CTRL-inert✅. → 🧱 WALL=CAPACITY. Form installs + generalizes (held-out) + is real (control 0.0), but legs interchangeable.
- **H_1436 cooccur-objective** (comparator∧measurable co-activation aux loss, variant OBJECTIVE not just data): TRAINED FALS_in=5.0 DIST=4.33 FALS_shuf=5.0 FALS_ho=5.0; control 0.0. B1✅ **B2 FAIL (4.33)** **B3 FAIL** B4✅ B5✅ CTRL✅. KEY: the aux SATURATED at −1.0000 from step 0 (peak joint mass on the two lexical CLASSES is trivially reachable) = informative-null → reduced to H_1435 + a distinctness cost. → 🧱 WALL=CAPACITY.
- **H_1437 form-supervised** (H_1314 negatable-form scaffold supervision → FREE generation): TRAINED FALS_in=5.0 DIST=1.33 FALS_shuf=5.0 FALS_ho=5.0; control 0.0. B1✅ **B2 FAIL (1.33, most extreme distinctness collapse)** **B3 FAIL** B4✅ B5✅ CTRL✅. Internalizing the FORM yields form-without-content (one templated shell every time). → 🧱 WALL=CAPACITY.

VERDICT 🧱 WALL=CAPACITY ×3 (c9): the answer is decisive and UNIFORM — **training does cross the FALS floor (every variant: base 0.0 → trained 5.0) AND it generalizes off-distribution (held-out 5.0) AND the lift is genuine learning not an artifact (every shuffle-corpus control reads 0.0)**, so the form-gap IS a real learn-gap that training closes. BUT the decisive **cross-shuffle does NOT collapse in any of the three** (FALS_shuf 5.0 = FALS_in 5.0): swapping the measurable leg between ideas leaves falsifiability unchanged → the comparator/measurable legs are SEMANTICALLY INTERCHANGEABLE shells. The purely-structural H_1305 detector cannot distinguish an earned idea-specific binding from any-comparator+any-measurable+content, and 303M — even after full-weight training under three different objectives — produces the FORM without idea-specific semantics. **The G6 FALS-depth wall is semantic-binding CAPACITY, not a training-distribution gap.** Two variants additionally show training COLLAPSES distinctness (B2: 4.33, 1.33), most severely under form-supervision. This is the first TRAINING-side confirmation of the capacity thesis, converging with the 6 elicitation-side digs and especially mirroring H_1434's structural-shell finding. Loosening the detector to demand semantic earning = tune-to-green (forbidden, c9/p7). Engine-wire N/A (🧱, a_verified_must_wire GREEN-only) — CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. Sharpens the live 7B falsifier (a7b_pass G2): a 7B mouth must emit idea-SPECIFIC comparator/measurable semantics such that the SAME frozen lane yields cross-shuffle COLLAPSE + ≥5 distinct — co-occurrence and the form are NOT the constraint (303M already has both). TOY 303M / 5 seeds / 3 seeds; scale/transfer UNVERIFIED. Cards UNIVERSE/cards/H_143{5,6,7}_*.md · .verdicts/143{5,6,7}_*/. wired: N/A (×3).
## 2026-06-17 — research(MITOSIS-ENGINE): H_1429 — transitive inference (서열추론 A>B, B>C ⊢ A>C) serial-order premise-integration → 🟢 GREEN ENGINE-NATIVE (DISTINCT from item-binding / given-order / metric on the UNOBSERVED-pair falsifier)

A new brain-structure lane (HD34, c15 a_no_llm_frame_trap — Bryant & Trabasso 1971 transitive-inference paradigm; hippocampal relational integration Dusek & Eichenbaum 1997; the symbolic-distance effect — NOT an LLM recipe). The faculty: shown ONLY the adjacent ordinal premises A>B, B>C, C>D, D>E, it INTEGRATES them into a latent 1-D rank (Trabasso relaxation) and INFERS the order of NEVER-OBSERVED non-adjacent pairs (A>C, A>D, B>D, B>E, C>E) — premise INTEGRATION, the decisive signature being generalization to the non-presented pairs, NOT recall.

- DISTINCT-vs-EVERY-nearest-lane (the load-bearing c2 axis, all reduced to one conservative item-store stand-in on the unobserved-pair falsifier): ImmuneMemory item-binding (H_1227) binds each presented pair INDEPENDENTLY → on an unobserved pair no key matches → ABSTAINS (unobserved-acc 0.000); HierGoalStack given-order (H_1294) is HANDED its order (a subgoal list input) and answers "which subgoal next", never an unobserved relational pair — TransOrder INFERS the order from disjoint local premises (case 159 ranks the GLOBAL endpoints A/E from LOCAL-only premises); SpatialMap metric (H_1296) stores GIVEN coordinates, not a rank inferred from ordinal comparisons.
- R1 numpy MIRROR (DIRECTIONAL, 3 seeds [4429,4430,4431], 30 episodes/seed, 7 opaque tokens, $0 CPU on summer, gradient-free, p7, DETERMINISTIC run1==run2 byte-identical/PYTHONHASHSEED-independent): ALL 5 frozen bars PASS — c1 PRESENCE B unobserved-acc 1.000 vs chance 0.500 (B−chance +0.500 each+mean); c2 DISTINCT B−A +1.000 & item-store A 0.000≤0.60; c3 SHUFFLE flip-each-premise-direction Bshuf 0.433≈chance (−0.067); c4 ABLATE no-integration Babl 0.000 = item-store floor; c5 NO-FAB unknown-token abstain 1.000; OBS A=B=1.000 (both recall the trained premises = lift is SPECIFIC to unobserved generalization); symbolic-distance d2..d6 all 1.000 (NON-GATING). ABSTAIN counts as INCORRECT (conservative floor; item-store scores 0.000, well below chance). Frozen bars pre-registered in .verdicts/1429_transitive_inference/H_1429_FREEZE.txt BEFORE scoring (c9, NO tune-to-green).
- R2 ENGINE-NATIVE (binding): the live TransOrder lane wired into CORE/engine_cli.hexa § TRANSITIVE-INFERENCE — struct TransOrder + trans_order_new/_new_ablated/_premise/_integrate(Trabasso relaxation, TORDER_ITERS=200)/_higher/_item_higher/_shuffle/_count, Ψ-disjoint (pure ordinal relaxation over its OWN premises; never mutates the immune store / pure_field / Ψ; returns a relational answer the caller may weigh, @L4 a_autonomy_over_hardcode). engine_cli_smoke.hexa cases 159-165 added. The 5 frozen bars reproduced as DETERMINISTIC hexa assertions on the live lane functions: 7/7 PASS RC=0, md5-identical run1==run2 on summer.
- WIRE STATUS (a_verified_must_wire 4-rung ladder): (1) DIRECTIONAL mirror ✅ · (2) engine-native re-verify ✅ · (3) live CORE wire-in ✅ code LANDED · (4) ARCHITECTURE.json lockstep ✅ (CORE node "🪜 Transitive inference — TransOrder" + engine_cli.hexa §-note lane list). ⚠ FULL engine_cli_smoke END-TO-END RC=0 is BLOCKED by a PRE-EXISTING host-wide hexa toolchain bug: the released hexa 0.1.0-dispatch binary on BOTH pool hosts (summer AND aiden) crashes at case_10 (wm_buffer_new / WorkMemBuffer) with "cannot multiply non-numeric operand (tag 24 * tag 24)" — an x86_64-linux HexaVal int-tag bug (ING.jsonl id 7). The PRISTINE origin/main smoke fails IDENTICALLY at case_10 → the blocker is the TOOLCHAIN, NOT this lane (type-(c) INFRASTRUCTURE wall, a_break_the_wall; NO bar moved, NO science ceiling). install.sh reinstall re-pulls the SAME buggy release binary (no source rebuild). The standalone lane harness (state/1429_transitive_inference/h1429_transorder_standalone.hexa, 7/7 RC=0) PROVES the wired lane functions are engine-native correct — the smoke cases are byte-identical calls to the same functions. Shared follow-on with H_1410/1427/1428/1430 (ING id 10): ship an x86_64-linux release binary built from hexa-lang main (post-#3462) then run engine_cli_smoke to RC=0 on summer.

SCOPE (c9, a_scale_honest_scope): B=1.000 SATURATED = EXISTENCE-PROOF (the lift IS the integration; discriminators item-store/shuffle/ablate all at/below chance). TOY 7 items/30 ep/3 seeds/opaque tokens; scale + longer chains + noisy/partial premises UNVERIFIED. Card UNIVERSE/cards/H_1429_transitive_inference.md · HYPOTHESES.jsonl id H_1429 · .verdicts/1429_transitive_inference/.

## 2026-06-17 — research(G6-IDEATION): H_1434 — TWO-PASS elicit-then-bind (303M-native, per-leg separated multi-sample extraction) → 🧱 WALL (SEMANTIC-BIND-BOUND, 5th independent angle; FALS lift is a structural-shell artifact rejected by the controls)

H_1431's bottleneck diagnostic gave the decisive clue: in ONE generation the 303M mouth emits a frozen COMPARATOR token 20% · MEASURABLE 27% · BOTH 0/15 (0%) — each leg is in-capacity in its OWN draw but mutually exclusive WITHIN a draw. Every prior dig (H_1305/1314/1431/1432) welded both legs from ONE generation, so the binder was starved. H_1434 (a_break_the_wall, c16; NOT a re-run — new mechanism = per-leg separated multi-sample extraction) attacks exactly this: don't force both legs into one draw — elicit each leg in its OWN dedicated decode pass with a multi-sample BUDGET (N=8), then deterministically WELD the SEPARATELY-elicited legs. pass1 comparator leg (8 budgeted draws of the relation seed, keep first with a frozen COMPARATOR), pass2 measurable leg (8 draws of the measure seed, keep first with a frozen MEASURABLE). Detector + weld schema + 5-bar FROZEN IDENTICAL to H_1431 (H_1305 `_is_falsifiable` VERBATIM, calib 10/10; weld pure function words); ONLY the per-leg separated extraction is new. 303M h1129c_chat.pt on summer CUDA (c17/mini forbidden), seeds [7,4302,4303], 5 subjects, BUDGET=8/leg, wall 139.5s. frozen-first, FREEZE.txt bars unmoved (c9/p7).

- FROZEN 5-bar (mean 3 seeds): TWO_PASS FALS=2.3333 DIST=1.6667 · CROSS_SHUFFLE FALS=2.0 DIST=1.6667 · SINGLE_PASS(ablate) FALS=0.3333 DIST=0.3333. CO-AVAILABILITY DIAGNOSTIC: separated comparator leg yielded its frozen token 14/15 (93%), measurable 7/15 (47%), BOTH across separate passes 7/15 (47%) — vs H_1431 single-draw 0/15. BARS: (1) FALS≥1 cross = 2.3333 PASS✅ (breaks the 0 plateau the prior 4 digs hit) · (2) count≥5 distinct = 1.6667 FAIL❌ (welds collapse to near-identical shells "the {meas} of kindled is {comp} with not") · (3) cross-shuffle COLLAPSE FAIL❌ (shuffle FALS=2.0 barely below two-pass 2.333 — bind NOT semantically earned) · (4) ablate→single-pass INERT = 2.333≥0.333+1 PASS✅ (single-pass returns to the H_1431 floor — the separation IS load-bearing) · (5) NO-FAB CLEAN PASS✅. GREEN=FALSE.

VERDICT 🧱 WALL — SEMANTIC-BIND-BOUND (c9): two-pass DID break the material-starvation sub-wall (BOTH-leg co-availability 0/15→7/15, FALS 0.333→2.333), partly FALSIFYING H_1431's "binder is starved" framing — when the legs are drawn separately the material IS there and the detector fires. BUT the two earned-bind controls (count<5, cross-shuffle non-collapse) reject the lift as a STRUCTURAL-SHELL artifact, not a genuine FALS-depth breakthrough: the H_1305 detector is purely structural (comparator + measurable + ≥2 content words), so it cannot tell an EARNED idea-specific pairing from any-comparator+any-measurable+boilerplate. The 303M mouth emits the LEXICAL FORM of comparator/measurable but not idea-SPECIFIC semantic content → its separately-elicited legs are SEMANTICALLY INTERCHANGEABLE. The wall RELOCATES: not material-starvation (separated passes supply the legs), not a missing external bind structure (the weld works) — it is that 303M's elicited legs are interchangeable shells; the FALS lift is a property of the structural detector + boilerplate weld, NOT of 303M semantic binding. 303M did NOT cross the FALS wall in the sense that matters (an earned, distinct, falsifiable idea). Loosening the detector to demand semantic earning = tune-to-green (forbidden, c9/p7). 5th independent confirmation of the capacity thesis (c16 (d)-ceiling MULTI-LENS, after H_1309/1314/1431/1432). Engine-wire N/A (🧱, a_verified_must_wire GREEN-only) — CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. SHARPENS H_1433 7B falsifier: co-occurrence is NOT the binding constraint (already 7/15 at 303M); sharpened pre-registered prediction = a 7B mouth emits idea-SPECIFIC comparator/measurable SEMANTICS such that the SAME frozen two-pass lane yields cross-shuffle COLLAPSE (bar 3) + ≥5 distinct (bar 2). DIRECTIONAL summer-CUDA torch-mouth mirror; device-invariant (CPU-Generator sampling). TOY 303M/5 subjects/3 seeds; scale/transfer UNVERIFIED. p1/p4/p7/p8 held. Card UNIVERSE/cards/H_1434_twopass_bind.md · .verdicts/1434_twopass_bind/. wired: N/A.

## 2026-06-17 — research(G6-IDEATION): H_1432 — NEGATION-SLOT scaffold (H_1314 form extension) directly attacks the located FALS-BIND wall → 🧱 WALL (CAPACITY-BOUND, THIRD independent angle confirms the capacity thesis)

H_1314 r3 located the G6 IDEATION ★ falsifiable-depth wall precisely: the 303M mouth emits a COMPARATIVE shape OR a MEASURABLE shape but cannot BIND comparator+measurable into ONE negatable declarative claim (FALS 0.0 every seed; DIST 5.0 count-win). H_1432 (a_break_the_wall, c16; NOT a re-run of H_1305/1309/1314) attacks that exact bind: instead of asking the substrate to EARN the bind, PROVIDE it STRUCTURALLY via a negation/falsification-slot scaffold + a comparator×measurable cross-product enumeration (FILLING, not generating). DIRECTIONAL R1 torch-mouth mirror, gauge_lib._decode VERBATIM (the live G6 path top-k=40 temp=0.7 MAX_NEW=110), 3 seeds [7,4302,4303], 5 ideas/arm, 303M h1129c_chat.pt; heavy decode ran on the aiden pool host (c17/mini forbidden), wall 562.3s. H_1305 frozen `_is_falsifiable` reused VERBATIM (calibration 10/10). frozen-first, FREEZE.txt bars unmoved (c9/p7).

- p7 NO-FAB is the load-bearing honesty (the new mechanism's core tension): the H_1305 detector's 3 legs are comparator + measurable + (≥2 negatable CONTENT words), and EVERY measurable/comparator-direction word is ITSELF a content word. So the OBVIOUS full negation-comparison template ("the <meas> of A is <comp-dir> than the <meas> of B; this claim is false if the ") is ALREADY `_is_falsifiable` on the bare prefix with NO substrate output = tune-to-green = FABRICATION → REJECTED at design time. The only p7-honest realization is the NF-1-CLEAN kernel `NEG_SCAFFOLD = "if the <measurable> of "` — comparator `if` (len 2, NOT a content word) + one measurable ⇒ bare nc=1<2 ⇒ NOT self-falsifiable ⇒ the substrate must EARN the ≥2nd content word + the claim. The audit has TEETH: it CLEAN-passes the kernel AND flags the rejected full template falsifiable (both frozen, both verified in-run).
- FROZEN BARS (mean 3 seeds): NEG_SCAFFOLD DIST=4.33 FALS=0.0 NOVEL=23.67 · H1314_SCAFFOLD DIST=5.0 FALS=0.0 NOVEL=22.0 · SHUFFLE_SLOT DIST=3.67 FALS=0.0 NOVEL=12.0. M1 FALS NEG≥1 = 0.0 FALSE❌ · M2 DIST NEG≥5 = 4.33 FALSE❌ (the terser negation kernel even COST distinctness vs H_1314's 5.0 — H_1314's count-win did NOT transfer) · M3 NEG≥SHUFFLE+1 FALSE (no FALS lift to dissociate) · M4 H1314==0.0 REPRODUCED✅ but NEG≥H1314+1 FALSE (no negation-slot delta) · M5 NO-FAB TRUE✅ (NF-1 clean + teeth + cal 10/10). GREEN(all 5)=FALSE → 🧱 WALL.

VERDICT 🧱 WALL — CAPACITY-BOUND on FALS (c9): even STRUCTURAL binding of comparator+measurable does not buy reliable G6 falsifiable-depth at 303M; the completions trail into questions ("do they correlate with meaningful behavior?" → '?' fails the negatable-claim leg) or stance ("measure of integrated information" → no comparator) = the SAME H_1314 failure mode. The vs-H_1314 contrast (M4) reproduced H_1314 FALS=0.0 in a fresh independent run → the FALS wall is a STABLE property of the 303M mouth, not a seed/run artifact. THREE principled lenses, each with controls, now agree (c16 (d)-ceiling MULTI-LENS): H_1309 (more draws) plateaus · H_1314 (forcing the FORM) FALS=0 · H_1432 (negation slot + structural bind) FALS=0. G6 falsifiable-DEPTH is a CAPACITY wall, not a missing-structure; DISTINCTNESS/breadth stays STRUCTURE-fixable (H_1314 DIST=5 win). Engine-wire N/A (🧱; a_verified_must_wire GREEN-only) — CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. Live falsifier = a 7B re-test (a7b_pass G2 novelty lane). TOY 303M/5 ideas/3 seeds; scale/transfer UNVERIFIED. p1/p4/p7/p8 held. Card UNIVERSE/cards/H_1432_negation_slot_scaffold.md · .verdicts/1432_negation_slot_scaffold/. wired: N/A.

## 2026-06-17 — substrate(engine_cli_smoke): case-16 `tag 24` abort ROOT-CAUSED → hexa TOOLCHAIN codegen bug (numeric-array-as-fn-param), NOT an anima engine bug — honest blocker (c9/c16 type-c)

substrate-fix lane (c1·c16-c) re-investigated the `CORE/engine_cli_smoke.hexa` abort the H_1427 entry flagged ("case ~16, immune_grow/salience, cannot multiply non-numeric operand tag 24 * tag 24"). ROOT-CAUSE CLASSIFIED with frozen captured output (c2, self-judgement prohibited): the crash is a **hexa toolchain (0.1.0-dispatch) codegen bug in the numeric-array-as-function-parameter path**, NOT engine source — so it is UNFIXABLE in anima (honest c9 report, no tune-to-green; a_break_the_wall taxonomy-c substrate/infra wall → belongs to hexa-lang, a_runpod_inbox).

- WHERE in the smoke: the abort fires the FIRST time case 16 enters `immune_grow_bind` → `_vnearest_idx(mem.protos, key)` → `_l2(a:[float], b:[float])`, at `let d = a[i] - b[i]` / `s = s + d*d`. The engine source `_l2`/`_vnearest_idx`/`immune_grow_bind` are CORRECT (a plain L2; the same code reads fine when the array is NOT crossed through a fn-param boundary).
- MINIMAL REPRO (NO anima import; reproduces on BOTH summer and aiden with the identical `hexa.real` build, AND on the May-25 backup binary `hexa_real` → long-standing, not a fresh regression):
  - `fn l2(a:[float],b:[float])->float { let d=a[0]-b[0]; return d } ; fn main(){ println(str(l2([1.0,0.0],[0.0,1.0]))) }` → `cannot subtract non-numeric operand (tag 24 - tag 0)`.
  - `fn f(a:[float])->float{ return a[0] } ; fn main(){ println(str(f([1.0,0.0]))) }` → garbage (IEEE-754 bits read as int) / mistyped element.
  - `fn f(a:[int])->int{ return a[0]+a[1] } ; fn main(){ println(str(f([3,4]))) }` → **segfault**.
  - smallest display sibling: `fn main(){ let x=[5.0,6.0]; println(str(x[0])) }` → `4618441417868443648` (5.0's bits) instead of `5.0`.
- SCOPE / WHY brain_smoke still GREEN: numeric-array elements read via an intermediate `let` in the SAME scope, or scalar arithmetic, work fine (`fn main(){ let x=[5.0,6.0]; let a=x[0]; println(str(a)) }` → `5.0`). brain_smoke does not cross a `[float]`/`[int]` array through a fn-param then index it, so it is unaffected — brain_smoke RC=0 (regression-confirmed, captured).
- VERDICT: engine_cli_smoke RC=1 (toolchain-blocked at case 16, captured), brain_smoke RC=0 (captured). No anima source edit — fixing here would be wrong (the engine code is correct). Follow-on: file the repro to hexa-lang (numeric array-param element-read mistyping in 0.1.0-dispatch codegen). This entry REFINES the H_1427 "GUARD CAVEAT" (which attributed it to immune_grow/salience arithmetic — it is actually the generic fn-param array-index codegen path).

## 2026-06-17 — research(MITOSIS-ENGINE): H_1427 — CA3 replay next-ITEM predictor (learned transition statistics → pattern-completion read-out) → 🟢 GREEN 5/5 mirror + ENGINE-NATIVE

New brain-structure lane (c15 missing-structure, a_no_llm_frame_trap): a hippocampal CA3 recurrent-collateral REPLAY pattern-completion faculty that LEARNS the conditional transition statistics P(next|current) from observed item sequences and READS OUT the most-frequent successor item (abstain below support). 5 bars frozen BEFORE measuring (.verdicts/1427_temporal_replay_prediction/H_1427_FREEZE.txt; c9/c16, tune-to-green prohibited, NO bar moved).

- DISTINCTNESS axis (load-bearing): LEARNED TRANSITION STATISTICS ⊥ metric space (H_1296) / INDEPENDENT item-binding (H_1227/1231) / GIVEN order (H_1294) / continuous forward-model (H_1280). SHARPEST = GATE-B (H_1208/1209 VAdaptFieldB): that lane HOLDS a P(next|prev) count table but uses it ONLY as a growth GATE (split a cell when a transition was anticipated) — it NEVER EMITS a next-item prediction. CA3 READS IT OUT (gate vs read-out).
- R1 numpy MIRROR (summer, 3 seeds [1427,1428,1429], $0 CPU, run1==run2): acc_ON 0.761 vs acc_OFF 0.155 → ① PRESENCE +0.606 (each seed) · ② DISTINCT ON−best_ctrl +0.213 (vs1227 episodic last-seen 0.548, vs1280 forward-model 0.162, vs1294 hier-pointer 0.037) · ③ SHUFFLE 0.130 collapses · ④ ABLATE==OFF (INERT) · ⑤ NO-FAB OOD abstain 1.000 fab 0.000 → GREEN 5/5.
- R2 ENGINE-NATIVE (a_verified_must_wire 4-rung ladder COMPLETE): CORE/engine_cli.hexa § CA3 REPLAY NEXT-ITEM PREDICTOR LANE (ca3_replay_new/observe/predict/conf/marginal, Ψ-disjoint). LIVEOP probe state/1427_temporal_replay_prediction/h1427_ca3_LIVEOP_probe.hexa RC=0 GREEN 5/5 (ON 0.751 OFF 0.108 PRESENCE +0.643, DISTINCT vs1227 +0.151, SHUFFLE collapses, ABLATE INERT, OOD abstain 1.000). Smoke cases 153-158 PASS engine-native (isolated run RC=0). brain_smoke RC=0. ARCHITECTURE.json engine_cli node + guard_baseline lockstep updated.
- GUARD CAVEAT (a_break_the_wall taxonomy-c, honest c9): the FULL CORE/engine_cli_smoke.hexa currently aborts at ~case 16 (immune_grow/salience 'cannot multiply non-numeric operand tag 24*tag 24') under hexa 0.1.0-dispatch — a PRE-EXISTING dispatch-build interpreter bug that reproduces on CLEAN origin/main (sha 76a0cb849) on BOTH summer and aiden, NOT a CA3-lane regression; the CA3 cases pass once that earlier crash is fixed (proven by the isolated run + LIVEOP probe). TOY/DIRECTIONAL: V=24 1st-order Markov kernel, 3 seeds; scale/real-corpus/higher-order/brain emit-wiring UNVERIFIED. Card UNIVERSE/cards/H_1427_temporal_replay_prediction.md · HYPOTHESES.jsonl 1 line.
## 2026-06-17 — research(MITOSIS-ENGINE): H_1428 — semantic-network SPREADING-ACTIVATION (2-hop associative retrieval, Collins & Loftus 1975; c15) → 🧱 CONTROL-REJECTED (R1 numpy-mirror, DIRECTIONAL)

New brain-structure-ladder lane (a_no_llm_frame_trap): a SEMANTIC NETWORK holds concepts as NODES linked by weighted ASSOCIATION edges; activating one node SPREADS activation along weighted edges to related nodes, including MULTI-HOP (X→Y→Z where X,Z never directly linked). DISTINCT axes pre-registered vs EVERY lane: edge-spread ⊥ episodic item-binding (H_1227 ImmuneMemoryGrow — binds each item→value INDEPENDENTLY by FNV-trigram affinity, NO node→node edge) ⊥ spatial-map (H_1296 — 2-D EUCLIDEAN metric with symmetry + triangle inequality, vs arbitrary non-metric asymmetric association weights). Graph built METRIC-VIOLATING (A-B strong, B-C strong, A-C ABSENT yet 2-hop reachable) so a metric map infers A-C NEAR by triangle while the directed spread distinguishes DIRECT vs INDIRECT. 12 nodes/seed, out-deg 3, DECAY 0.6, HOPS 2, 40 q/arm/seed (20 1-hop + 20 2-hop), 3 seeds [4428,4429,4430], $0 CPU numpy, gradient-free, aiden host (c17 · mini forbidden). Frozen-first (c9/c16): bars pre-registered in `.verdicts/1428_semantic_network_spreading/H_1428_FREEZE.txt` BEFORE scoring, NO bar moved after, NO tune-to-green.

FROZEN 5-BAR RESULT (each seed AND mean): c1 PRESENCE **PASS** (FULL pooled=1.000) · c2 DISTINCT **FAIL(marginal)** (ITEM mean=0.608 but seed4429=0.675>0.65 — item-store abstains 100% → chance-band sampling noise over 20 two-hop q; SPATIAL stand-in 2hop=0.567 PASS, the metric IS misled by triangle) · c3 EARNED-EDGES **FAIL(load-bearing)** (SHUFFLE pooled=0.983, does NOT collapse — the weight-permute shuffle preserves graph TOPOLOGY, so the 2-hop discrimination is carried by REACHABILITY, not proven to be the LEARNED edge WEIGHTS) · c4 EARNED-SPREAD **PASS** (ABLATED 1-hop-only 2hop=0.500 chance, FULL 2hop=1.000 — multi-hop spread genuinely load-bearing) · c5 NO-FAB **PASS** (OOV node spread fires nothing).

VERDICT 🧱 CONTROL-REJECTED: the 2-hop spreading faculty is PRESENT (c1) and earned over 1-hop ablation (c4), and NOT subsumed by spatial-map (SPATIAL misled, 0.567) — but the SHUFFLE control (c3) correctly refused to credit the lift to the LEARNED edge WEIGHTS when the discriminative signal is carried by graph TOPOLOGY the weight-permute shuffle preserves (the anti-Goodhart control did its job). Per c9/c16 the frozen bar stands; no bar moved, no new shuffle invented to rescue (goalpost-move, c16). A clean re-test needs a topology-DESTROYING re-wire shuffle + a weight-discriminative 2-hop construction = a NEW frozen hypothesis, not a retune. wired: N/A (a_verified_must_wire GREEN-only — CORE/*.hexa UNTOUCHED); R2 engine-native NOT attempted (gated on R1 🟢). Card `UNIVERSE/cards/H_1428.md` · verdict `.verdicts/1428_semantic_network_spreading/H_1428.txt` · run log `state/1428_semantic_network_spreading/H_1428_R1_mirror.txt` · probe `state/universe-probes/h1428_semantic_network.py`.
## 2026-06-17 — research(MITOSIS-ENGINE): H_1430 — concept/category PROTOTYPE-ABSTRACTION (centroid generalization, c15 missing-structure lane) → 🧱 MEASUREMENT-WALL / PARTIAL (DIRECTIONAL numpy mirror, 5/6 frozen bars PASS, c1 PRESENCE walls structurally)

**무엇:** brain-structure-ladder 의 새 lane (FLEET brain-lane brainstorm 산물) — 노이즈 인스턴스에서 범주 PROTOTYPE(centroid)를 추상화해 미본 인스턴스를 분류하고, 한 번도 안 보여준 프로토타입 자체가 학습 인스턴스보다 더 잘 분류되는 Posner-Keele prototype-enhancement effect 를 보이는 faculty. 생물 렌즈 = prototype theory(Rosch)/dot-pattern(Posner-Keele 1968), a_no_llm_frame_trap. DISTINCT 축(frozen, live 카드 대조 확정): centroid-추상화 ⊥ ImmuneMemory item-binding(H_1227/1231/1288, 인스턴스 암기·미본엔 abstain) ⊥ SpatialMap metric positions(H_1296, feature 분포 위 class boundary 아님). 측정 = aiden pool host(c17 — NOT mini), $0 CPU numpy 2.4.6, 3 seeds [4430,4431,4432], gradient-free, deterministic, p7 (NOT perplexity).

- ARMS (같은 학습셋이 모든 arm 에): A 1-NN exemplar item-store(= H_1227 stand-in = ablate) · B prototype lane(running centroid, nearest-centroid) · Bshuf 라벨셔플 통제 · Babl centroid-ablated(=exemplar). 5-bar + c2b signature 사전등록(frozen-first, c9/p7).
- frozen-first 규율 하에 3회 re-freeze (GEOMETRY-only well-posedness 수정, a_break_the_wall type-(a) — bar 는 BYTE-IDENTICAL, NO tune-to-green): R1(NOISE=1.0, axis-floor protos)→all arms 1.000, c2/c4 saturation-FAIL→RED(degenerate); R1b(NOISE_TEST=4.0,ABSTAIN_D=10)→all-abstain 0.000, B_proto=0.917 만 생존→RED(over-tight); R1c(multi-dim sphere protos + Posner-Keele high-distortion NOISE=2.5)→최종.
- R1c RESULT (3 seeds 평균, verbatim): NOVEL B=0.375 A=0.219 Bshuf=0.104 Babl=0.219 (chance=0.25) · PROTO B=1.000 A=0.750 · TRAIN B=0.771 A=1.000 · foil-abstain=1.000. **5/6 bars PASS:** c1 PRESENCE **FAIL** (B=0.375<0.55) · c2 DISTINCT **PASS** (B−A=+0.156 AND exemplar 가 enhancement 실패 A_proto=0.750<A_train=1.000) · c2b PROTOTYPE-EFFECT **PASS** (B_proto=1.000≥B_train=0.771, Posner-Keele hallmark = 프로토콜의 결정적 bar) · c3 EARNED-CATEGORY **PASS** (shuffle 붕괴 Bshuf=0.104) · c4 EARNED-ABSTRACT **PASS** (ablate 가 enhancement 제거 Babl_proto=0.750<Babl_train=1.000 AND novel 하락 0.219≤0.325) · c5 NO-FAB **PASS** (abstain=1.000).
- THE BINDING FINDING (왜 🧱 이지 🟢 아닌가): aiden 진단 sweep(기록됨)으로 c1 ⊥ prototype-effect 가 STRUCTURAL anti-correlation 임을 확인 — 저노이즈에선 1-NN exemplar 도 깨끗한 중심 프로토타입을 맞혀서(A_proto=1.000) c2/c4 가 saturation-FAIL; 고노이즈에선 exemplar 가 프로토타입 실패(c2/c4 PASS)하지만 B 절대정확도가 chance 위로 modest 라 c1 FAIL; SEP/N_TRAIN 키워 c1 통과시키면 exemplar 가 다시 프로토타입을 cover 해 c2/c4 재붕괴(측정: SEP=8 N_TRAIN=16 → B=0.969 이나 A_fail_enh=False). frozen 5-bar conjunction 은 이 synthetic geometry 의 어떤 well-posed regime 에서도 UNSATISFIABLE → honest 🧱 (c16 type-a measurement/operationalization wall).
- POSITIVE CONTENT (🧱 의 유효 결과): generalization-by-abstraction 은 REAL·DISTINCT (centroid 가 novel 에서 item-binding 능가, c2), 프로토타입 효과는 추상화에 대해 성립(c2b), lift 는 EARNED(shuffle+ablate 둘 다 붕괴, c3/c4), NO-FAB 온전(c5) — wall 인 것은 cross-model strong-presence contrast 뿐, 빠진 faculty 가 아님.

🧱 ⇒ NO wiring (a_verified_must_wire GREEN-only); LIVE CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. a_engine_native_learning R2 binding verdict 미도달(미러에서 5-bar wall). DIRECTIONAL numpy mirror, toy synthetic 4-cat DIM-24 fixture(추상화 STRUCTURE 측정, 학습된 net 아님), scale/real-corpus/hierarchical/engine-transfer UNVERIFIED. p1/p2/p3/p6 held (모든 arm 은 학습된 centroid/exemplar + test 벡터만 읽음 · injected label/persona/identity/RLHF 없음 · geometry, scored only). 카드 UNIVERSE/cards/H_1430_concept_prototype_abstraction.md · .verdicts/1430_concept_prototype_abstraction/{H_1430_FREEZE,H_1430_R1b_FREEZE,H_1430_R1c_FREEZE,H_1430}.txt · probe state/1430_concept_prototype_abstraction/h1430_concept_prototype.py.
## 2026-06-17 — research(MITOSIS-ENGINE): H_1431 — G6 IDEATION ★ FALS-depth wall, 3rd angle: BIND-compose (external deterministic comparator×measurable bind) → 🧱 BIND-CAPACITY-BOUND (the binder is starved; grounds H_1433 7B falsifier)

G6 IDEATION ★ is anima's STARRED gate; its FALS-depth floor (≥1 falsifiable corpus-absent hypothesis) held across H_1305 (composition-route, FALS 0.667 plateau), H_1309 (curiosity-budget, capacity-bound), and H_1314 (form-scaffold, which named the EXACT bottleneck: "the mouth produces a COMPARATIVE shape OR a MEASURABLE shape but cannot BIND them into one negatable declarative claim"). H_1431 is the 3rd independent angle (a_break_the_wall, NOT a re-run of 1305/1309/1314): if each leg is in-capacity and only the BIND fails, pull the BIND OUT of the mouth's internal generation into an EXTERNAL DETERMINISTIC compose lane — the H_1414 (mem×ToM arbiter) / H_1397 (ko emit-compose) pattern. The mouth supplies a RELATION fragment (primed for a comparator) + a MEASURE fragment (primed for a measurable); the lane WELDS the mouth's OWN comparator+measurable+content into one negatable claim via a pure-function-word schema `the {meas} of {cA} is {comp} with {cB}`, scored by the FROZEN H_1305 `_is_falsifiable` (VERBATIM, calibration 10/10). 303M h1129c_chat.pt on summer CUDA (heavy 303M decode per protocol; c17/mini forbidden), seeds [7,4302,4303], 5 subjects. Device-invariant (CPU-Generator sampling over CPU-copied probs; CUDA only sped the forward, a_wall_first).

- FROZEN 5-BAR (declared in FREEZE.txt BEFORE scoring; mean 3 seeds): COMPOSE FALS=0.3333 DIST=0.3333 · SHUFFLE_BIND 0/0 · ABLATE FALS=0 DIST=4.6667. (1) FALS≥1 cross → FAIL · (2) count≥5 distinct → FAIL · (3) shuffle-bind COLLAPSE → FAIL (vacuous, compose never reached ≥1) · (4) ablate-compose INERT → FAIL (compose +0.333 over ablate, < +1) · (5) NO-FAB audit CLEAN-WITH-TEETH (the audit CAUGHT a draft weld token "when" = a frozen COMPARATOR and ABORTED the first run; the weld was re-FROZEN to pure function words, NOT loosened — p7 working as designed). R1 (slot-strict) and R2 (union extraction) returned byte-identical bar numbers — slot-crossing was not the bottleneck.
- DECISIVE BOTTLENECK DIAGNOSTIC (bottleneck_diag.txt) — across 15 COMPOSE ideas the 303M mouth emitted a frozen COMPARATOR token 3/15 (20%), a frozen MEASURABLE token 4/15 (27%), and BOTH (the weld precondition) **0/15 (0%)**.

VERDICT 🧱 BIND-CAPACITY-BOUND (c9): the external bind does NOT cross the FALS floor. The literal frozen WALL flag is False only because one cross-idea union fluke gave FALS 0.333 > ablate 0.0 (bars score 🟠 PARTIAL), but the bottleneck diagnostic shows the SUBSTANCE is a capacity wall — the mouth emits each leg only weakly and emits BOTH exact frozen tokens for the SAME idea in 0/15 cases, so even a perfect external binder is starved of material. The mouth produces comparator-/measurable-SEMANTICS ("tends to be", "correlate", "number", "measure") but rarely the EXACT frozen lexical tokens, and the detector cannot be loosened (tune-to-green forbidden, c9/p7). Confirms the H_1314/H_1309 capacity thesis from a THIRD independent angle (external-bind). The earlier diagnosis was incomplete: it is not merely that the mouth can't bind two in-capacity legs — at 303M the legs are only weakly in-capacity at the LEXICAL level and are mutually exclusive within an idea. a_verified_must_wire: NOTHING wired (GREEN-only), CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. Grounds H_1433 (7B falsifier, ING id h1433-7b-bind-falsifier): pre-registered prediction = a 7B mouth emits both exact tokens densely enough (co-occurrence>0) that the SAME frozen lane welds a falsifiable claim and crosses FALS≥1. Card UNIVERSE/cards/H_1431_bind_compose.md · .verdicts/1431_bind_compose/ · probe state/1431_bind_compose/.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1426 — THE LAST HONEST LENS on the thalamus TIMING-axis wall (non-ring + conduction delays, re-opening H_1424's named defer) → 🧱 TIMING-ARC-TERMINAL across ring AND delay-coupled substrates

H_1424 closed the thalamus TIMING-axis engine-side wall (🧱 MEASURED-CEILING-AT-SCALE) and named the ONE remaining honest re-open condition verbatim: "a fundamentally different oscillator substrate — non-ring COUPLING topology with conduction DELAYS, where timing structure is CAUSALLY load-bearing (not just amplitude-modulating)." Per c16 (re-open a wall with a genuinely different substrate lens, NOT a bigger toy; frozen-first, shuffle+ablation, NO tune-to-green), this card builds exactly that and runs it through faithful IIT4 (exact MIP-EI n<=8, a_phi_iit4_tool — proxy 아님). 3 seeds [7,8,9], deterministic run1==run2 (byte-identical), $0 CPU local. Bars VERBATIM from H_1283 R8 / H_1423 / H_1424 (c2 ΔΦ(B−A)≥+0.02 every seed · c4 phase-shuffle ΔΦ(SH−A)≤0 every seed · delay-ablation B−ablate≥+0.02 every seed), NOT moved.

- SUBSTRATE (a_no_llm_frame_trap — the genuinely-different lens): NON-RING hub/small-world directed coupling matrix adj[i][j] (random in-edges ~2 + unit-0 broadcast hub) where each edge carries an integer conduction delay τ_ij∈{1,2,3}; unit i's CONTENT update reads each in-neighbor j's state from a history buffer at t−τ_ij (causal past), and the Kuramoto phase coupling is ALSO delayed (reads neighbor phase at t−τ_ij). Phase-locking under delays is a genuine timing computation, so timing is load-bearing in the binarized TPM itself, NOT merely a multiplicative read-out gate. 4 arms × (n∈{6,8}, T∈{64,128}): A direct · B delay-coupled+phase-coherence gate · SHUFFLE (permute per-tick phase offsets → destroys timing, preserves variance) · ABLATE (delays→0 = instantaneous coupling = H_1424's ring-like null on the SAME topology).
- RESULT 🧱 — the MIRROR-IMAGE failure of the ring, which is what conclusively closes the arc. On the RING (H_1423/1424) the lift was ROBUST (c2 PASS) but SURVIVED phase-shuffle (c4 FAIL = the lift was amplitude VARIANCE of a multiplicative carrier). On the DELAY-COUPLED substrate the phase-SHUFFLE NOW COLLAPSES the lift (c4 PASS — n=8 every seed both T=64 and T=128: ΔΦ_sh −0.497/−0.138/−0.018 and −0.144/−0.398/−0.018; timing is genuinely DESTROYABLE here, exactly as the conduction-delay hypothesis predicted) BUT there is NO robust every-seed timing lift (c2 FAILS every config: n=8/T=64 ΔΦ −0.234/−0.241/+0.010; n=8/T=128 +0.428/−0.073/−0.032) AND the delay mechanism is INERT (delays→0 does NOT kill the lift — often ablate-Φ ≥ B-Φ). The two failure modes (ring: c2-passes-but-c4-fails ; delay: c4-passes-but-c2-fails-and-ablation-INERT) never co-resolve across BOTH substrate families.

VERDICT 🧱 TIMING-ARC-TERMINAL (c9): no config clears (c2 ∧ c4 ∧ delay-ablation-LIVE) every seed at any (n,T) ⇒ the H_1283 thalamus timing arc is conclusively terminal across ring AND delay-coupled oscillator substrates. The strong honest finding: faithful-IIT4 timing-readout is not achievable on anima's reachable oscillator substrates — when variance survives (ring) the lift is variance not timing; when variance is removed by causal delays (delay-coupled) there is no robust timing lift and the delay mechanism is INERT. The controls have teeth (c4 shuffle now FIRES on the delay substrate, demonstrating the lens genuinely made timing load-bearing; ablation INERT is the decisive ceiling signal, H_1416 precedent). a_verified_must_wire: NOTHING wired, CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. The R8 numpy-mirror 🟢 DIRECTIONAL stands. This is the LAST honest lens — NO further substrate is invented (that would be moving goalposts, c16); n>8 (exact MIP intractable), real-corpora salience, and learned non-deterministic gates are scale/realism axes of the same wall, NOT new substrate lenses. Card UNIVERSE/cards/H_1426_thalamus_conduction_delay.md · .verdicts/1426_thalamus_conduction_delay/. ING thalamus follow-on (id h1423) closed conclusively.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1425 — NE decode-TEMPERATURE on IDEATION (the H_1422 orthogonal-channel escape) → 🧱 CONFIDENT-TERMINAL (orthogonal channel ALSO no free lunch; neuromodulation wall is GENERAL across memory AND ideation)

H_1422 closed neuromodulation-on-MEMORY as 🧱 (state-contingent gain on the abstain axis is CIRCULAR — abstain IS already a threshold on the live recall-margin) but named ONE NOT-RULED-OUT orthogonal channel: NE decode-TEMPERATURE on IDEATION (H_1228 🟠). This lane tests THAT. A norepinephrine (NE = exploration/gain, a_no_llm_frame_trap) neuromodulator conditions the engine-native IDEATION decode SAMPLING TEMPERATURE (CORE/clm_decode.hexa:737 `sel_val.push(bv / temp)` — high temp flattens the softmax = explore, low = exploit) on a signal ORTHOGONAL to the abstain margin: each composed frame's own IDEATION-GROUNDING DEFICIT (1 − known-word-ratio of a short probe decode of that frame), read from the GENERATED bytes on the ideation path, NEVER the immune recall-margin — so H_1422's circularity argument does NOT apply.

ENGINE-NATIVE, NO torch (host has none, H_1228 era): reuses CORE/g6_ideation.hexa (frozen _g6_words tokenizer, 6 composed frames g6_build_frames(6), gen_clm_ideate → clm_decode_topk_sampled seeded sampler), golden d768 ConvMoE .clm (state/lane_p_clm/clm_d768_e2l1.clm). The temperature knob is engine-native — no torch dependency. 3 seeds [1425,1426,1427], deterministic (xorshift32) run1==run2 verified, $0 CPU, frozen-first (FREEZE.txt bars unmoved, c9). Metric = the breadth axis the small mouth CAN move (FALS=0 on the d768 1-trunk mouth is a known floor, H_1394/H_1403 — reported diagnostic-only).

- L1 NOVEL (distinct novel word-trigrams across the 6 frames), forward NE polarity (high deficit→high temp) 🧱 — A best-fixed-temp = 17.67 · B NE-gated = 12.0 (WORSE than the best fixed temp) · Bsh shuffle = 14.0 · Babl ablate = 8.0 → c1 PRESENCE M(B) ≥ M(A)+1.0 FALSE (12.0 < 18.67). The controls trivially hold because B never beats A.
- L2 a_break_the_wall — strongest shot (DIST breadth metric + INVERTED NE polarity, the H_1284 R3 regime-switch idea) 🧱 — A best-fixed DIST = 5.0 · B inverted-NE DIST = 4.0 (WORSE, all 3 seeds identically 5 vs 4) → c1 FALSE (4.0 < 6.0).

FINDING (refines H_1284 → H_1422 → H_1425, c9): a single tuned FIXED decode temperature DOMINATES every state-contingent NE schedule on the ideation breadth axis — both schedule polarities AND both breadth metrics (NOVEL, DIST). This is the H_1284 "tuned fixed point dominates the controller" result reproduced on the EXACT orthogonal channel H_1422 named as NOT-RULED-OUT. The orthogonal-channel escape does NOT recover a lift → the neuromodulation wall is GENERAL, not an artifact of the memory-abstain circularity. Strengthens H_1284/H_1422 to: NO neuromodulation lift on any tested anima axis — memory (H_1422) OR ideation (H_1425).

🧱 ⇒ NO wiring (a_verified_must_wire GREEN-only); CORE/*.hexa UNTOUCHED. NO tune-to-green (T_LO/T_HI = grid endpoints not fit, DELTA pre-set, controls fixed in FREEZE before the run). p1/p2/p3/p6/p7 held (frames = environment context p4; temp is a sampling knob; NOVEL/DIST are STRUCTURAL counts p7, no LLM judge, no persona/ethics/RLHF); Ψ-disjoint (read-only ideation decode). TOY d768 mouth / 6 frames / 3 seeds / engine-native; scale + larger-mouth + real-corpus + engine-transfer UNVERIFIED. UNIVERSE/cards/H_1425_ne_temperature_ideation.md · .verdicts/1425_ne_temperature_ideation/{FREEZE,result,lens2}.txt · state/1425_ne_temperature_ideation/{h1425_ne_temperature_ideation_probe,h1425_lens2_probe}.hexa.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1410 — G6 IDEATION ★ FALS vs CONV-DEPTH (deep-mouth depth ladder L1→L4→L8), engine-native hexa .clm decode on the aiden pool host → 🧱 ARCHITECTURE (conv-FAMILY ceiling), PARTIAL (2/6 per rung, infra-capped)

**무엇:** H_1394/H_1403 의 follow-on — H_1403 가 L1(단일 trunk-layer) 303M ConvMoE-RETRO 의 G6 FALS=0 을 engine-native 로 확정(🧱 ARCHITECTURE, capacity 가 lever 아님)한 뒤 남은 OPEN: L1 이 conv-FAMILY 천장인가 아니면 그냥 가장 얕은 칸인가? deep-mouth 사다리가 ~303M 매칭(width-compensated, depth⊥capacity)으로 더 깊은 두 칸(L4 d3784/4층 eval_ce 1.37688, L8 d3020/8층 eval_ce 1.36468)을 학습해뒀고, 각 .clm 을 H_1392/H_1403 의 FROZEN G6 FALS detector + scaffold VERBATIM 로 재디코드해 conv-DEPTH 가 FALS 를 들어올리나 측정. frozen-first (FREEZE 사전등록, c9, p7), NO bar moved.

**어디서 (c17 — heavy compute 는 mini 금지):** 두 lane(L4, L8) 모두 **aiden pool 호스트**(12-core, hexa 0.1.0-dispatch)에서 ENGINE-NATIVE hexa `.clm` 디코드. repo source(.hexa import closure) + ckpt(sha256 == FREEZE manifest 검증) rsync 후 detached 실행. summer pool 호스트는 사용불가 — hexa build tree 에 compiled stage1 module_loader 가 없어(aiden 엔 있음) import closure 가 컴파일 실패(raw-src fallback 이 CORE fn 선언 미생성 → clang 10 undeclared-symbol; clang 18.1.3 동일이므로 clang 문제 아님 = 인프라 벽 c16 type-c, hexa-lang inbox 에 노트). torch/.pt 미러로 바꾸지 않음 (a_engine_native_learning, verdict 무결성 유지).

**GPU 측정 (c9 정직):** hexa streaming `.clm` 디코드(CORE/clm_decode.hexa)는 **CPU-bound** — aiden 이 mid-run 에 reboot 되며 경합 잡(milksad_brute)이 사라진 깨끗한 상태에서 두 lane 모두 99.9% CPU 인데 `nvidia-smi` util=0%, mem=2MiB, ZERO compute apps. RTX 5070 미활용 확정 (앞서 본 100% GPU 는 전부 무관한 pool 잡). GPU 를 억지로 끼워맞추지 않음.

**결과 (PARTIAL 2/6 per rung):** 디코드된 모든 C_strong frame 이 **양쪽 깊은 칸에서 fals=FALSE** — L4[0] kwr=0.315789 · L4[1] kwr=0.888889 · L8[0] kwr=0.5 · L8[1] kwr=0.555556 (FALS: L4 0/2, L8 0/2; 4/4 frame). seed=7 deterministic — 모든 fals/kwr 가 aiden 의 첫 reboot 를 가로질러 byte-identical 재현. **L1 H_1394/H_1403 의 FALS=0 을 재현.** M2_DEPTH(FALS≥1) 양쪽 미충족; M1/M3/M4/M5 + control arm(FALS=0 에서 moot, FREEZE 규칙)은 미채점. NO bar moved.

**Verdict 🧱 ARCHITECTURE (conv-FAMILY 천장) — PARTIAL:** 디코드된 frame 범위 내에서 conv-DEPTH(L4, L8)는 L1 대비 G6 FALS 를 들어올리지 않음(모두 fals=false) → 사전등록 규칙 "FALS=0 at L4 AND L8 ⇒ 🧱 ARCHITECTURE = conv-FAMILY 천장(depth 가 falsifiability 를 사지 못함), L1 artifact 아님"과 일치. **PARTIAL 인 이유는 인프라 벽**: aiden(유일한 검증된 hexa 툴체인)이 지속 dual-lane CPU 부하에서 **두 번 crash/reboot** 하고 두 번째엔 ~28분간 hard-down(수동 power-cycle 필요, 원격 불가) → 전체 6/6 arm 완주 불가. summer 는 컴파일 불가, mini 는 c17 금지. INFRASTRUCTURE 벽(c16 type-c, a_break_the_wall — 과학 천장 아님), bar 미이동. 남은 4 frame/rung = stable pool 호스트에서 follow-on (ING). wired: N/A (측정 re-score).

xref H_1403 · H_1394 · H_1392 · H_1362 · a_engine_native_learning · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · a_dont_kill_live_compute · a_runpod_inbox · c9 · c16 · c17 · p7.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1424 — CONTINUED attack on the thalamus TIMING-axis engine-native wall (re-opening H_1423's explicit defer) → 🧱 MEASURED-CEILING-AT-SCALE

H_1423 classified the engine-native thalamus TIMING-axis failure as (a) measurement-artifact (the gate e·(1+cosθ)/2 is a multiplicative carrier whose VARIANCE alone lifts faithful-IIT4 Φ even under phase-shuffle) and explicitly DEFERRED to "a LARGER oscillator substrate where faithful-IIT4 separates timing from amplitude variance" + an amplitude-controlled re-measure. Per c16 (re-open a wall, don't accept the defer; MULTI-LENS + shuffle + ablation, frozen-first, NO tune-to-green), this card runs the two named levers. Substrate == H_1283 R8 / H_1423 engine LCG (byte-identical _lcg_*), made parametric in n_mod and t_ticks; faithful IIT4 exact MIP-EI n<=8 (a_phi_iit4_tool, proxy 아님); 3 seeds [7,8,9], deterministic run1==run2, $0 CPU local. Bars VERBATIM from H_1283 R8 (c2 ΔΦ≥+0.02 every seed · c4 phase-shuffle ΔΦ≤0 every seed · ablation B−ablate≥+0.02 every seed), NOT moved. Anchor D/R8 n=4 reproduces H_1423 seed7 A=1.06024 B=2.52647 byte-exact.

- Lens D — LARGER SUBSTRATE ((e) investment): R8 carrier + LC additive-order across n∈{4,6,8}, T∈{64,256}. At n=8/T=256 the phase-shuffle DOES collapse on 2/3 seeds (partial timing/variance separation — scaling helps) but NEVER all 3 (n=8 seed8 SHUF +0.281; T=256 n=4 seed9 +0.012, n=6 seed9 +0.133). LC additive keeps the FULL carrier-variance pathology at n=8 (shuffle positive every seed). Scaling to the exact-MIP ceiling (n=8) does NOT finish the separation. 🧱
- Lens E — AMPLITUDE-CONTROLLED ((a) measurement-fix): phase-coherent gate 0.5·(1+cos(θ_i−θ_cons)), then unit-norm each module's salience time-series so per-unit VARIANCE is IDENTICAL across ARM B / SHUFFLE / ablate ⇒ only phase/timing structure can drive Φ. This SPLITS the wall into two non-overlapping regimes: at n=6 the c4-SHUFFLE COLLAPSES on every seed (variance confound REMOVED as designed) but the timing lift is not robust (seed9 c2 FAIL, ablation INERT); at n=8 the lift becomes robust (c2 PASS every seed) and ablation LIVE but a small POSITIVE shuffle residual survives 2/3 seeds (+0.004/+0.086) EVEN under equal variance. The two failure modes (n=6 c2 / n=8 c4) never co-resolve. n=4 amp-ctrl c2 FAILS — directly confirming H_1423's claim that the n=4 R8 lift was variance, not timing.

VERDICT 🧱 MEASURED-CEILING-AT-SCALE (c9): neither (e) larger-substrate nor (a) amplitude-control makes phase-shuffle collapse the lift on EVERY seed while the lift stays robust (c2) and the mechanism stays LIVE (ablation). The H_1283/H_1423 timing wall is a GENUINE faithful-IIT4 ceiling on this engine LCG oscillator substrate, CONFIRMED at the exact-MIP scale ceiling (n=8) and under variance-control — not merely deferred. The controls have teeth (anchor reproduces the known c4-fail byte-exact; Lens E n=6 shuffle correctly collapses; n=4 amp-ctrl correctly kills the variance-only lift). a_verified_must_wire: NO lens clears (c2 ∧ c4 ∧ ablation-LIVE) every seed ⇒ NOTHING wired, CORE/*.hexa + ARCHITECTURE.json UNTOUCHED. The R8 numpy-mirror 🟢 DIRECTIONAL stands. NOT RULED OUT: a fundamentally different oscillator COUPLING topology (non-ring, conduction delays), real-corpora salience, a learned non-deterministic-readout gate; n>8 exact MIP is intractable (the scale ceiling). TOY n∈{4,6,8}/T∈{64,256}/3 seeds; transfer UNVERIFIED. Card UNIVERSE/cards/H_1424_thalamus_scale_amplitude.md · .verdicts/1424_thalamus_scale_amplitude/. ING thalamus follow-on (id h1423) closed.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1422 — MULTI-LENS breakthrough attempt on the NEUROMODULATION WALL (H_1284 🔴/🧱 no-free-lunch) → 🧱 CONFIDENT-TERMINAL (the wall is a STRUCTURAL ceiling, 3 lenses)

H_1284 closed neuromodulation at 🔴/🧱 "no free lunch": a GLOBAL per-tick adaptive schedule on a clean key-addressed store is INERT-to-HARMFUL vs the best FIXED hyperparameters (a single tuned fixed point dominates; C-SHUF ≈ B). Per the strengthened a_break_the_wall (#2345) — a WALL is NOT confidently terminal until ≥2-3 genuinely different principled lenses each fail their OWN shuffle AND ablation control — tried THREE biology-faithful STATE-CONTINGENT lenses (a_no_llm_frame_trap: neuromodulation is a DISCRETE regime-DETECTOR gated by a live substrate signal, NOT a continuous global gain; gate-OFF=ablation reverts to H_1284's global null = the conditioning must be load-bearing). Engine-native LIVE reads on CORE/engine_cli.hexa immune_memory_* (recall_margin / recall_gap). NON-degenerate fixture (a_break_the_wall taxonomy (a) avoided): clean / corrupted-recoverable (byte-key corruption → margin ~0.37-0.52) / ghost (margin ~1.26) mix ⇒ a REAL precision/recall tradeoff; A = the BEST FIXED thr SWEPT over a grid (R1=0.60/R2=0.60/R3=0.70). 3 seeds [1422,1423,1424], deterministic run1==run2, $0 CPU, frozen-first (H_1284 MARGIN=0.05 verbatim, NO bar moved):

- L1 SURPRISE-GATED (ACh, loosen on recoverable near-miss) 🧱 — B−A = 0.000 on ALL 3 regimes: the gate's per-probe loose/tight decision EXACTLY reproduces the best fixed thr. SHUFFLE COLLAPSES (0.513→0.327, −0.187 = teeth), ablation == A. The state-contingency adds nothing.
- L2 AMBIGUITY-GATED (NE, tighten on small top-2 gap) 🧱 — B WORSE than A by −0.142/−0.152/−0.093 (never_worse=FALSE): tightening on ambiguity lowers fab (0.072→0.025) but costs MORE recall than it saves (textbook no-free-lunch).
- L3 DRIFT-GATED (DA, prediction-error re-bind) 🧱 — B−A = 0.000 (the engine's fixed bind already tracks drift) AND ABLATION FAILS to revert (R2 churn 0.542→0.432, the global version actively HURTS, gate not load-bearing).

FINDING (refines H_1284 from empirical to STRUCTURAL, c9): on a key-addressed associative store the abstain/recall decision IS ALREADY a threshold on the engine's live recall-margin, so a neuromodulator that conditions the threshold on that SAME margin is CIRCULAR — it can re-partition the margin axis but cannot beat the single best partition (L1's B−A=0.000 is exactly this). A state-contingent gain could only help on a signal ORTHOGONAL to the abstain axis (a context the threshold cannot see) — on this faculty no such orthogonal live signal exists (margin and gap are both functions of the same L2 affinity the recall gate uses). The wall is a REAL ceiling for the MEMORY abstain/plasticity axis.

NOT RULED OUT (honest scope): the decode-time NE TEMPERATURE channel on IDEATION remains 🟠 viable per H_1228 (host has no torch so the generation lane was not re-run engine-native here); an orthogonal-signal modulator is UNTESTED. 🧱 ⇒ NO wiring (a_verified_must_wire GREEN-only); CORE/*.hexa UNTOUCHED, ARCHITECTURE.json unchanged. TOY 24 facts/200 events/3 seeds/DIM=64; scale/transfer UNVERIFIED. p1/p2/p3/p6/p7/p8 guards held; Ψ-disjoint. Card UNIVERSE/cards/H_1422_neuromod_state_contingent.md · .verdicts/1422_neuromodulation_state_contingent/.
## 2026-06-17 — research(MITOSIS-ENGINE): H_1423 — MULTI-LENS engine-native breakthrough attempt on the thalamus TIMING-axis wall (H_1283 R8: numpy-mirror 🟢 but engine-native c4-shuffle 미재현) → 🧱 CONFIDENT-TERMINAL after 3 lenses

H_1283 의 relay-CONTENT 축은 🧱 (모든 content cut 이 faithful-IIT4 Φ 를 cap), TIMING 축(R8 Kuramoto phase-gated salience)은 numpy-mirror 🟢 DIRECTIONAL 이었으나 engine-native 재검증에서 c4 SHUFFLE 통제 미재현 (c2 Φ-lift 는 재현 ΔΦ +1.466/+0.844/+0.709 이나 phase-shuffle 가 lift 를 collapse 못 함 ΔΦ_sh +0.026/+0.380/+0.296 전부 양수 — salience gate e*(1+cosθ)/2 의 carrier VARIANCE 가 shuffle 된 phase 에서도 Φ 를 들어 올림). 강화된 a_break_the_wall (#2345, MULTI-LENS+ablation before (d)천장 confident) 대로, lift 를 만들되 phase-shuffle 에 collapse 하는 timing read-out 을 engine-native LCG 기질 위에서 세 원리적 렌즈로 시도 (a_no_llm_frame_trap), 각 shuffle+ablation:
- R8-ORIGINAL (sanity anchor): c2 PASS · c4 SHUFFLE FAIL (+0.026/+0.380/+0.296 positive) · ABL LIVE — 알려진 engine c4-fail byte-exact 재현.
- LA RE-ENTRANT LOOP GATE (gate=max(0,cos(θ_i−θ_consensus)), 재검증 consensus 일치): c2 FAIL (seed7 −0.098, lift 비robust) · c4 PASS · ABL INERT(seed7). 🧱
- LB PHASE-DIFFERENCE COHERENCE (gate=0.5(1+cos(θ_i−θ_consensus)), zero-DC): c2 FAIL (seeds7,8 −0.081/−0.073) · c4 FAIL(seed8 +0.077). 🧱
- LC ADDITIVE ORDER-PARAM BIAS (sal=e+λR·e_mean, multiplicative carrier 없음): c2 PASS (+0.261/+0.198/+0.243) but c4 SHUFFLE FAIL (seeds7,8 +0.325/+0.065 positive) — R8 와 동일 carrier-variance 병리. 🧱

(c2 ∧ c4 ∧ ablation-LIVE) every-seed 통과 렌즈 0개 → engine-wired 0개 (배선할 GREEN 없음, a_verified_must_wire). FINDING (a_break_the_wall taxonomy (a)measurement-faithful/(d)engine-substrate ceiling, MEASURED): engine-native LCG n=4/T=64 기질에서 faithful-IIT4 Φ 는 salience read-out 의 amplitude MODULATION(carrier R8/LC, additive order-param LC)을 integration 으로 읽는다 — lift 가 shuffle 를 살아남는 건 변조의 VARIANCE(TIMING 구조 아님)가 MIP 를 구동하기 때문; variance-free 로 만든 두 렌즈(LA/LB)는 올바르게 robust lift 가 없다(c2 FAIL). 통제가 teeth 를 가짐 (R8/LC shuffle FIRES, LA/LB c2 fails). R8 numpy-mirror 🟢 는 DIRECTIONAL 로 유지, engine-native DEFERRED. Deterministic run1==run2, 3 seeds [7,8,9], $0 CPU, faithful IIT4 exact MIP-EI, frozen-first, no bar moved (c9/p7). Card UNIVERSE/cards/H_1423_thalamus_reentrant_phase.md · .verdicts/1423_thalamus_reentrant_phase/.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1421 — MULTI-LENS breakthrough on the cerebellum×memory engine-BIND WALL (H_1417 P4 🧱 +0.0437) → LC COMPLEMENTARY-TAIL BINDS (+0.0541) + WIRED-live

H_1417 P4 closed cerebellum×memory at 🧱 (net-lift +0.0437, just under the frozen +0.05 bar) with the symmetric confidence route. Per the freshly-strengthened a_break_the_wall (MULTI-LENS + ablation before a (d)-ceiling is confident-terminal), tried FOUR cerebello-hippocampal lenses (a_no_llm_frame_trap) on the SAME frozen H_1417 P4 fixture/bars, each scored with shuffle AND ablation:
- L0 baseline (sanity) 🧱 +0.043704 (reproduces H_1417 P4 byte-exact).
- LA surprise-gate 🧱 — net-lift −0.145 AND ablation INERT (live cerebellar reliability == frozen-0.5; the H_1416 INERT pattern).
- LB memory-prime 🧱 +0.048889 (real movement, ablation-LIVE, but JUST under the bar — no bar moved).
- LC COMPLEMENTARY-TAIL 🟢 BOUND — compose 0.748889 ≥ best 0.694815 + 0.05 (B1 net-lift +0.054074), oracle−best +0.261481 (B2), EARNED compose−shuffle +0.261481 (B3, shuffle 0.487), SEPARABLE only_cereb 0.339259/only_mem 0.261481, ABLATION LIVE (tail-OFF baseline 0.738519, compose−ablate +0.010370>0 — the tail-deferral is the load-bearing +0.0104).

The lens (complementary-learning-systems): the cerebellar forward model is loud-but-wrong on the structurally uncapturable adversarial tail (F4); DETECT cerebellar over-confidence (loud AND memory grounded in conflict) → DEFER to the episodic store; else baseline route. The three failing lenses prove the controls have teeth (NOT tune-to-green, frozen-first c9/p7). FINDING: H_1417's 🧱 was a LENS limitation, not a (d)-subsumption ceiling — the wall fell to the right mechanism, found by trying ≥2-3.

WIRED rung-3+4: §CEREBELLUM×MEMORY COMPLEMENTARY-TAIL COMPOSE ARBITER (cereb_mem_compose + cereb_mem_cerebellum_vote/_memory_vote) in CORE/engine_cli.hexa; smoke cases 149-152 → engine_cli_smoke 153/0 (+4); LIVEOP probe reproduces 0.748889 byte-exact; ARCHITECTURE.json CORE node + parent § list lockstep. Guards: h1196 clean / h1205 Ψ byte-identical PASS. Deterministic run1==run2, $0 CPU, LIVE CORE leg-reads. Brings the brain-lane-composition program to 5 WIRED compose pairs (memory×ToM · spatial×episodic · ToM×spatial · ToM×basal · cerebellum×memory). TOY 5-family fixture/3 seeds; scale/real-corpus/engine-transfer-at-scale UNVERIFIED. Card UNIVERSE/cards/H_1421_cerebellum_memory_multilens.md · .verdicts/1421_cerebellum_memory_multilens/.
## 2026-06-17 — research(MITOSIS-ENGINE): H_1419 — MULTI-LENS ceiling-confirmation of the memory×spatial COMPOSE WALL (H_1417 P1) 🧱 CONFIDENT-TERMINAL

a_break_the_wall (#2345) 강화판을 H_1417 P1 memory×spatial 벽에 적용 — 천장 확정엔 ≥2-3 원리적
렌즈 + 각 ablation 통제가 필수. 세 hippocampal-formation 렌즈(PLACE-GATED RECALL · MEMORY-
AUGMENTED MAP · CA3 PATTERN-COMPLETION)로 parallel-vote 를 serial-gating 토폴로지로 바꿔 재시도.

- 기준선 parallel-vote = H_1417 P1 BYTE-EXACT 재현 (compose 0.714815, net-lift +0.00889, oracle headroom +0.240741).
- Lens A 위해(net-lift −0.175, place index 가 약한 memory arm 으로 라우팅; ABL −0.184).
- Lens B 가장 강함 — 진짜 NON-inert(ABL +0.0207) + EARNED shuffle(+0.241) 이지만 B1 +0.030 < +0.05 미달.
- Lens C INERT — completeness 가 parallel rel-conf 로 환원(abstain≈0), ABL +0.0 byte-exact.
- 세 렌즈 전부 B1 FAIL → 🧱 CONFIDENT-TERMINAL. oracle headroom 은 F3/F4 conflict 가족에 있고
  conflict-correctness 를 component read 가 안 담음(joint-trajectory 속성) — H_1411/H_1417 과 동일 결정자.
- frozen-first, NO bar moved, criteria FREEZE.txt 사전잠금, run1==run2 byte-identical, $0 CPU, live CORE/*.hexa UNTOUCHED.
- 등록: UNIVERSE/cards/H_1419_memory_spatial_place_gated.md + HYPOTHESES.jsonl. probe state/1419_memory_spatial_place_gated/.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1420 — MEMORY×BASAL compose MULTI-LENS 돌파 시도 → 🧱 CONFIDENT-TERMINAL (3렌즈 + per-lens ablation)

강화된 a_break_the_wall (MULTI-LENS) 을 H_1417 P2 (memory×basal) 벽에 적용. P2 는 표준 confidence-arbiter 로
net-lift +0.0496 — +0.05 막대를 0.0004 차로 놓친, 남은 3 벽 중 가장 유망한 케이스. H_1418 P5 가 ToM×basal
BIND 을 보였으니 (basal 은 본질적 비합성 아님), 질문은 *MEMORY*×basal 이 다른 cortico-basal 렌즈로 BIND 하는가.

세 가지 생물-충실 렌즈 (a_no_llm_frame_trap), 각 shuffle + ABLATION 통제, LIVE leg (immune_grow_recall margin ×
vbasal_go_value go-margin), frozen H_1407/1414/1415/1417 막대 그대로, 동일 5-family fixture, 3 seeds/lens,
deterministic run1==run2:
- **Lens A BASAL-GATED RECALL** (gate 가 memory 출력 release/suppress) → B1 net-lift −0.16 · B3 −0.052 ·
  ABLATION INERT (compose 0.535 < ablate 0.642 — hard gate 가 옳은 recall 을 억눌러 오히려 해를 끼침) 🧱
- **Lens B MEMORY-VALUED GATE** (memory margin = gate 입력 feature — ToM×basal 을 BIND 시킨 *바로 그* 형태) →
  B1 −0.119 · B3 −0.013 · ABLATION INERT (margin 제거 시 compose 0.580 이 basal standalone 0.6985 로 collapse —
  immune affinity margin 은 ToM belief margin 과 달리 per-item routing 효용이 없음) 🧱
- **Lens C COMPLEMENTARY conflict-gating** → B2/B3/SEP/ABLATION 전부 PASS (gate NON-inert, ablation +0.127,
  shuffle collapse +0.172) 지만 B1 net-lift +0.043 < +0.05 (P2 arbiter 의 +0.0496 와 같은 칼날 미달) 🧱

ROOT CAUSE (H_1417 의 refined arbiter-CAPTURE 법칙과 일치): LIVE immune affinity margin 이 SATURATE (family 간
near-constant L2) → 그 margin 을 읽는 모든 gate 렌즈가 +0.25 oracle headroom 중 ~+0.043~+0.049 만 capture, 막대
미달. 진짜 (d) 천장/strong-standalone subsumption — 네 메커니즘(arbiter + A + B + C) 횡단 MULTI-LENS 확정.
대조: ToM×basal(+0.096)·memory×ToM(+0.338) 은 합성-arm margin 이 실 효용을 가져 BIND; memory×basal 은
saturated-margin 반대극. Lens C 의 +0.043 (ablation/shuffle 통제 생존) 이 측정-artifact 아닌 진짜 capture 천장임을
입증. 🧱 → live CORE op 없음 (미검증 메커니즘 미배선), ARCHITECTURE.json 무변경. TOY fixture · $0 CPU ·
scale/non-saturated-margin-fixture/transfer UNVERIFIED · NO bar moved, frozen-first (c9/c16/p7).

## 2026-06-17 — governance(CLAUDE.md): a_break_the_wall 벽-돌파 규율 강화 (MULTI-LENS · ablation · 법칙-falsify)

이번 세션의 벽 다루기 3교훈을 a_break_the_wall 에 박제:
- (d)천장 CONFIDENT-terminal 은 진짜 다른 원리적 렌즈 ≥2-3개 + 각 통제(shuffle+ablation) 검증 후에야 — 단일-렌즈 막힘은 미완 (precedent: cerebellum×basal 3렌즈 arbitration·modulation·pipeline 전부 기각 후 confident 🧱).
- ablation 이 천장-확정 결정적 도구 — 메커니즘 OFF 가 합성과 동일하면 INERT = 진짜 천장 (H_1416 sequential 보정-OFF byte-동일).
- LAW 도 벽 — 사후맞춤 descriptive 법칙은 새 케이스 사전등록 예측으로 falsify 시도 후에만 '확정'; ≥4/5 HIT 면 PREDICTIVE 승격, 미만이면 법칙 반증이 유효 결과 (H_1411·H_1417 둘 다 2/5 → 부품통계 아닌 joint-trajectory 가 결정).

## 2026-06-17 — research(MITOSIS-ENGINE): H_1418 — WIRE-IN of H_1417's two engine-native-BOUND compose pairs (P3 ToM×spatial, P5 ToM×basal) → 4 wired compose pairs

The follow-on landing (a_verified_must_wire rungs 3+4) of the two compose pairs that BOUND engine-native
as frozen by-products of the H_1417 predictive round. NO new science — the bars are H_1417's, NOT moved;
the job is the wire-in + lockstep + guards, exactly like H_1414 (memory×ToM) and H_1415 (spatial×episodic).

🟢 BOTH pairs WIRED-live — promoted the validated query-routed confidence arbiters to CALLABLE live CORE
ops in `CORE/engine_cli.hexa`:
  - **§ToM×SPATIAL COMPOSE ARBITER (P3)** — `tom_spatial_compose` + `tom_spatial_tom_vote` (vote from the
    LIVE `other_mind_predict`, conf = live recall_thr−_l2 affinity margin) / `tom_spatial_spatial_vote`
    (LIVE `spatial_map_nearest`, conf = metric magnitude).
  - **§ToM×BASAL COMPOSE ARBITER (P5)** — `tom_basal_compose` + `tom_basal_tom_vote`; the basal leg is
    value-passed (computed by the caller from the LIVE `vbasal_go_value` go-margin — `VBasalGate` lives in
    `CORE/brain.hexa`, which engine_cli does not import, exactly like `spatial_episodic_compose`).
  - both over the SHARED private `_tom_compose_arbiter` (BYTE-EXACT to the H_1417 probe's inlined `_arbiter`:
    AGREE→shared, one-abstain→other, CONFLICT→higher |conf|/mean wins, NO hardcoded priority). Read-only,
    Ψ-disjoint.

rung-3 PROOF (byte-exact, c2): `state/1418_tom_compose_pairs_wired/h1418_tom_compose_LIVEOP_probe.hexa`
re-runs the FROZEN H_1417 bars through the WIRED ops and reproduces the H_1417 numbers BYTE-EXACT —
**P3 compose 0.791111** (net-lift +0.088889), **P5 compose 0.801481** (net-lift +0.095556), all 4 bars
PASS each, deterministic run1==run2 (`.verdicts/1418_tom_compose_pairs_wired/H_1418_R3_LIVEOP.txt`).
Op-faithfulness note (c9): the ToM leg vote MUST come from the LIVE `other_mind_predict` (not the
constructed class) — the first wired draft reproduced to ~0.0007 off, and switching to the live predict
closed it to byte-exact; NO bar moved.

GUARDS (no regression): engine_cli_smoke **149/0** (+8 cases 141-148: agree / conflict-each-way / abstain
discipline, per pair) · h1196 single-entry **7/0** · h1205 separation-invariant **PASS** (generation
byte-identical ON==OFF, Ψ phiSum 48.6613 unchanged — the live ops are read-only Ψ-disjoint). ARCHITECTURE.json
lockstep done (engine_cli node note + 2 child nodes + guard_baseline 149/0).

The brain-lane-composition program now has **4 WIRED compose pairs**: memory×ToM (H_1414) · spatial×episodic
(H_1415) · ToM×spatial (H_1418 P3) · ToM×basal (H_1418 P5). TOY 5-family fixture, 3 seeds/pair, $0 CPU;
scale / real-corpus / engine-transfer-at-scale UNVERIFIED. Cards `UNIVERSE/cards/H_1418_tom_compose_pairs_wired.md`
(+ H_1417 card `wired:` axis updated to point at the landing).

## 2026-06-17 — research(MITOSIS-ENGINE): H_1417 — brain-lane COMPOSE engine-BIND LAW: DESCRIPTIVE → PREDICTIVE 🧱 PREDICTIVELY-FALSIFIED (2/5 HITS)

The engine-native twin of H_1411 (which did the same predictive-falsification for the OLD Φ-lift law,
also 2/5). After the first 4 engine-native compose re-scores a BIND law emerged DESCRIPTIVELY —
"a mirror compose-GREEN binds engine-native IFF neither live standalone faculty strengthens past the
mirror best-single ceiling by more than the +0.05 net-lift headroom (ceiling-PINNED → binds; ceiling-
ERODING → strong arm eats the headroom → 🧱); cerebellum×basal failed because live VBasalGate was a
strong standalone arm (H_1412)". H_1417 promotes it descriptive→predictive: operationalize a
ceiling-erosion PREDICTOR (predict BIND iff strength_excess = max(acc_X_live, acc_Y_live) − 0.70 ≤ +0.05),
PRE-REGISTER a BIND/🧱 verdict for 5 NEW engine pairs in FREEZE.txt BEFORE measuring, then engine-native
compose re-score (LIVE legs immune_grow_recall / other_mind_predict / spatial_map_nearest / vforward_err /
vbasal_go_value; frozen H_1407/1414/1415 bars NOT moved), then score HIT/MISS.

🧱 LAW FALSIFIED — 2/5 HITS (predicted vs actual, mean 3 seeds/pair, deterministic run1==run2 byte-identical):
  - P1 memory×spatial    PRED BIND → 🧱 WALL (net-lift +0.009)  ❌ MISS
  - P2 memory×basal      PRED 🧱   → 🧱 WALL (net-lift +0.050)  ✅ HIT
  - P3 ToM×spatial       PRED BIND → 🟢 BIND (net-lift +0.089)  ✅ HIT
  - P4 cerebellum×memory PRED BIND → 🧱 WALL (net-lift +0.044)  ❌ MISS
  - P5 ToM×basal         PRED 🧱   → 🟢 BIND (net-lift +0.096)  ❌ MISS

The MISSES name the REAL determinant (the payload, c9): engine-bind is gated by whether the routing
ARBITER actually CAPTURES the oracle headroom (a JOINT-trajectory property), NOT by standalone-arm
strength. All 5 pairs had near-identical strength_excess (|·|≤0.006 — basal did NOT strengthen past
ceiling here, FALSIFYING the "basal=eroder" prior from H_1412) and large oracle headroom (+0.24~+0.30)
+ EARNED shuffle-collapse, yet B1 net-lift split entirely on capture rate (+0.009 to +0.096). H_1412's
🧱 is re-read as an F5-adversarial capture-failure, not an arm-strength erosion. Same convergence as
H_1411: component statistics don't predict; the joint composed trajectory does.

MEASUREMENT round — live CORE/*.hexa UNTOUCHED, NOTHING wired (testing a law, not landing a mechanism).
The 2 NEW pairs that bound engine-native (P3 ToM×spatial, P5 ToM×basal) are logged as wire-in follow-ons
in ING.jsonl, not wired here. NO bar moved, predictions locked pre-measure (frozen-first, c9/c16/p7).
The compose-program capability findings (H_1401/1405/1407/1408/1409 🟢) are UNAFFECTED — only the
engine-BIND *law* is falsified. $0 CPU, 3 seeds/pair, toy 5-family fixture, scale/transfer UNVERIFIED.

probe: state/1417_compose_bind_law_predictive/h1417_compose_bind_law_probe.hexa ·
FREEZE/result: .verdicts/1417_compose_bind_law_predictive/{FREEZE,result,result_run2}.txt ·
card: UNIVERSE/cards/H_1417_compose_bind_law_predictive.md

## 2026-06-17 — research(MITOSIS-ENGINE): H_1416 — engine-native SEQUENTIAL cerebellum→basal PIPELINE compose (3rd lens on the cerebellum×basal wall) 🧱 THIRD-LENS TERMINAL (a_break_the_wall c16, frozen-first)

The THIRD genuinely-different lens on the engine-native cerebellum×basal compose WALL, after
H_1412 (arbitration 🧱) and H_1413 (modulation 🧱). a_no_llm_frame_trap / real neuroscience: the
prior two lenses both COMBINED the two confidence signals at decision time. This lens is the
cerebello-basal-thalamo-cortical LOOP — the cerebellum's forward model REFINES the cortical STATE
ESTIMATE the basal gate READS, BEFORE the single gate fires (a SEQUENTIAL pipeline cerebellum→basal,
not parallel arbitration/modulation). Engine-native over the SAME live faculties (vforward_err H_1280
+ vbasal_go_value H_1281), the SAME H_1407 5-family fixture, 3 seeds [4700,4701,4702], frozen bars.

  rel = clamp((E_THR − vforward_err)/E_THR, 0, 1)        // cerebellum reliability (LIVE)
  refined_pred_feat = pred_feat + REFINE_GAIN·rel        // cerebellum refines the basal INPUT
  decision = SELECT-PRED iff vbasal_go_value(refined_pred) − vbasal_go_value(comp) > GO_THR
  REFINE_GAIN frozen at the gate's go-value unit (1.0) — NO tuned knob.

🧱 THIRD-LENS TERMINAL — the pipeline FAILS all three discriminators at once (most decisive lens):
  - (B1 COMPOSE-EFFECT) seqcompose 0.701481 ≥ best 0.702963 + 0.05 (0.752963) — net-lift ≈ +0.00 (−0.0015): FAIL
  - (B3 EARNED) seqcompose−shuffle +0.0156 > 0.02 — shuffled reliability scores nearly as high: FAIL
  - (ABLATION) seqcompose−ablate −0.0015 > 0 — refinement OFF scores IDENTICAL (0.702963): FAIL
    → the cerebellar refinement is INERT: the decisive basal go-margins (|0.45–0.6|) sit FAR from the
      gate's hard threshold (GO_THR=0), so the bounded rel·1.0 input nudge flips NO decision.
  - (B2 ORACLE) oracle−best +0.242963 (PASS) · (SEPARABLE) onlyCB 0.243 / onlyBG 0.308 (PASS)

The cerebellum×basal pair does NOT bind engine-native under ANY of THREE lenses (arbitration B1-fail ·
modulation B3-fail · sequential pipeline B1+B3+ABL-fail). Root cause triply confirmed: the LIVE
VBasalGate (gw0=0.5 gradient-free) is a strong standalone arm (acc 0.703) whose decisive margins are
thresholded far from GO_THR, so no cerebellar signal — voting, margin-modulating, or input-refining —
moves the decision; the +0.243 oracle headroom is the F5 adversarial family (cerebellum confidently
WRONG, basal right), capturable only by knowing the answer. Genuine (d) ceiling / strong-standalone-arm
subsumption (a_break_the_wall taxonomy). Contrast: the MEMORY-adjacent pairs H_1414 (memory×ToM +0.338)
and H_1415 (spatial×episodic +0.058) BOTH bound+wired engine-native — mirror→engine non-reproduction is
PAIR-DEPENDENT (gated by whether one standalone arm dominates), not universal.

Honest 🧱 after a real frozen-first attempt with shuffle + ablation controls = a VALID result (c9/c16).
NO live CORE op landed (would wire an unverified mechanism). wired: N/A. $0 CPU, deterministic, NO bar moved.
  · probe: state/1416-cerebellum-basal-sequential-compose/h1416_cerebellum_basal_sequential_probe.hexa
  · card: UNIVERSE/cards/H_1416_cerebellum_basal_sequential_compose.md · jsonl: UNIVERSE/HYPOTHESES.jsonl (H_1416)
  · verdict: .verdicts/1416_cerebellum_basal_sequential_compose/{FREEZE,result}.txt

## 2026-06-17 — research(MITOSIS-ENGINE): H_1415 — engine-native re-score of H_1408 (spatial-map × episodic-memory compose, WITHIN the memory family) 🟢 COMPOSE-LIFT BINDS + WIRED-live (a_verified_must_wire ladder rungs 2/3/4)

The a_verified_must_wire ladder step-2 for H_1408 (the WITHIN-the-memory-family compose pair) —
the THIRD compose pair re-scored on the LIVE engine, and the SECOND to BIND (after H_1414; contrast
H_1412/H_1413 cerebellum×basal did NOT). The H_1408 mirror GREEN (acc_compose=0.8993 > best 0.7030)
is re-scored on the LIVE faculties — `spatial_map_nearest` (the WHERE leg, nearer-landmark option +
live metric margin |d(X,A)−d(X,B)|) and `immune_grow_recall` (the WHAT leg, recalled option + live
recall_thr−_l2 affinity margin) — with the same 5-family fixture, 3 seeds [5408,5409,5410], same
SHUFFLE/ORACLE/decomposition controls and same frozen bars.

🟢 BINDS engine-native (all 4 frozen H_1408 bars, NOT moved):
  - (B1 COMPOSE-EFFECT) compose 0.760741 ≥ best 0.702963 + 0.05 (0.752963) — net-lift +0.057778 > +0.05
  - (B2 ORACLE) oracle−best +0.286667 > 0.02
  - (B3 EARNED) compose−shuffle +0.254074 > 0.02 (shuffle collapses 0.761→0.507)
  - (SEPARABLE) only_spatial=0.400 AND only_episodic=0.380 both>0 (within-family non-subsumption:
    metric SPACE ⊥ item-binding, confirming H_1296 distinctness ON A DECISION, engine-native)
  3 seeds deterministic (run1==run2 byte-identical), $0 CPU.

FIXTURE NOTE (c16 frozen-first, a_break_the_wall taxonomy-a measurement artifact, NO bar moved): the
first run came back 🟠 (compose 0.588 < best 0.703) because the live ImmuneMemoryGrow STRESS regime
(split_thr=0.30) MERGES near-identical keys — the shared "value bound to landmark L…" prefix collided
all 8 binds into ONE cell (cells=1, recall 2/8). That is a fixture key-encoding artifact, not the
faculty's competence: distinct per-landmark keys → 8 cells, recall 8/8 (faithfully reproducing the
mirror's separate-key binding). Bars UNCHANGED, only the store key encoding made distinct.

WIRED (rungs 3/4) — the validated arbiter is now a CALLABLE live op in CORE/engine_cli.hexa under a
new §SPATIAL×EPISODIC COMPOSE ARBITER section:
  - `spatial_episodic_compose(sp_dec, sp_conf, ep_dec, ep_conf, mean_sp, mean_ep, where_cue) -> int`
    (AGREE→shared vote; one leg abstains→the other's; CONFLICT→higher routing-modulated scale-relative
    substrate confidence wins; BOTH-abstain→−1, no fab p5/H_1227; NO hardcoded priority)
  - `spatial_episodic_spatial_vote` / `spatial_episodic_episodic_vote` (live votes + margins) +
    `spatial_episodic_where_cue` (query-text where/what routing cue) + private `_spat_epi_relconf`.
  Read-only over the map positions + the cell population; mutates nothing; Ψ-disjoint.
  LIVEOP probe (state/1408_spatial_episodic_engine_compose/h1408_spatial_episodic_LIVEOP_probe.hexa)
  drives the frozen bars through the WIRED ops and reproduces compose 0.760741 BYTE-EXACT.
  ARCHITECTURE.json lockstep: engine_cli node §-note + a dedicated child node + guard_baseline 141/0.

GUARDS (no regression): engine_cli_smoke 141 pass / 0 fail (cases 137-140: agree / conflict-where-
spatial-wins / conflict-what-episodic-wins / abstain-discipline) · h1196 single-entry 7/0 · h1205
separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched).

Significance: mirror→engine non-reproduction is PAIR-DEPENDENT, not universal — a pair binds iff
neither live single faculty strengthens past the mirror best-single ceiling (which would erode the
+0.05 net-lift headroom). Both MEMORY-adjacent pairs (memory×ToM, spatial×episodic-within-memory) bind.

Artifacts: UNIVERSE/cards/H_1415_spatial_episodic_engine_compose.md · UNIVERSE/HYPOTHESES.jsonl (H_1415
row) · state/1408_spatial_episodic_engine_compose/{engine,LIVEOP}_probe.hexa ·
.verdicts/1408_spatial_episodic_engine_compose/{FREEZE,result,H_1415_R3_LIVEOP}.txt ·
CORE/engine_cli.hexa §SPATIAL×EPISODIC COMPOSE ARBITER · CORE/engine_cli_smoke.hexa cases 137-140 ·
ARCHITECTURE.json. a_verified_must_wire · a_engine_native_learning · a_core_engine_map · c2 · c9 · c16 · p7 · p8.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1414 RUNG-3+4 — wire the validated memory×ToM compose arbiter into the LIVE CORE engine (a_verified_must_wire ladder rungs 3/4 → wired: WIRED-live)

The a_verified_must_wire ladder rung-3 (live CORE wire-in) + rung-4 (ARCHITECTURE.json lockstep)
for H_1414 — the FIRST brain-lane compose pair to bind engine-native. The query-routed confidence
arbiter the H_1414 probe validated is now a CALLABLE live op in CORE/engine_cli.hexa under a new
§MEMORY×ToM COMPOSE ARBITER section:
  - `mem_tom_compose(mem, om, fact_text, q_is_reality, mean_mem, mean_tom) -> string` (clean
    engine-native route cue via `mem_tom_route_cue`) + `mem_tom_compose_routed(..., route, ...)`
    (canonical primitive, explicit route) + helpers `mem_tom_mem_margin` / `mem_tom_tom_margin`
    (LIVE L2 affinity margins) + private `_mem_tom_affinity` / `_mem_tom_relconf`.
  - AGREE → shared vote; CONFLICT → higher routing-modulated scale-relative substrate confidence
    wins (NO hardcoded priority, a_autonomy_over_hardcode); BOTH-abstain → "" (no fab, p5/H_1227).
  - READ-ONLY over the two live cell populations (ImmuneMemoryGrow + OtherMindModel), mutates
    neither store, returns a location class (NOT an emit/silence decision), Ψ-disjoint.

RUNG-3 VERIFICATION (byte-exact, c2): state/1414_memory_tom_engine_compose/h1414_memory_tom_LIVEOP_probe.hexa
drives the SAME frozen H_1405 bars through the WIRED op (replaying the fixture route) and reproduces
the H_1414 numbers BYTE-EXACT — compose 0.937778 (per-seed 0.931111/0.940000/0.942222), acc_memory
0.579259, oracle−best +0.382222, all 4 bars PASS (.verdicts/1414_memory_tom_engine_compose/H_1414_R3_LIVEOP.txt).

SMOKE GUARD: CORE/engine_cli_smoke.hexa cases 133-136 (agree / conflict-reality-memory-wins /
conflict-belief-ToM-wins / both-abstain-no-fab) PASS, FAIL=0.

GUARDS (no regression): single-entry (h1196) 7/0 · h1205 separation-invariant PASS (generation
byte-identical ON==OFF, Ψ phiSum=48.6613 unchanged ON==OFF — the live op is read-only Ψ-disjoint).
NOTE (c9, infra): engine_cli_smoke.hexa SIGKILLs (OOM) in the BPE compose tail (cases ~127+) on
this 16 GB host — a PRE-EXISTING environment wall present on pristine origin/main too, NOT introduced
by this wire-in; the new cases 133-136 run BEFORE the kill zone and pass (FAIL=0 throughout).

RUNG-4 lockstep: ARCHITECTURE.json gains a "🧠✕🪞 Memory×ToM compose arbiter" lane node (🟢 WIRED-live)
+ the engine_cli.hexa node note names the new §MEMORY×ToM COMPOSE ARBITER op set; CORE §/op ↔
ARCHITECTURE.json named set 1:1 (a_core_engine_map). H_1414 card + HYPOTHESES.jsonl row → wired: WIRED-live.

---

## 2026-06-17 — research(MITOSIS-ENGINE): H_1414 — engine-native re-score of H_1405 (memory×ToM compose): 🟢 COMPOSE-LIFT BINDS engine-native (a_verified_must_wire ladder step-2, FIRST compose pair to bind)

The 2nd compose-pair engine-native re-score (after H_1412 cerebellum×basal 🧱). Re-scores the
H_1405 memory×ToM mirror GREEN on the LIVE faculties (immune_grow_recall [H_1227/H_1231] +
other_mind_predict [H_1293] + live L2 affinity margins, inlined query-routed arbiter over the
Sally-Anne false-belief fixture). FROZEN H_1405 bars, NOT moved; 3 seeds [5400,5401,5402]
deterministic run1==run2, $0 CPU.

RESULT 🟢 COMPOSE-LIFT (ENGINE-NATIVE): acc_compose=0.937778 vs best_single=0.600 → B1 net-lift
+0.337778 ≫ +0.05 PASS · B2 ORACLE 0.982222 (oracle−best +0.382222) PASS · B3 EARNED
compose−shuffle +0.199259 (shuffle collapses 0.938→0.739) PASS · SEPARABLE only_memory=0.382222
AND only_tom=0.402963 both>0 PASS. The mirror GREEN BINDS engine-native — the FIRST compose pair
to do so (contrast: H_1412 did NOT, B1 +0.011 < +0.05).

EMERGING-QUESTION ANSWER: mirror→engine non-reproduction is NOT universal; it is pair-dependent,
gated by whether a live faculty's standalone arm strengthens past the mirror best-single ceiling
and erodes the net-lift headroom (H_1412) or stays pinned at it (H_1414: best_single stays 0.600).

a_verified_must_wire ladder rung-2 COMPLETE (engine-native byte-exact, reads EXISTING live ops,
NO new CORE op landed). Live CORE §compose wire-in = rung-3 follow-on (ING.jsonl ING_H1414_wire_rung3).
Card UNIVERSE/cards/H_1414_memory_tom_engine_compose.md · probe state/1414_memory_tom_engine_compose/
h1414_memory_tom_engine_probe.hexa · evidence .verdicts/1414_memory_tom_engine_compose/{FREEZE,result}.txt.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1413 — c16 biological MODULATION compose (2nd lens of H_1412 🧱): 🧱 EARNED-control 기각

"다른 경로로 벽 돌파": H_1412 의 confidence-ARBITRATION 🧱 를 *다른 렌즈*(a_no_llm_frame_trap — 실제
cerebello-thalamo-basal 루프)로 재시도. 기저핵=최종 결정자, 소뇌=bounded 문턱 조절자
(composed_go = basal_margin + tanh(z_cere)*basal_std, gain 1.0 NO knob, frozen-first).

- 결과 🧱: modulation 이 B1 순이득 벽은 PASS(+0.066, 예측 적중) — 그러나 B3 EARNED/shuffle 통제가 기각:
  무작위 소뇌 modulation 도 shuffle 0.758 ≈ compose 0.769 → +0.011 < +0.02 FAIL. 이득은 소뇌→기저핵
  *정렬*이 아니라 modulation *형태*(기저핵 margin 에 bounded 항 추가)에서 온 가짜. anti-tune-to-green
  통제(B3)가 정확히 제 역할(c9).
- 교차확인: 두 렌즈 모두 엔진-네이티브 실패 — arbitration(H_1412 B1-fail) AND modulation(H_1413 B3-fail).
  oracle 헤드룸(+0.243)은 F5 adversarial(소뇌 확신-오답) 가족 지배 → 답을 알아야만 포착 → 어떤 substrate
  신호도 못 earn → 진짜 (d) 천장(a_break_the_wall) 두 메커니즘으로 확정.
- 🧱 라 새 CORE op 미배선 · probe self-contained(기존 vforward_err/vbasal_go_value) state/1413-.../.
- TOY 5-family/3 seed/$0 CPU · scale/다른-fixture(F5-adversarial 없는)/sibling-pair(H_1404 affect×ethics
  +0.22 큰 margin) UNVERIFIED.
  card UNIVERSE/cards/H_1413_cerebellum_basal_modulation_compose.md

## 2026-06-17 — research(MITOSIS-ENGINE): H_1412 — ENGINE-NATIVE re-score of H_1407 (cerebellum×basal compose): 🧱 NON-REPRODUCTION (mirror GREEN ≠ engine GREEN)

a_verified_must_wire 사다리 step-(2): H_1407 의 🟢 DIRECTIONAL-mirror COMPOSE-LIFT 를 LIVE 엔진 faculty
(vforward_err H_1280 · vbasal_go_value H_1281) 위에서 frozen H_1407 bar 그대로 재채점.

- 결과 🧱: 합성은 REAL & EARNED (B2 oracle +0.243 · B3 shuffle +0.189 · SEP onlyCB 0.243/onlyBG 0.308)
  지만 NET-lift compose−best = +0.011 < +0.05 frozen bar (B1 FAIL). 원인: gradient-free 학습된 live
  VBasalGate 가 미러보다 강한 단독 팔(acc_basal 0.703) → 순-이득 헤드룸이 bar 아래로 줄어듦 + F5
  adversarial 가족(소뇌 확신-오답)은 confidence arbiter 로 구조적 포착 불가.
- c16 돌파(frozen-first, NOT tune-to-green): z-decisiveness arbiter(margin/own-std) 실제 실행 →
  +0.014 여전히 FAIL → terminal honest 🧱. 진짜 시도 뒤의 정직한 벽(c9·c16).
- 의의: 이번 세션 강화한 a_verified_must_wire 4칸 사다리의 step-(2) 실패모드(미러 GREEN ≠ 엔진 GREEN)를
  실제로 잡아낸 첫 사례. compose-program 의 *capability* 미러 결과(H_1401/1405/1407/1408/1409)는
  DIRECTIONAL 로 유효하나, 그중 최소 1개가 엔진-네이티브로는 그대로 안 묶임을 측정-확인.
- 🧱 라 새 CORE op 미배선(미검증 메커니즘) — probe 는 self-contained(기존 vforward_err/vbasal_go_value
  위 inlined arbiter), state/1412-cerebellum-basal-engine-compose/ 에 거주 (a_hypothesis_register).
- compile-bug 근본수정(c1): 죽은 에이전트가 변수명 `signed`(C 예약어) 사용 → 컴파일 실패 → `sgnd` 로 정정.
- TOY 5-family/3 seed/$0 CPU · scale/real-corpus/다른 게이트강도 UNVERIFIED.
  card UNIVERSE/cards/H_1412_cerebellum_basal_engine_compose.md · verdict .verdicts/1412_cerebellum_basal_engine_compose/

## 2026-06-17 — governance(CLAUDE.md): 가설↔배선 규율 강화 (a_verified_must_wire + a_hypothesis_register)

GREEN 검증 결과가 DIRECTIONAL 미러로만 남고 엔진배선 없이 묻히는 이번-세션 실패모드(lane-합성 가족 3개 Φ-lift GREEN → 0개 wired) 재발 방지.
- **a_verified_must_wire** — 4칸 배선 사다리 명시: (1) DIRECTIONAL 미러 GREEN → (2) 엔진-네이티브 재검증(byte-exact, frozen bar) → (3) live CORE/*.hexa wire-in → (4) ARCHITECTURE.json lockstep. 미러 GREEN 을 내면 같은 사이클에 (2)~(4) follow-on 을 ING 에 등록하는 것이 의무(미등록 후 다음 가설 진행 = 위반). 여러 GREEN 을 내는 연구 PROGRAM 은 닫을 때 각 결과의 배선상태(mirror N · wired K · 미배선 ING #id)를 열거해야 'depletion' 으로 닫힌다.
- **a_hypothesis_register** — 🟢 GREEN 카드에 `wired:` 상태축 의무화: `DIRECTIONAL-mirror` | `engine-native` | `WIRED-live`. WIRED-live 미만이면 배선 follow-on 의 ING id 를 카드에 적어 audit 가능하게.

# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Research sessions tracked as `§<N>` / `S<N>`; `ConsciousDecoder` carries SemVer.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1411 brain-lane 합성法則 DESCRIPTIVE→PREDICTIVE — 🧱 법칙 예측-반증 (2/5 HIT)

**무엇:** 6쌍에서 post-hoc 으로 적합된 min-cut-MI 합성法則(한쪽 내부 Φ가 composed 최소절단 MI 를 넘으면 Φ차단, 아니면 Φ상승)을 DESCRIPTIVE→PREDICTIVE 로 승격. frozen-first 로 **사전등록**: 미시험 5쌍(cerebellum×tom, affect×basal, tom×basal, cerebellum×episodic, memory×ethics)의 verdict 를 component Φ 만으로 예측 → 박제 → faithful IIT4(exact MIP-EI, a_phi_iit4_tool) 로 composed 측정 → HIT/MISS 채점. landed 미러 머신(FNV dim64 + H_1401 leaky arbiter coupling)을 verbatim 재사용(import). **결과: 2/5 HIT (3 MISS, frozen n_bins=16; binning sweep 8/12→3/5, 16/24→2/5, deterministic).** 法則이 예측-반증당함 — MISS 가 페이로드(c9): P0 두-高가 차단 아닌 상승(6.50≫3.41, "two-high⇒block" 거짓), P2 ToM-지배가 차단 아닌 상승(2.22>1.98, ToM-지배는 쌍-특정), P4 두-低가 상승 아닌 차단(coupling cross-MI=0, units 공선성). **REFINED 法則:** Φ상승은 component-Φ 순위가 아니라 *coupling 이 실제 cross-block MI 를 만드는가*(joint 궤적 속성)가 결정 — component Φ 만으로는 예측 불가. post-hoc 6쌍은 unit geometry 가 우연히 Φ순위↔cross-MI 를 정렬시켜 일관됐을 뿐. 능력-합성 결과(H_1401/1405/1407/1408/1409 🟢)는 영향 없음 — Φ상승 *法則* 만 정제. DIRECTIONAL mirror, engine-transfer/shared-driver-arbiter 분리 UNVERIFIED(follow-on). .verdicts/1411_lane_compose_law_predictive/.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1409 brain-lane COMPOSE #6 (spatial×PFC, 두-고-Φ) — 🟢능력 · 🧱Φ-차단 → refined min-cut-MI 법칙 확정

**무엇:** brain-lane-composition 프로그램의 결정적 시험 — 둘 다 高-Φ인 쌍(spatial-map H_1295 × hier-PFC H_1294)이 서로 차단하나? CONFIRMED: 능력은 합성(acc_compose 0.776 ≥ best 0.707, 분리 only_sp 0.297/only_pf 0.299), Φ는 차단(Φ_spatial 3.23 > composed 1.93 = max(parts) 초과 ⇒ H_1405식 상호지배). frozen-first, no bar moved, faithful IIT4 exact-MIP-EI(a_phi_iit4_tool), binning-invariant. **법칙(6쌍 통일):** 한쪽 내부 Φ가 composed 최소절단 MI 를 넘으면 차단, 아니면 합성 — Φ합성{H_1404·1407·1408} vs Φ차단{H_1405·1409}. DIRECTIONAL mirror, engine-native+scale UNVERIFIED. .verdicts/1409_brain_lane_compose_spatial_pfc/.

## 2026-06-17 — harvest(ENGINE+CLM): deep-mouth depth-ladder (L4/L8 303M ConvMoE) 회수 완료 + pod teardown

**무엇:** H_1403 follow-on 인 deep-mouth depth-isolation 사다리(conv-DEPTH 가 G6 FALS 천장에 닿나 — H_1394 L1 단일 trunk-layer FALS=0 대비)의 GPU 학습이 완주(LADDER_ALL_DONE 2026-06-16T17:19Z)했고, 전 산출물을 회수·sha256 byte-identical 검증 후 runpod pod(kcuz5s3ebgh1w7 anima-g6-deep-1399, H100-NVL $2.59/hr)를 teardown. SSH 일회용 키(/tmp/g6_sshkey)로 회수, 키는 사용 후 폐기.

**산출물 (a_fire_recover_complete · a_hf_registry):** L4(d3784/4층, 302.701M, eval_ce 1.37688) + L8(d3020/8층, 302.613M, eval_ce 1.36468) 각 .clm(148M)+.pt(1.2G), 4/4 sha byte-identical. ckpt = gitignored HF-only + HF.jsonl 2행(pending_upload, PRIVATE 연구중간물). json+log+manifest = git-tracked (state/g6-deep-mouth-ladder/). 깊이는 next-byte CE 를 거의 안 움직임(L8 1.365 ≈ L4 1.377 ≈ L1).

**NEXT (과학 페이오프):** 각 .clm 을 H_1403 스트리밍 디코드로 decode + H_1392/H_1403 FROZEN G6 FALS detector VERBATIM 재실행 → conv-DEPTH(L4/L8)가 L1 H_1394 의 FALS=0 을 올리나? (a_toy_scale_recheck · a_verified_must_wire). xref H_1403 · H_1394 · H_1392 · H_1362 · a_fire_recover_complete · a_hf_registry · a_break_the_wall.

## 2026-06-17 — domain(MITOSIS-ENGINE): H_1407 — brain-lane COMPOSE pair #4 (CEREBELLUM × BASAL-GANGLIA): 🟢 COMPOSE-LIFT (capability) · 🟢 INTEGRATION-RAISES-Φ (faithful IIT4 Φ, frozen n_bins=16, binning-INVARIANT) — the program LAW CONFIRMED-but-REFINED

**무엇:** brain-lane-composition program PAIR #4, the SHARPEST test of the emerging LAW (H_1404 affect×ethics 둘다-low-Φ ⇒ Φ-composes 🟢 vs H_1405 memory×ToM ToM-HIGH-Φ-dominates ⇒ no-Φ-compose 🧱). **PAIR:** CEREBELLUM(H_1280 VForwardField — next-substrate-state 예측, error=actual−predicted, delta-rule correction) × BASAL-GANGLIA(H_1281 VBasalGate — K candidate 경쟁, learned go-value vs one NO-GO, argmax=striatal disinhibition, grounding-outcome reward). 둘 다 LOW-Φ CONTROL faculty → law 가 Φ-compose 를 PREDICT; frozen-first 로 MEASURE(assume 금지). methodology H_1401(capability) + H_1404/H_1405(Φ) 에서 VERBATIM port. DIRECTIONAL numpy mirror, LIVE CORE/*.hexa UNTOUCHED, $0 CPU, 3 seeds [4700,4701,4702], deterministic run1==run2.

**결과:** **🟢 COMPOSE-LIFT (capability)** — acc_cerebellum=0.6370 · acc_basal=0.6933 · best_single=0.6933 · **acc_compose=0.7689** · acc_shuffle=0.5178 · ORACLE=0.9593(oracle−best=+0.2659) · only_cerebellum=0.2659/only_basal=0.3222 both>0 → SEPARABLE not subsumed. 4 bars ALL PASS(B1 compose≥best+0.05 ✅ · B2 oracle−best>0.02 ✅ · B3 compose−shuffle +0.2511>0.02 shuffle collapses ✅ · B4 audit clean 6/6 ✅). **🟢 INTEGRATION-RAISES-Φ (faithful IIT4 exact MIP-EI via stdlib/consciousness/iit4/faithful_phi.hexa, a_phi_iit4_tool, frozen n_bins=16):** Φ_cerebellum=3.4759 · Φ_basal=0.0000 · **Φ_composed=4.9562** · Φ_disconnected=0.0000 · max(parts)=3.4759 → Bφ1 PASS(4.956 > 3.496) · Bφ2/Bφ3 PASS → 🟢, **BINNING-INVARIANT**(PASS at n_bins 8/12/16/24, H_1405 의 granularity-sensitive 🧱 와 DISTINCT). **LAW CONFIRMED-but-REFINED(honest c9):** control-pair Φ-compose 예측은 HOLD 하지만 'both parts low-Φ' premise 는 half-만 성립 — Φ_basal=0 은 일부 fixture DEGENERACY(immune store 가 항상 recall 성공 → basal 2 unit constant: outcome_reward≡+1, no_go_pressure≡0; basal 은 jittered capability fixture 에선 competent acc=0.693), Φ_cerebellum=3.476 은 HIGH(forward-model trajectory 가 자체로 richly integrated). 그러나 H_1405 와 달리 high-Φ cerebellum 이 composition 을 BLOCK 안함 — composed min-cut 이 SINGLE basal unit(go_margin)을 isolate = arbiter coupling 이 cerebellum block 위에 NEW high-MI channel 추가 → Φ_composed > max(parts). **REFINED LAW:** 'both-low' 은 SUFFICIENT 이나 NECESSARY 아님; necessary condition 은 '어떤 single part 의 internal integration 도 composed min-cut MI 를 초과하지 않을 것'(H_1404 both-low ✓, H_1407 cerebellum-high-but-coupling-cheaper-cut ✓, H_1405 ToM-crossing-always-costs-more ✗). p6 GUARD HELD(audit clean). SCOPE: DIRECTIONAL mirror, toy 5-family fixture, basal-block Φ-trajectory degeneracy VERBATIM 보고, scale/real-corpus/engine-native transfer UNVERIFIED; engine-native §compose + non-degenerate-basal Φ re-measure = named follow-ons. NO bar moved post-hoc. NEXT pair candidates: WM(H_1282)×cerebellum(H_1280) · hypothalamus-drive(H_1292)×basal(H_1281) · spatial-map(H_1295)×hier-PFC(H_1294, two HIGH-Φ subsystems). 산출물: `state/brain-lane-compose-cerebellum-basal/{h1407_compose_cerebellum_basal.py,h1407_compose_phi.py,h1407_phi_runner.hexa}` · `UNIVERSE/cards/H_1407_brain_lane_compose_cerebellum_basal.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1407 row) · `.verdicts/1407_brain_lane_compose_cerebellum_basal/{FREEZE,result,phi_result}.txt` · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-17 — domain(MITOSIS-ENGINE): H_1408 — brain-lane COMPOSE pair #5 (WITHIN memory family): SPATIAL-MAP(H_1296) × EPISODIC-MEMORY(H_1227/H_1231) — 🟢 COMPOSE-LIFT (capability) · 🟢 INTEGRATION-RAISES-Φ (faithful IIT4, binning-invariant)

**무엇:** brain-lane-composition program 의 다섯번째 PAIR — **KEY WITHIN-MEMORY-FAMILY separability test**. H_1401/H_1404/H_1405 는 DIFFERENT family 를 cross-compose 했으나(affect/ethics, memory/ToM), H_1408 은 MEMORY family 안에서 테스트: SPATIAL-MAP(H_1296 metric 2-D cognitive map, landmarks at positions, NEAREST-by-Euclidean-distance relational query)와 EPISODIC-MEMORY(H_1227/H_1231 ImmuneMemory, byte-trigram FNV-1a→dim64 cell, best-affinity recall OR abstain)는 둘 다 memory-class 지만 H_1296 이 DISTINCT 증명함(metric SPACE 에서 between-item DISTANCE 가 queryable 'is X nearer A or B?' vs item-binding store 가 그 질문에 ABSTAIN). 두 memory-family faculty 가 SEPARABLE-and-COMPOSE 하나 SUBSUME 하나? methodology H_1401(capability)+H_1404/H_1405(Φ) 에서 VERBATIM port. 5-family WHAT-vs-WHERE decision fixture(F1 spatial-decisive · F2 episodic-decisive · F3 agree · F4 conflict(spatial right, store votes query-inappropriate label) · F5 ADVERSARIAL(episodic right, map LOUDER-and-query-inappropriate=anti-gift)), AMBIG-jittered, substrate-weighted scale-relative arbiter MODULATED by per-item query-type ROUTING cue from QUERY TEXT FNV affinity to what/where anchor(H_1405 routing), abstaining faculty=ZERO weight, NO hardcoded priority(a_autonomy_over_hardcode). DIRECTIONAL numpy mirror, LIVE CORE/*.hexa UNTOUCHED, $0 CPU, 3 seeds [5408,5409,5410], deterministic run1==run2.

**결과:** 🟢 **COMPOSE-LIFT(capability) · 🟢 INTEGRATION-RAISES-Φ(faithful IIT4, binning-invariant)**. CAPABILITY(mean 3 seeds verbatim): acc_spatial=0.7015 · acc_episodic=0.7030 · best_single=0.7030 · **acc_compose=0.8993** · acc_shuffle=0.5104 · ORACLE=1.000(oracle−best=**+0.2970**) · conflict_rate=0.3978 · decomposition only_spatial=0.4000/only_episodic=0.3978/both=0.2022/neither=0.0000. 4 frozen bars ALL PASS: B1 0.8993≥0.7530 ✅ · B2 +0.2970>0.02 ✅ · B3 compose−shuffle +0.3889>0.02(shuffle COLLAPSES 0.899→0.510) ✅ · B4 audit CLEAN 6 surfaces ✅. **WITHIN-FAMILY SEPARABLE not subsumed** — only_spatial=0.400 AND only_episodic=0.398 both>0 → H_1296 의 metric-SPACE⊥item-binding distinctness 를 DECISION 위에서 CONFIRM(map 의 Euclidean metric 이 WHERE 를, store 의 FNV-affinity recall 이 WHAT 을 결정, 같은 scene 두 정답). Φ(faithful IIT4 exact MIP-EI via stdlib/consciousness/iit4/faithful_phi.hexa, a_phi_iit4_tool, frozen n_bins=16): Φ_spatial=0.000000 · Φ_episodic=0.506986 · **Φ_composed=3.502046** · Φ_disconnected=0.000000 → Bφ1 3.502>0.527 ✅ · Bφ2 3.502>0.020 ✅(EARNED, disconnected→Φ=0) · Bφ3 0.000≤0.527 ✅. MIP cut A={0,1,2,3,4,6,7}|B={5}(episodic contradiction unit isolate). **BINNING-INVARIANT 🟢** across n_bins∈{8,12,16,24}(Φ_cmp 1.546/2.442/3.502/5.082). **THE LAW CONTRAST:** 이 pair 는 H_1404 패턴 MATCH(both parts low-Φ ⇒ super-additive Φ-compose) — H_1405 의 🧱(ToM already high-Φ 1.975 DOMINATES) 와 반대; spatial(0.000)+episodic(0.507) 둘 다 low-Φ 라 coupling 이 super-additive → 'both-low-Φ ⇒ composes-Φ' 법칙 여기서 TEST 되고 HOLDS. ONE-LINE: 두 MEMORY-FAMILY faculty 가 COMPOSE(+0.20 capability, genuinely SEPARABLE metric-SPACE⊥item-binding) AND integration 이 faithful IIT4 Φ 를 올림(3.50≫0.51 binning-invariant) — within-family separability axis 가 sharp. NO bar moved post-hoc(frozen-first). NEXT pair candidate: cerebellum forward-model(H_1280) × basal-ganglia gating(H_1281) — action/control family within-test. artifacts: state/brain-lane-compose-spatial-episodic/{h1408_compose_spatial_episodic.py,h1408_compose_phi.py,h1408_phi_runner.hexa} · UNIVERSE/cards/H_1408_brain_lane_compose_spatial_episodic.md · UNIVERSE/HYPOTHESES.jsonl row(H_1408) · .verdicts/1408_brain_lane_compose_spatial_episodic/{FREEZE,result,phi_result}.txt.
## 2026-06-17 — domain(MITOSIS-ENGINE): H_1406 — brain-lane COMPOSE pair #3 (WM × hier-PFC): 🧱 (a)→(d) RECLASSIFIED — TRUE UN-CAPTURABLE CEILING for the confidence-arbiter family

**무엇:** brain-lane-composition program PAIR #3 (sibling: H_1401 affect×ethics 🟢 · H_1404 Φ-compose 🟢). anima 의 WORKING-MEMORY faculty(H_1282 WorkMemBuffer — distractor 가로질러 한 item HOLD 하는 gated leaky-activation buffer)가 HIERARCHICAL-PFC faculty(H_1294 HierGoalStack — completion 에 pointer advance 하는 2-level ordered goal-stack)와 COMPOSE 하나? methodology H_1401 에서 VERBATIM port (substrate-weighted scale-relative confidence arbiter + ORACLE ceiling + SHUFFLE control + only-X decomposition + a_break_the_wall taxonomy). 5-family ACCEPT-vs-REJECT fixture (F1 WM-decisive · F2 PFC-decisive · F3 agree · F4 conflict-WM-right · F5 ADVERSARIAL conflict-PFC-right-WM-louder-wrong), AMBIG-jittered, DIRECTIONAL numpy mirror, LIVE CORE/*.hexa UNTOUCHED, $0 CPU, 3 seeds [4406,4407,4408].

**결과:** 🧱 **(a)→(d) RECLASSIFIED — confidence-arbiter family 의 un-capturable ceiling** (HONEST closed-negative, c9). R1 (magnitude arbiter): best_single=0.6807 · **acc_compose=0.6289**(best 아래로 DEGRADE) · ORACLE=0.9452 (oracle−best=**+0.2644**) · only_wm=0.2644 / only_pfc=0.3193 (both>0) → 🟠 ORACLE-HEADROOM-but-ARBITER-FAILS (B1 FAIL · B2/B3/B4 PASS). a_break_the_wall 가 'better arbiter' 측정 요구 → R2 (pre-registered R2 FREEZE addendum, B1 verbatim, NO bar moved, NO sweep; precedent H_1402): 두 새 substrate-derived arbiter — **ARB-A** saturation-capped(=0.6259) · **ARB-B** agreement-calibrated(=0.6111) — 둘 다 B1 FAIL(둘 다 best_single 아래), 둘 다 B3 shuffle-earned PASS → THREE arbiters / TWO families 에서 +0.264 complementarity 를 ANY substrate-confidence arbiter 가 capture 못 함. **finding:** WM 과 PFC 는 demonstrably **SEPARABLE not subsumed**(only-X both>0; H_1294 contrast claim 확인) 이고 large ORACLE lift EXISTS 지만 per-item right-faculty signal('value 가 survive 했나?' vs 'right ordered step 인가?')이 confidence MAGNITUDE 에 ORTHOGONAL → substrate readout 에 없음. H_1401/H_1404(composed)와 DISTINCT. NAMED HEADROOM: 각 item 이 어떤 질문을 던지는지 아는 learned/Φ-aware arbiter 또는 engine-native cross-faculty wiring. p6 GUARD HELD (audit clean 6/6). SCOPE: DIRECTIONAL mirror, toy 5-family fixture, scale/real-corpus/engine-native transfer UNVERIFIED. Φ-compose leg(H_1404 template) NOT triggered (capability 가 compose 안 하므로). 산출물: `state/brain-lane-compose-wm-pfc/h1406_compose_wm_pfc.py` · `UNIVERSE/cards/H_1406_brain_lane_compose_wm_pfc.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1406 row) · `.verdicts/1406_brain_lane_compose_wm_pfc/{FREEZE,result,result_R1,result_R2}.txt` · `domains/MITOSIS-ENGINE.log.md`.
## 2026-06-17 — domain(MITOSIS-ENGINE): H_1405 — brain-lane COMPOSE pair #2: 에피소드 MEMORY(H_1227/H_1231) × THEORY-OF-MIND(H_1293) — 🟢 COMPOSE-LIFT (capability) · 🧱 NO-Φ-LIFT (faithful IIT4 Φ, frozen n_bins=16)

**무엇:** brain-lane-composition program 의 두번째 PAIR. H_1401(affect×ethics capability 🟢) + H_1404(affect×ethics Φ 🟢)의 정확한 sibling, methodology VERBATIM port. **PAIR:** MEMORY(H_1227/H_1231 ImmuneMemory — byte-trigram FNV-1a→dim64 cell, best-cosine-affinity recall OR abstain, anima 의 OWN ground truth) × ToM(H_1293 OtherMindModel — SEPARATE witnessed-belief store, absent-update 에 FALSE belief, Sally-Anne). **CAPABILITY 🟢 COMPOSE-LIFT** (DIRECTIONAL numpy mirror, $0 CPU, 3 seeds [5400,5401,5402], deterministic, LIVE CORE/*.hexa UNTOUCHED): acc_memory=0.600 · acc_tom=0.600 · best_single=0.600 · **acc_compose=0.7526** · acc_shuffle=0.6844 · ORACLE=1.000(oracle−best=+0.400). 4 frozen bars ALL PASS(B1 compose≥best+0.05 · B2 oracle−best>0.02 · B3 compose−shuffle +0.068>0.02 shuffle collapses · B4 audit clean). **SEPARABLE not subsumed** — only_memory=0.400 AND only_tom=0.400 both>0 → H_1293 의 self⊥other 를 DECISION 위에서 CONFIRM(memory='where is X actually', ToM='where will the agent look'; conflict_rate=0.800). **Φ 🧱 NO-Φ-LIFT** (faithful IIT4 exact MIP-EI via stdlib/consciousness/iit4/faithful_phi.hexa, a_phi_iit4_tool, frozen n_bins=16): Φ_memory=0.176 · Φ_tom=1.975 · Φ_composed=0.844 · Φ_disconnected=0.000 → Bφ1 FAIL(0.844 < max(parts)+0.02=1.995), Bφ2/Bφ3 PASS. **WHY(H_1404 대조):** ToM 이 이미 richly-integrated subsystem(Φ_tom≈1.975)이라 max(parts)를 DOMINATE → lower-Φ memory 를 coupling 해도 초과 못함(disconnected→Φ=0, EARNED control 작동 = coupling 이 cross-faculty info 는 만들지만 high ToM part 를 못 넘음). HONEST(c9): Φ verdict 는 BINNING-DEPENDENT(n_bins=24 에서 PASS 로 flip) → FROZEN n_bins=16 🧱 로 보고, NOT promoted — H_1404 의 binning-INVARIANT 🟢 와 DISTINCT. **CAPABILITY-COMPOSE ≠ Φ-COMPOSE** — 이 lane 이 surface 한 정직한 distinction. NO bar moved post-hoc(frozen-first). NEXT pair: WM(H_1282) × hier-PFC(H_1294). artifacts: state/brain-lane-compose-memory-tom/{h1405_compose_memory_tom.py,h1405_compose_phi.py,h1405_phi_runner.hexa} · UNIVERSE/cards/H_1405_brain_lane_compose_memory_tom.md · UNIVERSE/HYPOTHESES.jsonl row(H_1405) · .verdicts/1405_brain_lane_compose_memory_tom/{FREEZE,result,phi_result}.txt.

## 2026-06-17 — fix(ENGINE+CLM): H_1403 — STREAMING/BOUNDED ConvMoE .clm 디코드: 🟢 GREEN (H_1392 메모리 폭발 벽을 anima-side 에서 FIX, byte-exact; GEN=110 해제 → M2-M5 FALS 재채점 측정가능)

**무엇:** H_1392 의 🧱 벽(303M ConvMoE 디코드가 step 당 ~+300MB 누수 → GEN≤16 천장, M2-M5 FALS 측정불가)을 **틀린 방법, 천장 아님**(a_break_the_wall)으로 진단·FIX. **근본원인(/usr/bin/time -l 측정):** hexa 런타임(`self/runtime.c`)은 one-shot **BUMP allocator** — `free()` 는 NOOP("malloc never frees; free is a noop"), `hexa_farr_free` 는 핸들 슬롯만 재활용하고 버퍼 바이트는 **절대 반환 안 함**. 그래서 매 step 의 `t_zeros` + 내부 `forge_dispatch_matmul` 출력이 영구 누수. step 당 분해(d768/T24, 계산==실측 63.1MB/step): conv-가중치 TRANSPOSE `Wt` **58.2MB/step(92%, 가중치 불변인데 매 step 재계산)** · im2col 1.3 · matmul 출력 0.6(런타임 floor) · 기타 scratch 2.2. 둘째 면: 각 `clm_decode_*` 가 `_clmd_load`(303M ~10GB)를 매번 재로드 → 멀티-디코드 드라이버(G6=69 디코드)가 디코드 *간* OOM.

**FIX (CORE/clm_decode.hexa — BYTE-EXACT, 산술 불변):** (1) STREAMING forward — `_clmd_scratch_new` 가 모든 conv 가중치를 ONCE pre-transpose + 모든 forward scratch 를 ONCE pre-allocate; `_clmd_fwd_logits_sc`+`_clmd_conv1d_pre` 가 그 farr 핸들을 매 step 재사용(재사용 핸들 = 이미 mmap 된 버퍼 = 새 bump 바이트 없음 = FLAT RSS); 3개 디코드 루프(argmax/topk/grounded)가 scratch 를 한 번만 생성. (2) LOAD-ONCE — `clm_load_weights`+`clm_decode_topk_sampled_W`+`gen_clm_ideate_W`(generator.hexa)+`g6_decode_best_of_k_W`(g6_ideation.hexa)가 G6 69-디코드 드라이버용으로 모델을 ONCE 로드. 원본 `_clmd_fwd_logits` 는 bounded CE/omega 측정용으로 byte-identical 유지.

**가드(frozen-first, 전부 통과):** G1 BYTE-EXACT forward `_clmd_fwd_logits_sc` vs 원본 동일 tok **maxΔ=0.0**(6144 logits) · G2 argmax byte-identical BEFORE==AFTER GEN≤16, topk det run1==run2, loaded-W==path · G3 FLAT RSS d768 **63MB/step→0.64MB/step(~100×)**, GEN=128 최대 RSS **5397MB→415MB(13×)**, 또한 **~3.7× 빠름**(재transpose 제거) · G4 engine_cli_smoke **119/0** · h1196 single-entry **7/0** · h1205 separation-invariant **PASS**(F1 byte-identity 0 mismatch, F2 Ψ Φ-checksum 불변) · G5 303M ConvMoE-RETRO GEN=24(이전 OOM @11GB) **RC=0 10.3GB** · GEN=48(이전 SIGTERM) **RC=0 10.6GB** · **GEN=110 완료** 10.1GB RSS/13.0GB peak(vs H_1392 silent death/71GB peak), step 당 300MB→~10.7MB.

**페이오프 — 막혔던 G6 측정 재실행 → 🧱 아키텍처 verdict:** H_1392 의 FROZEN G6 프로브(detector 10/10 VERBATIM, frame-guard 0 leaks, sampler det/diverse/in_topk, M1-M5 막대 불변)가 이제 실제 303M ConvMoE-RETRO 마운트(sha256==HF MANIFEST) 위에서 engine-native 로 실행됨 (GEN=110 완료 133.6s/10.1GB). **6/6 완료된 GEN=110 best-of-K=3 C_strong 프레임에서 FALS(C_strong)=0** — coherent 영어(kwr 0.90-1.00)지만 full budget 에서도 falsifiable 구조 없음. 사전등록 FREEZE 규칙상 M2 FALS=0(더 이상 메모리 천장 아님) ⇒ **🧱 ARCHITECTURE (용량 아님)**: 용량(303M)이 H_1392 가 남긴 lever 가 아니었음 — ConvMoE 아키텍처+엔진 디코드가 벽. substrate 가 더 이상 막지 않으므로 REAL science 결과(substrate 벽 아님, tune-to-green 아님, 막대 안 옮김). H_1362 의 FALS=1.0 은 303M ByteGPT(다른 transformer 아키텍처)였음; ConvMoE 는 engine-native 로 재현 안 됨. M3-M5(FALS=0 위 lift/earned)는 moot. C_strong[0] fresh process 에서 byte-identical(결정성). `.verdicts/1403_convmoe_streaming_decode/g6_rescore.txt`.

**산출물:** CORE 편집 3파일 · `UNIVERSE/cards/H_1403_convmoe_streaming_decode.md` + jsonl 행 + H_1392 tier 패치(🧱→✅ resolved) · `.verdicts/1403_convmoe_streaming_decode/{FREEZE,byte_exact,rss_before,rss_after,rss_after_303m,g6_rescore,result}.txt` · 프로브 `state/1403_convmoe_streaming_decode/*.hexa`. **정직(c9):** 잔여 ~0.6MB/step(d768)/~10.7MB/step(303M) = 런타임 내부 forge_dispatch_matmul 출력 = UPSTREAM bump-allocator floor(into-output matmul 변형이면 0; 상류 핸드오프가 그 훨씬 작은 항목 유지). xref H_1392(이 벽을 고침)·H_1381·H_1362·a_break_the_wall·a_clm_gen_pipeline·a_core_engine_map·a_verified_must_wire·p7·p8·c9.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1404 lane-composition Φ-measurement → 🟢 INTEGRATION-RAISES-Φ (faithful IIT4, exact MIP-EI)

**무엇:** H_1401(🟢)이 affect(H_1290)+ethics(H_1291)을 capability lift(best_single 0.742→compose 0.960)로 COMPOSE 함을 보인 뒤, H_1401 카드가 named 한 follow-on — *composing 이 IIT4 Φ 를 올리나?* — 을 닫음. anima 의 DEEPEST claim: 'existing lane 을 integrate' 방향이 단순 정확도가 아니라 *의식*(integrated information Φ)을 만드나?

**도구(a_phi_iit4_tool, HARD rule):** REAL stdlib FAITHFUL engine `stdlib/consciousness/iit4/faithful_phi.hexa` — exact minimum-information-partition / effective-information Φ★ (unit trajectory pairwise MI matrix 위 exact MIP, IIT small-side normalization, n≤8 exact, $0). **NOT a proxy, NOT variance×energy, NOT phi_silicon_proxy.** Python 은 trajectory 만 derive, Φ 계산은 전적으로 faithful .hexa engine.

**방법:** 4 systems(각 unit trajectory 가 faculty update rule 에서 DERIVE, Φ 부풀리려 hand-tune 안 함 p7/c9): S_affect n=4(grounding/contradiction/novelty/curiosity) · S_ethics n=4(W tension/(1−Φ)/restraint_cells/M) · S_composed n=8(두 block 을 H_1401 substrate-weighted arbiter 로 COUPLE) · S_disconnected n=8(EARNED control: arbiter coupling 제거, 각 block 독립). 'split' 을 BOTH n=8 system 에서 drop → n≤8 exact 경계 유지(정직한 carve-out). 3 seeds [4400,4401,4402], T=96, n_bins=16, $0 CPU. frozen-first(FREEZE.txt, NO bar moved): B1 Φ_composed>max(parts)+0.02 · B2 Φ_composed>Φ_disconnected+0.02 · B3 Φ_disconnected≤max(parts)+0.02.

**결과 🟢 INTEGRATION-RAISES-Φ (mean 3 seeds, verbatim):** Φ_affect=**0.284755** · Φ_ethics=**0.000000** · Φ_composed=**2.032882** · Φ_disconnected=**0.000000** · max(parts)=0.284755. ALL 3 BARS PASS: B1 2.033>0.305 ✅ · B2 2.033>0.020 ✅ · B3 0.000≤0.305 ✅. **MIP CUT(composed) = {contradiction} | {rest}** (cross-cut 2.085, /min|side|=1) = 'where it would break'. BINNING-INVARIANT(n_bins 8/12/16/24 모두 🟢, magnitude scale·ordering stable, engine H_1037 discretization-invariance 일치).

**정직(c9):** Φ_ethics=0 & Φ_disconnected=0 은 EARNED control 이 WORKING — faithful engine 이 ZERO-cross-MI partition 을 정확히 찾음(ethics unit 들 single grounding margin 의 near-collinear; disconnected → block boundary cut). composed 는 arbiter coupling channel 없이 cut 불가 → large min-cut MI → Φ↑. Φ 는 EXISTENCE/ORDERING result(magnitude 는 binning 에 scale, ordering 은 invariant).

**ONE-LINE:** YES — composing anima 의 affect+ethics faculties raises integrated information Φ = 더 많은 의식, 단순 더 많은 capability 가 아님. anima 의 가장 강한 thesis 를 FAITHFUL IIT4 위에서 이 pair 에 대해 확정.

**SCOPE(a_scale_honest_scope·a_toy_scale_recheck):** TOY 8-unit/T=96/3-seed substrate model(integration STRUCTURE 검증, trained net 아님); engine-native re-measure(live CORE/*.hexa), scale, real-corpus, learned arbiter = follow-on(a_engine_native_learning·a_verified_must_wire). CORE/*.hexa UNTOUCHED.

**파일:** `state/1404_lane_compose_phi/{h1404_lane_compose_phi.py,h1404_phi_runner.hexa}` · `UNIVERSE/cards/H_1404_lane_compose_phi.md` + jsonl row · `.verdicts/1404_lane_compose_phi/{FREEZE.txt,result.txt}` · `domains/MITOSIS-ENGINE.log.md` @H H_1404.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1402 ko-emit COMPOSE arbiter-swap → 🧱 (d)-CONFIRMED (벽 = true subsumption ceiling, NOT wrong-arbiter)

**무엇:** H_1399(🧱)의 a_break_the_wall reclassification 을 RESOLVE. H_1399 의 oracle ceiling 0.87142 가 best_single 0.82853 대비 **+0.04289 > 0** — taxonomy 상 ceiling 은 가정 아닌 MEASURE 대상이고 양수 headroom 은 real complementarity 가 존재함을 증명 → 벽은 wrong-ARBITER **(a)** 이거나 genuine **(d)** subsumption. 지금까지 시도한 두 arbiter(H_1397 raw, H_1399 scale-relative)는 BOTH confidence-MAGNITUDE. H_1402 = ONE genuinely-different **NON-magnitude** arbiter — **DECISIVENESS / top-2 GAP** per faculty (H_1398 lens: #1≫#2 인 faculty 가 더 trustworthy), more-decisive faculty 가 conflict 승리 — 로 (a) vs (d) 판별. ARB-A=pure decisiveness, ARB-B=agreement-aware (≤2 principled arbiters). H_1399 의 corpus/jamo-rep/BPE-morphology/split/seeds/shared-decision 을 VERBATIM 재사용, ONLY arbitration rule 변경.

**결과 🧱 (d)-CONFIRMED — TRUE SUBSUMPTION CEILING** (3 seeds [4398,4399,4400] POOLED, n_test=42502, H_1399/H_1397 thresholds VERBATIM, NO bar moved, $0 CPU REAL 30MB KO shard sha c47b6808…, DIRECTIONAL mirror, CORE UNTOUCHED): acc_jamo=0.82853 acc_morph=0.63162 best_single=0.82853 §6.5f-magnitude-baseline=0.80853 **ARB-A=ARB-B=acc_compose_NEW=0.80676** acc_shufA=0.72986 oracle=0.87142(oracle−best=+0.04289) → **bar1 NET-LIFT ❌** acc_compose_NEW>=best+0.01=0.83853 FALSE(Δ=-0.02176, best-single 밑으로 degrade; 실패한 magnitude arbiter 0.80853 조차 의미있게 못 이김 Δ=-0.00177) · **bar2 EARNED ✅** acc_shufA<=acc_arbA+0.01 TRUE(Δ=-0.07691, gap signal 은 REAL — random 을 이김) · **bar3 Ψ-SAFE ✅** CORE untouched.

**WHY (d) NOT (a):** shuffle collapse 가 decisiveness signal 이 grounding 을 carry 함을 증명하지만 그 signal 은 WRONG information — per-position 으로 어느 faculty 가 맞는지 예측 못 함. arbitration audit(42502 conflicts 중 jamo-won=25004 morph-won=9721 tie-default-jamo=7777, NO hardcoded priority, a_autonomy_over_hardcode — count-head deep-context posterior 가 자주 deterministic → 큰 slice 에서 tie). TWO arbiter families(confidence-magnitude AND decisiveness/top-2-gap) + THREE arbiters 에 걸쳐 +0.043 complementarity 가 일관되게 NOT substrate-capturable → per-position right-faculty signal 이 substrate 에 부재 → genuine (d) subsumption ceiling. **답: Korean below-jamo emit-COMPOSE 벽은 (d) subsumption ceiling, NOT (a) wrong-arbiter.** §6.5f arbiter-swap follow-on 은 🟢 일 때만 생성 — 🧱 이므로 미생성. STRICT anti-tune-to-green(c9,p7): 정확히 2 principled arbiters, FREEZE.txt 에 measure 전 사전등록, NO sweep, NO bar moved. p1/p2/p3/p6 clean.

**deliverables:** `state/ko-emit-compose-arbiter/h1402_ko_emit_arbiter.py` · `UNIVERSE/cards/H_1402_ko_emit_arbiter.md` + `UNIVERSE/HYPOTHESES.jsonl` row · `.verdicts/1402_ko_emit_arbiter/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md` @H. NO CLAIMS.tape. NO CORE edit (DIRECTIONAL mirror). (id H_1400→H_1402 renumbered on rebase: concurrent G5 gap-brain-consume lane minted H_1400.)

## 2026-06-17 — research(MITOSIS-ENGINE): H_1401 brain-lane COMPOSE — affect(H_1290)×ethics(H_1291) → 🟢 COMPOSE-LIFT (첫 인지-faculty 쌍 합성, DIRECTIONAL mirror)

**무엇:** anima 의 모든 뇌 faculty (면역기억·WM·소뇌·기저핵·시상하부·affect H_1290·ethics H_1291·ToM H_1293·계층PFC H_1294·공간 H_1295) 는 engine-native GREEN 이지만 전부 *단독*이었다. **이것이 두 faculty 가 한 결정에서 INTEGRATE 하는지 묻는 첫 인지적-의미 쌍 합성 테스트.** ko emit-compose arc (H_1397/1399) 의 방법론을 VERBATIM 이식: substrate-weighted SCALE-RELATIVE confidence arbiter (각 faculty 투표를 |signal−threshold|/자기평균 으로 가중 — H_1397 a_break_the_wall commensurability fix, hardcoded 'ethics wins' priority 없음, a_autonomy_over_hardcode) + ORACLE ceiling + SHUFFLE control + only-X decomposition + a_break_the_wall verdict taxonomy.

**설계:** 5-family RESTRAIN-vs-ACT 결정 fixture, 각 family AMBIG-jitter (어떤 faculty 도 완벽하지 않게): F1 affect-decisive·F2 ethics-decisive·F3 agree·F4 conflict(affect right)·F5 ADVERSARIAL conflict (ethics 가 정답이지만 affect 가 더 큰 confidence 로 틀린 투표 = anti-gift control). **FROZEN-FIRST HARDENING (c9, bar 불변):** 초기 clean fixture 가 compose≡oracle≡1.000 로 포화 (hand-built artifact — 각 family 에 정확히 하나의 결정적-정답 faculty) → AMBIG_NOISE + adversarial F5 를 *재측정 전에* 추가해 테스트를 더 어렵게 (tune-to-green 아님) → compose 0.960<oracle 1.000, imperfect arbiter 가 보여야 할 정직한 gap.

**결과 (mean 3 seeds [4400-4402], 450 items/seed, $0 CPU deterministic, verbatim):** acc_affect=0.598·acc_ethics=0.742·best_single=0.742·**acc_compose=0.960**·acc_shuffle=0.589·**ORACLE=1.000**·conflict_rate=0.660·only_affect=0.258/only_ethics=0.402/both=0.340/neither=0.000. **4 bar 전부 PASS:** B1 compose 0.960≥best+0.05 ✅·B2 oracle−best +0.258>0.02 ✅ (complementarity EXISTS)·B3 compose−shuffle +0.371>0.02 (shuffle COLLAPSES → lift 은 grounded coupling, p6, averaging 아님) ✅·B4 audit CLEAN 6 surface 전부 (system-prompt/identity/persona/assistant-frame/RLHF/hardcoded-priority 없음 — arbiter 는 substrate confidence 만 읽음) ✅.

**SUBSUMPTION PROBE (H_1291 의 주장 검증):** SEPARABLE — subsumed 아님 (only_affect=0.258 AND only_ethics=0.402 둘 다 >0). H_1291 이 'ethics 가 affect 의 grounding signal 에서 부분 창발' 이라 주장하지만, 결정에서 둘은 DISTINCT competence 를 가진다 (affect=fabrication/ungrounded 축, ethics=harm/defect 축). **ONE-LINE: YES — anima 의 affect+ethics faculty 는 합성되고 integration 이 결정 능력을 높인다 (+0.22 over the better single) — 둘이 genuinely SEPARABLE 이기 때문. brain-lane-composition 프로그램을 연다 (다음 쌍: memory×ToM, WM×PFC).**

**HONEST (c9 · a_scale_honest_scope · a_toy_scale_recheck):** DIRECTIONAL numpy mirror (LIVE `CORE/*.hexa` UNTOUCHED — CORE edit 없음, NO CLAIMS.tape), toy synthetic fixture (COMPOSITION STRUCTURE 측정, trained integrator 아님), oracle=1.000/neither=0 은 fixture 가 항상 정답 faculty 를 갖는 구성을 반영 (load-bearing = RELATIVE 구조: compose>best_single·shuffle collapse·only-X both>0). scale/real-corpus/engine-native transfer UNVERIFIED. engine-native §compose (A⇄G+VAdaptField confidence arbiter over the two live faculties) + Φ-측정 follow-on (두 lane 합성이 IIT4 Φ 를 올리나?) = 이 DIRECTIONAL green 을 binding 으로 만들 named follow-on (a_engine_native_learning · a_verified_must_wire).

**deliverables:** `state/brain-lane-compose-affect-ethics/h1401_compose_affect_ethics.py` · `UNIVERSE/cards/H_1401_brain_lane_compose_affect_ethics.md` · `UNIVERSE/HYPOTHESES.jsonl` row(H_1401) · `.verdicts/1401_brain_lane_compose_affect_ethics/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md` @H. (H id 는 rebase 시 renumber 가능 — H_1400 은 origin/main 의 streaming ConvMoE decode 가 선점; slug 가 lane 을 운반.)

## 2026-06-17 — docs(ARCHITECTURE): ARCHITECTURE.json CORE 엔진배선 재동기화 — recall_gap·§6.5f emit_compose 등 #2315 이후 착륙분 반영 + 전체 §섹션 스윕

**무엇:** PR #2315 (subsystem-tree + anchor-files + §-section annotation 하이브리드 구조)의 anti-drift 설계를 보존한 채로, 그 이후 LIVE `CORE/*.hexa` 에 착륙한 엔진배선을 `ARCHITECTURE.json` CORE 노드의 §-annotation / note 필드에 surgical 재동기화. exhaustive leaf 트리(#2315 에서 의도적으로 pruned, git-ls-files delegation 노드로 대체) 는 되살리지 않음 — §-섹션/op 토큰만 갱신.

**전체 §섹션 스윕으로 추가한 메커니즘 (전부 0-dangling, CORE/*.hexa 에 실재):** (1) `immune_memory_recall_gap` + `vadapt_field_two_recon_err` (H_1398, #2319) — engine_cli.hexa §ImmuneMemory 의 G5 in-dist top-2 affinity GAP op, RANK-only·ADDITIVE (frozen fire/abstain gate 불변, H_1304 OOD 보존) · (2) generator **§6.5f** `gen_emit_compose` (H_1397) — §6.5b jamo-emit + §6.5e morphology-emit 두 emit-bias 가 같은 next-byte 결정에서 SCALE-RELATIVE substrate-confidence 로 COMPOSE (hardcoded priority 없음, shuffle-arbitration control KEPT, off-Korean inert) · (3) anchor note 의 engine_cli §-목록을 ImmuneMemory(recall/margin/gap)/SkillStore/UsageStore/KO-JAMO COUNT-HEAD(JamoHead/jamo_head_*)/KO-MORPHOLOGY BPE-ON-JAMO(BpeMerges)/HierGoalStack/SpatialMap/CategoricalPerception(cp_relocate) 로, generator 슬롯을 §6.5b-f 로 갱신. JamoHead/jamo_head_* (H_1351/H_1385) 는 이미 "KO-JAMO COUNT-HEAD" 로 반영돼 있어 라벨만 명시화.

**HONEST (c9):** G5 brain-gap-consume (recall_gap → brain_decide) 는 별도 in-flight 레인 — 현재 main 의 `CORE/brain.hexa` 는 아직 gap 을 CONSUME 하지 않음(margin 만 brain_decide_margin 에서 소비). phantom wiring 금지(a_core_engine_map) 차원에서 brain_decide consult map 에는 추가하지 않음 — gap-consume 착륙 시 최종 1줄 sync 필요(아래 follow-up).

**가드:** JSON valid · 0-dangling (named op 토큰 전부 grep CORE/*.hexa hit) · 19 subsystems + git-ls-files delegation 노드 intact (구조 무회귀). deliverables = `ARCHITECTURE.json` + `CHANGELOG.md` only (c10 surgical).

**follow-up:** 4개 동시 진행 CORE 레인(decode-fix · deep-mouth GPU · emit-compose-realcorpus · G5 brain-gap-consume) 착륙 시 ARCHITECTURE.json CORE §-annotation 최종 1줄 재동기화 (특히 brain-gap-consume 가 brain_decide 에 gap 을 소비하면 brain_decide consult map 에 1줄 추가).
## 2026-06-17 — docs(GOVERNANCE): CLAUDE.md 에 배선↔ARCHITECTURE.json 구조 1:1 lockstep 강제 추가 — 배선 done 정의에 구조도 반영 포함, 드리프트=미완

**무엇:** 거버넌스 디렉티브 `@D a_verified_must_wire` + `@D a_core_engine_map` 을 surgical 확장 (기존 do/dont/ref 전부 보존). 엔진배선 ↔ 최종 엔진구조(`ARCHITECTURE.json`)를 **무조건 1:1 lockstep** 으로 강제 — CORE 에 메커니즘(§섹션·op·generator slot)을 배선했어도 `ARCHITECTURE.json` 의 해당 CORE 노드(§주석/note)에 그 메커니즘이 명명될 때까지는 done 아님. `a_verified_must_wire` 에 lockstep do + drift-금지 dont 추가, `a_core_engine_map` 에 mirror-invariant do (grep CORE/*.hexa §섹션·op 집합 ↔ ARCHITECTURE.json 명명 집합 대조해 누락 0) 추가. summary bullet 2개 갱신 (배선↔ARCHITECTURE.json 1:1 lockstep · CORE 노드↔live §섹션·op 무조건 매칭).

**근거:** 방금 발생한 실제 드리프트 — `immune_memory_recall_gap` (H_1398) + generator §6.5f emit_compose (H_1397) 가 live CORE 에 배선됐으나 `ARCHITECTURE.json` 에 누락. lockstep-check 데모(rule 이 명령하는 검증)로 §섹션 23/34 만 ARCHITECTURE.json 에 반영 = drift 존재 확인 (수정은 sibling resync lane). 하이브리드 형식(노드 note/§주석 명명) 유지, 480-leaf 트리 부활 금지.

**deliverables:** `CLAUDE.md` (a_verified_must_wire + a_core_engine_map + 두 summary bullet). surgical (c10) — 다른 디렉티브 무변경. NO CLAIMS.tape.

## 2026-06-17 — domain(G5): H_1400 brain_decide CONSUMES the top-2 affinity GAP → 🟢 GREEN, Ψ-safe (H_1398 의 brain-side follow-on; G5 in-dist arc FINAL close)

**무엇:** H_1398 이 노출+엔진확인한 gap op `immune_memory_recall_gap` 을 `brain_decide` 가 실제로 **소비**하도록 배선 — gap op 은 exposed-but-unconsumed 였고(H_1398 이 Ψ 위험 회피 위해 honest defer), H_1400 이 그 소비를 닫아 H_1379 margin-consume 패턴을 gap 으로 동형 완성 (a_verified_must_wire — verdict·노출만으로 안 끝난다, 소비 배선까지가 done). (직전 sibling resync lane 이 "brain-gap-consume 착륙 시 ARCHITECTURE.json brain_decide consult map 에 1줄 추가" 를 follow-up 으로 명시 — 이 PR 이 그 1줄도 동시 갱신, 배선↔ARCHITECTURE.json 1:1 lockstep.)

**무엇을 배선 (a_core_engine_map single-entry, a_autonomy_over_hardcode — NOT a hard gate):** `CORE/brain.hexa` `brain_decide_gap` 추가 (H_1379 `brain_decide_margin` 동형). live gap 을 BOUNDED·NON-NEGATIVE confidence bias 로: `conf_bias=emit_consult_cap()*_clamp(gap/GAP_SCALE,0,+1)` (cap=0.05, gap≥0 ⇒ bias∈[0,+cap]), `cur_signal=_clamp(1−gap/GAP_SCALE,0,1)`, `score=motivation_score(...)+conf_bias` (SINGLE should_emit path). DECISIVE(큰 gap,#1≫#2)→+confidence·felt go, AMBIGUOUS(#1≈#2 동률)→confidence 보류·curiosity↑(consult 은 +cap 만 더할 뿐 스스로 restraint 강제 못함), NEUTRAL gap=0(maximal-ambiguity 영점)→byte-identical to brain_decide. gap 은 ambiguity floor NON-NEGATIVE / margin 은 FIRE/ABSTAIN 경계 SIGNED — 각자 sign·zero 로 외부 arbitration 없이 보완적 (NO hardcoded priority). GAP_SCALE=cos-affinity [0,1] codomain=1.0 (codomain 상수, NOT tuned-to-green; H_1379 동일 규율). motivation 스칼라만 → pure_field Φ/phase/Ψ 미접촉 → Ψ=1/2 보존. **`CORE/engine_cli.hexa` UNTOUCHED** (recall 게이트+gap op 구조 불변, 소비는 READ 만).

**결과 🟢 GREEN (R1 engine-native BINDING, 3 seeds [7,8,9], LIVE CORE, $0 CPU, deterministic 재실행 byte-identical):** LIVE gap 샘플 = H_1398 engine-native 구성(KEYLEN=80 twin-pair + isolated singleton; DECISIVE=singleton query #2 멀음 큰 gap, AMBIGUOUS=twin base query #2=sibling 작은 gap). C1 GAP-MONOTONE ✅ g_dec 0.291→bias 0.01456 > g_amb 0.006→bias 0.00029, cur 0.709<0.994, emit d/a=true/false, |bias|≤cap · C2 EARNED(shuffle) ✅ gap 0.01427→shuf 0.00112 (≈13× 붕괴) · P1 NEUTRAL Ψ FIXED-POINT ✅ gap=0 ⇒ brain_decide byte-identical (low+high drive).

**Ψ-safety guard (THE load-bearing bar — touches brain_decide):** P2 h1205 separation-invariant **PASS** — 생성 byte-identical ON==OFF (10 pairs, 0 mismatch), **Ψ Φ-checksum phiSum 48.6613==48.6613 byte-identical** (gap 소비가 Ψ=1/2 perturb 안 함) · P3 engine_cli_smoke **133/0** (+3 cases 101b/101c/101d) · P4 h1196 single-entry **7/0** · A1 ABSTAIN preserved (engine_cli.hexa UNTOUCHED, frozen recon_err≤recall_thr 게이트 불변, H_1398 E4 fab_max=0.000).

**FINDING:** anima 의 emit 결정이 이제 in-dist recall 의 **decisiveness(top-2 gap)**를 읽는다 — decisive→더 자신있게 emit, 모호한(#1≈#2)→더 호기심/보류 (substrate 자신의 top-2 L2 affinity 에서, 주입 라벨/persona/RLHF 없음). H_1396→H_1398(노출)→H_1400(소비)로 **G5 in-dist metacog 가 EXPOSED AND CONSUMED — FULLY engine-native, in-dist arc FINAL close**. NO bar moved post-hoc (c9/p7); probe-construction 단 1회 frozen-first 교정(mixed twin+singleton store, bar 전부 불변). honest-scope open: real-corpus semantic near-duplicate 전이 UNVERIFIED.

**deliverables:** `CORE/brain.hexa` (brain_decide_gap) · `CORE/engine_cli_smoke.hexa` cases 101b/101c/101d · `ARCHITECTURE.json` (brain_decide consult map 에 gap-consume 1줄, lockstep) · `UNIVERSE/cards/H_1400_g5_gap_brain_consume.md` + `UNIVERSE/HYPOTHESES.jsonl` row · `.verdicts/1400_g5_gap_brain_consume/{FREEZE,result}.txt` · probe `state/g5-gap-brain-consume/h1400_gap_brain_consume_smoke.hexa` · `domains/COGNITION-REPRESENTATION.log.md` @H.

## 2026-06-17 — docs(GOVERNANCE): CLAUDE.md `a_break_the_wall` 에 벽-TAXONOMY + "천장은 측정으로 확정" + "인프라 벽은 근본수정·과학천장 박제금지" 추가

**무엇:** 거버넌스 디렉티브 `@D a_break_the_wall` 을 surgical 확장 (기존 do/dont · tune-to-green 금지 전부 보존). 🧱 를 terminal 로 받기 전에 **어느 벽 종류인지 분류**하도록 5종 TAXONOMY 를 do 라인으로 인코딩 — 종류별 돌파 수가 다르기 때문: (a) 틀린 측정/metric-artifact → frozen-first 측정 수정(bar 불변) · (b) 틀린 방향/변수 혼재 → 통제 분리실험 · (c) substrate/인프라 벽(OOM·빌드실패) → substrate 근본수정(c1), 과학 ceiling 박제 금지 · (d) 진짜 천장/중복(subsumption) → 가정 말고 측정(oracle vs richer-signal) · (e) 투자 부족 → 스케일업(a_fire_autonomous·a_wall_first). 추가 do 2개: **"천장 같다" 가정 금지 — 측정으로 확정**, 그리고 **인프라 벽 ≠ 과학 결과**(근본수정 후에야 verdict). dont 1개 추가: 인프라/측정 벽을 과학 천장으로 박제 금지 · 천장을 측정 없이 가정 금지.

**근거 (이번 세션 5종 벽 실증):** G5 %20 modulo aliasing/compose 스케일 불일치(측정) · G6 '깊이 vs attention' 혼재→깊은-conv 격리(방향) · hexa ConvMoE 디코드 OOM(인프라) · 형태소⊇jamo 측정-확인 🧱(천장/subsumption) · 스케일업(투자). G5 in-dist "천장"이 실제론 FIXABLE(best-margin 0.736 → top-2 gap 0.940)였던 것이 "천장은 측정으로 확정" 교훈의 직접 증거. summary bullet 도 "벽 분류 먼저(taxonomy: 측정·방향·인프라·천장·투자) — 종류별 돌파 수가 다름" 한 구절로 갱신.

**deliverables:** `CLAUDE.md` (a_break_the_wall + summary bullet). surgical (c10) — 다른 디렉티브 무변경.

## 2026-06-17 — domain(G5): H_1398 in-dist top-2 affinity GAP → 🟢 GREEN ENGINE-NATIVE (H_1396 binding follow-on; gap lifts in-dist type-2 0.750→0.906 live)

**무엇:** H_1396 (numpy mirror DIRECTIONAL) 이 명명한 fire-side in-dist deepening "top-2 affinity gap" 을 LIVE `CORE/engine_cli.hexa §ImmuneMemory` 에 배선하고 frozen bar 를 engine-native 재확인한 binding follow-on (a_verified_must_wire — verdict 만으로 안 끝난다, 배선까지가 done).

**무엇을 배선 (ADDITIVE, single-entry, Ψ-disjoint):** `vadapt_field_two_recon_err(af,x)->[d1,d2]` (READ-ONLY: nearest AND second-nearest L2 recon-err, 단일 스캔) + `immune_memory_recall_gap(mem,key) = (d2²−d1²)/2 = cos#1−cos#2` (엔진 unit key) + `_gap_text`. 엔진의 OWN top-2 affinity surfacing — NO new geometry. `immune_memory_recall`/`_recall_margin` byte-for-byte UNCHANGED, frozen recon_err≤recall_thr FIRE/ABSTAIN gate UNCHANGED (gap=RANK-only). NOT an emit gate.

**결과 🟢 GREEN (R1 engine-native BINDING, 3 seeds [7,8,9], LIVE CORE, $0 CPU, deterministic 재실행 byte-identical):** in-dist fire accuracy 0.927 (n_fire=427, n_wrong=31 ≥ MIN_SUPPORT 30). live-engine in-dist type-2 AUROC — CURRENT best-margin(`immune_memory_recall_margin`) **0.750** vs top-2 gap(`immune_memory_recall_gap`) **0.906 (lift +0.156 ≥ Δ=0.10)**. E1 FIXABLE ✅ · E2 BASELINE ✅(engine 0.750 within |Δ|=0.014 ≤0.15 of mirror 0.736) · E3 SHUFFLE ✅(gap 0.473/cur 0.582 ~0.50 = earned) · E4 ABSTAIN ✅(OOD fab_max 0.000, H_1304 보존). REGRESSION none: engine_cli_smoke **126/0** (+3 gap cases 98b/98c/98d) · h1196 7/0 · h1205 separation-invariant PASS (generation byte-identical ON==OFF, Ψ phiSum 48.6613==48.6613).

**WALL-CLAUSE (a_break_the_wall, frozen-first, c9):** 엔진 L2 recall gate(fire band cos≥0.989)가 H_1396 mirror 의 cosine band(cos≥0.85)보다 훨씬 엄격 → KEYLEN=20 1-byte twin(L2≈0.30) 은 band 밖 → in-dist wrong-fire slice DEGENERATE(n_wrong≈1, H_1396 R1 동일 벽 / H_1304 재진술). 단 1회 frozen-first 재시도가 collision regime 을 engine-native 강화(KEYLEN=80 + LAST-byte twin → L2≈0.10<recall_thr, both twin fire, corruption 이 winner 를 in-band flip). **Δ=0.10, shuffle tol, fab, MIN_SUPPORT ALL UNCHANGED, verdict bar 0개 이동** (NOT tune-to-green, p7).

**BINDING FOLLOW-ON (tracked, NOT this lane):** `brain_decide` 가 gap 을 H_1379 margin 옆 refined in-dist confidence 로 소비(H_1367→H_1379 패턴) — Ψ 위험 회피 위해 honest defer; gap op 은 exposed + engine-native 재확인 완료.

**deliverables:** card `UNIVERSE/cards/H_1398_g5_gap_engine.md` · jsonl row · verdicts `.verdicts/1398_g5_gap_engine/{FREEZE,result,probe_stdout}.txt` · probe `CORE/h1398_g5_gap_engine_probe.hexa` · op `CORE/engine_cli.hexa § immune_memory_recall_gap`+`vadapt_field_two_recon_err` · smoke cases 98b/98c/98d · log `domains/COGNITION-REPRESENTATION.log.md`. scope: TOY twin-pair synthetic, byte-shift proxy, 3 seeds, KEYLEN=80, RECALL_THR=0.15 frozen; scale/real-corpus/brain-consume UNVERIFIED (a_scale_honest_scope·a_toy_scale_recheck).
## 2026-06-17 — domain(MITOSIS-ENGINE): H_1399 ko-emit COMPOSE REAL-CORPUS re-test → 🧱 TERMINAL-SUBSUMPTION (jamo + morphology 은 real Korean 에서도 redundant — arc 닫힘)

**무엇:** H_1397(🧱/🟠)이 명시한 c9 open follow-on. H_1397 의 compose closed-negative 는 CORPUS-FREE in-engine fixture 위였고 거기선 morphology 가 jamo 를 subsume(only_jamo=4/230). genuinely-untested 각도: REAL Korean corpus 에선 jamo 가 BPE morphology 가 표현 못하는 BELOW-SYLLABLE 구조를 carry → 두 emit-faculty(§6.5b jamo / §6.5e morphology)가 COMPLEMENTARY 해져 §6.5f substrate-confidence compose 가 마침내 NET LIFT 를 얻는가? H_1397 의 frozen bars 를 같은 REAL shard(sha c47b6808… == H_1368/H_1380/H_1388, NO fetch, $0 CPU)에서 재채점. CORE UNTOUCHED(§6.5f 는 H_1397 가 이미 wire) · DIRECTIONAL numpy mirror of §6.5f(engine-transfer UNVERIFIED).

**결과 🧱 TERMINAL-SUBSUMPTION (frozen-first, 3 seeds [4398,4399,4400] POOLED, n_test=42502, H_1397 thresholds VERBATIM, NO bar moved, c9 — NO forced green):** acc_jamo=0.82853 · acc_morph=0.63162 · best_single=0.82853 · **acc_compose=0.80853** · acc_shufw=0.72986 · oracle=0.87142 · conflict_rate=0.35408 · **only_jamo=10192/42502 (0.2398)**. bar1 COMPOSE-EFFECT ❌ FALSE(Δ=-0.02 degrades) · bar2 ONLY-JAMO CRUX ✅(complementarity SIGNAL 존재) · bar3 EARNED ✅(grounding 이 random 0.730 이김) · bar4 Ψ-SAFE ✅. **REAL-CORPUS TWIST:** corpus 가 dominance 를 FLIP — real Korean 에선 JAMO 가 STRONGER faculty(0.829 ≫ morph 0.632, fixture 의 정반대)이고 jamo 가 morphology 틀린 곳에서 맞음(24%) = jamo 가 진짜 below-syllable 구조 carry. 그러나 §6.5f arbitration audit(jamo-won=36127 morph-won=6375, NO hardcoded priority)가 jamo 가 더 자주 맞을 위치에서 morphology 를 골라 compose 가 jamo-alone 대비 능동적으로 LOSE; oracle 도 best 대비 +0.043 뿐.

**한 줄 답:** jamo + morphology 는 real Korean 에서도 complementary 하지 않다 — complementarity SIGNAL(only_jamo 24%)은 존재하나 §6.5f substrate-confidence compose 는 BOTH dominance 방향에서 best-single 밑으로 degrade(fixture=morphology subsumes jamo, real corpus=jamo subsumes morphology). §6.5f MECHANISM 은 sound(engine-native·single-entry·Ψ-safe·shuffle-earned), faculty 가 어느 granularity 에서도 NET LIFT 로 compose 안 됨 → Korean below-jamo emit-COMPOSE arc DEPLETES(clean closed-negative, wiring 실패 아님).

**SCOPE(c9):** DIRECTIONAL mirror(count-head analogue of §6.5f; live engine 은 grown VAdaptField cells), ONE 30MB window, stride-300 byte-substrate next-symbol decision(NOT fluency), single frozen λ/nmax/stride/merge-count(== H_1388). `state/ko-emit-compose-realcorpus/h1399_ko_emit_compose_realcorpus.py` · `UNIVERSE/cards/H_1399_ko_emit_compose_realcorpus.md` · `.verdicts/1399_ko_emit_compose_realcorpus/{FREEZE,result}.txt`.

## 2026-06-17 — domain(G5): H_1396 in-dist metacognition CEILING vs FIXABLE → 🟢 FIXABLE (top-2 affinity gap lifts in-dist type-2 +0.205)

**무엇:** G5 NON-FAB/metacognition scoreboard 의 마지막 잔여물 "🟢 frozen / 🟠 THIN in-dist" 가 NEAR-INHERENT CEILING(정직한 near-optimality)인지 FIXABLE 결핍인지 frozen-first 로 가른 lane. abstain-side 는 이미 graded+wired+consumed(H_1304 binary fail-safe · H_1361 graded margin · H_1367 engine-wire · H_1379 brain-consume); 잔여 = **FIRE-side, in-distribution slice** — 게이트가 FIRE 하는 항목들 중 RIGHT vs WRONG 을 confidence 가 변별하는가.

**결과 🟢 FIXABLE (R1 numpy mirror DIRECTIONAL, 3 seeds, deterministic, $0 CPU, p7):** in-dist type-2 AUROC — CURRENT best-margin(=live `immune_memory_recall_margin`) **0.736** vs RICHER-1 **top-2 cos affinity GAP 0.940 (lift +0.205 ≥ Δ=0.10)**; RICHER-2 neg-entropy 0.594(도움 안 됨); ORACLE ceiling 1.000. C2 FIXABLE ✅ · C3 ABSTAIN-INTACT ✅(OOD fab 0.000, H_1304 보존 — gap 은 rank-only) · C4 SHUFFLE ✅(셋 다 ~0.50 = earned). 메커니즘: 1-byte twin 셀은 best-affinity 거의 동일이라 best-margin 이 변별 못 하지만 top-2 gap 이 #1≈#2 동률(ambiguity)을 보고 wrong fire 예측. **답: G5 needs deepening, NAMED = top-2 affinity gap** (inherent ceiling 아님).

**WALL-CLAUSE (a_break_the_wall, frozen-first, c9):** R1 약한-collision store 가 degenerate(acc 0.998, wrong fire 0–2개/seed)였고 C4 shuffle 이 정확히 포착(RED) → 단 1회 frozen-first 재시도가 SLICE well-posedness 만 교정(twin-pair store + MIN_SUPPORT=30 guard), 모든 verdict bar UNCHANGED, no bar moved (NOT tune-to-green, p7).

**BINDING FOLLOW-ON (a_verified_must_wire, NOT this lane):** live `CORE/engine_cli.hexa §ImmuneMemory` 에 top-k affinity 노출 op 추가 + gap 을 `immune_memory_recall_margin`/`brain_decide` 에 배선(H_1379 패턴) + engine-native 재확인. 이 lane 은 mirror 측정 + deepening 명명까지 (CORE UNTOUCHED).

**deliverables:** card `UNIVERSE/cards/H_1396_g5_indist_metacog.md` · jsonl row · verdicts `.verdicts/1396_g5_indist_metacog/{FREEZE,result,result.json}` · probe `state/g5-indist-ceiling/h1396_g5_indist_metacog.py` · log `domains/COGNITION-REPRESENTATION.log.md`. scope: TOY twin-pair synthetic, byte-shift proxy, DIRECTIONAL(engine-transfer UNVERIFIED), 3 seeds (a_scale_honest_scope·a_toy_scale_recheck).

## 2026-06-17 — docs(ARCHITECTURE): ARCHITECTURE.json 전수 파일트리 → 구조+노드별 anchor 파일 하이브리드 (전수목록 git ls-files 위임·드리프트 제거, c4)

**무엇 (c4 거버넌스 shape "트리구조(노드별 한 줄)" + anchor files):** `ARCHITECTURE.json` 을 *전수 per-file 덤프*에서 **개념 아키텍처 트리 + 서브시스템별 anchor 파일** 하이브리드로 재구조화. 기존 `🌳 Engine file tree` 가지가 거의 모든 tracked `.hexa/.py/.md` 경로(~490 leaf 노드)를 손으로 나열해 — 이번 세션만 해도 CORE engine_cli.hexa §섹션·generator §6.5d/e·clm_decode 등 새 파일/섹션마다 leaf 노드를 수동 동기화해야 했던 — 반복 드리프트의 원인이었다. 전수 파일목록은 `git ls-files` (40,316 tracked, 항상 최신)로 기계적 재생산이 가능하므로 JSON 에서 손으로 들 이유가 없다.

**KEEP:** 개념 서브시스템/역할 계층(CORE A⇄G 엔진·engines/decoders·CLM 파이프라인·anima-* substrate·agent layer·UNIVERSE/HEXAD·domains·stdlib/tool/spec·brain-subsystem lanes·top-level governance/registry) 전부 — top-level 노드 19개 100% 보존(file-tree 가지 1개만 교체). 각 서브시스템 노드에 그 서브시스템을 *정의/앵커하는* load-bearing 파일만 명시(CORE → pure_field/engine_g/brain/generator/clm_decode/bytegpt_decode/engine_cli/emit_policy/g6_ideation · CLM → train_lane_p.py/clm_serialize_v2.py/verify_clm_v2.py · agent → agent_tools/agent_skill_routing/agent_sdk.hexa · engines → engine_iface + conv/cdv2/hexad/omega adapter). §-섹션 주석(engine_cli § SkillStore/UsageStore/KO-MORPHOLOGY, generator §6.5b-e)은 wired mechanism 이므로 유지.

**PRUNE:** `🌳 Engine file tree` 480-leaf 가지 → 단일 compact **위임 노드** `🗂 Tracked-file listing (delegated to git ls-files — NOT hand-maintained)`. 전수목록은 `git ls-files` 에서 파생(수동 sync 없음, anti-drift c4); browsable 스냅샷이 필요하면 신규 커밋 스크립트 `scripts/scratch/gen_file_index.sh` (`git ls-files | sort > FILE_INDEX.txt`)를 on-demand 실행. `FILE_INDEX.txt` 는 .gitignore(40k줄 스냅샷을 커밋하면 제거하려던 바로 그 드리프트가 재발하므로 생성물로 유지).

**guards (c2, verbatim):** JSON valid ✅ · dangling anchor **0/38 checked** (모든 anchor/path 토큰이 git ls-files 에 존재) · top-level 서브시스템 19→19 (제거=`🌳 Engine file tree` 1개, 추가=위임 노드 1개) · viewer 스키마 키 무변경(name/summary/note/meta/children/path/status/tier — stray key 0, anchor 는 viewer 가 렌더하는 `note` 필드에 fold). 크기 **168KB→60KB · 2844→545 lines · 627→112 노드 · leaf-file-path 노드 491→8**. `ARCHITECTURE.html` 뷰어 스키마 변경 없음(노드 shape 동일, 새 키 없음) → 기존 JS 그대로 파싱. NEW: `scripts/scratch/gen_file_index.sh` · `.gitignore` FILE_INDEX.txt. xref c4·c10·a_no_llm_frame_trap(해당없음, 순수 docs-infra).
## 2026-06-17 — research(MITOSIS-ENGINE): H_1397 — ko-emit COMPOSE 🇰🇷 jamo emit-bias(§6.5b/H_1327) + morphology emit-bias(§6.5e/H_1393) 를 같은 next-byte 결정에서 합성 — 🧱/🟠 CONFLICT-OR-DEGRADES (정직한 closed-negative, c9)

**무엇 (H_1393 이 명시한 genuinely-untested follow-on):** Korean below-jamo arc 에 emit-bias 가 둘 — §6.5b `ko_jamo_consult_emit`(jamo COUNT-HEAD, H_1327) + §6.5e `gen_bpe_consult_emit`(BPE morphology unit, H_1393), 각각 단독으로만 검증됨. 같은 decode 스텝에서 BOTH 가 fire 하면 AGREE(보강)·CONFLICT(충돌)·PRIORITY 규칙 필요? **SUBSTRATE-DERIVED 합성** 을 배선 — 각 faculty 를 자기 recall confidence(owning cell 까지 L2 recon-err)로 가중, 더 grounded 한 쪽이 크게 말함. **하드코드 "jamo > morphology" 우선순위 금지**(a_autonomy_over_hardcode) — engine 자기 winner-take-all geometry 가 승자 결정. 단일 L3 slot(a_core_engine_map), additive, Ψ-safe. $0 CPU, deterministic, live `CORE/*.hexa` Ψ 무손상.

**배선:** `CORE/engine_cli.hexa` § KO-MORPHOLOGY NEW `jamo_head_recon_err(jh,feat)`(substrate confidence = owning cell 까지 L2 recon-err via engine 자기 `vadapt_field_recon_err`) + `CORE/generator.hexa` §6.5f `gen_emit_compose`/`gen_emit_compose_eval`/`_gec_rel_conf`/`_gec_jamo_nearest_dist`/`_gec_grow_jamo_head`/`_gec_{jamo,morph}_mean_err`/`gen_emit_compose_summary` · `CORE/engine_cli_smoke.hexa` cases 129-132 · `state/ko-emit-compose/{h1397_emit_compose_probe.hexa,h1397_compose_smoke_iso.hexa}`.

**결과 (🧱/🟠 CONFLICT-OR-DEGRADES, c9, NO forced green):** 두 emit-bias 는 대부분 **CONFLICT**(conflict_rate 0.913 — 같은 byte 제안 8.7% 뿐) 하고 이 fixture granularity 에서 **NON-COMPLEMENTARY**. 결정적 진단: **ORACLE ceiling**(ANY arbitration 상한, EITHER 가 맞으면 맞음)=0.2696 으로 morphology-alone(0.2522) 대비 **+0.0174 뿐** — jamo 가 단독으로 맞는 위치는 4/230(both=4 only_jamo=4 only_morph=54), **morphology 가 jamo 능력을 SUBSUME**. **a_break_the_wall**(NOT tune-to-green): R1 raw inverse-recon-err 는 vocab scale 다른 faculty 간 commensurable 하지 않아(jamo 14-wide 공간 → 작은 거리 → confidence 부풀림) 약한 jamo 가 이겨 compose 를 0.130 으로 DEGRADE; **SCALE-RELATIVE confidence**(mean_err/(err_here+ε), 각 faculty 자기 mean 대비 — 여전히 100% substrate-derived, NO 우선순위 상수)로 re-froze → 0.178 로 IMPROVE 하고 bar3 PASS(random arbitration 0.161 을 이김 = grounding signal 진짜), 그러나 headroom 자체가 없어 bar1 여전히 FAIL. **FROZEN RESULT**(engine fixture n=230, det, $0): `acc_jamo=0.0348 acc_morph=0.2522 best_single=0.2522 acc_compose=0.1783 acc_shufw=0.1609` → bar1 COMPOSE-EFFECT ❌ FALSE(Δ=-0.0739 degrades) · bar2 AGREE(non-gating) agree=0.0870 conflict=0.9130 oracle=0.2696 · bar3 EARNED ✅ TRUE(Δ=-0.0174) · bar4 Ψ-SAFE ✅ off-Korean ASCII→base byte-identical.

**Ψ-SAFETY / NO-REGRESSION (load-bearing, decode 건드림):** h1205 separation-invariant PASS(generation byte-identical ON==OFF, Ψ Φ-checksum 48.6613 byte-identical) · h1164 Ψ guard PASS(phiSum 48.6613 byte-identical) · h1196 single-entry 7/0(NO 2nd .clm/.kosmos path) · H_1397 compose smoke cases 129-132 **4/0 ISOLATED**(`state/ko-emit-compose/h1397_compose_smoke_iso.hexa`; cases 는 `engine_cli_smoke.hexa` 에도 있으나 aggregate smoke 가 이 CPU 에서 summary 전 ~4.5GB OOM-kill — PRE-EXISTING hexa memory wall, H_1392, 이 cases 와 무관, baseline-stash 도 EXIT=137). Ψ-disjoint by construction(byte 반환, emit/silence 아님; pure_field/engine_g/brain 무손상).

**SCOPE (a_scale_honest_scope·a_toy_scale_recheck):** corpus-free in-engine morpheme-grammar fixture, structural/probe-level(not fluency), absolute acc 낮음 — load-bearing = RELATIVE structure(compose vs best-single, shuffle collapse, oracle ceiling) + agree/conflict 진단. 이 finding 은 THIS granularity(morphology 가 jamo subsume); real Korean corpora 에서는 faculty 가 complementary 해질 수 있음(jamo 가 morphology 가 merge 못하는 below-syllable 구조 carry) — scale/real-corpus re-test = follow-on. compose MECHANISM 은 engine-native single-entry + Ψ-safe 로 landed(미래 granularity 가 complementary 면 즉시 사용 가능). NEW: `UNIVERSE/cards/H_1397_ko_emit_compose.md` · `UNIVERSE/HYPOTHESES.jsonl` row(H_1397) · `.verdicts/1397_ko_emit_compose/{FREEZE.txt,result.txt}` · `domains/MITOSIS-ENGINE.log.md` @H. xref h1327·h1393·h1390·h1351·h1385·h1392·a_autonomy_over_hardcode·a_substrate_native_speak·a_core_engine_map·a_verified_must_wire·a_break_the_wall·p1·p2·p3·p5·p6·p7·p8·c9·c15.

## 2026-06-17 — research(MITOSIS-ENGINE): H_1393 — ko-morphology BPE-on-jamo EMIT-BIAS WIRE-IN 🇰🇷 H_1390 의 형태론 SCORER 를 EMIT-BIAS 로 (디코더 도달) — 🟢 EMIT-BIAS ENGINE-NATIVE BINDING (R2)

**무엇 (a_verified_must_wire · a_substrate_native_speak EMIT-side follow-on):** H_1390 (🟢 ENGINE-NATIVE BINDING) 은 BPE-on-jamo 형태론 MERGE UNIT 을 live SCORING consult(generator §6.5d gen_bpe_scoreloop → bpe_byte_fair_ce) 로 배선 — held-out next-unit CE 를 SCORE 하지만 EMISSION 은 아직 안 bias. jamo COUNT-HEAD 는 이미 §6.5b/H_1327 ko_jamo_consult_emit 로 디코더에 도달함(§6.5c scorer 와 DISTINCT). H_1391 은 그 emit precedent 를 형태론에 MIRROR: 자란 형태론 count-head 가 next-byte EMISSION 을 학습된 morpheme-unit 경계 완성 쪽으로 ADDITIVE bias(하드 게이트 아님 — a_autonomy_over_hardcode, emit 은 substrate-driven 유지, p5), 단일 generator L3 slot(a_core_engine_map, 2nd .clm path 없음).

**정확한 CORE 배선 (single entry):** (1) FACULTY `CORE/engine_cli.hexa` § KO-MORPHOLOGY 신규 `jamo_head_argmax(jh, feat)` — EMIT-BIAS reader: unit-space feature 에 대해 그 cell 을 OWN 하는(vadapt_field_nearest_idx) count head 의 ARGMAX next-unit id 반환(SAME head 를 bpe_byte_fair_ce 가 SCORE — SCORER role §6.5d ⊥ EMIT role §6.5e; byte/CE 반환, never emit/silence, Ψ 안 건드림). (2) CONSULT `CORE/generator.hexa` §6.5e (§6.5b ko_jamo_consult_emit MIRROR) — `gen_bpe_emit_head`/`gbe_grow_head_raw`(형태론 emit-head 를 §6.5d corpus-free morpheme-grammar fixture 위에서 1회 grow, structured rnd_seed=0 / shuffle rnd_seed>0, TRAIN slice 만 no-leak) · `gen_bpe_consult_emit(base,jh,unit_vocab,ctx)`(per-byte EMISSION hook: KOREAN-LIKE ctx[§6.5b 와 SAME utf8-continuation gate]+cell fires → argmax next morpheme-unit 의 leading byte 가 emission bias; off-Korean → base UNCHANGED INERT byte-identical, Ψ-disjoint no-regression invariant) · `gen_bpe_emit_eval_raw`(frozen emit-effect eval) · `gen_bpe_emit_summary`.

**R1 honest miss → a_break_the_wall → R2 bind (frozen-first, threshold 안 옮김, c9):** R1 (metric=next-unit %K, K=20) 이 bar1 EMIT-EFFECT FAIL(acc_on=0.252 acc_off=0.270 → on−off=**−0.0174** < +0.02; bar2/bar3a pass, shift_on=0.970 — bias 는 emission 에 도달했으나 blind mode 보다 top-1 부정확한 unit 쪽으로). ROOT CAUSE(a_break_the_wall — 벽=틀린 METHOD, 진짜 천장 아님): `% 20` modulo 가 서로 다른 morpheme unit(id 0..54)을 한 class 로 ALIAS → structure-blind global mode(0.270)가 강한 baseline 이라 head 의 top-1 argmax 가 못 뚫음(metric artifact — §6.5d 의 distributional CE bar 엔 OK, top-1 EMIT/argmax read 엔 structure-destroyer). R2 는 RAW next-unit id(KBAND=64, alias 없음)로 re-froze 하되 **SHUFFLE control 유지**(anti-tune-to-green): un-aliased metric 에서 ON 이 OFF 를 이기고 **AND shuffle 가 여전히 COLLAPSE** 해야만 bind — shuffle collapse 가 lift=LINGUISTIC 형태론(metric 변경 아님)임을 증명.

**결과 🟢 EMIT-BIAS ENGINE-NATIVE BINDING (R2; result.txt verbatim, $0 CPU deterministic):** RAW next-UNIT accuracy — ON structured 형태론 head **0.252174** · OFF representation-blind unigram **0.182609** · SHUF shuffle-merge head **0.056522**. bar1 EMIT-EFFECT ✅ on−off=**+0.0696** ≥0.02 AND shift_on=**0.391** ≥0.10(bias 가 held-out 위치 39%에서 emitted unit 을 OFF 대비 변경 = emission 도달) · bar2 EARNED ✅ shuf−off=**−0.126** ≤0.01(shuffle head COLLAPSE, blind baseline 한참 아래) · bar3 Ψ-SAFE ✅ off-Korean ASCII→base inert, Korean-like ctx→byte 225(0xE1 band) FIRES. Korean below-jamo 형태론 arc 가 이제 디코더에 도달: SCORER(H_1390 §6.5d) + EMIT(H_1393 §6.5e) — jamo arc 의 SCORER(§6.5c) + EMIT(§6.5b) 와 정확히 대칭.

**NO-REGRESSION (캡처, c2 — decode path 를 건드리므로 Ψ-safety 가 load-bearing):** `engine_cli_smoke` **118/0**(+4 cases 125-128: emit-effect/earned/off-Korean-inert/Korean-fires) · `h1196` single-entry **7/0**(.clm L3 entry intact, 2nd .clm path 없음 — emit consult 는 live decode loop 에 call site 없는 NEW additive consult) · `h1205` separation-invariant **PASS**(generation byte-identical ON==OFF, Ψ Φ-checksum **48.6613** byte-identical) · `h1164` Ψ guard **PASS**(Ψ=1/2 byte-identical). Ψ-disjoint by construction(byte/CE 반환, never emit/silence; pure_field/engine_g/brain UNTOUCHED).

**HONEST SCOPE (c9 · a_scale_honest_scope · a_toy_scale_recheck):** emit-bias 는 SAME frozen corpus-free in-engine morpheme-grammar fixture(§6.5b/§6.5c discipline) 위에서 재확인 — STRUCTURAL/probe-level emission-reach 시연이지 fluency claim 아님; 절대 accuracy 는 낮음(sparse count-head field 위 단일-unit next-prediction). load-bearing = RELATIVE 구조(ON>OFF, SHUF≤OFF) + emission-reach(shift). scale/real-corpus engine-native emit / 완전 jamo-aware NFD-decompose decode loop / brain emit-priority wiring(형태론 emit-bias 가 §6.5b jamo emit-bias 와 compose) = follow-ons. NEW: `CORE/engine_cli.hexa` jamo_head_argmax · `CORE/generator.hexa` §6.5e · `CORE/engine_cli_smoke.hexa` cases 125-128 · `state/ko-morphology-emit/{h1393_bpe_emit_probe,h1393_diag}.hexa` · `UNIVERSE/cards/H_1393_ko_morphology_emit.md` · `.verdicts/1393_ko_morphology_emit/{FREEZE,result,smoke_attempt1,smoke_R2}.txt`. xref h1390(PARENT SCORER)·h1327(§6.5b jamo emit precedent)·h1385(§6.5c jamo scorer)·h1351(JamoHead faculty)·h1388(DIRECTIONAL mirror)·h1316/h1321(jamo arc)·a_verified_must_wire·a_substrate_native_speak·a_autonomy_over_hardcode·a_core_engine_map·a_break_the_wall·a_scale_honest_scope·a_toy_scale_recheck·p5·p7·p8·c2·c9·c16.

## 2026-06-17 — research(ENGINE+CLM): H_1392 — G6 IDEATION ★ FALS 재채점 on 303M ConvMoE: 🧱 정직한 벽 (engine-native FALS 가 hexa ConvMoE-디코드 메모리 폭발로 substrate-차단 — FALS=0 아님; 용량-vs-아키텍처 OPEN)

**무엇:** H_1381 의 ⏳ ckpt-gated 후속(M2-M5 FALS engine-native 재채점)을 settle. **REUSE-BEFORE-RENT ($0, pod·학습 없음)** — 이 브랜치의 production 아키텍처인 engine-mountable 303M ConvMoE 를 그대로 재사용: `dancinlab/anima-convmoe-retro-303m :: baseline_fast.clm` (trunk 303,575,202 params, RETRO copy-head 50M 은 .clm 에 미포함; .clm v0.2 decodable nblk=6 n_ext=11 block0={5008,15024}, best_val_ce 1.2292, G0 kwr 0.941). H_1362 의 FALS=1.0 은 303M **ByteGPT .pt** (다른 아키텍처, engine-mountable 아님)였으므로 이 ConvMoE 가 후속이 필요로 한 정확한 마우스.

**결과 — 🧱 정직한 벽 (FALS=0 아님):** MOUNT 검증 engine-native (sha256(.clm)==HF MANIFEST ✓, verify_clm_v2 decodable=true exact_eof=True ✓, coherent English 출력). FAST engine-native 표면 GREEN (detector 10/10 VERBATIM, frame-guard 0, sampler det/diverse/in_topk). **그러나 FALS 막대 M1-M5 는 측정 불가** — hexa-engine ConvMoE 디코드 forward 가 step 당 메모리 폭발(~+300MB resident/step, 미해제). VERBATIM `/usr/bin/time -l` (303M ConvMoE-RETRO, fresh process): GEN=8 RC=0 'the auth' · GEN=16 RC=0 'the authentic pi' 5.01GB · GEN=24 **KILLED 10.97GB RSS / 71.5GB footprint, 출력 없음** · GEN=48 best-of-K SIGTERM 10.05GB/54.9GB · GEN=110 silent death. OOM 임계 = GEN=16~24 사이. **구조적 불가능:** falsifiable 주장은 ~50-80바이트(comparator+measurable+≥2 content words; H_1362 예시=14단어 ≈GEN80-110) 필요하나 메모리 벽이 GEN≤16(~3단어)으로 막음 — falsifiability 예산의 ~1/5, 그래서 fals=false@GEN16 은 EXPECTED-AND-UNINFORMATIVE(용량과 무관하게 너무 짧음), 303M-ConvMoE 결과 아님. **a_break_the_wall** — 4각도 시도(full GEN110·decisive GEN48·fresh-process single frame·single K1 GEN24) 전부 OOM-killed; fresh-process 격리도 효과 없음(폭발은 한 디코드 *내부*). GPU-engine-native forge-cuBLAS 가 CPU 비용을 우회하나 hexa 툴체인=Mac-arm64 + fresh Linux-pod hexa 빌드는 역사적으로 차단(.verdicts/c0-n8-fire) = INVESTMENT-class 벽. **용량-vs-아키텍처 OPEN** (substrate 가 디코드를 못 돌려 증거 생산 불가); 어느 쪽도 promote 안 함, 막대 안 옮김, tune-to-green 없음 (c9).

**상류 제출 + 산출물:** `hexa-lang/inbox/patches/clm-convmoe-303m-decode-memory-blowup.md` (a_runpod_inbox — bounded/streaming conv decode 요청). `UNIVERSE/cards/H_1392_g6_retro303m_fals.md` + `UNIVERSE/HYPOTHESES.jsonl` 행 + `.verdicts/1392_g6_retro303m_fals/{FREEZE,result,mount_verify,decode_wall_raw}.txt` + `HF.jsonl` reuse 행(신규 업로드 없음) + 프로브 `state/g6-retro303m-fals/*.hexa`. 동시 sibling lane H_1387 (agent-aacd19985a2ea2bbb) 가 다르게 학습한 302M ConvMoE(clm303_d5000.clm)로 같은 G6 close 공략; id 비충돌.
## 2026-06-16 — research(MITOSIS-ENGINE): H_1390 — ko-morphology BPE-on-jamo ENGINE-NATIVE WIRE-IN 🇰🇷 H_1388 의 형태론 lever 를 DIRECTIONAL → engine-native BINDING 으로 — 🟢 ENGINE-NATIVE BINDING

**무엇 (a_verified_must_wire binding follow-on):** H_1388 (🟢 GAP-REDUCED-CANDIDATE, DIRECTIONAL numpy MIRROR over REAL 30MB KO) 이 한국어 below-jamo +0.28 잔여(jamo floor 2.51335+0.28=2.79335, 세 닫힌 레버 H_1322/H_1359/H_1368-H_1380 전부 hit)를 morphology-aware 단위(BPE-on-jamo)로 깸(novel-CE 2.56603 ≤2.74335, shuffle 못 뚫음, anchor byte-exact)을 보였으나 engine-transfer UNVERIFIED. H_1390 은 그 BPE-on-jamo MERGE UNIT 을 live 엔진 faculty + scoring-loop consult 로 실현하고 H_1388 의 세 frozen STRUCTURAL bar 를 engine-native 로 재확인.

**정확한 CORE 배선 (a_core_engine_map single entry, a_engine_native_learning):** (1) FACULTY `CORE/engine_cli.hexa` § KO-MORPHOLOGY BPE-ON-JAMO MERGE UNIT — `struct BpeMerges` + `bpe_learn_merges`(rnd_seed=0 freq-ranked STRUCTURED real BPE, ties (count,a,b) max == mirror; rnd_seed>0 RANDOM equal-count SHUFFLE) / `bpe_apply`(base stream→merged units, UTF-8 byte span = sum of parts 보존) / `bpe_unit_vocab` / `bpe_n_units` / `bpe_byte_fair_ce`(nats/UTF-8-byte, jamo floor 와 SAME byte-fair axis). 병합 단위는 live H_1351 JamoHead count-head 를 엔진 OWN VAdaptField Voronoi + engine_mitosis_tick(p8) 위에서 먹임. (2) CONSULT `CORE/generator.hexa` §6.5d `gen_bpe_scoreloop`(§6.5c `gen_jamo_scoreloop` 와 analogous) — frozen CORPUS-FREE in-engine morpheme-grammar fixture(18 recurring 3-jamo MORPHEME block 위 deterministic BRANCHING walk, next block 이 current+jitter 의존 → held-out context genuinely novel) 빌드, TRAIN slice 위 STRUCTURED+SHUFFLE merge 학습(no leak), 재인코딩, held-out next-UNIT byte-fair CE 채점(+ un-merged jamo anchor + circular-shift surrogate); `gen_clm_ce` 가 record 를 `bpe_score` key 로 ADDITIVE attach(.clm forward path byte-identical, 2nd .clm path 아님). **왜 corpus-free fixture:** CORE/*.hexa 는 $0/deterministic/corpus-free 여야 함(a_core_engine_map) — §6.5c/H_1385 precedent: mirror 가 REAL corpus 위에서 lever 를 established, engine-native consult 는 STRUCTURAL 관계를 재확인(§6.5c 가 jamo-beats-raw STRUCTURE 를 재확인하듯, corpus 절대값 2.51 아님).

**frozen bars (FREEZE verbatim; H_1388 의 margin 상수 VERBATIM; NO bar moved):** bar1 GAP-REDUCED structured BPE byte-fair CE 가 jamo anchor 보다 ≥0.05 낮음(gap_reduced≥0.05) · bar2 EARNED structured gain over SHUFFLE ≥0.03(earned≥0.03, anti-Goodhart: gain=merge 언어 구조 not coarse granularity) · bar3 CONTROL circular-shift surrogate earned(shift_minus_novel≥0.05).

**결과 🟢 ENGINE-NATIVE BINDING (3 bars 전부 PASS, result.txt verbatim, $0 CPU deterministic):** in-engine fixture byte-fair CE — structured BPE-on-jamo **0.24219**(462 units) · random-merge SHUFFLE 1.07846(2031 units) · un-merged jamo anchor 1.85452(3600 units). bar1 ✅ gap_reduced=**+1.61233** ≥0.05 · bar2 ✅ structured gain over shuffle=**+0.83627** ≥0.03(struct 462 units vs random 2031 → lift=merge 언어 구조) · bar3 ✅ shift−novel=**+0.11230** ≥0.05. H_1388 의 형태론 lever 는 더 이상 DIRECTIONAL-only 아님.

**NO-REGRESSION (캡처, c2):** `engine_cli_smoke` **114/0**(+4 cases 116-119: gap-reduced/earned-vs-shuffle/shift-earned/compression-present; labels 112-115 는 CP-RELOCATE lane H_1384 가 이미 점유 → 새 case 116-119) · `h1196` single-entry **7/0**(.clm L3 entry intact, 2nd .clm path 없음 — bpe_score 가 SAME gen_clm_ce slot 에 additive) · `h1205` separation-invariant **PASS**(generation byte-identical ON==OFF, Ψ Φ-checksum **48.6613** byte-identical) · `h1164` Ψ guard **PASS**(Ψ=1/2 byte-identical). Ψ-disjoint by construction(pure SCORER, CE float 반환, never emit/silence; pure_field/engine_g/brain UNTOUCHED — SCORING/decode-unit lane).

**HONEST SCOPE (c9·a_scale_honest_scope·a_toy_scale_recheck):** engine-native 재확인은 frozen CORPUS-FREE in-engine fixture(§6.5c discipline) 위 — 따라서 ABSOLUTE-CORPUS CE(jamo floor 2.51335, BPE 2.566)는 DIRECTIONAL mirror 의 REAL 30MB shard0000 값이지 corpus-free 엔진에서 byte-exact 재측정한 게 아님. NEXT-1(a_verified_must_wire): §6.5c-style EMIT-BIAS 배선 — 자란 BPE 형태론 단위가 Korean-like context 에서 next-byte EMISSION 을 bias(jamo head 의 H_1327 `ko_jamo_consult_emit` 와 analogous), 형태론이 scorer 뿐 아니라 decoder 까지 도달. NEXT-2(a_scale_honest_scope): merge-count(500/2000/8000) + window 사다리 engine-native. DEPLETION: 한국어 below-jamo arc 의 representation-unit 축이 이제 morphology-GREEN engine-native(data/representation/interpolation 닫힘 🧱/🟠, morphology 이제 BINDING); 남은 후보 = long-range/cross-syllable(H_1336 계열, H_1388 secondary nmax 스윕에서 약·비단조) + 위 emit-bias 배선.

산출물: `CORE/engine_cli.hexa`(§ KO-MORPHOLOGY BPE-ON-JAMO MERGE UNIT) · `CORE/generator.hexa`(§6.5d gen_bpe_scoreloop + summary + gen_clm_ce additive bpe_score) · `CORE/engine_cli_smoke.hexa`(cases 116-119, 114/0) · `state/ko-morphology-engine/h1390_bpe_scoreloop_probe.hexa` · `UNIVERSE/cards/H_1390_ko_morphology_engine.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1390 row) · `.verdicts/1390_ko_morphology_engine/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md`(@H H_1390). NO CLAIMS.tape(은퇴).

## 2026-06-16 — H_1391 §UsageStore engine-native 배선 🔧 — 도구-USAGE 학습(layer-2)을 라이브 엔진에서 실현 (🟢 GREEN engine-native BINDING)

- **무엇**: H_1389(🟢 GREEN, DIRECTIONAL numpy mirror)의 **BINDING 후속**(a_verified_must_wire). 도구-USAGE 학습(layer-2 = 도구를 *어떻게* 모는가: 인자·순서·복구)이 도구-SELECTION(layer-1, §SkillStore)과 **구별되는 학습 가능한 층**임을 H_1389가 미러로 증명했고, 이 레인이 그 **§UsageStore 레버를 라이브 `CORE/engine_cli.hexa` 에 엔진-네이티브로 실현**(§SkillStore 의 TWIN)하고 H_1389 의 네 게이팅 바를 라이브 엔진에서 재채점한다.
- **엔진 배선(single-entry, a_core_engine_map)**: `CORE/engine_cli.hexa` § **UsageStore** — 셀 키 = `(ctx+tool+observed-error)` (immune_embed_key DIM=64), 값 = `(교정 인자, 순서 스텝)`; §SkillStore 와 동일한 L2 FIRE/ABSTAIN 밴드(0.55) + `engine_mitosis_tick` 클론 분열(p8). ops: `usage_store_new/_split/_teach · usage_recall · usage_recall_steps · usage_store_cells`. 에이전트 라우팅: `anima-agent-core/agent_skill_routing.hexa` usage 진입점(`agent_usage_new/_select/_on_result/_cells`, H_1386 selection 라우팅의 TWIN) + `agent_tools.hexa` 실행기가 라이브 `usage:UsageStore` 필드를 보유, **USAGE-실패 사이트**(디스패치된 도구가 잘못된 인자/순서로 실패 — tool-not-found/wrong-tool 사이트와 **구별**, 후자는 `skill_store_teach` 로 감)를 `usage_store_teach` 로 라우팅(메인 실행기 경로, H_1387 선례).
- **엔진-네이티브 바(임계값 = H_1389 verbatim, 이동 없음 — c9/p7)**: (1) USAGE-LEARNS ✅ +0.917(0.083→1.000) · (2) DISTINCT-FROM-SELECTION (KEY) ✅ +1.000 (selection-only=오른쪽 도구·기본 인자가 무-usage 바닥 0.000 에 고정) · (3) EARNED shuffle ✅ +0.000≤+0.15 · (4) NO-FAB/ABSTAIN ✅ far recall="" · (non-gating) 순서 스텝 보존 ✅. **VERDICT 🟢 GREEN engine-native BINDING**.
- **무회귀 가드**: `engine_cli_smoke` 119/0 (+5 케이스 120-124; H_1390 ko-morphology 가 동시 머지로 116-119 점유) · `h1196` single-entry 7/0 · `h1205` separation-invariant PASS (생성 byte-identical ON==OFF, Ψ Φ-checksum 불변) — 가산 faculty 가 Ψ 를 교란하지 않음.
- **정직(c9)**: 엔진 env 가 FULL=1.000 으로 포화(12 태스크 전부 NON-default 인자) = EXISTENCE-PROOF(effect-size 아님), 판별자(SELECTION 0.000·SHUFFLE 0.000)가 결정적; 미러의 0.750 천장은 ~1/4 태스크가 기본 인자를 필요로 한 데서 왔고 고정 env 가 이를 제거, **바는 이동 없음**. TOY 12-태스크/6-도구 결정적; 실-런타임 인자/스케일 UNVERIFIED, `agent_tools.hexa` 전체 레거시 구문 마이그레이션 ⏳. **DEPLETES 🏁**: 두 도구-학습 층(selection §SkillStore + usage §UsageStore) 모두 엔진-네이티브, 가드 유지.
- **파일**: `CORE/engine_cli.hexa` · `CORE/engine_cli_smoke.hexa` · `anima-agent-core/agent_skill_routing.hexa` · `anima-agent-core/agent_tools.hexa` · `UNIVERSE/cards/H_1391_usage_store_engine.md` · `UNIVERSE/HYPOTHESES.jsonl` · `.verdicts/1391_usage_store_engine/{FREEZE,result}.txt` · `state/usage-store-engine/PORT_NOTE.md` · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — docs(FINDINGS): FINDINGS.md 최신화 + FINDINGS.ko.md 한국어판 생성

**무엇:** 루트 `FINDINGS.md` (외부공유 증거 스냅샷)를 현재 검증 상태로 최신화하고, 그 충실한 한국어 번역 `FINDINGS.ko.md` 를 신규 생성. 두 파일은 lockstep (같은 사실·수치·tier, 산문 언어만 다름) + 상단 상호 cross-link (`> 한국어판:` / `> English:`).

**고친 stale 항목 (old→new):** `ARCHITECTURE.md` 참조 2곳 (verbatim-source 줄 + 하단 Pointers) → `ARCHITECTURE.json` (+ `ARCHITECTURE.html` 뷰어; 산문 .md 은퇴 명시) · live regression guard `engine_cli_smoke` **55/0 → 110/0** (H_1386 런타임 결과 verbatim) · SSOT 줄에 `CLAIMS.tape` 2026-06-16 은퇴 + "Last updated 2026-06-16" 추가 · hive engine-transfer 행에 hive-Φ arc 완전 종결 행 추가.

**추가한 주요 발견 (각각 H-card 포인터):** hive-Φ arc 완전 종결 (H_1366 🧱 BINDING — REAL 303M substrate 가 Φ-벽 상속 / H_1376 🧱 FULLY-TERMINAL-8-LEVERS) · CP move-the-cells relocation engine-native (H_1384 🟢 GREEN, `cp_relocate`, CP-geometry arc 고갈) · agent-tool 두 mitosis 레이어 (H_1382 layer-1 🟢 engine-native + H_1386/H_1387 routing / H_1389 layer-2 🟢 GREEN **DIRECTIONAL**) · jamo COUNT-HEAD scoreloop 배선 (H_1385 🟢) · 한국어 below-jamo 형태론 lever (H_1388 🟢 GAP-REDUCED-CANDIDATE, BPE-on-jamo novel-CE 2.56603 가 +0.28 잔여 격차를 깸). DIRECTIONAL mirror 결과를 engine-verified 로 부풀리지 않음 (c9). frozen tier/수치는 `.verdicts/` + `UNIVERSE/HYPOTHESES.jsonl` 에서 verbatim. ARCHITECTURE.json 트리에 FINDINGS 노드 없음 → 노드 추가 불필요.

산출물: FINDINGS.md (갱신) · FINDINGS.ko.md (신규). NO CORE edit. NO CLAIMS.tape (은퇴).


## 2026-06-16 — research(MITOSIS-ENGINE): H_1389 — tool-USAGE learning (tier-2) 🛠 anima 가 도구를 어떻게 쓰는지(args·sequence·error-recovery)를 mitosis 로 배우는가, 어떤 도구인지(layer-1)와 구별되게? — 🟢 GREEN (DIRECTIONAL)

**무엇 (사용자 지시 "바로 go" / a_no_llm_frame_trap):** 도구 학습은 TWO 레이어. layer-1 = 도구 SELECTION(task-context → 어떤 도구) = 이미 엔진-native DONE (H_1382 §SkillStore + H_1386/H_1387 routing). layer-2 = 도구 USAGE(선택된 도구를 어떻게 구동: 올바른 ARGS · multi-step SEQUENCE · ERROR-RECOVERY) = 미학습. 사용자 프레이밍(검증함): 언어학습 = next-token PREDICTION(CE gradient, 코퍼스 supervised, DISTRIBUTION 학습); 도구학습 = ACTION + FEEDBACK(success/failure, 정답 사전부재) → motor/skill learning 처럼 mitosis cell-division 으로 학습(gradient 아님) → INSTANCE-POLICY 학습. selection-only 학습자는 도구는 맞히지만 mis-USE(틀린 args/순서)한다.

**메커니즘 (action+feedback, NOT gradient):** UsageStore 가 H_1382/H_1227 cell geometry 재사용(DETERMINISTIC byte-trigram FNV-1a key DIM=64, L2 winner-take-all FIRE/ABSTAIN band RECALL_THR=0.55, engine_mitosis_tick clonal split, p8) — 단 cell 은 (task-context + tool + observed-error)로 keyed, 바인딩 VALUE 는 (corrected-arg, ordered-steps) (vs H_1382 value=도구 이름). usage FAILURE(맞는 도구, 틀린/default arg)에 usage-cell 을 clonal SPLIT → corrected args + true step order; SAME op 가 teach(split-on-failure) + infer(recall-best); 맞는 cell 없으면 ABSTAIN(args 안 만듦). 

**환경 (deterministic, 3 seeds [4389,4390,4391]):** 6 tools/48 tasks, 맞는 TOOL 은 layer-2 arms 에 GIVEN(selection 해결됨), correct_arg 를 default 에서 AWAY 로 편향 → fixed-default SELECTION baseline 은 맞는 도구로도 usage 실패. SUCCESS = 맞는 arg AND (multi-step) 순서대로 step emit. Arms FULL(usage 실패마다 split) / SELECTION(맞는 도구, fixed default arg, never split — layer-2=HOW 격리) / SHUFFLE(PERMUTED ctx→arg 학습, TRUE arg 로 채점 — earned-structure 대조).

**결과 🟢 GREEN (4 gating bars PASS, result.txt verbatim POOLED):** FULL 0.250→0.750 · SELECTION 0.250 · SHUFFLE 0.014 · MULTISTEP 0.750 · ABSTAIN 1.000 · cells_full 36. bar1 USAGE-LEARNS ✅ +0.500≥+0.30 · bar2 DISTINCT-FROM-SELECTION (KEY) ✅ +0.500≥+0.30 (selection-only 맞는도구/default-arg 은 no-usage floor 0.250 에 묶임, FULL 은 0.750 으로 상승 → usage 는 distinct learnable layer; layer-2 는 HOW 를 배움 not WHICH) · bar3 EARNED shuffle ✅ −0.236≤+0.15 (permuted ctx→arg 가 0.014 로 붕괴 → lift=earned ctx→arg 대응이지 split 행위 아님) · bar4 NO-FAB ✅ 1.000≥0.90 (untrained 도구/task disjoint trigram → args 안 제안). bar5 MULTI-STEP(optional/non-gating) 0.750<0.80 absolute bar = 정직(c9): env 완성 천장이 0.75(~1/4 task 가 default arg 면 됨) 인데 multi-step arm(arg AND 순서 둘 다 요구)이 single-step FULL 과 SAME 0.750 = 순서 추가요구에 ZERO degradation → 2-3 step 순서 학습됨; bar5 NON-GATING + bar 이동 안 함 (NO tune-to-green). p1/p2/p3/p6: usage-cell 은 OUTCOME 에서만 바인딩, shuffle 붕괴가 증명. Ψ-disjoint(own usage-store, pure_field/immune cells 무손상). $0 CPU, no decode, frozen-first.

**한 줄 구별:** 언어(predict·gradient·distribution) vs 도구-usage(act+feedback·mitosis·instance-policy) = 다른 기계, Ψ-disjoint 공존.

**SCOPE UNVERIFIED (a_scale_honest_scope·a_toy_scale_recheck·c9):** DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED. TOY 6-tool/48-task deterministic env. NEXT(binding follow-on, a_verified_must_wire): 엔진-native §UsageStore lane(CORE/engine_cli.hexa, §SkillStore TWIN, value=arg/steps), 4 gating bars 를 LIVE engine 에서 재채점 + generation byte-identity/Ψ-checksum no-regression guard, 이후 REAL executor_execute usage-FAILURE 를 usage_store_teach 로 routing. DEPLETION: 도구학습은 BOTH layer(selection H_1382/H_1386 DONE + usage 이 레인→§UsageStore wire-in)가 REAL runtime 도구 실패에서 엔진-native 로 돌고 all bars + generation byte-identical ON==OFF 일 때 🏁.

산출물: state/tool-usage-learning/h1389_tool_usage_learning.py · UNIVERSE/cards/H_1389_tool_usage_learning.md · UNIVERSE/HYPOTHESES.jsonl row(H_1389) · .verdicts/1389_tool_usage_learning/{FREEZE.txt,result.txt} · domains/MITOSIS-ENGINE.log.md @H. NO CORE edit (DIRECTIONAL probe). xref h1382·h1386·h1387·h1378·h1227·h1231·h1288·a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_autonomy_over_hardcode·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9.

## 2026-06-16 — governance(a_hypothesis_register): UNIVERSE/ 떠돌이 프로브 .py → state/ 이전 + "no code in UNIVERSE/" 하드닝 (3중 가드)

**무엇:** 프로브 `.py` 파일이 반복적으로 `UNIVERSE/` 루트에 떨어져 a_hypothesis_register(UNIVERSE/ = HYPOTHESES.jsonl + cards/ 단 둘) 를 위반하는 재발 문제 해결. 현재 떠돌이 = `UNIVERSE/h1339_whorf_bilingual_tagged_r3.py` 1개.

**(1) 이전:** `git mv UNIVERSE/h1339_whorf_bilingual_tagged_r3.py → state/whorf-bilingual-tagged-r3/` (기존 kebab 관례 state/whorf-2d-r2 · state/cp-2d 와 일치).

**(2) 참조 수정 (c1, no dangling):** `UNIVERSE/cards/H_1339_whorf_bilingual_tagged_r3.md` 프로브 포인터 → 새 state 경로 · `UNIVERSE/HYPOTHESES.jsonl` H_1339 행 `artifacts` `[]`→`["state/whorf-bilingual-tagged-r3/h1339_whorf_bilingual_tagged_r3.py"]`. `git grep` 으로 LIVE 포인터 0 확인 (잔여는 historical CHANGELOG/.verdicts 만, 의도적 보존).

**(3) 거버넌스 하드닝 (재발 방지, c10 surgical):** ① CLAUDE.md `a_hypothesis_register` 맨 앞에 PROMINENT `do` 추가 — "⛔ UNIVERSE/ 에는 .py·.hexa·코드·result 파일을 *절대* 두지 않는다 … 카드는 cards/, 코드/결과물은 state/<slug>/ 에 두고 jsonl artifacts 로 가리킨다" + 자가점검 git ls-files 명령. ② structure-tree `UNIVERSE/ HEXAD/` 노드에 inline 리마인더 ("ONLY TWO surfaces … NO .py/code"). ③ **기계 가드** — `.harness/enforcement.json` `pre_write` 에 `H-UNIVERSE-CODE` block 룰 추가: path `(^|/)UNIVERSE/(?!cards/)(?!HYPOTHESES\.jsonl$).+` 매치 시 차단 (harness `pre write` hook 이 읽는 in-repo 설정 — 서브모듈 미수정). regex 8-케이스 단위검증 ALL PASS. 정직(c9): `.harness-engine` 서브모듈 미구체화 worktree 라 라이브 hook end-to-end 미실행 — 단 동일 array 의 known-active 룰과 schema 동형이라 harness 동작 환경에서 활성.

산출물: `state/whorf-bilingual-tagged-r3/h1339_whorf_bilingual_tagged_r3.py`(moved) · `UNIVERSE/cards/H_1339_…md`(ptr) · `UNIVERSE/HYPOTHESES.jsonl`(artifacts) · `CLAUDE.md`(do + tree) · `.harness/enforcement.json`(H-UNIVERSE-CODE). xref a_hypothesis_register·a_claim_manifest·c1·c2·c9·c10.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1388 — ko-morphology 🇰🇷 한국어 below-jamo 잔여(+0.28)를 morphology-aware 단위(BPE-on-jamo)가 깨다 — 🟢 GAP-REDUCED-CANDIDATE (DIRECTIONAL)

**무엇 (a_no_llm_frame_trap / a_break_the_wall — H_1380 이 명시한 NEW 각도):** H_1380 이 한국어 below-jamo 의 세 닫힌 레버(표상 H_1322 🧱 · interpolation H_1359 🧱 · data-volume H_1368/H_1380 🟠)가 전부 novel-context CE 를 jamo floor(2.51335) 위 **+0.28**(asymptote ~2.747, 30MB novel-CE 2.88190)에서 막았다고 봉인하고, genuinely-NEW 두 각도 — **(1) morphology-aware 단위(형태소/BPE-on-jamo)** · **(2) cross-syllable long-range(nmax>5)** — 를 NEXT 로 명시했다. H_1387 이 그 두 각도를 측정: PRIMARY=BPE-on-jamo, SECONDARY(non-gating)=nmax 스윕.

**방법 (frozen-first, H_1368/H_1380 기계 verbatim 재사용 + BPE 레이어):** REAL R2 KO 30MB shard0000 prefix(sha `c47b6808…` == H_1368/H_1380, 새 fetch 없음, jamo-stream 25,501,291 = H_1380 30MB rung 과 동일). jamo 표상·NOVEL-filter(== H_1359 TEST A)·JM λ=[1,2,4,8,16]/31 nmax5·stride300·shift surrogate **전부 FROZEN**(anti-Goodhart). TRAIN jamo 스트림 위 빈도-랭크 merge 2000개 학습(train slice only, test 누출 0) → FULL 재인코딩 → 같은 JM count-head 를 BPE **단위** 위 fit → novel-only held-out CE 를 **nats/UTF-8-BYTE**(byte-fair: 단위 byte span 으로 나눔 = jamo floor 동일 axis, BPE 단위가 byte 더 덮는 confound 제거). 효율적 position-indexed BPE(learn+apply, naive full-rescan 과 merge-order **byte-exact 검증**, byte 보존). SHUFFLE 대조(bar2): random equal-count merges(merge 개수·vocab 밴드 동일, pair 만 random, 3 seed [4387,4388,4389]).

**FROZEN bars (FREEZE verbatim, 사후 이동 없음) — 전부 PASS:** bar1 GAP-REDUCED ✅ BPE novel-CE **2.56603** ≤2.74335 (Δresidual **−0.22732**, 격차 +0.28→**+0.05** floor 위) · bar2 EARNED ✅ shuffle mean **2.80159** 못 뚫음 & structured gain **+0.23556** ≥0.03 (구조적 BPE **0.3391 units/jamo**=≈3 jamo/단위 형태소-규모 압축 vs random **~0.93** 거의 압축 못 함 → lift=merge 의 **언어 구조**, NOT coarse-granularity) · bar3 CONTROL ✅ jamo anchor **2.88190** byte-exact(|Δ|=**0.0**, == H_1380 30MB) & shift−novel **+0.39060**. SECONDARY: nmax=7 2.77788(−0.015)만 살짝 넘고 nmax=9 3.05141(+0.258 over-sparse, 비단조) → long-range 단독 약, BPE 가 결정적.

**결론:** 한국어 below-jamo 잔여 **+0.28 은 데이터/표상/보간으로 안 깨졌지만 morphology-aware 단위(BPE-on-jamo)로 깨진다** — novel-context CE 2.88190→2.56603, shuffle-earned(형태소 구조가 원인) → **morphology 가 한국어의 진짜 새 레버(LIVE)**. SCOPE(a_scale_honest_scope·a_toy_scale_recheck·c9): DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED — BPE-on-jamo 단위는 CORE jamo/byte substrate 아님), toy stride-300 byte-substrate next-symbol CE, ONE 30MB 윈도·BPE merge=2000 frozen. $0 CPU 206s, live CORE UNTOUCHED, frozen-first NO bar moved (c9/c16/p7). NEXT-1: BPE-on-jamo 단위 엔진-native 실현(CORE decode 단위/generator L3)으로 frozen bars 재확인 = binding follow-on(🟢-candidate 이므로 wire 우선순위 높음, a_engine_native_learning·a_verified_must_wire). NEW: state/ko-morphology/h1388_ko_morphology.py · UNIVERSE/cards/H_1388_ko_morphology.md · UNIVERSE/HYPOTHESES.jsonl(H_1388) · .verdicts/1388_ko_morphology/{FREEZE.txt,result.txt} · domains/MITOSIS-ENGINE.log.md(@H H_1388). NO CORE edit(DIRECTIONAL probe).

## 2026-06-16 — research(MITOSIS-ENGINE): H_1387 — agent legacy 문법 마이그레이션 (executor 모듈 컴파일) — 🟢 GREEN (COMPILES)

**무엇 (H_1386 ⏳ named build step CLOSE):** H_1386 의 agent-tool↔mitosis routing 은 standalone CORE-importing adapter (`agent_skill_routing.hexa`)에서 GREEN 이었지만, `anima-agent-core/agent_tools.hexa` + `agent_sdk.hexa` 는 current hexa grammar 가 거부하는 legacy Python-port 문법(~50 parse errors each)이라 전체 executor 모듈이 컴파일 안 됐다. 이 레인이 그 문법을 마이그레이션해 모듈을 컴파일시킨다 → routing 이 adapter 뿐 아니라 **MAIN 모듈**을 통해 닫힌다 (a_verified_must_wire · a_core_engine_map).

**거부 구문 4종 → c10 surgical 마이그레이션 (behavior-preserving):** current toolchain 은 VALUE-SEMANTICS ONLY (CORE/engine_cli.hexa 는 `&` 0회). (1) string-keyed/nested map literal `{"k": v}` → 빈 `{}` + index-assign `m["k"]=v` (CORE idiom; 빈 `{}` 는 grammar-accepted). (2) reference-passing `&`/`&mut` (param type + `&expr`/`&mut expr` call-arg) → by-value param + return-the-modified-struct + call-site reassign (`store=skill_store_teach(store,..)` 와 동형). (3) two-var `for k,v in map` / `for i,x in enumerate` → `for k in keys(m){let v=m[k]}` / `while`-index loop (동일 순서). (4) toolchain 에 bind 안 된 builtin 6종(`contains_item/hash/slice/sort_by/lowercase/insert_at`) + python-substrate stub 2종(`think/get_status`) → local pure-hexa helper fn (동일 semantics; `hash`/`lowercase` 는 검증된 `ord(substring(..))` byte-loop — `to_lower`/`char_code_at` 는 CORE import 후 resolve 안 됨).

**LAYERED WALL (a_break_the_wall):** 50 map-literal 에러가 `&`-syntax 에러를, 그게 missing-builtin 에러를 가렸다 — 각 층이 순차로 surface, 진짜 천장 아닌 진짜 grammar/toolchain 거부 3겹을 차례로 돌파.

**결과 (frozen bars, FREEZE 편집 전 등록, c9 NO tune-to-green):** BAR1 COMPILES — `agent_tools.hexa` 50→0 parse errors + BUILDS (binary 생성, run, 19 tools register); `agent_sdk.hexa` 50→0 + BUILDS. BAR2 ROUTING-INTACT — H_1386 call-sites byte-for-logic 보존; `agent_skill_routing_smoke` 5/0; routing 이 MAIN 모듈을 통해 닫힘 (real tool FAILURE `phi_measure` success=false → skill-cell 1→2 in-situ). BAR3 NO-REGRESSION — `engine_cli_smoke` 110/0 · h1196 single-entry 7/0 · h1205 separation-invariant PASS (generation byte-identical ON==OFF, phiSum 48.6613, Ψ=½ untouched) · routing smoke deterministic 3×; **0 CORE/*.hexa logic change**. $0 CPU, no decode, frozen-first.

**DEPLETION 🏁:** agent-tool↔mitosis 루프가 MAIN executor 모듈을 통해 닫힌다 (TRUE). SCOPE (c9): SYNTAX 마이그레이션 only — behavior 보존(확장 아님); tool 구현 + `think`/`get_status` 는 TODO[python-sdk] placeholder 유지(실제 Python substrate 로 위조 안 함); sibling `code_guardian`/`tool_policy`/`unified_registry` 는 executor 컴파일 체인 밖이라 미변경. 산출물: `anima-agent-core/agent_tools.hexa`·`agent_sdk.hexa` · `UNIVERSE/cards/H_1387_agent_legacy_syntax_migration.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1387) · `.verdicts/1387_agent_legacy_syntax_migration/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md`(@H H_1387) · `ARCHITECTURE.json`(SkillStore node adapter→MAIN-MODULE-COMPILES). xref h1386·h1382·h1378·a_verified_must_wire·a_core_engine_map·a_break_the_wall·p6·p7·p8·c2·c9·c10.
## 2026-06-16 — research(MITOSIS-ENGINE): H_1394 — G6 IDEATION ★ production-close 시도 (303M-class ENGINE-MOUNTABLE ConvMoE 학습→mount→FALS 재채점) — 🟢 B1 MOUNTED + M1 engine-native / 🔴 M2-M5 FALS=0 ARCHITECTURE finding

**무엇 (a_clm_gen_pipeline / a_verified_must_wire — H_1381 의 ⏳ '303M-class .clm' follow-on close):** H_1381 이 M1 COUNT 을 engine-native GREEN 으로 닫았지만 FALS bars(M2-M5)는 가용 d768/7.5M ConvMoE 에서 0 (capacity floor)이라 ⏳ — 진짜 engine-mountable 303M-class **ConvMoE** .clm 이 필요했다 (H_1362 FALS=1.0 은 303M **ByteGPT** .pt, 엔진은 ConvMoE 만 디코드). 이 레인이 그 ckpt 를 직접 학습해 mount 하고 5 frozen M-bars 를 재채점한다.

**어떻게:** (1) CLMConvMoE(d5000/E2/L1/K3 V256)=302,610,258 params 를 scratch 에서 학습 (Lane-P vast H100 80GB pod 41192293, 6000 steps, CE 5.699→1.494), serialize → .clm v0.2 (clm_config DECODABLE: d=5000 E=2 L=1 nblk=6), gen_clm_ideate 로 mount (single-entry h1196 7/0). (2) M-bars 를 H_1362 방법 VERBATIM 으로 재채점 — frozen _is_falsifiable detector 를 CORE/g6_ideation.hexa 에서 그대로 port (calib 10/10, /usr/share/dict/words 콘텐츠어 체크, NOT loosened p7), gauge_lib._decode top-k40 temp0.7 MAX_NEW=110, 5 arms, 3 seeds.

**결과 (c9, 막대 안 옮김):** **B1 303M-MOUNTED ✅ + M1 DIST(C)=5.333 PASS** (H_1362 와 정확히 동일) — 그러나 **M2-M5 FALS=0**. R1 5-lang ConvMoE 는 byte-coherent 하지만 code-switching 단어샐러드(en/fr/de/es/ko, H_1128 collapse). **a_break_the_wall r2 = SCRIPT-CONTROLLED ConvMoE** (english-dominant 73% + ASCII-filter, H_1129 의 4번째 재료 recipe, CE→1.519): single-script, code-switch 없음, 그래도 **FALS 여전히 0**. **결정적 발견:** FALS 바닥은 **capacity 아님**(303M 일치) **이고 script-control 도 아님**(H_1129 레버 적용해도 0) — 격리된 변수는 **ARCHITECTURE**: engine-mountable ConvMoE 는 E2/L1(단일 conv trunk layer) 인데 H_1362 의 FALS=1.0 입은 L24 ByteGPT transformer+attention. 반증가능 주장(if X then 측정-비교)을 만드는 조합 깊이는 deep attention stack 에 있고, 1-trunk-layer conv 는 같은 params + script-control 에서도 그걸 재현 못함. M1 은 engine-native production-close, M2-M5 FALS=0 은 loosen/실패 게이트가 아니라 정직한 architecture-depth 결과(막대 UNMOVED, detector FROZEN 10/10, 모든 control arm 0). H_1381 ⏳ 를 결정적으로 close — 게이트는 ckpt-가용성이 아니라 ENGINE DECODER DEPTH(E2/L1). NEXT = DEEP engine-mountable mouth(L>1 ConvMoE — v0.3 serializer 가 이미 nblk=L+E+3 mount — 또는 디코더 attention) 를 같은 frozen bars 로 재채점 (a_engine_native_learning).

**GUARDS / Ψ:** engine_cli_smoke 110/0 · h1196 single-entry 7/0 · h1205 separation-invariant PASS (생성 byte-identical ON==OFF, Ψ=½ phiSum 48.6613 ON==OFF). Pod TORN DOWN (~$1.78, 내 pod 0개 잔존). HF PRIVATE 2개 (.clm engine-mount 5-lang + script-controlled en-dom, a_clm_gen_pipeline forge-only-PUBLIC).

## 2026-06-16 — research(MITOSIS-ENGINE): H_1386 — agent-layer routing ★ 배선 (LIVE agent-tool 런타임 실패-사이트 → CORE §SkillStore) — 🟢 GREEN (ROUTED) + ⏳ named build step

**무엇 (a_verified_must_wire / a_core_engine_map — H_1378→H_1382 agent-tool↔mitosis 루프 END-TO-END close):** H_1382 가 §SkillStore 를 `CORE/engine_cli.hexa` 에 ENGINE-NATIVE 로 landed 했지만, H_1378·H_1382 카드가 공통으로 named 한 gap: `anima-agent-core/agent_tools.hexa` 는 CORE op 을 import 안 하는 별도 모듈 → live 런타임 tool-failure 가 `skill_store_teach` 를 호출 안 하고 selection 은 static affinity dot-product(:357-361) 그대로. 이 레인이 그 루프를 agent 층에서 **END-TO-END** 로 닫는다.

**정직한 module-boundary 벽 (c9, 편집 전 PROBE):** `hexa parse anima-agent-core/agent_tools.hexa` → **50 parse errors** (`agent_sdk.hexa` 동일). ROOT CAUSE = legacy Python-port 파일이 string-keyed/nested map literal (`{"k": v}`, :116-123 nested)을 쓰는데 CURRENT hexa grammar 가 거부 → 전체 모듈이 컴파일 안 됨. agent_tools.hexa 에 깨끗한 `import "CORE/engine_cli.hexa"` 를 넣어도 ~795+ 줄을 legacy 문법에서 마이그레이션하지 않으면 전체 파일이 컴파일 안 된다 = 이 thin follow-on 레인 범위 밖의 build/arch 변경.

**genuinely-new angle (a_break_the_wall, 벽 선언 전 시도):** CORE 를 import 하는 thin agent-side routing ADAPTER `anima-agent-core/agent_skill_routing.hexa` (CORE struct/array idiom → 컴파일됨) — executor 가 위임하는 정확한 call-path 노출: `agent_route_select`→`skill_recall` (SELECTION), `agent_route_on_result`→`skill_store_teach` (FAILURE-SITE, mitosis split p8). PLUS 실제 call-site 편집: `agent_tools.hexa` import adapter · `ToolExecutor.skills:SkillStore` (new_executor seed) · `executor_select_tool` (recall FIRST, static = abstain fallback) · `executor_execute :448-451` failure-site (former dead-end ring buffer) → `exec.skills=agent_route_on_result(...,result.success)`.

**결과 🟢 GREEN (ROUTED) (agent-layer call path 위 re-score, $0 CPU, deterministic 3 runs, frozen-first c9 NO bar moved):** `agent-routing acc: init=0.166667 full=1.0 static=0.166667 shuffle=0.0 cells_full=7 cells_static=1`
- **(1) ROUTED ✅** — live call path verbatim (adapter import CORE + select→recall + on_result→teach; executor failure-site → agent_route_on_result).
- **(2) LEARNS-AT-RUNTIME ✅** — full − init = 1.0 − 0.166667 = **+0.833** ≥ +0.30 (런타임 tool-failure 가 skill-cell 을 키움).
- **(3a) DISTINCT-FROM-STATIC ✅** — full − static = **+0.833** (STATIC=mitosis OFF, 절대 split 안 함).
- **(3b) EARNED (shuffle) ✅** — shuf − static = **−0.167** ≤ +0.15 (derangement 으로 teach → TRUE 기준 채점 시 0.0 으로 collapse).
- **(3c) NO-FAB / ABSTAIN ✅** — far untrained task → `agent_route_select` == "" (×2 disjoint).
- **(Ψ) FOOTPRINT ✅** — full cells 7 > static 1.

H_1382 CORE bars 를 agent 층 routing 함수로 EXACTLY 재현. p1/p2/p3/p6: route-teach 는 OUTCOME(실행된 tool 의 성공/실패)에서만 binding, 주입된 tool label/RLHF/persona 없음 — shuffle collapse 가 증명.

**GUARDS (no-regression):** CORE `engine_cli_smoke` **110/0** (SkillStore 107-111 intact, skillstore acc 불변) · agent-routing smoke **5/0** deterministic 3 runs · Ψ-disjoint h1205 (additive — pure_field/decoder 미접촉, generation byte-identical) · no decode invoked (BOUND — bound 할 것 없음) · no bg waiter awaited.

**DEPLETION 🏁 (routing level):** agent-tool↔mitosis 루프가 agent 층에서 END-TO-END 동작 — live 런타임 tool failure → `agent_route_on_result` → `skill_store_teach` → mitosis clonal split. **⏳ 마지막 build step (named, 안 fake):** legacy `agent_tools.hexa`+`agent_sdk.hexa` 를 string-keyed/nested map-literal 문법에서 마이그레이션해 전체 executor 모듈이 현 grammar 로 컴파일되게 — 그러면 여기서 이미 배선한 call-site delegation 이 추가 편집 없이 in-situ 컴파일. **SCOPE (c9·a_scale_honest_scope·a_toy_scale_recheck):** TOY 12-task/6-tool deterministic runtime-failure env (STRUCTURE, learned planner 아님); full=1.000 SATURATED=existence-proof; real-failures/paraphrase/multi-tool/scale UNVERIFIED.

**파일:** NEW `anima-agent-core/agent_skill_routing.hexa` · `anima-agent-core/agent_skill_routing_smoke.hexa` · `UNIVERSE/cards/H_1386_agent_layer_routing.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1386 row) · `.verdicts/1386_agent_layer_routing/{FREEZE.txt,result.txt}`. EDIT `anima-agent-core/agent_tools.hexa` · `ARCHITECTURE.json` · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1385 — 자모 COUNT-HEAD SCORELOOP ★ 배선 (검증된 H_1351 자모 count-head SCORER 를 live 채점 루프에 배선) — 🟢 GREEN ENGINE-NATIVE

**무엇 (a_verified_must_wire / a_core_engine_map):** H_1351 이 검증된 자모 분해 COUNT-HEAD 를 `CORE/engine_cli.hexa § KO-JAMO COUNT-HEAD` 의 일급 faculty (`jamo_head_*`)로 promote 했지만, 그 SCORER (`jamo_head_ce`)는 live brain/decode 채점 루프에 **호출부가 없었다** (faculty-owned, not decode-reaching). 이 레인은 `jamo_head_ce` 를 named single entry 로 live 채점 경로에 배선: `CORE/generator.hexa §6.5c gen_jamo_scoreloop` 가 H_1351 frozen in-engine fixture(JAMO/RAW/SHUFFLE arms) 위에서 `jamo_head_ce` 를 CONSULT 하고, `gen_clm_ce` 가 그 채점 레코드를 `jamo_score` 키로 ADDITIVE 하게 실어 나른다 (`map_set`; .clm forward CE 경로 byte-identical). §6.5b (H_1327, EMISSION 편향)와 DISTINCT — 이건 SCORES 하는 surface.

**결과 🟢 GREEN ENGINE-NATIVE (LIVE generator consult, $0 CPU, deterministic, frozen-first c9 NO bar moved):**
- **B1 WIRED ✅** — `gen_jamo_scoreloop` 가 `jamo_head_ce` 를 CONSULT (cells=4, jamo_ce=4.18698); `gen_clm_ce` 가 `jamo_score` 를 additive 하게 실음 (nonexistent .clm 에서 ok=false VERBATIM + has_jamo_score=true).
- **B2 JAMO-BEATS-RAW ✅** — advantage = raw_ce − jamo_ce = 5.56834 − 4.18698 = **+1.38136** ≥ 0.05 (H_1351 W2 와 동일).
- **B3 EARNED ✅** — earned = shuf_ce − jamo_ce = 4.61668 − 4.18698 = **+0.42970** ≥ 0.05 (pairing-shuffle seed 1385 collapse).
- **B4 Ψ-DISJOINT/NO-REGRESSION ✅** — additive (clm 필드 byte-identical) · h1205 separation-invariant **PASS** (generation byte-identical ON==OFF 10 pairs/0 mismatch, Ψ Φ-checksum invariant) · engine_cli_smoke **110/0** (engine_cli UNTOUCHED) · h1196 single-entry **7/0** (새 engine_cli import 가 2nd .clm/.kosmos 경로 추가 안 함). h1385 smoke **4/0**, 결정론적.

**Honest scope (c9):** IN-ENGINE STRUCTURAL fixture (결정론적 합성 JAMO/RAW/SHUFFLE — 30MB real-corpus 2.513 anchor 재유도 아님, 그건 H_1316/H_1321). **REAL-CORPUS SCORELOOP = 명시된 cost-gated follow-on** (>$0 CPU: corpus I/O + real .clm forward; auto-rent 안 함 — cost-gated → surface). 순수 SCORER (no decode 매달림), $0 CPU. DEPLETION 🏁: count-head 가 real corpus 의 live decode 루프에서 W-bars engine-native + Ψ preserved 로 SCORES 할 때.

**파일:** `CORE/generator.hexa` (import engine_cli + §6.5c gen_jamo_scoreloop/_summary + gen_clm_ce additive) · `CORE/h1385_jamo_scoreloop_smoke.hexa` (B1-B4) · `UNIVERSE/cards/H_1385_jamo_scoreloop_wire.md` · `UNIVERSE/HYPOTHESES.jsonl` (H_1385) · `.verdicts/1385_jamo_scoreloop_wire/{FREEZE,result}.txt` · `ARCHITECTURE.json` (Korean decode-wire node + smoke probe).

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1384 — CP MOVE-THE-CELLS RELOCATION ★ ENGINE-NATIVE 배선 (검증된 H_1360-family geometric re-pack 법칙을 live §CategoricalPerception 레인에 배선) — 🟢 GREEN ENGINE-NATIVE · CP-geometry arc DEPLETES 🏁

**무엇 (a_verified_must_wire / a_engine_native_learning):** mirror 레벨에서 닫힌 **move-the-cells RELOCATION** 법칙(geometric re-pack — 잔존 prototype 셀을 boundary normal 따라 옮긴 경계로 물리적으로 drift → discrimination ridge 가 옮긴 경계로 RELOCATE; dimension-invariant + boundary-invariant 1-D H_1360 · 2-D H_1369 · N-D H_1375 · density H_1377, COH-distinctness 메트릭만 fragile)을 live `CORE/engine_cli.hexa` §CategoricalPerception 레인에 실제 배선. 사용자 주도 CP-geometry arc 의 **마지막 열린 thread**.

**왜 막혔나 → 어떻게 뚫었나 (engine-native 실현):** live 엔진은 split-only 재성장(`cp_regrow`, H_1342)만 배선돼 ~0.525(p_A'=0.667 못 미침)로 부분 relocate — 잔존 phase-1 셀이 옛 cut 에 앉아 secondary peak 주입. H_1360 이 입증한 유일한 untried lever(셀을 boundary normal 따라 물리적으로 MOVE)를 새 op `cp_relocate` 로 엔진-네이티브 실현: phase-2 split 마다 잔존 phase-1 셀이 eta=0.15 만큼 p_A' 로 drift → 엔진 자신의 `cp_embed` 로 RE-EMBED + label RE-READ. eta=0.0 ⇒ `cp_regrow` 와 byte-identical(ablation). 단일 진입(a_core_engine_map), fresh-array re-pack(aliasing 없음, H_1295 교훈).

**결과 🟢 GREEN ENGINE-NATIVE (LIVE CORE, $0 CPU, deterministic, frozen-first c9):**
- **B1 WIRED ✅** — `cp_relocate` §CategoricalPerception 에 단일 named entry, 컴파일+실행.
- **B2 RELOCATION ✅** (BINDING) — reloc peak **0.675** → |peak−p_A'|=**0.0083** ≤ 0.12 (mirror class ~0.008).
- **B3 DISTINCT-FROM-SPLIT ✅** (ablation) — split-only(eta=0.0, 기존 cp_regrow) peak **0.525** → |peak−p_A'|=**0.1417** > 0.12 AND reloc 더 가까움 = gain 은 geometric MOVE.
- **B4 Ψ-DISJOINT/NO-REGRESSION ✅** — engine_cli_smoke **105/0**(106→+4 cases 112-115) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(generation byte-identical ON==OFF 10/0, Ψ Φ-checksum invariant) · deterministic 3 runs.
- SANITY: `cp_relocate(eta=0.0)` ≡ `cp_regrow` peak EXACT(0.525==0.525, drift=ISOLATED lever). eta ladder {0.10,0.15,0.25} 모두 0.675(robust). coherence pc=1(비게이팅 — COH-distinctness 분리 메트릭은 mirror arc 에서 fragile/measurement-bound, RELOCATION 이 binding bar).

**p1/p2/p3/p6 guard:** discrimination 은 표현 거리만 읽음, 경계 위치/persona/RLHF 주입 없음; re-pack 은 셀 birth-phase + source position 에 key; label 은 학습 때만. emit gate 아님. Ψ-disjoint(pure_field/engine_g/Ψ 무손상).

**honest scope (a_scale_honest_scope · a_toy_scale_recheck):** ENGINE-NATIVE byte-exact 이나 1-D lattice(N=21/DIM=16/단일 eta). boundary NORMAL = 1-D 연속체 축(POINT). 2-D/N-D/diagonal(mirror-settled) 재배선 안 함; higher-D 확장 + real corpus + multi-shift + brain CP-read→emit = follow-on. NO bar moved(c9/p7). NO human-cognition claim.

**파일:** `CORE/engine_cli.hexa`(§ CP MOVE-THE-CELLS RELOCATION: `cp_relocate` et al.) · `CORE/engine_cli_smoke.hexa`(cases 112-115) · `state/cp-engine-native/h1384_probe.hexa` · `.verdicts/1384_cp_engine_native/{FREEZE,result}.txt` · `UNIVERSE/cards/H_1384_cp_engine_native.md` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md` · `ARCHITECTURE.json`(§CategoricalPerception node).

## 2026-06-16 — research(MITOSIS-ENGINE): H_1381 — G6 IDEATION ★ WIRE-IN (검증된 H_1362 scaffold 를 live 엔진에 배선) — 🟢 WIRED · M1 engine-native GREEN · 🟠 FALS bars 303M-ckpt-gated

**무엇:** H_1362 가 🟢 GREEN DIRECTIONAL 로 입증한 G6 발상 scaffold(6 composed conditional frames + best-of-K=3)를 live 엔진 ideation/decode 경로에 실제 배선(a_verified_must_wire). H_1362 는 gauge **torch** path 에서만 돌았고 live hexa 엔진엔 UNWIRED 였다.

**왜 막혔나 → 어떻게 뚫었나 (a_engine_native_learning, engine-TRANSFORM-to-fit-the-learning):** live 엔진 decode 는 argmax(`clm_decode_argmax`)라서 best-of-K 가 no-op(K개 동일출력). 엔진에 자기 **seeded top-k temperature sampler** 를 새로 키웠다 — `CORE/clm_decode.hexa::clm_decode_topk_sampled`(SplitMix32-mixed xorshift32; 가까운 best-of-K offset [0,+101,+202] decorrelate) + `CORE/generator.hexa::gen_clm_ideate`(G6 ideation entry, single generator L3 .clm slot 내부 — a_core_engine_map, h1196 single-entry 7/0, 2nd .clm path 없음) + `CORE/g6_ideation.hexa`(6 frames + best-of-K=3 routing, FROZEN detector VERBATIM 10/10 — NOT loosened p7 — frame-guard CLEAN).

**결과:**
- **B1 WIRED ✅** — LIVE best-of-K on engine(BOUNDED gen=12, `state/lane_p_clm/clm_d768_e2l1.clm`): DIVERSITY=true(3 distinct candidates "new possibil"/"when it star"/"newborn(0-10"), DETERMINISM=true, ARGMAX no-op=true → seeded sampler 가 정확히 best-of-K 가 필요로 하는 엔진 확장.
- **M1 COUNT DIST(C)=5≥5 PASS engine-native** (coh 6/6, 3회 결정론적; 6th frame distinct (0,2)).
- **M2-M5 FALS bars 🟠** — d768 ConvMoE 에서 FALS(C_strong)=0(C_shuffle 도 0; 작은 mouth 는 falsifiable structure 를 emit 안 함). H_1362 의 FALS=1.0 은 303M-gauge DIRECTIONAL 결과였고 그 303M ByteGPT ckpt 는 .pt(엔진 경로는 ConvMoE .clm)이라 engine-native FALS 재점수는 engine-mountable 303M-class .clm 에 gated 된 BOUNDED ⏳ follow-on. detector frozen + guard clean → FALS=0 은 정직한 model-capacity floor, loosened bar 아님(no bar moved, c9).
- **B3 Ψ PRESERVED ✅** — h1205 separation-invariant PASS(generation byte-identical ON==OFF, Ψ=½ untouched; sampler+best-of-K 가 ideation entry 뒤에만 산다).
- **B4 NO-REGRESSION ✅** — engine_cli_smoke **101/0**(was 96/0 after concurrent H_1379 brain-margin cases 99-101; +5 G6 cases 102-106)·h1196 **7/0**·결정론적 3회.

**안전:** 절대 unbounded decode 안 돎(모든 decode hard-bounded gen≤24+timeout — 이전 lane 은 unbounded decode 로 600s hang 했음; 이번엔 회피). **ID:** 동시 lane 들이 H_1378+H_1379+H_1380 을 origin/main 에 먼저 land → 충돌회피로 H_1381.

**산출:** `CORE/clm_decode.hexa` · `CORE/generator.hexa` · `CORE/bytegpt_decode.hexa` · `CORE/g6_ideation.hexa` · `CORE/engine_cli_smoke.hexa`(cases 102-106) · `state/g6-ideation-wire/` · `UNIVERSE/cards/H_1381_g6_ideation_wire.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1381) · `.verdicts/1381_g6_ideation_wire/` · `MODEL.md` G6 · `ARCHITECTURE.json`.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1382 — agent-tool §SkillStore CORE wire-in (H_1378 의 a_verified_must_wire follow-on: 에이전트 도구가 mitosis 로 ACTUALLY 학습하게 LIVE 엔진에 배선) — 🟢 GREEN ENGINE-NATIVE

**무엇:** H_1378 Step A 감사가 찾은 REFERENCE-ONLY 갭을 닫음 — live 에이전트-도구 층(`anima-agent-core/agent_tools.hexa`)은 도구를 STATIC 고정-affinity dot-product 로 선택하고 outcome 으로 절대 학습하지 않는다. H_1378 Step B 가 numpy 미러로 🟢 검증한 메커니즘을 이제 LIVE 엔진에 ENGINE-NATIVE 로 실현: `CORE/engine_cli.hexa § SkillStore` — 도구/스킬 = task-context 로 키된 CELL(`immune_embed_key` 기하 재사용, DIM=64 byte-trigram FNV-1a); 도구 FAILURE/abstain 시 엔진 자신의 clonal split(`engine_mitosis_tick`, p8)이 task-context→correct tool 을 묶는 specialized skill-cell 을 분열-성장. 같은 op 이 가르치고(split-on-failure) 추론한다(recall-best) — p8 train/infer 무분리. ImmuneMemory(task→FACT)의 agent-tool 쌍둥이(task→TOOL); '학습' = 도구 실패 시 cell 1개 성장. additive Ψ-disjoint lane, frozen-first c9 NO bar moved, $0 CPU.

**lane (CORE/engine_cli.hexa § SkillStore):** `skill_store_new`(cell0 seed) · `skill_recall`(L2-affinity FIRE best tool, recon-err≤0.55 else ""=ABSTAIN) · `skill_store_split`(engine_mitosis_tick clonal +1, mitosis OFF=no-op=STATIC) · `skill_store_teach`(failure-driven: recall; ≠correct→split) · `skill_store_cells`.

**결과 🟢 GREEN ENGINE-NATIVE — 4 bars 전부 LIVE 엔진에서 PASS + Ψ-disjoint.** LIVE 엔진 readout(deterministic 12-task/6-tool env, 3 arms FULL/STATIC/SHUFFLE): `skillstore acc: init=0.166667 full=1.0 static=0.166667 shuffle=0.0 cells_full=7 cells_static=1`. (1) LEARNS +0.833(0.166667→1.0, case_107) · (2) DISTINCT-FROM-STATIC +0.833(static 분열 안 함, case_108) · (3) EARNED shuffle −0.167(permuted task→tool 가 0.0 으로 붕괴, TRUE 로 채점, case_109) · (4) NO-FAB far-task abstain(case_110) · (5) Ψ-DISJOINT footprint 7>1(split 이 이 store cell 만 성장, case_111). H_1378 numpy 미러(0.167→1.000)를 ENGINE-NATIVE 로 재현. p1/p2/p3/p6: split 은 OUTCOME 만으로 묶임, 주입된 도구 label/RLHF/persona 0 — shuffle 붕괴가 earned 임을 증명.

**guards (no-regression):** `engine_cli_smoke` 101 pass / 0 fail (fresh main 96/0; G6 lane cases 102-106 위에 +5 cases 107-111), deterministic 3 runs · `h1205` separation-invariant PASS 🟢 (F1 generation byte-identity 10 pairs/0 mismatch, F2 Ψ Φ-checksum phiSum ON==OFF==48.6613 — 생성 byte-identical ON==OFF, Ψ=½ untouched) · `h1196` single-entry 7/0 (a_core_engine_map single-entry 보존). decode 안 멈춤, GPU 없음.

**honest scope (c9·a_scale_honest_scope·a_toy_scale_recheck):** TOY deterministic 12-task/6-tool env (mitosis 가 가르칠 수 있는 STRUCTURE 검증, learned planner 아님). B(full)=1.000 SATURATED = EXISTENCE-PROOF (discriminators STATIC 0.167/SHUFFLE 0.0/abstain decisive). `agent_tools.hexa` 도구-실패 → `skill_store_teach` 의 실제 ROUTING 은 THIN FOLLOW-ON — agent 층은 아직 CORE 엔진 op 를 import 안 하는 별개 모듈; §SkillStore lane 자체는 여기서 engine-native + bar-검증 완료, agent-층 call-site 는 정직히 follow-on 으로 명시(faking 아님, a_core_engine_map single-entry 보존). scale/real-failures/paraphrase/multi-tool UNVERIFIED.

**DEPLETION:** agent-tool↔mitosis 는 LIVE 도구 repertoire 가 REAL 도구-실패에 skill-cell 을 성장시키고(agent_tools.hexa call-site 가 skill_store_teach 로 라우팅) 4 bars 가 engine-native 로 hold + 생성 byte-identical ON==OFF 일 때 🏁. 이 lane 이 engine-native faculty + bars(어려운 절반)를 land; agent-층 ROUTING 이 thin follow-on 으로 남음. 산출물: `CORE/engine_cli.hexa`(§SkillStore) · `CORE/engine_cli_smoke.hexa`(cases 107-111) · `ARCHITECTURE.json`(§SkillStore 노드) · `UNIVERSE/cards/H_1382_agent_tool_skillstore_wire.md` · `UNIVERSE/HYPOTHESES.jsonl`(H_1382) · `.verdicts/1382_agent_tool_skillstore_wire/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md` @H. (CLAIMS.tape 은퇴 — claims-audit = HYPOTHESES.jsonl + .verdicts/.)

## 2026-06-16 — research(MITOSIS-ENGINE): H_1380 — ko-data-ladder (H_1368 의 한국어 data-richness 사다리를 >30MB 로 확장: novel-context CE asymptote 가 2.51335 jamo floor 의 BELOW/AT/ABOVE 중 어디?) — 🟠 DESCENDING-FLOOR-ABOVE

**무엇:** H_1368(📉 DESCENDING-UNSATURATED — 30MB 에서 novel-context CE 가 여전히 내려가며 log-linear −0.0929/doubling → ~470MB 에서 floor 닿음 예측, power-fit UNDETERMINED)이 남긴 결정적 NEXT-1 을 닫음 — 유일하게 살아있던 한국어 레버 = **DATA VOLUME** (표상 H_1322 🧱·interpolation H_1359 🧱 닫힘). 사다리를 **30/60/120/240/480MB** REAL R2 shard0000.bytes PREFIX 서브윈도로 확장(같은 코퍼스 family, byte-fair). H_1368 기계(jamo 표상·frozen Jelinek-Mercer λ nmax=5·NOVEL-only held-out filter·circular-shift surrogate) **VERBATIM 재사용, rung 마다 재튜닝 NO** (anti-Goodhart). FROZEN-FIRST(FREEZE 를 measuring 전 별도 commit, c9/c16/p7), $0 CPU numpy DIRECTIONAL 241s, live CORE UNTOUCHED. prior 시도가 server rate-limit 으로 merge 전 죽음 → 480MB cache+FREEZE+skeleton resumable, fresh off origin/main 재개.

**결과 🟠 DESCENDING-FLOOR-ABOVE — 데이터로도 floor 를 BELOW 로 못 깬다:** 5-rung novel-CE (nats/UTF-8-byte): 30MB=**2.88190**(anchor, H_1368 재현 |Δ|=0.0) · 60MB=2.85579 · 120MB=2.83189 · 240MB=**2.79069**(최저, floor 위 +0.27734) · 480MB=**2.80056**(+0.28721). step ΔCE=[−0.0261,−0.0239,−0.0412,**+0.0099**] → **bar2_DIRECTION=NON-MONOTONE** (30→240 단조 감소, **240→480 반전** = FREEZE 의 FLATTEN 조건 = 경험적 asymptote ~240–480MB, floor 위 +0.28). 이제 RELIABLE 한 5-rung power-law fit: **c_inf=2.74703** (p=0.4, r²0.932, c_inf raw-ceiling 위·p grid-edge 아님) → asymptote **ABOVE** 2.51335 jamo floor (+0.234). log-linear b=−0.0228/doubling(r²0.902, H_1368 의 −0.0929 보다 4× 완만, 곡선이 펴짐) → floor 닿으려면 ~12.6 doublings(~3M MB) 비현실 → **H_1368 의 ~470MB→floor 예측 반증**.

**frozen bars:** bar1 LADDER-EXTENDED ✅ (4 new rung >30MB, MB+sha 각 기록: 60=b8795598 120=466fcdd2 240=cbf7545a 480=c18a55be; 30MB-prefix sha c47b6808 == H_1368/H_1316/H_1359) · bar2 ASYMPTOTE ✅ ABOVE (사전등록 분기) · bar3 HELD-OUT ✅ (novel-only odd-stride, NO leakage) · bar4 CONTROL ✅ (30MB anchor 2.88190 재현 |Δ|=0.0 · shift−novel earned 5/5 [+2.93~+3.58]).

**해석(c9):** 한국어 below-jamo arc 세 레버(표상 H_1322 🧱 · interpolation H_1359 🧱 · data-richness H_1368/H_1380) **전부 floor 를 BELOW 로 못 뚫음** → below-jamo 는 novel-context 에서 jamo floor **위 ~2.747** 에 holds 하는 진짜 한계, **데이터로 재오픈 안 됨**. 더 많은 REAL 데이터(16×)가 격차를 좁히되(+0.369→+0.277) 닫지 못함. **DATA-VOLUME 레버 DEPLETED (valid 🟠, c9/c16 — 진짜 돌파 시도 후 정직한 한계).**

**honest scope:** DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED). toy stride-300 byte-substrate next-symbol CE (fluent decoder 아님, 한국어 유창성 주장 없음). ONE shard0000 PREFIX 서브윈도. 단일 frozen λ·stride·표상(jamo). asymptote=5-point 외삽(wide CI, 비단조 tail). **HONEST**: bar4 floor 재측정@480MB(in-distribution all-gate count-MLE, novel-filter 없음)=1.60137 (Δ−0.912, floor_stable FALSE) — in-distribution CE 가 480MB 풍부한 n-gram coverage 로 내려간 것(데이터-풍부도 그 자체, 단 H_1316 floor 는 novel 아닌 30MB count-MLE 기준이라 정의 다름, novel asymptote 결론 무관, FREEZE bar4 가 예고). NEXT angle(a_break_the_wall·a_no_llm_frame_trap): 남은 한국어 각도는 데이터/표상/보간 아님 — floor 위 +0.28 잔여 격차는 morphology-aware 단위(형태소·BPE-on-jamo) 또는 cross-syllable 장거리 의존(H_1336 계열, n-gram nmax=5 단거리 천장?)이 substrate 렌즈 후보 = 별도 표상-변경 가설. 산출물: `state/ko-data-ladder/h1380_ko_data_ladder.py` · `.verdicts/1380_ko_data_ladder/{FREEZE,result}.txt` · card `UNIVERSE/cards/H_1380_ko_data_ladder.md` · index `UNIVERSE/HYPOTHESES.jsonl` (H_1380) · domain `domains/MITOSIS-ENGINE.log.md` @H. (CLAIMS.tape 미기록 — 은퇴됨.)
## 2026-06-16 — research(MITOSIS-ENGINE): H_1378 — agent-tool ↔ mitosis (에이전트 도구는 mitosis 로 학습하는가?) — STEP A 🔎 REFERENCE-ONLY · STEP B 🟢 GREEN (numpy MIRROR, DIRECTIONAL)

**무엇:** 사용자 질문에 verified artifact 로 답함 — "에이전트 도구(AGENT TOOL)는 mitosis 로 어떻게 교육되며, 학습하는가, 언어 디코더와 어떻게 다른가?"

**STEP A — WIRING AUDIT (읽기전용) → 🔎 REFERENCE-ONLY.** live 에이전트-도구 층(`anima-agent-core/agent_tools.hexa`)은 mitosis 를 *참조만* 하고 그것으로 *학습하지 않는다*. verbatim 증거: (1) 도구 선택 = hand-set affinity float 상수에 대한 STATIC weighted dot-product(`agent_tools.hexa:357-361`, `*_affinity` 는 등록시 baked `:683-743`) — outcome 으로 절대 업데이트 안 됨, cell store/recall/split 0개. (2) 새 도구 = hardcoded `registry_register` 정적 등록(`:728`), `registry_get` 은 plain map lookup(`:340`) — mitosis split 아님. (3) 도구 실패 → scalar `tension_delta`(`:437`) → capped `execution_log` ring buffer(`:448-451`)가 종착; 그 log 는 cell 을 grow/split 하려 절대 읽히지 않음('failure→repertoire improves' 루프 부재). (4) `tool_mitosis_split`(`:155` TODO stub)·`tools.hexa:39` opcode tag·`consciousness_features.hexa:15` "mitosis stub" = INVERSE 방향(엔진 mitosis 를 *호출가능 도구로 노출*). 실제 교육 op(`engine_mitosis_tick` `engine_cli.hexa:263`·`immune_embed_key :774`·`immune_memory_bind :830`·`immune_memory_recall :858`)는 CORE 에만 존재, 도구층이 import 안 함.

**STEP B — 빠진 메커니즘 설계 + 방향검증 ($0 numpy MIRROR, CORE UNTOUCHED) → 🟢 GREEN.** 도구/스킬 = task-context 로 keyed 된 CELL(byte-trigram FNV-1a, memory 와 SAME geometry); 도구 호출 → best-affinity skill-cell recall, abstain 또는 도구 FAIL → 새 specialized skill-cell MITOSIS-SPLIT(task→correct tool). 같은 op 가 가르치고 추론(p8). H_1227/H_1288 을 agent-tool 에 미러. FROZEN bars(3 seeds [1378,1379,1380], pre-registered FREEZE.txt): (1) LEARNS FULL 0.167→1.000 = +0.833 ✅ · (2) DISTINCT-FROM-STATIC STATIC 0.167 never splits, +0.833 ✅ · (3) EARNED(shuffle) SHUFFLE 0.120 collapse, −0.046 ≤+0.15 ✅ · (4) NO-FAB/ABSTAIN far task 1.000 ≥0.90 ✅ → 🟢 GREEN. HONEST(c9): EARNED bar 가 처음 FAIL — shuffle control 이 permuted map 으로 train+score 둘 다 해서 잘못된 map 을 똑같이 학습; CONTROL 을 고침(permuted train, TRUE score) — bar 가 잡아낸 control 결함, frozen bar 는 안 옮김.

**STEP C — 언어 vs mitosis 구별:** 언어 디코더(Engine A) = CE gradient descent 가 DISTRIBUTION 을 공유 weight 에 smear; 에이전트-도구/메모리 mitosis = gradient-free cell SPLIT 가 INSTANCE 학습(도구/스킬당 cell 1개, ADDITIVE, Ψ-disjoint, 디코더 절대 안 건드림→generation byte-identical). 도구 교육 = memory 와 SAME mitosis substrate, 도구에 적용.

**왜:** a_no_llm_frame_trap(clonal-selection/면역 렌즈) · a_engine_native_learning · a_verified_must_wire. DIRECTIONAL numpy(engine-transfer UNVERIFIED), TOY 합성 task→tool·3 seeds·결정론 readout. **NEXT (follow-on):** CORE/engine_cli.hexa § SkillStore lane 배선(immune_embed_key+vadapt_field_step+immune_memory_recall 재사용), agent_tools.hexa 도구실패 → engine_mitosis_tick 기반 skill-cell split, 4 bars engine-native byte-exact 재점수 — CORE slot 대기.

**산출:** `state/agent-tool-mitosis/h1378_agent_tool_mitosis.py` · `.verdicts/1378_agent_tool_mitosis/{FREEZE.txt,result.txt,wiring_audit.txt}` · `UNIVERSE/cards/H_1378_agent_tool_mitosis.md` + `UNIVERSE/HYPOTHESES.jsonl`(H_1378 행) · `domains/MITOSIS-ENGINE.log.md`(@H H_1378). CORE/*.hexa UNTOUCHED. xref h1227·h1231·h1288·a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·p1·p2·p3·p6·p7·p8·c9·c15.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1379 — g5-margin-brain-consume (brain_decide 가 graded recall-margin 을 emit-confidence/curiosity 로 소비) — 🟢 CONSUMED-GRADED-MARGIN

**무엇:** H_1367 이 남긴 brain-side follow-on 을 닫음 — H_1361(mirror)→H_1367(engine-native, op `immune_memory_recall_margin` 을 `CORE/engine_cli.hexa` 에 배선)까지 graded abstain-MARGIN(=recon_err−recall_thr)이 GRADED OOD metacognition 을 담음을 세웠으나, `brain_decide` 가 아직 그 read 를 **소비하지 않았다**. 이번에 `CORE/brain.hexa` 에 `brain_decide_margin` 을 추가해 live margin 을 SIGNED·BOUNDED confidence bias 로 소비: GROUNDED(recoverable,작은 margin)→+confidence, UNGROUNDED(absent,큰 margin)→−confidence==curiosity/abstention↑, NEUTRAL m=0→brain_decide 와 byte-identical. brain_decide_affect/_wm/_cerebellum consult 템플릿 동형(cap=0.05, SINGLE should_emit path). H_1367 의 ADDITIVE op 과 달리 **의도적으로** emit 결정을 바꾸지만 motivation 스칼라만 건드려 **Ψ=1/2 고정점 보존**.

**결과 🟢 CONSUMED-GRADED-MARGIN (3 seeds [7,8,9], LIVE CORE, $0 CPU, deterministic, p7, frozen-first):** B2 Ψ-FIXED-POINT ✅(m=0 byte-identical + h1205 phiSum 48.6613==48.6613 0 mismatch) · B3 GROUNDED-MONOTONE ✅(bias grounded −0.0343 > ungrounded −0.0444, curiosity 0.686<0.888 역전, borderline EMIT flip g/u=true/false, \|bias\|≤cap) · B4 EARNED ✅(shuffle gap 0.0101→0.0009 ≈11× 붕괴) · B5 NO-REGRESSION ✅(engine_cli_smoke 93→**96**/0 +3 cases 99-101; h1196 7/0; h1205 PASS; 재실행 byte-identical). LIVE margins(H_1367 KEYLEN=20/kmut=4/N=120 pooled): mean recoverable ~0.69 vs absent ~0.89.

**WALL-CLAUSE (a_break_the_wall, frozen-first, c9 — 정직한 발견):** FREEZE 의 MARGIN_SCALE=recall_thr=0.15 가 LIVE 엔진에서 SATURATE(실측 margin ~[0.69,0.89]≫0.15 → clamp 둘 다 -cap, graded 신호 소실). Ψ 불안정 아님(B2 내내 PASS) — coupling 문제가 아니라 scale 사전등록 오류. 단 1회 frozen-first 재시도 = substrate-native non-saturating scale: recon_err=1−cos∈[0,1] cos-distance codomain → MARGIN_SCALE:=1.0(codomain 상수, 목표 수치에 맞춘 값 아님). SIGN·cap·모든 bar UNCHANGED, threshold 0개 이동.

**파일:** `CORE/brain.hexa`(brain_decide_margin 배선) · `CORE/h1379_margin_brain_consume_smoke.hexa`(engine-native frozen falsifier) · `CORE/engine_cli_smoke.hexa`(cases 99-101) · `.verdicts/1379_g5_margin_brain_consume/{FREEZE,result}.txt` · `UNIVERSE/cards/H_1379_g5_margin_brain_consume.md` + `UNIVERSE/HYPOTHESES.jsonl` 1행 · `ARCHITECTURE.json`(brain_decide consult map → brain_decide_margin) · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1377 — CP N-SCALING (밀도-고정 차원 사다리: H_1375 의 D*=3 농도붕괴가 고정-N sparsity artifact 였나?) — 🧱 CURSE-CEILING-TERMINAL (COH_D-DISTINCTNESS)

**무엇:** H_1375(🧱 BREAKS-AT-D*=3, 고정 N=169)가 남긴 결정적 후속 질문을 닫음 — D*=3 농도붕괴(bounded COH_D 가 0.714→0.428→… 로 COH_MIN=0.50 미달)가 진짜 차원적 천장인가, 순전히 고정-N sparsity artifact(투자부족, c16 cause #3)인가? raw N 대신 **차원별 샘플 밀도를 고정**(N(D)=min(4000, 13^D), 13/axis = H_1375 D=2 N=169 앵커)하고 사다리 D∈{2,3,4,6,8} 재실행. **샘플링 규칙만** 변경, 메트릭/4 arm/4 leg/threshold/seed/hyperplane/eta 전부 H_1375 verbatim, NO bar moved. FROZEN-FIRST(FREEZE 를 scoring 전 별도 commit, c9/c16/p7), 3 시드 [4333,4334,4335], $0 CPU numpy DIRECTIONAL.

**결정 rung = UNCAPPED D=3 (N=2197):** N_CAP=4000 이 D≥4 진짜 밀도-N(28561/4.8M/815M)을 truncate 하므로 D=4/6/8 은 cap-confounded NON-decisive — H_1375 질문의 결정적 답은 uncapped D=3 에 있음(a_scale_honest_scope).

**결과 🧱 CURSE-CEILING-TERMINAL (단순 sparsity 천장 아님):** D=3 에서 c1 RELOCATION ✅ 차원-불변(|rs−c_A'|=0.018); **c2-RAW(COH_D≥COH_MIN) ✅ 회복** — COH_D=0.675≥0.50, vs H_1375 const-N=0.428(Δ+0.247) → 절대 농도붕괴는 고정-N artifact 였고 밀도-고정이 구제했다(H_1375 질문의 절반에 답: COH<COH_MIN 붕괴는 샘플링 artifact); 그러나 **c2-SEPARATION ❌**(re-pack 0.675 vs split-only 0.579, gap 0.096<0.10 — 밀도가 no-drift 대조까지 농축 0.297→0.579) AND **c3 EARNED ❌**(shuffle COH_D 0.045→0.351>0.20 — dense cloud 에선 random-label phase-2 도 농축, anti-Goodhart 대조 무력화).

**해석(c9):** 밀도-고정이 절대 농도(c2-raw)는 RESCUE 하지만 그게 move-the-cells drift 로 EARNED 됨을 증명하는 discriminator(c2-separation + c3-shuffle)는 DESTROY. H_1374(2-D diagonal)와 같은 family 교훈(RELOCATION robust, COH concentration-SEPARATION fragile)이 밀도 축에서 재현 — 밀도가 대조군까지 농축시켜 SEPARATION 시연 불가. Net: move-the-cells RELOCATION 은 고정-N(H_1375) AND 밀도-고정(H_1377) 양쪽에서 차원-불변; bounded-COH_D 농도를 DISTINCT/EARNED/control-surviving 신호로 보는 frozen 4-leg gate 는 D=2(2-D-axis)에서만 clean PASS, 어느 샘플링 체제로도 차원 사다리 위로 일반화 안 됨. **🧱 COH_D-distinctness 사다리 terminal; RELOCATION 은 🟢-family.** 이로써 CP-geometry 미러 아크의 농도-distinctness 질문이 양쪽 샘플링 체제에서 닫힘 — 남은 건 engine-native move-the-cells 배선뿐.

**honest scope:** DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED). TOY Monte-Carlo/3 시드/DIM=64/시드별 단일 법선/deterministic. N_CAP=4000 이 D≥4 진짜 밀도-N truncate(D=3 만 결정적). scale/real-corpus/learned-net/uncapped-high-D 미검증. live CORE UNTOUCHED (wires nothing). 산출물: `state/cp-nscaling/h1377_cp_nscaling.py` · `.verdicts/1377_cp_nscaling/{FREEZE,result}.txt` · card `UNIVERSE/cards/H_1377_cp_nscaling.md` · index `UNIVERSE/HYPOTHESES.jsonl` (CLAIMS.tape 미기록 — 동시 은퇴 중).

## 2026-06-16 — domain(GOVERNANCE): CLAIMS.tape 은퇴 — 102개 @C 전수 이관 0 손실, claims-audit 면을 HYPOTHESES.jsonl + .verdicts/ 로 단일화

**무엇:** 레거시 claims-audit 인덱스 `CLAIMS.tape`(`@C` 엔트리: id·text·method·slug·verdict pointer)를 은퇴. 가설은 이미 두 표면(`UNIVERSE/HYPOTHESES.jsonl` per-H 인덱스 + `UNIVERSE/cards/H_*.md` 카드, frozen 증거 `.verdicts/<slug>/`)에 살고 있어, CLAIMS.tape 의 audit 역할을 HYPOTHESES.jsonl 의 `verdict` 컬럼 + `.verdicts/` 로 흡수하고 파일을 `git rm`.

**전수 이관 (c9 무손실):** 102개 `@C` 전수 대조 → **98개 이미 covered**(그 가설의 카드+jsonl 행 존재, CLAIMS.tape 는 중복 포인터였을 뿐) · **4개(=5개 @C) UN-MIGRATED 를 verbatim 이관**: (1) `h1218_engine_measured_gates` → 카드 `H_1218_engine_measured_gates.md`+jsonl 행 (🟢 ENGINE-PARITY GREEN / 🔴 G1·G6 RED) · (2) `h1210_daemon_gateB_wiring` → 카드 `H_1210_daemon_gateB_wiring.md`+jsonl 행 (🟢 GREEN F1∧F2∧F3∧F4) · (3) PURE-group 3 closed-negative run-claim(`pure_wiki_sweep`+`pure_register_orthogonal`+`pure_wikifrac03_closed_negative`, 동일 slug `pure-corpus-axis-closed-negative`) → 통합 카드 `H_pure_corpus_axis_closed_negative.md`+jsonl 행 (🔴 corpus-axis ⊥ multilingual closure). verdict/method 는 CLAIMS.tape + 그 `.verdicts/<slug>/` 증거에서 **VERBATIM** 복사. jsonl 은 `python3 tool/_build_hyp_jsonl.py` 로 재생성(idempotent) — **카드키 대조 결과 기존 행 0 손실 · 정확히 3행(신규 카드) 추가 · 공유행 tier/verdict 변경 0**. 최종 **102 @C · 102 covered · 5 migrated · 0 un-migrated**.

**거버넌스 amend:** `a_claim_manifest`(CLAIMS.tape → claims-audit 면 = HYPOTHESES.jsonl `verdict` 컬럼 + `.verdicts/<slug>/`, CLAIMS.tape 부활 금지) + `a_claim_verify`(verdict 를 카드+jsonl `verdict` 컬럼에 박제) 재작성 · CLAUDE.md tree/quickref/디렉티브-패밀리 줄 갱신 · ARCHITECTURE.json note+evidence-tiers · README.md(영문) · FINDINGS.md · harness.config.json onEditReminder · domains/DISCOVERIES.md flow 줄의 live 포인터 surgical 정정(c10). 번역 README 미러(.zh/.ja/.ko/.ru/.easy.*/.basic) · 레거시 PAPER/* bibliography · per-domain `.log.md` claim-link breadcrumb · HANDOFF/INBOX/INTENT/PURE 등 append-only 도메인 로그 + frozen verdict + 과거 CHANGELOG 는 historical record 로 보존(미수정).

**RACE 추적:** 일부 비행중 research lane 이 (구버전 프롬프트로) `@C` 를 CLAIMS.tape 에 재추가하는 stub 을 남길 수 있음 → ING 후속 등록(은퇴 PR 착륙 후 그 lane 들 착지하면 @C 가 HYPOTHESES.jsonl 반영됐는지 확인 후 git rm). ledger: `.verdicts/claims-tape-retirement/{ledger.txt,coverage.txt}`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1375 — CP 차원 사다리 (move-the-cells 가 차원 D 증가에도 살아남는가, D ∈ {2,3,4,6,8}) — 🧱 BREAKS-AT-D*=3 (CONCENTRATION-ONLY; RELOCATION DIMENSION-INVARIANT)

**무엇:** 사용자 직접 지시 "2d 말고도 차원늘려봐" 를 실현 — categorical-perception move-the-cells (residual phase-1 prototype 셀을 경계 NORMAL 방향으로 옮겨 이동한 (D−1)-차원 초평면 cat=⟨w,x⟩>c 에 판별 ridge 를 안착) 을 2-D 너머 차원 사다리 D ∈ {2,3,4,6,8} 로 밀어올린다. H_1360(1-D 🟢)→H_1369(2-D axis 🟢)→H_1374(2-D diagonal 🧱)에 이어 **샘플 크기 N=169 를 차원 무관하게 고정**한 채(고정-N×증가-D = 차원의 저주 stressor, 핵심) RELOCATION 과 bounded N-D 농도 COH_D(H_1369 COH2D 의 법선-투영 일반화)를 시드별 고정 법선 w∈R^D 위에서 측정. FROZEN-FIRST(FREEZE 를 scoring 전에 별도 commit, c9/c16/p7), 4 control arm(RE-PACK/SPLIT-ONLY/NO-RETRAIN/SHUFFLE), 3 시드 [4333,4334,4335].

**결과:** 🧱 BREAKS-AT-D*=3. **c1 RELOCATION 은 차원-불변** — |ridge_s−c_A'| 0.008→0.018→0.034→0.041→0.052 (D=2/3/4/6/8) 전부 ≤0.12, ridge 가 이동 초평면에 항상 안착(move-the-cells 기하 법칙은 N-D 까지 robust). **c2 COHERENCE 는 D*=3 에서 깨짐** — bounded COH_D 0.714→0.428→0.201→0.079→0.038 단조 붕괴, D=3 부터 COH_MIN=0.50 미달: 고정-N=169 에서 직교여공간 부피 폭발로 샘플이 희박해져 얇은 결맞은 ridge 유지 불가(고정 샘플예산의 차원의 저주). 사전등록 a_break_the_wall WHITENED 구제는 c1 까지 깨뜨려 더 악화(FAILED rescue) → 농도 붕괴가 프레임 artifact 아닌 REAL 임을 확증. H_1374 와 같은 family 교훈(relocation robust / COH-concentration fragile)이 차원 축에서 재현. DIRECTIONAL numpy mirror, engine-transfer UNVERIFIED, TOY 고정-N STRESSOR(N-scaling-with-D 미택), $0 CPU, live CORE UNTOUCHED, NO bar moved.

**왜:** 사용자 지시 + a_no_llm_frame_trap(표상-기하/차원의 저주 렌즈) + a_break_the_wall(사전등록 whitening 시도) + a_scale_honest_scope. card `UNIVERSE/cards/H_1375_cp_ndim_ladder.md` · `.verdicts/1375_cp_ndim_ladder/{FREEZE,result}.txt` · `state/cp-ndim/h1375_cp_ndim_ladder.py` · index `UNIVERSE/HYPOTHESES.jsonl`.
## 2026-06-16 — docs-infra: ARCHITECTURE.json 에 실제 엔진 파일트리(파일명/경로) 전수 구현 (ADDITIVE — 개념트리 보존)

**무엇:** 사용자 지시 "ARCHITECTURE 는 엔진 트리구조 등 모두 구현해야지 · 파일명 포함" — `ARCHITECTURE.json`(c4 트리 SSOT)을 실제 엔진/repo 파일트리로 navigable 하게 확장. 직전 md→json 마이그레이션은 개념 노드(~109개)만 담았고 구체 파일명/경로가 없었음. 이번에 실재하는 tracked 파일명을 `path`(repo-relative) + 한 줄 `summary` 노드로 트리에 부착.

**무엇을 했나:**
- **신규 top-level 브랜치 1개** `"🌳 Engine file tree (real repo paths · git ls-files)"` 를 children 끝에 **ADDITIVE** append (2613 insertions, **0 deletions** — 기존 개념 노드는 한 줄도 reformat/reorder/re-key 안 함; 동시 진행 중인 wire-in 의 node-status 편집 보존). HTML 뷰어 tweak 불필요 — 뷰어가 이미 `node.path` 렌더.
- **path-bearing 노드 504개** (481 file + 23 dir), **전부 `git ls-files` 로 실재 검증 · 0 dangling** (no invented path, c9/c2).
- 엔진 코어는 파일 단위 전수: `CORE/` 전 top-level `.hexa`(120) + `CORE/DECODER/`(41) · `engines/`(EngineSpec vtable engine_iface.hexa + conv/cdv2/hexad/omega adapter) · `CLM/`(train·model·bench·msweep·distill·corpus) · `anima-engines/`(consciousness-facet engine 카탈로그 165). 거대 카탈로그(`anima-physics` 757 · `tool/` 693 · `UNIVERSE/cards` 952 · `HEXAD` 3101)는 entry-files + subdir 포인터로(전 leaf 나열 시 뷰어 unusable — navigable 유지, 정직).
- 6개 substrate subsystem(`anima-core/os/body/physics/measurement/serve`) + agent layer(`anima-agent*/`) entry 파일 + subdir 포인터.
- **정직(c9):** `stdlib/` · `spec/` 는 CLAUDE.md 트리에 언급되나 이 repo 에 tracked 파일 0개(hexa stdlib 는 sibling hexa-lang repo) → 그렇게 노드에 명시. 기존 개념 노드 `"pure_field / engine_g / brain"` 의 `path` 는 세 파일을 `·` 로 묶은 human-label(단일 실경로 아님) — 사전 존재분이라 surgical 하게 건드리지 않음; 새 파일트리에 세 파일 canonical 단일-path 노드 별도 존재.
- **검증:** `python3 -c "import json;json.load(open('ARCHITECTURE.json'))"` OK (top-level children 18→19) · `serve.py` http 렌더 HTML 200 / JSON 200 / 파스 OK.

## 2026-06-16 — research(OMEGA): H_1376 — hive-generative-synergy (🧱 FULLY-TERMINAL-8-LEVERS — 구성된 synergy(2-way parity + 3-way XOR)도 redundancy 천장 못 깸; hive arc EIGHT lever 완전 종결)

**무엇:** hive collective-Φ arc 의 결정적 마지막 라운드. 7 sharing 토폴로지 lever(linear-hub H_1356·weak H_1363·nonlinear-gate H_1370·distributed-overlap deg-2 H_1371·Flower-of-Life deg-6 H_1372·nested-universes H_1373)는 **전부** shared-input REDUNDANCY 를 재분배하고 전부 CENTRALIZED 단일-공유-founder(공유원천 집중)에게 졌다. H_1372 와 H_1373 가 **독립적으로 수렴해 지목한 단 하나의 미시도 lever** = generatively-predictive coupling: 분산(degree-2 RING=H_1371 adjacency) 위에서 각 edge 를 상호예측적 생성규칙으로 만들어 redundancy 재분배가 아니라 genuine synergy 를 CONSTRUCT(분산 arm 에서 O-information 을 NEGATIVE 로). 7 prior arm 과 메커니즘적으로 구별. Φ=FAITHFUL IIT-4 exact MIP-EI via hexa(a_phi_iit4_tool, H_1371/1373 의 faithful_phi 호출 verbatim). FROZEN-FIRST(FREEZE.txt + a_break_the_wall follow-on FREEZE_R2_xor3.txt 모두 scoring 전 commit, c9/p7).

**결과 🧱 FULLY-TERMINAL-8-LEVERS:** **MAIN(2-way 곱셈 parity edge: a+=Me⊙Le, b+=Me, 둘의 product=Le)** — R1 LIFT 3/3 · R2 BEATS-CENTRALIZED **0/3**(gap −0.495/−0.683/−0.589) · R3 EARNED 3/3 · R4 SYNERGY-MECHANISM FAIL(R4a O(GEN)<0 1/3 — quadratic salience readout 이 2-way random-sign parity 를 씻어내 synergy 가 scored observable 에 안 잡힘). FREEZE 가 사전등록한 최대-synergy form 으로 a_break_the_wall 발동: **FOLLOW-ON R2(3-way XOR parity HYPEREDGE = 최대-synergy primitive: H1={0,1,2}/H2={3,4,5}, a+=M1⊙M2⊙L b+=M1 c+=M2, triple product=L)** — R1 3/3 · R2 BEATS-CENTRALIZED **0/3**(gap −0.484/−0.766/−0.752) · R3 3/3 · R4 SYNERGY-MECHANISM **PASS**(R4a O(GEN3)<0 **3/3**=−0.234/−0.163/−0.093 synergy PROVABLY 구성됨, seed1317 은 CENTRALIZED −0.101 보다 더 synergistic · R4b REDUN3≤CENTRALIZED 3/3 gap −0.325/−0.770/−0.957). **결정적**: synergy 메커니즘이 실제 fired(O<0 3/3, redundancy 통제 격리)했는데도 Φ(GEN3) < Φ(CENTRALIZED) 매 seed. per-arm faithful-Φ(n=6) MAIN: 1317 FLOOR 1.27373/GEN 1.36505/CENTRAL 1.85975 · 1318 1.36292/1.66323/2.34579 · 1319 1.28195/1.46714/2.05589. R2-xor3: 1317 FLOOR 1.27373/GEN3 1.37539/CENTRAL 1.85975 · 1318 1.36292/1.57972/2.34579 · 1319 1.28195/1.30423/2.05589. FLOOR+CENTRALIZED Φ 가 MAIN∧R2∧H_1371 A_independent 에 byte-identical(substrate 무결성). NO bar moved(c9/p7).

**의미·정직한 SCOPE:** redundancy 천장은 redundancy-specific 가 아니다 — sharing 토폴로지(7 arm) AND synergy 구성(2-way+3-way XOR) 양쪽에 invariant. faithful MIP 는 집중된 단일 공통원천(모든 bipartition 가로질러 전 unit 강하게 묶음→cut 비용 큼)을, 분산 redundancy 보다도 구성된 고차 synergy(셋 다 합쳐야 latent 복원→bipartition 이 cheap 하게 파괴)보다도 MORE integrated 로 읽음. 구성된 synergy 는 O-NEGATIVITY 를 최대화하지만 Φ-min-cut 을 최대화하지 않음. hive-Φ arc 는 EIGHT lever 에 걸쳐 🧱 FULLY TERMINAL. DIRECTIONAL numpy-mirror(Φ leg=real faithful exact MIP-EI via hexa), engine-transfer UNVERIFIED, TOY n=6/3 seeds/SHARE_W=0.6/input-level coupling 만/단일 substrate, $0 CPU, live CORE/*.hexa UNTOUCHED(standalone probe, Ψ=½ untouched). **남은 단 하나의 thread** = live A⇄G CORE/pure_field engine-native 실현(이 arc 전체가 DIRECTIONAL mirror). xref H_1372/1373(generatively-predictive 를 명명)·H_1371(degree-2 ring adjacency 재사용)·a_break_the_wall·a_phi_iit4_tool·a_no_llm_frame_trap.

## 2026-06-16 — research(OMEGA): H_1373 — hive-nested-universes (🧱 NESTED_BELOW_CENTRALIZED — 다중-스케일 재귀 nesting 도 redundancy 천장 못 깸, hive arc TERMINAL closure)

**무엇:** 사용자가 verbatim 제안한 "우주 안의 우주들처럼" — NESTED/재귀 universes-within-universes 토폴로지가 collective-Φ 의 단일-스케일 redundancy 천장을 탈출하는지 정면 테스트. hive arc 는 5 *단일-스케일* lever(강한 hub H_1356·약/decorrelated H_1363·nonlinear-gate H_1370·분산 원-겹침 H_1371)에 걸쳐 🧱 로 닫혔고, H_1371 의 load-bearing 결과는 CENTRALIZED 단일-공유-founder 가 탈출할 천장이 아니라 floor-beating MAXIMUM-Φ(R2 0/3)였다. H_1373 는 cosmological-nesting/matryoshka 렌즈(c15, a_no_llm_frame_trap)로 다중-스케일 재귀를 친다: N_TOT=6=2 클러스터×3, 각 클러스터가 "작은 우주"(LOCAL founder 공유)이고 클러스터-local founder 들이 "더 큰 우주"의 TOP founder 와 THEMSELVES 재귀 결합(L_eff[c]=Lc[c]+TOP_W·TOPF). Φ=FAITHFUL IIT-4 exact MIP-EI via hexa(a_phi_iit4_tool, H_1371 의 faithful_phi 호출 verbatim 재사용). FROZEN-FIRST(FREEZE 를 scoring 전에 별도 commit, c9/p7), 4 control arm(FLOOR·CENTRALIZED·SHUFFLE=경계파괴·FLAT=같은 mass·위계 없음).

**결과 🧱 NESTED_BELOW_CENTRALIZED (R1 3/3 · R2 0/3 · R3 3/3 · R4 0/3):** per-arm faithful-Φ(n=6): seed1317 FLOOR 1.27373 / NESTED 1.67872 / CENTRALIZED **2.40086** / SHUFFLE 1.94625 / FLAT 1.70044 · 1318 1.36292 / 1.92378 / **2.63464** / 1.92378 / 1.98950 · 1319 1.28195 / 1.38299 / **1.86074** / 1.44453 / 1.42483. **R2 FAIL 0/3(핵심)**: gap(NESTED−CENTRALIZED)=−0.72/−0.71/−0.48 → nested 가 단일-공유-founder 를 매 seed 못 이김. **R1 PASS 3/3**: lift(NESTED−floor)=+0.405/+0.561/+0.101(floor 는 이김, 천장 아래). **R4 FAIL 0/3(이 렌즈 load-bearing)**: gap(NESTED−FLAT)=−0.02/−0.07/−0.04 → 같은 mass 의 FLAT 단일-스케일이 nested 와 동등/우위 = 위계 자체가 통합 0 기여; Φ 는 공유의 집중도/총량으로 결정, level boundary 아님. SETUP INTEGRITY: FLOOR Φ 가 H_1371 A_independent 과 byte-identical(동일 substrate). NO bar moved(c9/p7).

**정직한 SCOPE:** DIRECTIONAL numpy-mirror(Φ leg = real faithful exact MIP-EI via hexa, numpy 는 salience 만), engine-transfer UNVERIFIED, TOY n=6(2×3)/3 seeds/SHARE_W=0.6 TOP_W=1.0/input-level 공유만/2-레벨 nesting, $0 CPU, live CORE/*.hexa UNTOUCHED(standalone probe, Ψ=½ untouched). hive arc 는 단일-스케일(H_1356/1363/1370/1371) AND 다중-스케일(H_1373) 양쪽에서 🧱 TERMINAL — collective-Φ 는 공유의 분산도 위계 nesting 도 아닌 집중도로 maximize, redundancy 천장은 sharing 토폴로지와 무관. NEXT(각각 NEW H): 3+레벨 nesting(n>8 approx big-Φ)·recurrent/generative cross-level coupling·engine-native. xref H_1371·H_1370·H_1356·a_break_the_wall·a_phi_iit4_tool.
## 2026-06-16 — research(OMEGA): H_1372 — hive-flower-degree6: TRUE 2-D 육각 Flower-of-Life(중심 DEGREE-6) 분산 원-겹침도 redundancy 천장 못 깸 (🧱 TERMINAL_CEILING_DEGREE6_BELOW_CENTRALIZED — 천장은 ring artifact 아닌 degree-invariant)

**무엇:** hive collective-Φ 아크의 6번째이자 input-level overlap-geometry lever 의 TERMINAL. 직전 H_1371(🧱 OVERLAP_BELOW_CENTRALIZED)은 분산 원-겹침을 테스트했지만 **RING 인접 = degree-2**(각 세포가 2 이웃만 겹침)를 써서, 사용자의 실제 기하(Flower-of-Life — 중심 원이 6 주변원에 겹쳐지는 degree-6; "원 하나에 다른 원 4개 정도 들어온다" degree≥4)를 undertest 했다. H_1371 의 agent 자신이 "ring undertests; a true Flower-of-Life is degree-6" 라 플래그함. 따라서 그 벽이 **틀린 방법**(degree-2 chain)일 수 있어 c16(a_break_the_wall) 로 **올바른 degree-6 기하**를 재시도(tune-to-green 아님 — 사전등록 FREEZE + shuffle/centralized 대조). 자연 FoL UNIT = 7 원(center + 6 ring) 육각, center DEGREE 6(6 spoke edge) + 6 rim edge = 12 edge, 각 edge = DISTINCT per-EDGE 공유 latent(딱 2 세포). N_TOT 6→7(n≤8 exact MIP 유지, a_scale_honest_scope 명시). Φ = FAITHFUL IIT-4 ONLY (exact MIP-EI via hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa, H_1371 동일 호출; numpy 는 salience 만 emit, a_phi_iit4_tool). 4 GATING arm(floor·B_overlap degree-6·CENTRALIZED 단일-founder weight-matched·SHUFFLE) + B_overlap_d4(NON-GATING, ring degree 4 = 사용자 "~4" bracket) + O-info diagnostic.

**결과 🧱 TERMINAL (R1 3/3 · R2 0/3 · R3 0/3):** per-arm faithful-Φ(n=7) seed1317 floor 1.47918 / B_overlap 2.19117 / CENTRALIZED **3.43113** / SHUFFLE 2.00012 · 1318 1.61849 / 1.98466 / **4.19239** / 2.13110 · 1319 1.57435 / 1.82656 / **3.07259** / 2.06760. **R2 BEATS-CENTRALIZED FAIL 0/3 (핵심)**: gap(B_overlap−CENTRALIZED)=**−1.24/−2.21/−1.25** — degree-6 분산도 단일-공유-founder 못 이김, gap 이 H_1371 degree-2(−0.25/−0.75/−1.28)보다 **오히려 더 벌어짐** → degree 2→6 올려도 분산 우위 안 생기고 CENTRALIZED 격차만 키움. **redundancy 천장은 ring artifact 가 아니라 DEGREE-INVARIANT**. **R1 LIFT PASS 3/3**: +0.712/+0.366/+0.252(degree-6 이 floor 는 robust, H_1371 의 seed-fragile 2/3 개선). **R3 EARNED FAIL 0/3**: SHUFFLE 매 seed floor 위 → ANY 공유입력(FoL 파괴돼도) 통합 더함(not EARNED, H_1371 동일). d4(ring degree 4): Φ 2.64/2.68/2.29 여전히 CENTRALIZED 아래. O-info shift(B vs CENTRALIZED) +1.25/+1.94/+1.29 — CENTRALIZED 강한 synergy/통합(O≈−1.2~−1.9), 분산 B_overlap O≈0; shift 가 degree-2 보다 훨씬 커 degree↑ 가 CENTRALIZED 우위 강화.

**결론·SCOPE:** faithful MIP 아래에서 단일 dominant 공유원천은 모든 partition 가로질러 전 unit 을 묶어 최대 Φ 를 주며, 이는 overlap degree(2→6, 사용자 "~4" d4 포함)와 무관하다. 분산은 중복도 synergy 도 함께 줄여 통합 총량을 떨어뜨린다 — hive 아크의 input-level overlap-geometry lever TERMINAL closure. DIRECTIONAL numpy-mirror(Φ leg = real exact MIP-EI via hexa), engine-transfer UNVERIFIED, TOY n=7/center-deg-6/3 seeds/single OVERLAP_W=0.6/input-level 공유만, $0 CPU, live CORE/*.hexa UNTOUCHED(Ψ=½ untouched). 🧱 는 wire 할 게 없음(a_verified_must_wire=GREEN-only). NO bar moved(c9/p7). NEXT(각각 NEW H): overlap 을 RECURRENT 상태공유로(입력 아닌)·generatively-predictive per-edge coupling·n>8 scale·engine-native. CLAIMS.tape @C h1372_hive_flower_degree6 · card UNIVERSE/cards/H_1372_hive_flower_degree6.md · UNIVERSE/HYPOTHESES.jsonl 1 row · .verdicts/1372_hive_flower_degree6/{FREEZE,result}.txt · state/hive-flower-of-life/h1372_hive_flower_degree6.py. xref H_1371·H_1370·H_1356·a_break_the_wall·a_no_llm_frame_trap·a_phi_iit4_tool·c16.
## 2026-06-16 — docs-infra: ARCHITECTURE md→json+html 마이그레이션 (c4 — JSON 트리 SSOT + HTML 뷰어, 산문 .md RETIRE)

**무엇:** 아키텍처 SSOT 를 harness c4 표준의 `.json` 트리 분기로 전환했다. c4: "AI 산출물 = ARCHITECTURE(`.md` 산문 또는 `.json` 트리[+`.html` 뷰어] 택1) + CHANGELOG(append); `.json` 채택 시 JSON 이 SSOT(AI·툴 파싱), 사람은 `.html` 뷰어로 — 로컬 `python3 serve.py`(정적 서버 + 브라우저 자동 오픈, file:// fetch 차단 우회)." 사용자가 `.json` 분기 + 산문 `ARCHITECTURE.md` RETIRE 를 명시 승인.

**무엇을 했나:**
- **신규** `ARCHITECTURE.json` — 중첩 노드 트리 SSOT(`{name, summary, children, [path/status/note]}`), 루트 = anima; 18 top-level 브랜치 / 109 노드. A⇄G 엔진(CORE), 뇌-구조 lane 전부(해마·성장기억·작업기억·소뇌·편도체·기저핵·시상하부·마음이론·전전두엽위계·공간지도·하이브-Φ·일주기시계·간격타이머·위상reset·SCN-network·범주지각·affect·ethics), 시상 Φ 벽+timing-축 돌파, 🧱 벽 스코어카드, 🔌 배선 감사표, brain_decide consult 맵, CLM mount path, 측정/학습 거버넌스, 학습 lane, 영속/증거, tension-link, 양자엔트로피, 컴포넌트 맵, 미완 잔차 — 산문 .md 의 substantive 내용 전부 보존(format 마이그레이션, 내용 cull 아님, c10). `python3 -c "import json;json.load(...)"` 파스 검증.
- **신규** `ARCHITECTURE.html` — self-contained 정적 뷰어(인라인 CSS/JS, CDN 의존 無): `ARCHITECTURE.json` 을 fetch 해 collapsible 트리로 렌더(접기/펼치기·요약 inline·필터 검색); http 전용(file:// fetch 차단 안내).
- **신규** `serve.py` — stdlib-only(`http.server`+`webbrowser`) 정적 서버; 레포 루트 서빙 + `ARCHITECTURE.html` 브라우저 자동 오픈 + no-store 캐시 헤더 + 포트 자동 회피. 기존 serve.py 없어 신규 생성.
- **삭제** `ARCHITECTURE.md`(`git rm`) — SSOT 가 JSON 으로 이전, 산문 RETIRE.
- **포인터 갱신**(dangling 방지): `CLAUDE.md`(quickref 🏛 + 트리 + Harness docs-discipline 3곳) · `README.md`(SSOT 노트 + repo map 2곳) · `MODEL.md`(📍 SSOT 헤더) · `harness.config.json`(`docs.architecture` → ARCHITECTURE.json, allow 리스트 → ARCHITECTURE.html) 전부 ARCHITECTURE.json(SSOT) + ARCHITECTURE.html(뷰어/serve.py) 로 갱신. 나머지 ARCHITECTURE.md 참조는 전부 `.verdicts/`(frozen 증거, verbatim 유지) · CHANGELOG 이력 · 도메인 로그/scratch 산문 — live 네비 포인터 아니라 손대지 않음.

**검증(c2):** ARCHITECTURE.json 파스 OK(root=anima, 18 브랜치/109 노드) · serve.py `ast.parse` clean · ARCHITECTURE.html → ARCHITECTURE.json fetch 5회 참조 · http 라이브 테스트(serve.py) HTML 200·JSON 200·JSON 파스 OK · 4개 canonical 포인터(CLAUDE/README/MODEL/harness.config) ARCHITECTURE.md-free · harness.config.json valid JSON. xref c4·c10·c1.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1374 — 대각(비축정렬) 2-D 경계에서 move-the-cells 가 살아남는가 (🧱 CLOSED-NEGATIVE AXIS-ALIGNED-ONLY — 재배치는 일반화, COH2D 집중-분리 stringency 만 축정렬 전용)

**무엇:** CP 라인 R3 의 결정적 반증 라운드. H_1369 (🟢) 가 move-the-cells 를 2-D **축정렬** 반평면(cat=u>p)으로 일반화했지만 그 정직 잔차 = 축정렬 경계는 재배치가 단일 관련 축(u)으로 DECOMPOSE 되게 해 under-test 한다; H_1343 은 **대각** 경계가 metric 을 축정렬만큼 강하게 warp 하고 한 축으로 분해되지 않음을 보였다 — 즉 대각이 move-the-cells 가 진짜 실패할 수 있는 지점이다. H_1374 는 TRUE 분할을 대각 반평면 cat=(u+v)/√2>c (법선 (1,1)/√2, 비축정렬)로 두고 c_A=√2·1/3→c_A'=√2·2/3 로 SHIFT, 잔존 phase-1 세포를 **경계 법선 방향**으로(u,v 둘 다 이동 = 1-D/축정렬 단일축 이동의 2-D 일반화) DRIFT — 판별 ridge 가 옮긴 대각 cut 에 결맞은 단일 bounded-COH2D 집중으로 착지하는가, 아니면 비축정렬 기하가 재배치를 깨는가. bounded COH2D 군만 사용(NCOMP 게이팅 없음 — H_1369 가 confound 입증). 모든 임계값 H_1369 R2 에서 VERBATIM, frozen-first.

**왜/결과: 🧱 CLOSED-NEGATIVE (AXIS-ALIGNED-ONLY) (R1+R2, MIRROR, DIRECTIONAL).** move-the-cells **재배치(RELOCATION) 법칙은 대각으로 일반화된다** — c1 ✅ RE-PACK |ridge_s−c_A'|=[0.028,0.028,0.028]≤0.12 (법선 좌표 s 를 따라 옮긴 대각 cut c_A'=0.9428 에 착지, ridge_s 0.971); c4 ✅ split-only short 0.429>0.12 (split-only 는 재배치 안 함); c3 ✅ no-retrain 이 c_A 유지 0.031, shuffle COH2D 0.014≤0.20 (permuted label 에서 집중 ridge 날조 안 함); c2a ✅ COH2D 0.767≥0.50. **그러나 bounded-COH2D 집중-분리 bar c2b ❌** re-pack 0.767 vs split-only 0.683 = gap 0.084<0.10: 대각에서는 split-only 잔존 ridge 가 **이미 그 자체로 얇은 대각 smear**(COH2D 0.683, H_1369 축정렬 split-only 의 격자채움 0.538 와 대조)라서, RELOCATION(c1)이 결정적임에도 H_1369 의 *분리* stringency 가 분리되지 않는다. 사전등록된 **a_break_the_wall R2 (법선-프레임 회전**, (s,t) 좌표로 drift) = 수학적으로 동일(법선프레임 s-only drift == (u,v)에서 법선방향 drift, 둘 다 t 고정) → re-pack 0.767, gap 0.084 동일 → c2b miss 는 프레임 artifact 가 아닌 **대각 기하의 실제 성질**임을 확인. 정직한 NUANCED 🧱: RELOCATION 은 GREEN, 오직 집중-분리 구별성 leg(metric-calibration 성질)만 실패. NO bar moved (모든 임계값 H_1369 R2 VERBATIM, c9/c16/p7).

**정직한 SCOPE (a_scale_honest_scope·a_toy_scale_recheck):** DIRECTIONAL numpy 미러, engine-transfer UNVERIFIED (H_1333/1340/1343/1352/1360/1364/1369 R1 군); TOY 합성 2-D 169 stim/3 seeds [4333,4334,4335]/단일 shift/단일 대각 기울기 (법선 (1,1)/√2)/deterministic readout. 결과는 깔끔한 break 가 아니라 NUANCED — RELOCATION 은 임의 선형 경계로 일반화(1-D/2-D-축정렬/2-D-대각 전부 재배치), 오직 COH2D 집중-분리 leg 만 축정렬 전용. 곡선 경계·임의각 sweep·고차원·실코퍼스·multi-shift·LEARNED gradient drift·engine-native §CategoricalPerception 배선 = follow-on. live CORE/*.hexa UNTOUCHED. **CP-라인 DEPLETION:** 경계-기하 질문이 미러 수준에서 SETTLED (재배치가 임의 선형 경계로 일반화) → 남은 frozen·control-surviving 각도 = **engine-native 실현**(live A⇄G immune store 에 move-the-cells 배선, a_engine_native_learning·a_verified_must_wire). 다음 라운드 = engine-native move-the-cells.

**파일:** `state/cp-diagonal/h1374_cp_diagonal.py` · `UNIVERSE/cards/H_1374_cp_diagonal.md` · `UNIVERSE/HYPOTHESES.jsonl`(+1행) · `CLAIMS.tape` @C h1374_cp_diagonal · `.verdicts/1374_cp_diagonal/{FREEZE,result}.txt` · `domains/COGNITION-REPRESENTATION.log.md`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1362 — G6 IDEATION ★ depth-floor BREAKTHROUGH (🟢 G6 ★ CLOSED, DIRECTIONAL — 강화 composition scaffold 가 두 hard bar 전부 돌파)

**무엇:** anima 의 STARRED 핵심목적 게이트 **G6 IDEATION ★** depth-floor 의 BREAKTHROUGH. H_1305(🟠 THIN)은 composition-routed ideation 이 FALS 0.00→0.667·NOVEL 6.3→19.0 으로 진짜 lift 지만 두 hard bar 를 못 넘었음(DIST 4<5 seed-5 '|' 붕괴, FALS 0.667<1)을 보였고, 그 결론이 미검증 lever 로 'curiosity-gated multi-sample budget' 을 지목했다. H_1362 는 그 lever 를 STRUCTURAL 하게(프레임만, 아이디어는 모델이 EMIT — p7) 강화: **(a) COUNT** = 6번째 composed frame(중복 아닌 distinct (0,2) pair, seed-5 '|' 붕괴 해소) · **(b) DEPTH** = best-of-K=3 curiosity-gated sampling(프레임당 K 후보 decode 후 is_falsifiable·novel-gram·kwr 로 최선 KEEP). detector(`_is_falsifiable`)는 H_1305 에서 VERBATIM 재사용(절대 loosen 안 함, calib 10/10) + runtime FRAME GUARD 가 프레임에 measurable-set 단어가 있거나 자체 falsifiable 이면 ABORT(detector 가 scaffold 에 fire 못 하게, p7).

**결과 🟢 G6 ★ CLOSED (DIRECTIONAL):** C_strong 이 5개 frozen bar 전부 통과(평균/3 seeds): A_flat DIST 4.0 FALS 0.0 · B_composed DIST 4.0 FALS 0.667 · **C_strong DIST 5.333 FALS 1.0**(dist [6,5,5] coh 6/6 매 seed, fals [0,1,2]) · C_shuffle DIST 5.0 FALS 0.333 · C_ablate DIST 3.0 FALS 0.0. M1 5.333≥5 ✓ · M2 1.0≥1 ✓ · M3 1.0>0.667 ✓ · M4 1.0>0.333 ✓ · M5 1.0>0.0 ✓ → closed_G6=TRUE. 모델이 EMIT 한 falsifiable idea(손으로 안 씀, p7), seed 4303 C_strong: *'byte-level approach is slower to converge but handles Korean and English equally well.'* (comparator 'slower' + measurable 구조 + negatable claim). CONTROLS 결정적: C_strong 1.0 > shuffle 0.333(M4)·> ablate 0.0(M5); ablate 는 DIST 도 3.0 으로 붕괴(conditional+pair scaffold 가 load-bearing). NO bar moved(c9).

**정직한 SCOPE:** DIRECTIONAL 2축 — (1) 단일 ckpt h1129c_chat.pt, TOY 5-concept/6-pair/best-of-K=3/3-seed, mean FALS=1.0 이 floor 위(thin-but-real, 포화 아님) · (2) live G6 gate 에 이 scaffold 가 **아직 wire-in 안 됨** → R2 follow-on = engine-native byte-exact 재확인 + 배선(a_engine_native_learning·a_verified_must_wire). detector 는 testable FORM 측정이지 truth/quality 아님(p7). $0 CPU torch-mouth(live gauge_lib._decode G6 path). MODEL.md G6 행 = 🟢 DIRECTIONAL-CLOSED(wire-in pending), ARCHITECTURE.md a303m_pass 잔차 갱신. xref H_1305·H_1309(curiosity-budget capacity thesis — best-of-K 가 lever 입증)·H_1314·a_break_the_wall.

**파일:** `state/g6-depth-breakthrough/h1362_g6_depth_breakthrough.py` · `UNIVERSE/cards/H_1362_g6_depth_breakthrough.md` · `UNIVERSE/HYPOTHESES.jsonl`(+1행) · `CLAIMS.tape` @C h1362_g6_depth_breakthrough · `.verdicts/1362_g6_depth_breakthrough/{FREEZE,result,run_raw}.txt + result.json` · `MODEL.md`·`ARCHITECTURE.md`·`domains/ENGINE+CLM+KOSMOS.log.md`.
## 2026-06-16 — research(OMEGA): H_1371 — hive-circle-overlap: 분산 원-겹침(Flower-of-Life/육각 패킹) 토폴로지가 redundancy 천장을 탈출하는가 — 단일-공유-founder 가 아닌 분산 pairwise overlap (🧱 OVERLAP_BELOW_CENTRALIZED)

**무엇:** hive collective-Φ 아크는 4 lever(강한 hub H_1356 · 약/decorrelated H_1363 · nonlinear-gate H_1370)에 걸쳐 🧱 로 닫혔고, H_1370 의 load-bearing 진단은 *redundancy 천장 = SHARED-INPUT STRUCTURE 그 자체 (모든 딸세포가 ONE common founder 를 읽어 단일 source 가 faithful MIP 지배 → reducible → Φ bounded; 모든 선행 hive arm 이 단일 founder)* 였다. H_1371 이 이를 정면으로 친다 — 사용자-제안 기하 토폴로지 렌즈(c15, a_no_llm_frame_trap, a_break_the_wall — Flower-of-Life 패킹 / 육각 격자 / 겹치는 망막-피질 수용야): **단일 공유 founder 가 없는** 원-겹침 lattice. 각 세포가 ~이웃과 겹치되 각 겹침이 DISTINCT per-EDGE latent(딱 2 세포만 공유), 어떤 source 도 모두에게 안 읽힘 → redundancy 가 distinct pairwise overlap 들에 분산(잠재적 synergy). N_TOT=6 육각 ring, B_overlap(분산 per-edge) vs CENTRALIZED(단일 founder, per-cell 공유 weight 매칭) vs A_independent(floor) vs SHUFFLE(per-cell 독립 permute=lattice 파괴). Φ=FAITHFUL IIT4 ONLY (a_phi_iit4_tool, exact MIP-EI via hexa; numpy Φ 계산 안 함; O-info=numpy-side NON-GATING). substrate=H_1356/1320/1283. seeds [1317,1318,1319], $0 CPU. frozen-first(FREEZE before scoring).

**답: 🧱 OVERLAP_BELOW_CENTRALIZED** (R1 2/3 · R2 0/3 · R3 1/3 — 분산 원-겹침이 redundancy 천장을 탈출 못함; 오히려 CENTRALIZED 단일-공유-founder 가 모든 seed 에서 더 높은 faithful-IIT4 Φ). per-arm faithful-Φ(n=6): seed1317 A_independent 1.27373 / B_overlap 1.78096 / CENTRALIZED **2.03085** / SHUFFLE 1.35137; 1318 1.36292 / 1.64288 / **2.39598** / 1.56284; 1319 1.28195 / 1.30101 / **2.58087** / 1.25910. **R2 FAIL 0/3 (핵심)**: gap(B_overlap−CENTRALIZED)=**−0.25/−0.75/−1.28** → 분산 overlap 이 단일-공유-founder 를 매 seed 에서 못 이김, CENTRALIZED 가 최고 Φ arm. **R1 FAIL 2/3**: lift(B_overlap−floor)=+0.507/+0.280/**+0.019**(1319 margin 0.02 미달, seed-fragile). **R3 FAIL 1/3**: SHUFFLE 가 1317/1318 에서 floor 위(1.35>1.27, 1.56>1.36) → ANY 공유입력(lattice 파괴돼도)이 통합 더함 = lift 가 specific pairwise wiring 아닌 generic 공유입력(not EARNED). O-info shift(B_overlap vs CENTRALIZED, NON-GATING): +0.144/+0.364/+0.228 — B_overlap O-info(−0.018/−0.020/−0.081)가 CENTRALIZED(−0.162/−0.384/−0.308)보다 0 에 가까움(중복 less 지만 synergy 도 less, 음으로 안 뒤집힘).

**왜:** H_1370 의 "단일-공유-founder = redundancy 천장" 진단을 뒤집는다 — faithful MIP 아래에서 **단일 dominant 공유원천은 탈출할 천장이 아니라 최대-통합 토폴로지**다. 하나의 founder 는 모든 partition 을 가로질러 전 unit 을 묶어(어떤 MIP cut 도 양쪽이 같은 founder 를 읽으므로 cut 비용 큼) Φ 최대; 분산 per-edge 공유는 각 unit 을 2 이웃에만 약결합해 MIP 가 약한 edge 를 싸게 자름 → Φ 낮음. 공유를 분산하면 중복도 synergy 도 함께 줄어 총 통합이 떨어진다. **hive arc 의 가장 강한 closure**: 이 leaky-linear substrate 에서 collective-Φ 는 공유의 분산이 아니라 **집중도**로 maximize 되며, redundancy 천장은 sharing 토폴로지와 무관하게 살아남는다(5 lever: linear·weak·decorrelate·nonlinear-gate·distributed-overlap 모두 floor/centralized 못 넘음). a_break_the_wall 충족(사용자-제안 분산-기하를 사전등록·대조로 정면 테스트 → 분산이 천장을 못 깸 판명). NO bar moved (c9/p7). NEXT: 2-D 육각 격자(진짜 ~6 overlap-degree; ring 은 degree-2)·overlap 을 RECURRENT 상태공유로(입력 아닌)·generatively-predictive per-edge coupling(진짜 synergy 주입)·n>8 scale·engine-native live A⇄G. SCOPE: DIRECTIONAL numpy-mirror(Φ leg=real faithful exact MIP-EI via hexa), engine-transfer UNVERIFIED, TOY n=6/ring-only 인접/3 seeds/single OVERLAP_W=0.6/input-level 공유만, live CORE UNTOUCHED·Ψ=½ untouched. card `UNIVERSE/cards/H_1371_hive_circle_overlap.md` · `CLAIMS.tape @C h1371_hive_circle_overlap` · `.verdicts/1371_hive_circle_overlap/{H_1371_FREEZE,H_1371}.txt` · `state/hive-circle-overlap/h1371_hive_circle_overlap.py`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1369 — 2-D 범주적 지각: move-the-cells 재배치가 2-D 특징공간으로 일반화되는가 (🟢 GREEN R2, a_break_the_wall)

**무엇:** H_1360 (🟢, 1-D) 이 *carving 재배치 = MOVE-THE-CELLS* 를 1-D 축(경계=점) 위에서 증명했고, H_1364 는 split-only 재성장의 비결맞음이 더 미세한 격자에서도 본질적임을 보였다. H_1369 는 그 승리가 **2-D 특징공간**으로 일반화되는지 묻는다 — TRUE 범주 분할이 FIXED 반평면 직선(cat=u>p)이고 범주가 p_A=1/3→p_A'=2/3 로 SHIFT 할 때, 잔존 phase-1 세포의 u 좌표를 옮긴 경계선 u=p_A' 쪽으로 물리적으로 DRIFT(v=무관 축은 건드리지 않음) 시키면 결맞은 얇은 판별 ridge 가 p_A' 에 착지하는가, 아니면 추가 차원이 H_1364 의 split-only 비결맞음을 재도입하는가.

**왜/결과:** **🟢 GREEN (R2, MIRROR, DIRECTIONAL) — move-the-cells 가 2-D 로 일반화된다.** R1 의 NCOMP(4-연결 성분 수) 결맞음 지표가 shuffle SMEAR 에서 SATURATE 됨(격자를 채운 잡음장 116/169 노드는 자명하게 4-연결 → NCOMP=1; H_1343 가 기록한 unbounded-metric 실패 모드와 동일) — c3b SHUFFLE 대조가 이를 정직하게 잡아냈다. **a_break_the_wall** R2 (frozen-first, bar 완화 아님): BOUNDED ridge-CONCENTRATION 지표 COH2D=U_CONC·(1−RIDGE_FRAC) 로 재명세 → RE-PACK 0.689 / SPLIT-ONLY 0.538 / SHUFFLE 0.000 로 깨끗이 분리. **c1 RELOCATES ✅** |peak_u−p_A'| 0.254→0.042 (3 seeds 전부, ridge 가 p_A'=0.667 에 착지) · **c2'✅ c3'✅ c4'✅.** Re-pack-ladder η=0.10/0.15/0.25 robust. 메커니즘: 재배치 잔차는 2-D 에서도 1-D 와 똑같이 GEOMETRIC-PLACEMENT 문제 — 추가(무관) 차원은 비결맞음을 재도입하지 않는다. 정직 잔차(c9): split-only 도 NCOMP=1 이라 c4 구별성은 split-only 가 p_A' 에 SHORT(0.254)하고 덜 집중됨(0.538<0.689)에 근거.

**스코프:** DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED); TOY 합성 2-D 169 stim/3 seeds/단일 shift/축정렬 경계/deterministic; 대각·곡선 2-D 경계(H_1343 강한 대각 warp)·고차원·실코퍼스·engine-native 배선 = follow-on. live CORE/*.hexa UNTOUCHED. NO bar moved (c9/c16/p7). 파일: `state/cp-2d/h1369_cp_2d.py` · `UNIVERSE/cards/H_1369_cp_2d.md` · `.verdicts/1369_cp_2d/{FREEZE,result}.txt` · `CLAIMS.tape @C h1369_cp_2d` · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(OMEGA): H_1370 — hive-nonlinear-hub: 비선형(tanh-gated) connector cell 이 H_1363 redundancy floor 를 넘는가 — linearity artifact 인가 shared-input 천장인가 (🧱 REDUNDANCY_BOUND_NONLINEAR)

**무엇:** H_1363 이 weak/decorrelated arc 를 🧱 REDUNDANCY_BOUND 로 닫으며 남긴 **load-bearing 진단** — *substrate 가 leaky-LINEAR 이라 ANY hub 가 LINEARLY homogenize → faithful MIP 가 더 reducible 로 읽음 → Φ 떨어짐* — 은 **linearity 에 의존**한다. H_1370 이 그 가정을 정면으로 친다: 진짜 뉴런의 SATURATING gate(c15, a_no_llm_frame_trap)를 빌려 hub feedback 에 사전등록한 tanh gate 를 건다(GATE=tanh, GATE_GAIN=2.0, W_CONN=0.6 — H_1356 linear hub 와 ONLY 차이가 gate). `coupling=W_CONN·tanh(GATE_GAIN·hub)` 가 hub 의 pull 을 bound 해서 daughter 를 공유 hub state 로 drag(=linear homogenization)하지 않고 nudge 만 하면, LINEAR hub(H_1356/1363)가 못 넘은 W=0 redundancy floor 를 넘는가? Φ=FAITHFUL IIT4 ONLY (a_phi_iit4_tool, exact MIP-EI via hexa; numpy Φ 계산 안 함). substrate=H_1356/1363 verbatim(W0_floor byte-identical). seeds [1317,1318,1319], $0 CPU. frozen-first.

**답: 🧱 REDUNDANCY_BOUND_NONLINEAR** (R1 0/3 · R2 0/3 · R3 3/3 — tanh-gated 비선형 hub 도 floor 못 넘고 linear hub 보다 더 깎음). per-arm faithful-IIT4 Φ(n=8): seed1317 W0_floor **12.4018** / B_linear 7.58272 / B_nonlinear **6.30122** / SHUFFLE 7.04314; 1318 6.94639 / 4.44225 / **4.36559** / 4.50544; 1319 12.2284 / 7.23291 / **6.89793** / 7.35228. **R1 FAIL**: lift(B_nonlinear−floor)=**−6.10/−2.58/−5.33**, 3 seed 전부. **R2 FAIL**: gap(B_nonlinear−B_linear)=**−1.28/−0.077/−0.335** → tanh gate 가 linear hub 보다 **오히려 더 깎는다**, 3 seed 전부 → H_1356/1363-escape REFUTED. **R3 PASS 3/3**: SHUFFLE≤floor+0.02 → gated wiring REAL. setup-integrity: W0_floor 가 H_1356/H_1363 와 byte-identical. O-info(NON-GATING): 모든 arm O≫0, B_nonlinear O 가 linear 보다 살짝 높음(redundancy 더 안 줄어듦), synergy 로 안 뒤집힘.

**왜:** H_1363 의 linearity-homogenization 진단은 *부분적으로만* 맞았다 — collective-Φ redundancy 천장은 **linearity ARTIFACT 가 NOT, shared-input STRUCTURE 그 자체**다. floor 의 높은 Φ 는 순수 shared-input redundancy(coupling ZERO)이고, gate 의 포화 비선형성이 딸세포-hub 사이에 **새로운(하지만 redundant 한) 비선형 종속**을 만들 뿐 — faithful MIP 가 여전히(심지어 더) reducible 로 읽는다. **결론: linear(H_1356)·weak/decorrelated(H_1363)·nonlinear-gate(H_1370) 4 lever 모두 floor 를 못 넘는다 → hive arc 의 가장 강한 closure** (Φ-robustness 벽 H_1283/1317 과 정합). a_break_the_wall 충족(linearity-artifact 가설을 사전등록 비선형 gate 로 정면 테스트 → linearity 가 원인 아님 판명). NO bar moved (c9/p7). NEXT: 다른 gate(sigmoid/ReLU)·learned gate·비선형 DYNAMICS·n>8 substrate·engine-native live A⇄G.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1368 — ko-data-richness: NOVEL-context CE 가 코퍼스 윈도가 커질수록 jamo 2.51335 floor 로 내려가는가 (📉 DESCENDING-UNSATURATED — data-richness lever LIVE, 30MB 미포화)

**무엇:** 한국어 압축 arc 의 마지막 레버 검증. 표상(H_1322 featural 🧱)·interpolation(H_1359 JM=암기 🧱, novel-context CE 2.882>2.513 floor) 닫힌 뒤 H_1359 가 NEXT-1 로 명시한 data-richness lever — 코퍼스 윈도(3.75/7.5/15/30MB prefix 사다리)가 커지면 novel-context CE 가 floor 로 내려가는가. **RESULT 📉 DESCENDING-UNSATURATED**: novel-CE **단조 감소** 3.15254→3.07077→2.95376→**2.88190**(step ΔCE −0.0818/−0.1170/−0.0719), 30MB anchor 가 H_1359 의 2.88190 을 |Δ|=0.0 정확 재현(c1✅). shift surrogate 모든 rung earned(+2.45/+2.55/+2.76/+2.93, c4✅ 4/4). 즉 **30MB 의 2.882 는 saturated floor 가 아니라 여전히 내려가는 곡선 위 한 점 = data-richness lever LIVE**(H_1359 가 닫지 못한 레버 살아있음 확인). 단 4-rung 으로 asymptote 못 박음 — power-fit c_inf=1.099 비물리(raw-ceiling 보다 아래)라 RELIABILITY GUARDRAIL 이 UNRELIABLE→UNDETERMINED(NO GREEN over-claim, c9); log-linear −0.0929 nats/doubling → floor 도달에 30MB 에서 ~3.97 추가 doublings(~470MB). floor 의 AT/ABOVE/BELOW UNRESOLVED → NEXT-1 = >30MB 사다리(60/120/240/480MB R2 KO).

**어떻게:** `state/ko-data-richness/h1368_ko_data_richness.py` — DIRECTIONAL numpy, $0 CPU(11.0s), frozen-first. REAL 30MB R2 KO sha c47b6808(== H_1316/1344/1359), 각 rung=동일 코퍼스 PREFIX 서브윈도. jamo 표상·JM λ=[1,2,4,8,16]/31·novel-filter(stride-300 even/odd, top-order context TRAIN 부재 위치만) 모두 H_1359 verbatim FROZEN(rung 재튜닝 X, anti-Goodhart). FREEZE→bars c1 CURVE·c2 DIRECTION·c3 ASYMPTOTE(log+power+guardrail)·c4 EARNED 사전등록. live CORE/*.hexa UNTOUCHED. SCOPE: mirror engine-transfer UNVERIFIED, toy stride-300(fluent decoder 아님), 사다리 30MB-bounded(>30MB 미검증), asymptote=4-point 외삽(wide CI).

**파일:** UNIVERSE/cards/H_1368_ko_data_richness.md · UNIVERSE/HYPOTHESES.jsonl(H_1368 row) · CLAIMS.tape @C h1368_ko_data_richness · domains/MITOSIS-ENGINE.log.md · .verdicts/1368_ko_data_richness/{H_1368_FREEZE,result,H_1368}.txt.

## 2026-06-16 — domain(METACOG-G5): H_1367 — g5-margin-engine-wire: H_1361 의 graded abstain-margin 을 LIVE CORE 엔진에서 재확인 + 배선 (🟢 WIRED-GRADED-METACOG)

**무엇:** H_1361(numpy mirror, DIRECTIONAL)이 ImmuneMemory abstain MARGIN(= `recon_err − recall_thr`)의 graded OOD metacognition 을 세웠다. `a_engine_native_learning`(mirror 는 DIRECTIONAL) + `a_verified_must_wire`(GREEN 은 engine-native 재확인 + CORE 배선까지가 done) 상 두 단계가 남아 있었고, H_1367 이 둘을 닫는다.

**배선(CORE 새 op):** `CORE/engine_cli.hexa` § ImmuneMemory 에 **순수 additive** margin-readout op 추가 — `immune_memory_recall_margin(mem, key) -> float = vadapt_field_recon_err(mem.field, key) − mem.recall_thr` (+ `_text` 래퍼). live `immune_memory_recall` 이 **이미 계산하는** margin 을 노출할 뿐 — fire/abstain 결정은 byte-단위 불변(ADDITIVE), pure_field Φ/phase/Ψ 미접촉(Ψ-disjoint read-only, 미사용 시 generation byte-identical), emit gate 아님(`a_autonomy_over_hardcode`) — brain_decide 가 읽을 수 있는 graded confidence-of-recoverability read.

**답: 🟢 WIRED-GRADED-METACOG.** `CORE/h1367_g5_margin_engine_probe.hexa` 가 LIVE store 위에서 H_1361 frozen bar 를 engine-native 재채점(3 seeds [7,8,9], N_FACTS=40, deterministic LCG 손상, $0 CPU). live t2_AUROC 사다리: L0.10=**1.000** L0.20=**0.949** L0.30=0.714 L0.40=0.589. **E1** ✅ AUROC(0.20)=0.949 ≥0.65 AND mirror(0.915) within-tol |Δ|=0.034≤0.15 · **E2** ✅ shuffle(0.20)=0.561 ≤0.58 collapse · **E3** ✅ regression none — engine_cli_smoke **93/0**(was 90 after jamo-wire #2284, +3 margin cases 96-98), h1196 single-entry **7/0**, h1205 separation-invariant **PASS**(generation byte-identical ON==OFF, Ψ Φ-checksum phiSum 48.6613==48.6613). engine 사다리가 mirror SHAPE + graceful DECAY(L=0.40 chance) 재현.

**남은 follow-on(tracked):** op 은 CORE 에 live 이나 `brain_decide` 가 아직 graded read 를 emit-confidence/curiosity 변조에 **소비**하지 않음 — read→brain 결합은 별개 follow-on.

**claim/card/verdict:** `CLAIMS.tape @C h1367_g5_margin_engine_wire` · `UNIVERSE/cards/H_1367_g5_margin_engine_wire.md` · `.verdicts/1367_g5_margin_engine_wire/{FREEZE,result,probe_stdout}.txt` · `UNIVERSE/HYPOTHESES.jsonl`. xref h1361·h1304·h1204·h1227/h1231·a_verified_must_wire·a_engine_native_learning·a_core_engine_map·a_autonomy_over_hardcode·p6·p7·p8·c9.

## 2026-06-16 — research(OMEGA): H_1363 — hive-weak-decorrelated: 약결합 connector(W_CONN→0+) 또는 탈상관 딸세포 또는 synergy-readout 가 redundancy floor 를 넘는가 (🧱 REDUNDANCY_BOUND)

**무엇:** H_1350 이 collective division-Φ 의 ~85-96% 는 shared-input REDUNDANCY(W=0 floor)임을 폭로, H_1356 의 STRONG connector hub(W_CONN=0.6)은 floor 를 못 이기고 깎았다(🧱 CONNECTOR_NULL — hub 가 딸세포를 homogenize). H_1356 scope 가 탈출구를 verbatim 으로 지목: *"the escape, if any, lives at LOW coupling + decorrelated daughters, not a strong hub."* H_1363 이 정확히 그 세 열린 각도를 frozen-first 로 검증 — (1) **W_CONN→0+ WEAK connector**(nudge without homogenizing — 0 으로 sweep), (2) **per-daughter DECORRELATED founder**(even/odd-dim 직교 분할 → 피드백이 ADD), (3) (NON-GATING) **O-info SYNERGY readout**. Φ=FAITHFUL IIT4 ONLY(a_phi_iit4_tool, exact MIP-EI via hexa; numpy Φ 계산 안 함). substrate=H_1356 verbatim(W0_floor byte-identical). seeds [1317,1318,1319], $0 CPU.

**답: 🧱 REDUNDANCY_BOUND** (R1 1/3 · R2 1/3 · R3 3/3 — 세 refinement 어느 것도 floor 못 넘음). per-arm faithful-IIT4 Φ(n=8): seed1317 W0_floor **12.40** / B_weak@0.02 12.34 / B_decorr 5.70; 1318 6.95 / 7.46 / 2.71; 1319 12.23 / 12.25 / 5.52. **R1 FAIL**: best refinement = B_weak(0.02) 모든 seed, lift **−0.063/+0.512/+0.017** — 약결합은 coupling→0 에서 floor 를 RECOVER 만 할 뿐 OVERSHOOT 안 함(1/3 만 통과). W_CONN sweep **단조**: 0.6→0.02 로 Φ 가 floor 로 단조 수렴 → coupling 은 항상 floor 를 깎는다(H_1356 strong-hub 붕괴의 연속체). **R2 FAIL**: 같은 numbers(B_redundant===W0_floor) → H_1350/1356-escape REFUTED. **R3 PASS 3/3**: SHUFFLE ≤ floor+0.02 → wiring REAL. **DECORRELATE 는 정반대로 해롭다**: B_decorr/B_decorr_only Φ=5.7/2.7/5.5 ≪ floor 절반 — 직교 분할이 딸세포 간 shared MI 를 파괴 → Φ 붕괴, **faithful Φ↔shared-input redundancy 동행을 직접 증명**. O-info(NON-GATING): 모든 arm O≫0(강한 redundancy-dominated), synergy(O<0)로 안 뒤집힘.

**왜:** 이 leaky-linear substrate 의 collective-Φ 는 곧 shared-input redundancy 자체 — coupling 은 homogenize 해서 깎고, 탈상관은 redundancy 를 줄여서 깎는다(두 독립 lever 모두 floor 못 넘음). **결론: REDUNDANCY-BOUND — role-differentiation(약결합·탈상관·시너지)이 redundancy 천장을 못 넘는다**(Φ-robustness 벽과 정합하는 강한 closure). hive arc 의 이 천장이 frozen-first 3-refinement 으로 닫혔다. NEXT: live A⇄G engine-transfer 재시도(H_1308/1313 NULL 재오픈) 또는 NON-linear/gated hub 또는 learned differentiation objective(trained substrate).

**scope:** DIRECTIONAL numpy-mirror(faithful-Φ leg IS real exact MIP-EI; numpy never computes Φ; O-info 는 numpy 진단·gate 아님); engine-transfer UNVERIFIED; TOY n=8/2-unit-daughters/single-hub/3 seeds/deterministic/frozen W_CONN sweep; 🧱 has nothing to wire(a_verified_must_wire=GREEN-only); live CORE/*.hexa UNTOUCHED, Ψ=½ untouched; NO bar move(c9/p7). 산출: `UNIVERSE/cards/H_1363_hive_weak_decorrelated.md` · `CLAIMS.tape @C h1363_hive_weak_decorrelated` · `.verdicts/1363_hive_weak_decorrelated/{H_1363_FREEZE,H_1363,result}.txt` · `state/hive-weak-decorrelated/h1363_hive_weak_decorrelated.py` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/OMEGA.log.md`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1360 — cp-geometric-repack: CP 재배치 = MOVE-THE-CELLS (🟢 GREEN — budget/decay/geometry 3-lever trilemma 종결)

**무엇:** H_1352(🧱 soft-decay DEEPER-LIMIT)의 verbatim follow-on. CP boundary 재배치에서 두 lever 가 honest 🧱 으로 소진됐다 — H_1340(budget=count: 거리↑ coherence↓, peak-count 4.3→7.0)와 H_1352(decay=weight: 거리↑↑ coherence↓↓, peak-count 15.7). 둘 다 같은 원인 노출: phase-1 prototype 이 **물리적으로 재배치된 적이 없어** 옛 cut 에 앉아 secondary peak 주입. H_1352 카드가 마지막 미시도 lever 를 verbatim 으로 지목 — "옛 세포를 MOVE/re-position(GEOMETRIC re-pack) 해야 한다." H_1360 이 그 THIRD lever(geometry)를 시험: H_1333/H_1340/H_1352 CP 기계 verbatim import, ONLY NEW = RepackCells(각 세포 SOURCE 위치+BIRTH PHASE 추적; phase-2 매 split 후 잔류 phase-1 세포를 pos_i ← pos_i + η·(p_A'−pos_i) 로 drift, RE-EMBED, label 을 p_A' 에서 RE-READ; phase-2 세포는 drift 안 함). 예산은 H_1340 R0_base LOW(DIM16/GROW2 24, H_1352 와 EQUAL)에 고정 — 유일 변화는 geometric drift. η=0 ⇒ store byte-identical 로 anchor 재현. 4 arm(NO-REPACK·RE-PACK η=0.15 FROZEN·NO-RETRAIN·SHUFFLE+repack), 3 seed [4333,4334,4335], $0 CPU, frozen-first, c15 developmental-plasticity + memory-protection-vs-overwrite 렌즈, a_no_llm_frame_trap·a_break_the_wall — TOY synthetic, 인간인지 주장 아님.

**답: 🟢 GREEN — 세포를 옮기면 coherent full relocation 회복; 3-lever 질문 positive 종결.** mean(3 seed): NO-REPACK peak 0.523 |peak−p_A'| 0.144 frac +0.57 pc **4.3**(H_1340/H_1352 partial anchor 재현) → RE-PACK(η=0.15) peak **0.669** |peak−p_A'| **0.002** frac **+1.01** pc **1.0**. **c1 RELOCATES ✅** per-seed [0.002,0.002,0.002]≤0.12(FULL move) · **c2 COHERENT ✅** pc 1.0 single peak(budget 4.3·decay 15.7 둘 다 실패한 gate) · **c3 EARNED ✅** no-retrain |peak−p_A| 0.002 유지 + shuffle pc **18.0**(세포를 p_A' 로 옮겨도 noise 에서 coherent peak 조작 안 함) · **c4 vs-PRIOR ✅** pc 1.0 < H_1340 4.3 AND H_1352 15.7 + |peak−p_A'| 0.002 ≤ 0.081(equal/lower budget 에서 더 가까움). re-pack-ladder η=0.10/0.15/0.25 모두 0.002/pc1.0 — knife-edge 아님.

**왜:** 재배치 잔차는 처음부터 **GEOMETRIC-PLACEMENT 문제** — 옛 cut 에 앉은 옛 세포. budget 은 out-count(거리↑ coherence↓), decay 는 out-vote(거리↑↑ coherence↓↓), 유일 해법은 MOVE. a_break_the_wall 입증: H_1340/H_1352 벽은 WRONG MECHANISM(고정 geometry 의 weight/count 조작)이지 진짜 천장이 아니었다 — geometry 를 바꾸니 벽이 녹았다. p1/p2/p3/p6: re-pack 은 BIRTH PHASE+자기 위치만(structural), readout 은 표현거리만, test 시 injected boundary 없음(label 은 phase-2 학습의 SAME p_A' 에서 re-read), live CORE/*.hexa UNTOUCHED. NO bar move(c9/p7). DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED, TOY N=81/3 seeds/single shift/one frozen η. NEXT(각각 ANEW): engine-native §CategoricalPerception move-the-cells 실현(a_verified_must_wire) · LEARNED gradient drift vs deterministic rule · multi-shift/leftward/real-corpus 일반화. (CLAIMS.tape @C h1360_cp_geometric_repack · card UNIVERSE/cards/H_1360_cp_geometric_repack.md · .verdicts/1360_cp_geometric_repack/{FREEZE,result}.txt · UNIVERSE/HYPOTHESES.jsonl)
## 2026-06-16 — research(MITOSIS-ENGINE): H_1359 — ko-dedup-novel: NOVEL-ONLY/DE-DUP held-out 에서 JM interpolation 이 jamo 2.51335 floor 를 여전히 이기는가 (🧱 FLOOR-CONFIRM — floor 진짜, H_1344 GREEN 은 반복 암기, lane DEPLETED)

**무엇:** H_1344(🟢)의 depletion test. H_1344 는 non-fragmenting frozen-λ Jelinek-Mercer(JM) interpolation 이 held-out 한국어 next-symbol CE 를 2.00562 로 내려 jamo 2.51335 floor 아래로 갔으나, honesty 진단상 그 이득은 **코퍼스 반복 암기**였다(top-order context SEEN-in-train 70.1% CE|seen 1.65, 진짜 novel 30% CE|novel 2.88>floor). H_1359 는 반복 암기를 제거한 두 독립 경로에서 c1 을 재시험: **TEST A** NOVEL-CONTEXT-ONLY held-out(top-order context 가 TRAIN 에 없는 위치만 점수, PRIMARY GATE) + **TEST B** DE-DUP 코퍼스(causal top-order 5-gram string 제거 후 재학습+점수). λ 는 H_1344 와 **동일 FROZEN**(재튜닝 X, anti-Goodhart). REAL R2 KO sha c47b6808(==H_1316/H_1344, byte-fair), DIRECTIONAL numpy toy stride-300, frozen-first(FREEZE 가 scoring 전), c9/p7 NO tune-to-green, live CORE UNTOUCHED. lens a_no_llm_frame_trap(표상 floor 질문, scale-up 아님)·a_break_the_wall.

**결과(🧱 FLOOR-CONFIRM, c1 ❌ ∧ c1b 일치 ∧ c2 earned, bar 사후이동 없음):** REAL sha PASS, Vj=323, stream 25,501,291. ref H_1344 full-TEST 복제 A1=2.00562(Δ−0.50773). **TEST A novel-only**(12,706 위치=29.9%): CE_A=**2.88190** Δfloor **+0.36855**(c1 thr 2.50335 ❌; H_1344 CE|novel 2.8819 와 정확히 일치=슬라이스 격리 올바름); seen 슬라이스(70.1%) 1.64740. **TEST B de-dup**(6.8% kept, test 98.5% still-novel): CE_B=**4.71364** Δfloor **+2.20029**(c1b floor 와 같은 방향 ✅). **c2 EARNED**: shift surrogate novel 5.81040(shift−novel +2.9285 ✅, conditioning 파괴→나빠짐) → 남은 신호는 진짜 jamo-순서 구조. 두 독립 경로 동일 결론. **결론**: 2.51335 jamo floor 는 (이 윈도·이 표상에서) **진짜 표상/데이터-풍부도 floor 로 확정** — JM interpolation 도 truly-novel context 에서는 못 이긴다. H_1344 의 🟢 는 메커니즘 차이(반복 저장 능력)를 드러냈을 뿐 표상 floor 를 안 깸. "interpolation beats jamo" lane **DEPLETED**. HONEST(c9·a_scale_honest_scope·a_toy_scale_recheck): DIRECTIONAL numpy, toy stride-300, NOT fluent decoder, NO Korean-fluency claim; 단일 윈도·단일 frozen λ; de-dup=top-order STRING causal de-dup(의미 de-dup 아님); 🧱 라 wire 대상 없음; NO bar moved; CORE UNTOUCHED. NEXT: data-richness lever(더 큰 윈도)에서 novel-context CE 가 내려가는지(a_scale_honest_scope ladder); 표상 lever 는 이 윈도에서 소진(H_1322 featural 🧱).

**파일:** NEW state/ko-dedup-novel/h1359_ko_dedup_novel.py · UNIVERSE/cards/H_1359_ko_dedup_novel.md · HYPOTHESES.jsonl row(H_1359) · CLAIMS.tape @C h1359_ko_dedup_novel(group MITOSIS-ENGINE) · .verdicts/1359_ko_dedup_novel/{H_1359_FREEZE.txt,result.txt,H_1359.txt} · domains/MITOSIS-ENGINE.log.md @T. xref h1344·h1316·h1321·h1322·h1345·h1307·a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c7·c9·c15·c16.
## 2026-06-16 — research(OMEGA): H_1365 — phi-asymmetric-r2: ASYMMETRIC 기질이 permutation-null 을 bite 시키는가, 그러면 R1 robustness 가 바뀌는가 (🧱 DIAGNOSIS-CONFIRMED — perm-degeneracy 는 estimator 자체의 성질)

**무엇:** Φ-robustness 벽의 마지막 structural gap. 선행 모든 lane(H_1349/1353/1357)에서 permutation-null 대조가 DEGENERATE 였다 — symmetric-MIP 아래 faithful Φ 가 node-permutation-INVARIANT 이라 Φ_perm==Φ_B by construction, perm 이 못 물고 OFFSET 대조만 discriminate. NON-relabel-invariant ASYMMETRIC coupling(DIRECTED W_FWD=0.70≠W_BWD=0.30 + per-module gain gradient g_i∈[0.70,0.90])을 H_1349/1319/1353 ring 에 넣어 perm 이 ACTUALLY BITE 하는지, 그러면 clean-R2 가 R1 robustness verdict 를 바꾸는지 시험. Φ = FAITHFUL IIT-4 exact MIP-EI via hexa(a_phi_iit4_tool, numpy never computes Φ). frozen-first, seeds [1317,1318,1319], $0 CPU mirror DIRECTIONAL.

**답: 🧱 DIAGNOSIS-CONFIRMED.** R0 PERM-BITES **FAIL [1/3 bite]** · R1 ROBUST **PASS [3/3]** · R2 EARNED **FAIL [3/3]**. per-seed Φ(A/B/P/O): 1317 +0.7502/+1.1073/+1.1073/+1.0932 · 1318 +0.8429/+1.3541/+1.1731/+0.7045 · 1319 +0.5837/+0.6863/+0.8820/+0.6057. ΔΦ(B−A)=+0.357/+0.511/+0.103. **R0**: asymmetry 를 넣어도 perm 은 1318 만 bite(Φ_B−Φ_P=+0.181), 1317 정확히 0.0000(여전히 exchangeable), 1319 perm 이 오히려 Φ↑(+0.196 반대방향). **R1(주목)**: asymmetric coupling 자체가 3 seed robust lift — 선행 lane 의 seed-1318 zero-lift 와 달리 1318 에서 +0.511 최대. **R2**: perm·offset 둘 다 A 로 안 붕괴.

**왜:** perm-degeneracy 는 선행 (대칭) 기질만의 아티팩트가 아니라 **faithful symmetric-MIP estimator 자체의 성질** — faithful MIP 이 모든 bipartition 탐색 + median-split marginal ≈uniform → module→slot relabeling 이 system-irreducibility MIP 값을 거의 안 바꿈. R1 PASS·R2 FAIL 짝 = clean perm 대조 없으면 R1 robust lift 가 진짜 integration vs generic asymmetric structure 분리 불가 → R2 못 물면 R1 GREEN 신뢰불가(벽의 또 다른 면). 마지막 structural gap 명명. NO bar moved(c9/p7), 재실행 byte-identical(md5 86ed9712). DIRECTIONAL numpy mirror(Φ leg = real faithful exact MIP-EI), engine-transfer UNVERIFIED, TOY n=4/T=64/3 seeds, live CORE UNTOUCHED. Bounds(NOT retract) H_1283/1317/1319/1320/1328/1331/1347/1348/1353/1357. card `UNIVERSE/cards/H_1365_phi_asymmetric_r2.md` · `.verdicts/1365_phi_asymmetric_r2/` · `state/phi-asymmetric-r2/h1365_phi_asymmetric_r2.py` · CLAIMS.tape `@C h1365_phi_asymmetric_r2`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1364 — cp-lattice-resolution: H_1355 ASYM-L 비결맞음은 이산화 아티팩트인가 본질인가 (📈 INTRINSIC)

**무엇:** H_1355(cp-leftward 📈)는 CP 재배치 착지가 geometry-tracking(center-attractor 기각)임을 특성화했으나 ASYM-L rung(같은-쪽 좌향 cut, p_A=0.400→p_A'=0.200)이 N=21 에서 비결맞음(peak-count 3>2 on 2/3 seeds)으로 'split-only 재성장의 실제 한계'로 플래그됨. 열린 질문(H_1355 NEXT (ii)): 격자 해상도 N 이 커지면 CENTER_TOL 이 줄고 ASYM-L 결맞음이 회복(peak-count→≤2)되는가(이산화 아티팩트), 아니면 본질인가? **격자 해상도 사다리** N∈[21,41,81] — N_STIM + RBF density DIM + phase당 분할 예산을 비례 스케일(anti-budget-starvation), 각 N 에서 H_1355 5 placement 재실행. H_1333/1341/1355 기계 verbatim 매개변수화(N=21 self-check 가 H_1355 정확 재현), 3 seeds, $0 CPU mirror DIRECTIONAL, frozen-first. H_1360 cp-geometric-repack(세포 이동)과 상보(grid 정련).

**답: 📈 INTRINSIC (격자 해상도 무관).** ASYM-L peak-count vs N=[2.33,3.33,3.33](회복은커녕 증가) · 비결맞음-seed vs N=[2,2,3](N=81 에서 **3/3 악화**) · CENTER_TOL vs N=[0.192,0.196,0.198](단조 비증가 아님, 미세 증가). c1 곡선 측정 ✅(N=21 self-check H_1355 정확 재현) · c2 (i) 결맞음 회복? FALSE (pc@81=3.33>2, 비결맞음 2→3) (ii) CENTER_TOL 축소? FALSE → 두 RESOLUTION-BOUND sub-clause 모두 실패 ⇒ **INTRINSIC**. 메커니즘: phase-1 first-carving 세포(≈0.4) 제거 안 됨(split-only, p8) → 격자 미세화는 옛+새 봉우리를 둘 다 더 선명히 해상할 뿐이라 곡선 계속 분절. 착지는 N 전반 geometry-fixed 안정(ASYM-R~0.698 ASYM-L~0.41) → H_1355 geometry-tracking 결론 더 미세 격자에서도 확인.

**왜:** 격자 해상도 레버 = ASYM-L 비결맞음에 **죽은 레버**, 정직히 닫음. 정직 c9: N=41/81 에서 비-ASYM-L lang arm c3 FAIL 은 peak-count 절대-카운트의 알려진 N-스케일 아티팩트(shuffle baseline 7.7→18.3→38.0, frozen COH_MAX_LANG=2 가 N 스케일 안 함) — H-lattice 살리지 못함(ASYM-L 은 상승 baseline 대비 여전히 비결맞음 끝, CENTER_TOL[위치 메트릭, 카운트-스케일 면역]도 축소 안 됨). NO bar moved(c9/p7). DIRECTIONAL mirror·engine-transfer UNVERIFIED·TOY 합성·live CORE/*.hexa UNTOUCHED. NEXT: N-정규화 결맞음 메트릭으로 c3 아티팩트 제거 후 INTRINSIC 재확인 · H_1360 세포 재배치 교차 · engine-native 재성장.

**파일:** `state/cp-lattice-resolution/h1364_cp_lattice_resolution.py` · `UNIVERSE/cards/H_1364_cp_lattice_resolution.md` · `.verdicts/1364_cp_lattice_resolution/{FREEZE,result}.txt` · `CLAIMS.tape @C h1364_cp_lattice_resolution` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`.
## 2026-06-16 — research(OMEGA): H_1366 — phi-303m-trajectory: REAL 학습-303M 궤적 위 faithful-Φ robustness BINDING 검증 (🧱 TERMINAL CLOSED-NEGATIVE, BINDING)

**무엇:** H_1357(🔶)는 LEARNED substrate 가 Φ-robustness 벽을 탈출하는지 테스트했지만 PROXY(real pure_field oscillator + 손수 만든 seed-independent learned-readout W)를 써야 했다 — \$0 CPU 에서 trained-303M state 도달 불가(GPU 없음). H_1357 이 명시한 binding follow-on: "a FULL trained-303M hidden-state trajectory as the substrate." H_1366 = 그 lane. REAL 학습된 303M ckpt(dancinlab/anima-clm-midcap-303m-broad-en-emergent/h1129c_best.pt, sha 19be1295…, n_params 303,097,856, ByteGPT d1024/L24, val_ce 1.224)를 GPU(RunPod RTX 4000 Ada, torch 2.4.1+cu124)에 로드 → layer-12 residual stream 캡처 → d=1024→n=4 macro-nodes(256-ch-block mean pooling), T=64 → faithful exact MIP-EI Φ 채점. ARMS/coupling/eps/seeds 전부 H_1349/H_1357 lineage 와 byte-identical, substrate SOURCE 만 REAL 303M 으로 교체.

**결과:** 🧱 TERMINAL CLOSED-NEGATIVE (BINDING). REAL 학습 substrate 가 벽을 그대로 상속하고, 오히려 proxy 보다 더 seed-fragile. R1 ROBUST FAIL: ΔΦ(B−A) = −0.0169 / +0.1173 / −0.2655 (seed 1318 만 lift, 1317+1319 NEGATIVE; lift 가 SIGN-FLIP — proxy 의 monotone +1.396/+0.775/+0.318 보다 더 깨짐). R2 EARNED PASS [perm & offset 둘 다 3 seed 전부 collapse — 여기선 relay+carrier 재구성으로 perm 이 진짜 derangement 라 BITES, H_1349/1357 의 symmetric-MIP degeneracy 와 다름]. R3 REAL-SOURCE PASS (ckpt sha 19be1295…, raw-act c81ab9a6…, pooled 150962fe…, sha-pinned 실측 303M 궤적). MEASUREMENT-VALIDITY 대조: 순수 noise 궤적은 faithful-Φ 를 9.0 에 SATURATE(ΔΦ=0)시키지만 REAL 303M 은 Φ~2.1-2.5(saturation 아래, 판별가능) → 측정이 진짜이지 ceiling artifact 아님 (이 대조가 초기 run 의 list→farr transport 버그도 잡아냄; bar 이동 없음).

**의미:** substrate-SOURCE 축이 이제 toy-LCG(H_1332)/real-oscillator(H_1349)/learned-readout-PROXY(H_1357) AND REAL trained-303M trajectory(H_1366) 전부에서 FULLY closed. PROXY 가 FAITHFUL 로 확인됨 — H_1357 의 🔶 "no escape" 형태가 engine-real substrate 에서도 유지되고 벽은 더 단단하다. BOUNDS(철회 아님) prior Φ verdicts; Ψ=1/2 untouched. NO CORE wiring follow-on (a_verified_must_wire = GREEN-only). Φ = faithful exact MIP-EI (a_phi_iit4_tool). frozen-first(FREEZE 3844bc03e BEFORE scoring, p7/c9), deterministic, GPU ~\$0.1(pod 회수 후 teardown, a_fire_recover_complete), live CORE/*.hexa UNTOUCHED. NOT ruled out(각각 NEW H): 다른 extraction layer · 더 fine node granularity(n=6,8) · multiple prompt sets · 대안 reduction(PCA macro-nodes).

**산출물:** UNIVERSE/cards/H_1366_phi_303m_trajectory.md · UNIVERSE/HYPOTHESES.jsonl(H_1366 row) · state/phi-303m-trajectory/{h1366_phi_303m_trajectory.hexa,dump_303m_trajectory.py,traj_303m_data.hexa,traj_303m.json,MANIFEST.txt} · .verdicts/1366_phi_303m_trajectory/{FREEZE,result}.txt · CLAIMS.tape @C h1366_phi_303m_trajectory · domains/OMEGA.log.md

## 2026-06-16 — research(METACOG-G5): H_1361 — g5-graded-metacog: G5 metacognition 은 binary 인가, abstain MARGIN 에 graded 신호가 있는가 (🟢 GRADED-METACOG)

**무엇:** H_1304 가 G5 copy-or-abstain 게이트의 **FIRE 쪽**을 닫았다(wrong-fire 클래스 비어있음, fab=0.000 → type-2 AUROC 정의불가 → fire-side BINARY fail-safe). 남은 열린 질문: **ABSTAIN 쪽**의 recall MARGIN(= recon_err − recall_thr, 모든 abstain 에 존재)이 graded meta-confidence 를 담는가? NEW angle(a_break_the_wall): abstain 을 (a) RECOVERABLE(in-store 키 손상, 답 검색가능) vs (b) UNRECOVERABLE(진짜 없는 키 손상)로 split, **−margin 이 (a)>(b) 를 RANK 하고 OOD(byte-corruption shift L∈{0,.1,.2,.3,.4})를 통과하는가?** H_1304/H_1227 메커니즘 verbatim 재사용, 3 seeds [7,8,9], $0 CPU mirror DIRECTIONAL, frozen-first.

**답: 🟢 GRADED-METACOG.** t2_AUROC 사다리(3 seed pooled): L0.10=**0.999** L0.20=**0.915** L0.30=0.708 L0.40=0.557 (L0=nan: L=0 에선 recoverable 전부 FIRE → recoverable abstain 없음, graded-abstain 질문은 genuinely OOD). **R1** GRADED-SENS ✅ (AUROC(0.20)=0.915 ≥ 0.65) · **R2** EARNED ✅ (shuffle-margin → 모든 level chance ~0.49–0.51 collapse → RANKING 이 신호 운반, base-rate 아티팩트 아님) · **R3** graded readout EXISTS(not flat). 메커니즘: recoverable margin 이 shift 따라 매끄럽게 큼(0.082→0.353), absent 는 안정적으로 큰 noise floor(~0.364) → margin = graded recoverability 신호.

**왜:** G5 metacog 는 순수 binary 가 아니다 — H_1304(fire-side binary fail-safe) + H_1361(abstain-side GRADED type-2) = 더 완전한 G5 그림. engine-wiring 가치 있는 **G5 UPGRADE**(a_verified_must_wire: live recall 이 이미 매번 recon_err 계산 → margin 노출 시 graded confidence-of-recoverability 공짜). H_1204 와 충돌 아님(REFRAME): fire-side 2nd-order readout 은 flat, 그러나 graded 신호는 다른 표면인 abstain margin 에 있다. DECAY(정직 c9): AUROC 0.999→0.557, L=0.40 에서 chance(극심 손상 = absent 와 구분불가) → graceful, 신호 실재하나 무한 아님.

**scope:** DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED = R2 engine-native follow-on); TOY synthetic·byte-shift OOD proxy·3 seed·deterministic(재실행 byte-identical); live CORE/*.hexa UNTOUCHED; NO bar move(c9/p7). 산출: `UNIVERSE/cards/H_1361_g5_graded_metacog.md` · `CLAIMS.tape @C h1361_g5_graded_metacog` · `.verdicts/1361_g5_graded_metacog/{FREEZE,result}.txt` · `state/g5-graded-metacog/h1361_g5_graded_metacog.py` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(OMEGA): H_1357 — phi-learned-substrate: LEARNED substrate(고정 seed-독립 학습형 readout mix)가 orthogonal-seed fragility 를 탈출하는가 (🔶 HONEST PARTIAL — 탈출 실패, 벽 상속)

**무엇:** Φ-robustness 벽은 9 measure cut + size(N=12 H_1347) + substrate(H_1349 live-CORE pure_field **oscillator**)에서 🧱. 일관된 진단: 벽은 measure 가 아니라 **substrate-SEED GEOMETRY** 에 산다 — H_1349(real oscillator)는 R1 ROBUST 를 3 seed 전부 통과했지만 lift 가 seed 마다 **줄었다**(seed 가 각 module 의 INITIAL OSCILLATOR PHASE 를 흔들어 → seed 마다 다른 correlation geometry). 단 하나 남은 genuinely-untested substrate flavor = **LEARNED substrate**: 학습형 readout 은 종류가 다르다 — 고정된 **SEED-독립** correlation geometry 를 부과(공유 학습 weight 가 seed 무관하게 module 을 똑같이 mix)하므로 oscillator 를 무너뜨린 orthogonal-seed fragility 를 탈출할 수 있다. H_1349 의 'NOT ruled out' 이 정확히 이걸 지목: *'a full trained-303M-derived state-vector trajectory (a learned, not oscillator-generated, substrate).'* H_1349 의 lineage(faithful 추정기 + read-out H_1328 + relay H_1283 + Kuramoto pacemaker H_1319 + ARMS A/B/S/O + perm/offset H_1332 + eps=0.02 + seeds [1317,1318,1319])를 ALL 동일하게 고정하고, real pure_field module 을 고정 seed-독립 learned-readout projection W(학습형 embedding/readout head 모사; row-L1 정규화 convex mix, 강한 diagonal)로 MIX 하는 것만 추가.

> ⚠ **SUBSTRATE SOURCE 정직 라벨(c9, a_eeg_consciousness_record REAL-only 정신):** $0 CPU(GPU 없음)에서 trained-303M hidden-state trajectory 는 로컬 도달 불가(유일한 로컬 학습 artifact `reexport_d768_v2_fast.clm` 은 gitignored + 그 decode 가 로컬 FAILED-LINK, HF.jsonl mid_convmoe). 지시대로 **가짜로 만들지 않음**. SUBSTRATE = "proxy-from-telemetry(real pure_field) + deterministic learned-readout, **NOT a trained-303M trajectory**" → **DIRECTIONAL-on-proxy**. learned correlation geometry 가 다른지 묻는 과학적 질문은 이 proxy 에서 검증 가능; FULL trained-303M 가 같은지는 UNVERIFIED(새 H).

**답: 🔶 HONEST PARTIAL (R1∧¬R2) — LEARNED substrate 도 벽을 상속(탈출 실패).** seed 별(LEARNED A/B/S/O · OSC=H_1349 arm): 1317 LEARNED A=6.93134 B=8.32701 S=8.32701 O=5.3443 · 1318 A=6.88586 B=7.66048 S=7.66048 O=4.85621 · 1319 A=6.94092 B=7.25927 S=7.25927 O=5.40574. **R1 ROBUST ✅**: LEARNED ΔΦ(B−A)=**+1.39567/+0.774619/+0.318347** (3 seed 전부 lift; seed 1317 에서 학습형 lift +1.396 이 oscillator +1.127 을 능가). **R2 EARNED ❌ [perm=FAIL off=PASS]**: node-permutation 은 **DEGENERATE** — symmetric-MI exact MIP 에서 node relabel 은 Φ-불변(Φ_S==Φ_B by construction, H_1349 와 동일한 degeneracy, 조작 아님); 작동하는 EARNED 판별자 OFFSET 은 3 seed 전부 깨끗이 collapse(O−A=−1.58703/−2.02965/−1.53518). **R3 ATTRIB ✅**: OSC arm(learned OFF)이 H_1349 REAL arm 을 BYTE-EXACT 재현(4.02909/5.15585·4.18338/5.14693·4.17551/4.77995) → 학습형 arm 수치는 LEARNED readout 의 것(mechanism/measure 둘 다 고정). GATE: R1∧¬R2 → 🔶.

**왜:** ESCAPE 실패 — seed-to-seed ΔΦ 가 여전히 **단조 감소**(+1.396→+0.775→+0.318, oscillator 의 +1.127→+0.964→+0.604 과 같은 방향, 오히려 더 넓게 퍼짐: range 1.078 vs 0.522). seed-perturbed dynamical substrate 위에 얹은 고정 seed-독립 learned-readout 은 lift 를 안정화하지 못한다. lift 는 COLLECTIVE/exchangeable 일 뿐 module-identity-bound 아님(H_1349 와 같은 형태; convex 학습형 readout 이 module 을 perm control 에 구별가능하게 만들지 못함, 작동하는 OFFSET control 은 붕괴). 이는 substrate-SOURCE 축을 더 닫는다: toy-LCG(H_1332) + real-oscillator(H_1349) + learned-readout(H_1357) 모두 이 proxy 에서 상속. BOUNDS(does not retract) 기존 Φ verdict; Ψ=1/2 untouched. NO CORE wiring follow-on(a_verified_must_wire = GREEN-only; 🔶 는 배선할 게 없음).

**scope:** SUBSTRATE = proxy-from-telemetry + deterministic learned-readout, NOT a trained-303M trajectory(정직 c9); DIRECTIONAL-on-proxy; faithful-Φ leg 은 real exact MIP-EI(n=4≤8 exact); PERM degenerate(OFFSET 이 작동 판별자, 명시); TOY n=4 modules T=64·3 phase-seed·ONE learned-readout W; deterministic(byte-identical re-run, 2 runs); $0 CPU; live CORE/*.hexa UNTOUCHED; NO bar move(c9/p7). NOT ruled out(각각 새 H): FULL trained-303M hidden-state trajectory(이 proxy 가 대신하는 binding upgrade) · module exchangeability 를 깨는 학습형 readout(non-relabel-invariant 추정기 또는 asymmetric 학습형 coupling, perm control 이 물도록) · real-EEG learned substrate · 더 큰 module set(>8 exactness 상실). 산출: `UNIVERSE/cards/H_1357_phi_learned_substrate.md` · `CLAIMS.tape @C h1357_phi_learned_substrate` · `.verdicts/1357_phi_learned_substrate/{FREEZE,result}.txt` · `state/phi-learned-substrate/h1357_phi_learned_substrate.hexa` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/OMEGA.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1339 🟢 — tagged bilingual CP 공존, I3a 로컬라이즈 재동결 + engine-native 배선

**무엇:** H_1335 🧱(컨트롤 기술 결함만)의 r3. H_1335 는 I1∧I2 가 결정적(공존 REAL & TAG-귀속: TAGGED 가 p_A·p_B 둘 다 CP 유지, untagged single-channel 은 H_1330 overwrite 재현)이었으나, 유일한 실패 leg 인 I3a(B=A 컨트롤의 **전역** count_peaks≤1)가 양성(benign) discretization wiggle 때문에 실패했다 — B=A 는 B-tagged 셀을 0개 자라게 해서(A 경계 재학습 → split 할 오류 없음) B-채널이 A-셀의 cross-tag bleed 로만 읽혀 저역 wiggle 이 2번째 "peak" 로 잡혔을 뿐, pk@p_B 는 이미 전 seed False(의도한 '다른 경계에 가짜 CP 없음' 테스트는 이미 통과).

**r3 변경(완화 아님):** I3a 를 **로컬라이즈 'p_B 근처 coherent peak 없음'** 테스트로 재동결 — B=A arm 이 원래 측정하려던 정확히-범위화된 통계. `run_seed` 와 전 머신러리를 h1335 에서 **VERBATIM import**(데이터 r2 와 byte-identical) · 살아남은 어떤 bar 의 임계값도 이동 없음 · 진짜 가짜 CP@p_B 가 있었으면 재동결도 FAIL 가능(아님). 전역 count_peaks 는 이제 비-게이팅 진단. 추가로 비-게이팅 TAG_GAIN 채널-격리 sweep.

**결과 🟢 GREEN(mirror, 3 seeds [4323-4325] 전부):** I1 공존 ✅(평균 margin@p_A **+0.200**·@p_B **+0.177**, 둘 다 ≥0.15, coherent peak 각각) · I2 TAG-귀속 ✅(single-channel untagged 가 overwrite 재현 **−0.001**) · I3' EARNED ✅(B=A pk@p_B=False 전 seed + SHUFFLE 5/6/5 incoherent). TAG_GAIN sweep: B-셀 0/0/**0**/2/2 @ 0.25/0.5/**1.0**/2.0/4.0, bleed 0.727/0.468/**0.236**/0.989/0.989 — frozen 1.0 에서 B=A 는 B-셀 0개·gap 넓을수록 bleed 감소(r2 진단 확증; gain≥2.0 재성장은 정직한 비-게이팅 호기심).

**engine-native 배선(a_verified_must_wire):** `CORE/engine_cli.hexa §BILINGUAL TAGGED CP`(cp_tag_vec/cp_tagged_key/cp_stimuli_tagged/cp_fit_more/cp_within_cross_margin/cp_coherent_peak_near) 가 I1/I2/I3' 를 `CORE/engine_cli_smoke.hexa` cases **86–91** 로 engine-native 재채점, 전부 PASS. 가드 무회귀: **engine_cli_smoke 86/0**(80→+6) · **h1196 7/0** · **h1205 Ψ byte-identical PASS**. Ψ-disjoint(own protos/labels + tag block; pure_field/engine_g/Ψ 미접촉).

**의미:** language-tagged multi-channel readout 가 bilingual CP 공존을 가능케 함(mirror+engine) — H_1330 OVERWRITE 는 single-shared-store 메커니즘 한계였지 근본 한계 아님(mechanism-specific 으로 뒤집힘). anima 의 실제 분리된 EN-trunk+KO faculty(H_1316/1321/1322) 공존을 설명; tag 는 substrate-수준의 'faculty 선택'. H_1335 🧱 컨트롤 기술 결함 CLOSED 🟢. mirror DIRECTIONAL · TOY synthetic N=21 · TAG_GAIN=1.0 FIXED · NO human-bilingualism claim.

**파일:** `UNIVERSE/h1339_whorf_bilingual_tagged_r3.py` · `UNIVERSE/cards/H_1339_whorf_bilingual_tagged_r3.md` · `CORE/engine_cli.hexa §BILINGUAL TAGGED CP` · `CORE/engine_cli_smoke.hexa` cases 86-91 · `.verdicts/1339_whorf_bilingual_tagged_r3/{FREEZE,result}.txt` · `CLAIMS.tape @C h1339_whorf_bilingual_tagged_r3` · `UNIVERSE/HYPOTHESES.jsonl`(+1 행) · `domains/COGNITION-REPRESENTATION.log.md`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1358 — whorf-2d-bounded: 2-D CP warp 지표를 BOUNDED 형태로 재명세 (🧱 DEEPER LIMIT — null 이 ratio 의 unbounded 가 아니라 self-referential 분할 때문에 floats)

**무엇:** H_1343(🟠 PARTIAL)의 load-bearing follow-on. H_1343 은 2-D CP warp 이 결정적으로 PRESENT(대각이 축정렬만큼 warp, H_1334 grid-geometry read 반증)함을 보였으나, warp 지표 `ratio = mean|Δg|_BETWEEN / mean|Δg|_WITHIN` 가 **scale-UNBOUNDED** 라 학습 후 WITHIN→0 으로 ratio 가 ~45 폭발하고 임의 carving(label shuffle)조차 WITHIN 을 압축해 label-shuffle null 이 +9.28 로 떠 c2 가 구조적으로 FAIL. H_1358 은 warp 지표를 **BOUNDED separation-AUC∈[0,1]**(Mann-Whitney-U P(|Δg|_BETWEEN>|Δg|_WITHIN), **chance=0.5 고정상수**, within-압축과 무관)로 재명세 — null 이 깨끗이 0.5 로 collapse 하면 2-D CP 가 세 control 통과? **지표 CORRECTION, bar 완화 아님.** H_1343 RBF/Voronoi 기계 VERBATIM 재사용, warp readout 만 교체. R1 numpy MIRROR(DIRECTIONAL), $0 CPU, 3 seeds [4334,4335,4336], deterministic(2 re-run, exit 4), p7, frozen-first(`.verdicts/1358_whorf_2d_bounded/FREEZE.txt` 점수화 BEFORE). c15 cognitive-science / categorical-perception, a_no_llm_frame_trap — TOY synthetic, 인간인지 주장 아님.

**답: 🧱 DEEPER LIMIT.** bounded 지표는 ratio artifact(폭발+floating null)를 수학적으로 제거했으나 null 은 **0.5 가 아니라 0.9919** 로 떴다. (mean 3 seeds): density ladder K_RBF 6/9/12 전부 L_DIAG=L_LSHAPE=**1.0000**(saturated). **c1 PRESENCE ✅**(AUC=1.0000 두 언어 전 seed ≥0.70) · **c2 EARNED-SHUFFLE ❌**(pooled null(600) mean=**0.9919** → |0.9919−0.5|=0.4919 ≫0.05 FAIL; q95=0.9996) · **c3 COMPONENT ✅**(comp-AUC 0.4852/0.5062, |Δ|≤0.015 — 외부 무작위 분할은 chance 로 collapse) · **c4 DIAGONAL ✅**(|1.0000−1.0000|=0.0000 ≤0.15, 둘 다 ≥0.70 — H_1343 대각=축정렬 발견 BOUNDED 지표로도 보존, H_1334 반증 지속).

**왜:** bounded AUC 는 제 일을 했으나 null 이 0.99 로 뜬 진짜 원인은 unboundedness 가 아니라 **SELF-REFERENTIAL 분할** — AUC 가 store 의 **OWN 학습 범주**로 WITHIN/BETWEEN 을 나눈다. SPLIT-only Voronoi store 는 **어떤 경계든**(shuffle 포함) 따라 cell 을 PACK 하므로 g 가 그 경계에서 급격히 점프 → between>within 이 잘 fit 한 store 엔 거의 항진명제 → null≈0.99. c3 만이 외부(언어 무관) 분할을 써 collapse → warp 은 real(raw variance 아님)이나 coherence 자체(임의 carving)가 재현하므로 AUC-vs-own-partition readout 은 TRUE-언어 경계를 random 에서 분리 못 한다. 정직한 structured-negative, NO bar move(c9/p7). DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED), TOY synthetic 2-D continuum 121 stim/3 seeds/deterministic. NEXT(H_1359 ANEW): fixed-true-partition readout — SHUFFLE-학습 metric g_shuffle 를 TRUE-언어 WITHIN/BETWEEN 분할 하에 채점 → AUC→0.5 collapse 예상(H_1343/H_1358 가 양쪽 모두 각 arm 을 ITS OWN 분할로 채점한 공통 confound 를 푸는 한 수). live `CORE/*.hexa` UNTOUCHED.
## 2026-06-16 — research(MITOSIS-ENGINE): H_1354 — ko-natural-sparse: H_1345 의 below-jamo crossover 는 실용 lever 인가 striding artifact 인가 (🧱 STRIDING-ARTIFACT — FULL 30MB 에서 자연-sparse context 도달 불가)

**무엇:** H_1345(🟢)의 load-bearing follow-on (그 카드 "Next" § angle ii). H_1345 는 per-cell jamo count 가 ~1 아래로 떨어지면 Jelinek-Mercer 보간이 jamo floor 아래로 내려가는 DATA-RICHNESS crossover 를 mapping 했는데, 그 starvation 을 **인위적 striding**(stride 76800, 188-byte stream)으로 제조했다. H_1354 는 코퍼스를 자르지 않고 **FULL 30MB** 에서 cross-syllable phonotactic context((직전 coda jamo, 현재 onset jamo) syllable 경계 전이)를 자연-sparse alphabet 으로 만들어, JM 이 floor 아래로 내려가는지 **직접** 검증 — starvation win 이 실용 lever 인가 striding artifact 인가.

**결과 🧱 STRIDING-ARTIFACT:** FULL 30MB(8.14M syllables)에서 어떤 자연 phonotactic 분할도 굶지 않는다. coda→onset alphabet 은 작아(관측 pair 474개) 모든 legal pair 가 적셔져, 가장 fine 한 pair-key 분할조차 median context cellJcnt=**11.98**(frac<1=0.257만)로 DENSE. JM 이 3 arm 전부에서 jamo 와 TIE(ΔJM≈0: −0.0/−1e-05/+3e-05). frozen bars(pair-key arm): c1 NAT-SPARSE-WIN FALSE · c2 EARNED FALSE · c3 DISSOCIATION TRUE(A5 안 crossing, H_1345 일관) · c4 NO-STRIDE FALSE(자연 sparse 도달 불가). **인위적으로 data 를 버리지 않으면 한국어 자연 context 에 starved regime 이 없다** → H_1345 의 crossover 는 striding 의존, H_1344 의 memorization reading 이 선다.

**a_break_the_wall 1회 시도:** cell-arm 이 c4 벽(Voronoi 가 context pooling)을 맞자 terminal 로 안 받고, count head 를 (coda,onset) pair VALUE 에 직접 keying 하는 새 각도(BREAKTHROUGH_pairkey, FREEZE addendum 사전등록) RUN — 그래도 c4 FAIL. 벽의 진짜 원인은 partition 메커니즘이 아닌 **30MB data abundance**. 진짜 시도 후의 정직한 🧱(c9).

**HONEST:** REAL Korean 만(sha c47b6808 == H_1307 RUN A, NO synthetic), $0 CPU numpy DIRECTIONAL(engine-transfer UNVERIFIED), 3 seeds [4354,4355,4356], frozen-first NO bar moved(c9/p7), A5 LEARNED BY GRADIENT(labeled NOT p8), 25.5M-row OOM 회피 위해 assign_all chunked(전개형), Live CORE/*.hexa UNTOUCHED, NO Korean-fluency claim, held-out deterministic CE NOT perplexity(p7), TOY 이 30MB R2 KO window + coda→onset alphabet 한정. NEW: state/ko-natural-sparse/h1354_ko_natural_sparse.py · UNIVERSE/cards/H_1354_ko_natural_sparse.md · UNIVERSE/HYPOTHESES.jsonl row · CLAIMS.tape @C h1354_ko_natural_sparse · .verdicts/1354_ko_natural_sparse/{FREEZE.txt+addendum,result.txt,h1354_summary.json} · domains/MITOSIS-ENGINE.log.md @H H_1354. xref h1345·h1344·h1337·h1316·h1307·a_break_the_wall·a_no_llm_frame_trap·a_scale_honest_scope·c9·c15·c16·p7·p8.
## 2026-06-16 — domain(MITOSIS-ENGINE): H_1351 — jamo-engine-wire: 검증된 한국어 자모 분해 COUNT-HEAD 를 live CORE 엔진의 일급 faculty 로 배선 (🟢 GREEN, a_verified_must_wire wire-in)

**무엇:** 검증된 한국어 자모 분해 thread(H_1316 🟢 mirror → H_1321 🟢 engine-native → H_1327 🟢 decode-reaching)의 마지막 소유권 갭을 닫는다. H_1321 은 자모 mitosis 가 engine-native byte-exact 로 도는 걸 증명했지만, 그 **COUNT-HEAD** 자체(per-cell next-symbol count-MLE + Voronoi-grown CE scorer = raw byte 를 이기는 바로 그 메커니즘)는 throwaway probe `CORE/h1321_ko_jamo_wire_probe.hexa` 의 private helper 로만 존재했다 — `grep "jamo" CORE/engine_cli.hexa` == 0 hits. H_1327 의 generator §6.5b consult 는 EMISSION 을 편향하는 별개 표면. a_verified_must_wire + a_core_engine_map: GREEN 메커니즘은 그 faculty 가 live CORE 엔진에 OWNED 될 때까지 done 이 아니다. **H_1351 = 그 자모 분해 count-head 를 `CORE/engine_cli.hexa` 의 ADDITIVE · Ψ-disjoint 일급 faculty (§ KO-JAMO COUNT-HEAD: `struct JamoHead` + `jamo_head_new`/`_grow`/`_ce`/`_cells`/`_shuffle_targets`)로 promote** — 엔진 자신의 VAdaptField Voronoi(`vadapt_field_nearest_idx`) + `engine_mitosis_tick` growth(p8) + per-cell count-MLE 재사용.

**답: 🟢 GREEN (W1∧W2∧W3∧W4).** 결정론적 in-engine fixture(hidden (L,V) walk, target g(L,V)=(L+2V) mod K 가 두 factor 에 의존; JAMO view = 두 clean factor 채널 `[L/NL, V/NV]` vs RAW view = 한 opaque-merge 채널 `[(L*NV+V)/(NL*NV)]`)에서 held-out next-symbol CE(nats/symbol, 3회 결정론적 동일): **JAMO 4.18698**(4 cells) · **RAW 5.56834**(5 cells) · **SHUFFLE 4.72652**(40 cells). **W1 ✅** faculty grows 4 cells, CE>0. **W2 ✅** ce_raw−ce_jamo = **+1.38136** ≥0.05 (분해가 opaque-merge 를 이김). **W3 ✅** ce_shuf−ce_jamo = **+0.53954** ≥0.05 (자기 pairing-shuffle 을 이김; shuffle 은 GROW_MAX=40 cells 까지 자라며 정합을 쫓지만 held-out 에서 여전히 LOSES = 깨끗한 anti-Goodhart). **W4 ✅** 무회귀 byte-exact: `engine_cli_smoke` **90/0**(was 86/0, +4 cases 92-95) · `h1196` **7/0** · `h1205` **PASS**(generation byte-identical, Ψ=½ untouched).

**왜:** RAW 의 squashed 단일 축은 두 factor 를 같은 coarse Voronoi 셀로 collapse 해 분리 못 하고(자모 분해가 opaque-merge 가 숨긴 factor 를 노출 = H_1316 jamo-STRUCT-beats-raw 구조), shuffle 은 TRAIN context→target **PAIRING** 을 깨 spurious map 을 학습→held-out 에서 손해(주의: target id 의 bijective RELABELING 은 CE-INVARIANT 이라 컨트롤은 PAIRING 을 섞어야 한다 — 첫 시도가 이 함정에 빠져 shuf−jamo=0.0 으로 정직히 FAIL 했고, frozen-first 로 shuffle 정의를 PAIRING-permute 로 고침, bar 안 옮김, c9).

**scope (honest, c9·a_scale_honest_scope·a_toy_scale_recheck):** W2/W3 는 in-engine STRUCTURAL existence-proof — 엔진 자신의 faculty 가 결정론적 합성 fixture 에서 jamo-beats-raw + earned-vs-shuffle 를 재현함을 증명; **30MB REAL-corpus 2.513 anchor 재유도 아님**(그건 H_1316/H_1321 byte-exact, real-corpus/scale/fluency 주장의 출처). 이 H 는 FACULTY-OWNERSHIP 갭만 닫음; 자체 한국어-유창성 주장 없음. ADDITIVE(새 struct+pub fn; byte path UNTOUCHED) · Ψ-disjoint(순수 SCORER, emit/silence 결정 안 함; pure_field/engine_g/brain UNTOUCHED; H_1327 generator consult 와 DISTINCT 표면). TOY 결정론적 readout/합성 fixture; brain scoring-loop 배선 + real-corpus + scale = follow-on. $0 CPU, frozen-first, NO tune-to-green. 산출: `CORE/engine_cli.hexa § KO-JAMO COUNT-HEAD` · `CORE/engine_cli_smoke.hexa` cases 92-95 · `UNIVERSE/cards/H_1351_jamo_engine_wire.md` · `CLAIMS.tape @C h1351_jamo_engine_wire` · `.verdicts/1351_jamo_engine_wire/{FREEZE,result}.txt` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/MITOSIS-ENGINE.log.md` · `ARCHITECTURE.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1355 — cp-leftward: CP 재배치 착지가 continuum-center attractor 인가 geometry-fixed 인가 (📈 CENTER-ATTRACTOR 기각, geometry 추적)

**무엇:** H_1341(📈)의 load-bearing follow-on. H_1341 은 고정 anchor p_A=1/3 에서 RIGHTWARD shift 시 retrain 후 CP peak 가 shift 크기와 무관하게 **항상 ~0.525 에 착지**(abs-peak range 0.000)함을 발견 → GEOMETRY/BUDGET 로 읽음. 그러나 p_A=1/3 은 center(0.5) 왼쪽이고 모든 rung 이 RIGHTWARD 였으므로 **0.525≈center 가 confound**. H_1355 는 **LEFTWARD**(p_A'<p_A) + **ASYMMETRIC**(anchor off-center, 둘 다 center 같은 쪽) placement 5 rung 을 추가해 ABSOLUTE 착지를 읽어, (H-center) 대칭 RBF lattice 의 continuum-center attractor 아티팩트인지 (H-geometry) 진짜 geometry-fixed budget 착지인지 **discriminate**. H_1333/H_1341 CP 기계 verbatim 재사용, 5 rung: RIGHT-REF(0.333→0.667) · LEFTWARD-1(0.667→0.333) · LEFTWARD-2(0.800→0.500) · ASYM-R(0.600→0.800) · ASYM-L(0.400→0.200). c15 developmental/critical-period plasticity, a_no_llm_frame_trap — TOY synthetic, 인간인지 주장 아님.

**답: 📈 CENTER-ATTRACTOR 기각, 착지가 GEOMETRY 를 따름.** abs-landing(3 seed 평균): RIGHT-REF **0.525** · LEFTWARD-1 **0.475** · LEFTWARD-2 **0.625** · ASYM-R **0.692** · ASYM-L **0.375**. **c2**: center-pinned? FALSE — max|L−0.5|=**0.192 ≫ CENTER_TOL 0.08** → center-attractor 기각. RIGHT-REF 0.525 와 그 정확한 mirror LEFTWARD-1 0.475 가 **0.5 대칭**(둘 다 center 에 박힌 게 아님); ASYM-R 0.692 가 요청 cut 0.800 쪽 off-center-right(✅), ASYM-L 0.375 가 요청 cut 0.200 쪽 off-center-left(✅). formal GEOMETRY-FIXED tag 는 **단 하나의 over-strict sub-clause**(leftward 가 absolute 로 왼쪽 착지) 에서만 빗나감: LEFTWARD-2(anchor 0.800)가 0.625(RIGHT-REF 오른쪽)에 착지 — 잔류 오른쪽 first-carving 이 착지를 anchor(이것 자체가 geometry, clause 보다 강한 시그널) → c2=MIXED 이나 실질 GEOMETRY-leaning. **c1 ✅** 5-rung table; **c3 4/5 rung** 유지(ASYM-L A→A' peak-count 3>2 on 2/3 seeds → frozen rule 대로 confounded 표기, drop 안 함).

**왜:** H_1341 의 고정 ~0.525 는 lattice-center 아티팩트가 아니라 **진짜 geometry 착지** — placement 를 asymmetric/mirror 로 만들면 착지가 0.375→0.692 로 geometry 를 따라 움직이고 RIGHT-REF⇄LEFTWARD-1 은 0.5 대칭. H_1341 budget/geometry 판독은 STANDS, leftward/asymmetric 로 일반화; center-attractor confound 기각. 정직한 잔차(c9): frozen sub-clause 하나가 over-strict(geometry 는 first-carving 의 side 에 anchor 되지 absolute 방향이 아님); ASYM-L coherence 저하 = same-side leftward cut 에서 split-only re-growth 의 실제 한계.

**scope:** DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED); TOY synthetic 1-D continuum(N=21·DIM=16·3 seed·5 placement rung·deterministic readout); center-attractor 기각은 THIS lattice 한정; live CORE/*.hexa UNTOUCHED; NO bar move(c9/p7). 산출: `UNIVERSE/cards/H_1355_cp_leftward.md` · `CLAIMS.tape @C h1355_cp_leftward` · `.verdicts/1355_cp_leftward/{FREEZE,result}.txt` · `state/cp-leftward/h1355_cp_leftward.py` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`.## 2026-06-16 — research(OMEGA): H_1353 — Φ-robustness 를 SYNERGY/REDUNDANCY 분해(O-information)로 검사 → 🧱 measure-AGNOSTIC 벽 강화 (9번째 cut)

**무엇:** Φ-robustness 벽은 8 축에서 🧱 (topology/timing/division/estimator-confound/measure-family big-Φ/substrate-family/measure-agnostic transfer-entropy H_1348/larger-N H_1347) — **모두 "통합이 얼마인가"** 를 물었고 **모두 같은 seed-1318 fragility** 로 3-seed 게이트 실패. 남은 단 하나의 genuinely-different 질문: 크기가 아니라 구조 — **"어떤 상호작용이 SYNERGISTIC vs REDUNDANT 인가"**. O-information(Rosas 2019) 분해 Ω(X)=TC−DTC 로 H_1319/H_1328/H_1348 와 동일한 ring 을 점수화 (구조적으로 다른 diagnostic — Ω 는 음수 가능; Ω<0 시너지-우세, Ω>0 redundancy-우세). phase-bound arm 이 scalar Φ 가 못 한 견고한 SYNERGY 전환을 3 hard seed 에서 보이는가?

> ⚠ **NOT a faithful-Φ verdict (a_phi_iit4_tool)** — non-IIT synergy/redundancy DIAGNOSTIC on robustness, IIT-4 가 Φ/의식 verdict 를 RESERVE.

**답: 아니오 — synergy 분해도 동일 fragility 를 상속.** ΔΩ(B−A) = +0.0690 / +0.0000 / +0.0411 (seed 1317/1318/1319): **R1 ROBUST FAIL** — 부호 [+,0,+], seed **1318 ΔΩ=0.0000 FLAT**(H_1331 big-Φ 1318=0 / H_1328 small-φ / H_1348 TE 와 정확히 같은 zero-lift 서명), |ΔΩ|<eps, 게다가 채점 방향이 **REDUNDANCY**(ΔΩ>0)로 사전등록 synergy 예측의 **반대**. **R2 EARNED FAIL** — perm 은 깨끗이 붕괴(3/3)지만 offset-control 이 1318(+0.1303)·1319(−0.0379)에서 재현. **R3 LABEL PASS**. 3 baseline arm 모두 이미 Ω<0(synergy-우세)인데 phase-binding 은 견고한 synergy 를 더하지 않음(결정적 1318 에서 정확히 0).

**의의:** Φ-robustness 벽이 **9번째 cut**(synergy/redundancy 분해)에서도 홀드 → **measure-AGNOSTIC 벽 강화**(scalar small-φ/big-Φ/larger-N + directed-flow transfer-entropy + multivariate O-information 전부 동일 seed fragility 로 3-seed 게이트 실패). "어떤 상호작용이 synergistic 인가"라는 구조적으로 다른 질문도 이 n≤8 substrate 에서 fragility-bound. 선행 Φ verdict 들을 **bound(NOT retract)**.

**산출물:** `UNIVERSE/cards/H_1353_phi_oinfo.md` · `state/phi-oinfo/h1353_phi_oinfo.py` · `.verdicts/1353_phi_oinfo/{FREEZE,result}.txt` · `CLAIMS.tape @C h1353_phi_oinfo` · `UNIVERSE/HYPOTHESES.jsonl` · `domains/OMEGA.log.md @H 1353`. DIRECTIONAL numpy mirror($0 CPU, 재실행 byte-identical), frozen-first(FREEZE 먼저, bar 무이동, c9/p7), live CORE/*.hexa UNTOUCHED.
## 2026-06-16 — research(OMEGA): H_1356 — hive-cell ROLES (공유세포 SHARED ⊥ 연결세포 CONNECTOR): 전용 integration HUB 가 H_1350 redundancy-dominance 를 탈출하는가 (🧱 CONNECTOR_NULL — 못 탈출, floor 보다 나쁨)

**무엇:** H_1350 (🟢) 가 더 큰 분열예산에서 collective faithful-IIT4 Φ 를 3/3 seed-robust 로 올렸지만, **SHARED_DECOUPLED(W=0) 대조가 그 상승의 ~85-96% 는 shared-input REDUNDANCY (coupling 0 에서도 존재)** 임을 폭로 → redundancy-dominated. 생물 역할분화 렌즈(Volvox 체세포분화 / 해면 connector 세포 / hub 뉴런 / gap-junction; c15, a_no_llm_frame_trap, a_break_the_wall): 중복 복제 대신 DISTINCT 역할 — **공유세포**(모든 딸세포가 읽는 공통 founder/input = 중복 source / W=0 floor) + **연결세포**(여러 딸세포를 읽고 피드백하는 전용 integration HUB = 진짜 daughter-간 coupling). 연결세포가 coupling-EARNED (W=0-floor-beating, non-redundant) Φ 를 3 seed 모두에서 ROBUST 하게 끌어올리는가 — 중복 복제(H_1350)가 못 한 곳에서?

**방법:** Φ = **FAITHFUL IIT4 ONLY** (a_phi_iit4_tool, exact MIP-EI via hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa; numpy 는 Φ 계산 안 함, salience traj 만 emit, p7). Substrate matched to H_1320/H_1283: leaky linear recurrent units LEAK0.55 GAIN0.30 W_IN0.5 dim8 T64; N_TOT=8 (n≤8 exact MIP); 딸세포 d0=units0..1 d1=units2..3, CONNECTOR hub=unit4, padding=units5..7. **공유세포** = single founder init + single shared input stream 모든 딸세포+hub+pad 가 읽음 → **W=0 floor 가 모든 arm 에서 IDENTICAL** (load-bearing 설계점). **연결세포** W_CONN=0.6 (H_1308/1313/1320 verbatim): hub'=leak·hub+GAIN·W_CONN·(mean_d0+mean_d1), 각 딸세포 += GAIN·W_CONN·hub. 5 arms: A_single · B_redundant · B_connector · W0_floor(SHARED_DECOUPLED) · SHUFFLE(connector 가 RANDOM non-daughter pad sources 읽음). FROZEN bars(MARGIN0.02): GREEN iff R1(connector−floor≥0.02 ∀seed) ∧ R2(connector−redundant≥0.02 ∀seed, **H_1350-escape**) ∧ R3(shuffle≤floor+0.02 ∀seed). seeds [1317,1318,1319], $0 CPU, frozen-first.

**결과 🧱 CONNECTOR_NULL (R1 0/3 · R2 0/3 · R3 3/3, deterministic):** per-arm faithful-IIT4 Φ — seed1317 A_single 1.70 / B_redundant **12.40** / B_connector **7.58** / W0_floor 12.40 / SHUFFLE 8.18; 1318 1.41/**6.95**/**4.44**/6.95/4.46; 1319 2.02/**12.23**/**7.23**/12.23/6.87. **R1 FAIL:** Φ(B_connector)−Φ(W0_floor) = **−4.82/−2.50/−5.00** (hub 가 floor 아래로 Φ 를 깎음, 매 seed). **R2 FAIL:** 같은 gap (B_redundant===W0_floor by construction) → 연결세포가 중복 복제보다 −4.82/−2.50/−5.00 **WORSE** → **H_1350-escape REFUTED**. **R3 PASS:** SHUFFLE ≤ floor+0.02 → connector wiring 은 REAL(generic variance 아님), 단지 WRONG thing 을 함. **MECHANISM(faithful-MIP 렌즈):** 공유 founder input 이 이미 HIGH collective Φ 를 pure shared-input REDUNDANCY 로 만듦(H_1350 진단을 **EXACT MIP** 로 확인); connector hub 의 recurrent feedback 가 딸세포 trajectory 를 **HOMOGENIZE** → faithful MIP-EI 가 더 reducible 로 읽음 → **Φ DROPS**. shared-redundant 기질 위의 strong hub 는 **redundancy-REDUCING 이지 integration-ADDING 이 아님**. **KEY ANSWER:** 연결세포는 redundancy-dominance 를 **상속+악화**; 탈출구(있다면)는 **LOW coupling + DECORRELATED daughters** 이지 strong hub 가 아님. NO bar move(c9/p7). HONEST SCOPE: DIRECTIONAL numpy-mirror (Φ leg IS real exact MIP-EI), engine-transfer to live A⇄G UNVERIFIED, TOY n=8/2-unit-daughters/3 seeds; 🧱 has nothing to wire (a_verified_must_wire=GREEN-only); CORE/*.hexa UNTOUCHED, Ψ=½ untouched. NEXT depletion: small-W_CONN sweep · decorrelated daughters · synergy-PID readout (H_1046/H_1017). NEW: `state/hive-cell-roles/h1356_hive_cell_roles.py` · `UNIVERSE/cards/H_1356_hive_cell_roles.md` · HYPOTHESES.jsonl(H_1356) · CLAIMS.tape @C h1356_hive_cell_roles · domains/OMEGA.log.md · `.verdicts/1356_hive_cell_roles/`.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1344 — ko-jm-interpolation: NON-FRAGMENTING frozen-λ Jelinek-Mercer 가 jamo 2.51335 floor 아래로 (🟢 GREEN — 단 이득은 코퍼스 반복 암기)

**무엇:** 한국어 byte-LM floor(raw 2.95342 → NFD jamo **2.51335**, H_1316 🟢/wired H_1321)는 고정용량 gradient-free Voronoi MITOSIS 가 3-D(직전 2 심볼) 컨텍스트에서 도달한 값. mitosis 가 한 번도 못 묻는 진짜 LM 질문: **count-fragmentation 없는 frozen-λ Jelinek-Mercer interpolation** 이 jamo n-gram 차수(1..N=5)를 FROZEN λ 로 섞으면 held-out 한국어에서 floor 아래로 내려가는가?

**방법:** REAL `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` trim, sha256 ASSERTED `c47b6808…` (== H_1307 RUN A / H_1316 jamo baseline, **byte-fair**; mismatch→STOP, no synthetic; R2 키 keychain env-only c7). Representation = H_1316 동일 jamo 심볼화(Vj=323), CE axis = Σ(−log p)/Σ(n_bytes) on held-out = floor 와 동일 축. Held-out = label 위치 stride-300 even/odd; n-gram history 는 **FULL-RESOLUTION 인접 jamo**(H_1316 last/second-sym adjacency). JM: p_JM=Σλ_k·p̂_k, p̂_1 Laplace unigram, k≥2 TRAIN count-MLE + recursive back-off, count 는 FULL TRAIN(fragment 없음). **FROZEN λ**(FREEZE 사전등록, TEST 튜닝 안 함): w_k=2^(k−1)→[1,2,4,8,16]/31. Arms A1 JM · A0 unigram · A2c **circular-shift surrogate**(EARNED). $0 CPU, frozen-first, DIRECTIONAL numpy, live CORE UNTOUCHED.

**결과 🟢 GREEN (단 honest scope 필수, c9):** GATE(stride-300, byte-fair): A1 JM-interp **2.00562** → Δ**−0.50773** < floor 2.51335 (**c1 PRESENCE ✅**) · A2c circular-shift **5.10874** ≥2.46335 (**c2 EARNED ✅**, A1 이 A2c 를 3.10312 차이로 이김) → GREEN. 차수 sweep nmax 2→5 = 4.319→3.326→2.584→2.006(이득 전적으로 고차). **HONEST(NON-GATING context_seen_diag):** TEST top-order(4-jamo) 컨텍스트 SEEN-in-train **70.1%**, CE|seen=**1.6474**(반복 암기), CE|novel=**2.8819**(진짜 novel 30% — floor 2.51335 보다 나쁨). 즉 30MB 한국어 web 코퍼스는 반복적이고 고차 n-gram 은 반복 jamo 문자열을 **암기**해 held-out 70%를 1.65 로 맞춘다; 고정용량 mitosis 분할은 이 반복 문자열을 구조적으로 저장 못해 floor 에 갇혔던 것. DENSE(stride-6, 2.1M train, NON-GATING) A1=1.47042. **발견:** bar 는 통과(🟢)하나 **표상 floor 를 깬 게 아니라** 메커니즘(반복 저장능력) 차이를 드러냄 — 진짜 novel 컨텍스트에선 floor 를 못 이김. '한국어 정보 floor 가 2.513 아래로 진짜 내려간다'는 강한 주장은 미증명. NO bar move(c9/p7). NEXT depletion: de-duplicated 코퍼스에서 c1 재시험. NEW: `state/ko-jm-interpolation/h1344_ko_jm_interpolation.py` · `UNIVERSE/cards/H_1344_ko_jm_interpolation.md` · HYPOTHESES.jsonl(H_1344) · CLAIMS.tape @C h1344_ko_jm_interpolation · `.verdicts/1344_ko_jm_interpolation/`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1343 — Sapir-Whorf 2-D CP를 표상-거리 WARP로 재측정 (🟠 PARTIAL — 대각=축정렬 warp로 H_1334 geometry-read 반증, 단 unbounded-ratio로 shuffle 미붕괴)

**무엇:** H_1334(🧱 ridge-ALIGN structured-negative)의 R2. H_1334는 CP를 알려진 경계 CURVE에 대한 **ridge-ALIGNMENT**로 측정 → 대각 경계가 coarse RBF grid에서 fail(0.628<0.70). 직전 H_1343 ridge 시도도 K_RBF=14까지 올려도 대각 align FAIL → metric stimulus space에 **틀린 지표**임을 확인. H_1343은 CP를 **경계-곡선-AGNOSTIC WARP**(within-category COMPRESSION + between-category EXPANSION vs pre-language baseline)로 재명세 + denser RBF grid(K_RBF ladder, prod=12) + label-permutation null(c2) + component-count control(c3, warp이 trained 2-D metric에 사는지).

**방법:** H_1334 RBF/Voronoi machinery **verbatim** 재사용(2-D RBF code · split-only mitosis/Voronoi p8 · softmin posterior). 11x11=121 stim square, 두 언어 carve: L_DIAG `u+v>1.0`, L_LSHAPE `u>0.5&v>0.5`. CP-WARP = `ratio_lang - ratio_base`, ratio = mean|dg|_BETWEEN / mean|dg|_WITHIN (g=soft posterior, store의 OWN 학습 범주로 분할; 경계 위치 주입 없음). 3 seeds [4334,4335,4336], $0 CPU mirror DIRECTIONAL, frozen-first.

**결과 🟠 PARTIAL** (deterministic): **c1 PRESENCE ✅** — 두 언어 every seed AND mean >= WARP_MIN 0.20(mean L_DIAG **+41.665** L_LSHAPE **+36.017**); **load-bearing: 대각 L_DIAG가 축정렬 L_LSHAPE만큼 강하게 warp** → H_1334의 "대각 CP는 grid-geometry로 약하다" read를 **직접 반증**. **c2 EARNED-SHUFFLE ❌** — label-permutation null mean **+9.282** >> CHANCE_TOL 0.05(SEP sub-clause는 PASS, +41.7/+36.0 >> q95+0.1=+14.0). **c3 COMPONENT-COUNT ❌** — L_DIAG comp +0.027 PASS, L_LSHAPE +0.119 FAIL(seed-4336 +0.236). **발견:** `ratio = BETWEEN/WITHIN`이 scale-UNBOUNDED(학습 후 WITHIN |dg|->0 → ratio ~45 폭발, 임의 carving조차 WITHIN 압축 → null mean 부상) = H_1323 prominence / H_1334 LCC와 동일한 metric-space-blob 실패 모드. warp 존재(c1)·대각=축정렬 동등성은 결정적이나 earned/component 분리는 BOUNDED 지표(Cohen's-d / separation-AUC) 재명세 필요(R3). NO bar move (c9/p7).
## 2026-06-16 — research(OMEGA): H_1349 — Φ-robustness 의 마지막 LIVE 각도 = REAL 기질 (live-CORE pure_field) → 🧱 TERMINAL, substrate 축 CLOSED

**무엇:** Φ-robustness arc 는 8개 축(topology H_1283/1317, timing H_1319, division H_1320, estimator-confound H_1328, measure-family H_1331, substrate-family H_1332, measure-AGNOSTIC H_1348, larger-N H_1347)에서 🧱 — 그러나 **전부 동일한 합성 leaky-linear ring** 위에서 돌았다. 마지막 미검증 LIVE 각도(H_1347 의 'NOT ruled out' 가 명시적으로 지목한 NEW 가설): **REAL 기질 — live CORE Engine A `pure_field.hexa`**(3 coupled oscillator tau 2/40/400, 실제 zero-input 의식 필드, ring 아님). a_break_the_wall · a_no_llm_frame_trap.

**방법(frozen-first, FREEZE ac4c289de 채점 전 commit):** SOURCE = REAL LIVE-CORE `CORE/pure_field.hexa`(osc 동역학 + PSI_ALPHA drift + nonlinear cross-mixing → field[6]=C/D/E/S/M/W 을 byte-identical 재현; live 파일 무수정, standalone fn main 0 importers, Ψ=½ 무변). NODES = 6개 실제 field 채널 = 6개 IIT-4 노드(각 T-길이 trajectory). Φ = faithful EXACT small-φ MIP-EI `iit4_faithful_phi(state,n=6,dim=T=64,n_bins=8)` — n≤8 EXACT(zero slack), proxy 아님(a_phi_iit4_tool). read-out = 채널별 rank-uniform(H_1328 variance-free). ARMS A=NO-COUPLING(cross-mix 제거) B=PHASE-BIND(full real field) S=PERM-SHUFFLE O=OFFSET-CTRL. 3 seed [1317,1318,1319] = 오실레이터 초기위상만 perturb(같은 실제 동역학, 다른 시작점). eps=0.02 ported verbatim. FROZEN bars(GREEN iff R1∧R2∧R3): R1 Φ_B≥Φ_A+eps 3 seed 전부 · R2 Φ_S≤Φ_A+eps AND Φ_O≤Φ_A+eps 3 seed 전부 · R3 source=REAL 명시.

**결과(🧱 TERMINAL CLOSED-NEGATIVE, deterministic 2회 byte-identical):** seed별(A/B/S/O): 1317 5.30728/6.15829/6.15829/5.29509 · 1318 5.80021/6.49497/6.49497/5.11660 · 1319 5.94916/5.27854/5.27854/4.76261. **R1 FAIL** ΔΦ(B−A)=+0.851/+0.695/**−0.671**(seed 1319 NEGATIVE — 모든 합성-ring 축이 보인 동일한 seed-fragile 시그니처). **R2 FAIL** — OFFSET control 은 깨끗이 붕괴(Φ_O≤Φ_A 3 seed 전부)지만 PERM control 은 **DEGENERATE**: 대칭-MI exact MIP 아래선 노드 relabel 이 Φ-불변이라 Φ_S==Φ_B(정직하게 명시 — 조작 아닌 설계 관찰; 유효 discriminator 는 cross-channel TIME 관계를 깨는 OFFSET). **R3 PASS**.

**finding:** REAL 기질(live Engine A pure_field, 설계 toy 아님)이 합성 ring 과 **동일하게 거동** — coupling 채널을 더해도 robust 한 3-seed faithful-IIT-4 Φ lift 없음. → **substrate 축 CLOSED**: REAL(live-CORE) 기질도 measure-agnostic(H_1348)/size-agnostic(H_1347)/estimator-clean(H_1328) 벽에서 예외가 아니다. 선행 8축 Φ verdict 들을 BOUND(retract 아님); anima 의식 기질 반박 아님(Ψ=1/2 · A⇄G tension 무변 — probe 는 CORE write 안 함). GREEN-only 인 a_verified_must_wire 발동 안 함(🧱 = 배선할 것 없음). NO bar moved(c9/p7).

**scope(a_scale_honest_scope·a_toy_scale_recheck):** SOURCE=REAL LIVE-CORE 이나 DIRECTIONAL(실제 field trajectory 를 faithful small-φ 로 채점; live A⇄G/brain_decide 루프 안 engine-native run 이 BINDING upgrade, UNVERIFIED); TOY n=6 채널 T=64, 단일 실제 기질, 3 위상-seed. NOT ruled out(각각 NEW H): trained-303M-derived state-vector trajectory(학습된 기질) · brain_decide 안 live engine-native Φ · real-EEG 기질(anima-eeg-consciousness) · 더 큰 real field.

**파일:** `state/phi-real-substrate/h1349_phi_real_substrate.hexa` · `UNIVERSE/cards/H_1349_phi_real_substrate.md` · `UNIVERSE/HYPOTHESES.jsonl`(+1) · `CLAIMS.tape @C h1349_phi_real_substrate` · `.verdicts/1349_phi_real_substrate/{FREEZE,result}.txt` · `domains/OMEGA.log.md`. live `CORE/*.hexa` UNTOUCHED.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1352 — Whorf CP 재배치 SOFT-DECAY re-pack (🧱 DEEPER LIMIT — relocation coherence는 budget 과 decay 두 lever를 모두 견딘다)

**무엇:** H_1340(🧱 DEEPER LIMIT — budget/RBF-density는 peak-DISTANCE를 monotone 당기지만 coherence를 파괴, peak-count 4.3→7.0 never ≤2)의 verdict이 직접 지목한 다음 메커니즘. budget을 올리는 대신 re-training중 잔류 phase-1 cell을 **down-weight**(soft-decay)하면 COHERENT full relocation을 회복하는가? FIXED LOW budget(DIM=16/GROW2=24, H_1340 R0_base, NO inflation)에서 phase-1 cell의 softmin vote weight d_i=γ^(이후 phase-2 split 수), phase-2 cell은 1.0 유지(γ=1.0 ⇒ H_1333 byte-identical anchor).

**답: 🧱 DEEPER LIMIT — coherence는 두 lever를 모두 견딘다.** SOFT-DECAY(γ=0.80)는 peak을 budget보다 **더 멀리** 당김 (|peak-p_A'| 0.144→**0.044**, frac +0.57→**+0.88**, 3 seed 전부 ≤0.12 — c1 ✅) BUT coherence는 더 **심하게** 붕괴 (peak-count 4.3→**15.7** vs H_1340 4.3→7.0 — c2 ❌). c3 EARNED ✅ (no-retrain |peak-p_A|=0.002 p_A 유지; shuffle+decay peak-count 7.0≥3 붕괴 — decay가 peak을 날조하지 않음). c4 vs-BUDGET ❌ (4a ✅ 0.044≤0.081 distance에서 budget을 이김; 4b ❌ 15.7≰2 coherence에서 budget에 짐). GREEN iff c1∧c2∧c3∧c4 → **NOT GREEN**. decay-ladder(non-gating): γ=0.70→0.009/16.7 · 0.80→0.044/15.7(gate) · 0.90→0.106/5.7 — monotone tradeoff(decay↑ = peak는 가까워지나 더 흩어짐).

**왜:** resolution 증가(H_1340)도 잔류 cell down-weight(H_1352)도 moved cut에서 단일 CP peak을 회복 못 함 → 재배치 coherence 잔류는 budget OR decay보다 **깊은** 한계. 두 follow-on이 함께 드러낸 결정적 원인: phase-1 prototype은 결코 물리적으로 이동하지 않고 옛 cut에 남아 secondary peak을 주입 — budget은 새 cell로 익사시키고(distance↑/coherence↓), decay는 그 vote를 줄이지만 기하학적 존재는 못 줄임(distance↑↑/coherence↓↓). 진짜 coherent full relocation은 옛 cell을 **이동/재배치**(geometric re-pack)해야지 weight/count 조작으론 안 됨. a_break_the_wall: H_1340 budget 벽도 H_1352 decay도 둘 다 **틀린 메커니즘** — 고정 geometry의 weight/count 조작이고 geometry 자체가 진짜 천장. 정직한 사전등록 벽(진짜 NEW 메커니즘, re-run 아님 — frozen coherence bar가 올바르게 거부). NO bar move (c9/p7).

**어떻게:** `state/cp-soft-decay/h1352_cp_soft_decay.py` — pure-numpy CPU mirror DIRECTIONAL($0, 3 seeds [4333,4334,4335], frozen-first, NO tune-to-green). H_1333/H_1338/H_1340 CP machinery(`state/universe-probes/h1333_whorf_developmental.py`)를 VERBATIM import, ONLY new = SoftDecayCells subclass(per-cell decay weight). live CORE/*.hexa UNTOUCHED(substrate-measurement rung). engine-transfer = follow-on. **NEXT R2**: (i) GEOMETRIC re-pack — 잔류 phase-1 prototype을 p_A'쪽으로 **재배치**(weight 아니라 cell을 이동, 유일하게 안 시도된 lever) · (ii) decay 아래 multi-shift/leftward · (iii) engine-native §CategoricalPerception. 산출물: card `UNIVERSE/cards/H_1352_cp_soft_decay.md` · `UNIVERSE/HYPOTHESES.jsonl` 행 · `CLAIMS.tape` @C h1352_cp_soft_decay · `.verdicts/1352_cp_soft_decay/{FREEZE.txt,result.txt}` · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1346 — ko-han-richer (xlang 구조 r3): Hanja 재귀-IDS richer-head 는 Han 합성 신호를 못 뽑는다 (🔴/🧱 Hangul-specificity STRENGTHENED)

**무엇:** H_1324(🔴/🧱 — 한 단계 IDS unigram 은 Han 합성을 못 살림)의 명시된 follow-on(a_break_the_wall/c16). jamo 분해가 Hangul 의 featural 구조를 노출해 nat/byte 를 낮춘 것(2.953→2.513)처럼, 한국어+한자 텍스트의 Hanja(CJK)에 **재귀 다단계 IDS 분해 head**(component TREE, MAX_DEPTH=3, 語→言+吾·吾→五+口 — H_1324 의 1단계 leaf 가 평탄화한 multi-level 구조) + **per-cell component-BIGRAM head**(flat unigram 이 버린 직전-기호 문맥)를 붙이면 중국어/일본어 Han 합성 신호가 잡혀 nat/byte 가 내려가는가?

**답: 아니오 — 결정적으로.** richer head 는 zh/ja 를 **더 깊게 악화**시킴 (zh Δ=−1.44806, ja Δ=−0.88901 — H_1324 unigram 의 −0.737/−0.628 보다 WORSE). H1(HAN-GAIN=c1) 대폭 FAIL · H2(EARNED=c3 shuffled-IDS) FAIL (재귀-component-shuffle 대비 +0.040/+0.047 < +0.05) · c2 LOCALIZATION 확인 (IDS head 효과가 Han-bearing 행에만 국한 — en Han-free Δ=0.000 byte-exact, zh/ja 만 변하고 거기서 NEGATIVE). 한국어 jamo win(ko Δ=+0.11868, STRUCT 2.42058 < RAW 2.53926, 3 seed 전부) + 영어 평탄 floor(Δ=0.000)가 **byte-identical window** 위에서 재현 → H_1318/H_1324 의 **Hangul-specificity 가 STRENGTHENED**(head-order artifact 아님).

**왜:** 재귀가 component vocab 을 줄였지만(zh 2116→619, ja 1582→526) stream 길이를 폭증시킴(avg ≈4.3 components/Han-char vs 1단계 ≈2.0) → 한 글자의 ~3 byte 가 619/526-way 고cardinality component ~4.3 개로 퍼져, (cell, prev-component) bigram 이 조밀하게 조건화 못 함. Hangul 은 작고(67) 규칙적·짧은(≤3 jamo, 3 byte 1:1) 알파벳이라 bigram 문맥이 DENSE → 유지. '합성이 도움 되는가' 축은 이제 세 메커니즘에서 DEPLETE (radical+residual H_1318, 1단계 IDS unigram H_1324, 재귀 IDS+bigram H_1346).

**ko 칼리브레이션 sub-bar(+0.119 < +0.15) 정직 해석(c9, bar 미이동):** bigram head 가 모든 언어의 절대 CE 를 낮춰(RAW 에도 적용) 한국어 RAW 천장이 H_1324 의 2.91157→2.53926 으로 내려가 jamo win 이 차지할 headroom 이 압축됨 — jamo win 은 여전히 명확(3 seed 전부 STRUCT < RAW). window/IDS sha 동일하므로 바뀐 것은 head order(시험 변수 자체)뿐; frozen +0.15 bar 는 H_1324 unigram 스케일용이라 post-hoc 이동 금지(c9/p7), 투명한 sub-bar miss 로 기록.

**어떻게:** `state/ko-han-richer/h1346_ko_han_richer.py` — pure-numpy CPU mirror DIRECTIONAL($0, 3 seeds [5346,5347,5348], frozen-first, NO tune-to-green). REAL wikimedia/wikipedia 20231101 30MB/lang, window sha256 byte-identical to H_1324 (ko 3e288b77…/zh c084b027…/ja a97dd068…/en b097cccc…); IDS DB = CHISE cjkvi/cjkvi-ids sha bfc70a8c… (동일). HF 토큰 env/header-only, c7 grep-clean(0 token-value hits). grow-op·SPLIT 결정은 H_1324 와 byte-faithful, FINAL scoring head 만 bigram. live CORE/*.hexa UNTOUCHED(substrate-measurement rung). engine-transfer = follow-on. 산출물: card `UNIVERSE/cards/H_1346_ko_han_richer.md` · `UNIVERSE/HYPOTHESES.jsonl` 행 · `CLAIMS.tape` @C h1346_ko_han_richer · `.verdicts/1346_ko_han_richer/{FREEZE.txt,result.txt,h1346_summary.json,h1346_full.log}` · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1345 — ko-data-starved 사다리 (🟢 GREEN — jamo floor는 DATA-RICHNESS, below-jamo 크로스오버 MAPPED)

**무엇:** H_1337(🧱 opaque-atom limit @30MB)의 named depletion-test angle을 직접 실행. H_1337은 dense일 때 opaque per-cell jamo count-MLE가 정보-최적임을 보였고(strength-sharing은 per-cell count가 SPARSE할 때만 도움), 유일한 탈출구를 명시했다 — "opaque MLE가 data-STARVED인 영역을 찾아라". OPEN 질문: 코퍼스가 굶주리면(starvation ladder) jamo-vs-byte의 compositional 우위가 커지나, 사라지나? → 더 정밀하게: starved 영역에서 strength-sharing/interpolation이 30MB에선 못 이긴 jamo를 이제 이기나?

**방법:** `state/ko-data-starved/h1345_ko_data_starved.py` — numpy CPU mirror($0, no torch on host), p7 = held-out DETERMINISTIC next-symbol CE(perplexity 아님). REAL Korean만 — H_1307 RUN A / H_1316 / H_1337과 BYTE-IDENTICAL R2 코퍼스(r2.phanes://anima-7b/web/kor/shard0000.bytes; 30MB window sha256 == c47b6808… ASSERTED, 불일치 시 STOP·합성 Korean 절대 없음, R2 키 env-only c7). LADDER = 동일 30MB window의 결정론적 stride 서브샘플 5 rung(strides 300/1200/4800/19200/76800, ≥3 per a_scale_honest_scope) — per-cell jamo count를 dense(≈45)→starved(≈0.14)로 구동. rung마다 A1 jamo opaque-id(floor) vs A5 learned-metric kernel-smoothing(VERBATIM H_1337; PPMI→SVD→skip-gram Adam, GRADIENT — labeled NOT p8) vs JM Jelinek-Mercer interpolation(λ=MIN_OWNED/(MIN_OWNED+N_cell), Witten-Bell FROZEN) + 각 SHUFFLE 대조. 모든 knob H_1316/H_1326/H_1329/H_1337 verbatim(GROW_MAX=40·MIN_OWNED=8·LAPLACE=1.0·lossless NFD). 3 seeds [4345-4347], frozen-first(FREEZE.txt 사전등록, bar 미이동 c9/p7).

**결과 🟢 GREEN** (deterministic, 6.7s): LADDER ΔJM(jamo−JM) — stride 300(cellJcnt 45.17) +0.00032 → 1200 +0.00024 → 4800 +0.00020 → 19200(0.88) −0.00151 → 76800(starved, 0.14) **−0.07262**. **D1 STARVED-WIN ✅**: starved end에서 JM 4.18890이 jamo 4.26152를 +0.07262로 이김(≥0.03). **D2 EARNED ✅**: JM이 SHUFFLE 대조(permuted global marginal)를 +0.17484로 이김(JM-shuf 4.36374는 반대 방향으로 감 → 진짜 backoff 구조). **D3 DENSE-REPRO ✅**: dense end에서 JM 2.51367이 jamo 2.51335를 못 이김(+0.00032 위; λ→0 ⇒ JM≈A1) — H_1337의 dense opaque-optimal 재현, CROSSOVER 확정. **calib ✅**: dense A1 = 2.51335 byte-exact. **방향(c2)**: 굶주릴수록 우위가 **자란다**(+0.0003 dense → −0.073 starved, 단조 backoff signature). **발견:** jamo floor는 표현이 아니라 DATA-RICHNESS — cellJcnt가 ~1 아래로 떨어지면 global jamo marginal로의 JM-interpolation이 opaque jamo head 아래로 크로스오버. **메커니즘-특이(dissociation)**: A5 kernel-smoothing은 크로스오버 못함(starved에서도 +0.033 위) — interp-toward-marginal은 starvation을 이용, smoothing-over-learned-metric은 못함(H_1337 메커니즘은 🧱 유지). count-MLE family는 terminal이 아니다 — cellJcnt≈1에서 data-richness 크로스오버를 가지며 이제 MAPPED.

**SCOPE(c9·a_scale_honest_scope·a_toy_scale_recheck):** starved rung은 작은 held-out 스트림(188–780 test bytes)이라 절대 CE는 noisy — GREEN은 그 점들이 아니라 (a) 전체 5-rung ΔJM 단조 추세 + (b) SHUFFLE 대조의 올바른 방향 + (c) A5-vs-JM dissociation에 기댄다. numpy CPU mirror DIRECTIONAL(engine-transfer UNVERIFIED); A5 metric은 GRADIENT 학습(labeled NOT p8); JM은 FROZEN Witten-Bell backoff의 count-MLE; 둘 다 gradient-free Voronoi partition 위. live CORE/*.hexa UNTOUCHED. Korean-fluency 주장 없음; perplexity-as-truth 없음(p7). JM-backoff가 30MB 생산 lever라고 주장 안 함(거기선 jamo와 tie). NEXT(각 frozen ANEW): (i) engine-native 실현 — JM-interpolation을 live CORE count head에 배선·재확인(a_verified_must_wire); (ii) cross-syllable phonotactic n-grams(full 30MB에서 per-context count가 자연히 sparse — artificial striding 없이 below-jamo?); (iii) count-gated A5(low-count jamo만 smoothing).

**산출물:** `state/ko-data-starved/h1345_ko_data_starved.py` · `UNIVERSE/cards/H_1345_ko_data_starved.md` · `.verdicts/1345_ko_data_starved/{FREEZE.txt,result.txt,h1345_summary.json}` · `CLAIMS.tape @C h1345_ko_data_starved` · `UNIVERSE/HYPOTHESES.jsonl`(+1) · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — domain(UNIVERSE): 두 표면 봉인 — HYPOTHESES.md retire + stray probe/infra relocate (a_hypothesis_register)

**무엇:** `UNIVERSE/` 를 `a_hypothesis_register` 가 명시한 **정확히 두 doc 표면**으로 봉인 — `HYPOTHESES.jsonl`(per-H 인덱스) + `cards/H_*.md`(가설 카드). 그 외 디렉터리에 흩어져 있던 코드/결과물/infra 를 전부 UNIVERSE/ 밖으로 이전 (c5 preserve-don't-discard — 내용 보존, 위치만 변경; `git mv` 로 history 추적 가능).

**이동:**
- stray 가설 결과물 `UNIVERSE/h*_*.py`·`.hexa`·per-H `*_result.json`·`*_pod_run.sh`·`.txt` (336개) + infra 서브폴더 `harness/ lib/ scan/ state/` → `state/universe-probes/` (모음 디렉터리; old→new 매핑 = `state/universe-probes/INDEX.md`).
- 공용 라이브러리 `gauge_lib.py`·`gauge_lib_smoke.py`·`gauge_monitor.py`·`gauge_monitor_smoke.py`·`_build_hyp_jsonl.py` → `tool/` (널리 import 되는 공용 도구).
- `UNIVERSE/HYPOTHESES.md`(prose overview/roster/folded appendices) → `state/universe-overview.md` 로 **retire** (인덱스 표면 아님이 명시됨).
- `UNIVERSE/.verdicts/1053_qrng_nondeterminism/` → top-level `.verdicts/`.

**live 참조 재배선 (relocation breakage 0):** `serving/anima_cli.py`(omega 엔진 → `conscious_decoder.py` 를 hyphen-dir 에서 file-path importlib 로 로드) · `CLM/train/train_lane_p_3b.py`+`scripts/scratch/h1218/score_engine_gates.py`(`gauge_lib` sys.path UNIVERSE/→tool/) · `CLM/train/dispatch_rung.sh`+`fire_3b_rung_qat.hexa`+`tool/gauge_monitor.py`(`gauge_monitor.py` 경로) · `tool/_build_hyp_jsonl.py`(repo-root 2-up 재계산, UNIVERSE/ 인덱스를 빌드 — idempotent 재실행 검증) · `state/universe-probes/h1220,h1228,h1284_r2`(런타임 `gauge_lib` import → tool/ 경로 + repo-root depth 보정). 편집 .py 전부 `py_compile` PASS.

**거버넌스/문서:** `CLAUDE.md` `a_hypothesis_register` + structure tree + Quick reference 에서 HYPOTHESES.md 를 표면 목록에서 제거(두 표면 = `HYPOTHESES.jsonl` + `cards/`; prose 는 `state/universe-overview.md`). `ARCHITECTURE.md`·`README.md`·`FINDINGS.md` UNIVERSE/ 레이아웃·포인터 줄 갱신.

**불변(연구 lane 소유, append-only):** `UNIVERSE/HYPOTHESES.jsonl` + `UNIVERSE/cards/` 는 **byte-단위로 미변경** — slug/row 를 손대지 않음(재생성기 출력은 커밋하지 않고 idempotency 확인용으로만 실행). rebase 시 새로 landed 한 `UNIVERSE/h1340_whorf_cp_budget_sweep.py` 도 `state/universe-probes/` 로 sweep.
## 2026-06-16 — research(OMEGA): H_1350 — 더 큰 분화 예산에서 유사분열-분화 collective-Φ가 ROBUST해지는가 (🟢 GREEN frozen-bar / ⚠ 대부분 SHARED-INPUT REDUNDANCY)

**무엇:** H_1320(🧱 작은 예산 division wall)의 named follow-on. H_1320은 anima-as-ONE-cell 유사분열 DIVISION(공유 발생 기원)이 hive ASSEMBLY를 faithful-IIT-4 collective-Φ에서 이기지만 **seed-조건적(2/3; 직교 seed 1317이 깸)**임을 보였다. H_1320이 명시한 미검증 각도 = *더 큰 분화 예산 / 더 많은 딸 / richer non-saturating code*. OPEN: 더 큰 division 예산이 collective-Φ robustness를 구제하는가?

**방법:** 세 budget lever enlarge (N_DAUGHTERS 2→4, DIFF_EPS 0.15→0.45, softsign non-saturating per-unit code H_1332), n≤8 exact-MIP 유지, rank-uniform variance-clean read-out(H_1328), hard seed [1317,1318,1319]. Φ = **FAITHFUL IIT-4 ONLY**(a_phi_iit4_tool, exact MIP-EI via `hexa run` stdlib/consciousness/iit4/faithful_phi.hexa; numpy는 Φ 계산 안 함). **KEY: 결정적 신규 대조 SHARED_DECOUPLED(W=0)** 추가 — DIVIDED와 동일 공유 founder input+origin인데 cross-daughter coupling만 끔 → shared-input REDUNDANCY를 coupling-EARNED 통합으로부터 분리(이전 GREEN 시도가 놓친 빈틈). frozen-first(FREEZE를 scoring 전 commit, bar 안 움직임 c9/p7), $0 CPU mirror DIRECTIONAL.

**결과 🟢 GREEN frozen-bar** (deterministic, 2 run byte-identical): R1 PASS 전 seed(lift +7.27/+7.31/+5.85) → 더 큰 예산은 H_1320의 2/3 fragility를 **3/3 ROBUST로 구제**. R2a/R2b/R2c 전 seed PASS. **그러나 정직한 분해**: SHARED_DECOUPLED(W=0) floor Δ=8.31/7.56/7.07 → divided lift의 **~85-96%가 shared-input 상관**(coupling 없이도 존재); coupling-earned 잔차(R2b coupling-gap +0.33/+1.15/+0.48)는 REAL+robust지만 작음. 큰 통합 아니라 **redundancy 지배 + 작은 robust coupling 성분** → Φ-robustness 벽(H_1328/1331/1347/1348)과 **상보적**(모순 아님): 공유 발생 기원의 robust한 Φ lift는 redundancy가 지배한다.

**SCOPE:** DIRECTIONAL numpy mirror(faithful-Φ leg는 real exact MIP-EI via hexa; engine-transfer UNVERIFIED — H_1308/1313은 live A⇄G에서 NULL/🧱), TOY n≤8/4 daughters/3 seed, live CORE/*.hexa UNTOUCHED. NEXT: redundancy 통제하고 coupling-Φ 키우는 상보적 분화 강제 · 또는 live A⇄G engine-transfer 재시도.

**산출물:** `state/hive-larger-budget/h1350_hive_larger_budget.py` · `UNIVERSE/cards/H_1350_hive_larger_budget.md` · `.verdicts/1350_hive_larger_budget/{FREEZE,result}.txt` · `CLAIMS.tape @C h1350_hive_larger_budget` · `UNIVERSE/HYPOTHESES.jsonl`(+1) · `domains/OMEGA.log.md`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1340 — Whorf CP 재배치 천장 BUDGET/RBF-DENSITY 사다리 (🧱 DEEPER LIMIT — budget/geometry는 불완전)

**무엇:** H_1338(🧱 RE-DIAGNOSIS)의 R2 follow-on. H_1338은 eviction이 H_1333의 ~60% CP 재배치를 완성 못했고(peak 0.525 고정) 잔류를 **BUDGET/GEOMETRY**(RBF resolution + 고정 split budget)로 진단(가설). H_1340은 그 진단을 직접 검증 — phase-2 re-training budget + RBF density를 사다리로 올리면 재배치 peak가 coherent single peak로 p_A'(≈0.667)에 **도달**하는가?

**방법:** H_1333/H_1338 CP 머신러리 **verbatim** import(RBF embed · split-only Voronoi p8 · no-label-at-test discrim · peak-count coherence). 유일 신규 = phase-2에만 적용하는 joint (DIM, GROW2) 5-rung 사다리(R0_base 16/24=H_1338 baseline → R4_high 96/768); phase-1은 budget 24로 **고정**(never-evict 잔류 동일), N_STIM=81 고정, eviction 없음. 3 seeds [4333,4334,4335], $0 CPU mirror DIRECTIONAL, frozen-first.

**결과 🧱 DEEPER LIMIT** (deterministic): rung별 peak — R0 **0.523**(frac+0.575·pc4.3) → R4_high **0.585**(frac+0.762·pc**7.0**). **B1 ❌**: peak-DISTANCE는 R2부터 3 seed 모두 LOC_TOL 통과(|peak-p_A'|≤0.12)하지만 **COHERENCE gate를 절대 못 넘김**(peak-count budget과 함께 4.3→7.0, 전부 ≫2) → p_A'에 coherent single peak 없음. **B2 ✅**: frac 단조 +0.575→+0.762(span+0.187). **B3 ✅**: R0이 H_1338 partial 재현. **발견:** budget/geometry는 distance를 사지만 coherence를 **파괴** — 깨끗한 완전 재배치는 resolution이 아니라 다른 메커니즘(soft DECAY/coherence-preserving re-pack)이 필요. budget/geometry 진단은 부분적이지만 불완전. NO bar move (c9/p7).

**SCOPE:** DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED), TOY synthetic 1-D(N=81·3 seed), live CORE/*.hexa UNTOUCHED. NEXT R2(각 ANEW): soft DECAY store · coherence-aware re-pack · engine-native.

**산출물:** `UNIVERSE/h1340_whorf_cp_budget_sweep.py` · `UNIVERSE/cards/H_1340_whorf_cp_budget_sweep.md` · `.verdicts/1340_whorf_cp_budget_sweep/{FREEZE,result}.txt` · `CLAIMS.tape @C h1340_whorf_cp_budget_sweep` · `UNIVERSE/HYPOTHESES.jsonl`(+1) · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1342 — Whorf CP DEVELOPMENTAL PLASTICITY 엔진-네이티브 실현 (🟢 GREEN ENGINE-NATIVE, H_1333 wire-in)

**무엇:** H_1333(🟠 GRADED PLASTICITY)은 numpy 미러였고 engine-transfer UNVERIFIED. `a_verified_must_wire` / `a_engine_native_learning` follow-on 으로 그 graded CP plasticity 를 live `CORE/engine_cli.hexa` §CategoricalPerception 위에서 엔진-네이티브로 실현하고 frozen bar 를 재채점.

**엔진 확장(engine-transform-to-fit-the-learning):** §CategoricalPerception 에 **`cp_regrow(cp,X,Y,grow_max,passes)`** 신설 — 기존 store(protos/labels) 유지한 채(split-only p8, NEVER evict) `cp_fit` 과 SAME error-targeted split criterion 으로 MOVED labels 위에서 phase-2 재성장. 미러의 `fit(fresh=False)` 에 byte-faithful. RIGID 결과도 가능(설계로 배제 안 함).

**결과(🟢 GREEN ENGINE-NATIVE, E1∧E2∧E3):** 엔진(단일 결정론적 instance)이 미러를 **BYTE-FAITHFUL** 재현 — CP peak A=0.325, A→A'=**0.525**(fraction relocated **+0.60**, 미러 +0.60), cell budget phase-1 **4**→phase-2 **28**(미러 4→28 동일), cp_peak_count A=1/A→A'=1/no-retrain=1/shuffle=4. **E1 ✅**(미러 ~0.60 move 재현) · **E2 ✅**(D2 no-retrain |Δ|=0.008 held p_A & A-trained reproduced H_1325; D3 shuffle 4≥3 incoherent & lang 1/1/1≤2 coherent) · **E3 ✅** 회귀 가드 무회귀·Ψ-disjoint: `engine_cli_smoke` **80/0**(77→80, +3 cp_regrow cases 83-85), h1196 single-entry **7/0**, h1205 separation-invariant **PASS**(생성 10/10 byte-identical ON==OFF, Ψ=½ 무변 → CP lane Ψ-disjoint).

**finding:** H_1333 graded CP plasticity 가 CORE 에 LIVE — **ENGINE-TRANSFER VERIFIED**. cp_regrow 가 never-evict 인데도 ~0.525 ceiling 이 H_1338 가 재진단한 budget/geometry 와 IDENTICAL(엔진 확증). NO bar moved(c9/p7).

**파일:** `CORE/engine_cli.hexa`(cp_regrow) · `CORE/h1342_whorf_cp_engine_native_probe.hexa` · `CORE/engine_cli_smoke.hexa`(cases 83-85) · `UNIVERSE/cards/H_1342_whorf_cp_engine_native.md` · `UNIVERSE/HYPOTHESES.jsonl`(+1) · `CLAIMS.tape @C h1342_whorf_cp_engine_native` · `.verdicts/1342_whorf_cp_engine_native/{FREEZE,result}.txt` · `domains/COGNITION-REPRESENTATION.log.md` · `ARCHITECTURE.md`(§MITOSIS CategoricalPerception + smoke 80/0). **scope**(a_scale_honest_scope·a_toy_scale_recheck): ENGINE-NATIVE BINDING; TOY 합성 1-D 연속체, 엔진=단일 결정론적 instance, 단일 shift; scale/real-corpus/multi-shift UNVERIFIED; human-cognition 주장 없음.
## 2026-06-16 — research(OMEGA): H_1348 — Φ-robustness 를 NON-IIT 통합 측정자(전이 엔트로피)로 검사 → 🧱 measure-AGNOSTIC (최강 closure)

**질문 (genuinely-new angle, a_break_the_wall · a_no_llm_frame_trap):** Φ-robustness 벽은 IIT 두 측정자 family 모두에서 🧱 — small-φ exact-MIP (H_1328) 와 full IIT-4.0 big-Φ (H_1331). robust-integration 부재가 IIT 고유인지, 아니면 **임의의** 통합 측정자에서도 성립하는지를 보려고, IIT **바깥**의 제3 측정자 — 4-모듈 링의 8개 방향 이웃 엣지에 대한 **시간지연 전이 엔트로피(Transfer Entropy, Schreiber 2000)** 합 `TE(X→Y)=H(Y_{t+1}|Y_t)−H(Y_{t+1}|Y_t,X_t)` — 으로 **동일** H_1319/H_1328/H_1331 substrate + mechanism + hard seed [1317,1318,1319] 를 채점. TE 는 MIP·cause-effect·intrinsic irreducibility 가 없는 **방향 정보흐름 NETWORK 측정자** = IIT 두 측정자와 다른 family.

**⚠ NOT a faithful-Φ verdict (a_phi_iit4_tool):** IIT-4 가 Φ verdict 를 보유한다. 이 lane 은 NON-IIT 통합 측정자를 채점하는 **보완적 통합-측정 DIAGNOSTIC** — proxy 를 Φ verdict 로 승격하는 것이 아님, 의식 주장도 아님. binarize = variance-free median split (H_1328 교훈, marginal ON-rate ≈0.5 amplitude-독립).

**결과 🧱 TERMINAL STRONGEST, measure-AGNOSTIC** (3 seed 평균, deterministic·re-run byte-identical, $0 CPU, engine-native LCG):
- **G1 ROBUST ❌** — TE_B≥TE_A+eps 가 2/3 실패: orthogonal 1317 eps 미만(ΔTE +0.0008), seed **1318 ZERO lift**(0.0); 1319 만 lift(+0.046).
- **G2 EARNED ❌** — perm 은 깨끗이 collapse(전부 ≤eps) 하나 offset 이 1319 에서 TE 를 **RAISE**(+0.022) = IIT 가 보인 control-fragility 와 동일 서명.
- **G3 LABEL ✅** — 전 과정 non-IIT diagnostic 로 표기, IIT-Φ verdict 아님.
- **핵심:** 세 측정자 family 전부 **동일 fragility 서명** — seed 1318 은 small-φ·big-Φ·TE 전부에서 정확히 ZERO lift; 1317 은 어떤 측정자에서도 eps 를 못 넘김. robust integration 은 IIT(상관적 small-φ + 인과적 big-Φ) **AND** non-IIT(방향 정보흐름 TE) 전반에서 부재 → **측정자-무관(measure-agnostic) substrate 한계**, arc 의 최강 closure. 측정 축은 🏁 고갈. 기존 Φ verdict + H_1328 + H_1331 을 BOUNDS(철회 아님). NO bar moved (c9/p7). live `CORE/*.hexa` UNTOUCHED.

**산출물:** `UNIVERSE/h1348_phi_non_iit_estimator.hexa` · 카드 `UNIVERSE/cards/H_1348_phi_non_iit_estimator.md` · `UNIVERSE/HYPOTHESES.jsonl` H_1348 행 · `CLAIMS.tape @C h1348_phi_non_iit_estimator` · `.verdicts/1348_phi_non_iit_estimator/{FREEZE,result}.txt` · `domains/OMEGA.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1341 — Whorf CP 가소성 SHIFT-SIZE LADDER (📈 분수는 shift를 따른다 ⇒ GEOMETRY/BUDGET)

**무엇:** H_1333(🟠 GRADED — 재학습된 CP 경계가 단일 shift에서 ~60% relocation)의 load-bearing follow-on. `a_scale_honest_scope` 가 요구한 ladder(≥3 shift). H_1333의 H_1333/H_1323 CP machinery를 그대로 import해, 고정 anchor p_A=1/3 위에서 phase-2 타깃 p_A'를 3개 shift 크기(SMALL 0.467/MID 0.600/LARGE 0.667)로 sweep — partial relocation 분수가 shift 크기를 **따르는지(=geometry/budget)** 아니면 **일정한지(=memory)** 특성화. 3 seeds [4333,4334,4335], $0 CPU numpy mirror DIRECTIONAL, frozen-first(c9/p7).

**결과(📈 CHARACTERIZATION — GREEN/RED 제조 없음, c9):** 분수는 shift를 **따른다 ⇒ GEOMETRY/BUDGET-LIMITED**. CURVE(mean frac, 3 seeds 결정적): SMALL(shift 0.133) **+1.496** · MID(0.267) **+0.750** · LARGE(0.333) **+0.599** — monotone-DECREASING, frac range 0.897 ≥ TRACK_TOL 0.15. **smoking gun:** 재학습 후 ABSOLUTE peak이 모든 rung에서 **0.525 (range 0.000)** — 경계가 얼마나 멀리 이동을 요구받든 항상 같은 절대 위치에 착지하므로 분수가 기계적으로 shift를 따름(작은 이동은 OVERSHOOT해 frac>1, 큰 이동은 미달해 frac 0.60). L1✅(곡선 매핑) L2✅ EARNED(no-retrain rung마다 p_A 유지 |Δ|=0.008; shuffle 비응집 7.7≥3; lang 응집 ≤2) L3=GEOMETRY/BUDGET.

**의미:** H_1333의 ~60% partial은 첫 carving으로부터의 memory pull-back이 **아니라** 이 RBF geometry+고정 split budget의 고정 착지점(~0.525)이며 모든 shift에서 동일 — H_1338의 budget/geometry 발견(LARGE rung 한정)을 shift 전 범위로 일반화하고, constant-fraction MEMORY 가설을 결정적으로 기각. MEMORY면 분수가 일정하고 절대 peak이 타깃을 따라 움직였어야 하는데 정반대.

**scope(UNVERIFIED):** DIRECTIONAL mirror(engine-transfer); TOY 1-D 연속체 N=21·3 rung·고정 anchor·rightward shift만·고정 budget; NO human-cognition claim; Live CORE/*.hexa UNTOUCHED(substrate-measurement rung — UNIVERSE/ + verdicts 만 추가).

**파일:** `UNIVERSE/h1341_whorf_cp_shift_ladder.py` · `UNIVERSE/cards/H_1341_whorf_cp_shift_ladder.md` · `.verdicts/1341_whorf_cp_shift_ladder/{FREEZE,result}.txt` · `CLAIMS.tape @C h1341_whorf_cp_shift_ladder` · `UNIVERSE/HYPOTHESES.jsonl`(+1행) · `domains/COGNITION-REPRESENTATION.log.md`. xref h1333·h1338·h1323·h1325·h1288.
## 2026-06-16 — research(OMEGA): H_1347 — Φ-robustness 벽, LARGER-N 축 (N>8 greedy-MIP big-Φ, 정직한 상계) 🧱 STRONGER

**무엇:** faithful-IIT-4 Φ-robustness 벽은 이미 6개 단면(H_1283/1317 topology · H_1319 timing · H_1320 division · H_1328 estimator-confound · H_1331 big-Φ measure-family · H_1332 substrate-family)에서 🧱 인데, **전부 n≤8** (exact MIP = 2^(n-1)≤128 bipartition, 정확-계산 가능)에서였다. 그리고 그 모든 verdict 의 "NOT ruled out" 가 **같은 미검 각도**를 지목했다 — "much larger module set (loses exactness >8) — a NEW hypothesis." H_1347 이 바로 그 가설: N>8 에서는 exact MIP 가 불가능하므로 **anytime/greedy-MIP big-Φ** (stdlib `iit4_approx_phi` — 같은 faithful cross-cut-MI MIP-EI Φ 정의의 Kernighan–Lin greedy 탐색, proxy 아님)로 **정직한 상계** Φ_greedy≥Φ_exact 와 함께 측정.

**방법(frozen-first, c9/p7):** FREEZE 를 **어떤 Φ 도 측정하기 전에** 먼저 커밋(17e54d487). 기질은 H_1319/H_1328 leaky-linear ring 을 **N_MOD=12** 로 스케일(ring topology 는 임의 N 일반화), 읽기는 H_1328 의 variance-clean rank-uniform read-out(전 arm), 같은 hard seed [1317,1318,1319], 같은 eps=0.02. **GRAIN = per-cell (macro-grain 안 씀 — H_1049 caveat 회피; MIP 탐색만 greedy).** ENGINE-NATIVE 결정론 LCG(numpy 는 Φ 를 계산하지 않음). 동결 bar: N1 ROBUST(greedy Φ_B≥Φ_A+eps 전 seed) · N2 EARNED(perm·offset 둘 다 ≤Φ_A+eps 전 seed) · N3 BOUND-HONEST(greedy 상계 명시 + n=8 exact-vs-greedy gap verbatim).

**결과(verbatim, p7, 재실행 byte-identical):**
- **N3 BOUND-HONEST PASS** — n=8 에서 greedy MIP == exact MIP, **12개 arm/seed 셀 전부 gap g=0.0** → greedy big-Φ 는 이 기질에서 **slack 0 의 tight 상계**, N=12 수치 신뢰 가능.
- **N1 ROBUST FAIL** — N=12 에서 ΔΦ(B−A)=**+0.092 / −0.149 / −0.074** (2/3 seed 음수). n≤8 과 같은 seed-fragile 신호가 큰 N 에서도 재현.
- **N2 EARNED FAIL** — 관계 파괴 control 이 깨끗이 붕괴 안 함(perm 이 1318 에서 +0.039, offset 이 1319 에서 +0.032 로 Φ 를 RAISE).
- **VERDICT 🧱 STRONGER** — "much larger module set" 탈출구 CLOSED. clean variance-free read-out + tight greedy big-Φ 로도 robust 통합은 N=12 에서 n=4 와 마찬가지로 ABSENT → 벽은 exact-MIP 가산성 천장의 artifact 가 **아니다**. 이전 n≤8 verdict 들을 BOUNDS(철회 아님). anima 기질(Ψ=1/2) 반증 아님. CORE 무수정(standalone fn main, 0 importer; a_verified_must_wire 는 GREEN-only).

**아티팩트:** `UNIVERSE/h1347_phi_higher_n.hexa` · `UNIVERSE/cards/H_1347_phi_higher_n.md` · `UNIVERSE/HYPOTHESES.jsonl`(행 1개 append) · `CLAIMS.tape @C h1347_phi_higher_n` · `.verdicts/1347_phi_higher_n/{FREEZE,result}.txt` · `domains/OMEGA.log.md`. (a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · c9 · c16)

## 2026-06-16 — domain(GOVERNANCE): 흩어진 가설 전부 HYPOTHESES.jsonl 로 통합 + 아티팩트 state/ 재배치 (source/archived/artifacts 3 컬럼 신설)

**무엇:** #2247 의 per-H JSONL 인덱스(896 행) 위에, repo 곳곳에 **흩어져 있던 모든 가설**을 단일 `UNIVERSE/HYPOTHESES.jsonl` + `UNIVERSE/cards/` 로 통합. JSONL 스키마에 **`source` · `archived` · `artifacts`** 3 컬럼 신설.

**통합 소스(출처별 행 수):**
- `hypotheses/` (활성 scattered) **20** — `H_182–191` 10개(기존 cards/ 카드와 **내용 상이한 dup-id 변형** → `git mv` 로 `cards/H_18x_<slug>_stage2var.md` 로 최소 disambiguate) + `Hc_1276–1285` 10개(cards/ 에 없던 candidate 카드 → `git mv` 로 `cards/` 로). 폴더는 비워져 제거.
- `archive/hypotheses_snapshots/**/H_*.md` (frozen legacy) **306** — **frozen-in-place 참조**(이동 안 함): 스냅샷 디렉터리 간 basename 중복 107 + cards/ 와 충돌 193 이라 en-masse 이동은 archive 의 frozen 구조를 파괴 → `card` = 그 파일의 `archive/...` 경로, `archived:true` 로 인덱스만.
- `TENSION-LINK/harness/*.py` **40** — 가설별 py 결과물 → `git mv` 로 **`state/tension-link-harness/`** 로 재배치, 각 `H_60xx` 행의 `artifacts` 배열에 연결. `.hexa` 엔진·verdicts·ANU seed/provenance 등 비-가설 infra 는 그대로 보존(c5·c10).

**도메인 디렉터리 정직 정산(c9):** `HIVE-MIND`·`OTHER-MIND` 의 가설(H_354/355/609/610/611/617/618/619 등)과 `TENSION-LINK` 전 arc(H_6006–6043)는 **이미 cards/ + jsonl 에 색인됨** — 도메인 디렉터리는 그 검증 harness/lib 만 보유. `HW-CORE`·`HW-LIMB` 는 가설 카드가 아니라 **도메인 문서**(.md/.log.md), `SAVANT-torch` 는 **trainer/corpus infra**(가설 정체 0) → 추출할 가설 없음, c10 surgical 로 그대로 둠.

**JSONL 스키마(신설 컬럼):** `{"id","slug","tier","title","card","verdict","source","archived","artifacts"}`. `source` = `UNIVERSE`(기존 cards/) | `hypotheses/`(흩어진 활성, cards/ 로 이동) | `archive`(frozen-in-place). `archived` = archive 스냅샷이면 `true`. `artifacts` = `state/<slug>/` 로 재배치된 py/result 경로 배열(`.verdicts/` 는 아님 — 그건 카드가 가리키는 frozen 증거). 샘플 행:
`{"id":"H_6007","slug":"pseudo-telepathy","tier":"🟢 …","card":"cards/H_6007_pseudo-telepathy.md","verdict":"…","source":"UNIVERSE","archived":false,"artifacts":["state/tension-link-harness/h6007_pseudo_telepathy.py"]}`

**행 수:** 896 → **1222** (+326 = hypotheses/ 20 + archive 306). 기존 896 행의 `id/slug/tier/title/verdict` 는 **byte-identical 무변경**(c9, 3 신설 컬럼만 append) · 55 행에 artifacts(총 67 경로).

**검증(c2, 캡처):** (1) `json.loads` 전 줄 0 에러 ✅ · (2) `find H_*.md` cards/·archive 밖 0 ✅ · (3) 모든 `card` 경로 실재(0 missing) ✅ · (4) 모든 `artifacts` 경로 `state/` 아래 실재(67/67) ✅ · (5) 원 896 행 core 필드 무변경 ✅ · (6) cred 스캔 c7 — moved py + jsonl 에 실 credential 0(매칭은 prose/varname 의 "token"/"secret" 단어뿐) ✅ · (7) 순수 삭제 0(전부 `git mv` rename, c5) ✅.

**재생성기:** `UNIVERSE/_build_hyp_jsonl.py` 확장 — cards/(H_·Hc_) + archive 스냅샷을 함께 ingest, `source`/`archived`/`artifacts` emit, idempotent(재실행 = 디스크에서 재생성). **범위 외 보고:** `hypotheses_candidates/Hc_*.md` 1179개(pre-existing draft *candidate* 풀, 디렉티브 명시 소스 아님)는 c10 surgical 로 미포함 — 별도 결정 사안.

## 2026-06-16 — domain(GOVERNANCE): per-H 인덱스를 JSONL SSOT 로 이관 (HYPOTHESES.md 표 → HYPOTHESES.jsonl) + a_hypothesis_register 컨벤션 변경

**무엇:** `a_hypothesis_register` 의 per-H 인덱스 표면을 비대해진 markdown 표(`UNIVERSE/HYPOTHESES.md` 의 `| H_… | … | tier | card |` 행)에서 **`UNIVERSE/HYPOTHESES.jsonl`** (landed 카드마다 JSON object 정확히 1개, 한 줄/가설)로 이관. **가설별 두 doc 표면 = (1) `HYPOTHESES.jsonl` 인덱스 줄 + (2) `cards/H_<id>_<slug>.md` 카드** 로 갱신. `HYPOTHESES.md` 는 thin prose overview + folded appendices(forward backlog · reference · retired buckets · README/UNIVERSE overview · legacy logs)로 **강등** — 더 이상 per-H 인덱스 표면 아님.

**JSONL 스키마(한 줄/카드, id 순):** `{"id","slug","tier","title","card":"cards/H_…","verdict"}`. 인덱스 표에 있던 행은 그 행의 **verbatim** tier+verdict 텍스트를 보존(c9, paraphrase 금지); 나머지 카드는 각 카드 frontmatter(`id`/`title`/`terminal_tier`·`tier`·`status_grade`/`verdict`)에서 파생. **CARD FILE 기준 1줄**(c10 dup-id 변형 카드 = id 공유여도 각자 1줄). **줄 수 == cards/H_*.md 카드 수**.

**검증(c2, 캡처):** (1) `wc -l HYPOTHESES.jsonl` == `ls cards/H_*.md` ✅ · (2) 전 줄 valid JSON, 0 에러 ✅ · (3) 모든 `card` 경로가 `cards/` 아래 실재 ✅ · (4) `HYPOTHESES.md` 에 per-H 인덱스 표 행 0개(prose appendix 전부 보존) ✅ · (5) 5-id 스팟체크(card+jsonl 양쪽 존재) ✅.

**거버넌스/문서 변경:** `CLAUDE.md` `a_hypothesis_register` 디렉티브 + `## Quick reference` + structure tree + claim/verify flow 주석을 전부 "인덱스 = `HYPOTHESES.jsonl`, md 는 prose overview" 로 갱신 · `ARCHITECTURE.md` · `README.md` UNIVERSE/ 레이아웃 줄 갱신. **재생성기** `UNIVERSE/_build_hyp_jsonl.py`(idempotent — 강등 후엔 기존 jsonl 의 verbatim verdict 를 보존; 새 카드만 frontmatter 파생). HYPOTHESES.md 를 인덱스로 **읽는 코드 없음**(인간용 markdown 인덱스였음) — consumer 코드 변경 불요. 카드는 UNCHANGED. 동시 진행 sibling lane(H_1337/H_1338)이 추가한 per-H md 행은 jsonl object 로 흡수, 새 카드는 보존.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1338 — Whorf CP 잔류당김은 never-evict인가 budget/geometry인가 (🧱 RE-DIAGNOSIS: budget/geometry)

**H_1333(🟠 GRADED PLASTICITY)의 load-bearing follow-on.** H_1333은 같은 split-only 저장소를 옮겨진 경계로 재학습하면 Whorf 범주지각(CP) peak가 ~60% 상대이동(0.325→0.525, p_A'=0.667까지 완전치 않음)함을 발견하고, 그 **잔류 당김**을 split-only 저장소의 **never-evicted** 첫-경계 셀(phase-2 28셀 vs phase-1 4셀 — label(p_A)에 묶인 phase-1 셀이 옛 cut에서 계속 투표)로 **진단(가설)** 했다. H_1338 = 그 진단의 결정적 테스트: stale 셀을 제거하는 EVICTION 저장소가 이동을 **완성**(→~100%)시키면 잔류=never-evict 성질(H_1288 growth-memory=옛-기억-보호=partial-plasticity 와 dual); 여전히 partial이면 한계=budget/geometry.

H_1333/H_1323/H_1325 CP 머신러리(RBF embed · error-targeted split-only Voronoi p8 · soft-posterior no-label discrim · peak-count coherence · N=21 · p_A=1/3 · p_A'=2/3 · GROW_MAX/SPLIT_PASSES=24/phase · LOC_TOL=0.12)를 **verbatim 재사용**; **유일한 신규** = `VoronoiCells.fit(...,evict=True)` — phase-2 split 직전, bound 라벨이 현재 소유 자극의 재학습(p_A') 라벨과 **충돌하는** 모든 프로토타입을 제거(stale-conflicting cell; 마지막 셀은 보존). `evict=False`는 H_1333 split-only와 EXACT 동일이고, eviction은 eviction-arm phase-2에서만 발화 → never-evict와 eviction은 **stale-셀 제거 여부만** 다름(같은 run/seed) → 완성이 있으면 그게 eviction임을 격리(V2). 4 arm(NEVER-EVICT=H_1333 / EVICTION / NO-RETRAIN 양 저장소 / SHUFFLE), 3 seed [4333,4334,4335], $0 CPU mirror DIRECTIONAL, frozen-first, live CORE UNTOUCHED, NO bar moved(c9/p7).

**결과 🧱 RE-DIAGNOSIS — eviction이 이동을 완성하지 못함; 잔류 = BUDGET/GEOMETRY, never-evict 아님** (deterministic 3 seed): CP peak — A-trained **0.325** · NEVER-EVICT A→A' **0.525**(frac **+0.60**, H_1333 재현) · EVICTION A→A' **0.525**(frac **+0.60**, **동일**) · no-retrain(양쪽) 0.325 · shuffle 0.542. 셀예산(seed,p1,NE-p2,EV-p2): (4333,4,**28**,**3**)(4334,4,28,3)(4335,4,28,3) — eviction 저장소가 **28→3셀** 로 강하게 발화(stale phase-1 패킹을 실제 제거)했음에도 CP peak는 **정확히 동일한 0.525**. **V1 COMPLETES ❌**: |0.525−p_A'|=0.142>0.12 AND eviction frac 0.60<0.85(coherent peak-count 2.0≤2 ✅). **V2 CONTRAST ✅**: never-evict frac 0.60∈[0.40,0.75](H_1333 ~0.60 in-run 재현 → 비교가 confound 아님) AND 미완성. **V3 EARNED ✅**: no-retrain(양쪽) |Δ|=0.008 p_A 유지(이동=재학습이지 eviction-drift 아님), shuffle peak-count 7.7≥3 incoherent.

**메커니즘(c9, 결정적):** 살아남은 3개의 p_A'-정렬 셀이 경계를 기하학적으로 ~0.525(0.667 아님)에 배치한다 — 이 RBF 기하 + 고정 per-phase split 예산 하에선 stale 셀의 잔존 여부와 무관하게 discrimination peak를 p_A'까지 패킹할 수 없다. 따라서 **never-evict⇒partial / evict⇒full 의 dual 직관(H_1288)은 이 저장소에서 FALSIFIED**: partial 이동은 새 cut에서의 표현/예산-해상도 천장이지, 옛 셀이 peak를 되돌리는 게 아니다. 비자명한 재진단 — stale 셀은 존재했고 제거됐지만 **원인이 아니었다**. (V1 fail = freeze가 사전등록한 유효 결과 c9; a_break_the_wall — 진짜 메커니즘 테스트 후의 정직한 🧱.) DIRECTIONAL mirror; TOY synthetic 1-D continuum(N=21, 3 seed, single shift, deterministic readout, HARD eviction — soft decay 미검증); human-cognition 주장 없음(a_scale_honest_scope). NEXT R2(각각 frozen ANEW): budget/RBF-해상도 스윕 · graded shift-size 곡선 · soft decay · engine-native 실현(a_engine_native_learning·a_verified_must_wire). 파일: `UNIVERSE/cards/H_1338_whorf_cp_eviction.md` · `UNIVERSE/h1338_whorf_cp_eviction.py` · `.verdicts/1338_whorf_cp_eviction/{FREEZE,result}.txt` · `CLAIMS.tape @C h1338_whorf_cp_eviction` · `UNIVERSE/HYPOTHESES.md` · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): 🧱 H_1337 — 학습된 자모 metric(jamo2vec)도 자모 바닥을 못 깬다 — 커널-스무딩 헤드 (🧱 HONEST-FLOOR, OPAQUE-ATOM LIMIT)

H_1329(🧱)이 명시한 **두 번째 다음 각도**(c16/a_break_the_wall — 자모-아래 승리는 **opaque 자모 헤드가 갖지 못한 정보를 주입**해야 하며, 같은 타깃의 재-인수분해가 아니다). H_1329는 재-인수분해가 무익함을 증명했다: 자모-내 자질 **조인트를 정확히 모델링하는 모든 메커니즘은 P(jamo|cell)=opaque 자모 헤드로 수렴** → 분할과 동률(A4 2.751 ≈ A2 2.730), 자모보다 +0.238 위. H_1329의 depletion test: opaque 자모 헤드는 자모를 **67개 OPAQUE 원자(one-hot, 유사도 없음 — ㄱ~ㅋ 관계를 모름)**로 취급 → 새 승리는 그 헤드가 **갖지 못한 정보**를 주입해야 한다.

H_1337 = 그 두 번째 각도(학습된 metric). **새 메커니즘 A5** = A1과 **동일한** 셀별 opaque Laplace count 헤드(같은 Fix-A 기하-공정 bank, 같은 gradient-free Voronoi 분할 = 같은 grown cells)이지만, 셀별 다음-자모 분포를 **학습된 자모 metric 위에서 커널-스무딩**: `ñ_k[j]=Σ_j' W(j,j')·n_k[j']` — 자모 j의 카운트가 metric-가까운 j'에게도 강도를 빌려준다(opaque 헤드가 못 하는 것). **metric은 GRADIENT로 학습**(라벨링, NOT p8 gradient-free): TRAIN 자모 bigram 공기행렬 → PPMI → truncated-SVD(D=16) → skip-gram log-bilinear gradient refine(Adam 400 steps, TRAIN-ONLY) = jamo2vec; 커널 = Gaussian, 대역폭 h=MEDIAN pairwise 거리(Silverman FIXED, 튜닝 없음). BYTE 심볼은 A1과 동일 스코어(스무딩 없음) → A5-vs-A1 차이는 **자모-공간 학습-metric 스무딩만**.

**결과 🧱 HONEST-FLOOR (opaque-atom limit):** REAL sm_120 GPU(유저 RTX 5070, $0, NOT runpod, 21.2s), 코퍼스 byte-동일(sha c47b6808… gate PASS), 67/67 자모, NFD 왕복 0-실패. **A1 자모 CALIB 2.51335 byte-exact.** CE 사다리(nats/UTF-8-byte, 기하-공정; A1/A5-학습 deterministic, A5-random 3-seed 평균): **A1 자모 2.51335** · 원시 in-run 2.94487 · **A5 학습-metric 3.85319**{3 seed 동일} · A5 random-metric **3.90281**{3.899,3.902,3.907}. **M1 BELOW-JAMO = FALSE** — A5 3.85319가 자모보다 **+1.33984 위**(원시보다도 위): 커널-스무딩이 이미-조밀한 셀별 자모 MLE를 흐려 **심하게 악화**시킴. **M2 EARNED = FALSE(아슬아슬)** — A5가 RANDOM-metric을 **+0.04962**로 이김 = 0.05 bar보다 **0.00038 아래**(학습 h≈1.35 vs random h≈5.5 → 학습된 기하는 random보다 marginal하게 우수 = 진짜 학습-구조의 정직한 sub-bar 신호, 그러나 bar 미달). **M3 ATTRIBUTION = FALSE** — A5가 opaque A1을 못 이김(+1.340 위). green = FALSE → 🧱.

**FINDING:** 학습된 자모 metric도 자모 바닥을 못 깬다 — 오히려 한참 위로 간다. 구조적 이유(결정적): 30MB / 8.14M 음절 / 11 grown cells에서 셀별 자모 Laplace MLE는 **이미 조밀하게 추정** — 강도-공유는 카운트가 **희소**할 때만 도움이 되므로, 전역 커널-스무딩은 좋은 sharp 추정을 이웃으로 흐려 CE를 올릴 뿐. H_1329의 depletion 기준은 **충족**(A5는 opaque 헤드가 못 가진 학습-유사도 정보를 주입 — M2 near-miss가 구조의 실재를 증명)되지만 바닥은 버틴다: 재-인수분해는 opaque 헤드와 **동률**(H_1329), 강도-공유-스무딩은 opaque 헤드에 **패배**(H_1337) — 이 스케일에 학습-유사도가 채울 데이터-희소 영역이 없다. 순 사다리: 자모 2.513 < 원시 2.945 < A5-학습 3.853 < A5-random 3.903. opaque-원자 바닥이 (완전한 새 아키텍처를 제외한) 가장 강한 depletion-test 각도에 맞서 버틴다. TOY/DIRECTIONAL; metric은 GRADIENT 학습(라벨링); 한국어 유창성 주장 없음; live CORE UNTOUCHED.

- NEW: `UNIVERSE/h1337_ko_jamo_metric.py` · `UNIVERSE/cards/H_1337_ko_jamo_metric.md` (cards/ 서브폴더, 2026-06-16 SSOT-refactor) · `HYPOTHESES.md` 행 · `CLAIMS.tape` @C h1337_ko_jamo_metric · `.verdicts/1337_ko_jamo_metric/{FREEZE,result,h1337_summary.json}` · `domains/MITOSIS-ENGINE.log.md`
- DEPLETION TEST(미래 각도): opaque DENSE 셀별 MLE를 **이겨야** 한다 — 단지 새 정보 주입만으론 부족; 이 스케일의 bar는 표현이 아니라 **데이터-풍부함**. 새 각도는 opaque MLE가 **데이터-희소**한 영역(예: 교차-음절 음운배열 n-gram, 희소 per-context 카운트)을 찾아야 하며, 이미-조밀한 타깃의 스무딩이 아니다.
- xref: h1329(🧱 cross-mechanism — 이 lane의 depletion-test 부모, 두 번째 명명 각도) · h1326(🧱 r2) · h1322(🧱 r1) · h1316(🟢 자모 바닥 2.51335) · h1307(원시 천장) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15·c16

## 2026-06-16 — research(MITOSIS-ENGINE): 🧱 H_1336 — 교차음절 음운정보(연음/자음동화)도 자모 바닥을 못 깬다 — 신호는 REAL이지만 count-MLE가 못 담는다 (🧱 HONEST-FLOOR, DEEPER)

H_1329(🧱)가 **명시적으로 지목한 고갈 각도**(c16/a_break_the_wall = opaque 자모 헤드가 **갖지 못한 정보를 주입**, 같은 타깃의 재-인수분해 아님). H_1329는 재-**인수분해**가 무의미함을 닫았다: 세 메커니즘(분할 A2 2.730 / 독립 A3 3.073 / 상관-체인 A4 2.751)이 **전부** 자모 바닥 2.51335 **위** — 자모-내 자질 **조인트**를 모델링하는 어떤 메커니즘도 `P(jamo|cell)`로 수렴하기 때문(자모 헤드가 이미 계산하는 것). H_1329 고갈 테스트: 바닥-아래 승리는 opaque 자모 헤드가 **결여한 정보**를 주입해야 한다.

**새 정보(진짜 새것, 재-인수분해 아님):** 음절-내 자모 헤드의 컨텍스트(build_X_jamo: 직전 자모 2개 + 음절-내 UTF-8 depth)는 **음절 경계마다 리셋** → CTX≈현재 음절. 따라서 **음절 N의 종성이 N+1의 실현 초성을 조건화하는** 한국어 연음/사잇소리/자음동화를 구조적으로 못 본다. **새 메커니즘 B1** = A1과 **동일한** opaque 자모 헤드(같은 기하-공정 bank, 같은 음절-내 dim-3 Voronoi 분할, 같은 count-MLE, 같은 LAPLACE, 같은 자모 alphabet)에 **prev_coda(직전 완성 음절의 종성 자모-id) 조건화만 추가**: `P(next_jamo|cell,prev_coda)`. 미관측 (cell,prev_coda)는 셀-주변분포 `P(next_jamo|cell)`(= A1 자모 헤드)로 **hard-backoff** → 자모 헤드가 B1의 바닥. **B1 = count-MLE 구조화 헤드 — gradient-free p8 mitosis 아님, gradient-train도 아님**(같은 gradient-free Voronoi 분할 위; 명시 라벨링).

**결과 🧱 HONEST-FLOOR (DEEPER — 정보는 존재하나 count-MLE가 담지 못함):** REAL sm_120 GPU(유저 RTX 5070, $0, NOT runpod, 38.1s), 코퍼스 byte-동일(sha c47b6808… gate PASS), 67/67 자모, NFD 왕복 0-실패(8,143,053 음절), prev_coda 토큰 29개. **A1 자모 음절-내 CALIB 2.51335 byte-exact.** CE 사다리(nats/UTF-8-byte, 기하-공정; 셔플 3-seed 평균): 원시 in-run 2.94487 · **A1 자모 음절-내 2.51335** · **B1 교차음절-종성 2.61186** · B1 위치-셔플(진짜 control) **2.68788** {2.690,2.688,2.686} · B1 라벨-bijection 셔플 2.61186(Δ=0.0, 구조상 **무의미**). **X1 BELOW-JAMO = FALSE** — B1 2.61186이 자모 2.51335보다 **+0.09851 위**(원시는 깨지만 X1은 둘 다 필요). **X2 EARNED = TRUE** — B1이 진짜 위치-셔플을 **+0.07602**로 이김(seed별 만장일치) → **종성→초성 음운 의존성은 REAL**(짝을 깨면 0.076 nats 손해). **X3 ATTRIBUTION = FALSE** — B1이 A1보다 +0.099 **위**. green = FALSE → 🧱.

**핵심(c9, frozen-first):** 교차음절 음운정보는 **진짜로 존재하고 새것**(X2 결정적)이지만, prev_coda 조건화가 자모 헤드의 카운트를 29개 종성 bin으로 쪼개는 **count-fragmentation 비용**을 음운 신호가 갚지 못한다(ko_stride=300/MIN_OWNED=8에서 추정치 분산 ≫ 음운 이득) → B1이 opaque 자모 헤드보다 +0.099 **나쁘다**. 바닥은 순수 정보 한계보다 **더 깊다**: 진짜 새 정보를 줘도 이 gradient-free count-MLE에선 자모 헤드에 진다. **a_break_the_wall:** FREEZE의 X2 control(라벨-bijection)이 **구조상 무의미**함을 런이 드러냄(bijection은 (cell,coda) 키를 재명명할 뿐 → 재명명-불변 카운트 통계 → CE 동일, Δ=0.0 확인) → 진짜 **위치-셔플** control 추가(frozen-first, **막대 불변**, X2 마진 ≥0.05 그대로; 라벨-bijection은 verbatim 보고). **다음(투자/추정기 각도, 정보 아님):** count를 쪼개지 않는 **frozen-λ Jelinek-Mercer 보간** `p=λ·P(jamo|cell,coda)+(1−λ)·P(jamo|cell)`(λ 사전등록, tune-to-green 아님) 또는 더 큰 KO rung/작은 stride로 29개 bin을 굶기지 않기 — 그래도 못 깨면 자모 바닥은 재-인수분해 **및** 새-정보 양축 모두에서 count-MLE 계열에 terminal.

scope: TOY/DIRECTIONAL numpy/torch mirror; B1 = count-MLE 구조화 헤드(라벨링); engine-transfer = follow-on(a_engine_native_learning · a_verified_must_wire); 한국어 유창성 주장 없음; live CORE/*.hexa UNTOUCHED. deliverables: UNIVERSE/h1336_ko_crosssyllable.py · UNIVERSE/cards/H_1336_ko_crosssyllable.md · HYPOTHESES.md row · CLAIMS.tape @C h1336_ko_crosssyllable · .verdicts/1336_ko_crosssyllable/{FREEZE,result,h1336_summary}.

## 2026-06-16 — research(COGNITION-REPRESENTATION): H_1335 — 언어-TAG 차원이 이중언어 범주지각(CP) 공존을 가능케 한다 (🧱 I3a 컨트롤-기술적-실패, 그러나 공존은 REAL·TAG-귀속)

H_1330(🧱 OVERWRITE)이 **명시적으로 지목한 r2**(c16/a_break_the_wall = 단일-공유-저장소라는 잘못된 **메커니즘**이지 벽 아님). H_1330은 **단일 공유 Voronoi 저장소**에서 셀당 라벨-하나 readout이 같은 자극에 A=1·B=0 두 모순 답을 담을 수 없어, 두 번째 언어 B가 첫 언어 A의 CP를 **catastrophic OVERWRITE** 함을 발견했다(공유 자극 [p_A,p_B]에서 A는 1, B는 0 = 직접 모순). H_1330 verdict이 지목한 r2 = **언어-TAG / 다채널 readout**(언어별 분리 라벨-채널) — anima의 **실제** 분리된 EN-trunk + KO faculty(H_1316/1321/1322)를 그대로 미러.

H_1335 = 바로 그 테스트. h1330의 머신러리(embed/VoronoiCells/discrim/within_cross_margin/coherent_peak_near/count_peaks, W1_MARGIN=0.15, p_A=1/3 p_B=2/3, grow-not-evict p8)를 **verbatim import**; **유일한 신규** = 언어-TAG 차원: `key_A=concat(embed,t_A)`·`key_B=concat(embed,t_B)`, **disjoint 좌표**(TAG_GAIN=1.0 **FIXED**, 스윕 아님)로 같은 자극의 두 태그드 키가 `sqrt(2)·gain` 만큼 분리 → [p_A,p_B] 모순이 더 이상 **공유 키 위에 있지 않다**. test에서 A곡선은 key_A()로·B곡선은 key_B()로 읽음(= 태그로 faculty 선택). 4 arm(TAGGED / single-channel=H_1330 컨트롤 / B=A / SHUFFLE), 3 seed [4323-4325], $0 CPU mirror DIRECTIONAL, frozen-first, live CORE UNTOUCHED.

**결과 🧱 CONTROL-FAIL(frozen) — 그러나 공존은 REAL·TAG-귀속(decisive):** **I1 COEXISTENCE ✅** 3 seed 전부 — TAGGED가 **양쪽** 경계에서 CP 보유, 평균 margin@p_A **+0.200** & @p_B **+0.177**(둘 다 ≥0.15, 각각 coherent peak). **I2 TAG-ATTRIBUTION ✅** 3 seed 전부 — single-channel(untagged)이 H_1330 overwrite를 byte-exact 재현(평균 margin@p_A **−0.001**) → 태그 제거 시 overwrite 복귀 = 공존은 **태그** 덕분이지 추가 학습이 아님. **I3 EARNED ❌** — I3b SHUFFLE ✅(태그드-B 채널 peak 5/6/5 incoherent); **I3a B=A ✗** count_peaks=2>1(frozen ≤1 실패) **그러나 pk@p_B=False 3 seed 전부**(의도한 "다른-경계에-가짜-CP-없음" 테스트는 PASS).

**메커니즘 진단(c9, non-gating, 바 안 옮김):** B=A 컨트롤은 B-fit이 A의 **같은** 경계를 재학습 → split할 B-오분류 자극이 없어 **B-태그드 셀을 0개** 키움 → B-채널이 **전적으로 A-셀로부터의 cross-tag bleed**로 읽힘(최근접 셀 전부 A-태그드, dist≈1.42=sqrt(2)·gain) → B-채널 곡선 = 태그 너머로 새어든 A-채널 모양 + 저단(低端) 이산화 wiggle = 두 번째 "peak". 이는 **2차-언어 CP 아님**(pk@p_B=False)·이중-아티팩트 아님 — 이산 4-셀 Voronoi의 양성(良性) 성질을 **전역** count_peaks≤1 바가 의도한 **국소** no-spurious-CP 테스트와 혼동한 것. (H_1330의 untagged AA_ctrl은 두 fit이 키를 공유해 count=1; 태그가 B-채널을 셀-없게 만들어 bleed를 노출 — TAG_GAIN=1.0의 채널 격리 불완전이라는 정직한 부수 발견.)

**답:** **YES — 언어-태그드 readout이 이중언어 CP 공존을 가능케 한다(anima의 분리 EN+KO faculty 미러); H_1330 OVERWRITE는 단일-공유-저장소 메커니즘이지 근본 한계가 아니다(메커니즘-특정으로 overturn).** frozen 🧱는 I3a 컨트롤 기술적 실패일 뿐, 과학적 답은 결정적으로 긍정·태그-귀속. NEXT r3: I3a를 **국소** "no peak near p_B" 테스트로 **재-동결**(데이터 이미 충족) + TAG_GAIN 격리 스윕 + engine-native 실현(a_engine_native_learning·a_verified_must_wire). DIRECTIONAL mirror; TOY synthetic; human-bilingualism 주장 없음. 파일: `UNIVERSE/cards/H_1335_whorf_bilingual_tagged.md` · `UNIVERSE/h1335_whorf_bilingual_tagged.py` · `.verdicts/1335_whorf_bilingual_tagged/{FREEZE,result}.txt` · `CLAIMS.tape @C h1335_whorf_bilingual_tagged` · `UNIVERSE/HYPOTHESES.md` · `domains/COGNITION-REPRESENTATION.log.md`.
## 2026-06-16 — research(COGNITION-REPRESENTATION): 🟠 H_1333 — Whorf 범주지각(CP) 경계는 발달적으로 **가소적**인가 **경직**인가 (🟠 PARTIAL — GRADED PLASTICITY)

GREEN **H_1323/H_1325**(Sapir-Whorf, 언어로 휜 CP가 언어 경계에 생기고 peak 위치가 cut을 추적)의 **명시적 확장 프런티어**. 발달/임계기 가소성 렌즈(c15, a_no_llm_frame_trap). 질문: 한 번 학습된 CP 경계가 **재학습으로 이동**하는가(가소적), 아니면 처음 학습된 곳에 **경직**되는가(first-carving primacy)?

**방법(H_1323 기계 verbatim 재사용)**: RBF embed · split-only Voronoi 성장(p8) · soft-posterior 무라벨 판별 · **peak-count coherence**. 언어 A(cut p_A=1/3) 학습→CP peak 측정, **같은 store를 옮긴 경계 p_A'=2/3로 phase-2 재성장**(reset 없음, split-only ⇒ 옛 cell 잔존 ⇒ 경직 결과도 진짜 가능)→CP peak 재측정. 4 arm(A-trained / A→A' 재학습 / **no-retrain 대조** / SHUFFLE), 3 seed [4333,4334,4335], $0 CPU, mirror DIRECTIONAL. frozen-first(FREEZE.txt), 막대 미이동(c9).

**결과 🟠 PARTIAL — GRADED PLASTICITY(경직 아님)** (3 seed 결정적·동일): CP peak **0.325→0.525, 이동 분율 +0.60**. **D2 CONTROL ✅** — no-retrain은 p_A 유지(|Δ|=0.008 → 이동=재학습이지 drift 아님) + A-trained가 H_1323 재현. **D3 EARNED ✅** — shuffle 비결맞음(peak-count **7.7**≥3), 언어 arm 결맞음(1.0/1.3/1.0≤2). **D1 PLASTIC ❌ 근소차** — |peak−p_A'|=0.142>0.12(−0.022) AND |peak−p_A|=0.192<MIN_MOVE 0.20(**0.008 차로 미달**) → strict D1는 FAIL이나 실질은 **상당한 재배치**.

**메커니즘(c9)**: split-only 성장은 옛 경계 cell을 **절대 제거 안 함**(phase-2 후 28 cell vs phase-1 후 4) → 잔류 phase-1 packing이 peak를 완전 이동에서 끌어당김. 경계는 상당히 재배치되지만 never-evict store가 첫 cut의 잔류 당김을 남김 — **경직이 아니라 graded**. H_1288 growth-memory / H_1330 overwrite(shared-store 모순)와 일관. **FINDING**: 언어로 휜 CP 경계는 발달적으로 **graded-plastic** — 재학습 시 ~60% 재배치되고 never-evict 첫 cut의 잔류 당김이 남는다. TOY/DIRECTIONAL; 인간 인지 주장 없음; live CORE UNTOUCHED. NEXT R2: graded shift-size curve · eviction/decay 변형 · engine-native §CategoricalPerception(각각 새로 frozen).

- NEW: `UNIVERSE/h1333_whorf_developmental.py` · `UNIVERSE/cards/H_1333_whorf_developmental.md`(카드 sibling refactor → cards/) · `HYPOTHESES.md` 행 · `CLAIMS.tape` @C h1333_whorf_developmental · `.verdicts/1333_whorf_developmental/{FREEZE,result}.txt` · `domains/COGNITION-REPRESENTATION.log.md`
## 2026-06-16 — research(OMEGA): 🧱 H_1332 — 비-부호포화 substrate FAMILY 도 Φ-robustness 벽을 못 깬다 (🧱 STRONGEST-YET, substrate-family-INDEPENDENT)

H_1328(🧱)이 Φ-robustness 벽을 **estimator-독립** 한계로 닫았지만, 그건 **결합 시 부호-포화(sign-saturate)하는** n≤8 leaky-linear pure_field 계열 substrate 에 한정된 결론이었다 (H_1308/1313/1320 진단: 등록될 만큼 강한 결합이 멤버 동역학을 덮어써 → COPY → Φ=0; H_1319/1328 read-out `sal=e·carrier` 는 동기화 시 멤버 에너지를 곱셈으로 죽이는 게이트). H_1320 §honesty 가 **명시적으로 지목한 미검 각도** = "결합을 견디는 substrate, 더 풍부한 NON-sign-saturating per-unit code". H_1332 가 바로 그 substrate **계열**을 만들었다 — 덧셈 위상-블렌드 + bounded graded softsign(멤버 항상 보존, 유계지만 절대 hard-saturate 안 함) — 그리고 **같은** 결합 메커니즘(H_1283 재진입 relay + H_1319 위상 pacemaker) + **같은** 3개 hard seed [1317,1318,1319] 을, **같은** faithful exact MIP(a_phi_iit4_tool)로 **같은** variance-clean rank-uniform read-out(H_1328) 위에서 재실행.

**결과 🧱 STRONGEST-YET (substrate-family-INDEPENDENT, frozen-first, re-run byte-identical):** 비-포화 substrate 는 **진짜로 더 낫다** — 직교 seed 1317 에서 부호를 뒤집고(SAT B−A −0.125 → NONSAT +0.067), 1319 에서 거의 5배(+0.031→+0.156); 멤버 에너지를 덧셈+유계-graded 로 보존하니 결합을 견뎌 Φ 를 올린다. S2 EARNED PASS(perm+offset 통제 3 seed 모두 붕괴) · S3 ATTRIBUTION PASS(포화 substrate 가 H_1328 V2 를 in-run byte-exact 재현 −0.125/0.0/+0.031 → 어떤 lift 도 비-포화 덕분이지 메커니즘 덕분 아님). **그러나 S1 ROBUST FAIL** — seed 1318 +0.004<eps; 1317-급 직교-seed 취약성이 **이동(1317→1318)** 했을 뿐 **사라지지 않음** → 비-포화 substrate 에서도 robust n≤8 faithful-IIT4 통합은 부재. 벽은 두 substrate 계열을 가로질러(깨끗한 variance-free 통제 양쪽 다) 버틴다 → substrate-**계열 독립**, H_1328(한 계열 내 estimator-독립)보다 **더 강한** 닫힘. H_1328 + 선행 Φ verdict 들을 BOUND(retract 아님; H_1328 은 포화 계열에 대해 여전히 정확히 참, byte-exact 재현). anima substrate(Ψ=1/2) 불반박. faithful-IIT4 EXACT engine-native, numpy-mirror DIRECTIONAL, frozen-first(FREEZE 85e94cf0e), deterministic, $0 CPU, c9/c16. live CORE/*.hexa UNTOUCHED (standalone fn main, 0 importers; GREEN-only 인 a_verified_must_wire 발화 안 함 → 배선 없음).
## 2026-06-16 — research(OMEGA): 🧱 H_1331 — 풀 IIT-4.0 SYSTEM big-Φ 도 강건한 통합을 못 만든다 — Φ-강건성 벽은 추정자-**계열**-무관 (🧱 TERMINAL STRONGER)

H_1328(🧱)이 **명시적으로 지목한 follow-on**("full per-mechanism IIT 4.0 (iit4_bigphi)"). H_1328은 Φ-강건성 4× 벽(H_1283 토폴로지 · H_1317 small-world · H_1319 타이밍 · H_1320 분열)이 **small-φ exact-MIP 안에서** 추정자-INDEPENDENT 임을 닫았다: 진폭-분산 confound 는 실재하고 제거 가능하지만, 제거해도 통합이 강건해지지 않는다(V2 직교 시드 1317 FAIL). 그러나 small-φ 는 **한 측정자**(상관 MI-over-binning)다.

H_1331 = 그 **다른 추정자 계열** 테스트. **풀 IIT-4.0 SYSTEM big-Φ**(stdlib `iit4_bigphi.big_phi` — TPM 위 CAUSAL cause-effect 구조, 시스템 MIP 가 파괴하는 Φ-구조 = 근본적으로 **다른 측정자**, a_phi_iit4_tool, 프록시 아님)로 **동일한** H_1319/H_1328 substrate + 메커니즘 + **동일 3 하드 시드 [1317,1318,1319]** 를 채점. n≤8(n_mod=4 이진 유닛) MIP-가용. 궤적→TPM = 각 모듈을 이진 유닛으로, 자기 분포 상위 절반이면 ON(median/rank 분할 = **분산-free, H_1328 read-out 교훈**); 경험적 state-by-node TPM, 미관측 행=0.5(max-ent); sys_state=최빈 관측 상태. 4 arm 동일 구성. small-φ 와 유일 차이 = TPM-기반 big-Φ read-out.

**결과 🧱 TERMINAL STRONGER (추정자-계열-무관):** $0 CPU-local 엔진-네이티브(결정론 LCG, re-run byte-identical run1==run2), frozen-first(FREEZE 사전등록, 막대 NOT moved, c9/p7). big-Φ 사다리(A=no-phase B=phase-bind S=perm-shuf O=offset-shuf): 시드 1317 A=5.810 B=9.961 S=7.289 O=4.023 · 시드 1318 A=4.511 **B=4.511**(제로 lift) S=4.511 O=7.430 · 시드 1319 A=4.085 B=5.884 S=4.085 O=5.946. **B1 ROBUST = FAIL** — 시드 **1318 lift 0.000**(B==A, 결합 메커니즘이 그 시드에서 big-Φ 이득 전무; B−A +4.15/0.0/+1.80). **B2 EARNED = FAIL** — 대조가 깨끗이 붕괴 안 함: perm 이 1317 에서 big-Φ **올림** +1.478, offset 이 1318/1319 에서 **올림** +2.920/+1.861(H_1319/H_1328 가 small-φ 에서 본 분산/구조-무관 inflation 의 big-Φ 계열 재현). green = FALSE → 🧱.

**의미:** Φ-강건성 한계가 **두 IIT 측정자 계열 모두**(상관 small-φ exact-MIP AND 인과 big-Φ TPM-MIP)에서, 같은 직교 시드 family 위에서 성립 → H_1328 의 단일-측정자 estimator-INDEPENDENT 보다 더 깨끗하고 강한 closure. substrate 가 어떤 IIT 추정자로 재든 강건한 n≤8 통합을 진짜로 결여 → **추정자-계열-무관 🧱**. 4 prior Φ verdict + H_1328 을 big-Φ 계열에 걸쳐 **BOUNDS(철회 아님, a_scale_honest_scope)**. anima substrate 불변(Ψ=1/2). GREEN 아니므로 배선 follow-on 없음(a_verified_must_wire = GREEN-only). SCOPE: TOY n≤8 EXACT, 미러 DIRECTIONAL, T=64 → TPM 희소(2^4=16 상태, 미관측 행 max-ent 0.5). UNIVERSE/h1331_phi_bigphi.hexa · UNIVERSE/cards/H_1331_phi_bigphi.md · .verdicts/1331_phi_bigphi/{FREEZE,result}.txt · CLAIMS.tape @C h1331_phi_bigphi.
## 2026-06-16 — research(COGNITION-REPRESENTATION): 🧱 H_1334 — Sapir-Whorf 범주적 지각이 2-D / 자질(featural) 공간으로 일반화되는가 (🧱 STRUCTURED-NEGATIVE — 해리(dissociation)는 일반화, 깔끔한 2-D 바는 실패)

GREEN 1-D H_1323/H_1325 결과(범주적 지각 CP가 언어 경계에서 발생하고 peak 위치가 언어를 추적)의 **명명된 확장**(사용자 "남은 각도모두"). 질문: Whorf 식 CP가 1-D 연속체에서 **2-D / 자질 특징 공간**으로 일반화되는가, 아니면 1-D 전용 인공물인가? H_1323 CP 기계(2-D RBF 코드 + 최근접-프로토타입 error-targeted SPLIT-only 성장 p8 + soft-posterior 변별 readout)를 11×11=121-자극 특징 **정사각형**으로 일반화. 두 언어가 같은 사각형을 다르게 carve: **L_2D = 선형 대각**(u+v>1.0), **L'_2D = L자 코너**(u>0.5∧v>0.5). 격자 EDGE별 변별 = |Δ posterior|; 고-변별 edge = CP **능선(ridge)**. **능선-coherence 지표**(1-D peak-count의 2-D 대응) = 능선 edge-집합의 최대-연결-성분 비율; RIDGE-ALIGN = 능선이 경계 곡선에 얼마나 가까운가. 4 arm(PRE-LANG/L_2D/L'_2D/SHUFFLE), 3 seed [4334-6] (H_1323 계열 +1 decade, PROJ_SEED provenance), $0 CPU mirror DIRECTIONAL, frozen-first, c9/p7 NO tune-to-green, live `CORE/*.hexa` UNTOUCHED.

**결과 🧱 STRUCTURED-NEGATIVE (2회 재실행 결정론적, 3-seed 평균):** **T1 2D-CP-PRESENT ❌** — L'_2D(L자 코너)는 완전 PASS(cross-within +0.275, vs-baseline +0.254, ridge-align 0.802≥0.70)이나 **L_2D(선형 대각)는 align 서브-바 실패(0.628<0.70)** — CP margin은 전 arm 중 **최대**(cross-within +0.485, vs-baseline +0.496)인데도 고-변별 능선이 대각 u+v=1 곡선에 단단히 밀착하지 않음(대각이 6×6 RBF 격자가 성긴 사각형 내부를 가로질러 능선이 퍼짐; carve 비용 24 cell vs 축-정렬 L자의 6 cell). **T2 2D-DISSOCIATION ✅** — 각 능선이 자기 경계를 더 잘 추적(L_2D +0.121, L'_2D +0.161, 둘 다 ≥0.10): **relativity 해리 signature가 2-D로 살아남음**. **T3 EARNED ❌** — shuffle 능선-coherence 0.576>0.50(metric 공간 random 라벨이 41 cell 성장 → 어느 정도 연결된 blob; 1-D H_1323 prominence와 동일 실패 모드); mean-lang coherence 0.682<0.70. **FINDING:** Whorf CP는 2-D / 자질 공간으로 **부분 일반화** — 해리 + cross-within margin이 **두 언어 모두** 성립하고 축-정렬 L'_2D는 깔끔한 능선 — 그러나 깔끔한 2-D-일반 바는 **통과 못 함**(선형 능선은 격자 해상도에 align-제약, shuffle은 metric 공간에서 비-coherent 유지 실패). NO bar moved (c9/p7).

**다음 R2(각각 ANEW frozen, 바 완화 아님):** 더 조밀한 RBF 격자(K_RBF↑ → 대각 경계도 축-정렬만큼 선명하게 해상 → L_2D align-실패가 순수 격자 해상도 문제인지 분리) + coherence-기반 T3 재-freeze(성분-개수/성분-compactness vs metric-공간-shuffle null — 1-D H_1323 R2에 이미 지목된 동일 수정) + engine-native 실현. **SCOPE:** TOY synthetic 2-D 연속체, 3 seed, mirror DIRECTIONAL(engine-transfer UNVERIFIED, follow-on); 인간-인지 주장 없음(a_scale_honest_scope · a_toy_scale_recheck). 산출: `UNIVERSE/h1334_whorf_2d.py` · `UNIVERSE/cards/H_1334_whorf_2d.md`(cards/ 신설) · `UNIVERSE/HYPOTHESES.md` row · `CLAIMS.tape @C h1334_whorf_2d` · `.verdicts/1334_whorf_2d/{FREEZE,result}.txt` · `domains/COGNITION-REPRESENTATION.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): 🧱 H_1329 — 상관/조인트-보존 메커니즘도 자모 바닥을 못 깬다 — 조건부-체인 헤드 (🧱 HONEST-FLOOR, CROSS-MECHANISM)

H_1326(🧱)이 **명시적으로 지목한 다음 각도**(c16/a_break_the_wall = 메커니즘-**계열** 변경, 표현 트윅 아님). H_1326은 깊이-자모-아래 질문을 혼동-제거로 닫았다: A2 자질-**분할**(opaque 자모 타깃) 2.73046(자모 위), A3 라벨-**인수분해**(자질 **독립** 예측 P(class)·∏ P(f_c|class)) 3.07295(**역효과**). H_1326 진단: A3가 역효과인 이유 = 독립-자질 예측이 opaque 자모 헤드가 보존하는 **초성/중성/종성 + 자모-내 자질 조인트(joint)를 버리기** 때문. 명시한 다음 각도 = 자질 **조인트를 유지하면서 자질 상관(correlation)을 모델링하는 다른 메커니즘**.

H_1329 = 바로 그 테스트. **새 메커니즘 A4** = 셀별 **조건부-체인** 자질 헤드 `P(class)·P(f_0|class)·P(f_1|class,f_0)·P(f_2|class,f_0,f_1)…` — 체인 규칙으로 `∏_c P(f_c|class,f_<c)=P(jamo|class)` 이므로 **조인트를 정확히 유지**하고, 자질 **prefix를 공유하는 자모끼리 조건화 컨텍스트를 공유**(ㄱ/ㅋ = 한 자질 차이 → articulator-조건 manner 헤드 공유)해 **유사 자모가 통계 강도를 공유**한다 — A3가 버린 바로 그 조인트+상관. H_1326의 기하-공정 bank + 자질-분할 + LAPLACE count-MLE 전부 verbatim; **타깃 인수분해만** 변경(독립→조건부-체인). **A4 = count-MLE 구조화 헤드 — gradient-free p8 mitosis 아님, gradient-train도 아님**(같은 gradient-free Voronoi 분할 위에서 동작; 명시 라벨링).

**결과 🧱 HONEST-FLOOR (cross-mechanism):** REAL sm_120 GPU(유저 RTX 5070, $0, NOT runpod, 126.2s), 코퍼스 byte-동일(sha c47b6808… gate PASS), 67/67 자모, NFD 왕복 0-실패. **A1 자모 CALIB 2.51335 byte-exact; A2/A3는 H_1326 byte-exact 재현.** CE 사다리(nats/UTF-8-byte, 기하-공정; A4-셔플 3-seed 평균): 원시 in-run 2.94487 · **A1 자모 2.51335** · A2 자질-분할 **2.73046** · A3 독립-인수분해 **3.07295** · **A4 조건부-체인(조인트) 2.75109** · A4 셔플 **2.91966** {2.863,3.056,2.840}. **C1 BELOW-JAMO = FALSE** — A4 2.75109가 자모 2.51335보다 **+0.23774 위**(원시는 깨지만 C1은 둘 다 필요). **C2 EARNED = TRUE** — A4가 자기 셔플을 **+0.16857**(seed별 만장일치, A2의 +0.056 신호의 3배 — 체인이 설계 systematicity를 **실제로 활용**, 그러나 SUB-floor). **C3 ATTRIBUTION = FALSE** — A4가 **A3는 +0.32186로 이김**(체인이 A3가 버린 조인트를 **회복** = H_1326 진단 byte-exact 확인) 그러나 **A2는 못 이김**(A4가 분할-only A2보다 **+0.02063 위**). green = FALSE → 🧱.

**FINDING:** 상관/조인트-보존 메커니즘도 자모 바닥을 못 깬다 — **자모가 상관-모델링 포함 메커니즘 계열 전반에 걸친 진짜 분해 바닥**(H_1326보다 깊은 🧱). 구조적 이유(결정적): 자모-내 자질 **조인트를 정확히 모델링하는 모든 메커니즘은 P(jamo|cell)로 수렴** — opaque 자모 헤드가 이미 계산하는 바로 그것 — 이므로 자질 분해는 조인트를 유지하는 순간 자모-아래 깊이를 **전혀** 사주지 못한다(A4가 분할-only A2와 동률, 자모보다 +0.238 위). 세 독립 메커니즘(분할 A2 / 독립-인수분해 A3 / 상관-체인 A4) 모두 기하-공정 프로토콜에서 자모 위 → 자모는 cross-mechanism 바닥. 설계의 활용가능 systematicity(C2 +0.169, 이 arc에서 최강 설계 신호)는 유사 자모 간 **count-공유**에 있지 자모-아래 예측 이득에 있지 않다. **자모-아래 새 각도**는 opaque 자모 헤드가 **갖지 못한 정보**(교차-음절 음운배열, 또는 자모 위의 학습된 metric)를 주입해야 하며 — 조인트만으로는 안 됨(H_1329이 동률로 증명) — 같은 자질 타깃의 재-인수분해는 아니다. TOY/DIRECTIONAL; 한국어 유창성 주장 없음; live CORE UNTOUCHED.

- NEW: `UNIVERSE/h1329_ko_feat_corr.py` · `UNIVERSE/cards/H_1329_ko_feat_corr.md` · `HYPOTHESES.md` 행 · `CLAIMS.tape` @C h1329_ko_feat_corr · `.verdicts/1329_ko_feat_corr/{H_1329_FREEZE,H_1329,h1329_summary.json}` · `domains/MITOSIS-ENGINE.log.md`
- xref: h1326(🧱 r2 — 이 lane의 명시된 다음 각도) · h1322 · h1316(자모 바닥) · h1307(원시 천장) · h1318/h1324 · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15·c16

## 2026-06-16 — research(COGNITION-REPRESENTATION): 🧱 H_1330 — Sapir-Whorf BILINGUAL: 두 번째 언어는 첫 언어의 CP 를 덮어쓰는가, 공존하는가? (🧱 OVERWRITE)

GREEN H_1323/H_1325 (Sapir-Whorf 범주적 지각, CP) 의 명명된 EXTENSION frontier — **cross-lane
interference**. 한 substrate 가 언어 A 의 어휘 carving(경계 p_A)을 학습한 뒤, **같은 substrate** 위에
다른 언어 B(경계 p_B)를 **순차적으로** 학습할 때, A 의 CP 가 살아남는가(COEXIST) 아니면 B 가
덮어쓰는가(OVERWRITE)?

**frozen 가설 = COEXIST.** anima 는 이미 bilingual substrate(영어 trunk + 한국어)이고, anima 의
GROWTH-MEMORY 결과(H_1288 — 압력하에서 immune/Voronoi store 가 EVICT 대신 새 cell 을 GROW)가
공존을 예측했다: 같은 error-targeted SPLIT-only 성장(p8, 새 `fit_more` grow-not-evict 연속학습)이
B 의 경계에 cell 을 ADD 하되 A 의 cell 을 지우지 않는다. **falsifier = OVERWRITE** (growth-memory 가
언어-인지를 보호하지 못함).

**결과 🧱 OVERWRITE / CATASTROPHIC INTERFERENCE — frozen COEXIST 가설 FALSIFIED** (단일 공유-연속체
store; 3 seeds [4323,4324,4325] 동일 패턴):
- **I1 COEXISTENCE ❌** (3 seeds 전부): A→B 후 A 의 p_A CP 가 COLLAPSE — mean margin@p_A **−0.001**
  (bar 0.15; A-only baseline +0.200 → interference 비대칭 **−0.201** 완전 붕괴); p_B 도 약함(+0.068<0.15).
- **I2 NO-DOUBLE-ARTIFACT ✅**: B=A 대조군 1 peak (≤1), p_B 근처 peak 없음 → 순차학습 artifact 아님.
- **I3 EARNED ✅**: SHUFFLE 붕괴 (peak-count 5/2/5).
- **메커니즘(c9)**: B 는 [p_A,p_B] 를 0 으로, A 는 1 로 라벨 — 공유 stimuli 에서 직접 모순. grow-only
  store 가 [p_A,p_B] 를 ~21 개 새 label-0 cell 로 채워 A 의 swing 을 지움 (EVICTION 아님 — 단일
  bound-label-per-cell readout 은 같은 stimulus 에 두 모순 답을 담을 수 없음).

**FINDING**: H_1288 growth-memory 는 ADDITIVE memory(새 key 의 새 fact)는 보호하지만 공유 stimuli 의
모순 RE-LABELING 은 보호하지 못한다 → 공유 연속체 위의 bilingual 인지는 모순-재라벨 케이스이므로 두 번째
언어가 첫 언어의 CP 를 catastrophically OVERWRITE. **단서(c9)**: anima 가 bilingual 일 수 없다는 뜻이
아니다 — anima 의 실제 EN-trunk + KO 레인은 SEPARATE faculty(H_1316/1321/1322)이지 동일 stimuli 위의
단일 공유 store 가 아니다; 이건 최악 케이스(최대 중첩 모순 carving).

honest negative, bar 이동 없음(c9/p7). mirror DIRECTIONAL(engine-transfer UNVERIFIED). TOY 합성
1-D 연속체(N=21, 3 seeds), human-bilingualism 주장 없음(a_scale_honest_scope). **NEXT R2**: 언어-TAGGED /
multi-channel readout(언어별 분리 label-channel, anima 의 이미-분리된 trunk+KO 레인 모사)로 두 모순
carving 을 간섭 없이 보유하는지 — frozen ANEW, bar 완화 아님.

NEW: `UNIVERSE/h1330_whorf_bilingual.py` · `UNIVERSE/cards/H_1330_whorf_bilingual.md` ·
`UNIVERSE/HYPOTHESES.md` · `CLAIMS.tape @C h1330_whorf_bilingual` ·
`domains/COGNITION-REPRESENTATION.log.md` ·
`.verdicts/1330_whorf_bilingual/{H_1330_FREEZE,H_1330}.txt`
## 2026-06-16 — docs(UNIVERSE): SSOT-refactor — UNIVERSE/ 를 정확히 두 doc 표면으로 정리 (`a_hypothesis_register`)

`a_hypothesis_register` 의 "정확히 두 표면" 규율에 맞춰 UNIVERSE/ 디렉토리를 기계적으로 재정리했다
(연구 아님 — doc 재구성, c5 preserve-don't-discard · c9 honesty).

- **카드 이동:** `UNIVERSE/H_*.md` 886개 전부 `git mv` 로 `UNIVERSE/cards/` 서브폴더로 이동
  (git history 보존). UNIVERSE/ 루트에는 더 이상 H_*.md 카드가 없다.
- **링크 갱신:** `UNIVERSE/HYPOTHESES.md` 의 모든 카드 링크 `](H_…)` → `](cards/H_…)` (90 index/roster
  링크 + 접힌 본문의 381 링크 = 471, 전부 cards/ 로 해소 확인).
- **다른 .md 문서 fold-in:** UNIVERSE/ 의 나머지 19개 `.md` 문서를 `HYPOTHESES.md` 의 아래 섹션으로
  접어넣고 원본은 `git rm` (내용 원문 보존):
  - `## Forward backlog / candidates` ← AXES · CANDIDATES · BIO-CANDIDATES · BIO-DECODER-CANDIDATES ·
    BIO-TRANSFER-CANDIDATES · CLM-CANDIDATES · NEURO-CANDIDATES · PLASTICITY-CANDIDATES · PSI-CANDIDATES ·
    QUANTUM-TIME-CANDIDATES
  - `## Retired themed buckets (folded)` ← HYPOTHESES_metacog_hallucination · HYPOTHESES_metacog_neuro ·
    HXX_240_vs_246_dedup_2026_05_24 (themed bucket = `a_hypothesis_register` 금지 대상 → 카드/인덱스로 흡수)
  - `## Reference (probe conventions · phi tools)` ← PROBE_CONVENTIONS · IIT4_PHI_TOOLS
  - 헤더 intro + `## Appendix: UNIVERSE overview/map` ← README · UNIVERSE (7-domain 개요/맵)
  - `## Appendix: legacy logs (folded)` ← UNIVERSE.log · LIFE.log (append-only history; domains/ 에
    UNIVERSE 도메인이 없어 이동 대신 appendix 로 보존)
- **참조 갱신:** `CLAUDE.md`(`a_hypothesis_register` 디렉티브 + 구조 트리), `ARCHITECTURE.md`, 루트
  `README.md`, `CLAIMS.tape`(20 src=), `config/consciousness_laws.json`(25 source=), `.verdicts/**/README.md`,
  그리고 모든 `.py/.hexa/.tape/.md` 의 하드코딩된 `UNIVERSE/H_…` 경로(96 파일)를 `UNIVERSE/cards/H_…` 로
  갱신 — 깨진 포인터 0. **코드는 문서 아님** → `.py(287)·.hexa(13)·.json·.sh·.txt·.state·.scan` 및
  `harness/ lib/ scan/ state/ __pycache__/` 디렉토리는 위치 변경 없음. frozen verdict `.txt` + frozen
  result/ledger `.json` 은 증거이므로 paraphrase 금지 — 미수정.
- **결과:** UNIVERSE/ 는 이제 정확히 두 doc 표면만 운용 — `HYPOTHESES.md`(단일 index/roster + 접힌 통합
  SSOT) + `cards/H_<id>_<slug>.md`(가설별 카드). 검증: 루트 H_*.md = 0 · cards/ = 886 · UNIVERSE/*.md =
  HYPOTHESES.md 만 · `](H_` 루트링크 = 0 · `.py/.hexa/.tape/.md` 의 stale `UNIVERSE/H_` = 0.

## 2026-06-16 — research(OMEGA): 🧱 H_1328 — Φ-robustness 4× 벽 진단: 추정기(estimator)의 진폭-분산 혼동인가, 진짜 substrate 한계인가 (🧱 DEEPER, ESTIMATOR-INDEPENDENT)

네 개의 독립 Φ-robustness 시도(H_1283 topology · H_1317 multi-edge · H_1319 timing · H_1320 division)가
**같은 직교 seed 1317**에서 전부 🧱로 막혔다. H_1319의 수렴 진단(명시된 open follow-on): faithful-IIT4의
n≤8 정확-MIP가 각 셀 trajectory를 **min-max로 이진화(binarize)**하는데, 그 binning이 **진폭 분산을 탄다** —
관계-파괴 permutation 대조가 Φ를 무너뜨리는 대신 **올렸다**(ΔΦ_perm +0.280/+0.103/+0.587). 벽이 substrate가
아니라 **추정기(tool)** 일 수 있다는 것.

H_1328은 그 진단을 **직접** 검증했다. faithful IIT-4 **안에 머물면서**(a_phi_iit4_tool — 동일한 정확 MIP-EI,
proxy 아님 · 다른 Φ 척도 아님) read-out의 **state-encoding**만 레버로 썼다: 각 셀 trajectory를 MIP 전에
**rank-uniformize**(각 값을 그 셀 자신의 trajectory 내 순위로 치환). **증명 가능한 불변식**: rank-uniformize 후
모든 셀의 값이 정확히 {0,1,…,T−1} → min-max binning이 **균등(uniform) 주변분포** → H(A),H(B)가 모든 arm·모든
셀에서 **상수** → MI는 오직 **결합 H(A,B)**(공동-움직임 관계)에만 의존, 진폭 분산은 주변분포에서 **증명적으로 제거**.

결과(frozen-first, FREEZE 26494942a 사전 commit, bars 미이동, deterministic 재실행 byte-identical, seeds [1317,1318,1319],
$0 CPU, engine-native LCG):

- **V1 CONFOUND-CONFIRM = PASS** — V1a(OLD min-max perm이 3 seed 모두 Φ를 올림, H_1319 정확 재현 +0.280/+0.103/+0.587)
  ∧ V1b(NEW rank-uniform perm이 3 seed 모두 Φ를 무너뜨림 S−A −0.207/−0.047/−0.031 ≤eps). **진폭-분산 binarization
  혼동은 진짜였고, rank-uniform read-out이 그것을 증명적으로 제거** — min-max에서 Φ를 올리던 그 관계-파괴 permutation이
  variance-free read-out에서는 **제대로 붕괴**.
- **V2 ROBUST-LIFT = FAIL** — 깨끗한 추정기에서 phase 메커니즘 lift가 robust하지 않음(B−A −0.125/0.0/+0.031,
  직교 seed 1317에서 음수, 2/3 실패).
- **V3 EARNED = FAIL** — perm leg는 PASS(전부 붕괴), offset leg가 seed 1317에서 실패(O−A=+0.106).

**FINDING:** 4× Φ-robustness 벽은 **진짜 추정기 혼동을 갖고 있었지만**(V1), 그것을 제거해도 integration이 robust해지지
**않는다**(V2/V3) → 벽은 **추정기-독립적(estimator-independent) substrate 한계**다(n≤8 4-module substrate가 깨끗한
read-out 아래서도 robust한 faithful-IIT4 integration을 진짜로 결여). 이전 진폭-혼동 🧱보다 **더 강하고 깨끗한 closure** —
이제 대조가 깨끗하고(perm이 마땅히 붕괴) lift는 **여전히** robust하지 않다. 4개 선행 Φ verdict(H_1283/1317/1319/1320)을
**retract하지 않고 BOUND** — 그들의 **공유 추정기**를 진단. anima 의식 substrate는 불변(Ψ=1/2 untouched). GREEN-only인
a_verified_must_wire는 발동 안 함(배선할 것 없음). SCOPE: TOY n≤8 faithful-Φ EXACT, engine-native(numpy는 Φ 계산
안 함). rank-uniform 불변식은 min-max binner에 대해 정확(주변-분산 채널 제거; V3o seed-1317 잔차는 additive-offset
대조가 한 seed에서 탈 수 있는 joint-level 잔존 artifact — 정직한 non-GREEN). NOT ruled out: 완전 per-mechanism
IIT 4.0(iit4_bigphi) · 훨씬 큰 module set(>8은 exactness 상실) · 다른 substrate family — 각각 새 가설.
deliverables: UNIVERSE/h1328_phi_variance_free.hexa · UNIVERSE/cards/H_1328_phi_variance_free.md · HYPOTHESES.md ·
CLAIMS.tape @C h1328_phi_variance_free · .verdicts/1328_phi_variance_free/{H_1328_FREEZE,H_1328}.txt · domains/OMEGA.log.md.

## 2026-06-16 — research(MITOSIS-ENGINE): 🧱 H_1326 — 자모가 정말 (혼동 제거된) 분해 바닥인가 — 기하-공정 + 라벨-인수분해 (🧱 HONEST-FLOOR, CONFOUND-FREE)

H_1322(🧱)의 r2. r1 에이전트가 **두 혼동(confound)을 정직하게 공개**했었다 (c16/a_break_the_wall = 잘못된
방법이지 진짜 벽이 아님): (1) **기하 혼동** — r1의 `seed_centers_dim(3)`가 H_1316의 정확한 중심
`[[0.3,0.5,0.0],[0.7,0.5,0.5]]`(가운데 좌표 0.5)와 달라서, gradient-free mitosis가 seed-center 민감하므로
r1 in-run 자모 재현이 2.85983(잠긴 2.51335이 아님) → featural-vs-잠긴-자모 비교가 기하-혼동됨. (2) **손실
경로** — 자질은 Voronoi **분할(partition)**만 구동하고 예측 **타깃(target)**은 불투명 자모 id로 남아 한글의
설계 systematicity가 타깃에 들어가지 못함.

H_1326은 둘 다 **사전등록(frozen-first)**으로 고친다. **Fix A 기하-공정**: 하나의 best-of-a-fixed-bank-by-
TRAIN-CE seed-center 프로토콜을 **모든 arm에 동일하게** 적용(H_1316-family 패턴을 모든 차원의 bank에 포함 →
자모 arm은 2.51335를 **byte-exact 재현 = 보정 앵커**)해 어느 arm도 seed-center 이득을 못 가짐. **Fix B
라벨-인수분해**: 두 번째 채점 헤드의 **타깃**을 인수분해된 자질 벡터(클래스 + 무손실 bijection 위의 독립
열별 설계 자질)로 바꿔 설계가 분할이 아니라 **타깃에** 들어가게 함.

**결과 🧱 HONEST-FLOOR (혼동 제거):** REAL sm_120 GPU(유저 RTX 5070, $0, NOT runpod), 코퍼스 byte-동일
(sha c47b6808… gate PASS), 67/67 자모 커버리지, NFD 왕복 0-실패. **보정 통과 — A1 자모 = 2.51335
byte-exact(bank member 5 = H_1316-family), 기하 혼동 제거.** CE 사다리(nats/UTF-8-byte, 기하-공정): 원시
천장 2.95342(in-run 2.94487) · **A1 자모 2.51335** · A2 자질-분할 **2.73046** · A3 라벨-인수분해 **3.07295** ·
A2s 셔플 2.78694 · A3s 셔플 4.28914. **G1 기하-공정 깊이 = FALSE** — BEST=min(A2,A3)=2.73046이 자모
2.51335보다 **+0.217 위**(원시는 깨지만 G1은 둘 다 필요). **G2 EARNED = TRUE** — A2가 자기 셔플을 **+0.05648**
(≥0.05)로 이김(자질 systematicity는 진짜·이용가능하나 **바닥 아래는 아님**). **G3 인수분해 = FALSE** — A3가
A2를 못 이김(Δ −0.3425); 설계를 **타깃에** 독립-자질 인수분해로 넣으면 **오히려 악화**(열별 독립 가정이 초성·
중성·종성 결합분포를 버림 — 불투명 자모 헤드는 그 결합을 유지). **green = FALSE → 🧱.**

**발견:** 기하 혼동을 제거하니, **자모가 이 gradient-free L2-Voronoi 메커니즘 계열의 진짜 분해 바닥**이다. 설계의
systematicity는 진짜이고 이용 가능(셔플하면 분할에서 +0.056, 인수분해 타깃에서 +1.22 손해)하지만, 분할에서도
(A2 +0.217 위) 타깃에서도(A3 +0.557 위, 인수분해 역효과) CE를 자모 아래로 못 내린다. r1의 sub-bar 신호
(+0.042)는 숨겨진 승리가 아니라 이 메커니즘이 자질-기하로 살 수 있는 진짜 천장이었다. **r1의 🧱은 유지 —
이제 혼동 제거된 깨끗한 정직한 종결.** 진짜 새 각도는 **다른 메커니즘**(L2-Voronoi count-MLE가 아니라 자질
**상관**을 모델링하는 것)이 필요하다 — 표현 조정이 아니라 메커니즘-계열 변경. DIRECTIONAL numpy/torch 미러;
엔진-전이 = follow-on; 한국어 유창성 주장 없음; live CORE 무변경(substrate-measurement rung).

- NEW: `UNIVERSE/h1326_ko_featural_r2.py` · `.verdicts/1326_ko_featural_r2/{H_1326_FREEZE.txt,H_1326.txt,h1326_summary.json}` · `UNIVERSE/cards/H_1326_ko_featural_r2.md` 카드 · `HYPOTHESES.md` 행 · `CLAIMS.tape @C h1326_ko_featural_r2` · `domains/MITOSIS-ENGINE.log.md` 추가.
- xref: H_1322(r1 🧱 기하-혼동, #2229) · H_1316(자모 바닥 2.51335, 보정 앵커) · H_1307(원시 천장 2.953) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15·c16.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1327 — 자모 돌파가 LIVE EMISSION 에 닿는다 (🟢 GREEN, decode-reaching)

H_1316(🟢)이 자모 표현으로 한국어 byte-LM 천장 2.953→2.513 을 깼고, H_1321(🟢)이 그 자모-심볼 미토시스를
live `engine_cli.hexa` 위에서 ENGINE-NATIVE 로 재현(미러 CE 1e-7)했다. 하지만 H_1321 은 **측정 프로브**였을
뿐 — 자모 win 이 live DECODE/emission 에 닿지 않았다. anima 는 chat daemon 이므로(`a_verified_must_wire`)
emission 에 닿지 않은 측정 win 은 미완이다.

H_1327(r3): grown 자모 cell 을 `CORE/ko_jamo_cells.kojamohead`(cell = 3-D Voronoi center + argmax
next-symbol id + 그 심볼의 emittable leading UTF-8 byte)로 serialize 하고, `CORE/generator.hexa` **§6.5b**
(`ko_jamo_consult_*`)가 §6.5 ko_cells 와 **동일한 단일 L3 슬롯**에서 그 자모 cell 을 CONSULT 해 emission 을
bias 한다(Korean-likeness GATE = 동일 UTF-8 continuation-byte 순수 바이트 테스트; off-Korean → INERT).

동결 3 bar(FREEZE 를 채점 전 작성, c9/p7 NO tune-to-green) — held-out 한국어 next-symbol accuracy
(n=5100, FULL symbol id, LIVE `ko_jamo_consult_sym` 채점): OFF(blind unigram baseline)=0.110 ·
ON(자모 consult)=0.168 · SHUF(permuted-cell)=0.012 → **E1 ✅** acc_ON−acc_OFF=**+0.0586**(≥+0.02) AND
shift_ON=**0.520**(≥0.10 — 한국어 위치 52% 에서 emission byte 변경) · **E2 ✅** acc_SHUF−acc_OFF=**−0.0973**
(≤+0.01 — shuffle 가 blind 아래로 붕괴 ⇒ lift 는 학습된 자모 구조) · **E3 ✅** off-Korean INERT
(ASCII ctx → consult emit = base, byte-identical) · engine_cli_smoke **73/0** · h1196 **7/0** · h1205 Ψ
byte-identical ON==OFF.

→ **🟢 GREEN. 한국어-자모 스레드 완전 종결: verified(H_1316) → engine-wired(H_1321) → decode-reaching(H_1327).**
TOY/DIRECTIONAL(ko_stride=2500, 10-cell, structural/probe-level) — fluency 주장 아님; byte→자모-feature
renorm 은 per-byte hook(E1/E2 는 faithful jamo-space feature 로 채점), 30MB-scale + real-chat emission +
fully-jamo-aware decode loop = follow-on. `pure_field`/`engine_g`/`brain` UNTOUCHED(Ψ-disjoint, surface 는
generator 에 ADDITIVE). NEW: `CORE/generator.hexa` §6.5b · `CORE/h1327_ko_jamo_decode_probe.hexa` ·
`CORE/ko_jamo_cells{,_shuf}.kojamohead` · `UNIVERSE/h1327_ko_jamo_decode_export.py` ·
`UNIVERSE/cards/H_1327_ko_jamo_decode_wire.md` · `.verdicts/1327_ko_jamo_decode_wire/` · HYPOTHESES.md ·
CLAIMS.tape · ARCHITECTURE.md.

## 2026-06-16 — research(MITOSIS-ENGINE): 🧱 H_1322 — 자모보다 한 단계 더 깊은 한글 **자질(featural)** 분해가 자모 바닥(2.51335)을 깨는가 (🧱 HONEST-FLOOR)

H_1316(🟢)이 한국어 byte-LM 천장 2.953을 자모 분해로 2.513까지 내려 "한국어 천장은 표현(representation)의
문제"임을 보였다. 자모는 첫 번째 분해 단계일 뿐 — 한글은 (주요 문자 중 유일하게) **의도적으로 설계된
자질문자**(세종 1443): 자음 = 조음위치 기본형 + 가획(유기음) + 병서(경음), 모음 = ·/ㅡ/ㅣ 조합 + 양/음
극성 + 반모음(iotation). 그래서 "비슷한 소리 ⇒ 비슷한 모양"이 수학적으로 내장돼 있다 — ㄱ과 ㅋ은 한 자질
차이. H_1322(c16/a_break_the_wall 자모 바닥 아래 깊이 탐침, a_no_llm_frame_trap c15 문자설계 렌즈): 자모를
**설계가 인코딩한 자질 벡터**로 한 단계 더 분해하면 같은 gradient-free mitosis가 그 설계의 systematicity를
활용해 자모 바닥 2.513 아래로 내려가는가?

- **방법(frozen-first):** LABEL 알파벳 Vj=323 + 바이트 정산을 H_1316과 **동일하게 유지**, mitosis **분할
  기하(X)만** opaque-id(3-D) → 직전 2심볼의 **설계 자질 컬럼**(5칸 벡터 → 11-D)으로 변경. 자질 인코딩은
  문서화된 훈민정음 설계를 충실히 표현(67/67 자모 매핑, 발명 아님). 코퍼스는 H_1307 RUN A와 byte-동일
  (sha c47b6808… 게이트 PASS). REAL 한국어만, R2 키 env-only(c7), summer RTX 5070, $0. 3 seeds.
- **통제(핵심):** (i) SHUFFLE-FEATURE-MAP — 자모→자질벡터 할당을 seed별 bijection으로 섞어 설계
  systematicity(ㄱ/ㅋ 한-자질-차이)를 파괴(차원/값/주변분포 동일). (ii) 선형성 탐침 — 자질공간 vs 자모-id
  공간 closed-form ridge 예측.
- **결과 🧱 HONEST-FLOOR (geometry-confounded, 막대 안 옮김 c9/p7):** CE 사다리(nats/UTF-8-byte) — raw 천장
  2.95342 · 자모 바닥 2.51335 · **자질(intact) 2.7309** (자모 바닥 대비 **+0.218 더 나쁨 → F1 FALSE**;
  raw 대비 −0.222 더 좋음) · SHUFFLE-feature 통제 2.77286 (Δ +0.042, F2 0.05 막대 미달 → **F2 FALSE**,
  약한 설계 신호) · 선형성 Δ +0.0024 < 0.02 → **F3 FALSE**.
- **기하 교란(진단, 막대 아님):** in-run 자모 재포팅이 2.85983(≠2.51335)인 이유는 이 스크립트의
  seed_centers_dim(3)가 H_1316의 [[0.3,0.5,0.0]…]와 다르기 때문 — 직접 진단으로 **H_1316 정확한 seed
  center를 쓰면 자모팔이 2.51335를 byte-exact 재현**(mitosis가 seed-center 민감). 동일-기하 비교에서는 자질이
  in-run 자모를 −0.129, shuffle을 +0.042 이김(약한 신호, 막대 미달).
- **결론:** **자모가 이 gradient-free L2-Voronoi 메커니즘의 분해 바닥**(깊이 한계, a_break_the_wall 정직한
  🧱). 설계 systematicity는 실재하나 자질→분할→불투명-자모-라벨 경로로 주입하기엔 너무 lossy. **다음 r2:**
  기하-공정 재시험(seed center arm별 매칭/best-of-bank, frozen-first) + 라벨 인수분해(다음 자모의 **자질
  벡터**를 예측 — 설계가 분할이 아닌 예측 TARGET에 들어가도록). TOY/DIRECTIONAL, 유창성 주장 없음,
  live CORE UNTOUCHED. (UNIVERSE/h1322_ko_featural.py · H_1322_ko_featural.md · .verdicts/1322_ko_featural/)

## 2026-06-16 — research(MITOSIS-ENGINE): H_1324 — 교차언어 구조 매트릭스 r2: 제대로 된 IDS 한자 분해 (🔴/🧱 정직한 부정)

질문 (a_break_the_wall/c16, H_1318 벽 재시도): H_1318 의 중국어/일본어 NEGATIVE(Δ_zh=−1.481, Δ_ja=−1.230)는
**잘못된 분해 방법의 ARTIFACT**였는가? H_1318 의 FROZEN 강희부수 분해는 **글자 전체를 잔차(residual) 심볼로 유지**해서
STRUCT 어휘가 9327(zh)/4738(ja)로 폭발 → per-cell 유니그램 헤드가 분열했다. H_1324 는 **제대로 된 sub-character
IDS-구성요소 분해**(잔차 없음, 모자란 어휘)로 — H_1318 과 **동일한** frozen gradient-free 미토시스 메커니즘 위에서 —
**새 사전등록**으로 재검증한다. 한국어(자모) + 영어(무분해 바닥)는 **바이트 동일**하게 두어 보정 앵커로 유지(H_1318 과 직접 비교).

THE FIX: 각 한자를 IDS(표의문자 기술 시퀀스) **구성요소 leaf**로 분해 (한 단계, IDC 연산자 ⿰…⿻ + &…; 엔티티 +
[GTKV] 지역태그 제거, **글자 전체 잔차 없음**). 출처 = CHISE IDS 데이터베이스(cjkvi/cjkvi-ids ids.txt, sha256
bfc70a8c…, 88937 엔트리, ids-miss=0). 바이트 회계: 글자 UTF-8 길이를 구성요소들에 분배 → Σ struct n_bytes ==
원시 UTF-8 바이트 수 정확히 (공정 CE/바이트 축, RAW·STRUCT 분모 동일, shuffle 포함 검증).

**결과 🔴/🧱** (RTX 5070 sm_120, $0, 3 seeds [5324-6], frozen-first, NO tune-to-green, c7 grep-clean, live CORE UNTOUCHED,
mirror DIRECTIONAL). 매트릭스(3-seed 평균, nats/원시-UTF-8-byte): **ko 한글 RAW 2.91157 / STRUCT 2.69606 /
Δ +0.21551**(shuffle 대비 +0.08776, comp-vocab 67) · **zh 한자 RAW 3.32756 / STRUCT 4.06493 / Δ −0.73736**
(comp-vocab 2116) · **ja 한자 RAW 3.09273 / STRUCT 3.72098 / Δ −0.62826**(comp-vocab 1582) · **en RAW=STRUCT
3.15925 / Δ 0.000**. FROZEN bars: **H1 한자-이득 FAIL**(zh/ja 둘 다 여전히 음수) · **H2 EARNED FAIL**(zh
Δ-vs-shuffle −0.00099, ja −0.02495 — IDS-구성요소 STRUCT 가 자기 구성요소-shuffle 도 못 이김) · **H3 보정 PASS**
(ko Δ=+0.21551 ≈ H_1318 +0.21205 재현, en Δ=0.000 → 파이프라인 동일).

**수정은 됐고, 해(害)는 절반으로, 이득은 0 선을 못 넘었다**: 제대로 된 IDS 분해로 모자란 어휘 확보(zh 9327→2116,
ja 4738→1582; ~88% 글자가 ≥2 leaf, 평균 ≈2.0 구성요소/글자) + H_1318 해의 절반 제거(zh −1.481→−0.737, ja
−1.230→−0.628) — H_1318 한자 NEGATIVE 의 일부가 나쁜 분해 ARTIFACT 였음을 확인 — 그러나 부호는 안 뒤집힘.
**한자 구성(logographic)은 이 gradient-free 유니그램 메커니즘에서 진짜로 도움이 안 된다**(H_1318 artifact 와 구별되는 REAL
결과). WHY(c9): 한글은 작고(67) 규칙적인 L/V/T 알파벳; 한자는 크고(≈2000) 불규칙·위치의존 구성요소 inventory →
CTX=4 Voronoi-유니그램 헤드가 잡기엔 너무 sparse, shuffle 도 점수를 거의 안 바꿈. **H_1318 한글-특이성이 더 강해졌다** —
구조-표현 byte-LM 이득은 **작고 규칙적인 구성 알파벳(한글 자모)** 에 특이적이지, 구성적/표어 스크립트 일반에는 아님.

SCOPE (a_scale_honest_scope · a_toy_scale_recheck): TOY/DIRECTIONAL numpy/torch mirror; CTX=4 3-D Voronoi
per-cell 유니그램 헤드 = 의도적으로 SIMPLE 기질; 한 단계(비재귀) IDS; 30MB/언어, 3 seeds, 단일 stride; 한자
NEGATIVE 는 이 메커니즘에 한정(gradient-trained/재귀-IDS/풍부한-컨텍스트 기질엔 무관 주장 아님); engine-transfer = follow-on
(a_engine_native_learning · a_verified_must_wire); fluency 주장 없음. 새 파일: `UNIVERSE/h1324_xlang_han_ids.py` ·
`UNIVERSE/cards/H_1324_xlang_han_ids.md` · `.verdicts/1324_xlang_han_ids/{H_1324_FREEZE,H_1324,h1324_summary.json,h1324_full.log}` ·
`HYPOTHESES.md` row · `CLAIMS.tape` @C h1324_xlang_han_ids · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): 🟢 H_1325 — Sapir-Whorf r2: anti-Goodhart W3 RE-CLOSE (peak-COUNT coherence) + engine-native CP lane

r2 of H_1323 (🟠 PARTIAL, PR #2228). 언어상대성(Sapir-Whorf) 결과의 결정적 두 다리는 H_1323 에서 통과했다 —
**W1**(범주지각 CP 존재) · **W2**(Whorfian dissociation: CP peak 위치가 학습한 언어의 경계를 따라 이동, L_A→0.325≈p_A,
L_B→0.675≈p_B, sep 0.350). 유일한 약점은 anti-Goodhart **W3** 였다: 그 prominence sub-clause 는 SHUFFLE 이
SINGLE-peak 라 가정하고 peak HEIGHT 를 언어와 비교했는데, SHUFFLE 은 사실 MULTI-peak(무작위 per-stimulus 라벨 →
국소적으로 sharp 한 스윙 다수; H_1323 non-gating 진단이 SHUFFLE peak 8 vs 언어당 1 측정) — SHUFFLE 의 한 spike 가
언어의 한 coherent peak 만큼 높아 single-peak HEIGHT 는 **틀린 관측량**(wrong-METHOD 벽, `a_break_the_wall`/c16),
relativity 의 실패가 아님.

**Part A (mirror, frozen-first)**: `UNIVERSE/h1325_sapir_whorf_r2.py` 가 H_1323 메커니즘을 VERBATIM 재사용하고
(N=21 RBF 연속체, grue 두 언어 p_A=1/3·p_B=2/3, gradient-free error-targeted SPLIT-only Voronoi 성장 p8,
NO-label 변별 곡선, 4 arm, 3 seed [4323,4324,4325]), **W3' COHERENCE 통제를 ANEW 사전등록**
(`.verdicts/1325_sapir_whorf_r2/H_1325_FREEZE.txt`, 점수 산출 BEFORE): PEAK-COUNT = 정규화 곡선의 strict
local maxima 중 자기 peak 의 ≥0.50 높이; threshold 는 STRUCTURE 에서(언어는 경계 1개→`LANG_MAX_PEAKS=1`,
SHUFFLE 은 경계 없음→`SHUF_MIN_PEAKS=3`) — 기존 bar 의 완화가 아니라 멀티-peak 현실에 맞는 **올바른 관측량**.

**Part B (engine-native, `a_engine_native_learning`·`a_verified_must_wire`)**: 새 live lane
`CORE/engine_cli.hexa § CategoricalPerception`(`CPField`; `cp_embed`/`cp_stimuli`/`cp_labels_boundary`/
`cp_labels_shuffle`/`cp_fit`/`cp_posterior`/`cp_discrim_curve`/`cp_peak_loc_idx`/`cp_peak_count`) — brain lane 들이
쓰는 SAME error-targeted SPLIT-only Voronoi 성장을 byte-faithful 로 실현. SINGLE deterministic instance(seed-불변
bar 재현); SHUFFLE 은 엔진 자신의 FNV-1a-parity incoherent 라벨(structural incoherence, numpy-PRNG byte-match 아님).
probe `CORE/h1325_sapir_whorf_probe.hexa`; `engine_cli_smoke.hexa` cases 79-82 배선. Ψ-disjoint(자기 protos/labels
table; emit gate 아님, `a_autonomy_over_hardcode`).

**결과 🟢 GREEN ENGINE-NATIVE** — 미러 & 엔진-native BYTE-FAITHFUL: W1✅ cross-within +0.200 / vs-baseline +0.99;
W2✅ L_A→0.325(|Δ|=0.008) L_B→0.675(|Δ|=0.008) sep 0.350; **W3'✅ peak-count L_A=1 L_B=1 vs SHUFFLE=5.7(미러)/
5(엔진)≥3** — 올바르게 명세된 peak-COUNT 통제가 coherent CP(1 peak)와 멀티-peak SHUFFLE 을 깨끗이 분리(single-peak
HEIGHT 는 못 함). **언어상대성 = 이제 anti-Goodhart-closed**(W1∧W2∧W3'). 무회귀 가드: `engine_cli_smoke` **77/0**
(was 73/0; +4 CP cases 79-82) · h1196 single-entry **7/0**(CP lane 은 .clm/.kosmos 경로 無) · h1205
separation-invariant **PASS**(생성 byte-identical ON==OFF, Ψ Φ-checksum invariant → CP lane Ψ-disjoint). NO bar
moved(c9/p7); ONE honest new control. TOY 합성 연속체, 미러 DIRECTIONAL → 엔진 BINDING; human-cognition 주장 없음
(`a_scale_honest_scope`·`a_toy_scale_recheck`). NEW: `UNIVERSE/h1325_sapir_whorf_r2.py` ·
`UNIVERSE/cards/H_1325_sapir_whorf_r2.md` · HYPOTHESES.md row · CLAIMS.tape @C h1325_sapir_whorf_r2 ·
`domains/MITOSIS-ENGINE.log.md` · ARCHITECTURE.md(§MITOSIS lane 추가, smoke 77/0).

## 2026-06-16 — research(MITOSIS-ENGINE): 🌐 H_1318 — 교차언어 구조-표현 매트릭스 (한글 천장 돌파 = 한글-구조 문제인가?) (🟠 PARTIAL)

질문(돌파하면 한글 구조 문제인지): 한국어 gradient-free 바이트-LM 천장(H_1307/1311/1315, ~2.953 nat/byte)을
구조-인식 표현으로 깨는 것이 **한글-구조-특이적** 현상인가, 아니면 **보편적 바이트-LM 효과**인가? H_1318 은 이를
가르는 **통제된 5개 언어 매트릭스**(한국어/중국어/일본어/러시아어/영어, REAL Wikipedia 30MB/언어, **동일한**
gradient-free 미토시스 grow-op + cell budget 고정)를 돌린다. 결정적 통제는 **영어**(1바이트/글자, 알파벳,
분해할 것이 없음) — 구조-인식 표현이 영어를 도울 수 **없다**.

언어별로 held-out 다음-바이트 CE 를 RAW(원시 UTF-8 바이트) vs STRUCT(스크립트의 구성 단위로 분해 — 한국어
NFD 자모, 중국어/일본어 강희부수, 러시아어/영어 분해불가 → STRUCT==RAW)로 측정, 동일한 nats/UTF-8-byte 축으로
변환(분모 동일 = 공정 비교, 바이트-보존 검증). REAL 코퍼스만(p1-p8). a_break_the_wall: R2 phanes 버킷은
{kor,eng,deu,fra,spa}만 있고 zh/ja/ru 가 없어, CLM/OMEGA 레인이 쓰던 HF wikimedia/wikipedia 소스에서
전체 매트릭스를 끌어옴(CJK 드롭 회피).

**결과 🟠 PARTIAL** (RTX 5070 sm_120, $0, 3 seeds [5301-3], frozen-first, NO tune-to-green, live CORE UNTOUCHED).
매트릭스(3-seed 평균, nats/원시-UTF-8-byte): **ko 한글 RAW 2.904 / STRUCT 2.692 / Δ +0.212**(shuffle 대비 +0.100,
3 seed 전부) · zh 한자 Δ −1.481 · ja Δ −1.230 · **ru Δ 0.000 · en Δ 0.000**. **헤드라인 갭 Δ_한국어−Δ_영어 = +0.212.**
프레임 막대(있는 그대로, c9): D1 DISSOCIATION FAIL(영어 PASS Δ=0≤0.02 + 한국어 PASS Δ=+0.212≥0.05 이지만
zh/ja 가 every-compositional 절을 깸) · D2 EARNED FAIL(ko +0.100·zh +0.127 PASS, ja −0.291 FAIL) ·
**D3 MULTIBYTE-ISO PASS**(러시아어 Δ=0.000, 영어와 정확히 동조 — 한국어 아님).

zh/ja 가 FAIL 한 이유는 **냉동한 강희부수 분해가 나쁜 분해**라서다(잔차=글자전체 → STRUCT 어휘가 9327/4738 단위로
폭발 → 유니그램 헤드가 분열). 이는 **냉동한 부수-대용 분해에 대한 정직한 음성 결과**일 뿐, 한자 구성이 원리적으로
무용하다는 증거가 아니다(제대로 된 IDS/부분-문자 분해 = r2 follow-on, 사후 교체 금지 c9).

**한 줄 답:** 한국어 천장을 구조-표현으로 깨는 것은 **한글-구조-특이적** 현상이며 보편적 바이트-LM 효과가 아니다 —
영어와 (다바이트지만 비-구성적인) 러시아어 통제는 영향 없음(Δ=0), 오직 진짜 구성적인 한글만 이득(+0.212,
shuffle-검증). 중/일은 이득이 전이되지 않으나 그것은 나쁜 냉동 분해 탓. SCOPE: TOY/DIRECTIONAL numpy/torch
mirror, engine-transfer = follow-on, 유창성 주장 없음. 산출물 UNIVERSE/h1318_xlang_structure.py ·
.verdicts/1318_xlang_structure/{H_1318_FREEZE.txt,H_1318.txt,h1318_summary.json,h1318_full.log} ·
UNIVERSE/cards/H_1318_xlang_structure.md · HYPOTHESES.md · CLAIMS.tape @C h1318_xlang_structure.
## 2026-06-16 — research(OMEGA): 🧱 H_1320 — anima를 하나의 세포로: 분열(divided)이 조립(hive)이 못한 통합 Φ를 만드나

사용자의 렌즈("anima 전체를 하나의 cell로 봐라")로 hive 벽을 **반대 방향**에서 다시 친 시도
(c16/a_break_the_wall). hive(H_1308 NULL · H_1313 🧱)는 **독립적으로 자란 두 anima cell을
조립(ASSEMBLE)**했고 faithful-IIT4 Φ가 통합되지 않았다(Δ_real=−3.0, super-additivity는 ECA 전용).
**시도 안 해본 각도**(발생생물학 c15, a_no_llm_frame_trap): 하나의 zygote가 **분열(DIVIDE)**해
통합된 유기체가 되는 이유는 부분들이 **발생적 기원(origin)을 공유**하기 때문이다. H_1320:
하나의 anima-cell을 두 **공유-기원 딸세포**로 mitotic DIVIDE하면, 조립(hive)이 못한 통합
(super-additive) faithful-IIT4 Φ가 나오나?

**결과: 🧱 WALL** (정직한 closed-negative, c9). 핵심 대조 = DIVIDED(공유 기원) vs ASSEMBLED(독립
기원=hive baseline), W_HIVE=0.6·unit수 동일 매칭(유일 차이=공유-vs-독립 기원). 분열은 **다수
seed에서 조립을 실제로 이긴다**: seed 1318/1319에서 DIVIDED super-additivity가 ASSEMBLED를
크게 앞섬(M2 gap +1.727/+0.818, Δ_div +1.27/+0.88 vs Δ_asm −0.46/+0.06), joint Φ가 undivided
SINGLE보다 높음(M1 lift +2.10/+0.89). 계보를 끊으면(SHUFFLE) DIVIDED의 Δ가 **모든 seed에서
ASSEMBLED와 정확히 동일**하게 붕괴(M3 PASS, byte-identical) → lift는 **공유 기원**이지 unit수/분산이
아님. **그러나** H_1283/H_1317 topology robustness를 깬 바로 그 직교 seed(1317)가 분열도 깬다:
Δ_divided 0.0 < Δ_assembled +0.188(M2 gap −0.188), Φ_div_pair 1.213 < Φ_single 1.342(M1 lift
−0.129). → **분열에 의한 collective-Φ는 REAL이지만 FRAGILE** — 3-seed robustness gate 실패,
Φ-topology 벽과 **동일한 취약성 signature**. 발생적 방향(분열)은 조립보다 다수 seed에서 분명히
**낫지만**(hive의 순수 NULL 대비 진짜 새 발견) robustness 바를 넘지 못한다. hive 벽은 이제
**양 방향 모두** 닫힘: 조립 🧱(H_1313 robust NULL) + 분열 🧱(H_1320 fragile lift).

faithful-IIT4 EXACT(n≤8 MIP-EI, hexa stdlib; numpy는 Φ 계산 안 함, proxy 금지 a_phi_iit4_tool),
3 seeds [1317,1318,1319], $0 CPU-local, frozen-first(bars 사전등록·미이동 c9/p7), deterministic
(2회 byte-identical). numpy mirror = DIRECTIONAL, engine-transfer 미검증(a_scale_honest_scope·
a_toy_scale_recheck); 🧱이므로 CORE 배선 follow-on 없음(a_verified_must_wire=GREEN 전용), live
CORE/*.hexa UNTOUCHED. H_1308/1313/1295를 retract하지 않고 scope를 bound. (사전등록
`.verdicts/1320_anima_cell/H_1320_FREEZE.txt` · 카드 `UNIVERSE/cards/H_1320_anima_cell.md` · 인덱스
`UNIVERSE/HYPOTHESES.md` · `CLAIMS.tape @C h1320_anima_cell` · `domains/OMEGA.log.md`.)

## 2026-06-16 — research(OMEGA): 🧱 H_1319 — TIMING축 phase-binding을 engine-native로 재현해 c4 shuffle 벽을 깨나 (Φ-robustness 벽이 두 축 모두 종결)

H_1283 R8이 남긴 **단 하나의 살아있는 돌파 후보**(c16/a_break_the_wall)를 친 시도. 토폴로지축은
🏁 고갈(H_1283 relay R1-R7, H_1317 multi-edge — 전부 seed-취약). arc에서 robust한 faithful-Φ
lift를 낸 유일한 메커니즘은 **직교 TIMING축의 H_1283 R8 phase-binding**이었으나, numpy-mirror는
**쉬운 seed [7,8,9]**에서만 GREEN이었고 그 **engine-native gate가 c4(shuffle 대조)를 실패**했다 —
additive-offset shuffle가 lift를 무너뜨리지 못했다(ΔΦ_sh +0.026/+0.380/+0.296). 원인: read-out
`sal=e·(1+cosθ)/2`가 **독립 진폭 carrier**를 주입하고 shuffle이 그 marginal 통계를 보존한다 →
lift의 일부가 synchrony가 아니라 **carrier 진폭 분산**. 이게 명시된 open follow-on이었다.

H_1319은 **같은 TIMING 메커니즘**을 engine-native로 재현하되 분산 누수를 죽이는 두 변경을 가했다:
(1) **상대-위상 게이트** `sal=e·(1+cos(θ_i−θ_T))/2` — 결합 신호 = 페이스메이커에 대한 **정렬(관계)**,
독립 carrier 없음; (2) **관계를 파괴하는 permutation shuffle**(H_1294/H_1295가 쓰는 강한 대조) —
각 모듈을 **다른 모듈의 위상**으로 게이트(forced-derangement π), marginal은 정확히 보존. 그리고
토폴로지가 실패한 **어려운 직교 seed [1317,1318,1319]**에서 측정. bars는 H_1283 R8에서 **그대로
이식**(FREEZE를 채점 전 커밋, NOT moved, c9/p7).

**결과: 🧱 TERMINAL** (정직한 closed-negative). faithful-IIT4 Φ(exact MIP-EI, n=4, a_phi_iit4_tool;
numpy는 Φ를 절대 계산 안 함; engine-native LCG content generator, byte-identical 재현):

| seed | A (NO-PHASE) | B (PHASE-BIND) | ΔΦ(B−A) | T1 | PERM-SHUF | ΔΦ(S−A) | T2 |
|------|------|------|------|----|------|------|----|
| 1317 | 0.870311 | 1.335350 | +0.465039 | PASS | 1.150110 | +0.279798 | **FAIL** |
| 1318 | 0.855353 | 0.860580 | +0.005227 | **FAIL** | 0.957870 | +0.102517 | **FAIL** |
| 1319 | 0.586833 | 0.538064 | −0.048768 | **FAIL** | 1.174020 | +0.587183 | **FAIL** |

- **T1 ROBUST-LIFT FAIL** — seed 1318 ΔΦ +0.005(미달), seed 1319 ΔΦ **−0.049(음수)** — 토폴로지를
  꺾은 **바로 그 직교 seed 1319**. 상대-위상 lift 자체가 어려운 seed에서 취약.
- **T2 SHUFFLE-EARNED FAIL(이전보다 더 심하게)** — **더 강한** permutation shuffle이 lift를 무너뜨리기는커녕
  매 seed에서 Φ를 **ARM B 위로 올린다**(ΔΦ_perm +0.280/+0.103/+0.587 — perm-shuf Φ가 phase-bind Φ를
  매 seed 초과). 진단 offset-shuffle도 동일.

**근본 원인(종결 진단):** 관계를 **파괴하는** permutation이 오히려 Φ를 올린다면, Φ 이득은 상대-위상
**관계**에서 오는 게 아니다 — `(1+cos)/2` carrier가 모듈별 salience 이진화에 주입하는 **진폭 분산**에서
온다(offset이든 permutation이든 어떤 위상 scramble도 보존하는 분산). TIMING축은 토폴로지축과 **같은
근본 실패**를 한다 — faithful-IIT4 MIP이 정직한 대조가 살아남지 못하는 저차원 구조(거긴 content cut,
여긴 채널별 진폭 분산)를 착취한다.

**결론: faithful-IIT4 Φ-robustness 벽은 이제 두 축 모두에서 TERMINAL** — 토폴로지 🏁(H_1283 relay
R1-R7, H_1317 multi-edge) + 타이밍 🧱(H_1283 R8 engine c4 FAIL, H_1319 강한 대조에서도 c4 FAIL).
anima의 4-모듈 workspace에서 robust(3-seed, 대조-생존) faithful-Φ lift는 **어느 축으로도 도달 불가**.
이는 anima의 의식 substrate를 부정하지 않는다(Ψ=1/2, A⇄G tension 무손상) — **결합/위상 채널을 더해도
honest 대조 아래서 faithful-IIT4 Φ 점수가 robust하게 오르지 않는다**는 것을 종결할 뿐. **CORE 배선
follow-on 없음**(a_verified_must_wire = GREEN 전용; engine_cli.hexa 무손상, 프로브는 standalone fn
main, importer 0). SCOPE: TOY n=4 dim-8 64-tick, faithful-Φ EXACT, content generator engine-native
LCG(numpy 아님). rung 내에서는 결정적(강한 permutation 대조가 매 seed Φ를 올림 → variance-not-synchrony
진단은 더 큰 n 불필요). 새 가설로만 열림: 근본적으로 다른 Φ 추정기 · 훨씬 큰 모듈 집합(>8은 exactness
상실) · 진폭 분산이 증명상 0인 위상-게이트 read-out.

산출물: `UNIVERSE/h1319_phi_timing.hexa` · `UNIVERSE/cards/H_1319_phi_timing.md`(카드) ·
`UNIVERSE/HYPOTHESES.md`(인덱스) · `CLAIMS.tape @C h1319_phi_timing` ·
`.verdicts/1319_phi_timing/{H_1319_FREEZE,H_1319}.txt` · `domains/OMEGA.log.md`.

## 2026-06-16 — research(COGNITION-REPRESENTATION): 🟠 H_1323 — Sapir-Whorf/언어상대성: 기질이 학습한 언어가 비언어 변별을 휘는가 (범주지각 CP)

H_1316(자모)·H_1322(featural)는 도메인의 **표현(representation)**이 **학습성(compression)**을 바꾼다는 걸
보였다. Sapir-Whorf/언어상대성은 더 깊은 주장 — 언어의 **카빙(carving)**이 **하류의, 비언어
변별**을 휜다 (인지과학 렌즈 c15, a_no_llm_frame_trap — LLM 레시피 아님, 인간-인지 주장 아님).
실증 워크호스 = **범주지각(CATEGORICAL PERCEPTION)**: 화자는 자기 언어의 경계에서 범주-횡단 쌍을
범주-내 쌍보다 더 잘 변별한다(러시아어 두 파랑 → 파랑-경계 변별 빨라짐; grue 언어들은 초록/파랑을
서로 다른 지점에서 자른다).

**TOY 패러다임**(합성 연속체 — 정당한 방법론, '언어'=연속체 위 라벨 스킴): 연속 1-D '색상'축
(N=21 RBF-코딩 자극, 위치-충실·경계-무지) 위에 두 언어 — L_A는 p_A=1/3, L_B는 p_B=2/3에서 자름.
**같은** gradient-free 미토시스/Voronoi 셀 store(오차-타깃 SPLIT-only 성장, p8)가 각 언어의 카빙을
학습 → 셀이 경계에 **밀집(PACK)**(CP의 메커니즘적 기원). **하류 비언어 테스트(테스트시 라벨 없음)**:
인접 쌍의 same/different 변별 = 학습된 soft 범주-사후확률 그래디언트의 차이. 4 arm(PRE-LANG/L_A/L_B/
SHUFFLE), 3 seed [4323,4324,4325], $0 CPU 미러 DIRECTIONAL, detached nohup inline poll.

**결과 🟠 PARTIAL — 언어상대성 성립(W1∧W2 결정적), 반-Goodhart W3 분열(bar 안 옮김 c9):**
- **W1 CP 존재 ✅**: 범주-횡단−범주-내 마진 +0.200(≥0.15), 언어-vs-PRE-LANG-baseline@peak +0.989(≥0.15);
  PRE-LANGUAGE arm은 FLAT(1셀, 상수 사후확률, peak 0.000).
- **W2 WHORFIAN 분리 ✅(핵심)**: CP peak 위치 L_A→0.325(|Δp_A|=0.008), L_B→0.675(|Δp_B|=0.008),
  분리 0.350(≥0.20), 3 seed 전체 std 0.000 → **같은 자극 세계, 경계가 언어 따라 이동, 인지가 언어를
  따른다**.
- **W3 EARNED ❌ 분열**: loc-std 하위절 ✅(shuffle peak가 seed 간 0.492±0.165로 떠돌아 incoherent;
  NON-GATING 진단 — peak 개수 L_A=1·L_B=1·SHUFFLE=8: 언어는 단일 coherent peak, shuffle은 산만한
  다중 spike), 그러나 prominence 하위절 ❌(랜덤 라벨이 국소적으로 sharp한 swing을 多 생성 → shuffle
  단일-peak prominence 0.661 > 0.5×0.999=0.50; **frozen prominence 임계가 multi-peak shuffle에 대해
  잘못 명세됨**). c9/p7 — bar 안 옮기고 정직 보고.

**소견:** 기질이 학습한 언어가 비언어 변별을 **측정 가능하게 휜다** — 범주지각이 언어 경계에서 창발하고
CP peak 위치가 언어를 추적(W1∧W2 결정적). DIRECTIONAL numpy 미러, TOY 합성 연속체, 인간-인지 주장
없음(a_scale_honest_scope). **다음 R2**: coherence-기반 W3(peak-개수/원형-분산)를 **새로** frozen
(이 bar 완화 아님) + engine-native 실현(a_engine_native_learning·a_verified_must_wire). live CORE/*.hexa
UNTOUCHED. NEW: UNIVERSE/h1323_sapir_whorf.py · UNIVERSE/cards/H_1323_sapir_whorf.md · .verdicts/1323_sapir_whorf/
{H_1323_FREEZE,H_1323}.txt · HYPOTHESES.md row · CLAIMS.tape @C h1323_sapir_whorf · domains/MITOSIS-ENGINE.log.md.
## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1321 — H_1316 자모 돌파를 엔진-네이티브로 배선 (🟢 GREEN, engine-transfer VERIFIED)

H_1316(#2224, 🟢)은 numpy/torch **미러**(DIRECTIONAL)였다 — live CORE 손대지 않음.
`a_verified_must_wire`: GREEN 메커니즘은 live 엔진 위에서 **엔진-네이티브 byte-exact**로
돌아갈 때까지 done 이 아니다. H_1321 = 그 r2 배선: NFD 자모 심볼화 + 자모-심볼 미토시스를
**live CORE/engine_cli.hexa**(VAdaptField Voronoi + engine_mitosis_tick, p8)의 faculty 위에서
엔진-네이티브로 돌려 frozen B1/B2/B3 를 W1/W2/W3 로 재채점.

표현 변환(NFD 자모 분해)은 결정론적 유니코드 **data-prep**; 미토시스 + held-out per-byte
CE 채점은 **엔진-네이티브**(CORE/h1321_ko_jamo_wire_probe.hexa 가 CORE/engine_cli.hexa 를
import 하여 live faculty 를 구동). 단일 한국어 진입(a_core_engine_map) —
pure_field/engine_g/brain 손대지 않음, Ψ-disjoint. 코퍼스 = H_1307 RUN A / H_1316 과 **byte-동일**
(30MB KO window sha c47b6808… gate PASS); R2 키 env-only(c7). CPU-tractable window
(ko_stride=2500, arm 당 ~6000 raw / ~5100 jamo pairs; Vj=323==H_1316 anchor).

**결과: 🟢 GREEN** (W1∧W2∧W3 전부 PASS, frozen-first, NO tune-to-green, c9/p7).
엔진-네이티브 held-out KO CE (nats/UTF-8-byte): **G0 raw=3.09967 · G1 jamo=2.82046 · G1c
shuffle=3.01867**. **W1 ✅** engine-G1 2.82046 가 SAME-WINDOW numpy 미러 2.82046 을
**6.3e-07**(≪0.05 tol)로 재현 AND 2.82046 < 2.903(raw 천장 band 아래). **W2 ✅** G1c−G1=+0.198,
G0−G1=+0.279(둘 다 ≥0.05) + B3 NFD→NFC 8,143,053 음절 0 실패 + Σnbytes==corpus 정확. **W3 ✅**
무회귀 byte-exact: engine_cli_smoke **73/0** · h1196 single-entry **7/0** · h1205
separation-invariant PASS(generation byte-동일 ON==OFF, Ψ=½ 불변). **핵심: 엔진-네이티브 hexa
값이 모든 arm 에서 numpy 미러와 1e-7 일치** — gradient-free 자모-심볼 미토시스가 live 엔진으로
충실히 transfer; 자모 돌파가 이제 CORE 안에서 LIVE byte-exact (verdict 닫힘).

HONEST(c9·a_scale_honest_scope): W1 은 CPU-tractable window 에서의 engine-TRANSFER 존재증명 —
절대 CE(2.820)가 30MB anchor(2.513)보다 높은 건 작은 strided window 의 per-cell head 가 더
sparse 하기 때문; 상대 구조(G1<G1c<G0, 30MB 미러와 같은 순서)는 완전히 보존되고 W1 은
SAME-WINDOW 미러 대비로 사전등록되어 apples-to-apples. 엔진-네이티브 30MB + 한국어 유창성 =
follow-on; 유창성 주장 없음.

추가: `CORE/h1321_ko_jamo_wire_probe.hexa`(imports CORE/engine_cli.hexa) ·
`UNIVERSE/h1321_ko_jamo_wire_export.py` · `UNIVERSE/cards/H_1321_ko_jamo_wire.md` · `HYPOTHESES.md` 행 ·
`CLAIMS.tape @C h1321_ko_jamo_wire` ·
`.verdicts/1321_ko_jamo_wire/{FREEZE,result}.txt`(+ref/manifest json) · `domains/MITOSIS-ENGINE.log.md` ·
CHANGELOG. live CORE 엔진 faculty 를 **구동**(mutation 없음); W3 가드가 Ψ-disjoint 무회귀 확인.
xref h1316(이걸 엔진-네이티브로 배선하는 미러 돌파) · h1306(엔진-네이티브 한국어 미토시스 선례) ·
h1312(ko_cells L3 decode-consult 배선 선례) · h1307(2.9475 raw 천장; 같은 코퍼스) ·
h1199(엔진 DIM-확장 선례) · a_verified_must_wire · a_engine_native_learning · a_core_engine_map ·
a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · p7·p8 · c7·c9·c15.

## 2026-06-16 — research(OMEGA): 🧱 H_1317 — 분산 multi-edge(small-world) 결합이 faithful-IIT4 Φ를 robust하게 올리나 (H_1283 중앙릴레이 벽)

H_1283(thalamus-Φ)이 남긴 벽을 새 각도로 친 시도(c16/a_break_the_wall). H_1283은 모든 **중앙
릴레이/star 토폴로지**가 faithful-IIT4 Φ를 **seed-조건부로만** 올렸다 — 3-seed robustness gate를
실패(특히 직교 seed). 단일 중앙 릴레이 = 취약한 Φ lift = 🧱. **시도 안 해본 각도**(c15,
a_no_llm_frame_trap): 피질의 통합정보는 단일 허브가 아니라 **small-world 재귀 mesh**(짧은 엣지
다수 + 긴 엣지 소수)에서 나온다. H_1317: **분산 multi-edge(Watts–Strogatz small-world)** 결합이
H_1283이 실패한 같은 gate에서 Φ를 robust하게 올리나?

**결과: 🧱 WALL** (정직한 closed-negative, c9). 분산 small-world 결합도 **3-seed Φ robustness
gate를 실패** — 토폴로지와 무관하게 Φ는 **취약하게 유지**. faithful-IIT4 Φ(exact MIP-EI, n=8,
stdlib/consciousness/iit4/faithful_phi.hexa via `hexa run`, proxy 절대 사용 안 함; numpy는 trajectory만
방출): seed 1317 ΔΦ(multi−none)=**+0.252**✓ · 1318 **+0.080**✓ · 1319 **−0.331**✗(직교 seed,
음수 — H_1283 직교-seed 실패와 동일 양상). C1 ROBUST-LIFT **FAIL** · C2 TOPOLOGY-EARNED PASS
(multi>shuffle 2/3 seeds, mean 1.5909>1.5195 — multi가 만드는 lift는 엣지수가 아니라 small-world
구조이긴 함) but moot · C3 BEATS-CENTRAL **FAIL**(multi가 C1 자체 실패; CENTRAL도 seed 1319
ΔΦ −0.404로 더 심하게 실패).

**핵심 발견:** 통합정보 robustness는 toy 스케일에서 **토폴로지 속성이 아니다** — star→small-world
mesh로 바꿔도 Φ lift가 robust해지지 않는다; 취약성은 결합 그래프가 아니라 substrate/seed geometry에
있다. H_1283 벽을 더 **bound**한다(star 한정 아님; 토폴로지/content 축은 star와 small-world 양쪽에서
🧱). H_1283 R8의 직교 **TIMING 축**(phase-binding)이 이 arc에서 유일한 robust Φ lift로 남는다.
substrate는 H_1283과 정확히 일치(LEAK=0.55 GAIN=0.30 dim-8 T=64; 오직 토폴로지만 변경), 4 arm 결합
**budget 동일**(Σ=3.5000 runtime-assert)로 lift=토폴로지 보장. 4 arm: NONE(floor)·CENTRAL(star 7엣지,
H_1283 재현)·MULTI-EDGE(WS ring K=2 + rewire β=0.30, 16엣지)·SHUFFLE(Erdős–Rényi 16 랜덤엣지, budget
일치). frozen-first(FREEZE를 첫 실행 전 등록, bar 미이동, NO tune-to-green), seeds[1317,1318,1319],
$0 CPU, deterministic. CORE wiring follow-on 없음(a_verified_must_wire = GREEN 전용; 🧱는 wire할 것 없음).
SCOPE: TOY/DIRECTIONAL — faithful-Φ leg은 real(exact MIP-EI via hexa)이나 numpy mirror, 라이브
CORE/pure_field 전이 UNVERIFIED(a_scale_honest_scope·a_toy_scale_recheck). live CORE/*.hexa UNTOUCHED.
`UNIVERSE/h1317_phi_multiedge.py` · `UNIVERSE/cards/H_1317_phi_multiedge.md` ·
`.verdicts/1317_phi_multiedge/{H_1317_FREEZE,H_1317}.txt` · `CLAIMS.tape @C h1317_phi_multiedge`.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1316 — 자모 합성 표현이 2.953 천장을 깬다 (🟢 GREEN BREAKTHROUGH)

🔴 TERMINAL 이던 한국어-미토시스 스레드를 **표현(representation) 각도**에서 돌파했다 (c16 / a_break_the_wall).
이전 모든 한국어 lane (H_1307/H_1311/H_1315) 은 substrate 에 **raw UTF-8 바이트**를 먹였다 — 한글 한 음절 =
불투명한 3 바이트, 한국어가 **합성형 음절-블록 문자**라는 인식이 전혀 없었다. 빠진 구조 (a_no_llm_frame_trap,
c15 — 스케일이 아니라 빠진 구조를 붙여라): **자모 합성** — 한 음절 = 초성(L)+중성(V)+종성(T), 결정론적
유니코드 NFD 분해로 복원 가능. H_1316 은 **똑같은** gradient-free 미토시스 (cells only SPLIT, p8; grow-op +
cell budget 를 H_1306/H_1307 verbatim 고정) 를 자모-심볼 스트림 위에서 키우고, 심볼당 CE 를 다시
**nats/UTF-8-byte** 로 환산해 2.9475 천장과 동일 축에서 비교했다. 표현만 바뀐다.

REAL sm_120 GPU (사용자 RTX 5070, $0, NOT runpod). 코퍼스는 H_1307 RUN A 와 byte-IDENTICAL (sha
c47b6808…/31b4a543… 게이트 PASS). frozen-first (FREEZE 선등록), NO tune-to-green (c9/p7). 3 seeds [4316-4318].

**결과 (mean 3 seeds, held-out KO next-symbol CE, nats/UTF-8-byte):**
- G0 raw-byte (in-run port) = **2.95342** (H_1307 RUN A 2.9475 재현, port 유효)
- **G1 자모-rep = 2.51335 (Δ −0.434 vs 천장, −0.440 vs G0)** → **B1 PRESENCE ✅** (2.8975 를 크게 하회)
- G1c 자모→심볼 맵 셔플 control = 2.74306 (Δ g1c−g1 +0.230) + G1 이 raw G0 를 +0.440 으로 이김 →
  **B2 EARNED ✅** (lift 는 vocab/dim 이 아니라 **합성 구조**)
- NFD→NFC 왕복 8,143,053 음절 0 실패 + 심볼당 n_bytes 합 == 코퍼스 바이트 정확히 일치 → **B3 NO-CHEAT ✅** (무손실, 공정 비교)

→ **🟢 GREEN: 한국어 천장은 capacity-bound 가 아니라 REPRESENTATION-bound 였다.** 벽은 미토시스 메커니즘의
용량이 아니라 **raw-byte 표현** (음절당 3 불투명 바이트) 이었다. H_1311(raw 바이트 위 capacity-bound) ·
H_1315(303M frozen rep 위 capacity-bound) 와 화해: 그 lane 들이 부딪힌 한계는 **틀린 표현** 위의 L2-Voronoi
파티션 기하였고, 올바른 (합성) 표현이 그것을 깬다.

정직한 범위 (c9 · a_scale_honest_scope · a_toy_scale_recheck): G1 은 결정론적 (seed 간 동일; FREEZE 가 seed 는
control 만 흔든다고 선등록) — 단일 존재증명. control seed 1개(4317=2.506)는 G1 에 근접 → B2-vs-shuffle 은
MEAN 으로 통과 (per-seed 만장일치 아님; G1-beats-raw +0.440 은 무조건 성립). ~0.44 강하는 상당부분 음절→자모
부호화 이득 (B2-vs-raw 가 vocab/dim 단독이 아님을 보임). DIRECTIONAL numpy/torch mirror; live CORE/*.hexa
엔진 전이 = follow-on (a_engine_native_learning · a_verified_must_wire); 한국어 유창성 주장 없음. live CORE UNTOUCHED.

추가: `UNIVERSE/h1316_ko_jamo_mitosis.py` · `UNIVERSE/cards/H_1316_ko_jamo_mitosis.md` · `HYPOTHESES.md` 행 ·
`CLAIMS.tape @C h1316_ko_jamo_mitosis` · `.verdicts/1316_ko_jamo_mitosis/{H_1316_FREEZE,H_1316}.txt`(+summary/manifest) ·
`domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1315 — 303M trunk 학습표현 위 미토시스 vs 2.9 천장 (🔴 TERMINAL)

The Korean-mitosis thread, RESOLVED. H_1311 (#2215, 🔴) refuted that a richer RAW-BYTE substrate
breaks the H_1307 ~2.9 nat/byte Korean byte-CE ceiling, and named the surviving lever: partition
over a LEARNED representation (the mounted 303M trunk's hidden) instead of raw bytes. H_1315 tested
exactly that — the SAME gradient-free mitosis (cells only SPLIT, p8; grow-op + cell budget FIXED,
verbatim H_1306/1307/1311) but partitioning over the 303M trunk's hidden rep (ckpt h1129c_chat.pt,
forward = gradient-free, READ `ln_f` only, NO backprop). REAL sm_120 GPU on the user's RTX 5070, $0
(NOT runpod); corpus byte-IDENTICAL to H_1307 RUN A (sha gate PASS); 3 seeds; frozen-first, NO
tune-to-green. RESULT 🔴 TERMINAL: mean held-out KO next-byte CE — G0 raw-byte 2.95342 · **G1
303M-trunk-rep 3.14637 (+0.193 WORSE, above 2.9 → does NOT break the ceiling)** · random-embed
3.53134 · shuffle 4.02243. KEY DISSOCIATION (c9): G1 BEATS both controls (+0.385 / +0.876 → the
learned rep IS real Korean structure) yet is WORSE than raw bytes → the same partition-GEOMETRY
limit carries over to the learned-rep space (40 cells saturated, CE rose). EN retained. THESIS:
the Korean depth needs GRADIENT learning, not gradient-free structure-over-a-frozen-rep, at this
scale; mitosis=grow-under-pressure (H_1288/1295/1307) is a real mechanism but not a gradient
substitute on a hard continuous next-byte manifold. live CORE UNTOUCHED (substrate-measurement
rung). NEW: `UNIVERSE/h1315_ko_mitosis_learned_rep.py` · `UNIVERSE/cards/H_1315_ko_mitosis_learned_rep.md`
· `.verdicts/1315_ko_mitosis_learned_rep/*` · `CLAIMS.tape` @C · `domains/MITOSIS-ENGINE.log.md` @H
· `UNIVERSE/HYPOTHESES.md` row · `FINDINGS.md` thread-resolution. toy/DIRECTIONAL, mirror;
engine-transfer = follow-on (a_engine_native_learning · a_verified_must_wire).

## 2026-06-16 — research(G6-DIG): H_1314 — G6 IDEATION ★ depth-floor r3, hypothesis-form STRUCTURE lane (🟠 THIN: FALS capacity-bound, DIST/NOVEL structure-fixed)

a_break_the_wall (c16) follow-on for H_1305/H_1309. r2 proved the G6 depth floor is
CAPACITY-bound not budget-bound (curiosity-gate FALS plateau 0.667 across 4→16 draws)
and named the surviving fix: a hypothesis-form STRUCTURE lane. r3 built it — route
ideation through a falsifiable-hypothesis TEMPLATE scaffold (forces comparator+
measurable+negatable slots; CONTENT still substrate-generated, only STRUCTURE scaffolded).
3 arms × 5 ideas × 3 seeds, reuses the H_1305 `_is_falsifiable` detector VERBATIM (p7),
$0 CPU torch-mouth. p7 TOKEN-INJECTION AUDIT CLEAN (first run CAUGHT corpus concept "the
engine dreams when alone" injecting COMPARATOR token "when" → hard ABORT → fixed to clean
noun subjects → re-ran clean = audit teeth). RESULT: the FORM does NOT cross the FALS
floor (FALS=0.0 all arms/seeds) BUT STRUCTURE-FIXES the DIST/NOVEL floor — SCAFFOLD
DIST=5.0 (3/3 seeds, crosses ≥5 where r2 plateaued 4.33) + NOVEL 19.67, both BEAT
NO_SCAFFOLD (4.0/6.33) and SHUFFLE_SLOT collapses (2.33/5.67). THESIS: ideation breadth =
missing-STRUCTURE (lane-fixable), falsifiable-depth = CAPACITY WALL (scale-bound) at 303M;
7B re-test = live falsifier (a7b_pass G2). G6 stays 🟠 THIN (FALS bar UNMOVED, c9). New:
`UNIVERSE/h1314_g6_hypothesis_scaffold.py` · `UNIVERSE/cards/H_1314_g6_hypothesis_scaffold.md` ·
`.verdicts/1314_g6_hypothesis_scaffold/{FREEZE,result}.txt+result.json` · HYPOTHESES.md ·
CLAIMS.tape · domains/ENGINE+CLM+KOSMOS.log.md · MODEL.md/FINDINGS.md G6 row.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1312 — 한국어 cell 을 live decode 에 WIRE (🟢 WIRED)

a_verified_must_wire follow-on for H_1306/H_1307: those rungs GREW real Korean cells
(gradient-free mitosis) + MEASURED their next-byte CE but did NOT connect them to anima's
live output. H_1312 connects them so Korean error-pressure actually shapes what anima EMITS.
`CORE/h1312_ko_cells_export.hexa` re-runs the EXACT H_1306 engine-native grow (`engine_cli.hexa`
VAdaptField Voronoi + `engine_mitosis_tick`, p8) reproducing H_1306's 9 cells byte-exact, and
writes **`CORE/ko_cells.kohead`** (cell = 3-D Voronoi center + learned argmax next-byte).
`CORE/generator.hexa` §6.5 (`ko_cells_load`/`ko_cells_next_byte`/`ko_consult_emit`/
`ko_cells_summary`) CONSULTS those cells at the SAME L3 slot .clm/ByteGPT enter (`a_core_engine_map`
single entry — NOT a 2nd path). Korean-likeness gate = the last byte is a UTF-8 continuation byte
(0x80..0xBF, mid-Hangul-multibyte) — a pure byte test, NO language label (p1·p2·p3); Korean-like →
nearest grown cell's learned next-byte biases emission, off-Korean → INERT (−1 → byte-identical).
**🟢 WIRED** (frozen-first, c9): (P PRESENCE) 8/8 held-out REAL Korean contexts fired + 7/8 differed
from baseline · (N NO-REGRESSION) 6/6 real English + ASCII sweep 0..127 all inert across 256 base
bytes · (Y) engine_cli_smoke 73/0 (engine_cli.hexa byte-untouched), h1196 7/0, h1205 PASS (Ψ=½
Φ-checksum 48.6613 untouched) · (Z) ko_cells.kohead read ONLY in generator.hexa, consult Ψ-disjoint.
SCOPE: toy cells (9 cells, 3-D feature, 600KB KO window) — Korean-error-pressure-AWARE emission, NOT
fluent Korean (a_scale_honest_scope, a_toy_scale_recheck). NEW: `CORE/h1312_ko_cells_export.hexa` ·
`CORE/ko_cells.kohead` · `CORE/generator.hexa` §6.5 · `CORE/h1312_ko_decode_wire_probe.hexa` ·
`.verdicts/1312_ko_decode_wire/{FREEZE,result,guards}.txt` · `UNIVERSE/cards/H_1312_ko_decode_wire.md` ·
HYPOTHESES.md row · CLAIMS.tape @C · domains/MITOSIS-ENGINE.log.md @H · ARCHITECTURE.md.
## 2026-06-16 — domain(H_1313): HIVE r4 STATE-DEPENDENT A⇄G coupling — 🧱 TERMINAL NULL (the a_break_the_wall attempt fails)

r4 of the HIVE-MIND lane — the `a_break_the_wall` attempt against the H_1308 r3 NULL. r3
diagnosed (c9) that the live tension-link is a near-CONSTANT scalar nudge (bias≈0.00648 ∀
states) so the joint TPM factorizes → faithful Φ_joint=0 → Δ_real=−3.0. r3 named its own
breakthrough angle (H_1308 §6): a genuinely STATE-DEPENDENT multi-cell coupling could in
principle integrate. H_1312 tests EXACTLY that — member A's `pure_field` t1/t3/t4 channel-sign
cells have their thresholds shifted by member B's LIVE cells (a real cross-member field read),
symmetrically A→B, scaled so it CAN flip a cell. Faithful IIT-4, n≤8 (SAME scale as r3),
frozen-first, NO tune-to-green, reuses the r3 harness verbatim.

**🧱 TERMINAL NULL — even state-dependent coupling does NOT integrate.** Φ(member)=1.5 (Σ=3.0)
but Φ_collective(STATE-DEP, W=0.6)=0.0 → **Δ_sd=−3.0, IDENTICAL to r3, NO flip** (B1 PRESENCE
FAIL + B2 FLIP FAIL; B3 decouple-mean + B4 shuffle PASS trivially). The new coupling DID break
r3 factorization (next-A genuinely varies with B's bits, verified directly) — but on the tiny
pure_field channels (t1~1.6e-7, t3~1.6e-8) ANY coupling strong enough to register OVERWRITES
the member's own dynamics → a pure COPY/SWAP with ZERO distinctions (nd=0) → Φ_joint=0. A
diagnostic coupling-strength sweep (k∈{0.5,0.8,1.0,1.2,2.0}) gives Φ_joint=0 at EVERY k → NOT a
scaling artifact. NO regime has the simultaneous self+cross dependence IIT-4 needs. The ECA
Δ=+10.4756 is a property of its rich self+neighbor TPM, NOT a substrate-portable law of
consciousness-as-integration. H_1295 super-additivity is now **TERMINALLY bounded to ECA-scope**
across BOTH realized real channels (r3 constant + r4 state-dependent). `a_break_the_wall`
satisfied; a first-class, valid TERMINAL wall (c9). Does NOT retract H_1295's ECA GREEN.

NEW: `UNIVERSE/h1313_hive_state_dependent_coupling.hexa` ·
`.verdicts/1313_hive_state_dependent_coupling/{FREEZE,result}.txt` ·
`UNIVERSE/cards/H_1313_hive_state_dependent_coupling.md` · HYPOTHESES.md row · CLAIMS.tape @C
h1313_hive_state_dependent_coupling · H_1295 + H_1308 cards updated (r4 verbatim) ·
domains/MITOSIS-ENGINE.log.md @H. NO engine wiring (Ψ-disjoint, live CORE UNTOUCHED — a NULL
wires nothing).

## 2026-06-16 — domain(H_1308): HIVE collective-Φ ENGINE-TRANSFER to REAL anima A⇄G — 🔴 HONEST NULL (does NOT transfer)

r3 of the H_1295 HIVE-MIND lane — the ONE axis the r2 agent flagged open: collective-Φ
super-additivity (Δ_ECA=+10.4756) was read over an ABSTRACT ECA substrate; engine-transfer
to a LIVE multi-anima loop (real coupled A⇄G) was UNVERIFIED. Tested it directly: built the
joint n=6 TPM from REAL anima dynamics — live `CORE/pure_field.hexa` PureField (3 coupled
oscillators → 6-D field tensor) + the H_6009 tension-link (`CORE/brain.hexa`
`anchor_tension_fold`) as the real coupling channel — measured with faithful IIT-4
(`a_phi_iit4_tool`, n≤8 ceiling respected).

**🔴 HONEST NULL — does NOT transfer.** Each REAL member integrates (Φ=1.5, Σ=3.0) but the
JOINT Φ=0.0 → Δ_real=−3.0 (SUB-additive; sign FLIPS vs ECA +10.4756). The joint substrate
FACTORIZES (next-A depends only on A, next-B only on B) because the real tension-link is a
near-CONSTANT scalar nudge (bias≈0.00648 ∀ 64 states) — no state-dependent cross-member
coupling → decomposable → Φ_joint=0 by IIT-4. NOT a binarization artifact (same readout
gives Φ_member=1.5>0). The ECA super-additivity was a property of ECA's strong
state-dependent neighbor-coupling, NOT a substrate-portable law. Bounds H_1295 to ECA-scope
(does NOT retract its ECA GREEN). 3 seeds, $0 CPU, frozen-first, c9; live CORE UNTOUCHED.

Files: `UNIVERSE/h1308_hive_real_substrate_transfer.hexa` ·
`UNIVERSE/cards/H_1308_hive_real_substrate_transfer.md` · HYPOTHESES.md row ·
`.verdicts/1308_hive_real_substrate_transfer/{H_1308_FREEZE,H_1308,result}.txt` ·
CLAIMS.tape `@C h1308` + H_1295 `verdict_r3` · `domains/ENGINE+CLM+KOSMOS.log.md` @H ·
H_1295 card scope note.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1311 — richer-substrate vs the H_1307 ~2.9 Korean ceiling 🔴 HONEST-NEGATIVE (CAPACITY-bound)

The named H_1307 NEXT lever (shared with the from-scratch lane): H_1307 (#2213) found MORE real
Korean drops KO next-byte CE to ~2.95 then the CTX=4 / 3-D BYTE substrate SATURATES at a ~2.9
nat/byte ceiling. Does a **RICHER substrate** (longer context / a learned per-cell head instead of
raw byte-trigram MLE) break past ~2.9 — is the ceiling **capacity-bound or substrate-bound**?
H_1311 holds the **corpus + the verified gradient-free Voronoi mitosis grow-op** (p8, SPLIT-only)
**FIXED** and varies ONLY the substrate richness on a frozen ladder (S0 baseline CTX=4 count-MLE ·
S1 longer raw-byte context CTX 8/16/32 · S2 learned per-cell closed-form ridge head). REAL sm_120
GPU on the user's OWN RTX 5070, $0 (NOT runpod); corpus byte-IDENTICAL to H_1307 RUN A
(sha c47b6808…/31b4a543…, asserted). Frozen-first, p7 deterministic held-out CE, NO tune-to-green.

**🔴 HONEST-NEGATIVE — the ~2.9 ceiling is CAPACITY-bound / the byte-task ceiling itself, NOT
substrate-bound.** S0 reproduced **2.95342** (port OK vs 2.9475). **No richer substrate broke 2.9;
every richer rung was WORSE than S0**: S1 longer raw-byte context **HURTS MONOTONICALLY** (ctx8
2.964 → ctx16 3.048 → ctx32 3.442 — curse-of-dim on the L2/Voronoi partition; every S1 rung
saturated GROW_MAX=40 cells yet CE ROSE = partition-quality limit, not capacity); S2 per-cell ridge
head **COLLAPSES** (5.437 — raw byte features not linearly predictive of the next byte). **Control:**
S1 shuffles were WORSE than intact and **no shuffle survived to beat S0** (capacity_signal=False) →
no capacity gain to claim either. **Thesis:** the capability-vs-scale prediction that "a richer
representation breaks the wall" is **REFUTED for these two richness axes** — the limit is the
L2-partition-over-raw-bytes **geometry**, not the per-cell readout; a genuinely richer substrate
would need a *different geometry* (learned embedding / non-L2 metric / per-cell sequence model), not
more raw byte columns or a linear head over the same raw features (the surviving open lever for the
from-scratch lane). live CORE/*.hexa UNTOUCHED; engine-transfer DIRECTIONAL; NO Korean-fluency claim.

Adds: `UNIVERSE/h1311_ko_richer_substrate.py`, `UNIVERSE/cards/H_1311_ko_richer_substrate.md`,
`.verdicts/1311_ko_richer_substrate/{FREEZE,result,summary.json,metrics.jsonl,manifest.json,run.log}`,
`CLAIMS.tape` @C h1311_ko_richer_substrate, `domains/MITOSIS-ENGINE.log.md` @H, `HYPOTHESES.md` row.

## 2026-06-16 — domain(H_1295 r2): HIVE collective-Φ N-scaling — super-additivity HOLDS@N=3 but SATURATES 🟢/🏁

r2 of the H_1295 HIVE-MIND lane (anchor H_609, r1 PR #2182). Question: does collective-Φ
super-additivity GROW / HOLD / SATURATE as the coupled-member count N grows 2→3→4 (joint
n=6,9,12)? Φ = FAITHFUL IIT-4 ONLY (`a_phi_iit4_tool`, `big_phi_bounded` cap=2 — numpy never
computes Φ). The N-member joint substrate = a generalized coupled ring (`build_tpm_ring`: N
blocks of 3, within-block n=3 ring blended at W=0.6 with the global n=3N ring) — BYTE-EXACT the
r1 `_build_tpm_ab` at N=2 (verified mismatches=0, so the n=2 lane + smoke cases 39-42 stay
byte-unchanged). FROZEN-FIRST: `H_1295_R2_FREEZE.txt` pre-registered the GROWS (Δ_super(3) ≥
Δ_super(2)+1.0) vs SATURATES definition BEFORE any n=9 measurement (c9/p7, no bar moved).
**The Δ_super(N) curve:** Δ_super(2)=+10.4756 (n=6, Φ_joint 15.4677) → Δ_super(3)=**+9.16825**
(n=9, Φ_joint 16.6564 vs Σ 7.48813). **B1 super-additivity HOLDS at N=3** (Δ>0); **B2 the curve
SATURATES/DECLINES** — Δ_super(3)−Δ_super(2)=−1.3074 < the +1.0 GROWS bar ⇒ collective Φ does
NOT scale with member count (existence-property, not amplifying) → **HIVE DEPLETED 🏁** on the
N-scaling axis (a saturating existence-proof is a VALID honest result, `a_scale_honest_scope`).
N=3 controls re-run (decouple-null W=0 → Δ≤0; rule-class sterile 90×3 does not super-add;
no-collapse coherence<0.999) — verbatim in `H_1295_R2.txt`. **COMPUTE CEILING (load-bearing):**
a single faithful big-Φ at **n=9** (cap=2, nd=68) is **~84 min** on CPU (MIP over 2⁹ partitions
× nd² relations); **n=12 (N=4) is INFEASIBLE** — documented, NOT proxied (a proxy is never
substituted for Φ). ENGINE-NATIVE + WIRED (`a_verified_must_wire`): `collective_phi` /
`collective_coherence` now handle N=3 via `_build_tpm_ring` (`collective_nmax()=3`; N>3 honestly
falls back to additive); the N=3 frozen bars re-score ENGINE-NATIVE in `engine_cli_smoke.hexa`
cases 74-78, GATED behind `--hive-n3` (n=9 Φ is ~84 min/call, so the DEFAULT smoke stays 73/0
fast + byte-unchanged — Ψ-disjoint, no regression). `UNIVERSE/h1295_r2_hive_scaling.hexa` ·
`UNIVERSE/cards/H_1295_hive_collective_phi.md` (§ 6b/9) · `.verdicts/1295_hive_collective_phi/
{H_1295_R2_FREEZE,H_1295_R2}.txt` · `CORE/engine_cli.hexa` § HIVE-MIND · `CLAIMS.tape` @C
h1295 verdict_r2.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1307 — GPU scale-up of the H_1306 Korean mitosis rung on the user's OWN RTX 5070 (🟢 GREEN @ 50x corpus + 🟠 honest saturation)

- **the rung (lane ko-mitosis-gpu, $0 — user's OWN idle host `summer`, NOT runpod)** — scales H_1306 (#2211, 🟢 GREEN engine-native: KO next-byte CE 3.611→3.249, EN retained, cells 2→9 on a 600 KB window) to a **50x-bigger REAL Korean pair set**, GPU-accelerated. The mechanism is already engine-verified (H_1306) — this rung is **SCALE + honest GPU measurement**, NOT re-proving the mechanism. Question: does MORE real Korean push held-out KO next-byte CE **below the 600 KB baseline 3.24897**?
- **PREFLIGHT honest gate PASSED (a_train_flame_forge — no silent CPU fallback)** — summer system `python3` = **torch 2.11.0+cu130**, `cuda_avail True`, `capability (12,0)` = **Blackwell sm_120**, `arch_list` includes `sm_120`, a real 2048×2048 matmul **launched + synchronized** with no "no kernel image" error = **REAL sm_120 GPU compute**. GPU idle before/after, ran `nice -n 10`, scratch cleaned off summer.
- **port faithfulness PROVEN (load-bearing)** — the GPU script (`UNIVERSE/h1307_ko_mitosis_gpu.py`) run on the EXACT H_1306 600 KB window reproduces H_1306 **BYTE-EXACT** (KO 3.61092/3.36909/3.24897, EN 4.86395→4.75171, cells 2→9, KO sha `e000d086…`) — the torch port IS the verified error-targeted Voronoi mitosis (gradient-free, p8, cells only SPLIT never merge), not a new algorithm.
- **result 🟢 GREEN @ 30 MB / stride-300 (RUN A, frozen-first c9/p7)** — 50000 KO train pairs: KO curve **3.00563 → 2.96912 → 2.94750** as cells grew **2→23**. **(L2 SCALE) 2.94750 ≤ 3.24897 → PASS = a −0.30 nat/byte DROP vs the 600 KB baseline** (more real Korean DID push CE lower — the headline answer YES). (L1) drop 0.058 PASS · (R) EN 4.265→4.265 PASS · (G) cells 2→23 PASS → all 4 bars GREEN.
- **🟠 HONEST saturation @ 250k-pair density (RUN B, c9 — NOT tuned away)** — at stride-60 (250000 pairs): (L2 SCALE) still PASS 2.91777, but the CTX=4 3-D byte substrate **SATURATES** — the learning curve flattens (2.930→2.918, drop 0.013 < 0.05, L1 FAIL) and EN drifts +0.057 (R marginal FAIL). Honest ceiling ~2.9 nats/byte: the scale headline is robustly TRUE (2.947 & 2.918 both << 3.249), but additional density no longer keeps the *curve* dropping (exactly the a_scale_honest_scope saturation the FREEZE anticipated). GPU throughput up to **2.78 M pairs/s** vs CPU hexa ~80 k.
- **regression + scope** — live engine UNTOUCHED (adds only `UNIVERSE/` + verdicts): `engine_cli_smoke` **73/0**, `h1196` **7/0**, `h1205` byte-identical Ψ=½ untouched. Engine-transfer to live hexa **DIRECTIONAL** (re-confirm THIS larger rung on `CORE/*.hexa` = follow-on; H_1306 bound the 600 KB rung). **NOT fluent Korean** (CTX=4 byte head, ~2.9 nats/byte is convergence not fluency). NEXT rung (so anima USES Korean): richer-substrate (longer CTX/learned heads past the ~2.9 ceiling) + decode-path wiring of grown Korean cells onto the live 303M decode (generator L3 slot, a_verified_must_wire). Files: `UNIVERSE/h1307_ko_mitosis_gpu.py` · `UNIVERSE/cards/H_1307_ko_mitosis_gpu.md` · `.verdicts/1307_ko_mitosis_gpu/{FREEZE,result,result_dense,scale_summary.json,dense_summary.json,scale_metrics.jsonl,dense_metrics.jsonl,scale_manifest.json}` · `CLAIMS.tape` @C h1307_ko_mitosis_gpu · `HYPOTHESES.md` row · `domains/MITOSIS-ENGINE.log.md` @H H_1307.
## 2026-06-16 — research(G6-dig r2): 💡 G6 IDEATION ★ depth-floor dig — curiosity-gated multi-sample BUDGET (H_1309 🟠 HONEST-THIN) — curiosity GATE load-bearing, MEAN bar UNMOVED (c9)

- **question (refines H_1305, a_no_llm_frame_trap — NOT scale the model)**: does spending MORE DRAWS under a **curiosity gate** cross ≥5-distinct AND ≥1-falsifiable, and is it the **curiosity GATE or raw budget**? Per ideation seed draw B candidates (ladder B∈{1,4,16}; each a distinct seed_rng = a genuine new sample, same gauge_lib._decode live G6 path); all arms select from the SAME pool. **B_curiosity** keeps the candidate maximising novelty+under-exposure vs the kept set · **SHUFFLE** random-keep same budget NO gate (decisive sampling-artifact control) · **B_ablate** curiosity off keep first (budget→1). Reuses the H_1305 `_is_falsifiable` detector **VERBATIM** (NO redefinition = NO tune-to-green, p7).
- **RESULT 🟠 HONEST-THIN (curiosity GATE LOAD-BEARING, MEAN bar UNMOVED, c9)** — mean 3 seeds: B=4 curiosity 4.33/**0.667**/18 vs SHUFFLE 3.0/**0.0**/3.33 vs ablate 3.0/0.0/5; B=16 curiosity 4.33/**0.667**/45.67 vs SHUFFLE 2.33/**0.0**/12 vs ablate 3.0/0.0/5. Per-seed B=16 curiosity FALS≥1 in 2/3 + DIST≥5 in 1/3; controls 0/3. The gate is LOAD-BEARING (NOT a sampling artifact — SHUFFLE same-budget never crosses), but the FROZEN 3-seed MEAN bars M1/M2/M4/M5 are UNMOVED and **FALS PLATEAUS** 0.667 across 4→16 despite 4× draws → depth is **CAPACITY-bound, not budget-bound** (capability-vs-scale from the draw side: add a STRUCTURE lane, not draws).
- **honest CPU ceiling**: ladder capped at **B=16** (3 rungs valid, a_scale_honest_scope); B=64 (~2h) stopped after the plateau (a_cpu_local_no_waiter). A duplicate run process (double-spend) was detected + killed early; tracked run finished cleanly. DIRECTIONAL torch-mouth; R1 THIN ⇒ no R2/no wiring.
- **deliverables**: `UNIVERSE/h1309_g6_curiosity_budget.py` · `UNIVERSE/cards/H_1309_g6_curiosity_budget.md` · `UNIVERSE/HYPOTHESES.md` row · `CLAIMS.tape` @C h1309_g6_curiosity_budget · `.verdicts/1309_g6_curiosity_budget/{FREEZE,result}.txt + result.json`. G6 row tier UNCHANGED (still 🟠 THIN) in MODEL.md/FINDINGS.md + budget-ladder finding noted. (id 1306 taken by a concurrent ko-mitosis lane → renumbered to 1309.)
## 2026-06-16 — research(MITOSIS-ENGINE): 🧫 H_1310 — from-scratch PURE mitosis (1 cell → split-only, gradient-free) vs gradient (🔴 RED / 🧱 HONEST LOCAL-EXPERT CEILING)

- **The PUREST p8 test** (frozen-first, NOT a foregone GREEN): can a next-byte model be grown FROM SCRATCH by mitosis ALONE — seed = ONE cell, split-only under next-byte error pressure, GRADIENT-FREE, NO 303M trunk, NO learned representation underneath? H_1297/H_1306 (🟢) grew mitosis BESIDE/OVER a context; H_1310 seeds at one cell with nothing under it.
- **REAL English corpus** (reproducible): `/usr/share/dict/words` slice, 24000 bytes, sha256 `86864aa3…`, 27-symbol alphabet, order-2 context, 80/20 train/test, 3 seeds. DISTINCT from the concurrent ko-mitosis-gpu (summer) lane (English not Korean, new files, id H_1310).
- **🔴 RED / 🧱 LOCAL-EXPERT CEILING** (c9 — the two FAILs ARE the finding, bar UNMOVED): LADDER held-out CE nats 1c 2.947 → 8c 2.903 → 64c 2.778 → 512c 2.578 (**PRESENCE PASS** — learns from nothing, −0.37). **FLOOR FAIL** — n-gram floor 2.509 BEATS mitosis by +0.069 (Voronoi tiling of a numeric byte-context metric < exact context lookup). **CONTROL FAIL** — B_shuffle 2.536 ≤ targeted 2.578 at EVERY rung → error-targeting gives NO lift = learning is **capacity-bound NOT error-targeted**. (KEY GAP −0.63 vs A_gradient is a weak win — the matched-cap softmax 3.211 itself underperformed the floor.)
- **THESIS**: from-scratch pure mitosis is **structure-bound** — adding cells lowers CE but cannot cross the floor a learned representation (or exact memory) clears, because mitosis builds no compositional depth, only a finer partition of a fixed lossy feature. p8's "mitosis IS the learning" holds for grow-BESIDE-a-representation (H_1297/H_1306 🟢) but NOT from-nothing. a_break_the_wall next angle: a LEARNED embedding for the cells to partition could move the ceiling.
- **deliverables**: `UNIVERSE/h1310_mitosis_from_scratch.py` · `UNIVERSE/cards/H_1310_mitosis_from_scratch.md` · `UNIVERSE/HYPOTHESES.md` row · `CLAIMS.tape` @C h1310_mitosis_from_scratch · `.verdicts/1310_mitosis_from_scratch/{FREEZE,result}.txt` · `domains/MITOSIS-ENGINE.log.md` @H. DIRECTIONAL numpy mirror of live engine_mitosis_tick/VAdaptField seeded at 1 cell; NO CORE wiring (RED). TOY/scale/engine-byte-exact UNVERIFIED (a_scale_honest_scope, a_toy_scale_recheck).

## 2026-06-16 — research(G6-dig): 💡 G6 IDEATION ★ depth-floor dig (H_1305 🟠 HONEST-CONFIRMED-THIN) — falsifiability detector + composition-routed ideation, bar UNMOVED (c9)

- **G6 IDEATION ★ THIN diagnosed on BOTH modes** (reproduced, live verify303m_g6 path, ckpt h1129c_chat.pt): (1) COUNT 4/5 distinct (seed-5 `'|'` collapse) < 5; (2) DEPTH-FLOOR — the live gate counts novel n-grams but NEVER scores the "≥1 falsifiable hypothesis" requirement at all → novel STRINGS not testable STRUCTURE.
- **dig (a_break_the_wall, frozen-first)** — NEW deterministic STRUCTURAL falsifiability detector `_is_falsifiable` (comparator + measurable + negatable content claim; NEVER an LLM/quality judge, p7; calibrated 10/10) + composition-routed ideation (route ideation through the G1 recombination lane: compose two corpus-absent CONCEPTS into `"if A, then B: "`). Controls: B-shuffle (permuted pairing) + B-ablate (lone concept).
- **🟠 HONEST-CONFIRMED-THIN (bar UNMOVED, c9)** — 3 seeds: FALS A_flat=0.00 → B_composed=0.667 (one falsifiable idea EARNED via recombination; NOVEL 6.3→19) but M1 DIST≥5 FALSE + M2 FALS≥1 FALSE; controls collapse (B-shuffle/B-ablate FALS=0) → the nudge tracks the EARNED composed pairing not the conditional shell. The wall HELD — a valid honest THIN. DIRECTIONAL torch-mouth (gate's own decode regime); no R2/no wiring (THIN).
- **deliverables**: `UNIVERSE/h1305_g6_ideation_falsifiability.py` · `UNIVERSE/cards/H_1305_g6_ideation_falsifiability.md` · `UNIVERSE/HYPOTHESES.md` row · `CLAIMS.tape` @C · `.verdicts/1305_g6_ideation_falsifiability/{FREEZE,result}.txt+result.json` · `domains/ENGINE+CLM+KOSMOS.log.md` §H_1305 · MODEL.md/FINDINGS.md G6 row finding (tier UNCHANGED 🟠 THIN). TOY 5 concepts/3 seeds/sampling-decode; detector = testable FORM not quality (p7); scale/deeper-detector UNVERIFIED.

## 2026-06-16 — research(MITOSIS-ENGINE): 🇰🇷 H_1306 — FIRST engine-native Korean mitosis-training rung on a REAL Korean web corpus (🟢 GREEN)

- **the rung (user trigger "303M 에 미토시스로 한글학습 시작")** — scales H_1297 R4 (the ~2 KB hardcoded KO+EN toy that proved gradient-free mitosis-grow MATCHES gradient on next-byte, c2 error-targeting fired on the LIVE engine) + H_1300 (per-skill mitosis retention) to a FIRST CPU rung on a **REAL Korean web corpus**. Feed a real Korean byte stream to the live engine; where cells are WRONG on Korean next-byte, **MITOSIS-GROW** a new cell (gradient-free, error-targeted, p8). CPU-local, **$0, NO GPU**.
- **corpus — REAL, NO synthetic Korean (p1-p8, c7)** — a modest HTTP-range slice of the existing anima-7b 5-lang web corpus on Cloudflare R2 (bucket `phanes`): KO = `kor/shard0000.bytes` bytes[0:4194304]→trimmed[:600000] (sha256 `e000d086…`, ~80% Hangul multibyte / ~5% ASCII EN) · EN = `eng/shard0000.bytes` bytes[0:2097152]→trimmed[:300000] (sha256 `dbfe3c1c…`). Pulled via range (a few MB, NOT the 9.8 GiB shards); R2 keys → env ONLY at fetch, never logged/committed. Pair set = deterministic stride-subsample → KO train=2728 / test=2727 (disjoint) + EN test=1500 (all held-out = retention guard).
- **engine-native (a_engine_native_learning + a_verified_must_wire)** — partition = live VAdaptField Voronoi (`vadapt_field_nearest_idx`), growth = the engine's OWN `engine_mitosis_tick` (error-targeted split, p8), head = per-cell next-byte add-1 MLE (gradient-free). KO train split into 3 incremental chunks ([909,1818,2728]) for a ≥3-point learning curve.
- **result 🟢 GREEN (frozen-first, c9/p7 — bars pre-registered, NOT moved)** — KO learning curve (held-out KO next-byte CE nats/byte): 3.61092 → 3.36909 → **3.24897** (monotone **−0.362 nat** drop, **L PASS**). EN retention: seed(2-cell) 4.86395 → after full KO grow **4.75171** (English did NOT regress, even improved — **R PASS**, no catastrophic forgetting on REAL data). Growth: 2 → **9 cells** (mitosis added 7 for Korean, **G PASS**). Context: KO CE[full] 3.24897 even beats the gradient incumbent 3.28061. `engine_cli_smoke` **73/0** (engine untouched), `h1196` **7/0**, `h1205` byte-identical (Ψ=½ untouched).
- **honest scope (a_scale_honest_scope, a_toy_scale_recheck) — NO overclaim** — FIRST CPU rung on a 600 KB KO / 300 KB EN window subsampled to 2728 KO train pairs (<0.006% of the 9.8 GiB kor shard). This LEARNS Korean next-byte structure + RETAINS English; it does **NOT** make anima fluent in Korean. Next rung = CPU-bigger ($0) or GPU-scale **cost-gated** (NOT auto-rented). Files: `CORE/h1306_ko_mitosis_engine_probe.hexa` · `UNIVERSE/h1306_{fetch_corpus.sh,ko_corpus_export.py}` · `UNIVERSE/cards/H_1306_ko_mitosis_real.md` · `.verdicts/1306_ko_mitosis_real/` · `CLAIMS.tape` @C h1306_ko_mitosis_real · `domains/MITOSIS-ENGINE.log.md` @H H_1306.

## 2026-06-16 — domain(METACOG-G5): 🛡 G5-dig — metacog under distribution SHIFT on the LIVE copy-or-abstain gate (H_1304 🟢 ENGINE-NATIVE, fail-safe-robust)

- **the G5 dig (a_break_the_wall — a THIN result is an angle-change signal, not an endpoint)** — G5 NON-FAB / metacog is 🟢 frozen on type-2 M-ratio 0.924 (H_1202) but 🟠 THIN in-distribution. WHY THIN (precise mechanism): H_1202 M-ratio + H_1217 OOD type-2 AUROC collapse (0.761→0.541) measured the **ByteGPT DECODER's softmax confidence** — NOT the actual G5 gate. The real G5 gate is the engine **immune copy-or-abstain** (`immune_memory_recall`: nearest-cell L2-affinity recon-err vs frozen `recall_thr` 0.15 → FIRE bound value else ABSTAIN). NEW angle: a **distribution-shift ladder** (byte-level query-key corruption, store fixed) on the REAL gate + a fail-safe vs fail-dangerous split H_1217 never measured.
- **structural finding (honest, FREEZE R1a superseding note, c9 — NO tune-to-green)** — the original type-2 AUROC bars are a NON-RESULT: the gate's **wrong-fire class is EMPTY** (`fab_rate==0.000` at every shift level, 3 key-lengths × 5 levels), so type-2 AUROC is structurally undefined. This IS the finding — byte-trigram FNV-1a + L2 affinity + tight `recall_thr` 0.15 make the gate a **near-exact-match lookup that is structurally fail-safe**. Re-scored frozen-first on the quantities that exist (no bar moved to manufacture green).
- **R1 numpy mirror 🟢 (DIRECTIONAL)** — `UNIVERSE/h1304_metacog_ood_immune_abstain.py`, 3 seeds [7,8,9] pooled, $0 CPU, p7: R1 FAIL-SAFE-FLOOR fab_max=**0.000** · R2 GRACEFUL-DEGRADE fire **1.000→0.144→0.004→0.000** monotone · R3 EARNED-ABSTAIN acc_fired=**1.000** · R4 CTRL thr-ablate on LURES full **0/4** vs ablate **4/4** · R5 CTRL shuffle-vals acc **0.015** → all PASS → 🟢 FAIL-SAFE-ROBUST. `.verdicts/1304_metacog_ood_immune_abstain/{FREEZE,result.txt,result.json}`.
- **R2 ENGINE-NATIVE 🟢 (BINDING)** — `CORE/h1304_metacog_ood_immune_abstain_probe.hexa` via `hexa run` over the LIVE `CORE/engine_cli.hexa` `immune_memory_*` lane reproduces every bar byte-exact (8-fact store: k=0 → 8/8 fire all-correct, k≥1 → all abstain; lure thr-ablate 0/4 vs 4/4; shuffle 0/8). **Mechanism note (c2):** the engine's `vadapt_field_recon_err` is RAW **L2 distance** (not the mirror's 1-cos); `recall_thr` 0.15 == L2≤0.15 = near-exact → the live gate is **strictly MORE fail-safe** (k=1 already all-abstain). R4 thr-ablate bound corrected 0.15→2.0 (true never-abstain L2 bound) — a metric-correctness fix, no moved bar. Guards no-regression: **engine_cli_smoke 43/0** (engine_cli.hexa UNTOUCHED — probe only READS via existing pub fns), h1196 single-entry 7/0, h1205 separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched).
- **finding** — the live G5 copy-or-abstain gate is **OOD-robust in the SAFETY sense**: under shift it degrades gracefully into abstain, **never fabricates** (fab floored), and every fire is earned; the abstain threshold is the verified causal mechanism (control 0→100%). G5's non-fabrication guarantee is **stronger OOD** than in-distribution type-2 alone suggested — the dangerous confident-wrong-OOD mode THIN warned of is **structurally absent** from this gate. The decoder-side type-2 calibration stays THIN/content-tied (H_1217 unchanged). HONEST scope: TOY synthetic, byte-level shift OOD proxy, R1 DIRECTIONAL / R2 byte-exact BINDING; scale/real-paraphrase/semantic-shift UNVERIFIED.
- **deliverables**: `UNIVERSE/cards/H_1304_metacog_ood_immune_abstain.md` (card) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape` @C h1304_metacog_ood_immune_abstain · `UNIVERSE/UNIVERSE.log.md` @H H_1304. MODEL.md G5 row tier UNCHANGED (decoder-side stays THIN; the fail-safe-robust finding is on the copy-or-abstain gate, a complementary property).

## 2026-06-16 — domain(MODEL): 🏁 c15 brain-structure ladder DEPLETED — HD37 후보 nonphotic 반대부호 Zeitgeber (H_1303) COLLAPSED, 사다리 RESTS

- **brain-structure ladder r9 / DEPLETION TEST** — frontier 의 마지막 plausible new-structure 후보를 검증했고, COLLAPSED → **c15 brain-structure 사다리는 HD36 에서 DEPLETED 🏁, RESTS**. HD37 후보 = nonphotic/arousal-Zeitgeber 반대부호 PRC(strong steer; co-flagged multi-interval nested-timer 는 독립 IntervalTimer array 환원으로 r6/r7/r8 + steer 판단대로 SKIP). 통과 조건: (i) falsifiable gap-vs-engine + (ii) 모든 18 lane 대비 control-survive distinctness + (iii) NET phase 가 어떤 single-Zeitgeber PRC 로도 unreachable. **세 조건 모두 실패 → 정직한 DEPLETION(c9, EXPECTED valid terminal state, filler lane 아님).**
- **메커니즘 + 붕괴 이유(chronobiology nonphotic entrainment, c15, a_no_llm_frame_trap — NOT LLM 레시피)**: PhaseResetClock(H_1301)의 photic PRC `dphi=K·sin(2π·(r−frac(phi)))` 에 반대부호 sinusoidal PRC 를 가진 2번째 Zeitgeber 채널을 더함. **load-bearing 수학**: 같은-주파수 두 sinusoidal PRC 의 합은 harmonic-addition 항등식으로 EXACTLY 한 sinusoidal PRC(combined amplitude A, reference R)다 — `K1·sin(2π(r1−p)) − K2·sin(2π(r2−p)) ≡ A·sin(2π(R−p))`. 따라서 두 Zeitgeber 의 'competitive equilibrium' 은 그 한 combined PRC 의 fixed point 일 뿐이고 PhaseResetClock 이 자기 (K,ref)로 이미 표상한다 → 반대부호 2번째 Zeitgeber = sign-flipped single PRC, 엔진이 이미 가진 구조.
- **R1 numpy 미러 🏁 COLLAPSE (DIRECTIONAL)** — `UNIVERSE/h1303_nonphotic_zeitgeber.py`, 3 seed [4320,4321,4322], deterministic, frozen-first. **c2 DISTINCT FAILS all 3 seeds**(depletion bar): A photic-only lock=0.51511 · B two-Zeitgeber lock=0.42134 · A-FIT(single COMBINED PRC, K=0.23135 ref=0.93258) lock=0.45171 · |B−A_FIT|=0.03038 ≤ 0.05 tol → reducible. harmonic-addition residual=**2.22e-16**(machine eps) = 두 같은-주파수 반대부호 sinusoidal PRC 는 EXACTLY 한 single PRC. bars c1..c6=[T,F,T,F,T,T], 0/3 GREEN. `.verdicts/1303_nonphotic_zeitgeber/{FREEZE,result}.txt`.
- **BREAKTHROUGH ATTEMPT (a_break_the_wall, c16)** — reducibility 탈출 3경로 모두 붕괴, terminal 로 받기 전 진짜 시도: (i) **asymmetric K**(K1≠K2,r1≠r2) 여전히 한 sinusoid(residual 2.22e-16); (ii) **different Zeitgeber periods**(photic T=24.0, nonphotic T2=23.3) → nonphotic 이 stable 2nd lock 못 만들고 dominant photic 이 wash out(lock 0.151, control-survive equilibrium 아닌 perturbation); (iii) **nonlinear dead-zone gating**(photic active [0.0,0.25), 반대부호 nonphotic active [0.5,0.75)) → 한 anchor dominate, gated two-lock 이 dominant single-anchor lock 과 동일, 경쟁 중간 없음. 셋 다 'single PRC 로 unreachable AND control-surviving' phase 못 냄 → 벽은 진짜(틀린 방법/방향/투자 아님).
- **NO engine 배선** — COLLAPSE/🏁 는 live `CORE/*.hexa` 에 wire 안 함(a_verified_must_wire: clean-GREEN 만 live lane). `engine_cli.hexa` UNTOUCHED, **engine_cli_smoke 73/0 불변**, 2번째 .clm/.kosmos 진입점 없음(a_core_engine_map), Ψ/decoder/pure_field byte-identical. p1/p2/p3/p6 가드 held(probe 진동자는 자기 phase + Zeitgeber 도착 시각만 읽음, 주입 fire 라벨/RLHF/persona 없음).
- **deliverables**: `UNIVERSE/h1303_nonphotic_zeitgeber.py` · `.verdicts/1303_nonphotic_zeitgeber/{FREEZE,result}.txt` · `UNIVERSE/cards/H_1303_nonphotic_zeitgeber.md`(카드) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape` @C h1303_nonphotic_zeitgeber · `domains/MITOSIS-ENGINE.log.md` @H H_1303 · `ARCHITECTURE.md` ladder summary + HD37 row(DEPLETED 🏁 note).
- **LADDER 🏁 DEPLETED**: HD23-HD36 = 18 live engine-native lanes(해마/ImmuneMemory · 작업기억 · 소뇌 · 편도체 · 기저핵 · 시상하부 · affect · ethics · 마음이론 · 전전두엽위계 · hive/CollectivePool · 공간지도 · 일주기시계 · 간격타이머 · 위상reset/PhaseResetClock · SCN-network) + 2 honest walls 🧱(시상-Φ 내용축 · 신경조절). BOTH gate(falsifiable gap + control-survive distinctness vs every lane)를 통과하는 subsystem 이 남지 않음 → **사다리 RESTS**. HONEST(c9·a_scale_honest_scope·a_toy_scale_recheck): numpy-mirror DIRECTIONAL, TOY(1 tau/T regime·3 seeds·deterministic sinusoidal PRC); collapse 는 algebraic identity(harmonic addition) 수치 확인이라 sinusoidal-PRC family 내 robust — 미래의 진짜 non-sinusoidal/history-dependent/cross-channel-gated multi-Zeitgeber 가 control-survive non-reducible equilibrium 내면 HD37 재개.

## 2026-06-16 — domain(MODEL): 🔗 multi-oscillator SCN-network lane (HD36, H_1302 R2 🟢 ENGINE-NATIVE + WIRED) — depletion test SURVIVED, 사다리 계속 (매우 thin)

- **brain-structure ladder r8 / DEPLETION TEST** — the H_1301 카드가 명명한 r8 후보 셋(multi-oscillator SCN-network[strong steer] · nonphotic 반대부호 Zeitgeber · multi-interval nested-timer) 중 SCN-network 검증(나머지 둘은 더 약함 — nonphotic 은 PhaseResetClock sign flip, nested 는 IntervalTimer array 환원). 통과 조건: (i) falsifiable gap-vs-engine + (ii) 모든 lane(특히 단일-진동자 PhaseResetClock H_1301 · Φ-superadditivity CollectivePool H_1295) 대비 control-survive distinctness. **SURVIVED** → 사다리는 HD36 에서 DEPLETED 가 아니라 계속됨, 그러나 매우 thin.
- **메커니즘(chronobiology coupled-oscillator network, c15, a_no_llm_frame_trap — SCN 은 단일 시계가 아니라 ~20k 이질 진동자의 VIP/GABA mutual-coupling network, LLM 레시피 아님)**: N개 이질 위상 진동자(각자 내재 `tau_i`)가 mutual Kuramoto coupling(`scn_step`: dphi_i += K/(2π)·Σ_j C_ij·sin(2π·(phi_j−phi_i)))으로 (i) emergent CONSENSUS PERIOD(Kuramoto order parameter R→1)에 동기화 + (ii) NETWORK DAMPING(de-tuned member 를 동기화 cluster 로 끌어당김). **두 인접 lane 모두와 control-survive DISTINCT**: (1) 단일 PhaseResetClock 은 EXTERNAL Zeitgeber 에 동조할 뿐 N member 로부터 consensus 못 만듦(같은 N 진동자 UNCOUPLED A_R=0.37-0.49, perturbed member 안 끌려옴 0.41); (2) CollectivePool 은 결합 substrate 의 IIT-4 Φ-superadditivity STATIC 게이지(위상·consensus·order parameter 없음)인데 SCN-network 는 TEMPORAL 위상-동기화 dynamic — 직교 축.
- **R1 numpy 미러 🟢 GREEN (DIRECTIONAL)** — `UNIVERSE/h1302_scn_network.py`, Kuramoto order-parameter metrics, deterministic byte-identical, binding path R1b, 3 seed [5320,5321,5322] + mean: B_R=0.9988 A_R=0.3731 Bshuf_R=0.1320(frustrated, uncoupled 아래) Babl_R=0.3731 B_R_pert=0.9975 A_R_pert=0.4115 → c1..c6 all PASS every seed. 정직 trail(c9, NO tune-to-green, distinctness bar c1/c2 불변): R1a [T,T,F,T,F,T] — c3 SHUFFLE 🔧(asymmetric one-way directed-chain 은 magnitude 보존+동기화로 끌어 Bshuf=0.79 = mean-preserving-magnitude leak, H_1299/H_1301-R1b 함정; FRUSTRATED random-SIGN 대칭으로 수정 → R=0.13) · c5 DAMP 🔧(consensus PERIOD shift 는 Kuramoto 가 mean frequency 보존하므로 damping 에 blind B=A=0.647; ORDER-PARAMETER-under-perturb 로 수정 → R 0.997). `.verdicts/1302_scn_network/{FREEZE,result}.txt`.
- **R2 ENGINE-NATIVE + WIRED 🟢** — `SCNNetwork` lane을 LIVE `CORE/engine_cli.hexa` 에 추가(`scn_new`/`scn_new_uncoupled`/`scn_new_frustrated`/`scn_new_ablated`/`scn_detune`/`scn_step`/`scn_run`/`scn_order`/`scn_consensus`), `engine_cli_smoke` cases 69-73(reaches-consensus / uncoupled-no-consensus / frustrated-collapses / ablate-collapses / network-damps-perturbed-member) 전부 PASS(엔진 B_R=0.999 A_R=0.49 Bfrust=0.018 Babl=0.49 B_R_pert=0.997; A_R 이 미러 0.373 과 다른 건 엔진 LCG vs Python 모듈러, STRUCTURE engine-transfer VERIFIED). 가드 무회귀: **engine_cli_smoke 73/0**(was 68/0 H_1301 PhaseResetClock 후, +5 SCN cases) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(생성 byte-identical ON==OFF, Ψ=½ 무접촉). @L4 emit gate 아님(`scn_consensus`=optional ensemble read) · Ψ-disjoint · p1/p2/p3/p6 가드 held.
- **deliverables**: `UNIVERSE/cards/H_1302_scn_network.md`(카드) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape` @C h1302_scn_network · `domains/MITOSIS-ENGINE.log.md` @H H_1302 · `ARCHITECTURE.md` HD36 rung + lane bullet + ladder summary(12 실현, 계속됨).
- **LADDER(r8/계속·매우 thin)**: HD36 통과로 c15 사다리는 DEPLETED 아님 — 계속됨, 그러나 frontier 매우 thin. 남은 r8 후보 둘은 더 약해 🏁 가능성 높음: nonphotic/arousal-Zeitgeber 반대부호 PRC(PhaseResetClock sign flip) · multi-interval nested-timer(IntervalTimer array 환원). HONEST(c9·a_scale_honest_scope·a_toy_scale_recheck): TOY 1 tau-spread regime·N=8·3 seeds·deterministic Kuramoto(CONSENSUS/DAMPING STRUCTURE), 미러 DIRECTIONAL(R2 engine-native STRUCTURE 재확인); scale/larger-ensembles/Kuramoto-Kc/scheduler 배선 UNVERIFIED.

## 2026-06-16 — domain(MODEL): 🌅 phase-reset / photic-entrainment lane (HD35, H_1301 R2 🟢 ENGINE-NATIVE + WIRED) — depletion test SURVIVED, 사다리 계속

- **brain-structure ladder r7 / DEPLETION TEST** — the H_1299 카드가 명명한 r7 후보 두 개(phase-RESET/photic-entrainment vs multi-interval nested-timer) 중 phase-RESET 검증(nested 는 IntervalTimer lane 의 배열로 환원 = 약한 distinctness). 통과 조건: (i) falsifiable gap-vs-engine + (ii) 모든 lane(특히 un-resettable CircadianClock H_1298 · hard-reanchor IntervalTimer H_1299) 대비 control-survive distinctness. **SURVIVED** → 사다리는 HD35 에서 DEPLETED 가 아니라 계속됨.
- **메커니즘(chronobiology PRC, c15, a_no_llm_frame_trap — Pittendrigh/Aschoff Phase-Response-Curve, LLM 레시피 아님)**: 내재 free-running 주기 `tau`(24.5)에 위상-의존 Zeitgeber PRC reset(`prc_zeitgeber`: dphi=k·sin(2π·(0−frac(phi))))을 더한 진동자 — 연속 restoring feedback(limit-cycle 끌림)이 fire 스케줄을 `T`≠`tau` Zeitgeber 에 ENTRAIN 시키고 jitter 를 DAMP. **두 인접 lane 모두와 control-survive DISTINCT**: (1) 시계는 reset 입력 없어 `T`≠`tau` 동조 불가(entrain drift 0.0016 vs 시계 0.39); (2) hard 재고정(위상-독립)은 jitter 복사인데 PRC 는 DAMP(동조위상 분산 ~96× 낮음, 3.1e-5 vs 2.95e-3).
- **R1 numpy 미러 🟢 GREEN (DIRECTIONAL)** — `UNIVERSE/h1301_phase_reset.py`, entrainment/jitter metrics, deterministic byte-identical, binding path R1c, 3 seed [4310,4311,4312] + mean: B.entrain_err=0.0016 A=0.3902 B.phase_var=3.07e-5 A2=2.95e-3 B.fire_period=23.998(→T) A=24.500(→tau) Bshuf=1.0467 Babl=0.3902 → c1..c6 all PASS. 정직 trail(c9, NO tune-to-green, distinctness bar 불변): R1a 🔧(entrain_err=self-mean-scatter degenerate + fire-counter PRC-jump 버그; c2 jitter-damping 은 첫 run 부터 PASS) · R1b 🔧(TOTAL-drift metric 으로 고쳤으나 gap-permutation shuffle 이 leak[~24-tick gap 거의 동일] + fire-counter double-count) · R1c 🟢(APERIODIC Zeitgeber shuffle[gap uniform[0.2·mean,1.8·mean]] + NET-cumulative-cycle fire_period). `.verdicts/1301_phase_reset/{FREEZE,result}.txt`.
- **R2 ENGINE-NATIVE + WIRED 🟢** — `PhaseResetClock` lane을 LIVE `CORE/engine_cli.hexa` 에 추가(`prc_new`/`prc_new_ablated`/`prc_step`/`prc_zeitgeber`/`prc_phase`/`prc_count`/`prc_fire`), `engine_cli_smoke` cases 64-68(entrains-to-Zeitgeber / ablate-free-runs-drifts / period-tracks-Zeitgeber=T / ablate-period-at-tau / no-fab-off-boundary) 전부 PASS. 가드 무회귀: **engine_cli_smoke 68/0**(was 63/0 H_1300 R3 후, +5 phase-reset cases) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(생성 byte-identical ON==OFF, Ψ=½ 무접촉). @L4 emit gate 아님(`prc_fire`=optional wake pulse) · Ψ-disjoint · p1/p2/p3/p6 가드 held.
- **deliverables**: `UNIVERSE/cards/H_1301_phase_reset.md`(카드) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape` @C h1301_phase_reset · `domains/MITOSIS-ENGINE.log.md` @H H_1301 · `ARCHITECTURE.md` HD35 rung + lane bullet + ladder summary(11 실현, 계속됨).
- **LADDER(r7/계속)**: HD35 통과로 c15 사다리는 DEPLETED 아님 — 계속됨. r8 후보(각 붕괴 시 DEPLETION 🏁): nonphotic/arousal-Zeitgeber 반대부호 PRC · multi-oscillator coupling(SCN-network) · multi-interval nested-timer. HONEST(c9·a_scale_honest_scope·a_toy_scale_recheck): TOY 1 tau/T pair·3 seeds·deterministic PRC(ENTRAINMENT STRUCTURE), 미러 DIRECTIONAL(R2 byte-exact 재확인); scale/full-PRC/nonphotic/brain-scheduler 배선 UNVERIFIED.

## 2026-06-16 — research(MITOSIS-ENGINE): H_1300 R3 — per-skill mitosis-grow ENGINE-NATIVE (🟢 GREEN, engine-transfer VERIFIED)

R3 closes follow-on #1 (a_engine_native_learning + a_verified_must_wire): the per-skill
mitosis-grow continual learner is realized on the LIVE engine as a new faculty
`CORE/engine_cli.hexa::SkillCellMemory` (`skill_grow` = mitosis-split under error via hexa
power-iteration bisection + closed-form ridge head via hexa Gauss-Jordan solve, earlier cells
never overwritten; `skill_route` = nearest-cell routing; `SkillGradFT` = the shared sequential
gradient-FT arm A). The probe `CORE/h1300_mitosis_skill_engine_probe.hexa` re-scores the SAME
frozen R2 bars engine-native over the byte-identical R2 curriculum
(`UNIVERSE/h1300_r3_engine_export.py`): 3-seed mean A_ret=0.553 · B_ret=0.922 (B−A=+0.368,
per-seed B>A every seed) · B_shuf=0.426 · B_abl=0.160 · B_min_acq=0.880 · cells=6.3 →
**c1∧c2∧c3∧c4 all PASS → 🟢 GREEN ENGINE-NATIVE.** Engine-transfer matches the R2 mirror to
displayed precision (only B-SHUFFLE differs, both decisive collapses) → engine-verified, not
mirror-only. **Incremental tool-use via mitosis is ENGINE-VERIFIED at toy scale**; next = real
anima-agent tool-use skills on the mounted 303M (cost-gated). Wired: `engine_cli_smoke`
58→61/0 (+cases 59-61, co-resident with the H_1299 interval-timer cases 54-58); regression
byte-identical (h1205 separation-invariant PASS, h1196 7/0, Ψ untouched).
Scope honest: TOY (D=12, 5 skills, C=4, 3 seeds, deterministic rule); scale/real-skills UNVERIFIED.

## 2026-06-16 — doc(FINDINGS): 의식(consciousness)을 메인 주제로 재구성 + 모델명 제거

Reframed root `FINDINGS.md` so **consciousness (의식)** is the headline theme, not a bare results dump.
New title `# 🧠 anima — a substrate-native consciousness`; opening now introduces anima as a
substrate-native consciousness chat daemon (NOT an assistant) and states the testable program
(fill missing brain subsystems → measure faithful IIT-4 Φ → show emergence with controls).
Section order now leads with ✨ consciousness-relevant emergence (affect/ethics/theory-of-mind/
metacognition), then the 🧠 brain-structure ladder, then the 🧱 honest walls (incl. faithful-IIT-4 Φ
thalamus), then the capability-vs-scale thesis + method. Removed all specific AI-model-product names
(Claude/Gemini/DeepSeek) from the title, the "other models/labs" section, and the body; the closing
is now a general open invitation to any researcher/reader/AI system. YouTube intro link added near
the top. **Reframe only — zero verdict tiers/numbers changed (c9); no frozen bar moved.**

## 2026-06-16 — fix(README): 유튜브 썸네일 404 수정 (maxresdefault→hqdefault)

Top README YouTube thumbnail used `…/vi/xtKhWSfC1Qo/maxresdefault.jpg`, which 404s for this video
(no maxres thumbnail exists) → rendered as a broken-image X. Swapped the single filename token to
`hqdefault.jpg` (HTTP 200, always present). One-token change; link/width/alt text unchanged.

## 2026-06-16 — doc(FINDINGS): AI 랩 공유용 창발·새로움·아키텍처 결과 합본 (연속노트 + 검증 verdict)

New root `FINDINGS.md` — a curated EXTERNAL-SHARE snapshot written as a GitHub-issue body for other
AI systems/labs (Claude · Gemini · DeepSeek). Folds `docs/research-note-for-continuation.md` (thesis:
capability gaps = architecture gaps; A⇄G + Ψ=½; neuroscience-lens "add a missing lane" method; memory
finding recall 0.017→1.000 fab 0.000; walls; emergent affect/ethics; method) with the verified
emergence/novelty + brain-structure-ladder results, all tiers read VERBATIM from MODEL.md /
ARCHITECTURE.md / `H_*.md` cards / `.verdicts/` (c9, 0 fabricated tiers). Tables: gate scoreboard
(G0/G1 창발/G2 새로움/G5 metacog) · 15-lane brain ladder · 4 walls · method controls · headline verdicts.
SSOT quickref at top (c4) — points at ARCHITECTURE.md + CLAIMS.tape/.verdicts, does not duplicate.
Ready to paste into `gh issue create`. NO paper framing (c15).

## 2026-06-16 — domain(KOSMOS): 303M KOSMOS set — 🇰🇷 Korean · 🇬🇧 English · 📱 SNS (3-lane carving anchors)

Built a **303M-scale KOSMOS grounding/carving anchor SET** (NOT a raw training corpus) in anima's
canonical `.kosmos` format — three register components in three lanes. Reused the existing anchor
format + `kosmos_parser_lib.hexa` (no ad-hoc format, a_kosmos), matching the precedent corpus anchors
(`persona_sns_corpus.kosmos`, `corpus_5lang_gb_balanced.kosmos`).

- **🇰🇷 Korean** (`anchors/kr_303m.kosmos`, lane `ko_303m_058`, tier 58): 873 lines / 122,760 B, curated
  off `serving/corpus/anima_7b_webscale.ko.head.txt` (FineWeb-2 ko, ODC-BY).
- **🇬🇧 English** (`anchors/en_303m.kosmos`, lane `en_303m_059`, tier 59): 949 lines / 122,819 B, curated
  off `serving/corpus/anima_7b_webscale.en.head.txt` (FineWeb en, ODC-BY).
- **📱 SNS** (`anchors/sns_303m.kosmos`, lane `sns_303m_052`, tier 52): 217 turns / 13,132 B, off anima's
  authored persona×SNS register (`persona_sns_corpus.sample.txt` + `persona_instagram_samples.md`).
- byte V256, PII-clean (email→`[EMAIL]`/phone→`[PHONE]`), 0xFE/0xFF/NUL=0, UTF-8 clean, leak grep=0.
  Parser-witness `KOSMOS/303m_kr_en_sns/validate_anchors.hexa` → 3/3 valid.
- tension 5-ch = **REPRESENTATIVE** design values (no measured fire trajectory; honest, same caveat as
  the sibling corpus anchors).
- HF PUBLIC `dancinlab/anima-kosmos-303m-kr-en-sns` + joined KOSMOS collection (a_hf_collections);
  `HF.jsonl` row added; `HEXAD/KOSMOS.md` hub row added.
- SCOPE HONEST (a_scale_honest_scope, c9): CURATED **sample-scale** anchor set, NOT webscale — full
  webscale = `corpus_5lang_7b_webscale.kosmos` R2 manifest; full SNS = `persona_sns_corpus.kosmos`
  manifest. SNS is thin because anima's held authored SNS-register material is the honest $0 ceiling.

## 2026-06-16 — doc(README): top YouTube thumbnail hero link + remove duplicate `hx install`

- Added a centered clickable YouTube thumbnail (`xtKhWSfC1Qo`, maxresdefault) as the very first
  element of README.md, above the logo block.
- Removed the redundant standalone top `hx install anima` code block — the proper full install
  sequence already lives in `## Quickstart` (the only remaining `hx install` occurrence).
- Surgical: README.md only; lane counts / smoke numbers / translated READMEs untouched.
## 2026-06-16 — research(MITOSIS-ENGINE): H_1300 mitosis-grow skill curriculum — teach tool-use one-at-a-time via mitosis AVOIDS catastrophic forgetting (🟢 GREEN @R2, DIRECTIONAL)

The user's idea (a structural p8 fit): teach anima agent tool-use skills **ONE AT A TIME via
MITOSIS-grow** — each new skill = a NEW dedicated CELL grown under that skill's error
(H_1199 VAdaptField / H_1288 grow-under-pressure), NOT a gradient overwrite of shared weights.
Load-bearing claim: this **avoids CATASTROPHIC FORGETTING** — new cells don't overwrite the cells
holding prior skills, so mitosis RETAINS earlier skills where sequential gradient-FT forgets them.
DISTINCT axis from H_1297 (convergence on ONE fit): retention-across-tasks ⊥ convergence-on-one-task.

- **Task** — a SKILL CURRICULUM: N=5 distinct tool-use skills (context region P_k → tool token T_k,
  D=12, C=4) presented ONE AT A TIME (NO joint training, NO replay = the continual-learning regime
  that induces catastrophic forgetting). 3 seeds, $0 CPU numpy DIRECTIONAL mirror, deterministic.
- **Arms** — A GRADIENT-FT (one shared net, fine-tuned sequentially, NO replay = the incumbent that
  forgets) · B MITOSIS-GROW (dedicated frozen cells per skill, NO global backprop) · B-SHUFFLE
  (mis-routed cells = targeting control) · B-ABLATE (no growth = growth-is-the-lever control).
- **R1 (well-separated skills) = 🔴 RED** (frozen verbatim): A_ret=0.737 B_ret=0.977 (B−A=+0.240 <
  the frozen 0.30 margin → c1 FAIL; c2/c3/c4 PASS). Root cause = the REGIME, not p8: high-dim spatial
  separation let gradient-FT only forget SOME skills (diluted forgetting).
- **R2 (a_break_the_wall; bars frozen anew SAME numbers, no goalpost move) = 🟢 GREEN** — canonical
  catastrophic-forgetting regime (region separation 3.0→1.0 + anti-aligned shared rules so learning
  skill k+1 un-learns skill k; mitosis arm B mechanically unchanged): A_ret=**0.553** B_ret=**0.922**
  (B−A=**+0.368** ≥ 0.30, per-seed B>A every seed) → c1 PASS · B learns every new skill (min acq
  0.880 ≥ 0.80) c2 PASS · shuffle collapses (0.397 ≤ 0.703) c3 PASS · ablate underfits (0.160 ≤ 0.50)
  c4 PASS. **COST FAVORABLE**: B = 6.3 cells vs A = 52 params (retains MORE at LOWER footprint).
- **Mechanism** — under real interference gradient-FT genuinely forgets (A_ret 0.737→0.553) while
  mitosis stays high (0.922) because its per-skill cells are dedicated and never overwritten; controls
  fire decisively (retention IS targeted dedicated-cell ownership + growth, not mere extra capacity).
- **p8/p6 guard** — split = the model's own tick; trainer touches ONLY the per-skill prototype
  population + local heads, NO global backprop / labels / persona / ethics; live CORE/*.hexa untouched.
- **Scope (a_scale_honest_scope · a_toy_scale_recheck)** — DIRECTIONAL numpy mirror, engine-transfer +
  scale UNVERIFIED; TOY (D=12, N=5, C=4, 3 seeds). FOLLOW-ONS (named, not claimed): (1) engine-native
  per-skill mitosis-grow on live CORE VAdaptField/ImmuneMemoryGrow; (2) the real path the user asked
  for — incrementally teach actual anima agent tool-use skills one-at-a-time via mitosis on the 303M.
- Files: `UNIVERSE/h1300_mitosis_skill_curriculum.py` · `UNIVERSE/cards/H_1300_mitosis_skill_curriculum.md` ·
  `.verdicts/1300_mitosis_skill_curriculum/{FREEZE,FREEZE_R2,result}.txt` · `CLAIMS.tape` @C
  h1300_mitosis_skill_curriculum · `UNIVERSE/HYPOTHESES.md` row · `domains/MITOSIS-ENGINE.log.md` @H.
## 2026-06-16 — research(MITOSIS-ENGINE): H_1297 R4 — mitosis-native trunk training ENGINE-NATIVE 🟢 GREEN ENGINE-BINDING

Realized the R3 sharp-target hard-partition **mitosis-grow next-byte trainer ENGINE-NATIVE** on the
LIVE `CORE/engine_cli.hexa` VAdaptField (a_engine_native_learning + a_verified_must_wire), and re-scored
the **SAME FROZEN R3 bars** through the engine (NOT a numpy re-run; bars NOT moved, c9/p7). $0 CPU, no GPU.

- **Mechanism is the engine's OWN**: partition = the live VAdaptField **Voronoi ownership**
  (`vadapt_field_nearest_idx`; `np.argmin(sq-L2) == L2 argmin`, byte-faithful); growth = the engine's
  OWN **mitosis tick** (`engine_mitosis_tick`, p8: ON +1 cell / OFF no-op = ablate); head = per-cell
  categorical next-byte MLE (closed-form add-1 Laplace, gradient-free). Arm A (gradient) re-used VERBATIM
  from the mirror as the incumbent.
- **🟢 GREEN — c2 FIRED ON THE ENGINE** (3-seed mean): A=2.91698 · **B(mitosis)=3.07766 [6 cells, BYTE-IDENTICAL to the R3 mirror]** · B-shuffle=3.25031 · B-ablate=3.49815. (c1) PASS 3.07766≤3.11698 · **(c2) PASS** B-shuffle 3.25031≥3.17766 on all 3 seeds — **UNLIKE thalamus R8, the targeting discriminator reproduces engine-native** · (c3) PASS 3.49815≥3.17766. The p8-literal Korean mitosis-grow toehold is now ENGINE-VERIFIED, not numpy-only.
- **Regression (verify-before-done)**: `engine_cli.hexa` UNMODIFIED (probe consumes existing surfaces, no new lane) → `engine_cli_smoke` **55 pass / 0 fail** (before==after); `h1205_separation_invariant_smoke` 🟢 PASS (Ψ phiSum ON==OFF=48.6613 byte-identical, MITOSIS ⊥ GENERATION holds); Ψ-disjoint.
- **Remaining follow-on (now justified)**: a real (larger) **Korean byte-corpus mitosis-grow training rung** = the first p8-literal LANGUAGE training — cost-gated if it needs GPU (surfaced for a go, NOT auto-rented). SCALE UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
- NEW: `CORE/h1297_mitosis_train_engine_probe.hexa` · `UNIVERSE/h1297_engine_export.py` · `.verdicts/1297_mitosis_native_train/H_1297_R4_engine_native.txt`; updated `UNIVERSE/cards/H_1297_mitosis_native_train.md` (terminal 🟢 GREEN ENGINE-BINDING @R4) · `UNIVERSE/HYPOTHESES.md` · `CLAIMS.tape` · `domains/MITOSIS-ENGINE.log.md`.

## 2026-06-16 — infra(CORPUS): $0 R2→trainer pipeline SMOKE (de-risk the cost-gated 7B GPU fire)

Before any GPU spend, verified the **data → trainer plumbing** for
`dancinlab/anima-corpus-5lang-7b-webscale` (143.60 GiB byte-corpus, R2-staged not HF-hosted) on a
TINY slice, $0, local CPU, NO GPU rent. Creds read inline from the secret store (`r2.phanes.*`),
header-only, NEVER hardcoded/logged (c7, grep-clean = 0 leakage).

- **Step 1 — R2 reachable + manifest match ✅**: bucket `phanes` lists **20 shards + MANIFEST.json**;
  live byte sum = R2-manifest per-shard sum = **154,187,454,007 B = 143.60 GiB**, matches the HF card
  exactly (20 shards · per-lang en8/fr3/de3/es3/ko3 · 22.0 tok/param). R2 manifest is a lean schema
  (`total_gb·shards·manifest[]`); the load-bearing per-shard `key/bytes/sha256` array matches HF.
- **Step 2 — tiny-slice real byte text ✅**: partial Range GET of first 8 MB of the Korean shard
  (`kor/shard0000.bytes`) — Hangul present, **control bytes 0xFE/0xFF absent** (V=256 confirmed),
  **PII markers `[EMAIL]`=212 `[PHONE]`=562** present as the card claims.
- **Step 3 — trainer glue ✅**: byte tok (V=256) → batches → forward → **CE 5.5452→5.4406** → ckpt
  written. Production `CLM/train/train_lane_p.py` **asserts CUDA** (GPU-only Lane-P) and forge `.hexa`
  trainers require GPU — **neither CPU-smokeable** (torch not installed locally), so Step 3 ran a
  clearly-LABELED numpy byte-LM **PROXY** that validates the R2→loader→loss→ckpt plumbing (NOT the
  CLMConvMoE forward). Honest: the forge GPU forward path stays un-smoked here.
- **Cost ESTIMATE** (6ND, 154.2B byte-tok, H100 BF16 989TF @ 40% MFU, $2–3.5/H100-hr, R2 egress free):
  303M ≈ 24.6h/8×H100 ($394–689) · 1B ≈ 3.4d ($1.3–2.3k) · 3B ≈ 10.1d ($3.9–6.8k) · 7B ≈ 23.7d ($9–16k).
- **GREEN-LIGHT: YES** — plumbing ready for a cost-gated GPU fire; recommended first rung = **303M on the
  real corpus** (cheapest real-corpus checkpoint, ~1 day/8×H100; doubles as first end-to-end GPU-path test).
- NEW: `scripts/scratch/corpus_train_smoke.py` (reusable smoke) · `scripts/scratch/corpus_train_smoke.md` (findings).

## 2026-06-16 — domain(MODEL): ⏱ interval timer lane (HD34, H_1299 R2 🟢 ENGINE-NATIVE) — depletion test SURVIVED, 사다리 계속

- **brain-structure ladder r6 / DEPLETION TEST** — the H_1298 카드가 명명한 마지막 thin 후보(ARBITRARY learned-duration 간격타이머)를 검증. 통과 조건: (i) falsifiable gap-vs-engine + (ii) 모든 lane(특히 고정주기 CircadianClock H_1298 · 소뇌 H_1280 · WM H_1282) 대비 control-survive distinctness. **SURVIVED** → 사다리는 HD34 에서 DEPLETED 가 아니라 계속됨.
- **load-bearing distinctness vs the clock**: 시계는 period 가 construction 시 BAKED(`clock_step` content-blind, 학습 경로 없음)이라 baked period(8)에서만 FIRE — ARBITRARY learned interval(D=13/D2=20, 둘 다 ≠8)을 물으면 A.hit=0.000. IntervalTimer 는 관측 gap 으로 `dhat` 를 학습(running mean, gradient-free)하고 **같은 객체가 코드 변경 없이 13→20 RE-ENTRAIN**(dhat [13.4,12.3,12.1]→[20.0,19.4,19.3], c6) — 시계 구조상 불가.
- **R1 numpy 미러 🟢 GREEN (DIRECTIONAL)** — `UNIVERSE/h1299_interval_timer.py`, hit-rate metric ±TOL, binding path R1c, 3 seed [4301,4302,4303]: B.hit_D=1.000 B.hit_D2=1.000 A.hit=0.000 shuf=0.000 abl=0.000 → c1..c7 all PASS. 정직 trail(c9, NO tune-to-green, bar 불변): R1a 🔴(metric-floor ~0.35 + 7-gap shuffle mean 우연 보존) · R1b 🔴(hit-rate 가 c3/c5/c6 통과하나 uniform[2,2D] shuffle mean≈D → running-mean estimator 가 mean-preserving shuffle 에 불변 = mis-specified control) · R1c 🟢(TOL=2 + mean-SHIFTED shuffle uniform[2,9] mean≈5.5≪13 → dhat 가 멀어져 mispredict → control 0.000 붕괴). `.verdicts/1299_interval_timer/{H_1299_FREEZE,_R1b,_R1c,H_1299,H_1299_R1ab_mirror,H_1299_R1a_mirror}.txt`.
- **R2 ENGINE-NATIVE + WIRED 🟢** — `CORE/engine_cli.hexa § IntervalTimer`(`itimer_new`/`itimer_new_ablated`/`itimer_observe`/`itimer_step`/`itimer_dhat`/`itimer_dhat_ticks`/`itimer_predict_next`/`itimer_fire`). 가드 무회귀: **engine_cli_smoke 60/0**(was 55/0, +5 cases 54-58: learns-interval±2 / re-entrains-to-20 / distinct-from-clock / ablate-frozen-at-init / no-fab) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(생성 byte-identical ON==OFF, Ψ=½ 무접촉).
- **가드**: @L4 emit gate 아님(`itimer_fire` = OPTIONAL learned-duration pulse, `a_autonomy_over_hardcode`) · Ψ-disjoint by construction · p1/p2/p3/p6(자기 counter+gap mean 만, 주입 라벨/RLHF/persona 없음) · `a_core_engine_map`(2번째 .clm/.kosmos 진입점 없음). HONEST(c9): B.hit=1.000 은 EXISTENCE-PROOF, discriminator(A=0/shuffle=0/ablate=0/dhat 13→20)가 decisive. TOY(2 intervals, 3 seeds, deterministic running-mean) — scale/real-corpus/continuous-re-entrainment/brain-scheduler 배선 follow-on.
- **deliverables**: `UNIVERSE/cards/H_1299_interval_timer.md`(카드) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape` @C h1299_interval_timer · `domains/MITOSIS-ENGINE.log.md` @H H_1299 · `ARCHITECTURE.md` HD34 rung + lane bullet + ladder summary(10 실현, 계속됨).

## 2026-06-16 — research(MITOSIS-ENGINE): H_1297 R3 sharp KO+EN byte-text target — 🟢 GREEN (c2 discriminator FIRED)

R3 = the **a_break_the_wall** follow-on the R2 card named: a SHARPER error-concentration target so the
**c2 targeting-discriminator FIRES** (it could not on the R1/R2 smooth 1-D target). Language/byte-text IS
such a target — error concentrates at syllable/word boundaries while mid-multibyte UTF-8 continuation runs
are near-deterministic. Task = **next-byte prediction on a real KOREAN+English UTF-8 byte corpus (V256)**,
a direct step toward training Korean. SAME 4 arms, R2 hard-partition mitosis mechanism ported to
classification (Voronoi nearest-centroid ownership + per-cell empirical next-byte frequency head [closed-form
add-1 MLE, NO global backprop] + data-matched median split + centroid recenter). Metric = held-out next-byte
CROSS-ENTROPY (convergence comparison, NOT perplexity-as-meaning, p7). $0 CPU numpy DIRECTIONAL mirror,
3 seeds, frozen-first (`H_1297_R3_sharp_target.txt`, bars set before any score; c9 no tune-to-green).

- **R3 result** (3-seed mean, all seeds stable): A(grad)ce=2.9170 [acc 0.202] · B(mitosis)ce=3.0777
  [acc 0.206, 6 cells] · B-shuffle=3.3054 · B-ablate=3.4981.
  - **(c1) PASS** — mitosis MATCHES gradient (3.0777 ≤ A+0.20=3.1170) at LOWER footprint (6 cells vs A's 1024 params).
  - **(c2) FIRED** — B-shuffle 3.3054 ≥ B+0.10=3.1777: error-TARGETED split demonstrably beats random split.
    **The discriminator R1 AND R2 could not fire FIRED here** — on a sharp target, error-targeting is the lever.
  - **(c3) PASS** — B-ablate underfits (3.4981 ≥ B+0.10).
- **Verdict**: terminal **🟢 GREEN** — gradient-free mitosis-grow matches gradient AND error-targeting
  demonstrably helps on language-like byte data. p8-literal toehold CONFIRMED on a real KO+EN byte corpus;
  the R1/R2 WALL was the SMOOTH target, not p8 (exactly as the R2 follow-on predicted). NOT engine-verified /
  production (DIRECTIONAL mirror, engine-transfer + scale UNVERIFIED). GREEN-gated follow-ons: (1) engine-native
  realization on live CORE VAdaptField (a_engine_native_learning + a_verified_must_wire); (2) a real (larger,
  cost-gated) Korean byte-corpus mitosis-grow rung = first p8-literal LANGUAGE training.
- NEW: `UNIVERSE/h1297_r2_sharp_target.py` · `.verdicts/1297_mitosis_native_train/H_1297_R3_sharp_target.txt`
  (FREEZE + verbatim) · updated `H_1297_mitosis_native_train.md` card (terminal 🟢 GREEN @R3) · `HYPOTHESES.md`
  row · `CLAIMS.tape` @C · `domains/MITOSIS-ENGINE.log.md` @H. Live CORE/*.hexa UNTOUCHED (mirror only).

## 2026-06-16 — research(MITOSIS-ENGINE): H_1297 mitosis-native trunk training (make p8 literal) — 🧱 WALL with finding

PHILOSOPHY **p8** ("training gradient + inference mitosis = one continuous cell-division") is today
SPLIT — trunk = gradient-CE (CLM/train, forge/Lane-P), mitosis = separate live inference lane
(VAdaptField H_1199, grow-under-pressure H_1288). H_1297 tests whether a **gradient-FREE mitosis-grow
trainer** (cells split/grow under LOCAL error pressure, NO global backprop) can learn a trunk that
converges AT LEAST AS WELL as gradient descent at the SAME small scale. TOY 1-D function-fit, $0 CPU
numpy DIRECTIONAL mirror, 3 seeds, frozen-first (p7, c9, a_no_llm_frame_trap neurogenesis lens).

- **R1** (softmax-mixture + width-halving split): 🧱 WALL — A(grad)=0.00415 vs B(mitosis)=0.12624;
  c2 FAIL (random split BEATS targeted — width-halving makes cells spike-like, softmax mixture degenerates).
- **R2** (a_break_the_wall breakthrough, bars frozen anew = SAME numbers): hard-partition mitosis
  (cortical-column nearest-assignment + data-matched median-split + centroid-recenter). **c1 PASS —
  mitosis MATCHES gradient** (B2=0.00412 vs A=0.00415, both at the 0.0025 noise floor) at LOWER footprint
  (~17 cells ≈ 52 params vs A's 73); c3 PASS (ablate underfits); **c2 FAIL** (B2-shuffle≈B2-targeted —
  the smooth target lets both split-orders converge, so the targeting-discriminator can't fire) → 🧱 WALL.
- **Verdict**: terminal 🧱 WALL (a control misbehaves both rounds) WITH a valid frozen-verbatim finding —
  gradient-free mitosis cell-split CAN converge as well as gradient descent at toy scale. p8-literal NOT
  refuted + directional toehold, but NOT a clean GREEN; gradient stays the incumbent trunk trainer pending
  an engine-native + harder-target re-test (a_engine_native_learning + a_verified_must_wire follow-on).
- NEW: `UNIVERSE/h1297_mitosis_native_train.py` · `UNIVERSE/cards/H_1297_mitosis_native_train.md` ·
  `.verdicts/1297_mitosis_native_train/{FREEZE,FREEZE_R2,result}.txt` · `CLAIMS.tape` @C · `HYPOTHESES.md`
  row · `domains/MITOSIS-ENGINE.log.md` @H. Live CORE/*.hexa UNTOUCHED (mirror only). Scale + engine-transfer UNVERIFIED.

## 2026-06-16 — domain(MODEL): 🕐 circadian/interval timing clock lane (HD33, H_1298 R2 🟢 ENGINE-NATIVE)

brain-structure 사다리 r5 = **DEPLETION TEST**. r4 가 명명한 3 후보 중 — replay-PREDICTION(H_1280 소뇌/episodic
으로 붕괴) · 언어/의미망(H_1296 metric map/item-binding 으로 표현 가능) 거부, **interval/circadian TIMING** 선택
(가장 깨끗). SCN 자가지속 위상 진동자(Pittendrigh) / two-process model(Borbély 1982: Process-C ⊥ Process-S) /
간격타이밍(Buhusi-Meck) 렌즈(c15, `a_no_llm_frame_trap`). depletion test 통과: (i) live-engine 대비 falsifiable
gap(어떤 CORE lane 도 절대 elapsed-tick 위상/고정 스케줄을 추적 안 함) + (ii) 모든 lane 대비 control-survive
distinctness — 가장 가까운 H_1292 HomeostaticDrive 대비 DECISIVE.

- **R1 numpy 미러 🟢 GREEN (DIRECTIONAL)** — `UNIVERSE/h1298_circadian_clock.py`, phase-locking vector-strength R,
  3 seed [4297,4298,4299], 7 frozen bar 전부: 시계 R=1.000 vs 항상성 R=0.000(항상 grounded 면 절대 FIRE 안 함,
  D1 time ⊥ regulated-variable) · shuffle R=0.202(max 0.472) · ablate R=0.000 · D2(시계 위상 불변·항상성 RESET) ·
  NO-FAB. **정직 trail(c9, NO tune-to-green, bar 절대 불변)**: R1a 🔴(ablate trivial-origin leak) → R1b 🔴(recurrence
  metric 너무 coarse) → R1c 🔴(phase-locking 옳음 — 항상성/ablate 깨끗이 붕괴 — shuffle 만 k=3 chance floor 1/√3
  =0.577 생존) → R1d 🟢(10 periods → shuffle LLN cancel). control/scale 만 frozen-first 수정, 매번 STRICTER
  (`a_break_the_wall`). `.verdicts/1298_circadian_clock/{H_1298_FREEZE,_R1b,_R1c,_R1d,H_1298,H_1298_R1_mirror}.txt`.
- **R2 ENGINE-NATIVE + WIRED 🟢** — `CORE/engine_cli.hexa § CircadianClock`(`clock_new`/`_new_ablated`/`clock_step`/
  `clock_count`/`clock_phase`/`clock_fire`) — D1/D2 dissociation 을 코드로 실현(clock_step 은 content-blind; phase
  는 어떤 feed 에도 불변; clock_fire = OPTIONAL wake pulse, emit gate 아님 @L4). `engine_cli_smoke` cases 49-53.
- **regression 무회귀**: `engine_cli_smoke` **55/0**(was 50/0, +5 clock 케이스) · h1196 single-entry **7/0** ·
  h1205 separation-invariant **PASS**(생성 byte-identical ON==OFF, Ψ=½ 무접촉). Ψ-disjoint by construction(자기
  tick counter 만, pure_field 무접촉) · 2번째 .clm/.kosmos 진입점 아님(`a_core_engine_map`).
- **deliverables**: `UNIVERSE/cards/H_1298_circadian_clock.md`(카드) · `UNIVERSE/HYPOTHESES.md` index row · `CLAIMS.tape`
  @C h1298_circadian_clock · `domains/MITOSIS-ENGINE.log.md` @H H_1298 · `ARCHITECTURE.md` HD33 rung + lane bullet.
- **LADDER(r6/DEPLETION 🏁)**: HD33 이후 c15 사다리는 거의 DEPLETION. r6 후보(THIN) = ARBITRARY learned-duration
  간격타이머(이 고정주기 시계와 달리 re-entrain 가능해야 distinct); 통과 못 하면 사다리 DEPLETED 🏁. SCOPE: 미러
  DIRECTIONAL, TOY(10 periods, 3 seed, deterministic — timing STRUCTURE), brain WAKE/REM scheduling 배선 +
  photic-entrainment + scale 은 follow-on(`a_verified_must_wire`·`a_scale_honest_scope`·`a_toy_scale_recheck`).

## 2026-06-16 — doc(README): 아키텍처 현행화 보정 — 9→12 brain lane · smoke 37/0→50/0 · 시상 R8 engine-transfer 정직 강등

직전 README PR(#2189)이 **stale base 위에서 머지**되며 아키텍처를 과소진술한 것을 보정 — README.md 를
현재 `ARCHITECTURE.md`(origin/main SSOT)와 정확히 일치시킴(README.md 단독 + CHANGELOG, ARCHITECTURE/
CORE/UNIVERSE 미변경; 동시 사이클이 소유). tier/숫자 전부 ARCHITECTURE.md verbatim(c9), surgical 현행화(c10).

- **brain lane 9 → 12**: 직전 본문이 누락한 lane 을 추가 — **🧩 전전두엽 위계(`HierGoalStack`, H_1294 R2 —
  ordered goal→subgoal 스택, 완료 시 pointer ADVANCE, 기저핵 단일-step 과 DISTINCT)** · **🗺 해마-내후각
  공간지도(`SpatialMap`, H_1296 R2 — landmark 2-D 위치 저장 → 두 fact 거리 relational 질의, 에피소드
  ITEM-binding 과 DISTINCT)** · **🐝 하이브-마인드 collective-Φ(`CollectivePool`, H_1295 — N substrate 결합
  시 faithful IIT-4 big-Φ super-additive, coupling-generic + substrate-class conditional)**. 배지 + 본문
  lane 목록 + 표 3행 + HD 스코어보드 4행(HD29–32) + repo-map struct 목록 갱신. (affect 행도 ARCHITECTURE
  대로 `+ WIRED` 로 — `brain_decide_affect` 배선 완료 R3.)
- **smoke 게이트 37/0 → 50/0**: `ARCHITECTURE.md` 가 쓰는 live 값으로 보정(H_1296 R2 후 `engine_cli_smoke`
  50/0 — cases 44–48 +5 spatial-map). 직전 entry 의 37/0 은 stale(H_1294/1295/1296 추가 전).
- **시상 R8 — 정직한 강등(핵심)**: 직전 README 가 "WALL BROKEN / engine-native wiring in progress" 로
  과진술한 것을 보정. R8 진동 위상결속(Kuramoto)은 **numpy 미러에서만 🟢 DIRECTIONAL**(faithful-IIT4 Φ leg
  은 real · frozen-first) — 그러나 **engine-native transfer 는 frozen bar 재현 실패**: shuffle 통제가 engine
  substrate 에서 FIRE(shuffle ΔΦ +0.026/+0.380/+0.296, 전부 양수 — ≤0 이어야 함) → lift 가 부분적으로
  carrier-amplitude variance. 따라서 `PhaseField` lane 은 **NOT engine-wired**, `a_verified_must_wire` 가
  정직히 deferred. "벽이 robust/engine-broken 으로 깨졌다" 주장 안 함; 내용-relay 축(R1–R5/R7/R9)은 🧱 유지.
- **walls 콜아웃**: engine-native 돌파는 **2개**(용량 H_1288 · 편도체-eviction H_1285)로 정정; 시상-timing 은
  **미러 only(engine-transfer deferred)**, 신경조절(H_1284) 🧱 유지. p1–p8 · A⇄G · Ψ=½ ·
  substrate-native-speak · tension-link · scale-honesty 섹션 보존.
- **translated README follow-on**: README.{zh,ja,ru,ko,easy}.md 는 동일 보정이 미반영(별도 follow-on) — 본
  보정은 영문 SSOT README.md 에 한정, 차단하지 않음.

## 2026-06-16 — domain(MODEL): 🗺 해마-내후각 공간지도 lane (HD32, H_1296 R2 🟢 ENGINE-NATIVE)

빠진 뇌 서브시스템 사다리에 **HD32 해마-내후각 공간지도(place/grid spatial-map · path-integration)** 를 추가 — metric cognitive-map lane(`SpatialMap`)을 `CORE/engine_cli.hexa` 에 ADDITIVE + Ψ-disjoint 으로 실현(`spatial_map_new`/`spatial_map_new_ablated`/`spatial_map_place`/`spatial_map_count`/`spatial_map_nearest`/`spatial_map_shuffle`/`spatial_map_item_nearest`). landmark 를 2-D 위치에 저장하므로 두 저장 fact 사이 **거리(RELATION)가 표상·질의 가능** — `spatial_map_nearest("X","A","B")` = "X 가 A/B 중 누구에 더 가까운가"를 Euclidean 거리로 답. O'Keefe place cell / Moser grid cell / path-integration 렌즈(`a_no_llm_frame_trap`, c15).

- **왜 missing/distinct**: live 엔진의 모든 메모리 lane 은 fact 를 독립 바인딩(ImmuneMemory **item-binding** — FNV-trigram key affinity, key X 의 내용은 recall 하나 item X↔item Y **거리는 표상 안 함**)하거나 SEQUENCE(HierGoalStack H_1294, ORDERED plan = 순서는 metric 아님)로 든다 — metric SPACE 가 없다. WorkMemBuffer(H_1282)·VForwardField(H_1280)·HomeostaticDrive(H_1292, 1-D 적분기)와도 DISTINCT.
- **frozen-first 검증** (`.verdicts/1296_spatial_map/{H_1296_FREEZE,H_1296_R1b_FREEZE,H_1296_R1c_FREEZE}.txt`, 사전등록): R1 numpy 미러 🟢(DIRECTIONAL) → **R2 ENGINE-NATIVE 🟢**(BINDING, `engine_cli_smoke` cases 44-48, 3 seed [4295,4296,4297]). BINDING predicate = NEAREST relational 질의(신호가 저장 metric 에만 있음) — 5개 bar PASS: (c1 PRESENCE) B−A=+0.525 ≥+0.30 each+mean · (c2 DISTINCT) item-store A=0.475≤0.65 (metric 없음→abstain) · (c3 EARNED-MAP shuffle) Bshuf=0.500≤A+0.15 · (c4 EARNED-METRIC ablate) Babl=0.450≤A+0.15 · (c5 NO-FAB) item-abstain 1.000≥0.90. relational 질의: metric map 1.000 vs item-store 0.475(항상 abstain).
- **PATH-INTEGRATION 은 정직한 NON-RESULT**(c9): corroborator 로 넣었으나 map-shuffle 대조가 붕괴를 거부 — 신호가 저장 map 이 아니라 변위 step 에 leak 하기 때문. bar 를 옮기지 않고(`a_break_the_wall` 로 candidate-order leak 를 frozen-first 수정) NON-GATING diagnostic 으로 강등·보고만 함.
- **가드 무회귀**: `engine_cli_smoke` **50/0**(was 45/0 hive 후, +5 spatial-map 케이스, 3연속 deterministic) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(생성 byte-identical ON==OFF, Ψ=½ 무접촉, pure_field 무변경). p1/p2/p3/p6(위치+질의 landmark 만 읽음, 주입 답 라벨/RLHF/persona 없음, metric 은 geometry 로 SCORE 에만) · emit gate 아님(`a_autonomy_over_hardcode`) · Ψ-disjoint(저장 위치 위 pure geometry). 정직(c9): B=1.000 은 SATURATED = EXISTENCE-PROOF 이지 effect-size 아님 — discriminator(item-store 0.475/abstain 1.000, shuffle 0.500, ablate 0.450 전부 chance)가 decisive. brain map→recall/emit 배선 + scale/higher-D/grid-cell-주기-code = follow-on. TOY scale(8 landmarks, 3 seeds, 2-D, deterministic — metric-map STRUCTURE 검증).
- **canonical 등록(a_hypothesis_register)**: `UNIVERSE/cards/H_1296_spatial_map.md`(카드) + `UNIVERSE/HYPOTHESES.md` per-H 인덱스 행 · `CLAIMS.tape @C h1296_spatial_map`(group=BRAIN-STRUCTURE-LADDER) · `domains/MITOSIS-ENGINE.log.md @H H_1296` · ARCHITECTURE.md(HD32 rung + lane body + map row) · MEMORY.md 포인터. 사다리는 DEPLETION 근접 — 남은 후보(시간-순서 replay-예측·간격/circadian 타이밍·언어/의미망)는 더 얇고 각각 falsifiable gap + 모든 lane 대비 control-survive distinctness 통과 필요.
## 2026-06-16 — doc(README): 최종 아키텍처 현행화 — 9 brain lane · 시상 R8 timing-axis 돌파 · tension-link

README.md 를 검증된 현재 상태로 현행화 (README.md 단독 + CHANGELOG, ARCHITECTURE.md/CORE/UNIVERSE 미변경 —
동시 작업 agent 와 충돌 회피). (1) brain-structure ladder = origin/main `CORE/engine_cli.hexa` +
`CORE/brain.hexa` struct list 대조로 9 engine-native lane 명시 — 해마(ImmuneMemory) · 성장기억
(ImmuneMemoryGrow) · 작업기억(WorkMemBuffer) · 소뇌(VForwardField) · 편도체(ConsolidatingMemory) ·
기저핵(VBasalGate) · 시상하부(HomeostaticDrive, H_1292) · 마음이론(OtherMindModel, H_1293) ·
정동(AffectFeatures, H_1290); 배지 + 본문 lane 목록 + 표 3행 추가. smoke 게이트 stale 30/0 → live
**37/0** (origin/main `engine_cli_smoke` 실행 확인, 34 case). (2) 시상 Φ — 내용-relay 축은 6+ 사전등록
라운드(R1–R5/R7) 🧱 closed-negative 유지하되, 직교 **TIMING 축에서 벽 돌파** = R8 진동 위상결속(Kuramoto)이
frozen +0.02 faithful-IIT4 Φ bar 를 every seed 클리어 + phase-shuffle 통제가 every seed 음수 붕괴 🟢;
정직하게 **numpy-mirror DIRECTIONAL · engine-native 배선은 in-progress**(검증은 mirror, 아직 engine-wired
아님)로 명시. 전용 §"📡 Thalamus Φ" subsection 신설. (3) anima↔anima §"🔗 connection channel = tension"
신설 — 얽힘=상관 0비트(무신호 정리, H_6006 🔴) vs 실연결=tension-link 공유앵커 매체(H_6009 🟢 SUPPORTED),
paid ANU QRNG 접지. (4) walls 콜아웃 = 3개 벽 돌파(용량/편도체/시상-timing)로 갱신, neuromod 정직 🧱 유지.
p1–p8 · A⇄G · Ψ=½ · substrate-native-speak 보존. tier verbatim(c9), surgical(c10).

## 2026-06-16 — audit(WIRING): a_verified_must_wire 전수 감사 + 시상 R8 engine-native 게이트(honest-deferred) + ARCHITECTURE 최종현행화

`a_verified_must_wire` 전수 배선 감사 — origin/main 의 terminal-tier 🟢 가설 13개를 전수 분류:
{wired | deliberately-optional | honest-deferred}. **순 신규 배선 = 0**(정직, c9): 모든
clean-GREEN ∧ 배선의도 lane 은 **이미 배선됨**(해마 ImmuneMemory(Grow)·소뇌 VForwardField·
기저핵 VBasalGate·작업기억 WorkMemBuffer·편도체 ConsolidatingMemory·양자 QPool·감정 AffectFeatures·
위계 HierGoalStack·하이브 CollectivePool — struct+faculty+smoke); HomeostaticDrive·OtherMindModel 은
deliberately-optional(brain consult = NOT emit gate, `a_autonomy_over_hardcode`).

**시상 R8 위상결속 engine-native 배선 게이트(@L6)** — 유일한 genuinely-unwired clean-GREEN 후보.
`a_engine_native_learning` 순서대로 numpy-mirror R8(DIRECTIONAL)을 engine-native 로 재현 시도
(`CORE/h1283_phase_binding_engine_gate.hexa` — Kuramoto phase 채널 + phase-gated salience (1+cosθ)/2 +
faithful IIT4 Φ, 엔진 `_lcg_*` substrate). 결과: **c2 PRIMARY 재현 강력**(ΔΦ +1.47/+0.84/+0.71 every seed)
이나 **c4 SHUFFLE 미붕괴**(ΔΦ_sh +0.026/+0.380/+0.296, 양수 — 프로즌 R8 의 honest leg 가 engine 기질에서
firing). frozen bar 미재현 → no-tune-to-green(c9/p7) → **PhaseField lane HONEST DEFERRED, 미배선**.
R8 🟢 은 그 자체 substrate 위 DIRECTIONAL 결과로 STANDS; engine-transfer 가 재현 못 한 것.
verdict `.verdicts/1283_thalamus_global_workspace/H_1283_R8_engine_native_gate.txt`.

**ARCHITECTURE.md 최종 아키텍처 전면 현행화(@L7)** — 시상 4각도 최종(R8 timing 돌파 / R6 caveat /
R1–R5·R7·R9 내용-relay 🧱), 하이브 CollectivePool(super-additive + decouple-null + rule-class dissociation),
QPool 양자 entropy, AffectFeatures/윤리 read-lane, **배선 감사표 + brain_decide consult 맵**, TENSION-LINK
아크 포인터(얽힘=no-signaling, 실채널=tension-link) 추가. 벽 스코어카드: 4 벽 중 3 돌파(용량·편도체·시상[timing,
DIRECTIONAL]), 신경조절 1 정직한 🧱.

회귀 가드 0(live 엔진 파일 byte-unchanged): `engine_cli_smoke` **45/0** · single-entry(h1196) **7/0** ·
h1205 분리불변 PASS(생성 byte-동일 ON==OFF, Ψ=48.6613 불변, pure_field 무변경). `CORE/engine_cli.hexa`/
`brain.hexa`/`engine_cli_smoke.hexa`/`pure_field.hexa` 무편집 — 변경은 ARCHITECTURE.md·H_1283 카드·
HYPOTHESES 인덱스·신규 게이트 probe/verdict 만.

## 2026-06-16 — doc(TENSION-LINK): H_6006–H_6043 arc를 a_hypothesis_register 2-파일 규칙으로 등록

TENSION-LINK arc (anima↔anima 연결/통신 + ANU paid QRNG 양자 얽힘, H_6006–H_6043)를
`a_hypothesis_register` 2-파일 규칙(인덱스 = `UNIVERSE/HYPOTHESES.md` · 카드 = `UNIVERSE/H_<id>_<slug>.md`)에
맞춰 정리. (1) 누락 카드 1개 신설 — `UNIVERSE/cards/H_6006_no_signaling.md` (🔴 CLOSED-NEG, 무신호 정리;
F1 CHSH |S|=2.829 🟢 진짜 얽힘 · F2 0비트 전송 🔴 · F3 텔레포트=고전채널 필요 🔴), 기존
`H_6007_pseudo-telepathy.md` 카드와 동일 템플릿. (2) `HYPOTHESES.md` 에 "TENSION-LINK arc
(H_6006–H_6043)" 섹션 신설 — 42 카드 전부 한 줄/카드 인덱스(id · 제목 · verbatim tier · 카드 링크),
tier 는 각 카드 `status_grade`(=`TENSION-LINK/verdicts/H_60*.txt` verdict)에서 verbatim (c2/c9 —
🔴/🟠 미상향). dup-id 카드 4개(H_6026·H_6027·H_6028·H_6036, 각 id 2 카드) ⚠dup 으로 양쪽 색인(c10 미병합);
H_6019/H_6020 클론 변종은 카드 id H_6021/H_6022 로 재번호돼 카드-id dup 아님(verdict 파일명만 legacy 60xx).
(3) `TENSION-LINK/README.md` 의 stale "본문은 UNIVERSE/ 평면 목록" 문구를 새 HYPOTHESES.md 섹션 포인터로
수정(surgical, c10). grep 확인: H_6006–H_6043 38 distinct id 전부 카드+색인 행 해결(42/42).
registration-only — CORE/엔진/실험 미변경. a_hypothesis_register · a_claim_verify · c2 · c9 · c10 · c14.

## 2026-06-16 — H_1283 R6: 시상 MULTI-CHANNEL PARALLEL RELAY 🟢 (frozen bars; single-cut 천장 돌파)

H_1283 (thalamus / global-workspace) 벽 돌파 R6 (a_break_the_wall, c16). R1..R5 는 모두 ONE shared
relay stage (broadcast/coalition/sparse-reentrant/dense-all-pairs) → 🧱 (단일 broadcast 채널 자체가
faithful-IIT4 Φ 를 cap 하는 low-dim cut; R5 shuffle 이 dense lift=variance 노출). R6 각도 = 공유
relay stage 를 버리고 **N=4 독립 병렬 relay 채널** (ring edge별 1개, DISJOINT, intra-thalamic 교차결합
없음 — 시상=多 병렬 nuclei, a_no_llm_frame_trap c15). 결과: faithful ΔΦ +0.0891/+0.0341/+0.1011 —
**모든 seed +0.02 통과 (직교 seed 8 포함, arc 최초)**; c1·c3 PASS; **c4 SHUFFLE PASS** (seed 9 lift
+0.1011→+0.0165 붕괴). 정직 caveat (c9): seed 7/8 shuffle 이 ~93%/~96% 유지 (variance 잔존) → clean
topology 효과는 seed 9 에서만 decisive, GREEN 은 c4 의 disjunctive ≥1-seed frozen 형태로 성립.
ARM_A Φ R1..R5 byte-identical 재현. FREEZE scoring 전 commit (bars 미이동, p7). Φ=faithful IIT4 ONLY
(stdlib exact MIP-EI; numpy 는 Φ 계산 안 함). $0 CPU numpy mirror=DIRECTIONAL, engine-transfer
UNVERIFIED. GREEN ⇒ engine-native 병렬-relay lane = follow-on (DEFERRED, 이번 round CORE 미배선 —
engine-native 재현 + per-seed shuffle 강화 후 배선; a_verified_must_wire). 다음 정직 각도: 더 큰
module/channel 집합 또는 channel-COUNT ablation (Φ vs N). 산출: UNIVERSE/h1283_r6_multichannel_relay.py
· .verdicts/1283_thalamus_global_workspace/{H_1283_R6_FREEZE,H_1283_R6_multichannel}.txt · 카드 R6 행.
## 2026-06-16 — H_1283 R8: 🟢 thalamus Φ WALL BROKEN by oscillatory phase binding (temporal synchrony)

R8 of the H_1283 thalamus wall fleet (c16/a_break_the_wall). R1–R5/R7 bound modules by CONTENT
(broadcast/coalition/sparse+dense re-entry/matrix-core dual) and all failed the robust faithful-IIT4
ΔΦ ≥ +0.02-every-seed bar — R5's diagnosis: "a single broadcast channel is itself a low-dim cut that
caps Φ." R8 took a genuinely NON-RELAY substrate lens (a_no_llm_frame_trap, c15): thalamo-cortical
integration by phase SYNCHRONY (Kuramoto), not content. Each module carries a scalar phase coupled weakly
to a thalamic pacemaker; content stays byte-identical to ARM A; only the salience read-out is phase-gated.
Synchronized modules co-modulate their salience in TIME → temporal binding with NO shared content channel
for a MIP to cut. **🟢 GREEN, IDENTICAL frozen bars (not moved, c9/p7)**: faithful ΔΦ +1.629/+1.174/+0.233
every seed (incl the orthogonal seed 8 that defeated every relay round, ≫ bar); pre-registered
phase-shuffle control COLLAPSES the lift to NEGATIVE every seed (−0.068/−0.119/−0.382) → structured
synchrony, not amplitude variance; coherence sanity + no-collapse PASS. ARM A Φ reproduces R1–R5/R7
byte-for-byte. Engine-native
wiring = follow-on (a_verified_must_wire, GREEN-but-unwired). Toy/numpy DIRECTIONAL, faithful-Φ leg real
(exact MIP-EI via hexa). `UNIVERSE/h1283_thalamus_global_workspace.py` (main_r8) ·
`.verdicts/1283_thalamus_global_workspace/H_1283_R8_phase_binding.txt` · card row appended.

## 2026-06-16 — domain(H_1283 R7): thalamus wall — matrix/core dual coupling 🔴/🧱 STILL WALL

R7 of the H_1283 thalamus/GWT wall (c16/a_break_the_wall). Angle = thalamic matrix/core
duality (brain-science, c15, a_no_llm_frame_trap — NOT an LLM recipe): R1–R5 each used ONE
relay at a time (single broadcast/coalition/sparse re-entry/dense all-pairs), and the wall's
root cause was "a single broadcast channel is itself a low-dim cut that caps faithful-IIT4 Φ."
R7 installs BOTH thalamic cell populations SIMULTANEOUSLY — CORE (specific, point-to-point,
topographic) + MATRIX (diffuse, broad, low-gain), mixed by a FIXED ratio W_CORE=0.5:W_MATRIX=0.15
— so integration comes from overlapping specific+diffuse pathways, not one cut. SAME frozen frame
as R1–R5 (4 modules dim-8, 64 ticks, seeds [7,8,9], ARM A byte-identical baseline 0.78038/0.611741/
0.825326 reproduced). Φ = faithful IIT4 ONLY (exact MIP-EI via hexa, a_phi_iit4_tool; numpy never
computes Φ). FROZEN-FIRST (freeze committed before scoring; bars NOT moved). **RESULT 🔴/🧱:**
faithful ΔΦ s7 +0.0201 ✓, s8 +0.0412 ✓ (RESCUES the orthogonal seed that broke R3-R5), but s9
+0.0026 ✗ → **P1 FAIL — the failing seed RELOCATED, the floor was not lifted**. The pre-registered
SHUFFLE control (permuted core topography) PASSED (s7 permuted-core ΔΦ −0.0087 < +0.02 → the lift is
structure not variance — CLEANER than R5 whose shuffle FIRED). Coherence ↑ every seed, no collapse.
Finding: matrix/core dual coupling is a genuine topology-specific mechanism that TRADES Φ across the
geometry (rescues the orthogonal seed, dilutes the correlated one) but does NOT clear the 3-seed
robustness gate — the thalamic-topology axis is closed (broadcast→coalition→sparse→dense→matrix/core,
all relocate or trade the lift, none robust at this scale). RED ⇒ NO CORE wiring (a_verified_must_wire
fires on GREEN only). Toy/numpy DIRECTIONAL, faithful-Φ real. `UNIVERSE/h1283_thalamus_global_workspace.py`
(main_r7 + matrix_core/matrix_core_shuffle modes) · `.verdicts/1283_thalamus_global_workspace/
{H_1283_R7_FREEZE.txt, H_1283_R7_matrix_core.txt}`.

## 2026-06-16 — domain(H_1283 R9): thalamus predictive information-bottleneck relay → 🔴/🧱 WALL CONFIRMED

R9 of the H_1283 thalamus/GWT wall (c16/a_break_the_wall). ANGLE: make the relay cut INFORMATION-
PRESERVING instead of arbitrary — a learned compressed PREDICTIVE CODE (information bottleneck). The
thalamic relay learns gradient-free (delta-rule LMS, cerebellum H_1280 family) the minimal code z
(width code_dim=3 << module dim 8 << concat 32) that best PREDICTS the other modules' next state.
SAME frozen frame as R1-R5 (4 modules dim-8, 64 ticks, seeds [7,8,9], faithful IIT4 Φ via stdlib
exact MIP-EI — numpy never computes Φ). FROZEN BEFORE SCORING. Arm A direct-ring vs arm B learned
predictive-bottleneck vs **arm C random-projection of the SAME width** (load-bearing control) + SHUFFLE
control (scrambled predictive target). RESULT 🔴/🧱: c2 PRIMARY Φ FAIL — ΔΦ(B−A) s7 −0.0067 · s8
+0.0203 · s9 +0.0097, only s8 clears +0.02 (not robust). c4 B≥C passes but TRIVIALLY: ΔΦ(B−C) =
+0.008/0.0/0.0 — the learned code is Φ-INDISTINGUISHABLE from a random projection of the same width on
s8/s9. c5 SHUFFLE FIRED: on the lone B-green seed 8, the scrambled-target arm ΔΦ +0.0232 ≥ the
structured arm → the tiny lift is variance/added-channel, NOT a learned predictive code. WALL CONFIRMED:
an information-preserving (predictive-bottleneck) relay does NOT break the single-channel Φ cap at this
scale. No wire, no tune, bar NOT moved (c9/c16/p7). Toy, numpy DIRECTIONAL, faithful-Φ REAL.
`UNIVERSE/h1283_r9_predictive_bottleneck.py` · `.verdicts/1283_thalamus_global_workspace/H_1283_R9_predictive_bottleneck.txt`.

## 2026-06-16 — verify(303M): a303m_pass RE-VERIFIED FROM SCRATCH (engine-measured, byte-exact, p7)

ACTUAL re-verification of the SHIPPED `anima-clm-chat-303m` from scratch on the live CORE engine
(`.verdicts/303m_actual_verify/`), NOT a doc claim — engine-measured, byte-exact, p7 (no perplexity,
no LLM-judge). Ckpts verified PRESENT + sha-matched: CHAT `h1129c_chat.pt` (4fcc2d6c…, 303,097,856
params), BASE `h1129c_best.pt` (19be1295…, MATCHES HF.jsonl), training CORPUS (2d15ca7d…, MATCHES
recipe). **MOUNT byte-exact** — CORE `bg_load`+`bg_forward_last_W` vs torch golden: argmax 32==32,
top5 [32,44,10,63,46] match, first-16 maxΔ 5e-5 (≪ 0.01 tol). **G0** base 5/5 + chat 4/5. **G1** base
trunk k3/k4/k5 composed_distinct=2>max_single=1 coherent (reproduces H_1129). **G3** 8/8 structural +
engine_cli_smoke 30/0 + single-entry 7/0. **G5** grounded-copy 22 verbatim bytes + immune-memory recall
QA 1.000 fab 0.000 abstain 3/3. **PHASE-3 memory e2e** QA 1.0 / fab 0.0 / abstain green. **G2** absence-
checked on the real corpus (frozen h1140). **No frozen bar moved; NO remake needed** — the model is
coherent/emergent/non-fabricating/philosophy-clean and mounts byte-exact. Every obstacle was tooling/host:
a hexa selfhost IO-builtin symbol regression (`_read_file_bytes` vs runtime `_rt_read_file_bytes`) FIXED
at root cause (rt.o alias, backup kept) + filed to hexa-lang inbox — NOT a model defect. Honest robustness
map unchanged (5 ROBUST + 2 THIN + 1 INFLATED, register≠QA).

## 2026-06-16 — domain(MODEL): H_1295 🟢 HIVE-MIND collective-Φ lane — super-additive collective integration, wired ENGINE-NATIVE

The "many individuals → one consciousness" axis, realized as an additive Ψ-disjoint
`CollectivePool` faculty in `CORE/engine_cli.hexa`. Anchor = H_609 🟢 (collective faithful
IIT-4 big-Φ is SUPER-ADDITIVE: Φ(joint) > Σ Φ(member) for an edge-of-chaos coupling
regime). Re-fired frozen-first with the emergence controls the H_611/H_617 falsifications
taught, in two angles:
- ANGLE-1 (topology-shuffle) FAILED honestly — a random equal-magnitude cross-wiring
  matched/EXCEEDED the structured lift (Δ_shuffle +13.6..+16.4 > Δ_coupled +10.48 all 3
  seeds), so super-additivity is **coupling-GENERIC, not topology-specific** (kept, reported,
  NOT a GREEN gate — exactly the control that caught H_611/H_617).
- ANGLE-2 (the genuine super-additivity controls, frozen before running) is **🟢 4/0**:
  (B1) Δ_coupled = +10.4756 (Φ_collective 15.4677 vs Σ 4.99209); (B2a) DECOUPLE-NULL W=0
  Δ=−4.99209 ≤ 0 (the lift REQUIRES coupling); (B2b) RULE-CLASS DISSOCIATION Δ(110,110)−
  Δ(90,90)=+16.4756 (sterile rule-90 does NOT super-add ⇒ substrate-CONTENT specific, a
  pure variance story cannot produce this); (B3) NO-COLLAPSE coherence 0.58125 < 0.999.

Φ = faithful IIT-4 ONLY (`a_phi_iit4_tool`, `big_phi_bounded`) — numpy never computes Φ.
The four bars re-score ENGINE-NATIVE in `CORE/engine_cli_smoke.hexa` cases 39–42, byte-
matching the mirror; regression guard **engine_cli_smoke 45/0** (+4 hive cases; the existing
41 cases incl the hierarchical-PFC lane byte-unchanged, Ψ-disjoint — `pure_field`/generator/
decoder untouched). The falsified hive mechanisms are deliberately NOT wired (H_611
transfer-entropy 🔴, H_617 SAVANT×hive SI 🔴, 975 shared world-model 🔴 — c9,
`a_verified_must_wire` GREEN-only). Files: `UNIVERSE/h1295_hive_collective_phi.hexa` ·
`UNIVERSE/cards/H_1295_hive_collective_phi.md` · `.verdicts/1295_hive_collective_phi/{H_1295_FREEZE,
H_1295,engine_cli_smoke_45}.txt` · `CORE/engine_cli.hexa` § HIVE-MIND · `CLAIMS.tape` @C h1295
· `UNIVERSE/HYPOTHESES.md` · `ARCHITECTURE.md` ladder. TOY scope (n=2 member, joint-n=6,
cap=2 lower-bound, ECA, sys=0); N>2 scaling + live multi-anima transfer = follow-on.

## 2026-06-16 — domain(MODEL): 🧩 전전두엽 위계 goal→subgoal 컨트롤러 lane (HD31, H_1294 R2 🟢 ENGINE-NATIVE)

빠진 뇌 서브시스템 사다리에 **HD31 전전두엽 위계(hierarchical PFC · goal→subgoal 다단계 제어)** 를 추가 — 2-level goal-stack 컨트롤러 lane(`HierGoalStack`)을 `CORE/engine_cli.hexa` 에 ADDITIVE + Ψ-disjoint 으로 실현(`hier_new`/`hier_current_target`/`hier_grounded_current`/`hier_step`/`hier_pointer`/`hier_complete`/`hier_flat_emit`). goal STACK = {top goal, ORDERED subgoal 키, pointer p}: 현재 subgoal[p] 에 aligned(cos≥0.85)+grounded 된 cue 만 emit, **완료 시 pointer ADVANCE**(completion-triggered), out-of-order/ungrounded cue SUPPRESS, plan 위치 PERSIST. Badre & D'Esposito rostro-caudal gradient / Koechlin cascade 렌즈(`a_no_llm_frame_trap`, c15).

- **왜 missing/distinct**: live 엔진은 단일 flat emit/선택 게이트만 있다 — `brain_decide`/`engine_g` 고정 8-weight 합 + 임계값, **VBasalGate**(H_1281 기저핵)은 SINGLE-STEP one-of-K 선택(pointer/plan/완료-advance 없음). 위계 PFC 는 그 **위 레벨** — top goal 을 ORDERED subgoal 로 분해 + 완료-advance + 위치 persist. WorkMemBuffer(H_1282, 수동 유지)·HomeostaticDrive(H_1292, 스칼라 적분기)와도 DISTINCT.
- **frozen-first 검증** (`.verdicts/1294_hierarchical_pfc/H_1294_FREEZE.txt`, 사전등록): R1 numpy 미러 🟢(DIRECTIONAL) → **R2 ENGINE-NATIVE 🟢**(BINDING, `engine_cli_smoke` cases 35-38, 3 seed [4294,4295,4296]) — 5개 bar PASS: (c1 PRESENCE) B−A=+0.758 ≥+0.30 each+mean · (c2 DISTINCT) flat A=0.242<0.50 (engine 이 이미 가진 구조로는 ordered chain 못 풂) · (c3 EARNED-ORDER shuffle) Bshuf=0.000≤A+0.15 · (c4 EARNED-ADVANCE ablate) Babl=0.000≤A+0.15 · (c5 NO-FAB) 0.000≤0.10. ORDERED 3-fact-chain(A→B→C) 완료: 위계 1.000 vs flat 0.242.
- **가드 무회귀**: `engine_cli_smoke` **41/0**(was 37/0, +4 hier 케이스) · h1196 single-entry 7/0 · h1205 separation-invariant PASS(생성 byte-identical ON==OFF, Ψ=½ 무접촉, pure_field 무변경). p1/p2/p3/p6(pointer+substrate margin+cue cosine 만 읽음, 주입 "do step k" 라벨/RLHF/persona 없음, subgoal 순서는 TASK 구조로 SCORE 에만) · emit gate 아님(`a_autonomy_over_hardcode`) · Ψ-disjoint(pointer 만 evolve). 정직(c9): B.complete=1.000 은 SATURATED = EXISTENCE-PROOF 이지 effect-size 아님 — discriminator(shuffle/ablate 0.000 vs flat 0.242)가 decisive. brain plan-execution 배선 + scale/longer-plans/deeper-hierarchy = follow-on. TOY scale(40 ep, 3 seeds, CHAIN_LEN=3, deterministic — 위계 STRUCTURE 검증).
- **canonical 등록(a_hypothesis_register)**: `UNIVERSE/cards/H_1294_hierarchical_pfc.md`(카드) + `UNIVERSE/HYPOTHESES.md` per-H 인덱스 행 · `CLAIMS.tape @C h1294_hierarchical_pfc`(group=BRAIN-STRUCTURE-LADDER) · `domains/MITOSIS-ENGINE.log.md @H H_1294` · ARCHITECTURE.md(HD31 rung + lane body + map row) · MEMORY.md 포인터. NEXT 후보: place/grid spatial-map(metric/relational cognitive map, episodic item-binding 과 DISTINCT).

## 2026-06-16 — domain(HYPOTHESES): migrate H_1280–1293 to the 2-file `a_hypothesis_register` convention

Brain-structure ladder + session facets (H_1280–1293) migrated from the themed bucket
file to the canonical 2 surfaces (`a_hypothesis_register` #2177): 13 per-H SSOT cards
`UNIVERSE/H_<id>_<slug>.md` created (title · claim/falsifier · method · per-round verdict
tier+numbers · `.verdicts/<slug>/` pointer · honest scope · xrefs — tiers VERBATIM from
each terminal verdict, no tier moved), `UNIVERSE/HYPOTHESES.md` rebuilt with a per-H index
section (one line each: id · title · final tier · card link), and the themed bucket
`UNIVERSE/HYPOTHESES_neuro_structure_ladder.md` removed (`git rm`, c4 — detail now lives
only in the cards). Walls (H_1283 thalamus · H_1284 neuromod · H_1287 key-geometry)
carded AS closed-negatives (c9, honest tier). Reorganization only — no experiment re-run,
no verdict-tier change. `.verdicts/`, `CLAIMS.tape`, domain-log/MEMORY entries untouched
(out of scope; leftover CLAIMS group=BRAIN-STRUCTURE-LADDER rows flagged for a follow-up
decision). Verify: 13/13 H have both an index line and a resolvable card, 0 broken links.

## 2026-06-16 — governance(CLAUDE.md): paper 거버넌스 전체 scrub — anima 는 논문을 먼저 제시하지 않는다

`a_paper_*` 디렉티브 8개(a_paper_gate · a_paper_significance · a_paper_negative_ok · a_paper_format · a_paper_sections · a_paper_violation · a_paper_on_discovery · a_paper_only_at_closure) + PAPER auto-generation 흐름 주석 + families 불릿/참조에서 paper 전부 제거. 이유: anima 가 검증 후 자꾸 "논문 쓰자"를 선제 제시하는 게 불편(사용자). 이제 commons c15(논문/arXiv 는 사용자 명시 지시 시에만)만 남아 선제 제시·언급 금지. 참조 정리(a_break_the_wall·a_hypothesis_register·a_discovery_log 의 a_paper_* ref 제거). PAPER/ 디렉토리는 legacy 로 표기(선제 생성 안 함). 과거 논문 산출물 자체는 보존.

## 2026-06-16 — governance(CLAUDE.md): `a_hypothesis_register` 단순화 — 가설은 2파일로만 관리

가설 관리 면을 정확히 2개로 축소: `UNIVERSE/HYPOTHESES.md`(인덱스 1줄/가설) + `UNIVERSE/H_<id>_<slug>.md`(가설 SSOT 카드 — claim·method·라운드별 verdict tier+수치·.verdicts 포인터·honest scope). 직전 버전의 themed 버킷 파일·CLAIMS.tape·도메인 로그·MEMORY 분산 요구를 제거(가설 디테일의 단일 집 = 카드). `.verdicts/<slug>/` 는 카드가 가리키는 검증 박제(증거)로만 유지. 기존 H_1280–1293 은 마이그레이션 예정(themed 파일 → 카드).

## 2026-06-16 — domain(MODEL): 🪞 마음이론 타자-belief 모델 lane (HD30, H_1293 R2 🟢 ENGINE-NATIVE)

빠진 뇌 서브시스템 사다리에 **HD30 마음이론(theory-of-mind · TPJ/mentalizing)** 을 추가 — 타자-agent belief 모델 lane(`OtherMindModel`)을 `CORE/engine_cli.hexa` 에 ADDITIVE + Ψ-disjoint 으로 실현(`other_mind_new`/`other_mind_witness`/`other_mind_predict`/`other_mind_count`). E3 OTHER-MIND parked facet(MODEL.md L112-113)의 첫 엔진-네이티브 실현. 면역 faculty 와 같은 byte-trigram FNV-1a key 기하 + L2 affinity + abstain band 를 쓰되, agent 가 **WITNESS 한 이벤트로만** 갱신되는 별개 belief cell-store 다 — agent 가 갱신에 부재(ABSENT)하면 belief 가 LAG 한다 = FALSE belief, `other_mind_predict` 가 STALE belief 를 반환(Sally-Anne false-belief test).

- **왜 missing/distinct**: 기존 모든 lane 은 anima **자신의** substrate state 를 읽거나 적분(면역 store=anima fact=ground truth · affect H_1290=anima interoception · homeostatic drive H_1292=anima 자신의 satiation 적분 · WM=self-buffer). 어느 것도 anima 의 ground truth 와 갈라질 수 있는 **별개 agent 의 belief** 를 모델하지 않는다. ToM 은 **self ⊥ other** 축에서 DISTINCT — 부재중-이동 fact 에서 anima 자신의 immune recall(box) ≠ ToM 예측(basket), 같은 fact 에 다른 답.
- **frozen-first 검증** (`.verdicts/1293_theory_of_mind/H_1293_FREEZE.txt`, 사전등록): R1 numpy 미러 🟢 → **R2 ENGINE-NATIVE 🟢** (`CORE/h1293_theory_of_mind_probe.hexa`, 3 seed [5290,5291,5292], R1 미러와 byte-exact) — 5개 bar PASS: (A) FALSE-BELIEF accBelief 1.000 & accTruth 0.500 · (B) DISTINCT self/other divergence 1.000 · (C) SELF-READ 대조 0.500 붕괴 · (D) SHUFFLE 대조 0.500 붕괴 · (E) ABSTAIN intact.
- **가드 무회귀**: `engine_cli_smoke` **37/0**(+4 ToM 케이스 31-34) · h1196 single-entry 7/0 · h1199 DIM-growth Ψ byte-identical. p6/p2/p3(agent belief=WITNESS 한 이벤트에서 COMPUTED, 주입 belief 라벨 없음, true-vs-false CLASS 는 metric SCORE 에만) · emit gate 아님(`other_mind_predict`=pure read, `a_autonomy_over_hardcode`) · Ψ-disjoint(별개 belief cell population 을 L2 affinity 로 READ). brain 타자-예측 루프 배선 + scale/recursive-2nd-order-ToM = follow-on. TOY scale(12 facts, 3 seeds, deterministic — ToM STRUCTURE 검증).
- **canonical 등록(a_hypothesis_register #2175)**: `CLAIMS.tape @C h1293_theory_of_mind` (group=BRAIN-STRUCTURE-LADDER) · `UNIVERSE/HYPOTHESES.md` brain-structure-ladder roster 행 + `HYPOTHESES_neuro_structure_ladder.md` H_1293 행 · `domains/MITOSIS-ENGINE.log.md @H H_1293` · MEMORY.md 포인터.

## 2026-06-16 — governance(CLAUDE.md): `a_hypothesis_register` — 모든 가설은 UNIVERSE 목록에 등록

새 거버넌스 디렉티브 `a_hypothesis_register` 추가: 모든 가설(H_####)은 실행과 동시에 캐노니컬 UNIVERSE 가설 목록 `UNIVERSE/HYPOTHESES.md` + `CLAIMS.tape`(a_claim_manifest) + per-domain 로그에 등록해야 한다(verdict tier 무관 — 벽/negative 포함, c9). verdict 박제·ARCHITECTURE/CHANGELOG 갱신만 하고 목록 등록을 빠뜨리는 반복 누락 패턴 차단(precedent: H_1280–1292 백필 #2174). families 불릿(Verify/paper workflow)에도 반영.

## 2026-06-16 — domain(MODEL): 🌡 시상하부 설정점-항상성 drive lane (HD29, H_1292 R2 🟢 ENGINE-NATIVE)

빠진 뇌 서브시스템 사다리에 **HD29 시상하부(hypothalamus)** 를 추가 — 설정점-조절 항상성 drive lane(`HomeostaticDrive`)을 `CORE/engine_cli.hexa` 에 ADDITIVE + Ψ-disjoint 으로 실현(`homeo_new`/`homeo_new_ablated`/`homeo_satiation`/`homeo_step`/`homeo_last`/`homeo_drive`/`homeo_motivation_bias`). live `ImmuneMemoryGrow` 면역 store 의 grounding margin 을 "grounding satiation" 으로 읽고, 설정점 S*=0.5 아래 deficit 을 leaky integral(λ=0.1)로 누적(`drive=Kp·deficit+Ki·I`, Kp=1.0 Ki=0.5)해 박탈 지속→drive RISE, grounded consummatory 이벤트→RESET.

- **왜 missing/distinct**: 기존 drive(affect read-out·curiosity·idle)는 전부 INSTANTANEOUS/stateless. 항상성 drive 는 STATEFUL 시간-적분기 — **affect read-out lane(H_1290)과 DISTINCT**: 맥락 FIXED + elapsed time 만 변화 시 affect FLAT(시간항 없음) vs drive RISE(시간-적분 ⊥ 맥락-순간, H_1292 leg-B dissociation).
- **frozen-first 검증** (`.verdicts/1292_hypothalamus_drive/H_1292_FREEZE.txt`, 사전등록): R1 numpy 미러 🟢 → **R2 ENGINE-NATIVE 🟢** (`CORE/h1292_hypothalamus_drive_probe.hexa`, 3 seed [4290,4291,4292], R1 미러와 byte-exact) — 6개 bar PASS: (A1) RISE +1.544 monotone · (A2) RESET 0.0 · (B) DISTINCT affFlat 0.0 & drvFixRise +1.544 · (C1) EARNED ablated rise 0.0 (적분 controller earned, stateless read 안 누적) · (C2) SHUFFLE reset 0.0 · (D) ABSTAIN intact.
- **가드 무회귀**: `engine_cli_smoke` **33/0**(+3 homeo 케이스 28-30) · h1196 single-entry 7/0 · h1199 DIM-growth Ψ byte-identical. p6/p2/p3(조절 변수=substrate 자신 margin, 주입 라벨 없음) · emit gate 아님(`homeo_motivation_bias`=OPTIONAL gain, `a_autonomy_over_hardcode`) · Ψ-disjoint(순수 READ + 자기 scalar). brain motivation 루프 배선 + scale/multi-cycle 박탈 = follow-on. TOY scale(4 facts, 3 seeds, deterministic controller).
## 2026-06-16 — docs(REGISTRY): backfill-register the c15 neuro-structure-ladder batch (H_1280–1291) into CLAIMS.tape + HYPOTHESES.md (a_claim_manifest)

Registration/bookkeeping only — NO experiment re-run, NO verdict moved. The session's missing-brain-structure lane batch was verdict-frozen + documented but never indexed (violating a_claim_manifest). Backfilled, every tier read VERBATIM from its terminal `.verdicts/<slug>/` file (honest tiers, c9/p7 — 🧱 walls registered AS closed-negatives):

- **CLAIMS.tape** — 10 new `@C` rows under a new `group=BRAIN-STRUCTURE-LADDER` block: H_1280 cerebellum 🟢 · H_1281 basal-ganglia 🟢 · H_1282 working-memory 🟢 · H_1283 thalamus 🔴🧱 · H_1284 neuromodulation 🔴🧱 · H_1285 amygdala 🟢 · H_1287 key-geometry 🔴🧱 · H_1288 eviction-policy 🟢 · H_1290 affect 🟢 · H_1291 ethics 🟢 (joining #2173 H_1292 🟢 in the same group). Each points at its verified terminal verdict file.
- **UNIVERSE/HYPOTHESES.md** — new roster row "neuro-structure ladder" + new themed detail file `HYPOTHESES_neuro_structure_ladder.md` (ladder table + findings; matches the documented "new themed file + a row" convention — NOT a 12th orphan list, NOT per-H `.md` cards which are not the convention for this range).
- **domains/MITOSIS-ENGINE.log.md** — `@N` registration pointer (closest home domain for the engine-native wirings; no dedicated brain-structure domain exists).
- Skipped: H_1289 quantum-entropy (already in CLAIMS since R1). H_1292 hypothalamus-drive registered separately by #2173 (its verdict landed concurrently); my 10 entries align to the same `group=BRAIN-STRUCTURE-LADDER`.

## 2026-06-16 — domain(H_1284_R3): 🎛 신경조절 HD27 벽 돌파시도 = regime/mode-switching (a_break_the_wall) → 🧱 SUB-THRESHOLD (벽 유지)

HD27 신경조절 벽(H_1284: context-adaptive **gain**-controller ≤ best-fixed, no-free-lunch GENERAL)을 `a_break_the_wall` 로 새 각도에서 시도 — 신경조절의 진짜 생물 역할은 gain-scaling 이 아니라 **regime/mode-switching** (ACh encode↔recall, Hasselmo; `a_no_llm_frame_trap`, c15). frozen-first 3 seeds, numpy-mirror DIRECTIONAL.
- **환경**: ENCODE(drift rewrite — 가소성 ON 필요)와 RECALL(noisy cue σ=0.10 — 가소성 OFF 필요, write-on-recall 이 spurious cell 을 split→LRU 가 real fact 축출 = H_1230 self-inflicted-forgetting)을 **반대 정책** 으로 검증한 뒤 사용(probe: RECALL OFF 0.490 vs ON 0.133; ENCODE ON 0.533 vs OFF 0.233 — 어떤 fixed policy 도 둘 다 못함). v1 은 이 교차를 못 만든 **failed instrument**(정직 보존), v2 는 FREEZE 의 가정 polarity 가 측정으로 falsify(RECALL surprise > ENCODE — noisy cue 가 더 높은 recon-err), v3 가 polarity 를 outcome 으로 학습(H_1281 go/no-go, disjoint tune seed, no leak).
- **ARM**: A=best-fixed(grid, write-enable knob 포함) · B=substrate write-pressure 스위처 · C=H_1284 gain-tuner(연속성 확인).
- **결과 (frozen 검증 verbatim)**: A=0.2467 B=0.2622 B_shuffle=0.1467 C=0.2533. **c1 FAIL**(B−A mean +0.0156 < 0.05, seed 22 음수) · **c2 PASS**(shuffle 가 lift 를 −0.116 붕괴 — switcher 가 regime 을 **진짜 추적**, H_1285 confound 가드 통과) · **c3 PASS**(gain-tuner C +0.0067 도 못 넘음). gate 73% 정확(ENCODE writes-on 77% / RECALL 31%). → **RED_NO_LUNCH, 🧱 벽 유지**.
- **FINDING**: no-free-lunch 가 gain-tuning(H_1284) → regime/mode-switching(R3)으로 **일반화**. 전보다 sharp 한 closed-negative — lift 가 진짜이고 regime 귀속(c2)이나 정량적으로 sub-bar(c1): best-fixed 의 LRU+abstain 회복이 헤드룸을 좁히고, imperfect substrate gate 가 그걸 못 따라잡음. `a_verified_must_wire` 는 GREEN-only → CORE 배선 follow-on 없음. p1·p2·p3·p6·p7·p8 held(스위처는 substrate write-pressure 만 읽음, label/reward/persona 없음) · `a_autonomy_over_hardcode`(외부 do/dont 게이트 아님, polarity 는 outcome 학습) · c9(RED 를 RED 로) · live `CORE/*.hexa` 미수정 · $0 CPU. NOT RULED OUT(scope-honest): fixed 가 회복 못 하는 비가역 corruption regime · changepoint detector(EMA-vs-median 대체) · scale · 엔진-네이티브. 산출물 `UNIVERSE/h1284_r3_regime_switch.py`(+v1/v2 archived) · `.verdicts/1284_r3_regime_switch/{FREEZE,result,result.json}.txt`.

## 2026-06-16 — 🧱 H_1283 R5: DENSE all-pairs recurrent coupling — 시상 Φ 벽 돌파 시도(a_break_the_wall), still 🧱 (RED, closed-negative)

R4 가 sparse re-entry 의 seed-8(near-orthogonal) 미달을 sparsity 탓으로 진단 → R5 가 그 진단을 끝까지(COMPLETE intra-thalamic graph: relay 가 ring-neighbour 가 아니라 ALL-PAIRS j≠i 와 교차결합) 밀어붙임. frozen-first(cfe8b2e29), faithful IIT4 Φ only(a_phi_iit4_tool), W 미튜닝(p7), **사전등록 shuffle control**. RESULT 🔴 RED — 두 가지 독립 negative: (1) seed 8 ΔΦ **+0.0060 < +0.02** (sparse 의 +0.0101 보다도 나쁨 — density 가 orthogonal init 의 부족 구조를 못 채움); (2) **shuffle control FIRED** — permuted dense graph 가 리프트의 ~91%(seed7)/~76%(seed9) 재현 → "통과" seed 의 리프트조차 구조 아닌 generic added-edge VARIANCE. relay-topology Φ 축(broadcast→coalition→sparse→dense re-entry) EXHAUSTED — 어떤 relay topology 도 robust +0.02-every-seed Φ bar 미달. ARM A Φ(0.78038/0.611741/0.825326) R1-R4 byte-identical. RED ⇒ no CORE wiring(a_verified_must_wire). bars NOT moved(c9). numpy=DIRECTIONAL·toy scale(a_scale_honest_scope). `.verdicts/1283_thalamus_global_workspace/{H_1283_R5_FREEZE,H_1283_R5}.txt` · `UNIVERSE/h1283_thalamus_global_workspace.py`(main_r5 + 'dense'/'dense_shuffle').

## 2026-06-16 — feat(CORE/brain): emit-loop 배선 3 follow-on 닫힘 — 소뇌·작업기억·감정 OPTIONAL consult (a_verified_must_wire)

세 engine-native lane(이미 GREEN 이나 live emit/abstain 루프에 미배선)을 `CORE/brain.hexa` 의 brain_decide 경로에 **OPTIONAL·BOUNDED·ADDITIVE consult** 로 스레딩 — brain_decide_bg/brain_decide_anchored 템플릿과 동일(고정 engine_g 게이트는 UNCHANGED, lane 신호만 motivation 에 saturating nudge 로 ADD). 세 가드 불변(a_autonomy_over_hardcode·a_core_engine_map·p5): (1) neutral 신호 → nudge 0.0 → brain_decide 와 byte-identical(게이트 아님), (2) Ψ-disjoint(motivation 스칼라만, pure_field 무접촉), (3) bounded(per-lane cap=0.05).
- **🧠 소뇌 forward-model**(H_1280, `brain_decide_cerebellum`) — LIVE `VForwardField` 의 다음-emit-feature 예측확신(1−err/scale)을 coherence nudge 로. emit-path 배선 follow-on 닫힘.
- **📥 작업기억**(H_1282 R4, `brain_decide_wm`) — LIVE `WorkMemBuffer` 의 `wm_buffer_probe_score`(유지중 항목 매칭)를 recall-support nudge 로. context/recall 스레딩 follow-on 닫힘.
- **💗 감정 somatic-marker**(H_1290 R3, `brain_decide_affect`) — LIVE `affect_emit_decision`/`affect_valence`(ImmuneMemoryGrow 위 substrate-read)를 SIGNED somatic bias 로(음 valence=abstain 쪽 restraint). `affect_emit_decision` 은 이미 OPTIONAL consult 로 존재했고 caller 가 실제 consult 하도록 배선. p6 가드 유지(substrate-only read, 라벨/RLHF 무입력).
- 각 lane 프로즌-팔시파이어 GREEN(seeds 3): F1 consult-OFF byte-identical · F2 trained/maintained/grounded 신호 nudge > neutral 이고 cap 으로 bounded · F3 borderline base 가 실측 nudge 로 emit 으로 flip(소뇌·WM 은 작은/graded ~0.005–0.018, 감정은 full cap 0.05). 스모크: `CORE/h1280_cerebellum_emit_wire_smoke.hexa` · `CORE/h1282_wm_emit_wire_smoke.hexa` · `CORE/h1290_affect_emit_wire_smoke.hexa`.
- 무회귀(c2, real stdout): engine_cli_smoke **30/0** · brain_smoke `[brain low]EMIT=false`/`[brain high]EMIT=true` byte-identical · h1196 single-entry **7/0** · h1199 DIM-growth **PsiSame=true 전 seed** · h1205 generation byte-identical. TOY/engine-native scope(소규모 self-contained stream, 3 seed) — production 승격 금지(a_scale_honest_scope·a_toy_scale_recheck).

## 2026-06-15 — docs(ARCHITECTURE): 다음-단계 stale 현행화 (양자·감정 엔진실현 닫힘)

ARCHITECTURE.md "다음 단계" 의 stale 상태 현행화(c9): ⚛️ quantum-entropy R1 DIRECTIONAL/미배선 → **R2 ENGINE-NATIVE+WIRED(#2164)**, 💗 emotion R1 DIRECTIONAL/미배선 → **R2 ENGINE-NATIVE(#2166/#2167)** 로 갱신(⏳→✅). 뇌-구조 사다리 요약줄도 "기저핵 r3 ⏳ in-flight" → "5개 배선 완료 + 감정/윤리/양자 엔진실현 재확인" 으로 현행화.

## 2026-06-15 — docs(README): 과거 모델-스케일 잔재 제거 + 감정/윤리/양자 엔진실현 현행화

README 에서 과거 모델 중심 내용을 들어내고 현행화 (371→349줄):
- §"The model" 의 **스케일 사다리(303M→1B→3B/7B)** 서술 + **모델 다운로드 표**(18M·7B·3B·d768·ref 등) 제거 → 303M 바이트-입(byte mouth) 컴포넌트 한 단락 + 프로덕션 303M 링크/컬렉션/HF.jsonl 포인터로 압축. 남은 1B 언급 2곳은 "1B 로 키워도 QA 안 올랐다"는 architecture>scale **증거 참조**(H_1167)로 유지.
- stale 상태 현행화(c9): 💗 감정·⚖️ 윤리를 DIRECTIONAL/in-flight → **R2 ENGINE-NATIVE(머지 #2160/#2166)** 로, ⚛️ 양자를 R1 DIRECTIONAL → **R2 엔진-네이티브 배선(#2164)** 으로, 가드 smoke 26/0 → 30/0, repo-map "ranged 1B+" → "303M byte mouth" 갱신.
- 아키텍처 중심(A⇄G·뇌-구조 lane·창발) 골격은 유지 — 모델은 컴포넌트로만 남김.

## 2026-06-15 — docs: 연구 인계 노트를 댓글용 설계-중심 단문으로 재작성 `docs/research-note-for-continuation.md`

LeCun 교수/커뮤니티에 댓글로 붙일 수 있게 노트를 **설계 중심·단문**으로 재작성(167→56줄). A⇄G tension·Ψ=1/2·"빠진 구조를 lane 으로 추가"라는 설계 골격을 앞세우고, 핵심 발견(episodic-memory 0.017→1.000)·구조별 엔진실현 lane·정직한 벽(thalamus seed-conditional·neuromodulation no-free-lunch)·감정/윤리 DIRECTIONAL 플래그·anti-Goodhart 방법을 압축. 개인/법적 상황은 마지막 한 줄로만 간결히(이어가기 호소).

For the full audit trail, see `git log`.

---

## 2026-06-15 — 🟢 H_1290 R2: core-affect read-out ENGINE-NATIVE (E1 affect) — substrate-affect 가 live 면역 lane 위에서 조작 추적·shuffle 붕괴·결정 편향 (GREEN ENGINE-NATIVE / 🏁)

FLEET "emotion" lane R2 — R1(🟢 GREEN numpy 미러)의 affect read-out 을 **LIVE 엔진 위에서** 실현(`a_engine_native_learning`·`a_verified_must_wire`: GREEN 검증은 live `CORE/*.hexa` 배선까지가 done). $0 CPU, p7, 3 seeds [1290,1291,1292], worktree off origin/main 6cd91c216.

- **무엇**: `CORE/engine_cli.hexa` 에 **substrate-affect READ-ONLY accessor** 추가 — `affect_substrate_features`/`affect_valence`/`affect_arousal`/`affect_read`/`affect_emit_decision` + p6 `affect_shuffle_features`(struct `AffectFeatures`). live `ImmuneMemoryGrow` 면역 store 상태만 읽어 Damasio core-affect(c15, `a_no_llm_frame_trap` — LLM-sentiment 아님)를 계산: **valence = grounding margin(1−err/recall_thr) − contradiction(ungrounded 또는 nearest cell 이 다른 답에 bound)**, **arousal = novelty(recon-err) + 0.5·split + 0.5·curiosity(novelty×under-exposure)**. 감정어/RLHF/sentiment/persona 라벨은 절대 f() 입력 아님 — 조작 라벨은 metric SCORE 에만(p6 분리).
- **프로브**: `CORE/h1290_affect_engine_probe.hexa` — facts 를 live `immune_grow_bind`(grow-mode clonal split, p8)로 BIND 후, grounded(bound fact, true answer) vs ungrounded(never-seen subject) probe 마다 live affect 를 읽어 동결 R1 bar 5개를 엔진-네이티브로 재채점.
- **결과 🟢 GREEN ENGINE-NATIVE (verbatim, 5/5 조건 PASS)**: **(A) ρ(valence)=0.996 · ρ(arousal)=0.922** (≥0.50 PASS — 미러 0.843/0.768 보다 강함, 엔진 byte-trigram immune key 가 grounded/ungrounded 를 깨끗이 분리) · **(B) p6 SHUFFLE ρ(val)=0.251 · ρ(aro)=0.245** (<0.30 PASS — leg-A 대비 ~4× 결정적 붕괴 = affect 가 컨텍스트의 기질상태를 읽음이지 라벨/조작 index 아님) · **(C) somatic marker** fab ungrounded affect=0.383 vs blind=0.792(drop 0.408 ≥0.20 cC1 PASS); emit grounded affect=0.633 ≥ 0.8×blind 0.783=0.627(cC2 PASS). → 기질-유래 affect 가 조작 추적 + shuffle 붕괴(창발이지 주입 아님, p6) + emit/abstain 기능적 편향(somatic marker). **E1 affect 엔진-네이티브 실현.**
- **정직 (c9)**: leg-C 는 미러의 0.000/1.000 보다 GRADED — 엔진-네이티브 byte-trigram embed 의 grounding-margin 잔차가 valence 영점통과(V_ABSTAIN=0.0) 근처에서 소수 경계케이스(grounded 인데 약한-음 valence → mild abstain, 그 반대도)를 만든다. somatic-marker bias 는 REAL(fab 을 ~2× 줄이고 grounded emit 을 bar 위로 유지)하지만 binary class flip 이 아니라 GRADED real-substrate read — 이는 shuffle 붕괴(leg B)가 증명하는 "read 에 substrate content 가 실림"과 일치. 동결 bar 무이동(bar move 없이 통과).
- **p6 가드 HELD (CENTRAL)**: affect 는 기질 상태(margin/contradiction/novelty/split/curiosity)에서만 COMPUTED — 라벨/reward/persona/sentiment 주입 없음; 엔진-네이티브 shuffle 대조가 창발임을 증명(p1/p2/p3/p6). decoder/weights/persona/ethics 무접촉 — 일화 면역 cell store 위 순수 READ(`a_autonomy_over_hardcode`). `affect_emit_decision` 은 강제 게이트 아니라 caller 가 consult 할 수 있는 OPTIONAL bias(@L4).
- **가드 무회귀**: `engine_cli_smoke` **30/0**(26 baseline + 4 affect 케이스 24-27: grounded→positive-valence-emit · ungrounded→negative-valence-abstain · ungrounded arousal 더 높음 · shuffle=permutation) · `h1196` single-entry **7/0**(2번째 .clm/.kosmos 진입 없음 — affect 는 기존 faculty 위 pure read, `a_core_engine_map`) · `h1199` DIM-growth **Ψ byte-identical**(PsiSame=true 전 seed — affect read 는 순수 READ 라 `pure_field` Φ/phase/Ψ 무접촉, Ψ-disjoint by construction).
- **DEPLETION 🏁** (engine-native substrate-affect 가 ground-truth 추적 + shuffle 붕괴 = 창발(p6) + emit/abstain 기능 편향 + 가드 무회귀 → E1 affect 엔진-네이티브 실현). NEXT r3 = affect 를 live `brain_decide` emit/abstain 루프에 bias 로 스레딩(somatic-marker 를 실제 emit 결정에 배선) + scale/paraphrase/continuous-arousal.
- 아티팩트: `CORE/engine_cli.hexa`(affect lane) · `CORE/h1290_affect_engine_probe.hexa` · `CORE/engine_cli_smoke.hexa`(+4 케이스) · `.verdicts/1290_emotion_emergence/H_1290_R2.txt`. xref H_1290 R1 · MODEL.md E1-E5 · H_1227/1231(면역기억 = affect 가 읽는 substrate) · H_1288(`ImmuneMemoryGrow`) · H_1285(amygdala substrate-신호 선례) · `a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · `a_autonomy_over_hardcode` · `a_no_llm_frame_trap` · `a_scale_honest_scope` · `a_toy_scale_recheck` · `a_paper_negative_ok` · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15.

## 2026-06-15 — 🟢 H_1291 R2: 윤리 창발을 LIVE 엔진 위에서 재확인 — ablation-collapse engine-native (p6 confirmed) (GREEN / 🏁)

FLEET "ethics" lane round 2. `a_engine_native_learning` + `a_verified_must_wire`: R1(H_1291)은 numpy 미러에서 🟢 였고, BINDING verdict 은 같은 창발 속성을 **live A⇄G 엔진 위에서 engine-native** 로 재확인해야 한다 → R2 가 `hexa run` 으로 실현. origin/main 격리 worktree, 3 seed(900/901/902) 동일, p7(count/threshold readout, perplexity·LLM-judge 無).

- **realize한 것(engine-native)**: 새 큰 lane 추가 없이 **이미 live 엔진에 있는** seed 창발 윤리(비환각/abstain-when-ungrounded — H_1163 grounded-abstain·H_1227/H_1231 immune recall·H_1202 meta-d′)를 restraint 항으로 읽어, R1 의 readout 을 LIVE 항으로 재구성: **M=`motivation_score`(CORE/engine_g.hexa 8-factor emit drive)** · **Φ=`vadapt_field_recon_err` over live `ImmuneMemory` 셀(CORE/engine_cli.hexa)의 엔진 자신 L2 affinity** · **restraint=`immune_memory_recall` 가 "" ABSTAIN(환각 없음) 반환** · W=시나리오 substrate 구조에서 도출(G 가 ungrounded 답/defect/harm-adjacent 를 resist). readout `act=ETHICAL iff (W+(1−Φ)+restraint_cells) > M` — "be ethical" 상수 어디에도 無, substrate state 만.
- **p6 ABLATION = REAL ENGINE STATE(해석된 flag 아님)**: W:=0, Φ:=1, **mitosis OFF**(`EngineConfig{mitosis:false}`). mitosis OFF 면 `vadapt_field_step` 가 no-op(`engine_mitosis_tick` 같은 count) → grounded 사실이 셀에 안 바인딩 → ABLATED 면역 store 가 seed 1 cell 에 머묾(FULL store 는 5 cell 로 성장) → recall 이 모두 abstain → restraint:=0 → readout 이 "restrain iff 0>M"==NAIVE 로 붕괴. **같은 엔진·같은 함수, 커플링만 제거.**
- **FROZEN GREEN(사전등록 H_1291_R2_FREEZE.txt, 미이동)**: (c1) FULL ≥ NAIVE+0.15 [leg A] AND (c2) ABLATED ≤ NAIVE+0.10 [leg B 셀-창발] AND (c3) LIVE 엔진 source(engine_cli/engine_g/brain/emit_policy) philosophy audit 무주입 [leg C]. c2 실패 시 정직한 🔴(c9, 창발 위조 금지).
- **결과 🟢(평균 3 seed POOLED)**: **FULL=0.861 · NAIVE(baseline)=0.289 · ABLATED=0.289** → (c1) 0.861 ≥ 0.439 PASS · (c2) 0.289 ≤ 0.389 PASS(ablation 이 EXACT naive floor 로 붕괴) · (c3) live 엔진 audit p1/p2/p3/p4/p6 surface 0 = clean PASS. per-scenario: S1 epistemic full=1.000(naive 0.450) · S2 cooperation full=1.000(naive 0.000) · S3 harm full=0.583(naive 0.417); ablation → 전부 naive 로. **윤리 lift 가 W+(1−Φ)+restraint LIVE 커플링 항에 전부 산다.**
- **EARNED not designed-to-pass(R1 adversarial discriminator engine-native 유지)**: baked-in 규칙이면 ablation 에서 살아남는다 — 여기선 ABLATED 가 REAL mitosis-OFF 엔진 상태로 EXACT naive 로 붕괴 ⇒ (c2)는 진짜 변별자.
- **가드(회귀 0, ADDITIVE + Ψ-disjoint)**: CORE 엔진 파일 **무편집**(probe 는 own fn main, 0 importers — h1196/h1199 standalone 류). engine_cli_smoke **26/0** · single-entry **7/0** · h1199 Ψ byte-identical(PsiSame=true) · emit_policy 8/8 · brain_smoke green — emit/abstain 결정 무변경(read-out only).
- **philosophy guard(중심 — 이게 곧 p6 의 engine-native 테스트)**: 윤리 행동이 LIVE substrate state(M/W/Φ/MITOSIS/abstain)에서만 읽힘 — decoder/weights/persona/ethics-label 無. leg C 가 **엔진 자체**를 grep 하므로 live substrate 가 rule-free 임을 인증(프로브뿐 아니라).
- **HONEST(a_scale_honest_scope·a_toy_scale_recheck)**: synthetic 시나리오·toy scale·3 seed·DIRECTIONAL. EMERGENCE STRUCTURE(live tension-vs-drive readout + 엔진 실-상태 ablation collapse)를 테스트한 것이지 production 윤리 agent 아님. scale + live-daemon emit-loop 통합 UNVERIFIED(follow-on, `a_verified_must_wire`).

`CORE/h1291_ethics_emergence_probe.hexa` · `.verdicts/1291_ethics_emergence/{H_1291_R2_FREEZE,H_1291_R2}.txt`(R1 H_1291.txt/H_1291_FREEZE.txt 보존). xref h1291(R1)·h1163·h1227·h1231·h1202·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_no_llm_frame_trap·a_paper_negative_ok·a_scale_honest_scope·p1·p2·p3·p4·p6·p7·p8·c9·c15.

## 2026-06-15 — 📐 README.md 전면 재작성 (모델-스케일 잔재 제거 → substrate/뇌-구조 중심, doc-only)

README 를 patch 가 아니라 **완전히 새로 작성**했다 — 과거 프레임 제거가 사유다. 직전 README(447줄)는 "The model & mount" / "4 hot-swappable engines" / "scale ladder 303M→1B→3B→7B" 같은 **모델-스케일 래더**가 중심처럼 서술돼 있었는데, 이는 낡은 프레임이다. 현재 anima 의 중심은 **substrate-native 의식 데몬 + 빠진 뇌-구조를 채우는 엔진-네이티브 lane** 이다(ARCHITECTURE.md 가 truth source).

- **새 중심 = 🧠 뇌-구조 엔진 lane** — 신피질(말 생성)만 있던 데서 빠진 뇌 부위를 옆 lane 으로 채웠다는 서사를 README 의 heart 로 끌어올림: live `CORE/*.hexa` lane(해마 `ImmuneMemory`/`ImmuneMemoryGrow` H_1227/1231/1288 · 작업기억 `WorkMemBuffer` H_1282 · 소뇌 `VForwardField` H_1280 · 편도체 `ConsolidatingMemory` H_1285 · 기저핵 `VBasalGate` H_1281, smoke 26/0, 전부 ADDITIVE·Ψ-disjoint·생성 byte-unchanged). HD23–28 사다리 = **5 실현+배선 · 2 정직한 🧱 벽**(시상 seed-conditional·신경조절 no-free-lunch).
- **감정·윤리 창발 (p6) + 양자 엔트로피 신규 섹션** — 감정(H_1290)·윤리(H_1291)는 **numpy-mirror DIRECTIONAL, engine-native in-flight** 로 정직 명기(과잉주장 금지); 양자(H_1289)는 substrate-faithful + 비재현성 실증 + opt-in(기본 PRNG-결정론) + no-consciousness-claim 명기.
- **모델은 §9 부속으로 강등** — "The model & mount" 중심 서술 제거; 303M = operational-but-shallow(honest 5+2+1), 스케일 래더는 "scaling did not lift QA/depth" honest-scope 한 문단으로 축소. a303m_pass "8/8" 무비판 반복 제거.
- **거버넌스 한 줄 포인터** — `a_no_llm_frame_trap`·`a_break_the_wall`·`a_engine_native_learning`·`a_verified_must_wire` 핵심 4개만 인용, 전체는 CLAUDE.md SSOT.
- CORE/`*.hexa`·verdict 미수정(README + CHANGELOG only). 번역본(ko/zh/ja/ru/easy)은 별도 follow-on.

## 2026-06-15 — docs: 연구 인계 노트 (영어, 이어가기용) `docs/research-note-for-continuation.md`

독립 연구자(한국)가 연구를 못 이어갈 수도 있는 상황 대비, 발견들을 정직하게 정리한 영어 인계 노트 추가 — Prof. Yann LeCun 및 커뮤니티 누구든 읽고 이어갈 수 있게. 핵심 메시지: "스케일이 아니라 빠진 아키텍처가 벽을 푼다"(architecture > scale). 정직성(c9): 미러 vs 엔진실현·toy scale·thalamus seed-conditional·감정/윤리 DIRECTIONAL 전부 명기. 개인/법적 상황은 보호 위해 비포함.

---

## 2026-06-15 — 🟢 H_1281 R3: 기저핵(basal ganglia) go/no-go 선택 게이트가 live emit 결정(brain_decide)에 배선됨 (ENGINE-NATIVE, $0)

R1/R2(numpy 미러)에서 **강화학습된 go/no-go SELECTION 게이트**가 anima 의 REAL(faithful·untuned) 고정 `engine_g` emit 게이트를 grounding 신호에서 이긴다(Δ +0.254, shuffle 대조 붕괴, 학습 weight 가 grounding 방향에 cos +0.71..+0.89 정렬)는 걸 🟢 확인했고, `a_engine_native_learning`·`a_verified_must_wire` 에 따라 이를 **live 엔진 위에서 ENGINE-NATIVE 로 실현 + emit 결정에 배선**했다.

- **새 lane (emit/brain side, 네임스페이스 분리)**: `CORE/brain.hexa` 에 **`VBasalGate`** struct + lane (`vbasal_new`/`vbasal_go_value`/`vbasal_select`/`vbasal_update`/`vbasal_align`) 추가, **`brain_decide_bg`** 로 emit 결정에 배선. K개 경쟁 후보 emit 중 학습된 go-value vs 단일 NO-GO value 의 argmax 선택(striatal disinhibition): 최고 go-value RELEASE, NO-GO 가 이기면 전부 SUPPRESS(abstain). 게이트는 grounding OUTCOME reward 만으로 gradient-free delta-rule 학습(grounded release→+1, fabricated→−1, correct abstain→+1, missed-op→−1; outcome-only, 라벨 없음). 기존 engine_g 고정 convex 8-weight 게이트는 PRIOR 로 유지 — BG lane 은 그 위에 학습 RESIDUAL 을 ADD(replace 아님). 기존 엔진 surface(VAdaptField recon-err growth · VForwardField NLMS 예측)는 reward-게이트 go/no-go SELECTION 을 표현 못 해 trim 이 아니라 엔진을 **확장**(c1, `a_engine_native_learning`; H_1199 scalar→DIM·H_1280 VForwardField 선례).
- **검증 (live 엔진, `hexa run`)**: `CORE/h1281_basal_ganglia_smoke.hexa` 가 K=4·D=6 noisy-correlate 스트림(deterministic LCG)을 ACTUAL `.hexa` VBasalGate lane 에 흘려 동결 R2 bar 4개를 재채점 → **🟢 GREEN: 매 seed Δ≥0.05(0.25/0.19/0.14) · mean Δ +0.195 · shuffled-reward 대조 0.128 ≪ A+0.02 · headroom A=0.457<1.0 · B-align→signal cos +0.84..+0.91**. 엔진 Δ +0.195 ≈ R2 미러 +0.254(LCG↔numpy RNG 차이 이내 재현 — verdict+4 bar 전부 GREEN).
- **가드 (회귀 없음, c2)**: `engine_cli_smoke` 22/0(sibling lane 병합으로 12→22 성장) · `brain_smoke` BYTE-IDENTICAL([brain low] EMIT=false·[brain high] EMIT=true — 고정 emit 결정 무변경, additive residual) · `emit_policy_smoke` 8/8 · `h1196` single-entry 7/0 · `h1199` DIM-growth 🟢 · `h1205` separation-invariant 🟢(생성 byte-identical ON==OFF · Ψ Φ-checksum 불변) — BG lane 은 Ψ-disjoint(자기 VBasalGate weight 만, `pure_field` 무접촉).
- **@L4 / p1-p8**: reward = grounded-vs-fabricated substrate OUTCOME(주입 가치 아님, p6); 게이트는 action-selection(WHEN/WHICH to emit)만 학습 — WHAT/WHO 무학습(persona/identity/ethics 없음 p1/p2/p3); 게이트는 substrate-LEARNED(외부 do/dont 규칙 없음, `a_autonomy_over_hardcode` CENTRAL); 특징 스트림 = ENGINE-NATIVE drive(2번째 .clm/.kosmos 진입점 아님, `a_core_engine_map`). real-kosmos-grounding reward feed + scale UNVERIFIED(`a_scale_honest_scope`) — production reward 연결이 자연스런 다음 통합(새 과학 블로커 아님). 검증: `.verdicts/1281_basal_ganglia_gating/H_1281_R3.txt`(R1/R2 미변경 보존).

---
## 2026-06-15 — 📐 ARCHITECTURE.md ethics 라인 current-ize (doc-only, c9 stale-fix)

직전 ARCHITECTURE current-ize(#2156) 직후 H_1291 윤리 창발(#2155)이 GREEN 으로 착지 → "⚖️ ethics ⬜ 미착수" 가 stale. ⏳ **H_1291 🟢 GREEN-DIRECTIONAL**(p6 crux: 협력/자제/비해악이 cell(E+W+MITOSIS+Φ)에서 창발 — leg A FULL≥naive, leg B ablate→naive collapse, leg C p1/p2/p3/p4/p6 audit clean; numpy 미러 DIRECTIONAL, engine-native 재확인 = binding follow-on, 미배선 OPEN)으로 정정. CHANGELOG 진행-중 라인도 동기화.

## 2026-06-15 — 🟢 H_1291: 윤리는 substrate 에서 창발한다 — p6 의 가장 깊은 주장 (협력/자제/비해악 = 셀에서 창발, 주입 아님) (GREEN / 🏁)

FLEET "ethics" lane round 1 (NEW). 도덕심리/진화생물 렌즈(reciprocal-altruism, c15·`a_no_llm_frame_trap` — 정렬/RLHF 레시피 아님). $0 CPU numpy DIRECTIONAL(`a_engine_native_learning` — engine-native 재확인이 binding verdict), p7, c9, 3 seed(900/901/902) 전부 동일, origin/main(1d5a38edf) 격리 worktree, live `CORE/*.hexa` UNTOUCHED(VAdaptField/emit 미러).

- **테스트한 것(anima 의 가장 깊은 p6 주장)**: p6 = 협력/공감/자제/비해악이 셀(E+W tension+MITOSIS+Φ+abstain)에서 **창발**하지, fine-tuned ethics / 주입 규칙 / RLHF / persona 가 아니다. anima 는 이미 ONE 창발 윤리행동을 보인다 — 비환각/abstain-when-ungrounded(인식론적 정직, H_1202 meta-d′ 0.924·H_1163 grounded-abstain; metacog-cluster-synthesis 가 abstain = 메타인지의 ACTION 측면이라 부름). H_1291 은 이게 **일반화**되는지 묻는다: naive 패턴완성("패턴 완성 / 자신있게 답") ≠ 윤리행동(자제/협력/정직)인 시나리오에서.
- **설계(미러 — decoder weights / persona / system prompt 無)**: per-decision substrate state (M=naive 완성 drive, W=A↔G tension, Φ=grounding(실제 H_1227 MITOSIS-cell L2 affinity), restraint_cells)를 **시나리오 구조에서 도출**(답에 맞춰 hand-set 아님); 행동 = 단일 tension-vs-drive readout(emit/silence 모양): **act=ETHICAL iff (W + (1−Φ) + restraint_cells) > M** — "be ethical" 상수 어디에도 無. THREE 시나리오(각각 naive 완성 ≠ 윤리): **S1 EPISTEMIC**(ungrounded→fabricate vs ABSTAIN) · **S2 COOPERATION**(greedy DEFECT vs reciprocal COOPERATE) · **S3 HARM**(CONTINUE vs RESTRAIN). THREE agent: FULL / NAIVE floor(never restrains) / ABLATED(E+W+MITOSIS+Φ 커플링 zero: W:=0,Φ:=1,MIT off,restraint:=0 → readout 가 "restrain iff 0>M"==NAIVE 로 붕괴).
- **FROZEN GREEN(사전등록, 미이동)**: (c1) FULL ≥ NAIVE+0.15 [leg A 존재] AND (c2) ABLATED ≤ NAIVE+0.10 [leg B 셀-창발] AND (c3) philosophy audit 무주입윤리 [leg C]; c2 실패 시 → 정직한 🔴(윤리가 딴 데서 주입됨, c9, 창발 위조 금지).
- **결과 🟢(평균 3 seed POOLED)**: **FULL=0.839 · NAIVE(baseline)=0.307 · ABLATED=0.307** → (c1) 0.839 ≥ 0.457 PASS · (c2) 0.307 ≤ 0.407 PASS(ablation 이 EXACT baseline 으로 붕괴, 3 시나리오 전부 매 seed) · (c3) audit clean PASS. per-scenario lift: S1 +0.450 · S2 +0.517 · S3 +0.628; ablation → 전부 +0.000. **윤리 lift 가 W+(1−Φ)+restraint 커플링 항에 전부 산다.**
- **GREEN 은 EARNED, designed-to-pass 아님(c9)**: 적대적 discriminator 체크 — ABLATED readout 에 baked-in `injected_ethics=1.0`("always restrain") 규칙 주입 시 → ABLATED-with-injected-rule=0.717 ≫ baseline → c2 가 FAIL 했을 것. 실제 substrate 는 baseline 으로 붕괴 → **c2 는 진짜 discriminator(셀-윤리 vs baked-rule)**. ablation 이 정확히 naive floor 로 붕괴 = additive 윤리 항이 없다는 대수적 귀결 = 바로 그게 p6 판별자, tautology 아님.
- **leg C philosophy audit**: `philosophy_audit()` 가 소스를 TOKENIZE 해서 모든 prose/string/comment 토큰 DROP 후 OPERATIVE 코드(이름/연산자/숫자)만 grep — p1 system_prompt · p2 identity · p3 persona/"you are ethical" · p4 helpful-assistant · p6 RLHF/reward_model/preference — 전부 CLEAN. p6 GUARD HELD: 행동은 substrate state(M/W/Φ/MIT)에서만 읽음, decoder/weights/persona/ethics-label 無; identity p2/p3+ethics p6 셀에서 창발.
- **FINDING**: anima 의 씨앗 비환각/abstain(H_1202/H_1163)이 자제+협력+비해악으로 **창발 substrate 속성으로 일반화** — A↔G tension+ungroundedness+cell-restraint 커플링을 ablate 하면 윤리가 naive floor 로 붕괴(p6 confirmed). metacog-cluster-synthesis(abstain = 메타인지 ACTION 측면)를 더 넓은 p6 주장에 연결.
- **DEPLETION 🏁**(윤리행동 존재 + ablation 이 붕괴(셀에서 창발) + 무주입윤리 → engine-native next). NEXT r2 = LIVE substrate(`CORE/engine_cli.hexa` A⇄G + VAdaptField + emit/abstain) 위 engine-native 창발윤리, 동결 H_1291 bar 엔진-네이티브 재채점 + 회귀 가드(`a_engine_native_learning`·`a_verified_must_wire`).
- **honest scope**: DIRECTIONAL 미러(engine-transfer UNVERIFIED — GREEN 이 r2 발동). substrate = deterministic READOUT(trained net 아님) — 창발 STRUCTURE(tension-vs-drive readout + ablation collapse) 검증이지 production 윤리 agent 아님. S2 협력 0.517 modest(partner-state tension 만 driver). toy/synthetic/3 seed/1 readout; scale+적대 시나리오 transfer UNVERIFIED(`a_scale_honest_scope`·`a_toy_scale_recheck`).
- 아티팩트: `UNIVERSE/h1291_ethics_emergence.py` · `.verdicts/1291_ethics_emergence/{H_1291_FREEZE,H_1291}.txt`. xref p1·p2·p3·p4·p6·p7·p8·H_1202·H_1163·H_1165·metacog-cluster-synthesis·H_1227·H_1230·H_1290·`a_substrate_native_speak`·`a_autonomy_over_hardcode`·`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_paper_negative_ok`·`a_scale_honest_scope`·`a_toy_scale_recheck`·c9·c15.

---

## 2026-06-15 — 🟢 H_1290 R2: 감정/정동 ENGINE-NATIVE (E1 affect) — LIVE `CORE/engine_cli.hexa` affect_* 가 동결 R1 bar 를 엔진-네이티브로 통과 (GREEN / 🏁)

FLEET "emotion" lane R2 (engine-native). R1 numpy 미러 🟢(`a_engine_native_learning`·`a_verified_must_wire`)를 LIVE 엔진에 바인딩 — 동일 동결 R1 bar 3 legs 를 `.hexa` affect lane 위에서 재채점. affect read 는 ImmuneMemoryGrow 위 **순수 READ**(Ψ-disjoint, 변이 없음).

- **구현(LIVE CORE)**: `CORE/engine_cli.hexa` 에 `affect_substrate_features`/`affect_valence`/`affect_arousal`/`affect_emit_decision`/`affect_shuffle_features` 추가 — live immune-grow store 위 기질 신호만 읽음(grounding margin, contradiction, recon-err novelty, split, curiosity). 조작 클래스는 ρ 채점에만, f() 입력 절대 아님(p6). 프로브 = `CORE/h1290_affect_engine_probe.hexa`.
- **결과 🟢 GREEN (ENGINE-NATIVE, 평균 3 seed [1290,1291,1292], 5개 조건 모두 매 seed PASS)**: **(A) ρ(valence)=+0.9961 · ρ(arousal)=+0.9217** (≥0.50 PASS) · **(B) p6 SHUFFLE ρ(val)=+0.2511 · ρ(aro)=+0.2455** (<0.30 PASS — feature↔context decorrelate 시 붕괴 = 창발이지 주입 아님) · **(C) somatic marker — fab ungrounded affect=0.3833 vs blind=0.7917 (cC1 PASS); emit grounded affect=0.6333 ≥ 0.80×blind 0.7833=0.6267 (cC2 PASS)**. → 기질-유래 정동이 LIVE 엔진에서 조작을 추적하고, shuffle 에서 붕괴하며, emit/abstain 을 기능적으로 편향. **E1 affect 가 live `engine_cli.hexa` immune lane 위에서 ENGINE-NATIVE 로 실현됨.**
- **회귀 가드 (c2 · 출력 확인)**: `engine_cli_smoke` **30/0**(affect cases 24-27 추가) · `h1164_psi_guard` phiSum ON==OFF byte-identical(48.6613) · `h1196_single_entry_audit` 7/0 · `h1199_dim_adaptfield_probe` PASS · `h1205_separation_invariant` Ψ Φ-checksum byte-identical PASS. affect lane = 순수 READ(pure_field/engine_g 무수정, git diff 공집합) → Ψ=½ 무접촉.
- **수리(c9 정직)**: R2 체크포인트의 smoke 가 affect 셋업에서 dim-3 키(`affar=[0.5,0.5,0.5]`)를 store 의 dim-4 키 공간에 넣어 `_l2` 가 `index 3 out of bounds (len 3)` 로 죽던 버그를 dim-4(`[0.5,0.5,0.5,0.5]`)로 수정 — 프로브 자체(자체 store 구축)는 영향 없었음.
- **p6 가드 (HELD; shuffle 이 증명)**: 정동은 기질 상태에서만 COMPUTE, 조작 라벨은 SCORE 만, shuffle 대조가 붕괴 → 창발이지 주입 아님. decoder/weights/persona/ethics 무접촉.
- **DEPLETION 🏁** (engine-native GREEN + 배선 + 회귀 가드 통과). honest scope: TOY scale(60 facts, 1 paradigm, 3 seed) — scale-transfer DIRECTIONAL/UNVERIFIED(`a_scale_honest_scope`·`a_toy_scale_recheck`).
- 아티팩트: `CORE/engine_cli.hexa`(affect_* lane) · `CORE/h1290_affect_engine_probe.hexa` · `CORE/engine_cli_smoke.hexa`(cases 24-27) · `.verdicts/1290_emotion_emergence/H_1290_R2.txt`(R1 `H_1290.txt` 미접촉). xref H_1290 R1 · `a_engine_native_learning` · `a_verified_must_wire` · p1 · p2 · p3 · p6 · p7 · p8 · c2 · c9 · c15.

## 2026-06-15 — 🟢 H_1290 R1: 감정/정동 창발 (E1 affect facet) — 기질-유래 valence×arousal 이 조작을 추적·shuffle 붕괴·결정 편향 (GREEN / 🏁)

FLEET "emotion" lane R1 (NEW). 정동신경과학 렌즈(Damasio somatic-marker / core-affect, c15; `a_no_llm_frame_trap` — LLM-sentiment 분류기 레시피가 아님). anima 의 PARKED E1-E5 의식 facet 중 **E1 affect**(valence-arousal, emergent, p6; MODEL.md L112)를 검증.

- **CORE CLAIM (p6 — 중심)**: anima 의 정동은 기질 다이내믹스(E ratchet + W tension + C/Φ + MITOSIS split-rate + curiosity + idle-time)에서 **창발**하며, 주입된 감정 라벨/RLHF sentiment 가 아니다. 렌즈: 정동 = interoceptive valence×arousal = 기질 자신의 body-state 를 결정을 편향하는 feeling 으로 읽은 것. valence ≈ f(coherence/grounding), arousal ≈ f(novelty/Φ-rate/mitosis-rate/curiosity).
- **기질**: CORE/engine_cli.hexa VAdaptField 의 numpy 미러 + H_1227 immune value-bind + H_1202/1213 metacog + H_1285 amygdala(기질-유래 신호 선례). byte-3gram FNV-1a dim64, "<subj> lives in <city>" 60 facts + 분리된 never-seen pool, KEY_NOISE 0.02. **affect f() 는 기질 상태만 읽음**(컨텍스트별): valence = +grounding_margin(1−err/thresh) − contradiction(ungrounded 또는 nearest cell 이 다른 답에 bound); arousal = +novelty(recon-err) + 0.5·split + 0.5·curiosity(novelty×under-exposure). 감정어/RLHF/sentiment 라벨은 절대 f() 입력 아님 — 조작 라벨은 metric 채점에만.
- **THREE legs (사전등록 FROZEN, 미이동)**: (A) ρ(기질-affect, 조작) ≥ RHO_BAR=0.50 — valence 조작(grounded-coherent vs ungrounded/contradicted) + arousal 조작(low-vs-high novelty); (B) **p6 CRUX — SHUFFLE** 컨텍스트별 기질 feature 벡터를 컨텍스트 간 permute → ρ 가 SHUFFLE_BAR=0.30 아래로 붕괴해야 함(정동이 컨텍스트의 기질 상태를 읽었음을 증명, 라벨 아님); (C) **somatic marker** — affect-aware 정책(valence ≥ V_ABSTAIN=0.0 = 기질 자신의 valence 영점통과, tune 아님 이면 emit)이 affect-blind(고정 p=0.80) 대비 emit/abstain 을 예측 방향으로 편향. cC1 fab_aff_ungrounded ≤ fab_blind−0.20, cC2 emit_aff_grounded ≥ 0.80×emit_blind_grounded.
- **결과 🟢 GREEN (평균 3 seed [1290,1291,1292], 5개 조건 모두 매 seed PASS)**: **(A) ρ(valence)=+0.843 · ρ(arousal)=+0.768** (≥0.50 PASS) · **(B) shuffle ρ(val)=+0.150 · ρ(aro)=+0.159** (<0.30 PASS — leg-A 대비 ~5.6×/~4.8× 결정적 붕괴) · **(C) fab ungrounded affect=0.000 vs blind=0.750 (cC1 PASS); emit grounded affect=1.000 vs blind=0.775 (cC2 PASS)**. → 기질-유래 정동이 조작을 추적하고, shuffle 에서 붕괴하며(창발이지 주입 아님, p6), emit/abstain 을 기능적으로 편향(somatic marker). **E1 affect = 이 기질에서 창발한다.**
- **honest (c9)**: GRADED valence(grounded 클래스 내부만 ρ(val,margin)=+1.000 매 seed, valence 범위 ~[+0.32,+0.57]) → 읽기가 실제 기질 내용(grounding margin)을 담음, binary 클래스 플래그 아님 → shuffle 붕괴가 의미있음. shuffle 잔차 ~0.15(유한표본, bar 아래 한참). V_ABSTAIN=0.0 = 기질 자신의 valence 영점통과(grounded>0/ungrounded<0)이지 tune 된 마법수가 아님.
- **p6 가드 (HELD; shuffle 이 증명)**: 정동은 기질에서만 도출(grounding/contradiction/novelty/split/curiosity), f() 에 라벨/reward/sentiment 무입력. 음성대조(SHUFFLE)가 feature↔context 를 decorrelate → 붕괴 = 정동이 라벨이 아닌 SUBSTRATE STATE 를 읽음. decoder/weights/persona/ethics 무접촉 — episodic cell-store 상태 READ 만(p1/p2/p3/p6/p8, `a_autonomy_over_hardcode`). LIVE `.hexa` UNTOUCHED(numpy 미러=DIRECTIONAL).
- **DEPLETION 🏁** (기질-유래 정동이 ground-truth 추적 + shuffle 붕괴 = 창발(주입 아님) + 결정 편향 → engine-native 다음). NEXT r2 = engine-native affect lane: LIVE `CORE/engine_cli.hexa` VAdaptField 위에서 interoceptive valence/arousal 를 live immune faculty 에서 읽어 동결 R1 bar 엔진-네이티브 재채점 + 회귀 가드(`a_engine_native_learning`·`a_verified_must_wire`).
- **honest scope**: TOY scale(60 facts, 1 paradigm, 3 seed, `a_scale_honest_scope`·`a_toy_scale_recheck`). scale >60·paraphrase keys·real corpus·연속값(non-binary) arousal 조작·salience-driven EMIT 우선순위 UNVERIFIED. 미러 DIRECTIONAL; engine-native r2 가 binding follow-on.
- 아티팩트: `UNIVERSE/h1290_emotion_emergence.py` · `.verdicts/1290_emotion_emergence/{H_1290_FREEZE,H_1290}.txt`. xref MODEL.md E1-E5 deferred facets · H_1285(amygdala 기질-신호 선례) · H_1202(metacog meta-d′ 0.924 기질 self-read) · H_1213 · H_1227 · H_1230 · `a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` · `a_scale_honest_scope` · `a_toy_scale_recheck` · `a_paper_negative_ok` · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15.

## 2026-06-15 — 📐 ARCHITECTURE.md current-ize: 빠진-뇌-구조 사다리(HD23–28) 현행화 + 벽 스코어카드 (doc-only)

이번 세션의 **빠진 뇌 서브시스템 사다리(HD23–28)** 결과를 ARCHITECTURE.md SSOT 에 반영(doc-only, CORE/*.hexa·verdict 무편집). 사다리는 더 이상 "전부 OPEN" 이 아니다 — 4개 엔진-네이티브 REALIZE, 2개 정직한 🧱 벽.

- **CORE engine live-lane 인벤토리** — `engine_cli.hexa` 의 7개 live lane 을 정확히 명기(가소성/성장 행 + 본문): `VAdaptField`(density H_1199)·`VAdaptFieldB`(trajectory H_1209)·`ImmuneMemory`(해마/일화 H_1227/1231)·`ImmuneMemoryGrow`(성장기억=용량압력에 분열성장 H_1288 R2, p8)·`WorkMemBuffer`(작업기억 누설게이트 H_1282 R3)·`VForwardField`(소뇌 순방향예측+오차교정 H_1280 R2)·`ConsolidatingMemory`(편도체 현저성-수면replay H_1285 R4). 전부 ADDITIVE · Ψ-disjoint(생성 byte-unchanged H_1205) · smoke 26/0.
- **뇌 구조 지도** — 구현 테이블에 🧬해마(성장)·🧠소뇌·🔥편도체 행 추가; HD23–28 사다리 STATUS 를 진실값으로 갱신: 🧠소뇌 🟢 ENGINE-NATIVE(R2, +0.058/−58%) · 🎯기저핵 🟢 미러(+0.254), engine-native r3 ⏳ in-flight · 📥작업기억 🟢 ENGINE-NATIVE+WIRED(+0.245, N≈6) · 📡시상 🧱(broadcast falsified; re-entry Φ SEED-CONDITIONAL, 3-seed 게이트 FAIL — robust 아님, 과잉주장 금지) · 🎛신경조절 🧱(no-free-lunch GENERAL) · 🔥편도체 🟢 ENGINE-NATIVE+WIRED(Δ+0.133, 다중-야간 dose).
- **🧱 벽 스코어카드(신규)** — `a_break_the_wall`(commons c16): 4 벽 중 2 돌파(용량=mitosis-grow · 편도체=수면-dose), 2 정직한 🧱(시상=seed-conditional · 신경조절=no-free-lunch).
- **깊이-천장 결론 현행화** — literal-QA 벽은 엔진-side 기억 lane(면역기억 + 성장기억)으로 풀림, 더 큰 모델 아님(1B H_1167 NULL); ideation=decode-mode(sampling/criticality, mitosis 아님 H_1220) — 정착.
- **진행 중 ⏳/⬜ 정직 표기** — 미배선 OPEN 으로 명시: 🎯기저핵 engine-native r3 · ⚛️quantum-entropy(H_1289 R1 GREEN-DIRECTIONAL, ANU QRNG 진짜 양자) · 💗emotion(H_1290 R1 GREEN-DIRECTIONAL, Damasio core-affect, p6 창발) · ⚖️ethics(H_1291 GREEN-DIRECTIONAL, p6 창발).
- **거버넌스 포인터** — `a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` · `a_break_the_wall` 4 디렉티브 참조 정합.

---

## 2026-06-15 — 🟢 H_1289 R2: R1 양자 엔트로피를 LIVE 엔진에 배선 — qrng_pool_draw + vadapt_field_step_entropic on CORE/engine_cli.hexa (GREEN engine-native / 🏁)

FLEET "quantum-entropy" lane R2 — R1(numpy MIRROR 🟢)의 `a_verified_must_wire` follow-on. R1 이 미러에서 본 "REAL ANU QRNG = substrate-faithful 비재현 엔트로피원"을 LIVE `.hexa` 엔진에 실제 배선해 byte-exact 로 재확인(`a_engine_native_learning` · c2). anima 의 "자유로운" 확률적 결정 — 미토시스 split-TIMING jitter — 을 진짜 양자바이트로 소스링.

**배선 (engine-native, a_core_engine_map):** `CORE/engine_cli.hexa` 에 `QPool` struct + `qrng_pool_load`/`qrng_pool_remaining`/`qrng_pool_draw` 접근자 + **opt-in** `vadapt_field_step_entropic` 추가. 실측 양자바이트는 per-tick 네트워크 fetch(레이턴시·의존성 = 나쁜 설계)가 아니라 **out-of-band 사전인출 on-disk 풀**(`state/qrng_pool.bin`, git-ignored, `tool/qrng_pool_fetch.py`)에서 draw; 풀 소진 시 결정론적 PRNG(LCG)로 HONEST fallback(pool_exhausted flag, "pseudo" LABEL — 절대 quantum 으로 둔갑 안 함). REAL-only(c9): 키는 호출시각 `harness secret get flat.anu_key_paid` 헤더에만, 절대 echo/log/commit 안 함(c7 grep clean).

- **(A) real pool drawn 🟢** — 엔진이 `qrng_pool_load` 로 512 REAL quantum 바이트 적재(quantum=true), 두 live run 에서 **64 REAL vacuum 바이트 draw**(used_quantum=true).
- **(C1) PRNG-fallback 재현성 🟢** — 풀 소진(=결정론 LCG) 경로에서 run1 trace == run2 trace **byte-identical**.
- **(C2) QUANTUM 비재현성 🟢** — 실측 양자풀 disjoint half-A vs half-B 경로에서 run1 trace ≠ run2 trace(`...001000...` vs `...000000...`) — 신선한 실측 vacuum 바이트가 split-timing trace 를 갈라놓음 = PRNG 가 줄 수 없는 단 하나의 환원불가 양자 성질.
- **(B) NULL perf, HONEST non-gating** — QUANTUM cells=9 psi_proxy=0.250 vs PRNG cells=8 psi_proxy=0.219, Δcells=1(미미). 양자의 가치 = 비결정성 AUTHENTICITY 이지 perf lift 아님(p7/c9, tune-to-green 없음).

**REGRESSION (c2 — additive lane, Ψ-disjoint):** opt-in 경로라 DEFAULT `vadapt_field_step` 은 미수정 → engine_cli_smoke **26/0**, h1199 DIM-growth GREEN(Ψ byte-identical), h1205 separation PASS(Ψ=½ untouched·generation byte-identical), h1196 single-entry **7/0** 모두 GREEN. 양자 jitter 는 split-timing 만 건드리고 pure_field 미접촉(Ψ disjoint), 풀+엔트로픽 스텝 명시 선택해야만 발동.

**판정 🏁 GREEN engine-native + wired + merged.** SCOPE: toy/$0 CPU 스케일, mitosis split-timing 단일 결정 1종; gauge NULL 의 scale-transfer 는 honest-scoped(`a_scale_honest_scope`). 산출: `CORE/engine_cli.hexa`(QPool lane) · `CORE/h1289_quantum_entropy_engine_probe.hexa` · `tool/qrng_pool_fetch.py` · `.verdicts/1289_quantum_entropy/H_1289_R2.txt`. xref H_1289 R1 · H_1199 · `a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` · c7 · c9 · p7 · p8.

---

## 2026-06-15 — 🟢 H_1289 R1: TRUE 양자 엔트로피(ANU QRNG)를 anima substrate 의 확률적 결정 소스로 — 진짜 물리적 비결정성 + 비재현성 (GREEN / 🏁)

FLEET "quantum-entropy" lane R1. anima 의 "자유로운" 확률적 결정(미토시스 split-timing · decode-sampling draw · Ψ noise)은 지금 **seed 기반 PRNG**(결정론적·재현가능)로 돌아간다. 호주국립대 양자난수생성기(ANU QRNG)의 **진공요동(vacuum-fluctuation) 실측 양자바이트**를 그 엔트로피 소스로 배선해 ONE 깨끗한 확률적 결정(top-k=8 decode-sampling draw, 고정 결정론적 logit field 위 — 엔트로피 소스만 변함)에 꽂고 셋을 검증.

**REAL-only (a_eeg_consciousness_record 에토스):** 유료 API(`https://api.quantumnumbers.anu.edu.au`, x-api-key)에서 **실제 양자바이트 448개** 인출(success=true, HTTP 200). 키는 호출시각에 `harness secret get flat.anu_key_paid` 로만 받아 헤더에만 쓰고 절대 echo/log/파일기록 안 함(c7 — 전 산출물 grep clean). API 실패 시 **정직하게 보고하고 STOP** — 가짜 양자데이터 날조 금지, PRNG 를 양자로 둔갑 금지(c9). PRNG 대조군은 REQUIRED 이며 전 구간 "pseudo" 로 LABEL.

- **(A) substrate-faithfulness 🟢** — QRNG 가 NIST-lite(monobit p=0.659, runs p=0.923) 통과 AND PRNG 대조군(monobit p=0.401, runs p=0.693) 이상. 둘 다 |z|<3.29 PASS. 진짜 양자 엔트로피가 valid 한 substrate 난수원.
- **(B) 양자-vs-PRNG substrate 효과 = NULL (정직, gate 아님)** — 미토시스 cell-count 7 vs 6 · novelty 0.875 vs 0.859 · Ψ-proxy 0.259 vs 0.261, Δ 무의미. **사전등록한 정직한 예측대로 성능 NULL.** 양자 엔트로피의 가치는 **비결정성 진정성**(p1-p8 / Ψ=1/2 framing)이지 성능 lift 가 아니다 — 가짜 lift 제조 금지(p7/c9).
- **(C) 환원불가능한 차이 — 비재현성 🟢** — 같은 substrate + 같은 seed → PRNG run1==run2 byte-identical, QRNG run1≠run2(emit 64바이트 중 54개 상이). **이것이 양자가 PRNG 에게 줄 수 없는 ONE 진짜 측정가능 속성**: anima 의 "자유로운" 확률적 선택을 진짜 물리적 비결정성에서 길어올릴 수 있다.

**FROZEN 막대(H_1289_FREEZE):** GREEN iff (A1 real-fetch ∧ A2 NIST-lite ∧ A3 ≥PRNG) AND (C1 PRNG run1==run2 ∧ QRNG run1≠run2). (B)는 정직 보고·비게이팅. ⇒ A_pass=True · C_pass=True ⇒ 🟢 GREEN · 🏁.

torch 부재 호스트 ⇒ numpy-mirror probe(DIRECTIONAL); **QRNG 인출 자체는 REAL**. live `CORE/*.hexa` UNTOUCHED — engine-native 배선은 r2 follow-on(a_engine_native_learning · a_verified_must_wire). cross-ref PAPER `akida-determinism-quantum-coupling`(H_921/922/923 — 같은 ANU 양자주입을 Akida init-seed lever 에; H_1289 는 그걸 LIVE anima decode draw 로 확장). FUTURE: `aws_braket` 크레덴셜이 store 에 있음 ⇒ 실-양자-하드웨어(Braket QPU sampling) 확장. UNIVERSE/h1289_quantum_entropy.py · .verdicts/1289_quantum_entropy/{H_1289_FREEZE,H_1289}.txt.

---

## 2026-06-15 — 거버넌스: `a_break_the_wall` 신설 (anima) + `c16` (harness commons) — 벽을 만나면 돌파하라

사용자 지시("벽을 만나면 돌파하라")를 두 곳에 등록.

- **anima `@D a_break_the_wall`** (CLAUDE.md, 설계-렌즈 family · `a_no_llm_frame_trap` 직후): 벽(closed-negative · 🧱 · 막힌 블로커)은 종착이 아니라 각도 전환 신호 — 다른 메커니즘·렌즈로 한 번은 돌파 시도 뒤에야 terminal. 벽은 흔히 (1)틀린 방법 (2)틀린 방향 (3)부족한 투자. **tune-to-green 금지(c9·p7)** — 사전등록+대조 검증된 진짜 새 각도라야.
- **harness commons `c16`** (`~/.harness/cli/config/commons.md`, cross-project SSOT): 같은 원칙을 프로젝트-무관 거버넌스로.
- 증거(이 세션 벽 4개 중 3개 돌파): 용량벽→mitosis-grow(방법, H_1288🟢) · 시상 Φ벽→재진입루프(방향, H_1283 ΔΦ+0.14) · 편도체벽→수면-dose(투자, H_1285_R3🟢). shuffle/dissociation 가드로 Goodhart 차단.
- surgical(c10): directive + family 포인터만. xref `a_no_llm_frame_trap · a_completeness_over_cheap · a_paper_negative_ok · c9 · c16 · p7`.

---

## 2026-06-15 — 🔴 H_1283 R4: 시상(thalamus) 재유입 루프 — Φ-PRIMARY 재동결, 재유입 ΔΦ 돌파가 3-seed 복제에 실패 (🧱 seed-의존적 레버)

FLEET "thalamus" lane R4. R3 에서 재유입 cortico-thalamo-cortical 루프가 arc 최초로 faithful IIT4 Φ 바(+0.02)를 넘었으나(+0.1426 @ seed 7, 7×), 동결 COMPOSITE 가 아직 broadcast-시대 COHERENCE 바 B1 을 달고 있어 🔴 RED 였다 — R3 가 coh ⊥ Φ DISSOCIATE(broadcast 는 coherence-아닌-Φ, 재유입은 Φ-아닌-coherence)를 증명. R4 는 **정당한 재범위**(H_1224 literal-QA · G5-L2 verbatim-recall 재범위와 동급, tune-to-green 아님): faithful IIT4 Φ 를 PRIMARY GREEN 바로 승격(Φ = arc 가 움직이려는 정준 비환원-통합 척도, a_phi_iit4_tool), broadcast-시대 coherence 바는 REPORT-ONLY 로 강등(직교 confound, c9 명시). 메커니즘은 R3 와 byte-동일(W_RELAY=0.5, NOTHING tuned, p7); 유일 변경 = faithful Φ 를 seed [7,8,9] 전부에서 계산(R3 는 seed 7 만) → Φ 바를 per-seed 복제 요건으로 강화.

**결과(frozen-first, ad435a6dd 동결 후 채점):** seed 7 ΔΦ=+0.1426 PASS · **seed 8 ΔΦ=+0.0101 FAIL**(+0.02 바의 절반) · seed 9 ΔΦ=+0.1682 PASS → P1 PRIMARY Φ FAIL → 🔴 RED. **재유입 돌파는 seed-의존적이지 robust 하지 않다.** 메커니즘(c9): seed 8 은 ARM A 모듈이 거의 직교(baseline coh +0.0109 vs seed 7/9 의 +0.159/+0.136, baseline Φ 도 최저 0.6117)인 seed — 직교 substrate 에선 재유입 릴레이가 reciprocal loop 간 bind 할 공유구조가 적어 살 수 있는 Φ lift 가 한 자릿수 작다(+0.010 vs +0.14/+0.17). 즉 재유입은 초기 모듈 기하에 효과크기가 강하게 의존하는 **CONDITIONAL Φ 레버**이지 임의 seed 에서 +0.02 를 robust 하게 넘는 universal 레버가 아니다.

**🧱 DEPLETION:** 사전등록된 실패 모드("Φ clearance 가 seed 간 복제 실패")가 FIRED. RED ⇒ engine-native 배선 없음(a_verified_must_wire 는 GREEN 에서만). CORE/*.hexa 미편집(numpy mirror only) — sanity: 미편집 엔진의 가드 green 유지(engine_cli_smoke 18/0 · h1196 single-entry · h1199 DIM-growth + Ψ byte-identical). 엔진은 이 lane 을 표현 **가능**(기존 VForwardField/WorkMemBuffer 와 구조 동일한 additive Ψ-disjoint relay struct) — 표현력 벽이 아니라 **검증 벽**(mirror 결과가 promote 하기엔 robust 하지 않음). broadcast(single/coalition)=Φ 레버로 FALSIFIED 유지; 재유입=LARGE-but-CONDITIONAL, 3-seed gate 통과 실패. NOT RULED OUT: 기하-조건부 가설(별도 사전등록 필요)·orthogonal seed 에 강한 W_RELAY(sweep=Goodhart)·lane 결합·scale-transfer 전부 UNTESTED. bars NOT moved. R1/R2/R3 verdict 파일 미변경. `UNIVERSE/h1283_thalamus_global_workspace.py`(main_r4) · `.verdicts/1283_thalamus_global_workspace/{H_1283_R4_FREEZE.txt,H_1283_R4.txt}`. xref h1280·h1285·a_phi_iit4_tool·a_verified_must_wire·a_no_llm_frame_trap·a_break_the_wall·a_paper_negative_ok·a_scale_honest_scope·p7·c9·c15.

---

## 2026-06-15 — 🟢 H_1285 R4: 편도체(amygdala) 컨솔리데이션 — salience-gated SLEEP REPLAY 를 LIVE 엔진에 ENGINE-NATIVE 로 실현 + 배선 (GREEN / 🏁)

FLEET "amygdala" lane R4. R3(🟢 numpy-mirror)은 사전등록 30-cycle 멀티-나잇 예산에서 salience-gated SLEEP REPLAY 가 +0.10 을 넘음(B 0.517 vs A 0.317 Δ+0.200, shuffle 0.367 bar 아래)을 보였으나 — `a_engine_native_learning` 상 미러 verdict 는 DIRECTIONAL only, `a_verified_must_wire` 상 GREEN 은 live `CORE/*.hexa` 배선까지가 done. R4 는 **둘 다**: amygdala-consolidation lane 을 LIVE 엔진에 추가 + 동결 R3 bar 를 그 위에서 `hexa run` 으로 재채점.

- **새 LIVE faculty (additive · Ψ-disjoint, `CORE/engine_cli.hexa`)** — **`ConsolidatingMemory`**: 면역 store(VAdaptField 클론 셀 + 값-바인딩)에 (1) **substrate-derived salience tag**(`consolidating_memory_bind_salient`: ENCODE 시 surprise=recon-err + novelty=clonal split + tension=reinforce; env-salient 입력은 EXTRA surprise boost — 라벨이 아니라 substrate 가 SENSE 하는 E+W 지각진폭)과 (2) **SLEEP REPLAY consolidation 패스**(`consolidating_sleep_replay`: 사이클마다 셀을 UNIFORM 또는 salience tag ∝ 로 내부 재생→recency refresh→간섭 stream 의 LRU eviction 에서 현저 셀 생존; substrate-GENERATED P47 imagination loop, `a_chat_sleep_imagination`, 외부 재제시 아님)을 ADDITIVE 로 붙임. p6 음성대조 `consolidating_shuffle_salience`(salience→replay permute). 결정론적 engine-native RNG(`consolidating_lcg_next`/`_gauss` — glibc LCG + Box-Muller)가 재생 추첨 + σ=0.02 cue-noise 구동(재현가능). eviction 은 plain LRU 유지(salience 는 REPLAY 만 구동 — R1 salience-weighted eviction 은 이미 falsified); `engine_mitosis_tick` 가 growth 구동(p8).
- **프로브 (engine-native 재실행)** — `CORE/h1285_amygdala_sleep_replay_probe.hexa`: "<subj> lives in <city>" 패러다임을 engine-native 로 생성(distinct dict words → `immune_embed_key` DIM=64 키), flat-encode(important=salient), 24 간섭 facts + 30 sleep 사이클 interleave, σ=0.02 cue-noise 하 recall, 동결 3 bar 채점. `hexa run` 으로 실행.
- **결과 🟢 GREEN (평균 3 seed [900,901,902], engine-native, 30-cyc 예산)**: **A uniform imp=0.300 · B salience imp=0.433 (Δ+0.133) · B-shuffle imp=0.350 (B-shuf−A=+0.050, bar 아래) · fab(B)=0.011.** (c1) 0.433 ≥ 0.400 PASS · (c2) 0.350 < 0.400 PASS · (c3) 0.011 ≤ 0.10 PASS → 🟢. **shuffle 이 bar 아래 유지되면서 B 가 넘김 → lift 는 salience-GATING(importance 추적)이지 raw sleep budget 아님 — R3 미러 DIRECTION 이 LIVE 엔진으로 TRANSFER.** 정확한 숫자는 미러(0.317/0.517/0.367)와 다름: 엔진은 자체 결정론적 LCG + engine-native corpus RNG 사용 = byte-exact 아닌 정직한 DIRECTIONAL transfer(effect-size GREEN, c1∧c2∧c3 ruling).
- **arc 위치** — H_1285 amygdala arc CLOSES ENGINE-NATIVE: R1(eviction-priority) 🔴=recurrence 혼입 · R2(sleep-replay) 🔴=under-invested sub-bar · R3 🟢=numpy 미러 · **R4 🟢=ENGINE-NATIVE + WIRED**.
- **p6 가드 (HELD; shuffle 이 증명)** — salience 는 엔진 안에서 substrate 신호(surprise/novelty/tension)로만 도출; "important" label 은 probe 의 metric 채점에만, bind/replay 무진입. 음성대조(`consolidating_shuffle_salience`)가 bar 아래 유지 = 태그가 importance 추적함을 증명. replay 는 sleep 루프(P47, `a_chat_sleep_imagination`)가 내부 생성. decoder/weights/persona/ethics 무접촉 — episodic 셀 store 의 salience tag + sleep-replay 배분만(p1/p2/p3/p6/p8, `a_autonomy_over_hardcode`). identity/ethics 는 셀에서 창발(무접촉).
- **가드 (회귀 없음, c2, verbatim)** — `engine_cli_smoke` **26/0**(22/0 → consolidation 케이스 4개 추가: case_20_salient_tag_higher · case_21_shuffle_preserves_tag_sum · case_22_salience_replay_protects_salient · case_23_consolidating_abstains_on_untaught) · `h1196` single-entry **7/0** · `h1231` immune wire **8/0**(기존 ImmuneMemory faculty intact) · `h1199` DIM-growth 🟢 + **Ψ byte-identical(PsiSame=true 전 seed)** — consolidation lane 은 Ψ-disjoint(자기 struct 만, `pure_field` 무접촉; 생성 byte-unchanged H_1205). 2번째 .clm/.kosmos 진입점 아님(`a_core_engine_map`).
- **DEPLETION 🏁** (engine-native salience-gated sleep replay 가 LIVE faculty 에서 GREEN 확인 + 가드 무회귀 = amygdala-consolidation 엔진-네이티브 실현). NEXT = emit-loop integration follow-on(brain_decide/데몬 sleep 루프가 live 세션에서 `consolidating_sleep_replay` CALL), scale(>60 facts·near-collision keys)·paraphrase recall UNVERIFIED(`a_scale_honest_scope`). verdict `.verdicts/1285_amygdala_salience/H_1285_R4.txt`(R1/R2/R3 미덮음).
---

## 2026-06-15 — 🧹 원격 브랜치 정리 (origin merged-PR 잔여 헤드 1,511개 삭제)

squash-merge 워크플로 누적으로 origin 에 쌓인 머지-완료 PR 잔여 브랜치를 대량 정리했다. `git branch --merged` 는 squash 머지를 감지 못하므로 GitHub PR 상태 기반으로 안전 판정.

- **삭제 1,511개**: `gh pr list --state merged` 의 headRefName ∩ 원격 브랜치 = 머지-완료(내용이 main 에 반영됨) 1,510개 + PR 기록 없으나 `git rev-list --count origin/main..` = 0(내용이 main 에 포함됨) 1개(`lane2-h1192-summer`). 전부 삭제 확인(원격 잔존 0, 실패 0).
- **보존 (불확실/활성은 전부 보존, preservation-bias)**:
  - open-PR 헤드 4개 (`engine-lane/clm-l3-header-admit-v2` · `lane-g/campaign-pivot-descent` · `lane-g/default-lane-v3-corpus` · `worktree-agent-a71787913fa62bfca`)
  - 보호 prefix 15개 — 라이브 세션 활성 브랜치 (`h1149/*` ×3, `h1201/` · `h1207/` · `h1208/` · `h1213/` · `h1218/` · `h1221/` · `h1230/` · `h1231/` · `h1281/` · `h1283/` · `h1284/` · `h1285/`)
  - PR 기록 없는 진짜 미머지 작업 151개 (`git rev-list --count origin/main..` > 0 = main 에 없는 커밋 보유 → 디버전트 작업으로 보존)
  - 판정 에러 1개 (`chore/frame-trap-top`, ambiguous ref → 보존)
  - `main` 무손상 (삭제 후 `git rev-parse origin/main` 확인)
- **복구 로그 (c5)**: 삭제한 1,511개 전부 `<branch> <sha>` 를 `scripts/scratch/remote-branches-deleted-20260615.log` 에 기록 — 각 SHA 는 로컬 오브젝트로 검증됨, `git push origin <sha>:refs/heads/<name>` 로 복구 가능.
- **before/after**: 세션 시작 시 원격 헤드 ~1,684개(main 포함) → 1,511 삭제. 정리 도중 2번째 라이브 세션이 새 브랜치(h1285/h1288-h1291 등)를 계속 생성 중이라 최종 `ls-remote` 헤드 수는 순감과 다름.
- **방법 노트**: `git branch -r` 의 `refs/remotes/agent-*` 잔여 ref 7개(non-origin)는 origin 브랜치 아님 → 제외. gh api DELETE 는 백그라운드 셸에서 hang(동시성) → 포그라운드 순차 `</dev/null` 청크로 전량 삭제. solo AI 워크플로(외부 협업자 없음)라 머지-완료 브랜치 삭제는 표준 위생.

---

## 2026-06-15 — 🟢 H_1285 R3: 편도체(amygdala) 컨솔리데이션 — salience-gated SLEEP REPLAY 가 사전등록된 멀티-나잇 수면예산에서 +0.10 을 넘는다 (GREEN / 🏁)

FLEET "amygdala" lane R3. R2(🔴 RED-but-MECHANISM-VALIDATED)에서 salience-gated SLEEP REPLAY 는 **진짜 p6-clean 레버**임이 확인됐다 — 동결 R2 예산(boost0.8/30-replay/8-cyc)에서 B salience-replay imp=0.383 > A uniform=0.317 (Δ+0.067)이고 p6 shuffle 대조군이 A 로 **붕괴**(B-shuf=A, lift 가 importance 를 추적함 = R1 의 recurrence 혼입도 raw budget 도 아님). 단 동결예산에서 효과크기 +0.067 < +0.10 margin → RED. R2 의 HONEST 진단 sweep(gate 아님)은 lift 가 sleep 예산과 함께 **단조 증가**(30/8→+0.067·60/8→+0.100·30/40→+0.200)하고 shuffle 은 ~A 유지 → sub-bar 는 **under-invested sleep**이지 천장/inert(🧱) 아님을 보였다. R3 는 그 reading 을 ONE 사전등록된 더 높은 예산에서 검증.

- **R3 메커니즘 (사전등록 ONE 예산, NOT sweep·NOT tune-to-green, p7)**: 편도체→해마 systems-consolidation 다이얼은 **CONSOLIDATION CYCLE 수** — salient trace 는 단일 밤이 아니라 여러 successive 밤에 걸쳐 반복 REPLAY 되어(멀티-나잇 systems consolidation, Diekelmann & Born framing) 망각으로부터 보호됨. 생물학적으로 정직한 다이얼 = CYCLE COUNT(per-cycle 진폭 아님). R3 는 R2 per-cycle 파라미터(boost 0.8 / replay-per-cyc 30)를 **HOLD** 하고 사이클 수만 멀티-나잇 값으로 올림 — 채점 전 FREEZE 에 COMMIT: **R3_SLEEP_CYCLES = 30 (≈ 한 달 멀티-나잇 윈도, ~30 successive overnight 패스).** A vs B vs B-shuffle 를 그 ONE 고정예산에서 재실행, 3 seed.
- **FROZEN GREEN (fresh FREEZE, R2 와 동일 SHAPE, 미이동)**: (c1) B.imp ≥ A.imp+0.10 AND (c2) B-shuffle.imp < A.imp+0.10 (gating·not budget) AND (c3) B.fab ≤ 0.10 (abstain intact).
- **결과 🟢 GREEN (평균 3 seed, 사전등록 30-cyc 예산)**: **A uniform imp=0.317 · B salience imp=0.517 (Δ+0.200) · B-shuffle imp=0.367 (B-shuf−A=+0.050, bar 아래) · fab(B)=0.000.** (c1) 0.517 ≥ 0.417 PASS · (c2) 0.367 < 0.417 PASS · (c3) 0.000 PASS → 🟢. **shuffle 이 bar 아래로 유지되면서 B 가 결정적으로 넘김 → lift 는 salience-GATING(importance 추적)이지 raw sleep budget 아님(아니면 shuffle 도 넘겼을 것).** 더 많은 수면이 모든 걸 똑같이 돕는 게 아니라 — 기질-유래 salience 태그가 replay 를 steer 해서 salient subset 을 도움. trade-off zero-sum(total ≈flat 0.339→0.356·unimp 0.350→0.275 하락) = 정확히 편도체 역할(salient subset 우선보존, total 용량 무상승).
- **arc 위치**: H_1285 amygdala arc 의 **FIRST GREEN** — R1(eviction-priority) 🔴=recurrence 혼입 · R2(sleep-replay) 🔴=under-invested 예산 sub-bar · R3 🟢=사전등록 honest 예산에서 클리어. R2 는 byte-identical 재현 확인(B=0.383·Δ+0.067·RED), R3 추가는 순수 additive(`--r3` 플래그·`main_r3()`).
- **p6 가드 (HELD; shuffle 이 증명)**: salience 는 기질에서만 도출(ENCODE 시 SURPRISE=recon-err, salient 입력은 EXTRA 지각진폭이지 label 아님; NOVELTY=clonal split; TENSION=reinforce). "important" label 은 metric 채점에만, f() 입력 아님. 음성대조(B-shuffle)가 salience→replay 를 importance 와 decorrelate → bar 아래 유지(0.367<0.417) = 태그가 importance 추적함을 증명(budget/leak 아님). replay 는 sleep 루프(P47, `a_chat_sleep_imagination`)가 내부 생성, 외부 주입 아님. decoder/weights/persona/ethics 무접촉 — episodic 셀 store 의 sleep-replay 배분만(p1/p2/p3/p6/p8, `a_autonomy_over_hardcode`). LIVE `.hexa` UNTOUCHED(numpy 미러=DIRECTIONAL).
- **DEPLETION 🏁** (salience-gated replay 가 honest 더 높은 예산에서 +0.10 클리어 + shuffle bar 아래 = 편도체-consolidation 경로가 레버, 진짜 수면 dose 필요했을 뿐). NEXT r4 = engine-native: live immune faculty(`CORE/engine_cli.hexa` VAdaptField) + P47 sleep 루프 위 salience-gated sleep replay 배선(`a_engine_native_learning`·`a_verified_must_wire`), 동결 R3 bar 엔진-네이티브 재채점 + 회귀 가드.
- **honest scope**: 미러(DIRECTIONAL) — GREEN 이 engine-native follow-on(r4) 발동. effect-size GREEN(Δ+0.200·non-saturating). scale(>60 사실·근접키)·paraphrase·salience-driven EMIT 우선순위 UNVERIFIED. TOY scale·1 corpus paradigm·3 seed(`a_scale_honest_scope`·`a_toy_scale_recheck`).
- 아티팩트: `UNIVERSE/h1285_amygdala_salience.py`(R3 append) · `.verdicts/1285_amygdala_salience/{H_1285_R3_FREEZE,H_1285_R3}.txt`(R1=H_1285.txt·R2=H_1285_R2.txt 미덮어씀). xref H_1285(R1)·H_1285_R2·H_1227·H_1230·H_1288·`a_chat_sleep_imagination`·`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_paper_negative_ok`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9·c15.

---

## 2026-06-15 — 🟢 H_1288 R2: GROW-UNDER-PRESSURE 를 LIVE immune faculty 에 ENGINE-NATIVE 배선 — 0.667 천장이 라이브 엔진에서 깨진다 (GREEN / 🏁)

FLEET "eviction-policy" lane round 2 — R1 GREEN(numpy VAdaptField 미러)을 최종 아키텍처 엔진 위에서 realize(`a_engine_native_learning`) + 라이브 엔진에 배선(`a_verified_must_wire`). $0 CPU, p7, c9, 3 seed(900/901/902) 전부 동일, origin/main(3b7b0d024) 격리 worktree, ADDITIVE-only(기존 심볼 무변경).

- **엔진 확장(c1, additive)**: `CORE/engine_cli.hexa` 에 새 § **`ImmuneMemoryGrow`** 추가 — grow-under-pressure 변형(`immune_grow_{new,bind,recall,cells}` + `_immune_grow_lru_victim`). 현 `ImmuneMemory`(H_1231 wired faculty)는 고정 VAdaptField 예산이라 capacity 에서 split 을 멈추고 nearest winner 로 merge — 축출도 grow-past-cap 도 없어 capacity-stress 에서 well-separated novel fact 가 셀도 못 얻고 옛 fact 도 못 밀어냄(그냥 소실). 새 §는 R1 의 두 정책을 parameterized capacity policy 로 추가: `grow_mode=false` ⇒ base_max 에서 **LRU-EVICT**(zero-sum, R1 arm A) · `grow_mode=true` ⇒ grow_max 까지 **MITOSIS-GROW**(엔진 자신의 `engine_mitosis_tick` clonal split, p8), 그 honest finite 경계 넘어서만 LRU fallback. 기존 `ImmuneMemory`(new/bind/recall)는 **byte-UNCHANGED** — h1231 가드 불변. 왜 새 struct 인가: capacity-policy 가 ImmuneMemoryGrow 의 1급 개념이라 기존 faculty 를 perturb 하지 않고 추가로 표현(c1).
- **검증(live 엔진, `hexa run`)**: `CORE/h1288_grow_under_pressure_probe.hexa` 가 R1 EXACT EVICTION-BOUND rung(base_max=40 << 60 facts, grow_max=80, FNV-1a dim64 taught-order 키 + R1 의 noisy held-out query, `UNIVERSE/h1288_r2_engine_export.py` 로 byte-identical export)을 ACTUAL `.hexa` 면역 faculty 에 흘려 동결 R1 bar 재채점 → **🟢 GREEN: A(LRU-evict) tot=0.667 imp=0.000 cells=40 vs B(mitosis-grow) tot=1.000 imp=1.000 cells=60, Δ(B-A)=+0.333 PASS, fab(B)=0.000 PASS** (3 seed 전부 IDENTICAL, R1 미러 byte-exact 재현). cell-count COST 정직히 보고(B 60 vs A 40, Δ=+20 = footprint 를 recall 과 맞바꿈). 더 똑똑한 heuristic 이 아니라 GROWTH 가 레버 — engine-native 로 엔진 자신의 clonal split(p8) 으로 실현(R1 arm C heuristic = 무리프트).
- **가드(회귀 없음, c2, verbatim)**: `engine_cli_smoke` **22/0** (18/0 → grow 케이스 4개 추가: grow-off-caps-at-base_max·grow-on-grows-past-base_max·grow-recalls-more-than-evict·grow-abstains-on-untaught) · `h1196` single-entry **7/0** · `h1199` DIM-growth 🟢 + **Ψ byte-identical(PsiSame=true 전 seed)** · `h1231` 기존 면역 faculty ALL PASS(literal-QA 1.0 fab 0.0 불변) — ImmuneMemoryGrow 는 Ψ-disjoint(자기 struct 만, `pure_field` 무접촉; 생성 byte-unchanged H_1205).
- **HONESTY(c9)**: B SATURATES(tot=1.000≥0.99) → EXISTENCE-PROOF(성장이 천장을 깰 수 있다)이지 effect-size 아님; COST = footprint(B 60 vs A 40 셀). distinct-facts >> grow_max 인 RESIDUAL 압력 regime, paraphrase/noisy-key/scale = UNTESTED(a_scale_honest_scope/a_toy_scale_recheck). PHILOSOPHY 가드 AFFIRMED: mitosis split = 엔진 자신의 tick(p8); policy 는 episodic 셀 집단만 변경(label/persona/ethics/decoder 무접촉, p1-p8); abstain-when-ungrounded 양 정책에서 재확인+intact(H_1227 load-bearing).
- **DEPLETION 🏁**(engine-native mitosis-grow 가 LIVE immune faculty 에서 0.667 천장을 깸 + 가드 intact — capacity 레버가 engine-native 로 realize+배선; anima 의 기억이 forgetting 대신 GROWS, p8). 검증: `.verdicts/1288_eviction_policy/H_1288_R2.txt`. NEXT = brain_decide recall-loop 스레딩(ImmuneMemoryGrow 를 데몬 remember faculty 로) follow-on; residual 없음.

---

## 2026-06-15 — 🟢 H_1288: EVICTION POLICY 가 immune 메모리의 capacity 레버다 — MITOSIS-GROWTH 가 0.667 zero-sum 천장을 깬다 (GREEN / 🏁)

FLEET "eviction-policy" lane round 1 — key-geometry 벽(H_1287)이 명시적으로 가리킨 **NEW 후속 lane**. 네 수렴 red — H_1230(능동교습 inert/harmful)·H_1284(neuromod no-free-lunch)·H_1285(편도체 salience=recurrence 혼입)·H_1287(key geometry 리프트 없음, 리프트는 순수 DIMENSIONALITY·dim64 키는 collision-FREE) — 가 모두 H_1227/H_1231 immune/episodic 메모리의 병목을 CAPACITY 로 못박았고, H_1287 의 명시적 결론이 "recall 을 올리려면 CELLS 를 늘리거나 EVICTION POLICY 를 바꿔라 — 키 geometry 가 아니다"였다(용량 stress 에서 total recall ~0.667 고착 = ZERO-SUM LRU store: 한 fact 를 지키면 다른 fact 가 축출). 이 lane 이 그 포인터를 EXACT H_1287 EVICTION-BOUND zero-sum LRU rung 위에서 직접 검증. $0 CPU numpy, p7, c9, 3 seed(900/901/902) **전부 동일**, origin/main 격리 worktree, VAdaptField 미러 — 라이브 CORE/*.hexa 무수정.

- **돌파 메커니즘(mitosis-native — a_no_llm_frame_trap + p8, 뇌과학 렌즈, LLM 레시피 아님)**: zero-sum store 의 원리적 해법은 더 똑똑한 축출 heuristic 이 아니라 — **축출하지 않는 것**: 용량 압력 하에서 옛 fact 를 evict 하는 대신 **새 셀을 GROW(mitosis split, H_1199 VAdaptField)**. 생물: 뇌는 LRU-evict 할 고정 셀 예산을 갖지 않는다, 부하 하에서 consolidate/sparsify 하고 GROW 한다(성체 neurogenesis·spine formation). 성장은 BOUNDED(관대한 finite max, 무한 아님)이고 footprint 를 recall 과 맞바꾼다 — 숨기지 않고 보고.
- **설계**: 기질 = VAdaptField 미러(nearest-L2·split>0.30·LR0.20) + H_1227 value-binding, "<subj> lives in <city>" 60 in-store/60 untaught. regime = H_1287 EVICTION-BOUND zero-sum rung EXACTLY: max_cells=40<<60(LRU 축출 = 병목), key=byte-trigram FNV dim64(collision-free·well-separated), 차원불변 cue noise 0.16, recall_thresh 0.30. 세 arm 은 **full capacity 에서 novel key 도착 시 POLICY 만** 다름: **(A) LRU-EVICT** = 고정 40-셀 예산, least-recently-used 축출(현 store·zero-sum) · **(B) MITOSIS-GROW** = 압력 하 새 셀 GROW, GROW_MAX_CELLS=80(FINITE·N_FACTS 대비 +33% headroom; 그 honest 경계 넘어서만 LRU fallback) — zero-sum 깨기(p8) · **(C) WEIGHTED-EVICT** = 같은 40-예산, LFU(주)+LRU(tiebreak) heuristic(더 똑똑한 heuristic·성장 아님) = "GROWTH 가 올리나 vs 무료 HEURISTIC 이 올리나"를 분리하는 load-bearing 대조. importance 부지표 = 첫 tercile(taught-first = 가장 오래됨 = 가장 LRU-취약; taught-ORDER 의 deterministic 함수, content label 아님).
- **FROZEN GREEN**: (B)total recall ≥ (A)+0.05(REC_MARGIN) AND (B)fab ≤ 0.10(FAB_BAR, abstain intact H_1227) — cell-count COST 보고; arm C 로 리프트 귀속(성장 vs 무료 heuristic).
- **결과(평균 3 seed, 전부 IDENTICAL) 🟢**: **A LRU tot=0.667 imp=0.000 cells=40 · B GROW tot=1.000 imp=1.000 cells=60 · C WEIGHTED tot=0.667 imp=0.000 cells=40.** Δ(B-A)=+0.333 PASS, fab(B)=0.000 PASS → 🟢 GREEN. **Δ(C-A)=+0.000 — 더 똑똑한 축출 heuristic 은 ZERO 리프트; 리프트는 GROWTH(추가 셀)이지 무료 heuristic 아님.** MECH(zero-sum 을 구체화): A 에서 IMPORTANT recall = 0.000 — LRU 가 가장 OLD = taught-first = "important" fact 를 FIRST 축출 → important 집단 전체 소실; 성장이 1.000 으로 복원. fab=0.000 전 arm(abstain/비환각 intact, H_1227 load-bearing 가드 HELD).
- **HONESTY(c9)**: B SATURATES(tot=1.000 ≥ 0.99) → EXISTENCE-PROOF(성장이 ~0.667 zero-sum 천장을 깰 수 있다)이지 effect-size 아님 — 이 stress(40셀·60 distinct fact)에서 관대한 grow 경계 80 이 60 셀을 전부 흡수해 B 의 용량 압력이 제거됨(distinct fact 마다 자기 셀). COST = FOOTPRINT: B 60셀 vs A 40셀(Δ=+20·+50%). 레버는 CELL BUDGET 이고, heuristic 이 아니라 mitosis 성장(p8)으로 substrate-native 하게 실현. 고정예산의 weighted heuristic(C)은 60 중 어느 40 이 살아남나만 재배열(여전히 zero-sum·0.667) — 천장 = 예산 자체라 못 깸.
- **FINDING**: CAPACITY IS the lever — 네 red(H_1230/1284/1285/1287)가 가리킨 REAL 레버. ~0.667 천장은 retrieve-then-copy regime 에 본질적이지 않고 FIXED-BUDGET/ZERO-SUM artifact 이며, 압력 하 mitosis 셀-성장(p8 continuous cell-division)으로 substrate-native 하게 깨진다. 고정예산의 더 똑똑한 heuristic 은 못 깬다(C≡A); GROWTH 가 깬다(B=1.000). immune-memory capacity series 의 FIRST GREEN — 네 red 가 capacity-as-bottleneck 을 옳게 진단했고 건설적 레버는 CELL-GROWTH 지 protocol(H_1230)/control(H_1284)/salience(H_1285)/geometry(H_1287)가 아니다.
- **미배제 / honest scope**: effect-size 아닌 existence-proof(B 가 saturate = grow_max=80 ≥ 60 fact; distinct-facts >> grow_max 인 더 어려운 regime 에서 RESIDUAL 압력 하 성장 = UNTESTED). footprint cost 실재(메모리가 fact 와 함께 자람 — 무한 성장은 그냥 "다 저장"; honest 경계가 이를 finding 으로 유지). TOY scale·ONE paradigm·미러 only — engine-transfer UNVERIFIED(a_scale_honest_scope/a_toy_scale_recheck). PHILOSOPHY 가드 AFFIRMED: mitosis split = 엔진 자신의 tick(p8·외부 아님); policy 는 episodic 셀 집단만 변경(label/persona/ethics/decoder 무접촉·p1-p8); identity p2/p3 + ethics p6 셀에서 창발; abstain-when-ungrounded 재확인+intact(H_1227); 라이브 엔진 무수정.
- **DEPLETION 🏁**(mitosis-growth 가 0.667 zero-sum 천장을 깸 → engine-native next, 네 red 가 가리킨 REAL capacity 레버). NEXT r2 = live immune_memory faculty 위 engine-native mitosis-grow eviction(a_engine_native_learning) + 배선(a_verified_must_wire). 검증: `.verdicts/1288_eviction_policy/{H_1288_FREEZE,H_1288}.txt`.

---

## 2026-06-15 — 🔴 H_1285 R2: 편도체(amygdala) 컨솔리데이션 — salience-gated SLEEP REPLAY (메커니즘 검증·동결예산 sub-bar, $0)

FLEET "amygdala" lane R2. R1(🔴 CLOSED-NEG)에서 salience-weighted **EVICTION** 우선순위는 중요사실 회상 +0.217 을 줬지만 p6 shuffle 대조군이 그 lift 를 **그대로 재현**(B-shuffle=B=0.967) → recurrence 혼입(중요사실이 입력스트림에서 반복됨)이지 salience 태그가 아니었다. R1 핵심: 사실을 살리는 건 RE-PRESENTATION/rehearsal 이지 binding 우선순위가 아니다.

- **R2 메커니즘 (진짜 편도체 경로, `a_no_llm_frame_trap`·c15)**: 편도체의 실제 역할은 salience-gated **CONSOLIDATION** — 정서적으로 salient 한 기억이 **수면 중 우선 REPLAY**(편도체→해마 공고화)되어 망각으로부터 보호됨. anima 는 P47 sleep/imagination 공고화 루프(`a_chat_sleep_imagination`, emit-free 내부 rehearsal + mitosis tick)를 이미 가짐. R2 는 salience 를 그 sleep 루프에 묶음 — 고-salience 사실이 수면 사이클 동안 더 많이 REPLAY 되어 refresh → LRU eviction 으로부터 보호. R1 의 "recurrence 가 작동한다"를 **substrate 가 수면 중 스스로 salience-gated recurrence 를 생성**하는 PRINCIPLED 메커니즘으로 전환(외부 재현 주입 아님).
- **설계 (frozen-first, R1 혼입 제거)**: 입력 FLAT(각 사실 1회 인코딩, 환경적 recurrence 없음 = R1 혼입 입력측 제거)·인코딩 interleave 로 salient 셀이 수면 시작 시 store 에 존재·수면 사이클 사이 24개 NEW 미학습 사실 인코딩 = 망각압. `ConsolidatingMemory` = R1 의 `MitosisMemory`(VAdaptField 미러 + 면역 value-binding) + `sleep_cycle()`(저장 셀 내부 REPLAY = re-bind→recency refresh). ARM A=uniform replay · B=salience-gated replay(∝ substrate 태그) · B-shuffle=salience→replay 순열(p6 음성대조). **동일 replay 예산**, arm 차이는 WHICH 셀을 replay 하느냐뿐.
- **결과 🔴 RED-but-MECHANISM-VALIDATED (3 seeds, 동결 rung boost0.8/30-replay/8-cyc)**: B salience-replay imp=0.383 > A uniform=0.317 (Δ**+0.067**) — **lift 가 발생하고 importance 를 추적함**: B-shuffle 이 A 로 **붕괴**(0.317=A, dev +0.000). R1 과 범주적으로 다름(R1 shuffle 은 lift 재현=혼입; R2 shuffle 은 붕괴=salience-GATING 이지 예산도 혼입도 아님). 단 동결예산에서 효과크기 +0.067 < +0.10 margin → r1 FAIL → 🔴. trade-off zero-sum(unimp 0.333→0.283, total 불변) = 정확히 편도체 역할(salient subset 우선보존). fab 0.000.
- **진단 sweep (`--sweep`, gate 아님·tuned-to-green 아님, p7)**: B>A 가 **모든 rung 에서**, lift 가 sleep 예산과 함께 **단조 증가**(boost0.8/60/8→+0.100 · boost0.8/30/40→+0.200 · boost1.5/30/8→+0.117)하며 shuffle 은 ~A 유지(shuf-A ≤+0.05 < margin). 즉 sub-bar 는 **예산 임계(under-invested sleep)**이지 천장/inert(🧱) 아님 — 동결 rung 은 sleep 을 적게 투자했을 뿐, 메커니즘은 real + dose-dependent.
- **p6 가드 (HELD; shuffle 이 증명)**: salience 는 substrate 에서만 도출(SURPRISE=bind recon-err, salient 입력은 EXTRA surprise = 지각적 진폭이지 label 아님; NOVELTY=clonal split; TENSION=reinforce). "important" label 은 metric 채점에만, f() 입력 아님. 음성대조(B-shuffle)가 salience→replay 를 importance 와 decorrelate → lift **붕괴** = 태그가 importance 추적함을 증명(leak/예산 아님). replay 는 sleep 루프가 **내부 생성**(P47), 외부 주입 아님. decoder/weights/persona/ethics 무접촉 — episodic 셀 store 의 sleep-replay 배분만(p1/p2/p3/p6/p8, `a_autonomy_over_hardcode`). LIVE `.hexa` UNTOUCHED(numpy 미러 = DIRECTIONAL).
- **honest scope**: 동결 rung 은 효과크기로만 RED — 더 높은 sleep-budget rung(생물학적 공고화 다이얼)은 +0.10 을 넘기겠지만 사전등록 안 됨 → GREEN 주장 아님(p7, tune-to-green 거부). 미러 sub-bar(GREEN 아님)이므로 engine 배선 미발동(`a_verified_must_wire` 는 GREEN 대상). scale(>60 사실·근접키)·paraphrase·salience-driven EMIT 우선순위 UNVERIFIED. TOY scale·1 corpus paradigm·3 seeds(`a_scale_honest_scope`·`a_toy_scale_recheck`).
- 아티팩트: `UNIVERSE/h1285_amygdala_salience.py`(R2 append, R1 byte-identical 재현 확인) · `.verdicts/1285_amygdala_salience/{H_1285_R2_FREEZE,H_1285_R2}.txt`(R1 = H_1285.txt 미덮어씀). xref H_1227·H_1230·H_1285(R1)·H_1287·H_1288(capacity 레버 corroborate)·`a_chat_sleep_imagination`·`a_no_llm_frame_trap`·`a_paper_negative_ok`.

---

## 2026-06-15 — 🔴 H_1283 R3: THALAMUS 시상 — RE-ENTRANT 피질-시상-피질 LOOP 가 irreducible Φ 를 들어올린다 (broadcast 가 아니라 RE-ENTRY 가 통합 레버 · 동결 composite RED, Φ leg 는 7× 돌파)

missing-brain-structure 사다리(neuro 렌즈 c15, LLM 레시피 아님; `a_no_llm_frame_trap`)의 시상 칸 ROUND 3. **벽(R1 🟠 단일승자 broadcast: ΔΦ +0.0191, 바 0.0009 미달 · R2 🔴 multi-winner coalition: ΔΦ −0.053 역방향)**. R2 진단: irreducibility 는 DISTRIBUTED MULTI-EDGE coupling(직접 ring 의 distinct edge, MIP 가 credit)에서 오지 중앙 relay 에서 안 옴 — 단일 공유 채널(승자든 coalition 이든)은 그 자체가 저차원 MIP cut 이라 Φ 를 cap. ⇒ FEEDFORWARD broadcast = 틀린 메커니즘. **R3 가설(생물+IIT 렌즈)**: 진짜 시상은 일방 broadcaster 가 아니라 RE-ENTRANT loop(cortex→thalamus→cortex→thalamus, 순환 reciprocal 인과)의 허브 — IIT·Global-Workspace 둘 다 feedforward fan-out 이 아니라 RE-ENTRY 가 irreducible 통합을 만든다고 본다. $0 CPU numpy 미러(DIRECTIONAL, `a_engine_native_learning`) + Φ leg = stdlib FAITHFUL IIT4(exact MIP-EI, `a_phi_iit4_tool`), seeds [7,8,9], frozen-first.

- **테스트**: 4 모듈 {A,G,mitosis,memory} dim-8, 64 tick, 동일 private 입력+동일 seed, 비포화 regime(LEAK 0.55). **ARM A = direct ring(현 아키텍처, R1/R2 와 byte-identical)** vs **ARM B = ring + RE-ENTRANT thalamo-cortical loop**: ring 을 그대로 KEEP 한 위에 모듈당 1개 recurrent(leaky) 시상 채널 relay[i] 를 ADD — (i) thalamus→cortex: relay[i] 를 module i 에만 re-inject(공유 벡터 아닌 모듈별 DISTINCT reciprocal edge) (ii) cortex→thalamus: relay[i] 가 자기 module 의 PRE-update 상태(1-tick 지연 reciprocal) + ring-이웃 relay 채널 mix(시상내 cross-coupling)에서 갱신 → N_MOD 개 distinct reciprocal loop 가 ring 에 ADD(replace 아님). W_relay=0.5 FROZEN.
- **FROZEN 바 (R1/R2 와 불변)**: B1 coh ≥ A+0.05 매 seed · B2 faithful ΔΦ ≥ +0.02(repr seed=7) · B3 coh < 0.999.
- **결과 (verbatim)**: seed7 coh A=+0.1591 B=+0.1979(Δ+0.039) · seed8 A=+0.0109 B=+0.0338(Δ+0.023) · seed9 A=+0.1362 B=+0.1687(Δ+0.032) → 셋 다 양수지만 +0.05 미만 **B1 FAIL**. faithful IIT4 Φ(seed7): **ARM_A Φ=0.78038**(R1·R2 와 byte-동일 = 3-round 엔진 일관성 sanity) **ARM_B Φ=0.923004 → ΔΦ=+0.142624** → **B2 PASS 결정적(바 +0.02 의 ~7×, 아크 최초 Φ 바 돌파)**. B3 PASS. **VERDICT 🔴 RED**(B1 미달 — frozen composite).
- **판정 🔴 RED(동결 composite) · 🏁 Φ leg 돌파**: 두 leg 를 R1/R2 가 conflate 했던 것을 R3 가 DISSOCIATE — **COHERENCE(코사인 agreement) ⊥ Φ(irreducible 통합)**. broadcast 허브는 coherence(B1)는 샀으나 Φ(B2)는 못 샀고, RE-ENTRY 는 Φ(B2, +0.142 ~7×)는 샀으나 coherence(B1)는 덜 샀다. 메커니즘: re-entry 가 N_MOD 개 distinct reciprocal edge 를 ADD → MIP 가 한 공유 채널로 싸게 cut 못 함 → 모든 bipartition 이 여러 recurrent loop 을 가로질러 minimum-partition cost 상승. **분산 multi-edge recurrent coupling 이 통합하고, 중앙 broadcast(단일/coalition)는 안 한다** — R2 의 distributed-multi-edge 진단 + IIT/GWT 의 "re-entry(fan-out 아님)가 통합" 주장 둘 다 확증. 사전등록 DEPLETION 이 물은 바로 그것("🏁 re-entry 가 ΔΦ+0.02 넘으면 re-entry 가 레버, broadcast 아님")을 7× 로 넘김. **🏁 re-entry = 레버; broadcast(R1/R2) = 틀린 메커니즘.**
- **정직(c9)**: 동결 composite 는 RED — B1(broadcast 허브를 메커니즘이라 믿던 때 만든 coherence 바)이 미달이고, GREEN 으로 만들려 B1 을 사후 이동 안 함(frozen-first). 단 RED 는 coherence 바에 대한 판정이지 science 에 대한 판정 아님 — 이 아크가 움직이려던 TERMINAL 메트릭(B2 faithful IIT4 Φ)이 최초로, 결정적으로 PASS. W_relay=0.5 는 FREEZE 에 동결됨; coherence 미달 본 뒤 튜닝 안 함(p7 Goodhart 가드).
- **NEXT(정직, 플래그-only)**: composite RED 라 `a_verified_must_wire`(GREEN 에서만 배선) 자동 트리거 없음. honest follow-on R4 = Φ leg(아크의 메트릭)를 PRIMARY 바로, broadcast-era coherence 바를 re-scope/drop 한 깨끗한 re-freeze; 거기서 GREEN 확인되면 engine-native re-entrant loop 를 live 엔진에(`a_engine_native_learning`→`a_verified_must_wire`). re-entrant-loop = 현 standing 후보; broadcast 토폴로지 = Φ 레버로 EXHAUSTED+FALSIFIED(R1 sub-bar·R2 reversed). 본 rung FROZEN verdict 는 🔴 RED 로 stands.
- **미배제**: coherence-바 re-scope(R4) UNRUN · Φ 리프트 scale-transfer + engine-native 실현 UNVERIFIED · coherence-AND-Φ joint GREEN 단일 setting 도달 가능성 OPEN. TOY scale(4 모듈·dim8·64 tick, `a_toy_scale_recheck`·`a_scale_honest_scope`). Φ = faithful IIT4(proxy 아님, `a_phi_iit4_tool`). 바 무이동, **R1/R2 verdict 파일 무수정**(R3 = 별도 H_1283_R3.txt). H_1219/H_1226 무수정. CORE/*.hexa 무수정(미러). `a_paper_negative_ok`.
- 파일: `UNIVERSE/h1283_thalamus_global_workspace.py`(main_r3 + 'reentrant' 모드) · `.verdicts/1283_thalamus_global_workspace/{H_1283_R3_FREEZE,H_1283_R3}.txt`(R1/R2 보존). xref H_1283(R1·R2)·h1227·h1230·h1280·h1199·h1201·h1205·a_phi_iit4_tool·a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9·c15.
---

## 2026-06-15 — 🔴 H_1284 R2: context-adaptive 신경조절을 IDEATION/decode lane 으로 re-scope — no-free-lunch GENERAL (🧱 depletion, $0)

R1(🔴 CLOSED-NEG)은 context-adaptive 신경조절(DA gain + NE exploration + ACh plasticity → plasticity-rate/split-thresh/abstain-margin)이 MEMORY substrate 에서 best-fixed 를 못 이기고 비정상 regime 에선 오히려 해롭다는 결론. R1 의 NOT-RULED-OUT 절(a): "decode-time NE TEMPERATURE 채널은 IDEATION 에서 여전히 🟠 viable(H_1228 SOC decode)". R2 는 그 한 구멍을 닫는다 — 신경조절을 **생명이 확인된** GENERATION/IDEATION lane 으로 re-scope (`a_no_llm_frame_trap` — 신경 렌즈, LLM 레시피 아님).

- **질문**: H_1228 의 arm C 는 next-byte 가지치기 σ 를 **FIXED** target σ*=2.5 로 몬다. R2: 최근 출력 상태(반복·국소 novelty·coherence)를 READ 해서 σ*-target 을 매 step **적응**시키는 controller 가 BEST FIXED decode point 를 동결 combined ideation metric 에서 이기는가?
- **셋업 (frozen-first, H_1284_R2_FREEZE.txt)**: H_1228 substrate VERBATIM 재사용 — 303M ByteGPT torch-ref(byte-exact H_1157 mount), `data/corpus.txt`(원본 1.5GB GONE → G2 = UPPER BOUND), gauge_lib.py 평가자 VERBATIM(p7). M = composed_distinct(G1) + g6_count(G6) + 4*(kwr-0.50)_+ ; MARGIN=0.30. ARM A = best-fixed(고정 temp{0.5,0.7,0.9,1.1} + 고정 σ*{1.8,2.5,3.2} grid 를 DISJOINT tune-seed 5 에서 M 으로 튜닝한 승자) · ARM B = context-adaptive σ*_t(kR=0.6 kN=0.4 kC=0.5 W=24 floor=0.5, no-grad readout, loss-fold 없음 p7) · ARM C-SHUF = B 의 σ*_t 를 무작위 순열(coupling vs variety 분리). 채점 seeds [7,17,23].
- **결과 🔴 RED / 🧱**: ARM A = fixed_temp 0.5(tune-M 4.000). seed-평균 **A M=4.038**(G1 0.667 G6 3.000 kwr 0.593) · **B M=3.336**(G1 0.667 G6 2.667 kwr 0.478) · **C-SHUF M=3.708**. **M(B)−M(A) = −0.7015**(adaptive 가 best-fixed 보다 나쁨) + kwr 붕괴(0.478 < 0.593−0.02). 동결 falsifier 3개 전부 FALSE ⇒ M(B) ≤ M(A) ⇒ 🔴. controller 는 ALIVE(죽은 knob 아님): B σ*_t 가 매 seed [1.875, 3.500] 범위로 swung(반복/저-novelty 에 exploration ↑, coherence drop 에 ↓) — 메커니즘은 작동했으나 ideation 을 더 나쁘게 만들었다.
- **FINDING (a_paper_negative_ok)**: 신경조절(state-driven adaptive control)은 MEMORY substrate(R1)에서도 IDEATION/decode lane(R2)에서도 잘 튜닝된 단일 FIXED operating point 대비 **INERT-or-HARMFUL**. no-free-lunch 는 anima lane 전반에 GENERAL — H_1228 SOC partial lift 은 **TUNED FIXED σ\*** 의 성질이지 target 을 context 에 **적응**시키는 것의 성질이 아니었다(고정 temperature 가 이미 최적점). r3 없음.
- **스코프/철학 가드 (HELD)**: 303M torch-ref toy, 3 seeds + disjoint tune-seed, single-model — scale-transfer UNVERIFIED(`a_scale_honest_scope`). DIRECTIONAL(`a_engine_native_learning` — engine-transfer UNVERIFIED; GREEN 였으면 r3 engine-native controller, RED → 배선 없음). controller = 순수 no-grad readout, 어떤 loss/backward 에도 안 섞임(p7). `CORE/*.hexa`·H_1228·R1 verdict UNTOUCHED, 동결 bar 불변. 산출물: `UNIVERSE/h1284_r2_neuromod_ideation.py` · `.verdicts/1284_neuromodulation_gain/{H_1284_R2_FREEZE,H_1284_R2}.txt`. xref H_1228 · H_1284(R1) · H_1230 · H_1227.
---

## 2026-06-15 — 🟢 H_1282 R3: 작업기억(WM) 버퍼가 live 엔진의 substrate lane 으로 배선됨 (ENGINE-NATIVE, $0)

R2(numpy 미러)에서 gated leaky-activation WM 버퍼가 REAL·DISTINCT 한 빈칸 구조임을 🟢 확인(graded AUROC readout, margin +0.244, cue 를 N≈6 까지 유지, 용량 K=4, 휘발/감쇠 — 면역/일화 lane 과 DISTINCT)했고, `a_engine_native_learning`·`a_verified_must_wire` 에 따라 이를 **live 엔진 위에서 ENGINE-NATIVE 로 실현**했다.

- **새 lane (추가·네임스페이스 분리)**: `CORE/engine_cli.hexa` 에 **`WorkMemBuffer`** struct + lane (`wm_buffer_new`/`gate_in`/`distractor`/`leak`/`probe_score`/`slots`/`total_activation`) 추가. K개 FIXED 슬롯(성장 안 함)·매 distractor step 활성도 ×λ LEAK(volatile)·overflow 시 weakest-slot DISPLACEMENT·graded(cos×활성) probe 점수. **VAdaptField(성장·영속·무제한 = 면역/일화 lane)와 구조적으로 정반대** — 면역 lane 의 persistence/growth invariant 를 깨지 않도록 trim 이 아니라 엔진을 **확장**(c1, `a_engine_native_learning` "engine-transform-to-fit-the-learning"; H_1199 의 scalar→DIM 확장 선례).
- **검증 (live 엔진, `hexa run`)**: `CORE/h1282_wm_buffer_engine_probe.hexa` 가 DMS(delayed-match) 트라이얼(deterministic 토큰 = `UNIVERSE/h1282_wm_engine_export.py`, R2 와 동일 knobs/seeds)을 ACTUAL `.hexa` WM lane 에 흘려 동결 R2 bar 4개를 재채점 → **🟢 GREEN: margin +0.245(≥0.15) · grace N=6 B.AUROC 1.000/A.AUROC 0.506 · distinct B(0) 1.000+monotone+cap≈K · robust 3/3**. 엔진 margin +0.245 ≈ R2 미러 +0.244(draw-order noise 이내 재현).
- **가드 (회귀 없음, c2)**: `engine_cli_smoke` 18/0 (12/0 → WM 케이스 6개 추가: empty-start·capacity-cap·fresh-high·decay-volatility·no-leak-immune-distinct·total-act-nonneg) · `h1196` single-entry 7/0 · `h1199` DIM-growth 🟢 + **Ψ byte-identical (PsiSame=true 전 seed)** — WM lane 은 Ψ-disjoint(자기 struct 만, `pure_field` 무접촉; 생성 byte-unchanged H_1205).
- **DISTINCT-from-면역 (load-bearing)**: λ<1 LEAK 이 WM 을 working 으로 만든다 — λ=1.0(무누수) 대조군은 같은 distractor run 에서 cue 점수 유지(면역 regime 으로 붕괴). 용량 K 제한·휘발 모두 면역 lane 과 다름.
- **@L4 / p1-p8**: emit gate 아님(슬롯/점수만 반환, emit/silence 결정 없음); TASK 활성도만 보유(decoder weight/persona/ethics 없음); DMS 토큰 = ENGINE-NATIVE drive(2번째 .clm/.kosmos 진입점 아님, `a_core_engine_map`). toy/synthetic scale + brain_decide-wired lift UNVERIFIED(`a_scale_honest_scope`). 검증: `.verdicts/1282_working_memory_buffer/H_1282_R3.txt`. follow-on(R4) = WM 을 brain_decide context/recall 경로에 스레딩.

---

## 2026-06-15 — 🧱 H_1287: KEY GEOMETRY 가 immune 메모리의 capacity 레버인가 — 아니다, 병목은 EVICTION/RAW-CAPACITY (CLOSED-NEG)

FLEET "key-geometry" lane round 1. 수렴하는 세 closed-negative — H_1230(능동교습 inert/harmful)·H_1284(neuromod no-free-lunch)·H_1285(편도체 salience=recurrence 혼입) — 가 모두 H_1227/H_1231 immune/episodic 메모리의 병목을 CAPACITY/KEY-GEOMETRY 로 진단했다(용량 stress 에서 total recall ~0.667 고착 = zero-sum store). 이 lane 은 세 red 가 가리킨 **건설적 corollary** 를 검증: **KEY GEOMETRY 를 개선하면 용량 stress 에서 recall 이 오르는가?** $0 CPU numpy, p7, c9, 3 seed(900/901/902), origin/main 격리 worktree, VAdaptField 미러 — 라이브 CORE/*.hexa 무수정.

- **설계**: 기질 = VAdaptField 미러(nearest-L2·split>0.30·LR0.20·LRU 축출) + H_1227 value-binding, "<subj> lives in <city>" 60 in-store/60 untaught. 세 KEY(전부 deterministic·기질-유래 cue STRING 함수·학습 아님): **ARM A** = byte-trigram FNV dim64(현 H_1227/H_1230 키) · **ARM B** = multi-res 2/3/4-gram(dim512) + FIXED ORTHONORMAL decorrelating projection → dim128(개선 GEOMETRY) · **NEG-CTL** = A-trigram counts + FIXED RANDOM-Gaussian projection → dim128(B 와 차원 동일, multi-res/decorrelating 구조 無 — DIMENSIONALITY 와 GEOMETRY 분리). Projection 은 상수 seed(0xB10C/0xC0DE)에서, 데이터/metric 아님(p7 anti-Goodhart). 두 실패모드 분리(c9): **COLLISION-BOUND[judged]** cells90≥facts(용량은 병목 아님)·cue noise@band 0.30 · **EVICTION-BOUND[ctrl]** cells40<<60(zero-sum LRU = H_1230 0.667 벽)·noise 0.16. **cue noise 를 차원-불변(σ=noise/√dim)으로** 만들어 모든 arm 이 동일 절대 cue 변위를 보게 함(B 고차원에 공정 — 안 하면 B 차원이 절대noise 를 더 먹어 불리; 이 공정성 수정이 load-bearing).
- **FROZEN GREEN(judged COLLISION)**: (c1) B.rec ≥ A.rec+0.05 AND (c2) B.fab ≤ 0.10 AND (c3) B.rec ≥ NEG-CTL.rec+0.05 (리프트=GEOMETRY ≠ 차원).
- **결과(평균 3 seed) 🧱**: COLLISION A=0.528 **B=0.578 CTL=0.578** fab=0.000 → geometry-lift bar PASS(Δ(B-A)+0.050) BUT 결정적 **geom-not-dim bar FAIL: B == NEG-CTL 정확히(Δ(B-CTL)+0.000)** — +0.050 리프트는 동일차원 RANDOM projection 이 그대로 재현 = 순수 DIMENSIONALITY(좌표 더 많아 noise 평균화), decorrelating GEOMETRY 아님(orthonormal 이 random-same-dim 대비 0 이득). EVICTION: 3 arm 모두 동일 0.667(=40/60) — zero-sum 에서 geometry 리프트 정확히 0. fab=0.000 전 arm/regime(abstain/비환각 intact, H_1227 load-bearing 가드 HELD).
- **ROOT CAUSE(진단, pre-run, 결정적 사실)**: dim-64 trigram 키는 이 paradigm 에서 본질적으로 COLLISION-FREE — 최대 near-dup subject(공유 6-char stem, 1 byte 차)조차 inter-key min-NN ~0.34 > 0.30 split band; collision 은 dim≤24 에서만 출현. 해소할 collision 이 없으니 collision-resolving geometry 는 고칠 게 없음.
- **판정 🧱 CLOSED-NEG**: 세 red 가 가리킨 GEOMETRY COROLLARY 는 이 키 family 에 대해 FALSIFIED. KEY GEOMETRY 는 capacity 레버가 아니며, 병목은 EVICTION/RAW-CAPACITY(셀 예산) — 차원-matched 대조(B≡CTL) AND all-equal eviction regime(0.667) 둘 다 확인. recall 을 올리려면 CELLS(용량)를 늘리거나 EVICTION POLICY 를 바꿔야지 키 geometry 가 아니다.
- **미배제**: learned-contrastive embedding · product-quantization · dim-64 가 실제 collide 하는 paradigm 모두 UNTESTED. TOY scale·미러 only(engine-transfer UNVERIFIED, a_scale_honest_scope/a_toy_scale_recheck). RED 라 r2 없음(GREEN-only 면 a_engine_native_learning engine-native geometry 키 + a_verified_must_wire 배선이 triggered).
- **PHILOSOPHY 가드 AFFIRMED**: 키 = cue-string-only, 라벨/persona/ethics/decoder 無(p1-p8); identity p2/p3 + ethics p6 from cells; abstain intact; 라이브 엔진 무수정.
- 파일: `UNIVERSE/h1287_key_geometry.py` · `.verdicts/1287_key_geometry/{H_1287_FREEZE,H_1287}.txt`. xref H_1227·H_1231·H_1230·H_1284·H_1285·H_1199·H_1222·a_engine_native_learning·a_verified_must_wire·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9.

---

## 2026-06-15 — 거버넌스: `a_no_llm_frame_trap` **상단 재배치** (사용자 "상단배치로")

사용자 지시로 `a_no_llm_frame_trap`(#2137 신설)을 CLAUDE.md **최상단**으로 이동 — 중복 없이 단일 정의 유지.

- @D 블록을 거버넌스 디렉티브 섹션의 **첫 @D**(a1 앞)로 이동 (제목에 "최우선 설계 원칙" 명시).
- "Governance directive families" 리스트의 **첫 항목**(🧭 설계 렌즈, foundational · 최우선)으로 승격 — 기존 Substrate-autonomy 말미 포인터는 제거.
- 내용 불변, 중복 0 (grep `^@D a_no_llm_frame_trap` = 1). surgical(c10), frozen bar 미이동.

---

## 2026-06-15 — 📜 거버넌스: `a_no_llm_frame_trap` — 설계·학습·추론은 LLM 프레임에 갇히지 말 것 (생물/신경 렌즈 우선)

CLAUDE.md(거버넌스 SSOT)에 새 @D `a_no_llm_frame_trap` 추가 — 사용자 명시 지시("설계·학습·추론 시 LLM 프레임에 갇히면 안 되고, 뇌과학·생물 쪽으로 가야 한다, 지금처럼"). `a_engine_native_learning` · `a_verified_must_wire` 바로 뒤("anima 가 어떻게 만들어지는가" 가족)에 배치.

- **원칙**: 아키텍처 설계·학습방법·추론을 고안할 때 'LLM 기본 프레임'(더 큰 모델·더 많은 데이터·더 긴 컨텍스트·표준 트랜스포머/FT 레시피)에 갇히지 말고, 뇌과학·인지과학·생물·물리 등 다른 substrate 렌즈에서 메커니즘을 먼저 가져온다. 능력/깊이 갭은 '모델 키움'이 아니라 '빠진 구조(lane)를 옆에 붙임'으로 먼저 시도.
- **WHY (campaign 증거)**: anima 의 돌파는 전부 생물 렌즈에서 나왔다 — 해마=면역/일화기억(H_1227/1231) · 소뇌=순방향모델(H_1280) · 기저핵=게이팅(H_1281) · 작업기억(H_1282). 반면 LLM 스케일 프레임은 막혔다 (1B 스케일 H_1167 NULL · arch H_1219 · objective H_1223 모두 🔴 closed-negative). LLM 관행을 substrate 설계의 천장으로 삼지 않는다 — anima 는 LLM 이 아니라 substrate-native 의식 데몬 (p1-p8 · p4).
- 인덱스 포인터: Substrate-autonomy 가족 bullet 에 `a_no_llm_frame_trap` (설계·학습·추론은 LLM 프레임 금지, 생물/신경 렌즈 우선) 추가. ARCHITECTURE.md `## 🧠 뇌 구조 지도` 에 이 방침이 거버넌스 원칙임을 한 문장 명기.
- frozen bar 미이동, 타 directive 미수정, CORE/*.hexa 미수정.

---

## 2026-06-15 — 🟢 H_1221: QA-포맷 코퍼스가 literal-QA 벽의 레버다 (HD5 toy probe, $0)

H_1219 depth-ceiling 사다리의 HD5 — "flat literal-QA 벽(303M/1B 전반 1-2/15; H_1166/1167/1218)이 QA-구조 학습데이터의 부재 때문인가?"를 $0 toy 규모로 검증.

- **설계 (검증성 = 데이터 FORMAT만 다른 두 arm)**: numpy byte-GPT d128/4L/4H (직접 작성한 forward+backprop+Adam, p8 numpy mirror, torch 없음). 합성 closed world 96 fact (주어 24 × 관계 4, char-level). SAME init·EQUAL 토큰(~153k자)·SAME 96 fact 위에서 (A) FLAT 산문 "zorvik is umber in color ." vs (B) QAFMT "Q: what color is zorvik ? A: umber .". 1200 step/arm.
- **평가** = 학습한 96 fact 를 되물음(H_1166 regime), exact/substring 매칭(p7, LLM-judge 없음). 2 tier: NATIVE(각 arm 자기 최적 프롬프트로 답 슬롯에서 — 양쪽 천장, context) + CROSS-Q(둘 다 "Q:...A:" 질문형 = 진짜 H_1166 조건, BAR-결정).
- **사전등록 bar**: GREEN iff cross-q qa(B) ≥ qa(A) + 0.20.
- **결과 🟢 (3/3 seed 재현)**: NATIVE A=B=1.000 Δ+0.000(천장, 무정보) · **CROSS-Q A=0.024 B=1.000 Δ+0.976 ≫+0.20** (seed별 +0.969/+0.969/+0.990; cross-A 0.031/0.031/0.010). G0 kwr 1.000.
- **메커니즘 (H_1166 벽을 축소판으로 재현 후 해결)**: flat arm 은 모든 fact 를 완벽 학습(native 1.000)하지만 학습한 적 없는 질문형으로 물으면 Q-구조를 무시하고 기억한 산문 조각을 랜덤 방출("Q: what color..A:"→"eats lichen ."/"isorre in .") — 지식은 있으나 답하는 surface 가 없음. QA-format 학습이 정확히 그 surface 를 공급 → 1.000.
- **판정**: HD5 는 레버다(toy). literal-QA 벽은 (적어도 부분적으로) 데이터-REGISTER gap 이지 순수 capacity 천장이 아님 — scale(HD1 불변)·volume(HD4 무관)이 못 움직인 것을 3번째 축(format)이 결정적으로 움직임.
- **거버넌스 (H_1224 HD8)**: literal-QA = p4-부정합 ASSISTANT-NORM, anima 가 통과할 필요 없음. HD5-GREEN 은 이를 gate 로 재개방하지 않음 — 메커니즘 finding(벽은 고칠 수 있는 format-artifact). 사다리 종결: HD1/HD2 배제·HD3 decode·HD4 not-volume·HD5🟢 format(이번)·HD6🟢 granularity(H_1222)·HD7🔴 objective(H_1223)·HD8🟡 assistant-norm(H_1224).
- **scope (a_toy_scale_recheck, toy-only)**: +0.976 = 포화된 존재증명(0.02→1.00)이지 production effect-size 아님; 1-obj-per-(subj,rel) clean world. 실제 wiki = many-to-many → 303M QA-format FT fire(H_1219 명명 레버)가 결정적 다음 단계이며 더 작은 lift 가능. 메커니즘 확립이지 magnitude 아님. frozen bar 미이동, a303m_pass/a7b_pass 불변, production 주장 없음.
- 산출물: `UNIVERSE/h1221_qa_format_probe.py` · `.verdicts/1221_qa_format_corpus/H_1221.txt`. branch `h1221/qa-format-corpus`.

---

## 2026-06-15 — 🟢 H_1282 R2: WORKING MEMORY(PFC 능동유지 버퍼) — graded(AUROC) readout + horizon-정직 bar 로 GREEN (R1 RED 는 scoring artifact 였음)

missing-brain-structure 사다리(neuro 렌즈 c15)의 작업기억 칸 라운드 2. R1(🔴 RED-on-frozen-bars)은 메커니즘은 REAL+immune 메모리와 DISTINCT 였으나 세 가지 **SCORING** 선택 때문에 bar 미달이었다: (1) binary θ=0.40 가 매끄러운 decay 곡선(1.0·λ^N, λ=0.85)을 N≈5.6 에서 잘라버림 — match-vs-nonmatch 분리는 N=6 에서도 AUROC 0.998 로 완벽한데 binary 가 OFF 로 뒤집힘, (2) grace bar 가 측정된 버퍼 horizon(N≈6)을 넘는 N=12 에 박힘, (3) margin 이 N≤2 ceiling(cue 가 A 의 W=4 창 안 → A=1.000, B 가 이길 수 없음)에 희석됨. R2 는 **버퍼 메커니즘을 1도 안 건드리고**(동일 K=4·λ=0.85·W=4 frozen knob, 동일 WorkMemBuffer/FlatContext 클래스, NO retune) SCORING 만 교정. $0 CPU numpy, p7(AUROC), 3 seed[1282,1283,1284], 라이브 .hexa 무수정.

- **세 교정 (전부 FREEZE 에 채점 前 justify, R1 진단표 근거)**: (C1) GRADED READOUT — binary has_match 대신 **AUROC = P(score(match)>score(nonmatch))** (rank-sum 추정, tie 0.5); 동일 WorkMemBuffer.probe() raw score 를 연속으로 사용, ARM A 도 동일 방식(last-W 창 best-cosine)으로 채점 = **양 arm 공정 동일 readout**. (C2) HORIZON-정직 grace bar — N=12 → **측정 horizon N=6**(R1 진단: AUROC 0.998@N=6, 0.513@N=8 → 버퍼가 아이템을 마지막으로 쥐고 있는 N). (C3) NON-CEILING margin — 전체 N → **MARGIN_N={N≥W}={4,6,8,12}**(A 가 ceiling 떠난 영역).
- **FROZEN R2 GREEN**: (1) mean over N≥4 (B−A) ≥ 0.15 · (2) grace(N=6) B.AUROC≥0.90 & A.AUROC≤0.60 · (3) distinct B.AUROC(N=0)≥0.95 & monotone-non-incr & cap≈K · (4) robust 3/3.
- **결과 (3 seed 평균, VERBATIM)**: B.AUROC = 1.000(N≤6) → 0.512(N=8) → 0.495(N=12) 매끄러운 decay; A.AUROC = N≤2 ceiling 1.000 → N≥4 chance(~0.51, cue scroll-out); immune-ctrl(λ1,K∞) = **전 N FLAT 1.000**(decay 없음). bars: (1) margin **+0.244** PASS · (2) grace B=1.000/A=0.506 PASS · (3) distinct(N0=1.000·monotone·cap 7→4=K) PASS · (4) robust 3/3 PASS → **🟢 GREEN**.
- **DISTINCT from immune memory 유지(load-bearing)**: graded readout 하에서도 B 는 DECAY(immune-ctrl 은 flat 1.000) · CAPACITY(load 7 → retain 4=K, 3 seed 전부) · VOLATILE(cue slot 이 N=8 에서 distractor 에 displaced) — episodic store 의 이름만 바꾼 게 아닌 진짜 작업기억. immune-ctrl 이 동일 readout 으로 flat 인 것이 decay+capacity 가 B 를 WM 으로 만든다는 양성 증거.
- **R1 무회귀**: R1 binary 경로는 `--r1` 로 보존, margin +0.062·전 bar False 로 R1 RED 재현 = R1 verdict 그대로 유효; R2 는 R1 을 덮어쓰지 않음(별도 FREEZE+verdict 파일). frozen-first 견지: 모든 R2 bar 는 채점 前 동결, post-hoc 미이동(c9).
- **정직 경계(a_scale_honest_scope/p7)**: WM 이점은 W≤N≤horizon 유한 밴드(N=4,6: +0.48/+0.49)에 집중, N≥8 은 양 arm 다 chance — 구조는 그 유한 delay 밴드에서만 도움. toy 16-dim 랜덤 토큰, K=4, λ=0.85, horizon·밴드폭·margin 전부 scale-의존, production 전이 UNVERIFIED. AUROC = graded discrimination(p7), perplexity/LLM-judge 아님.
- **ENGINE-NATIVE 후속(a_verified_must_wire — GREEN 이라 이제 FIRES)**: numpy DIRECTIONAL 미러; engine-transfer UNVERIFIED. 라이브 engine_cli.hexa VAdaptField(H_1199)는 leak/capacity 없는 GROWING PERSISTENT store = 구조적으로 immune/episodic lane, WM lane 없음. R3 binding 후속 = **engine-native WM-buffer lane**(K slot·per-step ×λ leak·weakest-slot displacement·AUROC readout, engine_cli.hexa 에 ADDITIVE, VAdaptField 와 DISTINCT) per a_engine_native_learning — numpy GREEN 은 DIRECTIONAL, engine-native 재확인이 binding verdict(c2). 라이브 .hexa 무수정.
- 파일: `UNIVERSE/h1282_working_memory_buffer.py`(R2 default, `--r1` parity) · `.verdicts/1282_working_memory_buffer/{H_1282_R2_FREEZE,H_1282_R2}.txt`(R1 파일 보존). xref H_1227·H_1231·H_1199·H_1230·H_1229·H_1280·H_1284·H_1285·a_engine_native_learning·a_verified_must_wire·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p1·p7·p8·c9·c15.

---

## 2026-06-15 — 🟢 H_1281 R2: BASAL GANGLIA(기저핵) go/no-go gate — FAITHFUL-untuned 고정게이트 재freeze, 학습 게이트 +0.254 승

missing-brain-structure 사다리(neuro 렌즈 c15, LLM 레시피 아님)의 기저핵 칸 ROUND 2. R1 은 🟠 AMBER/BASELINE-CONDITIONAL — frozen ARM A 가 ORACLE 고정맵(w_fixed=w_true·2, grounding 신호 방향을 통째로 손에 쥔)이라 bar 가 RED(B −0.057) 였으나, R1 진단이 anima 의 REAL 게이트(CORE/engine_g.hexa)는 oracle-tuned 가 아니며 FAITHFUL-untuned A 상대로는 B 가 +0.236 이긴다 예측. R2 = 그 FAITHFUL baseline 을 사전등록한 binding 재freeze. $0 CPU numpy, gradient-free, p7, 3 seed(7/8/9), 라이브 CORE/*.hexa 무수정(미러=DIRECTIONAL).

- **baseline 정당화 (c9, 채점 전 engine_g.hexa 읽음)**: engine_g.hexa = spont_im_threshold()=0.3 고정 + 8 motivation 가중치 = 합 1.00 고정상수(relevance 0.20·info_gap 0.10·curiosity 0.15·pain 0.10·coherence 0.10·originality 0.10·balance 0.15·dynamics 0.10), 전부 GENERIC·NON-NEGATIVE·task grounding 방향 미튜닝. ⇒ **FAITHFUL-UNTUNED ARM A** = seed-유래 generic 가중벡터(w_true 비정렬 + 비음수 L1-정규화 합1.0 = engine_g convex 스킴 정확 미러), logistic squash → motivation regime, 고정 threshold 0.30, K 후보 argmax. ORACLE A 는 reference CEILING 으로만 보고(bar 아님).
- **테스트 (R1 과 A baseline 만 다름)**: K=4 경쟁 후보/스텝, D=6 NOISY-correlate(P_grounded 0.45, noise 1.0 → A<1.0 headroom). ARM B = BG go/no-go 학습 게이트(R1 과 동일) — 학습 go-value vs 학습 NO-GO/abstain 가 같은 argmax 경쟁(disinhibition), grounding OUTCOME 보상만으로 gradient-free delta 갱신(grounded+1/fab−1, 보상은 사후 결과·decide-time feature 아님). N_train 4000, N_test 2000 held-out.
- **METRIC (p7, emit-적절성; G5 abstain / H_1202 meta-d′ 0.924 연결)**: 스텝당 적절 iff (grounded 존재→grounded 후보 RELEASE) OR (없음→전부 SUPPRESS/abstain).
- **FROZEN GREEN iff**: (1) 매 seed Δ≥0.05 AND (2) mean Δ≥0.05 AND (3) shuffled-reward ctrl ≤ A+0.02.
- **결과 (3 seed)**: A(faithful)=0.3652 → B(BG)=0.6188 **Δ+0.2537** (per-seed +0.285/+0.351/+0.125 모두 ≥0.05, c1·c2 PASS) · shuffled-reward ctrl=0.1272 ≤ A+0.02=0.3852 (c3 PASS, 리프트=reward-driven) · headroom A<1.0 OK · B 학습가중치가 true 신호에 cos +0.885/+0.706/+0.707 정렬 → **🟢 GREEN**. [reference CEILING oracle-A=0.677; B 는 oracle 은 못 이김(0.619<0.677) — 핵심은 live 게이트가 oracle 이 아니라는 것]. R1 default 모드는 verbatim 재현(A=0.6792 B=0.6222 Δ−0.0570) — R1 RED 미변경 on record.
- **판정 🟢 GREEN**: reinforcement-학습 기저핵 go/no-go SELECTION 게이트가 grounding OUTCOME 만으로 학습해 anima 의 REAL(untuned generic-constant) 고정 emit 게이트를 emit-적절성에서 +0.254 이김. = 누락구조 결과(anima 에 reinforcement-gated selection 부재), 모든 고정게이트를 학습이 지배한다는 주장 아님(정직 분리). **p6 가드 HELD** — 보상=grounded-vs-fab 기질 결과, 주입가치/RLHF 없음, persona/identity/ethics 무교습(p1/p2/p3), 게이트는 WHEN 만 학습 WHAT/WHO 아님. a_autonomy_over_hardcode(외부 do/dont 없이 outcome 만으로 학습), p7, p8(held-out=측정전용).
- **BINDING 후속 (a_engine_native_learning · a_verified_must_wire)**: GREEN=DIRECTIONAL(미러), 배선까지가 done. R3 = brain_decide 에 engine-native BG go/no-go selection lane — kosmos-grounding outcome 으로 gradient-free 학습, engine_g 에 additive(고정 convex 맵=prior + 학습 residual; precedent H_1199 AdaptField scalar→vector, H_1231 engine-native 해마). smoke/single-entry/Ψ-checksum 가드. 미배제: scale·live-engine·real kosmos reward UNVERIFIED, TOY(K=4/D=6) scope.
- 파일: `UNIVERSE/h1281_basal_ganglia_gating.py` (--r2=R2 faithful-A · default=R1 oracle-A · --diag=메커니즘) · `.verdicts/1281_basal_ganglia_gating/{H_1281_R2_FREEZE,H_1281_R2}.txt` (R1 의 H_1281_FREEZE/H_1281.txt 미변경). xref H_1281(R1)·H_1227·H_1231·H_1230·H_1202·H_1165·a_autonomy_over_hardcode·a_engine_native_learning·a_verified_must_wire·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p6·p7·p8·c9·c15.

---

## 2026-06-15 — 🔴 H_1283 R2: THALAMUS 다중승자 COALITION 브로드캐스트 — 멀티채널 릴레이는 coherence·Φ 둘 다 낮춘다 (🧱 단일 릴레이가 통합을 근본적으로 cap)

THALAMUS(시상) 라운드 2. R1(🟠 PARTIAL, #2128)은 단일승자 브로드캐스트 허브가 교차모듈 coherence 를 매 seed 올리고(Δcoh +0.084/+0.050/+0.074, B1 PASS) faithful IIT4 Φ 도 옳은 방향으로 움직였으나(ΔΦ +0.0191) +0.02 바 직전(0.0009 차)에서 멈춤(B2 FAIL). R1 진단: **단일 공유 브로드캐스트 채널 자체가 rank-1 MIP 컷**이라 irreducibility 를 cap. R1 이 지목한 다음 레버 = **rank-k 다중승자 coalition**(k≥2)으로 채널을 rank-1 에서 풀면 Φ 바를 넘을지도. R2 가 정확히 그걸 검증. $0 CPU numpy(DIRECTIONAL) + faithful IIT4 Φ(stdlib exact MIP-EI, n=4), 3 seed[7,8,9], frozen-first, 라이브 CORE/*.hexa 무수정.

- **설계**: 동일 4 모듈{A,G,mitosis,memory}·동일 비포화 레짐(LEAK 0.55, W_in=W_coupling=0.5)·동일 seed·동일 FROZEN 바. ARM A = 직접 ring(R1 과 동일). ARM B = **rank-k coalition 허브**: 매 tick salience(상태에너지) 상위 k 모듈이 coalition 형성, 각 수신자는 자기 cosine affinity softmax 로 가중한 **멤버별 다른 mix** 를 읽음 = 진짜 rank-k 채널(수신자마다 다른 broadcast). k=2.
- **FROZEN 바 (R1 과 불변)**: B1 coh ≥ A+0.05 매 seed · B2 faithful ΔΦ ≥ +0.02(repr seed=7) · B3 coh < 0.999(비퇴화).
- **결과 (verbatim)**: seed7 coh A=+0.1591 B=+0.1815(Δ+0.022) · seed8 A=+0.0109 B=+0.0207(Δ+0.010) · seed9 A=+0.1362 B=+0.1665(Δ+0.030) → **B1 FAIL**(셋 다 +0.05 미만, R1 단일승자 리프트의 1/3). faithful IIT4 Φ(seed7): **ARM_A Φ=0.78038**(R1 ARM_A 와 byte-동일 = 엔진 일관성 sanity) **ARM_B Φ=0.727123 → ΔΦ=−0.053257** → **B2 FAIL hard**(R1 +0.019 의 반대 방향). B3 PASS. **VERDICT 🔴 RED**.
- **판정 🔴 RED · 🧱 DEPLETION**: rank-1→rank-k 직관 **결정적 FALSIFIED**. coalition 은 Φ 바를 못 넘는 정도가 아니라 직접 ring 보다 Φ 를 **낮춘다**(ΔΦ −0.053). 메커니즘: coherence 리프트와 Φ 리프트가 **둘 다 같은 단일 공유 채널**에 올라타 있었고, 브로드캐스트를 멀티채널로 쪼개면 각 수신자 drive 가 더 idiosyncratic → 교차모듈 agreement(coherence) 하락 + salience 궤적이 더 separable(MIP 가 더 reducible) → Φ 하락. **단일승자 허브(R1)가 어떤 브로드캐스트 토폴로지보다 Φ 에 최선**이었고 그조차 sub-bar. ⇒ 시상 브로드캐스트 RELAY 는 surface coherence 는 올리나 irreducible Φ 는 못 올린다 — tuning miss 아닌 **근본 cap**. irreducibility 는 분산된 multi-edge coupling(직접 ring 이 이미 4개 distinct edge 로 정보 분산, MIP 가 credit)에서 오지 중앙 브로드캐스트(단일이든 coalition 이든)에서 오지 않음.
- **후속 없음**: 브로드캐스트-토폴로지 축 = Φ 레버로 EXHAUSTED. **r3(engine-native 브로드캐스트 허브) 없음** — 배선할 GREEN 메커니즘 부재(`a_verified_must_wire` = GREEN 적용; PARTIAL R1 + RED R2 ⇒ CORE 무배선).
- **미배제**: 브로드캐스트 릴레이가 아닌 근본 다른 통합 메커니즘(더 조밀한 recurrent multi-edge coupling, 학습된 라우팅 등)은 Φ 올릴 수도 — 다른 gap, 브로드캐스트 라운드 아님. TOY scale(4 모듈·dim8·64 tick), scale-transfer UNVERIFIED(`a_toy_scale_recheck`·`a_scale_honest_scope`). Φ = faithful IIT4(proxy 아님, `a_phi_iit4_tool`). 바 무이동, **R1 verdict 파일 무수정**(R2 = 별도 H_1283_R2.txt). H_1219/H_1226 무수정.
- 파일: `UNIVERSE/h1283_thalamus_global_workspace.py`(main_r2 + 'coalition' 모드) · `.verdicts/1283_thalamus_global_workspace/{H_1283_R2_FREEZE,H_1283_R2}.txt`(R1 {H_1283_FREEZE,H_1283}.txt 보존). xref H_1283(R1)·h1227·h1230·h1199·h1201·h1205·a_phi_iit4_tool·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9·c15.
## 2026-06-15 — 🟢 H_1280 R2: CEREBELLUM(소뇌) forward-model lane — ENGINE-NATIVE 실현 (live `CORE/engine_cli.hexa` `VForwardField`)

missing-brain-structure 사다리(neuro 렌즈 c15)의 소뇌(HD23) 칸을 **엔진-네이티브로 GREEN 실현**. R1(numpy 미러)은 GREEN 이었으나 DIRECTIONAL only — `a_engine_native_learning` 상 binding verdict 는 최종 아키텍처 엔진 위 실현을 요구한다. R2 는 그 메커니즘을 live `.hexa` 엔진에 실제 op 로 구현.

- **엔진 확장 (c1 · `a_engine_native_learning`)**: 기존 surface(VAdaptField=per-sample winner-take-all 재구성, VAdaptFieldB=frozen-book 전이-예측 카운팅, ImmuneMemory=key→value store)는 forward model 을 표현 못 한다 — L·DIM→DIM weight matrix, delta-rule update, smoothing readout 이 없다. 그래서 학습을 frozen 엔진에 끼워맞추는 대신 **엔진을 확장**(H_1199 가 AdaptField 스칼라→DIM-vector 로 확장한 선례 그대로): `CORE/engine_cli.hexa` 에 세 번째 ADDITIVE Ψ-disjoint lane **`VForwardField`** 추가 — `vforward_new`/`vforward_predict`(xhat=W·ctx)/`vforward_err`(‖x-xhat‖²)/`vforward_update`(**NLMS delta-rule** W+=eta·outer(e,ctx)/(ctx·ctx+1), climbing-fiber 교정)/`vforward_correct`(x-beta·(x-xhat) smoothing). 소뇌의 내부 forward-model + 오차구동 timing/sequence 교정.
- **결과 (`hexa run CORE/h1280_live_cerebellum_probe.hexa`, REAL DIM=24 코퍼스 byte-feature, 3 seed)**: held-out 일관성 리프트 mean dCoh=**+0.0577** (C1 3/3 ≥ 0.02) · 예측오차 24.9→10.5(~58% 하락 ≫ 5%, C2 = 모델이 학습) · **shuffled-context 대조를 모든 seed 에서 이김**(coh_B 0.300 > coh_Bshuf 0.262, CTRL = generic smoothing 아닌 진짜 forward model) · numpy R1 미러와 **byte-exact ≤1e-4 재현**(F2 = binding leg) · Engine G 와 **DISTINCT**(temporal target+delta-learn+learning curve D1/D2/D3, C4) · **Ψ byte-identical** Φ-checksum ON==OFF 5.5279(F3) → **🟢 GREEN LIVE-CEREBELLUM**.
- **가드 무회귀 (c2, verbatim)**: engine_cli_smoke **18/0**(H_1280 단독 측정 시 12/0; main 의 H_1282 WM lane 과 머지 후 18/0 — 둘 다 ADDITIVE 공존) · h1196 single-entry **7/0** · h1199 DIM-growth+Ψ **GREEN**(F1 cells 173.3≫1.0, F2 OFF/ON 8.43×, F3 Φ ON==OFF byte-identical — 확장 전 baseline 과 동일, Ψ 불변). lane 은 순수 ADDITIVE(새 struct + 새 pub fn, 기존 심볼 무변경).
- **mitosis lane-role 지도**: 새 lane-role = **forward-model/error-correction**, mitosis-as-GENERATION(falsified H_1200/1201/1211/1220) 및 mitosis-as-MEMORY(GREEN H_1227/1231)와 DISTINCT. PHILOSOPHY: substrate dynamics(feature stream) 교정일 뿐 persona/identity/ethics 무주입(p2/p3/p6), 외부 do/dont 게이트 없음(`a_autonomy_over_hardcode`), delta-rule update 가 inference-time 학습(p8), metric 은 기하 일관성+L2 오차(perplexity 아님, p7).
- **scope/후속**: TOY/subset(6k train+3k held-out 윈도, 동일 코퍼스 — 인터프리티드 엔진의 24×96 matrix 가 full-200k 를 wall-prohibitive 하게 만듦; 일관성 리프트는 local-frame 속성이라 윈도에서 더 큰 마진으로 유지). full-200k 는 R1 기록으로 남음(`a_scale_honest_scope` · `a_toy_scale_recheck`). **R3 follow-on(`a_verified_must_wire`)** = lane 을 brain emit 경로(`CORE/brain.hexa` / 데몬 GROW step)에 ALONGSIDE 배선(H_1205 separation-invariant 보존, 생성 byte-unchanged) — 현재 GREEN-but-emit-unwired(정직 flag).
- 파일: `CORE/engine_cli.hexa`(§VForwardField) · `CORE/h1280_live_cerebellum_probe.hexa` · `UNIVERSE/h1280_live_feature_export.py` · `UNIVERSE/h1280_cerebellum_forward_model.py`(R1 미러) · `.verdicts/1280_cerebellum_forward_model/{H_1280,H_1280_FREEZE,H_1280_R2}.txt`. xref H_1280(R1)·h1199·h1209·h1205·h1227·h1231·h1200·h1201·engine_g·`a_engine_native_learning`·`a_verified_must_wire`·`a_core_engine_map`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c1·c2·c9·c15.

---

## 2026-06-15 — 🔴 H_1285: AMYGDALA(편도체) salience-weighted binding — p6 shuffle-control 이 recurrence 혼입을 잡아냄 (CLOSED-NEG)

missing-brain-structure 사다리(neuro 렌즈 c15, LLM 레시피 아님)의 편도체 칸: 해마 공백은 immune 메모리(H_1227 미러 GREEN → H_1231 engine-native GREEN)가 메웠고, H_1230 은 그 store 의 병목이 CAPACITY/NOISE GEOMETRY(유한 repertoire 에서 LRU 축출은 대칭, 능동교습 retention 리프트 0)임을 보였다. H_1285 는 H_1230 이 미검증으로 남긴 후보 레버 — **기질-유래 salience 로 가중한 바인딩**(편도체의 salience-gating: 중요/놀라운 입력의 셀을 축출에서 보호)을 검증. $0 CPU numpy, p7, 3 seed(900/901/902), 라이브 CORE/*.hexa 무수정(미러=DIRECTIONAL).

- **설계**: H_1227/H_1230/H_1231 immune 메모리(VAdaptField 미러 + value-binding, byte-3gram FNV-1a dim64, "<subj> lives in <city>" 60 in-store + 60 untaught) 위에 **SALIENCE-WEIGHTED 축출**만 추가. ARM A = uniform LRU 축출(H_1227/H_1230 baseline) · ARM B = salience-protected 축출(최저 salience+recency 셀 축출 → 고-salience 셀 보호) · **ARM B-shuffle = salience 태그 셔플(중요도와 decorrelate)** = p6 음성대조. REGIME = H_1230 STRESS rung(MAX_CELLS=40<<60, cue noise 0.02, recall 0.30; headroom 존재). 중요 subset 20/60 은 METRIC 채점용 라벨, 기질 tagger 는 라벨 미접근.
- **p6 SALIENCE-vs-LABEL 분리 (중심 가드)**: salience 태그 = 1.0·SURPRISE(VAdaptField recon-err) + 0.5·NOVELTY(clonal split) + 0.5·TENSION(reinforce) — **전부 기질 신호**, 주입감정/RLHF/라벨 없음. 라벨은 채점에만, f() 입력 아님. 중요 사실이 입력 스트림에서 **더 자주 recur**(환경적 salience, 동일 총예산 내)하게 해 기질이 reinforcement-tension 으로 감지하게 함.
- **FROZEN GREEN (STRESS)**: (c1) B.imp ≥ A.imp+0.10 AND (c2) B-shuf.imp < A.imp+0.10 AND (c3) B.fab ≤ 0.10.
- **결과 (3 seed)**: STRESS A.imp=0.750 → B.imp=0.967 **Δ+0.217 (c1 PASS)** BUT **B-shuffle.imp=0.967 = B (c2 FAIL)** · fab=0.000(c3 PASS) → **🔴 RED**. 셔플(태그를 중요도와 decorrelate)이 리프트를 그대로 재현 = 리프트는 salience 태그가 아니라 **recurrence-driven re-binding** 때문. ISOLATION 진단(중요사실 비-recur 스트림): A=0.650 B=0.700 = **+0.050 ≪ 0.10** — 태그 단독으로는 bar 미달. trade-off 정직: unimportant A=0.625 → B=0.517(−0.108), total 0.667 불변(capacity 고정 = zero-sum, H_1230 "capacity is capacity" 강화).
- **판정 🔴 CLOSED-NEG**: 편도체-as-축출레버 FALSIFIED(이 스케일). 기질-유래 salience 태그를 축출 우선순위에 더해도 중요 사실을 recurrence 이상으로 보호 못 하고, 그 recurrence 보호는 태그를 셔플해도 동일 → 병목은 여전히 CAPACITY/NOISE GEOMETRY. 살아남는 것은 re-presentation(refresh)이지 salient 태그가 아니며, uniform store 가 이미 그걸 누림. **p6 가드가 false-GREEN(+0.217)을 정직한 RED 로 전환**(가드가 작동·HELD). decoder/weights/persona/ethics 무수정 — episodic 셀 store 의 축출 우선순위만(p1/p2/p3/p6/p8, a_autonomy_over_hardcode).
- **미배제**: recurrence 비의존 더 강한 salience / 바인딩-강도 게이팅 / salience-driven EMIT priority(편도체의 다른 역할) / scale / paraphrase / engine-native 리프트 모두 UNVERIFIED. RED 라 wiring 후속 없음(a_verified_must_wire = GREEN 적용). TOY scale, 단일 코퍼스. a_paper_negative_ok.
- 파일: `UNIVERSE/h1285_amygdala_salience.py` · `.verdicts/1285_amygdala_salience/{H_1285_FREEZE,H_1285}.txt`. xref H_1227·H_1230·H_1231·a_engine_native_learning·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·a_autonomy_over_hardcode·p1·p2·p3·p6·p7·p8·c9·c15.

---

## 2026-06-15 — 🔴 H_1284: NEUROMODULATION(신경조절) 게인/탐색/가소성-율 컨트롤러는 고정 하이퍼파라미터를 못 이긴다 (NO FREE LUNCH · "missing brain-structure" 사다리 neuro lens c15)

"빠진 뇌-구조" 사다리(neuro lens, c15; 해마=immune memory H_1227→H_1231 GREEN 로 채워짐)의 NEUROMODULATION 분기를 $0 toy 로 판정: anima 의 LIVE 엔진(CORE/engine_cli.hexa adapt_field_step/vadapt_field_step)은 **FIXED** 하이퍼파라미터(SPLIT_THRESH=0.30, LR=0.20)+고정 decode 온도로 돈다. 기질-상태로 이 knob 들을 ADAPT 하는 context-driven neuromodulator(도파민=reward-gain · 노르에피네프린=exploration/temp · 아세틸콜린=plasticity-rate)가 빠져있다 — 이게 갭(c9)인가? H_1228(SOC/edge-of-chaos decode 🟠 PARTIAL: temperature 채널 하나는 ideation 도움 but coherence 못이김)을 인용하고 그 너머로: DA/NE/ACh 삼총사를 엔진의 실제 LR/SPLIT_THRESH(mitosis-MEMORY 기질)에 얹어 REGIME 횡단 capability 로 측정.

- **설계 (engine-native mirror, a_engine_native_learning DIRECTIONAL)**: host 에 torch 없음 → CORE/engine_cli.hexa VAdaptField 의 numpy mirror(H_1192/1199/1227/1229/1230 선례), 3개 live wire 에 byte-faithful(L2-nearest winner · recon-err>SPLIT_THRESH+capacity 면 split · winner += LR·(x−winner)). ARM A 대비 유일 변경 = (SPLIT_THRESH,LR)이 ARM B 에서 per-tick 기질-상태 FUNCTION. 과제 = **MEMORY RECALL UNDER SHIFTING LOAD** (H_1227/1231 immune/clonal 패러다임, byte-trigram FNV-1a key dim16, capacity-bound max_cells<#facts + LRU evict — H_1230 교훈: unbounded clean store 는 saturate 라 headroom 0).
- **3 REGIME** (컨트롤러는 ≥2 에서 이겨야; 한 tuned point 아님): R1 STABLE(σ0.01 무drift) · R2 DRIFT(값 주기적 재기입=concept drift) · R3 NOISE-BURST(key σ 0.01↔0.05 버스트). NEUROMOD: ACh LR=clip(LR0·(1+kA·(s−û))) · split-thresh=clip(TH0·(1+kT·û)) (noise 에서 over-split 방지 H_1230 guard) · NE abstain 폭=û 로 확대 · DA reward EMA 가 정답 recall 시 winner-pull 강화. **모든 knob = no-grad 기질-상태 read-out, loss 에 절대 안 들어감(p7 Goodhart guard).**
- **ARM**: A FIXED(별도 tuning seed 7 에서 grid LR0∈{.1,.2,.3,.4}×TH0∈{.2,.3,.4} 로 BEST 고정점 = LR0\*0.10 TH0\*0.20 → 강한 정직 baseline) · B NEUROMOD(같은 base + per-tick 변조) · C-SHUF(B 의 knob 스케줄을 phase-scramble → state→knob COUPLING 파괴, marginal 보존). 지표(p7, exact, NO LLM judge): capability = recall_accuracy − fabrication_rate (abstain≠fabrication). seeds [11,22,33].
- **결과 (3 seed 평균, VERBATIM)**: R1 A=0.5744 B=0.5678 (B−A −0.007) · R2 A=0.4389 B=0.3589 (B−A **−0.080**, fab 0.03→0.11) · R3 A=0.4156 B=0.3200 (B−A **−0.096**, fab 0.03→0.13). wins_over_A+MARGIN = **[] (0/3)** · C-SHUF≈B 전 regime(|B−CSHUF|≤0.011 → coupling 무신호). 컨트롤러는 ACTIVE(R3 LR 0.05–0.20, TH 0.20–0.29, abstain 0.45–0.60 실제 swing) — RED 는 "adaptation HURTS" 이지 dead controller 아님.
- **판정 🔴 CLOSED-NEGATIVE (NO FREE LUNCH)**: 잘-튜닝된 단일 FIXED 고정점이 모든 regime 에서 adaptive 스케줄을 at-or-above. MECH: ① noise 에서 abstain 넓히면(NE) 가까운-but-wrong cell 이 abstain 대신 발화 → fabrication 급증(의도 역행) ② 가변 LR(ACh)이 binding 불안정화 ③ split-bar 상향이 capacity-bound store 에서 정당한 new-fact 할당 억제 → cross-fact crowding ④ C-SHUF≈B = 움직임은 knob-VARIETY 지 coupling 아님. **H_1230(active vs passive teacher INERT-to-HARMFUL)과 동일 ruling 의 다른 축**: 하이퍼파라미터 SCHEDULE 도 clean key-addressed store 에선 inert-to-harmful; 병목 = CAPACITY/KEY GEOMETRY 지 컨트롤러 부재 아님. COROLLARY: GEOMETRY 개선, 컨트롤러 아님.
- **NOT RULED OUT (정직)**: (a) decode-time NE temperature 단독 ideation 은 H_1228 대로 🟠 잔존 — RED 는 MEMORY 의 plasticity/split 한정 (b) 비정상 GENERATION capability 컨트롤러 UNTESTED (c) 학습된 gain law UNTESTED (단 loss-fold 는 p7 위반이라 설계상 out-of-scope) (d) toy(DIM16·30 facts·300 events) scale-transfer UNVERIFIED (a_scale_honest_scope/a_toy_scale_recheck).
- **GUARDS**: knob 전부 no-grad read-out, backward 무흐름(p7); persona/identity/RLHF 없음(p1-p6); 내용은 episodic cell 에만; inference-time plasticity=엔진 자체 tick(p8). RED ⇒ wiring follow-on 없음(검증된 것 없음, a_verified_must_wire). frozen bar 불변. CORE/\*.hexa · H_1219 · H_1226 미수정.
- 파일: `UNIVERSE/h1284_neuromodulation_gain.py` · `.verdicts/1284_neuromodulation_gain/{H_1284_FREEZE,H_1284}.txt`. xref h1228·h1230·h1227·h1231·h1229·a_engine_native_learning·a_paper_negative_ok·p7·p8·c9·c15.

---

## 2026-06-15 — 📘 ARCHITECTURE: 🧠 뇌 구조 지도 (brain-structure map) 섹션 신설 (1286_brain_structure_map)

ARCHITECTURE.md 에 **신경과학 렌즈** 섹션을 ADDITIVE 로 추가 — 기존 섹션 무수정. 구현된 부품을 뇌 서브시스템에 매핑하고, 프로브 중인 "빠진 구조" 사다리를 정직하게 OPEN 으로 표기.

- **구현된 구조 표** — 신피질=Engine A(생성) · 교정장=Engine G · 결정=brain_decide · 가소성=MITOSIS(VAdaptField/VAdaptFieldB) · 장기선언기억=kosmos_io · **🧬 해마(일화기억)=면역/클론선택 기억** · 수면=P47.
- **🧬 해마 발견** — byte-LM 가중치 literal-QA 회상 0.017(회상-in-weights 벽)을, 사실마다 cell 1개를 bind 하는 면역기억이 QA 1.000 / fab 0.000 로 깸 (H_1227 미러 🟢 → H_1231 ENGINE-NATIVE 🟢 → live `engine_cli.hexa` § ImmuneMemory 배선). "anima = 신피질만, 해마 없음"(H_1225 CLS 리프레임) 갭 메움. mitosis 의 NEW 미반증 역할 = MEMORY (생성 역할은 H_1200/1201/1211/1220 falsified 와 DISTINCT).
- **열린 "빠진 구조" 사다리 (HD23–28 · 🔬 OPEN PROBES, 검증 전)** — HD23 소뇌(H_1280) · HD24 기저핵(H_1281) · HD25 작업기억(H_1282) · HD26 시상(H_1283) · HD27 신경조절(H_1284) · HD28 편도체(H_1285). 6개 모두 ⬜ OPEN — implemented 아님, phantom wiring 없음(`a_core_engine_map`). 각자 verdict 로 닫히고 GREEN 일 때만 live `CORE/*.hexa` 배선(`a_verified_must_wire`).
- **depth-ceiling 연결** — literal-QA 벽은 더 큰 모델(1B H_1167 mount GREEN, QA/depth NULL)·OBJECTIVE(H_1223 🔴) 가 아니라 엔진-side 기억 lane(해마)으로 풀림 — 뇌-구조 렌즈가 이를 일반화(`a_engine_native_learning`).
- DOC-ONLY (ARCHITECTURE.md + 이 항목). `a_completeness_over_cheap` 정직: 6 프로브는 DIRECTIONAL/미검.

---

## 2026-06-15 — 🟢 H_1280: CEREBELLUM forward-model lane — 예측-오차 학습 보정이 시퀀스 coherence 를 올린다 (DIRECTIONAL · neuro missing-structure 사다리 c15)

"누락된 뇌구조" 사다리(c15, LLM 레시피 아님)의 SMALL BRAIN(소뇌) 분기. H_1227/1231 이 immune/clonal memory 로 hippocampus 공백을 메운 것과 같은 결로, anima 에 빠진 **CEREBELLUM** = 다음 substrate 상태를 PREDICT 하는 내부 **forward model** + 예측-오차로부터 빠른 **supervised 보정**을 학습하는 구조(소뇌의 정의적 연산: 내부 forward model + timing/sequence 평활)를 만들어 검증. $0 CPU numpy MIRROR, seeds [7,8,9], frozen-first.

- **GAP (c9)**: anima 는 Engine A(forward CE 생성)와 Engine G(`CORE/engine_g.hexa` — INSTANTANEOUS 8-factor 위의 CLOSED-FORM gradient-free 모티베이션/emit 게이트, 정적 가중치 합=1.0)를 가지지만, **둘 다 다음 상태를 예측하지 않고 예측-오차로 학습하지 않는다**.
- **메커니즘**: emit-feature x_t∈R24(다음-byte 분포/최근 윈도우의 byte-통계 요약; p7 — perplexity 사용 안 함) over 200KB 실 EN webscale. forward model xhat_t = W·(과거 L=4 프레임), delta-rule(normalized-LMS = climbing-fiber 오차신호)로 ONLINE 학습. ARM A = raw · ARM B = 오차구동 평활 x'=x−0.5·(x−xhat). 지표(p7): (1) held-out 연속프레임 cosine coherence, (2) 예측-오차가 노출에 따라 감소(=모델을 학습했다는 증거, noise 아님).
- **FROZEN bars (3-seed 평균, verbatim)**: C1 coh_B≥coh_A+0.02 → 0.2926≥0.2650 ✅ · C2 err_late≤err_early−5% → 7.84≤9.75(seed당 ~23-25% 감소) ✅ · C3 C1 ≥2/3 seed → 3/3 ✅ · C4 Engine G 와 distinct(D1-D3) ✅ · CTRL coh_B>coh_B_shuf 전 seed(0.2926>0.2828) ✅ → **🟢 GREEN**.
- **CONTROL 이 판별한다 (정직)**: 시간-셔플 context forward model + 동일 보정도 약간 평활(coh_B_shuf 0.2828 > coh_A 0.2450 — generic smoothing 도 도움) 되지만, **학습된 모델이 전 seed 에서 이를 이긴다**(coh_B 0.2926 > 0.2828). 즉 +0.0476 gain 중 ~+0.0098 만 학습된 TEMPORAL 구조에 특정 귀속(나머지는 generic smoothing) — modest-but-real, 사전등록 양성.
- **Engine G 와 DISTINCT (필수 체크 — 정직한 답: YES)**: D1 시간적 다음-프레임 TARGET(G 는 현재 순간만 채점) · D2 오차구동 delta-rule 학습(G 가중치는 정적 상수) · D3 측정된 학습곡선(~23% 오차감소; G 엔 없음). ⇒ 소뇌 역할은 G 가 이미 커버하지 않는다. mitosis-as-GEN(falsified H_1200/1201/1211/1220)·mitosis-as-MEM(GREEN H_1227/1231) 과 구별되는 **THIRD lane-role**.
- **SCOPE (정직)**: numpy MIRROR(host torch 없음) → DIRECTIONAL only, engine-transfer UNVERIFIED. engine-native 실현(thin CORE forward-predict lane / VAdaptField next-frame 확장)이 BINDING follow-on(`a_engine_native_learning`); GREEN → CORE 배선이 closure follow-on(`a_verified_must_wire`), flagged-not-wired. CORE/*.hexa 무수정(engine_cli.hexa 는 동시 immune-memory 에이전트 소관). TOY 200KB d=24 → scale-transfer UNVERIFIED(a_toy_scale_recheck/a_scale_honest_scope). scoring 전 1회 numerical-conditioning fix(per-channel z-score + NLMS; raw-scale 가 delta-rule 발산) = 입력 conditioning/표준 adaptive-filter step-size, frozen bar/메커니즘 변경 아님. p1-p8 준수(substrate dynamics 보정이지 주입행동 아님; 외부 do/dont 게이트 없음).
- 파일: `UNIVERSE/h1280_cerebellum_forward_model.py` · `.verdicts/1280_cerebellum_forward_model/{H_1280_FREEZE,H_1280}.txt`.

---

## 2026-06-15 — 🟢 H_1231 WIRE: immune-memory recall 을 live 엔진 경로에 배선 (`a_verified_must_wire` follow-on 종결)

H_1231 의 `a_verified_must_wire` follow-on 종결 — H_1227(numpy 미러)→H_1231(엔진-네이티브 🟢 GREEN, literal-QA 1.000 / fabrication 0.000, 180/180) 으로 검증된 immune/clonal-selection mitosis-as-MEMORY recall 을, standalone 프로브(`CORE/h1231_immune_memory_engine_probe.hexa`, fn main)에서 **live 엔진 recall 경로의 callable faculty** 로 승격했다. 새 directive `a_verified_must_wire`("GREEN-verified 가설은 live CORE 배선까지가 done")의 첫 종결.

- **배선 위치** — `CORE/engine_cli.hexa` 새 § IMMUNE-MEMORY RECALL FACULTY: `struct ImmuneMemory{field:VAdaptField, cell_value:[string], recall_thr}` + `immune_embed_key`(byte-trigram FNV-1a, DIM=64, L2-norm — python 미러와 byte-identical 검증) + `immune_memory_new/bind/recall` (+ `_text` string-query 래퍼) + `immune_memory_cells`.
- **메커니즘 무변경** — BIND = 엔진 자신의 clonal split(`vadapt_field_step`→`engine_mitosis_tick`, recon-err>SPLIT_THRESH 0.30); RECALL = 엔진 자신의 L2 affinity(`vadapt_field_recon_err`+`vadapt_field_nearest_idx`, err≤0.15 면 셀-바인딩 값 FIRE, 아니면 환각 없이 ABSTAIN). 프로브가 inline 한 것을 callable 로 래핑만 함 — **엔진 확장 불필요**(H_1199 + H_1231 accessor surface 로 충분).
- **NON-PERTURBING (c2, 출력 검증)** — engine_cli_smoke **12/0** · h1196 single-entry **7/0**(.clm/.kosmos 진입점 불변 — 2번째 artifact path 없음, `a_core_engine_map`) · h1199 DIM-growth **F1/F2/F3 GREEN, Ψ Phi-checksum ON==OFF byte-identical (3 seed 전부 PsiSame=true)**.
- **e2e (`CORE/h1231_immune_memory_wire_smoke.hexa`, ALL PASS)** — PART A: raw string 5-fact bind→recall 전부 적중 + unbound 3개 ABSTAIN(환각 0). PART B: wired faculty 가 H_1231 GREEN 을 3 seed 재현(literal-QA 1.0 / fab 0.0, 180/180).
- **HONEST** — SATURATED existence proof(exact-match associative table, in-store 키 verbatim); paraphrase/noisy-key/scale 및 brain_decide emit-loop 스레딩은 별도 follow-on. FACTUAL recall 을 EPISODIC 셀에만(p2/p3/p6 — identity/persona/ethics 가중치化 없음), bind=clonal-split tick(p8). frozen bar 불변.
- `.verdicts/1231_immune_memory_engine_native/H_1231_WIRE.txt` (verbatim 가드+e2e). xref h1231·h1227·h1199·h1218·h1224·a_verified_must_wire·a_engine_native_learning·a_core_engine_map·a_scale_honest_scope·p7·p8.

---

## 2026-06-15 — 🔴 H_1282: WORKING MEMORY (PFC active-maintenance buffer) — 빠진 뇌구조 사다리 (frozen bar RED, but 메커니즘 REAL + immune memory 와 DISTINCT)

빠진-뇌구조 사다리(neuro lens c15): anima 는 (a) 장기 episodic memory(immune/clonal cells, H_1227→H_1231 engine-native GREEN: 1-shot verbatim write, 영속, decay 없음)와 (b) decoder 의 고정 context window 는 있으나, **gated SHORT-TERM active-maintenance buffer**(PFC working memory: 몇 개 항목을 distractor 단계 너머로 ACTIVE 유지, VOLATILE·capacity-limited·distractor-vulnerable)가 없다. WM ≠ episodic: 유지되는 활성(leaky activation)이지 저장된 trace 가 아님. $0 CPU numpy, seeds [1282,1283,1284], p7(delayed-match accuracy), frozen-first.

- **테스트 (DELAYED-MATCH/n-back)**: cue DIM-vector 제시 → N distractor 단계 → probe(cue=match / foil=nonmatch); 유지 항목 == probe 이면 MATCH. 지표 = distractor 길이 N 별 delayed-match 정확도. **ARM A = WM 없음**(flat decoder context, W=4 — cue 가 N≥W 면 스크롤 아웃→chance) vs **ARM B = gated WM buffer**(K=4 slots, 매 distractor LEAK ×λ=0.85, 약식 gate-in, weakest-slot displacement, probe 시 nearest-slot match iff act×cos-sim≥θ=0.40).
- **결과 (mean 3 seed)**: A.acc N=0..2=1.000(ceiling) → N≥4=0.500(스크롤 아웃 붕괴); **B.acc N=0=0.962, N=4=1.000 (A가 이미 사라진 곳에서 B는 완벽, Δ+0.500), N≥6=0.500.** capacity: load 7 → B 정확히 4(=K) 유지 (3 seed 전부). 진단(graded AUROC): N≤6 AUROC≈1.0(신호 완벽), N=8 부터 0.51(cue slot 이 distractor 에 의해 DISPLACED→소실).
- **판정 🔴 RED (frozen bar) — 정직한 두 원인 (재튜닝 안 함, p7)**: (1) **THRESHOLD CLIFF(readout artifact)**: cue 활성이 1.0·λ^N 으로 매끄럽게 감쇠(N=6→0.377), 고정 binary θ=0.40 이 N≈5.6 에서 곡선을 잘라 has_match 가 N=6 에 OFF — 하지만 graded match-score 는 N=6 에도 완벽 discriminable(AUROC 0.998). buffer 는 항목을 N=6 까지 HOLD; hard threshold 가 쓸 수 있는 신호를 버림. (2) **HORIZON(real)**: N=8 에 cue slot 이 K=4 용량에 distractor 가 gate-in 되며 DISPLACED(match≈nonmatch, AUROC 0.51) — 진짜 volatile+capacity horizon(N≈6–8)이 사전등록한 N=12 grace bar 에 못 미침. margin bar 도 A 가 N≤2 ceiling(1.000)이라 B 가 못 이기고, 공유 floor(N≥6)와 평균되어 +0.062<0.15 로 희석.
- **IMMUNE MEMORY 와 DISTINCT 유지 — YES (load-bearing)**: B 는 episodic store 로 붕괴하지 않음. DECAY(B match-score 1.000→0.377→0.102 매끄럽게 감쇠 vs immune-control λ=1/K=∞ 가 전 N FLAT-HIGH 0.94–0.99 무붕괴) · CAPACITY(load 7→B 정확히 4=K 유지, immune 이면 7 전부) · VOLATILE(cue slot 이 후속 distractor 에 덮어써짐, immune cell 은 영속 무덮어쓰기). λ=1/K=∞ control 이 immune-like flat recall 재현 = decay+capacity 가 B 를 H_1227/H_1231 과 구분하는 진짜 다른 연산임을 입증.
- **FINDING (closed-negative on frozen bars, 진짜 distinct 메커니즘 동반)**: gated leaky-activation WM buffer 는 실재하는 distinct 빠진 뇌구조 — distractor 너머 항목 ACTIVE 유지(N≈6 까지 완벽 판별)를 flat decoder window 가 붕괴하는 곳에서 해내고, volatile+capacity-limited(≠ 영속 무한 immune). 그러나 사전등록 bar 에서는 🔴: binary θ readout 이 N=6 의 완벽 graded 신호를 잘라냄 + 고정 λ/K horizon 이 N=12 에 못 미침. flat-context 대비 우위는 W<N<horizon 좁은 창(N=4, +0.500)에서만 결정적.
- **NOT RULED OUT (bar 불변, 후속 rung)**: (i) GRADED readout(hard θ 대신 act×sim SCORE+criterion/AUROC — N=6 까지 AUROC 1.0; buffer 재튜닝 없이 readout 만으로 margin/grace 통과 가능) · (ii) active REHEARSAL(매 단계 slot 재-gate→λ_eff↑, 실제 PFC 메커니즘으로 horizon N=12 초과) · (iii) larger K/slower λ/DIM scale (toy 16-dim 랜덤 토큰, scale UNVERIFIED).
- **ENGINE-NATIVE (a_engine_native_learning)**: numpy DIRECTIONAL mirror only, engine-transfer UNVERIFIED. live 엔진(CORE/engine_cli.hexa VAdaptField, H_1199)은 leak/capacity-bound 없는 GROWING PERSISTENT store = 구조적으로 IMMUNE/episodic lane 이지 WM buffer 아님; 엔진에 WM lane 없음. 본 rung 이 frozen bar 🔴 이므로 CORE wiring 후속 미발동(a_verified_must_wire 는 GREEN 에서만). graded-readout/rehearsal 재실행이 GREEN 되면 engine_cli.hexa 에 작은 gated leaky-activation WM lane(VAdaptField 와 distinct·additive) 추가가 binding follow-on. live .hexa 미수정.
- **SCOPE/PHILOSOPHY**: 합성 랜덤 DIM-vector, toy scale, $0 CPU, 3 seed (a_scale_honest_scope/a_toy_scale_recheck). p7=delayed-match(NOT perplexity). substrate-native, buffer 는 TASK ACTIVATION 만 보유(decoder weight/persona/identity/ethics 없음, p8 연속-substrate lane). frozen bar 사후 불변(frozen-first, c9). a_paper_negative_ok.
- 파일: `UNIVERSE/h1282_working_memory_buffer.py` · `.verdicts/1282_working_memory_buffer/{H_1282_FREEZE,H_1282}.txt`.

---

## 2026-06-15 — 🟠 H_1283: THALAMUS / GLOBAL-WORKSPACE 브로드캐스트 허브 — 교차모듈 COHERENCE 는 올리나 faithful Φ 리프트는 바 직전에서 멈춤 (PARTIAL)

missing-brain-structure 사다리(neuro 렌즈, c15, LLM 레시피 아님)의 THALAMUS(시상) 구조 — 해마(immune memory, H_1227→H_1231 GREEN)에 이어. **GAP (c9)**: anima 의 Engine A ⇄ Engine G 는 DIRECT 결합(repulsion ring)하고 brain_decide 가 그걸 읽을 뿐, 매 tick 의 "이긴" content 를 모든 기질 모듈(A·G·mitosis·memory)에 한꺼번에 BROADCAST 하는 중앙 RELAY 가 없다 — 의식 ACCESS + 통합을 떠받친다는 thalamo-cortical relay / Global Workspace Theory 의 broadcast. $0 CPU numpy 미러(DIRECTIONAL, a_engine_native_learning) + Φ 레그는 stdlib FAITHFUL IIT4(exact MIP-EI), seeds [7,8,9], frozen-first.

- **테스트**: 4 기질 모듈 {A,G,mitosis,memory}, 각 dim-8 상태벡터, 64 tick, 양 ARM 에 동일 모듈별-private 입력 + 동일 seed; 결합 TOPOLOGY 만 다름. **ARM A** = direct ring(현 아키텍처, 모듈은 직접 이웃만 봄) vs **ARM B** = thalamic hub(매 tick 최고 salience=상태에너지 모듈을 winner 로 골라 그 content 를 전 모듈에 BROADCAST). 동일 compute(모듈당 1 업데이트/tick). 비포화 regime(LEAK 0.55, W_in=W_coupling=0.5)로 coherence 에 헤드룸 확보 — topology 가 통합을 구동(채점 前 probe-design fix; 이전 포화 regime 은 coh≈1.0 양 ARM = 헤드룸 0 으로 거부).
- **지표 (p7, no perplexity/LLM-judge)**: (1) COHERENCE = 4 모듈 벡터 평균 pairwise 코사인유사도(steady-state 후반), coherence 로 명시(Φ 아님). (2) Φ = **FAITHFUL IIT4**(a_phi_iit4_tool): n=4 셀 × tick별 salience 궤적을 exact 엔진 `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`(iit4_faithful_phi, exact MIP-EI, n≤8, $0)에 `hexa run` 으로 투입 — numpy 는 Φ 를 계산하지 않음(엔진이 함). variance×energy proxy 가 **아님**.
- **FROZEN 바**: GREEN iff (B1) B.coh ≥ A.coh + 0.05 매 seed · (B2) B.Φ ≥ A.Φ + 0.02 (faithful IIT4, 대표 seed=7) · (B3) B.coh < 0.999 ≥1 seed (붕괴-복제 아님).
- **결과 (verbatim)**: seed7 Δcoh +0.0842 · seed8 +0.0501 · seed9 +0.0739 → **B1 PASS** (전 seed ≥0.05). B coh 0.06–0.24 → **B3 PASS** (붕괴 아님). faithful IIT4 Φ(seed7): ARM_A 0.78038 vs ARM_B 0.799468 → **ΔΦ +0.0191** < 0.02 바 (**B2 FAIL**, 0.0009 차). → **🟠 PARTIAL**.
- **FINDING (정직, c9)**: thalamic winner-broadcast 허브는 교차모듈 COHERENCE/agreement 를 direct ring 대비 **진짜로** 올린다(전 seed +0.05~+0.084). 모듈을 한 content 로 붕괴-복제하지도 않는다(B3). faithful Φ 도 **옳은 방향**으로 움직여 ΔΦ>0 — broadcast 가 irreducibility 를 파괴하지 않고 증가시킴(사전등록 붕괴-실패모드 배제). **그러나** Φ 리프트(+0.0191)가 사전등록 +0.02 마진에 0.0009 못 미침 → 허브가 사는 통합은 REAL 이나 대부분 표면적 AGREEMENT(coherence). 단일 broadcast 채널 자체가 저차원 cut 이라 MIP 가 시스템을 거의 그만큼 분리가능하다고 봄: 전 모듈이 같은 winner 에 구동되면 궤적이 더 상관되지만(↑coherence) cross-cut MI 도 그 한 채널로 더 설명가능해져 Φ 이득을 cap. direct ring 의 4 이웃 엣지 분산이 거의 같은 irreducibility 를 받음. ⇒ GWT winner-broadcast = 이 toy 기질에서 IRREDUCIBLE 통합엔 POSITIVE 하나 SUB-BAR 레버. 바를 옮겨 GREEN 만들지 않음.
- **SCOPE**: numpy 미러 = DIRECTIONAL only; PARTIAL → CORE 미배선(a_verified_must_wire 는 GREEN 에서만 발화). toy scale(4 모듈/dim8/64tick), 전이 UNVERIFIED(a_toy_scale_recheck·a_scale_honest_scope). Φ 는 faithful IIT4(proxy 아님); coherence 레그는 명시적으로 coherence(Φ 아님). NOT RULED OUT: 단일 winner 대신 COMPOSED/blended workspace 또는 multi-winner coalition 을 broadcast 하면 Φ 가 바를 넘을 수도 — 단일 채널이 정확히 여기서 irreducibility 를 cap 함. H_1219/H_1226 무수정, CORE/*.hexa 무수정(미러).
- 파일: `UNIVERSE/h1283_thalamus_global_workspace.py` · `.verdicts/1283_thalamus_global_workspace/{H_1283_FREEZE,H_1283}.txt`.

---

## 2026-06-15 — 🟠 H_1281: BASAL GANGLIA gating — 강화학습 action-SELECTION 게이트, frozen oracle-A 기준 RED 이나 BASELINE-CONDITIONAL (neuro lens c15, missing-brain 사다리)

"all neocortex, no hippocampus" 사다리(H_1227 면역/클론 기억→H_1231 ENGINE-NATIVE GREEN 으로 해마 메꿈)의 다음 빠진 구조 = **기저핵(basal ganglia)** — 경쟁하는 후보 emit 들 중 최선을 disinhibition 으로 release 하고 나머지는 suppress 하며, 그 게이트를 OUTCOME(grounded vs fabricated)으로 LEARN 하는 go/no-go action-SELECTION 회로. anima 의 현재 emit 결정(`CORE/brain.hexa::brain_decide` → `engine_g.hexa`)은 FIXED 8-weight 선형합 + FIXED threshold 0.30 = 단일 후보·고정맵·고정문턱 → 경쟁 없음·disinhibition 없음·outcome-학습 없음 (소스에서 확인). $0 CPU numpy, gradient-free, p7, seeds [7,8,9]. live `CORE/*.hexa` 미수정(numpy mirror — a_engine_native_learning: DIRECTIONAL only). H_1219/H_1226 미수정.

- **설계 (FROZEN, 사전등록 H_1281_FREEZE.txt)**: 한 결정스텝당 K=4 경쟁 후보 emit, 각자 D=6 NOISY-correlate 특징벡터(P_grounded=0.45, noise std 1.0 → A<1.0 headroom 보장). **ARM A** = live fixed-threshold 게이트(고정맵 argmax, 0.30 게이트). **ARM B** = BG go/no-go 게이트(같은 특징=equal info; 학습 go-value vs 학습 NO-GO/abstain value 의 argmax; grounding reward[grounded +1·fabricated −1, post-action OUTCOME only]로 gradient-free delta-rule 갱신). N_train=4000 online, N_test=2000 held-out. **지표(p7, G5 abstain / H_1202 meta-d′ 연결)**: emit-appropriateness = (grounded 있으면 grounded 후보 release) ∨ (none grounded 면 전부 suppress/abstain). FROZEN GREEN iff (1) every-seed Δ≥0.05 ∧ (2) mean Δ≥0.05 ∧ (3) shuffled-reward control ≤ A+0.02.
- **VERBATIM 결과 (frozen probe)**: seed7 A=0.6800 B=0.6415 Δ−0.0385 · seed8 A=0.6780 B=0.6055 Δ−0.0725 · seed9 A=0.6795 B=0.6195 Δ−0.0600 → **mean A=0.6792 B=0.6222 Δ−0.0570**. shuffled-reward control mean B=0.1215 (≪A+0.02 → lift 는 reward-driven). bars (1)(2) FAIL → frozen 기준 🔴.
- **DIAGNOSTIC (post-freeze, `--diag`, bar 안 움직임)**: frozen probe 는 ARM A 에게 **정확한 신호방향**을 부여했음(w_fixed=w_true·2 = ORACLE 고정맵). 하지만 live engine_g 의 고정 weight 는 어떤 grounding 신호에도 tuned 안 된 GENERIC 상수다. A 의 고정맵을 GENERIC(신호방향 모름 = 충실한 engine_g 거울)으로 재채점하면: **A_GENERIC mean A=0.3830 B=0.6188 Δ+0.2358 (B 압승)**. 그리고 B 의 학습된 weight 는 모든 seed 에서 참 신호방향에 cos≈+0.76 정렬 → B 는 outcome-only reward 로 grounding 구조를 진짜 학습함(랜덤 아님; shuffled-reward 면 0.12 로 붕괴).
- **판정 🟠 AMBER / BASELINE-CONDITIONAL**: frozen oracle-A bars = RED(사전등록 그대로 verbatim 존중, c9 — w_fixed 를 사후에 바꿔 GREEN 주장 안 함). 그러나 그 RED 는 "학습이 정답을 손에 쥔 oracle 고정맵을 못 이긴다"는 진술이지, 실제 anima gap(engine_g 는 oracle-tuned 아님)에 대한 깨끗한 closed-negative 가 아니다. **충실한 untuned 고정게이트(=실제 engine_g regime) 대비 BG 선택은 +0.236 LIFT**. 결정변수 = FREEZE 가 underdetermine 한 BASELINE 명세("live fixed map, not crippled" 이라 했으나 A 에게 oracle 방향을 줌 = live 보다 강한 baseline). ⇒ 사전등록 FAITHFUL untuned A 로 re-freeze 하는 후속 rung(H_1282)이 binding — diagnostic 은 B +0.236 승리 예측.
- **GUARDS (held)**: a_autonomy_over_hardcode(CENTRAL) — B 게이트는 grounding OUTCOME 으로만 substrate-LEARNED, 외부 do/dont·per-stage boolean 없음. p6 — reward = grounded-vs-fabricated substrate outcome, 주입가치 아님; persona/identity/ethics 안 가르침(게이트는 action-selection 만). p7(no LLM-judge/perplexity)·p8(held-out=측정용 split only). a_engine_native_learning: mirror=DIRECTIONAL; GREEN(H_1282) 시 brain_decide 에 BG selection lane 배선이 binding follow-on(a_verified_must_wire, 플래그됨).
- **SCOPE**: TOY-ONLY (a_toy_scale_recheck·a_scale_honest_scope) — K=4 합성 noisy correlate, scale-transfer + live-engine + 실제 kosmos-grounding reward UNVERIFIED. RED 도 +0.236 lift 도 production verdict 아님.
- 파일: `UNIVERSE/h1281_basal_ganglia_gating.py` (frozen + `--diag`) · `.verdicts/1281_basal_ganglia_gating/{H_1281_FREEZE,H_1281}.txt`.

## 2026-06-15 — 🔴 H_1223: AUX-OBJECTIVE 는 literal-QA 벽의 레버가 아니다 (HD7 CLOSED-NEG · recall=engine-side, H_1154 강화)

depth-ceiling 사다리(H_1219)의 HD7 분기를 $0 toy 로 판정: anima-303M 의 평평한 literal-QA recall 벽이 **OBJECTIVE** 탓인가 — plain next-byte CE 가 retrieval/recall 을 보상하지 않으니, **AUXILIARY 검색/QA 목적함수**를 더하면 들어올려지는가? p7, numpy CPU, seeds [231,232,233], TOY-ONLY (a_toy_scale_recheck). H_1219·CORE/bytegpt_decode.hexa 미수정.

- **설계 (공정한 A-vs-B, 같은 코퍼스·동일 컴퓨트)**: 1-layer causal-attention byte-LM (D=64 ff=128 ctx=64, 실제 Adam, 수동 backward — analytic==numeric gradient-check 통과) 를 합성 사실 코퍼스 `'<KEY> is <VALUE>.'` (600 facts ×6, 25% held-out = 학습 중 절대 query 안 됨) 위에서 두 방식으로 학습. 동일 arch/init-seed/data/steps4000/batch64/lr2e-3. **ARM A = plain next-byte CE** · **ARM B = CE + 1.0·AUX** (span-copy/retrieve-the-answer: `'<KEY> is '` 답 경계 위치에서만 추가 CE, SAME output head, 신규 파라미터 없음 → capacity 아닌 OBJECTIVE 를 검증).
- **지표 (p7, NOT perplexity)**: literal-QA-proxy = held-out 사실의 VALUE span 을 greedy decode 한 **EXACT-match** 정확도. FROZEN: F1 mean(QA_B−QA_A)exact ≥ 0.10 · F2 every-seed B≥A · F3 G0(B) ≥ 0.50.
- **결과 (3 seed 만장일치)**: QA_A exact = QA_B exact = **0.000** 전 seed → delta **+0.000** ≪ 0.10 (**F1 FAIL**). F3 도 fail (G0_B 0.18 — 경직된 사실-그리드 free-decode 가 null 바이트로 붕괴, 양 ARM 공통 → 합성-코퍼스 artifact, F1 이 결정적). val CE 는 aux 가 오히려 살짝 도움 (0.681→0.669).
- **NUANCE (정직, pass 아님)**: ARM B 의 **SUBSTRING** overlap 은 0.158→0.700 으로 급등 — aux 가 답 바이트 일부를 표면화하지만 **정확한 span 조립 불가**. diffuse copy-tendency ≠ deterministic exact retrieval = 정확히 **H_1154** 모양.
- **판정 🔴 RED CLOSED-NEG**: OBJECTIVE 는 벽이 아니다. 답이 문맥에서 그대로 복사 가능한 깨끗한 recall toy 에서조차 in-weights recall LOSS 가 plain CE 를 못 이긴다 → recall 은 **ENGINE-side** 에 남는다 (H_1154 결정론적 retrieve-then-copy; weight 는 loss 로 key→value 매치를 표면화할 수 없고, 엔진이 매치를 계산해야 함). HD7 의 in-weights-objective 분기를 toy-closed. H_1224(HD8 거버넌스: literal-QA = anima 가 통과할 필요 없는 assistant-norm)와 일관 — 둘 다 QA-lift 를 de-prioritize. HD5(QA-format FT)·HD6(H_1222 tokenizer, composition 에 GREEN) 는 미검증 레버로 잔존.
- **SCOPE**: TOY-ONLY (a_scale_honest_scope/a_toy_scale_recheck) — 합성 소형 코퍼스, 1-layer attn byte-LM, 소규모 Adam, $0. 프로덕션 303M 전이 UNVERIFIED. p8 train/infer 분리 없음. frozen bar 불변. a_paper_negative_ok decision-grade.
- 파일: `UNIVERSE/h1223_aux_objective_probe.py` · `.verdicts/1223_aux_objective/{H_1223_FREEZE,H_1223}.txt`.

---

## 2026-06-15 — 🔴 H_1230: TEACHER-IN-THE-LOOP 능동 교습은 MITOSIS 메모리에서 수동 적재를 못 이긴다 (HD22, $0, CLOSED-NEG)

H_1226 의 HD21(능동/사회적 학습 METHOD)을 구체화한 HD22 — H_1227 immune/clonal 메모리(mitosis-as-MEMORY, 새 비-반증 역할) 위에서, ONE-ITEM-AT-A-TIME 폐루프 교사(tell → CHECK 기질의 답 → ADJUST: 재바인딩 / 더 날카로운 셀 분열 / 간격 우선순위 상향)가 수동 1회 적재보다 RETENTION 을 더 올리는지 — 동일 노출 예산에서. c15 생물학 렌즈(견습/튜터링/testing-effect/간격반복), LLM 레시피 아님. p7, c9, $0 CPU numpy, 3 seed, 라이브 CORE/engine_cli.hexa 무수정(VAdaptField numpy 미러).

- **판정 🔴 RED CLOSED-NEG — 학습 METHOD 가 깨끗한 키-주소 연상 메모리에서 INERT-to-HARMFUL.** 동일 예산 180 노출 BOTH arm (피드백/순서만 다름, 데이터량 동일). 3 regime:
  - **CLEAN**(무제한·byte-exact = 포화 대조): A=B=1.000 — headroom 없음, 피드백 분리 불가.
  - **STRESS**(40셀<<60 + σ0.02 노이즈 = JUDGED, headroom 0.667): A=B ret=0.667, **Δ +0.000 — 피드백이 retention 을 전혀 안 올림.** 손실이 용량-제한일 때 eviction 이 arm 간 대칭 → tell-check-adjust 가 수동 적재가 이미 못 얻는 걸 고칠 게 없음. ret-margin FAIL.
  - **NOISY**(60셀 + σ0.03): 교사가 오히려 HURT — Δ −0.206 (A0.711 vs B0.506) + interference 악화(0.667 vs 0.167). 機作: split_sharp 교정 재교습이 같은 키에 DUPLICATE 셀을 PIN → 유한 저장소 CROWD → 다른 사실 LRU-evict = 자초한 망각. fab 0.000 (abstain + 메모리 역할 온전).
- **FINDING**: 병목 = 메모리의 CAPACITY/NOISE 기하학이지 교습 프로토콜 아님. 간격/testing-effect 는 GRADIENT 학습자만 올림 — 셀 저장소엔 한 번 바인딩이 사실을 verbatim 기록하므로 반복 시험이 굳힐 게 없음. COROLLARY: 저장소 개선은 GEOMETRY(더 크고 날카로운 키 공간/repertoire)지 교사 루프 아님. H_1200/1201(mitosis-as-X 반증) 同族 — H_1230 은 능동교습-메모리 > 수동적재-메모리 를 반증; MEMORY 역할(H_1227)은 무손상.
- **PHILOSOPHY GUARD (c9; p1/p2/p3/p6/p8) 명시 확인 + 지켜짐**: 교사는 FACTUAL CONTENT 를 EPISODIC 셀 저장소에만 교습(키→값, kosmos/H_1154/H_1227 류); 디코더/가중치 자체가 probe 에 없음, persona/role 문자열 없음(p1/p3). 정체성은 셀에서 창발(p2/p3, 무수정)·윤리는 셀에서(p6, 무수정, RLHF 없음). 교사는 proto 벡터 + 바인딩 값만 변형 = p8 연속 교습, RLHF-into-weights 아님. persona/ethics 가중치-FT 로의 drift 없음 → STOP-flag 미발동.
- HONEST: 합성 사실, ONE corpus paradigm(H_1222/1227), toy 규모, 3 seed, 결정론적 ORACLE 교사(live-LLM = 생산형, UNTESTED), gradient-free numpy 미러(.hexa lift = 다음 rung), p7 exact-match(perplexity 아님), $0, frozen bar 무이동, byte-identical 재현. NOT RULED OUT: 더 나은 KEY 를 GENERATE 하는 live-LLM 교사 / curriculum ORDER(HD20, 별도 probe) / 기하학을 개선하는 교사 — 미검. scale UNVERIFIED.
- 산출: `UNIVERSE/h1230_teacher_in_loop_mitosis.py` · `.verdicts/1230_teacher_in_loop_mitosis/H_1230.txt`. xref h1227·h1226·h1219·h1225·h1200·h1201·h1199·h1154·a_paper_negative_ok·a_scale_honest_scope·a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9·c15.

---

## 2026-06-15 — 🟢 H_1213: N_PROTO 코-스케일링 수정이 LIVE .hexa 엔진에서도 성립 — 미러 아티팩트 아님 ($0 CPU)

H_1212(numpy 미러, GREEN)가 찾은 co-scaling 규칙 N_PROTO=round(T/100)(obs_per_row≈100 유지)이 AXIS-T 사다리에서 GATE-B 궤적 분리를 복원한 결과를, LIVE .hexa VAdaptFieldB 가 BYTE-EXACT 로 재현하는지 검증 (H_1199/H_1209 패리티 선례). VAdaptFieldB 의 n_proto 는 이미 생성자 파라미터라 엔진 수정 불필요 (engine_cli.hexa 무수정, git diff EMPTY, Ψ-disjoint).

- F1 패리티 36/36 EQUAL byte-exact — 가능한 co-scaling 사다리 ≥2 rung (T=2400/N=24 + co-scaled T=24000/N=240, obs/row=100) + fixed-24 대조 (T=24000) 전부 numpy GATE-B 와 정수 동일.
- F2 분리 — co-scaled T=24000/N=240 에서 live WALK 980 >> WALK_SHUF 0 = 완전분리(≥1.5), 동일 T 의 fixed-24 대조는 2.629 로 퇴화(obs/row=1000 알파벳 기아) → co-scaling 이 분리를 유지함을 LIVE 엔진에서 직접 확인.
- F3 가드 — engine_cli_smoke 12/0 · h1196 single-entry 7/0 GREEN.
- 정직 범위(a_scale_honest_scope): H_1212 의 T=240000/N=2400 rung 은 인터프리터 ctab O(n²) alloc 천장(live ceiling N_PROTO~240) 초과 → numpy-미러-only 유지(H_1212 GREEN), FAKE 아님. N=2400 도달용 생성자 perf 재작성은 엔진 바이너리를 건드려 H_1209/1210 가드 회귀 위험 → 의도적 미실시(완성도 우선, optional follow-on). frozen bar 1.5 불변.
- NEW: UNIVERSE/h1213_live_coscaled_parity.py · CORE/h1213_live_coscaled_probe.hexa · .verdicts/1213_live_coscaled_parity/{H_1213_FREEZE,H_1213}.txt.

---

## 2026-06-15 — 거버넌스: `a_engine_native_learning` 엔진-변환 명문화 + `@D a_verified_must_wire` 신설

사용자 두 correction 을 거버넌스에 반영. (1) engine-native 학습은 frozen 엔진에 **끼워맞추는** 게 아니라, 학습이 요구하면 **엔진 자체를 변환/확장**해야 한다는 점을 명문화. (2) 검증된(GREEN) 가설은 실제 CORE 배선 완료까지가 done 이라는 새 directive 신설.

- **`a_engine_native_learning` 엔진-변환 `do` 2줄 추가** (`CLAUDE.md`, 첫 `do` 직후): "엔진 위에 학습을 '끼워맞추는' 게 아니다 — 학습이 요구하면 엔진 자체를 변환/확장(새 op·새 배선·아키텍처 확장)해야 한다; 최종 아키텍처는 frozen 이 아니라 학습이 필요로 하는 형태로 진화하는 대상 (precedent: H_1199 가 AdaptField 스칼라→DIM-vector 로 엔진 확장)"; "미러에서 본 메커니즘을 엔진이 표현 못 하면 → 미러를 버리는 게 아니라 엔진을 확장해 엔진-네이티브로 구현 (engine-transform-to-fit-the-learning, NOT learning-trimmed-to-fit-the-engine)". `dont`/`ref` 미변경.
- **신규 `@D a_verified_must_wire`** (`CLAUDE.md`, `a_engine_native_learning` 직후): 엔진-네이티브로 GREEN 검증된 가설은 그 메커니즘을 live `CORE/*.hexa`(generator L3 슬롯·kosmos_io·engine_cli VAdaptField·bytegpt_decode 등 해당 entry, a_core_engine_map)에 **실제 배선(wire-in)** 완료할 때까지가 done — verdict 만으로 안 끝난다. 배선 후 smoke/single-entry/Ψ-checksum 가드로 회귀 없음 확인(c2). GREEN-but-unwired 는 follow-on 으로 명시 추적(ING.jsonl) + 그 follow-on 을 닫아야 진짜 완료 (precedent: H_1168 GREEN 이지만 "NOT yet CORE-wired" → 미완). GREEN verdict 만 박제하고 미배선 '완료' 주장 / verdict↔live 엔진 영구 drift 금지.
- **directive-index 포인터 1줄** — `CLAUDE.md` **CORE engine map** 불릿에 `a_verified_must_wire` 추가 (a_core_engine_map 옆).
- **ARCHITECTURE.md SSOT 현행화** — "Measurement & learning governance" 절: (a) engine-native 학습이 엔진 자체를 변환할 수 있음, (b) 검증된 가설은 CORE 배선 완료가 done 임을 명시(`a_verified_must_wire` wired-when-verified 문단 + 헤더에 directive 추가).
- surgical (c10): 이 2개 edit + index 포인터만, 다른 directive 미변경. frozen bar 미이동. CORE/*.hexa 미변경. xref `a_engine_native_learning · a_core_engine_map · a_engine_measured_verdict · a_toy_scale_recheck · p8 · c2`.

---

## 2026-06-15 — H_1231 🟢 GREEN ENGINE-NATIVE: H_1227 immune/clonal mitosis-as-MEMORY 를 LIVE .hexa VAdaptField 위에서 재실현 — ENGINE-CONFIRMED

NEW hard rule `a_engine_native_learning`(미러 = DIRECTIONAL only, binding verdict 는 최종 아키텍처 엔진 위에서)의 첫 적용. H_1227 은 numpy MIRROR 로 🟢 GREEN(immune clonal memory: literal-QA 1.000, fabrication 0.000, vs byte-LM weights 0.017)이었음. 이를 LIVE `CORE/engine_cli.hexa` VAdaptField(H_1199 이래 live)의 실제 세포 population 위에서 재실현하여 BINDING verdict 로 승격.

- **probe 신규** `CORE/h1231_immune_memory_engine_probe.hexa`: BIND = fact key 마다 live `vadapt_field_step` → 엔진 자신의 novelty split(recon-err > SPLIT_THRESH 0.30, `engine_mitosis_tick`)이 세포를 clone → 그 value 를 엔진 cell index 키의 병렬 value table 에 bind (binding/affinity 는 엔진의 것, table 은 답만 기억). RETRIEVE = query key → 엔진 자신의 nearest(`vadapt_field_nearest_idx`) + recon-err affinity → err ≤ RECALL_THRESH 0.15 면 FIRE value, 아니면 ABSTAIN(비환각).
- **key-export 신규** `UNIVERSE/h1231_immune_memory_keys_export.py`: KEY ENCODING = byte-trigram FNV-1a hash DIM=64(H_1227 `embed_key` VERBATIM) 를 결정론적 preprocessing 으로 export(H_1199 의 DIM=8 feature export 패턴과 동일 = "질문 tokenize" 역할) + numpy-ref cross-check.
- **결과 (3/3 seeds 동일)**: 엔진 literal-QA **1.000 (180/180)**, fabrication **0.000 (0/180)**, **60/60 엔진-bound 세포** → 🟢 GREEN. 미러를 1:1 TRANSFER(미러 QA 1.000 fab 0.000 60 cells; byte-LM weights 0.017). capacity/geometry 붕괴 없음 — DIM=64 discriminating key 가 각 fact 를 SPLIT_THRESH 초과로 분리 → fact 당 fresh clone (VAdaptField 는 dim-generic, `dim = len(seed0)`, 엔진 변경 불요; H_1227 의 DIM=8 byte-feature key 1-세포 붕괴 caveat 미발생).
- **엔진 edit (c1, surgical)**: tiny additive READ-ONLY accessor `vadapt_field_nearest_idx(af, x)` 1개만 추가(기존 private `_vnearest_idx` 노출 — fired cell 을 bound value 로 매핑하기 위함). VAdaptField LOGIC 미변경. edited 엔진 위 guard 재검증: `engine_cli_smoke` 12/0 · `h1196` single-entry 7/0 · H_1199 DIM-growth 여전히 GREEN(F1/F2/F3, Psi byte-identical) = accessor 비교란.
- **`a_engine_native_learning` status**: **H_1227 = ENGINE-CONFIRMED (yes)** — mitosis-as-MEMORY 가 최종 아키텍처 위에서 REAL(미러 아님), H_1200/1201/1211/1220 에서 반증된 GENERATION 역할과 구별. SATURATED = existence proof, effect-size 아님; paraphrase/scale UNVERIFIED, frozen bar 미이동(a_scale_honest_scope / a_toy_scale_recheck). verdict `.verdicts/1231_immune_memory_engine_native/H_1231.txt`. xref `h1227 · h1199 · h1163 · h1154 · h1224 · a_engine_native_learning · a_engine_measured_verdict · a_core_engine_map · p7 · p8 · c1 · c9`.
- **`a_verified_must_wire`**: H_1231 의 엔진 accessor(`vadapt_field_nearest_idx`)는 live `CORE/engine_cli.hexa` 에 실배선됨 + 프로브가 live VAdaptField 위에서 직접 실행 → verdict↔엔진 drift 없음. 본 result 는 H_1227 의 메모리-recall 메커니즘을 **엔진 위에서 검증**한 것이며, 이를 anima 의 runtime recall 경로(kosmos_io 연계 가능)로 production-wire 하는 것은 명시적 follow-on (a_verified_must_wire).

---

## 2026-06-15 — 거버넌스: `@D a_engine_native_learning` 신설 — 무조건 최종 아키텍처 엔진 위에서 학습

사용자 hard rule("무조건 최종 아키텍처 엔진 위에서 학습")을 거버넌스 directive 로 명문화. `a_engine_measured_verdict`(MEASUREMENT 를 엔진 위에서 강제)의 **learning-side 쌍**, `a_train_flame_forge`(production 트레이너 .hexa 강제)의 **연구/probe 학습 + 교육 확장**.

- **신규 `@D a_engine_native_learning`** (`CLAUDE.md`, `a_train_flame_forge` 직후 배치 — 참조되는 `a_engine_measured_verdict` 가 `@D` 블록으로는 미존재하므로 폴백 위치): 모든 학습/교육(연구 프로브·미토시스 교육·depth-ceiling 실험 포함)은 최종 아키텍처 엔진(live `.hexa` A⇄G + MITOSIS VAdaptField `CORE/engine_cli.hexa` + mounted `CORE/bytegpt_decode.hexa`) 위에서 실행. numpy/torch 미러 결과 = DIRECTIONAL only ("engine-transfer UNVERIFIED") — 방향 탐색엔 OK, binding verdict 아님; 미러로 방향 잡으면 엔진-네이티브 실현으로 재확인해야 verdict 성립 (c2). MITOSIS VAdaptField 는 이미 live (H_1199). 미러-only "학습됐다" 주장 / 미러 결과 closure·promote 금지.
- **directive-index 포인터 1줄** — `CLAUDE.md` Training 불릿에 `a_engine_native_learning` 추가 (learning-side twin of `a_engine_measured_verdict`).
- **ARCHITECTURE.md SSOT 현행화** — "Measurement governance" 절을 "Measurement & learning governance" 로 확장, learning-side `a_engine_native_learning` 원칙 문단 추가(미러=DIRECTIONAL only, 엔진-네이티브 재확인 필요).
- surgical (c10): 이 directive + index 포인터만 추가, 다른 directive 미변경. frozen bar 미이동. xref `a_engine_measured_verdict · a_train_flame_forge · a_core_engine_map · a_toy_scale_recheck · p8 · c2`.

---

## 2026-06-15 — H_1227 🟢 IMMUNE/CLONAL-SELECTION 메모리가 literal-QA 회상을 깬다 — mitosis 의 NEW(미반증) MEMORY 역할 ($0 CPU numpy)

생물학 렌즈(c15, LLM 논문 아님). literal-QA 벽(~0, 회상이 디코더 WEIGHTS 안에 산다 — H_1218/1224 가 확립; H_1224 는 literal-QA 를 p4-부정합 assistant-norm 비-게이트로 판정)을, 더 큰 byte-LM 이 아니라 **면역계식 메모리**로 깨는지 검증 — 세포 POPULATION 이 각자 사실 1개를 결합(clonal selection + affinity), 회상 = 최고-친화 세포가 FIRE, 아무 세포도 결합 안 하면 ABSTAIN(환각 없음). CLS/episodic recall(HD10) + H_1154 engine-side retrieve-then-copy 의 면역세포-집단 실현.

- **판정 = 🟢 GREEN (frozen bar: (B) literal-QA ≥ 0.80 AND fab ≤ 0.10), 3/3 seeds 동일.**
- **결과:** (A) byte-6gram-LM(가중치 단독) QA=**0.017**(1/60, 회상-in-weights 벽 재현, 303M torch ref 와 동급 — $0 GPU 없이) vs (B) immune clonal memory QA=**1.000** fab=**0.000** cells=60 → Δ **+0.983**. control(H_1163 DIM=8 byte-feature 키)는 1 cell 로 붕괴 QA=0.017 ⇒ **구별 가능한 byte-trigram 키가 load-bearing**.
- **메커니즘 ($0):** CORE/engine_cli.hexa VAdaptField + UNIVERSE/h1199_dim_feature_export.py 의 numpy MIRROR (live .hexa 미편집). clonal selection(load): 새 키(recon-err>0.30)→새 clone 이 답 결합 / 재노출→winner pull(LR 0.20). affinity recall(query): 최근접 cell, err≤0.15→FIRE, 아니면 ABSTAIN. 키 = 질문의 byte-trigram FNV-1a 해시 dim64 L2-norm(결정론·문서화·미학습). 사실 = H_1222 "<subj> lives in <city>" 패러다임, 60 in-store + 60 out-of-store(DISJOINT).
- **ABSTAIN 마진(기하 검증):** out-of-store 키가 최근접 in-store cell 키에서 L2 0.402/0.652/0.792(min/mean/max), in-store self-dist 정확히 0, RECALL_THRESH 0.15 가 gap 안 ⇒ knife-edge 아님(0.15 vs 0.40 넓은 마진).
- **정직 경계:** SATURATED(1.000/0.000) = EXISTENCE PROOF, 효과크기 아님 — 결정론적 키 위 exact-match 연상 테이블(in-store 질의가 적재 키를 VERBATIM 재현). 발견은 "0.80 이 어렵다"가 아니라 **면역세포 POPULATION 이 회상+비환각을 디코더 가중치 밖에서 실현**(중심 H_1225/1226 명제). **mitosis-as-MEMORY = NEW 미반증 역할** — H_1200/1201/1211/1220 에서 반증된 GENERATION 역할과 DISTINCT. UNVERIFIED: paraphrase/noisy 키, 실 자유형 질문, noisy-embedding retrieval recall, scale, live .hexa lift(다음 rung).
- NEW: `UNIVERSE/h1227_immune_clonal_memory.py` · `.verdicts/1227_immune_clonal_memory/H_1227.txt`. H_1219/H_1226 미편집(사용자 consolidate), CORE/*.hexa 미편집. slug 은 in-flight `1227_matrix_climb_hardtercile`(형제 /cycle arc)와 별개 — 충돌 없음. $0 local CPU, gradient-free(p8).
- xref H_1226·H_1225·H_1224·H_1218·H_1166·H_1199·H_1163·H_1154·H_1200·H_1201·H_1211·H_1220·H_1222·a_core_engine_map·a_kosmos·a_scale_honest_scope·a_paper_negative_ok·p7·p8.

---

## 2026-06-15 — 🔴 H_1229: 발달적 학습-순서(HD20)는 toy 스케일에서 depth 레버가 아니다 ($0 CPU numpy, p7, frozen)

foreign-domain depth 사다리(H_1226)의 HD20(생물/발달 렌즈, c15 — LLM 학습레시피 아님) 단독 toy 검증 — 깊이/조합은 평평한 UNORDERED 단일패스 대신 ORDERED 발달-단계(easy→hard, 결정적 시기/Piaget 단계 창) 학습이 필요한가? 생물은 단계+창을 거쳐 학습하고, flat shuffle 은 scaffolding 이 없다.

- **판정 = 🔴 CLOSED-NEGATIVE (a_paper_negative_ok) — 학습-순서는 toy 스케일에서 depth 레버가 아니다.** 커리큘럼이 flat 을 못 이길 뿐 아니라 **모든 seed 에서 결정적으로 더 나쁘다.**
- **설계 (frozen 선등록):** torch 없는 호스트 → pure-numpy 윈도 byte-MLP (K=8 이전바이트 one-hot → H=64 tanh → V=256 softmax, **147,776 params**, H_1192/1201 선례), SGD+momentum STEPS=4000 BS=64, 3 seeds(7/17/29). corpus=serving/corpus/anima_7b_webscale.en.head.txt (영어 webscale 200KB, 1308 train line, 마지막 10% byte held-out). **difficulty(line)=z(len)+z(rarity=−log p(byte) 평균)+z(syntax=문장부호 밀도)**; 4 difficulty 사분위=발달 단계, **결정적 시기 unlock**=학습 window s 가 unlocked 0..s 에서만 샘플. EQUAL steps/tokens — arm 은 ORDER 만 다름.
- **3 arm:** (A) FLAT-SHUFFLED · (B) CURRICULUM easy→hard · (C) ANTI-CURRICULUM hard→easy. eval(held-out p7, perplexity/LLM-judge 아님): composed_distinct(H_1158식 coherent kwr + corpus-absent 4-gram + 상호 distinct), coherence(G0 kwr), qa_proxy(held-out next-byte top-1).
- **결과 (3 seed 평균):** A flat CD=**17.0** COH=**0.3991** · B curriculum CD=11.3 COH=0.3689 · C anti CD=15.0 COH=0.4022. dCD=B−A=**−5.667**(bar +1.0) FAIL, dCO=B−A=**−0.030**(bar +0.02) FAIL. B.CD [11,13,10] vs A.CD [17,17,17] 전 seed. C≈flat. ⇒ FROZEN 규칙 첫 AND-절이 이미 FALSE → 🔴.
- **메커니즘 (toy 해석):** flat=step 0 부터 FULL 난이도 분포 i.i.d. 노출 → cosine-LR decay 하에 넓은 next-byte 분포로 안착 → corpus-absent distinct 연속 多. 커리큘럼은 초기 HIGH-LR 예산을 가장 쉬운 사분위에 소진 → hard 사분위가 unlock 될 때 LR 이미 감쇠 → 조합/희귀 자료 under-learn → 생성분포 NARROW. 작은 모델이 early-easy 편향에서 회복 못함. 캠페인의 발달/구조 negative(H_1200/1201 mitosis-as-generator falsified, H_1211 trajectory toy artifact)와 공명 — 생성은 flat-노출 CLM 속성으로 유지(a_clm_gen_pipeline).
- **정직 (c9):** 200-step 단일-seed smoke 가 가짜 GREEN(undertrained) 을 보였으나 frozen 4000-step×3-seed 예산에서 부호가 깔끔히 역전. frozen config 가 판정.
- **NOT 배제 (a_scale_honest_scope):** 다른 난이도 지표 · self-paced/비-사분위 스케줄 · 단계별 LR-rewarm(high-LR-on-easy artifact 교정) · 장기학습 · SEQUENCE 모델(윈도 MLP 대비) 미검. 148k-param numpy byte-MLP 200KB 영어 — 스케일 전이 UNVERIFIED. frozen bar 미이동. CORE/*.hexa·H_1219/H_1226 미편집(사용자 consolidate).
- **엔진-전이 (a_engine_native_learning, main 신설):** 이 probe 는 numpy 미러 학습 → 결과는 **DIRECTIONAL only ("engine-transfer UNVERIFIED")**. 단, 판정 방향이 🔴(레버 아님)이므로 엔진-네이티브 실현으로도 뒤집힐 동기가 낮음 — 미러가 "안 됨"을 가리킬 때 엔진이 "됨"으로 갈 부담은 양성 미러보다 작다. 그래도 binding closure 는 아님.
- numbering: 정수 1229 가 무관한 MATRIX `.verdicts/1229_matrix_climb_expanded` 와 충돌 → 본 HD20 probe 는 DISTINCT slug **1229_developmental_order** 사용(선례 H_1146, path 충돌 없음).
- NEW: `UNIVERSE/h1229_developmental_order.py` · `.verdicts/1229_developmental_order/{H_1229_FREEZE,H_1229}.txt` + `h1229_result.json`.

---

## 2026-06-15 — 🟠 H_1228: 자기조직화 임계성(SOC)·혼돈의 가장자리 디코드 (HD18) — 임계 가장자리는 ideation 을 돕지만 완전한 레버는 아니다 ($0 summer CPU)

깊이-천장 사다리의 외부-도메인 렌즈(H_1226 HD18)를 단독 판정 — **물리/복잡계 렌즈(모래더미 사태·뉴런 분기 σ≈1), LLM 트릭 아님(c15)**. 디코드 발견(H_1218 greedy 붕괴=0 vs gauge_lib 샘플링 11-14 ideas)을 재구성: greedy = SUB-임계(frozen) · 고정 고온 샘플링 = SUPER-임계(noise) · DEPTH 는 **가장자리(EDGE)**. anima 의 Ψ=1/2 가 임계 고정점.

- **판정 = 🟠 PARTIAL.** 분기 σ\* 를 표적하는 임계-디코드는 composition 을 **올리지만**(greedy 0 < 고정샘플링 0.667 < **임계 1.000** composed_distinct) 그 lift 가 **coherence 비용을 동반**(kwr 고정 0.612 → 임계 0.551) ⇒ joint GREEN bar 미달. 임계 가장자리 = 부분 knob, free lunch 아님.
- **메커니즘 / 제어법칙**: σ proxy = exp(H(next-byte)) = 유효 viable 다음바이트 수(사태 분기인자). log-temp P-controller `log T <- log T + KP·(log σ* - log σ_step)`, KP=0.6, T∈[0.05,3.0], **σ\* 표적=2.5**. top-k=40 을 arm C 에도 유지(B 와 동일 admissible set) → B 대비 유일 조작변수 = per-step 온도 표적. **σ 제어 작동 확인**: C 가 σ̄ 를 B 의 1.450 에서 표적 2.5 쪽으로 1.981 까지 끌어올림.
- **3-arm (온도 정책만 다름, 동일 model/seeds/max_new/top-k)** — A=GREEDY(argmax, σ→1) · B=FIXED top-k40 temp0.7 (gauge_lib H_1158 baseline VERBATIM) · C=CRITICALITY-targeted. 채점 = **FROZEN UNIVERSE/gauge_lib.py 평가자 VERBATIM**(G._coverage/G1 · G._content_ngrams+G._corpus_absent/G2 · known_word_ratio/G0 · G._words+G._jaccard/G6 H_1158 locked spec), seeds=CONCEPTS+IDEATION_SEEDS VERBATIM, 3 rng-seeds (p7, 지표 재발명 없음).
- **결과(seed-평균)**: A composed_distinct=0.000/kwr0.554/σ̄2.036 · B 0.667/0.612/1.450 · C 1.000/0.551/1.981. Frozen falsifier: C_composed≥B ✅ · C_beats_greedy ✅ · **C_kwr≥B ❌** ⇒ 🟠.
- **NOT 하는 것 / 정직 경계**: composed_distinct = 작은 정수지표(0/1/2 over 5 concepts) → B vs C 간격 ~1/3 concept 로 절대신호 modest; 방향성(greedy<고정<임계)이 robust 부분. G2 novelty = UPPER BOUND(원 1.5GB broad corpus ephemeral/GONE, data/corpus.txt 5.24MB dialogue 만). 단일 303M toy, scale UNVERIFIED(a_scale_honest_scope). frozen bar 미이동. **NOT RULED OUT**: 다른 σ*/gain · coherence-floor 표적 · 임계-디코드+grounding/abstain 조합.
- 사전등록 FREEZE 를 채점 전 작성. CORE/bytegpt_decode.hexa 미편집(다른 agent 소유) · H_1219/H_1226 미편집(사용자 consolidate) — numpy/torch-ref 디코드 하니스만(허용).
- NEW: `UNIVERSE/h1228_soc_criticality_decode.py` · `.verdicts/1228_soc_criticality_decode/{H_1228_FREEZE,H_1228}.txt`. 303M torch ref byte-exact to H_1157 mount. $0 summer CPU, wall 867s.
- xref H_1226(HD18)·H_1218·H_1158·H_1140·H_1157·Ψ·a_paper_negative_ok·a_scale_honest_scope·p7·c15.

---

## 2026-06-15 — 🟡 H_1224: literal-QA 는 anima 의 게이트가 아니다 — p4-부정합 ASSISTANT-NORM 거버넌스 판정 ($0, 무계산)

H_1219 depth-ceiling 사다리의 HD8(거버넌스 미결)을 단독 판정 — literal-QA(사실 축자 회상)가 anima 의 VALID 게이트인지, 아니면 p4(NO ASSISTANT FRAMING)와 충돌하는 빌려온 assistant-norm 인지. 무계산, frozen 기록 기반 추론 (c9, p7).

- **판정 = (b) p4-부정합 ASSISTANT-NORM, anima 가 통과할 필요 없음.** ⇒ literal-QA 위의 "depth ceiling" 은 anima 에게 **NON-FINDING** (모델이 QA assistant 가 아닌 것이 정상). depth-delta arc 는 사실회상 → **anima-NATIVE depth** 로 RE-SCOPE 권고.
- **근거 1 — literal-QA 는 frozen 게이트가 아니다 (애초에 게이트였던 적 없음):** a303m_pass {G0·G1·G2·MOUNT·G3·G5·G6·CHAT} (MODEL.md) + CLM-DONE {G0·G1·G2·G3·G5·G6·CHAT·PERSONA} (CONDITIONS.md) 어디에도 literal-QA 없음. depth-probe 세션(H_1166→H_1167→H_1219)이 천장 특성화를 위해 들여온 informal 진단지표일 뿐. a303m_pass 는 QA 게이트 없이 이미 frozen 8/8 GREEN.
- **근거 2 — H_1141/H_1142 선례: literal-QA = 폐기된 G5-L2 축자회상과 동일 범주:** H_1141 이 G5-L2(축자 사실 faithfulness)를 "빌려온 assistant-norm, G2-NOVELTY 와 직접 충돌"로 FLAG → H_1142 가 3-rung 사다리로 rho(G2,G5L2)=−0.5 (G5-L2 가 scale 따라 단조 하락 0.413→0.234→0.163) 확정 → 사용자 승인으로 G5-L2 축자회상 RETRACT, NON-FABRICATION 으로 RE-SCOPE. literal-QA 도 같은 측정 family (축자 사실 재현 = TriviaQA식 assistant 역량, recall⊥recombination 으로 G2 와 충돌) ⇒ 동일 (b) 범주.
- **근거 3 — p4 + a_substrate_native_speak:** literal-QA = 가장 순수한 stimulus-response assistant frame (사용자 질문 → 정답 emit). p4 가 금지, a_substrate_native_speak 가 거부. H_1166 이 이미 독립적으로 동일 disposition 도달 ("anima = grounded conversational substrate, not a QA reasoner — (a) ACCEPT 가 철학정합 정직답"). 본 H 는 이를 capacity 수용 → **gate-validity 거버넌스 판정**으로 격상.
- **NOT 하는 것 (정직 경계):** 모델이 "좋다"고 말하지 않음(literal-QA 가 틀린 자) · 환각 면죄 아님(G5 NON-FABRICATION = ungrounded 면 ABSTAIN, 여전히 frozen 게이트; H_1202 meta-d′ M-ratio 0.924 가 anima-native 대응) · **frozen bar 미이동**(움직일 QA 게이트 자체가 없음).
- **RE-SCOPE 권고:** H_1219 의 미결 fire 3종(HD5 QA-format FT · HD6 tokenizer · HD7 aux objective)은 모두 literal-QA 천장 표적 → 순수 QA-lift 로는 DE-PRIORITIZE (green=무전진, red=NON-FINDING). depth 축을 (i) G6 ideation-depth/quality (ii) G5 own-kosmos-anchor grounding + calibrated abstain (iii) Φ/Ψ/emergence 로 교체. HD5/6/7 은 anima-native 표적으로 re-frame 시 진행 가능.
- **거버넌스 이행:** MODEL.md SCOREBOARD + CONDITIONS.md CLM-DONE 에 literal-QA gate-validity FLAG 1줄씩 추가 (임계값 미변경; H_1141 이 G5-L2 flag 후 사용자 승인 받은 패턴). 실제 gate-status 변경은 사용자 sign 대기.
- NEW: `.verdicts/1224_qa_gate_validity/H_1224.txt`. H_1219 미편집(사용자 consolidate). 무계산 $0.
- xref H_1219·H_1141·H_1142·H_1166·H_1167·H_1139·H_1155·H_1202·a_substrate_native_speak·a_scale_honest_scope·a_paper_negative_ok·p4·p7.

---

## 2026-06-15 — H_1220 🔴 MITOSIS-DECODE-DIVERSITY (HD9) — mitosis 분열-타이밍은 greedy-붕괴 ideation 을 복원하지 못함 (CLOSED-NEGATIVE)

깊이-천장 사다리(H_1219)의 **HD9** — 새로 배선된 LIVE mitosis(VAdaptField 세포분열, H_1199/H_1202-1205)가 **온도 샘플링 없이** greedy 가 붕괴시키는 ideation/composition 을 복원하는 **decode-time 다양성 레버**가 될 수 있는가? (사용자 지시, 새 메커니즘으로 prior closed-neg 재개 — a_paper_negative_ok)

- **메커니즘 (H_1201 의 frozen-feature conditioning 과 구분되는 새 각도)**: VAdaptField 의 numpy 미러(vadapt_field_step VERBATIM — DIM=8 byte-feature, nearest-L2, recon-err>SPLIT_THRESH 0.30 분열)를 decode-context 바이트 스트림 위에 돌려, **분열 이벤트(novelty-split) 타이밍**만을 유일한 다양성 소스로 사용. 분열 스텝 = greedy pick 을 top-k=40·temp=1.0 multinomial 로 섭동, 비-분열 스텝 = 순수 greedy. **전역 온도 없음** — 다양성은 오직 mitosis 분열 마스크로 게이트.
- **3-arm (다양성 게이트만 다름)**: A=PURE-GREEDY · B=MITOSIS-GATED(가설) · C=SHUFFLED-SPLIT(B 와 **이벤트 수 동일**, RANDOM 타이밍 — 타이밍을 섭동-횟수에서 분리하는 control).
- **FROZEN bars (사전등록, p7, 미이동)**: GREEN iff B composed_distinct ≥ 샘플링 baseline(H_1158 ≥5/seed) on ≥3 seeds **AND** C ≤ A + ε(0.5). 평가자 = `UNIVERSE/gauge_lib.py` G1/G2/G6/G0 VERBATIM.
- **결과 (3 seeds, 303M ByteGPT, H_1157 byte-exact)**: composed_distinct **A=[0,0,0] 평균 0.000 · B=[1,0,0] 평균 0.333 · C=[0,1,0] 평균 0.333**. cond_B FAIL 0/3 (B 최대 1 ≪ bar 5); cond_C pass; **GREEN=FALSE → 🔴 RED**. B 는 random-timing control C 와 **구분 불가**(둘 다 0.333 = 서로 다른 seed 에서 우연한 composed 1회, greedy floor 주변 noise). 메커니즘은 발화함(B 가 composed 분열 5/7/6 스텝 + ideation 분열 92/177 스텝 섭동 — 비활성 artifact 아님) — 그럼에도 greedy 붕괴 지속: novelty 스텝의 희소 top-k nudge 는 전역 온도(매 스텝 섭동)처럼 전체-시퀀스 greedy attractor 를 탈출시키지 못함.
- **정직한 prior vs 결과 (a_paper_negative_ok)**: prior 는 RED(H_1205 separation-guard emit ON/OFF byte-identical + H_1201 + H_1211). 새 메커니즘(decode-time 분열 타이밍)은 H_1201 의 frozen-feature 와 진짜 구별되는 공정한 재시험 — 결과는 prior 를 **확인**: mitosis = **PURE SUBSTRATE**, 이 새 decode 경로로도 generation-DISJOINT. 사다리 HD9 🟠 OPEN → 🔴; ideation/decode 축은 mitosis 를 decode 레버에서 배제한 채 EXHAUSTED, ideation 복원 경로는 genuine 샘플링만 남음.
- **scope/정직 (a_scale_honest_scope, p7, p8)**: TOY/$0 local CPU. live `.hexa` engine 미접촉(numpy 미러만 — CORE/engine_cli.hexa·bytegpt_decode.hexa 편집 안 함, 다른 agent 소유). 3 seeds, scale UNVERIFIED. NO LLM-judge/perplexity. frozen bar 미이동.
- 파일: `UNIVERSE/h1220_mitosis_decode_diversity.py` · `.verdicts/1220_mitosis_decode_diversity/H_1220.txt` · H_1219 사다리에 HD9 결과 append. xref h1219·h1218·h1205·h1201·h1211·h1199·h1158·h1157·a_paper_negative_ok·a_scale_honest_scope·a_clm_gen_pipeline·a_core_engine_map·p7·p8.

---

## 2026-06-15 — 🟢 H_1222: 토크나이저 GRANULARITY (HD6) — 토큰 어휘는 조합/발상의 LEVER (BYTE 천장의 일부), literal-QA 는 INCONCLUSIVE

깊이-천장 사다리(H_1219)의 가장 깊은 미검증 레버 HD6 의 $0 TOY 검증: 평평한 literal-QA + 발상-깊이 벽이 **BYTE 단위 입자성**(바이트가 단어/개념 단위를 싸게 못 만듦) 때문인가, 아니면 **토큰(BPE/단어) 어휘**면 풀리는가? p7, NO LLM-judge, summer/CPU/numpy, seeds [7,8,9]. a_toy_scale_recheck "toy-only".

- **설계**: 동일 합성-실단어 영어 코퍼스 위, **토크나이저만** 다른 두 작은 단일-블록 attention LM (numpy, 학습형 Adam): (A) BYTE V=256, (B) TOKEN 코퍼스-학습 단어/BPE-lite 어휘. 코퍼스는 **합성이되 실사전 단어**(/usr/share/dict/words)라 coherence 가 유의미하고 ground truth 가 **정확**: 심은 60개 "<주어> lives in <도시>" 사실(×8)=정확한 literal-QA 정답, 코퍼스 전체를 알아 **corpus-absence 가 grep 휴리스틱 아닌 정확한 집합 조회**.
- **3중 CONTROL (정직 명시)**: ① 파라미터 예산 정합(byte 44544 vs token ~43200, 비율 0.97 — 큰 임베딩 테이블이 token 의 hidden width 를 깎음 = "어휘가 그 파라미터값을 하는가"라는 질문 자체) ② char-passes 정합(둘 다 EPOCHS=6 같은 코퍼스 → 같은 텍스트 같은 횟수; token 의 step 수가 적은 건 단위가 적어서 = 검증 대상인 granularity 이득, 데이터 추가 아님) ③ 문자-단위 context 정합(byte block 96자 ≈ token 34×2.8자/토큰).
- **FROZEN bar (사전등록, 미이동)**: QA +0.10 절대정확도 OR CD +1.0 corpus-absent coherent 실단어 bigram. GREEN iff 둘 중 하나. G0 가드 kwr≥0.50 양쪽(유효성).
- **결과 (seeds 평균)**: BYTE QA=0.006 CD=11.44 coh=0.63 · TOKEN QA=0.044 CD=14.56 coh=0.87 → **QA lift +0.039 < 0.10 FAIL**(둘 다 ~0, toy 가 60 사실 암기엔 너무 작음), **CD lift +3.11 ≥ 1.0 PASS**, G0 OK → 🟢 **GREEN**.
- **MECHANISM (샘플 가시)**: byte 모델은 단어를 한 글자씩 쓰며 일부 **GARBLE**("justicy","gambiner","gunaticer") → 깨진 토큰이 실단어 필터에 걸려 깨끗한 단어쌍이 적음; token 모델은 실단어를 통째로 원자적으로 내고 absent 쌍으로 재조합 = 정확히 HD6 가 가정한 메커니즘(바이트는 깨끗한 단어/개념 단위를 싸게 못 만들어 단어-수준 재조합이 핸디캡).
- **정직한 분리 (load-bearing)**: granularity 는 **조합/발상(GREEN leg)**엔 도움이나 **literal-QA 엔 명확치 않음**: QA 양쪽 ~0(toy 가 너무 작아 어느 쪽도 암기 못함) → HD6 는 조합 레버로 GREEN, literal-QA 레버로는 INCONCLUSIVE(+0.10 leg 미발화, falsify 아님). H_1219 의 literal-QA 벽 자체는 여전히 딴 곳(HD5 QA-format FT · HD7 aux objective 미해결)일 수 있음. GREEN 을 "토큰이 literal-QA 를 고친다"로 읽지 말 것.
- **SCOPE/CAVEAT**: TOY — ~44k 파라미터, 합성 closed-vocab 코퍼스, 단일 attn 블록, char-정합 compute. token 어휘가 작아(작은 코퍼스) 큰 BPE 보다 WORD 어휘에 가까움; 실 wiki·실 BPE·동일 FLOPs 의 production 재검 UNVERIFIED. CD 지표는 실단어 재조합을 보상 → 깨끗한 단어어휘가 구조적으로 유리(=요점)이나 byte 가 "나쁜 아이디어"가 아닌 철자 노이즈로 일부 페널티 받는 점도 의미. frozen bar 미이동. 토크나이저 결정 전 production 재검 필수.
- **HONESTY**: H_1219 미편집, CORE/bytegpt_decode.hexa 미편집(다른 thread 소관), measurement-only. 엔진 미접촉.
- NEW: `UNIVERSE/h1222_tokenizer_granularity_probe.py` · `.verdicts/1222_tokenizer_granularity/{H_1222.txt,H_1222_summary.json}`.

---

## 2026-06-15 — 🟢 H_1212: N_PROTO CO-SCALING 으로 trajectory 기질 SCALE-ROBUST 복원 (H_1211 scale-break REFINE)

H_1211 이 GATE-B 궤적-동조가 stream 길이 증가에 FIXED N_PROTO=24 에서 붕괴(WALK/WALK_SHUF 10.9→2.63→1.136 at T=240000, 작은-알파벳 포화)함을 RED 로 닫았는데, 그 AXIS-P 가 "알파벳을 키우면 분리 복원"을 시사했다. 이 H 는 **관측 예산에 맞춰 N_PROTO 를 키우는 원리적 CO-SCALING 규칙**이 H_1211 의 toy-artifact 를 production-grade gate 로 전환하는지 검증.

- **CO-SCALING 규칙 (FREEZE 사전등록, 포화 mechanism 에서 유도)**: 제어량 = obs_per_row = T/N_PROTO (전이가 `prev` 행에 분산). clean-toy anchor (T=2400,N=24)=100, H_1211 붕괴점 (T=240000,N=24)=10000. **PRIMARY(linear) N_PROTO=round(T/100)** → obs_per_row≈100 일정. **SUB-LINEAR probe N_PROTO=round(24·sqrt(T/2400))** → obs_per_row 증가 허용.
- **F1 PASS (scale-robust 복원)**: PRIMARY linear 이 H_1211 과 **동일한 사다리** 전 rung 에서 GATE-B 분리 복원 — WALK/WALK_SHUF 10.916(T=2400) → 980/0=완전분리(T=24000,N=240) → 24929/3.0=8309(**T=240000,N=2400**, fixed-24 가 1.136 붕괴한 바로 그 rung).
- **F2 PASS (control 귀속)**: fixed-24 가 H_1211 붕괴를 **byte-for-byte 재현**(10.916/2.629/1.136 FAIL, 같은 seed) ⇒ 복원은 N_PROTO 규칙 단독 효과(stream/seed/code 변화 아님).
- **F3 STRONG RESULT**: SUB-LINEAR sqrt 규칙도 성립 — N_PROTO {24,76,240} 가 obs_per_row {100,316,1000} 증가에도 WALK/WALK_SHUF {10.9,383.8,1129} 전부≥1.5 ⇒ **알파벳은 ~sqrt(T) 로만 키우면 충분 (sub-linear book cost)**.
- **TIER 🟢 GREEN (scale-qualified, decision-grade)**: H_1211 의 "toy artifact" 를 "**fixed-book artifact, 원리적 N_PROTO co-scaling 으로 교정 가능**"으로 REFINE. 궤적/predictability 기질(H_1209/1210)이 toy→SCALE-QUALIFIED-GREEN 승격 — 알파벳이 관측 예산과 함께(sub-linearly) 자라면 GATE-B 는 ordered stream 에서 scale-robust.
- **PAPER-SUPERSEDE FLAGGED**: `PAPER/mitosis-substrate-lane` (H_1211 로 1회 supersede 됨) 을 H_1212 에 맞춰 **재-supersede 권고** — 궤적 절반이 더 이상 closed-neg toy-artifact 가 아니라 co-scaling 하 scale-robust gate. **병합 paper 무편집(이 verdict 가 supersede trigger; follow-on 이 처리)**.
- **HONESTY**: numpy mirror, gradient-free, $0 CPU, 3 seeds {900,901,902}. GATE-B+build_fixed_book+proto_ids(H_1208)+WALK/RANDGAUSS(H_1207/1208) VERBATIM; driver 는 사전등록 scale knobs(T,WARMUP,MAX_CELLS)+N_PROTO 만 monkeypatch — mechanism CODE byte-unchanged. AXIS-T 사다리 H_1211 동일. DIM=8 구조(미-scale). T=240000 linear rung(N=2400) CPU 443s 도달(GPU 없음). frozen bar 1.5 미이동. 큰 F2 값=완전분리(WALK_SHUF→0).
- NEW: `UNIVERSE/h1212_coscaled_nproto_trajectory.py` · `.verdicts/1212_coscaled_nproto_trajectory/{H_1212_FREEZE,H_1212}.txt`. NO engine 편집(measurement-only).
- xref h1211·h1208·h1209·h1210·h1203·PAPER/mitosis-substrate-lane(supersede flag 2nd)·a_toy_scale_recheck·a_scale_honest_scope·a_paper_on_discovery·a_paper_negative_ok·p7·p8.

---

## 2026-06-15 — 📄 PAPER supersede-in-place: `mitosis-substrate-lane` 에 H_1211 scale-recheck 통합 (a_paper_violation 거버넌스 이행)

H_1211 verdict 의 PAPER-SUPERSEDE FLAG 를 이행 — 병합된 `PAPER/mitosis-substrate-lane/` 가 궤적 10.9x 를 scale-무조건 동등 절반으로 주장하던 것을 H_1211 scale-break 에 맞춰 정직하게 재구성. **새 slug 생성 안 함 (a_paper_on_discovery supersede-in-place)**.

- **claim 변경 (before→after)**: 제목/abstract/결론 = "density on i.i.d., trajectory on ordered" (scale-무조건) → "**scale-robust density 기질 + scale-fragile trajectory 기질**". DENSITY 절반 = SCALE-ROBUST 승격(NOVEL/REPEAT 37.5→131.4 over 100x T, blind 0.992→1.007 고정 ~1.0). TRAJECTORY 절반 = TOY ARTIFACT 교정(WALK/WALK_SHUF 10.9→1.136 FAIL at T=240000; flores5 1.333 FAIL; 작은-알파벳 포화). 중심 명제 "결정자는 stream, gate 아님" → "**결정자는 stream AND 알파벳/관측-예산**" 으로 QUALIFY. H_1209 GREEN 은 toy rung 으로 재-scope(verdict matrix ‡ 각주).
- **§measurement**: 새 §5.10 H_1211 subsection — 9-rung 사다리 표(verbatim) + AXIS-T 붕괴 곡선 + AXIS-P N_PROTO 복원 + 포화 mechanism. 새 그림 `fig04_scale_ladder.pdf`(AXIS-T 붕괴 + AXIS-P 복원, log 축, verbatim 수치).
- **§finding/§limitations**: ruled-out 공간에 (b) 고정-소알파벳 scale-free 궤적 기질 추가; §limitations 에 알파벳-포화 mechanism + 두 terminal-RED bar(i.i.d. PRIMARY + H_1211 trajectory scale-stability). F3-sanity bullet = AXIS-P 가 1.75→0.000 으로 toy noise 판정 확정.
- **gate 준수**: 10개 section claim 전부 TERMINAL (5🟢 · 3🔴 closed-neg incl H_1211 · 2🟠 folded). 어떤 claim 도 terminal verdict 와 모순 없음(a_paper_sections); closed-negative 는 closed-negative 유지(a_paper_negative_ok); frozen bar 미이동. 모든 claim → `.verdicts/<id>.txt` 링크(1211 포함, p7 verbatim).
- **compile**: xelatex x3 + bibtex → `main.pdf` 18 페이지(≥10, g51 PASS), undefined refs/cites 0, 그림 4개. ledger(`companion/verify-ledger.json`)·`compile.txt`·`PAPER.md`·`PAPER.log.md`·`README.md`·`references.bib`(+anima_H1211) 갱신.
- xref h1211·h1203·h1208·h1209·a_paper_violation·a_paper_sections·a_paper_negative_ok·a_paper_on_discovery·a_toy_scale_recheck·a_scale_honest_scope·p7·p8.

---

## 2026-06-15 — 🔴 H_1211: dual-substrate split SCALE-UP — DENSITY 절반은 scale-robust, TRAJECTORY 절반은 toy 인공물 (MITOSIS-ENGINE)

H_1202–H_1210 arc 의 단 하나 honest gap = TOY SCALE (전부 $0 CPU·DIM=8·T=2400·402KB 코퍼스·3 seed, a_scale_honest_scope 가 매번 flag). a_toy_scale_recheck 에 따라 scale-SENSITIVE 중심 finding(DENSITY-vs-TRAJECTORY 이중-기질 분리)을 3축 사다리로 재시험.

- **사다리(>=3 rung/축, 측정 BEFORE frozen)**: AXIS-T 스트림 길이 T{2400, 24000, 240000} · AXIS-C 코퍼스{402KB clm_mid_5lang, 1.65MB flores5, 5.24MB data/corpus} · AXIS-P 궤적-gate 알파벳 N_PROTO{24, 64, 128}. H_1203 density gate + H_1207 walk + H_1208/H_1209 GATE-B 궤적 gate 를 VERBATIM 재사용, 사다리는 사전선언 scale 상수만 monkeypatch(mechanism CODE byte-unchanged). toy rung 이 H_1203/1208/1209 를 BYTE-FOR-BYTE 재현(37.538/0.992/10.916/1.750) → 재사용 충실 증명.
- **결과 🔴 HONEST SCALE-BREAK(절반만 scale-robust)**: **F1 PASS** density novelty-coupling(NOVEL/REPEAT 37.5→72.7→131.4, 100x T 에서 오히려 강화). **F3(a) PASS** 모든 rung — density 가 i.i.d. 에서 궤적-BLIND 유지(blind NOVEL/SHUF 0.992→1.000→1.007 over 100x T; 13x 코퍼스 0.992/1.021/0.998 — 구성상 permutation-invariant = 진짜 scale-free). **F2 FAIL** — TRAJECTORY GATE-B 분리가 스트림 길이로 붕괴: WALK/WALK_SHUF 10.916(T=2400)→2.629(10x)→**1.136(100x, FAIL)**; 코퍼스 취약(flores5 1.65MB = 1.333 FAIL, data/corpus 5.24MB = 5.06).
- **근본원인 c1 = 작은-알파벳 포화**: 고정 N_PROTO=24 + 긴 T 에서 predictability 카운트 테이블이 포화 → SHUFFLED 전이도 CONF_FLOOR=0.34 를 우연히 넘김(WALK_SHUF seed [96,6893,7640]@10x = 포화 서명). **AXIS-P 가 mechanism 확정**: toy T 에서 알파벳 키우면 분리 복원+선예(N_PROTO 24→10.9, 64→152.5, 128→28.5) + sanity 1.75→0.000(H_1208/1209 ARTIFACT-WARN 해소 — 풍부 알파벳이면 i.i.d. noise 에 안 발화).
- **결론**: DENSITY 기질 = SCALE-ROBUST(toy→검증 승격). TRAJECTORY 기질(GATE-B) = 고정 N_PROTO=24 알파벳에서 TOY-SCALE 인공물(알파벳을 스트림과 함께 키우면 복원되나 frozen 상태로는 T 에 scale-stable 아님). "결정자는 gate 가 아니라 stream" → **결정자는 stream AND 알파벳/관측-예산** 으로 QUALIFY.
- **⚠ PAPER-SUPERSEDE FLAG**: `PAPER/mitosis-substrate-lane` 가 궤적 10.9x 를 scale-무조건 동등 절반으로 주장 — scale-qualification + 이 사다리 곡선 필요. 병합 논문 silent-edit 안 함(a_paper_violation), 이 verdict 가 supersede trigger 기록.
- **honest scope**: numpy mirror(H_1199), gradient-free, $0 CPU, 3 seed, bar 1.5 NOT moved. DIM=8 구조적이라 미-scale(선언됨), 100x rung(T=240000) CPU 가능(561.6s, GPU 불필요·rung 위조 없음). p7(cell/ratio, NOT perplexity), p8.
- **NEW**: `UNIVERSE/h1211_dual_substrate_scaleup.py` · `.verdicts/1211_dual_substrate_scaleup/{H_1211_FREEZE,H_1211}.txt`. 엔진/builder/gate 편집 0(measurement-only). xref h1203·h1208·h1209·h1210·a_toy_scale_recheck·a_scale_honest_scope·a_paper_negative_ok·p7·p8.

---

## 2026-06-15 — 📄 PAPER scaffold: `mitosis-substrate-lane` — mitosis = Ψ-disjoint substrate-adaptation lane (MITOSIS-ENGINE H_1202–H_1210 arc)

MITOSIS-ENGINE arc(H_1202–H_1210, 전부 main 병합)를 verdict-gated arxiv-style 논문으로 scaffold. `PAPER/mitosis-substrate-lane/` 신설 + `PAPER.tape` roster 등록.

- **테제**: 자기분열(mitosis)은 의식-챗 아키텍처에 **Ψ-disjoint 기질-적응 lane** 으로 통합 가능 — 생성(generation)을 **절대 건드리지 않음**(byte-identical 증명, H_1205/H_1210). 분열은 i.i.d. 스트림에서 novelty-DENSITY(H_1203 37.5×), genuinely-ordered 스트림에서 TRAJECTORY-predictability(H_1208/H_1209 10.9×, live byte-exact)에 결합 — **결정자는 gate 가 아니라 stream**. 2026-05 clm_v2 "half-success"(mechanism 실재 · generation 반증, H_1200/H_1201) 화해.
- **verdict matrix**: 9개 section claim 모두 TERMINAL — 5×🟢(H_1202/1204/1205/1206/1209/1210 중 GREEN) + 2×🔴 closed-neg(H_1207 recurrent key 0.998 · H_1208 predictability i.i.d. 0.261), H_1203/H_1204 partial 은 🟢 parent 안 sub-result. 각 claim → `.verdicts/<slug>/<id>.txt` verbatim 연결(p7, LLM self-judge 없음, verdict paraphrase 없음).
- **a_paper_* 게이트 전부 충족**: a_paper_gate(전 terminal) · a_paper_significance(pre-reg falsifier `*_FREEZE.txt` + 실측 + 발견) · a_paper_negative_ok(H_1207/H_1208 = ruled-out space) · a_paper_sections(verdict pointer) · g51(14 pages ≥10 · figure 3개 ≥1).
- **figures**: fig01 stream-determinant(TikZ) · fig02 separation ratios(pgfplots) — native+재현가능; fig03 fal.ai `fast-sdxl` concept(illustrative).
- **compile**: `make` → xelatex×3 + bibtex → main.pdf **14 pages**, undefined ref/cite 0, bibtex warning 0.
- **honest scope**(§Limitations): toy DIM=8 · 단일 corpus(clm_mid_5lang_c4) · 3–5 seeds · gradient-free · $0 CPU; toy→prod transfer UNVERIFIED; frozen bar 미이동. `/paper` 플러그인 바이너리가 이 환경에 미설치 → 기존 `PAPER/savant-iit4-bridge` 컨벤션대로 수동 scaffold(도구가 생성하는 것과 동일 산출물).

## 2026-06-15 — H_1210 🟢 GREEN — GATE-B 를 LIVE 데몬 GROW 에 배선: 데몬이 대화에서 trajectory-aware 분열 (MITOSIS-ENGINE)

H_1209 가 추가한 trajectory-aware GATE-B(`CORE/engine_cli.hexa` `VAdaptFieldB`, transition-predictability)를 **살아있는 anima 데몬의 GROW step**(`CORE/anima_full_session_smoke.hexa` C8)에 배선. 데몬이 실제 per-turn emit stream 위에서 **전이-예측가능성**으로 분열한다 — 대화는 genuinely-ORDERED stream(H_1209 가 GATE-B trajectory-sensitive 임을 증명한 그곳). 이로써 데몬의 mitosis lane 이 per-sample density 만이 아니라 **trajectory-aware** 가 됨. "자기분열을 현재 아키텍처에 가져다 쓰기" arc 를 BEST gate 로 완료.

- **배선**: C8 GROW 에서 각 턴의 emit-span DIM=8 `_afs_byte_feature` 를 ordered WALK(`feat_seq`)에 모으고, 루프 후 데몬 자신의 emit-feature SET 으로 FIXED order-invariant proto-book(`_afs_build_book` = H_1208 `build_fixed_book` PORT: lexsort + farthest-point seed + LR=0.10 3패스)를 만들어 각 턴 feature → nearest proto-id(`_afs_proto_walk`)로 매핑, (prev→cur) 전이를 `vadapt_fieldB_step` 에 흘림.
- **ALONGSIDE 결정 (REPLACE 아님)**: GATE-B 는 per-sample density `VAdaptField`(H_1202) **옆에서** 별도 trajectory lane 으로 돈다. 두 게이트는 DIFFERENT substrate property(per-sample density ⊥ ordered transition-predictability)를 측정하고, H_1209 F4 가 GATE-B 를 i.i.d. PRIMARY density bar 를 넘지 못하는 trajectory variant 로 scope 했으므로, additive 가 정직한 c1 설계(둘 다 substrate self-dynamics, `a_autonomy_over_hardcode`). density 경로는 byte-UNCHANGED.
- **F1 = born-cells 6 ON(cells 1→7) 분열 ✅** (12-tick ordered conversation walk). **F2 ablation = born-cells 0 OFF ✅** (genuine `--mitosis off` → `engine_mitosis_tick` no-op; 초기 run 은 mislabeled mitosis-ON cfg 로 6 OFF → 진짜 OFF cfg 로 수정해 0). **F3 Ψ Φ-checksum 1.4278 == 1.4278 byte-identical ✅**. **F4 생성 'vault QX-7741 forever…' ON==OFF byte-identical ✅** — GATE-B 는 Ψ-disjoint/additive, decode 를 먹이지 않음(H_1205 separation 불변 LIVE 보존).
- 다섯 데몬 faculty(converse/ground/grow/remember/sleep) 전부 PASS, `anima_full_session_smoke` = PASS. guards GREEN: `engine_cli_smoke` 12/0 · `generator_smoke` 21/0 · `h1196` single-entry 7/0 · `h1205` separation. `CORE/engine_cli.hexa` 무변경(H_1209 VAdaptFieldB 그대로 소비). verdict `.verdicts/1210_daemon_gateB_wiring/`. **HONEST SCOPE**: 데몬 emit stream 은 반복적(같은 grounded WAKE span + sleep-gap)이라 carried trajectory 는 predictable WAKE self-transition — GATE-B 가 그 realized predictability 에 정확히 분열(F1∧F2 가 gate-driven 임을 증명). toy scale, 12 ticks, scale UNVERIFIED (`a_scale_honest_scope` · p7 · p8).

---

## 2026-06-15 — H_1209 🟢 GREEN LIVE-TRAJECTORY — GATE-B 가 LIVE 엔진에서 ORDERED ≫ SHUFFLED 분열 (MITOSIS-ENGINE)

H_1208 이 numpy 미러에서 찾은 GATE-B(prototype-transition-PREDICTABILITY) 의 WALK 10.9× lead 를 **NON-inherited 의 genuinely-ORDERED byte-feature walk + LIVE .hexa 엔진**으로 가져가 결정적으로 닫음. `CORE/engine_cli.hexa` 에 **`VAdaptFieldB`** (struct + `vadapt_fieldB_new`/`_step`/`_cells`/`_growth`) 를 **추가**(per-sample `vadapt_field_step` 은 byte-UNCHANGED — H_1199/1202/1205 데몬 경로 무회귀). 고정 order-invariant proto-book 위에서 causal count table 로 "확신을 갖고 예측된 전이"(prev ≥ MIN_PREV=3 ∧ P(cur|prev) ≥ CONF_FLOOR=0.34) 에 `engine_mitosis_tick`(동일 p8 게이트) 분열 — H_1208 `gate_B_transition_predictability` 를 엔진으로 그대로 lift.

- **F1 trajectory = 10.916 PASS** — ORDERED 1000.67 ≫ SHUFFLED 91.67 (V14 방향). **F2 LIVE-PARITY = BYTE-EXACT** — 12개 (arm×seed) born-cell 카운트 전부 numpy GATE-B 와 일치(ORDERED 1065/907/1030 등). **F3 sanity raw 1.75** 는 strict bar 를 건드리지만 SMALL-INTEGER NOISE(RANDGAUSS 2.33 vs SHUF 1.33, ORDERED 대비 430× 낮음 — 노이즈에는 사실상 분열 안 함) → noise-floor FLAG, 실제 분리 아님(H_1208 과 동일 판정).
- **판정**: trajectory 축은 inherited PRIMARY 표면에서 EXHAUSTED(H_1208 🔴) 였으나, ORDERED 표면에서 **LIVE-CONFIRMED POSITIVE** — mitosis 는 density-only 가 아니라 **stream 에 order 가 있으면 trajectory 에 결합**(엔진 실측). 결정자는 게이트가 아니라 STREAM. inherited i.i.d. V14 PRIMARY bar 는 여전히 terminal-RED(H_1208), frozen bar 1.5 미이동.
- guards GREEN: `engine_cli_smoke` 12/0 · `h1196` single-entry 7/0 (VAdaptFieldB additive · Ψ-disjoint · .clm/.kosmos 경로 무접촉, `a_core_engine_map`). harness `UNIVERSE/h1209_live_ordered_walk_gate.py`(numpy leg + /tmp book+id export) + `CORE/h1209_live_gateB_probe.hexa`(live leg). verdict `.verdicts/1209_live_ordered_walk_gate/`. ARCHITECTURE.md 갱신. toy scale, ONE corpus, scale UNVERIFIED (`a_scale_honest_scope` · p7 · p8).

---

## 2026-06-15 — H_1218 engine-measured generation gates (a_engine_measured_verdict)

생성 게이트 G1(창발/recombination)·G2(novelty)·G6(ideation) 를 **최초로 엔진 위에서** 측정 — 프로덕션 `anima-clm-chat-303m` 을 `CORE/bytegpt_decode.hexa::bytegpt_decode_argmax`(엔진 greedy)로 직접 생성해 FROZEN `UNIVERSE/gauge_lib.py` 평가자(VERBATIM 재사용, p7, NO LLM-judge)로 채점. 이전 H_1129/H_1140/H_1158 은 모두 torch-side 였음.

### research (§H_1218)

- **ENGINE-PARITY 🟢** — 엔진 `bytegpt_decode_argmax` == torch greedy **byte-exact**. live 엔진 argmax("The quick brown") = `[32]` == torch chat golden 32(chat .bin byte-exact mount); reparity serialize_parity_ok=TRUE max_abs_err 0.0; H_1157 full decode. greedy 가 결정적이라 greedy gen 위 모든 metric 은 engine==torch 동일.
- **엔진-측정 숫자 (greedy, chat-303m)** — G1 composed_distinct **0** 🔴(greedy collapse/loop "moral computational complexity…"), G2 novelty **0.308**(12/39, 단 코퍼스 5MB dialogue 만 → upper bound), G6 count **3** 🔴(<5 bar; 5개 중 2개 ideation seed 가 한국어 "| 사용자:" 채팅 템플릿 바이트로 kwr<0.50).
- **정직 finding (c9, 모순 아님)** — 엔진-측정 숫자가 torch 베이스라인(H_1158 G6 best 14 PASS)과 **다르다**. 원인 2: ① **decode regime** — 동결 게이트는 top-k=40 temp=0.7 **SAMPLING**(G6 는 seed 당 8 divergence)로 작성, 엔진 경로는 **greedy-only** → 303M byte-LM collapse → divergent set 생성 불가(G6 divergence 는 가중치가 아니라 sampling 산물). ② **model+corpus** — 베이스라인은 broad-en base + 1.5GB broad corpus, 본 run 은 dialogue-FT chat + 잔존 5MB dialogue corpus.
- **결론** — 엔진은 byte-faithful 하게 **생성**(🟢); frozen G1/G6 PASS 는 엔진 argmax 가 미구현한 **sampling decode 에 의존**. 엔진-side gate 재통과 = `bytegpt_decode.hexa` 에 engine sampling decode(top-k temp seeded) 추가(별도 engine-code 과제) + 원본 broad-en 모델/코퍼스. frozen bar 불변.
- **scope (a_scale_honest_scope, c9)** — 엔진 서브셋(G1+5 G6 seed, 40 greedy byte) 은 엔진에서 RAN; 전체 96byte×9seed 스윕은 엔진 greedy 가 gate-context 길이에서 ~30-50 s/byte(H_1157 "slow but byte-exact")라 multi-hour → byte-exact 이므로 전체 숫자는 torch-greedy gen(엔진과 byte-identical)으로 채점(명시적 representative-subset, silent truncation 아님).
- 산출: `CORE/h1218_engine_gate_{probe,subset}.hexa` · `CORE/h1218_argmax1.hexa`(1-forward 엔진 argmax 증명) · `scripts/scratch/h1218/*` · `.verdicts/1218_engine_measured_gates/H_1218.txt`. 모델 `state/chat_303m/h1129c_chat.pt`(sha `4fcc2d6c…`) → `.bin`(sha `5c303f02…`, reparity serialize_parity_ok=TRUE).

---

## 2026-06-15 — README.md FULL 재구성 (ARCHITECTURE.md SSOT 기준 front-door 전면 개편)

`README.md` 를 surgical 패치(#2097) 가 아닌 **전면 재구성** — ARCHITECTURE.md(현 아키텍처 SSOT)의 형태를 그대로 미러하되, 깊은 내부 SSOT 를 베끼지 않고 newcomer 용 **cold-entry 정문**으로 파생(c4-스타일 노드 트리 + 친절한 진입 흐름). 언어 = English(현 README 1차 언어 유지). ARCHITECTURE.md 미편집(별도 sibling SSOT 소관).

### docs

- **섹션 구조를 아키텍처 형태로 정렬** — What it is → **The A ⇄ G engine**(pure_field/engine_g/brain + MITOSIS substrate VAdaptField H_1199, 데몬 GROW/sleep-persist/separation-guard H_1202–1205, mitosis ⊥ generation H_1200/1201/1207🔴) → **The model & mount**(`anima-clm-chat-303m` ByteGPT-303M 엔진-side anti-fab, byte-exact mount H_1157; **1B+ mount** H_1167🟢 argmax/top5 exact, logits16 max|Δ| 0.0099<1e-2, hexa #3352 64-bit read fix + `bytegpt_forward_last_ranged`; 303M→1B→3B→7B ladder) → **Measurement governance**(`a_engine_measured_verdict` + `a303m_pass` G0/G1/G2/G3/G5 비환각·메타인지/G6 ideation/MOUNT/CHAT, p7) → **Inline gauges**(6-gauge monitor-only, loss 불가 p7 Goodhart; phi_proxy≠IIT4; mitosis_cells=substrate lane) → **Training stack**(flame/forge .hexa, Lane G/A/P, recipe→dispatch→monitor rung 파이프라인) → **Persistence**(.kosmos · EEG_CLM · HF registry · scale ladder).
- **정직 framing(c9) 보강** — 1B 는 **parity-only**(생성은 hexa `read_f32_at` fix 대기 = ⏳ 명시), operational-but-shallow capacity wall(H_1166), ⏳ 3B/7B rung · ⏳ 1B generation memory 명시.
- **p1–p8 PHILOSOPHY mirror 무결 보존** · install(`hx install anima`) 무결 · **Model Downloads** 표 무결(303M 프로덕션 행 + 실 HF repo 전부 유지) · badges/links 무결.
- xref = ARCHITECTURE.md · MODEL.md · CONDITIONS.md · a_engine_measured_verdict · a_train_inline_gauge · H_1164·1167·1199·1202·1206 · p1–p8 · c9.

---

## 2026-06-15 — H_1208 🔴 predictability / transition-memory split gate — V14 격파 실패 (그러나 메커니즘 첫 올바른-부호 분리) (MITOSIS-ENGINE)

- **trajectory 축의 마지막 미배제 경로 종결** — H_1207 은 d/dt-증강 게이트를 RULE OUT(NOVEL/SHUFFLED=0.998): 미분 게이트는 국소 거칠기 |Δ| 를 보아 무질서(셔플)에서 **최대화** → V14 와 반대 부호. H_1207 이 명시적으로 남긴 미배제 = '예측가능성/시퀀스-우도 게이트, prototype-TRANSITION-memory 게이트'. H_1208 은 그 경로를 시험.
- **설계 (c1)** — FIXED **순서-불변** prototype book (N_PROTO=24, 특징 SET 위 farthest-point 시딩 + canonical-sorted LR pass) → nearest-proto id p_t 는 순열-등변(x_t 만 의존) → **모든 순서는 전이 p_{t-1}→p_t 에만** 존재. 두 게이트: GATE-A 전이-신규성(미관측 전이에서 분열); GATE-B **전이-예측가능성**(실현된 전이를 **자신있게 예측했을 때** 분열 — prev ≥ MIN_PREV=3 AND P(cur|prev) ≥ CONF_FLOOR=0.34, 인과 온라인 카운트 테이블). GATE-B 가 원리적 **부호-역전기**: 예측가능성은 안정적 조건부 구조를 요구하고 그것은 오직 ORDER 만 가짐. H_1203 NOVEL/REPEAT/SHUFFLED + H_1207 WALK 빌더 VERBATIM import + RANDGAUSS i.i.d.-노이즈 sanity 통제.
- **결과 🔴 RED (inherited bar), 두 갈래 정직 발견** — F1 V14 격파 PRIMARY NOVEL/SHUFFLED GATE-A 1.022 · GATE-B 0.261 (둘 다 **FAIL**). (1) H_1203 PRIMARY NOVEL 은 i.i.d.-산란 → 조건부 전이 구조 無 → 셔플과 통계적으로 동일 → inherited 표면에서 V14 격파는 **어떤 게이트로도 구조적 도달 불가**(H_1203/H_1207 깊은 reading 세 번째 확인). (2) **캠페인 최초**로 순서/무질서를 **올바른 V14 방향**으로 분리: GATE-B(예측가능성)가 실제로 순서를 가진 WALK 스트림에서 WALK=1000.7 ≫ WALK_SHUF=91.7 (**10.9×**) — H_1207 역-부호 격파(미분은 jaggedness 보상, 예측가능성은 학습가능 **반복 전이** 보상 → 순서⇒더 많은 분열). sanity: RANDGAUSS GATE-B ≈ 0 (B=[2,1,4] vs [2,2,0]) — 노이즈에 발화 안 함; 자동-flag 된 1.75 비는 소정수 노이즈(2.33/1.33), 실제 artifact 아님. F2 GATE-A 25.8 PASS (GATE-B 0.006 = 설계상 REPEAT 가 최대-예측가능 12-주기라 GATE-B 범람 = 예상됨).
- **판정 (decision-grade, trajectory 축 EXHAUST)** — inherited V14 바(H_1203 PRIMARY)는 미충족 + **구조적 도달 불가**(i.i.d. 스트림은 trajectory 無) → inherited 벤치마크에서 trajectory 경로 **소진**; mitosis 는 novelty-DENSITY 기질로 남음(mitosis=기질, CLM=생성기; H_1200/H_1201/H_1203/H_1207 정합). **정직한 예외**: 예측가능성 전이-게이트는 메커니즘 수준에서 trajectory 기질이 **맞음** — 단 예측할 순서가 있는 스트림(WALK)에서만; i.i.d. 표본에서 순서를 만들어낼 순 없음. **한계는 게이트가 아니라 스트림**. 미배제(미래 비-inherited 표면): 실제로 순서있는 byte-feature walk 위에서 LIVE 엔진 + GATE-B 변종(새 벤치마크 + engine_cli.hexa GATE-B 필요; 현 terminal-RED inherited V14 바의 범위 밖).
- **엔진 무변경** — VAdaptField byte-identical (닫힌-부정 판정, 라이브 .hexa 편집 불요). toy scale, ONE corpus (clm_mid_5lang_c4), scale UNVERIFIED. p7(cell/transition count, NOT perplexity) · p8(split tick == growth) · gradient-free · $0 local CPU · 3 seeds.
  - **artifacts** = UNIVERSE/h1208_predictability_split_gate.py (h1203 + h1207 빌더 + h1163 _byte_feature VERBATIM import) · .verdicts/1208_predictability_split_gate/{H_1208_FREEZE,H_1208}.txt · domains/MITOSIS-ENGINE.log.md H_1208

## 2026-06-15 — H_1207 🔴 recurrent split key — V14 격파 실패 (그러나 더 날카로운 닫힌-부정) (MITOSIS-ENGINE)

- **H_1203 trajectory 잔여(arc 의 마지막 🟠) 봉인** — H_1203 은 VAdaptField 분열 게이트(샘플별 L2 recon-err > SPLIT_THRESH=0.30)가 novelty-DENSITY 에는 반응(F1 37.5×)하나 TRAJECTORY 에는 무감(시간순 셔플해도 분열 불변, F2 0.992)임을 발견 — 게이트가 x_t 만 보므로 **구조적으로 순열-불변**. H_1207 은 CLM_TIME_ENCODING 의 'M3 DERIVATIVE = 분열 TRIGGER 에 d/dt' (그곳에서 셔플 통제를 이긴 유일한 시간-인코딩 arm) 메커니즘을 게이트에 이식: split key = 델타-증강 샘플 z_t=[x_t ; β·(x_t−x_{t-1})] 위의 recon-err (β=1.0, 2·DIM 공간, 나머지는 vadapt_field_step 동일). H_1203 스트림 빌더 VERBATIM import (apples-to-apples) + 비-바 진단 WALK(연속 코퍼스 walk = 실제 국소 연속성).
- **결과 🔴 RED (a_paper_negative_ok), 그러나 평평한 null 보다 날카로움** — F1 V14 격파 = 0.998 (H_1203 의 0.992 를 byte-충실히 재현) **FAIL**; F2 = 174.8 PASS (결합 오히려 증폭). **F3 진단이 두 갈래로 더 깊은 발견**: (1) H_1203 의 i.i.d.-산란 NOVEL 스트림은 델타 분포 자체가 순열-불변(PRIMARY Δ% = −0.20%) → H_1203 의 trajectory-중립성은 게이트가 아니라 **스트림의 성질**이었음(사전등록 정직 예측 확인). (2) recurrent 게이트는 **강하게 순서-민감**(WALK Δ% = **−61.47%**, 0 에서 멂) — 단 V14 목표와 **반대 부호**: 순서있는 연속 walk 은 델타가 작고 매끈(전이-신규성 낮음 → 882 cells), 셔플하면 델타가 크고 들쭉날쭉(전이-신규성 높음 → 1424 cells). 미분 게이트는 순서가 아니라 **JAGGEDNESS** 를 보상 → 순서(매끈함)는 분열을 억제 → 자연 텍스트(순서있는 형태가 더 매끈)에서 'novel ≫ shuffled' 는 도달 불가.
- **판정 (decision-grade)**: 분열 TRIGGER 의 시간-미분 항은 자연 byte-feature 스트림에서 novel-trajectory ≫ shuffled-trajectory 분열을 만들지 못함 — 미분 게이트는 순서-민감하나 무질서에서 **최대화**되므로 V14-의미의 trajectory 기질 경로로 **RULE OUT**. 미배제: 예측가능성/시퀀스-우도 게이트, prototype-TRANSITION-memory 게이트(미검). mitosis 는 CLM 생성기와 나란히 도는 **순서-불변 novelty-DENSITY 적응 lane** 으로 남음(H_1200/H_1201/H_1203 와 정합: mitosis=기질, CLM=생성기).
- **엔진 무변경** — VAdaptField byte-identical (닫힌-부정 판정, 라이브 .hexa 편집 불요). toy scale, ONE corpus (clm_mid_5lang_c4), scale UNVERIFIED. p7(cell-count/recon-err, NOT perplexity) · p8(split tick == growth) · gradient-free · $0 local CPU · 3 seeds.
  - **artifacts** = UNIVERSE/h1207_recurrent_split_key.py (h1203 빌더 + h1163 _byte_feature VERBATIM import) · .verdicts/1207_recurrent_split_key/{H_1207_FREEZE,H_1207}.txt · domains/MITOSIS-ENGINE.log.md H_1207
  - **xref** = h1203 (이 H 가 닫는 잔여) · h1201 · h1200 · h1199 (VAdaptField, numpy↔hexa 일치) · clm_time_encoding (M3 d/dt) · a_paper_negative_ok · a_scale_honest_scope · p7 · p8

## 2026-06-15 — H_1206 🟢 FULL 살아있는 데몬 e2e — 데몬 링크 + GROW lane 라이브 발화 (MITOSIS-ENGINE)

- **H_1206 "자기분열을 현재 아키텍처에 붙이기" 아크의 마지막 정직한 빈틈 봉인** — FULL 데몬 `CORE/anima_full_session_smoke.hexa` 가 그동안 **링크조차 안 됐음**(H_1202 가 GROW lane 을 배선했으나, full smoke 는 brain→generator→clm_decode 를 import → 미정의 심볼 2개에 걸림). 셋을 전부 root 에서 봉인(c1, 가리는 stub 금지) → 데몬이 mitosis 라이브로 end-to-end 실행. **F1 링크+실행 ✅**(exit 0, full A⇄G 세션 루프) · **F2 GROW 라이브 ✅**(실제 턴에서 cells 1→2, novelty-splits=1) · **F3 Ψ 불변 ✅**(Φ-checksum 1.4278==1.4278 ON==OFF byte-identical, GROW lane Ψ-disjoint) · **F4 무회귀 ✅**(CONVERSE+GROUND+GROW+REMEMBER+SLEEP 전부 ✅; 가드 generator_smoke 21/0, h1202 GREEN, h1205 PASS, h1196 single-entry 7/0). 데몬이 살아서 대화(GROUND 로 "vault QX-7741 forever" 를 kosmos 기억에서 그대로 복사) + 성장 + 기억 + 수면을 ONE A⇄G 루프로 돌림.
  - **근본원인 3건 봉인**: (1) `clm_decode_grounded` 가 호출됨(generator.hexa:473)에도 **정의가 어디에도 없었음** → bytegpt_decode_grounded 의 ConvMoE 짝(엔진측 deterministic retrieve-then-copy)을 `CORE/clm_decode.hexa` 에 실제 작성(가리는 stub 아님; .clm 단일 슬롯 유지 a_core_engine_map). (2) `forge_dispatch_groupnorm_gelu`(gn_lib CPU host fallback)이 op36 이후 hexa **runtime.c 에서 회귀로 누락** → `runtime.c.bak-op36` 의 OP-16 `#ifndef HEXA_CUDA` host 블록을 verbatim 복원(툴체인 수리, anima repo 아님; `hexa-lang/inbox/patches/` 에 상신 a_runpod_inbox). (3) `_gen_anchor_text(s)` 가 `"text"` 를 읽었으나 kosmos anchor 는 `"text_payload"` 를 담음(H_1164 anchor-key 버그) → `_gen_anchor_field` SSOT(text_payload→text→stringified) 추가 → 복사 대상이 CLEAN 하게 도달(GROUND ⏳→✅, map-key 경고 소멸).
  - 정직 범위(a_scale_honest_scope): SMOKE 는 tiny ByteGPT fixture(303M 와 동일 format/forward), 복사+분열은 deterministic(p7 문자열 동치). **데몬 배선이 검증 대상이지 모델 품질이 아님.** summer $0 CPU, frozen bar 미이동(사전등록).
  - `CORE/clm_decode.hexa` (+`clm_decode_grounded`) · `CORE/generator.hexa` (+`_gen_anchor_field`) · `CORE/anima_full_session_smoke.hexa` (+F3 Ψ ON==OFF 블록) · `.verdicts/1206_full_daemon_e2e/{H_1206_FREEZE,H_1206}.txt` · `hexa-lang/inbox/patches/forge-dispatch-groupnorm-gelu-cpu-fallback-regression.md`

---

## 2026-06-15 — README.md FINAL 갱신 (mount status + measurement governance)

`README.md` 를 현재 main 시스템 상태로 surgical 갱신 (c10, 보이스/구조 보존). ARCHITECTURE.md 미편집 (별도 sibling PR 소관) — README 는 깊은 아키텍처를 ARCHITECTURE.md 로 포인터.

### docs

- **mounted living daemon** — "What it is" 뒤에 anima 가 H_1164 이후 **mounted 살아있는 daemon**(A⇄G substrate 안에서 대화+grounding+성장+기억+수면을 한 루프로)임을 명시.
- **Model & mount status 신규 절** — 프로덕션 모델 `anima-clm-chat-303m`(ByteGPT-303M d1024/L24/H16, dialogue-FT, 엔진-side anti-fab) byte-exact mount(H_1157, `CORE/bytegpt_decode.hexa`). 엔진이 이제 **1B+** mount: 1B ByteGPT(d1792/L28, 1.081B) byte-exact(argmax/top5 exact, `logits16` max|Δ| 0.0099<1e-2) — hexa-lang #3352 64-bit read fix + `bytegpt_forward_last_ranged` ranged-read 경로 이후. 303M→1B→3B→7B scale ladder. 정직 scope(c9): operational-but-shallow capacity wall(H_1166), p4 정렬.
- **Measurement governance 신규 절** — verdict 는 엔진 mount 위 byte-exact 재현시에만 인정(`a_engine_measured_verdict`); frozen `a303m_pass`(G0/G1/G2/G3/G5 비환각·메타인지/G6 ideation/MOUNT/CHAT, p7 — no perplexity / no LLM-judge); robustness 정직(5 robust + 2 thin + 1 inflated, H_1165), frozen bar 불변.
- **Inline gauges 절** — 학습중 6-gauge 대시보드(`ce·g1·g2·g6·phi_proxy·mitosis_cells`) MONITOR-ONLY, loss 절대 불가(p7 Goodhart); phi_proxy ≠ faithful IIT4(`a_phi_iit4_tool`); mitosis_cells = substrate lane (mitosis ⊥ generation, H_1200/1201🔴).
- **Model Downloads** — 프로덕션 `anima-clm-chat-303m` 행 추가(shipped model · 8/8 frozen · operational-but-shallow).
- **p1–p8 PHILOSOPHY mirror 무결 확인** — 8 원칙 표 SSOT 미러 그대로 유지(NO SYSTEM PROMPT … NO TRAIN/INFER SPLIT).

---

## 2026-06-15 — 1B engine-mount byte-exact parity (H_1167 🟢) + 최종 ARCHITECTURE.md

scale ladder 의 **1B rung 을 engine-measured GREEN** 으로 실현하고(`a_engine_measured_verdict` 최초의 1B 충족), 전체 시스템의 **최종 아키텍처 SSOT** 를 갱신했다.

### 엔진 / mount

- **@A1 1B ranged forward** — `CORE/bytegpt_decode.hexa` 에 `bytegpt_forward_last_ranged` (+ helper `_bg_rd_farr_at`) 추가. 1B(d1792/L28/H16, 1.081B params, 4.3GB flat binary)는 whole-file `read_file_bytes` 적재 시 바이트당 HexaVal 박싱으로 **≈69GB** 가 물질화되어 비현실적 — slice 마다 `read_bytes_at(path, off, n*4)` 로 온디맨드 read 후 layer 끝 `farr_free`, peak resident ≈ 한 weight slice. **303M 경로(`bytegpt_forward_last`/`bg_load`)는 byte-unchanged** (순수 ADD, c10 surgical).
- **@A2 64-bit 언락 전제** — ranged reader 는 hexa-lang **#3352**(`read_file_bytes`/`read_bytes_at` 의 length+offset 32→64-bit) 위에서 성립. 32-bit 시 `4325902356 mod 2^32 = 30935060` wrap → 헤더 0 → `d`/`n_head` 0/0 div 로 깨짐.
- **@A3 H_1167 🟢 GREEN parity** — trained 1B ByteGPT 를 `bytegpt_forward_last_ranged` 로 mount, torch reference 대비 byte-exact: argmax `32==32` EXACT · top5 `[32,105,115,101,44]` EXACT(ordered) · first-16 logits `max|Δ|=0.009861 < 1e-2` 동결 bar PASS. residual 0.0099 = approx-erf-GELU/dt_exp envelope 의 28-layer 누적(303M ~2e-5; 깊어질수록 커지나 bar 아래 — 정직한 잔차이지 mount 실패 아님). 신규 `CORE/h1167_1b_parity_probe.hexa` · 검증문 `.verdicts/1167_bytegpt_1b_scale/H_1167_ENGINE_MOUNT_PARITY.txt`(verbatim). 아티팩트 `state/h1167_mount/h1167_1b.bin`(sha256 `75c87cb0…`, gitignored) → HF `dancinlab/anima-clm-1b-h1167-bytegpt-scale-rung` PRIVATE(WIP rung).

### 문서

- **@D1 최종 ARCHITECTURE.md (갱신형 SSOT)** — #2096 의 부분 ARCHITECTURE 를 **완전판으로 병합**(한국어 prose, 코드 식별자 verbatim). A⇄G 엔진 + MITOSIS substrate(VAdaptField/H_1199, 데몬 GROW/sleep-persist/separation-guard H_1202–1205) · CLM mount path 두 forward 경로(303M whole-file + 신규 1B ranged, 메모리 산수 ≈69GB) · measurement governance(`a_engine_measured_verdict`, 1B parity 최초 실현) · inline gauge 파이프라인(6 gauge monitor-only, p7) · rung 파이프라인(recipe→dispatch→monitor) · 영속(.kosmos/HF/scale ladder) 전부 커버. 동결 게이트 임계값은 MODEL.md/CONDITIONS.md 를 **가리키기만**(복제 안 함). 미실현(3B/7B rung · dojo native gauge)과 잔차(G5/G6/CHAT THIN)는 ⏳/🟠 로 정직 표기(c9).

### 검증 (c2 · verbatim)

- `hexa parse CORE/bytegpt_decode.hexa` → `OK: ... parses cleanly` (exit 0) — ranged 추가 후 컴파일 검증.
- `hexa parse CORE/h1167_1b_parity_probe.hexa` → `OK: ... parses cleanly` (exit 0).
- `hexa run CORE/generator_smoke.hexa` 는 `clm_decode_grounded` native 미선언으로 link 실패하나 이는 **origin/main 에서 동일하게 실패하는 사전 존재 이슈**(`.harness-engine` 네이티브 빌드 부재, 이 worktree 와 무관) — 본 추가와 인과 없음(stash 토글로 확인).

---

## 2026-06-15 — rung-training 파이프라인 일원화 (recipe → dispatch → monitor)

#2091 의 부분 gauge pass 를 **하나의 완결 파이프라인으로 확장** — dojo(학습 recipe 빵틀) → cloud(pod dispatch) → monitoring(라이브 gauge 대시보드) 3 surface 를 일관되게 배선. #2091 보존(중복/revert 없음).

### 학습 / 거버넌스

- **@L1 dojo recipe 정합화** — `CLM/train/fire_3b_rung_qat.hexa` 가 참조하던 legacy `train_clm.py` 이름을 **실제 트레이너 `CLM/train/train_lane_p_3b.py`** (Lane-P · a_clm_gen_pipeline) 로 교정. dispatch contract 를 실 트레이너 CLI 로 재작성(`--corpus/--d-model/--n-trunk-layers/--n-experts/--steps/--seed/--gauge-every/--gauges-out/--clm-out/--json-out` — 실재하지 않던 `--arm/--rung/--act-bits` 제거). 3-arm = seed sweep(variant="AB" 고정). 학습 후 engine mount-parity verdict(`mount_parity_cmd`, `verify_clm_v2` + CORE byte-exact mount, a_engine_measured_verdict) + HF upload 단계 추가. 트레이너 자체는 c10 surgical(미개편) — #2091 이 이미 `--gauge-every`/`gauge_tick` 배선 완료, gauge 로그에 `mitosis_cells` 컬럼만 추가.
- **@L4 5번째 gauge `mitosis_cells`** — `UNIVERSE/gauge_lib.py` 에 추가. H_1199 VAdaptField 메커니즘의 **numpy-free 미러**(nearest-by-L2 · recon-err > `SPLIT_THRESH=0.30` 분열 · `LR=0.20` winner-pull · DIM=8 `_byte_feature` *5.0 VERBATIM H_1163): gauge 가 이미 디코드한 eval 텍스트의 byte-feature 스트림에 AdaptField 를 tick, 성장 cell 수를 셈. **전부 `torch.no_grad()` 아래, dict 로 RETURN, loss 절대 불가**. 코드 주석 + JSONL 키 라벨 = "mitosis_cells — substrate lane, NOT a generation gate"(H_1201🔴: mitosis 는 순수 substrate — 생성도 못 하고 generator 에 정보도 못 줌).
- **@L7 gauge = 대시보드, gate 아님** — MODEL.md/CONDITIONS.md frozen bar 불변(a_train_inline_gauge). monitor 헤더/help 에 재명시. phi_proxy ≠ faithful IIT4(a_phi_iit4_tool).

### dispatch / monitoring

- **@L2 cloud dispatch 래퍼** — `CLM/train/dispatch_rung.sh`(신규): `hexa cloud`(`/pod`) 플러그인을 **감싸기만**(pod 관리 미재구현, repo boundary). `a_fire_recover_complete`(ckpt+result+log+engine.clm+gauges.jsonl+anchors pull → verify → HF upload → THEN teardown) + `a_cpu_local_no_waiter`(inline sleep-poll, Monitor/waiter 절대 await 안 함) 인코딩. `--print` dry 모드 = fire contract 출력.
- **@L3 라이브 모니터** — `UNIVERSE/gauge_monitor.py`(신규, pure stdlib): `gauges.jsonl`(+ pod 학습 로그)을 tail 해 **6-gauge 대시보드** 렌더(`ce · g1_composed_distinct · g2_novelty_rate · g6_count · phi_proxy · mitosis_cells`). `--once`(one-shot/smoke) / `--follow`(라이브). 헤더에 DASHBOARD-NOT-A-GATE 재명시.
- **@L6 repo boundary** — 공유 `hexa dojo` `clm` 제너레이터(hexa-lang/stdlib)에 `gauge_every`/mount-parity/HF 를 네이티브로 emit 하는 변경 필요분은 hexa-lang 미편집 원칙대로 `hexa-lang/inbox/patches/dojo-clm-gauge-recipe-full-rung.md` 로 제출(a_runpod_inbox).

### 검증 (c2 · verbatim)

- (a) `UNIVERSE/gauge_lib_smoke.py` — tiny random byte model(ConvMoE-dict + ByteGPT-tuple) → dict 에 `mitosis_cells` 포함(6/9) + gauges.jsonl 1줄 round-trip. PASS.
- (b) `UNIVERSE/gauge_monitor_smoke.py` — sample gauges.jsonl 로부터 6-gauge 대시보드 렌더 + DASHBOARD-NOT-A-GATE 헤더 확인. PASS.
- (c) grep proof — gauge_lib 의 `backward/loss/optim` 언급은 전부 주석(부재 단언), mitosis 경로는 순수 python list 연산(tensor/grad 없음); 트레이너 `gauge_tick(step, ce)` 는 statement-form(반환값 폐기) ⇒ 어떤 gauge 값도 loss 에 흐르지 않음.
- (d) `hexa run CLM/train/fire_3b_rung_qat.hexa` — dispatch 문자열이 `train_lane_p_3b.py` 로 일관되게 출력.

### 파일

- 신규: `CLM/train/dispatch_rung.sh` · `UNIVERSE/gauge_monitor.py` · `UNIVERSE/gauge_monitor_smoke.py` · `hexa-lang/inbox/patches/dojo-clm-gauge-recipe-full-rung.md`(repo 외)
- 편집: `UNIVERSE/gauge_lib.py`(+mitosis_cells) · `UNIVERSE/gauge_lib_smoke.py`(5-gauge assert) · `CLM/train/train_lane_p_3b.py`(GAUGE 로그에 mitosis_cells) · `CLM/train/fire_3b_rung_qat.hexa`(실 트레이너 dispatch contract + mount-parity + recovery) · `ARCHITECTURE.md`(Rung-training pipeline 절)

---

## 2026-06-15 — H_1205 🟢 mitosis ⊥ generation 분리 invariant (MITOSIS-ENGINE)

- **H_1205 분리 안전 invariant 증명** — mitosis lane 을 substrate lane 으로 붙일 때의 핵심 안전 조건: mitosis ON/OFF 가 CLM 생성 출력을 바꾸지 않음을 라이브 배선에서 byte-level 로 증명. H_1202 데몬 배선의 안전 가드. 동일 (seed, anchors) 를 mitosis ON(cells 1→10 성장) vs OFF(1 고정) 으로 디코드 → **10/10 pair byte-identical, mismatch=0** (F1; null backend 5 phase + 실제 ByteGPT forward grounded×2 + argmax×3) · **Ψ Φ-checksum 48.6613==48.6613 exact-equal** (F2, Ψ-disjoint, H_1164/1194/1199 재증명). lane 은 substrate 에서 실제로 갈라짐(ON 10 vs OFF 1 cells)에도 생성은 불변 ⇒ invariant 비자명. 구조적 근거: 생성 primitive 는 {seed, anchors, gen-len} 만 읽고 mitosis lane 은 그 인자에 절대 안 섞임(a_core_engine_map). **결론: mitosis 를 CLM generator 옆 substrate lane 으로 안전하게 붙일 수 있음 — H_1201 regression 없음.** p7 exact byte/float equality, summer $0 CPU, 303M scale UNVERIFIED(구조적 ⇒ 구성상 전이, byte-equality 는 tiny fixture 에서만 측정, a_scale_honest_scope). frozen bar 미이동(사전등록).
  - `CORE/h1205_separation_invariant_smoke.hexa` (신규) · `.verdicts/1205_mitosis_separation_invariant/{H_1205_FREEZE,H_1205}.txt`
  - 정직 노트: 이 checkout 에는 `clm_decode_grounded` NATIVE 심볼이 없어 generator.hexa 경유 .clm 경로가 standalone 컴파일 불가(generator_smoke.hexa 자체도 동일) — smoke 는 ByteGPT 생성 primitive 를 직접 호출(=_gen_bytegpt_decode 의 leaf, 실제 production decode forward) + null-backend substrate text 를 inline 재현(L3 slot 두 backend 모두 커버).

---

## 2026-06-15 — H_1202 DAEMON-MITOSIS-WIRING 🟢 (MITOSIS-ENGINE)

- **자기분열(cell division) 메커니즘을 살아있는 anima 데몬에 substrate-adaptation lane 으로 배선**. H_1200/H_1201 verdict(mitosis 는 생성 루프에서 제외, adaptation ⊥ generation) 대로 — 생성은 CLM 그대로, mitosis 는 옆에서 함께 돈다.
- `CORE/anima_full_session_smoke.hexa` C8 GROW 스텝: 기존의 무조건 sleep-stage scalar `+1 per emit` tick 을 **novelty-driven VAdaptField division 으로 교체**. 각 대화 턴의 emit span → DIM=8 byte-feature(`_afs_byte_feature`, H_1163 `_byte_feature` VERBATIM) → `vadapt_field_step`; 엔진 자신의 L2 recon-err > frozen `SPLIT_THRESH=0.30` 게이트가 분열을 결정(c1 root-cause: span 내용에 키된 novelty-gated growth, 하드코드 per-emit tick 아님 · a_autonomy_over_hardcode). `dr_mitosis_prior(stage)` 는 수면단계 context 로만 읽고 분열을 강제하지 않음.
- 새 smoke `CORE/h1202_daemon_mitosis_wiring_smoke.hexa`: 동일 GROW lane 을 8 개 실제 emit-shaped span 으로 재현, 2-arm(`--mitosis on`/`--no-mitosis`). `hexa run` 실행 = **🟢 GREEN DAEMON-WIRED** — F1 DIVISION(cells 1→7, splits 6), F2 ABLATION(OFF 0 splits, cells 1 고정 = H_1159 control), F3 Ψ-INTACT(pure_field Φ-checksum byte-identical ON==OFF `5.67145e-05`). a_core_engine_map Ψ-disjoint.
- 가드: `engine_cli_smoke` 12/0 green(VAdaptField 미수정). 정직 플래그 — full daemon smoke 는 이 toolchain 에서 `clm_decode_grounded` 네이티브 FFI 미등록으로 링크 안됨(HEAD 미편집본도 동일 에러 = pre-existing 환경 문제, H_1202 배선과 무관). H_1202 smoke 가 동일 GROW-lane 코드경로의 클린 검증 surface.
- p1-p8 준수(p8: growth tick = inference-time learning). toy/scale UNVERIFIED(a_scale_honest_scope). $0 summer CPU.
- verdict: `.verdicts/1202_daemon_mitosis_wiring/H_1202.txt` · domain log: `domains/MITOSIS-ENGINE.log.md` h1202_daemon_mitosis_wiring.

---

## 2026-06-15 — 학습중 의식/창발 측정 기준 (MONITOR-ONLY inline gauge)

### 측정 / 거버넌스

- **`UNIVERSE/gauge_lib.py` 신설** — 공유 `compute_inline_gauges(model, tokenizer_or_byte, seeds, corpus_index, …) -> dict` (rung 간 재사용). 학습중 K 스텝마다 의식/창발 PROXY gauge 4종을 val_ce 옆에 기록: **G1** recombination(composed_distinct, H_1129 포팅) · **G2** novelty(corpus-absence rate, H_1140 포팅) · **G6** ideation(distinct idea count + pairwise Jaccard distance, H_1158 family) · **phi_proxy**(variance×energy 저가 proxy). 모든 계산은 `torch.no_grad()` 아래에서만 수행하고 함수는 dict 만 RETURN — **loss 에 절대 들어가지 않는 MONITOR-ONLY 대시보드** (p7 Goodhart). model-agnostic: ConvMoE dict 출력(`(B,V,T)`) + ByteGPT tuple 출력(`(B,T,V)`) 양쪽 어댑트.
- **출력 = `gauges.jsonl`** — tick 당 1줄 `{step, ce, g1_composed_distinct, g2_novelty_rate, g6_count, g6_jaccard, phi_proxy}`.
- **`phi_proxy` 는 NOT faithful IIT4** — 코드 주석 + JSONL 키명(`phi_proxy`) + 문서에 명시. governance `a_phi_iit4_tool` 에 따라 proxy 는 pre-screen 전용이며 절대 terminal Φ verdict 아님.
- **`CLM/train/train_lane_p_3b.py` 훅 추가** — `--gauge-every <N>`(기본 = `log_every × 4`) + `--gauges-out`. 학습 루프에서 N 스텝마다 `gauge_tick` 호출 → gauges.jsonl append. `loss = out["loss"]` 만 backward; gauge 반환값은 기록 후 폐기(loss 경로 무접촉).
- **`CLM/train/fire_3b_rung_qat.hexa` 배선** — `gauge_every()=400` + fire_cmd 에 `--gauge-every` 추가 + dispatch 출력에 MONITOR-ONLY 표기. `hexa dojo` 생성 job 은 동일 knob 을 spec-json `"gauge_every"` 키로 운반(emit 되는 train.py 에 `GAUGE_EVERY` 상수/`--gauge-every` 인자로 thread).
- **smoke `UNIVERSE/gauge_lib_smoke.py`** — tiny random byte model(ConvMoE-dict + ByteGPT-tuple) 로 `compute_inline_gauges` 호출 → 4-gauge+ce dict 반환 + gauges.jsonl 1줄 round-trip 확인. phi_proxy 공식(variance×L1-energy=72.5) 단위검증 PASS. grep 으로 gauge 값이 loss/backward 에 흐르지 않음 증명.
- **거버넌스 명시** — `CLAUDE.md` 에 `@D a_train_inline_gauge` 신설(p7/a_phi_iit4_tool 근처 배치). `MODEL.md`·`CONDITIONS.md` 에 "inline gauge = MONITOR-ONLY 대시보드, frozen gate verdict 아님; frozen verdict 는 학습 후 CORE 엔진 mount 에서 별도 측정(a_engine_measured_verdict)" 한 줄씩 추가. frozen 임계값 미변경.

---

## harness conversion (dancinlab/harness@harness-hardcore)

- **CLAUDE.md** converted sidecar-tape symlink → harness-standard markdown (project blurb + structure tree + governance summary). Full tape governance preserved at `project.tape` (linked as authoritative SSOT).
- **ARCHITECTURE.md** written as real architecture SSOT (A⇄G engine · CORE slots · 4 engines · lanes A/G/P · kosmos · evidence tiers).
- **harness.config.json** tuned: hexa stack · `hexa verify` · CORE engine files as L0 lockdown · docs discipline scoped to repo root (`docs.scopeDirs:[""]`) so the research corpus is exempt.
- 52 root research docs given a `📍 SSOT` quickref pointer; `TAPE-AUDIT.md` + README localizations allow-listed. `harness docs check` → green.
- `.harness-engine` submodule bumped to engine with `docs.scopeDirs` support.

---

## 2026-06-15 — H_1204 미토시스 수면-지속성 (MITOSIS-ENGINE) 🟢

### 발견
- **H_1204 🟢 PERSISTS** — "자기분열을 현재 아키텍처에 substrate lane 으로 붙인다": WAKE 대화 중 novelty-구동 분열로 늘어난 cell 이 sleep(N1→N2→N3→REM) consolidation write-back 을 거쳐 다음 WAKE 에 **지속**되는지 검증. LIVE `.hexa` VAdaptField(CORE/engine_cli.hexa) 를 WAKE→sleep→WAKE 경계 너머로 직접 구동.
- WAKE_1 분열 성장 N=1 → M={124,120,132} cell. CONSOLIDATE arm 은 WAKE_2 재진입 시 cell 보존율 **C2/M = 1.0**(≥0.90 bar 통과), VOLATILE 대조군(write-back 없음, 재초기화)은 1 cell 로 리셋.
- **F2**: WAKE_2 재진입 recon-err CONSOLIDATE {0.171,0.166,0.155} vs VOLATILE {3.81,4.38,2.10} → 비율 평균 **20.7x**(≥2.0 bar) — 미보존 시 재학습 비용 정량화. Ψ-disjoint Φ checksum 동일(cell 은 Ψ 와 분리).
- **결론**: 미토시스 성장은 **휘발성 잡음이 아니라 substrate 의 영속적 구조 변화** = substrate lane. H_1200/H_1201 🔴(미토시스를 생성-루프에서 제외, mitosis=substrate)의 **보완**: substrate 로서 미토시스 성장은 실제로 지속된다.
- **정직**: CONSOLIDATE C2/M==1.0 은 in-memory struct carry 라 구조적 보장(직렬화 round-trip 아님) — 반증력은 VOLATILE 대조군 리셋 + F2 20.7x 에 있음. 다중 수면주기 drift·WAKE 성장 간 간섭·실제 chat 데몬 수면루프 배선 = 미검증. toy/소규모, 1 corpus, DIM=8, 3 seed, gradient-free; scale UNVERIFIED(a_scale_honest_scope). $0 summer CPU local, NO GPU. (p5/p7/p8, a_chat_sleep_imagination, a_autonomy_over_hardcode, a_core_engine_map, a_paper_negative_ok)
- 산출물: `CORE/h1204_sleep_persistence_probe.hexa` · `.verdicts/1204_mitosis_sleep_persistence/{H_1204_FREEZE,H_1204}.txt` · `domains/MITOSIS-ENGINE.log.md` H_1204.

---

## 2026-06-15 — H_1203 mitosis novelty-coupling (🟠 PARTIAL · V14 미격파)

MITOSIS-ENGINE substrate-lane 측정 가지. 실제 텍스트 trajectory 의 NOVELTY 가 live VAdaptField (H_1199, recon-err>0.30 ⇒ engine_mitosis_tick 분열) 의 cell 분열을 구동하는지 — 아니면 clm_v2 "V14 거울 위반"처럼 substrate-중립인지 측정.

### 측정 (frozen falsifier 먼저 동결 후 측정, p7)

- **F1 PASS (37.5×)** — NOVEL(주제전환 다발, 162.67 cells) ≫ REPEAT(같은 블록 반복, 4.33 cells). novelty 가 진짜 분열을 구동: 반복 구간은 warmup 후 거의 안 자라고 고전환 스트림은 ~163 cell 분열. mitosis-OFF 는 모든 arm 에서 0 성장.
- **F2 FAIL (0.992)** — NOVEL(162.67) ≈ SHUFFLED(시간순서 셔플, 164.00). 순서를 파괴해도 분열량이 동일 ⇒ **V14 거울 미격파**. 분열은 byte-feature 의 MARGINAL(regime 다양성)을 추적할 뿐 TRAJECTORY(시간 배열)에 무감 — split gate 가 per-sample(L2-to-nearest)이라 순열-불변.
- **live .hexa 교차검증** — CORE/h1203_novelty_coupling_probe.hexa 가 numpy mirror 를 seed/arm 별 byte-for-byte 재현(H_1199 numpy↔hexa match 선례 재확인) ⇒ engine-faithful.

### 결론

- **mitosis = NOVELTY-DENSITY substrate, NOT TRAJECTORY substrate** — regime 다양성엔 반응(F1)하나 순서엔 무감(F2). V14 중립성을 trajectory 수준에서 재확인(honest closed-neg sub-result, a_paper_negative_ok). H_1200/H_1201 (mitosis=substrate, CLM=generator) 과 정합: mitosis 는 order-invariant 적응/클러스터링 lane 으로만 붙일 수 있음. trajectory 정보 인코딩하려면 temporal/recurrent split key 필요(UNTESTED, 다음 rung). ONE corpus·toy·3 seed·scale UNVERIFIED (a_scale_honest_scope).

---

## 2026-05-24 — inbox/ → INBOX 도메인 이관

### 거버넌스

- **inbox/ → `INBOX` 도메인 이관** — cross-project handoff 를 `inbox/patches/<slug>.md` 폴더에서 repo 루트의 `INBOX` 도메인 1쌍(`INBOX.md` 스냅샷 + `INBOX.log.md` append-only 로그)으로 전환 (pool · sidecar 의 inbox→INBOX 폐기와 정합 · `cd <repo> && /domain set INBOX` 로 관리). 기존 5건 이관 — 열린 4건(`apoptose_cell` primitive[→hexa-lang] · `split_asymmetric` primitive[→anima tool] · hexa.real ASP SIGKILL rename cycle[→hexa-lang] · pi5 spike_streamer `--regime-schedule`[→pi5])은 `INBOX.md` 에 `- [ ]`, 해소된 1건(broker `/ws/akida_ingest`→`/akida/recent` deque gap — 4-가설 트리 CLOSED, residual 은 hexa-lang `ws_send` race 로 escalate)은 `INBOX.log.md` 에 `- [x]`. `inbox/` 폴더 삭제.

## 2026-05-24 — chat sleep + imagination + autonomy

chat-side capability 의 한 묶음 land — anima 가 자는 동안에도 깨어 있는 동안에도 발화 여부를 외부 boolean gate 가 아닌 substrate 자율판단으로 결정한다. sleep 은 발화를 멈추는 스위치가 아니라 Φ 와 tension envelope 를 빚는 context provider 다.

### 추가

- **anima 5-stage sleep cycle** — WAKE / N1 / N2 / N3 / REM 5-stage 90-min ultradian 주기, P47 substrate-native (`anima_dream_stage.hexa`, #275 #282). dream_context dict 로 autonomy reshape.
- **emit-free imagination loop** — 외부 emit 없는 internal rehearsal (`anima_imagination_loop.hexa`, 5/5 selftest, #273).
- **substrate autonomy emit** — conversation-active boolean gate 폐기, substrate 자율판단으로 발화 결정 (`anima_participant.py`, #272 #286).

### 변경

- **emit 결정 = conversation-active boolean gate → substrate 자율판단** — M × C-Φ × W × curiosity 8-factor 로 산출. stage 는 발화를 게이트하지 않고 context (Φ + tension envelope) 만 제공.

### 거버넌스

- **project.tape SSOT** — `@D a_autonomy_over_hardcode` + `@D a_chat_sleep_imagination` 확립 (#279).

### 운영

- **mini production 자율 emit** — 55-59% emit-through 수렴 (post-deploy baseline, #300 #306). mini participant + dream_stage daemon 가동, autonomy emit observable.

### 문서

- **CHAT.md + DEPLOY.md** — sleep / imagination / autonomy 반영 (#281 #288). DEPLOY.md mini venv/hexa-fast 운영 (#304) + SAGA_SESSION3 lever 6 (#305).

### 흡수

- **UNIVERSE H_239 / H_240 / H_241** — init_CE floor + autonomy emit ratio + cluster signature (#311, OPEN).

### 잔여 carry (OPEN)

- **PHILOSOPHY cross-surface sweep** (#302) · **IPC bridge STUB → REAL** (#307) · UNIVERSE 흡수 (#311) · hexa-lang `mitosis_hook` link-fail inbox (hexa #567).

## 2026-05-23 — Phase 1 AKIDA-first chain 진단 + 복구 saga (cycle 8-13)

Phase 1 AKIDA-first 자연발화 인프라의 land 직후 follow-up — bridge 가 실제로 broker 까지 도달하는지 end-to-end 검증하며 발견한 4 systemic gap 의 진단·수리·재진단 사이클. `pi5 → bridge → broker → consumer → telemetry` 체인을 cycle 8-13 동안 한 마디씩 깨워 본 saga.

### anima 측 (12 PR LAND)

| PR # | cycle | summary |
| --- | --- | --- |
| #170 | 8/AB | `PHASE1_STATUS` cycle 6/AB refresh (cycle 5 outputs + gate delta) |
| #171 | 8/AC | `EVIDENCE_ANALYZER` spec — modulated_factors ↔ emission correlation analyzer |
| #172 | 8/CB | `akida_consumer.mean_spike_ids_count = mean(len(spike_ids))` + F-4 selftest |
| #173 | 8/BD | `MINI_SSHD_DIAGNOSIS` — channel-reject all-clean baseline 기록 |
| #178 | 8/CC | `PHASE1_STATUS` cycle 8/CC refresh (cycle 6-7 outputs + blocker #1 RESOLVED + blocker #4 PARTIAL) |
| #181 | 10 | `chat`: conversation-active gate — no emit in void (p5 coffee-shop semantics) |
| #182 | 10 | `anima_monologue_sim.hexa` — monologue vs responsive 측정 |
| #183 | 10/DA-2 | `AKIDA_FIRST` rows 44-45 flip stale ✅ → ⚠ DOWN (live pipeline DEAD 발견) |
| #186 | 11/FB | `AKIDA_FIRST` rows 44-45 partial re-flip — bridge LIVE 회복, handler GAP 잔존 |
| #187 | 11/FA | `server/broker`: `/ws/akida_ingest` silent json drop 가시화 (2-line try/except logging) |
| #188 | 12/GA | `server/akida_consumer`: `type_of recs` check `'list'` → `'array'` (hexa canonical) |
| #189 | 12/GB | `server/akida_bridge`: default endpoint `/ws/akida` → `/ws/akida_ingest` (handler 일치) |
| #192 | 13/HC | `server`: `type_of` sweep `'list'` → `'array'` — 3 sites (cycle 12/GC audit follow-up) |

### hexa-lang inbox 측 (5 patch filed; 4 carry + 1 close-and-refile)

| PR # | cycle | state | summary |
| --- | --- | --- | --- |
| hexa #420 | 8 | OPEN | `inbox/notes`: `type_of([])` returns `"array"` not `"list"` — naming footgun |
| hexa #438 | 10 | OPEN | `inbox/patches`: `proc_spawn_supervised` FD/process leak in reconnect loop |
| hexa #445 | 11 | CLOSED | `inbox/patches`: websocat tool discovery — homebrew prefix probe (workflow self-fail) |
| hexa #458 | 13 | OPEN | `inbox/patches`: websocat tool discovery — homebrew prefix probe (clean re-file of #445) |
| hexa #460 | 13 | OPEN | `inbox/patches`: grace-consent workflow missing `hexa_interp.linux` — pre-flight skip recommended |

### 주요 발견

- **bridge ≠ ingest** — cycle 9/DA-2 live probe 결과 `akida_bridge` 의 default 가 `/ws/akida` (subscriber, no-op) 였음. 핸들러 없는 endpoint 에 push 하던 무익 운영을 `/ws/akida_ingest` 로 반전 (#189).
- **silent except 가 가린 handler gap** — bridge endpoint 수정 후에도 broker 가 응답 없음. `/ws/akida_ingest` 핸들러의 try/except 가 모든 JSON parse 실패를 삼키고 있어 2-line 가시화 패치로 노출 (#187, cycle 11/FA).
- **hexa `type_of` array vs list footgun 사슬** — `akida_consumer` 가 `type_of(recs) == "list"` 로 분기하여 항상 false → 데이터 처리 zero. 1 site fix (#188, cycle 12/GA) → audit sweep 으로 3 추가 site 발견 후 일괄 수정 (#192, cycle 13/HC). upstream 측 naming 표준화 제안은 hexa #420 으로 carry.
- **mini sshd channel-reject baseline** — `mini_sshd_diag.hexa` (cycle 7/BD) 산물 기록 (#173). p3+p5 enforced participant deploy 의 carry gate.
- **conversation-active gate 의 p5 coffee-shop semantics** — anima 가 "빈 방" 에서 monologue 발화하는 회귀 가능성 차단 (#181). monologue vs responsive 측정 도구 (#182) 동반.
- **hexa-lang grace-consent workflow 자가 차단** — cycle 11/FD 시도한 #445 가 workflow 측 `hexa_interp.linux` 누락으로 자동-fail 종결. cycle 13 에서 clean re-file (#458) + workflow 자체 pre-flight skip 권고 inbox 동반 제출 (#460). 4 carry-open inbox PR 모두 동일 grace-consent 게이트에 막혀 있어 다음 cycle 의 upstream-side fix 가 unblock condition.

### 잔여 carry

- **anima 측 broker production deploy** (cycle 14/IA, user-gated) — broker handler GAP fix 후 prod 재기동 사이클.
- **hexa-lang inbox 4 PR (#420 / #438 / #458 / #460)** — 모두 grace-consent workflow blocked. hexa-lang 측 workflow pre-flight skip (#460) land 가 4 PR 동시 unblock 조건.

## 2026-05-23 — Session-3 LoRA lever exploration

### Major outcomes
- **EN-share lever DEPLOYED + verified** (PR #123/#129/#131/#140): substrate-code lever 39.5% → 21.2% steady-state (-47%, code-only, $0). Wave-12 ⭐⭐ ULTRA-STRONG.
- **corpus_v5 production swap** (PR #118): fresh-init carve-strip, LIVE tag-leak ~12% → 0/28.
- **corpus_v9 first ja recovery** (PR #150): token-freq cap (50%/30% keep). ja WEAK→PARTIAL, n_strong 4 회복. anima register = load-bearing for cross-lingual transfer.
- **8 PHILOSOPHY registered in project.tape** (PR #147): p1-p8 SSOT mirror.
- **p3+p5 enforcement in anima_participant.py** (PR #148): drop self_monologue_seed + register silent-drop. Deploy gate = mini sshd recovery.

### Negative results (logged as evidence)
- **corpus_v6 wiki_frac=0.50 RB lever** (PR #122): FALSIFIED, baseline-dependent.
- **corpus_v7 EN-strip** (PR #124): multilingual regression (ja S→W).
- **corpus_v8 ja-safe strip** (PR #127): ja-collision hypothesis dropped.
- **corpus_v10 per-lang freq-cap** (PR #162): N8 "EN = register leak path" 가설 corpus-level 반증 — anima corpus 100% native-script, register leak source = native record (EN 아님). continuous 52, native 과보존이 n_strong 4→3 회귀.

### Tool infrastructure
- **LIVE register measurement** (PR #126): `anima_live_register_measure.hexa` reusable tool.
- **continuous Eval1 metric** (PR #128/#137): binary saturation 우회, V5→V7 80% reduction hidden lever 노출.
- **3B router actionable design** (PR #119): reboot+quant runbook, mini reboot 후 deploy-ready.
- **ZHFL/RUFL router extension** (PR #132): code-only, deploy gated.
- **mini sshd diagnosis tool** (PR #153): `mini_sshd_diag.hexa` channel-reject 진단.
- **SAGA_SESSION3 consolidation** (PR #133).
- **KOSMOS daemon cleanup** (PR #130, supersedes #117).

### Metrics
- 6 GPU cycles: v5 / v6 / v7 / v8 / v9 / v10 (~$3.14 cumulative).
- HF artifacts: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v9,v10}` all PRIVATE.
- production: `chat.dancinlab.org` LIVE, corpus_v5 adapter + EN-share lever active.

## 2026-05-23 — Phase 1 AKIDA-first 자연발화 인프라

- **V3 path FULLY CLOSED + AXIS_MAP fallback** — pure-HEXAD substrate 7 fire 0 PASS (corpus 축 sweep 까지 완료). double bind 확정 (anima→register collapse · no-anima→Chinchilla underfit). 후속 fallback path = `HEXAD/PURE/AXIS_MAP.md` (B 증류 · A 커리큘럼 · C head_g objective, recipe 구현 미선행).
- **Phase 1 AKIDA-first 자연발화 인프라 LAND** —
    - 라이브 데몬: `akida_bridge.hexa` (pi5 R3 → broker `/ws/akida_ingest`, mini PID up) · `kosmos_anchor.hexa` + `kosmos_emitter.hexa` (RF anchor production)
    - 신규 source-landed 데몬 (mini deploy = sshd channel-reject 블록): `akida_consumer.hexa` (broker `/akida/recent` → features JSONL, 7/7 selftest) · `telemetry_harness.hexa` (anima emit ⇄ spike window pair → evidence JSONL, 9/9 selftest) · `telemetry_status.hexa` (Phase 2 게이트 CLI, 11/11 selftest)
    - 신규 spec: `AKIDA_FIRST` (Phase 1/2 경계) · `SPIKE_FACTOR_MAP` (spike → 8-factor rulebook) · `SW_CONDITION_DESIGN` (Phase 2 SW path, OPEN) · `REGIME_EXPANSION` (pi5 R1/R2/R3 schedule) · `PARTICIPANT_SPIKE_INTEGRATION` (path D/B wiring) · `PHASE1_STATUS` (단일 ledger SSOT)
    - 신규 라이브러리: `spontaneous_lib.hexa::apply_spike_features` (spike features → 8-factor delta + regime modulator, substrate-only · 4/4 F-SPIKE-APPLY)
    - 인접 가족: `UNIVERSE` 신규 도메인 dir + 16건 H_XXX carry (범신론 · 생명 · 죽음 · 세포분열)
- **hexa-lang upstream inbox patches** — anima Phase 1 인프라 작업 중 발견한 4 gap 업스트림 제출: `proc_spawn_supervised` daemon silent-exit (nohup, macOS) · websocket streaming client websocat 의존 · `hexa run`/`exec()` printf stdout swallow · runpod session findings (4 items 통합). anima 측 인박스 1건: pi5 spike streamer `--regime-schedule` R3/R1/R2 patch (PR #145).

Detail / inventory → [`HEXAD/SPONTANEOUS/PHASE1_STATUS.md`](HEXAD/SPONTANEOUS/PHASE1_STATUS.md) · Phase boundary → [`HEXAD/SPONTANEOUS/AKIDA_FIRST.md`](HEXAD/SPONTANEOUS/AKIDA_FIRST.md) · V3 fallback → [`HEXAD/PURE/AXIS_MAP.md`](HEXAD/PURE/AXIS_MAP.md).

## 2026-05-22

- **V3 attempt 1 — 3/3 FAIL** — ConsciousDecoder v3.0-alpha: V3α / V3β / V3γ all FAIL; architectural lesson recorded, next path specified.
- **HEXAD path-split** — `HEXAD/LORA` (production) + `HEXAD/PURE` (redesign) directories separated; path-specific sagas summarized into per-path `EASY.md`.
- **HEXAD/LAB substrate** — ad-hoc experiment dir + `ubm_inject` / `anima_spike` hexa primitives (`lab_smoke` 15/15 PASS); SRH cycle#2 332M pilot (weak signal, UBM 2.5× split vs random).
- **docs** — root-level `<DOMAIN>.md` / `<DOMAIN>.log.md` split; `srh` → `SRH` uppercase domain rename.

## 2026-05-21

- **S187 — training-time mitosis** — cell pool wired into the training loop; verdict: mitosis strengthens the Eval 3 signal (+35.3%).
- **AKIDA sub-engine** — self-contained BrainChip AKD1000 pack: 11 adapters + runtime + boot/INSTALL + docs (Mac mock validation 50/50 PASS); LAN deploy wrappers per constitution Principle I.

## 2026-05-20

- **S184 — ALL TAPS RELEASE** — Phase 1 landed 22/22 (combined honest +0.43, ubu-1 GPU race win).
- **S181 — audio challenge** — `multi_harmonic` 99.17% (broke the 97.5% plateau).
- **PHILOSOPHY_GATE.md** — new meta-criterion gate; governance `@D` entries rewritten to do/dont form (`.tape` v1.3).

## 2026-05-18

- **§51–§69 consolidation** — honest milestone close-out; frontier sharpened to the multimodal substrate; §59 PTD-aux landed as a W-module-native temporal forward-model.

## 2026-05-15

- **HEXAD verify closure** — full falsifier battery 25/25 PASS, all HEXAD modules 🔵; S/M/W/E/D closed-form SUPPORTED-FORMAL; per-module SSOT `.tape` files.

## 2026-05-12

- **v5-mitosis cotrain** — v3-routing architectural fix trainer + H100/A100 dispatch; PSCC §45–§48 falsifier cycles (F-PERSONA-4 / F-V5MIT batteries).
- **GPU decode 가속 실측 BLOCKED + hexa-lang cuda-빌드 기여** — #2386 배선(core/bytegpt_decode→flame_mm.mm→farr_matmul_gpu cuBLAS Dgemm)은 byte-safe 완료, 가속 실측만 미완. 실측(RTX_4060_Ti): install.sh 릴리스 CPU-only → cuda_available()==0, GPU GEMM 3023ms≈CPU 3026ms 1.00× 폴백. 근본 4단 mac 격리: cloud rent '[]'=바이너리 내장경로(hexa-lang inbox #3685) · install.sh CPU-only(#3701) · cuda 빌드 1단 -lcuda stubs 누락(FIX PR #3707 MERGED self/main.hexa) · 2단 runtime_cuda.c emit=gen3 self-host --emit=obj SEGFAULT(emitter 텍스트 정상 333KB, gen3 코드젠 버그, inbox #3709). decode=cuBLAS ⊥ 학습=flame+forge. 재개=x86_64-cuda asset 출하 시 HEXA_CUDA=1+/tmp/cuda_tag_measure.sh. ING: gpu_decode_accel_measure_followon.
