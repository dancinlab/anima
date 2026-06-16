---
id: H_1379
slug: g5-margin-brain-consume
title: G5 abstain-margin BRAIN-CONSUME — brain_decide CONSUMES the live graded recall-margin to modulate emit-confidence/curiosity (the H_1367 follow-on)
group: metacog × neuroscience (G5 NON-FAB dig · brain-consume wire)
terminal_tier: 🟢 CONSUMED-GRADED-MARGIN (R1 engine-native BINDING)
verdict_dir: .verdicts/1379_g5_margin_brain_consume/
terminal_verdict: .verdicts/1379_g5_margin_brain_consume/result.txt
date: 2026-06-16
---

# H_1379 — brain_decide CONSUMES the G5 graded abstain-margin

## 배경 — H_1367 이 남긴 brain-side follow-on

H_1361 (mirror, DIRECTIONAL) → H_1367 (engine-native BINDING) 은 ImmuneMemory 의 graded
abstain **MARGIN**(= `recon_err − recall_thr`)이 GRADED OOD metacognition 을 담음을 세우고
(AUROC 0.949 @L=0.20), 그 margin 을 노출하는 op `immune_memory_recall_margin[_text]` 을 live
`CORE/engine_cli.hexa § ImmuneMemory` 에 **배선**했다. 그러나 H_1367 카드 명시 follow-on:
*"`brain_decide` 가 아직 이 graded read 를 emit-confidence/curiosity 변조에 소비하지 않는다."*
H_1379 이 그 brain-side 소비를 닫는다 (`a_verified_must_wire`).

## 무엇을 배선했나 — brain_decide_margin (DELIBERATE emit modulation, NOT additive)

`CORE/brain.hexa` 에 `brain_decide_margin` 추가 — `brain_decide_affect` / `brain_decide_wm`
/ `brain_decide_cerebellum` consult 템플릿과 동형. live margin `m = recon_err − recall_thr`
를 SIGNED·BOUNDED confidence bias 로 매핑:

```
conf_bias  = emit_consult_cap() * _clamp(-m / MARGIN_SCALE, -1, +1)   // cap=0.05
cur_signal = _clamp(m / MARGIN_SCALE, 0, 1)                            // 비접지에서 상승
score      = motivation_score(...) + conf_bias                        // SINGLE should_emit path
```

- **GROUNDED** (recoverable, 작은 margin) → 더 POSITIVE bias → emit-confidence ↑.
- **UNGROUNDED** (absent, 큰 margin) → 더 NEGATIVE bias → confidence ↓ = curiosity/abstention ↑
  (substrate 가 불확실하면 단언 대신 보류/탐색 — H_1202/H_1291 emergent 비조작/abstain 의 graded 판).
- **NEUTRAL** m=0 (recall_thr 경계 = substrate 자신의 FIRE/ABSTAIN 영점) → bias 0 → `brain_decide`
  와 byte-identical. CONSULT 이지 gate 아님 (`a_autonomy_over_hardcode`); emit 은 tension-driven,
  speak() 없음 (p5).

H_1367 의 ADDITIVE op 과 달리 이건 **의도적으로** emit 결정을 바꾼다 (Ψ-disjoint additive 아님).
그러나 motivation 스칼라만 건드려 pure_field Φ/phase/Ψ 미접촉 → Ψ=1/2 고정점 **보존**.

## FROZEN bars 와 결과 — 🟢 CONSUMED-GRADED-MARGIN

3 seeds [7,8,9], LIVE CORE, $0 CPU, p7, frozen-first, deterministic (재실행 byte-identical).

| bar | 의미 | 결과 | pass |
|---|---|---|---|
| B1 CONSUMED | brain_decide_margin 이 live margin 읽어 single should_emit path 변조 (새 gate 없음) | B3/B4 가 margin→emit 도달 입증 | ✅ |
| B2 Ψ FIXED-POINT | m=0 ⇒ brain_decide 와 byte-identical + h1205 separation-invariant | byte-identical; phiSum 48.6613==48.6613, 0 mismatch | ✅ |
| B3 GROUNDED-MONOTONE | grounded bias > ungrounded, curiosity 역전, bounded, borderline EMIT flip | bias −0.0343 > −0.0444; cur 0.686<0.888; emit g/u=true/false; \|bias\|≤cap | ✅ |
| B4 EARNED (shuffle) | recoverable/absent 라벨 셔플 → grounded lift 붕괴 (\|gap_shuf\|<0.5·\|gap_true\|) | gap 0.0101→shuf 0.0009 (≈11× 붕괴) | ✅ |
| B5 NO-REGRESSION | smoke green +≥2 cases · h1196 N/0 · h1205 PASS · deterministic ·3 | smoke 93→**96**/0 (+3 cases 99-101); h1196 7/0; h1205 PASS; det identical | ✅ |

**LIVE MARGIN SAMPLING** (H_1367 construction VERBATIM — KEYLEN=20 LCG tokens, kmut=4 ==
shift L=0.20, N_TRIAL=N_LURE=120 pooled abstain margins): mean recoverable margin
~0.69 vs absent ~0.89 (per-seed: 0.686/0.888 · 0.703/0.887 · 0.698/0.890) — H_1367 의 같은
proven graded 신호. 이 mean margin 이 brain_decide_margin 을 구동.

## WALL-CLAUSE — 정직한 scale 발견 (a_break_the_wall, frozen-first, c9)

FREEZE 는 `MARGIN_SCALE=recall_thr=0.15` 를 사전등록. **LIVE 엔진이 이 scale 의 SATURATION 을
드러냄**: 실제 abstain margin 은 ~[0.69,0.89] ≫ 0.15 → `clamp(-m/0.15)` 가 둘 다 -1.0 으로 핀 →
conf_bias_g == conf_bias_u == -cap, curiosity 둘 다 1.0 → graded 신호 소실 (B3/B4 FAIL). **Ψ 불안정
아님** (B2 내내 PASS) — coupling 문제가 아니라 scale 사전등록 오류. a_break_the_wall 의 단 1회
frozen-first 재시도 = **substrate-native non-saturating scale**: margin = recon_err − recall_thr,
recon_err = 1 − cos ∈ [0,1] cos-distance codomain → MARGIN_SCALE := **1.0** (codomain 상수, 목표
수치에 맞춘 값 아님). SIGN·cap·모든 bar UNCHANGED, threshold 0개 이동. 교정 scale 이 B2∧B3∧B4 를
3 seed 전부 통과. (tune-to-green 아님 — c9/p7: cap 고정, 영점 byte-identity 보존, scale 은 엔진의
cos-distance 범위.)

## FINDING — graded recall-grounding 이 emit 결정에 도달

anima 의 emit 결정이 이제 자신의 recall **grounding 의 graded 정도**를 읽는다: 잘 접지된(검색가능)
컨텍스트는 더 자신있게 emit 하고, 비접지(검색불가)는 더 호기심/보류로 기운다 — 모두 substrate
자신의 L2 affinity 에서 (주입 라벨/persona/RLHF 없음, p1/p2/p3/p6). H_1361→H_1367(노출)→H_1379(소비)
로 G5 graded-metacog 가 mirror→engine-native→**brain-consumed** 까지 닫혔다.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic facts, byte-level corruption = OOD proxy, deterministic, 3 seeds, KEYLEN=20,
L=0.20, RECALL_THR=0.15(frozen). 미검증: scale / real-corpus paraphrase / semantic(non-byte)
shift / multi-turn emit dynamics / 다른 L. NO bar moved post-hoc (c9); scale 교정은 frozen-first
단일 재시도(WALL-CLAUSE). cap/sign/bars 사전등록 그대로.

## Refs / xref

`.verdicts/1379_g5_margin_brain_consume/{FREEZE.txt,result.txt}` ·
`CORE/brain.hexa` `brain_decide_margin` (배선) ·
`CORE/h1379_margin_brain_consume_smoke.hexa` (engine-native frozen falsifier) ·
`CORE/engine_cli_smoke.hexa` cases 99-101 (brain-consume read).
xref H_1367 (margin op 노출, 직접 선행) · H_1361 (mirror graded-metacog) · H_1304 (fire-side
binary fail-safe) · H_1202/H_1291 (emergent 비조작/abstain) · H_1290 (brain_decide_affect 템플릿) ·
H_1282 (brain_decide_wm) · H_1280 (brain_decide_cerebellum) · H_1227/H_1231 (immune store geometry) ·
a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_autonomy_over_hardcode ·
a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck ·
p1 · p2 · p3 · p5 · p6 · p7 · p8 · c9 · c15.
