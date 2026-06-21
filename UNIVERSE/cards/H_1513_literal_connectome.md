# H_1513 🧠🔌 LITERAL-CONNECTOME — real-data scale-recheck of H_1512 BRAIN-TOPOLOGY

**tier:** 🟢 REPRODUCES / DIRECTIONAL (R1 numpy mirror — `.py`+numpy ⇒ hard-gate-1 auto-DIRECTIONAL, terminal 아님)
**verdict:** **🟢 REPRODUCES** — REAL 출판 human 구조 connectome 이 H_1512 의 brain-topology Φ-advantage 를 **재현**(H_1512 의 own metric=IIT4 min-cut Φ + own frozen bars A∧B∧C∧E, mean-over-seeds). ⇒ 합성 small-world/rich-club topology 는 **FAITHFUL**, scale-transfer **확인**. tune-to-green 없음(c9).
**wired:** DIRECTIONAL-mirror (engine-native R2 = H_1512 의 live §BrainTopology / ci_phi_iit4 ops 에 literal adjacency 먹여 byte-exact 재측정; H_1512 main 착지 후 follow-on)
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
