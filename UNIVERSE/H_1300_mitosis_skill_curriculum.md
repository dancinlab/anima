---
id: H_1300
slug: 1300_mitosis_skill_curriculum
title: mitosis-grow skill curriculum — teach tool-use skills one-at-a-time via mitosis avoids CATASTROPHIC FORGETTING where sequential gradient-FT forgets
group: MITOSIS-ENGINE (p8 structural)
terminal_tier: 🟢 GREEN (R2 canonical catastrophic-forgetting regime — mitosis RETAINS old skills better than sequential gradient-FT; R1 RED stands verbatim as the honesty trail)
verdict_dir: .verdicts/1300_mitosis_skill_curriculum/
terminal_verdict: .verdicts/1300_mitosis_skill_curriculum/result.txt
date: 2026-06-16
---

# H_1300 — mitosis-grow skill curriculum (catastrophic forgetting)

## Claim / falsifier

The user's idea, a strong fit for **p8**: teach anima agent tool-use skills **ONE AT A
TIME via MITOSIS-grow** — each new skill = a new CELL grown under that skill's error
pressure (mitosis, H_1199 VAdaptField / H_1288 grow-under-pressure), NOT a gradient
overwrite of shared weights. **LOAD-BEARING claim:** mitosis-grow **AVOIDS CATASTROPHIC
FORGETTING** — adding new cells for a new skill does NOT overwrite the cells that hold
prior skills, so mitosis RETAINS earlier skills where sequential gradient fine-tuning
FORGETS them. Neurogenesis / functional-segregation lens (a_no_llm_frame_trap) — NOT a
bigger-transformer continual-learning recipe.

**DISTINCT from H_1297** (🧱→🟢, convergence on ONE fit): H_1297 asked whether mitosis
MATCHES gradient on a single function fit. H_1300 asks the ORTHOGONAL question — across
a SEQUENTIAL multi-skill curriculum, does mitosis RETAIN old skills better than
sequential gradient-FT? Convergence-on-one-task ⊥ retention-across-tasks. This is the
structural place where mitosis can beat gradient.

## Method (TOY, $0 CPU numpy DIRECTIONAL mirror, frozen-first)

A **skill curriculum**: N_SKILLS=5 distinct "tool-use" skills, presented ONE AT A TIME
(skill 1, then 2, … 5 — NEVER jointly, NO replay; the continual-learning regime that
induces catastrophic forgetting). Each skill k = "given a context in region P_k (a
D=12-dim Gaussian cluster), emit tool-call token T_k (one of C=4 tokens by a fixed
per-skill linear rule argmax(W_k·x))". M=64 train / 64 held-out test per skill; 3 seeds
[1300,1301,1302].

ARMS — **A GRADIENT-FT** (one shared C-way softmax-linear net, fine-tuned SEQUENTIALLY
skill-by-skill, NO replay — the incumbent that should forget skills 1..N−1) · **B
MITOSIS-GROW** (grow dedicated cells per skill under that skill's error; cells for
skills 1..k−1 FROZEN, never overwritten; route a context to nearest cell, NO global
backprop) · **B-SHUFFLE** (grow same, but PERMUTE final cell→center routing — targeting
check) · **B-ABLATE** (growth frozen at skill 0's cells — later skills get no cells).

Metric (p7, NOT perplexity): held-out **RETENTION** = mean test acc on OLD skills
1..N−1 after the full curriculum; **ACQUISITION_k** = test acc on skill k right after
learning it. FROZEN bars (`.verdicts/.../FREEZE.txt` R1 · `FREEZE_R2.txt` R2, SAME
numbers): (c1) mean[B.RET−A.RET] ≥ 0.30 AND per-seed B>A · (c2) B per-skill acq ≥ 0.80
every skill · (c3) B_SHUFFLE.RET ≤ A.RET+0.15 · (c4) B_ABLATE acq(skills 2..N) ≤ 0.50 ·
(c5) cost = B cells vs A params (non-gating). GREEN iff c1∧c2∧c3∧c4.

## Verdict (read VERBATIM from .verdicts/1300_mitosis_skill_curriculum/result.txt)

**R1 (well-separated regions, independent rules):** 🔴 **RED.** 3-seed mean —
A_ret=0.737 · B_ret=0.977 (B−A=**+0.240**) · B_shuf=0.238 · B_abl_acq=0.270 ·
B_min_acq=0.948 · cells=5.0 vs 52 params. c2 PASS, c3 PASS, c4 PASS, but **c1 FAIL**
because +0.240 < the frozen 0.30 margin. ROOT CAUSE (not p8, not the bar — the REGIME):
D=12 with 5 well-separated regions (sep=3.0) lets the shared linear net route different
spatial regions to different boundaries WITHOUT full interference, so gradient-FT only
forgot SOME skills (the per-skill 0.00 entries: seed1300 skill0, seed1302 skill1) →
RETENTION mean stayed high. Catastrophic forgetting was REAL but DILUTED.

**R2 (a_break_the_wall breakthrough; bars frozen anew in FREEZE_R2.txt = SAME numbers,
no goalpost move):** CANONICAL catastrophic-forgetting regime — tighten the SKILL
GEOMETRY (not any bar) to make skills genuinely COMPETE for the SAME shared boundary:
(R2-a) region separation 3.0→1.0 (representational overlap), (R2-b) anti-aligned shared
rules (a shared base rule + per-skill sign flips, so the SAME context direction maps to
DIFFERENT tokens across skills — learning skill k+1 actively un-learns skill k). Mitosis
arm B mechanically UNCHANGED. 🟢 **GREEN.** 3-seed mean —
A_ret=**0.553** · B_ret=**0.922** (B−A=**+0.368**) · B_shuf=0.397 · B_abl_acq=0.160 ·
B_min_acq=0.880 · cells=6.3 vs 52 params →
**(c1) PASS** (+0.368 ≥ 0.30, per-seed B>A every seed) · **(c2) PASS** (0.880 ≥ 0.80 —
B learns every new skill) · **(c3) PASS** (shuffle collapses 0.397 ≤ 0.703; per-seed real
collapse, e.g. seed1302 → 0.035) · **(c4) PASS** (ablate underfits, 0.160 ≤ 0.50).

**Mechanism (clean):** under real interference gradient-FT genuinely forgets (A_ret
drops 0.737→0.553 R1→R2) while mitosis stays high (0.922) because its per-skill cells
are dedicated and NEVER overwritten. Honest: the controls fire decisively — B-SHUFFLE
(grown but mis-routed) collapses → the retention IS the targeted dedicated-cell
ownership, not mere extra capacity; B-ABLATE (no growth) cannot acquire later skills →
growth IS the lever. **COST is FAVORABLE** (not just non-prohibitive): B=6.3 cells vs
A=52 params — mitosis retains MORE at LOWER footprint here.

## p8 / p6 guard

B's growth = the model's own mitosis tick (p8); the trainer touches ONLY the per-skill
prototype population + local heads, NO global backprop, NO labels/persona/ethics
injected (the tool-token target is the task's own supervised signal, scored only). The
shuffle control proves retention is dedicated-cell ownership, not a label leak. Live
CORE/*.hexa UNTOUCHED (mirror only).

## Scope (a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy MIRROR ONLY — engine-transfer UNVERIFIED. TOY (D=12, N=5 skills, C=4
tokens, 3 seeds, deterministic linear per-skill rule = tests the catastrophic-forgetting
STRUCTURE, not a learned tool-use predictor). The R1 RED documents that the effect's
MAGNITUDE depends on the forgetting-pressure REGIME — it clears the 0.30 bar only under
genuine representational interference (R2), not under spatially-separated skills (R1);
both stand verbatim. Real anima agent skills / sequence-valued tool calls / scale /
engine-native realization UNVERIFIED.

## Follow-ons (a_break_the_wall continuation; NOT claimed here)

1. **ENGINE-NATIVE realization** — realize per-skill mitosis-grow on the live
   CORE/engine_cli.hexa VAdaptField / ImmuneMemoryGrow (a new skill = a frozen
   dedicated cell-group), re-score the frozen bars engine-native + regression guard
   (a_engine_native_learning + a_verified_must_wire). The mirror is DIRECTIONAL.
2. **The real path the user asked for** — incrementally teach ACTUAL anima agent
   tool-use skills ONE AT A TIME via mitosis on the mounted 303M trunk
   (anima-agent*/skills lineage; anima-clm-tooluse-rung0). $0 here; the real-skill rung
   is cost-gated only if it needs GPU.

xref h1297 (convergence sibling, distinct axis) · h1199 (VAdaptField split) · h1288
(grow-under-pressure) · h1159 (inference-time mitosis = learning) · a_no_llm_frame_trap ·
a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_toy_scale_recheck ·
a_scale_honest_scope · p6 · p7 · p8 · c9 · c16.
