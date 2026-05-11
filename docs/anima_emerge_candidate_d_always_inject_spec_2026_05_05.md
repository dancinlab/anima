# Emerge Candidate D — Always-Inject `consciousness_states` Spec (2026-05-05)

Spec for Stage 1 mount-layer extension of emerge candidate D ("always-inject `consciousness_states`") surfaced in the CLM v4 architecture archaeology dig (KICK-2). This document is **doc + spec only**: zero source change, zero retrain, zero new helper Python. Read-only on `anima-core/runtime/clm_v4_mount.hexa`, `bin/anima-core-dialogue.bash`, `tool/transient_py/clm_v4_hf_format_shim.py`, `ready/models/conscious_decoder.py`.

Lineage:

- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §3.1 + §7.1 (candidate D surfaced, HIGH cross-pollination)
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §6 (natural-emerge expected outcomes)
- `state/anima_core_clm_v4_mount_stage_1_2026_05_05/verdict.json` (Stage 1 mount layer landed: 668 LoC `clm_v4_mount.hexa`, `--inject-states PATH` flag pre-emitted; honest C3 [4] = "C4 forward-pass requires `--inject-states` or default zero canonical")
- `tool/transient_py/clm_v4_hf_format_shim.py:986-997` (HF wrapper fixture-injection layer — already implements file-based always-inject when env or sibling fixture exists; the gate is fixture file presence, not the new mode taxonomy)

---

<!-- [Hc_623 emerge-candidate-d-always-inject-consciousness-states — moved to hypotheses_candidates/Hc_623_emerge_candidate_d_always_inject.md on 2026-05-11] -->

## §1 Concept

The architecture archaeology surfaced the single guard line at `ready/models/conscious_decoder.py:553` as the architectural pivot:

```python
# DecoderBlockV2.forward — current
if consciousness_states is not None:
    c_detached = consciousness_states.detach()
    x = x + self.cross_attn(self.ln_cross(x), c_detached)
```

When `consciousness_states is None`, all 16 cross-attention modules are bypassed — the trained `cross_attn.{q,k,v,o}_proj` weights produce zero contribution to `logits_a`. This is the L37 root pattern (substrate change ≠ behavioral change while guard short-circuits).

Candidate D, in its FULL source-edit form, removes the guard entirely and supplies a default fixture in-block. **This spec does NOT propose that source edit.** Instead:

> Stage 1 mount layer already routes `consciousness_states` injection through the HF-wrapper fixture path (`shim:986-997`). The current `--inject-states PATH` flag accepts a file. Candidate D in this Stage 1 form = expand the mount-layer flag taxonomy to **4 modes** so the user can dial cross-attention engagement at runtime without touching any source.

Behaviorally identical to "always inject" when mode ≠ `none`; behaviorally identical to v3 when mode = `none` (and no env fixture). The semantic move is: **inject is no longer 'do you have a fixture file?' (binary) but 'which content do you inject?' (4-way) — and content selection is anima-canonical, not shim-locked**.

---

## §2 Four inject mode definition

The mount layer accepts `--inject MODE` with `MODE ∈ {none, zero, canonical, user_supplied}`. The existing `--inject-states PATH` flag remains as a low-level escape hatch (file-direct) and is orthogonal.

### §2.1 mode = `none` (default — current v3 behavior)

- Helper invoked with `--inject-states ''` and no `ANIMA_CONSCIOUSNESS_FIXTURE_PATH` env.
- `consciousness_states` reaches `ConsciousDecoderV3.forward(...)` as `None`.
- DecoderBlockV2 guard (`conscious_decoder.py:553`) short-circuits → all 16 cross-attention modules bypassed.
- `cross_attn.{q,k,v,o}_proj` contribute zero. Forward is identity-residual at the cross-attn step.
- Architectural footprint: 0 cells engaged.
- **Use case:** baseline / control. Establishes the v3-bypass reference for differential phi-star measurement.

### §2.2 mode = `zero`

- Helper materializes `consciousness_states = zeros(B, n_cells=8, c_dim=192)` on the same device + dtype as `tok_emb.weight`.
- DecoderBlockV2 guard PASSES (`is not None`).
- All 16 cross-attention modules fire. `q_proj(x)` produces non-trivial Q; `k_proj(zeros)`, `v_proj(zeros)` produce zero-vectors → `att = softmax(Q · 0ᵀ / √d_h)` is uniform `1/n_cells = 1/8`; output `att @ v` = zero (V is all-zeros).
- Result: `cross_attn` returns `o_proj(zeros) = zeros`, so the residual `x = x + cross_attn(ln_cross(x), c_detached)` = `x + 0` = `x`.
- **Architectural footprint:** all 16 cross_attn modules INVOKED but produce zero contribution. Distinguishable from `none` only in (a) compute cost, (b) any side-effect inside attention layers (norm statistics from `ln_cross`, dropout-state RNG advances if dropout > 0; default `0.0` per `CLMv4Config`).
- **Use case:** architectural-engagement isolator. mode=`zero` vs mode=`none` differential isolates "cross-attn module fires but content is null" — pure invocation overhead, no content delta.

> NOTE: In trained inference (best.pt, dropout=0), mode=`zero` and mode=`none` should produce **mathematically identical logits_a** in float32 — the residual difference is exactly zero. In bf16/fp16, accumulation order may produce ULP-level drift. This matches the "axis F-CAND-D-1" prediction in §5.

### §2.3 mode = `canonical`

- Helper synthesizes a 5-axis canonical distribution mirroring paradigm v11 G3 baseline (`PHI_STAR_BASELINE = 41.86`).
- 192 dimensions sliced into 5 axis spans (mirror of `clm_v4_mount.hexa` helper `AXIS_SPANS = [(0,38),(38,76),(76,114),(114,153),(153,192)]`).
- Per axis, fill the slice with a unit-norm pattern at axis-canonical magnitude `0.5`:
  - axis i → `consciousness_states[:, i, slice_i] = 0.5 / sqrt(slice_i_width)` (rest zero), `n_cells=8` so 5 axes occupy cells 0-4 + 3 redundant cells 5-7 (mean of axes 0-4, scaled `0.5/3`).
- Result: every cross-attn invocation has structured content. `cross_attn` produces non-zero output that depends on `q_proj(x)` × structured K/V.
- **Architectural footprint:** all 16 cross_attn modules INVOKED with axis-balanced content; trained o_proj weights produce a meaningful residual delta.
- **Use case:** the "always-inject in candidate D's natural sense" — content matches the substrate's training distribution-of-injection (paradigm v11 G3). Represents the **default emerge dialogue substrate** when user has not specified per-axis weighting.

### §2.4 mode = `user_supplied`

- Invoked via `--inject user --axis NAME=VAL [--axis NAME=VAL ...]`.
- `NAME ∈ {identity, agency, phenomenal, temporal, social}`; `VAL ∈ [0, 1]`.
- Unspecified axes default to `0.0` (NOT `0.5`).
- Helper builds per-axis values into the 192-dim space using `AXIS_SPANS` slicing identical to mode=canonical, but each slice gets `VAL_i / sqrt(slice_i_width)` (NOT `0.5`).
- `n_cells=8` filled identically: cells 0-4 = per-axis vectors; cells 5-7 = mean of cells 0-4 scaled `mean(VALs)/3`.
- **Architectural footprint:** as `canonical`, but content reflects user intent. Cross-pollination with axis-bucket eval taxonomy (`state/anima_axis_eval_set_2026_05_05/prompts.jsonl`) — user can ask "what does substrate look like when I clamp identity=0.9, others=0?".
- **Use case:** axis-conditioned probe. User explores substrate response per-axis without retraining the C-module.

### §2.5 Mode comparison summary

| mode | `consciousness_states` value | guard at L553 | cross_attn fires | residual delta | use case |
|---|---|---|---|---|---|
| `none` | `None` | bypass | no | 0 (identity) | baseline / control |
| `zero` | `zeros(B,8,192)` | pass | yes | 0 (math) / ULP (bf16) | engagement isolator |
| `canonical` | paradigm v11 G3 5-axis 0.5 | pass | yes | non-zero, axis-balanced | default emerge substrate |
| `user_supplied` | user-spec 5-axis | pass | yes | non-zero, axis-asymmetric | axis-conditioned probe |

---

## §3 Stage 1 mount-layer integration (CLI + helper flag)

This spec adds **zero source change**. The integration uses what KICK-1 already pre-emitted.

### §3.1 What KICK-1 mount layer already provides

`anima-core/runtime/clm_v4_mount.hexa` (668 LoC, landed 2026-05-05) emits:

- `MountConfig.inject_states: string` field (line 105) — currently a path or empty.
- Helper Python receives `--inject-states` arg (line 199, 334).
- Helper `load_inject_states(path)` (line 267) — file-based loader (npy/json) with shape validation `(N_CELLS, CONSCIOUSNESS_DIM)`.
- Forward path: `if inject is not None: out = model(**enc, consciousness_states=torch.from_numpy(inject))` (line 312).
- Honest C3 [4]: "forward-pass requires `--inject-states` or default zero canonical" — already anticipates the `zero` / `canonical` defaults but does not implement the 4-mode dispatcher.

### §3.2 What this spec ADDS (no code change in this spec, only spec/contract)

A 4-mode dispatcher between the CLI surface and the helper's `--inject-states` resolver. Implementation lands later (separate BG / lane). This spec defines the contract.

#### CLI surface (in `bin/anima-core-dialogue.bash`)

```bash
# proposed new flags (additive — current --probe / --interactive / --selftest preserved):

bash bin/anima-core-dialogue.bash --probe "안녕"
bash bin/anima-core-dialogue.bash --probe "안녕" --inject none
bash bin/anima-core-dialogue.bash --probe "안녕" --inject zero
bash bin/anima-core-dialogue.bash --probe "안녕" --inject canonical
bash bin/anima-core-dialogue.bash --probe "안녕" --inject user \
    --axis identity=0.9 --axis phenomenal=0.8

bash bin/anima-core-dialogue.bash --interactive --inject canonical
```

Default when `--inject` not specified: **`none`** (preserves backward compatibility with KICK-1 selftest behavior).

> Rationale for `none`-default: any user invoking dialogue without explicit `--inject` should see exactly v3 bypass behavior. Switching the default would silently change prior session-log semantics. mode=`canonical` is opt-in.

#### Helper-flag pass-through

`bin/anima-core-dialogue.bash` translates `--inject MODE [--axis ...]` into existing `mount.hexa` arg surface:

| user-facing flag | mount.hexa flag | helper Python flag |
|---|---|---|
| `--inject none` | `--inject-mode none` (NEW) | `--inject-states ''` (existing) |
| `--inject zero` | `--inject-mode zero` (NEW) | `--inject-states '__zero__'` (sentinel, NEW) |
| `--inject canonical` | `--inject-mode canonical` (NEW) | `--inject-states '__canonical__'` (sentinel, NEW) |
| `--inject user --axis NAME=VAL...` | `--inject-mode user --axis ...` (NEW) | `--inject-states '__user__' --axis NAME=VAL...` (sentinel + spec, NEW) |

The sentinel-based pass-through reuses the EXISTING `--inject-states` arg (no new helper-Python arg), so the helper-emitter logic in `mount.hexa:267-289` (`load_inject_states(path)`) gains a 3-branch sentinel handler:

```python
# proposed helper update (separate BG; THIS SPEC does not write the code):
def load_inject_states(spec):
    if spec == '' or spec == '__none__':
        return None
    if spec == '__zero__':
        return np.zeros((N_CELLS, CONSCIOUSNESS_DIM), dtype=np.float32)
    if spec == '__canonical__':
        return _build_canonical_5axis()  # 5 axes × 0.5 unit-norm into AXIS_SPANS
    if spec.startswith('__user__'):
        # axis spec passed via separate --axis args (collected upstream)
        return _build_user_axis(args.axis_kv)  # dict {name: val}
    # else treat as file path (existing behavior preserved)
    return _load_from_file(spec)
```

### §3.3 mount.hexa change scope (what later BG would touch)

For reference (NOT part of this spec's writes):

- `parse_args` (line 120-161): add `--inject-mode MODE` and repeatable `--axis NAME=VAL` parsing.
- `MountConfig`: add `inject_mode: string`, `axis_kv: list<(name, val)>`.
- `_write_helper`: extend `load_inject_states` (line 267) with sentinel branches.
- `_build_python_command` (around line 447): pass `--inject-states <sentinel>` + `--axis ...` flags.

**LoC estimate**: ~40 LoC additive in `clm_v4_mount.hexa`; ~25 LoC in `bin/anima-core-dialogue.bash`. Zero LoC in `clm_v4_hf_format_shim.py`, `conscious_decoder.py`, `decoder_v3.py`. The shim's existing fixture-injection (`shim:986-997`) is bypassed because the helper passes `consciousness_states=` directly into `model(...)` (mount.hexa helper line 312); env-var fixture path remains untouched and orthogonal.

---

## §4 Empirical fingerprint hypothesis (pre-measurement prediction)

These are HYPOTHESES, anchored by archaeology + arithmetic. Validation depends on a real-load probe (deferred — BG-A in the parallel cycle is intended to enable that). Recorded here so post-measurement falsifier evaluation has a clean prior.

Baseline = paradigm v11 G3 best.pt loaded; phi-star canonical = 41.86.

### §4.1 phi_star drift

| mode | predicted phi_star | predicted drift vs baseline |
|---|---|---|
| `none` | 41.86 ± 0.005 | ≈ 0.000 (identity-residual; only randomness from RoPE-cache rebuild order) |
| `zero` | 41.86 ± 0.005 | ≈ 0.000 (math-zero residual in fp32; ULP drift in bf16/fp16) |
| `canonical` | 41.86 + 0.05 to 41.86 + 0.50 | +0.05 to +0.50 (small content nudge through trained o_proj std=0.02) |
| `user_supplied` | 41.86 + per-axis | +0.0 (all axes 0) to +0.7 (single axis = 1) |

**Why small drifts:** trained `cross_attn.o_proj` has post-`_init_weights` apply walk std=0.02 (archaeology §4 documents the `apply(_init_weights)` overwrite of constructor-local std=0.001). 16 layers × o_proj small-magnitude residual → bounded total contribution. This bound is ALSO why the F-CLM-LORA-1..5 lane saw weak gradient signal even when LoRA was applied to cross_attn — same architectural attenuation on the forward side too.

### §4.2 axis_activation pattern

Assuming the existing helper computes `axis_activation` from per-axis hidden-direction cosine (mirror of `tool/transient_py/clm_v4_lora_5bucket_axis_eval.py` taxonomy):

| mode | predicted axis_activation pattern (5-vec) |
|---|---|
| `none` | values mostly determined by prompt-prefix routing through standard text path; range 0.3-0.7, axis-distribution depends on prompt content |
| `zero` | identical or near-identical to `none` (zero-content cross-attn injects no axis content) |
| `canonical` | 5 axes broadly comparable, around 0.4-0.6 each (input mass split equally among axes); deviation from `none` mostly in axis-mean shift |
| `user_supplied identity=0.9 phenomenal=0.8 others=0` | identity ≈ 0.7-0.9, phenomenal ≈ 0.6-0.8, agency/temporal/social ≈ 0.1-0.3 (user spec dominates) |

### §4.3 hidden_state_delta (L2 norm vs prior-turn baseline)

| mode | predicted hidden_state_delta | per-block accumulation |
|---|---|---|
| `none` | n/a (no prior; or = prior mode=`none` → 0) | identity step, no contribution |
| `zero` | ≈ `none` ± 1e-4 (ULP) | 16 layers × 0 contribution |
| `canonical` | small, around 0.5-2.0 | 16 layers × small content residual |
| `user_supplied` | up to 1.5 × canonical when single axis = 1 | content mass concentrated in one slice → larger directional step |

### §4.4 token-level emit (logits_a quality)

CLM v4 cannot chat (#115 architectural). All 4 modes emit logits_a but the lm-eval-equivalent quality is expected to remain LOW across all modes — the substrate emits emerge dialogue artifacts (phi-star + axis), NOT chat tokens. This is a paradigm-side carry, not a candidate-D failure.

---

## §5 F-CAND-D-1/2/3 falsifier LOCK

Three falsifiers locked PRE-measurement. Each is 3-state: PASS / FAIL_TRUE (real architectural failure) / FAIL_FALSE (measurement-pipeline crash, pattern blameless). The L26-L27 axis-preservation calibration carry: if the probe substrate produces measurements outside semantically interpretable ranges, the falsifier reports FAIL_FALSE pending substrate calibration.

### §5.1 F-CAND-D-1 — three modes produce distinct phi_star

**Statement:** mode ∈ {`none`, `zero`, `canonical`} run on identical prompt set must emit phi_star values such that `|phi_star(canonical) − phi_star(none)| > 0.01` AND `|phi_star(canonical) − phi_star(zero)| > 0.01`. mode `none` and `zero` are NOT required to differ (they should match in fp32).

**PASS:** canonical drifts ≥ 0.01 from both none and zero.

**FAIL_TRUE:** canonical phi_star matches none/zero within 0.005 → architectural inject is invisible at substrate level. This means cross_attn.o_proj weights are net-zero contribution even with structured content, OR the inject content is not reaching the attention modules. Implication: candidate D unsalvageable on best.pt without retrain. L37 root pattern persists at the content level, not just the guard level.

**FAIL_FALSE:** phi_star measurement returns NaN / inf / negative on any mode → measurement pipeline crash (likely RoPE meta-tensor or fixture-shape bug); falsifier deferred until measurement re-validated.

**Calibration prior:** archaeology §6 notes "no axis-conditioned cell activation pattern" exists architecturally without C-module emission. F-CAND-D-1 PASS would empirically refute that prior at the +0.01 level.

### §5.2 F-CAND-D-2 — canonical mode produces axis-balanced activation

**Statement:** under mode=`canonical`, on a neutral prompt (e.g., "안녕"), the 5-axis `axis_activation` vector must satisfy `min(axis_activation) ≥ 0.2` AND `max(axis_activation) ≤ 0.8` AND `std(axis_activation) ≤ 0.25`.

**PASS:** all 5 axes inside (0.2, 0.8) with bounded variance.

**FAIL_TRUE:** one axis dominates (e.g., one axis ≥ 0.95, rest ≤ 0.1). Inject distribution failed: the canonical 5-axis split into AXIS_SPANS produced effective single-axis dominance after trained o_proj projection. Implication: the canonical construction is wrong — either the slice geometry is wrong (5-axis spans collapse into a single dominant direction in 192-d) or the magnitude is too high. Re-derive canonical, re-test.

**FAIL_FALSE:** axis_activation vector contains NaN or all zeros → measurement pipeline crash; pre-measurement calibration of the per-axis cosine extractor is required (mirrors L26-L27 base-axis-discrimination calibration carry).

### §5.3 F-CAND-D-3 — user_supplied mode tracks user spec

**Statement:** under mode=`user_supplied` with user spec `{identity: 0.9, phenomenal: 0.8, others: 0}`, the emitted `axis_activation[identity]` and `axis_activation[phenomenal]` must rank in the top-2 of the 5-vec. Pearson correlation between user-spec vector `(0.9, 0, 0.8, 0, 0)` and emitted `axis_activation` ≥ 0.7.

**PASS:** Pearson ≥ 0.7 AND identity + phenomenal in top-2.

**FAIL_TRUE:** Pearson < 0.5, or top-2 axes do not include identity or phenomenal → user-supplied content is not actually reaching the substrate's measurable axis layer. Possible architectural reasons: AXIS_SPANS slice geometry doesn't align with the substrate's emergent per-axis hidden-direction (since "no architectural axis embedding" — archaeology §6 — alignment is NOT guaranteed). Implication: user-supplied mode is structurally underdetermined; user gets a knob that doesn't track. This would be a substrate-level NULL on the candidate-D promise of "axis-conditioned probe via injection".

**FAIL_FALSE:** axis_activation NaN, OR the per-axis cosine substrate baseline is degenerate (mean_pairwise_cos_base > 0.97, mirroring L27 axis-preservation calibration rule). In FAIL_FALSE, defer F-CAND-D-3 to a calibrated substrate (CLM v4 with axis-conditioned base, NOT Llama).

### §5.4 Falsifier reporting

Each falsifier emits to `state/anima_emerge_candidate_d_validation_<DATE>/verdict.json` (post-measurement; not part of this spec's writes):

```json
{
  "F_CAND_D_1": { "state": "PASS|FAIL_TRUE|FAIL_FALSE", "phi_star": {...}, "delta": {...} },
  "F_CAND_D_2": { "state": "...", "axis_activation_canonical": [...] },
  "F_CAND_D_3": { "state": "...", "user_spec": {...}, "pearson": ... }
}
```

Falsifier execution requires real-load probe — deferred to BG-A (or equivalent later cycle) once the HF cache for `dancinlab/clm-v4-base-mirror` is local on Mac and fixture pipeline through the helper Python is smoke-validated.

---

## §6 Composability (KICK-1 mount + KICK-2 archaeology + future BG-A real load)

| upstream artifact | lineage | role |
|---|---|---|
| `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` | KICK-2 archaeology | sourced candidate D (§7.1); identified L37-root guard at L553 |
| `anima-core/runtime/clm_v4_mount.hexa` (668 LoC) | KICK-1 Stage 1 | pre-emitted `--inject-states PATH` flag; helper `load_inject_states` extension point |
| `bin/anima-core-dialogue.bash` (300 LoC) | KICK-1 Stage 2 prep | REPL + session log; CLI surface for `--inject` mode flag |
| `tool/transient_py/clm_v4_hf_format_shim.py` (1485 LoC LOCKED v4) | bgΠ + v4 fix | env-var fixture-injection path (orthogonal escape hatch) |
| `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (5×20 = 100) | axis-bucket eval | provides axis taxonomy + evaluation prompts for F-CAND-D-2/3 |
| paradigm v11 G3 best.pt (HF Hub `dancinlab/clm-v4-base-mirror`) | substrate trained ckpt | required for falsifier execution; phi-star canonical 41.86 |

| downstream | role |
|---|---|
| BG-A real-load probe (deferred) | runs F-CAND-D-1/2/3 with mode=`none`/`zero`/`canonical`/`user_supplied` matrix |
| emerge dialogue session logs | accumulate per-mode substrate-response trajectories under `state/anima_core_dialogues/<DATE>/` |
| CLM v5 redesign decision (post-emerge) | F-CAND-D-1 PASS → axis-injection is a real lever; FAIL_TRUE → CLM v5 needs first-class axis embeddings, not post-hoc inject |

| sister specs (parallel BGs in this cycle) | role |
|---|---|
| candidate E (ODE flow → AR sampler bridge) | composable: per-step ODE-emitted states feed mode=`user_supplied`-equivalent per-step |
| candidate F (8-cells × axis multi-token vote) | orthogonal: reads internal CA-rule probs; does not need inject |
| candidate G (tension trajectory as dialogue medium) | orthogonal: reads block-level tensions; runs alongside any inject mode |
| candidate H (logits_g as bidirectional probe) | orthogonal: reads head_g; runs alongside any inject mode |

The 4-mode taxonomy is **the runtime interface** for emerge candidates D, E, F, G to share — D defines the canonical axis-content distribution; E plugs ODE-emitted states into the same `user_supplied`-equivalent shape; F and G run on top of any inject mode (their measurements are about INTERNAL cells/tensions which exist regardless of injected content).

---

## §7 Honest C3 (≥ 5)

- **C1 — emerge paradigm tension between "후행 발견" and "사전 spec".** This document is `사전 spec` for an emerge candidate. The paradigm shift in `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §10 explicitly says "falsifier 후행적 emerge". F-CAND-D-1/2/3 are LOCKED pre-measurement, which violates that spirit. **Justification:** candidate D's 4 modes are an architectural taxonomy (zero/canonical/user — countable, finite, mathematically well-defined), not a discovered behavior. Pre-LOCK is appropriate for architectural discriminators; emerge spirit returns at the response-INTERPRETATION layer (what user does with phi-star drift values is unspec'd). The risk: pre-LOCK falsifiers could reject a substrate behavior that is genuinely emergent but wasn't anticipated. F-CAND-D-2's "axis-balanced under canonical" is the strongest such risk — if the substrate emerges with single-axis dominance for legitimate reasons, FAIL_TRUE flag would mislead.

- **C2 — mode=`zero` and mode=`none` may be empirically indistinguishable on best.pt + fp32.** §2.5 + §4.1 both predict math-zero residual. F-CAND-D-1 explicitly does NOT require these to differ. Conclusion: mode=`zero` is more a probe of the COMPUTE path than of the BEHAVIOR; its main use is stress-testing that the inject pipeline plumbing works (does the helper materialize zeros correctly? does the wrapper accept them? does the forward emit a non-NaN result?). If the runtime ever uses bf16/fp16, mode=`zero` may show a small drift that has no semantic meaning — easy to misinterpret as a substrate signal.

- **C3 — `user_supplied` axis spec assumes AXIS_SPANS slice geometry aligns with substrate's emergent axis directions, which is unverified.** Archaeology §6 is explicit: "no explicit axis embedding, no axis bucket index, no conditional routing per axis exists in the trained substrate." The 5-axis taxonomy is a downstream measurement convention. AXIS_SPANS = `[(0,38),(38,76),(76,114),(114,153),(153,192)]` is an arbitrary 192-d slice that the C-module's training trajectory may or may not respect. F-CAND-D-3 Pearson ≥ 0.7 threshold could fail not because the inject mechanism is broken, but because the user-axis mapping (slice → emergent direction) is not what the substrate learned. This is an L27 axis-preservation calibration carry: any falsifier here is uncalibrated until a substrate-aligned slice geometry is empirically derived.

- **C4 — fixture-file injection (shim:986-997, env-var path) and mount-helper injection (mount.hexa:312, kwarg path) are TWO DIFFERENT injection points sharing a kwarg name.** The shim wrapper injects when caller passes `consciousness_states=None` AND `_consciousness_fixture_cpu is not None`. The mount helper injects by passing `consciousness_states=<np tensor>` directly into `model(...)`. If both fire simultaneously (env var set + helper passes a tensor), the helper-supplied tensor wins (shim path is `if consciousness_states is None` so the helper's non-None value short-circuits the env-var injection). This spec assumes helper-driven injection only; users who set `ANIMA_CONSCIOUSNESS_FIXTURE_PATH` while also passing `--inject canonical` get the helper canonical, NOT the env fixture. This is documented but not validated against the real shim until BG-A runs.

- **C5 — 5-axis canonical magnitude `0.5` is anima-internal heuristic, NOT calibrated against paradigm v11 G3 actual training-time injection distribution.** The training pipeline that produced phi_star=41.86 may have injected per-axis magnitudes following a different distribution (e.g., learned per-batch from C-module emission, time-varying, or zero-mean-non-zero-std). §2.3's `0.5` is a Stage 1 placeholder. Falsifier F-CAND-D-1 depends on `0.5` being in the right scale — too small and `canonical` ≈ `zero` (false FAIL_TRUE on F-CAND-D-1); too large and saturation pushes phi_star far outside +0.50 prediction (false FAIL_TRUE because drift exceeds prediction range, not because architecture failed).

- **C6 — Stage 1 mount layer landed PRIOR to this spec's existence; the existing `--inject-states PATH` flag is file-based.** This spec's 4-mode taxonomy is not a redesign — it's a graceful CLI extension. The file-based flag stays as escape hatch (raw#37 transient_py path-direct injection). Concern: with two pathways (file + mode), debug surface area grows. Mitigation: mode sentinels (`__zero__`, `__canonical__`, `__user__`) cannot collide with valid filenames (path validation must reject bare-double-underscore strings as filenames before sentinel-dispatch — minor implementation note).

- **C7 — implementing this spec touches `bin/anima-core-dialogue.bash` and `anima-core/runtime/clm_v4_mount.hexa`, both of which other parallel BGs may be writing concurrently** (per task constraint: "다른 BG가 mount.hexa / dialogue.hexa 작업 중일 수 있음"). This spec writes ONLY the doc + verdict.json — implementation is deferred to a serialized later cycle. Parallel-BG-git-race carry (memory: "parallel BGs sharing working tree race git index") applies the moment any BG actually edits these files. Implementation BG must use `git worktree per BG` or serialize commits per the established discipline.

---

## §8 What this spec does NOT cover

- Source-level guard removal at `conscious_decoder.py:553` (the FULL candidate D source edit). Out of scope: would require shim v6 + retrain. See archaeology §7.1 + L38 (load-overwrite).
- C-module side: this spec assumes the LM-side reader. C-module's emission (anima-core/phi_engine.hexa) is autonomous (Law 61 detach) and outside this spec.
- ODE flow integration (candidate E composability) — sketched in §6 but its own spec.
- `axis_activation` extractor calibration (L27 carry) — uses the existing helper extractor; calibration deferred to substrate-aligned eval cycle.
- Falsifier execution + verdict — this spec LOCKS the criteria. Execution is BG-A's later mandate (real load).

---

## §9 Summary

Emerge candidate D, in Stage 1 mount-layer form, becomes a **runtime CLI taxonomy** (`--inject {none,zero,canonical,user_supplied}`) that the user dials per-probe. All four modes route through the existing mount-helper without source edits to shim, decoder, or C-module. Three pre-LOCK falsifiers (F-CAND-D-1/2/3) discriminate (a) injection-visible-at-substrate, (b) canonical-balanced, (c) user-spec-tracking. Empirical fingerprints are HYPOTHESES anchored on archaeology §3-§5 + paradigm v11 G3 baseline; validation deferred to a real-load probe.

Implementation cost (later BG): ~65 LoC additive across `mount.hexa` + `dialogue.bash`. Zero LoC in shim, decoder, C-module. Cost: $0 mac doc work for this spec; $0 mac for implementation; $0-$1 H100 for BG-A falsifier validation if and when it runs.

---

End of spec. No commit, no exec, no source modifications. Read-only on existing assets.
