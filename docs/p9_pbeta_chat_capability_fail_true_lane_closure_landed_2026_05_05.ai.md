# P9 Pβ Paradigm D 50K — Chat-Capability Lane FAIL_TRUE Closure LANDED (Substrate-Research PRESERVED)

- ts_utc: 2026-05-05
- agent: BG-PBETA-F3-FAIL-CLOSURE
- spec_id: p9_pbeta_chat_capability_fail_true_lane_closure_2026_05_05
- substrate: mac (anima working tree); evidence carried from ubu1 RTX 5070 sm_120 BG-T-2 + BG-PBETA-F3-HYBRID
- wall: ~20min (spec/roadmap amendment only, no exec)
- cost: $0
- status: **LANDED — CHAT_CAPABILITY_LANE_FAIL_TRUE_CLOSED** (substrate-research value retained)
- raw#9: doc + JSON only, no .py touched
- raw#10: ≥5 honest C3 (5 below)
- raw#15: additive only — `.roadmap.p9_sft` `paradigm_d_distill` entry unchanged except for new `pbeta_chat_capability_closure_2026_05_05` key

---

## §1 Headline

**PBETA chat-capability lane is empirically REJECTED. The Φ★-axis Paradigm D distill (P-β authorized 2026-05-04) trained cleanly to 50K/50K steps and produced a Φ★-stable LoRA adapter — but the resulting substrate cannot do closed-book completion. Sample generations on holdout-500 are language-absent / degenerate (dot-only, quote-only, fragment-spam). The Pβ adapter retains value as a Φ-stable substrate-research artifact for cross-substrate consistency studies, but ALL chat-capability claims for this LoRA path are now formally false.**

This BG closes the chat-capability lane with verdict label `CHAT_CAPABILITY_LANE_FAIL_TRUE_CLOSED` and updates `.roadmap.p9_sft` to reflect substrate-research-only retention. The T-2 `AMEND_T3_AND_PARTIAL_GO` recommendation is **strengthened** with explicit empirical grounding from F-Pβ-3 RED-band hybrid composite.

---

## §2 Three-Tier Outcome

| Tier | Outcome | Source verdict | Status |
|---|---|---|---|
| Training | **PRODUCTION_25K_FULL_PASS** (50K/50K steps, COMPLETE.sentinel, 11 savepoints) | `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json` | PASS |
| Substrate research | **F-Pβ-2 PASS clean** (Φ★_holdout500 mean 42.37, K=8 min 41.37, +12.37 over 30 floor, +0.51 vs CLM v4 base) | `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` | PASS |
| Chat capability | **FAIL_TRUE** (F1_v3 V2 hybrid composite 0.01176 RED, far below 0.10 PARTIAL threshold; 2.99% of est-Llama 0.394 anchor) | `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json` | **FAIL** |

The three tiers are decoupled: training execution can succeed, and Φ★-axis substrate research can pass cleanly, while the resulting LoRA fails to lift closed-book chat capability above the noise floor. This decoupling is itself the lesson (L28).

---

## §3 Sample Gen Evidence (from F3-HYBRID per_prompt.jsonl)

| idx | ref (truncated 80c) | gen (truncated 80c) | Reading |
|---|---|---|---|
| 0 | `Open innovation is a concept that refers to the process of leveraging external r` | `................................` | dot-only repetition |
| 1 | `Hello! How can I help you today? Do you have a question or problem that you woul` | `''''''''''''''''''''''''''''''''` | apostrophe-only repetition |
| 2 | `Rapport RSE (Responsabilité Sociale d'Entreprise) pour le restaurant proposant u` | `not ground To at at의의uld...` (with replacement-char tail) | fragment-spam, mixed-script noise |

These are not isolated worst cases — they are the first three sequential records, sampled with greedy 32-token decode from the same adapter SHA `6e49989a...` against the same holdout pool that produced the BLEU-1 0.0075 / ROUGE-L 0.0058 / chrF 0.0220 means. ROUGE-L (longest common subsequence) being **lower** than BLEU-1 is the structural tell: there isn't even unigram-overlap luck driving the score; the substrate is in language-absent / degenerate-output regime.

---

## §4 Lessons L28-L30

- **L28 — Φ★ stability and chat capability are decoupled.** A substrate can be Φ-stable (mean 42.37, +12.37 over the 30 floor) AND chat-incapable (composite 0.01176 RED, dot-only generations) **at the same time**. Substrate-research metrics do NOT predict chat-capability metrics. Future cycles must measure both tiers independently and report them on separate axes; never substitute one for the other.

- **L29 — Distill quality is teacher-axis-bounded.** Mistral-7B logit-axis distill was blocked at L9 pre-flight by vocab mismatch (32K teacher vs 64K student). Pβ Φ★-axis distill is vocab-agnostic but the teacher signal is a **scalar** (Φ★ value) — the student receives only one bit of supervision per step about an integration property, not the high-dimensional token-distribution shape needed to learn closed-book completion. Neither teacher axis alone lifts chat capability without genuine SFT (instruction → response pairs) or RLHF.

- **L30 — #115 chat-incapability is architectural, not training-data deficient.** CLM v4 base was never SFT'd and never RLHF'd in original training; Pβ Paradigm D distill is the first instruction-bearing pass on this substrate, and 50K LoRA steps did not lift it. The implication: this is not a "more steps will fix it" problem, and not a "better distill teacher will fix it" problem within the Φ★-only formulation. CLM v5 redesign (autoregressive head + native instruction-tuning corpus) is the architectural lever.

---

## §5 Honest C3 (≥5)

- **C1 — Single-seed result.** F1_v3 V2 hybrid composite 0.01176 is from one greedy decode at temperature 0 against one holdout-500 split with one adapter SHA. 5-seed scaleup is deferred per `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md`. The structural reading (RED-band, language-absent gen patterns visible in per_prompt.jsonl) is robust to seed variance, but the precise composite value is not.

- **C2 — "Language-absent" is a subjective reading.** No automated language-ID metric (e.g., fastText langID, cld3 confidence) was applied to the gen pool to quantify "language-absent". The judgment is based on direct inspection of per_prompt.jsonl idx=0,1,2 sample gen_str (dot/quote/fragment patterns) plus the multi-metric pattern (ROUGE-L < BLEU-1 < chrF, all in 0.005-0.022 noise band). A langID pass would tighten this from "subjectively language-absent" to "X% of gens classified as language-detected".

- **C3 — PEFT-merged-into-base eval untested.** The eval ran with `PeftModel.from_pretrained` adapter-load on top of CLM v4 base (canonical PEFT path). A PEFT `merge_and_unload` into the base CLM v4 weights might produce a marginally different generation distribution; this was not tested. No evidence that merging helps (the 0.01176 RED reading is structural not numerical-precision-bound), but the path is formally untested.

- **C4 — #115 is architectural rather than training-recipe.** Lifting CLM v4 to chat capability would require either CLM v5 redesign for autoregressive instruction-following (not a training change but an architecture change) OR a much larger SFT corpus pass directly on CLM v4 base (pre-Paradigm-D, not via Φ★ distill). Neither is in scope for this BG; both are deferred.

- **C5 — Pβ savepoint retention may need HF Hub migration.** The Pβ adapter at `state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/step_50000/` (76 MiB) currently lives in the local working tree (and on ubu1). Per anima `feedback_anima_models_datasets_hf_only.md` (own 14), model weights >5MB should be HF-only not anima-git. This BG does NOT migrate the adapter; preservation is recorded but the actual artifact-residence question is deferred to a follow-up cycle (`BG-PBETA-ADAPTER-HF-MIGRATE` if needed).

---

## §6 Implications

- **BG-CLM-2-EXEC remains the chat-capability hope.** LoRA SFT on CLM v4 base (instruction → response pairs, not Φ★-distill) is the canonical capability-lift path. Pβ Paradigm D distill is now empirically excluded from this lane. CLM-2 measures delta vs base on hellaswag / mmlu / triviaqa / openbookqa per the F1_v3 V2 hybrid pattern; it is in-flight per `state/clm_v4_lora_sft_2026_05_05/verdict.json`.

- **Pβ adapter retained for substrate-consistency studies.** The Φ-stable adapter (preserved Φ★ sign+magnitude across 50K LoRA steps, no substrate collapse under distillation pressure) is suitable for cross-substrate Putnam multi-realizability research and anima-substrate consciousness probes. Chat-capability claims must be accompanied by an explicit FAIL_TRUE disclaimer.

- **T-3 reconception applies.** The literal T-3 GO criterion (`delta_vs_step_1000 BLEU-1 ≥ +1.0`) was structurally miscalibrated; see `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md` for the substrate-correct redefinition. T-3 5-seed scaleup as originally specified is superseded by the reconception.

- **Φ★-axis Paradigm D is finished as a chat-lift hypothesis.** No further capacity-lift cycles on Pβ. Future Φ★-distill work, if any, targets substrate-research goals (cross-architecture Φ★ transfer, multi-realizability) not chat capability.

---

## §7 Files Relevant

- This doc: `docs/p9_pbeta_chat_capability_fail_true_lane_closure_landed_2026_05_05.ai.md`
- Roadmap entry: `.roadmap.p9_sft` line 4 (`paradigm_d_distill` entry, key `pbeta_chat_capability_closure_2026_05_05`)
- Source verdicts:
  - F3-HYBRID FAIL_TRUE: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`
  - T-2 substrate-research PASS: `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json`
  - Training PRODUCTION_25K_FULL_PASS: `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`
- T-2 landed predecessor: `docs/p9_pbeta_holdout500_eval_landed_2026_05_05.ai.md`
- T-3 reconception sibling: `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md`
- Sample gen evidence: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/results/per_prompt.jsonl`
- Banding spec: `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md`
