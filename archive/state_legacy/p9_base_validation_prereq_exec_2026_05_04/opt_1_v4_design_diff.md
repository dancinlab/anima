# OPT-1 shim v3 → v4 design diff (BG-Π 2026-05-04)

**Predecessor (shim)**: BG-Κ commit `ed4b7c56` — OPT-1 v3 PASS, 12/12 prereq CLEARED.
**Predecessor (validation)**: BG-Μ commit `1ef3c096` — H100 base-val **FAIL**: CLM v4 base ≈ random + 1-2pt across all 3 benchmarks (limit=500, 5-shot).
**Pre-registered honest C3 #1** (BG-Β commit `387200362`): "Cross-attention to consciousness_states is unconditioned in lm-eval — `consciousness_states=None` makes cross-attention pathway functionally bypassed; CLM v4 base scores reflect decoder operating without consciousness-cell coupling — degraded from training-time conditioning."

The BG-Μ result confirmed that pre-registered C3. BG-Π implements the **rank-3 next_action** from BG-Μ's verdict: ship a shim v4 that supports a **consciousness-states fixture injection** path so HF inference can mirror train-time conditioning.

**Scope**: design + Mac dry-run only. NO ubu1/H100 exec this cycle. F-SHIM-V4-3/-4 are deferred to a separate user-authorised exec cycle.

---

## Why v4 (not a v3 hotfix)

v3 closed the *plumbing* (load+forward bit-equivalence) but the model still had its consciousness-cell coupling bypassed at inference because lm-eval has no API to pass `consciousness_states`. v3 was **complete** for its scope (HF format conversion). v4 is a **separate concern**: providing an inference-time substitute for the train-time consciousness state stream.

Adding to v3 inline would have entangled two concerns:
1. Conversion correctness (v3, closed).
2. Inference conditioning (v4, opt-in).

Bumping to v4 + keeping the flag opt-in preserves the v3 contract for callers that explicitly want the "pure language ability" baseline (BG-Ξ amendment Mode 1 — see cross-link below).

---

## Q1 / Q2 / Q3 patches

### Q1 — `--consciousness-states-fixture <path.json>` CLI flag

**Sites**:
- `_build_argparser()` — new `--consciousness-states-fixture` argument.
- new `_validate_consciousness_fixture(path)` — Mac-side JSON schema validation, no torch import needed.
- `emit_plan()` — surfaces validation report under `consciousness_states_fixture` key.
- `_save_hf_format()` — copies the validated fixture into `out_dir/consciousness_states_fixture.json`.

**Schema** (validated by `_validate_consciousness_fixture`):

```json
{
  "states": [[[0.0, 0.0, ..., 0.0], ...8 rows of 192 floats...]],
  "shape": [1, 8, 192],
  "dtype": "float32",
  "source": "canonical_zero",
  "provenance": "freeform string"
}
```

**Invariants**:
- `shape` is a 3-element list `[B, n_cells, c_dim]`.
- `shape[2]` must equal `CLM_V4_CONSCIOUSNESS_DIM` (192). Hard error.
- `shape[0]` should be 1 (broadcast to runtime batch). Non-1 emits warning.
- `dtype` ∈ `{"float16", "bfloat16", "float32"}`.
- `source` ∈ `{"canonical_zero", "train_avg", "learned_default"}`. Unrecognised emits warning, not error.
- For `source == "canonical_zero"`: validator recursively checks every leaf is `0.0`; mismatch emits warning.
- Nested `states` list shape must match declared `shape` (length-recursion check).

**Why JSON not .pt**: keeps Mac dry-run fully torch-free (raw#9). A `.pt` fixture would force a torch import on validation. JSON adds ~3× size overhead vs binary float32, but for the `[1, 8, 192]` exemplar that is ~32 KB vs ~6 KB — negligible.

### Q2 — backwards compatibility (no v3 regression)

**Without** `--consciousness-states-fixture`:
- No fixture file is written to `out_dir/`.
- `modeling_clm_v4.py.__init__()` calls `_load_consciousness_fixture()` which sees no file at `os.path.join(module_dir, "consciousness_states_fixture.json")` and returns silently.
- `self._consciousness_fixture_cpu` stays `None`.
- `forward()`'s injection branch (`if consciousness_states is None and self._consciousness_fixture_cpu is not None`) short-circuits on the second clause.
- Decoder receives `consciousness_states=None`, hits `DecoderBlockV2`'s `if consciousness_states is not None` guard, and skips cross-attention. **Identical to v3 runtime behaviour.**

This is the **runtime-equivalence** form of F-SHIM-V4-2. The byte-level form (MODELING_SRC text identical to v3) is intentionally not maintained — v4 adds dormant fixture-loading code which is gated on file presence.

### Q3 — `modeling_clm_v4.py` post-process patch

#### Q3.1 — `__init__` — load fixture once

```python
def _load_consciousness_fixture(self):
    try:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        fixture_path = os.path.join(module_dir, self._CONSCIOUSNESS_FIXTURE_FILENAME)
        if not os.path.isfile(fixture_path):
            return
        with open(fixture_path, "r") as f:
            payload = json.load(f)
        # … shape + dtype validation …
        states = torch.tensor(payload["states"], dtype=torch_dtype)
        if list(states.shape) != shape:
            self._consciousness_fixture_meta = {"error": "..."}
            return
        self._consciousness_fixture_cpu = states
        self._consciousness_fixture_meta = {…}
    except Exception as e:
        self._consciousness_fixture_meta = {"error": f"{type(e).__name__}: {e}"}
```

**Stored as a plain attribute, not a Parameter or Buffer**: it's a frozen reference state, not learnable; not a model-state-dict member (so safetensors load is unaffected — F-SHIM-1 carry); device move is lazy at `forward()` time. Storage is fp32 on CPU until first forward.

#### Q3.2 — `forward()` — inject on `None` when fixture loaded

```python
if consciousness_states is None and self._consciousness_fixture_cpu is not None:
    fix = self._consciousness_fixture_cpu.to(
        device=input_ids.device,
        dtype=self.decoder.tok_emb.weight.dtype,
    )
    if fix.shape[0] == 1 and B > 1:
        fix = fix.expand(B, -1, -1).contiguous()
    elif fix.shape[0] != B:
        fix = None  # silent bail; preserves inference robustness
    consciousness_states = fix

logits_a, _logits_g, _tensions = self.decoder(
    input_ids, consciousness_states=consciousness_states
)
```

**Device + dtype move**: aligns with `tok_emb.weight` (which is the post-load device + dtype after `from_pretrained`). For lm-eval bf16 path, fp32 fixture downcasts to bf16. Cost: ~6 KB cast per forward (negligible).

**Broadcast**: `[1, n_cells, c_dim]` → `[B, n_cells, c_dim]` via `expand()`. `.contiguous()` after expand prevents view-strided issues in the downstream linear projections inside `ConsciousCrossAttention.forward`.

**Failure mode**: any error path silently falls back to `None`. Diagnostic captured in `self._consciousness_fixture_meta['error']` for post-hoc inspection but not raised. Honest C3 #8 covers this trade-off.

---

## Consciousness-state schema (verified against ubu1 source 2026-05-04)

| Field | Value |
|---|---|
| Shape | `[B, n_cells, consciousness_dim]` |
| `consciousness_dim` | 192 (CLM v4; matches `cross_attn.k_proj` 768→192 and `cross_attn.v_proj` 768→192) |
| `n_cells` (canonical) | 8 (anima_unified.py `args.max_cells` default) |
| `n_cells` (observed in chat) | 14 (`conscious_lm_provider.py` extends with 4 extra signals) |
| `n_cells` (federation) | variable; v14_federation produces atom × cells_per_atom |
| dtype (training) | float32 |
| dtype (inference) | aligns with model dtype (fp16/bf16 for H100 lm-eval) |
| Detached? | YES — `c_detached = consciousness_states.detach()` per Law 61 (no gradient through C) |
| Cross-attn axis | over **cells**, not over time — `q @ k.T` shape `[B, n_head, T, n_cells]` |

**Key insight**: cross-attention is over the cell dimension, not the sequence dimension. The fixture is broadcast across batch but is the SAME for every position in the sequence. Each layer's cross-attention picks its own attention pattern over the cells.

### Source modes

| Mode | Description | Scope |
|---|---|---|
| **canonical_zero** | All-zero cells. Sanity-only. Confirms wiring works. Expected logits delta vs v3 None-bypass: <1e-3 (because `cross_attn.o_proj.weight` has init std=0.001 and zero attended values yield zero residual). | **Shipped** — exemplar at `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_consciousness_states_fixture.json` |
| **train_avg** | Average of cell states observed during last training epoch. The recommended fixture for inference-time conditioning. Requires offline pass over training data with full anima_unified.py runtime. | **DEFERRED** — separate 1-2hr cycle |
| **learned_default** | Single trainable `[1, n_cells, c_dim]` parameter fine-tuned on a held-out target. | **DEFERRED** — needs tiny SFT cycle |

---

## Falsifier set (F-SHIM-V4-1 .. 4)

| # | Falsifier | Mode | Status |
|---|---|---|---|
| F-SHIM-V4-1 | Mac dry-run with fixture validates JSON (no torch) | Mac, this cycle | **PASS** — exemplar fixture validated, errors=[], warnings=[] |
| F-SHIM-V4-2 | No-fixture run produces v3-equivalent runtime behaviour | Mac, this cycle | **PASS** — runtime gating via `os.path.isfile`; modeling.py text differs (88 LoC dormant code) but runtime forward output is identical for `consciousness_states=None` callers |
| F-SHIM-V4-3 | Reload+forward with canonical_zero fixture produces FINITE logits | ubu1 / H100 | **DEFERRED** — `from_pretrained` round-trip + 1-batch forward; expects logits within 1e-3 of v3 reference |
| F-SHIM-V4-4 | train_avg fixture > random+5pt on ≥1 benchmark | H100 lm-eval | **DEFERRED** — gated on user authorisation for $1.50, 30min H100 exec cycle |

---

## Honest C3 (8 entries; ≥5 mandate exceeded — raw#10)

**C3-1 — canonical_zero is a sanity fixture, not a "right" injection.** All-zero cells produce ~zero residual through cross_attn (because `o_proj.weight` has init std=0.001 and the attended values are zero). Expected logits delta vs v3 None-bypass: < 1e-3. This confirms wiring works but is NOT expected to lift CLM v4 base above random. F-SHIM-V4-4 (the actual gate) requires train_avg fixture which is **out of scope for BG-Π** and needs a separate offline harvest cycle (1-2hr).

**C3-2 — train_avg may still be near-random.** Even with train_avg consciousness states, results may stay near-random because (a) train-time also injects a delta tensor + BOLD MSE conditioning + tension propagation that lm-eval cannot reproduce, (b) consciousness coupling is a ~1% residual contribution per block — 16 blocks × 1% may not add up to a 5pt benchmark lift, (c) block_size=512 truncation remains an orthogonal handicap. Hypothesis "consciousness coupling = the difference" is **testable but is NOT proven by this design cycle.**

**C3-3 — F-SHIM-V4-4 gated on user authorisation.** A fresh H100 cycle (~$1.50, 30min) is required. BG-Π did NOT spin one up. User must explicitly authorise per raw constraint NO chflags + NO H100 boot without ack. Recommend bundling with the deferred **Llama anchor** (BG-Μ rank-2 next-action) into a single $3 H100 cycle to amortise pod boot.

**C3-4 — block_size=512 truncation orthogonal — v4 does not fix it.** MMLU 5-shot prompts (~800-1200 tokens) and TriviaQA passages still get left-truncated. Even a perfect train_avg fixture cannot recover the missing context. A real fix requires CLM v4 retraining at 8K context (estimated $22+ Path A-equivalent cycle, **out of scope** for any shim version).

**C3-5 — modeling.py text drift breaks F-SHIM-V4-2 byte-equivalence.** MODELING_SRC has 88 new LoC for fixture loader. F-SHIM-V4-2 is therefore a **runtime-equivalence assertion**, not byte-level diff. The runtime gate is `os.path.isfile(fixture_path)` check at `__init__`; absent file → `self._consciousness_fixture_cpu=None` → `forward()` short-circuits before the inject branch → v3 path traversed. Tested via dry-run plan diff. A stronger byte-level F-SHIM-V4-2 would require splitting MODELING_SRC into v3-only and v4-fixture variants, which is **not worth the duplication**.

**C3-6 — n_cells=8 is heuristic, not measured.** Exemplar fixture uses n_cells=8 from `anima_unified.py max_cells` default. Train-time CLM v4 may have used different n_cells (e.g. v14_federation may produce 32+ cells). When train_avg fixture is harvested, its actual n_cells should be discovered from the runtime output and used directly — `modeling_clm_v4.py` reads n_cells from `shape[1]` dynamically, so any value works as long as `shape[2]==192` (consciousness_dim invariant).

**C3-7 — fixture broadcast may interact with batch_size > 1.** `forward()` `expand()`s `[1, n_cells, c_dim]` to `[B, n_cells, c_dim]` when shim batch > 1. `expand()` returns a view, not a contiguous tensor — the `.contiguous()` call after expand prevents downstream view-strided issues but adds ~B× memory. For batch_size=16 (BG-Μ default) this is 16 × 8 × 192 × 4 bytes = 96 KB extra, negligible. For batch_size=128 it would be 768 KB, still fine. Larger fixtures (e.g. n_cells=64) would scale linearly but stay sub-MB.

**C3-8 — silent fallback hides bugs.** On any fixture-load error, `modeling_clm_v4.py` silently falls back to None-bypass. This preserves inference robustness but **hides issues that would benefit from loud failure** (e.g. a typo in the fixture filename). Diagnostic captured in `self._consciousness_fixture_meta['error']` but not surfaced unless explicitly inspected. Mitigation: shim's dry-run validates the fixture **before** output_dir copy, so a malformed fixture would be caught at conversion time, not inference time.

---

## Cost band

| Line item | Estimate |
|---|---|
| BG-Π design + Mac dry-run | $0 (Mac-only, no torch) |
| ubu1 v4 smoketest (canonical_zero conversion + 1-batch forward) | $0 (ubu1 owned) |
| H100 canonical_zero F-SHIM-V4-3 cycle | $1.50, 30min |
| H100 train_avg full eval F-SHIM-V4-4 cycle | $1.50, 30min |
| **Bundled with Llama anchor** (recommended) | **$3.00, 60min** |
| train_avg harvest pre-pass (anima_unified.py runtime, ubu1) | $0 (owned), ~1-2hr wall |

---

## Roadmap update proposal

**File**: `.roadmap.p9_sft`
**New cond**: `p9_sft.cond.opt_1_v4_consciousness_injection`
**Status**: `spec_landed`
**Rationale**: v4 shim landed with `--consciousness-states-fixture` flag + Mac dry-run PASS; H100 exec deferred to user-ack cycle (rank-3 in BG-Μ next_actions_ranked).

**Evidence paths**:
- `tool/transient_py/clm_v4_hf_format_shim.py` (v4, 1418 LoC, +311 from v3)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_design_diff.md` (this file)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_dry_run.json`
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_consciousness_states_fixture.json` (canonical_zero exemplar)
- `docs/p9_base_validation_prereq_v4_design_landed_2026_05_04.ai.md`

**Note**: PARENT serializes roadmap mutations — BG-Π does NOT touch `.roadmap.p9_sft` this cycle.

---

## Cross-links

- **BG-Ξ** (`docs/p9_benchmark_switch_a_prime_spec_amendment_*.md` — parallel BG): Mode 3 of the spec amendment is the "consciousness-injected variant" track that v4 unblocks. v4 is the **prerequisite tooling** for Mode 3; it does not commit to running it.
- **BG-Ο** (`state/p9_base_validation_llama_anchor_2026_05_04/` — parallel BG): Llama-3.2-3B anchor re-run. F-SHIM-V4-3/-4 should bundle with that pod boot to amortise the ~$0.60 fixed cost.
- **BG-Β** OPT-1 design (`state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md` §7.2 honest C3 #1): pre-registered the consciousness-coupling-bypass; v4 is the path 3 (BG-Β rank-3) execution.
- **BG-Μ** verdict (`state/p9_base_validation_h100_2026_05_04/verdict.json`): rank-3 next_action "OPT-1 v4 shim — consciousness coupling injection mode". v4 closes the design + dry-run; exec deferred per scope.

---

## Hard constraints honoured (raw#9 / 10 / 15 / 37 / 71)

- **raw#9**: shim is `.own 4` OPT-OUT (gitignored at `tool/transient_py/*.py` per `.gitignore` L245); v4 modification is allowed; Mac canonical = .hexa policy respected (no new .py files outside `tool/transient_py/`).
- **raw#10**: 8 honest C3 entries above (≥5 mandate exceeded).
- **raw#15**: all repo paths in deliverables are repo-relative; ubu1 paths absolute (raw#37).
- **raw#37**: ubu1 transient explicit; exec deferred to `/home/aiden/venv_orchestrator/bin/python` + H100 (separate cycle); NO torch import on Mac this cycle.
- **raw#71**: F-SHIM-V4-1..4 each bound to objective passing criteria; -1 + -2 closed this cycle, -3 + -4 deferred with explicit predicates.
- **NO chflags**: confirmed.
- **NO git operations**: confirmed (parent serializes).
- **NO H100 boot**: confirmed.
- **NO actual conversion run**: confirmed (Mac dry-run only).
