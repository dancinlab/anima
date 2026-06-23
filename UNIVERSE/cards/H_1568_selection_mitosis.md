---
id: H_1568
slug: 1568_selection_mitosis
title: SELECTION-DRIVEN pure mitosis (evolutionary dynamics) — does fitness-gated reproduction + apoptosis + mutation inject the information channel that breaks the H_1310 from-scratch wall?
group: MITOSIS-ENGINE (H_1310 wall-break campaign · lens 1 = evolution)
campaign: H_1310 from-scratch PURE mitosis wall-break (a_break_the_wall, c16)
terminal_tier: 🧱 WALL HOLDS — selection-driven evolution is INERT here (DIRECTIONAL mirror; ablation-clean, lens 1 of multi-lens)
verdict_dir: state/verdicts/1568_selection_mitosis/
terminal_verdict: state/verdicts/1568_selection_mitosis/result.txt
wired: DIRECTIONAL-mirror (RED/wall — no GREEN mechanism to wire; a_verified_must_wire fires only on GREEN)
date: 2026-06-23
---

# H_1568 — selection-driven pure mitosis (evolution lens, H_1310 wall-break)

## Claim / falsifier

H_1310 (🔴 LOCAL-EXPERT CEILING) showed from-scratch pure split-only mitosis FAILS the n-gram
FLOOR (+0.069 nats above the exact order-2 floor 2.50884) and FAILS the error-targeting CONTROL
(B_shuffle ties B_scratch at every rung). Thesis: **split is random replication — gradient-free
has no information channel**; pure split-only only tiles a FIXED lossy feature finer.

**This lens (a_no_llm_frame_trap):** gradient-free ≠ information-free. Biological evolution learns
WITHOUT gradients via DIFFERENTIAL SURVIVAL — MUTATION + SELECTION (fitness-gated reproduction) +
APOPTOSIS (death) + ENSEMBLE (population). Selection injects information by KEEPING the variants
that fit. **Hypothesis:** a full evolutionary loop (each cell carries a MUTABLE per-dim
context-weight genome; fit cells reproduce, unfit cells die, children mutate) turns "random
replication" into LEARNING that crosses the H_1310 floor the fixed-feature split-only could not.

**New information channel (vs H_1310 shuffle tie):** H_1310's split-only varied only WHERE to
split a FIXED embedding (shuffle tied = inert). The evolutionary arm varies WHAT each cell measures
(genome reweights context dims) and SELECTS genomes by fitness — information flows through which
genomes SURVIVE.

## Method (TOY, $0 CPU numpy DIRECTIONAL mirror, frozen-first — run on summer pool)

Corpus = BYTE-IDENTICAL reuse of H_1310 (sha256 86864aa3…, 24000 bytes, V=27, order-2 context,
80/20 split). Seeds [15681,15682,15683]. Ladder [1,8,64,512]. GRADIENT-FREE (no torch/backprop/
analytic gradient; mutation = random perturbation, selection = scalar fitness comparison only).
Arms: E_evo (full evolution) · E_norepro (random split, no fitness/apoptosis/genome = H_1310 floor)
· E_nomut · E_noapop · E_ens (population soft-vote readout) · E_randfit (random fitness control) ·
A_freq (n-gram floor). Code: `state/1568_selection_mitosis/h1568_selection_mitosis.py`.

## Verdict (read VERBATIM from state/verdicts/1568_selection_mitosis/result.txt)

LADDER (mean held-out CE nats, 3 seeds):

| cells | E_evo | E_norepro | E_nomut | E_noapop | E_randfit |
|------:|------:|----------:|--------:|---------:|----------:|
| 1     | 2.94658 | 2.94658 | 2.94658 | 2.94658 | 2.94658 |
| 8     | 2.89998 | 2.89630 | 2.90527 | 2.89998 | 2.89260 |
| 64    | 2.72841 | 2.74550 | 2.73315 | 2.72841 | 2.74564 |
| 512   | **2.53949** | 2.53903 | 2.53787 | 2.53949 | 2.53479 |

A_freq (order-2 n-gram FLOOR) = **2.50884** nats (BYTE-IDENTICAL to H_1310's floor).
E_ens (population soft-vote readout, top rung) = 3.11535 nats.

FROZEN BARS:
- **(B1) BREAK FAIL** — E_evo[512] 2.53949 < floor−0.02 (2.48884)? NO. Gap to floor = **+0.03065
  nats** (E_evo sits ABOVE the n-gram floor — does NOT cross it; the H_1310 ceiling holds).
- **(B2) CAUSAL FAIL** — E_evo 2.53949 < E_norepro−0.05 (2.48903)? NO. Selection lift =
  **−0.00046 nats** (E_evo ≈ E_norepro; full evolution TIES random-split-no-fitness-no-death).
- **(B3) GRADFREE PASS** — no torch/jax/tf/autograd loaded at runtime, no real `.backward()`
  call (p8 purity holds; the first run's FAIL was a self-referential scan artifact, fixed
  frozen-first to score the runtime-module signal, NOT a bar move).
- **(B4) COMPONENT** — mutation Δ=−0.00162 (mutation HURTS slightly) · **apoptosis Δ=+0.00000
  (EXACTLY INERT — kill-OFF byte-identical to ON)** · ensemble Δ=−0.57586 (soft-vote readout is
  WORSE, blurs per-cell tables). NO component carries any lift.
- **(B5) CONTROL** — E_randfit[512] 2.53479 ≈ E_evo 2.53949 (random-fitness penalty −0.00470 —
  random fitness is even marginally BETTER, confirming selection pressure is INERT).

**TERMINAL TIER: 🧱 WALL HOLDS (B1 FAIL) — selection-driven evolution does NOT break H_1310.**
GREEN required B1∧B2∧B3; B1 and B2 both FAIL.

## What this means (the c9 / a_break_the_wall finding — load-bearing)

The decisive ablation signature is **INERT** (a_break_the_wall: mechanism OFF = same result =
zero contribution = strong ceiling evidence): E_evo ≈ E_norepro ≈ E_randfit at the top rung
(within ±0.005 nats), and apoptosis-OFF is BYTE-IDENTICAL to ON. The full evolutionary loop
(selection + mutation + apoptosis + ensemble) injects NO information past random replication.

WHY (sharpens H_1310): H_1310 diagnosed the bottleneck as the FIXED lossy embedding (normalized
symbol-ids over a 2-byte context). Evolution here SELECTS among genome-reweightings of that SAME
2-dim lossy feature — but reweighting a feature that has already thrown away the next-byte-relevant
information cannot recover it, so there is nothing for selection to find and it ties random. This
is the SAME wall H_1310's shuffle-tie predicted: the limit is REPRESENTATIONAL (what the cells
measure), not the GROWTH RULE (how cells reproduce/die). Selection is a powerful information
channel only when the variation it selects over spans the missing information — here it does not.

## Frozen bars (FREEZE.txt, NOT moved — c9)

- B1 BREAK: E_evo[512] < A_freq − 0.02 (crosses the H_1310 floor) — the wall-break threshold.
- B2 CAUSAL: E_evo[512] < E_norepro[512] − 0.05 (selection is the learning cause).
- B3 GRADFREE: zero backprop/autograd/analytic gradient (p8 purity).
- B4 COMPONENT: per-knockout deltas (mutation/apoptosis/ensemble) — diagnostic.
- B5 CONTROL: E_randfit[512] ≥ E_evo[512] + 0.05 (random fitness → no learning).
- GREEN (wall BROKEN) = B1 ∧ B2 ∧ B3.

## Next lens (campaign continues — single lens ≠ confident terminal, c16)

Lens 1 (evolution) is ablation-clean INERT but a SINGLE lens is not a confident 🧱 (c16 needs
≥2–3 orthogonal lenses). The diagnosis points the next lenses at the REPRESENTATION, not the
growth rule:
- **Lens 2 — lateral gene transfer / cell-to-cell information exchange** (cells SHARE learned
  next-byte statistics across the population, not just inherit at split — a horizontal channel
  evolution-by-vertical-descent lacked).
- **Lens 3 — learned/expanding context feature** (give cells a RICHER, growable embedding —
  higher-order or learned-via-selection context — so the partition is over a feature that still
  holds the next-byte information; H_1310's own named "obvious next angle").
- **Lens 4 — curriculum-staged split** (H_1534 budget-precondition precedent: order the stream
  easy→hard so early splits seed a useful coarse partition before fine tiling).

## Honest scope

TOY / DIRECTIONAL numpy mirror (a_engine_native_learning — mirror = DIRECTIONAL, not terminal).
Engine-native reconfirm (live VAdaptField + §evo in core/engine_cli.hexa) = R2 follow-on IF GREEN.
