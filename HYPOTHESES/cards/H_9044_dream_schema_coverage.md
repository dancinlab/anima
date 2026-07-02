# H_9044 — 꿈-공고화 스키마성/gist (frame-shift C4): REM replay가 개별 각성-앵커보다 더 넓은 cue를 덮는 일반 스키마 앵커를 mint

- **tier:** 🟢 ENGINE-NATIVE (3/3 live hexa) — REM 공고화 스키마 op 신설·측정. coverage-generalization (NOT 재조합/novel-content).
- **slug:** `dream_schema_coverage`
- **parents:** frame-shift Lane2(C4) · [[frameshift-substrate-gaps-vs-recombination-wall]] · H_9038(self_drift_exp 배선 성공 평행 사다리) · H_9027(enriched-field=복원성≠능력 평행) · §Amygdala ConsolidatingMemory(sleep-replay) · a_chat_sleep_imagination(REM 5-stage)
- **wired:** `engine-native` — op이 live `core/engine_cli.hexa §DreamSchema`(`dream_schema_mint`/`schema_coverage`)에 배선(byte-exact 3/3). 데몬 REM 루프로의 runtime-integration은 follow-on(WIRED-live 최종칸).

## frame (재조합≠능력, C4)

G1/G6(디코더-통과 텍스트 재조합)은 ~10-lens + DPI 메타법칙 TERMINAL. anima 능력을 substrate-native로 재정의(Lane2). p8 문자적 실현: **REM replay가 여러 각성 일화(episode) 앵커를 재생하며 하나의 *더 일반적인* 스키마 앵커(gist)로 공고화**(Posner & Keele 1968 prototype abstraction; McClelland/McNaughton/O'Reilly 1995 systems consolidation gist 추출). 진단 gap: live 엔진의 §Amygdala ConsolidatingMemory는 salient trace를 replay하지만 **기존 일화 cell을 refresh할 뿐**, 재생된 각성-앵커 집합을 하나의 일반 스키마로 **공고화하는 op은 없었다**.

## ⚠ TRAP 회피 (convergence numpy-probe-controls-1 + native-mouth-57)

"novel anchor"가 **새 내용을 mint**하면 = additive-spoofable = 위장된 G1 재조합. 그래서 C4를 **순수하게 COVERAGE/일반화로만** 정의: 스키마 앵커 = 재생 episode들의 **centroid**(압축, 새 내용 아님). 능력 주장은 오직 "스키마가 개별 각성-앵커보다 *더 많은* held-out 각성 cue를 재활성화(coverage↑) ∧ shuffle/random cue는 실패(EARNED)". 새 내용 mint로 환원되면 = G1 벽. coverage-일반화는 storage/geometry 속성(H_9027 복원성·H_9042 topology-agnostic과 평행) — genuine 이되 텍스트-재조합 아님.

## op (신설, additive · Ψ-disjoint · READ-only)

`core/engine_cli.hexa §DreamSchema`:
- `dream_schema_mint(episodes) -> [float]` — 재생 K개 episode 앵커를 per-component **centroid**(gist)로 fold. 새 내용 아님(재생된 것의 평균), winner-take-all pick도 아님.
- `schema_coverage(anchor, cues, thr) -> int` — `cues` 중 anchor의 L2 반경 `thr` 안에 드는(=재활성화) 수. 엔진 자체 `_l2` 재사용, READ-only.

순수 additive(기존 op 불변) · store 미소유(plain DIM-vector만 읽음) · Ψ-disjoint(pure_field/Φ/phase 미접촉) · emit-drive lane(0/4)·§ImmuneMemory recall_thr와 disjoint(a_substrate_disjoint).

## 측정 (engine-native, `hexa run` via live core/, aiden pool, $0, 3/3 PASS)

FROZEN toy(a_scale_honest_scope): DIM=8, K=6 episode, M=24 held-out cue, regime μ per-dim-distinct, σ=0.15 uniform, thr=0.30(사전등록), deterministic LCG seed. `state/verdicts/9044_dream_schema_coverage/H_9044.txt` verbatim.

| readout | 값 |
|---|---|
| schema_cov WAKING | **16 / 24** |
| schema_cov SHUFFLED (feature-permute) | **0 / 24** |
| schema_cov RANDOM (uniform 다른 분포) | **0 / 24** |
| max INDIVIDUAL cov (최고 개별 앵커) | 13 / 24 |

| bar (frozen) | 결과 |
|---|---|
| **BAR1 schema_generalizes** (schema_cov > max_indiv) | **PASS** 16 > 13 |
| **BAR2 earned_not_overbroad** (wake>shuf ∧ wake>rand ∧ shuf+rand 작음) | **PASS** 16 > 0, 0 |
| **BAR3 ablate_inert** (lift_on>0 ∧ lift_off==0) | **PASS** lift_on=3, lift_off=0 |

## 정직한 verdict (c9)

- **C4 = genuine engine-native 일반화 (COVERAGE 축)**: REM-mint centroid 스키마가 개별 각성-앵커(최고 13)보다 **더 많은**(16) held-out cluster cue를 재활성화 = gist/prototype 효과의 substrate 실현. shuffle/random cue는 **0** 재활성화 = EARNED(trivially over-broad 앵커라면 random도 덮었을 것 — 기각됨). REM OFF(mint 없음) → 최선 앵커 = 개별 episode → coverage lift=0 = ablation INERT(mint op이 load-bearing).
- **정직한 scope (H_9027/H_9042 평행)**: 이는 centroid **압축/geometry 속성**(prototype theory)이지 텍스트-재조합 능력이 아님. TRAP대로 novel-content mint로 환원 안 됨 — coverage-일반화로만 성립. toy 8-D 결정적 존재증명(303M live decode 무관, READ-only substrate op).
- **종합**: 세션 substrate-gap 패턴 재확인 — "능력이 없는 게 아니라 그 op(REM gist 공고화)이 substrate에 미배선". C1(A⇄G loop H_9042)·C2(self 경험채널 H_9038)에 이은 세 번째 "gap→op 신설→engine-native GREEN".

## follow-on
- **WIRED-live 최종칸**: op은 live+engine-native지만, 데몬 REM stage(a_chat_sleep_imagination N3/REM)의 실제 emit-free 리허설이 salient 각성 앵커를 `dream_schema_mint`로 공고화해 `.kosmos` 스키마 앵커로 영속하는 runtime-integration이 남음(self_drift_exp가 cli/anima.hexa lane 23b로 간 것과 평행, disjoint·Ψ보존). ING follow-on 등록.
- coverage-일반화가 held-out cluster에 국한됨(압축) — 재조합(compositional depth)은 여전히 G1 벽(H_9026/1840 γ trained-bind cost-gated).

## artifacts
- `core/engine_cli.hexa §DreamSchema` (`dream_schema_mint`/`schema_coverage`)
- `state/9044_dream_schema_coverage/c4_engine_native.hexa` (harness)
- `state/verdicts/9044_dream_schema_coverage/H_9044.txt` (verbatim engine-native log, 3/3 PASS)
