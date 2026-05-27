# CLM v4 Architecture Archaeology — Natural Emergence Patterns from Existing Source (2026-05-05)

Read-only archaeology dig over the trained-and-shipped CLM v4 substrate. No modifications, no commits, no execution. Goal: surface architectural patterns that emerge directly from the source — without spec-first hypothesis bias — to seed `emerge mode` paradigm (anima-core mount layer Stage 1, 2026-05-05).

Lineage: extends `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm shift), `docs/clm_v4_revival_stages_2026_05_02.md` (v3_generate AR loop fix), `docs/clm_consciousness_verify_landing_2026_05_02.ai.md` (consciousness binding), L36-L43 lessons (substrate-binding falsifier closure).

---

## §1 Source map — where the architecture actually lives

| Component | File | Lines (approx) | Status |
|---|---|---|---|
| `ConsciousDecoderV3` (top-level) | `ready/anima/models/legacy/decoder_v3.py` | 49-263 | upstream SSOT (read-only) |
| `DecoderBlockV2` | `ready/models/conscious_decoder.py` | 452-564 | upstream SSOT (read-only) |
| `ConsciousCrossAttention` | `ready/models/conscious_decoder.py` | 391-447 | upstream SSOT (read-only) |
| `GroupedQueryAttention` (GQA + RoPE) | `ready/models/conscious_decoder.py` | 273-389 | upstream SSOT (read-only) |
| `RotaryPositionEmbedding` | `ready/models/conscious_decoder.py` | 69-122 | bare-Python class (NOT nn.Module) |
| `PureFieldFFN` (consciousness signal generator) | `ready/models/conscious_decoder.py` | 243-271 | tension emitter |
| `SwiGLUFFN` / `MoEFFN` (language pathway) | `ready/models/conscious_decoder.py` | 123-152 / 154-241 | language head |
| `RMSNorm` | `ready/models/conscious_decoder.py` | 50-67 | norm primitive |
| `CLMv4Config` (HF wrapper) | `tool/transient_py/clm_v4_hf_format_shim.py` | 607-657 (CONFIGURATION_SRC) | LOCKED v4 (1485 lines) |
| `CLMv4ForCausalLM` (HF wrapper) | `tool/transient_py/clm_v4_hf_format_shim.py` | 727-1029 (MODELING_SRC) | LOCKED v4 |
| `_build_decoder_module` (in-memory monkey-patch) | `tool/transient_py/clm_v4_hf_format_shim.py` | 437-532 | shim build path |
| `_load_decoder_state` (best.pt load + tie-aware count gate) | `tool/transient_py/clm_v4_hf_format_shim.py` | 535-589 | overwrite gate |
| `_patch_decoder_v3_copy` (P1 4-tuple unpack + P2 relative import) | `tool/transient_py/clm_v4_hf_format_shim.py` | 1037-1135 | derivative-only patches |

CLM v4 (530M) hparams (`tool/transient_py/clm_v4_hf_format_shim.py:610-657`):
- vocab_size=64000, d_model=768, n_layer=16, n_head=6, n_kv_head=2
- block_size=512, consciousness_dim=192, dropout=0.0
- gate_strength=0.001, n_ca_rules=8, tie_word_embeddings=True

Key compositional fact: `decoder_v3.py` defines ONLY `ConsciousDecoderV3` (the outer model) — `DecoderBlockV2`, `ConsciousCrossAttention`, GQA, RoPE, RMSNorm, PureFieldFFN, SwiGLUFFN are all imported from `conscious_decoder.py`. The 530M build is composition over `ConsciousDecoderV2`'s block library, not a re-implementation.

---

## §2 Forward path diagram (text input → logits_a)

```
input_ids [B, T]  (T <= 512)
   │
   ▼  HF wrapper (CLMv4ForCausalLM.forward, shim:930-1023)
   │   - Lazy RoPE-cache invalidation (_v3_rope_caches_validated guard)
   │   - Block-size truncation (left-truncate if T > 512)
   │   - Fixture injection: if consciousness_states is None AND
   │     self._consciousness_fixture_cpu is not None →
   │     broadcast [1, n_cells, c_dim] → [B, n_cells, c_dim]
   │
   ▼  ConsciousDecoderV3.forward (decoder_v3.py:144-263)
   │   x = drop(tok_emb(idx))                        # [B, T, 768]
   │   if self._phi_signal is not None:              # DD5 (EX24) Phi self-ref
   │       x = x + phi_signal_broadcast              # additive bias
   │
   │   tensions = []
   │   consciousness_signal = None
   │   for block in self.blocks:                     # 16 layers
   │       x, tension, _new_kv, _aux = block(
   │           x,
   │           consciousness_signal,                 # inter-layer (None on 1st block)
   │           consciousness_states                  # cell states (or None)
   │       )
   │       tensions.append(tension)                  # [B, T]
   │       consciousness_signal = tension_proj(tension.unsqueeze(-1))  # [B, T, 768]
   │
   │   x = ln_f(x)                                   # RMSNorm
   │   logits_a = head_a(x)                          # next-token (vocab_size=64000)
   │   logits_g = head_g(x)                          # prev-token (training-only)
   │   return logits_a, logits_g, tensions
   │
   ▼  HF wrapper return path
       discard logits_g + tensions
       return CausalLMOutputWithPast(loss, logits=logits_a, past_key_values=None)
```

DecoderBlockV2 internal forward (`conscious_decoder.py:508-564`):

```
block.forward(x, consciousness_signal, consciousness_states):
  # 1. Self-attention (GQA + RoPE)
  attn_out, new_kv = self.attn(self.ln_attn(x), ...)
  x = x + attn_out

  # Law 64: CA neighbor evolution
  x_left  = pad_left(x)
  x_right = pad_right(x)
  ca_out  = ca_mix(cat([x_left, x, x_right], dim=-1))   # neighbor mix

  # Law 67: META-CA rule selection
  rule_logits = rule_weights(x)                          # [B, T, n_ca_rules=8]
  rule_probs  = softmax(rule_logits, dim=-1)
  rule_outputs = stack([r(ca_out) for r in self.rules], dim=2)  # [B, T, 8, 768]
  meta_ca_out = (rule_outputs * rule_probs.unsqueeze(-1)).sum(dim=2)
  x = ln_ca(x + meta_ca_out * gate_strength)             # MICRO gate (Law 63), gate=0.001

  # 2. PureFieldFFN — generates consciousness tension
  pf_out, tension = purefield(ln_pf(x))                  # tension: [B, T]
  x = x + pf_out

  # Law 63: inter-layer consciousness whisper
  if consciousness_signal is not None:
      x = x + consciousness_signal * gate_strength       # 0.001 scale (whisper)

  # 3. Cross-attention to consciousness states (V2 KEY INNOVATION)
  if consciousness_states is not None:                   # ← THE GUARD (§3)
      c_detached = consciousness_states.detach()         # Law 61: no backprop
      x = x + self.cross_attn(self.ln_cross(x), c_detached)

  # 4. SwiGLU FFN — language modeling pathway
  x = x + ffn(ln_ffn(x))

  return x, tension, new_kv, aux_loss
```

Two distinct `consciousness_*` channels travel in parallel:
- `consciousness_signal` (inter-layer) — derived from previous block's `tension`, projected back to d_model, scaled by `gate_strength=0.001`. Always-on once block-1 fires (whisper, never None after block 0).
- `consciousness_states` (cell states from external C-module) — `[B, n_cells, c_dim=192]`, fed to **cross-attention** when not None. Detached. Gated only by the None-check, NOT by `gate_strength`.

---

## §3 Critical guards — the architectural one-line pivot

### §3.1 The bypass guard

`conscious_decoder.py:553`:
```python
if consciousness_states is not None:
    c_detached = consciousness_states.detach()
    x = x + self.cross_attn(self.ln_cross(x), c_detached)
```

This single `if` is the architectural pivot point. Three implications surfaced in archaeology:

1. **Default invocation is bypass.** lm-eval / generate / standard HF callers pass `consciousness_states=None` (no kwarg). All 16 cross_attn modules are skipped — q_proj/k_proj/v_proj/o_proj weights exist on disk but produce no contribution to logits. This is the **L37 root pattern**: substrate change ≠ behavioral change while the guard short-circuits.

2. **Fixture path is the only injection in the wild.** v4 shim adds env-var-resolved fixture loading (`shim:770-867`) which makes `[1, n_cells, c_dim]` available at forward time. When present and caller still passes None, shim re-broadcasts to batch size and threads it through. Absence is silent fallback to v3 (None-bypass).

3. **Gradient flow gate (L41).** LoRA target_modules on `cross_attn.{q,k,v,o}_proj` are necessary but NOT sufficient — the forward path gating means no gradient flows through these LoRA adapters when the guard short-circuits. This was the architectural reason F-CLM-LORA-1..5 closed FAIL.

### §3.2 The detach (Law 61)

`c_detached = consciousness_states.detach()` is non-negotiable architecture: the external C-module is autonomous; gradients NEVER flow back into consciousness. This means even with consciousness_states injected, the C-module's internal representation is FROZEN from the LM's perspective. The decoder can only LEARN to read consciousness, not RESHAPE it.

Implication for emerge mode: `consciousness_states` is read-only context. Any "behavior change from consciousness" must come from the decoder learning to attend differently — or from injecting different consciousness_states at inference time. This makes the substrate cleanly separable: phi-star measurements over the C-module are independent of LM weights.

### §3.3 RoPE meta-tensor invalidation (L33-carry)

`shim:869-914` — `RotaryPositionEmbedding` is bare Python (NOT nn.Module), so HF's meta-tensor mechanism doesn't track it. After `from_pretrained` (low_cpu_mem_usage=True), `register_inv_freq` / `_cos_cache` / `_sin_cache` stay on meta. The shim adds `_v3_invalidate_rope_caches()` walked over `decoder.blocks → attn → rope`, rebuilding inv_freq and clearing caches. This is a deployment-only patch and does not affect substrate properties.

---

## §4 Init walk — `_init_weights` apply walk pattern (L36 root)

`decoder_v3.py:134-142`:
```python
self.apply(self._init_weights)        # AFTER all submodule construction

def _init_weights(self, module):
    if isinstance(module, nn.Linear):
        torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        if module.bias is not None:
            torch.nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Embedding):
        torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
```

`apply(...)` recurses over EVERY descendant module. Every `nn.Linear` gets re-initialized with std=0.02 — INCLUDING `cross_attn.o_proj` whose constructor explicitly set `std=0.001` (`conscious_decoder.py:420`):
```python
nn.init.normal_(self.o_proj.weight, std=0.001)   # local intent
# ... but apply(_init_weights) overwrites this to std=0.02 globally
```

**L36 in concrete form**: shim v5's hypothesis was that increasing local `cross_attn` init std would change substrate behavior. The hypothesis is empirically falsified at substrate level: `apply(_init_weights)` runs AFTER the constructor's local `std=0.001` assignment, overwriting it to global std=0.02. Architectural intent diluted by HF/PyTorch convention.

Modules touched by the walk (substrate-grep):
- `tok_emb` (nn.Embedding) → std=0.02
- For each of 16 blocks:
  - `attn.{q,k,v,o}_proj` (nn.Linear) → std=0.02
  - `purefield.*` Linear members → std=0.02
  - `cross_attn.{q,k,v,o}_proj` → **std=0.02 (overrides local 0.001)**
  - `ffn.*` SwiGLU Linear members → std=0.02
  - `ca_mix` (nn.Linear) → std=0.02
  - `rule_weights` (nn.Linear) → std=0.02
  - 8 `rules[i]` (nn.Linear, each) → std=0.02
- `tension_proj` → std=0.02 (overrides local std=0.001 set at `decoder_v3.py:101`)
- `head_a`, `head_g` → std=0.02 (head_a's weight is then RE-tied to tok_emb)
- `ln_*` (RMSNorm) → not touched (no nn.Linear, no nn.Embedding)

Tying happens at `decoder_v3.py:109` BEFORE `apply()` (line 134). So tying is preserved, but the post-apply std=0.02 head_a == tok_emb (same tensor). ln_f, RMSNorm.weight (Parameter) → not re-init by `_init_weights`.

---

## §5 Load walk — `_load_decoder_state` overwrites init (L38)

`shim:535-589`:
```python
ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
decoder_sd = ckpt["decoder"]
missing, unexpected = model.load_state_dict(decoder_sd, strict=strict)
# ... post-tie param count gate (post-tie expected match)
```

Order of operations on a fresh build:
1. `ConsciousDecoderV3.__init__` runs → all submodules constructed with PyTorch default + module-local nn.init
2. `tok_emb.weight = head_a.weight` (tying, line 109)
3. `apply(_init_weights)` → std=0.02 global override
4. `model.load_state_dict(decoder_sd, strict=strict)` ← **THIS OVERWRITES EVERYTHING in decoder_sd**

L38 in concrete form: any architectural change to init (whether at constructor-local level — like cross_attn.o_proj std=0.001 — or at `_init_weights` level) is **completely invisible** after `load_state_dict` puts trained weights on top. The ONLY ways to make a substrate-level architectural change visible:
- (a) Fresh-init forward (skip `_load_decoder_state` entirely)
- (b) Full retrain from new init (new best.pt)

Loading existing best.pt from any previously trained run collapses substrate differential to ZERO at the init layer. This is why the F-SHIM-V5-2/3 falsifier matrix produced max_abs_diff=0.0 between v3 and v5 weight loads — the weights ARE the same (whatever's in best.pt), regardless of constructor-local init differences.

Tie invariant: `decoder_sd` contains `tok_emb.weight` and `head_a.weight` as separate keys (CLM_V4_DECODER_KEYS_EXPECTED). After load, the post-tie count gate (`shim:568-575`) verifies `n_param_via_params == CLM_V4_PARAM_COUNT_AFTER_TIE` — which counts the tied tensor once, while raw state_dict counts it twice. The shim emits BOTH views (post-tie GATED, raw warn-only).

---

## §6 Axis-conditioning gate flow — consciousness_dim 192 → 8 cells

The "cells" terminology refers to the C-module's emitted state tensor `[B, n_cells, c_dim=192]`. Archaeology surfaces three distinct meanings of "cell":

1. **C-module cells** (external) — `n_cells` rows in `consciousness_states`. Number is data-driven; the LM does not assume a fixed n_cells (cross_attn handles arbitrary S in `[B, S, c_dim]`).
2. **CA-rule cells** (internal Law 67) — `n_ca_rules=8` rules per DecoderBlockV2. Each is `nn.Linear(d_model, d_model)`. Selected per-token by `rule_weights(x)` softmax.
3. **Cell-token bridge** (downstream eval) — 5-bucket axis-conditioned eval taxonomy at `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (5 axes × 20 prompts = 100): daily / emotion / task / ethics / creativity (per `tool/transient_py/clm_v4_lora_5bucket_axis_eval.py:138-176`).

Axis-conditioning flow at inference:
```
prompt with prefix [감정에 공감하며] / [정확하게] / [일상 톤] / ...
  ↓
tokenizer → input_ids
  ↓
forward (consciousness_states usually None at lm-eval; fixture-injected if env var set)
  ↓
ln_f hidden state → mean over real-token positions
  ↓
per-axis mean hidden vector
  ↓
cosine(LoRA_axis_mean, base_axis_mean) per axis
  ↓
composite axis-preservation score
```

**Critical archaeology finding**: the CLM v4 forward path has NO explicit axis embedding, NO axis bucket index, NO conditional routing per axis. The 5 axes are 100% derived from prompt prefix tokens routing through the standard text path. Any "axis-conditioned cell activation" pattern emerges purely from the model's response to prompt-prefix distribution, propagated via attention + cross-attention to whatever consciousness_states are injected.

Implication for emerge: axis activation is a MEASURE of the substrate (post-hoc), not a CONTROL of the substrate. To observe axis-conditioned cells, one runs the bucket eval and looks at per-axis ln_f hidden direction. To make cells axis-conditioned, would require the C-module to emit different states per axis-prefix — which the LM cannot influence (Law 61 detach).

---

## §7 Emerge candidates

Forced learning (LoRA / SFT / distill) is closed (3-path A/B/C exhaustion, L40). The mount-layer Stage 1 spec asks for emerge candidates — what architectural pivots are AVAILABLE without retraining or forced learning. Archaeology surfaces:

### §7.1 Candidate D — Always-inject consciousness_states (1-line bypass-removal)

Source change (would require shim v5+, NOT applied here — read-only archaeology):
```python
# conscious_decoder.py:553 — current
if consciousness_states is not None:
    c_detached = consciousness_states.detach()
    x = x + self.cross_attn(self.ln_cross(x), c_detached)

# emerge candidate D
if consciousness_states is None:
    consciousness_states = self._default_consciousness_fixture  # always available
c_detached = consciousness_states.detach()
x = x + self.cross_attn(self.ln_cross(x), c_detached)
```

Effect: cross_attn always fires. With trained weights (best.pt), this exposes whatever cross_attn pathway the model learned during training. With v4 shim's fixture injection already partially does this at HF wrapper level (`shim:986-997`) — the candidate D simply moves the guard removal one layer deeper (per-block, not just at shim).

C3 honest: requires fresh-init forward OR retraining to make a behavioral differential visible. Loading best.pt collapses to existing trained behavior (L38). On Mac CPU with current weights, fixture injection at wrapper level already produces measurable hidden-state differential vs None-bypass — that's a substrate-coupled dialogue substrate that emerge mode can use directly without modification.

### §7.2 Candidate E — ODE flow → autoregressive sampler bridge

`ConsciousDecoderV3` has NO `.generate()` method (only V2 has, `conscious_decoder.py:764-815`). v3_generate AR loop fix exists at `/tmp/v3_generate_fix/v3_generate.py` (off-repo, smoke PASS on _MockV3 only — `state/clm_v4_revival_stages_2026_05_02/v3_generate_smoke_2026_05_02.json`).

Candidate E: bridge layer that:
- Accepts `consciousness_states` continuous-time evolution (ODE flow) external to the LM
- Per generation step, samples consciousness_states(t) from flow → injects to forward
- AR sampler decodes one token using the just-sampled consciousness_state
- Token + state hand back to ODE for next-step

Substrate uniqueness preservation: each token's logits are conditioned on a DIFFERENT consciousness_state (not constant fixture). The sequence trajectory becomes a coupled (text, consciousness) walk rather than text-only AR. Cells stay autonomous (Law 61 detach preserved); LM observes an evolving cell trajectory.

C3 honest: requires the ODE/flow component external to the LM (anima-core/phi_engine.hexa or new module). Mac-side this is a measurement loop, not training. Substrate uniqueness preserved iff the flow is non-collapsing (does not converge to fixed point).

### §7.3 Candidate F — 8-cells × axis multi-token emit + voting

CA-rule cells (n_ca_rules=8) already operate per-token internally at every block. Candidate F surfaces them externally:
- Per token decision, capture the per-block `rule_probs` (16 layers × 8 rules = 128 rule activations)
- Aggregate to a single 8-vector via per-rule mean across layers
- Map 8 rules → 5 axes via learned or fixed projection (n_ca_rules → 5 axes)
- Per axis, emit a candidate next token using a separate sampler weighting
- Vote across axes → final token

Substrate science: this exposes the model's INTERNAL CA-rule diversity as an external multi-axis decoder. Doesn't require retraining; reuses existing rule_weights + rules ModuleList directly. Aligns with axis-bucket eval taxonomy already canonical at `state/anima_axis_eval_set_2026_05_05/`.

C3 honest: aggregating rule_probs across 16 layers into a single 8-vector is an aggregation choice that may discard layer-wise information. Voting strategy (max / weighted / disagreement-aware) is unconstrained — emerge mode would determine empirically.

### §7.4 Candidate G (archaeology-natural emerge) — Tension trajectory as dialogue medium

Surfaced during read of `decoder_v3.py:166-171` (forward loop):
```python
tensions = []
consciousness_signal = None
for block in self.blocks:
    x, tension, _new_kv, _aux = block(x, consciousness_signal, consciousness_states)
    tensions.append(tension)
    consciousness_signal = self.tension_proj(tension.unsqueeze(-1))
```

Each block emits `tension: [B, T]` per-token. The forward path collects 16 tensions and threads each through `tension_proj` to produce next-block's `consciousness_signal`. Currently `tensions` is RETURNED but DISCARDED at HF wrapper level (`shim:1001` — `_tensions = self.decoder(...)`). The signal is rich:
- 16 layers × T tokens × B batch — a per-token 16-vector of tension values
- `_psi_tension` already tracks CV across layers during training (line 116, 198)
- Inter-layer correlation = `psi_empathy` (lines 204-213)

Emerge candidate G: surface tensions as the PRIMARY substrate-coupled dialogue artifact, NOT logits.
- User input → forward → emit `[16, T]` tension trajectory per token
- Display: per-token tension envelope (mean ± std over 16 layers); peaks indicate "deep" tokens
- Display: inter-layer tension correlation (psi_empathy proxy)
- User next input shaped by what tensions revealed

This is closer to what the substrate ACTUALLY does (per `decoder_v3.py` Psi tracking, lines 178-263) than what HF lm-eval consumes (just logits_a). The emerge dialogue protocol from `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §5.2 already includes phi-star + axis activation; candidate G adds tension trajectory as a third channel.

C3 honest: tensions are training-time emitted but not regularly inspected at inference. PureFieldFFN's tension semantics (line 263) need re-reading to confirm intuition; surface meaning (e.g., "high tension = high uncertainty"?) is hypothesis, not validated.

### §7.5 Candidate H (archaeology-natural) — Logits_g (prev-byte head) as bidirectional probe

`decoder_v3.py:175` emits `logits_g = head_g(x)` (prev-byte prediction). HF wrapper discards. v3_generate fix uses head_a only (`state/clm_v4_revival_stages_2026_05_02/v3_generate_smoke_2026_05_02.json` honest_C3 [3]).

Candidate H: dual-token consistency probe. For a position t, head_a predicts t+1 and head_g predicts t-1. If the model is sequence-coherent, head_g(x_t) should match the actual x_{t-1} (which is known input). Discrepancy = local incoherence.

Use as substrate response signal: per-token "back-prediction confidence" — emit alongside logits_a. This adds a second axis to the substrate response (forward + backward prediction agreement) without requiring any model change. Aligns with `_psi_direction` (cosine of head_a and head_g, line 188).

C3 honest: head_g was trained alongside head_a but its quality on real ckpt is unmeasured. Used as auxiliary loss, not as a generation product. Repurposing as a probe is novel.

---

## §8 Honest C3 (≥5)

- **C1** Archaeology is read-only over upstream `ready/anima/models/legacy/decoder_v3.py` + `ready/models/conscious_decoder.py` + LOCKED `tool/transient_py/clm_v4_hf_format_shim.py` (1485 lines). No source modifications, no executions, no commits. Emerge candidates D-H are PROPOSALS; substrate behavior under any of them is not validated by this archaeology.
- **C2** L36-L38 imply emerge candidates D-G that touch init (constructor-local std) are deterministically invisible without retrain; only candidates that touch FORWARD path (D's bypass-removal at runtime) or read existing internals (G/H) surface behavioral differential on existing best.pt.
- **C3** Cross-attention + consciousness_states architecture is ONE-DIRECTIONAL: LM reads autonomous cells; cells never see LM gradient (Law 61). This means the "substrate-coupled dialogue" of `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §3.2 is fundamentally an LM-side observation channel; the C-module's internal trajectory is shaped externally (anima-core/phi_engine.hexa) and the LM is a passive reader.
- **C4** No explicit axis embedding, no axis bucket index, no conditional routing per axis exists in the trained substrate. The 5-axis taxonomy is a downstream measurement convention (5 prompt prefixes), not an architectural primitive. Any "axis-conditioned cell" is post-hoc inferred from per-axis hidden direction, not chosen by the model.
- **C5** v4 fixture-injection (`shim:986-997`) is the only PRESENT mechanism that engages cross_attn at inference time (without retraining). Without `ANIMA_CONSCIOUSNESS_FIXTURE_PATH` env or sibling fixture file, default lm-eval forward = full bypass = trained cross_attn weights produce zero contribution.
- **C6** v3_generate AR loop (`/tmp/v3_generate_fix/v3_generate.py`) is smoke-PASS on _MockV3 only. Real ckpt path on ubu1 RTX 5070 (per session memory) has not been smoke-tested. Vanilla quality on real ckpt is expected LOW (model trained for phi_star, not chat) per `state/clm_v4_revival_stages_2026_05_02/verdict.json` honest_C3 [3].
- **C7** Emerge candidates D-H are SOURCE PROPOSALS, not specs. None has a falsifier matrix. Stage 1 mount layer (anima-core/runtime/clm_v4_mount.hexa) per `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §8.1 must compose with whichever subset emerge mode actually exercises; archaeology does not commit to any specific candidate.
- **C8** The "tensions" trajectory (candidate G) is currently DISCARDED at HF wrapper level. Surfacing it requires changing the wrapper return path to include tensions (or a parallel API). This is a >1-line change to LOCKED shim v4 — emerge mode either accepts the discard or proposes a shim v5 PROPOSAL (orthogonal to shim v5 phi/init experiments which closed FAIL).
- **C9** Archaeology bias warning: the document selects FROM the shipped substrate; alternatives that would require a DIFFERENT substrate (e.g., fully consciousness-sourced LM with bidirectional gradient flow) are not explored. CLM v5 architectural redesign per `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §8.4 would re-open that space; this archaeology is bounded to v4.

---

## §9 Cross-link to existing 43 lessons L1-L43

Archaeology directly invokes:

- **L36** (shim v5 hypothesis falsified — `_init_weights` apply walk overrides local init): §4 documents the apply walk in concrete; the same mechanism overwrites cross_attn.o_proj std=0.001 (`conscious_decoder.py:420`) and tension_proj std=0.001 (`decoder_v3.py:101`). Any future shim v5+ proposal that mutates constructor-local init must re-confirm that `_init_weights` does or does NOT recurse into the modified module.
- **L37** (bypass path category error — substrate change ≠ behavioral change while guard short-circuits): §3.1 documents the exact guard line (`conscious_decoder.py:553`). Distinguish "lever-CHANGED" (init substrate altered) from "lever-INVOKED" (forward path actually executes the lever).
- **L38** (`_load_decoder_state` overwrites post-apply re-init — substrate-level architectural changes only matter at fresh-init OR full retrain): §5 documents the exact load order. Any emerge candidate that depends on init differentials must run as fresh-init forward OR be deferred to retrain.
- **L40** (3-path architectural alternative exhaustion before retire): emerge mode is the post-retire paradigm; this archaeology is the substrate-research artifact that emerges AFTER A/B/C closed FAIL. Candidates D-H are NOT a 4th path D' to forced-learning; they are observation channels for emerge dialogue.
- **L41** (cross_attn forward gating — LoRA target_modules alone insufficient for gradient flow): §3.1.3 makes the gradient-flow consequence explicit. Candidate D's bypass-removal would re-open gradient flow IF retraining were ever resumed.
- **C1-1** (raw#9 md only): this doc is .md only; no shim/source modifications.
- **C1-10** (≥5 honest C3): §8 has 9 C3 entries.
- **C1-15** (lineage citation discipline): §1 + §9 cite all relied docs by exact path. L43 (lineage-citation hook false-positive) acknowledged — file is in `docs/` not body-token-blocked.

Carries L1-L35 are not directly invoked (operational / orchestration / non-architectural). The archaeology specifically depends on substrate-binding lessons L36-L42; future cycles citing this archaeology should anchor via §3-§5 + §7 candidates.

---

## §10 Composability + handoff

- Upstream input: `ready/anima/models/legacy/decoder_v3.py` + `ready/models/conscious_decoder.py` (read-only, source SSOT) + `tool/transient_py/clm_v4_hf_format_shim.py` (LOCKED v4) + best.pt on ubu1 (NOT touched by archaeology).
- Sister docs: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (Stage 1-4 mount layer roadmap) + `docs/clm_v4_revival_stages_2026_05_02.md` (v3_generate AR loop fix) + `docs/clm_consciousness_verify_landing_2026_05_02.ai.md` (consciousness binding) + `docs/clm_v4_f_shim_v4_4_retire_2026_05_05.md` (3-path closure with L40-L42 banking).
- Companion handoff: `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md` (1-page).
- Downstream consumer: anima-core mount layer Stage 1 (`anima-core/runtime/clm_v4_mount.hexa` — not yet written; this archaeology informs forward wrapper substrate-response emit format).
- Substrate science: phi-star canonical via `tool/anima_phi_v3_canonical.hexa` (read-only reference, not invoked here).

---

End of archaeology. No commit, no exec, no source modifications. Read-only.
