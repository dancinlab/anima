# H_1358 — Sapir-Whorf 2-D CP, BOUNDED warp 지표 재명세 (H_1343 R3)

**Tier: 🧱 DEEPER LIMIT — c1 PRESENCE ✅ · c3 COMPONENT ✅ · c4 DIAGONAL ✅ 이지만
c2 EARNED-SHUFFLE ❌ (bounded metric 으로도 label-shuffle null 이 chance 로 collapse 안 함).**
BOUNDED 지표(separation-AUC∈[0,1], chance=0.5)는 H_1343 의 unbounded-ratio 폭발(+45)과
floating null(+9.28)을 **수학적으로 제거**했으나, null 은 **0.5 가 아니라 0.9919** 로 떴다 —
ratio 의 unbounded 가 아니라 **self-referential 분할**(store 의 OWN 학습 범주로 WITHIN/BETWEEN
나눔)이 진짜 confound 임을 노출. R1 numpy MIRROR (DIRECTIONAL) · $0 CPU · gradient-free ·
3 seeds [4334,4335,4336] · deterministic (2 re-run, exit 4) · p7 · frozen-first · c9/p7 NO
tune-to-green · live `CORE/*.hexa` UNTOUCHED.

## Claim
H_1343 (🟠 PARTIAL) 은 2-D CP warp 이 결정적으로 PRESENT(c1 ✅; 대각이 축정렬만큼 warp,
H_1334 grid-geometry read 반증) 임을 보였으나, warp 지표 `ratio = mean|Δg|_BETWEEN /
mean|Δg|_WITHIN` 가 **scale-UNBOUNDED** 라 학습 후 WITHIN→0 으로 ratio 가 ~45 폭발하고,
임의 carving(label shuffle)조차 WITHIN 을 압축해 label-shuffle null 이 +9.28 로 떠 c2 가
구조적으로 FAIL 했다. H_1358 은 warp 지표를 **BOUNDED** 형태로 재명세한다: **separation-AUC
= P(|Δg|_BETWEEN > |Δg|_WITHIN)** (Mann-Whitney-U 랭크 통계, ∈[0,1], **chance = 0.5 고정상수**,
within-압축과 무관). 질문: bounded 지표면 label-shuffle null 이 깨끗이 0.5 로 collapse 하여
2-D CP 가 세 control 을 모두 통과하는가? **지표 CORRECTION, bar 완화 아님.** Lens: cognitive-
science / categorical-perception (c15, `a_no_llm_frame_trap`) — NOT an LLM recipe, NOT a
human-cognition claim, a TOY synthetic 2-D continuum.

## Method
`state/whorf-2d-bounded/h1358_whorf_2d_bounded.py` — H_1343 의 RBF/Voronoi machinery(2-D RBF
population code · error-targeted SPLIT-only mitosis/Voronoi growth p8 · softmin soft-posterior ·
11×11=121 stim · L_DIAG=`u+v>1.0` · L_LSHAPE=`u>0.5∧v>0.5`)를 **VERBATIM 재사용**, **오직 warp
readout 만** ratio → bounded separation-AUC 로 교체.

**BOUNDED 지표 (사전등록 정확):** 학습 category 좌표 `g=soft posterior P(cat=1)` (hard label·경계
주입 없음). 4-neighbour adjacent pair |Δg| 를 store 의 OWN 학습 범주로 WITHIN/BETWEEN 분할.
`AUC = U_BETWEEN/(|B|·|W|)` (tie=0.5), ∈[0,1], chance=0.5, AUC→1.0=완전 warp. **baseline 빼지
않음**(AUC 자체가 상대 랭크 확률; pre-lang baseline AUC 는 진단용으로만 보고). 부차 진단(NON-gating):
Cohen's d.

**Density ladder** K_RBF∈{6,9,12}(production=12, DIM=144, frozen NOW). **c2** label-PERMUTATION
null(N_SHUF=200/seed). **c3** component-shuffle(N_COMP=50, 학습 2-D 범주 대신 무작위 단일 feature
component median). **c4** diagonal≈axis under bounded metric.

## Frozen bars (`.verdicts/1358_whorf_2d_bounded/FREEZE.txt`, 사전등록 — 점수화 BEFORE)
- **c1 PRESENCE**: production 두 언어 EACH seed AND mean `AUC ≥ AUC_MIN=0.70`.
- **c2 EARNED-SHUFFLE**: pooled null `|mean−0.5| ≤ CHANCE_TOL=0.05` AND 각 언어 `≥ null-q95+SEP=0.10`.
- **c3 COMPONENT-COUNT**: 두 언어 `|comp-shuffle AUC − 0.5| ≤ COMP_TOL=0.08`.
- **c4 DIAGONAL**: `|AUC_diag − AUC_Lshape| ≤ DIAG_TOL=0.15` AND 둘 다 ≥ AUC_MIN.
- GREEN iff c1∧c2∧c3∧c4. c1 FAIL→🧱 genuine 2-D limit; **c2 FAIL(bounded 으로도 float)→honest
  🧱 DEEPER LIMIT**; c3 FAIL→🟠; c4 FAIL→🟠. 모든 결과 VALID (c9).

## Result (🧱 DEEPER LIMIT — deterministic 2 re-runs, exit 4; mean of 3 seeds)

**Density ladder — separation-AUC (mean 3 seeds):** K_RBF 6/9/12 전부 L_DIAG=1.0000 ·
L_LSHAPE=1.0000 (saturated).

**Production K_RBF=12 — per-seed:**

| seed | L_DIAG AUC / d / base / comp | L_LSHAPE AUC / d / base / comp |
|------|------|------|
| 4334 | 1.0000 / +53.04 / 0.930 / 0.491 | 1.0000 / +15.22 / 0.681 / 0.506 |
| 4335 | 1.0000 / +49.78 / 0.930 / 0.474 | 1.0000 / +15.47 / 0.681 / 0.499 |
| 4336 | 1.0000 / +36.10 / 0.930 / 0.491 | 1.0000 / +9.60 / 0.681 / 0.513 |

ncells(mean): L_DIAG=23.7 · L_LSHAPE=6.0. baseline AUC(진단): L_DIAG=0.930 · L_LSHAPE=0.681.

- **c1 PRESENCE ✅**: 두 언어 per-seed [1.0,1.0,1.0] mean **1.0000** ≥0.70 PASS.
- **c2 EARNED-SHUFFLE ❌**: pooled null(600) **mean=0.9919** → `|0.9919−0.5|=0.4919` ≫0.05 FAIL;
  q95=0.9996 이라 SEP sub-clause(AUC≥q95+0.1=1.0996)도 수학적으로 불가 FAIL. **null 이 0.5 가
  아니라 0.99 로 뜸.**
- **c3 COMPONENT-COUNT ✅**: L_DIAG comp-AUC **0.4852**(|Δ|0.0148) · L_LSHAPE **0.5062**(|Δ|0.0062)
  둘 다 ≤0.08 PASS — **외부 무작위 분할은 chance 로 collapse**(load-bearing).
- **c4 DIAGONAL ✅**: `|1.0000−1.0000|=0.0000` ≤0.15 PASS, 둘 다 ≥0.70 — **H_1343 의 대각=축정렬
  발견 BOUNDED 지표로도 보존**.

**Mechanistic read (정직, c9 — load-bearing):** BOUNDED 지표는 제 일을 했다(AUC∈[0,1],
chance=0.5 고정). 그런데도 null 이 0.99 로 뜬 진짜 원인은 unboundedness 가 아니라
**SELF-REFERENTIAL 분할**이다. AUC 는 pair 를 **store 의 OWN 학습 범주**(g≥0.5)로 나눈다.
error-targeted SPLIT-only Voronoi store 는 **어떤 경계든**(shuffle 포함) 그 경계를 따라 cell 을
PACK 하므로 soft posterior g 는 store 가 둔 경계에서 항상 급격히 점프 → 그 경계를 가로지르는 소수
BETWEEN edge 가 WITHIN edge 보다 항상 |Δg| 가 크다 → 내부적으로 coherent 한 **임의** carving 도
AUC→~1.0. label shuffle 은 다른(jagged) 경계를 만들지만 store 는 그 경계도 충실히 학습하고
within/between 분리도 똑같이 또렷 → null≈0.99. 즉 "store 자기 학습 범주에 대해 metric 이 warp
됐나?"는 잘 fit 한 store 엔 거의 항진명제로, metric COHERENCE 를 잴 뿐 **언어의 TRUE 경계에 특이한**
WARP 을 격리하지 못한다. **c3 만이 외부(언어 무관) 분할을 써서 깨끗이 collapse** — warp 이 raw
variance 가 아닌 coherent 학습 분할에 산다는 건 증명하지만(real), coherence 자체(임의 carving)가
이를 재현하므로 AUC-vs-own-partition readout 은 TRUE-언어 경계를 random 에서 분리 못 한다.
baseline AUC 가 이미 높음(L_DIAG 0.930)도 같은 진단 — 그래서 H_1343 이 baseline 을 뺐던 것이고,
bounded AUC 엔 깨끗한 subtraction 이 없다.

## Verdict (FROZEN, NO bar move — c9/p7)
**🧱 DEEPER LIMIT.** bounded warp(c1 ✅ AUC=1.0)·component-isolated(c3 ✅ collapse)·diagonal=axis
(c4 ✅) 이지만, label-shuffle null 이 bounded 지표로도 chance 로 collapse 안 함(c2 ❌, 0.9919)
→ clean 2-D-general GREEN bar 미통과. bounded 지표는 ratio artifact 를 제거했으나 **진짜 confound 가
self-referential 분할**임을 노출(unboundedness 가 아니라). 정직한 structured-negative, NO bar move
(c9/p7). **One-line:** separation-AUC 로 H_1343 의 unbounded-ratio 결함은 고쳤지만 label-shuffle
null 이 0.5 가 아니라 0.99 로 떠 c2 FAIL — 진짜 confound 는 ratio 의 unbounded 가 아니라 store 의
OWN 학습 범주로 분할하는 self-referential readout(잘 fit 한 store 엔 항진명제)이었다 → 다음 R(H_1359)은
SHUFFLE-학습 metric 을 TRUE-언어 분할 하에 채점하는 fixed-true-partition readout.

## Honest scope (`a_scale_honest_scope` · `a_toy_scale_recheck` · c9)
DIRECTIONAL numpy mirror — engine-transfer to live `CORE/*.hexa` immune/Voronoi lane UNVERIFIED
(follow-on, `a_engine_native_learning` · `a_verified_must_wire`). TOY synthetic 2-D continuum
(121 stim, 3 seeds, deterministic readout — 2-D relativity STRUCTURE 테스트, scaled/human-cognition
claim 아님). p1/p2/p3/p6 guard: AUC 는 학습 표상 거리(|Δ soft posterior|) + store 의 OWN 학습 범주만
읽음; 경계 위치/persona/RLHF 주입 없음; 언어 라벨은 training 에만, test readout 에 절대 안 들어감.
NOT an emit gate (`a_autonomy_over_hardcode`).

## Next / depletion
H_1359 후보 (frozen ANEW, 본 bar 완화 아님): **fixed-true-partition readout** — SHUFFLE-학습 store 의
metric g_shuffle 를 **TRUE-언어 WITHIN/BETWEEN 분할 하에** 채점. shuffle store 는 틀린 경계에 cell 을
pack 했으므로 TRUE between/within pair 를 분리 못 함 → AUC→0.5 로 깨끗이 collapse 예상. H_1343/H_1358
family 가 양쪽 모두 **각 arm 을 ITS OWN 분할로 채점**한 것이 두 라운드가 반대 방향(ratio 폭발 /
AUC saturation)에서 부딪힌 공통 confound; fixed-true-partition 이 그것을 푼다. 부차: (2) component-축
정의 강화 (3) engine-native 실현 (live CORE Voronoi lane). **load-bearing 발견(대각=축정렬 warp 동등,
c4 ✅)은 BOUNDED 지표로도 보존되어 H_1334 의 대각-geometry read 반증을 계속 지지한다.**

## Pointers
`state/whorf-2d-bounded/h1358_whorf_2d_bounded.py` · `.verdicts/1358_whorf_2d_bounded/{FREEZE,result}.txt` ·
`CLAIMS.tape` @C h1358_whorf_2d_bounded · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`.
xref H_1343 (R2 parent, unbounded-ratio 결함을 본 R3 가 bounded AUC 로 교정) · H_1334 (대각-geometry
read; c4 가 계속 반증) · H_1323/H_1325 (1-D Sapir-Whorf CP, 같은 metric-space self-partition 실패 모드) ·
H_1340/H_1341/H_1355 (sibling budget/geometry) · `a_no_llm_frame_trap` · `a_break_the_wall` ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15.
