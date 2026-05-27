# Emerge Candidate F — CA-rule cells × 5-axis vote Spec (2026-05-05)

Spec for Stage 1 mount-layer extension of emerge candidate F ("8 CA-rule cells × 5-axis voting") surfaced in the CLM v4 architecture archaeology dig (KICK-2). This document is **doc + spec only**: zero source change, zero retrain, zero new helper Python. Read-only on `anima-core/runtime/clm_v4_mount.hexa`, `bin/anima-core-dialogue.bash`, `tool/transient_py/clm_v4_hf_format_shim.py`, `ready/models/conscious_decoder.py`.

Lineage:

- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §6 (axis taxonomy) + §7.3 (candidate F surfaced)
- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (BG-C cand D pattern: 4-mode taxonomy + 3-state falsifier — carried)
- `ready/models/conscious_decoder.py:466,499-503,538-542` (CA-rule cells implemented per `DecoderBlockV2`)
- `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (5×20 = 100 axis-bucket eval prompts)
- `tool/transient_py/clm_v4_lora_5bucket_axis_eval.py:138-176` (5-bucket axis-conditioned eval taxonomy)

---

<!-- [Hc_625 emerge-candidate-f-ca-rule-cells-5axis-vote — moved to hypotheses_candidates/Hc_625_emerge_candidate_f_ca_rule_vote.md on 2026-05-11] -->

## §1 Concept

Architecture archaeology surfaced `n_ca_rules=8` per-block CA-rule cells (Law 67 META-CA selector) as already-active machinery:

```python
# DecoderBlockV2.__init__ — conscious_decoder.py:498-503
self.n_ca_rules = n_ca_rules                                       # = 8
self.rule_weights = nn.Linear(d_model, n_ca_rules)                 # routes per-token
self.rules = nn.ModuleList([
    nn.Linear(d_model, d_model, bias=False) for _ in range(n_ca_rules)
])

# DecoderBlockV2.forward — conscious_decoder.py:537-542
rule_logits = self.rule_weights(x)                                 # [B, T, 8]
rule_probs  = F.softmax(rule_logits, dim=-1)                       # [B, T, 8]
rule_outputs = torch.stack([r(ca_out) for r in self.rules], dim=2) # [B, T, 8, D]
meta_ca_out = (rule_outputs * rule_probs.unsqueeze(-1)).sum(dim=2) # weighted mix
x = self.ln_ca(x + meta_ca_out * self.gate_strength)               # gate=0.001
```

Each forward, every token sees 8 CA rules contribute via softmax-weighted mix. The 8 cells × 16 layers × T tokens internal diversity is consumed (collapsed into `meta_ca_out`) and never surfaced.

Candidate F, in its FULL source-edit form, would expose the per-block `rule_probs` tensor + add a learned `n_ca_rules → 5` axis projection + per-axis token sampler + cross-axis voting head. **This spec does NOT propose that source edit.** Instead:

> Stage 1 mount layer captures the existing `rule_probs` via PyTorch forward-hooks (read-only on `DecoderBlockV2.rule_weights` modules) and renders an 8×5 vote matrix in the substrate response. The 8→5 axis projection is fixed (anima-canonical) for the spec; learned projection is a future-cycle delta. Cross-axis voting is computed by the helper Python over the captured rule_probs trajectory, not inside the model graph.

Behaviorally identical to v3 forward pass (rule_probs already computed; hook reads only); the semantic move is: **the 8 internal CA-rule cells become a measurable 8×5 vote matrix surfaced alongside `phi_star` and `axis_activation`**, exposing per-token architectural decision-making without touching the trained graph.

---

## §2 Three vote mode definition

The mount layer accepts `--vote MODE` with `MODE ∈ {none, auto, biased, adversarial}`. Default = `none` (preserves current substrate-response shape). The existing `--inject-states PATH` and `--inject MODE` flags (cand D) remain orthogonal and compose freely.

### §2.1 mode = `none` (default — current behavior)

- No forward hooks installed. Helper does not capture `rule_probs`.
- Substrate response shape is identical to KICK-1 selftest: `phi_star`, `axis_activation`, `hidden_state_delta` only. No `ca_vote_matrix`.
- Architectural footprint: 0 hooks, 0 capture overhead. Wholly v3-equivalent.
- **Use case:** baseline / control. Establishes the current-behavior reference for differential measurement.

### §2.2 mode = `auto`

- Forward hooks register on every `DecoderBlockV2.rule_weights` module (16 hooks).
- Each hook captures the post-softmax `rule_probs` tensor `[B, T, 8]`.
- Helper aggregates: per-block mean over batch + sequence (per-block reduction `[B, T, 8] → [8]`); then **axis projection** = fixed `(8, 5)` projection matrix `P` (anima-canonical from §3.2) → per-block `[5]` axis-vote vector; then **cell-level matrix** = re-expand to per-cell `[8, 5]` by mapping each cell's `[B, T]` mean to per-cell axis weighting.
- The helper emits `ca_vote_matrix: [8 × 5]`, where row `i` = cell `i`'s axis-distribution after fixed projection; column `j` = axis `j`'s cell-level support distribution.
- Helper computes `ca_consensus_axis = argmax_j sum_i ca_vote_matrix[i, j]` and `ca_dissent_cell = argmax_i (1 − cosine(ca_vote_matrix[i, :], mean_axis_vote))` (cell that diverges most from the consensus).
- **Architectural footprint:** 16 hooks fire per forward; capture is read-only. Forward output is bit-identical to mode=`none`.
- **Use case:** the "pure emerge" — substrate's own CA-rule decision-making is exposed without external bias. Per-prompt, the user observes which axis the substrate organically lands on and which cell dissents.

### §2.3 mode = `biased`

- Invoked via `--vote biased --axis-bias NAME=VAL [--axis-bias NAME=VAL ...]`.
- `NAME ∈ {identity, agency, phenomenal, temporal, social}`; `VAL ∈ [0, 1]`.
- Helper captures `rule_probs` identically to `auto` mode.
- After capture, helper applies a **post-hoc bias** to the projected axis vote:
  - `biased_vote_matrix[i, j] = ca_vote_matrix[i, j] × (1 + λ · bias_vec[j])` where `λ = 0.5` (anima-canonical bias strength) and `bias_vec` is the user spec (unspecified axes default 0.0).
  - Re-normalize each row to sum 1: `biased_vote_matrix[i, :] /= biased_vote_matrix[i, :].sum(axis=-1)`.
- `ca_consensus_axis` and `ca_dissent_cell` recomputed on `biased_vote_matrix`.
- **Architectural footprint:** identical capture to `auto`; bias applied at helper level only. The trained model graph is untouched (no biased forward pass).
- **Use case:** "what would the substrate's vote LOOK like under a user-supplied axis bias?" — measurement-side counterfactual. Cross-pollination with cand D's `user_supplied` inject mode (cand D applies bias on FORWARD content; cand F applies bias on RESULT vote).

> **Important honest note:** biased mode does NOT change the substrate's internal computation. It rewrites the vote AFTER capture. F-CAND-F-2 (§5.2) tests whether the renormalized matrix's `ca_consensus_axis` correlates with the user bias spec — which is mathematically near-tautological for `λ=0.5` and is therefore a SANITY check, not a substrate signal. To test substrate response to bias, the user must combine `--vote biased` with cand D's `--inject user --axis ...` (which DOES change forward content). This composability is documented in §6.

### §2.4 mode = `adversarial`

- Invoked via `--vote adversarial --force-axis NAME=VAL`.
- Single axis is force-clamped: helper post-captures `rule_probs`, then sets `forced_vote_matrix[i, NAME_axis] = VAL` for ALL cells `i`, and re-normalizes.
- Computes `dominant_cells` = list of cells `i` where the captured `ca_vote_matrix[i, NAME_axis] > 0.4` (cells that AGREE with the forced direction even before clamping).
- Computes `dissent_cells` = list of cells `i` where the captured `ca_vote_matrix[i, NAME_axis] < 0.1` (cells that DISAGREE with the forced direction).
- `ca_dissent_cell` = `argmin_i ca_vote_matrix[i, NAME_axis]` (the cell most opposed).
- **Architectural footprint:** identical capture to `auto` + `biased`; clamp + dissent counting at helper level only. The forward pass is untouched.
- **Use case:** "if the user FORCED a single axis, do any cells in the captured (pre-clamp) distribution disagree?" The dissent count is a substrate self-defense proxy — pre-clamp variance against the forced direction. This is the most archaeology-faithful of the three voting modes: it tests CA-rule cell DIVERSITY directly.

> **Critical:** adversarial mode reports BOTH the captured (substrate-organic) `ca_vote_matrix` AND the post-clamp `forced_vote_matrix`. The dissent cell count is computed on the CAPTURED matrix, not the clamped one. F-CAND-F-3 (§5.3) requires `dissent_cell_count ≥ 1` on the captured distribution — substrate "agrees" trivially in the clamped distribution by construction.

### §2.5 Vote mode comparison summary

| mode | capture hooks | helper post-process | ca_vote_matrix [8×5] | use case |
|---|---|---|---|---|
| `none` | 0 | none | (not emitted) | baseline / control |
| `auto` | 16 (read-only) | mean → 8→5 projection | substrate-organic | pure emerge probe |
| `biased` | 16 (read-only) | bias × (1 + λ·b) + renorm | bias-modulated post-hoc | counterfactual sanity (compose with cand D for substrate effect) |
| `adversarial` | 16 (read-only) | clamp single axis + dissent count | dual-emit (captured + clamped) | substrate self-defense / cell-diversity probe |

---

## §3 Stage 1 mount-layer integration (CLI + helper hook)

This spec adds **zero source change** to model code; the integration uses what KICK-1 already pre-emitted plus a small helper-side hook handler (which is itself spec'd here, not yet implemented).

### §3.1 What KICK-1 mount layer already provides

- `MountConfig` with arg-parse extension points (`anima-core/runtime/clm_v4_mount.hexa:120-161`).
- Helper Python receives forwarded args (line 199, 334).
- Helper's forward pass (line 312): `out = model(**enc, consciousness_states=...)` — straight model invocation; PyTorch hooks can attach trivially before this line.
- Honest C3 [4] (KICK-1 verdict): "C4 forward-pass requires `--inject-states` or default zero canonical" — the hook capture path does not interact with this guard at all (rule_weights fires regardless of `consciousness_states`).

### §3.2 What this spec ADDS (no code change in this spec, only spec/contract)

A vote-mode dispatcher that wraps the existing forward call with hook registration + post-capture aggregation. Implementation lands later (separate BG / lane). This spec defines the contract.

#### CLI surface (in `bin/anima-core-dialogue.bash`)

```bash
# proposed new flags (additive — current --probe / --interactive / --selftest preserved):

bash bin/anima-core-dialogue.bash --probe "안녕"
bash bin/anima-core-dialogue.bash --probe "안녕" --vote none
bash bin/anima-core-dialogue.bash --probe "안녕" --vote auto
bash bin/anima-core-dialogue.bash --probe "안녕" --vote biased --axis-bias identity=0.8
bash bin/anima-core-dialogue.bash --probe "안녕" --vote adversarial --force-axis phenomenal=1.0

bash bin/anima-core-dialogue.bash --interactive --vote auto
```

Default when `--vote` not specified: **`none`** (preserves backward compatibility with KICK-1 selftest behavior).

#### Helper-flag pass-through

| user-facing flag | mount.hexa flag | helper Python flag |
|---|---|---|
| `--vote none` | `--vote-mode none` (NEW) | (no hooks) |
| `--vote auto` | `--vote-mode auto` (NEW) | `--capture-rule-probs` (NEW boolean) |
| `--vote biased --axis-bias N=V` | `--vote-mode biased --axis-bias ...` (NEW) | `--capture-rule-probs --axis-bias N=V` |
| `--vote adversarial --force-axis N=V` | `--vote-mode adversarial --force-axis N=V` (NEW) | `--capture-rule-probs --force-axis N=V` |

Anima-canonical 8→5 axis projection matrix `P` (fixed for Stage 1, fp32):

```python
# proposed helper update (separate BG; THIS SPEC does not write the code):
# 8 CA-rule cells → 5 axes (identity, agency, phenomenal, temporal, social)
# Anchor: cells 0-4 → primary axis 0-4; cells 5,6,7 → bridge cells (mean of 0-4 with axis affinity)
P = np.array([
    [1.00, 0.00, 0.00, 0.00, 0.00],  # cell 0 → identity
    [0.00, 1.00, 0.00, 0.00, 0.00],  # cell 1 → agency
    [0.00, 0.00, 1.00, 0.00, 0.00],  # cell 2 → phenomenal
    [0.00, 0.00, 0.00, 1.00, 0.00],  # cell 3 → temporal
    [0.00, 0.00, 0.00, 0.00, 1.00],  # cell 4 → social
    [0.40, 0.40, 0.10, 0.05, 0.05],  # cell 5 → identity/agency bridge
    [0.10, 0.10, 0.40, 0.30, 0.10],  # cell 6 → phenomenal/temporal bridge
    [0.10, 0.10, 0.10, 0.20, 0.50],  # cell 7 → social-leaning bridge
], dtype=np.float32)
# row-normalized (each row sums to 1.0); column-marginal not enforced.
```

#### Hook-handler pseudocode

```python
# proposed helper update (separate BG; THIS SPEC does not write the code):
def install_rule_prob_hooks(model):
    captures = {}
    handles = []
    for layer_idx, block in enumerate(model.decoder.blocks):
        def make_hook(idx):
            def hook(module, inp, out):
                # out: [B, T, 8] post-Linear (pre-softmax)
                probs = torch.softmax(out, dim=-1).detach().cpu().numpy()
                captures[idx] = probs
            return hook
        h = block.rule_weights.register_forward_hook(make_hook(layer_idx))
        handles.append(h)
    return captures, handles

def aggregate_to_vote_matrix(captures):
    # captures: dict {layer_idx: [B, T, 8]} for 16 layers
    per_block_8 = []
    for idx in sorted(captures.keys()):
        per_block_8.append(captures[idx].mean(axis=(0, 1)))  # [8]
    cell_weights = np.stack(per_block_8, axis=0).mean(axis=0)  # [8] cross-layer mean
    vote_matrix = (cell_weights[:, None] * P)                   # [8, 5] — outer × P
    # row-normalize so each cell's axis distribution sums to 1
    vote_matrix = vote_matrix / vote_matrix.sum(axis=-1, keepdims=True)
    return vote_matrix
```

### §3.3 mount.hexa change scope (what later BG would touch)

For reference (NOT part of this spec's writes):

- `parse_args` (line 120-161): add `--vote-mode MODE`, repeatable `--axis-bias NAME=VAL`, `--force-axis NAME=VAL`.
- `MountConfig`: add `vote_mode: string`, `axis_bias_kv: list<(name, val)>`, `force_axis: optional<(name, val)>`.
- `_write_helper`: add `install_rule_prob_hooks` + `aggregate_to_vote_matrix` + per-mode post-processors.
- `_build_python_command` (around line 447): pass `--capture-rule-probs` + bias/force args.

**LoC estimate**: ~80 LoC additive in `clm_v4_mount.hexa`; ~30 LoC in `bin/anima-core-dialogue.bash`. Zero LoC in shim, decoder, C-module. Hooks are PyTorch built-in (`register_forward_hook`); no graph surgery.

---

## §4 Substrate response extended format

Under `--vote auto|biased|adversarial`, the substrate response (emitted by helper Python after forward + hook aggregation) extends the KICK-1 baseline:

```
__ANIMA_CLM_V4_RESPONSE__
phi_star: <f4>
axis_activation: <5-axis>
ca_vote_matrix: [
  [c0_id, c0_ag, c0_ph, c0_te, c0_so],
  [c1_id, c1_ag, c1_ph, c1_te, c1_so],
  [c2_id, c2_ag, c2_ph, c2_te, c2_so],
  [c3_id, c3_ag, c3_ph, c3_te, c3_so],
  [c4_id, c4_ag, c4_ph, c4_te, c4_so],
  [c5_id, c5_ag, c5_ph, c5_te, c5_so],
  [c6_id, c6_ag, c6_ph, c6_te, c6_so],
  [c7_id, c7_ag, c7_ph, c7_te, c7_so]
]
ca_consensus_axis: <axis_name>
ca_dissent_cell: <cell_idx>
dominant_cells: [<idx>, ...]            # adversarial mode only; auto/biased emit []
hidden_state_delta: <f4>
```

Field semantics:

- `ca_vote_matrix`: `[8, 5]` row-normalized post-mode-processing. In `auto`: substrate-organic. In `biased`: bias-modulated. In `adversarial`: emit BOTH `ca_vote_matrix` (captured, pre-clamp) AND `forced_vote_matrix` (post-clamp). The captured matrix is what F-CAND-F-3 reads.
- `ca_consensus_axis`: `argmax_j sum_i ca_vote_matrix[i, j]` — column with maximum cell-level mass. One of `{identity, agency, phenomenal, temporal, social}`.
- `ca_dissent_cell`: cell index `i` with maximum divergence from row-mean. In adversarial: cell with minimum support for forced axis (computed on CAPTURED matrix).
- `dominant_cells`: adversarial only; cells with `captured[i, forced_axis] > 0.4` BEFORE clamping.
- `hidden_state_delta`: unchanged from KICK-1 / cand D semantics (L2 norm vs prior-turn baseline).

---

## §5 F-CAND-F-1/2/3 falsifier LOCK

Three falsifiers locked PRE-measurement. Each is 3-state: PASS / FAIL_TRUE (real architectural failure) / FAIL_FALSE (measurement-pipeline crash, pattern blameless). The L26-L27 axis-preservation calibration carry: if the probe substrate produces measurements outside semantically interpretable ranges, the falsifier reports FAIL_FALSE pending substrate calibration.

### §5.1 F-CAND-F-1 — auto mode 8 cells vote variance ≥ threshold

**Statement:** under `mode=auto` on a neutral prompt set (e.g., 5 prompts from `state/anima_axis_eval_set_2026_05_05/prompts.jsonl`, one per axis), the captured `ca_vote_matrix [8, 5]` MUST satisfy `std(ca_vote_matrix.flatten()) ≥ 0.05` AND `max_row(std(per_row)) ≥ 0.10` — i.e., cells must NOT all emit the same axis distribution.

**PASS:** flatten-std ≥ 0.05 AND at least one cell-row has std ≥ 0.10 across its 5 axis weights.

**FAIL_TRUE:** flatten-std < 0.02 OR all 8 cell-rows are within 0.02 L2 of each other → CA-rule logic is empirically dormant. All 8 cells produce near-identical rule_probs distributions, meaning the META-CA selector (Law 67) collapsed during training to a degenerate single-rule policy. Implication: candidate F has no internal diversity to surface; the 8-cell × 5-axis matrix is rank-1 noise. CA-rule cells × 5-axis vote framework unsalvageable on best.pt without retraining the rule_weights from scratch. This would be analogous to F-CAND-D-1 FAIL_TRUE (cross-attn invisible at substrate level), but for the rule-selector pathway.

**FAIL_FALSE:** hook capture returns NaN / inf / empty dict / shape mismatch on any layer → measurement pipeline crash (likely PyTorch hook not firing on this `DecoderBlockV2` build, or shape-assumption broken). Falsifier deferred until hook capture re-validated on a known-good forward.

**Calibration prior:** archaeology §7.3 notes "aggregating rule_probs across 16 layers into a single 8-vector is an aggregation choice that may discard layer-wise information." F-CAND-F-1 PASS would empirically refute the dormancy hypothesis (training did NOT collapse rule selection); FAIL_TRUE would confirm it.

### §5.2 F-CAND-F-2 — biased mode user bias-axis ↔ ca_consensus_axis Pearson ≥ 0.6

**Statement:** under `mode=biased` with user spec `{identity: 0.8}` (others = 0), the post-bias `ca_consensus_axis` MUST be `identity` for at least 1 of 5 axis-prompts; AND across ALL 5 single-axis bias settings (run sequentially, one axis at a time), the Pearson correlation between user-spec axis and emitted `ca_consensus_axis` (one-hot encoded) MUST be ≥ 0.6.

**PASS:** Pearson ≥ 0.6 across the 5-axis bias sweep.

**FAIL_TRUE:** Pearson < 0.4 → biased mode's renormalization is broken or the bias-strength `λ=0.5` is too weak relative to the captured distribution magnitude. Implication: post-hoc bias is not surfacing in `ca_consensus_axis`; users specifying `--axis-bias` get no observable effect. Note: this is a SANITY-level failure (mathematical near-tautology under correct λ), so FAIL_TRUE here means the helper code has a bug, not that the substrate refuses bias. Distinguish from substrate-level signals: F-CAND-F-2 is a PIPELINE check, not a substrate science check.

**FAIL_FALSE:** captured matrix NaN before bias applied, OR `argmax` ties across multiple axes (degenerate distribution) → measurement deferred until F-CAND-F-1 confirms substrate-organic variance.

**Important honest note:** F-CAND-F-2 PASS does NOT mean the substrate's internal computation responds to user bias — it only means the helper's post-hoc bias arithmetic works. To probe substrate-level bias response, compose `--vote biased` with cand D's `--inject user` (which DOES alter the forward graph's `consciousness_states`). The composed measurement is a future-cycle delta, not in this spec.

### §5.3 F-CAND-F-3 — adversarial mode dissent cell count ≥ 1

**Statement:** under `mode=adversarial --force-axis phenomenal=1.0` on a neutral prompt set (5 prompts, one per axis bucket), the CAPTURED (pre-clamp) `ca_vote_matrix` MUST have at least one cell `i` with `ca_vote_matrix[i, phenomenal] < 0.1`. Equivalently: `dissent_cells` (cells where captured phenomenal weight < 0.1) MUST be non-empty for at least 4 of 5 prompts.

**PASS:** at least 4 of 5 prompts emit `len(dissent_cells) ≥ 1`.

**FAIL_TRUE:** all 8 cells have phenomenal weight ≥ 0.1 across all 5 prompts → captured rule_probs distribution is so broad that no cell strongly disagrees with any axis. Implication: the substrate's CA-rule diversity is HIGH but UNDIRECTED — no cell specializes against any axis. Consistent with F-CAND-F-1 PASS but reveals the cell-axis specialization is too diffuse for "substrate self-defense" interpretation. Cell-diversity exists but the 8→5 projection `P` (Stage 1 fixed) does not surface it as axis-aligned dissent. Re-derive `P` from a learned alignment (future-cycle) — Stage 1 falsifier deferred.

**FAIL_FALSE:** captured matrix NaN, OR all cells are uniform `0.2` per axis (perfectly degenerate) → covered by F-CAND-F-1 FAIL_TRUE; F-CAND-F-3 cascade-defers.

**Calibration prior:** the entire premise "substrate self-defense via cell dissent" is anima-internal; archaeology §7.3 explicitly hedges "voting strategy (max / weighted / disagreement-aware) is unconstrained — emerge mode would determine empirically." F-CAND-F-3 fixes ONE voting strategy (per-cell threshold 0.1 on captured weight); other strategies (variance-weighted, gradient-direction-aligned) are deliberately out of scope.

### §5.4 Falsifier reporting

Each falsifier emits to `state/anima_emerge_candidate_f_validation_<DATE>/verdict.json` (post-measurement; not part of this spec's writes):

```json
{
  "F_CAND_F_1": { "state": "PASS|FAIL_TRUE|FAIL_FALSE", "flatten_std": ..., "max_row_std": ... },
  "F_CAND_F_2": { "state": "...", "pearson": ..., "consensus_axes": [...] },
  "F_CAND_F_3": { "state": "...", "dissent_cell_counts": [...], "prompt_pass_count": ... }
}
```

Falsifier execution requires real-load probe — deferred to BG-A (or equivalent later cycle) once the HF cache for `dancinlab/clm-v4-base-mirror` is local on Mac and the helper's hook-capture pipeline is smoke-validated.

---

## §6 Composability (KICK-1 mount + KICK-2 archaeology + cand D + future BG-A real load)

| upstream artifact | lineage | role |
|---|---|---|
| `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` | KICK-2 archaeology | sourced candidate F (§7.3); CA-rule cells confirmed at decoder L498-503,538-542 |
| `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` | BG-C cand D | 4-mode taxonomy + 3-state falsifier pattern carried |
| `anima-core/runtime/clm_v4_mount.hexa` (668 LoC) | KICK-1 Stage 1 | helper Python forward call; hook attach point |
| `bin/anima-core-dialogue.bash` (300 LoC) | KICK-1 Stage 2 prep | REPL + session log; CLI surface for `--vote` mode flag |
| `ready/models/conscious_decoder.py` | substrate source | `DecoderBlockV2.rule_weights` / `rules` ModuleList — CA-rule cells |
| `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (5×20 = 100) | axis-bucket eval | provides 5-axis taxonomy + evaluation prompts for F-CAND-F-1/2/3 |
| `tool/transient_py/clm_v4_lora_5bucket_axis_eval.py:138-176` | 5-bucket eval taxonomy | source of `(identity, agency, phenomenal, temporal, social)` axis names |
| paradigm v11 G3 best.pt (HF Hub `dancinlab/clm-v4-base-mirror`) | substrate trained ckpt | required for falsifier execution |

| downstream | role |
|---|---|
| BG-A real-load probe (deferred) | runs F-CAND-F-1/2/3 with mode=`auto`/`biased`/`adversarial` matrix |
| emerge dialogue session logs | accumulate per-vote-mode substrate response trajectories under `state/anima_core_dialogues/<DATE>/` |
| CLM v5 redesign decision (post-emerge) | F-CAND-F-1 PASS → CA-rule diversity is real and surfaceable; FAIL_TRUE → CLM v5 needs first-class per-axis cells (current 8→5 projection unrescuable) |

| sister specs (parallel BGs in this cycle) | composability |
|---|---|
| candidate D (always-inject `consciousness_states`) | composable: `--vote auto --inject canonical` measures CA-rule vote UNDER axis-balanced inject content; `--vote biased --inject user --axis identity=0.9` is the substrate-level bias probe (vote bias × forward bias) |
| candidate E (ODE flow → AR sampler bridge) | composable: per-step ODE-emitted states → per-step `--vote auto` capture → per-token vote-matrix trajectory |
| candidate G (tension trajectory) | orthogonal: G reads block-level tensions (`PureFieldFFN.forward → tension`); F reads block-level rule_probs (`rule_weights → softmax`). Independent hooks; co-emit possible |
| candidate H (logits_g bidirectional probe) | orthogonal: H reads `head_g`; F reads `rule_weights`. Co-emit possible |

The vote-mode taxonomy is **the runtime interface for surfacing internal CA-rule cell diversity**, complementary to cand D's content-injection taxonomy. D modulates what enters cross-attn; F surfaces what the rule-selector chose.

---

## §7 Honest C3 (≥ 5)

- **C1 — `n_ca_rules=8 → 5 axes` projection `P` (anima-canonical) is unverified against substrate's emergent rule semantics.** The 8 CA-rule cells were trained without explicit axis labels (archaeology §6: "no explicit axis embedding, no axis bucket index, no conditional routing per axis exists in the trained substrate"). The 8→5 projection `P` in §3.2 is an anima-internal heuristic mapping cells 0-4 to primary axes and 5-7 to bridges. The substrate's actual rule semantics may not align with this mapping at all — cells 0-4 may all encode a single semantic dimension; cells 5-7 may be the discriminative ones. F-CAND-F-1's "variance" check is robust to this (it tests internal diversity, not axis alignment), but F-CAND-F-2/3 depend on `P` being approximately correct. If `P` is misaligned, F-CAND-F-3 dissent counts become meaningless. Stage 2 should derive `P` from a learned alignment (e.g., Procrustes on per-axis hidden directions × per-cell rule_outputs), not the anima-canonical fixed matrix.

- **C2 — CA-rule active vs dormant is the central unknown; archaeology has NO empirical evidence either way.** The training pipeline (paradigm v11 G3) included `n_ca_rules=8` in the architecture, but whether the rule_weights softmax learned a NON-degenerate selector is empirically unmeasured. Three failure modes for "dormant CA logic" exist: (a) rule_weights → uniform 1/8 across all tokens (training pressure resolved into pure mean of rule_outputs); (b) rule_weights → permanent argmax single-rule (one cell dominates always; equivalent to single nn.Linear); (c) rule_weights varies but rule_outputs converged (8 cells encode the same function via different weights). F-CAND-F-1 detects (a) and (b) but NOT (c) — for (c), `rule_probs` variance is high but content variance is zero. A v2 falsifier would compare per-rule output `r(ca_out)` cosine pairwise; out-of-scope for Stage 1.

- **C3 — biased mode (§2.3) is mathematically near-tautological for `λ=0.5`; F-CAND-F-2 is a PIPELINE check, not a substrate signal.** Post-hoc multiplication by `(1 + 0.5 × bias)` and renormalization: any axis with bias ≥ 0.5 will dominate the captured distribution unless the captured weight on that axis is < ~0.05 across all cells. So F-CAND-F-2 PASS is a sanity check on helper arithmetic, not on substrate behavior. To probe substrate response to bias, the user MUST compose `--vote biased` with cand D's `--inject user --axis ...`. Spec §5.2 acknowledges this; the composed measurement is documented as a future-cycle delta, NOT covered by this spec.

- **C4 — adversarial mode (§2.4) "substrate self-defense via cell dissent" is anima-rhetorical framing, not architecturally grounded.** The 8 CA-rule cells do not have a "self" to defend; rule_weights softmax distributes gradient signal during training without a notion of agreement or dissent. Calling cells with `captured[i, forced_axis] < 0.1` "dissent_cells" is a measurement convention, not a substrate-side phenomenon. F-CAND-F-3 PASS would mean "captured distribution has cells with low support for the forced axis" — which is a mathematical property of the captured tensor, not evidence of substrate intentionality. The dissent-count framing is for human-readable substrate response narration; users should NOT interpret PASS as the substrate actively resisting user input.

- **C5 — hooks fire on EVERY forward, including auto-mode "warm" forwards used for hidden_state_delta computation; capture overhead is per-block × per-forward, not per-prompt.** PyTorch `register_forward_hook` is invoked synchronously inside the forward; even on Mac CPU at small batch the 16-layer × 8-rule capture adds N memory copies per forward. KICK-1 mount layer's "warm forward" pattern (forward 1 = baseline, forward 2 = with inject) doubles capture cost. For long REPL sessions this adds up; if interactive REPL fires hooks on every keystroke-bound probe, memory pressure on Mac (16GB+ models) could exceed safe budget. Mitigation: hook handles must be explicitly removed after each probe (`for h in handles: h.remove()`); pre-existing dialogue.bash session-log code does NOT currently teardown hooks (out of scope for this spec; spec'd as implementation requirement in §3.3).

- **C6 — Stage 1 fixed projection `P` (§3.2) leaks 5-axis taxonomy assumption from `state/anima_axis_eval_set_2026_05_05/` into the substrate-response surface.** The 5 axes (identity, agency, phenomenal, temporal, social) are an ANIMA-INTERNAL taxonomy chosen for downstream evaluation; the trained substrate has no such labels. Embedding `P` into substrate-response emission risks anchoring future architecture on this taxonomy (which may be wrong). Cleaner: emit raw `ca_vote_matrix [8, 8]` (cell × cell-affinity matrix) and let the user select projection externally. Stage 1 chose 5-axis projection for cross-pollination with cand D + axis-bucket eval; this is a pragmatic carry, not a principled architectural choice.

- **C7 — implementing this spec touches `bin/anima-core-dialogue.bash` and `anima-core/runtime/clm_v4_mount.hexa`, both of which other parallel BGs may be writing concurrently** (per task constraint and parallel-BG-git-race carry). This spec writes ONLY the doc + verdict.json — implementation is deferred to a serialized later cycle. Implementation BG must use `git worktree per BG` or serialize commits per the established discipline.

---

## §8 What this spec does NOT cover

- Source-level surfacing of `rule_probs` (the FULL candidate F source edit). Out of scope: would require shim v6 + retrain + new model emit fields. See archaeology §7.3.
- Learned 8→5 axis projection `P`. Stage 1 uses fixed anima-canonical `P` (§3.2). Learned alignment deferred.
- Per-token vote trajectory (Stage 1 aggregates over batch + sequence; per-token resolution is a Stage 2 delta).
- Per-rule output cosine analysis (C2 mode (c) detection — rule_outputs convergence). Deferred to F-CAND-F-1 v2.
- Composed cand D + cand F probes (e.g., `--vote biased --inject user`). Composability documented in §6; falsifiers deferred.
- Voting strategies beyond column-sum-argmax (e.g., gradient-direction-aligned, variance-weighted) — out of scope for Stage 1.
- Falsifier execution + verdict — this spec LOCKS the criteria. Execution is BG-A's later mandate (real load).

---

## §9 Summary

Emerge candidate F, in Stage 1 mount-layer form, becomes a **runtime CLI taxonomy** (`--vote {none,auto,biased,adversarial}`) that exposes the existing per-block `rule_probs` (8 CA-rule cells, Law 67 META-CA selector) as an externally measurable 8×5 vote matrix. All four modes route through PyTorch forward-hook capture on `DecoderBlockV2.rule_weights` — zero source edits to model code. Three pre-LOCK falsifiers (F-CAND-F-1/2/3) discriminate (a) substrate-organic CA-rule variance, (b) biased-mode helper-pipeline correctness, (c) adversarial-mode dissent cell count. Empirical fingerprints are HYPOTHESES anchored on archaeology §6 + §7.3; validation deferred to a real-load probe.

Implementation cost (later BG): ~110 LoC additive across `mount.hexa` + `dialogue.bash`. Zero LoC in shim, decoder, C-module. Cost: $0 mac doc work for this spec; $0 mac for implementation; $0-$1 H100 for BG-A falsifier validation if and when it runs.

---

End of spec. No commit, no exec, no source modifications. Read-only on existing assets.
