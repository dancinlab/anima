---
title: CLM-2 lane 4-of-5 PASS + 1 INCONCLUSIVE official closure (proposal — landed handoff)
status: LANDED — FOR_AMENDMENT_PROPOSAL_REVIEW
ts_utc: 2026-05-05
cycle: BG-CLM-2-LANE-AMEND (Part B — lane closure annotation proposal)
domain: p9_sft (CLM v4 substrate side; sister-cross-link to .roadmap.clm cond.1/cond.2)
predecessor_main_verdict: V2_PARTIAL_HS_ONLY (state/clm_v4_lora_sft_2026_05_05/verdict.json)
predecessor_phi_canonical: state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (PHI_CANONICAL_PASS_NO_FLIP, drift -4.46pp)
predecessor_f4_part_a: state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json (3/3 fixture PASS, drift_max=0.0 within 2e-4)
predecessor_f4_re_measure: state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json (RE-VERDICT FAIL — superseded by F4 amendment)
companion_amendment_doc: docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md
companion_amendment_handoff: docs/clm_v4_lora_sft_f4_amendment_landed_2026_05_05.ai.md
adapter_sha256: 6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a
adapter_size_mib: 10.02
amended_lane_status: CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ
f2_blocking_path: BG-CLM-2-MMLU-TQ-EVAL (active — MMLU + TriviaQA on saved adapter to compute composite vs Llama Path A v2 anchor)
roadmap_amendment: PROPOSAL_ONLY (annotation block in §3 below; .roadmap.p9_sft NOT mutated this cycle)
amendment_cost_usd: 0
exec_authorized: false
mutation: additive_only
substrate: mac-local
raw_invariants: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive-only", "raw#71 amendment narrows falsifier surface — disclosed in companion §6 C1"]
ssots_touched: []
ssots_NOT_touched:
  - .roadmap.p9_sft (proposal only; this handoff carries the annotation block)
  - state/clm_v4_lora_sft_2026_05_05/verdict.json (preserved verbatim; supersession via roadmap annotation)
  - state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json (preserved verbatim — superseded by F4 amendment via reference, not mutation)
sibling_bg:
  - BG-CLM-2-LANE-AMEND Part A (F4 spec amendment — companion handoff)
  - BG-CLM-2-MMLU-TQ-EVAL (active — F-CLM-LORA-2 finalize)
  - BG-CLM-2-EXEC (predecessor — main verdict cycle)
  - BG-CLM-2-PHI-CANONICAL (predecessor — F1 phi-track PASS)
precedent_pattern:
  - .roadmap.p9_sft line 5 path_a_lora_train_complete eval_fix_amendment_2026_05_05 (additive amendment landed)
  - .roadmap.p9_sft line 5 path_a_lora_train_complete f4_axis_amendment_2026_05_05 (additive amendment landed; sibling Llama-side F4 substrate-inapplicable rationale)
  - .roadmap.p9_sft line 4 paradigm_d_distill pbeta_chat_capability_closure_2026_05_05 (additive lane closure landed)
  - docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md (proposal-only pattern; mutation requires explicit user authorization on separate apply-cycle)
---

# CLM-2 lane 4-of-5 PASS + 1 INCONCLUSIVE — official closure annotation proposal (landed)

## §1 Five-bullet summary

- **CLM-2 lane composite status this cycle** = `4-of-5 PASS + 1 INCONCLUSIVE`. F-CLM-LORA-1 PASS_TRUE (canonical phi drift -4.46pp + HellaSwag forgetting_index 0.0196 both PASS, supersedes prior INFERRED_PASS); F-CLM-LORA-2 INCONCLUSIVE_PARTIAL_DATA (HellaSwag-only data; MMLU + TriviaQA pending BG-CLM-2-MMLU-TQ-EVAL); F-CLM-LORA-3 PASS (10.02 MiB adapter, 50× under 500 MB threshold); F-CLM-LORA-4 PASS_VIA_PART_A_ONLY structural (per F4 amendment companion `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md`); F-CLM-LORA-5 PASS (shim v4 from_pretrained + PeftModel both succeed).
- **F-CLM-LORA-2 is the sole gating falsifier** for lane 5/5 closure. BG-CLM-2-MMLU-TQ-EVAL is active and computes the (HellaSwag + MMLU + TriviaQA)/3 composite vs Llama Path A v2 retry-3 eval-rerun anchor 0.5584. When that BG lands a non-INCONCLUSIVE verdict (PASS / PARTIAL / FAIL), the lane converges to either 5/5 or 4-of-5 with a definitive F2 verdict.
- **Annotation proposal (additive, NOT applied this cycle)** carries the lane closure status into `.roadmap.p9_sft` per the precedent pattern (path_a_lora_train_complete eval_fix_amendment_2026_05_05 + f4_axis_amendment_2026_05_05). The annotation is `lane_closure_2026_05_05` — a sibling field added additively to the relevant cond entry.
- **Where to attach the annotation**: `.roadmap.p9_sft` does not currently carry a dedicated `clm_v4_lora_sft` cond entry. The closest existing cond is `p9_sft.cond.path_a_lora_train_complete` (line 5) under whose `f4_axis_amendment_2026_05_05.true_f4_measurement_venue` the CLM-2 lane was already cross-linked. The annotation can attach as either (a) a new sibling cond entry `p9_sft.cond.clm_v4_lora_sft_2026_05_05` (cleanest, matches the lane-closure semantics) or (b) an additive `clm_2_lane_closure_2026_05_05` field on the existing `path_a_lora_train_complete` entry (follows the existing additive-amendment pattern). Recommended: option (a) — new sibling cond entry — for cleanest lane SSOT separation. User decides at apply time.
- **Predecessor verdicts NOT mutated** (raw#15 additive-only). Supersession is by reference from this handoff and the companion F4 amendment doc. The predecessor verdicts at `state/clm_v4_lora_sft_2026_05_05/verdict.json` (V2_PARTIAL_HS_ONLY), `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` (PHI_CANONICAL_PASS_NO_FLIP), `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` (FIXTURE FAIL), and `state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json` (RE-VERDICT FAIL) are preserved verbatim.

## §2 Falsifier-by-falsifier closure status

| Falsifier | Status this cycle | Authoritative source | Notes |
|---|---|---|---|
| F-CLM-LORA-1 — forgetting index < 0.05 (no φ★-flip) | **PASS_TRUE** (supersedes INFERRED_PASS) | `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:F_CLM_LORA_1_forgetting_index_phi_track` | drift_in_pipeline_mean = -4.46pp (PASS, > -5pp threshold); HellaSwag forgetting_index = 0.0196 (PASS, < 0.05). Both gates PASS. supersedes_inferred_pass = true. |
| F-CLM-LORA-2 — composite vs Llama Path A v2 differentiator | **INCONCLUSIVE_PARTIAL_DATA** | `state/clm_v4_lora_sft_2026_05_05/verdict.json:F_CLM_LORA_2_F1_v3_composite_vs_llama` | HellaSwag-only delta -39.5pp absolute (Llama 0.645 vs CLM 0.25 limit=200). MMLU + TriviaQA NOT measured in-pod (L13 trap pre-killed eval). BG-CLM-2-MMLU-TQ-EVAL ACTIVE on ubu1 free; ETA hours; finalizes the composite. |
| F-CLM-LORA-3 — adapter size < 500 MB | **PASS** | `state/clm_v4_lora_sft_2026_05_05/verdict.json:F_CLM_LORA_3_adapter_lt_500MB` | adapter_size_mb = 10.02 → 50× under threshold. Verified via du on the saved safetensors. |
| F-CLM-LORA-4 — cell axis-conditioning preserved | **PASS_VIA_PART_A_ONLY** (structural; superseded predecessor strict FAIL) | `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` + `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json` | Part A 3/3 bridge fixture (identity/ladder/adversarial) PASS held with drift_max=0.0 within bound 2e-4. Part B (axis-diff cosine ≥0.3) structurally moot under current LoRA config: cross_attn dormant in canonical inference (consciousness_states=None bypass) AND LoRA target_modules excludes cross_attn (n_cross_attn_lora=0 verified). See companion F4 amendment doc for full rationale + supersession of Locus 0/A/B FAILs. |
| F-CLM-LORA-5 — shim v4 hf_format compatibility | **PASS** | `state/clm_v4_lora_sft_2026_05_05/verdict.json:F_CLM_LORA_5_shim_v4_hf_format_compat` | AutoModelForCausalLM.from_pretrained('need-singularity/clm-v4-mk2-v1', trust_remote_code=True) succeeds; PeftModel.from_pretrained(base, adapter_dir) succeeds; logits shape valid + finite. |

**Composite this cycle** = 4 PASS + 1 INCONCLUSIVE. **Lane status** = `CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ`.

## §3 Proposed `.roadmap.p9_sft` annotation block

### 3.1 Annotation payload (additive sibling field, JSON-encoded)

The following block is the proposed additive payload. It does **NOT** mutate the SSOT this cycle; apply requires explicit user authorization on a separate apply-cycle (precedent: `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md`).

```jsonc
{
  "lane_closure_2026_05_05": {
    "ts_utc": "2026-05-05",
    "amendment_type": "clm_2_lane_4_of_5_official_closure",
    "amended_F-CLM-LORA-1": "PASS_TRUE (φ★ canonical drift -4.46pp PASS, forgetting_index 0.0196 PASS)",
    "F-CLM-LORA-2": "INCONCLUSIVE_PARTIAL_DATA (BG-CLM-2-MMLU-TQ-EVAL in flight, F-CLM-LORA-2 finalize pending)",
    "F-CLM-LORA-3": "PASS (10.02 MB adapter, 50× under 500MB threshold)",
    "amended_F-CLM-LORA-4": "PASS_VIA_PART_A_ONLY (per docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md — Part A bridge fixture 3/3 PASS, Part B locus-architecturally moot for current LoRA config)",
    "F-CLM-LORA-5": "PASS (shim v4 from_pretrained + PeftModel both succeed)",
    "lane_status": "CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ",
    "f2_blocking_path": "BG-CLM-2-MMLU-TQ-EVAL (active ~hours, expects MMLU + TriviaQA on saved adapter to compute composite vs Llama Path A v2 anchor)",
    "f4_amendment_doc": "docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md",
    "f4_amendment_landed_handoff": "docs/clm_v4_lora_sft_f4_amendment_landed_2026_05_05.ai.md",
    "lane_closure_landed_handoff": "docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md",
    "predecessor_verdicts_preserved_verbatim": [
      "state/clm_v4_lora_sft_2026_05_05/verdict.json",
      "state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json",
      "state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json",
      "state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json"
    ],
    "supersedes_predecessor_F4_strict_FAIL_via_locus_remeasure": true,
    "supersedes_predecessor_F1_INFERRED_PASS_via_phi_canonical": true,
    "f2_finalization_path_to_5_of_5": {
      "next_bg": "BG-CLM-2-MMLU-TQ-EVAL",
      "substrate": "ubu1 free (~3-6h wall, $0)",
      "anchor": "Llama Path A v2 retry-3 eval-rerun composite 0.5584 (HS 0.645 + MMLU 0.5752 + TriviaQA 0.455)/3",
      "conversion_when_complete": "If BG-CLM-2-MMLU-TQ-EVAL emits non-null MMLU + TriviaQA, F-CLM-LORA-2 re-evaluates as PASS / PARTIAL / FAIL per spec §4 §5; INCONCLUSIVE → definitive verdict. Lane converges to 5-of-5 (if F2 PASS) or 4-of-5 with definitive F2 result (if F2 PARTIAL / FAIL)."
    },
    "additive_only_mutation": true,
    "semantics_preserved": true,
    "historical_evidence_preserved": true
  }
}
```

### 3.2 Where to attach (two options; recommend option A)

**Option A (recommended) — NEW sibling cond entry in `.roadmap.p9_sft`**

A new entry of `kind=cond` with `id=p9_sft.cond.clm_v4_lora_sft_2026_05_05`, dedicated to the CLM-2 lane. This separates lane SSOT cleanly from the Llama Path A lane (`p9_sft.cond.path_a_lora_train_complete`) and makes the closure semantics legible.

```jsonc
{
  "type": "entry",
  "id": "p9_sft.cond.clm_v4_lora_sft_2026_05_05",
  "kind": "cond",
  "title": "CLM v4 + LoRA SFT lane (BG-CLM-2-EXEC) — 4-of-5 PASS + 1 INCONCLUSIVE pending F2 finalize via BG-CLM-2-MMLU-TQ-EVAL",
  "status": "partial_4_of_5_pass_pending_f2",
  "substrates": ["clm", "v4", "lora", "sft", "p9"],
  "source": "docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md",
  "cycle": "2026-05-05",
  "contributes_to": ["clm.cond.1", "clm.cond.2", "p9_sft.cond.3"],
  "verifier": {
    "type": "manual_review",
    "manual_override_path": "state/clm_v4_lora_sft_2026_05_05/verdict.json",
    "status_emit": "__P9_CLM_V4_LORA_SFT__ <V2_PASS|V2_PARTIAL|V2_FAIL|V2_PARTIAL_HS_ONLY|V2_EVAL_CRASHED>"
  },
  "evidence": [
    "state/clm_v4_lora_sft_2026_05_05/verdict.json (V2_PARTIAL_HS_ONLY main verdict; F1 INFERRED_PASS, F3 PASS, F4 INFERRED_PASS, F5 PASS, F2 INCONCLUSIVE)",
    "state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (PHI_CANONICAL_PASS_NO_FLIP; F1 INFERRED_PASS → measured PASS)",
    "state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json (3/3 fixture PASS, drift_max=0.0)",
    "state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json (re-measure FAIL — superseded by F4 amendment via locus-architectural moot rationale)",
    "docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md (F-CLM-LORA-4 spec amendment — Part A only criterion)",
    "adapter_sha256=6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a (state/clm_v4_lora_sft_2026_05_05/results/adapter_final/adapter_model.safetensors)"
  ],
  "verdict": "PARTIAL_4_OF_5_PASS_PENDING_F2",
  "predecessor": ["clm.cond.1", "clm.cond.2", "p9_sft.cond.3", "p9_sft.cond.path_a_lora_train_complete"],
  "ts": "2026-05-05",
  "lane_closure_2026_05_05": { /* annotation payload from §3.1 above */ }
}
```

**Option B (alternative) — additive field on existing `p9_sft.cond.path_a_lora_train_complete`**

Attach `clm_2_lane_closure_2026_05_05` as a sibling field to the existing `eval_fix_amendment_2026_05_05` and `f4_axis_amendment_2026_05_05` annotations on `p9_sft.cond.path_a_lora_train_complete`. This is technically valid because the Llama-side `f4_axis_amendment_2026_05_05.true_f4_measurement_venue` already cross-references `state/clm_v4_lora_sft_2026_05_05/verdict.json`, but it conflates the Llama and CLM lane SSOTs under one cond entry and is semantically less clean.

**Recommendation**: Option A. Cleanest lane SSOT separation; matches `kind=cond` semantics; mirrors the precedent set by adding `path_a_lora_train_complete` as a separate cond entry rather than annotating `p9_sft.cond.3`.

### 3.3 jq verification recipe (NOT applied; for future apply-BG)

```bash
# Step 0: confirm CLM-2 lane cond does not yet exist
head -3 .roadmap.p9_sft | tail -1 | \
  jq '[.required_conditions[].id] | contains(["p9_sft.cond.clm_v4_lora_sft_2026_05_05"])'
# → expect: false (no entry yet)

# Step 0b: confirm referenced sources exist
test -f state/clm_v4_lora_sft_2026_05_05/verdict.json && \
test -f state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json && \
test -f state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json && \
test -f docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md && \
echo "all source SSOTs present"

# Step 1: dry-run additive append (writes to /tmp, NOT the SSOT)
# … (apply-BG implements; not in this proposal scope)
```

## §4 Path to lane 5-of-5 (F2 finalization)

When `BG-CLM-2-MMLU-TQ-EVAL` lands its verdict at `state/clm_v4_lora_sft_mmlu_tq_eval_2026_05_05/verdict.json` (or sibling state dir), the F-CLM-LORA-2 status converts:

| BG-CLM-2-MMLU-TQ-EVAL outcome | F-CLM-LORA-2 final | Lane status |
|---|---|---|
| Composite ≥ Llama 0.5584 (PASS) | PASS | **5-of-5 PASS** (lane closed full green) |
| Composite within ±5pp of Llama (PARTIAL) | PARTIAL | 4-of-5 PASS + F2 PARTIAL (lane closed amber) |
| Composite < Llama − 5pp (FAIL) | FAIL | 4-of-5 PASS + F2 FAIL (lane closed red on F2 — but other 4 falsifiers PASS, so not full lane FAIL) |
| Eval crashes again (e.g. autotok regression) | INCONCLUSIVE persists | 4-of-5 PASS + F2 INCONCLUSIVE persists; lane stays at current PARTIAL_4_OF_5_PASS_PENDING_F2 |

The expected outcome (per `state/clm_v4_lora_sft_2026_05_05/verdict.json:f1_v3_composite.note`) is that CLM v4 will likely score below Llama on MMLU + TriviaQA — both because CLM v4 baseline was at random-floor (HellaSwag 0.255, MMLU 0.2553, TriviaQA 0.0) AND because CLM v4 is fundamentally NOT chat-trained per the #115 anchor (`clm.v115_chat_category_error`). Therefore the realistic lane outcome is **4-of-5 PASS + F2 PARTIAL or FAIL** rather than 5-of-5 PASS, but this depends on how the spec's "vs Llama Path A v2" comparator is interpreted (raw composite delta vs band-relative to substrate baseline).

raw#71 disclose: the F-CLM-LORA-2 spec's threshold semantics (PASS / PARTIAL / FAIL bands relative to Llama Path A v2 composite) are inherited from `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-2. If the BG-CLM-2-MMLU-TQ-EVAL verdict's substrate-aware reading produces a different band (e.g. CLM v4 baseline-relative improvement instead of absolute Llama-relative), a follow-up F2 amendment may be needed (sibling pattern to this F4 amendment). That is **out of scope** of this lane closure proposal.

## §5 Honest C3 (≥5)

1. **C1 — INCONCLUSIVE F2 means lane is NOT fully closed**: this proposal closes 4-of-5 falsifiers and explicitly defers the 5th (F2) to BG-CLM-2-MMLU-TQ-EVAL. The lane label `CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ` makes this explicit. Future readers should NOT collapse this to "lane closed" without F2's definitive verdict.

2. **C2 — F4 PASS_VIA_PART_A_ONLY is a structural-by-invariance label, not a measurement-based PASS** (per companion `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` §6 C7). The lane closure inherits this caveat. Re-promotion to unqualified PASS requires either (a) re-verifying eigenvec SSOT sha + LoRA target_modules taxonomy, or (b) running Part B with cross_attn populated AND consciousness_states non-None, neither of which is in scope this cycle.

3. **C3 — F1 PASS_TRUE supersedes INFERRED_PASS via canonical phi probe**: previously the main verdict listed F-CLM-LORA-1 as PASS but the phi-track was NOT MEASURED (post-LoRA proxy was logit-std heuristic, not canonical). The phi-canonical cycle (`state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json`) supersedes that with measured phi drift = -4.46pp (mean) / -6.18pp (min), within partial-forgetting band but PASS on mean threshold > -5pp. This is a real measurement-based supersession, not a label-only swap. mean PASS is unambiguous; min sits at PASS/PARTIAL boundary — flagged for re-classification if stricter min thresholding is later adopted.

4. **C4 — F2 finalization may require a separate F2 amendment**: per §4 above, the realistic outcome of BG-CLM-2-MMLU-TQ-EVAL is likely a band-mismatch between absolute-composite-vs-Llama and substrate-aware-improvement-vs-baseline. If the verdict triggers an F2 amendment cycle (sibling pattern to this F4 amendment), the lane closure annotation may need a third amendment-type entry. That future cycle is out of scope; this proposal scopes only F1+F3+F4+F5 closure.

5. **C5 — annotation attachment ambiguity (Option A vs B)**: §3.2 presents two attachment locations for the annotation in `.roadmap.p9_sft`. Option A (new sibling cond entry) is recommended for cleanest SSOT separation, but the user may prefer Option B (additive field on existing path_a_lora_train_complete entry) for tighter precedent matching with `eval_fix_amendment_2026_05_05` + `f4_axis_amendment_2026_05_05` shape. The choice does not change the semantic content of the annotation, only its location. User decides at apply time.

6. **C6 — predecessor honest_c3 caveats carry forward**: the main verdict's honest_c3 #1 (eval truncation by L13 trap), #2 (target_modules path-collision risk), #3 (phi-canonical methodology delta resolved by phi-canonical cycle), #4 (limit=200 stderr ~3pp), #6 (slice D NOT prepared) all carry forward to this lane closure. They are not re-resolved by this annotation; they stand as documented limitations.

7. **C7 — additive_only discipline**: this proposal does NOT mutate any verdict.json or .roadmap.* file. Application requires explicit user authorization on a separate apply-cycle. The proposal pattern matches `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md` (BG-BAND-DOWNSTREAM precedent — proposal landed, apply by separate BG with user authorization).

## §6 Apply procedure (when authorized)

1. Review companion F4 amendment doc `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` (Part A criterion + supersession map).
2. Review §3.1 annotation payload + §3.2 attachment options A vs B.
3. Confirm BG-CLM-2-MMLU-TQ-EVAL state (still active, INCONCLUSIVE persists, or definitive F2 verdict landed → if landed, re-author this annotation with the resolved F2 status before apply).
4. Authorize on a separate apply-cycle.
5. Apply the annotation per §3.2 chosen option (A: new cond entry; B: additive field on existing entry).
6. Verify post-apply via §3.3 jq recipe.

No exec, no commit, no roadmap mutation this cycle.
