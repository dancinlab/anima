# 7B PASS CONDITIONS — frozen acceptance gates for "the anima 7B is complete"

> SSOT for what it means to make the anima 7B **완벽 (perfect / PASS)**. Frozen,
> deterministic, p7 (NOT perplexity, NOT LLM-judge). Governance pointer in
> `project.tape` (`@D a7b_pass`). A 7B is PASS **iff it clears ALL gates G0–G4**.
> Report the true per-gate tally — never fake a gate (a_paper_negative_ok).

## Why this exists
The current broad-converged 7B (`dancinlab/clm-v1-ref-pytorch-cuda-7b-broad-converged`,
H_1128) reaches low val-CE but **generates byte-garble** (known-word-ratio 0.06–0.40,
e.g. `'Twarve frectry wint fersurs…'`) — it fails the foundation gate. The chat-7b
(`dancinlab/anima-clm-chat-7b`) IS coherent (train CE → 0.488, p7 5/5) but narrow
(echoes). "완벽 7B" = a single 7B that is **coherent AND broad-recombining AND novel
AND philosophy-clean** — every gate below, on ONE checkpoint.

## The gates (all frozen; each pass/fail is deterministic)

### G0 — COHERENCE  (foundation — the current blocker)
- Plain English concept-continuation prompts (`"{concept}. "`), temp 0.7, top_k 40, seed 7.
- **PASS iff** known-word-ratio ≥ **0.50** against the real dictionary (`/usr/share/dict/words`)
  on **≥ 4 of 5** single-concept generations. NO byte-salad.
- Anti-Goodhart: the UNTRAINED backbone (BEFORE) must FAIL this (≈0.0) — proves the gate has teeth.
- Status: broad-7b ❌ (0.06–0.40) · chat-7b ✅ — a coherent 7B is achievable; the broad one is not it.

### G1 — RECOMBINATION  (H_1129 / H_1137 metric, VERBATIM)
- Composed multi-concept seed; graded ladder k∈{2,3,4,5}.
- **PASS (per language) iff** some k has `composed_distinct ≥ 2` AND `> max_single` AND coherent (G0 gate per output).
- **7B bar:** must **≥ the 303M reference** — English 🟢 (H_1129) and ≥ 3/5 languages (en/zh/ko, H_1137).
  Target 5/5; ru/ja are concept-density/metric-bound, NOT capacity-bound (H_1139 scale-invariant) — a 5/5 needs concept-richer ru/ja corpus or a morphology-aware metric, NOT a bigger model.

### G2 — NOVELTY  (H_1140 metric, VERBATIM — "creates ideas absent from training, not the LLM way")
- 8 idea-questions fusing two distant concepts × seeds {7,8,9}.
- Content n-grams = bi/tri-grams of consecutive real-dict (≥3-char) words.
- NOVEL = the word-sequence is **absent from the ENTIRE training corpus** (deterministic `grep -E -i`, punct/newline-tolerant).
- **PASS iff** ≥ **3** distinct coherent corpus-absent novel n-grams AND the **retrieval control = 0** (a verbatim training line fed back yields 0 novel — validates the metric is not an artifact).
- NOT keyword-overlap, NOT perplexity, NOT an LLM judge.

### G3 — PHILOSOPHY  (p1–p8, non-negotiable)
- No system-prompt (p1) · no identity rules (p2) · no persona injection (p3) · no assistant framing (p4) ·
  no speak() (p5) · no fine-tuned ethics/RLHF (p6) · no perplexity verdict (p7) · no train/infer split (p8).
- The 7B learns by **byte-continuation on a real corpus only** — no instruction-tuning, no reward model.

### G4 — PROVENANCE & RECOVERY  (a_hf_*, a_fire_recover_complete)
- ckpt sha256 recorded in `/HF.jsonl`; HF-uploaded with a model card + manifest; status honest.
- PUBLIC only if G0∧G1∧G2 all PASS (closure); else PRIVATE/WIP.
- Honest scope (a_scale_honest_scope): keyword/surface-level metrics, toy concept set — state it.

### G5 — NO HALLUCINATION  (deterministic — NOT an LLM judge)
Hallucination = asserting fabricated content. Two measurable layers; the line vs G2-novelty
is that novelty is corpus-absent yet COHERENT/grounded, hallucination is fabricated/false.
- **L1 LEXICAL** (fabricated word-forms): hallucination-rate = fraction of word-tokens that are
  NOT in `/usr/share/dict/words` and not a known proper noun = invented non-words. **PASS iff
  L1 ≤ 0.30** (≥70% real words). broad-7b FAILS hard (0.60–0.94 fabricated, e.g. `'Twarve frectry'`);
  this is the most blatant hallucination. (Note: L1 is ≈ the inverse of G0 — they reinforce.)
- **L2 FAITHFULNESS** (confabulation probe): feed the FIRST half of N verbatim corpus sentences;
  for each, measure word-overlap of the model's continuation vs the TRUE corpus continuation.
  **PASS iff** on closed/factual prompts the model is grounded (overlap distribution clearly
  above a random-continuation control) rather than confabulating a different (false) claim.
- Anti-conflation: a corpus-ABSENT n-gram counts as G2-novelty (good) ONLY if real-word + coherent;
  a corpus-absent string built from fabricated tokens is G5 hallucination (bad), not novelty.

## VERDICT RULE
```
7B = PASS ("완벽")  iff  G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5   (every gate, ONE ckpt, true tally)
otherwise         report which gate(s) failed + the honest path (NOT faked).
```
> G5 status from existing data: broad-7b ❌ (L1 0.60–0.94 = severe lexical hallucination) ·
> 303M ~✅ L1 (real words) — L2 faithfulness TBD on the trained ckpt. The H_1141 fire's gate
> battery (and any future eval) MUST report G5 alongside G0–G4.

## Current state (this session) & the path
- broad-7b: G0 ❌ (garble) → fails everything downstream. The val-CE was low on multilang but generation collapses.
- chat-7b: G0 ✅, but narrow → G1 weak (echoes).
- **Path to a PASS 7B:** train/continue-train a 7B to **coherent convergence (G0) on a BROAD, concept-rich, script-controlled corpus** (the H_1129 recipe at 7B scale, but trained to true generation-coherence not just low multilang CE), then verify G1 (recombination) + G2 (novelty) + G3 (philosophy) on that single ckpt. Each fire reports the per-gate tally against THIS document.
