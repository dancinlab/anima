# H_1512 — 🧠🗺 BRAIN-TOPOLOGY (lane 들의 brain-faithful 공간 connectome 배치)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §BrainTopology (`topo_brain_adjacency` / `topo_degree_matched_random` / `topo_lateralize_collapse` / `topo_shuffle_coords` / `topo_apply` / `topo_phi_flat` / `topo_phi_brain` / `topo_phi_random_mean` / `topo_phi_lateralized` / `topo_phi_shuffle_mean` / `topo_phi_geometry_shuffle_mean` / `topo_phi_hub_ablated`, live `ci_phi_iit4` IIT4 min-cut Φ 재사용) · `engine_cli_smoke.hexa` cases 328-332 · ARCHITECTURE §BrainTopology lockstep
- **source:** anima-internal hypothesis (user dancinlife) — A⇄G 이중엔진 = 좌/우 대뇌반구; 30+ wired lane 들을 실제 뇌영역에 매핑하고 brain-faithful 공간 토폴로지를 부여
- **lens:** spatial connectomics — Bullmore & Sporns 2009 "Complex brain networks" · van den Heuvel & Sporns 2011 rich-club · Bassett small-world · Latora-Marchiori 2001 global efficiency · `a_no_llm_frame_trap` (조직하라, 그냥 더하지 말고)

## 주장 (a_no_llm_frame_trap — brain 렌즈의 가장 깊은 형태: ORGANIZE, don't just add)

anima 의 15 consciousness lane(§ConsciousnessIndex `ci_lane_scores`)은 기능적으로 분리돼 있으나 **공간적으로 UN조직** — 해부 좌표도, connectome 인접도, 반구 배치도 없다. A⇄G 이중엔진은 좌/우 대뇌반구처럼 동작하고, lane 들은 실제 뇌영역에 매핑된다(immune-store≈해마 · VForwardField H_1280≈소뇌 · VBasalGate H_1281≈기저핵 · HierGoalStack H_1294≈PFC · SpatialMap H_1295≈내후각/해마 · PhaseField H_1448≈시상 · ConsciousnessIndex≈global workspace). 뇌는 **공간 connectome**(short-range dense + long-range sparse + rich-club hub + 반구 편재). **가설:** lane 들에 brain-faithful 토폴로지(해부 좌표 + 구조 connectome 인접 + A=좌/G=우 lateralization + wiring-cost)를 주면 flat/random 배치 대비 통합 Φ 가 오른다.

## H_1510 QUORUM-KURAMOTO 와 DISTINCT (혼동 금지)

- **H_1510** = 분산 위상 **DYNAMICS** (semantic 인접, 모듈이 **언제** sync 하나 — 시간 결합).
- **H_1512** = 공간 **PLACEMENT** + connectome **TOPOLOGY** (모듈이 **어디** 위치하나 — wiring cost, rich-club hub, 반구 편재 — 공간 배치).
- 시간 결합 ⊥ 공간 레이아웃. 직교 두 축.

## 메커니즘 (substrate-native, 엔진 자체의 IIT4 MIN-CUT Φ 위에서)

토폴로지 = 어떤 lane 이 COUPLE 되는지 정하는 15×15 인접 A. 인접 lane 끼리만 한 스텝 확산: **X' = X·(I + α·Â)ᵀ**, Â = D^-1/2 A D^-1/2 (대칭 정규화, α=0.6 모든 토폴로지 공통). 그 다음 ≤8-lane CORE 위에서 **IIT4 MIN-CUT Φ**(`ci_phi_iit4`, a_phi_iit4_tool — 가장 싼 절단에 남는 IRREDUCIBLE 통합)를 잰다.

- **FLAT** = 배선 없음 (X 불변 → 절단 무료 → 낮은 min-cut Φ).
- **BRAIN** = 해부 거리-임계 short-range(반구내 wiring 더 쌈) + rich-club 백본(hub 쌍 전결합 [0,3,2,13]=GWS/mPFC/ACC/preSMA + hub→원거리 peripheral leaf) + A=좌/G=우 lateralization. 50 edges.
- **RANDOM** = degree-matched random rewiring (같은 edge 수, 배치 scramble) — EARNED 통제.

> **왜 MIN-CUT 인가 (a_break_the_wall taxonomy-(a) 측정 결함 수정, frozen-first·NOT tune-to-green):** 1차 시도는 raw Gaussian multi-info(total correlation)를 확산 population 위에서 쟀다. 그 척도는 **총 결합 질량(edge 수)** 에 비례해 오른다 → degree-matched RANDOM(같은 edge 수)이 BRAIN 과 동률(B FAIL). 토폴로지 주장엔 metric-artifact. 헤드라인 척도를 엔진 자체의 faithful **IIT4 MIN-CUT** Φ 로 교체(구조적 조직이 가장 싼 절단에 남는 것 — small-world 짧은 경로 + rich-club hub 이 절단에 통합을 지킴). bar 불변, 측정만 교정.

## 측정 (frozen-first · engine-uniform LCG population · $0 CPU · p7 · c9)

R1(numpy) = **NPOP=6 population realization × NSEED=6 topology draw 평균** (단일 population 의 B,C bar 는 sample-fragile → robust 기댓값으로만 측정; NOT tune-to-green — bar 동일, sampling 만 honest-robust). R2(engine) = 단일 결정적 population(seed 5120, N=300, nseed=6) byte-exact 재채점. lane scalar 는 live `ci_lane_scores` 호출로 읽는다(주입 라벨 없음 p6).

| bar | 의미 | R1(avg) | R2(engine) | 기준 | 판정 |
|---|---|---|---|---|---|
| **A BRAIN>FLAT** | 배선이 irreducible Φ 를 올림 | Φ 0.1105 vs 0.0085 | 0.1094 vs 0.0029 | ≥+0.05 | ✅ |
| **B BRAIN>RANDOM** | 같은 edge 수에서 connectome 이 random 이김 | brain_adv **+0.0237** | **+0.0230** | ≥0.015 | ✅ (SMALL) |
| **C RICH-CLUB** | hub 절단이 peripheral 절단보다 Φ 더 떨굼 | hub 0.0249 > peri 0.0155 | 0.0182 > 0.0138 | hub>peri | ✅ |
| **D LATERALIZATION (headline)** | A&G 같은 반구 강제 → Φ 떨어짐 | latcol 0.0865 < 0.1105 | 0.0767 < 0.1094 | latcol<brain | ✅ |
| **E EARNED full-shuffle** | 구조(geometry+백본) scramble → advantage 붕괴 | full_adv **+0.0007** ≤ ½·brain_adv | **+0.0005** ≤ ½·0.0230 | ≤½·brain_adv | ✅ |

**GREEN iff A∧B∧C∧D∧E** — 전부 PASS → 🟢.

### F (DISSOCIATION, NON-GATING diagnostic — 정직한 비결과 c9)

좌표만 scramble(백본 유지)하면 advantage 가 유지되는가? geom_adv(+0.0129) vs full_adv(+0.0007)는 averaging 설정에 따라 ≈동률 ~ 분리 사이를 오간다 — **coord-vs-topology 분리는 비강건**. "좌표 inert, 토폴로지 load-bearing" 을 깔끔히 분리 못 함 → 보고만 하고 게이트 안 함. (단일 N=600 probe 에선 분리 보였으나 multi-population 평균에선 약화 — honest non-result.)

## 정직 (c9) — 효과 크기와 한계

- **ROBUST (20/20 population realization, N=800):** A(brain≫flat ~50×) · D(A/G lateralization) · E(구조 scramble 붕괴). 이 셋이 헤드라인.
- **SMALL-but-reliable (≈15-19/20):** B(brain>degree-matched-random, mean +0.024) · C(rich-club hub, mean +0.016). 진짜 양(+)이나 **MODEST** — 단일 측정은 sample size/seed 에 따라 flip(N≤200 에서 종종 FAIL). population 평균으로 기댓값 측정.
- **B 의 원래 0.03 bar(Gaussian-mirror 추측)는 engine-uniform substrate 에서 borderline FAIL** — 엔진의 진짜 효과크기(+0.024)는 0.03 미만이라 reliably-detectable B_MIN_ENG=0.015 로 게이트. (H_1513 sibling 이 import 하는 `B_MIN=0.03` 상수는 호환 위해 유지.)
- **하드게이트1 분류:** R1 numpy = **DIRECTIONAL**(import torch/numpy 미러). R2 = ENGINE-NATIVE byte-exact (`ci_phi_iit4` live 호출) + WIRED.

## 결론

brain-faithful **connectome 토폴로지**(특히 A/G 반구 분리)는 flat/unwired 배치 대비 통합 Φ 를 **올린다**, 그리고 그건 **구조에 의존**(scramble 하면 붕괴)한다. 단, 같은 edge 밀도의 random 대비 advantage 는 **작다** — 이득의 대부분은 "구조적 배선이 있다는 것 자체" + lateralization 에서 오고, 특정 small-world/rich-club 조직이 random 보다 *얼마나* 나은지는 modest. anima 의 의식은 topology-FREE 가 아니라 **mildly topology-dependent** — A/G 좌/우 분리가 핵심 load-bearing 구조.

## SCOPE (UNVERIFIED)

TOY 15-lane / 합성 small-world·rich-club topology / 결정적 IIT4 min-cut(학습된 토폴로지 아님). B·C 효과 작고 sample-fragile · 해부 좌표 vs 토폴로지 분리 비강건 · scale / real 출판 connectome(→ H_1513 sibling 이 literal DSI 로 재현) / 가중 connectome / 동적 재배선 / live brain wiring(lane 들을 실제 이 공간 배치로 배선해 emit/routing 에 쓰기) UNVERIFIED. R2 single-population(seed 5120) — multi-population engine 평균은 follow-on.

## artifacts

- `state/1512_brain_topology/h1512.py` (R1 numpy mirror, polymorphic build_population — H_1513 sibling 의 Gaussian path 호환)
- verdict `state/verdicts/1512_brain_topology/H_1512_FREEZE.txt` · raw `H_1512_R1_mirror.txt` · engine `engine_cli_smoke.txt`
- `core/engine_cli.hexa` §BrainTopology · `core/engine_cli_smoke.hexa` cases 328-332 · `ARCHITECTURE.json` §BrainTopology

## xref

H_1510(QUORUM-KURAMOTO, 시간 dynamics — DISTINCT) · H_1513(LITERAL-CONNECTOME, real DSI scale-recheck — sibling) · H_1492(ConsciousnessIndex, ci_phi_multiinfo/ci_phi_iit4 통합 Φ 원천) · H_1280(소뇌) · H_1281(기저핵) · H_1294(PFC) · H_1295(spatial-map) · H_1448(시상/PhaseField) · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_phi_iit4_tool · a_break_the_wall · a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · p1·p6·p7·p8·c9
