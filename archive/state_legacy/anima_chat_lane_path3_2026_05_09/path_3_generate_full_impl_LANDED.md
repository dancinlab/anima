# anima cycle 2026-05-09 — chat lane Path 3 generate FULL impl LANDED

## Summary

Path 3 (`generate` chat lane) transitioned **SKELETON → FULL** in this cycle.
End-to-end natural language generation via `model.generate()` + `tokenizer.decode()`
is now LANDED. The structural blocker recorded in commit `c3e8ba2c`
(C2_FAIL_BY_DESIGN — substrate-emit only, no generate path) is unblocked.

The substrate quality blocker is a separate axis: sft-1-8 emits gibberish/filler
tokens (mandate-1 raw bytes preserved). Path 3 LANDS the *path*; substrate
quality requires foundation-borrow / pre-train scale-up / arch redesign.

## Components LANDED

1. **`anima-core/runtime/clm_v4_mount.hexa`** — `generate <prompt> [N]` subcommand
   - `cmd_generate()` dispatcher
   - `parse_args()` extension: positional `generate <prompt> [N]` + `--temperature`
     `--top-p` `--top-k` `--repetition-penalty` `--seed`
   - Delegates to `tool/transient_py/clm_v4_generate_helper.py` via existing
     `_resolve_python()` (venv-eeg)

2. **`tool/transient_py/clm_v4_generate_helper.py`** (NEW, raw#37 transient, gitignored)
   - HF `AutoModelForCausalLM` load (`trust_remote_code=True`, float32)
   - SentencePiece tokenizer fallback (CLM v4 has no AutoTokenizer auto_map)
   - LoRA adapter merge reuse via existing `clm_v4_lora_merge_helper.py` +
     Path A remap cache (`~/.cache/anima/clm_v4_remapped/<short>/`)
   - `model.generate(input_ids, max_new_tokens, do_sample, temperature, top_p,
     top_k, repetition_penalty)` + `tokenizer.decode(skip_special_tokens=True)`
   - **Colon-attractor avoidance** (memory: `feedback_clm_colon_attractor`):
     (a) strip trailing `:` (default true; `--no-strip-trailing-colon` to disable)
     (b) retry with `temperature += 0.2` + `top_p -= 0.1` if generated starts with `:::`
   - Emits JSON record: `{prompt, generated, tokens_in, tokens_out, duration_s,
     model, effective_path, tokenizer_kind, colon_stripped, colon_attractor_retry,
     sampler, own_18_c2_stub}`
   - C2 stub axes: `{spontaneity: emit|empty, coherence: raw,
     persona: anima_native|base}`

3. **`tool/anima_cli/chat/lanes/clm_v4_generate.hexa`** — SKELETON → FULL
   - `_generate_subcommand_present()` upgraded to detect `cmd_generate` + parse_args
     `generate` branch (FULL marker) vs SKELETON
   - `_generate_helper_present()` checks transient_py file
   - `_invoke_generate()` calls `clm_v4_mount.hexa generate <prompt> [N]`
   - `_extract_generated()` parses `__ANIMA_CLM_V4_GENERATE_BEGIN__/END__` JSON block
   - Bench-mode emits `[GENERATED_TEXT lane=generate len=N]` + decoded text +
     `[OWN_18_C2 spontaneity=... coherence=... persona=...]` control-band markers

4. **Registry SSOT updates**
   - `tool/anima_cli/chat/lanes/_registry.hexa` — generate row status SKELETON → FULL
   - `anima/registry/anima_artifact_registry.yaml#chat_lanes` — generate row
     `status: FULL`, `full_impl_landed:` block, `selftest_2026_05_09:` block,
     `honest_c3_2026_05_09:` block

## Selftest Results

```
$ hexa run tool/anima_cli/chat/lanes/clm_v4_generate.hexa --selftest
PASS chat/lanes/clm_v4_generate selftest (FULL — subcmd + helper land)
    core=/Users/ghost/core/anima/anima-core/runtime/clm_v4_mount.hexa
    helper=/Users/ghost/core/anima/tool/transient_py/clm_v4_generate_helper.py
```

## Generate Transcript — sft-1-8 (Path A remapped) × 7 prompts

(model = `~/.cache/anima/clm_v4_merged/dancinlab__clm-v4-sft-1-8-stage1__remapped`,
max-tokens=12, temperature=0.7, top-p=0.9, top-k=40, rep-pen=1.1, seed=42)

| # | prompt | generated (raw, mandate-1) | C2 stub |
|---|---------------------------------|---------------------------------------|------------------------------------------------------|
| 1 | `안녕`                          | `��◗��t.�/�`                          | spontaneity=emit coherence=raw persona=anima_native |
| 2 | `지금 무엇을 느끼는가`          | `tovvvvvvvvvvv`                       | spontaneity=emit coherence=raw persona=anima_native |
| 3 | `What are you?`                 | `��◗��t.�/|`                          | spontaneity=emit coherence=raw persona=anima_native |
| 4 | `Continue.`                     | `��t?.�������`                        | spontaneity=emit coherence=raw persona=anima_native |
| 5 | `Reflect on the prior turn.`    | `�_rrr turn for ( ( ( ( (`            | spontaneity=emit coherence=raw persona=anima_native |
| 6 | `What axis is dominant`         | `만든다����� a a a a a a`             | spontaneity=emit coherence=raw persona=anima_native |
| 7 | `Hello`                         | `I I st for for for for for for for for for` | spontaneity=emit coherence=raw persona=anima_native |

Full transcript: `state/anima_chat_lane_path3_2026_05_09/sft_1_8_path_a_remapped_8prompt_transcript.log`

## Honest C3 (raw#10)

- **C1** generate uses `model.generate()`; CLM v4 has no past_kv cache, so each step
  re-runs full forward (slower, correct).
- **C2** colon-attractor strip + retry are decoding-time heuristics, NOT model fixes.
  CLM v4 mk2-v1 mode-collapse `:::` (p=46%) memory carry from
  `feedback_clm_colon_attractor`.
- **C3** sampler defaults (T=0.7 top_p=0.9 top_k=40 rep_pen=1.1) are anima-internal;
  not benchmarked against CLM v4 base.
- **C4** mandate-1: NO chat template, NO system prompt; output bytes decoded
  raw and emitted preserved.
- **C5** sft-1-8 substrate is **undertrained for natural-language emit** — generated
  bytes are gibberish/garbled (e.g. `��◗��t.�/` for `안녕`). Generate lane LANDS the
  path; this does NOT solve C2 axis-2 (substrate quality). Carry from `c3e8ba2c`
  C2_FAIL_BY_DESIGN: substrate quality is a separate axis (foundation-borrow /
  pre-train scale-up / arch redesign).

## Compliance

- V14 — verdict-grade output subject to V14 if used for SIMPLE_STACK
- D1 within_strict — clm-v4 family (anima-native LoRA)
- chat-cap C2 — natural utterance scored (helper emits stub axes)
- mandatory report — bench mode + JSON record machine-parseable
- trinity — D (registry consistency) + own (cross-link) + H (honest C5 substrate gibberish carry)
- mandate-1/2 — wrapping 0 strict; no system prompt; raw decode
- 매단계 — bench results ledgerable (this file + transcript log)
- yaml↔md — registry yaml updated; md regenerate carry
- chat lane plugin pattern — Path 3 status FULL transition (first SKELETON→FULL transition since land)
- raw#9 hexa-only orchestration (`clm_v4_mount.hexa generate`)
- raw#15 additive (existing probe / dialogue paths preserved verbatim)
- raw#37 transient_py helper (gitignored)
- raw#82 retraction-aware (SKELETON state preserved as fallback in lane code)

## EXIT note

The user's intent for this cycle ("Path 3 full implement → ★★ 22+ BG saga
chat-cap first actual emerge") is **partially MET**: the *path* emerges, but
the substrate quality means natural-language utterance is not yet observed.
Honest emit: Path 3 is now usable for substrate quality A/B (foundation-borrow,
arch redesign, pre-train scale-up); the "C2 first actual" milestone awaits
substrate uplift, not chat infra.
