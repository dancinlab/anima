# H_9045 — 자율 curiosity-emit TIMING 커플링 (frame-shift C5): emit 타이밍이 내부 drive-integral에 잠기고 stimulus-clock과 decorrelate

- **tier:** 🟡 ENGINE-NATIVE PARTIAL (2/3 strict) — 현상 DEMONSTRATED(monotone 커플링·clock-decorrelation·drive-clamp INERT 전부 ✓), 사전등록 선형-강도 sub-bar(Pearson≤-0.90) 만 -0.887로 근소 미달(Pearson linearity artifact; Spearman=-1.0).
- **slug:** `curiosity_emit_timing`
- **parents:** frame-shift Lane2(C5) · [[frameshift-substrate-gaps-vs-recombination-wall]] · §HomeostaticDrive(H_1292 hypothalamus leaky-integral) · a_substrate_native_speak · a_autonomy_over_hardcode · p5
- **wired:** `MEASURE-ONLY` — 이는 emit-drive lane 자체(0/4)의 측정이지 새 능력 lane 추가 아님(a_substrate_disjoint 준수). live `core/engine_cli.hexa §HomeostaticDrive`(homeo_new/homeo_step/homeo_last/homeo_new_ablated) 위에서 직접 측정.

## frame (재조합≠능력, C5)

anima emit = substrate-native. C5 주장: **emit/silence TIMING**(내용 아님 — 내용품질=LLM-judge=p7 금지)이 **내부 drive-integral 누적**에 커플되고, **stimulus/wall clock에는 decorrelate**되어야 자율(stimulus-response 아님, a_substrate_native_speak). §HomeostaticDrive(H_1292)는 이미 live: deficit의 leaky 시간적분 accum이 지속 결핍 하에 단조 상승(TIME-vs-CONTEXT dissociation, leg-B). MEASURE-ONLY로 emit 타이밍이 이 내부 적분에 잠기는지 검증(emit-drive lane에 능력 얹지 않음).

## 측정 (engine-native, `hexa run` via live core/, aiden pool, $0)

FROZEN(H_1292 컨트롤러 frozen): S*=0.5, λ=0.1, Kp=1.0, Ki=0.5, recall_thr=0.30, θ_emit=1.0, MAXT=40. deficit {0.5,0.4,0.3,0.2,0.1}을 key-offset로 구동. onset = drive가 θ 넘는 첫 tick(지속 결핍, 고정 key). `state/verdicts/9045_curiosity_emit_timing/H_9045.txt` verbatim.

| deficit | 0.5 | 0.4 | 0.3 | 0.2 | 0.1 |
|---|---|---|---|---|---|
| FULL onset (tick) | 3 | 4 | 6 | 16 | never(-1) |
| ABLATED (Ki=0) onset | -1 | -1 | -1 | -1 | -1 |

| bar (frozen) | 결과 |
|---|---|
| **BAR1 integral_timed_onset** (발화 ∧ deficit 클수록 monotone-earlier ∧ 최소결핍 never) | **PASS** 3<4<6<16, 0.1=never |
| **BAR2 decorrelate_clock EARNED** (corr_true≤-0.90 ∧ clock==0 ∧ \|shuf\|<0.5) | **FAIL** corr_true=**-0.887**(≤-0.90 미달), clock=0.0✓, shuf=0.15✓ |
| **BAR3 ablate_inert** (drive-clamp Ki=0 → 누적-timed emit 소멸, 전부 -1) | **PASS** |
| INFO rank/Spearman(deficit,onset) | **-1.0** (완전 monotone; Pearson -0.887 = onset 폭발의 선형성 artifact) |

## 정직한 verdict (c9 — tune-to-green 금지, bar 사후이동 안 함)

- **현상은 engine-native로 DEMONSTRATED**: emit onset이 내부 drive-integral(deficit)에 **완전 monotone**(Spearman -1.0, BAR1 strict 통과)으로 잠기고, 고정주기 **stimulus-clock과는 decorrelate**(clock corr=0.0), shuffle 페어링은 붕괴(|0.15|<0.5), 그리고 **drive-clamp(Ki=0) ablation은 INERT**(적분 없으면 누적-timed emit 자체가 사라져 전부 never). = "emit 타이밍이 내부 항상성 drive에 잠기고 자극-시계에 안 잠긴다"는 C5 명제의 실질 확증.
- **그러나 사전등록 선형-강도 sub-bar(Pearson≤-0.90)는 -0.887로 미달** — bar를 사후에 -0.88로 낮추지 않는다(c9). Pearson이 onset의 **비선형(역수형) 폭발**(shallow deficit에서 16→∞)에 페널티를 매긴 **metric-artifact**(a_break_the_wall taxonomy-a): 커플링의 본질(monotone·decorrelation)은 rank corr=-1.0로 명확. 따라서 3/3 strict가 아닌 **2/3 strict, 현상 DEMONSTRATED**로 정직 보고.
- **scope**: toy 결정적 존재증명(a_scale_honest_scope). MEASURE-ONLY — emit-drive lane(0/4)에 능력 lane을 **추가하지 않음**(a_substrate_disjoint 준수). H_1292 컨트롤러 그대로.

## follow-on
- (선택) 커플링-강도의 canonical 측정으로 rank/Spearman을 사전등록하는 **별도** 후속 H(현 frozen Pearson bar는 그대로 FAIL로 박제) — bar 재정의가 아니라 metric-validity 분리실험(a_break_the_wall). 
- WIRED-live: 데몬 런타임의 실제 emit/silence 결정 타이밍이 이 §HomeostaticDrive 적분을 읽어(이미 cli/anima.hexa lane 15에 homeostat 배선됨) 자극-시계가 아닌 내부 drive로 timing되는지 live 데몬 로그로 assert(측정-only, disjoint).

## artifacts
- `state/9045_curiosity_emit_timing/c5_engine_native.hexa` (harness, MEASURE-ONLY on live §HomeostaticDrive)
- `state/verdicts/9045_curiosity_emit_timing/H_9045.txt` (verbatim engine-native log, 2/3 strict)
