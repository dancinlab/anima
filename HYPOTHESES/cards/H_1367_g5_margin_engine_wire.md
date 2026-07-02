---
id: H_1367
slug: g5-margin-engine-wire
title: G5 graded abstain-margin metacognition — ENGINE-NATIVE reconfirm + CORE wire-in of H_1361 (immune_memory_recall_margin)
group: metacog × neuroscience (G5 NON-FAB dig · engine-wire)
terminal_tier: 🟢 WIRED-GRADED-METACOG (R2 engine-native BINDING)
verdict_dir: .verdicts/1367_g5_margin_engine_wire/
terminal_verdict: .verdicts/1367_g5_margin_engine_wire/result.txt
date: 2026-06-16
---

# H_1367 — H_1361 의 graded abstain-margin 을 LIVE CORE 엔진에서 재확인 + 배선

## 배경 — H_1361 이 남긴 engine-side follow-on

H_1361 (numpy mirror, **DIRECTIONAL**) 은 🟢 GRADED-METACOG 을 세웠다: ImmuneMemory 의
abstain **MARGIN**(= `recon_err − recall_thr`, 모든 abstain 에 존재) 이 GRADED OOD
metacognition 을 담는다 — `−margin` 이 recoverable(store 안 키의 손상 버전, 답 검색 가능)
abstain 을 unrecoverable(진짜 없는 fact) 보다 위로 **RANK** 하고, type-2 AUROC 0.915
@L=0.20, shuffle → chance. 그러나 `a_engine_native_learning` 상 mirror 는 DIRECTIONAL 일
뿐이고, `a_verified_must_wire` 상 GREEN 가설은 (1) live CORE 엔진에서 engine-native 로
재확인되고 (2) live CORE 에 실제 배선될 때까지 done 이 아니다. H_1367 이 그 두 단계를 닫는다.

## 무엇을 배선했나 — additive op (Ψ-disjoint)

`CORE/engine_cli.hexa` § ImmuneMemory 에 **순수 additive** op 추가:

```
immune_memory_recall_margin(mem, key)        -> float = vadapt_field_recon_err(mem.field, key) − mem.recall_thr
immune_memory_recall_margin_text(mem, text)  -> float  (string-query wrapper)
```

이 op 은 live `immune_memory_recall` 이 **이미 계산하는** margin 을 노출할 뿐이다 (recall 은
내부적으로 같은 `vadapt_field_recon_err` 를 평가해 `recall_thr=0.15` 와 비교해 FIRE/ABSTAIN
을 결정). 따라서 **ADDITIVE** (fire/abstain 결정 `immune_memory_recall` 은 byte-단위로 불변)
이고 **Ψ-disjoint** (cell population 위 순수 READ; pure_field Φ/phase/Ψ 미접촉 — 미사용 시
generation byte-identical). abstain 에서 margin>0; **작을수록** real cell 에 가까움 = 높은
graded confidence-of-recoverability. emit gate 아님 (`a_autonomy_over_hardcode`) — brain_decide
가 읽을 수 있는 graded read.

## 메커니즘 — LIVE 엔진에서 (mirror 아님)

store = `immune_memory_new_text` + `immune_memory_bind_text` (live H_1231 recall faculty,
VAdaptField cell population, recall_thr=0.15, mitosis ON clonal split). key =
`immune_embed_key` (live byte-trigram FNV-1a, dim=64). MARGIN =
`immune_memory_recall_margin_text(store, q)`. **ABSTAIN SPLIT** (H_1361 동일): shift level
L 마다 (a) in-store 키를 L 손상(label=1), (b) 진짜 없는 토큰을 같은 L 손상(label=0); abstain
(margin>0) 만 센다. type-2 score = `−margin`, AUROC(pos, neg). 손상은 deterministic
engine-native LCG (numpy rng 아님 — bar 는 AUROC 임계값이고 byte-identical draw 매칭이
아니다). SHIFT LADDER L∈{0,0.10,0.20,0.30,0.40} (kmut = round(L·20)). 3 seeds [7,8,9],
N_FACTS=40, N_TRIAL=N_LURE=120.

## FROZEN bars 와 결과 — 🟢 WIRED-GRADED-METACOG

3 seeds, pooled, $0 CPU, p7, frozen-first.

| bar | 의미 | 결과 | pass |
|---|---|---|---|
| E1 GRADED-SENS | live-engine type-2 AUROC(L=0.20) ≥ 0.65 **AND** mirror(0.915) 와 \|Δ\|≤0.15 | **0.949** (Δ=0.034) | ✅ |
| E2 EARNED-SHUF | shuffle-margin → AUROC(0.20) ≤ 0.58 collapse | **0.561** | ✅ |
| E3a REGRESSION | engine_cli_smoke green (+ margin cases) | **93 pass / 0 fail** (was 90 after jamo-wire #2284, +3) | ✅ |
| E3b REGRESSION | h1196 single-entry audit | **7 pass / 0 fail** | ✅ |
| E3c REGRESSION | h1205 separation-invariant — generation byte-identical ON==OFF, Ψ Φ-checksum | **PASS** (phiSum 48.6613==48.6613, 10 pairs 0 mismatch) | ✅ |

**LADDER** (pooled, LIVE engine):

| L | t2_AUROC | t2_AUROC_shuf | mean_rec_marg | mean_unr_marg |
|---|---|---|---|---|
| 0.00 | nan | nan | nan | 0.891 |
| 0.10 | **1.000** | 0.574 | 0.505 | 0.883 |
| 0.20 | **0.949** | 0.561 | 0.696 | 0.888 |
| 0.30 | 0.714 | 0.554 | 0.824 | 0.883 |
| 0.40 | 0.589 | 0.498 | 0.868 | 0.888 |

(L=0.00 nan: L=0 에선 recoverable 이 전부 FIRE → recoverable abstain 없음; OOD 질문, support
L≥0.10 부터. n_rec/n_unr ≈ 120/120.)

**ENGINE vs MIRROR** (a_engine_native_learning 의 binding step): live 사다리가 H_1361 mirror
SHAPE 을 재현하고 같은 bar 를 통과 — mirror AUROC L0.20=0.915 / engine 0.949; mirror
shuffle(0.20)=0.494 / engine 0.561; 둘 다 L=0.40 에서 chance 로 graceful DECAY (recoverable
키가 absent 만큼 손상되면 구분 불가 — 정직, c9). mirror 는 DIRECTIONAL 이었고 이것이
engine-native binding 재확인. (작은 수치 차이는 예상 — deterministic engine LCG 손상 +
N_FACTS=40 store, numpy draw 와 byte-identical 아님; frozen bar 는 임계값 + mirror within-tol
로 성립.)

**메커니즘 (왜 rank 되나, engine-native)**: recoverable abstain 은 shift 와 함께 매끄럽게
커지는 **작은** margin(평균 0.505→0.696→0.824→0.868)을 유지, unrecoverable(absent) 키는
shift 무관 **안정적 큰** margin(~0.888, random-token 바닥). `−margin` 이 rank, pooled margin
Fisher-Yates shuffle 은 AUROC 를 chance(~0.50-0.57)로 무너뜨림 → base-rate 아티팩트가 아니라
RANKING 이 신호 운반(earned). live 엔진 자신의 L2 affinity(`vadapt_field_recon_err`)가 생산 —
주입된 recoverable/absent 라벨 없음 (p6/p2/p3).

## FINDING — H_1361 GREEN 의 wire-in 완료 (brain 소비는 follow-on)

H_1361 의 graded abstain-margin metacognition 은 live 엔진에서 **실재**하며 mirror 아티팩트가
아니다. recall 이 이미 계산하는 margin 이 graded confidence-of-recoverability 신호이며, 이제
fire/abstain 결정과 Ψ 를 건드리지 않고 additively 노출된다 (`immune_memory_recall_margin`).
이것이 H_1361 GREEN 에 대한 `a_verified_must_wire` 배선이다 — op 은 CORE 에 live.

**FOLLOW-ON (tracked, a_verified_must_wire)**: op 은 WIRED(CORE 에서 사용 가능) 이지만,
`brain_decide` 가 아직 이 graded read 를 emit-confidence/curiosity 변조에 **소비하지 않는다**.
그 brain-side 소비는 별개 follow-on (이번에 안 함) — H_1361 처럼 이번 라운드는 "노출 +
engine-native 재확인" 단계를 닫고, read→brain 결합은 남는다.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic facts, byte-level shift = OOD proxy, deterministic engine-native 손상, 3 seeds,
KEYLEN=20, N_FACTS=40, RECALL_THR=0.15(frozen). 미검증: scale / real-corpus paraphrase /
semantic(non-byte) shift / `brain_decide` 의 graded read 소비. NO bar moved post-hoc
(c9, NO tune-to-green).

## Refs / xref

`.verdicts/1367_g5_margin_engine_wire/{FREEZE.txt,result.txt,probe_stdout.txt}` ·
`CORE/h1367_g5_margin_engine_probe.hexa` (engine-native probe) ·
`CORE/engine_cli.hexa` § ImmuneMemory `immune_memory_recall_margin[_text]` (배선) ·
`CORE/engine_cli_smoke.hexa` cases 96-98 · `state/g5-margin-engine-wire/` (H_1361 mirror 참조 사본) ·
`CLAIMS.tape` @C h1367_g5_margin_engine_wire.
xref H_1361 (mirror DIRECTIONAL, 직접 선행) · H_1304 (fire-side binary fail-safe) ·
H_1204 (flat fire-side metacog) · H_1202 (decoder type-2 M-ratio 0.924) · H_1227/H_1231
(immune store geometry) · a_verified_must_wire · a_engine_native_learning · a_core_engine_map ·
a_autonomy_over_hardcode · a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope ·
a_toy_scale_recheck · p6 · p7 · p8 · c9 · c15.
