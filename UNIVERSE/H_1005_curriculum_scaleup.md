---
id: H_1005
slug: curriculum-scaleup
title: Does the H_1003 curriculum crack of T2/T3 hold as the target sequence length scales up (≥2–3× longer), or does it break down at some horizon?
domain: cwm · cross-cutting · world-model · language-model · curriculum-learning · credit-assignment · scaling-law · horizon · re-test
source: H_1003 (🟢 CURRICULUM-CRACKS-T2T3 — a competence-gated easy→hard length ramp restores the WM>LM separator on T2/T3 at a SINGLE toy rung, T2 len=20 / T3 steps=18; its OWN stated OPEN gap was "production-scale + larger-recurrence curriculum transfer OPEN" — the scale ladder) + a_scale_honest_scope + a_toy_scale_recheck + a_paper_negative_ok + a_completeness_over_cheap
exploration_method: E5 (re-run the SAME curriculum-GRU + SAME tasks with ONLY the TARGET sequence LENGTH scaled up a ≥3-rung ladder) + a_toy_scale_recheck (a single toy rung is not closure for a scale-sensitive phenomenon — run the ladder) + a_scale_honest_scope (scope the verdict to the max length reached)
verification_method: W2 (pre-registered length-ladder falsifier · curriculum-GRU imported VERBATIM from H_1003 · task generators VERBATIM from H_1000/H_985 · LM + mem-aug arms VERBATIM from H_985 · in_dim FIXED across lengths · full-target-length held-out eval · curriculum vs LM vs mem-aug per task×length · shortest-rung harness-validation guard · stage-progression reached-FULL guard · equal-total-epoch-budget across lengths) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: TOY length ladder — T2 parity-track target len ∈ {20, 40, 80} (1×/2×/4× H_1003), T3 hidden-pos target moves ∈ {18, 36, 72} (1×/2×/4×), in_dim FIXED across lengths (T2=5, T3=9 — parity binary, position mod-P=6 at any move-count). Wall-time-honest TRIM (reported): 2 width-rungs {16,32} (of H_1003's {16,32,64,128}) × 6 seeds (of 10) × {train 600 / test 300}, $0 CPU-local pure-numpy GRU (BPTT+Adam), NO torch. TOTAL epoch budget = 40 per (task,length,seed) (== H_1003, same total compute, NOT scaled with length). The ONLY moved lever vs H_1003 is the TARGET LENGTH. Bounded toy ladder; production-scale + larger-budget + real-corpus transfer UNVERIFIED (a_scale_honest_scope). NOT a forge binary. NOTHING on AKIDA (a_lane_akida_gpu_split).
sister: H_1003 (the 🟢 CURRICULUM-CRACKS-T2T3 finding whose stated OPEN scale gap this directly runs — its T2=20 / T3=18 numbers are the shortest-rung column / harness validation), H_1000 (the 🔴 DEEPER-LIMIT direct-GRU baseline H_1003 cracked), H_985 (keystone scale-up — T2/T3 task generators + LM/mem-aug arms), H_970 (keystone delayed-cue WM>LM existence-proof, T1)
axes_seed: "the H_1003 curriculum fix is HORIZON-ROBUST — moving ONLY the target sequence length ≥2–3× longer (SAME curriculum-GRU / capacity / total budget / competence-gated ramp), the curriculum-GRU still SOLVES T2 AND T3 across ALL ladder rungs incl. the longest → CURRICULUM-SCALES" ⊥ H_1005 = the curriculum buys a BOUNDED horizon, not an unbounded one — accuracy collapses to chance / the integrator fails to bootstrap to full length at some longer horizon → CURRICULUM-HORIZON-CAPPED, report the breaking length (a real scaling-law finding)
verdict: 🔴 FAIL = CURRICULUM-HORIZON-CAPPED (SPLIT) — sweeping ONLY the TARGET length (SAME curriculum-GRU verbatim / capacity / total 40-epoch budget / competence-gated ramp 2→…→target), the two families DIVERGE. T2 XOR-parity SCALES: solves at every rung — len 20→0.977/1.000, 40→0.921/0.922, 80→0.918/0.912 (chance 0.5), d 2.7–17.3, gap vs LM ~0.42–0.49 at all of {20,40,80} (max tested). T3 modular path-integration is HORIZON-CAPPED: solves at len 18 (0.784/0.929, d 2.8/17.9, the H_1003 rung — harness validated) but BREAKS at 36 (0.363/0.389 ≈ chance 0.167-ish, d 0.60/1.16, gap ≤0.06, sep lost) and fully collapses to the LM at 72 (0.327/0.334 = LM 0.327, d≈0, gap≈0). The competence-gated ramp mechanically reaches the target stage but with the train-acc already at chance on the long stages (it spends its 40-epoch budget clearing short stages, arriving at the long stage too late to bootstrap), so reached-FULL=1.0 is a STAGE flag, not a SOLVE. Curriculum removes the H_1000 optimization wall up to a BOUNDED horizon — robustly for cumulative-parity (≥4× at fixed budget), but T3 path-integration caps at the H_1003 length (breaks at 2×). NOT an unbounded fix at fixed compute (closed-negative, a_paper_negative_ok). Toy ladder; larger-budget / production transfer OPEN.
---

# H_1005 — Does the curriculum crack of T2/T3 hold as the target sequence length scales up? (scale ladder of H_1003)

## 0. Motivation

**H_985** (🔴) found the H_970 WM>LM separator is task-specific: a persistent-state WM beats a stateless LM on **T1** (delayed-cue) but vanishes on **T2** (hidden XOR-parity) and **T3** (modular path-integration), where both sit at chance (mem-aug LM = 1.0 proves the tasks ARE state-bound). **H_1000** falsified the "primitive" diagnosis — a nonlinear BPTT-trained GRU fully recovers T1 yet STILL fails T2/T3 directly — and root-caused the wall to **BPTT long-range credit assignment**, naming a curriculum re-run as its next rung. **H_1003** ran it and **cracked it** (🟢 CURRICULUM-CRACKS-T2T3): a competence-gated easy→hard length ramp 2→4→8→16→FULL, SAME GRU / capacity / total budget, restores the WM>LM separator on BOTH T2 (chance→~1.0) and T3 (chance→~0.93) at the single toy rung (T2 len=20, T3 steps=18) — proving the wall was an OPTIMIZATION barrier, not the primitive.

But H_1003 was **one length**. Its own stated OPEN gap (verbatim): *"production-scale + larger-recurrence curriculum transfer OPEN."* Under **a_scale_honest_scope / a_toy_scale_recheck**, a single toy point on a scale-sensitive phenomenon is not closure — the question is whether the curriculum crack is **horizon-robust** or **horizon-capped**. **This H is that scale ladder.**

## 1. Hypothesis (one falsifiable claim)

The H_1003 curriculum fix is **horizon-robust**: scaling ONLY the target sequence length ≥2–3× longer (SAME curriculum-GRU, capacity, total epoch budget, competence-gated ramp extended to the new target), the curriculum-GRU still **SOLVES T2 AND T3** (≫ chance, large effect d>0.8 vs the stateless LM at ≥2 width-rungs, tracking the mem-aug ceiling) at **every** ladder rung **including the longest**, with the ramp reaching full target length at every rung.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07, BEFORE measurement)

**Setup:** re-run H_1003's curriculum-GRU + H_1000/H_985 task generators + H_985 LM/mem-aug arms **VERBATIM**. The **ONLY** change vs H_1003 is the **TARGET sequence LENGTH**, swept over a ≥3-rung ladder:
- **T2 parity-track** target length L ∈ **{20, 40, 80}** (1×, 2×, 4× H_1003)
- **T3 hidden-pos** target moves S ∈ **{18, 36, 72}** (1×, 2×, 4×)

At each target the curriculum's final stage is **extended** to that length (ramp 2→4→8→…→target via the SAME `_ramp()` rule), advancing on the SAME competence threshold (train-acc ≥ 0.85, min 2 ep/stage, leftover rolls forward), SAME **total 40-epoch budget** (NOT scaled with length — so the comparison isolates the HORIZON at fixed compute). **`in_dim` is FIXED across lengths** (T2 = 5: two toggle channels + cue + two answer; T3 = 9: two move channels + cue + six position channels; parity is binary and position is mod-P=6 at any number of moves) so the GRU/LM never sees a different input space — only the horizon over which credit must propagate grows. The LM + mem-aug arms are the SAME stateless windowed (ctx=4) predictors at each length — a control that CANNOT track parity/position regardless of length (stays at chance, the apples-to-apples baseline).

**Wall-time-honest trim (reported, not hidden):** the ladder triples the lengths (up to 4× longer BPTT) over H_1003's single length, so the width-rung set is trimmed to **{16, 32}** (of H_1003's {16,32,64,128}) and seeds to **6** (of 10). The shortest rung (T2=20 / T3=18) still mirrors H_1003 exactly, validating the harness against the published crack.

**Per (task, target-length, rung)** on the FULL-target-length held-out test set: curriculum-GRU vs LM vs mem-aug success, gap (curr−LM), Cohen d, Welch p, and the curriculum stage-progression (reached-FULL fraction across seeds).

**PASS-condition (frozen):** curriculum-GRU SOLVES T2 AND T3 (≫chance, d>0.8 vs LM at ≥2 rungs, tracking mem-aug) across ALL ladder rungs **including the longest**, AND the ramp reaches FULL target length at every rung → **🟢 CURRICULUM-SCALES** (horizon-robust; WM>LM generality holds as the horizon grows; toy ladder, production OPEN).

**FAIL-condition (frozen):** curriculum-GRU BREAKS at some horizon (accuracy → chance at a longer length, OR the ramp stalls before FULL, OR d<0.8 at the longest rung) → **🔴 CURRICULUM-HORIZON-CAPPED** (curriculum buys a bounded horizon; report the breaking length — a real scaling-law finding, a_paper_negative_ok).

**INCOMPLETE:** if even the shortest rung (== H_1003) fails to reproduce the crack here → harness mis-wired; fix before ruling.

## 3. Measurement (g5 CODE-measured · no LLM self-judge · `python3 -u` streaming)

`UNIVERSE/h1005_curriculum_scaleup.py` → `.verdicts/1005_curriculum_scaleup/h1005_curriculum_scaleup.txt` (verbatim).

| task | tgtLen | rung | chance | currGRU | LM | memLM | gap | d | reached-FULL | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| T2_parity | 20 | 16 | 0.500 | **0.977** | 0.511 | 1.000 | 0.467 | 9.62 | 1.00 | HOLD |
| T2_parity | 20 | 32 | 0.500 | **1.000** | 0.511 | 1.000 | 0.489 | 17.34 | 1.00 | HOLD |
| T2_parity | 40 | 16 | 0.500 | **0.921** | 0.475 | 1.000 | 0.446 | 3.27 | 1.00 | HOLD |
| T2_parity | 40 | 32 | 0.500 | **0.922** | 0.474 | 1.000 | 0.447 | 3.28 | 1.00 | HOLD |
| T2_parity | 80 | 16 | 0.500 | **0.918** | 0.494 | 1.000 | 0.424 | 2.95 | 1.00 | HOLD |
| T2_parity | 80 | 32 | 0.500 | **0.912** | 0.494 | 1.000 | 0.418 | 2.71 | 1.00 | HOLD |
| T3_hidden_pos | 18 | 16 | 0.167 | **0.784** | 0.342 | 1.000 | 0.443 | 2.79 | 1.00 | HOLD |
| T3_hidden_pos | 18 | 32 | 0.167 | **0.929** | 0.342 | 1.000 | 0.587 | 17.85 | 1.00 | HOLD |
| T3_hidden_pos | 36 | 16 | 0.167 | 0.363 | 0.333 | 1.000 | 0.030 | 0.60 | 1.00 | **BREAK** |
| T3_hidden_pos | 36 | 32 | 0.167 | 0.389 | 0.333 | 1.000 | 0.056 | 1.16 | 1.00 | **BREAK** |
| T3_hidden_pos | 72 | 16 | 0.167 | 0.327 | 0.327 | 1.000 | −0.000 | −0.00 | 1.00 | **BREAK** |
| T3_hidden_pos | 72 | 32 | 0.167 | 0.334 | 0.326 | 1.000 | 0.008 | 0.51 | 1.00 | **BREAK** |

(6 seeds, top-2 width-rungs; values verbatim from the verdict file.)

**Stage-progression (seed 0, rung 32) — the mechanism of the T3 cap:**
- T2 L=80: `(2,2) (4,3) (8,2) (16,2) (32,2) (64,2) (80,27,acc 0.552)` — clears every easy stage in min-epochs, pours 27 epochs into the full 80-length stage, and **generalizes** (test 0.912).
- T3 L=36: `… (16,13,acc 0.913) (32,18,acc 0.348) (36,2,acc 0.363)` — the integrator collapses **at the len-32 stage** (train-acc 0.348 ≈ chance) and never recovers; the 36-stage gets the last 2 epochs at chance.
- T3 L=72: `… (16,13,0.913) (32,16,0.34) (64,2,0.365) (72,2,0.373)` — same collapse at len-32; the ramp "reaches" 72 only as an epoch-budget formality.

## 4. Finding

**🔴 CURRICULUM-HORIZON-CAPPED — a SPLIT scaling law.** Moving ONLY the target length (everything else verbatim from H_1003, fixed 40-epoch budget, in_dim fixed) cleanly separates the two families:

- **T2 cumulative XOR-parity SCALES.** The curriculum solves it at every length 20→40→80 (curr-GRU 0.91–1.0, gap vs LM ~0.42–0.49, d 2.7–17.3) — robust to ≥4× the H_1003 horizon at fixed compute. Parity is a **commutative bit-accumulator** (XOR is associative/order-free, state is 1 bit): the curriculum's short-horizon foothold transfers to any length because the per-step update is the same at every position.
- **T3 modular path-integration is HORIZON-CAPPED.** It solves at the H_1003 length 18 (0.78/0.93, harness validated) but **breaks at 36** (≈ chance, d<0.8, sep lost) and collapses fully to the LM at 72. The integrator must maintain a **mod-6 ring counter** whose long-range credit chain the curriculum bootstraps up to ~length-18 at this budget but no further; the train-acc collapses at the **len-32 ramp stage**, so reaching the full target stage is a budget formality, not a solve.

The reading: the H_1003 curriculum removes the H_1000 long-range-credit-assignment wall **up to a bounded horizon, not unboundedly, at fixed compute** — and the horizon depends on the task's state structure (a commutative 1-bit accumulator scales far; a modular ring counter caps near the original length). This **bounds H_1003**: its 🟢 crack is real but **horizon-local for T3** and **horizon-robust for T2**. The mem-aug LM stays 1.0 at every length (the tasks remain perfectly state-bound — the cap is a *trainability-at-horizon* limit, not representability). Whether a larger total budget (scaled with length) or a denser per-step supervision lifts the T3 cap is the natural next rung (OPEN, a_completeness_over_cheap).

**Honest scope (a_scale_honest_scope, a_toy_scale_recheck):** TOY ladder — bounded dim {16,32}, 6 seeds, max length tested T2=80 / T3=72, pure-numpy GRU at a FIXED 40-epoch budget (NOT scaled with length, by design — isolates the horizon at fixed compute). The trim (2 rungs / 6 seeds vs H_1003's 4/10) is reported, and the shortest rung reproduces H_1003 (harness validated). Larger-budget / larger-recurrence / production / real-corpus transfer UNVERIFIED. NOT a forge binary; $0 CPU-local; nothing on AKIDA.

## 5. Sibling / xlinks

- ⇄ [H_1003](./H_1003_t2t3_curriculum.md) (🟢 CURRICULUM-CRACKS-T2T3 — the single-rung crack whose OPEN scale gap this runs; its T2=20 / T3=18 numbers are the shortest-rung harness-validation column here; this H **bounds** it: horizon-robust for T2, horizon-capped for T3 — status note appended there)
- ⇄ [H_1000](./H_1000_gru_wm_t2t3.md) (🔴 DEEPER-LIMIT — the direct-GRU baseline H_1003 cracked; the H_1003+H_1005 chain localizes its wall to an OPTIMIZATION barrier that curriculum removes up to a bounded horizon)
- ⇄ [H_985](./H_985_keystone_scaleup.md) (keystone scale-up — its T2/T3 task generators + LM/mem-aug arms are reused verbatim; mem-aug=1.0 state-boundness reproduces at every length, so the T3 cap is trainability-at-horizon, not representability)
- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (keystone delayed-cue WM>LM existence-proof — T1 stands; this H maps how far the WM>LM separator extends in *horizon* for T2/T3)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · world-model ladder) — a clean controlled scaling-law instance: curriculum buys a task-structure-dependent bounded horizon at fixed compute (CWM.log.md landscape)
- external: curriculum learning (Bengio et al. 2009); long-range credit assignment in recurrent nets — this toy result quantifies that an easy→hard length ramp's reach is bounded and depends on the target's state-update structure (commutative accumulator vs modular counter).

> **Follow-up (H_1006):** the T3 horizon cap is broken by DENSE per-step state supervision (H_1006 🟢) — NOT by more compute / ortho-init / warm-start / modulus-curriculum (H_1007-1010 🔴). The cap is a credit-DENSITY limit.
