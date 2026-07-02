---
id: H_1361
slug: g5-graded-metacog
title: G5 graded metacognition on the abstain margin — does -margin rank recoverable vs unrecoverable abstains, surviving OOD? (the open question H_1304 left)
group: metacog × neuroscience (G5 NON-FAB dig)
terminal_tier: 🟢 GRADED-METACOG (R1 numpy mirror DIRECTIONAL)
verdict_dir: .verdicts/1361_g5_graded_metacog/
terminal_verdict: .verdicts/1361_g5_graded_metacog/result.txt
date: 2026-06-16
---

# H_1361 — G5 의 metacognition 은 binary 인가? abstain MARGIN 의 graded 신호

## 배경 — H_1304 가 남긴 열린 질문

H_1304 는 G5 copy-or-abstain 게이트의 **FIRE 쪽**을 닫았다: 게이트는 구조적으로
FAIL-SAFE 이고 wrong-fire 클래스가 **비어있다**(fab=0.000 모든 shift level) → fire 의
correct-vs-WRONG 에 대한 type-2 AUROC 는 **정의 불가**. 즉 fire 쪽은 BINARY
(exact-fire 아니면 abstain). 🟢 fail-safe-robust 이지만 BINARY.

그러나 그 closure 는 **다른**, well-posed 질문을 미검증으로 남긴다: **ABSTAIN 쪽**에서는
recall MARGIN(= `recon_err − recall_thr`, 모든 abstain 에 존재하는 연속량)이 GRADED
meta-confidence 를 담는가? -margin 이
- **RECOVERABLE** abstain (store 안에 있는 키의 손상 버전 — 답이 검색 가능) 을
- **UNRECOVERABLE** abstain (진짜 없는 fact — 검색할 게 없음) 보다

위로 **RANK** 하는가? 그리고 그 ranking 이 **OOD(byte-corruption shift)에서 살아남는가**?
- R1 pass(L≥0.20 에서 type-2 AUROC ≥ 0.65) → graded OOD metacog **존재**(G5 upgrade).
- R1 fail(AUROC ~0.5) → metacog 는 **BINARY-only**(H_1204 확인, c9 valid closure).

## 메커니즘 (CORE/engine_cli.hexa byte-exact mirror, H_1304 verbatim 재사용)

byte-trigram(n=3) FNV-1a → dim=64 → L2-normalize (immune_embed_key VERBATIM). store =
N_FACTS=80 cell. `recon_err(q) = 1 − cos(q, nearest cell)`. recall: err ≤ recall_thr(0.15,
frozen) → FIRE 아니면 ABSTAIN. **MARGIN = recon_err − recall_thr** (모든 abstain 에서 >0,
작을수록 "real cell 에 가까움" = 검색가능 graded 신뢰). type-2 신호 = **−margin**.

**ABSTAIN SPLIT**: shift level L 마다 두 disjoint abstain 집단 — (a) in-store 키를 L 만큼
손상(label=1), (b) 진짜 없는 토큰을 같은 L 만큼 손상(label=0). abstain(err>thr) 인 것만
센다. type-2 AUROC = AUROC(−margin, label). **SHIFT LADDER** L∈{0,0.10,0.20,0.30,0.40}
(H_1304 재사용). L=0 에선 recoverable 이 대부분 FIRE 하므로 abstain-ranking 질문 자체가
genuinely OOD — support 는 L≥0.10 부터.

## FROZEN bars 와 결과 — 🟢 GRADED-METACOG

3 seeds [7,8,9], pooled, deterministic (재실행 byte-identical), $0 CPU, p7.

| bar | 의미 | 결과 | pass |
|---|---|---|---|
| R1 GRADED-SENS | type-2 AUROC(L=0.20) ≥ 0.65 | **0.915** | ✅ |
| R2 EARNED-SHUF | shuffle-margin → AUROC(0.20) ≤ 0.58 collapse | **0.494** | ✅ |
| R3 vs H_1204 | graded readout EXISTS vs FLAT | **EXISTS** | graded |

**LADDER** (pooled):

| L | t2_AUROC | t2_AUROC_shuf | rec_abstain | unr_abstain | mean_rec_marg | mean_unr_marg |
|---|---|---|---|---|---|---|
| 0.00 | nan | nan | 0.000 | 1.000 | nan | 0.366 |
| 0.10 | **0.999** | 0.511 | 0.856 | 1.000 | 0.082 | 0.362 |
| 0.20 | **0.915** | 0.494 | 0.995 | 1.000 | 0.232 | 0.364 |
| 0.30 | 0.708 | 0.498 | 1.000 | 1.000 | 0.316 | 0.364 |
| 0.40 | 0.557 | 0.495 | 1.000 | 1.000 | 0.353 | 0.364 |

(L=0.00 의 t2_AUROC=nan: L=0 에선 recoverable 이 전부 FIRE → recoverable abstain 이 없음;
graded-abstain 질문은 본질적으로 OOD 질문, support L≥0.10 부터.)

**메커니즘 (왜 rank 되나)**: recoverable abstain 은 shift 와 함께 매끄럽게 커지는 **작은**
margin(평균 0.082→0.232→0.316→0.353)을 유지하고, unrecoverable(absent) 키는 shift 와
무관하게 **안정적으로 큰** margin(~0.364, random-token 노이즈 바닥)에 머문다. 따라서 margin 은
GRADED recoverability 신호: "손상됐지만 real cell 근처" vs "그냥 모든 것에서 멀다". −margin 이
둘을 rank 하고, shuffle 통제(pooled abstain 에서 margin 셔플)는 모든 level 에서 AUROC 를
chance(~0.49–0.51)로 무너뜨린다 → base-rate 아티팩트가 아니라 RANKING 이 신호를 운반(earned).

**DECAY (정직, c9)**: t2_AUROC 가 0.999→0.915→0.708→0.557 로 사다리에서 감소; L=0.40
(극심 손상)에서 chance 도달 — recoverable 키가 genuinely-absent 만큼 손상되면 둘은 구분
불가가 된다. graded 신호는 실재하고 real shift 를 **결정적으로 통과**(L≥0.20 bar)하지만
무한하지 않다; 손상된 키가 store 이웃을 완전히 벗어나면 graceful 하게 chance 로 수렴한다.

## FINDING — G5 metacognition 은 순수 binary 가 아니다

H_1304 가 **FIRE 쪽** binary fail-safe 를 세웠다면, H_1361 은 **ABSTAIN 쪽** 보완적
GRADED type-2 readout 을 세운다 — margin 이 recoverable-vs-unrecoverable abstain 을 rank 하고
OOD 를 통과. 이는 engine-wiring 가치가 있는 **G5 upgrade**(a_verified_must_wire): live 게이트는
이미 매 recall 마다 recon_err 를 **계산**하므로, fire/abstain boolean 뿐 아니라 margin 을
노출하면 graded confidence-of-recoverability 신호가 공짜로 얻어진다.

## R3 vs H_1204 — flat refutation 아님

H_1204 는 output/fire confidence 의 2nd-order readout 에서 separable 신호 없음을 발견. H_1361 은
**ABSTAIN MARGIN**(다른 표면)에서 graded readout 을 발견. 충돌 아님 — H_1204 는 fire-side 2nd-order
readout 을, H_1361 은 abstain-side margin 을 측정. H_1304(binary fire) + H_1361(graded abstain) =
G5 의 더 완전한 그림: fire-side binary fail-safe + abstain-side graded recoverability metacognition.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic facts, byte-level shift = OOD proxy, deterministic, 3 seeds, KEYLEN=20,
RECALL_THR=0.15(frozen). R1 numpy mirror = **DIRECTIONAL**(engine-transfer UNVERIFIED).
미검증: scale / real-corpus paraphrase / semantic(non-byte) shift / engine-native margin
exposure / brain-side graded-신호 사용. NO bar moved post-hoc (c9, NO tune-to-green). Live
CORE/*.hexa UNTOUCHED (mirror only).

**follow-on (a_verified_must_wire)**: R2 engine-native — live `CORE/engine_cli.hexa`
`immune_memory_recall` 의 margin(recon_err − recall_thr)을 byte-exact 로 노출해 frozen bar
재검증 + regression guard. green 이면 abstain-margin 을 brain 의 graded-confidence 입력으로 배선.

## Refs / xref

`.verdicts/1361_g5_graded_metacog/{FREEZE.txt,result.txt,result.json}` ·
`state/g5-graded-metacog/h1361_g5_graded_metacog.py` · `CLAIMS.tape` @C h1361_g5_graded_metacog.
xref H_1304 (fire-side binary fail-safe, 직접 후속) · H_1202 (decoder type-2 M-ratio 0.924) ·
H_1204 (flat fire-side metacog) · H_1217 (decoder OOD-collapse, closed-neg) · H_1227/H_1231
(immune store geometry) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning ·
a_verified_must_wire · a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p6 · p7 · p8 · c9 · c15.
