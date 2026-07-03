# H_9113 — Referential-efficacy THRESHOLD resolution: how strong is anima's emit reference, in bytes?

**tier:** 🟠 PARTIAL (per frozen PREREG bar) — but the PRIMARY DELIVERABLE (coupling-strength scalar) ✅ RESOLVED: **b50_real ≈ 3.20 bytes**. The 🟠 is caused solely by the frozen bar#2 clause "real>shuffle at EVERY t" including the ≤2-byte noise floor where dominance is structurally impossible. · **wired:** none (research verdict, external-oracle-mediated; refines H_9112).

**verdict:** 🟠 (`state/verdicts/9113_referential_threshold/H_9113.txt` verbatim). Sub-8-byte truncation sweep (K=14 fixed, near-synonym distractors) to resolve H_9112's UNRESOLVED psychometric threshold (real stayed near-ceiling 0.982). anima FROZEN, external oracle receiver (claude-fable-5). **RESULT: real 8B=1.0 · 6B=0.857 · 4B=0.786 · 3B=0.429 · 2B=0.0 · 1B=0.071; shuffle ~0 throughout → b50_real ≈ 3.20 bytes (mean-acc 0.524 vs shuffle 0.036, 14× separation).** anima's grounded emit reference is decodable by an external mind from just ~3 bytes of clue among 14 candidates = **referential efficacy EXTREMELY strong**. H_9112's near-ceiling caveat is CLOSED with a quantified scalar.

## Why 🟠 not 🟢 (c9 honest — bar NOT moved)
Frozen bar#2 required "real>shuffle at EVERY t". It fails at t=1B (real 0.071 = shuffle 0.071) and t=2B (both 0.0) — the **noise floor**: a 1-byte clue is "a" for every emit (all descriptions begin "a …"), a 2-byte clue "a " carries zero referent info, so BOTH arms collapse to chance by construction. This is the expected information-theoretic floor, not a coupling failure. In the SIGNAL regime (8→3 bytes) real DOMINATES shuffle absolutely. Bar-design note (a_break_the_wall class-a measurement-artifact): bar#2 should have scoped t≥3 (≥1 content byte); the SCALAR deliverable (bar#3, descriptive) is unaffected and is the real result. Not re-scored to green (frozen-first, p7).

## Method (frozen-first, PREREG.md)
Re-score H_9111's 14 frozen emits. K=14 (hardest), byte-truncation t∈{8,6,4,3,2,1} of the degen-tail-cleaned head, batched oracle calls (12 total). Measure = b50 (clue-byte length at 50% decode, linear interp) = coupling-strength scalar. Arms: real / shuffle (deranged concept↔emit). STDLIB harness (grep-clean), 2-regime determinism.

## Answer
How strong is anima's emit reference? **b50 ≈ 3.2 bytes** — an external mind reconstructs the intended referent from ~3 bytes of anima's grounded description (among 14 candidates). This quantifies the H_9112 GREEN and feeds §2 forward-model (DIVERGENCE_fable.md §2): 3.2 bytes is the baseline byte-threshold a learned emit-policy would try to LOWER (make anima's emit decodable from even fewer bytes). Still DIRECTIONAL-on-external-oracle; engine-native receiver / receiver-panel = tier-lift follow-on (H_9112 re-open ②).

## Evidence (`state/9113_referential_threshold/`)
`PREREG.md` · `threshold_rescore.py` (STDLIB, grep-clean) · `rescore_fixture.jsonl` (raw picks) · `RESULT.md` · `../9111_llm_interlocutor/emits.tsv` (14).
