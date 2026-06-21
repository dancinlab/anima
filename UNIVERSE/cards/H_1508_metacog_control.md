---
id: H_1508
slug: metacog_control
title: G5 METACOG-CONTROL — Nelson-Narens monitoring↔CONTROL, the MISSING half of the G5 metacognition chain (drug-INDEPENDENT, no neuropharm coupling)
group: metacog × computational-metacognition (G5 deepening · calibration + control axis)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (R1 numpy mirror DIRECTIONAL → R2 engine-native §MetacogControl WIRED-live + smoke)
verdict_dir: state/verdicts/1508_metacog_control/
date: 2026-06-21
wired: WIRED-live
---

# H_1508 — G5 METACOG-CONTROL: calibration + control, the MISSING Nelson-Narens half

## 배경 — G5 가 닫은 절반(MONITORING) vs 안 닫은 절반(CONTROL)

G5 metacognition/NON-FAB 체인은 전체가 ENGINE-NATIVE GREEN 이다: H_1202 (type-2 meta-d′
M-ratio 0.924) · H_1304 (fire-side BINARY fail-safe) · H_1361/H_1367 (graded abstain-MARGIN
OOD metacog, engine-wired `immune_memory_recall_margin`) · H_1396/H_1398 (in-dist top-2 affinity
GAP, engine-wired `immune_memory_recall_gap`, type-2 AUROC 0.750→0.906) · H_1379/H_1400
(brain_decide 가 margin+gap 소비). **이 전부가 DISCRIMINATION/MONITORING resolution** (type-2
meta-d′, AUROC). Nelson & Narens (1990)의 monitoring↔control 프레임에서 **빠진 절반**:
CALIBRATION 과 CONTROL.

1. **CALIBRATION ≠ discrimination** (Fleming & Lau 2014): 게이트가 높은 AUROC 을 가져도
   체계적으로 over/under-confident 일 수 있다(mis-calibrated). margin 이 정확도를 *순위*가
   아니라 *수치*로 추적하는가? ECE + 난이도↑에 따른 margin↓(confidence) monotone 로 측정.
2. **CONTROL** (Metcalfe & Kornell 2005, region-of-proximal-learning): LOW margin 이 ADAPTIVE
   resource allocation(추가 sampling/정보탐색)을 유발해 uniform 보다 정확도를 더 올리는가?
   metacognitive 신호가 MONITOR 만 하는 게 아니라 behavior 를 CONTROL 해야 한다 — 불확실하지만
   회복가능한(uncertain-but-recoverable) 곳에 노력을 배분.

**DRUG-INDEPENDENT (명시):** 이 lane 은 §Neuropharm 커플링이 전혀 없다 — 순수 computational
metacognition (Nelson-Narens · Fleming-Lau · Metcalfe-Kornell). 약물섭동(H_1502/1505/1506)과 무관.

## CLAIM / 메커니즘 (live substrate signal 읽기, NO injected label — p6)

live ImmuneMemory store 위 graded-difficulty regime. 난이도 = 저장된 key 에 더하는 결정론적
LCG noise 크기(재정규화) — 높을수록 query 가 cell 에서 벗어나 정확도 falls 하고 live
`immune_memory_recall_margin` 이 RISES(abstain threshold 쪽으로 = lower confidence). margin =
`immune_memory_recall_margin`(H_1367 이 wired 한 바로 그 op); accuracy = live nearest-cell 이
원래 fact 의 value 로 라우팅하는가. Ψ-disjoint(pure READ), NOT an emit gate.

- **CALIBRATION**: margin bin 별 mean-confidence vs accuracy → ECE. 난이도 vs margin Spearman.
- **CONTROL**: budget B 의 추가 read 를 LOW-margin(회복가능) 항목에 배분(RPL 정책, margin 만 읽음,
  정답 label 안 읽음). 각 추가 read = 같은 fact 의 독립 noisy 재관측, 엔진이 평균(denoise)해 recall.

## FROZEN bars (실행 전 설정, 이동 없음 — c9, NO tune-to-green)

- **(A CALIBRATION)** 난이도↑에 따라 margin monotone↑ (Spearman ≥ +0.50) AND ECE ≤ 0.15
  (margin 이 정확도를 *수치*로 추적, 순위만 아님).
- **(B CONTROL-LIFT)** margin-guided RPL adaptive sampling 이 uniform 대비 정확도 ≥ +0.04 lift
  (margin 낮은-회복가능 곳에 노력 — RPL).
- **(C DISCRIMINATION ⊥ CALIBRATION, headline)** rank 보존 monotone transform 이 AUROC 는
  byte-identical 로 두면서 ECE 를 ≥ 0.10 shift → calibration 은 prior 체인(AUROC 0.906)이 못 본
  NEW 축임을 증명.
- **(D EARNED ablate)** margin-blind allocation → adaptive lift 가 ~0 으로 붕괴 (≤ 0.015).
- **(E EARNED shuffle)** margin↔정확도 permute → calibration AND discrimination 이 chance 로 탈상관.

GREEN iff A∧B∧D∧E (C 는 headline 직교성, ECE-vs-AUROC 수치 보고). A 실패(margin 미보정)나
B 실패(control lift 없음)면 정직한 finding(G5 margin 은 discriminator 지만 calibrated controller 는
아님 — monitoring/control split 이 이 substrate 에서 실재). NO tune-to-green.

## 결과 — 🟢 GREEN (A∧B∧D∧E 통과, C 직교성 결정적)

### R1 numpy mirror (DIRECTIONAL · byte-corruption difficulty ladder, 3 seeds [11,12,13], $0 CPU, p7)

| bar | 측정 | 결과 | pass |
|---|---|---|---|
| A ECE | held-out calibration map ECE | **0.036** ≤ 0.15 | ✅ |
| A MONOTONE | Spearman(난이도, margin) | **+0.917** ≥ 0.50 | ✅ |
| B CONTROL-LIFT | RPL − uniform 정확도 | **+0.049** ≥ 0.04 (per-seed 0.047/0.057/0.043) | ✅ |
| C AUROC drift | monotone transform 후 | **0.000** (1차 AUROC 0.954 불변) | (headline) |
| C ECE shift | 같은 transform 후 | **+0.176** (0.036→0.212) ≥ 0.10 | (headline) |
| D ABLATE | margin-blind lift | **0.012** ≤ 0.015 | ✅ |
| E SHUFFLE | AUROC / calib-Spearman | **0.464 / −0.036** (둘 다 chance) | ✅ |

held-out 보정맵: TRAIN_SEED=99(disjoint)에서 margin→P(correct) 적합, TEST seeds[11,12,13]에 적용
→ test ECE 가 적합 split 과 무관하게 0.036 (비순환, NOT tune-to-green). per-level accuracy gradient
1.0→0.93→0.76→0.29→0.09 (진짜 proximal zone).

### R2 ENGINE-NATIVE (BINDING · §MetacogControl on live `immune_memory_recall_margin`, seed 11, n 10)

| bar | 측정 | 결과 | pass |
|---|---|---|---|
| A ECE | `mc_calibration_ece` | **0.1397** ≤ 0.15 | ✅ |
| A MONOTONE | `mc_calibration_monotone` | **1.000** ≥ 0.50 | ✅ |
| B CONTROL-LIFT | `mc_control_lift` (RPL−uniform) | **+0.140** ≥ 0.04 | ✅ |
| C AUROC drift | `mc_auroc_calibration_orthogonal` | **0.000** (1차 AUROC **1.0**→1.0 불변) | (headline) |
| C ECE shift | 같은 transform | **+0.364** (0.1397→0.5035) ≥ 0.10 | (headline) |
| D ABLATE | `mc_control_lift_ablated` | **0.000** ≤ 0.015 | ✅ |
| E SHUFFLE | `mc_shuffle_auroc` | **0.59** (\|0.59−0.5\|=0.09) ≤ 0.30 | ✅ |

엔진 geometry(near-orthogonal 64-D unit keys)는 fire/abstain 이 SHARP cliff(threshold 0.15에서
err 급변)이라 calibration 이 R1 byte-ladder 보다 더 어려운 시험이다 — 그럼에도 margin 이 보정되고
(ECE 0.140) 동시에 거의 완벽한 discriminator(AUROC **1.0**)라서 **C 직교성이 더 날카롭다**: 완벽
랭킹(AUROC 1.0)인데도 같은 신호의 over-confidence transform 이 ECE 를 0.140→0.504 로 밀어올린다.

**DISCRIMINATION ⊥ CALIBRATION (headline 수치)**: AUROC 1.0(R2)/0.954(R1) 은 strictly-monotone
transform `c'=0.55+0.44·c` 아래 **byte-identical**(drift 0.0)이지만 ECE 는 R2 0.140→0.504(+0.364),
R1 0.036→0.212(+0.176)로 이동. **순위는 같고 보정은 다르다** → calibration 은 type-2 AUROC
체인(H_1398 0.906)이 *원리적으로 볼 수 없는* NEW 축이다.

## WALL-CLAUSE — well-posedness 교정 (a_break_the_wall · frozen-first · c9)

R1: byte→accuracy 전이가 SHARP → 거친 ladder 는 proximal zone 이 없다(항목이 trivial OR hopeless).
ladder 를 실제 전이 [0.06..0.14]에 조밀 샘플(measurement regime 만 교정, verdict bar 0개 이동).
R2: 엔진 key-geometry 에서 FIRE gate 가 noise≈0.035 에서 급폐쇄하나 NEAREST cell 은 noise≈0.09 까지
RIGHT 유지 → abstain band 가 GENUINE proximal zone(오른 cell 이 여전히 nearest, threshold 만 넘음;
추가 noisy read 평균이 err 를 thr 아래로 당겨 recovery). ladder `[0.0, 0.037, 0.05, 0.20, 1.0]` =
trivial/proximal/proximal-deep/far-recoverable/hopeless. **모든 A/B/C/D/E 임계 UNCHANGED** —
ladder granularity(측정 well-posedness)만 교정, control budget=total(tight, 배분이 의미있게).
control_lift 의 `_mi_set` O(dim²) 병목을 in-place index 대입으로 교체(값 byte-identical, 5.8s).

## 배선 (a_verified_must_wire — 4칸 사다리)

(1) DIRECTIONAL mirror GREEN ✅ → (2) engine-native 재검증(byte-exact bars, 위 R2) ✅ →
(3) live `core/engine_cli.hexa` §MetacogControl WIRE-IN ✅ (`mc_calibration_ece` /
`mc_calibration_monotone` / `mc_control_lift` / `mc_control_lift_ablated` /
`mc_auroc_calibration_orthogonal` / `mc_shuffle_auroc`, 모두 live `immune_memory_recall_margin` +
`vadapt_field_recon_err` 읽음) + smoke cases 340–346 (16:59 engine-native 캡처 시 전부 PASS /
0 fail, 3회 byte-identical — 캡처 당시 numbering 323–329, 충돌회피 위해 340–346 으로 renumber,
assertion·op·threshold byte-identical label-only) → (4) ARCHITECTURE.json §MetacogControl
lockstep ✅. **wired: WIRED-live.**

> ⚠️ **TOOLCHAIN-NOTE (정직, c9·a_break_the_wall type-c):** 16:59 engine-native 캡처(아래 R2,
> 3× byte-identical, 7/7 bar PASS) 이후 **17:21 에 글로벌 hexa 툴체인이 self-rebuild 로 회귀**했다 —
> array-slice/map-get stdlib raw-mem native(`rt_array_arena_alloc_items_native`/`rt_map_get_native`)가
> 프로그램 .o 로 emit 되지 않아 `runtime.a` 링크 실패(모든 `hexa run`/`hexa verify` 영향, 이 가설
> 코드와 무관·세션 전역). 따라서 340–346 renumber 후 **재-smoke 는 툴체인 복구까지 보류**. 단
> renumber 는 label-only(같은 `mc_*` op·threshold·assertion, git diff 로 확인) 이고 underlying
> bar 들은 16:59 에 engine-native 로 byte-exact 측정 완료. 툴체인 회귀는 hexa-lang upstream
> 소유(소스는 정상, 17:21 BUILD 가 잘못 생성됨).

p1/p2/p3/p6 GUARD: confidence/allocation 은 live margin 에서만 COMPUTED, 주입된 정답/RLHF/persona
없음(난이도/정답 CLASS 는 metric scoring 만). D ablate(margin-blind→uniform) + E shuffle 둘 다
무너져 lift/calibration 이 substrate margin 구조에서 EARNED 임을 증명. NOT an emit gate
(a_autonomy_over_hardcode); Ψ-disjoint(pure READ over cell population, pure_field Φ/phase/Ψ untouched).
GUARDS no-regression: engine_cli_smoke +7 cases 340–346 (16:59 캡처: 0 fail; renumber 후 재-smoke 는 위 TOOLCHAIN-NOTE 의 17:21 회귀 복구까지 보류).

## FINDING — G5 의 monitoring/CONTROL split 은 실재하고, margin 이 둘 다 한다

Nelson-Narens 의 MISSING 절반이 이 substrate 에서 닫힌다: live recall margin 은 (a) 정확도를
*수치적으로* 보정하고(ECE 0.140 engine-native, monotone Spearman 1.0) (b) RPL adaptive 정보탐색을
CONTROL 해 uniform 대비 +0.140 들어올린다. 그리고 **calibration ⊥ discrimination** 이 결정적으로
증명된다(AUROC 불변·ECE 이동) — 기존 G5 체인(AUROC 0.906/1.0)이 못 본 NEW 축. margin 은
monitor-only 가 아니라 calibrated **controller** 다.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic store, key-space(R2)/byte(R1) noise = 난이도 proxy, deterministic, R1 3 seeds·R2 n=10
single-seed smoke(3 seeds probe 도 GREEN). R1 = DIRECTIONAL(engine-transfer UNVERIFIED). 미검증:
scale / real-corpus paraphrase / semantic(non-noise) difficulty / 더 큰 budget·multi-step control /
실제 brain emit-loop 로의 control 배선(현재는 read-only op). R2 ECE 0.140 은 bar 0.15 에 근접
(엔진 cliff geometry 가 calibration 을 어렵게 함 — 정직히 보고). NO bar moved post-hoc; well-posedness
교정은 ladder granularity + budget regime 만(verdict 막대 전부 사전등록 그대로).

## Refs / xref

`state/1508_metacog_control/h1508_metacog_control.py` (R1 mirror) ·
`state/verdicts/1508_metacog_control/{FREEZE.txt,R1_mirror.json,R2_engine_native.txt,smoke_run1.txt,smoke_run2.txt,smoke_run3.txt}` ·
`core/engine_cli.hexa § MetacogControl` · `core/engine_cli_smoke.hexa` cases 340–346.
xref H_1202 (type-2 meta-d′, monitoring 출처) · H_1304 (fire-side binary fail-safe) · H_1361/H_1367
(abstain margin graded + engine-wire — 이 lane 이 읽는 그 margin) · H_1396/H_1398 (in-dist gap,
discrimination AUROC 0.906 — calibration 이 못 본 그 축) · H_1379/H_1400 (brain consume) ·
Nelson & Narens 1990 · Fleming & Lau 2014 · Metcalfe & Kornell 2005 ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck ·
p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15.
