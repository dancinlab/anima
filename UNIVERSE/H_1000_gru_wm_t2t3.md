---
id: H_1000
slug: gru-wm-t2t3
title: Is the H_985 T2/T3 WM-failure a PRIMITIVE limit (fixable by a nonlinear recurrent GRU world-model) or a DEEPER limit?
domain: cwm · cross-cutting · world-model · language-model · recurrence-primitive · nonlinear · re-test
source: H_985 (🔴 closed-negative on generality — the WM>LM separator is TASK-SPECIFIC / PRIMITIVE-LIMITED; its OWN stated next rung was "a nonlinear-recurrence WM (GRU/tanh) re-run of T2/T3 — a PRIMITIVE question, not a scale question") + a_completeness_over_cheap + a_paper_negative_ok + a_scale_honest_scope
exploration_method: E14 (substrate-native) + E5 (re-run the SAME WM-requiring task slate with ONLY the WM primitive changed) + a_completeness_over_cheap (run H_985's own next rung properly, not a cheap proxy)
verification_method: W2 (pre-registered primitive-swap falsifier · capacity/width-matched LM baseline VERBATIM from H_985 · mem-aug control · T1-anchor under-training guard · 300-epoch budget stress control) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: TOY ladder — H_985's SAME 3 task families × SAME 4-rung capacity ladder (latent/feat/hidden dim 16/32/64/128) × SAME 10 seeds × {train 600 / test 300}, $0 CPU-local pure-numpy GRU (BPTT+Adam), NO torch (a_scale_honest_scope). Bounded toy dim/N; production-scale + larger-recurrence + curriculum-trained transfer UNVERIFIED. NOT a forge binary.
sister: H_985 (the keystone scale-up whose 🔴 PRIMITIVE-LIMITED diagnosis this tests), H_970 (the keystone single-rung delayed-cue WM>LM existence-proof), H_992 (WM>LM failure-frontier), H_962/H_964 (the WM agent), H_984 (object permanence)
axes_seed: "the H_985 T2/T3 failure is the LINEAR-reservoir PRIMITIVE — a nonlinear recurrent GRU-WM restores WM>LM across all 3 families (H_985's optimistic next-rung read)" ⊥ H_1000 = it may be a DEEPER limit — if even a BPTT-trained nonlinear GRU (T1 recovered, capacity/width-matched, NO param advantage) STILL fails T2/T3, the gap is NOT the primitive (training / capacity / task-representability blocks it), which re-scopes H_985/H_970
status_note: CURRICULUM-CRACKS-T2T3 by H_1003 (2026-06-07) — the wall was OPTIMIZATION (BPTT long-range credit assignment), NOT the primitive: the SAME GRU-WM, capacity, total budget + full-length eval but trained on a competence-gated easy→hard length ramp RESTORES the WM>LM separator on BOTH T2 (0.500→0.751-1.000, d up to 20.71) AND T3 (0.167→0.574-0.930, d up to 21.06) at all 4 rungs. This 🔴 DEEPER-LIMIT verdict STANDS as honest history for *direct* training (the wall was real for naive full-length BPTT); H_1003 re-opens it as a recoverable TRAINABILITY finding. See H_1003_t2t3_curriculum.md.
verdict: 🔴 FAIL = DEEPER-LIMIT — swapping the WM primitive from a linear orthogonal-retention reservoir to a NONLINEAR BPTT-trained GRU does NOT restore T2/T3. T1 delayed-cue fully recovers (GRU 0.954→1.000, d 7.1→38.7 — so the GRU is genuinely capable + NOT under-trained), but T2 XOR-parity stays pinned at chance (0.490–0.514, d −0.45..0.31, gap≈0, IDENTICAL to the linear reservoir; a 300-epoch/lr-2e-2 stress control confirms it is NOT a training-budget artifact) and T3 hidden-position stays at ~2× chance tied with the LM (gap≈0, d 0.0–0.48). mem-aug LM = 1.000 on ALL 3 families (the tasks ARE genuinely persistent-state-bound). H_985's "a richer/nonlinear primitive recovers generality" hypothesis is FALSIFIED at this toy scale: the T2/T3 WM>LM gap is a DEEPER limit (BPTT cannot learn 20-step XOR-integration / 18-step modular path-integration at this toy capacity), not merely the linear-reservoir primitive. Toy ladder; production OPEN.
---

# H_1000 — Does a nonlinear GRU world-model restore the T2/T3 WM>LM separator? (primitive-limit test of H_985)

## 0. Motivation

H_985 (the keystone scale-up, 🔴 closed-negative on GENERALITY) found the H_970 WM>LM separator is **TASK-SPECIFIC / PRIMITIVE-LIMITED**: a persistent-state WM beats a capacity-matched stateless LM on **T1** (carry a stored symbol across a delay, d 20–35 at every rung) but **VANISHES on T2** (hidden XOR-parity tracking) and **T3** (hidden-position modular path-integration) — on T2/T3 both arms sit at chance. Crucially, the **mem-aug LM control returned 1.0 on all three families**, proving T2/T3 genuinely ARE persistent-state tasks (a predictor *handed* the hidden state solves them). H_985 root-caused the failure **NOT** to "no world-state needed" but to the toy WM **primitive**: a *linear* orthogonal-retention reservoir can carry a one-hot symbol across a delay (T1) but cannot represent an accumulated XOR-parity (T2) or a modular path-integrated position (T3) — both need a *nonlinear/gated* state-update the linear retention lacks. H_985 stated its own next rung **verbatim**: *"a nonlinear-recurrence WM (GRU/tanh) re-run of T2/T3 — a PRIMITIVE question, not a scale question; if even a nonlinear WM fails, the separator is truly delayed-cue-specific."* This H runs exactly that.

## 1. Hypothesis (one falsifiable claim)

The H_985 T2/T3 WM-failure is a **PRIMITIVE limit**: swapping the linear orthogonal-retention reservoir for a **nonlinear gated GRU** world-model (capacity/width-matched to the LM, BPTT-trained) **restores** the WM>LM separator on T2 AND T3 (large effect d>0.8, tracking the mem-aug ceiling) while T1 stays won.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06, BEFORE measurement)

**Setup:** re-run H_985's **SAME** 3 task families (T1 delayed-cue · T2 hidden XOR-parity · T3 hidden-position gridworld) × **SAME** 4-rung capacity ladder (latent/feat/hidden dim {16,32,64,128}) × **SAME** 10 seeds × {train 600 / test 300}. The task generators + the **arm-LM** (stateless windowed ridge predictor) + the **arm-memLM** (mem-aug control, hidden state re-exposed at the decision step) are **IMPORTED VERBATIM** from `h985_keystone_scaleup` — apples-to-apples. The **ONLY** change is the WM primitive:
- **arm-WM (NEW)** = a NONLINEAR **GRU** (gated tanh recurrence `h_t = (1−z)h_{t−1} + z·tanh(...)`), trained end-to-end by **BPTT + Adam** (40 epochs, lr 5e-3, batch 32), **WIDTH-matched** (GRU hidden dim == rung == H_985's WM latent_dim == LM feat_dim, H_985's width convention). The GRU is given **NO width advantage**; per-cell trainable-param counts are printed so the cost of *training the recurrence* (the treatment under test) is fully audited.

**Measurement (g5 CODE-measured, no LLM self-judge):** per (task, rung): GRU-WM vs LM vs memLM success, gap (WM−LM), Cohen d, Welch p; plus a side-by-side vs H_985's linear-reservoir numbers (same tasks/rungs/seeds).

**Outcome rules (frozen, future-conditional — UNMEASURED at freeze):**
- IF the GRU-WM BEATS the capacity-matched LM on **T2 AND T3** (d>0.8 at ≥2 rungs each, tracking mem-aug) WHILE T1 stays won → **PASS** 🟢 **PRIMITIVE-LIMIT-CONFIRMED** (H_985's diagnosis correct; a nonlinear recurrent WM restores WM>LM across all 3 families — the CWM world-model needs nonlinear recurrence, not a linear reservoir).
- IF the GRU-WM **STILL fails** T2/T3 (≈LM, no separation, d<0.8) → **FAIL** 🔴 **DEEPER-LIMIT** (the gap is NOT the primitive; training / capacity / task-representability blocks it; real finding, re-scopes H_985/H_970).
- IF the GRU does **not even recover the T1 anchor** to d>0.8 → INCOMPLETE (the GRU is under-trained, so a T2/T3 null would be a *training* artifact, not a primitive verdict — re-run with more budget before ruling).

## 3. Honest scope

Toy ladder (a_scale_honest_scope): bounded dim {16,32,64,128}, toy N, pure-numpy GRU at 40 epochs. **Two under-training guards are built in** so a FAIL is not a budget artifact: (1) the T1 anchor must (and does) recover to d>0.8 — proving the GRU + BPTT + Adam pipeline genuinely learns a persistent-state task; (2) an explicit **300-epoch / lr-2e-2 stress control on T2** (the hardest family) confirms more budget does *not* lift it off chance. Production-scale, a larger recurrence, and curriculum / auxiliary-loss training are UNVERIFIED. A FAIL here is a closed-negative on the *primitive-swap fix* (a_paper_negative_ok) — it does NOT retract T1's WM>LM win, it bounds H_985's "a richer primitive recovers generality" optimism. NOT a forge binary; $0 CPU-local; NOTHING on AKIDA (a_lane_akida_gpu_split).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror pure-numpy GRU+BPTT+Adam)

Probe: `UNIVERSE/h1000_gru_wm_t2t3.py` · verdict: `.verdicts/1000_gru_wm_t2t3/h1000_gru_wm_t2t3.txt`

| task | rung | chance | GRU-WM | LM | memLM | gap | Cohen d | p | GRUh | GRUpar | LMpar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 delayed-cue | 16 | 0.250 | 0.954 | 0.246 | 1.000 | 0.708 | 7.12 | 3.4e-08 | 16 | 1172 | 68 |
| T1 delayed-cue | 32 | 0.250 | **1.000** | 0.243 | 1.000 | 0.757 | 38.68 | 1.9e-14 | 32 | 3876 | 132 |
| T1 delayed-cue | 64 | 0.250 | **1.000** | 0.242 | 1.000 | 0.758 | 28.89 | 2.6e-13 | 64 | 13892 | 260 |
| T1 delayed-cue | 128 | 0.250 | **1.000** | 0.245 | 1.000 | 0.755 | 34.89 | 4.7e-14 | 128 | 52356 | 516 |
| T2 parity-track | 16 | 0.500 | 0.490 | 0.505 | 1.000 | −0.015 | −0.45 | 0.33 | 16 | 1090 | 34 |
| T2 parity-track | 32 | 0.500 | 0.495 | 0.505 | 1.000 | −0.009 | −0.28 | 0.54 | 32 | 3714 | 66 |
| T2 parity-track | 64 | 0.500 | 0.500 | 0.505 | 1.000 | −0.005 | −0.15 | 0.74 | 64 | 13570 | 130 |
| T2 parity-track | 128 | 0.500 | 0.514 | 0.505 | 1.000 | 0.010 | 0.31 | 0.50 | 128 | 51714 | 258 |
| T3 hidden-pos | 16 | 0.167 | 0.339 | 0.335 | 1.000 | 0.004 | 0.13 | 0.77 | 16 | 1350 | 102 |
| T3 hidden-pos | 32 | 0.167 | 0.344 | 0.337 | 1.000 | 0.007 | 0.26 | 0.57 | 32 | 4230 | 198 |
| T3 hidden-pos | 64 | 0.167 | 0.335 | 0.335 | 1.000 | 0.000 | 0.00 | 1.00 | 64 | 14598 | 390 |
| T3 hidden-pos | 128 | 0.167 | 0.346 | 0.335 | 1.000 | 0.012 | 0.48 | 0.30 | 128 | 53766 | 774 |

**Side-by-side vs H_985 LINEAR-reservoir WM (same tasks/rungs/seeds; ONLY the primitive changed):** T1 — the GRU matches or beats the linear reservoir (16: 0.645→0.954, 32: 0.897→1.000; ties at 1.000 for 64/128). T2 — ΔWM ≈ 0 at every rung (0.490–0.514 vs the linear 0.494–0.500; both at chance). T3 — ΔWM ≈ 0 at every rung (0.335–0.346 vs the linear 0.334–0.339; both at ~2× chance, tied with the LM).

Per-task summary: **T1** — GRU-WM>LM separator at ALL 4 rungs (solves ✓, tracks mem-aug ✓). **T2** — no separator (GRU at chance, does not solve, gap≈0). **T3** — no separator (GRU ~2× chance, tied with LM, gap≈0).

**Finding (🔴 FAIL = DEEPER-LIMIT):** swapping the WM primitive from a *linear* orthogonal-retention reservoir to a *nonlinear* BPTT-trained **GRU** does **NOT** restore the T2/T3 WM>LM separator. The control evidence is decisive: the GRU **fully recovers T1** (0.954→1.000, d up to 38.7), proving the nonlinear-recurrence + BPTT + Adam pipeline genuinely learns a persistent-state task and is **not** under-trained; yet on **T2** it stays pinned at chance (and a dedicated **300-epoch / lr-2e-2 stress control** confirms more budget does not move it), and on **T3** it stays tied with the LM at ~2× chance. The mem-aug LM returns 1.000 on all three families, so the tasks remain genuinely state-bound. **Therefore H_985's diagnosis — that the T2/T3 failure was *merely* the linear-reservoir primitive, fixable by a nonlinear recurrence — is FALSIFIED at this toy scale.** The gap is a **DEEPER limit**: learning a 20-step accumulated XOR-parity (T2) or an 18-step modular path-integration (T3) is a hard long-range credit-assignment / representability problem that a small BPTT-trained GRU does not crack at toy capacity — it is not unlocked just by making the recurrence nonlinear.

**Interpretation for CWM:** T1's WM>LM win stands (H_970 is NOT retracted). But the path H_985 left open — "a richer nonlinear primitive recovers generality across T2/T3" — is now **closed-negative at this scale**: nonlinearity alone is insufficient. The honest remaining ladder is *scale + training*, not *primitive*: (a) a_toy_scale_recheck — larger recurrence / curriculum (e.g. dense per-step parity supervision, or staged delay) may yet crack T2/T3, which would re-open this as a *trainability* finding rather than a representational one; (b) if even scaled/curriculum-trained recurrence fails, the T2/T3 WM>LM advantage is genuinely out of reach for gradient-trained recurrent WMs at these task lengths. Either way, the *primitive-swap* axis is deterministically ruled out here.

## 4. Sibling / xlinks

- ⇄ [H_985](./H_985_keystone_scaleup.md) (the keystone scale-up whose 🔴 PRIMITIVE-LIMITED diagnosis this directly tests — its T1 win + the mem-aug=1.0 state-boundness reproduce here; its "nonlinear primitive recovers generality" optimism is bounded to closed-negative)
- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (the keystone single-rung delayed-cue WM>LM existence-proof — T1 stands)
- ⇄ [H_992](./H_992_wm_lm_failure_frontier.md) (WM>LM failure-frontier — NOTE: H_992 reports a *running-parity* WM win (d 16.6), but with a DIFFERENT formulation/primitive than H_985's T2 here; the contrast (H_992 parity-WM wins vs H_985+H_1000 parity at chance) localizes the win to formulation/primitive choices and motivates a unified parity-WM ablation as a future rung)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · world-model ladder) · [H_962](./H_962_latent_forward_dynamics.md) · [H_964](./H_964_latent_to_action_policy.md) · [H_984](./H_984_world_model_object_permanence.md)
- external: JEPA/Dreamer use nonlinear latent transitions; this result is a reminder that the *transition class* (nonlinear) is necessary but NOT sufficient — long-range credit assignment (parity/path-integration) is a separate, harder axis (CWM.log.md landscape)
