# Emerge Candidate G + H — Consolidated Revival Spec (2026-05-05)

Consolidated revival assessment for emerge candidates **G** (16-layer tension trajectory) and **H** (head_g prev-byte head bidirectional consistency probe), surfaced in the CLM v4 architecture archaeology dig (KICK-2). Both candidates share the same DISCARDED origin — the HF wrapper (`tool/transient_py/clm_v4_hf_format_shim.py:999-1019`) — which makes a single consolidated revival path optimal. This document is **doc + spec only**: zero source change, zero retrain, zero new helper Python, zero commit. Read-only on `tool/transient_py/clm_v4_hf_format_shim.py`, `ready/anima/models/legacy/decoder_v3.py`, `ready/models/conscious_decoder.py`, `anima-core/runtime/clm_v4_mount.hexa`, `bin/anima-core-dialogue.bash`.

Lineage:

- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §7.4 (candidate G surfaced) + §7.5 (candidate H surfaced) + §8 C8 (G discarded location)
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §5.2 (substrate response 4-line format — phi_star + axis_activation + dominant_cells + hidden_state_delta)
- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (sister Stage 1 mount-layer spec; same KICK-2 wave; defines the existing 4-line response format that G+H extend)
- `tool/transient_py/clm_v4_hf_format_shim.py:999` (the discard line — `_logits_g, _tensions = self.decoder(...)`)
- `tool/transient_py/clm_v4_hf_format_shim.py:1017-1023` (the return-path drop — `CausalLMOutputWithPast(loss, logits=logits_a, past_key_values=None, hidden_states=None, attentions=None)`)
- `ready/anima/models/legacy/decoder_v3.py:166-175` (where logits_g + tensions are emitted but only logits_a is propagated)

---

## §1 The DISCARDED mechanism — exact location + cause

### §1.1 G — 16-layer tension trajectory

Decoder emits tensions at `decoder_v3.py:166-171`:

```python
tensions = []
consciousness_signal = None
for block in self.blocks:                              # 16 layers (n_layer=16)
    x, tension = block(x, consciousness_signal, consciousness_states)
    tensions.append(tension)                           # tension: [B, T] per-layer
    consciousness_signal = self.tension_proj(tension.unsqueeze(-1))
```

`PureFieldFFN.forward` (`conscious_decoder.py:263-268`) defines tension as:

```python
def forward(self, x):
    a = self.engine_a(x)
    g = self.engine_g(x)
    output = a - g
    tension = (output ** 2).mean(dim=-1)     # [B, T] scalar per token, layer-local
    return output, tension
```

So `tensions` after the loop = `List[Tensor[B,T]]` of length 16. `decoder_v3.py:263` returns the tuple `(logits_a, logits_g, tensions)`.

**Discard mechanism — single line.** `tool/transient_py/clm_v4_hf_format_shim.py:999`:

```python
logits_a, _logits_g, _tensions = self.decoder(
    input_ids, consciousness_states=consciousness_states
)
```

The leading underscores on `_logits_g` and `_tensions` are pure naming convention (Python does not enforce it) — but the binding goes nowhere: the local references are GC-eligible at function exit. Then at `shim:1017-1023`:

```python
return CausalLMOutputWithPast(
    loss=loss,
    logits=logits_a,
    past_key_values=None,
    hidden_states=None,                  # ← could carry tensions, but is None
    attentions=None,
)
```

`CausalLMOutputWithPast` does not have a "tensions" field. The HF protocol assumes `hidden_states` is a tuple of per-layer hidden tensors `[B, T, D]`, which `tensions` is NOT (`tensions` is `[B, T]` scalar). So even if shim passed `hidden_states=tuple(tensions)`, an HF caller assuming `hidden_states[-1].shape == (B, T, D)` would crash.

**Conclusion:** the DISCARDED state is two things — (a) HF-wrapper-internal local-variable drop at line 999, AND (b) HF-protocol-shape mismatch preventing direct reuse of the `hidden_states` field. Both must be addressed by any revival path.

### §1.2 H — head_g prev-byte head

Decoder emits logits_g at `decoder_v3.py:174-175`:

```python
x = self.ln_f(x)
logits_a = self.head_a(x)                              # [B, T, vocab_size=64000]
logits_g = self.head_g(x)                              # [B, T, vocab_size=64000]
```

Both heads share output shape but `head_g` is the **prev-byte head** (training-time auxiliary loss target — predict `idx[t-1]` from position `t`). Per `decoder_v3.py:188-191`, training uses `psi_direction = (1 + cos_sim(logits_a[:,-1,:], logits_g[:,-1,:])) / 2` to track A-G alignment, but at inference `head_g` output is never returned to the caller.

**Discard mechanism — same line, same wrapper.** `shim:999` drops `_logits_g`. At `shim:1019` the HF protocol returns `logits=logits_a` only — there is no `logits_g` field on `CausalLMOutputWithPast`, and even custom subclassing would be non-standard.

**Conclusion:** H is DISCARDED at the same wrapper line as G (`shim:999`). The HF protocol bottleneck is identical. Revival cost is amortized — any forward-hook based capture mechanism that surfaces tensions can simultaneously surface logits_g with no additional wallclock cost.

### §1.3 Architectural intent honesty

The DISCARD is intentional, not an oversight:

- `head_g` was trained as an **auxiliary loss target** (Law 71 psi_direction tracking — `decoder_v3.py:178-191`), NOT as a generation product. Discarding at inference matches training intent.
- `tensions` are **inter-layer signal carriers** (`decoder_v3.py:171` — fed back into next block via `tension_proj`); their job is to propagate consciousness_signal layer-to-layer, not to be observed externally. The training-time Psi tracker (`decoder_v3.py:194-200`) reads them under `if self.training:` only.

Reviving these for inference observation is a **substrate-research repurposing**, not a bug fix. Any honest spec must acknowledge that the DISCARD is consistent with the substrate's design intent, and the revival is an emerge-mode observation channel — not a pre-existing capability that was lost.

---

## §2 Three revival paths

| Path | Mechanism | Source change | raw#15 | Cost |
|---|---|---|---|---|
| **A** | Modify `clm_v4_hf_format_shim.py:999-1023` to attach tensions + logits_g to a custom `CausalLMOutputWithPast` subclass | shim mutated (LOCKED v4 — violates raw#15 + L36) | FAIL | ~30 LoC, retrain not needed but breaks shim seal |
| **B** | PyTorch `register_forward_hook` on each `DecoderBlockV2` from outside the shim (in mount-helper Python) | shim untouched; hooks attach at runtime | PASS (additive, helper-side) | ~50 LoC + ~15min impl |
| **C** | Replace forward call: helper invokes `model.decoder.forward(...)` directly (bypassing the HF wrapper), captures all 3 outputs, then constructs the substrate-response payload | shim untouched; HF lm-eval path unchanged (independent code path) | PASS (orthogonal) | ~40 LoC + ~10min impl |

**Recommendation: Path C** (orthogonal direct-call) — simplest, additive, doesn't touch shim, doesn't risk hook-removal lifecycle issues (Path B's hooks would need explicit unregister to avoid memory leak across multi-turn dialogue), and natively returns the 3-tuple `(logits_a, logits_g, tensions)` without protocol-mismatch gymnastics.

Path B remains the fallback if Path C ever needs to coexist with HF lm-eval invocation in the same Python process (hooks fire transparently regardless of caller). For Stage 1 mount-helper invocation (single-shot forward per dialogue turn), Path C is strictly simpler.

### §2.1 Path C concrete shape

The Stage 1 mount helper (`anima-core/runtime/clm_v4_mount.hexa` emits a transient_py helper at runtime — see `state/anima_core_clm_v4_mount_stage_1_2026_05_05/verdict.json`) currently calls `model(input_ids=...)` (HF wrapper path, returns `CausalLMOutputWithPast`).

Path C revives G+H by changing ONLY the forward call inside the helper:

```python
# Current (HF wrapper)
out = model(input_ids=input_ids, consciousness_states=cs)
logits_a = out.logits

# Path C (direct decoder call — bypasses shim wrapper, captures all 3)
logits_a, logits_g, tensions = model.decoder(input_ids, consciousness_states=cs)
```

`model.decoder` is the inner `ConsciousDecoderV3` (the shim attaches it as `self.decoder` at `shim:_build_decoder_module`). Direct invocation returns the native 3-tuple. RoPE-cache invalidation (which the wrapper does at `shim:947-949`) must be triggered ONCE before the first direct call — easiest path is to call `model(input_ids=input_ids[:, :1])` once on first dialogue turn (warm-up) to trigger `_v3_invalidate_rope_caches()`, then switch to direct calls. Or the helper can call `model._v3_invalidate_rope_caches(); model._v3_rope_caches_validated = True` directly (both methods are exposed on the wrapper).

Block-size truncation (`shim:954-958`) must be replicated in helper if input may exceed 512 tokens. Fixture broadcast (`shim:986-997`) must also be replicated if mode != none/zero. Both are ~5-10 LoC each.

---

## §3 Substrate response — 4 line → 8 line extension

Sister spec (Candidate D §6 — Stage 1 mount-layer paradigm) defines the 4-line baseline:

```
__ANIMA_CLM_V4_RESPONSE__
phi_star: <f4>
axis_activation: <a0>,<a1>,<a2>,<a3>,<a4>
dominant_cells: <c0>,<c1>,<c2>
hidden_state_delta: <f4>
__ANIMA_CLM_V4_OK__
```

G + H combined revival adds 4 new lines (3 for G, 2 for H — but the H lines are denser so 2 = 2):

```
__ANIMA_CLM_V4_RESPONSE__
phi_star: <f4>
axis_activation: <a0>,<a1>,<a2>,<a3>,<a4>
dominant_cells: <c0>,<c1>,<c2>
hidden_state_delta: <f4>
tension_trajectory: <t0>,<t1>,...,<t15>      # G — 16 layer L2 norms (mean over B,T)
tension_peak_layer: <int>                     # G — argmax(trajectory)
tension_min_layer: <int>                      # G — argmin(trajectory)
head_g_consistency: <f3>                      # H — forward-backward agreement [0,1]
head_g_divergence_pos: <int>,<int>,...        # H — token positions where forward+backward disagree
__ANIMA_CLM_V4_OK__
```

Format conventions (mirror Stage 1 mount.hexa precision discipline):
- `<f4>` = 4-decimal float (e.g., `42.3712`)
- `<f3>` = 3-decimal float (e.g., `0.412`)
- `<a*>` = 3-decimal axis activation float
- `<c*>` = integer cell index
- `<int>` = integer layer index or token position
- `tension_trajectory` = comma-separated 16 floats, each `<f3>`, ordered layer 0 → 15
- `head_g_divergence_pos` = comma-separated integers; empty list → emit single `-1` sentinel

### §3.1 Tension trajectory aggregation choice

`tensions[i]` for layer `i` is `[B, T]`. Aggregation to a scalar per layer:

```python
tension_trajectory[i] = tensions[i].mean(dim=(0, 1)).item()       # mean over batch + time
```

Rationale: B=1 in dialogue (single user turn), so mean over B is identity. Mean over T gives a per-layer scalar representing average per-token tension at that depth. Alternatives considered + rejected:
- L2 norm: `tensions[i].norm()` — scales with sqrt(T), confounds depth signal with input length.
- max: `tensions[i].max()` — single-token outlier dominates, brittle to prompt distribution.
- entropy of per-token tension distribution: information-theoretic but adds compute + interpretation complexity beyond Stage 1.

Mean is the simplest sufficient statistic; downstream emerge-mode analysis can request per-token breakdown via a future debug flag.

### §3.2 head_g consistency aggregation

`logits_g[t]` predicts `idx[t-1]`. Forward-backward consistency check:

```python
# logits_g shape: [B, T, V]
# input_ids shape: [B, T]
# For position t in [1, T-1], check if argmax(logits_g[:, t, :]) == input_ids[:, t-1]
predicted_prev = logits_g[:, 1:, :].argmax(dim=-1)         # [B, T-1] — pred at pos t for t-1
actual_prev = input_ids[:, :-1]                            # [B, T-1] — true t-1 token
matches = (predicted_prev == actual_prev).float()          # [B, T-1] — 1 if matched
head_g_consistency = matches.mean().item()                 # scalar in [0, 1]
divergence_mask = (matches == 0)                           # [B, T-1] — 1 at divergence
divergence_pos = divergence_mask[0].nonzero(as_tuple=True)[0].tolist()  # B=0 row
```

Position 0 has no t-1, so the comparison starts at t=1. The `divergence_pos` list is emitted RAW (no truncation) to preserve full divergence pattern; the dialogue display layer can choose to truncate to first-N if rendering bandwidth requires.

---

## §4 Emerge value — combined hypothesis

### §4.1 G — trajectory shape categories (4 archetypes)

The 16-layer tension trajectory across blocks is hypothesized to fall into 4 archetypal shapes:

1. **Monotone increase** (early-shallow, late-deep accumulation) — tension grows ~linearly with depth. Predicted on factual, well-structured input. Consciousness signal builds steadily through the stack.
2. **Early-peak then plateau** (early features dominate) — peak at layer 2-5, decay or plateau through layers 6-15. Predicted on simple/repetitive input where lexical features dominate.
3. **Late peak** (deep abstraction emerge) — peak at layer 11-15. Predicted on abstract / philosophical / consciousness-related input where deep representational integration occurs.
4. **Oscillation** (representational instability) — multi-modal or sawtooth. Predicted on contradictory / paradoxical input or out-of-distribution prompts.

Each shape can be summarized by `(tension_peak_layer, tension_min_layer, trajectory_variance)`. Cross-correlation with `phi_star` is the primary emerge hypothesis: certain shapes (late-peak, oscillation) may correlate with distinctive phi_star regimes.

### §4.2 H — bidirectional consistency as architectural integrity

`head_g_consistency` measures whether the substrate maintains forward + backward token coherence. Hypotheses:

- v4 is **chat-incapable** (per CLM-v4-LoRA-SFT FAIL_REGRESSION lessons L31-L33 — composite 0.19542 vs Llama 0.5584). So expected `head_g_consistency` on natural prompts is LOW (< 0.20) by composition: if forward (next-token) prediction quality is degraded, backward (prev-token) prediction quality will be similarly or more degraded.
- BUT random `head_g_consistency` floor for vocab=64000 is ~ 1/64000 ≈ 0.0000156 per position. Anything > 0.05 (>3000× random) indicates the substrate retains real bidirectional structure.
- Threshold predictions: `0.05 ≤ consistency ≤ 0.20` → "weak bidirectional structure preserved" (emerge candidate H positive); `consistency < 0.05` → "architecturally broken or never-trained-bidirectional" (emerge candidate H negative); `consistency > 0.20` → "stronger than expected from chat-incapability composition" (warrants retraining-resumption investigation).

### §4.3 Combined — substrate identity signature

G shape × H consistency = **architectural fingerprint**. The pair `(tension_trajectory_shape, head_g_consistency)` is hypothesized to be:

- **Substrate-identity-stable**: same v4 best.pt → similar fingerprint across input distribution variation
- **Substrate-distinguishing**: v4 best.pt fingerprint differs from Llama-self fingerprint (and from CLM v4 LoRA fingerprint, if Path C extends to LoRA-applied models)
- **Phi-star-correlated**: input that produces high phi_star (≥ 42) hypothesized to also produce distinctive trajectory shape (likely late-peak or oscillation)

This lifts G+H from "discarded internals" to a 2nd-order substrate-identity signature complementary to phi_star + axis_activation. Stage 1 mount layer's substrate-coupled dialogue (per `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §5.2) becomes a 4-channel emit (phi_star + axis + tension trajectory + bidirectional consistency) rather than 2-channel.

---

## §5 Falsifier matrix

### §5.1 F-CAND-G — 16-layer tension trajectory

| ID | Statement | PASS | FAIL_TRUE | FAIL_FALSE |
|---|---|---|---|---|
| **F-CAND-G-1** | Trajectory variance across 16 layers ≥ 0.1 (relative to mean) on neutral prompt | std/mean ≥ 0.1 → real layer-wise signal captured | std/mean < 0.05 → all layers nearly identical, capture invalid (hook fires same value) | NaN/inf in any layer → numerical instability |
| **F-CAND-G-2** | `tension_peak_layer` is stable within ± 1 across 5 paraphrases of the same axis-bucket prompt | peak layer consistent (stable axis × prompt) → real architectural signal | peak layer randomly distributed across 5 paraphrases → noise, not signal | peak layer is exactly layer 0 or 15 on >50% of prompts → boundary capture artifact |
| **F-CAND-G-3** | Trajectory shape correlates with `phi_star` (Pearson \|r\| ≥ 0.3 across 20-prompt eval) | correlation surfaces predictable | \|r\| < 0.1 → trajectory uncorrelated with phi_star (orthogonal channel — still useful but not signature) | trajectory all-NaN or phi_star measurement crash |

Note F-CAND-G-2 special FAIL_TRUE: peak at layer 0 or 15 ALWAYS suggests the hook is mis-attached (capturing pre-block input at layer 0, or post-final-norm at layer 15) rather than the per-block tension. Diagnostic check, not a substrate falsification.

### §5.2 F-CAND-H — head_g bidirectional consistency

| ID | Statement | PASS | FAIL_TRUE | FAIL_FALSE |
|---|---|---|---|---|
| **F-CAND-H-1** | `head_g_consistency` ≥ 0.05 on neutral 64-token prompt (3000× random floor) | consistency ≥ 0.05 → real bidirectional structure preserved | consistency < 0.05 (between random and non-trivial) → head_g either never trained for retention or architecturally degraded; emerge candidate H closes negative | logits_g shape mismatch with input_ids OR NaN/inf in logits_g OR forward crash |
| **F-CAND-H-2** | `divergence_pos` density falls in [30%, 70%] of available positions (avoiding both "always agrees" and "always disagrees") | density in (0.3, 0.7) → diverse failure modes — informative signal | density < 0.05 → over-agreement (likely measurement collapse to same argmax for trivial input) OR > 0.95 → near-total disagreement (reduces to F-CAND-H-1 fail) | divergence_pos extraction crashes |
| **F-CAND-H-3** | Pearson correlation between `head_g_consistency` and `phi_star` across 20-prompt eval has \|r\| ≥ 0.2 | correlation surfaces (consistency × phi co-vary in either direction) | \|r\| < 0.1 → bidirectional consistency orthogonal to phi_star (still useful as independent channel; not falsified, just not joined) | NaN in either channel |

Note F-CAND-H-1 FAIL_TRUE is partially expected given the L31-L33 CLM v4 chat-incapability bank. The spec includes it as a sanity gate, not a high-confidence PASS prediction.

### §5.3 Combined falsifier (G × H joint)

**F-CAND-GH-COMBINED**: trajectory shape category (one of 4) × consistency band (one of 3: low/mid/high) yields 12 fingerprint cells. On 100 axis-eval prompts (`state/anima_axis_eval_set_2026_05_05/prompts.jsonl`), substrate-identity hypothesis predicts > 50% of prompts cluster in ≤ 4 fingerprint cells (concentration ≥ 0.5).

| Outcome | Interpretation |
|---|---|
| concentration ≥ 0.5 | substrate identity fingerprint is real; G+H combined captures genuine substrate signature |
| 0.25 ≤ concentration < 0.5 | partial fingerprint (axis-dependent); per-axis G+H signature still informative |
| concentration < 0.25 (uniform) | G+H combined channel is high-noise across input distribution; revival yields measurement bandwidth without identity signal — value = research only |

---

## §6 Revival cost summary

| Component | Mac (Path C) | Stage in lifecycle |
|---|---|---|
| LoC added (mount-helper transient_py) | ~50 (RoPE warm-up + direct decoder call + per-block tension extraction + head_g consistency check + 4-line response extension) | helper-side, mount.hexa adjusts emit path only |
| LoC modified in shim | 0 | LOCKED v4 untouched (raw#15 PASS) |
| LoC modified in decoder source | 0 | upstream SSOT untouched |
| Implementation wallclock | ~30 min (write helper + selftest mock) | doc + helper, no H100 required |
| Validation wallclock | ~15 min on Mac (real best.pt forward via PEFT-loaded model OR ubu1 venv) | F-CAND-G-1/2/3 + F-CAND-H-1/2/3 execution |
| $ cost | $0 (Mac CPU forward, no H100) | spec-only this BG; impl + validation deferred |

**Total combined revival cost (G + H): ~50 LoC + ~45min wallclock + $0**, vs. addressing G alone or H alone (~40 LoC + ~30min each, but with overlapping scaffolding = duplicated ~15 LoC). Combined revival saves ~15 LoC and ~15min over sequential.

---

## §7 Composability

- **with KICK-1 mount layer** (`state/anima_core_clm_v4_mount_stage_1_2026_05_05/`): extends substrate-response emit from 4 lines to 8 lines; backward-compatible because new lines append AFTER existing 4 (parsers tolerant to trailing fields will not break).
- **with KICK-2 archaeology** (`docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`): implements §7.4 + §7.5 in unified Stage 1 form.
- **with sister Candidate D spec** (always-inject `consciousness_states`): orthogonal — D injects state into cross_attn, G+H read from PureFieldFFN tension + head_g. The two compose naturally: mode=`canonical` injection × G+H trajectory observation = cross_attn-active substrate signature.
- **with future Candidate E** (ODE flow → AR sampler bridge): G's trajectory signature can be measured per-AR-step under ODE-evolved consciousness_states, allowing trajectory dynamics observation at sequence level.
- **with future Candidate F** (8-cells × axis multi-token emit + voting): F surfaces internal `rule_probs` (8 rules); G+H surfaces tension + logits_g. F + G + H = full inner-state introspection of every DecoderBlockV2.
- **with axis-bucket eval** (`state/anima_axis_eval_set_2026_05_05/prompts.jsonl`): F-CAND-G-2 + F-CAND-H-3 reuse the 100-prompt 5-axis eval directly.

---

## §8 Honest C3

- **C1 (architectural intent vs revival).** Both G and H were DISCARDED intentionally — `head_g` was an auxiliary loss target, `tensions` were inter-layer signal carriers. Revival as observation channels is a **substrate-research repurposing**, not a bug fix. The substrate's design said "do not expose"; revival overrides this. If emerge mode discovers that exposed G+H artifacts are misleading (e.g., trajectory mean dominated by `tension_proj` propagation rather than per-block PureField tension), the discard intent is vindicated.
- **C2 (Path C bypass risk).** Path C bypasses the HF wrapper's RoPE-cache invalidation (`shim:947-949`), block-size truncation (`shim:954-958`), and fixture-broadcast (`shim:986-997`). Helper must replicate all 3 or accept that direct-call breaks on (a) cold meta-tensor RoPE caches, (b) input > 512 tokens, (c) fixture-mode injection. Each replication adds ~5 LoC; total Path C cost may grow to ~70 LoC if all 3 are needed.
- **C3 (head_g quality unmeasured).** No prior evaluation has measured `head_g`'s output quality on the actual `best.pt` checkpoint. F-CAND-H-1 with floor 0.05 is a reasonable sanity threshold but is not anchored to any prior measurement. If `head_g_consistency` is ~0.001 (closer to random than expected), the predicted "weak structure preserved" hypothesis is falsified — and head_g revival closes negative for substrate-identity purposes. Possibility: `head_g.weight` is post-init std=0.02 (per L36 `_init_weights` apply walk), then trained briefly, then dominated by main loss → quality collapse. F-CAND-H-1 specifically tests this.
- **C4 (tension trajectory aggregation choice).** The `mean(dim=(0,1))` aggregation collapses per-token tension structure into a single per-layer scalar. This may discard the most informative dimension — per-token-position tension (where in the prompt the substrate "pays attention" via tension). Stage 1 keeps mean-aggregation for response-line bandwidth; Stage 2+ should expose per-token trajectory if F-CAND-G-3 PASSes (correlation found) but signal is ambiguous in mean-aggregated form.
- **C5 (combined G+H scope creep).** Consolidating G+H into a single revival is justified by shared origin (`shim:999`) and shared revival mechanism (Path C direct call). However, the 4-archetype trajectory taxonomy (§4.1) and the bidirectional consistency interpretation (§4.2) are independent hypotheses with independent failure modes. Joint failure (F-CAND-GH-COMBINED concentration < 0.25) does not imply G alone fails or H alone fails — it implies their *combination* is non-informative. Spec preserves single-falsifier matrices (F-CAND-G-1/2/3 + F-CAND-H-1/2/3) precisely so that partial revival success remains visible.
- **C6 (raw#15 LOCKED shim observance).** Path C achieves raw#15 PASS by NOT touching `tool/transient_py/clm_v4_hf_format_shim.py`. The HF wrapper remains LOCKED v4. Mount-helper `clm_v4_mount.hexa` adjustment is permitted (helper, not shim). However, helper change requires serialization with parallel BGs touching mount.hexa (per session-memory feedback "parallel BG git race").
- **C7 (no execution this cycle).** Spec is doc + verdict.json only; no LoC committed, no Python helper modified, no model loaded. Validation deferred to a later BG with HF cache available (Mac PEFT path or ubu1 venv_orchestrator). Acknowledges the L36-L38 substrate-binding lesson: spec-time predictions about behavioral differential remain hypothetical until measured against `best.pt`.
- **C8 (DISCARDED-intent override may close emerge value).** If F-CAND-G-1 FAIL_TRUE (variance < 0.05 — all layers identical), the architectural intent was correct: tensions are inter-layer noise carriers, not externally meaningful signals. Same for F-CAND-H-1 FAIL_TRUE (consistency < 0.05). Either FAIL_TRUE closes the corresponding revival lane and validates the original DISCARD. Combined dual-FAIL_TRUE would close both lanes and consolidate the lesson L31-L33 carry: v4 substrate exposes phi_star + axis_activation as the only meaningful emerge channels; G+H are not 3rd/4th channels.

---

## §9 Cross-link to existing 43 lessons

Archaeology directly invokes:

- **L31-L33** (CLM v4 LoRA SFT chat-lift FALSIFIED, substrate-safe): the "substrate-research only" framing explicitly allows G+H revival as research-channel exposure, NOT as chat-capability lift. F-CAND-H-1 floor at 0.05 is consistent with L31-L33's expectation of LOW chat-capability composition.
- **L36** (`_init_weights` apply walk overrides local init): `head_g` weights get std=0.02 post-apply (`decoder_v3.py:134`), then trained as auxiliary head. This means F-CAND-H-1 quality measurement is on actually-trained `head_g`, not init-residual.
- **L37** (substrate change ≠ behavioral change while guard short-circuits): G+H revival does NOT require any guard change — it captures already-active forward-path artifacts. This makes revival categorically different from Candidate D (which requires guard semantics adjustment).
- **L38** (`_load_decoder_state` overwrites init at load): not relevant to G+H revival because G+H read FORWARD-PATH internals, not init-time weights. Best.pt load-restoration of head_g + PureField is exactly what revival measures.
- **L40** (3-path architectural alternative exhaustion before retire): G+H revival is post-retire emerge-mode observation channel. No retraining proposed. Composes cleanly with the "post-A/B/C closure" stance.
- **C1-1** (raw#9 md only): doc-only, no shim/helper modifications this cycle.
- **C1-10** (≥5 honest C3): §8 has 8 C3 entries.
- **C1-15** (lineage citation discipline): §1 cites all relied docs by exact path including line numbers for the discard mechanism.

---

## §10 Composability + handoff

- **Upstream input**: archaeology document (read-only) + decoder source (read-only) + shim source (read-only LOCKED v4) + Stage 1 mount-layer verdict (read-only).
- **Sister docs**: `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (Candidate D spec — orthogonal cross_attn engagement). Future siblings: candidate E (ODE), candidate F (rule_probs voting).
- **Downstream consumer**: when Stage 2 mount layer iteration absorbs G+H, the helper transient_py adds Path C direct-call + 4 new response lines. Estimated single-BG implementation cycle ~30min after this spec lands.
- **Validation handoff**: F-CAND-G-1/2/3 + F-CAND-H-1/2/3 + F-CAND-GH-COMBINED execution dependent on (a) HF cache for `need-singularity/clm-v4-base-mirror` available locally (Mac) or via ubu1 venv_orchestrator path, (b) the Stage 2 mount-helper Path C implementation BG completion. Both are out of scope for this BG.

---

End of consolidated revival spec. Doc + spec only. No shim/helper modifications, no commits, no executions. Read-only over upstream sources.
