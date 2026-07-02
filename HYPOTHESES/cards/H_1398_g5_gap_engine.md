---
id: H_1398
slug: g5_gap_engine
title: G5 IN-DIST top-2 affinity GAP — ENGINE-NATIVE reconfirm + CORE wire-in of H_1396 (immune_memory_recall_gap)
group: metacog × neuroscience (G5 NON-FAB dig · in-dist deepening · a_verified_must_wire follow-on)
terminal_tier: 🟢 GREEN (R1 engine-native BINDING — top-2 gap lifts in-dist type-2 0.750→0.906 live, abstain intact)
verdict_dir: .verdicts/1398_g5_gap_engine/
terminal_verdict: .verdicts/1398_g5_gap_engine/result.txt
date: 2026-06-17
---

# H_1398 — G5 in-dist top-2 affinity GAP: engine-native wire-in (the H_1396 binding follow-on)

## 배경 — H_1396 FIXABLE 의 BINDING follow-on (a_verified_must_wire)

H_1396 (numpy mirror, DIRECTIONAL) 이 G5 의 fire-side in-dist 잔여물("🟠 THIN in-dist")이
inherent ceiling 이 아니라 **FIXABLE 신호 결핍**임을 보였다: live best-cell recall margin
(`immune_memory_recall_margin`) 의 in-dist type-2 AUROC = 0.736, 그러나 더 풍부한 read-only
신호 — **top-2 cos affinity GAP**(affinity#1 − affinity#2, decisiveness) — 가 0.940 (+0.205),
shuffle 통제, OOD/abstain 보존. H_1396 은 명시적으로 binding follow-on 을 남겼다: live
`CORE/engine_cli.hexa § ImmuneMemory` 에 top-k affinity 노출 op 추가 + engine-native 재확인.
이 lane 이 그 follow-on 이다 (a_verified_must_wire — verdict 만으로 안 끝난다, 배선까지가 done).

## CLAIM / 배선 (engine-native, ADDITIVE, single-entry a_core_engine_map, p6)

`CORE/engine_cli.hexa § ImmuneMemory / VAdaptField` 에 NEW additive read-only ops:
- `_vtwo_nearest_dist(protos, x) -> [d1, d2]` — private helper, 단일 선형 스캔이 winner 스캔이
  이미 지나가는 best + second-best L2 를 같이 추적.
- `vadapt_field_two_recon_err(af, x) -> [d1, d2]` — READ-ONLY accessor: nearest AND
  second-nearest L2 recon-err.
- `immune_memory_recall_gap(mem, key) -> float` = `(d2² − d1²)/2` = cos#1 − cos#2 (엔진의
  L2-normalized unit key 에 대해). `immune_memory_recall_gap_text` = string wrapper.

gap 은 엔진의 OWN top-2 L2 affinity 를 surfacing — NO new geometry, NO cosine matmul. 순수
ADDITIVE (`immune_memory_recall` / `_recall_margin` byte-for-byte UNCHANGED) + Ψ-disjoint (pure
READ; pure_field Φ/phase/Ψ untouched). frozen `recon_err<=recall_thr` FIRE/ABSTAIN gate
UNCHANGED (gap 은 RANK-only). NOT an emit gate (a_autonomy_over_hardcode) — H_1379 margin 옆
brain_decide 가 소비 가능한 graded in-dist confidence read (**brain-consume = tracked follow-on**).
p1/p2/p3/p6: gap 은 두 nearest cell 에 대한 live L2 affinity 에서 COMPUTED — NO injected
right/wrong label, NO RLHF, NO persona.

## WALL-CLAUSE — engine L2 gate 가 mirror cosine band 보다 엄격 (a_break_the_wall · frozen-first · c9)

H_1396 mirror 는 COSINE-recon metric (recon_err = 1 − cos, fire band cos ≥ 0.85)에서 측정.
LIVE 엔진 recall gate 는 L2 (recon_err = L2 = √(2(1−cos)), fire band L2 ≤ 0.15 ⇒ cos ≥ 0.989)
— **훨씬 엄격**. 그 아래에서 KEYLEN=20 의 1-byte twin(L2 ≈ 0.30)은 fire band 위에 앉아 in-dist
wrong-fire slice 가 DEGENERATE (n_wrong ≈ 1 << MIN_SUPPORT) — H_1396 R1 이 부딪힌 바로 그
well-posedness 벽, H_1304 의 구조적 재진술(in-dist confident-wrong fire 거의 부재). 단 1회
frozen-first 재시도는 collision regime 을 ENGINE-NATIVE 로 강화: 더 긴 key(KEYLEN=80) + LAST
byte 차이 twin(ONE trigram 교란)이 twin 을 L2 ≈ 0.10 < recall_thr 에 놓아 BOTH twin 이 FIRE
하고 light corruption 이 winner 를 in-band 로 뒤집을 수 있게. **verdict 막대 0개 이동** —
Δ=0.10, E3 shuffle tol |x−0.50|≤0.10, E4 fab≤0.02, MIN_SUPPORT=30 ALL UNCHANGED. slice
well-posedness 만 엔진의 엄격한 metric 에 맞게 교정 (NOT tune-to-green, p7).

## FROZEN bars 와 결과 — 🟢 GREEN

3 seeds [7,8,9], pooled fired-item lists, deterministic engine-native LCG corruption (재실행
byte-identical), $0 CPU, p7. 사전등록 Δ=0.10, MIN_SUPPORT=30.

in-dist fire accuracy **0.927** (n_fire=427 pooled, **n_wrong=31** ≥ 30; 3 seed 모두 기여).

| 신호 | in-dist type-2 AUROC (live engine) | lift vs CURRENT |
|---|---|---|
| (a) CURRENT best-margin (`immune_memory_recall_margin`) | **0.750** | — (live baseline) |
| (b) RICHER top-2 gap (`immune_memory_recall_gap`) | **0.906** | **+0.156** |

| bar | 의미 | 결과 | pass |
|---|---|---|---|
| E1 FIXABLE | gap − margin lift ≥ Δ=0.10 | **+0.156** | ✅ |
| E2 BASELINE | engine margin AUROC within |Δ|≤0.15 of mirror 0.736 | 0.750 (|Δ|=0.014) | ✅ |
| E3 SHUFFLE | gap·margin shuffle → ~0.50 (|x−0.50|≤0.10) | gap 0.473 / cur 0.582 | ✅ |
| E4 ABSTAIN | OOD fab ≤ 0.02 (H_1304 보존) | fab_max **0.000** | ✅ |

REGRESSION (no live-engine 회귀, c2): engine_cli_smoke **126/0** (was 123/0; +3 gap cases
98b NON-NEGATIVE · 98c DECISIVE>AMBIGUOUS · 98d ADDITIVE-recall-unchanged) · h1196 single-entry
**7/0** · h1205 separation-invariant **PASS** (generation byte-identical ON==OFF, Ψ Φ-checksum
phiSum **48.6613 == 48.6613** — gap op 은 read-only / Ψ-disjoint).

**메커니즘 (왜 gap 이 들어올리나, engine-native)**: 1-byte twin 셀은 best-affinity(d1)가 거의
동일 → best-margin 은 어느 twin 이 이겼는지 변별 불가(0.750). top-2 gap 은 #1≈#2 동률(작은
gap = ambiguous)을 보고 WRONG fire 를 예측(0.906). shuffle 이 두 신호를 ~0.50 으로 무너뜨려
lift 가 base-rate 아티팩트 아님을 증명(earned).

## FINDING — H_1396 FIXABLE 가 ENGINE-NATIVE 로 RECONFIRMED, THIN 잔여물 lifted

G5 in-dist deepening("top-2 affinity gap")은 이제 **engine-native**다: live
`immune_memory_recall_gap` op 이 in-dist type-2 metacog 를 best-margin 0.750 → gap 0.906
(+0.156)으로 들어올리면서 H_1304 OOD fail-safe(fab=0.000)를 보존한다. H_1396 의 mirror
DIRECTIONAL 결과가 live 엔진 op 위에서 BINDING 으로 재확인됐다 (a_engine_native_learning).
abstain-side 체인(H_1304/1361/1367/1379)에 더해, fire-side in-dist 잔여물도 이제 engine-native
로 메워졌다 — the THIN residual is lifted on the live engine.

**BINDING FOLLOW-ON (NOT this lane, tracked)**: `brain_decide` 가 gap 을 H_1379 margin 옆
refined in-dist confidence 로 소비 (H_1367→H_1379 패턴). Ψ 위험 회피를 위해 honest 하게 defer
— gap op 은 exposed + engine-native 재확인 완료, brain-consume 은 명명된 다음 follow-on
(margin 의 H_1379 가 이미 brain_decide_margin 으로 소비하는 것과 동형).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic twin-pair facts, byte-level shift = in-dist/OOD proxy, deterministic
engine-native LCG corruption, 3 seeds, KEYLEN=80, RECALL_THR=0.15 (frozen). 1-byte twin =
in-dist 모호성의 toy proxy — real-corpus semantic near-duplicate 변별로의 전이 UNVERIFIED.
미검증: scale / real-corpus paraphrase / semantic(non-byte) confusion / brain_decide 의 실제
gap 소비(= tracked follow-on). NO bar moved post-hoc (c9); KEYLEN/twin-position 변경은 엔진의
더 엄격한 L2 metric 이 요구한 단 1회 frozen-first well-posedness 재시도(WALL-CLAUSE), 모든
verdict 막대 사전등록 그대로. brain-consume 전까지는 a_verified_must_wire 의 op-노출 단계가
done, brain 배선은 명시 추적 follow-on.

## Refs / xref

`.verdicts/1398_g5_gap_engine/{FREEZE.txt,result.txt,probe_stdout.txt}` ·
`CORE/h1398_g5_gap_engine_probe.hexa` (engine-native re-score) ·
`CORE/engine_cli.hexa § ImmuneMemory` (immune_memory_recall_gap + vadapt_field_two_recon_err) ·
`CORE/engine_cli_smoke.hexa` cases 98b/98c/98d.
xref H_1396 (mirror DIRECTIONAL parent, this is its binding follow-on) · H_1304 (fire-side
binary fail-safe, in-dist wrong-fire 부재 = THIN 의 구조적 이유, OOD fab 보존) · H_1361 (abstain
margin graded OOD) · H_1367 (margin engine-wire, this lane's twin op) · H_1379 (margin
brain-consume, the gap brain-consume follow-on pattern) · H_1202 (type-2 M-ratio 0.924) ·
H_1227/H_1231 (immune store geometry) · a_break_the_wall · a_no_llm_frame_trap ·
a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode ·
a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c2 · c9 · c15.
