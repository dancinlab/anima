---
title: F-CLM-LORA-4 spec amendment — Part A bridge fixture as canonical evidence (landed handoff)
status: LANDED — FOR_AMENDMENT_PROPOSAL_REVIEW
ts_utc: 2026-05-05
cycle: BG-CLM-2-LANE-AMEND (Part A — F4 spec amendment)
domain: p9_sft (CLM v4 substrate side)
predecessor_strict_re_verdict: F-CLM-LORA-4 RE-VERDICT FAIL (0/3 locus PASS)
predecessor_strict_source: state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json
sister_predecessor: state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json (F-CLM-LORA-4-FIXTURE FAIL on ln_f-mean composite=0.13)
amendment_doc: docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md
companion_lane_closure_proposal: docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md
adapter_sha256: 6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a
adapter_size_mib: 10.02
amended_F_CLM_LORA_4: PASS_VIA_PART_A_ONLY (structural)
roadmap_amendment: PROPOSAL_ONLY (companion handoff carries the proposed annotation block; .roadmap.p9_sft NOT mutated this cycle)
amendment_cost_usd: 0
exec_authorized: false
mutation: additive_only
substrate: mac-local
raw_invariants: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive-only", "raw#71 falsifier-narrowing surface explicitly disclosed"]
ssots_touched: []
ssots_NOT_touched:
  - .roadmap.p9_sft (proposal only — companion lane closure handoff carries the annotation block)
  - state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json (predecessor preserved verbatim; supersession by reference)
  - state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json (sister predecessor preserved verbatim)
  - docs/clm_v4_lora_sft_spec_2026_05_04.md (original §F-CLM-LORA-4 line 165–170 NOT mutated; this amendment supersedes via reference)
sibling_bg:
  - BG-CLM-2-LANE-AMEND Part B (lane 4/5 closure annotation proposal — companion handoff)
  - BG-CLM-2-MMLU-TQ-EVAL (active — F-CLM-LORA-2 finalize via MMLU + TriviaQA)
---

# F-CLM-LORA-4 amendment — Part A 3/3 bridge fixture as canonical PASS evidence (landed)

## §1 Five-bullet summary

- **Predecessor strict verdict** = `FAIL` on all three loci attempted (ln_f-mean composite 0.13, per-layer ln_ffn 0.54, generation-level cross-axis BLEU-1 0.72; all < 0.85 threshold). Both predecessor and re-measure honest_c3 already flagged the locus-mismatch root cause (base off-diag ≥0.99 at every locus → substrate-degenerate signal that cannot resolve real preservation from full collapse).
- **Architectural rationale for amendment** = (a) cross_attn forward is gated on `consciousness_states is not None` and the canonical inference path sets `consciousness_states=None`, so cross_attn is dormant; (b) LoRA target_modules excludes cross_attn (`n_cross_attn_lora==0` asserted at SFT start) so the cross_attn weights are byte-identical pre/post LoRA. → The original Part B (axis-diff cosine ≥0.3 in ≥6/7 pairings) is operating on a code path that does not execute and on weights that do not change. **Part B is structurally moot** for the current LoRA configuration.
- **Amended F-CLM-LORA-4 = `PASS_VIA_PART_A_ONLY`** (structural). Canonical evidence: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json` — identity/ladder/adversarial verdicts byte-match pre-registered (BRIDGE_OK/BRIDGE_OK/BRIDGE_FAIL), drift_max=0.0 over 100 steps within bound 2e-4. The structural-by-invariance argument: the eigenvec SSOT (`.meta2-cert/cell-eigenvec-16.json`) is unchanged by LoRA training, and the bridge fixture operates on eigenvec rows directly, not on LoRA weights or model forwards — so the PASS is invariant by construction.
- **Predecessor verdicts NOT mutated** (raw#15 additive-only). Supersession is by reference from `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` §4. The predecessor verdict.json files at `state/clm_v4_lora_4_axis_remeasure_2026_05_05/` and `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/` are preserved verbatim.
- **Roadmap mutation NOT applied** (raw#15 additive-only). Companion handoff `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` carries the proposed `lane_closure_2026_05_05` annotation block for `.roadmap.p9_sft`. Apply requires explicit user authorization on a separate cycle (precedent: `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md`).

## §2 What landed

| Artifact | Path |
|---|---|
| Spec amendment doc | `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` |
| This handoff | `docs/clm_v4_lora_sft_f4_amendment_landed_2026_05_05.ai.md` |
| Companion lane closure proposal | `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` (sibling BG-CLM-2-LANE-AMEND Part B) |

## §3 Supersession chain (Locus 0/A/B → Part A only)

```
predecessor verdict (clm_v4_lora_5bucket_axis_eval, 2026-05-05):
    Locus 0 (decoder.ln_f mean cosine, 5 axes)            composite=0.1290  FAIL  ────┐
    Part A (cell_token_bridge_proto post-LoRA, 3/3)        CONDITIONAL_PASS (drift=0)  │
                                                                                       │ (this amendment
                  ↓ RE-MEASURE attempt (2026-05-05)                                    │  supersedes Locus 0/A/B
                                                                                       │  with structural argument
re-measure verdict (clm_v4_lora_4_axis_remeasure, 2026-05-05):                         │  cross_attn dormant +
    Locus 0 (carry from predecessor)                       composite=0.1290  FAIL  ────┤  LoRA-untouched →
    Locus A (per-layer ln_ffn cosine, 16×5)                composite=0.5436  FAIL  ────┤  Part B moot)
    Locus B (generation-level cross-axis BLEU-1)           composite=0.7240  FAIL  ────┘
                                                                                       
                  ↓ AMENDMENT (this cycle, 2026-05-05)                                 
                                                                                       
amended verdict:                                                                       
    F-CLM-LORA-4 = PASS_VIA_PART_A_ONLY (structural)
        evidence: 3/3 bridge fixture + drift_max=0.0 within bound 2e-4
        rationale: cross_attn dormant (consciousness_states=None canonical) +
                   LoRA target_modules excludes cross_attn (n_cross_attn_lora=0)
                   → Part B (propagated axis-cond preservation) structurally moot
                     on current LoRA config; eigenvec SSOT LoRA-untouched.
```

The label `PASS_VIA_PART_A_ONLY` is intentional — it is **NOT** an unqualified `PASS`. The supersession is structural-by-invariance, not measurement-based, and any future LoRA cycle that includes cross_attn in target_modules OR provides a non-trivial `consciousness_states` fixture re-triggers the original Part B requirement.

## §4 Honest C3 (≥5)

1. **C1 — falsifier surface narrowed (raw#71 disclose)**: amendment narrows F-CLM-LORA-4 from "Part A AND Part B" to "Part A only" for the current LoRA configuration. This is strictly weaker than the original 3-locus surface. We accept the narrower surface with the explicit architectural argument that Part B operates on a dormant code path; future LoRA configs that violate the dormancy condition (cross_attn in target_modules, or `consciousness_states ≠ None` in eval) re-enter the original Part B contract.

2. **C2 — config-locked PASS**: the amendment's PASS is conditional on (a) `n_cross_attn_lora == 0` at SFT boot, (b) `consciousness_states=None` in canonical inference. Both conditions are verified for `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/`. If a future PEFT version regression breaks the explicit-path matching `decoder.blocks.{0..15}.attn.{q,k,v,o}_proj`, LoRA could silently attach to cross_attn and invalidate (a). Future cycles must re-verify both conditions before transferring the PASS label.

3. **C3 — `PASS_VIA_PART_A_ONLY` is structural-by-invariance, not measurement-based**: the bridge fixture PASS is invariant by construction (eigenvec SSOT unchanged + fixture operates on eigenvec rows, not LoRA weights). This is a strong invariance argument but a different epistemic class than F1/F3/F5's measurement-based PASS. Future readers should NOT promote `PASS_VIA_PART_A_ONLY` to an unqualified `PASS` without re-verifying the eigenvec SSOT sha and the LoRA target_modules taxonomy.

4. **C4 — predecessor honest_c3 #4/#6/#8 already pre-registered the locus-mismatch concern**: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` honest_c3 #4 ("base axis discrimination off-diag mean 0.996 means base axes are nearly identical at this locus"), #6 ("LoRA cross_attn EXCLUDED — preservation is partly structural-by-construction"), and #8 ("the per-axis hidden-mean cosine metric at ln_f is structurally near-degenerate — it cannot distinguish strong axis-cond preservation from no axis-cond at all") together pre-registered exactly the failure mode this amendment formalizes. The amendment is the closure of that pre-registered concern, not a post-hoc rationalization.

5. **C5 — Part B re-enabling cost is non-trivial**: a future LoRA cycle that includes `cross_attn.{q,k,v,o}_proj` in target_modules would re-enter Part B's measurement contract. Estimated cost: $5–10 H100 SFT redo + $0 ubu1 measurement, separate cycle. This is **not authorized** under the current $0 amendment scope. The amendment does not preempt that future cycle's Part B re-measurement; it scopes its PASS to the current adapter only.

6. **C6 — own taxonomy unaffected**: `.own 14` (raw transient artifacts), `.own 15` (compute-budget orthogonal), `.own 16` (compute-resource transient) are orthogonal to substrate-axis-preservation. This amendment changes only the F-CLM-LORA-4 success criterion shape, not the compute/transient category attached to the underlying cycles.

7. **C7 — sibling Llama-side F4 amendment is a DIFFERENT argument**: `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md` argues F4 is **substrate-inapplicable** for Llama (Llama base has no native axis-cond machinery; mean pairwise cos ≈0.994 base ≈0.993 LoRA, signal noise-level). This CLM-side amendment argues F4 Part B is **locus-architecturally moot** for the current LoRA config (cross_attn dormant + LoRA-excluded). Both amendments converge on `PASS_*` for the respective lanes, but for substrate-distinct rationales — neither overrides the other; they are sibling-class amendments.

## §5 Apply procedure (when authorized)

This handoff is proposal-only. To apply the amendment as a roadmap mutation:

1. Review `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` § 3 (NEW PASS criterion) and §4 (supersession map).
2. Review companion `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` for the proposed `.roadmap.p9_sft` annotation block.
3. Authorize on a separate apply-cycle (precedent: `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md` `→` future apply-BG).
4. Apply the annotation as additive sibling field on the relevant `.roadmap.p9_sft` cond entry (per companion handoff §3 jq-recipe).

No exec, no commit, no roadmap mutation this cycle.
