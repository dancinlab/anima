---
id: H_1460
slug: 1460_semantic_detector
title: G6 FALS-depth — SEMANTIC-AWARE detector 재채점 (measurement-artifact 가설)
group: G6 IDEATION FALS-depth wall — breakthrough lens ① (measurement-first, a_break_the_wall type-a)
terminal_tier: 🧱 CAPACITY-REINFORCED (DIRECTIONAL) — semantic(SAME-idea) detector 는 structural 보다
  엄격(calibration V2 2<4)하나 REAL generation 에서 cross-shuffle COLLAPSE 가 structural 과 동일(둘 다 0) →
  measurement-artifact 가설 반증, 벽은 capacity. H_1435/1436/1437/1439/1449 에 이은 수렴(7B 근거 a7b_pass).
date: 2026-06-20
provenance: G6 돌파 다각도 렌즈 ① — 5렌즈(H_1435 data/1436 objective/1437 form/1439 bind-head/1449 attention)
  전부 🧱 WALL(cross-shuffle 불붕괴). H_1435 honest finding "structural H_1305 detector CANNOT distinguish
  earned idea-specific binding from any-comparator+any-measurable+content" → 측정 artifact 일 가능성을 먼저 배제.
  NB: 팀리드 지정 id H_1450 은 다른 에이전트(workmem_hold_bind)가 선점 → 충돌 회피로 H_1460 재anchor.
---

# H_1460 — SEMANTIC-AWARE falsifiability detector 재채점 (측정결함 먼저 배제)

## Claim / falsifier
**가설(type-a 측정결함):** G6 5렌즈가 전부 🧱 인 이유가 *모델이 실제로 binding 하는데 H_1305 structural detector
가 못 봤기 때문*일 수 있다(measurement artifact). H_1305 `_is_falsifiable` 는 **structural** —
`(∃ comparator-word) AND (∃ measurable-word) AND (negatable content)`. comparator 와 measurable 이
**서로 다른 idea** 를 가리켜도(아무데나 흩뿌려져 있어도) 통과 → cross-shuffle 로 measurable 을 다른 idea 로
바꿔도 둘 다 여전히 ∃ → **structural FALS 가 안 무너지는 게 당연**(H_1435 가 박은 바로 그 결함).

**Semantic-aware detector(신규, FROZEN):** comparator-slot 과 measurable-slot 이 **SAME idea** 를
가리키는지를 추가 요구 — `semantic-FALS := structural-FALS AND SAME-idea-binding`.
SAME-idea-binding(순수 lexical, $0, no torch/embeddings) = 어떤 (comparator i, measurable j) 쌍이
(1) `|i-j| ≤ WINDOW`(한 절 안 공기) AND (2) 둘 사이에 clause-breaking connector 없음(다른 leg 로 용접 아님)
AND (3) 그 국소 절에 공유 subject content 토큰 ≥1(둘이 같은 주제를 술어). cross-shuffle 로 measurable 을 다른
idea 의 measurable 로 splice 하면 SAME-idea bridge 가 깨져 **semantic FALS 는 COLLAPSE 가능**.

**Falsifier(FROZEN, 채점 전 고정):** base + 학습된 G6 렌즈 ckpt 를 동일 generation 으로 두 detector 로
재채점 → cross-shuffle COLLAPSE = `FALS[composed] − FALS[shuffle]` 를 detector 별로.
- 🟢 **MEASUREMENT-BREAK** iff `collapse_sem ≥ collapse_struct + 1` AND `collapse_sem > 0`
  (semantic 이 structural 이 못 본 COLLAPSE 를 드러냄 → 벽은 측정 artifact, 모델은 idea-specific binding 함).
- 🧱 **CAPACITY-REINFORCED** otherwise (두 detector 모두 earned idea-specific binding 을 못 봄 → 측정결함
  아님, capacity 천장 유효).

## Semantic detector 정의 (frozen)
`state/1460_semantic_detector/semantic_detector.py` — `WINDOW=6 · MIN_SUBJECT=1` ·
clause-break set `{and,but,or,also,while,whereas-는 comparator 라 제외,...}`. H_1305 의
COMPARATOR/MEASURABLE/STANCE 집합 + structural `_is_falsifiable` 를 VERBATIM 재사용(p7, 재구현 아님 —
소스에서 정규식 파싱하여 torch import 회피).

## FROZEN discriminator-validity bar (채점 전 검증)
10개 designed 문자열(5 BOUND = comparator+measurable 가 한 절에서 한 주제 술어 · 5 SPRINKLE = 실험의
cross-shuffle splice 를 그대로 미러 = donor measurable 을 다른 idea 끝에 붙임):
- **V1 retain:** `bound_sem ≥ 4/5`(진짜 bound claim 유지)
- **V2 strict:** `sprinkle_sem < sprinkle_struct`(sprinkle 에서 structural 보다 엄격)
순수-lexical 천장(임베딩 없음)상 `sprinkle_sem==0` 은 요구하지 않음 — spliced measurable 이 우연히 trailing
comparator+subject 옆에 떨어지면 lexical 로는 못 잡음(정직한 천장, tune-away 아님 c9). 핵심은 **방향**:
semantic 이 structural 이 유지하는 cross-sprinkle FALS 를 제거.

## Result (verbatim — state/verdicts/1460_semantic_detector/)
**DETECTOR FREEZE(calibration):** BOUND struct 5/5 sem 5/5 · SPRINKLE struct 4/5 sem 2/5 →
V1 5≥4 ✅ · V2 2<4 ✅ → **DISCRIMINATOR VALID**. structural 은 cross-sprinkle 에 더 무딤(4/5 fire),
semantic 은 더 엄격(2/5 fire) — H_1435 의 "structural 은 binding 을 못 가린다" 를 구조적으로 재현.

**RE-SCORE (pool aiden RTX 5070, torch-mouth DIRECTIONAL, 3 seeds [7,4302,4303]):**
| ckpt | arm | FALS_struct | FALS_sem | collapse_struct | collapse_sem |
|---|---|---|---|---|---|
| BASE | composed/shuffle | 0.667 / 0.0 | 0.667 / 0.0 | **0.667** | **0.667** → 🧱 |
| H1441_CONTRASTIVE | flat/comp/shuf/ablate ALL | **5.0 매arm** | **5.0 매arm** | **0.0** | **0.0** → 🧱 |
| H1441_SHUFFLE_CTRL | composed/shuffle | 0.333 / 0.0 | 0.333 / 0.0 | 0.0 | 0.0 → 🧱 |

**(1) semantic 이 structural 이 못 본 COLLAPSE 를 드러냈나? NO.** 모든 ckpt 에서 collapse_sem == collapse_struct
(base 0.667==0.667 · 두 trained 0.0==0.0). semantic 은 calibration 에선 cross-sprinkle 를 더 잡지만
REAL generation 에선 structural 과 정확히 일치 → 모델의 falsifiable emission 은 *국소적으로는* 묶여 있으나
(comparator+measurable 한 절+공유주제) **idea-specific 이 아님**: 같은 국소 binding 이 cross-shuffle arm 에도 나옴.

**(2) 측정돌파 vs capacity강화 → CAPACITY-REINFORCED.** 결정적: H1441_CONTRASTIVE 가 **4개 arm 전부** FALS_sem=5.0
(A_flat=composed 구조 없는 맨 ideation seed 까지, B_shuffle 까지). contrastive 렌즈는 falsifiable FORM 을 *무조건적으로*
학습 — 어떤 두 idea 를 결합하느냐와 무관. cross-sprinkle splice 를 잡는 binding-aware detector 조차 cross-shuffle arm 을
못 무너뜨림 → 벽은 detector blind-spot 아님. 모델이 idea-specific binding 을 안 함. capacity 천장 유효.

**(3)** H_1435 honest finding("structural 은 earned binding 을 못 가린다")은 **detector 속성으로는 CONFIRMED**
(semantic 이 더 엄격, calibration V1/V2 PASS) 이나 **벽의 원인으로는 FALSIFIED** — 더 엄격한 detector 가 동일한
zero idea-specific collapse 를 찾음 → 벽은 애초에 측정 artifact 가 아니라 진짜 capacity.

## wired
DIRECTIONAL-mirror (torch-mouth decode via gauge_lib._decode on pool aiden GPU — a_engine_native_learning;
engine-native 재측정 = .hexa CORE/bytegpt_decode 채점 follow-on 등록). detector 자체는 score-side 순수 CPU.

## Scope / honest (c9)
TOY: 4 arms × 3 seeds × 5 frames, 303M ByteGPT G6 ckpt, lexical(no-embedding) binding score.
semantic detector 는 lexical 천장 — 학습된 임베딩 정합/NLI entailment 은 미구현(no model). scale/
real-corpus/embedding-grade binding/engine-native(.hexa) 재측정 UNVERIFIED. cross-refs
H_1305(structural detector)·H_1435(honest finding precedent)·H_1436/1437/1439/1449(5렌즈 벽).

## Artifacts
- `state/1460_semantic_detector/semantic_detector.py` — frozen dual detector + calibration
- `state/1460_semantic_detector/rescore_dual.py` — decode+dual-score cross-shuffle harness
- `state/1460_semantic_detector/run_all_aiden.sh` — pool GPU driver (base + lenses)
- `state/verdicts/1460_semantic_detector/` — raw verdict stdout
