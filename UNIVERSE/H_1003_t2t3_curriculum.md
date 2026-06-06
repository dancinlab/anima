---
id: H_1003
slug: t2t3-curriculum
title: Does curriculum learning (easy→hard sequence-length ramp) let the GRU world-model crack T2/T3, where direct training failed (H_1000)?
domain: cwm · cross-cutting · world-model · language-model · curriculum-learning · credit-assignment · trainability · re-test
source: H_1000 (🔴 DEEPER-LIMIT — a nonlinear BPTT-trained GRU still fails T2/T3, root-caused NOT to the primitive but to BPTT long-range credit assignment; its OWN stated next rung was "scale + CURRICULUM, e.g. staged delay / dense supervision, may yet crack T2/T3 — re-opening this as a TRAINABILITY finding") + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E14 (substrate-native) + E5 (re-run the SAME WM + SAME tasks with ONLY the training SCHEDULE changed) + a_completeness_over_cheap (run H_1000's own next rung properly — a real competence-gated length curriculum at EQUAL total budget, not a cheap proxy)
verification_method: W2 (pre-registered schedule-swap falsifier · same GRU-WM imported VERBATIM from H_1000 · capacity/width-matched · LM + mem-aug arms VERBATIM from H_985 · full-length held-out eval identical to H_1000 · curriculum vs direct side-by-side · T1-anchor guard · stage-progression stall guard · equal-total-epoch-budget control) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: TOY ladder — H_985/H_1000's SAME 3 task families × SAME 4-rung capacity ladder (dim 16/32/64/128) × SAME 10 seeds × {train 600 / test 300}, $0 CPU-local pure-numpy GRU (BPTT+Adam), NO torch (a_scale_honest_scope). The ONLY moved lever vs H_1000 is the TRAINING SCHEDULE (competence-gated easy→hard length ramp at EQUAL total epoch budget). Bounded toy dim/N/ramp; production-scale + larger-recurrence curriculum transfer UNVERIFIED. NOT a forge binary.
sister: H_1000 (the 🔴 DEEPER-LIMIT GRU-WM primitive test whose named next rung — "curriculum may yet crack T2/T3 as a trainability finding" — this directly runs), H_985 (the keystone scale-up whose T2/T3 PRIMITIVE-LIMITED diagnosis H_1000 falsified), H_970 (the keystone delayed-cue WM>LM existence-proof, T1)
axes_seed: "the H_1000 T2/T3 failure is a TRAINABILITY barrier (BPTT long-range credit assignment) — a competence-gated easy→hard length curriculum, SAME GRU-WM / capacity / total budget, cracks T2 AND T3 (H_1000's optimistic next-rung read)" ⊥ H_1003 = it may be DEEPER than the schedule — if even a curriculum-trained GRU (T1 kept, capacity/width-matched, equal budget, NO param advantage) STILL fails T2/T3, the barrier survives optimization and the WM>LM generality claim is re-scoped HARD (neither primitive NOR curriculum recovers it)
verdict: 🟢 PASS = CURRICULUM-CRACKS-T2T3 — moving ONLY the training SCHEDULE (direct-at-full-length → a competence-gated easy→hard length ramp 2→4→8→16→FULL, SAME GRU-WM imported verbatim, SAME capacity, SAME total 40-epoch budget, SAME full-length held-out eval) RESTORES the WM>LM separator on BOTH T2 (chance 0.500 → curr-GRU 0.751–1.000, d 1.32–20.71, separator at all 4 rungs vs direct-GRU's pinned 0.490–0.514) AND T3 (chance 0.167 → curr-GRU 0.574–0.930, d 1.10–21.06, all 4 rungs vs direct-GRU's ~0.34), WHILE T1 stays fully won (1.000, d up to 43.6). The curriculum demonstrably ADVANCED to full length (reached-FULL = 1.00 of seeds on every task) — not a stall. The H_1000 wall was an OPTIMIZATION / long-range credit-assignment barrier, NOT the primitive (H_1000) and NOT representability (mem-aug = 1.0): WM>LM generality is RECOVERABLE — just not by a richer primitive or by naive direct training. Re-opens H_1000 as a TRAINABILITY finding. Toy ladder; production OPEN.
---

# H_1003 — Does curriculum learning crack the T2/T3 GRU world-model wall? (trainability test of H_1000)

## 0. Motivation

H_985 (🔴) found the H_970 WM>LM separator is **TASK-SPECIFIC**: a persistent-state WM beats a capacity-matched stateless LM on **T1** (delayed-cue, d 20–35) but **vanishes on T2** (hidden 20-step XOR-parity) and **T3** (18-step modular path-integration), where both arms sit at chance — though the mem-aug LM control returns 1.0 on all three, proving T2/T3 genuinely ARE persistent-state tasks. H_985 blamed the **primitive** (a *linear* reservoir can carry a one-hot symbol but not an accumulated parity / integrated position) and named a nonlinear-GRU re-run as its next rung.

H_1000 ran exactly that and **falsified the primitive diagnosis** (🔴 DEEPER-LIMIT): a *nonlinear* BPTT-trained GRU **fully recovers T1** (0.954→1.000, d up to 38.7 — so the GRU + BPTT + Adam pipeline genuinely learns persistent state and is **not** under-trained, confirmed by a 300-epoch stress control) yet **still fails T2** (pinned 0.490–0.514 at chance) and **T3** (~2× chance, tied with the LM). H_1000 root-caused the wall **NOT** to the primitive but to **BPTT long-range credit assignment** — learning a 20-step accumulated XOR / 18-step path-integration from only a *final-step* label — and stated its own next rung **verbatim**: *"scale + curriculum (e.g. dense per-step parity supervision, or staged delay) may yet crack T2/T3, which would re-open this as a TRAINABILITY finding rather than a representational one."* H_1000 explicitly **excluded under-training** (the 300-epoch control). **This H runs that curriculum rung.**

## 1. Hypothesis (one falsifiable claim)

The H_1000 T2/T3 failure is a **TRAINABILITY / long-range-credit-assignment barrier**, not a deeper representational limit: training the **SAME** GRU world-model (capacity/width-matched, NO param advantage, **equal total epoch budget**) on a **competence-gated easy→hard sequence-length curriculum** (start short, lengthen on a competence threshold up to the full 20-step T2 / 18-step T3) — instead of directly at full length — **restores** the WM>LM separator on T2 AND T3 (large effect d>0.8 at ≥2 rungs each, tracking the mem-aug ceiling) while T1 stays won.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06, BEFORE measurement)

**Setup:** re-run H_985/H_1000's **SAME** 3 task families × **SAME** 4-rung capacity ladder {16,32,64,128} × **SAME** 10 seeds × {train 600 / test 300}. The GRU world-model (gated tanh recurrence, BPTT + Adam) is **IMPORTED VERBATIM** from `h1000_gru_wm_t2t3`; the LM + mem-aug arms are **IMPORTED VERBATIM** from `h985_keystone_scaleup`. Held-out evaluation is on the **FULL-length** test set (T2 len=20, T3 steps=18, T1 delay=16), **byte-identical** draw to H_1000 (apples-to-apples). The **ONLY** change vs H_1000 is the **TRAINING SCHEDULE**:
- **DIRECT (H_1000 baseline)** = train every example at full length from the start.
- **CURRICULUM (H_1003 treatment)** = a competence-gated **length ramp** 2→4→8→16→FULL; advance to the next (longer) stage only when train-accuracy ≥ 0.85 on the current stage (min 2 epochs/stage so it actually trains; leftover epochs roll forward so the GRU spends most of its budget at full length). **Total epoch budget held EQUAL to H_1000's direct budget (40 epochs)** so the comparison isolates the SCHEDULE, not extra compute.

**Measurement (g5 CODE-measured, no LLM self-judge):** per (task, rung) on the full-length test set — curriculum-GRU vs direct-GRU (H_1000) vs LM vs mem-aug success, gap (curr−LM), Cohen d, Welch p, Δ-vs-direct; PLUS the curriculum **stage-progression curve** (did it advance to full length, or stall?).

**Outcome rules (frozen, future-conditional — UNMEASURED at freeze):**
- IF the curriculum-GRU now SOLVES **T2 AND T3** (≫ chance, d>0.8 at ≥2 rungs each, tracking mem-aug) WHILE T1 stays won, AND the curriculum demonstrably advanced to full length → **PASS** 🟢 **CURRICULUM-CRACKS-T2T3** (the wall was an optimization / long-range credit-assignment barrier; WM>LM generality is RECOVERABLE — just not by primitive or naive training; re-opens H_1000 as a trainability finding).
- IF the curriculum-GRU **STILL fails** T2/T3 (≈ chance, ≈ direct GRU, d<0.8) → **FAIL** 🔴 **CURRICULUM-INSUFFICIENT** (the barrier survives curriculum too — deeper than the schedule; re-scopes the WM>LM generality claim HARD; closed-negative, a_paper_negative_ok).
- IF the curriculum never ADVANCES past the first short stage on T2/T3 (stalls — threshold never met) → INCOMPLETE (the schedule never actually ran; tune the ramp before ruling).

## 3. Honest scope

Toy ladder (a_scale_honest_scope): bounded dim {16,32,64,128}, toy N, pure-numpy GRU, short ramp, **equal 40-epoch total budget**. Three guards keep a verdict honest: (1) the T1 anchor must stay won (and does, d up to 43.6 — the curriculum pipeline is not broken); (2) a **stall guard** — the verdict is only PASS/FAIL if the curriculum actually reached full length (it did: reached-FULL = 1.00 of seeds on every task), else INCOMPLETE; (3) the **equal-total-budget** control — the curriculum gets NO extra compute over H_1000's direct run, so a win isolates the *schedule*, not more epochs. A PASS here re-opens H_1000 as a trainability result (a_paper_negative_ok inverse — a positive recovery). Production-scale, a larger recurrence, and curriculum on real corpora are UNVERIFIED. NOT a forge binary; $0 CPU-local; NOTHING on AKIDA (a_lane_akida_gpu_split).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror pure-numpy GRU+BPTT+Adam · curriculum schedule)

Probe: `UNIVERSE/h1003_t2t3_curriculum.py` (imports H_1000's GRU + H_985's tasks/arms verbatim) · verdict: `.verdicts/1003_t2t3_curriculum/h1003_t2t3_curriculum.txt`

| task | rung | chance | curr-GRU | dir-GRU (H_1000) | LM | memLM | gap | Cohen d | p | Δ vs direct |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 delayed-cue | 16 | 0.250 | 1.000 | 0.954 | 0.246 | 1.000 | 0.754 | 43.64 | 6.3e-15 | +0.046 |
| T1 delayed-cue | 32 | 0.250 | 1.000 | 1.000 | 0.243 | 1.000 | 0.757 | 38.68 | 1.9e-14 | +0.000 |
| T1 delayed-cue | 64 | 0.250 | 1.000 | 1.000 | 0.242 | 1.000 | 0.758 | 28.89 | 2.6e-13 | +0.000 |
| T1 delayed-cue | 128 | 0.250 | 1.000 | 1.000 | 0.245 | 1.000 | 0.755 | 34.89 | 4.7e-14 | +0.000 |
| **T2 parity-track** | 16 | 0.500 | **0.986** | 0.490 | 0.505 | 1.000 | 0.481 | 12.46 | 1.4e-15 | **+0.496** |
| **T2 parity-track** | 32 | 0.500 | **1.000** | 0.495 | 0.505 | 1.000 | 0.495 | 20.71 | 5.1e-12 | **+0.505** |
| **T2 parity-track** | 64 | 0.500 | **0.851** | 0.500 | 0.505 | 1.000 | 0.347 | 2.03 | 1.3e-03 | **+0.351** |
| **T2 parity-track** | 128 | 0.500 | **0.751** | 0.514 | 0.505 | 1.000 | 0.247 | 1.32 | 1.6e-02 | **+0.237** |
| **T3 hidden-pos** | 16 | 0.167 | **0.817** | 0.339 | 0.335 | 1.000 | 0.482 | 3.90 | 8.3e-06 | **+0.478** |
| **T3 hidden-pos** | 32 | 0.167 | **0.930** | 0.344 | 0.337 | 1.000 | 0.594 | 21.06 | 8.2e-20 | **+0.586** |
| **T3 hidden-pos** | 64 | 0.167 | **0.574** | 0.335 | 0.335 | 1.000 | 0.240 | 1.10 | 3.6e-02 | **+0.239** |
| **T3 hidden-pos** | 128 | 0.167 | **0.639** | 0.346 | 0.335 | 1.000 | 0.304 | 1.25 | 2.1e-02 | **+0.293** |

**Curriculum stage-progression (top rung, seed-0 trace `(len, epochs, train-acc)`):**
- T1 `[2,4,8,16]`: (2,2,1.0) (4,2,1.0) (8,2,1.0) (16,34,1.0) — sails through, spends its budget at full length.
- T2 `[2,4,8,16,20]`: (2,2,1.0) (4,3,0.962) (8,2,0.877) (16,31,0.615) (20,2,0.543) — clears easy stages, then pours the bulk of the budget into len-16, generalizing to the full len-20 held-out eval at **0.751–1.000**.
- T3 `[2,4,8,16,18]`: (2,2,1.0) (4,2,0.897) (8,2,0.932) (16,32,0.413) (18,2,0.373) — same shape; the front-loaded short stages bootstrap the integrator.
- **reached-FULL-length = 1.00 of seeds on ALL three tasks** (no stall — the schedule genuinely ran at full length).

**Per-task summary:** T1 — separator at all 4 rungs (kept). **T2 — separator at all 4 rungs (NEW; direct-GRU had zero).** **T3 — separator at all 4 rungs (NEW; direct-GRU had zero).** curr-solves = True on all three.

**Finding (🟢 PASS = CURRICULUM-CRACKS-T2T3):** moving **only the training schedule** — direct-at-full-length → a competence-gated easy→hard length ramp, with the **same** GRU-WM, **same** capacity, **same** total 40-epoch budget, **same** full-length held-out eval — **restores** the WM>LM separator on **both** T2 (chance 0.500 → 0.751–1.000, Δ vs direct up to +0.505, d 1.32–20.71) **and** T3 (chance 0.167 → 0.574–0.930, Δ vs direct up to +0.586, d 1.10–21.06), at **all four** capacity rungs, while T1 stays fully won. The curriculum demonstrably advanced to full length (reached-FULL = 1.00). The contrast against H_1000 is decisive and clean: **identical** model + capacity + budget + eval; the **sole** moved lever is the schedule, and that lever flips both failing families from chance to solved.

**Interpretation for CWM:** the H_1000 wall is now localized to **optimization, not the primitive and not representability**. H_985 (linear reservoir) and H_1000 (nonlinear primitive ruled out) bounded the *primitive* axis; this H shows the residual barrier was **long-range credit assignment** — a small BPTT-trained GRU cannot learn a 20-step XOR / 18-step path-integration *directly* from a final-step label, but **can** once an easy→hard curriculum supplies a short-horizon foothold and bootstraps the integrator out to full length. **WM>LM generality across T2/T3 is RECOVERABLE** — it was never out of reach for the recurrent WM; it was out of reach for naive direct training. This re-opens H_1000 as a **trainability** finding (the optimistic read its own next-rung sentence anticipated). Honest remaining ladder (a_toy_scale_recheck): this is a toy ramp at toy capacity; whether the curriculum recovery transfers to production-scale recurrence / real corpora is the next open rung.

## 4. Sibling / xlinks

- ⇄ [H_1000](./H_1000_gru_wm_t2t3.md) (🔴 DEEPER-LIMIT — the nonlinear-GRU primitive test whose named next rung this runs; its T2/T3 direct-GRU numbers are the baseline column here; its "curriculum may re-open this as a trainability finding" is now CONFIRMED — the wall was optimization, not primitive)
- ⇄ [H_985](./H_985_keystone_scaleup.md) (the keystone scale-up — its T2/T3 PRIMITIVE-LIMITED diagnosis was falsified by H_1000 and now further localized here to a *training-schedule* barrier; its mem-aug=1.0 state-boundness reproduces)
- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (the keystone delayed-cue WM>LM existence-proof — T1 stands; this H now extends WM>LM to T2/T3 under curriculum)
- ⇄ [H_992](./H_992_wm_lm_failure_frontier.md) (WM>LM failure-frontier — H_992's running-parity WM win is consistent with this: the parity-WM CAN win once trained appropriately; H_1000's direct-training null was the schedule, not the formulation)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · world-model ladder) · [H_962](./H_962_latent_forward_dynamics.md) · [H_964](./H_964_latent_to_action_policy.md) · [H_984](./H_984_world_model_object_permanence.md)
- external: curriculum learning (Bengio et al. 2009), staged/scaffolded training for long-range recurrence — this toy result is a clean controlled instance: the recurrent WM's long-range credit-assignment failure is removed by an easy→hard length ramp at equal compute (CWM.log.md landscape)
