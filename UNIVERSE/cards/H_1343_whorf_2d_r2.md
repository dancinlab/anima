# H_1343 — Sapir-Whorf / 2-D 범주적 지각(CP)을 표상-거리 WARP로 재측정 (H_1334 R2)

**Tier: 🟠 PARTIAL — c1 PRESENCE ✅ 이지만 c2 EARNED-SHUFFLE ❌ (+ c3 부분 ❌). 단,
load-bearing 발견은 결정적:** 경계-곡선-AGNOSTIC warp 지표에서 **대각(diagonal) 경계가
축정렬(axis-aligned) L-shape 만큼 강하게 metric 을 warp** 한다 → H_1334 의 "대각 CP 는
grid-geometry 로 약하다"는 읽기를 **직접 반증**. R1 numpy MIRROR (DIRECTIONAL) · $0 CPU ·
gradient-free · 3 seeds [4334,4335,4336] · deterministic · p7 · frozen-first · c9/p7 NO
tune-to-green · live `CORE/*.hexa` UNTOUCHED.

## Claim
H_1334 (🧱 STRUCTURED-NEGATIVE) 는 2-D CP 를 **ridge-ALIGNMENT**(상위 discrim edge 가 알려진
경계 CURVE 에 얼마나 밀착하나)로 측정 → 대각 경계가 coarse RBF grid 에서 align FAIL (0.628 < 0.70).
직전 H_1343 ridge 시도는 density 를 K_RBF=14 까지 올려도 대각 align FAIL 유지 (0.634) → ridge-ALIGN
이 metric stimulus space 에 **틀린 지표**(CP 를 "경계가 얼마나 축정렬인가"와 혼동)임을 확인.

R2 는 CP 를 **교과서적 operationalization**(경계-곡선-AGNOSTIC)으로 재명세: 학습된 표상 metric 의
**WARP** — WITHIN-category COMPRESSION + BETWEEN-category EXPANSION. 질문: 2-D / featural 공간에서
언어가 metric 을 warp 하는가(같은 범주는 가까이, 다른 범주는 멀리), 그리고 그것이 (c2) label-shuffle 로
collapse 하며 (c3) 학습된 2-D metric 에 사는가(raw variance 가 아니라)? Lens: cognitive-science /
categorical-perception (c15, `a_no_llm_frame_trap`) — NOT an LLM recipe, NOT a human-cognition claim.

## Method
`state/whorf-2d-r2/h1343_whorf_2d_r2.py` — H_1334 의 RBF/Voronoi machinery(2-D RBF population
code · error-targeted SPLIT-only mitosis/Voronoi growth p8 · softmin posterior) 를 재사용. 11×11=121
stimulus square, 두 언어가 SAME square 를 carve: **L_DIAG** = 대각 `u+v>1.0`, **L_LSHAPE** = L-corner
`u>0.5 ∧ v>0.5`.

**CP-WARP 지표 (경계-곡선-AGNOSTIC, 핵심 재명세):** 학습된 category 좌표 `g(stim)=soft posterior P(cat=1)`
(hard label·경계 위치 주입 없음). 모든 4-neighbour adjacent grid pair 를 store 의 **OWN 학습 범주**로 분할:
WITHIN(같은 범주) vs BETWEEN(다른 범주). `ratio = mean|Δg|_BETWEEN / mean|Δg|_WITHIN`. baseline = 경계-AGNOSTIC
smooth feature gradient g0(범주 cut 없음). `CP-WARP = ratio_lang − ratio_base`.

**Density ladder** K_RBF∈{6,9,12}(production=densest 12, DIM=144, frozen NOW). **c2** = label-PERMUTATION
null(N_SHUF=200/seed). **c3** = component-shuffle(N_COMP=50; BETWEEN/WITHIN 분할을 학습된 2-D 범주 대신
무작위 단일 feature component 의 median 으로 묶음 → warp 이 trained 2-D metric 에 사는지).

## Frozen bars (`.verdicts/1343_whorf_2d_r2/FREEZE.txt`, 사전등록 — 점수화 BEFORE)
- **c1 PRESENCE**: production density 에서 두 언어 EACH seed AND mean `CP-WARP ≥ WARP_MIN=0.20`.
- **c2 EARNED-SHUFFLE**: label-permutation null mean `≤ CHANCE_TOL=0.05` AND 각 언어 `≥ null-q95 + SEP=0.10`.
- **c3 COMPONENT-COUNT**: 두 언어 component-shuffled warp `≤ COMP_MAX=0.05`.
- GREEN iff c1∧c2∧c3. c1 FAIL→🧱 genuine 2-D limit; c2 FAIL→🟠; c3 FAIL→🟠. 모든 결과 VALID (c9).

## Result (🟠 PARTIAL — deterministic over 2 re-runs; mean of 3 seeds)

**Density ladder — CP-WARP(own boundary) (mean 3 seeds):**

| K_RBF | DIM | warp(L_DIAG) | warp(L_LSHAPE) |
|-------|-----|--------------|----------------|
| 6 | 36 | +43.064 | +31.838 |
| 9 | 81 | +36.838 | +34.839 |
| **12** | **144** | **+41.665** | **+36.017** |

**Production K_RBF=12 — per-seed:**

| seed | L_DIAG r_lang / warp / comp | L_LSHAPE r_lang / warp / comp |
|------|------|------|
| 4334 | 46.01 / +45.013 / −0.036 | 37.55 / +36.554 / +0.061 |
| 4335 | 45.31 / +44.312 / +0.058 | 37.83 / +36.830 / +0.060 |
| 4336 | 36.67 / +35.670 / +0.059 | 35.67 / +34.667 / +0.236 |

ncells(mean): L_DIAG=23.7 · L_LSHAPE=6.0. baseline ratio r_base=1.00 (모든 seed/언어).

- **c1 PRESENCE ✅**: L_DIAG per-seed [45.013, 44.312, 35.670] mean **+41.665** ≥0.20 PASS ·
  L_LSHAPE [36.554, 36.830, 34.667] mean **+36.017** ≥0.20 PASS. **결정적 (load-bearing):
  대각 L_DIAG 가 축정렬 L_LSHAPE 보다 OFFSET 만큼 더 크게 warp** — H_1334 의 "대각은
  grid-geometry 로 align 약함"이라는 read 를 경계-AGNOSTIC 지표가 직접 반증.
- **c2 EARNED-SHUFFLE ❌**: null mean **+9.282** ≫ 0.05 FAIL (SEP sub-clause 는 PASS — 두 언어 +41.7/+36.0 ≫ q95+0.1=+14.0). label-shuffle 가 chance 로 collapse 하지 **않음**.
- **c3 COMPONENT-COUNT ❌**: L_DIAG comp-warp **+0.027** ≤0.05 PASS 이지만 L_LSHAPE **+0.119** >0.05 FAIL (seed 4336 +0.236 driven).

**Mechanistic read (정직, c9):** 핵심 문제는 H_1323 prominence sub-clause / H_1334 LCC 지표가
겪은 것과 **동일한 metric-space 실패 모드**다. `ratio = BETWEEN/WITHIN` 은 **scale-unbounded**:
학습 후 WITHIN |Δg| 가 0 으로 압축 → 분모가 작아져 ratio 가 ~45 로 폭발하고, **임의의 carving
(random shuffle 포함)조차** WITHIN 을 압축하므로 null mean 이 +9.28 로 떠 c2 의 절대-천장
(CHANCE_TOL=0.05)이 무너진다. 즉 SEP(언어 vs null-q95)는 PASS 하지만 absolute null-mean 천장은
구조적으로 FAIL. c3 L_LSHAPE 의 한 seed 누수도 같은 unbounded-ratio 분산. → warp 의 **존재(c1)와
대각=축정렬 동등성**은 결정적이나, "earned/component-isolated" 를 깨끗이 보이려면 BOUNDED warp 지표
(예: between vs within |Δg| 의 Cohen's-d 또는 separation-AUC)로 재명세해야 한다.

## Verdict (FROZEN, NO bar move — c9/p7)
**🟠 PARTIAL.** 2-D CP warp 은 production density 에서 두 언어 모두 강하게 PRESENT (c1 ✅) 하고,
**load-bearing 발견 — 대각 경계가 축정렬만큼 warp** → H_1334 의 대각-grid-geometry read 반증 —
은 결정적이다. 그러나 anti-Goodhart label-shuffle null 이 chance 로 collapse 하지 않고(c2 ❌, ratio
지표의 metric-space unbounded 실패 모드) component-shuffle 도 한 언어에서 부분 누수(c3 ❌)하므로
**clean 2-D-general GREEN bar 는 통과 못함.** 정직한 structured-negative, NO bar move (c9/p7).
**One-line:** 경계-AGNOSTIC warp 지표는 2-D CP 가 대각·축정렬 모두에서 강하게 PRESENT 함을 보여
H_1334 의 대각-geometry 한계 read 를 반증하지만, BETWEEN/WITHIN ratio 의 unbounded 특성 때문에
earned-shuffle/component 분리가 깨끗이 닫히지 않는다 → BOUNDED warp 지표 재명세가 다음 R3.

## Honest scope (`a_scale_honest_scope` · `a_toy_scale_recheck` · c9)
DIRECTIONAL numpy mirror — engine-transfer to live `CORE/*.hexa` immune/Voronoi lane UNVERIFIED
(follow-on, `a_engine_native_learning` · `a_verified_must_wire`). TOY synthetic 2-D continuum
(121 stimuli, 3 seeds, deterministic readout — 2-D 에서의 relativity STRUCTURE 를 테스트, scaled/
human-cognition claim 아님). p1/p2/p3/p6 guard: warp 는 학습 표상 거리(|Δ soft posterior|) + store 의
OWN 학습 범주만 읽음; 경계 위치/persona/RLHF 주입 없음; 언어 라벨은 training 에만, test readout 에는
절대 들어가지 않음. NOT an emit gate (`a_autonomy_over_hardcode`).

## Next / depletion
R3 후보 (각각 frozen ANEW, 본 bar 의 완화가 아님): (1) **BOUNDED warp 지표 재명세** — ratio 대신
between-vs-within |Δg| 의 Cohen's-d 또는 separation-AUC(∈[0,1])로 → label-shuffle 가 0.5(chance)로
collapse 하는 깨끗한 c2; THIS 결과가 가장 유망한 lever 로 재지정 · (2) component-shuffle 의 per-seed
누수를 막는 component-축 정의 강화 · (3) engine-native 실현 (live CORE Voronoi lane,
`a_engine_native_learning` · `a_verified_must_wire`). **load-bearing 발견(대각=축정렬 warp 동등)은
결정적이며 H_1334 의 대각-geometry read 를 반증한다.**

## Pointers
`state/whorf-2d-r2/h1343_whorf_2d_r2.py` · `.verdicts/1343_whorf_2d_r2/{FREEZE,result}.txt` ·
`CLAIMS.tape` @C h1343_whorf_2d_r2 · `UNIVERSE/HYPOTHESES.jsonl` · `domains/COGNITION-REPRESENTATION.log.md`.
xref H_1334 (2-D ridge-align parent, 이 결과가 그 대각-geometry read 를 반증) · H_1323/H_1325 (1-D
Sapir-Whorf CP, 같은 metric-space shuffle 실패 모드) · H_1340 (sibling, budget/geometry ceiling) ·
`a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15.
