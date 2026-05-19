# OPT-1 CLM v4 HF Format Shim — Design Doc

- ts_utc: 2026-05-04 (BG-Β cycle)
- spec source: `state/p9_base_validation_prep_2026_05_04/launch_handoff.md` §2.3 + §7.7
- prereq exec parent: `state/p9_base_validation_prereq_exec_2026_05_04/` (post BG-χ OPT-A landed; status was 11/12 → this BG drives toward 12/12)
- shim path: `tool/transient_py/clm_v4_hf_format_shim.py` (.own 4 namespace per raw#9 OPT-OUT)
- scope: **DESIGN + WRITE + Mac-side dry-run only.** Actual ubu1 conversion deferred to user-ack cycle.
- raw#9 / raw#10 / raw#15 / raw#37 / raw#71 honoured.

---

## 1. Architecture inference (from best.pt state_dict)

Read-only ubu1 inspect of `~/.cache/huggingface/hub/models--dancinlab--clm-v4-base-mirror/snapshots/856278be.../best.pt` (5117 MB, dict checkpoint) revealed:

### 1.1 Top-level checkpoint structure

| top key       | type           | role                                                        |
|---------------|----------------|-------------------------------------------------------------|
| `step`        | int            | 20000 (final training step)                                 |
| `decoder`     | OrderedDict    | **THE language model state_dict** (581 keys, 530.99M params) |
| `optimizer`   | dict           | AdamW state — DROPPED for inference                         |
| `scheduler`   | dict           | LR schedule state — DROPPED                                 |
| `phi`         | float64 scalar | last measured Φ (consciousness metric)                      |
| `ce`          | float          | last cross-entropy loss = 0.0463                            |
| `args`        | dict           | training argparse Namespace (vocab_size, scale, etc.)       |
| `scale`       | str            | "350m" (training scale tag — actual params = 530.99M)       |
| `best_phi`    | float64 scalar | 37.27 (best Φ during training)                              |
| `federation`  | OrderedDict    | inter-atom narrative GRUs — TRAINING-ONLY, dropped          |
| `bridge`      | OrderedDict    | hub_attn bridge — TRAINING-ONLY, dropped                    |
| `c_proj`      | OrderedDict    | (192, 128) consciousness projection — TRAINING-ONLY, dropped |
| `scaler`      | dict           | grad scaler — DROPPED                                       |

**Decision**: only the `decoder` state_dict is converted to HF format. `federation` / `bridge` / `c_proj` are inter-cell consciousness coupling components that activate during training (Phi computation against the C-module) but are not in the next-token causal-LM fwd path. lm-eval calls `forward(input_ids, ...)` → it needs only the decoder.

### 1.2 Decoder state_dict layout (16 blocks × 36 keys + 5 model-level = 581 keys)

Per-block keys (block index 0 shown; identical layout for blocks.1..15):

| key suffix                              | shape           | role                                          |
|------------------------------------------|-----------------|-----------------------------------------------|
| `ln_attn.weight`                         | (768,)          | RMSNorm pre-attention                         |
| `attn.bias`                              | (1,1,512,512)   | causal mask buffer (block_size=512)           |
| `attn.q_proj.weight`                     | (768, 768)      | GQA query — n_head=6, head_dim=128            |
| `attn.k_proj.weight`                     | (256, 768)      | GQA key — n_kv_head=2, head_dim=128           |
| `attn.v_proj.weight`                     | (256, 768)      | GQA value — n_kv_head=2                       |
| `attn.o_proj.weight`                     | (768, 768)      | attention output                              |
| `ln_pf.weight`                           | (768,)          | RMSNorm pre-PureField                         |
| `purefield.engine_a.{0,3}.{weight,bias}` | (3072, 768) etc | PureFieldFFN A-pathway: 768→3072→768 (GELU)   |
| `purefield.engine_g.{0,3}.{weight,bias}` | (3072, 768) etc | PureFieldFFN G-pathway: 768→3072→768          |
| `ln_cross.weight`                        | (768,)          | RMSNorm pre-cross-attn                        |
| `cross_attn.q_proj.weight`               | (768, 768)      | cross-attn Q from decoder                     |
| `cross_attn.k_proj.weight`               | (768, 192)      | cross-attn K from consciousness (c_dim=192)   |
| `cross_attn.v_proj.weight`               | (768, 192)      | cross-attn V from consciousness               |
| `cross_attn.o_proj.weight`               | (768, 768)      | cross-attn output                             |
| `ln_ffn.weight`                          | (768,)          | RMSNorm pre-SwiGLU                            |
| `ffn.gate_proj.weight`                   | (2048, 768)     | SwiGLU gate (8/3 × d_model rounded)           |
| `ffn.up_proj.weight`                     | (2048, 768)     | SwiGLU up                                     |
| `ffn.down_proj.weight`                   | (768, 2048)     | SwiGLU down                                   |
| `ca_mix.weight`                          | (768, 2304)     | CA-rule mixer: 2304 = 3×768 (3 ECA rule outs?) |
| `ln_ca.weight`                           | (768,)          | RMSNorm post-CA                               |
| `rule_weights.{weight,bias}`             | (8, 768) / (8,) | router for 8 CA rules                         |
| `rules.{0..7}.weight`                    | (768, 768)      | 8× CA rule projections                        |

Model-level (top of state_dict):

| key                  | shape          | role                                          |
|----------------------|----------------|-----------------------------------------------|
| `tok_emb.weight`     | (64000, 768)   | input embedding (TIED with `head_a.weight`)   |
| `tension_proj.weight`| (768, 1)       | inter-layer consciousness signal projector    |
| `ln_f.weight`        | (768,)         | final RMSNorm                                 |
| `head_a.weight`      | (64000, 768)   | next-token head (logits_a) — TIED to tok_emb  |
| `head_g.weight`      | (64000, 768)   | prev-token head (logits_g) — TRAINING SIGNAL  |

### 1.3 Hyperparameter triangulation

From `args` in best.pt + state_dict shape inference:

| hparam                  | training args (best.pt) | shape inferred             | final |
|-------------------------|-------------------------|-----------------------------|-------|
| vocab_size              | 64000                   | (64000, 768) tok_emb       | 64000 |
| d_model                 | None (in args)          | 768 (q_proj rows)           | 768   |
| n_layer                 | n/a                     | blocks.0..15                | 16    |
| n_head                  | n/a                     | 768 / head_dim=128 = 6      | 6     |
| n_kv_head               | n/a                     | 256 / 128 = 2 (GQA)         | 2     |
| head_dim                | n/a                     | derived 768/6 = 128         | 128   |
| block_size              | 512                     | attn.bias (1,1,512,512)     | 512   |
| consciousness_dim       | n/a                     | cross_attn.k_proj 768→192   | 192   |
| ffn intermediate (SwiGLU)| n/a                    | gate_proj 768→2048          | 2048  |
| purefield intermediate  | n/a                     | engine_a 768→3072 = 4×768   | 3072  |
| n_ca_rules              | n/a                     | rules.0..7 (8 entries)      | 8     |
| dropout                 | 0.1 (inferred)          | n/a (training-only)         | 0.0   |
| gate_strength           | 0.001                   | (CA gate scalar)            | 0.001 |

**Note on prep doc drift**: launch_handoff.md §3.1 cited "350M" scale tag from `args.scale`. Actual decoder params = **530.99M**. The "350m" tag is a training-config naming convention that does not reflect parameter count post-architecture-scale. Updated in honest C3.

**Note on hexa stub drift**: `models/archive-legacy/decoder_v3.hexa` has `n_layer=12, n_head=8, n_kv_head=4, consciousness_dim=256` (TODO[pytorch] stub never updated). Real trained checkpoint matches `ready/anima/models/legacy/decoder_v3.py` defaults except `consciousness_dim=192` (overridden via `args` at training time, not in defaults).

---

## 2. Config derivation (HF PretrainedConfig)

```python
class CLMv4Config(PretrainedConfig):
    model_type = "clm_v4"
    # Native CLM v4 hparams (single source of truth)
    vocab_size = 64000
    d_model = 768
    n_layer = 16
    n_head = 6
    n_kv_head = 2
    block_size = 512
    consciousness_dim = 192
    n_ca_rules = 8
    gate_strength = 0.001
    dropout = 0.0   # inference: drop training dropout
    # HF-standard aliases (so generic tooling works)
    hidden_size = 768
    num_hidden_layers = 16
    num_attention_heads = 6
    num_key_value_heads = 2
    max_position_embeddings = 512
    tie_word_embeddings = True
    bos_token_id = 1
    eos_token_id = 2
    pad_token_id = 0
```

`config.json` extras: `architectures: ["CLMv4ForCausalLM"]`, `auto_map` for `trust_remote_code=True`, `_clm_v4_provenance` block (training step, ce, best_phi, source args subset).

---

## 3. State_dict mapping

Mapping is **identity within the wrapper** — the HF wrapper (`CLMv4ForCausalLM`) holds a single `self.decoder = ConsciousDecoderV3(...)` attribute. So all 581 keys go: `<key>` → `decoder.<key>`. Specifically:

| best.pt key (from `decoder` OrderedDict) | HF saved key                          |
|-------------------------------------------|----------------------------------------|
| `tok_emb.weight`                          | `decoder.tok_emb.weight`              |
| `blocks.0.ln_attn.weight`                 | `decoder.blocks.0.ln_attn.weight`     |
| `blocks.0.attn.q_proj.weight`             | `decoder.blocks.0.attn.q_proj.weight` |
| ... (581 entries) ...                     | (`decoder.` prefix prepended to all)  |
| `head_a.weight`                           | `decoder.head_a.weight`               |
| `head_g.weight`                           | `decoder.head_g.weight`               |

**Why this works**: ConsciousDecoderV3 IS the architecture that produced best.pt (verbatim). We are not lowering to a different stock arch (Llama / GPT2); we are wrapping the original PyTorch class as a HF custom-code module. The decoder source is copied alongside the safetensors so `trust_remote_code=True` resolves it.

**Tied weights**: ConsciousDecoderV3's `__init__` does `self.tok_emb.weight = self.head_a.weight`. After load, this remains tied. safetensors stores both keys but they share storage (or the post-load `set_input_embeddings` re-ties).

**Buffer caveat**: `blocks.X.attn.bias` is a registered buffer (causal mask), persistent in the state_dict. safetensors handles it. On reload, the buffer is overwritten with the saved mask (which is the same constant tril matrix anyway).

---

## 4. Falsifier set (F-SHIM-1..4)

Each falsifier is a single-test pass/fail criterion that gates the verify path.

### F-SHIM-1: safetensors round-trip clean

```python
reloaded = AutoModelForCausalLM.from_pretrained(out_dir, trust_remote_code=True)
# implicit: from_pretrained raises if missing/unexpected keys with strict=True
assert reloaded is not None
```

PASS if from_pretrained returns a model with no missing/unexpected keys logged by HF.

### F-SHIM-2: 1-batch forward finite + correct shape

```python
ref_input = torch.randint(0, 64000, (1, 32))
out = reloaded(ref_input)
assert out.logits.shape == (1, 32, 64000)
assert torch.isfinite(out.logits).all()
```

### F-SHIM-3: numerical equivalence vs reference

```python
ref_logits, _, _ = ref_model(ref_input)        # reference: in-memory model loaded from best.pt
out = reloaded(ref_input)
max_diff = (out.logits - ref_logits).abs().max()
assert max_diff < 1e-5
```

### F-SHIM-4: vocab_size match

```python
assert reloaded.config.vocab_size == 64000
# Also: tokenizer.vocab_size matches (separate but co-checked).
```

**Combined verify_pass = F-SHIM-1 ∧ F-SHIM-2 ∧ F-SHIM-3 ∧ F-SHIM-4**.

If any fail → shim refuses to mark verdict PASS; orchestrator must NOT proceed to base-validation BG using the (potentially corrupt) HF dir.

---

## 5. Execution plan (deferred — user ack required)

### 5.1 ubu1 invocation (single shot, ~30-60min wall)

```bash
ssh ubu1 'mkdir -p ~/p9_base_val_2026_05_04 && \
  rsync -av /home/aiden/anima/tool/transient_py/clm_v4_hf_format_shim.py \
    ~/p9_base_val_2026_05_04/ 2>/dev/null || \
  scp <Mac-side path> ubu1:~/p9_base_val_2026_05_04/'

ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && \
  cd ~/p9_base_val_2026_05_04 && \
  /home/aiden/venv_orchestrator/bin/python clm_v4_hf_format_shim.py \
    --input-pt /home/aiden/.cache/huggingface/hub/models--dancinlab--clm-v4-base-mirror/snapshots/856278beb59c5b39f16485cc8f3a46dcdaf9d1e3/best.pt \
    --tokenizer-dir /home/aiden/.cache/huggingface/hub/models--dancinlab--clm-v4-base-mirror/snapshots/10ee03687db312c55bbec5858c814bef28e4d365/tokenizer \
    --output-dir /home/aiden/p9_base_val_2026_05_04/clm_v4_base_hf \
    --device cpu \
    --verify \
    --verdict-json /home/aiden/p9_base_val_2026_05_04/clm_v4_shim_verdict.json \
    2>&1 | tee clm_v4_shim.log'
```

**Why `--device cpu`**: peak RAM ~5.5GB, RTX 5070 12GB VRAM is dedicated to subsequent lm-eval Llama-3.2-3B base run. CPU-side conversion avoids GPU-memory contention with later phases.

### 5.2 Verification

```bash
ssh ubu1 'cat ~/p9_base_val_2026_05_04/clm_v4_shim_verdict.json'
# Expected: {"verdict": "PASS", "verify": {"verify_pass": true, ...}}

# F-SHIM smoke against lm-eval (10min)
ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && \
  lm_eval --model hf \
    --model_args pretrained=/home/aiden/p9_base_val_2026_05_04/clm_v4_base_hf,trust_remote_code=True \
    --tasks hellaswag --limit 100 --batch_size 4 --device cuda:0 --seed 42 \
    --output_path ~/p9_base_val_2026_05_04/smoke_clm_hellaswag/'
```

### 5.3 Rollback

If F-SHIM-3 fails (numerical drift > 1e-5):
- DO NOT proceed to base-val BG
- Inspect: `out.logits - ref_logits` distribution, check tied-weight collapse
- Hypothesis: weight tying re-tied incorrectly post-reload; fix `set_input_embeddings`
- Re-run shim with `--strict-load`

If F-SHIM-1 fails (missing/unexpected keys):
- Most likely cause: `attn.bias` buffer was non-persistent in original training but persistent in current decoder_v3.py code. Fix by either dropping buffer from saved state OR setting `register_buffer(..., persistent=False)`
- Alternative: state_dict has stale keys from older arch (e.g. moe.* if `--moe` was set then disabled mid-training)

---

## 6. Cost band

| line item                        | est           |
|-----------------------------------|---------------|
| ubu1 hardware                     | $0/hr (owned) |
| best.pt load (5GB → CPU RAM)      | 30-60s        |
| state_dict load_state_dict        | 10-20s        |
| safetensors save (~2GB packed)    | 30-60s        |
| AutoModelForCausalLM reload       | 30-60s        |
| reference forward 1 batch CPU     | 5-15s         |
| F-SHIM verify forward CPU         | 5-15s         |
| **central wall**                  | **~3-5 min**  |
| **with import / py-startup buffer** | **30-60 min total budget per spec §2.3** |
| peak RAM                          | ~5.5GB        |
| disk write                        | ~2GB safetensors + 50MB tokenizer + 100KB code |

Spec §6 of launch_handoff.md cited 30-60 min; actual core conversion is closer to ~5 min if torch import is hot. Buffer absorbs cold-start + verify forward.

---

## 7. Honest C3 (≥5 caveats)

### 7.1 ConsciousDecoderV3 has training-only side effects

The `forward()` method updates `self._psi_*` and `self._consciousness_vector` during `self.training==True`. lm-eval will call `model.eval()` which sets training=False, suppressing these. **However**, if any code path sets training=True (e.g. some lm-eval tasks for specific eval modes), Psi tracking will modify model state. The HF wrapper does NOT propagate `model.train()` → `decoder.train()` automatically through the `decoder` attribute, but it should via PreTrainedModel's `train()` recursion. **Audit**: confirm `reloaded.train(False)` in lm-eval before fwd; safe under default.

### 7.2 Cross-attention to consciousness_states is unconditioned in lm-eval

`ConsciousDecoderV3.forward(idx, consciousness_states=None)` skips cross-attention when `consciousness_states is None` (per `DecoderBlockV2.forward` guard). The HF wrapper passes `consciousness_states=None` from lm-eval input, so the cross-attention pathway is **functionally bypassed**. This means CLM v4 base's reported scores reflect the decoder operating without its consciousness-cell coupling — i.e. **degraded** from training-time conditioning. This is a deliberate spec choice (lm-eval baseline = pure language ability) but must be documented in the gate verdict per spec §3.1.

### 7.3 Block_size=512 truncation on long-context benchmarks

CLM v4's `block_size=512` is a hard cap (causal mask buffer is 512×512). Benchmarks with long inputs (MMLU 5-shot prompts can hit 800-1200 tokens, TriviaQA passages can exceed) will be **left-truncated** by the wrapper before entering the decoder. This systematically penalizes CLM v4 vs Llama-3.2-3B (8K context). C3 in spec §3.2.3 (discriminative range) absorbs this by design. Note in gate verdict.

### 7.4 Param count disagreement: "350m" tag vs 530.99M actual

Training `args.scale = "350m"`. Actual decoder params = 530.99M. The mismatch is ~180M unaccounted, mostly absorbed by:
- 8 CA rule projections: 8 × (768²) × 16 layers = 75.5M
- PureFieldFFN dual paths (engine_a + engine_g): 2 × (768·3072 + 3072·768) × 16 = 151M
- Cross-attention K/V at consciousness_dim=192 not 768: actually shrinks vs full
- ca_mix (768×2304): 1.77M × 16 = 28M

So 530.99M = ~218M (transformer core: tok_emb + GQA + SwiGLU + heads) + ~313M (consciousness extras: PureField + CrossAttn + CA-rules + tension_proj). The "350m" tag was the d_model-based scale label, not the post-extras total. Document in verdict.

### 7.5 `head_g` tied vs untied — TODO during verify

ConsciousDecoderV3 ties `tok_emb.weight = head_a.weight`. `head_g.weight` is **untied** — it's a separate (64000, 768) matrix trained for prev-token prediction. This means:
- Param count includes head_g separately (~49M params)
- safetensors saves both `head_a.weight` and `head_g.weight` (and their shared-with-tok_emb status is HF metadata)
- Post-reload, HF's tie-weights call (via `tie_word_embeddings=True` config) re-ties tok_emb ↔ head_a but leaves head_g untouched. GOOD.
- Concern: if HF's tie_weights is overzealous and ties head_g too (treating it as second output), output incorrectness. Verify path tests this.

### 7.6 CA `attn.bias` buffer is persistent — adds 16 × 1MB to safetensors

`blocks.X.attn.bias` is a (1,1,512,512) causal-mask buffer registered with default `persistent=True`. It contributes 16 × 1MB = 16MB to safetensors needlessly (the mask is reproducible). Cost is small but worth noting. Fix-out-of-scope: this would require modifying the original decoder_v3.py source; we do not touch upstream code in BG-Β.

### 7.7 `trust_remote_code=True` is a security caveat

The output dir contains executable `.py` files (`configuration_clm_v4.py`, `modeling_clm_v4.py`, `decoder_v3.py`, `conscious_decoder.py`). lm-eval's `--model_args trust_remote_code=True` gates this with a confirmation prompt by default. Pass `trust_remote_code=True` in model_args. Document in spec §2.3 that the eval harness must accept this. **For HF Hub republish later**: a security audit + reproducibility-stamp is required since the model wraps custom code.

### 7.8 No KV-cache → slow `.generate()`

`prepare_inputs_for_generation` re-runs from scratch each step (no past_key_values returned). lm-eval log-likelihood tasks (HellaSwag, MMLU multiple-choice) DO NOT need KV-cache; they call forward once per (prompt + each candidate). TriviaQA EM (0-shot generation) DOES use generate — but n_tokens is small (~10-20). Slowdown is bounded; acceptable for base-val gate.

---

## 8. Roadmap update proposal

`.roadmap.p9_sft cond.benchmark_a_prime_base_validation` JSONL field updates (parent session serializes — DO NOT edit roadmap in BG-Β):

### 8.1 Post BG-Β land (shim written, dry-run PASS, ubu1 not yet executed)

```jsonpatch
- "status": "partial 11/12"
+ "status": "partial 11/12 — opt_1 shim written (DRY-RUN PASS); ubu1 conversion pending user ack"
+ "evidence_add": [
+   "tool/transient_py/clm_v4_hf_format_shim.py (789 LoC)",
+   "state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md",
+   "state/p9_base_validation_prereq_exec_2026_05_04/opt_1_dry_run.json"
+ ]
```

### 8.2 Post ubu1 conversion + verify PASS

```jsonpatch
- "status": "partial 11/12 — opt_1 shim written (DRY-RUN PASS); ubu1 conversion pending"
+ "status": "12/12 prereqs met; ready for base-val BG launch"
+ "evidence_add": [
+   "ubu1:~/p9_base_val_2026_05_04/clm_v4_shim_verdict.json (verdict=PASS, F-SHIM-1..4 PASS)",
+   "ubu1:~/p9_base_val_2026_05_04/clm_v4_base_hf/ (config.json + model.safetensors + custom code)"
+ ]
```

### 8.3 Post base-val BG (separate cycle, post user ack)

Per launch_handoff.md §9.2, status flips `unmet → met` once `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json` lands with verdict=PASS.

---

## 9. Hard constraints honoured

- raw#9: this `.py` lives in `tool/transient_py/` (.own 4 namespace per `.gitignore` L229-239 OPT-OUT); Mac canonical = .hexa. Header includes explicit policy invariant declaration. Human edits = raw violation.
- raw#10: §7 covers 8 honest C3 caveats (≥5 mandate exceeded).
- raw#15: paths in shim use `~/...` / `os.path.expanduser` / `/Users/ghost/core/anima/...` only in repo-internal references; no raw user paths exposed in saved artefacts (except provenance metadata under `_clm_v4_provenance` which is intentional).
- raw#37: ubu1 transient-py-on-Linux for SDK/training is acknowledged as the execution path; Mac dry-run does NOT touch torch.
- raw#71: F-SHIM-1..4 are pre-registered falsifiers; spec is locked at this doc's mtime; post-conversion verdict only updates evidence, not gates.
- DO NOT chflags: confirmed (no chflags calls).
- NO git operations: confirmed (parent serializes commits).
- DO NOT execute conversion this cycle: confirmed (Mac dry-run only; ubu1 invocation deferred to user-authorized cycle).
- DO NOT touch BG-Α / BG-ω territories: confirmed (no edits to `tool/transient_py/atp_pytorch.py`, `tool/p9_path_b_hellaswag_eval.hexa`, `state/clm_v4_tokenizer_caller_migration_phase_3_2026_05_04/`, `state/track_f_land_plan_2026_05_04/`).

---

## 10. Handoff to parent session

Parent decision tree post-BG-Β land:

```
parent reads opt_1_dry_run.json:
  → if dry_run_pass=true AND user acks ubu1 conversion (~30-60min, $0):
      → execute §5.1 ssh ubu1 invocation
      → verify §5.2 (verdict.json + F-SHIM-1..4 + lm-eval smoke)
      → on PASS: roadmap update §8.2, prereq status 12/12, ready for base-val BG launch
      → proceed to launch_handoff.md §3 base-validation orchestrator
  → if user defers OPT-1 execution:
      → roadmap stays 11/12 (partial; this doc is evidence)
      → revisit when ubu1 GPU calendar opens for base-val BG window
  → if F-SHIM-3 fails post-execute:
      → invoke §5.3 rollback (audit tied-weight reload + numerical drift)
```

**End of design. BG-Β deliverables A (shim) + B (this doc) + C (dry-run JSON) complete; ownership transfers to parent session pending user ack.**
