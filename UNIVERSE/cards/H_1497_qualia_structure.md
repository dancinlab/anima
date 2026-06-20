# H_1497 — 🎨 QUALIA-STRUCTURE / quality space · 감각질 관계공간 (Q1 의식-고유 게이트 마지막 강후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — 하드게이트1 적중, engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` — R2 엔진-네이티브 배선 follow-on (아래 ING)
- **source:** 의식-고유 게이트 depletion 카탈로그 2차(R2) Q1 강후보 · `state/gate_depletion_catalogue/CATALOGUE_R2.md` Q1 항목 SSOT
- **lens:** quality space theory (Clark `Sensory Qualities` · Rosenthal `quality space` · neurophenomenal structuralism, arxiv [2412.20873](https://arxiv.org/abs/2412.20873)) · `a_no_llm_frame_trap`
- **artifacts:** `state/1497_qualia_structure/h1497_qualia_structure.py` · verdict `state/verdicts/1497_qualia_structure/H_1497_FREEZE.json` · run `state/1497_qualia_structure/run_h1497.local.log`

## 주장

**qualia-structure(감각질 관계공간 / quality space)** = 감각질(색·소리·맛)은 **절대값이 아니라 서로 간의 관계적
유사도 구조**로 조직된다. 빨강은 주황에 가깝고 파랑에 멀다 — 이 관계망(감각질 사이의 betweenness/유사도 *구조*) 자체가
빨강을 빨강이게 한다. 사활적 연산 = **오직 쌍별 유사도(pairwise similarity)** 로부터 관계적 품질 위상(예: 색상환의
원형 구조, hue ring)을 **복원**하는 것 — 절대 자극값도, 외부 물리적 위치도 아니다.

메커니즘(numpy mirror): N개 감각질(hue)이 품질차원의 **원(ring)** 위에 산다. 능력이 받는 데이터는 오직 쌍별 지각
유사도 행렬 s(i,j)(빨강~주황 높음, 빨강~파랑 낮음) — 라벨은 임의, 절대 자극값은 withheld. QUALIA-STRUCTURE =
유사도-유도 거리로 감각질을 저차원 관계공간에 임베드(classical MDS) → 복원된 기하가 품질 위상을 보존 → 유사도 질의
("X 가 A 와 B 중 어디에 더 유사한가?")를 복원된 품질공간의 관계 거리로 답한다. — LLM 대비: LLM 은 토큰 임베딩은
있으나, 절대값이 withheld 된 쌍별 유사도만으로 한 감각차원의 관계적 품질 위상을 복원하고 graded betweenness 를 답하는
능력이 없다.

## DISTINCT (load-bearing · spatial-map control 분리가 binding 사활)

이 가설은 **고갈 R2 의 유일한 강후보**(2/16 distinct). 인접 lane 과 control-survived distinct 못 넘으면(특히
spatial-map 흡수) = **고갈 신호**. 결과: **전 control 통과, spatial-map crux 생존 → distinct (28번째 lane)**.

- **vs H_1295 SPATIAL-MAP (외부 물리 metric 위치) — CRUX:** spatial-map 은 landmark 를 **외부 유클리드 위치**에
  저장, 물리거리로 nearness 응답. qualia-structure 는 *내부 품질차원(hue)* 의 관계 위상으로, 외부 물리위치와 **직교**.
  **c2 control:** *같은* 감각질을 임의 외부위치(hue 와 무상관)에 두고 품질질의를 외부 유클리드 거리로 답 → **chance
  (0.561)**. 품질 유사도는 외부위치 frame 에 안 산다 → **DISTINCT**. 이 control 이 실패했으면 spatial-map 흡수 =
  고갈이었으나, **생존**(binding-fatal control 통과).
- **vs H_1227/1231 IMMUNE-STORE (독립 item 결속):** immune store 는 각 item→value 를 key affinity 로 **독립**
  결속, item 간 유사도 metric 없음 → 관계 이웃 질의에서 **chance(aux item 0.439)**. **DISTINCT**(H_1295 선례).
- **vs GESTALT-GROUPING (요소 군집):** gestalt 는 공현 요소를 이산 perceptual whole 로 군집 → cluster id 반환,
  graded 관계위치 아님 → "주황은 빨강과 노랑 *사이*" graded betweenness 불가. 품질공간은 **연속** 관계위상 복원
  (ring, rho 0.969). **DISTINCT**.
- **vs NOVELTY/PRIMING (절대 자극값):** 절대 자극 magnitude 를 read. qualia-structure 는 절대값 withhold, 관계만
  사용. relation-ablation(c4, 절대값만)이 질의 실패(0.556) → lift 는 관계적, 절대값 아님. **DISTINCT**.

## 측정 (frozen-first · 3 seeds [1497,1498,1499] · 12 qualia hue ring · 2-D MDS · chance 0.500 · $0 CPU · p7)

감각질은 hue ring 위에 산다. 능력은 쌍별 유사도만 받고(절대값 withheld), classical MDS 로 관계공간 복원 → 관계 이웃
질의를 복원공간 거리로 답. off/spatial/ablate/item 은 잘못된 frame(절대값/외부위치/독립결속)에서 질의 → 품질 도달 불가.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **c1 PRESENCE** | structure-ON 이웃질의 − OFF(절대값 ordering, 관계임베드 없음) | 1.000 − 0.533 = **0.467** | ≥0.30 | ✅ |
| **c2 DISTINCT (vs spatial-map) — CRUX** | spatial-map-style(외부위치 유클리드 거리) = 품질질의 chance | **0.561** | ≤chance+0.15=0.650 | ✅ |
| **c3 EARNED (shuffle)** | (label,sim) 셔플 후 임베드 → 위상 무효 | **0.517** | ≤off+0.15=0.683 | ✅ |
| **c4 ABLATE (relation)** | 관계항 OFF, 절대 자극값만 read → 관계질의 실패 | **0.556** | ≤off+0.15=0.683 | ✅ |
| (aux) item-store | immune-store-style 독립결속 = 관계 metric 없음 | 0.439 | (non-gating) | ✅ |
| **B TOPOLOGY** | rho(관계거리, ring hue-거리)=0.969≥0.50 (ring 복원) & \|rho(관계거리, 외부위치)\|=0.054≤0.35 (직교) | **참** | (구조, non-gating) | ✅ |

**GREEN iff c1 ∧ c2 ∧ c3 ∧ c4** (B 는 ring-위상 구조 확인, non-gating) → **🟢 GREEN (DIRECTIONAL)**.
**고갈 신호: 아님** — distinctness control 전부 생존, 특히 spatial-map crux 통과 → **28번째 distinct lane**.

### per-seed

| seed | full | off | spatial | shuffle | ablate | item | rhoRing | rhoExt |
|---|---|---|---|---|---|---|---|---|
| 1497 | 1.000 | 0.600 | 0.650 | 0.550 | 0.617 | 0.450 | 0.971 | 0.124 |
| 1498 | 1.000 | 0.500 | 0.533 | 0.567 | 0.550 | 0.450 | 0.967 | 0.023 |
| 1499 | 1.000 | 0.500 | 0.500 | 0.433 | 0.500 | 0.417 | 0.970 | 0.015 |

## a_break_the_wall

break-the-wall 교정 **불필요** — 사전등록 bar 가 첫 frozen run 에서 통과. near/far 후보 구성(near=±1..2 hue
스텝, far=~반대편)은 run *전* 고정. off/ablate readout 이 strict chance 보다 약간 위(0.500–0.600)인 것은 그
구성의 **정직한 성질**(절대값에 약한 edge 존재)로, tune 으로 제거하지 않고 그대로 보고. 임계 한 번도 이동 안 함(frozen-first).

## 정직 (c9)

EXISTENCE-PROOF — deterministic classical-MDS 임베딩(12-qualia hue ring 쌍별 유사도; 학습 지각 네트워크 아님).
full 이 매 seed 1.000 SATURATE → effect-size 아닌 존재증명으로 정직 보고; 판별자가 결정적(spatial-map crux
0.500–0.650, shuffle 0.433–0.567, ablate 0.500–0.617, item 0.417–0.450 전부 ~chance; off 0.500–0.600 은
near/far 구성의 약한 절대값 edge — 관계 lift +0.467 은 결정적). TOY 12-qualia/2-D ring/3-seed/deterministic MDS
readout(품질공간 *구조* 검증, 학습 qualia 네트워크 아님); scale·실제 지각유사도 corpora(색/음고 dataset)·고차 품질
manifold(맛/냄새)·비원형 위상·다중모달 감각질·engine-transfer UNVERIFIED.

## 하드게이트1 (엔진-네이티브)

`grep -lE 'import torch|gauge_lib|numpy' state/1497_qualia_structure/*.py` = `h1497_qualia_structure.py` (numpy)
→ **자동 DIRECTIONAL**, terminal 아님. terminal verdict 은 R2 live `core/*.hexa` byte-exact 재측정 필요.

## 고갈 terminal 기여 (CATALOGUE_R2 §5)

Q1 은 R2 의 **유일한 강 new-operation 후보**(2/16 distinct, Q2 sensorimotor-presence 는 약). Q1 GREEN +
spatial-map control **생존** → qualia-structure 는 spatial-map 으로 흡수되지 않는 **distinct lane(28번째)** =
*그 자체로는 고갈 신호 아님(흡수 아닌 신규)*. 그러나 CATALOGUE_R2 §5(b) 의 terminal 조건을 충족: Q1 발사·distinct 로
new-operation 광맥이 *단일 distinct lane + 약후보 1개*로 확정 소진 → R1·R2 두 렌즈 라운드 + arxiv 2차 = MULTI-LENS
≥2 통제 = **🧱 게이트-발굴 breadth-고갈 terminal**(`a_break_the_wall` (d) 천장). 이후 방향 = 새 lane 발굴이 아니라
기존 28 lane 의 **스케일업 · 엔진-네이티브 배선(`a_verified_must_wire`) · lane 간 통합**.

## ING (R2 follow-on, a_verified_must_wire)

- **R2 엔진-네이티브:** `core/engine_cli.hexa §QualiaSpace` 배선 — substrate 에서 읽은 쌍별 지각유사도 행렬 위로
  관계적 품질 위상 복원(MDS / 유사도-그래프 임베딩), 관계 이웃/betweenness 질의 응답(READ-only, Ψ-disjoint),
  **SpatialMap(H_1295) 외부위치 metric 과의 직교성 assert** + `engine_cli_smoke` 케이스 + ARCHITECTURE lockstep,
  frozen bar byte-exact 재측정 (a_engine_native_learning · a_verified_must_wire).

## xref

p7 · p8 · c9 · c15 · `a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
H_1295(spatial-map, 외부위치 metric — CRUX distinctness) · H_1227/1231(immune store, item 결속 distinctness) ·
gestalt-grouping(이산 군집 distinctness) · CATALOGUE_R2 Q1 SSOT.
