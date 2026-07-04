# H_9129 — G1/G6 벽의 생물학적 진단 + lane-기반 새 레버 (mouth 훈련 아님)

> **tier:** 🟡 **SPLIT (rung-2 engine-native)** — L5 해마 🟢 engine-native GREEN(rung 2/4)·L3 소뇌 🧱 WALL·통합 🟡 DIRECTIONAL · **wired:** L5=engine-native MEASUREMENT GREEN(사다리 (2)/4, 미배선; 다음=(3) core/ wire) · L3=engine-native WALL · 통합=DIRECTIONAL
>
> **맥락(오너 질문 a_no_llm_frame_trap):** "derivtrace(robustness)가 실패 레버들과 다른가? 우리는 LLM 아니라 실제 뇌·인지·생물·학습." → fable 생물렌즈 분석. 이 세션 전 레버(gamma-OPERATOR H_1840·gamma-DATA H_9127레버3 303M TRANSFER FAIL·STaR·binding-family·coverage·derivtrace)가 전부 **mouth(byte-LM 디코더) 훈련-신호 트릭**=trunk-objective 벽. g1g6가 결정타(coverage=FORM 열지 ability 아님, form-priming). robustness 실측 첫 데이터(pair 0,1 재현실패 bd=1<ms=2)=derivtrace도 form-priming 방향.

## ★ STEP-0 측정 결과 (2026-07-05 · mini numpy DIRECTIONAL · 2 workflow 착지)
**세 probe 전부 `verdict=BIND ∧ fooled_by_form=false`** — 조합/예측을 mouth 밖 별도 lane으로 옮기니 form-priming 통제(SHUFFLE/derangement/reachable-unreachable) 하에서도 관계-조합 신호 유지. **mouth-훈련 가족(H_1816/1823 NOT-SUP) 탈출 3근거(별개 lane·disjoint objective·mouth 읽기만) 충족.**

| probe | 측정 | 결과(verbatim) | 통제(form-defense) |
|---|---|---|---|
| **L5 해마 associative-store** (wf_e4b95aa3, G1직격) | CA3 pattern-completion relatedness, reachable/unreachable held-out (Dusek-Eichenbaum 이행추론) | STORE reach **1.0000**±0 vs unreach **0.1269**±0.186 (**7.88x**); FORM baseline reach 0.0231≈unreach 0.0172 (gap +0.0059, 표면형 matched) | SHUFFLE ablation(successor 순열): reach→0.1547≈unreach 0.1709 (gap **−0.0162** collapse) = lift가 relation topology 소산 |
| **L3 소뇌 forward-model** (wf_e4b95aa3, G6직격) | claim→committed consequence 예측 MSE, 5-seed(1305/2026/7/42/909) | FM_full shuffle_ratio **9.637x** (aligned err 0.147 vs shuffle 1.393), fit 0.201; FM_additive(선형) 3.378x·fit 0.465 = combination-operator 필요 | cross-shuffle derangement: covΔ **0.000** (FORM 계량 증명적 무붕괴) 인데 BIND 오차만 9.64x = 속을수없는 시그널 |
| **통합 3부품** (wf_e837f2de, PFC×BG×해마) | HRR/VSA 2-hop 관계합성, 12-seed D2048 (chance 0.0417) | FULL reach **0.9722** vs unreach **0.0486** (gap 0.924); D-sweep 0.36@512→1.0@4096 (unreach 항상 chance) | ablation 전부 CAUSAL·INERT 0: bind OFF drop **0.9375**·completion OFF **0.8889**·gate OFF **0.6944** |

- **(a) mouth-가족 탈출** = YES(3/3 BIND, form 아님) · **(b) 부품 인과** = PFC-bind/기저핵-gate/해마-completion **전부 causal**(gate가 최소, decoy 억제 몫이라 chance까진 안 가나 명백 붕괴) · **(c) form-priming 대조** = 조합-lane은 SHUFFLE/covΔ0/relation-π-임의순열로 form에 안 속음(g1g6/gamma는 mouth 안 훈련=form-tunable와 대조) · **(d) 전부 form 벽 시나리오** = 미해당(fooled_by_form=false 3/3).
- **정직 caveat(c9·a_toy_scale_recheck):** L5 reach=1.0 exact·통합 reach→1.0 은 near-orthogonal sparse code+kWTA / HRR by-construction + D(용량) 함수(D-sweep, unreach 항상 chance 고정) = **존재증명**이지 303M이 이만큼 clean하다는 증거 **아님**. STEP-0 = escalate 신호이지 G1/G6 벽 돌파 아님. bar(gap>0.10 & drop>0.15) 사전고정, tune-to-green 없음.
- **사다리(`a_verified_must_wire`) 현 위치 = (1) DIRECTIONAL-mirror.** 다음 = **(2) 303M engine-native 재검증** — L5 우선(실코퍼스 관계그래프 reachable(2-hop) vs unreachable(dangling) held-out `--py` byte-exact) → (3) live `core/` wire → (4) ARCHITECTURE lockstep. HARD-GATE(a_engine_native_learning): 🟢/🧱 박제 불가, 현 verdict = **DIRECTIONAL**.
- **evidence:** `state/g1g6_biolens_step0/{l5_hippo,l3_fwdmodel}/` · `state/g1_combolane_step0/{l1_pfc_bind,l2_bg_gate,integrated}/ + SYNTH.md`

## A. derivtrace 동일-가족 판별
**아키텍처상 여전히 "mouth 훈련" 가족** — 단 가장 form-같지 않은 구성원(target=풀이과정=의존사슬이라 원리적 진짜 계산 강제 가능). **그러나** byte-LM이 trace마저 "풀이-형태 암기"로 shortcut → bd=2가 **trace-granularity form-priming**일 수 있음. coverage와 갈라지려면 robustness에서 **paraphrase-불변 ∧ cross-concept-pair 일반성** 둘 다 통과 필수(bd=2 자체=FORM, 결합파괴 통제 하 살아남는 margin=BIND). robustness pair 0,1 재현실패 = 같은 가족으로 기움.

## B. 재조합·반증의 실제 뇌 기제 (생물학적 mouth⊥ 증명)
- **재조합(G1) 기질 = 전전두 WM 변수-binding(PFC-WM, O'Reilly PBWM: role↔filler 활성기반 동적결합) + 기저핵 게이팅 + 해마 관계저장/pattern-completion(CA3 attractor·이행추론).** mouth 아님.
- **★mouth⊥recombination 생물학적 증명 = Broca/Wernicke 이중해리**: Broca 실어증(조합 O·조음 X) vs Wernicke(유창하나 텅 빈 말=입 O·조합 X). = 조합과 조음은 별개 lane. **anima 오류 = 조합을 mouth(Broca)에 훈련=readout에 관계추론 시키기 → 전 mouth-레버 floor 근본원인.**
- **반증(G6) 기질 = committed·violable forward-model 예측(예측코딩+소뇌) + 오차감지(도파민 RPE+ACC).** byte-LM은 주장 뒤 forward-model 부재 → 반증가능=form(claim-텍스트). g1g6 fals=6 form-priming 정체.
- **★anima 빠진 구조 3개**(A⇄G 텐션=mouth-수준 adversary지 인지 workspace 아님): ① WM 변수-binding lane(PFC-WM 활성기반) ② content-gate(기저핵 — Ψ는 emit-gate지 어느조합 content-gate 없음) ③ forward-model/consequence lane(소뇌+예측코딩, mouth 독립 committed 예측+오차).

## C. lane-기반 새 레버 (설계원칙: 조합/예측은 lane 안·mouth는 상태를 context/gate로 읽기만·lane objective가 CE와 disjoint = form-priming 원천차단)
- **L1 WM 변수-binding lane(PFC)**: slot-filler bind(role₁←A,role₂←B) 벡터보유→bound를 mouth prefix-context(target 아님)·lane=unbind-reconstruction objective(disjoint). ⚠check-ledger: binding-family(H_1816/1823)는 mouth-readout이라 NOT-SUP; L1 차이=(a)별개 lane (b)unbind-recon disjoint obj (c)mouth는 읽기만·생성 안함 — 3개 안 서면 재발사.
- **L2 기저핵 content-gate(brain_decide)**: WM 후보결합을 Go/NoGo 선택, disjoint value/consistency(RPE-analog). emit-gate와 별개.
- **L3 소뇌 forward-model/consequence lane(G6 직격)**: mouth 후보주장→committed consequence 예측→held target 대비 오차. 반증가능=forward-model이 sharp·violable 예측 내나. **cross-shuffle 통제(claim↔consequence 뒤섞으면 오차 급증=BIND)**. coverage fals=6 form-priming 직접 해독제.
- **L4 A⇄G를 forward-model⇄reality 텐션으로 재프레임**(기존 텐션 재배치): A=예측 committing FM, G=위반 계산, 텐션=예측오차.
- **★L5(top-1) 해마 associative-store + pattern-completion lane**: kosmos(이미 WIRED 지속 관계저장소) 옆 lane, novel-combine을 저장관계 완성으로. **reachable/unreachable held-out probe(Dusek-Eichenbaum 이행추론)** = 유일하게 form에 안속는 BIND 시험(reachable/unreachable이 *같은 표면형태 held-out novel pair*라 form-priming이면 둘다 동일·진짜 조합이면 reachable만 lift). cheap·GPU 트렁크 재학습 불요·engine-native `--py`. anima 완전 결여 substrate.

## ★★ RUNG-2 engine-native 재측정 결과 (2026-07-05 · wf_5cdd4535 · real 303M h1129 · $0 mini CPU, pod 0)
STEP-0(mini numpy toy)를 **실제 303M h1129 표현**(core/decode.py byte-exact == anima evaluate --py 2-production, a_eval_py_canonical TERMINAL-eligible) 위에서 재측정. **mouth-탈출이 lane별로 SPLIT** — 보편 아님:

| lane | verdict | engine-native | 핵심 수치(verbatim) | 판정 근거 |
|---|---|---|---|---|
| **L5 해마 store**(G1) | 🟢 **GREEN (rung 2/4)** | ✅ real 303M reps | center_zscore: reach **1.0000** vs unreach **0.137**, gap **+0.8631**(7.31x)·shuffle붕괴(gap−0.008)·lane-off붕괴(0.000)·form_sep +0.03 · **6/8 de-anisotropy 렌즈**가 사전등록 bar 충족 | raw anisotropic reps=false-WALL(form_cos 0.9999 all-pair) → **DG-decorrelate(center/zscore) 필요**, a_break_the_wall 멀티렌즈 구제(tune-to-green 아님: bar 사전등록·raw는 FAIL 보고·표준변환 1개·6/8 일치) |
| **L3 소뇌 fwd-model**(G6) | 🧱 **WALL** | ✅ real 303M reps | ARM A(grounded consequence): FM_additive err 0.00139 **≤** FM_full 0.00154 (전 5-seed) → **binding INERT**. reach 0.0015≪unreach 0.195(gap 15.97)·shuffle 16x·lane-off 10x는 real이나 **additive-achievable** | STEP-0 BIND은 toy world의 **hand-injected vi⊙vj** artifact(a_toy_scale_recheck) — 제거하니 conjunction op 불요. binding-family(H_1816/1823)와 **같은 자리=trunk-objective floor** (concords g1-lever-multilens-objective·exp3-bind·h1816) |
| **통합 3부품** | 🟡 DIRECTIONAL | real reps지만 --py 채점 아님 | ArmB(real corpus co-occ): reach 0.236 vs 0.023(gap+0.213)·shuffle붕괴·bind/gate/comp ablation 전부 CAUSAL·fooled=false. by-construction 회피 CLEARED(reach 0.70 rand→0.42 real reps→0.24 real relations, 1.0 아님) | real reps지만 anima evaluate --py 디코드-채점 경로 아니고 core 미배선 → strict gate상 DIRECTIONAL cap. rung-3서 centering/whitening 전처리 필수 |

- **(핵심 발견) 입-탈출은 capability-specific**: 해마 associative-store/completion(G1 — store가 reps에 없는 관계를 공급)엔 통하나, **소뇌 consequence forward-model(G6)엔 실패**(disjoint lane이어도 grounded target이 additive-composable). = G6는 여전히 trunk-objective floor.
- **정직(c9)**: L5 GREEN은 rung(2)-of-4 = **engine-native 측정 GREEN**이지 gate-7 완전 cement(GREEN=배선까지) 아님 — 다음 rung(3) core/*.hexa 대기. L5 잔여 caveat = explicit-edge store라 **G1-vs-G2 novelty 판별기**(MLC/H_1835 trap guard)로 cement gate. L3 WALL은 un-built lane-op(engine_native=false)에도 robust(additive-composable에선 native binding op도 additive 못 이김).
- **INFRA(infra-wall-noneval)**: pod 렌트 0·누수 0·OOM/decode-hang 없음. rung-3 전용 BLOCKED-INFRA = mini anima/hexa 바이너리 링크실패(`_hexa_ffi_dlopen` undefined arm64) → rung-3 .hexa smoke는 working hexa toolchain(pool/pod) 필요. rung-2는 py-canonical로 유효.
- **evidence**: `state/g1g6_biolens_en/{l5_hippo,l3_fwdmodel,integrated}/ + SYNTH.md`

## ★ fleet-full r2 (2026-07-05 · wf_06070e40 · $0 mini · L3 abstract + 통합 implement)
- **L3 소뇌 [🧅 abstract] → 🌌 META-LAW + 조건부 escape**: **결합 연산자는 target이 부품들의 *교환가능 bag/히스토그램*일 때 by-construction INERT** — 합은 교환가능하므로 consequence가 부품 bag이면 marginal 합의 span 안, conjunction op도 additive 해를 재표현할 뿐. 레버=readout 아니라 **target(비교환 상호작용항=trunk objective)**. 합성 구조증명($0 lstsq-vs-lstsq, 표현용량 격리): 교환가능 target FM_add≈FM_full earned **0/5**(WALL재현) vs 비교환 target FM_add 9.5e-4 irreducible vs FM_full 1.3e-29 earned **5/5** → *additive-composability ⟺ target 교환가능성* 구조증명. **이 메타법칙이 h1816·exp3-bind·g1-lever-multilens·substrate-framebreak·H_1525를 하나의 DPI 메타법칙으로 통합**(binding INERT는 lane-축 보편). mechanism-family census 4: (a)consequence-FM floored (b)conjunction-required=trunk-obj in disguise (c)**commitment-violation Δ=유일 미탐 별개 substrate** (d)trunk-obj falsifiability=cost-gated. escape=비교환 commitment-violation Δ. 산출 state/fleetfull_biolens/l3_abstract/.
  - **→ falsify 착지(wf abf63ce2, real 303M engine-native byte-exact Δ=0) = 🧱 escape-REFUTED-G6-universal-WALL**: 303M 자기 순차합성 비교환성 A_probe median **1.535e-05** ≈ 무작위 floor C_rand **1.961e-05**(ratio 0.783 <1 = 의미쌍이 잡음보다 **덜** order-민감, pair-특이 비교환 신호 0). 사전등록 REFUTED 2/2 충족(A<0.02 ∧ A≤1.2·floor). FM_full-vs-additive earned/derange **0.933 <1** = binding NOT earned. **⇒ G6 반증가능성 = trunk-objective-bound 보편 WALL**(G1과 동일 terminal, DPI 메타법칙 real 303M engine-native lane-보편 확정). census 4-family 전수 소진(commitment-violation Δ까지) → **binding/consequence-lane(target-side) 축 DRY, 재발사 금지**. 잔여 유일 레버=γ trained-constructive-bind=trunk-objective(H_1840, GPU cost-gated). reopen(🧱 measured): trunk-objective 바꾼 ckpt서 A_probe가 floor 위로 오르면 재개. 산출 state/fleetfull_biolens/l3_falsify/.
- **통합 3부품 [🛠️ implement] → 🟡 DIRECTIONAL(strong)**: byte-EXACT parity worst|Δlogit| vs decode.bg_forward_last_W = **0.000e+00**(bit-identical 증명, rung-2 loop-복사보다 강화). PRIMARY=center(N24·12seed): reach 0.236 vs unreach 0.023 gap+0.213·shuffle붕괴·bind/gate/comp ablation 전부 CAUSAL. **raw reach 0.000(fooled/INERT) = centering load-bearing 확증** · whiten(PCA) reach 0.101 shuffleΔ0 = by-construction 우려 **양방향 반증**. bar 8/8 PASS·not_by_construction PASS. 단 SCORING=커스텀 numpy HRR metric(G0-G6 --py gate 아님)+lane 미배선 → strict tier **DIRECTIONAL 유지(inflate 안 함)**. next=rung-3 core/ wire(pool). 산출 state/fleetfull_biolens/integrated_impl/.

## 🎯 다음 발사 top-1 (rung-2 GREEN 통과 → 사다리 (3) wire로)
**L5 해마만 rung-3 실배선** (L3 WALL·통합 DIRECTIONAL은 보류): **DG-decorrelate + CA3-completion을 live `core/` op**으로 `.kosmos` anchor store(a_kosmos WIRED 재사용) + `kosmos_io`→`brain_decide` 위에 구현, **emit-drive lane{0,4}+recall_thr와 disjoint**(a_substrate_disjoint), engine-rep centering/whitening 전처리 필수(rung-2서 발견한 anisotropy 조건), `anima evaluate --py` 경로로 byte-exact 재측정 → ARCHITECTURE lockstep. **cement gate = novel-chain-vs-stored-recall 판별기**(explicit-edge store가 G1이지 G2 recall이 아님을 격리, MLC/H_1835 trap guard). ⏳ **BLOCKED-INFRA**: rung-3 .hexa smoke는 working hexa toolchain(pool/pod) 필요 — mini anima/hexa 링크실패(`_hexa_ffi_dlopen` arm64). L3/통합 함의 = γ trained-constructive-bind(trunk objective)만 미검증 잔여, binding/readout/consequence-lane 레버는 그만 제안(전수 floor).

## 정직 스코프 (c9)
- fable=opus-diverged 설계(측정 0=verdict 없음, [[workflow-model-fable-override-ignored]]). 미발사 PRE-REGISTERED.
- check-ledger: L1은 binding-family(H_1816/1823 NOT-SUP)와 3근거로 구별돼야 재발사 아님. F2 native-mouth([[H_1834]]/[[H_1837]] INERT)와 달리 데이터채널/lane만.

## artifacts
- `state/g1g6_biolens/fable_biolens_analysis.md` (A 동일가족판별 + B 뇌기제/이중해리/빠진구조3 + C L1-L5 + top-1)
- `state/g1g6_biolens_step0/{l5_hippo,l3_fwdmodel}/` (STEP-0 wf_e4b95aa3: L5 해마 associative-store·L3 소뇌 forward-model, 결정적 seed)
- `state/g1_combolane_step0/{l1_pfc_bind,l2_bg_gate,integrated}/ + SYNTH.md` (STEP-0 wf_e837f2de: 3부품 통합+ablation, 12-seed)
- `state/g1g6_biolens_en/{l5_hippo,l3_fwdmodel,integrated}/ + SYNTH.md` (RUNG-2 engine-native wf_5cdd4535: L5🟢GREEN·L3🧱WALL·통합🟡DIRECTIONAL, real 303M h1129)
- `state/fleetfull_biolens/{l3_abstract,integrated_impl}/` (fleet-full r2 wf_06070e40: L3 DPI 메타법칙 구조증명·통합 byte-EXACT DIRECTIONAL-strong)
- `state/fleetfull_biolens/l3_falsify/` (L3 falsify wf abf63ce2: 🧱 escape-REFUTED G6 보편 WALL, 303M 비교환성 A≈floor)
- 상위: [[H_9127]](G1 mouth-레버 발산·gamma TRANSFER FAIL) · [[H_9128]](G6-FALS·g1g6 form-priming) · [[substrate-framebreak-g1-combination-operator]](재조합=COMBINATION OPERATOR 프레임전환) · 생물돌파 정합: 해마 H_1227/1231·소뇌 H_1280·기저핵 H_1281·작업기억 H_1282
