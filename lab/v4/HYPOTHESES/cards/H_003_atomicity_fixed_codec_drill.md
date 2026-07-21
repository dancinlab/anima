---
id: H_003
ssot: ARCHITECTURE.json → next-gate.*, salvage.L4.*  (this card is the pre-register, not the SSOT)
slug: atomicity-fixed-codec-drill
title: an ATOMIC negator token in a fixed jamo-BPE codec CAUSES held-out negation recombination — the one variable is the encoder's span policy (atomic vs shattered), same vocabulary, same corpus, same model, same seed; predicted Δd_acc ≥ 0.15 (A-atom − A-shat) on an OOD panel whose control sits near 0.5
domain: verification-design (causal drill · pre-register)
status: falsified
exploration_method: design delegated to Fable 5 under fable-mode; span-policy lever derived independently and cross-checked; codec behaviour probed on the real decomposer
verification_method: deterministic panel audits (F7 · closed-form, pre-training) + trained-arm falsifiers (F1–F8) with a placebo and a leak-ceiling arm
pre_register_frozen: true
frozen_at: 2026-07-16 (encoder GREEN · panels F7 PASS · G-0 PASS · G-1 PASS by owner-delegated LLM judgment · drill 못=0; the only unrun piece is the training driver + 6-8h run)
deterministic: false
llm: none in the eval path (design only; the model is trained, the scoring is deterministic forced-choice)
---

# H_003 — atomicity, isolated: does an atomic negator token CAUSE recombination?

> **SSOT**: the design tree is `ARCHITECTURE.json` — this card is the pre-register. The claim, arms,
> and lever live at `next-gate.*`, `salvage.L4.what-was-actually-causal`, `salvage.L4.atomicity-was-
> luck-not-method`. Human viewer: `python3 serve.py`.

## Status — 🔴 FALSIFIED 2026-07-16 (RAN, clean measurement)

Pre-registered frozen 2026-07-16 (every $0 pre-training gate PASSED — encoder one-variable lever
GREEN 67/67, panels F7 PASS v3 SLOT-CONTRAST, G-0 codec audit PASS 3/3, G-1 grammar PASS by
owner-delegated LLM judgment, drill grid with held-out 못 = 0), then **RAN** to completion on local
MPS (d=384 L=4 ×2 seeds × 5 arms, ~5.5h). The frozen falsifiers returned **FALSIFIED** on a clean
measurement — see **## Verdict** below for the arm table and numbers.

It was the first mechanism in the campaign to reach the run stage, and it did so only because three
prior $0 gates cleared the ground: `H_001` killed the bet's falsifier, the literature gate killed its
objective, `H_002` killed the L5 premise — and all three left **one survivor**, atomicity
(`salvage.L4.what-was-actually-causal`). H_003 tested that survivor directly, in isolation — and it
did not hold. mech-3 is now dead in all four parts.

## Hypothesis

`salvage.L4b` established that a fixed jamo-BPE codec is *causal* for held-out negation recombination
(d_acc 0.9083/0.9167 vs a no-codec control 0.6167/0.5750). But that comparison varies **whether a
codec exists at all** — it cannot say *what about the codec* matters. `H_002` and the C2/C3 arms
narrowed it to one thing: **atomicity of the negator token** (not identity — C3; not pretraining
exposure — C2; not boundary visibility — H_002).

**Claim**: giving the negator its own atomic token *causes* held-out negation recombination. The one
variable is the encoder's span policy. Hold the vocabulary, corpus, model, steps, and seed identical;
vary only whether the negator span is emitted as its atomic token (**A-atom**) or shattered into base
jamo singletons (**A-shat**). Predicted `Δd_acc = d_acc(A-atom) − d_acc(A-shat) ≥ 0.15` on a held-out
recombination panel built so the control sits near 0.5.

## Why

This is the only mechanism the campaign has that stands on a survivor rather than a killed premise,
and the only one whose falsifier is admissible by construction (see Falsifiers — every threshold is
checked against the expected control before freeze, the discipline `H_001` forced). It also settles
what L4b left open: `next-gate.ng.the-one-variable` — a contrast that isolates atomicity from the
alphabet, which the M-vs-C1 comparison never did.

## The one-variable contrast (the lever)

**Probe-confirmed** (`state/h003_atomicity_fixed_codec_drill_2026-07-16/probe.json`): at K=2048 all
four negators are already atomic and pairwise-disjoint by frequency alone — 안=286, 않=520, 못=381,
아니=438 — and the `(C:ㅇ, V:ㅏ)` merge does **not** exist (`ca_merge_present=false`). So atomicity
cannot be toggled through the merge table without re-cutting other words (`adm.3` violation, corrected
in `ng.forcing-the-merge-table-is-not-one-variable`). The clean lever is **post-encode span policy**:

| arm | vocab | negator-span encoding | everything else |
|---|---|---|---|
| **A-atom** | V\* | greedy merge → the atomic negator id fires | byte-identical |
| **A-shat** | V\* | merges suppressed inside the matched span → base jamo singletons | byte-identical |

- ONE shared vocabulary V\* (jamo-BPE, K=2048, v1's audited K); the atomic negator ids exist in both
  arms. In A-shat they occur 0 times (G-0 audit assertion) — untrained, never scored.
- The span policy applies to CPT corpus, drill corpus, and eval panels alike within an arm.
- Corpus delta between arms = **only** tokens inside matched negator spans (expected 3–5% of tokens,
  `?` — the audit prints the exact fraction; > 10% is a flag).
- Why A-shat is a treatment and not noise (`ng.the-collision-is-the-mechanism`): 안/않/아니 share the
  jamo prefix `['C:ㅇ','V:ㅏ']`, so shattered, the negator's pieces collide with neighbours and no
  clean slot forms — v1's own stated reason raw utf-8 scored 0.617. A-shat should reproduce the C1
  floor **without removing the codec**, isolating atomicity from the alphabet.

## The ceiling problem (why the control lands near 0.5, not 0.9)

v1's panel was saturated (control at 0.90, ceiling 0.9167 → 0.083 headroom, the trap `H_001` caught).
H_003's panel is **heuristic-neutral by construction** via depth-parity minimal pairs:

- gold bit = `pol(V) XOR (negator_count mod 2)`; depth-2 = net no-flip.
- D1 and D2 share the same template tail (`…지는 않았다`), differing only in the inner negator, so:
  **presence heuristic** ("any negator ⇒ flip") is right on D1, wrong on D2 → **0.500** on a 50/50
  panel; **template-shape heuristic** → 0.500. Both are verified closed-form by F7 before any training.
- Expected control (A-shat) 0.50–0.60; operational ceiling (A-atom) ≥ 0.90 → **~0.35 headroom**.

## Arms

Per seed: **A-atom** (the mechanism), **A-shat** (the control), **C-plc** (placebo — shatter a
frequency-matched non-negator morpheme), **C-scaf** (CPT only, no drill — leak check), **C-perm**
(drill on permuted gold — harness check), plus **C-syl** (syllable-granularity dose arm, conditional
on F1 passing). C-plc is **not optional** — it is the single control that separates "atomicity enables
composition" from "shattering any frequent morpheme degrades it generically" (see Honest Limits L1).

## Panels

- **f2′** (verdict, OOD): held-out negator **못** (switched from 아니 — 아니's free form is archaic,
  `?` operator-confirm), 4 cells fully crossed × 16 verbs, **n=192**, 50/50 per cell. Cells: D1-free,
  D1-bound, D2-free, D2-bound — **both bound AND free in the held-out slot**, which is the requirement
  `salvage.L5.no-panel-can-test-it-out-of-distribution` imposes so this drill does not inherit v1's
  blind spot. Predicate identity held constant across bound/free cells → the contrast is morphology.
- **f1′** (liveness/ceiling): same 4-cell structure, drilled negators, held-out 4th conjugation,
  n=64. F2 gate: f1′(A-atom) < 0.85 ⇒ measurement DEAD, no verdict (v1's C3 liveness role).

## Falsifiers (pre-registered, admissible — every threshold checked against expected control)

Expected: control (A-shat f2′) E=0.55; ceiling (A-atom f1′) E=0.90; n=192 → σ≈0.036, 95% CI ±0.071.

- **F1 (primary)**: `Δ = d_acc(A-atom,f2′) − d_acc(A-shat,f2′)`. SUPPORTED iff Δ ≥ 0.15 at both seeds;
  DEAD iff Δ < 0.05 at both; else PARTIAL. **Reachable**: 0.15 ≤ ceiling − control = 0.90 − 0.55 =
  0.35 ✓ (v1's dead gate was 0.083 < 0.1 ✗; this is 2.3× inside headroom). **Not-free**: Δ < 0.05
  needs only A-atom ≈ A-shat, so both answers exist.
- **F2 (liveness)**: f1′(A-atom) < 0.85 ⇒ measurement DEAD (no F1 verdict). Leak-ceiling role.
- **F3 (not-free)**: f2′(C-scaf, no drill) > 0.60 ⇒ the grid leaks, scaffolding clears it. 0.60 =
  chance + ~2.8σ, so it triggers only on a real leak.
- **F4 (negative control)**: f2′(C-perm, permuted gold) ∉ [0.40, 0.60] ⇒ harness/label leak.
- **F5 (OOD bound/free)**: given F1 passes, per-cell Δ < 0.10 in any of the 4 cells, same sign both
  seeds ⇒ verdict restricted to the passing morphology (PARTIAL). Per-cell power is the weak point
  (CI ±0.14 > 0.10 → 2-seed-sign-gated; honest limit).
- **F6 (placebo)**: `d_acc(A-atom) − d_acc(C-plc) > 0.05` ⇒ effect is generic encode-disruption, F1
  pass **VOID** by pre-registration. The most important non-primary falsifier (Honest Limits L1).
- **F7 (panel bounds, closed-form, PRE-TRAINING)**: three checks, each must equal 0.500 ± 0.02 or the
  grid is rebuilt and **nothing trains** — (a) `presence_heuristic_score` (defeated by depth parity),
  (b) `held_out_blind_score` (a drilled-only reader must not recover the held-out negator — the
  semantically correct bar), (c) surface-suffix neutrality via shared-tail pairs. Plus per-cell 50/50
  `label_balance`. **STATUS: F7 currently FAILS** — it blocked the run twice (a template leak, then a
  held_out_blind = 0.25 drilled-detection leak); the panel is being redesigned before freeze. This is
  the gate working as intended (`state/h003.../build_panels.py`, `f7_audit.json`).
- **F8 (exposure match)**: |BPB(A-atom) − BPB(A-shat)| on held-out NSMC > 0.15 ⇒ arms not
  difficulty-matched, confound flag. BPB and d_acc reported **separately, never summed** (p7).

## Cost

d=384, L=4, V=256 (~15–25M params, `?` exact at init), seq_len 512, from scratch (C2 licenses it;
the 388M clm303 ckpt has the wrong d anyway). CPT 8k + drill 2.5k steps, 2 seeds. Local MPS, ~6–8h
total, **$0**. Pre-registered escalation: only if F2 fails at seed 0 (small model can't learn the
drill) → rent 1× GPU via `hexa cloud`, rerun d=1024, <$5. v1's OMEGA showed scale-STABLE behaviour
d384→d1024, so a small-scale verdict is meaningful.

## Open Parameters (must be resolved and frozen BEFORE `frozen_at`)

Nothing marked `?` here is tunable after freeze. Enumerated so the freeze is auditable:

- the balance unit for F7's `label_balance`: it must be a cell within which BOTH gold values occur
  (the pos/neg verb split), NOT the depth cell — depth alone fixes gold, so `label_balance` keyed on
  depth returns 1.0/0.0 by construction and cannot detect leakage. Pre-registered harness call must
  key on `verb_polarity × depth`, and every such cell must be 50/50 across the verb axis.
- exact jamo strings of each matched span + printed per-form match counts (G-0 audit output)
- fraction of corpus tokens inside matched spans (flag if > 10%)
- the 16-verb inventory after the G-1 grammar audit (min 12 survivors; 못-compatibility + polarity
  each operator-judged) — the `?`-marked stems in Fable's list
- 못 match-count in NSMC ≥ 500 (else atom embedding undertrained for a non-hypothesis reason)
- C-plc's placebo morpheme: frequency within 2× of total negator-span frequency, label-correlation ≈ 0
- 아니-vs-못 held-out choice confirmed (아니 free form archaic)
- MPS it/s → wall-clock estimate

## Honest Limits

- **L1 — the placebo (F6) is load-bearing, not decorative.** The most likely convincing false
  positive: A-shat loses because shattering *any* high-frequency morpheme into shared jamo singletons
  degrades its representation generically (embedding interference), not because atomicity enables
  composition. It would replicate at both seeds and look exactly like the predicted result. Only C-plc
  catches it, and only because F6 voids the F1 pass by pre-registration rather than post-hoc judgement.
- **L2 — A-shat's unmerged jamo runs are a "neon sign".** They are distributionally anomalous, which
  could mark negators for the model. The sign is *conservative* (it would help A-shat, shrinking Δ
  toward DEAD), and C-plc carries the same anomaly — but it is a real deviation from a clean control.
- **L3 — F5 per-cell power is weak.** ±0.14 CI vs a 0.10 threshold means the bound/free verdict is
  2-seed-sign-gated, materially weaker than the F1 primary. A clean bound/free split may need more n.
- **L4 — d=384 is a bet on scale-stability.** It rests on OMEGA's measured d384→d1024 stability; if the
  effect is scale-dependent in the *other* direction (small model can't form the atomic representation
  at all), F2 catches it as a dead measurement and forces the escalation, not a false DEAD.

## Cross-Links

- **architecture**: `next-gate.*`, `salvage.L4.what-was-actually-causal`,
  `salvage.L4.atomicity-was-luck-not-method`, `salvage.L5.no-panel-can-test-it-out-of-distribution`,
  `verification.admissibility-gate`
- **v1 record**: `anima/state/nbind_curriculum/` — `morph2b.py` (codec + G-0), `gen_morphatom_s1.py`
  (grid + RENDER table), `morphatom_eval.py` (forced-choice scorer)
- **sister H**: [H_001](H_001_mech3_falsifier_vacuity.md), [H_002](H_002_bound_vs_free_negation.md)
- **harness**: `tool/anima_v4.py` — `presence_heuristic_score`, `template_heuristic_score`,
  `label_balance`, `binom_sigma`, `Falsifier`, `evaluate`
- **design seed**: `state/h003_atomicity_fixed_codec_drill_2026-07-16/` (Fable spec + probe)

## Verdict

**🔴 FALSIFIED (2026-07-16)** — atomicity of the negator token does NOT cause held-out negation
recombination. The one-variable test (encoder span policy: atomic vs shattered, same K=2048 codec,
same NSMC corpus, same d=384 L=4 model, per-seed) returns **F1 Δd_acc = A-atom − A-shat = −0.1146
(seed 0), +0.0468 (seed 1)** — both below the 0.05 DEAD floor; at seed 0 the atomic arm scores
*lower* than the shattered one. Source: `state/h003_atomicity_fixed_codec_drill_2026-07-16/train_result_full.json`
+ `verdict.json`.

The measurement is CLEAN — this is a real DEAD, not a tool artifact (verdict-integrity cleared):

| arm | seed 0 f2' (d_acc) | seed 1 f2' | falsifier | reads |
|---|---|---|---|---|
| A-atom | 0.5677 | 0.6562 | — | atomic negator token |
| A-shat | 0.6823 | 0.6094 | **F1 primary** | Δ = −0.1146 / +0.0468 → both < 0.05 ⇒ DEAD |
| C-plc | 0.6458 | 0.6406 | **F6 placebo** | gap = −0.0781 / +0.0156 (≤0.05) ⇒ clean, F1 not void-able |
| C-scaf | 0.4948 | 0.5000 | **F3 leak** | ≈0.5 both ⇒ grid does not leak |
| C-perm | 0.5052 | 0.4844 | **F4 harness** | in [0.40,0.60] both ⇒ label/harness does not leak |

- **F2 liveness = f1'(A-atom) = 0.8594 at BOTH seeds ≥ 0.85** — the model learned and the scorer
  discriminates (contrast the quarantined windower-bug run, which read 0.5 everywhere). The DEAD is a
  measured null, not a no-train artifact.
- **F6 placebo clean** — A-shat's loss is not generic embedding-interference the way L1/Honest-Limits
  feared; the placebo control sits within 0.05 of A-atom, so the F1 pass (had there been one) would not
  have been void-able. Here there is no F1 pass to void — atomicity simply carries no advantage.

**What this means.** v1's attribution (`salvage.L4.what-was-actually-causal`: "ATOMICITY of the
negator token — and nothing else") does NOT survive isolation. Under a fixed frequency-trained codec,
giving each negator its own atomic token id buys nothing on held-out negation recombination versus
shattering it into jamo singletons. Whatever carried v1's MORPH-ATOM 🟢 (d_acc 0.9083/0.9167) was
confounded with atomicity — a different codec, corpus, or curriculum — not atomicity per se. This
retires mech-3's last surviving lever: it died a fourth way, and this one is a clean write-side
measurement, not an admissibility defect (`salvage.L4.atomicity-was-luck-not-method` is now confirmed,
not merely suspected). Next direction moves off the codec axis entirely (mech-1 파서 결투 / mech-7 반사실
편집자 — the other two independent tension families). Recorded to `ARCHITECTURE.json` → `scope.stage`,
`salvage.L4.what-was-actually-causal` (falsified child), `next-gate`, and REGISTRY tier 🔴.
