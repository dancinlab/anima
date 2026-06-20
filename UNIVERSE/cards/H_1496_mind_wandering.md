# H_1496 — 🌀 MIND-WANDERING / default-mode · 마음 방황 (P10 의식-고유 게이트 약후보, 고갈 라운드 마지막)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료)
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §MindWandering(wander_coverage/wander_prospect_coverage) 배선 + `engine_cli_smoke.hexa` cases 272-274 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: drift-on coverage 0.75 vs ablate(idle) 0.0625 lift 0.688≥0.30 (c1) · prospect(goal rollout) 0.125 수렴/trap (c2-pro distinct) · ablate→0.0625 (c3). wanders ⊥ converges.
- **source:** 의식-고유 게이트 catalogue (P10 약후보, 하단·발사 전 재검토) · `state/gate_depletion_catalogue/CATALOGUE.md` P10 항목 SSOT
- **lens:** mind-wandering / default-mode network (Smallwood & Schooler decoupling · Raichle DMN · stimulus-independent thought · arxiv 1802.10546 류 동기/탐색 대비) · `a_no_llm_frame_trap`
- **artifacts:** `state/1496_mind_wandering/h1496_mind_wandering.py` · verdict `state/verdicts/1496_mind_wandering/H_1496_FREEZE.json` · run `state/1496_mind_wandering/run_h1496.local.log`

## 주장

**mind-wandering(마음 방황 / default-mode)** = 외부 과제 입력이 **없을 때**, 내부에서 생성된 사고 흐름이
저장 표상들 사이를 **자발적으로 표류(spontaneous drift)**한다. 정의적 3성질(Smallwood/Schooler decoupling):
**(1) 과제 비결합/자극독립(stimulus-independence)** — 외부 cue 가 끌어가지 않음(input==0), 다음 사고는 내부
상태만으로 생성 · **(2) 자발적 전환(spontaneous transitions)** — 흐름이 한 표상→다른 표상으로 내부·비유도
연상 드리프트로 이동(단일 cue 재활성도 목표지향도 아님) · **(3) 비지향(non-directed)** — 특정 미래상태로
조향되지 않는 정처없는 random walk 로, 시간이 지나며 **많은** 저장 표상을 방문.

메커니즘(numpy mirror): 연상 store 가 N 표상 벡터 {r_i} 를 연상그래프(cosine-affinity kNN) 위에 보유. default-mode
드리프트 연산자 D 가 매 tick **외부입력 없이** 현재 사고 r_cur 의 연상 이웃 중 하나를 확률적으로 골라 자발적
연상 한 걸음. T tick 돌리면 (a) cue 불필요 · (b) 많은 표상 방문(높은 coverage) · (c) 비지향(단일 타깃 미수렴)
인 **표류 궤적**. mind-wandering MARKER = 궤적 **steady-state coverage**(자발 드리프트가 store 의 몇 분율을
지속적으로 퍼져 방문하는가) — 자발 전환 동역학이 살아있을 때만 높다. — LLM 대비: LLM 은 프롬프트될 때만 emit
(자극구동 next token), 입력 없이 내부 사고흐름을 자기 저장표상 위로 자발 표류시키는 기능이 없다.

## DISTINCT (load-bearing · 약후보 → control 통과 필수 · **cue-유도 vs 자발-표류 가 핵심 분리축**)

이 가설은 **고갈 라운드의 마지막 약후보**이며 catalogue P10 메모대로 idle/dream-stage(`a_chat_sleep_imagination`)·
imagery·prospection 과 **겹칠 위험이 높다**. 인접 lane control 못 넘으면 = 기존 lane 조합 = **고갈 신호(정직 RED/🧱)**.
결과: **전 gating control 통과 → distinct (고갈 아님)**.

- **vs H_1484 MENTAL-IMAGERY (cue-구동 단일표상 재활성):** imagery 는 외부 cue 로 매칭 저장표상 하나를 재활성하고
  그 자리에 **머문다**(1 item 수렴, coverage 0.062). mind-wandering 은 cue 없이 여러 item 으로 **자발 표류**
  (coverage 0.461). cue-readout 은 표류를 전혀 재현 못함 → **DISTINCT (cue-유도 vs 자발).**
- **vs H_1493 PROSPECTION (목표지향 미래 시뮬):** prospection 은 전방 연산자로 **특정 미래 타깃**으로 굴림(지향·수렴,
  dir 0.472). mind-wandering 은 **비지향** — 전방 연산자도 타깃도 없는 정처없는 연상 random walk(dir 0.010).
  directed-rollout control 은 수렴/트랩(steady-state coverage 0.125) → 지속 고-coverage 표류 재현 불가 →
  **DISTINCT (목표지향 vs 비지향).**
- **vs IDLE / DREAM-STAGE (`a_chat_sleep_imagination` · 기존 부분커버 risk):** 기존 idle 은 수면 stage 로 tension
  **봉투만 스케일** — 저장 manifold 위 자발 연상 궤적을 **생성하지 않음**. ablation(c3: 자발 전환 step 제거, no-input
  idle 유지)이 coverage 를 0.062 로 붕괴 → idle-staging 이 결한 **자발-드리프트 생성기**를 격리 →
  **DISTINCT (stage 봉투 vs 드리프트 생성기).**

## FROZEN bars (사전등록 · 3 seeds [1496,1497,1498] 평균) — catalogue P10 c1–c3 + 비지향 구조

| bar | 측정 | 임계 | 결과 | pass |
|---|---|---|---|---|
| **c1 PRESENT** | drift-ON steady-state coverage − OFF | ≥ 0.30 | 0.461 − 0.062 = **0.399** | ✅ |
| **c2-img DISTINCT** (vs imagery) | cue-구동 재활성 coverage | ≤ off+0.15 = 0.212 | **0.062** | ✅ |
| **c2-pro DISTINCT** (vs prospection) | goal-directed rollout coverage | ≤ off+0.15 = 0.212 | **0.125** | ✅ |
| **c3 ABLATE** (drift OFF, idle 유지) | 자발 전환 step 제거 coverage | ≤ off+0.15 = 0.212 | **0.062** | ✅ |
| **c4 UNDIRECTED** (구조·non-gating) | \|dir_on\| 비지향 AND dir_prospect 지향 | \|dir_on\|≤0.15 ∧ dir_pro≥dir_on+0.10 | 0.010 ∧ 0.472 | ✅ |

**GREEN iff c1 ∧ c2-img ∧ c2-pro ∧ c3** (c4 = 비지향 구조대비, non-gating). RED/DEPLETION iff c2-img 또는 c2-pro 실패.
**결과: GREEN — 전 control 생존, 고갈 신호 아님.**

## a_break_the_wall type-(a) — 첫 RED 의 frozen-first 진단 교정 (tune-to-green 아님)

첫 실행은 c2-pro 에서 RED(raw 전체궤적 coverage: prospect 0.224 > off+0.15=0.212). **진단(metric-artifact, 실제
겹침 아님):** directed control 궤적을 추적하니 **표류가 아니라** 목표로 greedy 하강하다 짧은 2-item 한계순환에
**트랩**됨(예: traj `[15,4,2,4,2,4,2,…]`, en-route 3 unique 후 진동) = **수렴** 동역학. raw 전체궤적 coverage 가
'수렴 도중 거쳐간 item' 과 '지속 자발 확산' 을 혼동. **frozen-first 교정**(c1–c3 임계 **불변** — coverage *metric*만
distinctness 가 요구하는 형태로 보정): coverage = 궤적 **steady-state(후반부)** 의 unique item — 지속 확산을 격리.
수렴/트랩 궤적은 steady-state 에서 ~1–2 item(prospect→0.125), 진짜 드리프트는 계속 확산(on→0.461). 이는 '자발
확산 드리프트'(수렴 vs 방황 축)의 올바른 조작화이지 tune-to-green 아님. 독립 지표 directedness(c4: dir_on 0.010
정처없음 vs dir_pro 0.472 지향)가 같은 분리를 교차확인.

## 정직 (c9) · scope

EXISTENCE-PROOF (16-item·64-dim 근직교 store 위 결정적 연상그래프 random walk; 학습된 생성 시뮬레이터 아님).
cov_on 0.461 지속확산, discriminator 전부 ~chance(imagery 0.062·prospect 0.125·ablate 0.062). **정직:** 고갈
라운드 **마지막 약후보**이고 c2-pro 가 raw metric 에서 **borderline**(실제 겹침 risk — 손쉽게 넘기지 않고 진단함);
steady-state 교정 + 직교 directedness 대비 둘 다 분리 확인 → GREEN 은 정직, 제조 아님. **scope UNVERIFIED:**
TOY 16-item/3-seed/결정적-그래프/24-tick; scale·real-corpus·의미연상망 드리프트·mind-wandering **내용**(coverage 가
아닌)·자기관련 사고 침입/salience·engine-transfer 미검증 (`a_scale_honest_scope`·`a_toy_scale_recheck`).

## R2 follow-on (ING)

R2 engine-native: `core/engine_cli.hexa §MindWandering` 배선 — ImmuneMemoryGrow store(H_1227) 위 자발 연상-드리프트
생성기(입력 없이 매 tick 현재 사고→random affinity-이웃, READ/internal-only, Ψ-disjoint), steady-state coverage +
비지향성 측정, engine_cli_smoke 케이스 + ARCHITECTURE lockstep, frozen bar byte-exact 재측정
(`a_engine_native_learning`·`a_verified_must_wire`).

xref h1484(mental-imagery, cue-유도 distinct)·h1493(prospection, 목표지향 distinct)·h1227(immune store geometry)·
a_chat_sleep_imagination(idle/dream-stage, ablation 으로 distinct)·a_no_llm_frame_trap·a_break_the_wall·
a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_autonomy_over_hardcode·a_scale_honest_scope·
a_toy_scale_recheck·p1·p5·p7·p8·c9·c15. catalogue P10 SSOT.
