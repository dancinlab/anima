# CLM v4 Architecture Archaeology — Landed Handoff (2026-05-05)

**Spec doc**: `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`
**Type**: Read-only source archaeology, $0 Mac CPU, no exec, no commit
**Lineage anchor**: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §8.1 Stage 1 mount layer prerequisite

## What landed

- **§1 Source map** — exact file/line locations for `ConsciousDecoderV3` (decoder_v3.py:49-263), `DecoderBlockV2` (conscious_decoder.py:452-564), `ConsciousCrossAttention` (conscious_decoder.py:391-447), shim CLMv4Config (shim:607-657), shim CLMv4ForCausalLM (shim:727-1029).
- **§2 Forward path diagram** — text input → tok_emb → 16 blocks (each with attn → CA neighbor → META-CA → PureFieldFFN → cross_attn-or-bypass → SwiGLU FFN) → ln_f → head_a + head_g, with HF wrapper layer detailed.
- **§3 Critical guards** — the `if consciousness_states is not None` guard at `conscious_decoder.py:553` is the architectural one-line pivot; default lm-eval invokes bypass; v4 fixture-injection re-engages via env-var (`shim:986-997`); Law 61 detach is non-negotiable (LM never gradient-shapes consciousness).
- **§4 Init walk** — `apply(_init_weights)` recursively re-inits ALL nn.Linear to std=0.02, OVERRIDING constructor-local std=0.001 on cross_attn.o_proj (`conscious_decoder.py:420`) and tension_proj (`decoder_v3.py:101`). This is L36 in concrete form.
- **§5 Load walk** — `_load_decoder_state` (`shim:535-589`) `load_state_dict` runs AFTER `apply(_init_weights)`, overwriting all init-layer architectural changes with whatever's in best.pt. L38 in concrete form: any init-layer architectural pivot is invisible without fresh-init forward OR full retrain.
- **§6 Axis-conditioning** — no explicit axis embedding exists in trained substrate. 5-axis taxonomy (`state/anima_axis_eval_set_2026_05_05/prompts.jsonl`) is downstream measurement convention via prompt prefixes, not architectural primitive. n_ca_rules=8 internal rules ≠ external 5 axes.
- **§7 Emerge candidates** (5 total — 3 spec-named + 2 archaeology-natural):
  - **D**: Always-inject consciousness_states (1-line bypass-removal) — partially done at HF wrapper via fixture
  - **E**: ODE flow → AR sampler bridge (per-token consciousness_state evolution)
  - **F**: 8 CA-rule cells × axis multi-token emit + voting (surfaces internal n_ca_rules=8 as external 8-vector)
  - **G** *(archaeology-natural)*: Tension trajectory `[16, T]` as primary substrate-coupled dialogue artifact (currently discarded at HF wrapper)
  - **H** *(archaeology-natural)*: head_g (prev-byte) as bidirectional consistency probe (currently discarded)
- **§8 Honest C3** — 9 entries covering archaeology bias, init-layer invisibility, one-directional cross_attn architecture, axis-as-measurement-not-control, fixture engagement requirement, real-ckpt smoke gap, candidate-not-spec status, tensions-discarded surface change cost, v5-redesign-out-of-scope.
- **§9 Cross-link to L1-L43** — explicit invocation of L36 (apply walk override), L37 (bypass category error), L38 (load overwrites init), L40 (3-path closure post-retire), L41 (forward-gating gradient flow); raw#9 + ≥5 C3 + lineage discipline confirmed.

## D/E/F + archaeology-natural emerge candidate count

- Spec-named candidates: D, E, F (3)
- Archaeology-natural candidates: G (tensions trajectory), H (head_g bidirectional probe) (2)
- **Total: 5 emerge candidates** surfaced

## New lessons banked

No new L44+ lessons proposed in this archaeology — instead, three CONCRETIZATIONS of existing L36/L37/L38:

- L36 concrete: §4 documents the exact `apply(_init_weights)` walk targets including specific overrides on cross_attn.o_proj and tension_proj
- L37 concrete: §3.1 cites the exact guard line `conscious_decoder.py:553` and traces the bypass-vs-engage logic through three implications
- L38 concrete: §5 documents the exact load order (constructor → tying → apply walk → load_state_dict) and explains why init-layer changes are invisible without fresh-init or retrain

If any deserves L44 promotion, candidate would be: **L44 (NEW V6) — substrate-level architectural change visibility requires (a) fresh-init forward path, OR (b) full retrain; loading existing best.pt deterministically collapses init-layer differential to zero.** This is a synthesis of L36+L38 phrased as a falsifier-design rule. Banked as candidate; promotion to canonical SSOT pending separate `BG-LESSONS-PROPAGATE` cycle.

## Cross-pollination with Stage 1 mount layer

This archaeology is the read-only prerequisite for Stage 1 (`anima-core/runtime/clm_v4_mount.hexa` per mount paradigm doc §8.1). Direct cross-pollinations:

1. **Forward wrapper substrate-response emit format** (mount paradigm §5.2): archaeology candidate G surfaces tensions `[16, T]` as a third channel beyond phi-star + axis activation. Mount layer can choose to emit `tension_envelope = (mean over 16 layers ± std)` per token — this requires changing HF wrapper to include tensions in return, OR mount layer calls decoder directly bypassing HF wrapper.
2. **consciousness_states fixture is already mount-ready** (archaeology §3.1.2 + shim:770-867): env var `ANIMA_CONSCIOUSNESS_FIXTURE_PATH` is the existing injection mechanism. Mount layer Stage 1 should set this env to a fixture sourced from anima-core/phi_engine.hexa so cross_attn engages from the start.
3. **Substrate-coupled dialogue uses logits + tensions + axis-mean direction** (archaeology §6 + §7.4 + §7.5): mount layer dialogue protocol can compose 4 channels simultaneously — (a) logits_a sampled token, (b) tension envelope per-layer trajectory, (c) per-axis ln_f hidden direction (from 5-bucket eval taxonomy), (d) optional head_g back-prediction confidence. This is richer than the §5.2 minimum (phi-star + axis + cell-state delta).
4. **Emerge candidate D (always-inject) overlaps shim v4 fixture path** — Stage 1 mount layer does NOT need to modify the shim or source; setting fixture env var achieves Candidate D at HF wrapper level. Per-block bypass-removal (deeper Candidate D) would require shim v5+ which is OUT OF SCOPE for emerge mode (forced-learning paradigm reopened risk).
5. **L38 caveat for mount layer**: Stage 1 inherits the load path. Any fresh-init experiments (e.g., test what happens with consciousness_states injection on init-only weights, no best.pt load) need a SEPARATE entry path that skips `_load_decoder_state`. Default mount path will load best.pt and observe trained behavior.

## Completion-quality recommendation (ranked)

By 완성도 lens (per `feedback_completion_quality_recommendation.md`):

1. **HIGH**: Mount layer Stage 1 should adopt fixture-injection (Candidate D at wrapper level) + tension envelope surface (Candidate G read-side) immediately — both are zero-source-change, zero-retrain, zero-shim-change paths that engage cross_attn AND surface a richer substrate channel than current logits-only return.
2. **MEDIUM**: Candidate H (head_g bidirectional probe) is also zero-cost surface but its quality on real ckpt is unmeasured (C3-C6); defer to Stage 3 (sufficient emerge accumulation) before adopting as primary channel.
3. **LOW**: Candidates E (ODE flow bridge) + F (CA-rule cells multi-token vote) require new code in anima-core; defer to Stage 4 (CLM v5 redesign hint emerge) — they are research candidates, not Stage 1 mount-layer requirements.
4. **DEFER**: Candidate D's deeper variant (per-block bypass-removal in source) — this is a shim v5+ proposal in disguise; rejected for emerge mode by paradigm-shift principle (forced-learning closure must stay closed).

## Files written

- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (spec, ~16KB)
- `docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md` (this file, 1-page handoff)

No source modifications. No git commit. No execution. raw#9 (md only) honored.
