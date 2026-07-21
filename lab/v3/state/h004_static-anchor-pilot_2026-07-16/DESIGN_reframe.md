# F1 reframing analysis — verbatim Fable 5 (seed of record)

- job fable-mrmmrpsm · claude-fable-5 · 2026-07-16 · triggered by the H_004 $0 proxy defect

---

All sources read, and I re-verified both structural claims independently plus ran the feasibility math for a fix. One of the two verification claims needed correction, and the correction matters for the fix design. Findings below.

---

## Verification first (adversarial re-check of the proxy's own claims)

- **Claim 2 (last-token separability): CONFIRMED and quantified.** A last-token Bayes lookup (fit on 40k phase-2 train lines, frozen codec) scores **1535/1536 = 0.9993** on the exact eval. 12 neg last-token types vs 62 plain, overlap 1. The frozen arm's eval is solvable by a positional unigram.
- **Claim 1 (27/27 fragments NEG-exclusive): OVERSTATED.** Checked against full plain **bodies** (stems included, 5000 rendered + all pos items) instead of plain affixes only: **34/36 affix-span fragment types also occur in plain material; only 2 are type-exclusive.** The leak is not type-exclusivity of fragments — it is **positional**: the token in body-final position is nearly class-disjoint. This changes what the fix must target (the conditional distribution of the final token, not just type sharing).
- **Second shortcut found: body length.** A length-only lookup scores **0.5716** — small, but not against a 0.20 kill line. Needs its own guard.
- The Δ_proxy **number** (−0.048) is decorative anyway: oracle_202 has F1 = 0.859 < the 0.90 gate (VOID under P-4 logic) and oracle seed spread is 0.14 (P-6 fires). The structural audits, not the training runs, are the evidence — and they are deterministic and scale-independent. **The rig-defect conclusion stands.**

## Q1 — yes, F1 is reframed, and more sharply than "class-non-sharing"

Correct, with one refinement. The lever is not "atomic token" and not even "class-exclusive fragment types" (mostly shared, per above). It is: **the codec sets the ORDER of the statistic needed to read the class.** Raw utf-8 (C1 = 0.617) demands binding an ~18-byte sequence with every unit shared everywhere — a high-order statistic. The current frozen codec concentrates class into an order-1 feature (final-token identity) — trivial. An oracle/atomic codec is the limiting case: order-1 by construction. Atomicity is a special case of **low-order class exposure**, and the proxy shows a static codec can supply it accidentally.

F1 restated: *the codec's causal contribution is compressing the credit-assignment span between form and consequence; refit is the organ that maintains that compression under drift.* The identity framing ("codec-is-the-self" = the self is what the codec dedicates representation to) survives verbally — but its measured support is now thinner.

`l4-morph-atom-slot-not-address` is **weakened, not killed**: CEMENT C2 deleted the held-out *stem* and still scored 0.917. Under lookup, the decision never consults the stem at all — stem-deletion invariance is *predicted* by the shortcut, so C2 no longer isolates "slot" compositionality. It survives only as "the class unit needn't be pretrained-addressed." Worse, held-out-stem success in *every* arm of the record is now explainable as stem-irrelevance rather than recombination.

## Q2 — fixable for the frozen arm, verified feasible; but the residual contrast is order-1 vs order-2

**Construction (donor pairs):** novel NEG allomorph = concatenation of two 1-syllable **carried PLAIN** affixes, `novel[i] = a⟨2i⟩‖a⟨2i+1⟩`. Verified against the real spec/codec:

- Inventory: **27** one-syllable carried plains exist; 24 distinct donors for 12 pairs is tight but available (fallback: reuse ≤2× with per-donor balance correction).
- **688/702** ordered pairs are junction-clean in isolation, **0/702** accidentally fuse. Structural guarantee: frozen can never atomize the whole — no `(a_i, a_j)` merge exists because the pair never occurs adjacent in phase 1 (one affix per body). The ≥6-jamo length hack becomes unnecessary; deficit 1.0 is guaranteed, not sampled.
- In-context, 30/50 stems straddle the stem→affix junction — acceptable (plain bodies straddle identically) but each pair must pass a per-context audit.
- **Frequency balance is mandatory:** at NOVEL_NEG_SHARE_P2 = 0.80, P(NEG | last = donor) ≈ **0.762** — the lookup survives as a probabilistic one. Fix: boost the 24 donors' plain-usage mass ×3.20 (→ 3.33%/donor, consuming 0.80 of phase-2 plain mass; the other 24 plains keep ~0.83% each). Keeps oracle fusability (novel-form absolute frequency unchanged) while flattening P(NEG | final token) to ~0.5.

**Pre-registered $0 guard battery** (deterministic, extends `audit.py`; any failure → do not fire):
G-A last-token Bayes lookup on eval ≤ 0.55 · G-B length-only lookup ≤ 0.55 (knob: reweight 2-syl plain usage to match length distributions) · G-C minimal-order sweep: order-k token classifiers, require k=1 fails, **report the k=2 ceiling verbatim** · G-D `atomicity_audit` frozen 0/12, oracle 12/12 · G-E existing leak/co-occurrence scans.

**The honest limit:** BPE does *not* inevitably recover an exclusive fragment (frozen tables can't grow), so the fix is real — but the whole form is necessarily class-exclusive at *some* order. The fix pushes the frozen arm's cheap path from order-1 to order-2 (bigram `a_i·a_j` vs `stem-tail·a_j`), and no construction pushes much further without breaking oracle fusability. **The repaired pilot can only ever measure "atomicity beyond bigram-binding" — and one attention head does bigrams.** That is a finding about the approach, and it drives Q3/Q5.

## Q3 — keep contrast (a), with the proxy's gating logic inverted

Recommend **(a)**: oracle vs fixed-frozen, guards G-A..E, kill line 0.20 unchanged. It is the corrected version of the pre-registered question and still upper-bounds refit. But re-scope two things:

1. **What Δ_pilot now means:** "value of atomic exposure over order-2 binding at 4.9M," not "atomicity vs nothing."
2. **The proxy's asymmetry flips.** Re-run `run_proxy.py` on the fixed generator first ($0, ~1 min) — but a *positive* Δ_proxy no longer de-risks anything: a ctx-12 numpy LM is exactly the model class too weak to bind bigrams, so it overstates atomicity's value. The fixed proxy can only **kill** (Δ_proxy ≈ 0 with a weak model ⇒ transformer Δ certainly ≈ 0 ⇒ skip even the MPS run), never license.

Option (c) applies only to interpretation, not machinery: the pilot as frozen (current genspec `fbcf0c8…`) is INVALID-by-precheck and needs an H_003-style REPAIR amendment — new genspec hash, guards added to the falsifier battery, P2 prediction revised downward. Not a silent edit.

## Q4 — yes, MORPH-ATOM is mislabeled in the SSOT

M = 0.908 vs C1 = 0.617 (Δ = +0.291, replicated) stands as a measurement. What it established: **codec segmentation that concentrates class into a low-order positional feature is causal for the held-out flip.** What it did *not* establish: that single-token atomicity is the operative property — no arm in the record ever contrasted "atomic" against "fragmented-but-low-order," and the proxy shows the latter suffices. C1 failed for absence of any low-order feature, not absence of atomicity. Relabel `l4-lens-b-morph-atom` roles accordingly ("morpheme atomicity" → "class-dedicated low-order exposure; atomicity un-isolated special case"), demote `slot-not-address` per Q1, and note that "held-out recombination" was never cleanly separated from stem-irrelevant lookup. F1-as-codec-is-the-self survives as a *mechanism-class* claim (codec allocation is causal); its atomicity instantiation does not.

## Q5 — F1-first is weakened; let the pre-registered kill do the re-ranking, at $0

Honest re-derivation: the chain that put F1 first (`decision-attributability`) was already superseded; the pilot was its repair; the proxy now shows (i) the repair's control was invalid, and (ii) once valid, the frozen arm faces only an order-2 task, so the prior on Δ_pilot(fixed) should be revised **down** — TWIN-REFUSED is now the expected outcome `?`. But the expectation is not the measurement, and the measurement costs $0–$2: fix the generator (Q2), re-run the proxy under the inverted gating (kill-only), and if it survives, the overnight MPS pilot. If Δ ≈ 0 lands, report it as the campaign result it is: **"a static codec's accidental fragment statistics already deliver the write-lever's receptive value; a refit organ buys nothing here"** — which per `rig-sequence-h004-kills` forces a campaign re-decision (F1's theatre moves to generation / long-range credit / continual-training interference, or F1 yields first place), not a silent switch. What the 55-second run refuted is not F1's mechanism class — it is the belief that the record had ever isolated **atomicity** as the lever. Say that in the SSOT plainly.