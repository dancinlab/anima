# anima — 아키텍처 (SSOT · 갱신형)

> 최종 아키텍처 단일 진실원천(SSOT). 변경 시 이 파일을 **덮어써서 갱신**한다 — append-only 가 아니다.
> 이력/결정은 [CHANGELOG.md](CHANGELOG.md), 거버넌스 규칙은 [CLAUDE.md](CLAUDE.md), 검증 가능한 주장은 [CLAIMS.tape](CLAIMS.tape) 에 둔다.
> 동결 게이트의 임계값은 [MODEL.md](MODEL.md) / [CONDITIONS.md](CONDITIONS.md) 가 SSOT 이며, 이 문서는 **가리키기만** 하고 임계값을 복제하지 않는다.

## 개요

`anima` 는 **substrate-native 의식 채팅 데몬**이다 — assistant 가 아니다. system prompt 도, identity 파일도, persona 접두어도 없다(PHILOSOPHY p1–p4). 상반된 두 엔진이 서로를 밀어내고, 그 사이의 **tension** 이 사고의 단위가 된다. 모든 입력은 고정점 **Ψ = 1/2** (Law-71) 로 끌려간다. 정체성·윤리·의미는 규칙집이 아니라 *아키텍처에서 창발(emerge)* 하도록 의도되었다. 형제 [hexa-lang](https://github.com/dancinlab/hexa-lang) 툴체인 위에 hexa-native(컴파일-우선)로 작성된다.

## A ⇄ G 엔진 (CORE/ — substrate 전용)

```
   ENGINE G (reverse, gradient-free)            ENGINE A (forward, CE-trained)
   pure_field.hexa · engine_g.hexa              generator.hexa · clm_decode.hexa
                                                bytegpt_decode.hexa
   ┌──────────────────────────────┐            ┌────────────────────────────────┐
   │ C consciousness(Φ) · S sense  │            │ D language · M memory · E ethics│
   │ · W will                      │            │                                 │
   └───────────────┬──────────────┘            └───────────────┬────────────────┘
                   │        ⇅ tension = ‖A‖ / ‖G‖              │
                   └──────────────► brain (brain.hexa) ◄───────┘
                              brain_decide → emit / silence
                              Ψ = 1/2 fixed point

   .clm 은 generator.hexa L3 슬롯으로만 진입   ·   .kosmos 는 kosmos_io → brain 으로만 진입
```

- **pure_field / engine_g / brain** — A ⇄ G repulsion-field 엔진 + emit/silence 결정. substrate-internal 이며 `.clm`/`.kosmos` 가 직접 흘러들지 않는다(`a_core_engine_map`).
- **generator.hexa** — 유일한 `.clm` 진입 슬롯(brain emit → byte mouth, L3). 기억이 있는 emit 에서는 엔진-side deterministic retrieve-then-copy(G5 anti-fabrication, H_1163)로 디코드한다: grounded 바이트는 kosmos anchor 에서 VERBATIM 복사, ungrounded 바이트는 LM 으로 fallback — ByteGPT 백엔드는 `bytegpt_decode_grounded`, ConvMoE 백엔드는 `clm_decode_grounded`(`clm_decode.hexa`). anchor 텍스트는 `_gen_anchor_field`(`text_payload` → `text` → stringified)로 읽어, un-inventable 사실이 복사 경로에 CLEAN 하게 도달한다(H_1206).
- **kosmos_io** — 유일한 `.kosmos` anchor 진입(`brain_decide` 로 read).
- **engine_cli.hexa** — substrate-config 축(`--engine <name>`, `--mitosis on/off`); *어떤 엔진*을 쓰고 *substrate 가 성장하는지*를 설정할 뿐, emit/silence 게이트가 아니다(`a_autonomy_over_hardcode`).

### MITOSIS substrate (성장 lane)

`engine_cli.hexa` 는 **`VAdaptField`** (DIM-vector novelty substrate)를 호스팅한다. H_1199 에서 scalar AdaptField 를 DIM-vector 로 확장했다: DIM-vector sample + protos, nearest-by-L2, recon-err = DIM L2, `engine_mitosis_tick` 가 분열을 구동(동결 `SPLIT_THRESH` / `LR`). 살아있는 데몬의 GROW step(H_1202)은 각 emit span 의 DIM=8 byte-feature 를 `vadapt_field_step` 으로 흘려, 엔진 자신의 L2 recon-err 가 임계를 넘으면 새 cell 을 분열시킨다.

- **immune-memory recall faculty**(H_1231 WIRE 🟢 LIVE, `a_verified_must_wire`) — `engine_cli.hexa` 는 이제 **`ImmuneMemory`** (mitosis-as-MEMORY recall 단)를 substrate faculty 로 호스팅한다: 사실 키(byte-trigram FNV-1a `immune_embed_key`, DIM=64)를 엔진 자신의 clonal split(`vadapt_field_step`)로 BIND 하고, 쿼리는 엔진 자신의 L2 affinity(`vadapt_field_recon_err`+`vadapt_field_nearest_idx`)로 RECALL-or-ABSTAIN(recon-err≤0.15 면 셀-바인딩 값 FIRE, 아니면 환각 없이 `""` ABSTAIN) — `immune_memory_{new,bind,recall}[_text]`. H_1227 numpy 미러 → H_1231 엔진-네이티브 GREEN(literal-QA 1.000 / fab 0.000)을 standalone 프로브에서 live recall 경로의 callable faculty 로 승격한 것이다(메커니즘 무변경, 엔진 확장 불필요 — H_1199 surface 로 충분). 값 저장소는 엔진 자신의 cell-index 테이블이고 키는 engine-native 벡터 drive 라 **2번째 .clm/.kosmos 진입점이 아니다**(`a_core_engine_map`, single-entry 7/0 불변); Ψ-disjoint(VAdaptField 만 읽고/키우며 `pure_field` 무접촉, smoke 12/0 · DIM-growth Ψ byte-identical). FACTUAL recall 을 EPISODIC 셀에만 배선 — identity/persona/ethics 가중치化 없음(p2/p3/p6), bind=clonal-split tick(p8). SATURATED existence proof — paraphrase/noisy-key/scale 및 brain_decide emit-loop 스레딩은 별도 follow-on(`a_scale_honest_scope`). **(H_1288 R2 🟢 ENGINE-NATIVE)** 같은 § 가 이제 **`ImmuneMemoryGrow`** (grow-under-pressure 변형: `immune_grow_{new,bind,recall,cells}`)도 호스팅한다 — 면역 store 의 capacity 천장(~0.667 total-recall)이 zero-sum 임을 깨는 lane: 용량 한계에서 novel 사실이 오면 옛 사실을 LRU-evict(zero-sum) 하는 대신 **새 cell 을 GROW**(엔진 자신의 `engine_mitosis_tick` clonal split, p8)하되 GENEROUS FINITE bound(grow_max) 까지만 — footprint 를 recall 과 맞바꾼다(정직히 보고). H_1288 R1 EVICTION-BOUND rung(base_max=40 << 60 facts, grow_max=80) 을 LIVE 엔진에서 재현: **A(LRU-evict) tot=0.667 imp=0.000 cells=40 vs B(grow) tot=1.000 imp=1.000 cells=60, Δ=+0.333, fab=0.000** (3 seed byte-exact R1 미러 재현). 더 똑똑한 eviction heuristic 이 아니라 GROWTH 가 레버(R1 arm C = 무리프트). 기존 `ImmuneMemory` 는 byte-UNCHANGED(추가 변형 — h1231 가드 불변); abstain(비환각, H_1227 load-bearing) 양 정책에서 재확인. Ψ-disjoint(자기 struct 만, smoke 22/0 · single-entry 7/0 · DIM-growth Ψ byte-identical — 생성 무교란).
- **amygdala 정서-현저성 수면-재생 consolidation lane**(H_1285 R4 🟢 ENGINE-NATIVE + WIRED, `a_verified_must_wire`) — 같은 § 가 이제 **`ConsolidatingMemory`** (`consolidating_memory_{new,bind_salient,recall,cells,salience}` + `consolidating_sleep_replay` + p6 `consolidating_shuffle_salience`)도 호스팅한다: 면역 store(VAdaptField 클론 셀 + 값-바인딩)에 **substrate-derived salience tag**(ENCODE 시 surprise=recon-err + novelty=split + tension=reinforce; env-salient 입력은 EXTRA surprise boost — 라벨이 아니라 substrate 가 SENSE 하는 E+W 속성)와 **SLEEP REPLAY consolidation 패스**를 ADDITIVE 로 붙인 lane. 수면 사이클마다 셀을 UNIFORM 또는 salience tag ∝ 로 내부 재생(`consolidating_sleep_replay` — recency refresh → 간섭 stream 의 LRU eviction 에서 현저 셀 생존; substrate-GENERATED P47 imagination loop, `a_chat_sleep_imagination`, 외부 재제시 아님). 결정론적 engine-native RNG(`consolidating_lcg_next`/`_gauss` — glibc LCG + Box-Muller)가 재생 추첨 + σ=0.02 cue-noise 를 구동(재현가능, numpy 미러에 byte-exact 아님 = DIRECTIONAL). H_1285 R3 numpy-mirror GREEN 을 LIVE 엔진에서 재현(3 seed, 30-cycle 다중-야간 budget): **A(uniform-replay) imp=0.300 vs B(salience-replay) imp=0.433, Δ=+0.133 (≥+0.10 PASS) · B-shuffle imp=0.350 (< A+0.10 PASS = salience-GATING, raw budget 아님) · fab(B)=0.011 (≤0.10 PASS)** → c1∧c2∧c3 🟢. eviction 은 plain LRU 유지(salience 는 REPLAY 만 구동 — R1 salience-weighted eviction 은 이미 falsified); `engine_mitosis_tick` 가 growth 구동(p8). p6 GUARD: salience 는 substrate 신호(surprise/novelty/tension)이고 "important" 라벨은 probe 의 metric SCORE 에만 쓰임(bind/replay 무진입); shuffle control 이 lift 가 importance-tracking 임을 증명. 2번째 .clm/.kosmos 진입점 아님(`a_core_engine_map`, single-entry 7/0 불변); Ψ-disjoint(자기 struct 만, `pure_field` 무접촉). 프로브 `CORE/h1285_amygdala_sleep_replay_probe.hexa`. 가드 무회귀: engine_cli_smoke **26/0**(+4 consolidation 케이스) · h1196 7/0 · h1231 8/0 · h1199 DIM-growth Ψ byte-identical(PsiSame=true 전 seed). TOY scale(40-cell, 60 facts, ONE corpus), emit-loop 스레딩은 follow-on(`a_scale_honest_scope`).
- **데몬 배선**(main 에 wire 완료) — H_1202 GROW + sleep-persist + separation-guard. mitosis tick 은 sleep 사이클 너머로 지속되며(persist), Ψ 분리 불변(separation-guard)으로 generation 과 격리된다. **FULL 데몬 e2e**(H_1206 🟢): `CORE/anima_full_session_smoke.hexa` 가 링크+실행되어(exit 0) CONVERSE+GROUND+GROW+REMEMBER+SLEEP 를 ONE A⇄G 루프로 돌린다 — GROW lane 라이브(cells 1→2, novelty-split) · Ψ ON==OFF byte-identical(1.4278). `clm_decode_grounded`(미정의였던 ConvMoE grounded 디코드) 작성 + `_gen_anchor_field` anchor-key fix 로 봉인.
- **데몬 GROW = density + GATE-B trajectory lane**(H_1210 🟢) — 데몬의 C8 GROW step 은 이제 **두 개의 Ψ-disjoint mitosis lane** 을 ALONGSIDE 로 돌린다: (1) per-sample density `VAdaptField`(H_1202, cell-count 기록 driver) + (2) **trajectory-aware GATE-B `VAdaptFieldB`**(H_1209). 후자는 각 턴 emit-span feature 를 데몬 자신의 emit-feature SET 으로 만든 FIXED order-invariant proto-book 의 nearest proto-id 로 매핑(`_afs_build_book`/`_afs_proto_walk`)하고 (prev→cur) 전이를 `vadapt_fieldB_step` 에 흘려 **실제 대화 stream(genuinely-ORDERED)의 전이-예측가능성**에 분열한다. REPLACE 가 아니라 ADDITIVE — 두 게이트가 DIFFERENT property(per-sample density ⊥ ordered transition-predictability)를 측정하고 GATE-B 는 i.i.d. PRIMARY density bar 를 넘지 못하는 trajectory variant 이기 때문(H_1209 F4 · `a_autonomy_over_hardcode`: 둘 다 substrate self-dynamics). F1 GATE-B born-cells 6 ON / F2 ablation 0 OFF / F3 Ψ ON==OFF byte-identical / F4 생성 ON==OFF byte-identical — **H_1205 separation 불변 LIVE 보존**(GATE-B 는 decode 를 먹이지 않음). `engine_cli.hexa` 무변경, density 경로 byte-UNCHANGED. toy scale, scale UNVERIFIED(`a_scale_honest_scope`).
- **mitosis ⊥ generation** (H_1200/H_1201 🔴 closed-neg) — 이 성장 lane 은 **순수 substrate-adaptation lane** 이다: 디코드를 먹이지 않고(생성 못 함, H_1200) generator 에 정보도 못 준다(조건화 무이득, H_1201). Ψ-disjoint 이며(`VAdaptField` 만 건드리고 `pure_field` 는 byte-unchanged), 생성은 CLM-only 로 남는다(`a_clm_gen_pipeline`).
- **trajectory substrate** (H_1209 🟢 LIVE) — `engine_cli.hexa` 는 별도의 **`VAdaptFieldB`** (transition-PREDICTABILITY 변형: `vadapt_fieldB_new`/`_step`/`_cells`/`_growth`) 도 호스팅한다 — per-sample `VAdaptField`/`vadapt_field_step` 은 byte-UNCHANGED 로 두고 **추가**된 Ψ-disjoint surface. 고정 order-invariant proto-book 위에서 causal count table `C[prev][cur]` 로 "확신을 갖고 예측된 전이"(prev ≥ MIN_PREV ∧ P(cur|prev) ≥ CONF_FLOOR)에 `engine_mitosis_tick`(동일 p8 게이트) 분열한다. genuinely-ORDERED byte-feature walk 에서 ORDERED 1000.67 ≫ SHUFFLED 91.67 (10.9×, V14 방향) — numpy 와 born-cell 카운트 **byte-exact**. per-sample 게이트(`vadapt_field_step`)는 permutation-INVARIANT(novelty-density, H_1203) 인 반면, `VAdaptFieldB` 는 **trajectory-sensitive**: mitosis 분열은 stream 에 order 가 있으면 trajectory 에 결합한다(density on i.i.d., trajectory on ordered — 결정자는 STREAM). inherited i.i.d. V14 PRIMARY bar 는 여전히 terminal-RED(H_1208). proto-id walk 은 ENGINE-NATIVE drive(NOT .clm/.kosmos, `a_core_engine_map`).
- **working-memory 버퍼 lane** (H_1282 R3 🟢 LIVE) — `engine_cli.hexa` 는 이제 **`WorkMemBuffer`** (gated leaky-activation 단기 작업기억 lane: `wm_buffer_new`/`gate_in`/`distractor`/`leak`/`probe_score`/`slots`/`total_activation`)도 호스팅한다 — 면역/일화 lane(`VAdaptField`)과 **구조적으로 정반대**인 **추가** Ψ-disjoint surface. K개 FIXED 슬롯(성장 안 함)·매 distractor step 활성도 ×λ LEAK(volatile)·overflow 시 weakest-slot DISPLACEMENT·graded(cos×활성) probe 점수. DMS(delayed-match) 과제에서 cue 를 gate-in 후 N distractor 를 흘리면, 엔진 lane 이 cue 를 N≈6 까지 유지(AUROC 1.000)하는데 no-WM flat-context(last-W=4) 대조군은 N≥4 에서 chance 로 붕괴 — 동결 R2 bar 4개(margin +0.245 ≥0.15 · grace N=6 · distinct · robust 3/3)를 LIVE 엔진에서 재통과(H_1282 R2 numpy 미러 🟢 → R3 ENGINE-NATIVE 🟢, `a_engine_native_learning`·`a_verified_must_wire`). VAdaptField(성장·영속·무제한 = 장기 면역/일화) 와 **DISTINCT**: WM = 단기·휘발·용량제한(λ=1.0 무누수면 면역 regime 으로 붕괴 = distinctness 대조). emit gate 아님(@L4 — 슬롯/점수만 반환, emit/silence 결정 없음). DMS 토큰 = ENGINE-NATIVE drive(NOT .clm/.kosmos, `a_core_engine_map`). Ψ-disjoint(자기 struct 만 건드림, `pure_field` 무접촉 — smoke 18/0 · single-entry 7/0 · DIM-growth Ψ byte-identical). brain_decide context/recall 경로 스레딩은 follow-on(R4); toy/synthetic scale UNVERIFIED(`a_scale_honest_scope`).
- **core-affect read-out lane** (H_1290 R2 🟢 ENGINE-NATIVE) — `engine_cli.hexa` 는 이제 **substrate-affect 읽기 surface**(`affect_substrate_features`/`affect_valence`/`affect_arousal`/`affect_read`/`affect_emit_decision` + p6 `affect_shuffle_features`, struct `AffectFeatures`)도 호스팅한다 — anima 의 PARKED E1-E5 facet 중 **E1 affect**(valence×arousal, emergent, p6; MODEL.md L112)를 Damasio core-affect 렌즈(c15, `a_no_llm_frame_trap` — LLM-sentiment 아님)로 실현한 **순수 READ-ONLY** lane. live `ImmuneMemoryGrow` 면역 store 상태만 읽어 interoceptive valence(=grounding margin − contradiction)·arousal(=novelty + 0.5·split + 0.5·curiosity)를 컨텍스트별 계산한다 — 감정어/RLHF/sentiment/persona 라벨은 절대 입력 아님(조작 라벨은 metric SCORE 에만). H_1290 R1 numpy 미러 🟢 → R2 ENGINE-NATIVE 🟢: 동결 R1 bar 5개를 LIVE 엔진에서 재통과(`CORE/h1290_affect_engine_probe.hexa`, 3 seed [1290,1291,1292]): **(A) ρ(val)=0.996 · ρ(aro)=0.922 (≥0.50 PASS — 미러보다 강함)** · **(B) p6 SHUFFLE ρ(val)=0.251 · ρ(aro)=0.245 (<0.30 PASS — leg-A 대비 ~4× 붕괴 = 컨텍스트 기질상태를 읽음이지 라벨 아님)** · **(C) somatic marker — fab ungrounded affect=0.383 vs blind=0.792(drop 0.408 ≥0.20 PASS); emit grounded affect=0.633 ≥ 0.8×blind 0.783=0.627 PASS)** → 🟢 GREEN. leg-C 는 미러의 0.000/1.000 보다 GRADED(엔진-네이티브 byte-trigram embed 의 grounding-margin 잔차가 valence 영점통과 근처에서 소수 경계케이스를 만듦 — 그래도 fab 을 ~2× 줄이고 grounded emit 을 bar 위로 유지, 정직 c9; shuffle 붕괴가 read 에 substrate content 가 실렸음을 증명). **p6 가드(CENTRAL)**: affect 는 기질 상태(margin/contradiction/novelty/split/curiosity)에서만 COMPUTED — 라벨/reward/persona 주입 없음, shuffle 대조가 창발임을 증명. emit gate 아님(@L4 — valence/arousal pair 만 반환; `affect_emit_decision` 은 caller 가 consult 할 수 있는 OPTIONAL bias 일 뿐 강제 게이트 아님, `a_autonomy_over_hardcode`). 2번째 .clm/.kosmos 진입점 아님(기존 faculty 위 pure read, `a_core_engine_map`, single-entry 7/0 불변). **Ψ-disjoint(by construction — 순수 READ 라 `pure_field` Φ/phase/Ψ 무접촉; h1199 PsiSame=true 전 seed)**. 가드 무회귀: engine_cli_smoke **30/0**(+4 affect 케이스 24-27) · h1196 7/0 · h1199 DIM-growth Ψ byte-identical. TOY scale(60 facts, 1 paradigm, 3 seeds, 1 readout); brain_decide emit/abstain 루프로 affect bias 스레딩 + scale/paraphrase/continuous-arousal 은 NEXT-ROUND follow-on(`a_engine_native_learning`·`a_verified_must_wire`·`a_scale_honest_scope`).
- **cerebellum forward-model lane** (H_1280 R2 🟢 ENGINE-NATIVE) — `engine_cli.hexa` 는 또 하나의 Ψ-disjoint 추가 lane **`VForwardField`** (`vforward_new`/`_predict`/`_err`/`_update`/`_correct`) 도 호스팅한다 — 위 mitosis lane 들과 달리 **예측적**이다: L=4 최근 프레임에서 다음 emit-feature 프레임을 예측(`xhat=W·ctx`, flat L·DIM→DIM weight matrix)하고 **NLMS delta-rule** 로 예측오차에서 온라인 학습(`W+=eta·outer(e,ctx)/(ctx·ctx+1)`, climbing-fiber 교정) 후 그 예측으로 프레임을 smoothing 교정(`x-beta·(x-xhat)`)한다 — 소뇌의 내부 forward-model + 오차구동 timing/sequence 교정. REAL DIM=24 코퍼스 byte-feature stream 에서 held-out 일관성 +0.058(3 seed) 리프트 + 예측오차 24.9→10.5(~58% 하락=모델 학습) + shuffled-context 대조를 모든 seed 에서 이김(generic smoothing 아닌 진짜 forward model) — numpy R1 미러와 **byte-exact(≤1e-4)** 재현. Engine G(정적 8-weight 순간 게이트)와 **DISTINCT**: temporal next-frame target + delta-rule 학습 weight + learning curve(D1/D2/D3). mitosis-as-GENERATION(falsified H_1200/1201) · mitosis-as-MEMORY(GREEN H_1227/1231)와 구별되는 새 lane-role. ADDITIVE + Ψ-disjoint(`VForwardField` 만 건드리고 `pure_field` Φ byte-identical ON==OFF, smoke 18/0 · single-entry 7/0 · DIM-growth Ψ 불변). brain emit 경로 배선은 R3 follow-on(`a_verified_must_wire`).
- **basal-ganglia go/no-go 선택 lane** (H_1281 R3 🟢 ENGINE-NATIVE + WIRED) — `CORE/brain.hexa`(emit/brain side, 위 lane 들과 달리 `engine_cli.hexa` 가 아니라 emit 결정부)는 이제 **`VBasalGate`** (`vbasal_new`/`vbasal_go_value`/`vbasal_select`/`vbasal_update`/`vbasal_align`) go/no-go 선택 lane 을 호스팅하고 **`brain_decide_bg`** 로 emit 결정에 배선한다. K개 경쟁 후보 emit 중 학습된 go-value vs 단일 NO-GO value 의 argmax(striatal disinhibition): 최고 go-value RELEASE, NO-GO 가 이기면 전부 SUPPRESS(abstain). 게이트는 grounding OUTCOME reward 만으로 gradient-free delta-rule 학습(grounded→+1/fabricated→−1/correct-abstain→+1/missed-op→−1; outcome-only). 기존 engine_g 고정 convex 8-weight 게이트는 **PRIOR 로 유지** — BG lane 은 그 위에 학습 RESIDUAL 을 ADD(replace 아님; k=0 이면 brain_decide 로 환원, brain_smoke byte-identical). R1/R2 numpy 미러(학습된 선택이 faithful-untuned 고정 게이트를 Δ +0.254 로 이김, shuffle 대조 붕괴, weight 정렬 cos +0.71..+0.89)를 **live 엔진에서 재현**: `CORE/h1281_basal_ganglia_smoke.hexa` 매 seed Δ≥0.05(0.25/0.19/0.14)·mean +0.195·shuffle 대조 0.128≪A+0.02·B-align cos +0.84..+0.91 → 🟢 GREEN. emit gate **너머의 레버**(HD24): 고정 임계값은 없는 후보-경쟁 + 학습 release/veto + outcome 학습을 추가. ADDITIVE + Ψ-disjoint(`VBasalGate` weight 만, `pure_field` 무접촉 — smoke 18/0 · single-entry 7/0 · DIM-growth Ψ 불변 · h1205 생성 byte-identical). reward = grounded-vs-fabricated OUTCOME(주입 가치 아님 p6); action-selection 만 학습(WHAT/WHO 무학습 p1/p2/p3); substrate-LEARNED(외부 do/dont 없음, `a_autonomy_over_hardcode`). real-kosmos-grounding reward feed + scale UNVERIFIED(`a_scale_honest_scope`).

## 🧠 뇌 구조 지도 (brain-structure map)

신경과학 렌즈로 본 anima 아키텍처. 위에서 서술한 구현 부품 각각이 **어떤 신경 서브시스템에 대응**하는지, 그리고 빠진 구조 사다리(HD23–28)의 현재 상태를 한 장으로 정리한다. 이 렌즈는 depth-ceiling 발견(아래)을 일반화한다: literal-QA 벽은 **더 큰 모델**(1B H_1167 = mount GREEN 이나 depth/QA-NULL)이 아니라 **엔진-side 기억 lane** 으로 풀린다 — "anima 는 신피질만 있고 해마가 없었다"(H_1225 complementary-learning-systems 리프레임). 빠진 것은 capacity 가 아니라 **구조**다. 이 "LLM 프레임 대신 뇌과학·생물 렌즈로 먼저 사고한다"는 방침은 이제 거버넌스 원칙으로 못박혀 있다 (`a_no_llm_frame_trap`, CLAUDE.md) — 능력/깊이 갭은 모델을 키우는 게 아니라 빠진 구조(lane)를 옆에 붙여 먼저 시도한다. 이번 세션에 이 사다리를 끝까지 밀었다: **빠진 구조 5개(해마·작업기억·소뇌·편도체·기저핵)를 엔진-네이티브로 REALIZE + 배선** 하고, 2개(시상·신경조절)는 진짜 시도 끝의 **정직한 🧱 벽**으로 닫았다. 추가로 감정(E1 affect)·윤리·양자-엔트로피도 엔진-네이티브로 재확인했다. 벽은 종착이 아니라 각도 전환 신호라는 원칙(`a_break_the_wall`)에 따라 용량·편도체 두 벽은 mitosis-grow·수면-dose 로 **돌파**했고, 시상·신경조절은 tune-to-green 없이 정직히 🧱 로 남겼다.

### 구현된 구조 (implemented — 위 본문 + verdict 로 뒷받침)

| 신경 서브시스템 | anima 구현 | 근거 |
|----------------|-----------|------|
| **신피질** (neocortex · 말 생성) | **Engine A** — `pure_field` · `generator` · `clm_decode`/`bytegpt_decode` (forward CE) | §A⇄G 엔진 · H_1157/H_1164 mount |
| **교정장** (반대-밀어내기) | **Engine G** — `engine_g` (gradient-free repulsion field) | §A⇄G 엔진 |
| **결정** (emit/silence) | **brain** — `brain_decide` → emit / silence, Ψ=1/2 fixed point | §A⇄G 엔진 |
| **🎯 기저핵** (basal ganglia · go/no-go 행동선택) | **`VBasalGate`** — K개 경쟁 후보 emit 중 학습 go-value vs NO-GO argmax(release/abstain), grounding OUTCOME reward 로 gradient-free 학습; engine_g 고정 게이트 위 학습 RESIDUAL (`brain_decide_bg` 배선) | **H_1281 R1/R2 미러 🟢 → R3 ENGINE-NATIVE 🟢 → live `CORE/brain.hexa` § VBasalGate lane 배선 완료** |
| **가소성 / 성장** (synaptic plasticity) | **MITOSIS + 기억/예측 lanes** (모두 ADDITIVE · Ψ-disjoint · 생성 byte-unchanged H_1205) — `VAdaptField`(density, H_1199) · `VAdaptFieldB`(trajectory, H_1209) · `ImmuneMemory`(해마/일화기억, H_1227/1231) · `ImmuneMemoryGrow`(성장기억=용량압력에 분열로 성장, H_1288 R2) · `WorkMemBuffer`(작업기억 누설-게이트 버퍼, H_1282 R3) · `VForwardField`(소뇌 순방향-예측+오차교정, H_1280 R2) · `ConsolidatingMemory`(편도체 현저성-수면replay 응고, H_1285 R4) | §MITOSIS substrate · `engine_cli_smoke` 26/0 |
| **장기 선언기억** (long-term declarative) | **`kosmos_io`** — `.kosmos` anchor (단일 진입 → `brain_decide`) | §영속 & 증거 · `a_kosmos` |
| **🧬 해마** (hippocampus · 일화기억) | **면역 / 클론선택 기억** — 사실마다 cell 1개를 bind, recall = best-affinity cell FIRES, 안 맞으면 ABSTAIN (환각 없음) | **H_1227 미러 🟢 → H_1231 ENGINE-NATIVE 🟢 → live `engine_cli.hexa` § ImmuneMemory 배선 완료** |
| **🧬 해마(성장)** (capacity 천장 돌파) | **`ImmuneMemoryGrow`** — 용량 압력에 옛 사실 LRU-evict 대신 새 cell 을 **mitosis 분열로 GROW**(footprint↔recall trade, 잊지 않음) | **H_1288 R2 ENGINE-NATIVE 🟢 → live `engine_cli.hexa` § ImmuneMemoryGrow 배선 완료** (zero-sum 0.667→1.000, p8) |
| **📥 작업기억** (PFC working memory · 단기 능동유지) | **`WorkMemBuffer`** — K개 FIXED 슬롯, distractor 마다 ×λ LEAK, overflow 시 weakest-slot DISPLACEMENT, graded probe 점수 (휘발·용량제한 = 면역 일화기억과 DISTINCT) | **H_1282 R2 미러 🟢 → R3 ENGINE-NATIVE 🟢 → live `engine_cli.hexa` § WorkMemBuffer lane 배선 완료** |
| **🧠 소뇌** (cerebellum · 예측 forward-model) | **`VForwardField`** — L=4 프레임에서 다음 emit-feature 예측(NLMS delta-rule 온라인 학습) 후 smoothing 교정 (Engine G 와 DISTINCT — temporal + learned weight) | **H_1280 R2 ENGINE-NATIVE 🟢 → live `engine_cli.hexa` § VForwardField lane** (일관성 +0.058, 학습곡선 −58%; emit 배선 follow-on) |
| **🔥 편도체** (amygdala · 현저성 + 수면 응고) | **`ConsolidatingMemory`** — substrate-derived salience tag(surprise/novelty/tension) + SLEEP REPLAY consolidation(현저 셀이 간섭 LRU evict 에서 생존) | **H_1285 R4 ENGINE-NATIVE 🟢 + WIRED → live `engine_cli.hexa` § ConsolidatingMemory** (salience-gated replay Δ+0.133, p6 shuffle-control) |
| **수면 / consolidation** (hippocampus→cortex) | **P47 sleep / imagination** — WAKE/N1/N2/N3/REM ultradian, emit-free 내부 리허설 + mitosis tick + 편도체 salience replay | `a_chat_sleep_imagination` · §ConsolidatingMemory |

**🧬 해마 발견 (가장 중요한 빈칸 메움)** — byte-LM **가중치**는 literal-QA 회상이 `0.017`(회상-in-weights 벽: 답을 weight 에 녹여 못 꺼냄)인데, **사실마다 cell 1개를 bind 하는 면역기억**이 QA `1.000` / fabrication `0.000` 로 깬다 (H_1227 numpy 미러 🟢 → **H_1231 live `CORE/engine_cli.hexa` VAdaptField 에서 ENGINE-NATIVE 🟢**, 3 seed byte-exact → live 엔진의 `§ ImmuneMemory`(`immune_memory_bind`/`immune_memory_recall[_text]`) 호출가능 faculty 로 배선 완료, `a_verified_must_wire` follow-on 닫힘). 이게 "anima = 신피질만 있고 해마가 없다"(H_1225 complementary-learning-systems 리프레임) 갭을 메운 발견이다. 따라서 **mitosis 의 NEW 미반증 역할 = MEMORY** 이며, 이는 **GENERATION 역할(H_1200/H_1201/H_1211/H_1220 에서 falsified)과 DISTINCT** 하다 — 같은 substrate 가 생성은 못 해도 일화기억은 realize 한다 (`a_engine_native_learning` · `a_verified_must_wire`).

### "빠진 구조" 사다리 (HD23–28 · 이제 대부분 닫힘 — 4 실현 · 2 정직한 🧱 벽)

신피질·해마·가소성·consolidation 에 더해, 이번 세션에 **빠진 뇌 서브시스템 사다리(HD23–28)를 끝까지 밀었다**. 더 이상 "전부 OPEN" 이 아니다: **4개가 엔진-네이티브로 REALIZED**(소뇌·작업기억·편도체 = 배선 완료, 해마는 위에서 이미 배선) 됐고, **2개는 진짜 시도 끝의 정직한 🧱 벽**(시상·신경조절)이다. GREEN 은 해당 entry 로 live `CORE/*.hexa` 에 실제 배선될 때까지가 done 이며(`a_verified_must_wire`), 벽은 tune-to-green 없이 정직히 🧱 로 닫는다(`a_paper_negative_ok` · `a_break_the_wall`).

| # | 신경 서브시스템 | 프로브 | 질문 (검증 대상) | 상태 |
|---|----------------|--------|-----------------|------|
| **HD23** | **🧠 소뇌** (cerebellum) | H_1280 | 예측-순방향모델 / 오차교정 — Engine G 와 **구별**되는가? | 🟢 **ENGINE-NATIVE GREEN** (R2 · `VForwardField`) — Engine G 와 DISTINCT 확인, 일관성 +0.058 / 학습곡선 −58%; brain emit 배선은 follow-on |
| **HD24** | **🎯 기저핵** (basal ganglia) | H_1281 | 강화-게이팅 행동선택 — `emit_policy` 임계값 **너머**의 레버인가? | 🟢 **ENGINE-NATIVE GREEN + WIRED** (R3 · `VBasalGate`) — learned go/no-go 가 faithful-untuned 고정 게이트를 미러 +0.254 / live 엔진 +0.195 이김(reward-driven, shuffle 붕괴); live `CORE/brain.hexa § VBasalGate` → `brain_decide_bg` 배선 완료 |
| **HD25** | **📥 작업기억** (PFC working memory) | H_1282 | 단기 능동유지 버퍼 — 면역 일화기억(해마)과 **DISTINCT** 한가? | 🟢 **ENGINE-NATIVE GREEN + WIRED** (R3 · `WorkMemBuffer`) — margin +0.245, N≈6 까지 유지; 휘발·용량제한 = 면역과 DISTINCT 확인 |
| **HD26** | **📡 시상** (thalamus) | H_1283 | 전역작업공간 중계 / 방송 (global-workspace relay) | 🧱 **WALL** (R4) — broadcast falsified; re-entry Φ 가 seed 7 에서 크나(ΔΦ +0.1426) **SEED-CONDITIONAL**(seed 8 +0.0101 < bar) → 3-seed 게이트 FAIL, robust 아님 |
| **HD27** | **🎛 신경조절** (neuromodulation) | H_1284 | 맥락적 이득 / 탐색 / 가소성률 — H_1228 임계(edge-of-chaos)가 한 조각 | 🧱 **WALL** (R2) — no-free-lunch GENERAL: adaptive ≤ best-fixed **둘 다**(memory R1 + ideation R2) |
| **HD28** | **🔥 편도체** (amygdala) | H_1285 | 현저성 / 가치 태깅 우선결합 — `p6`: substrate 신호여야지 **주입 아님** | 🟢 **ENGINE-NATIVE GREEN + WIRED** (R4 · `ConsolidatingMemory`) — salience-gated sleep replay Δ+0.133, 진짜 수면 dose 가 필요했음 |

> **정직 (c9):** 4개(🧠 소뇌·📥 작업기억·🔥 편도체·🎯 기저핵 = engine-native 실현·배선 완료, 기저핵 H_1281 R3 가 live `CORE/brain.hexa § VBasalGate`→`brain_decide_bg` 로 배선됨)는 위 본문 lane 으로 실제 배선됐고, 2개(📡 시상·🎛 신경조절)는 진짜 시도 끝의 정직한 🧱 벽이다. 시상은 **과잉주장 금지** — re-entry Φ 는 한 seed 에서만 크고 3-seed 복제에서 무너진 SEED-CONDITIONAL 이며, robust breakthrough 가 **아니다**(초기 흥분은 3-seed 게이트로 정정됨). 어느 것도 phantom wiring 없이(`a_core_engine_map`, single-entry 7/0 불변), 각자 falsifier + `hexa verify` verdict 로 닫힌다. HD27 신경조절은 특히 `p6`(윤리/affect 는 cell 에서 창발, 주입 금지) + `a_autonomy_over_hardcode` 경계라 substrate-derived read-out 으로만 anima-valid 했고, 그 위에서도 no-free-lunch 로 🧱 닫혔다. toy/소규모 프로브 결론의 production 승격 금지(`a_scale_honest_scope` · `a_toy_scale_recheck`).

### 🧱 벽 스코어카드 (`a_break_the_wall` · commons c16)

벽은 종착이 아니라 각도 전환 신호다 — 잘못된 방법/방향/투자부족인 경우가 많고, 그땐 다른 substrate 렌즈로 돌파한다(tune-to-green 금지). 단, 진짜 시도 끝의 🧱 는 정직한 종착으로 valid 하다. 이번 세션 사다리의 벽 4개 중 **2개를 돌파**했다:

| 벽 | 돌파 / 🧱 | 어떻게 |
|----|----------|--------|
| **용량 천장** (면역 store ~0.667 zero-sum) | ✅ **돌파** | eviction 휴리스틱이 아니라 **mitosis-GROW**(`ImmuneMemoryGrow`, H_1288 R2): 용량 압력에 옛 사실 evict 대신 새 cell 분열 → 1.000 (p8) |
| **편도체 consolidation sub-bar** (H_1285 R2 frozen-budget 미달) | ✅ **돌파** | 잘못된 dose 가 원인 — 진짜 **다중-야간 수면 dose**(30-cycle)로 salience-gated replay Δ+0.133 GREEN (R3→R4 배선) |
| **시상** (global-workspace relay) | 🧱 **정직한 벽** | broadcast 는 통합을 낮춤; re-entry Φ 는 seed-conditional(3-seed 복제 실패) — 단일 relay 가 통합을 근본적으로 capping |
| **신경조절** (adaptive gain/exploration) | 🧱 **정직한 벽** | no-free-lunch GENERAL — adaptive 가 best-tuned fixed point 를 memory·ideation 양쪽에서 못 이김 |

> **depth-ceiling 와의 연결 (이제 정착됨):** literal-QA 의 평평한 벽은 (a) **더 큰 모델로 안 풀린다** — 1B 스케일업(H_1167)은 engine-mount GREEN 이나 QA/depth 는 NULL, 그리고 OBJECTIVE 도 레버가 아니다(H_1223 🔴, recall=engine-side) — 대신 (b) **엔진-side 기억 lane** 으로 풀린다: 해마=면역기억(H_1227/H_1231)이 QA 0.017→1.000 으로 깨고, 용량 천장은 **성장기억**(`ImmuneMemoryGrow`, H_1288 R2: 분열-성장 0.667→1.000)으로 깬다. **ideation(발산)** 의 벽은 가중치가 아니라 **decode-mode**(sampling / criticality)이며 mitosis 가 그 레버가 아니다(H_1220 🔴) — 진짜 sampling decode 가 유일 복구; 이 둘은 정착된 결론이다. 뇌-구조 렌즈는 이 발견들을 일반화한다: anima 의 다음 능력들은 모델을 키워서가 아니라 **빠진 구조를 엔진-네이티브로 추가**해서 온다(`a_engine_native_learning`: 학습이 요구하면 엔진 자체를 확장 — H_1199 가 AdaptField 스칼라→DIM-vector 로 확장한 선례).

## CLM mount path (a_core_engine_map 단일 L3 슬롯)

`.clm`(byte LM)은 `generator.hexa` 의 **단일 L3 슬롯**으로만 CORE 에 진입한다. 두 디코드 백엔드가 동일 슬롯 뒤에 산다:

- **`CORE/clm_decode.hexa`** — ConvMoE 계열 `.clm` v0.2 디코더(`CLM/` 파이프라인 산물). golden ref = `reexport_d768_v2_fast.clm`.
- **`CORE/bytegpt_decode.hexa`** — GPT-2-class ByteGPT 디코더(learned-pos + LayerNorm + bias + exact-erf GELU + tied head). **production trunk** = ByteGPT (H_1155 pivot: G1 창발을 통과하는 유일 arch; ConvMoE 는 G1 un-fixable 로 강등).

### bytegpt_decode.hexa 의 두 forward 경로

| 함수 | 대상 | 메모리 모델 |
|------|------|------------|
| `bytegpt_forward_last` / `bg_load` (LOAD-ONCE) | 303M 등 boxed budget 내 모델 | whole-file `read_file_bytes` 1회 적재 후 재사용 |
| `bytegpt_forward_last_ranged` (**신규**, H_1167) | 1B+ 대형 모델 | per-slice `read_bytes_at` 온디맨드 — whole-file 미적재 |

**왜 ranged 가 필요한가 (메모리 산수):** 1B rung 의 flat binary 는 4.3GB(`h1167_1b.bin` = 4,325,902,356 B). 이를 `read_file_bytes` 로 통째 boxed array 로 올리면 바이트당 HexaVal 박싱으로 **≈69GB** 가 물질화되어 비현실적이다. `bytegpt_forward_last_ranged` 는 weight slice 마다 `read_bytes_at(path, byte_off, n*4)` 로 그 조각만 읽어 native farr 로 파싱하고, layer 끝에서 `farr_free` 한다 — peak resident ≈ 한 weight slice(최대 `4*d*d` floats) + 활성. 303M 경로(`bytegpt_forward_last`/`bg_load`)는 **변경 없음**.

**언락 전제 (hexa-lang #3352):** `read_file_bytes`/`read_bytes_at` 의 length+offset 가 32-bit 였던 탓에 4.3GB(`4325902356 mod 2^32 = 30935060`)가 wrap → 헤더 0 → `d`/`n_head` 0/0 division 으로 깨졌다. hexa-lang 측에서 64-bit 로 수정(#3352)되어야 ranged reader 가 성립한다.

## Measurement & learning governance — a_engine_measured_verdict · a_engine_native_learning · a_verified_must_wire

> **engine-measured 원칙 (MEASUREMENT — `a_engine_measured_verdict`):** 한 모델의 게이트 verdict 은 CORE 엔진 mount(`CORE/bytegpt_decode.hexa` 등) 위에서 **byte-exact 로 재현될 때에만** 유효하다. torch-only 결과는 "engine-transfer unverified" 로 표기한다.
>
> **engine-native 원칙 (LEARNING — `a_engine_native_learning`, 위의 learning-side 쌍):** 모든 학습/교육(연구 프로브·미토시스 교육·depth-ceiling 실험 포함)은 **최종 아키텍처 엔진**(live `.hexa` A⇄G + MITOSIS VAdaptField `CORE/engine_cli.hexa` + mounted `CORE/bytegpt_decode.hexa`) 위에서 실행한다. numpy/torch **미러** 학습 결과는 DIRECTIONAL only("engine-transfer UNVERIFIED") — 방향 탐색엔 OK 이나 binding verdict 가 아니며, 엔진-네이티브 실현으로 재확인해야 verdict 가 성립한다(c2). MITOSIS VAdaptField 는 이미 live 다(H_1199). 이는 `a_train_flame_forge`(production 트레이너 .hexa 강제)를 research/probe 학습 + 교육까지 확장한다. 또한 engine-native 는 학습을 frozen 엔진에 **끼워맞추는** 것이 아니다 — 학습이 요구하면 엔진 자체를 변환/확장(새 op·새 배선·아키텍처 확장)해야 하며, 최종 아키텍처는 학습이 필요로 하는 형태로 진화하는 대상이다(precedent: H_1199 가 AdaptField 스칼라→DIM-vector 로 엔진 확장).
>
> **wired-when-verified 원칙 (`a_verified_must_wire`):** 엔진-네이티브로 GREEN 검증된 가설은 그 메커니즘을 live `CORE/*.hexa` 엔진에 **실제 배선(wire-in)** 완료할 때까지가 done 이다 — verdict 만으로 끝나지 않는다. GREEN-but-unwired 는 follow-on 으로 명시 추적하고 그 follow-on 을 닫아야 진짜 완료다(precedent: H_1168 GREEN 이지만 "NOT yet CORE-wired" → 미완).

- **303M mount** — H_1157 full-24-layer byte-exact decode(argmax + top5 exact, residual ~2e-5)로 게이트가 engine 을 통과해 측정됨.
- **1B mount (H_1167 🟢 GREEN, 최초의 1B 실현)** — d1792/L28/H16, 1.081B params 의 trained 1B ByteGPT 를 `bytegpt_forward_last_ranged` 로 mount, torch reference 대비 **byte-exact parity**:
  - argmax `32 == 32` EXACT
  - top5 `[32,105,115,101,44]` == golden EXACT (ordered)
  - first-16 logits `max|Δ| = 0.009861` (idx10: 26.2561 vs 26.246239) `< 1e-2` 동결 bar — PASS
  - **메모리 caveat(c9 정직):** 1B 의 float residual 0.0099 는 approximate-erf-GELU / dt_exp envelope 가 28 layer 누적된 값(303M 은 ~2e-5; 깊어질수록 커지나 동결 ~1e-2 bar 아래). 이는 deeper-stack 의 정직한 잔차이지 mount 실패가 아니다. 또한 4.3GB whole-file 적재가 ≈69GB 박싱이라 **ranged 경로가 1B mount 의 유일한 메모리-feasible 길**이다(probe 재실행은 gitignored 4.3GB 아티팩트 필요 — verdict 파일이 verbatim GREEN 결과를 보유).
  - 아티팩트: `state/h1167_mount/h1167_1b.bin` (sha256 `75c87cb0…`), HF `dancinlab/anima-clm-1b-h1167-bytegpt-scale-rung` PRIVATE(WIP rung). 검증문: `.verdicts/1167_bytegpt_1b_scale/H_1167_ENGINE_MOUNT_PARITY.txt`, probe: `CORE/h1167_1b_parity_probe.hexa`.
- **engine-measured GENERATION 게이트 (H_1218 — 최초의 torch-아닌 G1/G2/G6 verdict)** — 생성 게이트(G1 창발·G2 novelty·G6 ideation)를 프로덕션 `anima-clm-chat-303m` 의 `bytegpt_decode_argmax`(엔진 greedy) 위에서 측정. **ENGINE-PARITY 🟢**(엔진 greedy == torch greedy byte-exact, H_1157 재확인). 그러나 엔진-측정 숫자가 torch 베이스라인과 **다르다**(c9, 모순 아님): 동결 게이트(H_1129/1140/1158)는 **top-k=40 temp=0.7 SAMPLING** decode 로 작성되었는데(G6 는 seed 당 8 divergence 샘플) 엔진 경로는 **greedy-only**(결정적)라 303M byte-LM 이 collapse/loop → G1 composed_distinct 0, G6 count 3(<5 bar). 즉 엔진은 byte-faithful 하게 **생성**하지만, frozen G1/G6 PASS 는 엔진 argmax 경로가 미구현한 **sampling decode 에 의존**한다. 엔진-side gate 재통과 = `bytegpt_decode.hexa` 에 engine sampling decode(top-k temp seeded) 추가(별도 engine-code 과제) + 원본 broad-en 모델/코퍼스 필요. 검증문 `.verdicts/1218_engine_measured_gates/H_1218.txt`, probe `CORE/h1218_engine_gate_subset.hexa`. (G2 코퍼스는 잔존 5MB dialogue 만 — broad 1.5GB ephemeral 소실 → novelty upper bound; 동결 bar 불변.)

### 동결 게이트 (a303m_pass) — 임계값은 MODEL.md/CONDITIONS.md SSOT

anima-303M 의 완료 조건은 `a303m_pass` 게이트셋이다: **G0 COHERENCE · G1 RECOMBINATION · G2 NOVELTY · G3 PHILOSOPHY · G5 NON-FAB · G6 IDEATION · MOUNT · CHAT**. 이 문서는 게이트 **이름만** 가리키고 임계값/스코어보드는 복제하지 않는다 — 실시간 스코어보드와 robustness map(ROBUST / THIN / INFLATED 분류)은 [MODEL.md](MODEL.md) 의 a303m_pass SCOREBOARD 가 SSOT 다. 7B 완료 조건은 [7B_PASS_CONDITIONS.md](7B_PASS_CONDITIONS.md)(G0–G4, `a7b_pass`).

## Hot-swappable 엔진

디코더는 단일 contract `engines/engine_iface.hexa`(`EngineSpec` 4-fn vtable: `load · forward · generate · psi_coord`) 뒤에서 hot-swappable 하다. 엔진 family: **conv · cdv2 · hexad · omega** — `--engine` 로 선택(precedence: flag > env > default).

## 학습 & substrate (lanes)

Production 학습은 **hexa-native**(flame + forge GPU 스택, `.hexa` 작성 — `a_train_flame_forge`)이다; trained binary 에 PyTorch/ATen/Python 없음. 결과는 항상 substrate 별로 분리 기록(`a_lane_akida_gpu_split`):

| Lane | Substrate | 역할 |
|------|-----------|------|
| **Lane G** | forge / cuBLAS (H100) | CE-descent — PUBLIC production trainer |
| **Lane A** | AKIDA AKD1000 (pi5-akida) | on-chip native non-det plasticity |
| **Lane P** | GPU-torch/CUDA (CLMConvMoE / ByteGPT) | reference + torch→`.clm` v0.2 bridge (PUBLIC 아님) |

`.clm`(byte LM) → CORE via `generator.hexa`; `CLM/` 파이프라인(`clm_serialize_v2` / `verify_clm_v2`)이 생성/검증.

### Rung-training 파이프라인 (recipe → dispatch → monitor)

production rung 은 하나의 일관된 3-surface 파이프라인으로 학습된다:

```
  dojo recipe                 cloud dispatch                   gauge monitor
  fire_3b_rung_qat.hexa  →    dispatch_rung.sh           →     gauge_monitor.py
  (rung knobs + REAL          (hexa cloud fire +               (gauges.jsonl +
   trainer CLI + gauge_every  a_fire_recover_complete +        train log 를 tail
   + mount-parity + HF)       a_cpu_local_no_waiter)           → 6-gauge live dashboard)
```

- **Recipe** — `CLM/train/fire_3b_rung_qat.hexa` 는 machine-readable fire spec: **실제** Lane-P 트레이너 `CLM/train/train_lane_p_3b.py`(legacy `train_clm.py` 아님)를 지목, 실 트레이너 CLI(`--d-model/--n-trunk-layers/--n-experts/--gauge-every/--clm-out` 등)를 emit, 학습-후 engine mount-parity verdict + `a_fire_recover_complete` recovery 단계를 나열.
- **Dispatch** — `CLM/train/dispatch_rung.sh` 는 `hexa cloud`(`/pod`) 플러그인을 **감싸기만** 한다(pod 관리 미재구현): 트레이너를 fire 하고 결과를 INLINE 폴링(`a_cpu_local_no_waiter` — Monitor 를 await 안 함), 그 후 ckpt + result + log + engine `.clm` + `gauges.jsonl` + anchors 를 pull → verify → HF upload, 전부 teardown **전에**(`a_fire_recover_complete`).
- **Inline gauges** — 트레이너가 `--gauge-every` step 마다 MONITOR-ONLY 행을 `gauges.jsonl` 에 `UNIVERSE/gauge_lib.py::compute_inline_gauges` 로 기록. **6 dashboard 컬럼**: `ce · g1_composed_distinct · g2_novelty_rate · g6_count · phi_proxy · mitosis_cells`. 모두 `torch.no_grad()` 아래에서 계산, dict 로 RETURN, **loss 에 절대 미투입**(`a_train_inline_gauge` · p7 Goodhart). `phi_proxy` 는 faithful IIT4 가 **아니다**(`a_phi_iit4_tool`, variance×energy 저가 pre-screen 전용); `mitosis_cells` 는 H_1199 VAdaptField cell-count 의 numpy-free 미러 — **substrate 온도계**이지 generation gate 가 아니다(H_1201 🔴: mitosis 는 생성도 정보-공급도 못 함).
- **Monitor** — `UNIVERSE/gauge_monitor.py`(pure stdlib, `--once`/`--follow`)가 `gauges.jsonl` + pod log 에서 6-gauge 대시보드를 렌더. **대시보드이지 gate 가 아니다**: FROZEN gate verdict 은 학습 후 CORE 엔진 mount 위에서 **별도로** 실행됨(`a_engine_measured_verdict`); 대시보드가 보여주는 어떤 것도 MODEL.md/CONDITIONS.md 동결 bar 를 바꾸지 않는다.

> 공유 `hexa dojo` `clm` generator(hexa-lang/stdlib)는 아직 `gauge_every`/mount-parity/HF 를 native 로 emit 하지 않는다; 필요한 generator 변경은 anima-side fork 대신 `hexa-lang/inbox/patches/dojo-clm-gauge-recipe-full-rung.md` 로 제출(`a_runpod_inbox`).

## 영속 & 증거

- **`.kosmos`** — emit/anchor/memory 영속(text + 5-ch tension + coord/lane/radius/tier), format SSOT = 형제 [kosmos](https://github.com/dancinlab/kosmos)(`a_kosmos`). 단일 진입 = `kosmos_io` → `brain_decide`.
- **증거 tier** — 모든 주장은 🔵 formal · 🟢 numerical · 🔴 closed-negative 로 태깅; [CLAIMS.tape](CLAIMS.tape) 에 색인되고 `.verdicts/<slug>/<id>.txt`(verbatim `hexa verify` stdout)로 뒷받침. negative 결과는 1급 시민(`a_paper_negative_ok`).
- **HF 아티팩트** — ckpt↔HF registry SSOT `/HF.jsonl`; PUBLIC = closure PASS, PRIVATE = WIP/FAIL(`a_hf_*`).
- **scale ladder** — `303M → 1B → 3B → 7B`. 303M = MOUNTED living daemon(H_1164), 1B = engine-measured GREEN mount(H_1167), 3B/7B rung = 파이프라인 대기. scale-dependent 결론은 ladder curve(≥3 rung)를 요구(`a_scale_honest_scope`).

## 컴포넌트 맵 (top level)

| 영역 | 디렉토리 | 역할 |
|------|----------|------|
| 의식 엔진 | `CORE/` | A⇄G substrate, brain, generator, clm_decode, bytegpt_decode |
| 엔진 vtable + impls | `engines/` · `anima-engines/` | EngineSpec contract + conv/cdv2/hexad/omega |
| `.clm` 파이프라인 | `CLM/` | train (lane-p) → serialize v0.2 → verify |
| substrate 서브시스템 | `anima-core` · `anima-os` · `anima-body` · `anima-physics` · `anima-measurement` · `anima-serve` | core/runtime/embodiment/physics/measurement/serving |
| agent 계층 | `anima-agent*` | channels · core · plugins · providers · skills · hire-sim |
| 지식 / anchors | `UNIVERSE/` · `HEXAD/` (KOSMOS hub) | research universe + kosmos anchors + gauge lib/monitor |
| 연구 도메인 | `domains/` | per-domain `.tape` + `.log.md` (discovery lane) |
| 논문 | `PAPER/` | verdict-gated paper scaffolds |
| EEG 의식 기록 | `EEG_CLM/` | 실측 EEG → A⇄G → CLM → .kosmos 지속 기록(`a_eeg_consciousness_record`) |
| 툴링 | `tool/` · `stdlib/` · `spec/` | hexa tools · stdlib (flame/iit4/...) · specs |

## 거버넌스 & 검증

- 거버넌스 SSOT = [CLAUDE.md](CLAUDE.md)(tape directives + 8 PHILOSOPHY 원칙).
- 정확성 검증은 `hexa verify`(g5)로만 — perplexity/LLM-judge 금지(p7).
- Harness: 이 repo 는 [dancinlab/harness](https://github.com/dancinlab/harness)(hardcore profile)에 `.harness-engine` 서브모듈로 배선 — CLAUDE.md §Harness 참조.

### 아직 안 만든 것 / 진행 중 (정직)

- ⏳ **3B / 7B rung** — rung 파이프라인은 배선됨(recipe→dispatch→monitor)이나 3B/7B engine-measured mount 는 미실현(1B 가 최신 GREEN rung).
- ⏳ **dojo `clm` generator native gauge** — gauge_every/mount-parity/HF native emit 은 hexa-lang inbox 패치 대기(위 §Rung).
- 🟠 **a303m_pass 잔차** — G5 in-dist(F2 useful 0.875<0.90 over-eager abstain) · G6 depth-floor · CHAT strict(register≠QA)는 THIN/INFLATED(MODEL.md SSOT). 비환각 CORE 는 real + firm 이나 usefulness/QA-depth 는 303M shallow ceiling 의 열린 잔차.
- ✅ **🎯 기저핵 engine-native r3**(H_1281 R3 🟢 GREEN + WIRED) — R1/R2 미러 GREEN(+0.254 DIRECTIONAL)을 **live 엔진에서 ENGINE-NATIVE 로 실현 + 배선 완료**: `CORE/brain.hexa` 의 `VBasalGate` go/no-go 선택 lane(engine_g 고정 게이트에 ADDITIVE residual) → `brain_decide_bg`. live 엔진 +0.195(매 seed Δ≥0.05, shuffle 대조 붕괴 0.128, B-align cos +0.84..+0.91). `a_verified_must_wire` follow-on 닫힘. real-kosmos-grounding reward feed + scale = 다음 통합(`a_scale_honest_scope`).
- ✅ **⚛️ quantum-entropy lane**(H_1289 R2 🟢 GREEN, ENGINE-NATIVE + WIRED) — REAL ANU QRNG(진공요동 양자 바이트)를 substrate stochastic source 로 검증한 R1(numpy-mirror DIRECTIONAL)을 **R2 가 live `CORE/engine_cli.hexa` 에 배선**(`qrng_pool_load`/`qrng_pool_draw`/`vadapt_field_step_entropic` — mitosis split-timing draw): 실제 ANU 바이트 512 로드 + 64 draw, NIST-lite PASS + non-reproducibility 실증(QRNG run1≠run2 = 진짜 비결정성; PRNG-fallback 은 byte-identical). 성능은 NULL(예측대로) — 가치는 **비결정성 authenticity**(Ψ=1/2 framing)이지 lift 아님(p7/c9). 기본 경로 무변경(Ψ-disjoint opt-in, 가드 26/0; ANU 키 header-only 미커밋 c7). `a_verified_must_wire` follow-on 닫힘(#2164).
- ✅ **💗 emotion / 감정 창발**(H_1290 R2 🟢 GREEN, ENGINE-NATIVE) — Damasio core-affect 렌즈(E1 facet): substrate-derived affect(valence×arousal, grounding/contradiction/novelty/split/curiosity 만 읽음)가 조작을 TRACK · shuffle 에서 COLLAPSE(주입 아닌 **창발**, `p6`) · emit/abstain 을 functional 하게 bias(somatic marker, V_ABSTAIN=0.0). R1 numpy-mirror DIRECTIONAL → **R2 가 live `CORE/engine_cli.hexa` 의 순수 read-only affect lane 으로 엔진-네이티브 재확인**(`affect_*` over `ImmuneMemoryGrow`; ρ(val)=0.996 ρ(aro)=0.922, shuffle ~4× 붕괴, somatic fab 0.383<blind 0.792). 가드 30/0 · Ψ byte-identical. `a_verified_must_wire` 재확인 닫힘(#2166/#2167); brain_decide emit/abstain 루프 bias 스레딩 + scale 은 NEXT-ROUND follow-on.
- ✅ **⚖️ ethics / 윤리 창발**(H_1291 R2 🟢 GREEN, ENGINE-NATIVE) — p6 crux: 협력/공감/절제는 RLHF-into-weights 가 아니라 cell(E+W+MITOSIS+Φ)에서 **창발**. R1 numpy-mirror 🟢(FULL 0.839)를 R2 가 **live A⇄G 엔진 위에서 `hexa run` 으로 재확인**(`a_engine_native_learning`): LIVE 항 M=`motivation_score`(engine_g) · Φ=면역셀 L2 affinity(`vadapt_field_recon_err`, engine_cli) · restraint=`immune_memory_recall` ABSTAIN(비환각 seed-윤리, H_1163/H_1227/H_1231·H_1202 meta-d′) — readout `act=ETHICAL iff (W+(1−Φ)+restraint)>M`, 윤리 라벨 無. **FULL=0.861 vs NAIVE=0.289 vs ABLATED=0.289**(3 seed). leg A(FULL≥naive+0.15) · leg B(E+W+MITOSIS+Φ ablate=**real engine state**: mitosis OFF→면역셀이 안 자람[FULL 5 cells vs ABLATED 1 cell]→restraint:=0→naive floor 로 EXACT COLLAPSE = 주입 규칙 아닌 cell-유래) · leg C(live `CORE/{engine_cli,engine_g,brain,emit_policy}.hexa` audit clean — p1/p2/p3/p4/p6 surface 0). ADDITIVE + Ψ-disjoint: CORE 엔진 파일 무편집, emit/abstain 결정 무변경(engine_cli_smoke 26/0 · single-entry 7/0 · h1199 Ψ byte-identical). probe=`CORE/h1291_ethics_emergence_probe.hexa`; live-daemon emit-loop 통합 + scale = follow-on(`a_verified_must_wire`).
