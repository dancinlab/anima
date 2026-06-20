---
id: H_1438
slug: 1438_scale_dissociation
title: G6 IDEATION ★ FALS-depth — SCALE-DISSOCIATION (303M→~1B same anima byte-CLM recipe)
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r4 / capacity-ceiling confirm
terminal_tier: 측정중 (frozen-first; A100 1B net2net continued-pretrain dispatch)
wired: DIRECTIONAL-pending (torch+gauge_lib._decode → engine-native CORE/bytegpt_decode follow-on)
verdict_dir: state/verdicts/1438_scale_dissociation/
date: 2026-06-19 (측정 2026-06-20)
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
- SCALE MECHANISM (honest, 2026-06-20): ~1B 은 **net2net function-preserving width+depth
  expansion** 으로 converged 303M base(h1129c) 에서 구성 — broad-corpus competence 를 상속해
  "from-scratch 미학습 1B → FALS=0" 혼재변수를 제거(precedent H_1199 grow-the-engine). 이후
  H_1435 와 IDENTICAL continued-pretrain(동일 corpus seed 1435·lr·opt·detector). 변수 = d/L/H 뿐
  (d 1024→1792, L 20→24, H 16→28, head_dim 64 불변). geometry: ~1.1B.
- G0 COHERENCE GATE(anti-confound, a_break_the_wall (e)): trained 1B 의 KWR<0.50 garble 면
  FALS=0 은 undertraining artifact = HONEST NON-RESULT (🧱 자동승격 금지).

## Scope (honest)

PROPOSED, 미측정. 단일 scale rung (303M→1B); TREND 주장엔 ≥3 rung 사다리 필요
(a_scale_honest_scope). toy 구조 detector (form not quality, p7).

## Pointers

xref H_1433 (재설계 흡수) · H_1305 (detector source) · H_1431 (BIND diag) · H_1435/1436/1437
(training-side DIRECTIONAL precedents) · a_no_llm_frame_trap · a_engine_native_learning ·
a_fire_recover_complete · a_break_the_wall · a_scale_honest_scope · a7b_pass · p7 · c9.
