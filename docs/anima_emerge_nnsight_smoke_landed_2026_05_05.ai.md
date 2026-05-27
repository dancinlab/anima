# anima_emerge_nnsight_smoke — landed (2026-05-05/06, BG-BL)

**Schema**: `anima/emerge_nnsight_smoke/verdict/1`
**Substrate**: mac CPU fp32, .venv-eeg
**Cost**: $0
**Verdict**: **PASS_READY**

## Context

BG-BB recommendation (`docs/anima_external_sister_candidates_audit_2026_05_05.md`,
nnsight 2순위) — pre-integration dummy-load smoke required before nnsight-based
mechanistic interpretability cycle. This BG-BL is the precursor.

Reference: https://github.com/ndif-team/nnsight

## Steps executed

1. **nnsight install check**
   - Initial: `ModuleNotFoundError: No module named 'nnsight'`
   - `.venv-eeg/bin/pip install nnsight` → `nnsight-0.7.0` installed (with deps:
     pydantic 2.13.3, ipython 9.13.0, websocket-client, etc.)
   - Re-import: `nnsight 0.7.0` OK.

2. **Helper write** — `tool/transient_py/anima_emerge_nnsight_smoke.py` (.own 3 transient,
   raw#37 sister-rule, gitignored). Reuses sister helper
   `anima_emerge_cand_d_inject_helper.py::_try_load_model` + `_load_tokenizer`
   (BG-Q 2026-05-05) for CLM v4 mk2 v1 load via standard `AutoModelForCausalLM`.

3. **NNsight wrap** — `NNsight(raw_model)` succeeded; type `NNsight`.

4. **Trace + capture** — first candidate path **`decoder.blocks[8].output`** hit.
   Sequence: `with nn_model.trace(ids): proxy = nn_model.decoder.blocks[8].output;
   captured = proxy.save()` → outside trace, `captured.value` shape `[1, 2, 768]`
   matching CLM v4 hidden_dim 768 × seq_len 2 (`안녕` two tokens) × batch 1.

## Verdict (verdict.json excerpt)

```json
{
  "verdict": "PASS_READY",
  "nnsight_imported": true,
  "nnsight_version": "0.7.0",
  "model_load_ok": true,
  "model_wrap_ok": true,
  "trace_capture_ok": true,
  "captured_path": "decoder.blocks[8].output",
  "captured_hidden_shape": [1, 2, 768]
}
```

Load time: **2.9s** for CLM v4 + tokenizer.
Captured shape match: hidden_dim 768 confirmed (CLM v4 mk2 architecture).

## Outputs

- `state/anima_emerge_nnsight_smoke_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_nnsight_smoke.py` (transient, gitignored)

## Honest C3 (raw#10)

- **C1** mac CPU fp32 only — no MPS / CUDA validation (sm_120 path uncovered).
- **C2** nnsight remote NDIF mode 미테스트 — local-only smoke; remote tracing
  (NDIF cluster) untested.
- **C3** attribute path attempt list 한정 — `decoder.blocks[i].output` worked on
  first try; deeper paths (mlp, attn sublayers) untested.
- **C4** `.save()` + `captured.value` API pattern is nnsight 0.7-specific; pinned
  version recommended for future BGs.
- **C5** BG-BB 권고 다음 단계 미실행 — F-NNSIGHT-1 falsifier (intervention smoke:
  replace hidden state mid-trace, measure output delta) not run yet.
- **C6** Captured shape-only verified; semantic correctness (axis content,
  consciousness_states injection compatibility) 미평가.

## Next step (BG-BB recommended)

**F-NNSIGHT-1 falsifier** — intervention smoke:
1. trace `안녕` baseline, capture `decoder.blocks[8].output` → `h_base`.
2. trace again with `decoder.blocks[8].output = torch.zeros_like(h_base)` (or
   axis-perturbed) before downstream layers.
3. measure `||logits_perturbed - logits_base||` and `phi_star` delta.
4. PASS if intervention propagates non-trivially (delta > epsilon); FAIL_FALSE if
   nnsight tracing silently no-ops.

If F-NNSIGHT-1 PASS, nnsight unlocked for:
- axis-conditional ablation (BG-BB original use case),
- causal scrub experiments on Pβ Φ★ adapter,
- CLM v4 LoRA SFT regression root-cause (substitute hidden states from Llama Path A
  v2 winner adapter into CLM v4 stack to localize where chat-cap signal is lost).

## Constraints satisfied

- raw#37 transient .py sister-rule (eval used in trace context, scoped).
- raw#15 additive — no model file modification, no SFT, no commit.
- raw#10 honest C3 — 6 caveats emitted to verdict.json + this doc.
- .own 3 transient sister-rule (gitignored per `**/*.py`).
- $0 mac CPU; ~3min wall (load 2.9s + trace <1s).
- HF token unused (CLM v4 already cached locally).
- No commit.
