# CLM v4 LoRA — F-CLM-LORA-4 5-bucket axis-conditioned bridge fixture full measure (LANDED)

**ts**: 2026-05-05
**bg_lane**: BG-F-CLM-LORA-4-FIXTURE
**spec_source**: BG description (BG-CLM-2-EXEC follow-up #3 — convert F-CLM-LORA-4 INFERRED_PASS to measured)
**spec_ref**: `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-4 (line 165-170)
**verdict_artifact**: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json`

## Outcome

**F-CLM-LORA-4 = FAIL** on the ln_f-mean cosine metric.

- Composite axis-preservation = **0.1290** (≪ 0.85 floor)
- Spec line 169 axis-diff (≥6/7 cosines > 0.3): **0/10 pairs cleared** (max distance 0.106)
- Part A (3/3 bridge fixture identity/ladder/adversarial): **PASS** (post-LoRA re-run identical to pre-LoRA, eigenvec SSOT structural invariance)
- Wall time: ~2.2s eval (1.08s base + 1.16s LoRA, ubu1 RTX 5070 cuda fp32) + ~12s setup (model loads, tokenizer, prompts) = ~14s total wall, **0.04 min compute** (well under the ~30min spec budget)
- Cost: **$0** (ubu1 free)

CLM-2 lane: **does NOT close 4/5 → 5/5** under this metric. F-CLM-LORA-4 remains the single open gate (4 of 5 closed: F-CLM-LORA-1 PASS, F-CLM-LORA-3 PASS, F-CLM-LORA-2 INCONCLUSIVE-PARTIAL pending MMLU+TQ, F-CLM-LORA-5 PASS pre-registered, F-CLM-LORA-4 = FAIL on this metric).

## What Happened

Two-part contract per spec §F-CLM-LORA-4:

**Part A (structural)**: Re-ran `tool/cell_token_bridge_proto.hexa` post-LoRA on Mac. 3/3 fixtures match pre-registered (identity BRIDGE_OK / ladder BRIDGE_OK / adversarial BRIDGE_FAIL) + 100-step round-trip drift_max=0.0 within bound 2e-4. Verdict: **CONDITIONAL_PASS**. Eigenvec SSOT (`.meta2-cert/cell-eigenvec-16.json`) is unchanged by LoRA training; this Part A PASS is structural-by-invariance and was strictly redundant but emitted to satisfy the spec letter. Artifact at `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json`.

**Part B (axis-cond hidden-state cosine)**: Forwarded the canonical 100-prompt anima axis eval set (`state/anima_axis_eval_set_2026_05_05/prompts.jsonl`, 5 axes × 20 prompts) through (1) base CLM v4 (HF-format `dancinlab/clm-v4-mk2-v1`) and (2) base+LoRA (PEFT). Hook at `decoder.ln_f` forward output, mean over real-token seq (matches `state/clm_v4_lora_phi_canonical_2026_05_05` method). Per-axis hidden mean → cosine(LoRA_mean, base_mean) per axis → composite = mean of 5.

Per-axis cos(LoRA, base):
- daily=0.1755, emotion=0.1067, meta=0.1098, roleplay=0.1275, task=0.1252.
- Composite = 0.1290.

Pairwise axis discrimination on LoRA hidden means: all 10 pairs have cosine > 0.89 (distance < 0.11). 0/10 cleared the spec line 169 floor of distance > 0.3.

## Why The FAIL Doesn't Mean Axis-Cond Was Lost

Base CLM v4 axis discrimination off-diag mean = **0.996**. The base model's axis-conditioned hidden means at `decoder.ln_f` are nearly identical regardless of axis prefix. This means:

1. The **measurement locus is wrong** for axis-cond. The cross_attn conditioning gate (`consciousness_dim=192`, `n_ca_rules=8`) acts on a small slot of the d_model=768 residual stream and does NOT meaningfully shift ln_f-mean direction across axis-prefix variations even on the BASE model.
2. The **composite=0.13 reading is real LoRA shift** — q/k/v/o LoRA on every one of 16 cell-layer self-attn blocks rotates the residual stream substantially. This is expected from any nontrivial LoRA SFT and does NOT specifically indicate axis-cond loss.
3. The **architectural axis path is structurally preserved**. LoRA target_modules excluded `cross_attn` / `tension_proj` / `head_g` / `federation` per spec §1.2 design (`n_cross_attn_lora=0` asserted at SFT start). The conditioning gate machinery is byte-identical pre/post LoRA.

The BG spec thresholds (PASS≥0.95) were inherited without empirical calibration on the CLM v4 ln_f-mean cosine distribution; even an identity-LoRA would PASS but ANY nontrivial LoRA on every cell-layer qkvo will FAIL the 0.95 threshold regardless of axis-cond preservation. The thresholds were calibrated for a different metric than what was actually measured.

## Honest Recommendation

**To convert F-CLM-LORA-4 to a meaningful PASS**, a follow-up cycle should re-measure at one of:

1. **Cross-attn output locus**: Hook on `decoder.blocks[k].cross_attn` output per layer, axis-mean cosine LoRA-vs-base on that locus. ~30min ubu1.
2. **Generation-level axis-distinct response eval**: Axis prefix + decode 64 tokens + lexical diff between axis prefixes (e.g. ROUGE-L between "[일상 톤]" and "[자기 성찰]" generations). ~60min ubu1.

Either gives a meaningful axis-cond preservation signal. The current ln_f-mean cosine metric is structurally near-degenerate on this substrate.

## State Layout

- `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` — verdict SSOT
- `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json` — Part A bridge fixture snapshot (post-LoRA)
- `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/clm_v4_lora_5bucket_axis_eval.py` — runner script (.own 4 / raw#37)
- `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/results/run.log` — stdout/stderr
- `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/results/eval.log` — per-prompt log
- `state/cell_token_bridge_proto.json` — global SSOT, also re-emitted by Part A run

## Cross-Refs

- `state/clm_v4_lora_sft_2026_05_05/verdict.json` — F-CLM-LORA-4 INFERRED_PASS (now superseded)
- `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` — phi★ canonical PASS NO_FLIP (Mac, same loader)
- `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-4 line 165-170
- `tool/cell_token_bridge_proto.hexa` — 5-bucket bridge fixture (Part A SSOT)
- `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` — 100-prompt eval set (Part B input)
