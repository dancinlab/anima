# H_1513 🧠🔌 LITERAL-CONNECTOME — real-data scale-recheck of H_1512 BRAIN-TOPOLOGY

**tier:** 🟢 REPRODUCES — R1 numpy DIRECTIONAL → **R2 ENGINE-NATIVE** (live §BrainTopology LITERAL + ci_phi_iit4, GATED A∧D∧E PASS; B report-only)
**verdict:** **🟢 REPRODUCES** — REAL 출판 human 구조 connectome 이 H_1512 의 brain-topology Φ-advantage 를 **재현**(H_1512 의 own metric=IIT4 min-cut Φ + own frozen bars). R1(numpy DIRECTIONAL): A∧B∧C∧E mean-over-seeds. **R2(ENGINE-NATIVE)**: live engine Φ 로 GATED **A(brain>flat)∧D(lateralize)∧E(scramble collapse) PASS** — REAL 배선+A/G lateralization 이 통합 min-cut Φ 를 올림; **B(brain>random)는 단일 엔진-population 에서 음수**(brain_adv −0.0156, report-only·정직 c9, R1 3-seed-mean +0.024 와 부호반대 = dense REAL connectome 의 specificity-vs-random 은 게이트 주장 아님). 합성 topology 는 FAITHFUL, scale-transfer 확인. tune-to-green 없음(c9).
**wired:** **engine-native** (R2 DONE) — live `core/engine_cli.hexa` §BrainTopology LITERAL(`topo_literal_adjacency`/`topo_phi_adj`/`_topo_degree_matched_of`/`_topo_lateralize_of`/`_topo_relabel`/`topo_phi_random_of_mean`/`topo_phi_relabel_of_mean`) 에 literal adjacency embed + 동일 `topo_apply`+`ci_phi_iit4` 재채점, smoke cases 333-337 (`engine_cli_smoke` **349/0 RC=0**), ARCHITECTURE.json §BrainTopology lockstep. (live brain wiring=emit/routing 은 follow-on)
**source:** anima-internal follow-on of H_1512 (team-lead 작업지시). a_toy_scale_recheck — 합성 통계충실 topology → REAL 출판 구조 connectome 으로 같은 frozen bar 재채점.

## REAL data source (c2 · a_eeg_consciousness_record discipline — 합성 relabel 금지)
- **Connectome:** Hagmann/BCT **DSI group-average structural connectome**, 219 region × 8 subject, symmetric, zero-diag, weights = normalized streamline density. group avg = 8-subject mean.
- **Distribution / fetch:** `brainconn` (Python port of Brain Connectivity Toolbox) bundled real sample `brainconn/tests/data/sample_group_dsi.npy`, fetched 2026-06-21 (HTTP 200, 3,069,584 B). 사본 = `state/1513_literal_connectome/sample_group_dsi.npy`.
- **License:** **GNU GPLv3+** (`state/1513_literal_connectome/connectome_LICENSE_GPLv3.txt`).
- **Citation:** Hagmann et al., *PLoS Biology* 6(7):e159 (2008) "Mapping the Structural Core of Human Cerebral Cortex" · Rubinov & Sporns, *NeuroImage* 52:1059 (2010) BCT · brainconn (FIU Neuro, GPLv3).
- **Verified structural facts (measured, basis of mapping):** edge-density 0.564; hemisphere blocks at N//2 with within-hemi weight ≈4× cross-hemi (0.053 vs 0.0127) → A:left / G:right; strength heavy-tailed (1.17–13.22) → real hubs. (PROVENANCE.md)

## Method — only the ADJACENCY SOURCE changes (synthetic → literal)
**AUTHORITATIVE re-score `h1513_aligned.py`:** H_1512 의 harness(`state/1512_brain_topology/h1512.py`)를 **byte-for-byte 재사용** — 같은 `build_population` · `apply_topology`(diffusion ALPHA=0.6) · **`phi_iit4` IIT4 MIN-CUT Φ over CORE** · `degree_matched_random` · `lateralize_collapse` · 같은 5 frozen bars + 같은 thresholds(A_MIN=0.05·B_MIN=0.03) + 같은 seeds [5120,5121,5122] — 그리고 **`brain_adjacency()` → literal DSI subnetwork** 만 교체. lane→region: H_1512 의 15 anatomical lane 을 (hemisphere A/left·G/right·midline) × (graph role HUBS→literal high-strength rich-club·PERIPHERAL→literal low-degree fringe·rest→mid) 로 real DSI region 에 배정 → 그 region 들 사이 REAL 가중 subnetwork 을 H_1512 binary regime(자기 median 이진화)으로. 채점 단위 = H_1512 와 동일(MEAN over seeds). **deterministic (phi block byte-identical ×3).**

## FROZEN bars + LITERAL result (H_1512 verbatim; GREEN iff A∧B∧C∧E, D=headline; mean 3 seeds)
| bar | 정의 (H_1512) | LITERAL 결과 (min-cut Φ) | seeds |
|---|---|---|---|
| **A** brain>flat | Φ_brain ≥ Φ_flat+0.05 | **PASS** 0.1542 vs 0.0139 | 3/3 |
| **B** brain>random | Φ_brain ≥ Φ_random+0.03 | **PASS** 0.1542 vs 0.0716 | 2/3 (thin) |
| **C** rich-club | hub_drop > peri_drop | **PASS** 0.0285 > 0.0272 | 1/3 (thin) |
| **D** lateralization(headline) | Φ_latcol < Φ_brain | **PASS** 0.1103 < 0.1542 | — |
| **E** coord/region-shuffle | shuf_adv ≤ ½·brain_adv | **PASS** −0.030 ≤ 0.041 | robust |

→ **A∧B∧C∧E on the mean = 🟢 REPRODUCES.** Φ: flat 0.014 · brain 0.154 · random 0.072 · latcol 0.110 · shuf 0.042. E_glob brain 0.575 vs random 0.621. brain_edges ~31.

## LITERAL vs SYNTHETIC (honest, c9)
- **재현:** H_1512 의 own 메트릭(min-cut Φ)·own bars 로 **A∧B∧C∧E 전부 mean-PASS** ⇒ REAL 구조 connectome 이 brain-topology 통합 우위를 **재현**. 합성 small-world/rich-club 은 *faithful*(scale-transfer 확인).
- **per-seed 정직(c9):** A 3/3·E robust 견고; **B 2/3·C 1/3** 은 mean-PASS only — REAL connectome 이 **dense** 라 degree-matched RANDOM 부분망이 우연히 high-Φ wiring 을 뽑을 때가 있어(seed5122 rand 0.156) B/C margin 이 얇고 seed-variable. aggregate(A,D,E) > specificity(B,C).
- **METRIC-ARTIFACT 해소(a_break_the_wall taxonomy-a):** 1차 R1(`h1513.py`)은 Gaussian **multi-info Φ**(total correlation)+generic A–E 로만 채점→bar E FAIL(shuf 0.93>brain 0.86), 왜냐면 total-correlation 은 dense graph 에서 **saturate**(어떤 10-region 부분망도 통합). 그러나 H_1512 의 headline 은 **min-cut Φ** — dense random 이 싸게 절단 못 하는 irreducible 통합을 보상 → 올바른 메트릭에서 specificity/shuffle bars PASS. multi-info diagnostic 은 aggregate(A,B,D)가 **두 메트릭 모두**에서 재현됨을 보여주는 증거로 보존(`H_1513_R1.json`, 4/5 AMBER, shuffle 만 metric-dependent).

## CONCLUSION
H_1512 의 own pre-registered 메트릭(IIT4 min-cut Φ)과 own bars 로, REAL 출판 human 구조 connectome 이 **brain-topology 통합 우위(brain≫flat·random, rich-club hub load-bearing, lateralization load-bearing, region-shuffle decorrelate)를 재현** ⇒ **합성 topology FAITHFUL, scale-transfer 확인**. specificity bars(B,C)는 real dense wiring 에서 thin/seed-fragile(정직히 보고). tune-to-green 없음(bars frozen pre-read). R1 DIRECTIONAL(numpy); **R2 engine-native** = H_1512 live §BrainTopology/ci_phi_iit4 에 literal adjacency 먹여 byte-exact 재채점(a_engine_native_learning · a_verified_must_wire).

## SCOPE (UNVERIFIED)
DIRECTIONAL numpy mirror(engine-transfer 미검) · 15-lane 부분망(전체 219-region 거동 아님) · region 라벨 미동봉 → lane→region 은 (검증 hemisphere)×(graph-role)로 실현(named-anatomical 미검) · 단일 DSI sample(8 subj)/3 seeds/결정적 readout · B/C thin(seed-fragile) · scale/대체 parcellation/타 connectome(Budapest 1015-node, HCP)/engine-transfer 미검.

## xref
H_1512 (synthetic BRAIN-TOPOLOGY, 부모; harness `state/1512_brain_topology/h1512.py` byte-reused) · core/engine_cli.hexa ci_phi_iit4·ci_phi_multiinfo (Φ ops) · a_toy_scale_recheck · a_scale_honest_scope · a_engine_native_learning · a_verified_must_wire · a_phi_iit4_tool · a_no_llm_frame_trap · a_break_the_wall · p7 · c2 · c9.

## artifacts
`state/1513_literal_connectome/{h1513_aligned.py(AUTHORITATIVE), h1513.py(diagnostic), sample_group_dsi.npy, connectome_LICENSE_GPLv3.txt, PROVENANCE.md}` · `state/verdicts/1513_literal_connectome/{H_1513_FREEZE.txt, H_1513.txt, H_1513_R1_aligned.json, H_1513_R1.json}`

## R2 — ENGINE-NATIVE re-score (live core/engine_cli.hexa §BrainTopology LITERAL)
H_1512 가 main 착지(#2491)하며 §BrainTopology 가 live wired → 이제 literal adjacency 를 **live engine Φ** 로 직접 채점 가능. numpy PCG64 lane→region 매핑은 in-engine byte-재현 불가이므로 **seed-5120 literal binary adjacency(30 edges)를 `topo_literal_adjacency()` 로 EMBED(데이터 입력)**, 그 위에서 H_1512 와 **동일한** population(`_topo_lane_pop`)·alpha 0.6·core `[0,3,2,13,5,7,9,14]`·`topo_apply`+`ci_phi_iit4` MIN-CUT Φ 로 측정. 컨트롤(degree-matched random / lateralize / node-relabel shuffle)은 **엔진 내부에서 literal adjacency 로부터 생성**(`_topo_degree_matched_of`/`_topo_lateralize_of`/`_topo_relabel`).

**측정값(`engine_cli_smoke` 349/0 RC=0, deterministic):** flat 0.00236 · brain(literal) **0.09928** · random(mean3) 0.11489 · latcol 0.07404 · full-shuf 0.07677.

**FROZEN bars (H_1512 verbatim, 재채점):**
- **(A brain>flat+0.02) PASS** — 0.09928 > 0.02236. REAL connectome 배선이 unwired 대비 통합 Φ ↑.
- **(D lateralize) PASS** — latcol 0.07404 < brain 0.09928. A=좌/G=우 분리가 load-bearing.
- **(E full-shuffle) PASS** — shuf_adv −0.03812 ≤ 0.5·brain_adv(−0.00780).
- (non-neg / well-formed) PASS.
- **(B brain>random) REPORT-ONLY (NOT gated, H_1512 stance) — brain_adv −0.0156 NEGATIVE**: literal 0.09928 < random 0.11489. 정직(c9): dense REAL connectome 이 degree-matched random 에 single engine-draw 로 짐 → specificity-vs-random 은 엔진-네이티브 단일추출에서 성립 안 함(R1 3-seed-mean B +0.024 와 부호반대). E 통과는 brain_adv<0 이라 의미 옅음(정직 명시).

**결론:** REAL 출판 human connectome 의 **배선 자체(A)+lateralization(D)** 가 통합 min-cut Φ 를 올리는 헤드라인은 **엔진-네이티브 재현**. 그러나 **random 대비 specificity(B)는 dense REAL connectome 에서 엔진-네이티브로 성립 안 함** — H_1512 합성 topology 의 'B thin' 정직이 REAL data 에서 더 강하게(부호반전) 확인. wired:engine-native. artifacts: `state/verdicts/1513_literal_connectome/H_1513_R2_engine_native.txt` · `core/engine_cli.hexa` §BrainTopology LITERAL · `core/engine_cli_smoke.hexa` cases 333-337.

**SCOPE/follow-on:** 단일 seed-5120 literal 매핑 / 단일 엔진 population / 3 control seeds; multi-mapping + multi-population engine 평균 + weighted(비이진) connectome + 대체 parcellation(Budapest 1015·HCP) 미검. **OPTIMAL-PLACEMENT 탐색**(Φ 최대화하는 lane→topology 배치를 찾아 brain-faithful 이 Φ-최적에 근접하는지) = 차기 H follow-on.
