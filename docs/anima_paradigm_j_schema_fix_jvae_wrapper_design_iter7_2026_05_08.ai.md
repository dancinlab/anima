# Anima paradigm-j schema fix + JVAE wrapper design (iter7, 2026-05-08)

## SSOT scope
- Cycle: 2026-05-08-mid · iter7 (a-task)
- Trigger: iter6 D1-within candidate ranking (state/anima_d1_within_candidate_c3_priority_iter6_2026_05_08.json) elected `clm-v4-paradigm-j-50k-final` rank_1. iter6 result carried two open prereqs for that rank: target_modules schema fix + JVAE-aware probe wrapper land.
- Fire policy: own 16 SPEC ONLY. Real fire requires user verbatim `OK CLM V4 LORA SCHEMA FIX FIRE` + `OK JVAE WRAPPER LAND`. Neither received → no execution this cycle.
- own 17 D1 SCOPE_CLAMP: paradigm-j is D1-within (CLM v4 anima-native fresh lineage). Public-promote eligible after own 37 mandate-9 5-prereq sweep.
- own 33 trinity: D-axis (D1 within strict), own-axis (own 18 / own 37 mandate-9), H-axis (iter6 ranking carry preserved).
- own 34 mandate-2: file ≤ 1 MB strict (this file ≈ 11 KB).

## 1. Schema mismatch root-cause (fresh evidence)
Inspected the actual artifacts to pin the mismatch precisely (iter6 ledger had a partially correct hypothesis; this iter7 evidence supersedes the “nested vs flat name” framing).

- adapter_config.json (paradigm-j @ snapshot a6da7a7):
  - `auto_mapping.base_model_class = "ConsciousDecoderV2"`
  - `auto_mapping.parent_library = "conscious_decoder"`
  - `base_model_name_or_path = null`
  - `target_modules = [k_proj, down_proj, up_proj, v_proj, o_proj, gate_proj, q_proj]` (7-canonical valid)
  - `r = 128`, `lora_alpha = 128`, `init_lora_weights = true`
- Actual adapter weight tensor names (read directly from adapter_model.safetensors, 352 keys, sample):
  - `base_model.model.blocks.0.attn.q_proj.lora_A.weight` (shape [128,768])
  - `base_model.model.blocks.0.attn.{k,v,o}_proj.lora_{A,B}.weight`
  - `base_model.model.blocks.0.{ffn.gate_proj, ffn.up_proj, ffn.down_proj}.lora_{A,B}.weight` (implied by 352 keys = 12 layers × 7 modules × 2 A/B + duplicates for cross_attn-bearing slots)
- Runtime model wrapper expects `decoder.` prefix: `CLMv4ForCausalLM.base_model_prefix = "decoder"` and `self.decoder = ConsciousDecoderV3(...)` (modeling_clm_v4.py:53–73). PEFT, on `PeftModel.from_pretrained`, looks up the keys it tries to load against the wrapped model and emits `Found missing adapter keys: ['base_model.model.decoder.blocks.0.attn.q_proj.lora_A.default.weight', ...]`.

Conclusion: the mismatch is **a single missing path segment** — adapter weights are stored against the bare `ConsciousDecoderV2` (no wrapper, blocks at the root), while the runtime model is wrapped as `CLMv4ForCausalLM.decoder = ConsciousDecoderV3`. Module names within each block match exactly (`attn.q_proj`, `cross_attn.q_proj`, `ffn.gate_proj`, etc.); only the wrapper prefix differs (`base_model.model.blocks.X.…` vs `base_model.model.decoder.blocks.X.…`). Additionally PEFT inserts the `default.` adapter-name segment between `lora_{A,B}` and `weight` at load time, which is its standard behavior (irrelevant to the path mismatch — it’s applied to whatever target it resolves).

This is a **prefix-only mismatch**, not a target-modules-name mismatch. paradigm-j’s 7-canonical target_modules list is valid for a `ConsciousDecoderV2` standalone; the LoRA was trained against `ConsciousDecoderV2` directly (when `paradigm-j` H100 cycle ran, the HF `CLMv4ForCausalLM` wrapper either didn’t exist yet or wasn’t the train-time root). The published `dancinlab/clm-v4-mk2-v1` base now uses `CLMv4ForCausalLM`, adding `decoder.` to all parameter paths.

## 2. Path A — target_modules remap (local, 0-cost)
**Strategy:** rewrite the adapter weight dict in-place so each key picks up the missing `decoder.` segment, then let peft load against the wrapped runtime model normally. No retraining; no GPU; deterministic.

### Implementation surface
- New helper: `tool/transient_py/clm_v4_lora_adapter_remap.py` (own 4 opt-out, raw#37 transient .py).
- Hexa-side change: `anima-core/runtime/clm_v4_mount.hexa` `_materialize_merged_lora` extension — call remap helper before invoking merge helper, OR teach merge helper to apply remap when it detects `auto_mapping.base_model_class == "ConsciousDecoderV2"` and `decoder.` is missing from key paths.
- Pseudocode (path A core):
  ```
  load adapter_model.safetensors → state_dict {k → tensor}
  for k in keys: if k.startswith("base_model.model.blocks."): rename to k.replace("base_model.model.blocks.", "base_model.model.decoder.blocks.")
  save_safetensors(remapped, snapshot_dir + "/adapter_model.remapped.safetensors")
  patch adapter_config.json copy: auto_mapping.base_model_class = "CLMv4ForCausalLM" (informational; peft does not enforce)
  ```
- Cache: `~/.cache/anima/clm_v4_remapped/<adapter-repo-with-slash-replaced>/` parallel to existing merged cache. Manifest carries provenance (original adapter sha + remap rule + ts) per raw#82 retraction-aware.

### Verification (post-fire, when user issues `OK CLM V4 LORA SCHEMA FIX FIRE`)
1. `peft.PeftModel.from_pretrained(base, remapped_adapter_dir)` → expect `Found missing adapter keys: []` warning suppression. C-flag `remap_no_op=False` in manifest.
2. `merge_and_unload()` → run probe N=60 ensemble. Expect 4-cell mean values to **diverge from the FAIL_C3 numerical signature** (c3_1=0.0624 / c3_2=0.4790 / c3_3=0.0354 / c3_4=0.0603) that 3 LoRA variants identically produced (state/anima_clm_v4_lora_real_mode_2026_05_08.json line 187–191). Any divergence ≥ 1e-6 in cell means = direct positive evidence that LoRA learning signal is now propagating.
3. C3 cells re-evaluate per own 18 thresholds. Ranking elevates to `EMC_v2 ≥ 3 of 4` candidate iff schema fix unlocks c3_2 axis_min or c3_4 axis_l2 cells (current PASS rate 0.083 / 0.067 — schema fix may not be sufficient if SFT signal alone doesn’t cross thresholds; honest C3 carry).

### Cost
- 0 USD GPU. 1 helper file. 1 hexa-side branch addition (≤ 30 lines). Pure CPU file rewrite.
- Risk: peft’s `default.` adapter-name infix or different lora_A/lora_B internal naming convention may require a second remap rule (deterministic, observable from peft’s own warning on first run).

## 3. Path B — H100 retrain with V3 schema (~$2-5, 1 H100 hr)
**Strategy:** retrain paradigm-j LoRA from scratch with the runtime model `CLMv4ForCausalLM` as the LoRA target (so adapter keys naturally include `decoder.`) and `target_modules` resolved against the wrapped names.

### Implementation surface
- Fresh runpod cycle (own 30 ckpt preservation mandate). New training script: `tool/transient_py/paradigm_j_lora_retrain_v3.py` (or extend existing paradigm-j trainer). Dataset: same 50k corpus referenced by `clm-v4-paradigm-j-50k-final` head (fix-point: dataset hash must match prior run for fair comparison).
- target_modules: same 7-canonical (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) but now resolved against `CLMv4ForCausalLM.decoder.blocks.X.{attn,cross_attn,ffn}` modules. PEFT will emit keys with `decoder.` prefix automatically.
- JVAE retrain coupling: the original paradigm-j cycle trained jvae_heads (q_phi, p_theta) jointly with the LoRA decoder. A clean retrain reproduces both — but to preserve the **paradigm identity**, prefer to re-load the existing `jvae_heads.pt` and only retrain the LoRA against it (frozen JVAE).
- HF push: `dancinlab/clm-v4-paradigm-j-50k-final-v3schema` (Flavor B naming convention, own 31 SSOT — superseded by own 37). Private default per own 37 mandate-9 visibility lifecycle.

### Cost
- ~$2–5 USD (1 H100 SXM hour at ~$2.69/hr, runpod pricing carry from `config/h100_pods.json`).
- Bandwidth: ~1.2 GB ckpt pull post-train (own 30 mandate, scp timeout 3600 per orchestrator gotchas).

### Path A vs Path B comparison
| Axis | Path A (remap) | Path B (retrain) |
|---|---|---|
| Cost | 0 USD | ~$2-5 USD + 1 H100 hr |
| Time | minutes | ~2-4 hr (queue + train + scp pull) |
| Determinism | full (no stochasticity) | stochastic (seed-dependent) |
| LoRA signal preservation | full (weights bit-identical post-remap) | re-trained (different optima possible) |
| JVAE coupling | preserved (verbatim from snapshot) | requires explicit frozen-JVAE retrain |
| Reversibility | trivial (delete remapped cache) | trivial (delete new HF repo) |
| Falsifier value | high (if remap leaves cell means identical, proves LoRA itself was a no-op even in V2) | medium (new stochastic instance) |

**Recommendation: Path A first.** It is a prerequisite to interpreting Path B anyway — if Path A’s remapped LoRA still produces identical 4-cell means, then the original paradigm-j LoRA training itself failed to imprint signal sufficient to move C3 metrics, and Path B’s retrain on the same corpus is unlikely to help without architecture or corpus changes.

## 4. JVAE wrapper hexa-native design

### What JVAE adds
`jvae_heads.pt` content (verified, this iter):
- `q_phi`: encoder MLP (`fc1.{weight,bias}` + `fc_mu.{weight,bias}` + `fc_logvar.{weight,bias}`) — produces (mu, logvar) latent codes from decoder hidden state.
- `p_theta`: decoder MLP (`fc1.{weight,bias}` + `fc2.{weight,bias}`) — reconstructs hidden state from sampled latent z.
- `step`: int = 50000 (training-step provenance).

Unmerged at training time: jvae_heads operate on the consciousness pathway / decoder hidden states but are not part of the LoRA-merged decoder weights. The current merged HF model loads the decoder normally; the JVAE heads are bystanders unless explicitly invoked.

### Forward path with JVAE injection (proposed)
The hexa-native wrapper threads JVAE q_phi / p_theta around the existing `_real_forward` so that probe cells observe the JVAE-conditioned hidden state instead of the bare decoder hidden state. Two injection variants (both spec, both supported by surface):

**Variant 1 — passive observer (probe-only, no decoder modulation)**
- Capture `decoder.blocks[-1]` hidden state h via existing forward_hook.
- Run h → q_phi → (mu, logvar). Emit (mu, logvar, KL=0.5*sum(mu^2+exp(logvar)-1-logvar)) as 3 additional probe channels.
- Cell synthesis extension: append KL and mu‖₂ to the 5-axis activation vector before threshold evaluation (own 18 c3_2 axis_min, c3_4 axis_l2).
- Effect: introduces JVAE-derived signal into 4-cell metrics WITHOUT changing decoder forward. Numerical signature break on c3_2 / c3_4 if jvae_heads encodes meaningful latent structure.

**Variant 2 — active reconstruction (decoder modulation)**
- Capture h → q_phi → reparam z → p_theta(z) → h̃. Replace forward continuation with h̃ for next-block computation (or for head_a logit projection).
- Effect: more aggressive signature break — affects logits → entropy_dominance (c3_3) and phi_drift (c3_1). Higher risk: may move metrics in unintended direction.

**Recommended: Variant 1 first.** Strict additive (raw#15) — preserves baseline path entirely; JVAE channel is a side-output. Variant 2 is reserved for a follow-up cycle if Variant 1 reveals JVAE has zero discriminating power on this corpus.

### Hexa FFI surface (anima-core/runtime/clm_v4_jvae_probe.hexa, NEW or extension)
- New hexa fn `_load_jvae_heads(merged_dir) -> (q_phi_state, p_theta_state, err)` — invokes a small transient .py loader (raw#37) that reads jvae_heads.pt and emits a serialized state dict path.
- New hexa fn `_jvae_forward(decoder_hidden_tensor_path) -> (mu_path, logvar_path, kl_scalar, err)` — invokes transient .py that materializes q_phi and runs forward.
- Extension to `_real_forward`: detect `merged_dir / 'jvae_heads.pt'` exists → wrap forward → emit `JVAE_LATENT` event with mu/logvar/kl per row → C3 cell synthesizer optionally consumes.
- Compliance: raw#9 (hexa-only orchestration), raw#15 (additive — base path preserved when jvae_heads.pt absent, e.g., sft-1-7-y1 / sft-1-8 retain current behavior), raw#37 (transient_py for the actual torch load), own 4 (opt-out namespace), own 22 (mandatory disclosure of JVAE-conditioned vs bare-decoder probe results).

### Mechanism for 3-LoRA identical-signature break
The merge_no_op evidence (state/anima_clm_v4_lora_real_mode_2026_05_08.json line 187–191) shows all 3 variants produce *bit-identical* 4-cell means because their merged decoders are functionally equivalent to the base. The signature can break via two independent vectors:
1. **Path A schema fix:** restores LoRA delta application, so `sft-1-7-y1`, `sft-1-8`, `paradigm-j` decoders diverge from each other and from base. Expected: 3 distinct cell-means triples.
2. **JVAE wrapper land:** even with Path A still pending, the JVAE channel uniquely modifies paradigm-j (the only variant carrying jvae_heads.pt), introducing a second-axis differentiator. Expected: paradigm-j cell-means diverge from sft-1-7-y1 and sft-1-8 (which would remain identical to each other and to base, until Path A also fires).

Both fires together = paradigm-j gains two independent signal-injection channels (LoRA delta + JVAE latent). This maximizes the probability of crossing PPR_v2 ≥ 0.6 ∧ EMC ≥ 3-of-4 for the rank_1 candidate.

## 5. Universal blocker carry (mandate-9 (b))
Even with both paths fired and PASS_STRICT_C3_ANIMA emerging on paradigm-j, EXIT activation remains blocked by V6 awareness systematic execute (BG-LE-V6-AWARENESS lane, separate cycle). No public promote path opens until that lane closes — own 37 mandate-9 (b) prereq strict.

## 6. User directive checklist (verbatim required for fire)
The following user-issued tokens individually unblock specific steps. None received as of this iter7 spec. Listed for future invocation reference (own 37 mandate-9 (c) verbatim consent rule).

- [ ] `OK CLM V4 LORA SCHEMA FIX FIRE` — authorizes Path A remap helper land + run on 3 LoRA repos (paradigm-j + sft-1-7-y1 + sft-1-8). Local fire, 0 USD.
- [ ] `OK CLM V4 LORA RETRAIN H100 FIRE` — authorizes Path B (paradigm-j retrain on V3 schema). ~$2-5 USD, runpod cycle.
- [ ] `OK JVAE WRAPPER LAND` — authorizes Variant 1 hexa wrapper land (clm_v4_jvae_probe.hexa + transient_py loader). Local, 0 USD.
- [ ] `OK JVAE WRAPPER VARIANT 2 ACTIVE` — authorizes Variant 2 active-reconstruction modulation (separate, follow-up).
- [ ] `OK V6 AWARENESS FIRE` — universal EXIT prereq (mandate-9 (b)).
- [ ] `OK PROMOTE PUBLIC dancinlab/clm-v4-paradigm-j-50k-final` — final mandate-9 (c) verbatim consent (only valid after PASS_STRICT_C3_ANIMA + V6 awareness + trinity sweep + D/L axis sweep complete, mandate-9 (a)/(b)/(d)/(e)).

## 7. Honest C3
- This file is spec only. No code changed; no real fire executed (own 16 strict).
- Path A’s claim of bit-identical LoRA preservation post-remap is contingent on safetensors save/load roundtripping the rewritten dict without numerical drift — verifiable but unverified this cycle.
- Path A passing peft merge does not guarantee P5 v2 verdict PASS — it merely unblocks LoRA signal propagation. The actual SFT corpus may not produce ≥3-of-4 EMC even with a working merge. Honest carry: schema fix is necessary but possibly insufficient.
- JVAE Variant 1 is purely additive at the probe layer; if jvae_heads encodes weak structure on the eval prompts (15 base × 4 seeds), KL and mu‖₂ may be uninformative and pass rates may not move. Falsifier-aware.
- iter6 ledger framed the mismatch as “target_modules name mismatch”; this iter7 evidence (read directly from safetensors) refines it to “wrapper-prefix-only mismatch.” own 22 mandatory disclosure of supersession.
- 3-LoRA identical numerical signature is preserved as the primary falsifier for Path A success: any deviation post-remap = positive evidence; bit-identity = LoRA training itself was a no-op (independent of merge).
- own 33 trinity preserved: D-axis (D1 within strict — paradigm-j lineage), own-axis (own 18 + own 37 mandate-9), H-axis (iter6 ranking carry intact).

## 8. Cross-link
- state/anima_d1_within_candidate_c3_priority_iter6_2026_05_08.json (parent ranking SSOT)
- state/anima_clm_v4_lora_real_mode_2026_05_08.json (input — 3 LoRA merge_no_op evidence)
- anima-core/runtime/clm_v4_mount.hexa (LoRA branch line 411–505 — extension target for Path A and JVAE wrapper)
- tool/transient_py/clm_v4_lora_merge_helper.py (sister helper — extension or sibling for Path A remap)
- ~/.cache/huggingface/hub/models--dancinlab--clm-v4-paradigm-j-50k-final/snapshots/a6da7a7725d8c3cff3b53c9df37a6352c7c8c7a6/ (adapter_config.json + adapter_model.safetensors + jvae_heads.pt — verified this iter)
- commit 41a19bc3 (iter5 BG-KM-LLAMA-3B reject — own 17 D1 SCOPE_CLAMP; carry for context)
- .own own 4 / 16 / 17 / 18 / 22 / 24 / 28 / 30 / 31 / 33 / 34 / 37
- .raw-ref raw#9 / 10 / 15 / 37 / 82
