# anima mount real-mode wiring landed (2026-05-05) — BG-K

## TL;DR

Two additive fixes landed in `anima-core/runtime/clm_v4_mount.hexa` per spec:
1. `_resolve_python` gained HEXA_PY env override + `.venv-eeg` auto-detect (additive; existing fallback chain preserved).
2. `DEFAULT_MODEL` const swapped from `need-singularity/clm-v4-base-mirror` (pre-HF best.pt mirror, lacked `model_type`) to `need-singularity/clm-v4-mk2-v1` (HF-format repo).

`raw#15` PASS — `_resolve_python` was extended (not edited), and only `clm_v4_mount.hexa` was touched. All other LOCKED files (`anima_unified.hexa`, `phi_engine.hexa`, `conscious_chat.hexa`, `consciousness_hub.hexa`, `clm_v4_hf_format_shim.py`, `anima_dialogue_load.py`, `anima-core-dialogue.bash`) are UNTOUCHED.

`--selftest` regression: NONE. `verdict: READY (Stage 1 + Stage 2 both landed)` preserved.

## V-fix-1 (wrapper real-mode probe) — PARTIAL PROGRESS, NOT FULL PASS

The 2 fixes ARE necessary and ARE correctly applied. They progressed the wrapper from the BG-A `Unrecognized model in clm-v4-base-mirror` failure (no `model_type` in config.json) to a deeper failure: `Unrecognized configuration class CLMv4Config to build an AutoTokenizer`. That is, the model class IS now loadable (auto_map registers `AutoConfig: CLMv4Config` and `AutoModelForCausalLM: CLMv4ForCausalLM`), but the helper inside `mount.hexa::_write_helper` calls `AutoTokenizer.from_pretrained(...)` which has no AutoTokenizer mapping.

This is a **third architectural blocker** beyond the BG-A 2-cause diagnosis. CLM v4's `tokenizer_64k_multilingual.model` is SentencePiece, and the BG-A helper at `tool/transient_py/anima_dialogue_load.py` correctly side-steps via direct `sentencepiece.SentencePieceProcessor()` loading. The mount.hexa-emitted helper does not have that fallback.

Wrapper real-mode therefore still emits `mode=synthetic_fallback`. Direct invoke of `anima_dialogue_load.py` (BG-A canonical path) continues to reach real-mode (`phi_star 42.1158`).

## V-fix-2 (selftest regression) — PASS

`bash bin/anima-core-dialogue.bash --selftest` -> `verdict: READY (Stage 1 + Stage 2 both landed)` (unchanged).

## V-fix-3 (anima top-level path) — PASS for routing equivalence

`HEXA_LOCAL=1 HEXA_PY=... ./bin/anima dialogue --probe "안녕"` correctly routes through `tool/anima_cli/dialogue.hexa` -> `bin/anima-core-dialogue.bash` -> `clm_v4_mount.hexa --probe`. Output is byte-identical to direct wrapper invocation. The routing is correct; the only blocker is the same V-fix-1 AutoTokenizer issue.

Note: without `HEXA_LOCAL=1`, `anima` top-level dispatches through docker by default and emits `sh: /Users/ghost/.hx/bin/hexa: not found` container-internal error (anima_runtime resolver behavior, unrelated to this BG).

## What works now that didn't work before

- HEXA_PY env override path is the documented developer affordance for venv selection.
- `.venv-eeg/bin/python` auto-detect is the implicit fallback for typical anima dev environments.
- `--model need-singularity/clm-v4-mk2-v1` is the default; mount.hexa now points to the HF-format repo with `model_type=clm_v4` registered.
- Model class instantiation via `AutoModelForCausalLM.from_pretrained` proceeds further (config class loads).

## What still doesn't work — third blocker

`AutoTokenizer.from_pretrained` rejects CLMv4Config because the auto_map has no AutoTokenizer entry. The helper has no SentencePiece fallback.

## Path forward (next BG)

Two options to fully unblock wrapper real-mode (both additive, raw#15-safe in mount.hexa scope):

- **Option A** (in-place SentencePiece fallback, ~30 LoC): augment `mount.hexa::_write_helper`'s `_try_load_clm_v4` Python emit with a try/except that falls back to `sentencepiece.SentencePieceProcessor` loading `tokenizer_64k_multilingual.model` from the snapshot directory (mirror `anima_dialogue_load.py:_load_tokenizer`).

- **Option B** (route to existing helper, ~15 LoC): teach `mount.hexa::_build_cmd` to dispatch CLM v4 family models to `tool/transient_py/anima_dialogue_load.py` directly (path-based dispatch), reusing the BG-A-tested code path. Avoids duplicating tokenizer logic.

Option B is cleaner; Option A keeps everything inside mount.hexa.

## Honest C3 (raw#10)

- C1 HEXA_PY env override is invisible to general users. Documentation must surface this in `bin/anima --help`, `anima dialogue --help`, and the spec doc. The `.venv-eeg` auto-detect handles typical cases but is fragile to non-canonical venv layouts.
- C2 The 2 spec-mandated fixes are necessary but NOT sufficient for wrapper real-mode. A third architectural fix (Option A or B above) is required.
- C3 BG-A's verdict claimed `HEXA_PY env + --model` would unblock the wrapper. Empirical test refutes that — the third AutoTokenizer blocker is real, independent, and persistent regardless of HEXA_PY/model fixes.
- C4 `.venv-eeg` auto-detect creates implicit coupling. If user renames or removes `.venv-eeg`, resolver silently falls to system python3, which has the OMP `libomp` double-init bug. A fail-loud stderr warning would help.
- C5 Until the third blocker is fixed, direct invoke of `tool/transient_py/anima_dialogue_load.py` remains the canonical real-mode entry. The wrapper `bin/anima-core-dialogue.bash` is best-effort fallback infrastructure today, not a real-mode entry point.

## Files changed

- `anima-core/runtime/clm_v4_mount.hexa` — 5 small edits (1 functional `_resolve_python` extension; 1 functional `DEFAULT_MODEL` const swap; 3 doc/consistency one-liners for `_argparse` default, header comment, `print_usage`).

## Files created

- `state/anima_mount_real_mode_wiring_2026_05_05/verdict.json`
- `docs/anima_mount_real_mode_wiring_landed_2026_05_05.ai.md` (this file)

## Cost + time

$0 (mac local), 14 minutes wall-time.
