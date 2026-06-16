---
id: H_1396
slug: g5_indist_metacog
title: G5 IN-DISTRIBUTION metacognition — CEILING vs FIXABLE? does a richer read-only confidence signal lift the "🟠 THIN in-dist" type-2 over the live best-margin? (the in-dist residual the abstain-side chain H_1304/1361/1367/1379 left open)
group: metacog × neuroscience (G5 NON-FAB dig · in-dist residual)
terminal_tier: 🟢 FIXABLE (R1 numpy mirror DIRECTIONAL — top-2 affinity gap lifts in-dist type-2 +0.205, abstain intact)
verdict_dir: .verdicts/1396_g5_indist_metacog/
terminal_verdict: .verdicts/1396_g5_indist_metacog/result.txt
date: 2026-06-17
---

# H_1396 — G5 in-distribution metacognition: is "🟠 THIN in-dist" an inherent CEILING or FIXABLE?

## 배경 — G5 의 마지막 잔여물 "🟠 THIN in-dist"

G5 NON-FAB/metacognition 은 체인 전체가 ENGINE-NATIVE GREEN 이다: H_1202 (type-2 meta-d′
M-ratio 0.924 ≈ near-optimal) · H_1304 (abstain fire-side BINARY fail-safe, OOD wrong-fire
class 구조적으로 비어있음) · H_1361 (abstain MARGIN 의 graded OOD metacog) · H_1367 (margin
engine-wired `immune_memory_recall_margin`) · H_1379 (brain_decide 가 graded margin 소비).
scoreboard tier = "🟢 frozen / 🟠 THIN in-dist": metacog 신호는 OOD/명백히-비접지(abstain)에서
STRONG 이지만, IN-DISTRIBUTION(전부 접지·정답처럼 보이는) 항목들 사이의 confidence 변별에서는
THIN. 이 잔여물이 **FIRE-side, in-distribution slice**다: 게이트가 FIRE 하는 항목들 중에서
RIGHT 와 WRONG 을 confidence 가 변별하는가?

이 lane 의 정직한 가설: in-dist thinness 는 (A) NEAR-INHERENT CEILING (모든 fire 가 거의
exact-correct 면 추적할 correctness 변동 자체가 거의 없다 — H_1304 의 구조적 발견의 재진술,
meta-d′ 가 이미 near-optimal) 일 수도, (B) FIXABLE (더 풍부한 confidence 신호가 들어올림)
일 수도 있다. frozen-first, NO tune-to-green (c9, p7) 로 둘을 가른다.

## CLAIM / 메커니즘 (read-only, NO new training, NO injected label — p6)

CORE/engine_cli.hexa `immune_embed_key` (byte-trigram FNV-1a, DIM=64, L2-norm, VERBATIM
H_1361/H_1304) + ImmuneMemory affinity geometry 의 faithful numpy mirror. recall: err =
1−cos(q, nearest cell) ≤ RECALL_THR(0.15, frozen) → FIRE 아니면 ABSTAIN. **mirror =
DIRECTIONAL** (engine-transfer UNVERIFIED) — 더 풍부한 신호는 FULL top-k affinity 분포를
읽는데, live 엔진은 현재 single-best(`recon_err`/`nearest_idx`)만 노출하므로 FIXABLE 🟢 의
binding follow-on = 엔진에 top-k 노출 op 추가 (a_verified_must_wire).

**IN-DIST SLICE (well-posedness, WALL-CLAUSE 참조)**: in-dist 에서 WRONG fire 가 실재하도록
store 를 TWIN-PAIR 로 구성 — 두 fact 가 **단 1 byte** 한 위치에서만 다르고(거의 동일 키, 거의
모든 trigram 공유) **다른 답**에 bound. light corruption(L∈{0,0.05,0.10})이 한 twin 의 fire 를
다른 twin 셀로 high-confidence 로 라우팅 → confidently-WRONG in-dist fire. type-2 =
AUROC(confidence, correctness) over FIRED items only.

**비교 confidence 신호** (전부 같은 cell store 에서 read-only): (a) CURRENT = best-cell recall
margin (= `immune_memory_recall_margin` 노출값, live baseline) · (b) RICHER-1 = top-2 cos
affinity GAP (decisiveness) · (c) RICHER-2 = top-k softmax 의 neg-entropy (2nd-order spread) ·
(d) ORACLE = determinate-correctness ceiling 참조.

## FROZEN bars 와 결과 — 🟢 FIXABLE

3 seeds [7,8,9], pooled raw fired-item lists, deterministic (재실행 byte-identical), $0 CPU, p7.
사전등록 Δ=0.10, MIN_SUPPORT=30 pooled wrong fires (well-posedness guard).

in-dist fire accuracy **0.981** (n_fire=2359 pooled, **n_wrong=44** ≥ 30; 3 seed 모두 기여 18/12/14).

| 신호 | in-dist type-2 AUROC | lift vs CURRENT |
|---|---|---|
| (a) CURRENT best-margin | **0.736** | — (live baseline) |
| (b) RICHER-1 top-2 gap | **0.940** | **+0.205** |
| (c) RICHER-2 neg-entropy | 0.594 | −0.142 (도움 안 됨) |
| (d) ORACLE ceiling | 1.000 | (상한 참조) |

| bar | 의미 | 결과 | pass |
|---|---|---|---|
| C1 CEILING-REF | oracle−current gap | **0.264** | (diagnostic) |
| C2 FIXABLE | best richer lift ≥ Δ=0.10 | gap **+0.205** | ✅ |
| C3 ABSTAIN-INTACT | OOD fab ≤ 0.02 (H_1304 보존) | fab_max **0.000** | ✅ |
| C4 SHUFFLE-CTRL | conf↔correctness 셔플 → ~0.50 | curr 0.489 / gap 0.524 / negent 0.485 | ✅ |

**메커니즘 (왜 gap 이 들어올리나)**: 1 byte 차이의 twin 셀은 best-affinity 가 거의 동일(≈1)
→ best-margin 은 어느 twin 인지 변별 불가(AUROC 0.736). 그러나 **top-2 gap** 은 #1 과 #2 가
거의 동률(작은 gap = "ambiguous/비결정적")임을 보고 → WRONG fire 를 예측(AUROC 0.940). neg-entropy 는
top-k 전체 spread 라 이 1-byte twin 모호성을 희석해 도움 안 됨(−0.142) — 정직하게, 모든 richer
신호가 듣는 게 아니라 **decisiveness 신호(top-2 gap)** 가 특정해서 듣는다. shuffle 이 세 신호
모두 ~0.50 으로 무너뜨려 lift 가 base-rate 아티팩트 아님을 증명(earned).

## WALL-CLAUSE — well-posedness 교정 (a_break_the_wall · frozen-first · c9)

R1 첫 실행은 in-dist slice 가 DEGENERATE 임을 드러냄: 약한 collision store 에서 in-dist fire
accuracy=0.998 → seed 당 WRONG fire 0–2개(seed8=0 → AUROC 정의불가), C4 shuffle 이 이를 **정확히
포착**(2-point positive class 는 안정적 ~0.50 셔플 불가) → RED(measurement artifact). 이건 그
자체로 구조적 발견(H_1304 재진술: in-dist wrong fire 거의 부재 = type-2 가 THIN 한 바로 그 이유)
이지만 measurement 가 well-posed 하지 않다. a_break_the_wall 의 단 1회 frozen-first 재시도는
**SLICE well-posedness 만** 교정 — twin-pair store 를 1-byte 차이로 강화해 non-trivial 비율의
fire 가 wrong-but-confident neighbor 로 라우팅되게. **Δ=0.10, C4 셔플 허용오차 |x−0.50|≤0.08,
C3 fab≤0.02 모두 UNCHANGED (verdict bar 0개 이동)**, 사전등록 MIN_SUPPORT=30 (< 30 이면
INCONCLUSIVE, green/ceiling 아님). tune-to-green 아님(p7) — verdict 막대가 아니라 측정 설계의
well-posedness 만 고침, control 이 요구한 교정.

## FINDING — in-dist thinness 는 FIXABLE (CEILING 아님)

G5 의 in-dist metacognition 잔여물은 **inherent ceiling 이 아니라 FIXABLE 신호 결핍**이다:
top-2 affinity GAP(decisiveness)이라는 read-only 신호가 live best-margin 대비 in-dist type-2
metacog 를 **+0.205** 들어올리면서 H_1304 OOD fail-safe(fab=0.000)를 보존한다. abstain-side
체인(H_1304/1361/1367/1379)이 OOD/비접지 graded metacog 를 닫았듯, 이 lane 은 fire-side
in-dist 잔여물의 deepening 을 **이름붙인다**: top-2 affinity gap.

**"G5 resolved or needs deepening?"** → **deepening (named): top-2 affinity gap**. abstain-side 는
이미 graded+wired+consumed 로 resolved; fire-side in-dist 는 best-margin 으로는 THIN 이지만
top-2 gap 으로 메울 수 있다 (이 lane 은 그것을 검증·명명; 배선은 binding follow-on).

**BINDING FOLLOW-ON (a_verified_must_wire, NOT this lane)**: live `CORE/engine_cli.hexa
§ ImmuneMemory` 에 top-k affinity 노출 op(예: `immune_memory_recall_gap`/top-k accessor)를
추가하고, 그 gap 을 `immune_memory_recall_margin` 옆에 / `brain_decide` 의 graded-confidence
입력으로 배선(H_1379 패턴) — engine-native 재확인 + regression guard 까지가 done. 이 lane 은
mirror DIRECTIONAL 측정 + deepening 명명까지만 (CORE UNTOUCHED).

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic twin-pair facts, byte-level shift = in-dist/OOD proxy, deterministic, 3 seeds,
KEYLEN=20, N_FACTS=80, RECALL_THR=0.15(frozen). R1 numpy mirror = **DIRECTIONAL**
(engine-transfer UNVERIFIED — top-k 노출이 live 엔진에 없음 → binding follow-on). 미검증:
scale / real-corpus paraphrase / semantic(non-byte) confusion / 더 풍부한 신호의 engine-native
재확인 / brain-side 소비. 1-byte twin 은 in-dist 모호성의 toy proxy — real-corpus 의 semantic
near-duplicate 변별로의 전이 UNVERIFIED. NO bar moved post-hoc (c9); well-posedness 교정은
frozen-first 단일 재시도(WALL-CLAUSE), 모든 verdict 막대 사전등록 그대로. Live CORE/*.hexa
UNTOUCHED (mirror measurement only).

## Refs / xref

`.verdicts/1396_g5_indist_metacog/{FREEZE.txt,result.txt,result.json}` ·
`state/g5-indist-ceiling/h1396_g5_indist_metacog.py`.
xref H_1202 (decoder type-2 M-ratio 0.924, in-dist 잔여물의 출처) · H_1304 (fire-side binary
fail-safe, in-dist wrong-fire 부재 = THIN 의 구조적 이유) · H_1361 (abstain margin graded OOD,
직접 자매 abstain-side) · H_1367 (margin engine-wire) · H_1379 (margin brain-consume) ·
H_1204 (flat fire-side 2nd-order readout — gap 은 best-margin 이 아닌 top-2 표면에서 신호 발견,
충돌 아님) · H_1217 (decoder OOD-collapse) · H_1227/H_1231 (immune store geometry) ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck ·
p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15.
