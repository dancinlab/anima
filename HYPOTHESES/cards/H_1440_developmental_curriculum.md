---
id: H_1440
slug: 1440_developmental_curriculum
title: G6 IDEATION ★ FALS-depth — DEVELOPMENTAL multi-task curriculum (comparator→measurable→bind 순차)
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r4
terminal_tier: RUNNING (torch DIRECTIONAL fired on A100; engine-native re-measure pending)
wired: N/A (🧱-track expected; engine-native re-measure for terminal)
verdict_dir: state/verdicts/1440_developmental_curriculum/
date: 2026-06-20
---

# H_1440 — DEVELOPMENTAL curriculum: comparator→measurable→bind 3단계 순차 학습

## Why (생물 렌즈 — 언어획득 단계, a_no_llm_frame_trap)

H_1436 은 comparator∧measurable 를 SAME loss 에서 **동시** 보상 → aux SATURATED step-0
(informative-null), distinctness 손실, cross-shuffle 안 무너짐 (🧱 WALL=CAPACITY).
생물 언어획득은 동시가 아니라 **SEQUENTIAL** (한 단어→두 단어→단순구문→내포구문).
처방 = 3단계 발달 커리큘럼: (1) comparator-form 숙달 → (2) measurable-form 숙달 →
(3) 둘을 bind. 각 단계가 다음의 전제(scaffolding). H_1436(동시 보상)을 통제 arm 으로 대조 —
**순차가 동시와 달리 idea-specific 결합(B3 cross-shuffle COLLAPSE)을 가르치는가?**

## Method (FREEZE before run — `state/verdicts/1440_developmental_curriculum/FREEZE.txt`, c9/p7)

- 303M `h1129c_chat.pt` (303,097,856 params, PRESERVED, c5 — 새 ckpt) 위 3-phase 순차
  continued-pretrain. phaseN 은 phaseN-1 의 weights 에서 시작.
- **phase 순서 FROZEN** (comparator→measurable→bind; 사후 재배열 금지).
- phase corpora ISOLATION (state/1440_developmental_curriculum 에서 검증):
  - phase1 comparator-form: comparative clauses, **measurable 토큰 0 leak**.
  - phase2 measurable-form: measurement clauses, **comparator 토큰 0 leak**.
  - phase3 bind: H_1435 의 negatable-claim corpus VERBATIM (둘 결합).
- detector = h1305 `_is_falsifiable` VERBATIM (FROZEN). decode = gauge_lib `_decode`
  (live G6 path top-k=40 temp=0.7 MAX_NEW=110). engine-native(live core/ decode) 로
  재측정해야 terminal; torch-side = DIRECTIONAL (a_engine_native_learning).
- corpus subjects DISJOINT from gauge CONCEPT / eval / held-out seeds (anti-tune-to-green).
  NO detector token authored into training targets.
- seeds [7, 4302, 4303], N_IDEAS=5.

### Arms
1. **STAGED** (primary trained arm): comparator→measurable→bind, FROZEN order.
2. **CURRICULUM-ORDER-SHUFFLE** (발달가설 killer): SAME 3 phase-corpora, SAME total budget,
   RANDOMIZED phase order. staged 만 B3 collapse 하고 order-shuffle 은 안 하면 → 순서가
   load-bearing (발달 SUPPORTED). order-shuffle 도 collapse → 발달 FALSIFIED (총노출이면 충분).
3. **SHUFFLE-CORPUS** (tune-to-green killer): 각 phase byte-shuffled (구조 파괴).
   lift 나오면 artifact → INVALID. (lift_real − lift_shuf) ≥ 1 = INERT.

### Frozen 5-bar (H_1435 동일)
- **B1** FALS-FLOOR: staged mean FALS_in ≥ 1
- **B2** COUNT: staged DIST_in ≥ 5
- **B3** X-SHUFFLE COLLAPSE (DECISIVE): staged FALS_shuf < FALS_in — ★순차 curriculum 이
  idea-specific binding 인가
- **B4** HELD-OUT: staged FALS_ho ≥ 1
- **B5** vs-BASE: staged FALS_in ≥ base + 1
- **CTRL** shuffle-corpus INERT + **order-shuffle** non-collapse

VERDICT: 🟢 (terminal only ENGINE-NATIVE) iff 5-bar all-pass AND order-shuffle non-collapse
(발달 SUPPORTED). 🧱 iff B1/B5 미통과 OR B3 non-collapse OR order-shuffle ALSO collapses.

## Result

(RUNNING — torch DIRECTIONAL fired on vast A100-SXM4-80GB pod 41790357, AdamW lr=3e-5,
phase_steps=200×3, seeds [7,4302,4303]. Filled after the run + engine-native re-measure.)

## Scope

커리큘럼 순서·각 phase step 수가 frozen (튜닝으로 GREEN 제조 금지, c9). TOY 303M / 5 ideas /
3 seeds; scale/transfer UNVERIFIED. torch-side DIRECTIONAL — terminal 은 engine-native.

## Pointers

xref H_1436 (동시보상 대조 대상, informative-null) · H_1435 (training-side r1, bind corpus) ·
H_1437 (form-supervised) · H_1305 (detector) · H_1431/1432/1434 (elicitation-side capacity) ·
a_no_llm_frame_trap · a_engine_native_learning · a_fire_recover_complete · p7 · c9.
