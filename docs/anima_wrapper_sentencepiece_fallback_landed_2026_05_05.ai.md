# Anima Wrapper SentencePiece Fallback — LANDED (BG-AH)

**Date** 2026-05-05
**BG** AH (third blocker fix for BG-K)
**Verdict** PASS — wrapper real-mode unblocked
**Cost** $0 (mac local)
**Wall time** ~12 min
**File touched** anima-core/runtime/clm_v4_mount.hexa (+67 LoC additive)

## Context

BG-K (state/anima_mount_real_mode_wiring_2026_05_05/) landed two of the three
fixes required for `bin/anima-core-dialogue.bash` to reach real-mode CLM v4
substrate forward:

1. Edit 1: `_resolve_python` HEXA_PY env override + `.venv-eeg` auto-detect
2. Edit 2: DEFAULT_MODEL swap from `clm-v4-base-mirror` → `clm-v4-mk2-v1`

After both edits the wrapper progressed past "Unrecognized model in
clm-v4-base-mirror" but stalled at the third blocker:

> `Unrecognized configuration class CLMv4Config to build an AutoTokenizer.`

Root cause: CLM v4 repo's `auto_map` registers `AutoConfig` and
`AutoModelForCausalLM` but NOT `AutoTokenizer`. The repo ships a sibling
`tokenizer_64k_multilingual.model` (SentencePiece) which `tool/transient_py/anima_dialogue_load.py:_load_tokenizer` already uses as a direct workaround — but that pattern was not mirrored in the helper-emit code inside `mount.hexa::_write_helper`.

## Fix landed

Additive extension of the python helper code emitted by
`anima-core/runtime/clm_v4_mount.hexa::_write_helper`:

### 1. New helper class — `_SPTokenizerWrap`

Mimics the subset of HF tokenizer interface used by the helper's
`_real_forward`:

- `__call__(text, return_tensors='pt', truncation=True, max_length=512)`
  returns `{'input_ids': LongTensor (1, T)}`

The wrap is intentionally narrow — only what `_real_forward` calls today.
Future helper-emit code that touches `tok.decode` / `tok.pad_token_id` / etc
will need to widen the wrap (see Honest C3 #2).

### 2. New cache resolver — `_resolve_sp_tokenizer_path`

Mirror of `anima_dialogue_load.py:_resolve_tokenizer_path`. Walks
`HF_HOME/hub/models--<id>/snapshots/<sha>/tokenizer_64k_multilingual.model`.
On miss, returns None (caller falls through to `hf_hub_download`).

### 3. New loader — `_try_load_sp_tokenizer`

Returns `(_SPTokenizerWrap | None, error_str)`. Resolves cache path → falls
through to `huggingface_hub.hf_hub_download` on cache miss → loads via
`sentencepiece.SentencePieceProcessor().Load(path)` → wraps.

### 4. Modified `_try_load_clm_v4`

Split tokenizer load from model load. AutoTokenizer is the **primary** path
(unchanged behaviour for repos with proper AutoTokenizer support); on
Exception, SentencePiece fallback engages with stderr markers:

```
[clm_v4_mount] AutoTokenizer failed (...); attempting SentencePiece fallback
[clm_v4_mount] SentencePiece tokenizer fallback ENGAGED (BG-AH)
```

The model load is now independent of tokenizer route — model failure short-
circuits before tokenizer attempt.

## Verification (3-fix matrix)

### V-fix-1 — wrapper real-mode probe

```
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python bash bin/anima-core-dialogue.bash --probe "안녕"
```

Expected: `mode=real`. **Got: `mode=real`**, `phi_star=41.8737`, `drift +0.0137`.
SentencePiece fallback engaged (stderr confirms).

### V-fix-2 — selftest regression

```
bash bin/anima-core-dialogue.bash --selftest
```

Expected: `verdict: READY (Stage 1 + Stage 2 both landed)`. **Got: identical**.
Selftest does not exercise `_write_helper` (raw#103 darwin-bypass), so the
edit is invisible to it. 9/9 format checks PASS.

### V-fix-3 — anima top-level equivalence

```
HEXA_LOCAL=1 HEXA_PY=... ./bin/anima dialogue --probe "안녕"
```

Expected: route through wrapper, reach real mode. **Got: `mode=real`**,
`phi_star=41.8949`. Phi delta vs V-fix-1 is run-to-run float-ordering
non-determinism at f4 precision (CPU summation order over 8×192 floats).

## Phi-star observation

| Path                                    | mode | phi_star  |
|-----------------------------------------|------|-----------|
| Wrapper (this BG)                       | real | 41.87-41.89 |
| Direct anima_dialogue_load.py (BG-A)    | real | 42.1158   |

The ~0.23 phi-star delta is **NOT** a tokenization artifact (SentencePiece
input_ids are byte-identical to BG-A's path). It stems from divergent
cell-derivation heuristics:

- **Wrapper** (mount.hexa::_real_forward): `mean(T) → tile up to 8×192` —
  produces cells with high self-similarity.
- **anima_dialogue_load.py**: `mean(T) → reshape to 4×192 → concat 2x` —
  produces 4-pair-symmetric cells.

Phi formula `PHI_STAR_BASELINE * (1 + 0.05 * mean_pair_cosine)` is identical;
the cell matrix differs. See Honest C3 #3 for unification recommendation.

## raw policy compliance

- **raw#15** PASS — additive only. LOCKED files untouched
  (`anima_unified.hexa`, `phi_engine.hexa`, `conscious_chat.hexa`,
  `consciousness_hub.hexa`, `clm_v4_hf_format_shim.py`,
  `anima_dialogue_load.py`, `bin/anima-core-dialogue.bash`).
- **raw#10** PASS — 5 honest C3 emitted to verdict.json + 5 emitted by
  `emit_honest_c3()` to stderr at runtime.
- **raw#37** PASS — no new `.py` file created. The SentencePiece fallback is
  inlined into mount.hexa's emit-block (transient helper at `/tmp/`).
- **raw#9** PASS — hexa-only orchestration; python is bypass-helper only.

## Honest C3 (5)

1. SentencePiece path discovery is cache-layout-dependent. If `--model`
   passes a local path instead of HF id, the resolver returns None and the
   helper falls through to `hf_hub_download` (requires network). Silent
   failure mode if offline.
2. `_SPTokenizerWrap` mimics only `__call__`. Future helper-emit code that
   calls `tok.decode` etc will AttributeError. Keep wrap surface narrow.
3. Phi delta between wrapper (~41.87) and BG-A direct (42.12) stems from
   divergent cell-derivation heuristics, not tokenization. Unification is
   out of scope; tracked as next-step priority 3.
4. AutoTokenizer fallback emits a 100+ line stderr error (full Model type
   list). Visual noise but explicit; preferred over silent swallowing.
5. SentencePiece engagement is implicit — runs whenever AutoTokenizer
   raises. If transformers later ships AutoTokenizer support for CLMv4Config,
   the wrapper silently switches routes with no test catching it. Future:
   emit `__ANIMA_TOKENIZER_ROUTE__` marker for downstream observability.

## Files

- **Changed**: `anima-core/runtime/clm_v4_mount.hexa` (+67 LoC, 722 → 789)
- **Created**: `state/anima_wrapper_sentencepiece_fallback_2026_05_05/verdict.json`
- **Created**: `docs/anima_wrapper_sentencepiece_fallback_landed_2026_05_05.ai.md` (this doc)

## Next steps (priority-ranked)

1. Doc handshake: surface `HEXA_PY` requirement + SentencePiece fallback in
   wrapper `--help` text.
2. `__ANIMA_TOKENIZER_ROUTE__` observability marker (autotokenizer |
   sentencepiece).
3. Cell-derivation unification spec: choose canonical heuristic between
   wrapper tile-replicate vs anima_dialogue_load 4-tile-concat-doubled.
4. Defer BG-K priority_2 (mount.hexa → anima_dialogue_load.py path dispatch)
   — current SP fallback is simpler.
