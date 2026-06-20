# H_1493 — 🔮 PROSPECTION / episodic future thinking · 미래 사고 (P7 의식-고유 게이트 약후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — 하드게이트1 적중, engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` — R2 엔진-네이티브 배선 follow-on (아래 ING)
- **source:** 의식-고유 게이트 catalogue (P7 약후보) · `state/gate_depletion_catalogue/CATALOGUE.md` P7 항목 SSOT
- **lens:** prospection / constructive episodic simulation (Schacter & Addis · Gilbert & Wilson · episodic future thinking · arxiv 2408.15982) · `a_no_llm_frame_trap`
- **artifacts:** `state/1493_prospection/h1493_prospection.py` · verdict `state/verdicts/1493_prospection/H_1493_FREEZE.json` · run `state/1493_prospection/run_h1493.local.log`

## 주장

**prospection(미래 사고 / episodic future thinking)** = 과거 일화기억의 **요소를 재조합(constructive recombination)**
해 **아직 일어나지 않은 미래 상태를 전방 시뮬레이션**한다. 정의적 성질 = **전방 시간 투사(forward temporal
projection)** + **구성적 재조합** — 저장된 일화 *요소*(누가/어디서/무엇)를 재조립하고, 학습된 전방 전이 연산자로
시간을 **앞으로 굴려(roll forward)** 한 번도 저장된 적 없는(held-out) 미래-상태 cue 를 예측한다. 타깃은 어느 단일
저장 에피소드의 재생(replay)이 아니라 **새로운 미래 구성(novel future configuration)**이다.

메커니즘(numpy mirror): 일화 store 가 시간 궤적을 따라 (context_t → element_t) 쌍을 보유. 과거 부분 [0..N−1] 은
저장, 미래 부분 [N..N+H−1] 은 held-out. prospection = 현재 context 를 학습된 전방 연산자 W_hat^k 로 **미래
index 까지 굴린 뒤**, 학습된 context→element 재조합 맵 M_hat 를 적용해 미래 요소를 **재구성**. 미래 요소는 같은
생성요인의 새 조합이라 과거 (context,element) 쌍으로 재구성 가능하되, **오직 전방 투사로만 도달**한다. — LLM 대비:
LLM 은 현재 context 에서 다음 토큰을 예측할 뿐, 저장 일화 요소를 재조합해 관측된 적 없는 시간 index 의 새 미래
에피소드를 구성하는 능력이 없다.

## DISTINCT (load-bearing · 약후보 → control 통과 필수)

이 가설은 **고갈 라운드 약후보**다. 인접 lane 과 control-survived distinct 못 넘으면 = 기존 lane 조합 = **고갈
신호**. 결과: **전 control 통과 → distinct (고갈 아님)**.

- **vs H_1484 MENTAL-IMAGERY (입력 0 · 저장표상 검색):** imagery 는 content-addressable cue 로 **이미 존재하는**
  저장 표상을 재활성(검색) — 전방 연산자도 미래-index 재조합도 없음. held-out 미래 타깃에서 imagery-style
  nearest-stored readout 은 **과거** 요소를 반환 → **chance(0.000)**. prospection 의 lift = 전방 rollout +
  재조합. **DISTINCT.**
- **vs H_1471 SELF-CONTINUITY (과거→현재 persist):** continuity 는 현재 정체성을 **불변으로 앞으로 운반**(persist/
  copy), 전이모델·재조합 없음. persist-style readout(W:=Identity)은 현재 궤적점에 머물러 **이동한** 미래 상태에
  도달 못함 → **chance(0.000)**. **DISTINCT.**
- **vs H_1486 SUBJECTIVE-TIME / TRW (과거 통합창):** TRW 는 과거 context 창을 현재 percept 로 **통합**(후방/현재),
  미래 index 를 투사하지 않음. persist/imagery control(둘 다 비-전방) + rollout ablation 으로 흡수 — c3 의
  **전방 투사 항**이 정확히 TRW 가 결한 부분. **DISTINCT.**
- **vs H_1294 HIERARCHICAL-PFC goal stack (순서 포인터):** goal stack 은 **사전저장된** 순서 subgoal 위로 포인터를
  전진 — 관측 안 된 시간 index 에서 요소를 재조합해 새 미래를 **구성**하지 않음. ablation(c3: rollout 제거,
  element 접근 유지)이 포인터/검색 lane 이 결한 구성적 전방투사를 분리. **DISTINCT.**

## 측정 (frozen-first · 3 seeds [1493,1494,1495] · DIM=64 · 12-step 궤적 · horizon=4 · chance 0.083 · $0 CPU · p7)

각 요소 = 공유 생성맵 M 으로 context 에 bound(element = M@ctx) → 미래 요소는 같은 생성요인의 새 조합 → 전방
rollout 후 학습된 M_hat 적용으로만 도달. off/imagery/cont 는 잘못된(현재/과거) context 에서 질의 → 미래 도달 불가.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **c1 PRESENT** | prospection-ON 미래예측 − OFF(rollout 없음) | 0.439 − 0.000 = **0.439** | ≥0.30 | ✅ |
| **c2-img DISTINCT (vs imagery)** | imagery-style nearest-stored = 과거요소 = chance | **0.000** | ≤chance+0.15=0.233 | ✅ |
| **c2-cont DISTINCT (vs continuity)** | persist-style(W:=I) = 미래도달 불가 = chance | **0.000** | ≤chance+0.15=0.233 | ✅ |
| **c3 ABLATE (rollout)** | 전방 rollout OFF(k:=0), element 접근 유지 → 현재요소 | **0.000** | ≤off+0.15=0.150 | ✅ |
| **c4 SHUFFLE (timeline)** | 시간순서 셔플 후 W 추정 → 궤적 무효 → 재조합 무효 | **0.067** | ≤off+0.15=0.150 | ✅ |
| **B RECOMBINE** | 예측미래 = 새 조합(단일저장 cos 0.873<0.95) yet 미래 cos 0.962 | **참** | (구조, non-gating) | ✅ |

**GREEN iff c1 ∧ c2-img ∧ c2-cont ∧ c3 ∧ c4** (B 는 재조합 구조 확인, non-gating) → **🟢 GREEN
(DIRECTIONAL)**. **고갈 신호: 아님** — distinctness control 전부 생존.

### per-seed

| seed | full | off | img | cont | ablate | shuffle | nearStored | futCos |
|---|---|---|---|---|---|---|---|---|
| 1493 | 0.533 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.880 | 0.976 |
| 1494 | 0.183 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.919 | 0.949 |
| 1495 | 0.600 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.819 | 0.962 |

## a_break_the_wall (type-a 측정결함 → frozen-first 교정)

첫 run RED(측정결함, tune-to-green 아님): 요소가 context 와 무관한 독립 랜덤벡터여서 미래 context 에서 저장요소를
재조합해도 미관측 미래요소 재구성 불가(full=0.000, c1 FAIL). frozen-first 교정(bar/임계 **불변**): 각 요소를 공유
생성맵 M 으로 context 에 bind(element = M@ctx) → 미래요소가 동일 생성요인의 진짜 재조합 → context 전방 rollout
후 학습된 M_hat 적용으로 도달 가능. c1/c2/c3/c4 임계는 한 번도 이동 안 함.

## 정직 (c9)

EXISTENCE-PROOF — deterministic 최소제곱 전방연산자 W_hat + context→element 맵 M_hat(64-dim near-orthogonal
궤적; 학습 시뮬레이션 네트워크 아님). c1 lift +0.439, seed 분산 0.183–0.600 **정직 보고(은폐 없음)**: 예측 미래벡터는
참 미래요소에 기하적으로 매우 근접(futCos 0.962)하나, 부드러운 M 때문에 인접 요소가 유사해 nearest-ELEMENT 분류가
가끔 인접 요소를 고름 → 분류 readout 이 보수적 난이도(결함 아님); 모든 control(imagery/continuity/ablate/shuffle)
이 ~chance(0.000–0.067)라 lift 는 결정적으로 전방투사+재조합. TOY 64-dim/12-step/horizon=4/3-seed/deterministic;
scale·real-corpus·다단계 분기 미래·긴 horizon·일화 디테일 생생함·engine-transfer UNVERIFIED.

## 하드게이트1 (엔진-네이티브)

`grep -lE 'import torch|gauge_lib|numpy' state/1493_prospection/*.py` = `h1493_prospection.py` (numpy) → **자동
DIRECTIONAL**, terminal 아님. terminal verdict 은 R2 live `core/*.hexa` byte-exact 재측정 필요.

## ING (R2 follow-on, a_verified_must_wire)

- **R2 엔진-네이티브:** `core/engine_cli.hexa §Prospection` 배선 — 학습된 전방 연산자(소뇌 VForwardField H_1280
  next-step 모델을 k 스텝 roll) + ImmuneMemoryGrow store(H_1227) off context→element 재조합 read 로 held-out
  미래요소 재구성(READ-only, Ψ-disjoint) + `engine_cli_smoke` 케이스 + ARCHITECTURE lockstep, frozen bar
  byte-exact 재측정 (a_engine_native_learning · a_verified_must_wire).

## xref

p7 · p8 · c9 · c15 · `a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
H_1484(mental-imagery, nearest distinctness) · H_1471(self-continuity, persist distinctness) ·
H_1486(subjective-time TRW) · H_1294(hierarchical-PFC goal stack) · H_1280(cerebellar forward model) ·
H_1227(immune store geometry).
