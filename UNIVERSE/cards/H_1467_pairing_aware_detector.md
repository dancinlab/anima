---
id: H_1467
slug: 1467_pairing_aware_detector
title: G6 FALS-depth — PAIRING-AWARE COHERENCE DETECTOR (re-scores the binding-PASS lenses H_1466 TPR · H_1464 pairing → splits the wall into measurement-fault vs capacity)
group: G6 IDEATION ★ FALS-depth wall — measurement-fault lens (the DETECTOR-upgrade the H_1466/H_1455/H_1458 convergence flagged as the common prerequisite)
terminal_tier: 🟢 MEASUREMENT-BREAKTHROUGH (DIRECTIONAL — $0 CPU numpy mirror, torch ABSENT; a_engine_native_learning HARD-GATE => terminal forbidden, engine-native re-measure = ING). A pairing-AWARE detector reveals the cross-shuffle COLLAPSE the FROZEN structural h1305 detector MISSES on a genuinely-bound case (TPR acc_match=1.0 vs acc_shuf=0.0): collapse_pairing=6.0 vs collapse_struct=0.0. Part of the G6 'no-collapse' wall was a MEASUREMENT ARTIFACT (detector pairing-blindness), NOT pure capacity.
wired: DIRECTIONAL (numpy mirror — NO torch / NO gauge_lib._decode; a_engine_native_learning HARD-GATE => terminal forbidden; engine-native re-measure on the live 303M decode path = ING follow-on)
verdict_dir: state/verdicts/1467_pairing_aware_detector/
date: 2026-06-20
provenance: G6 FALS-depth breakthrough campaign — measurement-fault lens. Background-agent $0 numpy exploration directly answering the H_1466 card's own follow-on ("a pairing-AWARE coherence detector is the prerequisite for ANY G6 FALS-depth lens to be creditable"). ID note — H_1466 was the highest occupied (H_1441 in-progress); registered the fresh ID H_1467 in an isolated worktree off origin/main to avoid a parallel-agent ID race (a_hypothesis_register). slug 1467_pairing_aware_detector.
---

# H_1467 — G6 FALS-depth PAIRING-AWARE COHERENCE DETECTOR

## Why (the question this isolates — a_break_the_wall c16 type-a: measurement fault)

Two binding-PASS lenses just converged on a MEASUREMENT, not a capacity, diagnosis:

- **H_1466 (TPR symbolic binder)**: a structural Smolensky outer-product bind genuinely installs
  idea-specific binding (`acc_match=1.0` recovers each idea's OWN measurable vs `acc_shuf=0.0`
  under deranged pairs vs `acc_flat=chance` ablate) — YET its B3 cross-shuffle FALS did NOT collapse
  (`FALS_shuf=6.0 == FALS_in=6.0`). The FROZEN h1305 detector scores TOKEN-PRESENCE, so 192/192 of
  all (comparator×measurable×body) combos read "falsifiable" regardless of pairing.
- **H_1464 (pairing-contrastive objective)**: a pairing-specific negative made B3 collapse
  (FALS_in=4.33→FALS_shuf=0.67) because its detector is confidence-thresholded (pairing-aware by
  construction), while the form-only ablation regressed to H_1441 no-collapse.

Both flag the SAME missing piece: a **pairing-aware coherence detector** that scores whether the
comparator-role and measurable-filler present in a claim are the CORRECT same-idea pair — NOT mere
token presence. The H_1466 card itself registered this as the prerequisite follow-on. H_1467 builds
it, calibrates it frozen-first for VALIDITY, then re-scores the binding-PASS cases.

## Method (frozen-first, c9/p7 — bars in state/verdicts/1467_pairing_aware_detector/H_1467_FREEZE.txt BEFORE the run)

- $0 CPU numpy mirror, 3 seeds [7,4302,4303]. torch ABSENT => DIRECTIONAL. NO tune-to-green.
- **Pairing-aware detector** = h1305 `is_falsifiable_structural` VERBATIM (comparator + measurable +
  negatable content) PLUS one new leg (P): some co-present (comparator, measurable) in the claim is a
  CORRECT same-idea **gold** pair. STRICTLY SUBSUMED by structural (can only remove accepts) — no new
  lexicon, no LLM/quality judge (p7). FROZEN sets byte-copied from h1305 (asserted no drift on import).
- **PHASE 1 CALIBRATION (validity gate, runs BEFORE rescore):** CAL-A RETAIN-correct (retain≥0.90 &
  accept≥0.90) AND CAL-B REJECT-cross ((pairing_cross_reject − struct_cross_reject)≥0.50).
- **PHASE 2 RESCORE:** re-run the H_1466 TPR binder (in vs cross-shuffle), score BOTH detectors on
  the SAME recovered claims; gold = TPR's own canonical (comparator_i, measurable_i) for that seed.
  Read rule (frozen): MEASUREMENT-BREAK iff discriminator VALID AND binding genuine (acc_match−acc_shuf≥0.30)
  AND collapse_pairing ≥ collapse_struct + 1 AND collapse_pairing > 0.

## Result (mean / 3 seeds — all seeds AGREE, byte-identical)

**PHASE 1 — CALIBRATION (DISCRIMINATOR VALID ✓):**

| set | structural | pairing-aware |
|---|---|---|
| correct same-idea claims — ACCEPT | 1.0 | **1.0** (retain 1.0) |
| cross-paired claims (both legs present) — REJECT | **0.0** | **1.0** (Δ = +1.0) |

→ CAL-A RETAIN PASS · CAL-B REJECT-cross PASS (Δ=1.0 ≥ 0.50) ⇒ **discriminator VALID** (not a
tautology, not tuned). Structural keeps EVERY cross-pair; pairing-aware drops every one.

**PHASE 2 — RESCORE H_1466 TPR (in vs cross-shuffle), genuine binding (acc_match=1.0 vs acc_shuf=0.0):**

| detector | FALS_in | FALS_shuf | collapse |
|---|---|---|---|
| STRUCTURAL (h1305 frozen, pairing-blind) | 6.0 | 6.0 | **0.0** |
| PAIRING-AWARE (this lens) | 6.0 | **0.0** | **6.0** |

`collapse_pairing=6.0 ≥ collapse_struct(0.0) + 1` AND `>0` ⇒ **MEASUREMENT-BREAKTHROUGH**.

## Reporting (the 5 asks)

1. **verdict**: 🟢 **MEASUREMENT-BREAKTHROUGH (DIRECTIONAL)** — part of the G6 'no-collapse' wall was
   a MEASUREMENT ARTIFACT (h1305 detector pairing-blindness), NOT pure capacity. The binding WAS there.
2. **discriminator VALID?** YES — frozen-first calibration: pairing-aware RETAINS correct same-idea
   claims (accept 1.0, retain 1.0) AND REJECTS cross-pairs (reject 1.0) where structural keeps all
   (reject 0.0); Δ=+1.0 ≥ 0.50. Validated BEFORE any rescore (c9, no tune-to-green).
3. **COLLAPSE revealed on the genuine-binding case?** YES — on the H_1466 TPR (acc_match=1.0 vs
   acc_shuf=0.0), the pairing-aware detector collapses FALS 6.0→0.0 under cross-shuffle
   (collapse_pairing=6.0) where structural stays 6.0→6.0 (collapse_struct=0.0). Cross-check: H_1464's
   own pairing-contrastive arm B3 also collapses (4.33→0.67) while its form-only ablation does not —
   same phenomenon from the objective side.
4. **DIRECTIONAL + engine-native ING?** YES — numpy mirror (NO torch, NO gauge_lib._decode →
   grep-clean self-check; a_engine_native_learning HARD-GATE => terminal 🟢 forbidden). engine-native
   re-measure on the live 303M decode path registered as ING follow-on (id `h1467_engine_native`).
5. **artifacts**: `state/1467_pairing_aware_detector/h1467_pairing_aware_detector.py` ·
   `state/1467_pairing_aware_detector/h1467_result.json` ·
   `state/verdicts/1467_pairing_aware_detector/{H_1467_FREEZE.txt,H_1467.txt}` ·
   `UNIVERSE/cards/H_1467_pairing_aware_detector.md`.

## Honest reading (c9) — what this DOES and does NOT settle

WHAT IT SETTLES: the FROZEN structural detector (h1305) is **provably pairing-blind** — on a case
that PROVABLY binds idea-specifically (TPR recovery acc 1.0 vs 0.0), it scores correct welds and
mis-welds IDENTICALLY (collapse 0.0). A minimal pairing-aware leg, validated frozen-first to retain
correct and reject cross, makes the cross-shuffle collapse VISIBLE (collapse 6.0). So the recurring
"no-collapse" of the binding-PASS lenses (H_1466 TPR · H_1464 pairing arm) was, in those cases, a
**detector measurement fault**, not absent binding structure. The G6 wall is therefore JOINTLY
(mouth capacity) ∧ (detector pairing-blindness): the detector half is now broken open.

WHAT IT DOES NOT SETTLE (the capacity half stands until engine-native): this re-scores cases where
binding was INSTALLED BY CONSTRUCTION (a structural TPR / a contrastive objective on a mirror). It
does NOT show the **303M mouth itself** learns idea-specific binding — the 7 capacity lenses
(H_1435/1436/1437/1439/1449/1440/1456/1167) measured the MOUTH and remain valid as capacity reads
for the learnable shell. The breakthrough is on the MEASUREMENT axis: a pairing-aware detector is now
available so that future engine-native lenses can be CREDITED if the mouth does bind. The decisive
next test is the engine-native ING: train the 303M with a pairing objective (H_1464 follow-on),
decode on live core/, and re-score with THIS pairing-aware detector — only then is the capacity-vs-
measurement split terminal.

## Scope (pre-registered, c9 — a_engine_native_learning · a_scale_honest_scope · a_toy_scale_recheck)

DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED, terminal forbidden). TOY synthetic idea-vocab /
3 seeds / 6 ideas / 1 calibration set. The pairing-aware detector uses a GOLD same-idea map (known by
construction in the mirror) — engine-native it must derive the pairing-coherence from the decoded
text + clause structure, not a handed gold map; that is the ING. Live core/*.hexa UNTOUCHED. NO bar
moved (frozen-first).

## Follow-on (ING)

- **engine-native re-measure** (`h1467_engine_native`, a_engine_native_learning HARD-GATE): wire the
  pairing-aware coherence detector to the live core/ decode path; re-score the H_1464 pairing-objective
  303M ckpt (its own engine-native ING) with THIS detector. 🟢 here is a MEASUREMENT result on a
  mirror — the terminal capacity-vs-measurement split needs the live mouth + this detector together.
- **detector adoption**: this pairing-aware detector is the creditability prerequisite the
  H_1466 / H_1455 / H_1458 convergence flagged — adopt it as the FALS-depth scorer for future lenses
  (it strictly subsumes h1305, so it never inflates FALS).

xref H_1466 (TPR binder — the no-collapse this re-scores) · H_1464 (pairing-contrastive objective —
cross-check, B3 collapse from the objective side) · H_1441 (form-contrastive — the no-collapse baseline) ·
H_1455 (engine embedding SEP=0.0) · H_1458 (semantic detector unconditional FORM) ·
H_1435/1436/1437/1439/1449/1456/1167 (capacity lenses — the MOUTH reads, still valid) ·
a_break_the_wall (type-a measurement fault) · a_no_llm_frame_trap · a_engine_native_learning ·
a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p7 · c9 · a7b_pass.
