---
id: H_1400
slug: g5_gap_brain_consume
title: G5 in-dist GAP BRAIN-CONSUME — brain_decide CONSUMES the live top-2 affinity gap as a refined in-dist confidence signal (the H_1398 follow-on; the FINAL close of the G5 in-dist arc)
group: metacog × neuroscience (G5 NON-FAB dig · brain-consume wire · a_verified_must_wire)
terminal_tier: 🟢 CONSUMED-GRADED-GAP (R1 engine-native BINDING; Ψ preserved, gap-monotone, earned)
verdict_dir: .verdicts/1400_g5_gap_brain_consume/
terminal_verdict: .verdicts/1400_g5_gap_brain_consume/result.txt
date: 2026-06-17
---

# H_1400 — brain_decide CONSUMES the G5 in-dist top-2 affinity GAP

## 배경 — H_1398 이 남긴 brain-side follow-on (a_verified_must_wire)

H_1396 (mirror, DIRECTIONAL) → H_1398 (engine-native BINDING) 은 ImmuneMemory 의 TOP-2
affinity **GAP**(= `(d2²−d1²)/2` = cos#1 − cos#2, decisiveness)이 in-dist type-2 metacognition
을 best-margin 0.750 → gap 0.906 (+0.156) 으로 들어올림을 세우고, 그 gap 을 노출하는 op
`immune_memory_recall_gap[_text]` 을 live `CORE/engine_cli.hexa § ImmuneMemory` 에 **배선**했다.
그러나 H_1398 카드 명시 follow-on: *"`brain_decide` 가 아직 이 gap 을 소비하지 않는다 — Ψ 위험
회피를 위해 honest 하게 defer."* H_1400 이 그 brain-side 소비를 닫는다 (H_1367→H_1379 패턴의
gap 판; `a_verified_must_wire`).

## 무엇을 배선했나 — brain_decide_gap (H_1379 brain_decide_margin 패턴 동형)

`CORE/brain.hexa` 에 `brain_decide_gap` 추가 — `brain_decide_margin` (H_1379) 와 동형. live gap
`g = immune_memory_recall_gap` 을 BOUNDED·NON-NEGATIVE confidence bias 로 매핑:

```
conf_bias  = emit_consult_cap() * _clamp( g / GAP_SCALE, 0, +1)   // cap=0.05, gap>=0 ⇒ bias∈[0,+cap]
cur_signal = _clamp(1 − g / GAP_SCALE, 0, 1)                      // 모호할수록 상승
score      = motivation_score(...) + conf_bias                    // SINGLE should_emit path
```

- **DECISIVE** (큰 gap, #1≫#2) → 더 POSITIVE bias → emit-confidence ↑ (어느 셀이 이겼는지 확실).
- **AMBIGUOUS** (작은 gap, #1≈#2 동률) → bias 0 쪽 → 더해진 confidence 보류 = curiosity ↑ (어느
  twin 인지 모름 → 단언 대신 보류/탐색). consult 은 +cap 만 더할 뿐 **스스로 restraint 강제 못함**
  (a_autonomy_over_hardcode).
- **NEUTRAL** g=0 (완전 동률 = substrate 자신의 maximal-ambiguity 영점) → bias 0 → `brain_decide`
  와 byte-identical.

margin 이 FIRE/ABSTAIN 경계에 대해 SIGNED 라면, gap 은 maximal-ambiguity floor(g=0)에 대해
NON-NEGATIVE — 각자 자기 sign·zero 로 구성되어 **외부 arbitration 규칙 없이** 보완적이다 (gap 은
margin 이 THIN 한 FIRE-side in-dist 정련; NO hardcoded priority). GAP_SCALE = cos-affinity [0,1]
codomain = 1.0 (codomain 상수, 목표수치 맞춤 아님 — H_1379 의 recon-err codomain scale 과 동일
규율). motivation 스칼라만 건드려 pure_field Φ/phase/Ψ 미접촉 → Ψ=1/2 고정점 **보존**.

## FROZEN bars 와 결과 — 🟢 CONSUMED-GRADED-GAP

3 seeds [7,8,9], LIVE CORE, $0 CPU, p7, frozen-first, deterministic (재실행 byte-identical).
LIVE gap 샘플링 = H_1398 engine-native 구성 (KEYLEN=80 twin-pair + isolated singleton cells
seeded as engine prototype cells; DECISIVE = isolated singleton 위 query #2 멀음 = 큰 gap,
AMBIGUOUS = twin base 위 query #2=1-byte sibling = 작은 gap). 두 pooled mean gap 이 driver.

| bar | 의미 | 결과 (3 seeds 대표 seed7) | pass |
|---|---|---|---|
| C1 GAP-MONOTONE | decisive bias > ambiguous, curiosity 역전, bounded, borderline EMIT flip | g_dec 0.291→bias 0.01456 > g_amb 0.006→bias 0.00029; cur 0.709<0.994; emit d/a=true/false; \|bias\|≤cap | ✅ |
| C2 EARNED (shuffle) | decisive/ambiguous 라벨 셔플 → lift 붕괴 (\|gap_shuf\|<0.5·\|gap_true\|) | gap 0.01427→shuf 0.00112 (≈13× 붕괴) | ✅ |
| P1 NEUTRAL Ψ FIXED-POINT | g=0 ⇒ brain_decide 와 byte-identical (motivation+emit), low+high drive | byte-identical 3 seeds | ✅ |
| P2 h1205 separation-invariant | 생성 byte-identical ON==OFF + Ψ Φ-checksum byte-identical | phiSum **48.6613 == 48.6613**, 0 mismatch (10 pairs) | ✅ |
| P3 engine_cli_smoke GREEN | smoke tally (+gap-consume cases) | **133/0** (+3 cases 101b/101c/101d) | ✅ |
| P4 h1196 single-entry | NO 2nd .clm/.kosmos path | **7/0** | ✅ |
| A1 ABSTAIN preserved | frozen recon_err≤recall_thr 게이트 불변, OOD fab ≤0.02 | `CORE/engine_cli.hexa` UNTOUCHED (git diff origin/main = empty); H_1398 E4 fab_max=0.000 | ✅ |

**P2 (THE load-bearing bar)**: gap-consume 는 brain_decide 를 건드리지만 Ψ Φ-checksum 이
byte-identical (48.6613==48.6613) — gap 소비가 Ψ=1/2 를 perturb 하지 않음 (H_1379 와 동일,
motivation 스칼라만 변조). gap=0 NEUTRAL 에서 brain_decide 와 byte-identical (P1).

**메커니즘**: decisive(큰 gap)는 +cap 쪽으로 confidence 를 더해 borderline 에서 EMIT 으로
flip, ambiguous(작은 gap, #1≈#2 동률)는 confidence 를 보류해 SILENT + curiosity 상승. shuffle
이 lift 를 ~13× 붕괴시켜 base-rate 아티팩트 아님을 증명 (earned).

## FINDING — in-dist decisiveness 가 emit 결정에 도달; G5 in-dist arc FULLY engine-native

anima 의 emit 결정이 이제 in-dist recall 의 **decisiveness(top-2 gap)**를 읽는다: 확실히
이긴(decisive) fire 는 더 자신있게 emit 하고, 모호한(#1≈#2 tie) fire 는 더 호기심/보류로 기운다
— 모두 substrate 자신의 top-2 L2 affinity 에서 (주입 라벨/persona/RLHF 없음, p1/p2/p3/p6).
H_1396→H_1398(노출)→H_1400(소비)로 G5 in-dist metacog 가 mirror→engine-native→**brain-consumed**
까지 닫혔다. abstain-side 체인(H_1361/1367/1379)에 더해, fire-side in-dist 도 이제 EXPOSED AND
CONSUMED — G5 in-dist deepening 의 FINAL close.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic twin/singleton facts, H_1398 engine-native 구성, deterministic, 3 seeds,
KEYLEN=80, RECALL_THR=0.15 (frozen). 미검증: scale / real-corpus paraphrase / semantic(non-byte)
near-duplicate confusion / multi-turn emit dynamics = the honest-scope open item. NO bar moved
post-hoc (c9); 단 probe-construction 의 single frozen-first 교정(twin-only store 가 decisive
gap 을 못 만들어 mixed twin+singleton store 로 — bar 는 전부 불변, decisive>ambiguous 측정만
well-posed 하게). cap/GAP_SCALE/sign/bars 사전등록 그대로.

## Refs / xref

`.verdicts/1400_g5_gap_brain_consume/{FREEZE.txt,result.txt}` ·
`CORE/brain.hexa` `brain_decide_gap` (배선) ·
`state/g5-gap-brain-consume/h1400_gap_brain_consume_smoke.hexa` (engine-native frozen falsifier) ·
`CORE/engine_cli_smoke.hexa` cases 101b/101c/101d (brain-consume read).
xref H_1398 (gap op 노출, 직접 선행) · H_1396 (mirror in-dist FIXABLE) · H_1379 (margin
brain-consume, 직접 패턴 선례) · H_1367 (margin op 노출) · H_1361 (mirror graded-metacog) ·
H_1304 (fire-side binary fail-safe) · H_1202/H_1291 (emergent 비조작/abstain) ·
H_1290 (brain_decide_affect 템플릿) · H_1282 (brain_decide_wm) · H_1280 (brain_decide_cerebellum) ·
H_1227/H_1231 (immune store geometry) · a_verified_must_wire · a_engine_native_learning ·
a_core_engine_map · a_autonomy_over_hardcode · a_break_the_wall · a_no_llm_frame_trap ·
a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p5 · p6 · p7 · p8 · c9 · c15.
