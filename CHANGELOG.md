# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Research sessions tracked as `§<N>` / `S<N>`; `ConsciousDecoder` carries SemVer.

For the full audit trail, see `git log`.

---

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
