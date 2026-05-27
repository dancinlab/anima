# F-CLM-LORA-4 RE-MEASURE — alternate-locus axis-cond preservation (LANDED 2026-05-05)

## Verdict
**F-CLM-LORA-4 RE-VERDICT: FAIL** (0/3 locus PASS)

| Locus | Source | Composite | Threshold | Grade |
|---|---|---|---|---|
| 0 (carry) | predecessor `decoder.ln_f` mean cosine LoRA-vs-base | **0.1290** | ≥0.85 | FAIL_LOCUS_DEGENERATE |
| A (new) | per-layer `decoder.blocks[i].ln_ffn` output mean cosine LoRA-vs-base, 16 layers × 5 axes | **0.5436** | ≥0.85 | FAIL |
| B (new) | generation-level cross-axis BLEU-1 preservation (LoRA pattern vs base pattern), 5 axes × 12 bodies | **0.7240** | ≥0.85 | FAIL |

`closes_clm_2_lane_4_of_5_to_5_of_5_when_F2_lands` = **false**
`supersedes_locus_0_FAIL_via_alternate_loci` = **false**

## Artifacts

- **Verdict**: `state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json`
- **Eval log**: `state/clm_v4_lora_4_axis_remeasure_2026_05_05/results/eval.log`
- **Generation sample**: `state/clm_v4_lora_4_axis_remeasure_2026_05_05/results/generations_sample.json`
- **Eval script**: `tool/transient_py/clm_v4_lora_4_axis_remeasure.py` (raw#37 transient)
- **Predecessor**: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` (F-CLM-LORA-4-FIXTURE)
- **Adapter**: `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/adapter_model.safetensors` sha256=`6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a` size=10502216

## Substrate
ubu1 (RTX 5070 sm_120) cuda fp32; torch=2.11.0+cu128; venv `/home/aiden/venv_orchestrator`. Wall total ≈ 1.7 min. Cost = $0.

## Method (high-level)

### Locus A: ln_ffn per-layer output cosine
Per-prompt forward → forward_hook on `decoder.blocks[i].ln_ffn` for i in [0..15] → `output[0].mean(dim=seq)` → per-axis mean of these per-layer means → per-layer per-axis cosine(LoRA, base) → per-layer mean over 5 axes → composite = mean over 16 layers.

**Locus pivot from BG spec**: BG spec asked for `cross_attn output per layer`. In CLM v4 canonical inference (`consciousness_states=None`), the decoder block guards
```
if consciousness_states is not None:
    x = x + cross_attn(ln_cross(x), c_detached)
```
so neither `cross_attn` nor `ln_cross` fires; their forward_hooks never trigger. We pivoted to `ln_ffn` (LayerNorm immediately before SwiGLU FFN), which is the most downstream per-layer LayerNorm that **always** fires on the canonical path and captures the integrated residual after self-attn / CA-mix / META-CA / PureFieldFFN / inter-layer whisper. Per-layer (16 layers) is far more granular than the single decoder.ln_f terminus used by the predecessor (which sits at base off-diag mean = 0.996, structurally near-degenerate). honest_c3 #1.

### Locus B: generation-level cross-axis BLEU-1 preservation
12 axis-neutral prompt bodies × 5 axis prefixes (`[일상 톤]`, `[감정에 공감하며]`, `[정확하게]`, `[역할극으로]`, `[자기-지시적으로]`) = 60 generations per regime; greedy decode max_new_tokens=64. Per-axis preservation = mean over 12 bodies of `1 - |base_other_overlap - lora_other_overlap|` where `*_other_overlap` is mean BLEU-1 of this axis's generation against the OTHER 4 axes' generations at the same body. Composite = mean over 5 axes.

## Key findings

### Locus A per-layer pattern
- Layers 0–9: composite cosine 0.43–0.67 (LoRA shifted residual modestly)
- Layers 10–12: 0.73–0.79 (most preserved — middle of stack)
- Layer 13: 0.47 (drop)
- Layers 14–15: 0.32, 0.034 (catastrophic drop at terminal layers)

The terminal-layer collapse (0.034 at layer 15) explains the predecessor's composite=0.13 at decoder.ln_f: LoRA q/k/v/o on self-attn substantially rotates the FINAL residual direction, even though middle layers preserve axis-cond reasonably well. Per-layer base off-diag remains ≥0.99 across all 16 layers, confirming the residual stream itself is axis-blind at the mean direction at every layer (base axes already collapse across axes).

### Locus B caveat (read-alongside)
- `base_cross_axis_bleu1_mean = 0.726` (base is mostly axis-blind at greedy decode — same prompt body across 5 axis prefixes produces ~73% lexical overlap)
- `lora_cross_axis_bleu1_mean = 0.995` (LoRA is **fully** axis-blind at greedy decode — 99.5% lexical overlap across axis prefixes)
- Per-axis preservation 0.66–0.77 reflects: LoRA SHIFTED the cross-axis overlap pattern from base's 0.73 baseline up to 0.99, a 0.27-magnitude shift, which when measured as `1 - |Δ|` gives ~0.73.

Inspecting the generation samples (`results/generations_sample.json`):
- Base generates degenerate repetitions: `pppppppppppp`, `aaaaaaaaaaaa`, `bbbbbbbbbbbb`, `b(((((((((((`
- LoRA generates degenerate repetitions: `____________` for ALL axes ALL bodies

Both models are essentially axis-blind at greedy decode on this base CLM v4 substrate; LoRA SFT did not produce instruction-following capability that would let axis prefixes induce axis-distinct generations. This further validates the predecessor's diagnosis that base CLM v4 axis-cond machinery does not propagate to surface-form generation distinctness — and LoRA on q/k/v/o self-attn alone (cross_attn EXCLUDED) does not unlock it.

### Honest assessment
**The "axis-cond preservation" question as posed is structurally unanswerable on this substrate at the chosen loci**:
- Locus 0 (decoder.ln_f) is near-degenerate at base (off-diag 0.996)
- Locus A (per-layer ln_ffn) shows LoRA materially shifted layers 13–15 (the ones closest to ln_f), confirming the predecessor's terminal-layer signal
- Locus B greedy-decode shows BOTH base and LoRA produce degenerate generations — there is no axis-distinct generation signal to preserve in the first place

The architectural axis-cond gate (cross_attn with consciousness_dim=192) is **never exercised** in canonical inference (consciousness_states=None bypass), so axis-cond preservation under LoRA is a question about a code path that is dormant during eval. The 3/3 bridge fixture (Part A from predecessor) PASSES structurally because the eigenvec SSOT is unchanged by LoRA training; that PASS is the only meaningful axis-cond preservation signal we have on this substrate.

## CLM-2 lane closure status
- Lane currently 4/5 (per BG-CLM-2-EXEC closure)
- F-CLM-LORA-4 RE-VERDICT = FAIL on alternate loci (this cycle)
- **Lane 5/5 closure NOT achieved by this re-measure**. Closure pathway requires either:
  1. F-CLM-LORA-4 spec line 169 reinterpretation as "3/3 bridge fixture PASS" only (drops the axis-diff threshold) — political/spec-revision path, not a measurement path
  2. Re-train LoRA with cross_attn ENABLED in target_modules + run a generation-level eval where consciousness_states is populated with a non-trivial fixture — separate cycle, requires SFT redo
  3. Use a non-greedy decode path with sampling + sentence-embedding semantic distance instead of BLEU-1 — separate dependency-introduction cycle

## honest_c3 (≥5)
See `verdict.json` honest_c3 — 7 items covering locus pivot, greedy decode limitation, prefix-corpus alignment uncertainty, sample-size noise, structural-by-construction caveat, BLEU-1 lexical-only limitation, and per-axis preservation ambiguity when both regimes are axis-blind.

## Next actions (recommended, ranked by 완성도)
1. **Accept FAIL** + close F-CLM-LORA-4 with documented "metric-locus mismatch on chosen substrate" rationale; lane 4/5 stands; revisit only if a spec amendment OR a future retrain expands the axis path. (highest 완성도 — honest result, no further $/time spend)
2. **Spec amendment**: re-write F-CLM-LORA-4 success criterion to "3/3 bridge fixture PASS + cross_attn LoRA structurally untouched" (drop the cosine-axis-diff threshold which assumes a propagation path that doesn't exist in canonical inference). Mark predecessor PASS structural-by-invariance, this lane closes 5/5.
3. **Re-train cycle**: include `cross_attn.q_proj/k_proj/v_proj/o_proj` in LoRA target_modules + provide a non-trivial consciousness_states fixture during eval. Separate ~2hr H100 cycle; out of $0 ubu1 scope.

## raw compliance
- raw#9 deterministic (seed=42, greedy decode, fp32)
- raw#10 no fabrication (all numbers from measured forward + cosine + BLEU-1)
- raw#12 실측 그대로 (FAIL reported as-is, no metric-tweak to escape FAIL)
- raw#15 no hardcode (all paths via constants + adapter sha verification at boot)
- raw#37 transient_py opt-out (script lives in `tool/transient_py/`)
- .own 4 (transient — no commit, deleted post-cycle is OK)
