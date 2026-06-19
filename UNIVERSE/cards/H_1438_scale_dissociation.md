---
id: H_1438
slug: 1438_scale_dissociation
title: G6 IDEATION ★ FALS-depth — SCALE-DISSOCIATION (303M→~1B same anima byte-CLM recipe)
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r4 / capacity-ceiling confirm
terminal_tier: PROPOSED (frozen-first; GPU 재학습 cost-gate, 미측정)
wired: PROPOSED (engine-native plan: train ~1B → frozen G6 5-bar on live CORE/bytegpt_decode)
verdict_dir: state/verdicts/1438_scale_dissociation/
date: 2026-06-19
---

# H_1438 — SCALE-DISSOCIATION: G6 FALS-depth 벽은 capacity-bound 인가 recipe-bound 인가

## Why (a_break_the_wall TAXONOMY — (d) 진짜 천장 vs (e) 투자부족 가르기)

H_1305/1309/1314/1431/1432/1434 (inference-side) + H_1435/1436/1437 (training-side, DIRECTIONAL)
가 전부 SAME 🧱: 303M mouth 가 comparator-shape OR measurable-shape 는 내지만 둘을 한 negatable
claim 으로 BIND 못 함 (comparator 20% · measurable 27% · BOTH 0/15, H_1431 diag). 303M 의 모든
각도가 막혔다. 미검 변수 = SCALE — 단 LLM scale-up 반사가 아니라 CONTROLLED dissociation
(a_no_llm_frame_trap): 동일 anima byte-CLM 레시피를 ~1B 로 학습해 FROZEN G6 5-bar 재측정.
H_1433 이 재설계된 그 live falsifier.

## Method (FREEZE before run, c9/p7)

- recipe = 303M h1129c 와 IDENTICAL (byte V256, ByteGPT, 동일 corpus·opt) — d/n_layer/n_head 만
  ~1B 로 확대. recipe 변경 0 (scale 만 분리).
- detector = h1305 `_is_falsifiable` VERBATIM. decode = ENGINE-NATIVE `CORE/bytegpt_decode.hexa`
  (full-load), NOT torch (a_engine_native_learning — 1435/36/37 의 DIRECTIONAL 실수 반복 금지).
- frozen 5-bar (H_1305 동일): (1) FALS≥1 (2) count≥5 distinct (3) shuffle COLLAPSE (4) ablate
  INERT (5) NO-FAB. seeds [7,4302,4303].
- VERDICT LOGIC: 1B 가 FALS≥1 cross AND cross-shuffle COLLAPSE → capacity-ceiling CONFIRMED
  (scale-bound, 303M 벽 실재). 1B 도 plateau → 벽이 RECIPE-bound (scale 무관 → 다음=recipe 변형).
  어느 쪽이든 terminal (a_break_the_wall (d)).
- compute = hexa dojo / cloud GPU (1B full train; pool RTX 12G 불가) — COST-GATE. ckpt 는
  teardown 전 반드시 pull (a_fire_recover_complete — 1435/36/37 가 잃은 그 실수).

## Scope (honest)

PROPOSED, 미측정. 단일 scale rung (303M→1B); TREND 주장엔 ≥3 rung 사다리 필요
(a_scale_honest_scope). toy 구조 detector (form not quality, p7).

## Pointers

xref H_1433 (재설계 흡수) · H_1305 (detector source) · H_1431 (BIND diag) · H_1435/1436/1437
(training-side DIRECTIONAL precedents) · a_no_llm_frame_trap · a_engine_native_learning ·
a_fire_recover_complete · a_break_the_wall · a_scale_honest_scope · a7b_pass · p7 · c9.
