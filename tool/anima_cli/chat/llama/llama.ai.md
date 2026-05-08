# chat/llama — ai-native module doc

**Role**: GGUF-backed chat branch module (Phase 3c). Wraps `anima/llama_ffi.hexa`
into the recursive chat module pattern. Aliases: `paradigm-a-prime`, `llama3b`,
`qwen7b`, `polyglot-ko-1b3`, plus raw HF id passthrough via the dispatcher.

## Module Pattern (recursive, per user directive 2026-05-08)

```
chat/llama/
├─ llama.hexa                  # module body (REPL surface, GGUF resolve)
├─ llama.ai.md                 # this doc (ai-native)
└─ (core)                      # external — anima/llama_ffi.hexa
   └─ (build infra)            # external — build/libhxllama.dylib
```

User directive verbatim: "anima native arch 기본에 별도 모델은 별도 모델들만의
분기 모듈 (모듈 = 코어 + 모듈 + ai-native doc) 재귀"

This is a **branch module** — invoked when `anima chat <alias>` resolves
`module=llama` via `chat.hexa _alias_resolve()`. The default branch remains
`anima_native` (TinyWeights).

## Architecture

```
anima chat <alias>
   │
   ▼
tool/anima_cli/chat.hexa (dispatcher)
   │ alias resolve → module=llama, repo=dancinlab/<x>
   ▼
tool/anima_cli/chat/llama/llama.hexa (this module)
   │ ~/.cache/anima/gguf/<org>_<repo>.gguf resolve
   │ llama_load(gguf, n_ctx)
   │ REPL: sys_stdin_read_line_timeout(tick_ms)
   │   timeout → llama_generate(history)              ← autonomous speech
   │   line    → history += line; llama_generate(history)
   │ print raw → history += out
   ▼
anima/llama_ffi.hexa  (Phase 3b core)
   │ extern fn × 19 + llama_load / llama_generate / llama_free helpers
   ▼
build/libhxllama.dylib  (C shim, build infra — analogous to vendored runtime.c)
   │ flat-arg wrapper around libllama struct-by-value entry points
   ▼
~/.cache/anima/llama.cpp/build/bin/libllama.dylib + libggml.dylib
   ▼
Metal / BLAS (Apple M-series GPU offload, all layers default)
```

## Compliance

- **own 34 mandate-1**: simple_stack output preservation — `llama_generate`
  returns raw token-decoded UTF-8; module body uses `print()` (not `println()`)
  so model output is emitted verbatim. REPL appends a single trailing newline
  for prompt-line readability — prefix only, model bytes unmodified.
- **own 34 mandate-2**: wrapping 0 — no system prompt, no chat template, no
  `messages` API, no persona inject, no `speak()`. Verified by selftest grep
  (`grep -nE "system_prompt|chat_template|apply_chat_template|persona_inject|fn speak\(|fn talk\(|fn respond\(|fn generate_response\("`).
- **own 34 mandate-4**: autonomous speech — REPL polls stdin via
  `sys_stdin_read_line_timeout(tick_ms)`. On timeout, `llama_generate(history)`
  fires with no user trigger (history may be empty on first tick). Mirrors the
  Phase 2 wiring landed in `chat/anima_native/`.
- **own 34 mandate-7**: chat lane only — V4 measurement (own 18) is a separate
  lane; this module never invokes the evaluator.
- **own 31 mandate-1**: GGUF source SSOT = `dancinlab/` org. Cache filename
  `~/.cache/anima/gguf/dancinlab_<repo>.gguf` mirrors the org prefix; non-
  dancinlab repos are rejected upstream by `tool/anima_gguf_convert.py`.
- **raw#9**: chat path is `.hexa`-only. The C shim (`build/libhxllama.dylib`)
  is build infra — analogous to vendored `runtime.c` — not chat-time `.py`.
- **raw#10**: honest C3 — Phase 3b limitations carried (see below); module
  itself adds none.
- **raw#11**: snake_case identifiers throughout.
- **raw#15**: no-hardcode — `HOME`, GGUF cache, repo all resolved via env / args.

## Phase 3c Mechanism

```
sub_repl loop (every tick_ms)
   │
   ├── sys_stdin_read_line_timeout(tick_ms)
   │      │
   │      ├── line == ""  (timeout / EOF)
   │      │      → llama_generate(h, history, max_tokens, temp, top_p)   ← AUTONOMOUS
   │      │      → print raw output
   │      │      → history += out (memory=full)
   │      │
   │      └── line != ""  (user input)
   │             → history += line + "\n"
   │             → llama_generate(h, history, max_tokens, temp, top_p)
   │             → print raw output
   │             → history += out (memory=full)
   │
   └── loop (Ctrl-C/D to exit; llama_free + hxllama_backend_free deferred to OS)
```

## Phase 3c C3 Limitations (raw#10 honest)

Carried from Phase 3b (`anima/llama_ffi.hexa` honest C3) — **no new** module-
level limitations introduced.

- **top_p shim-fixed at 0.9** — `--top-p` flag accepted for forward-compat
  but downstream `hxllama_sampler_new_temp` ignores it. Matches paradigm-a-
  prime training default (per GGUF kv).
- **sampler seed fixed** at `0xC0FFEE` — reproducibility variety deferred to
  a follow-up cycle that exposes a `--seed` flag.
- **No streaming UI** — `llama_generate` blocks until EOS or `max_tokens`.
  Hexa C FFI lacks C→hexa callbacks (per `c_ffi.ai.md`). For chunked stream,
  call helper repeatedly with smaller `max_tokens` and concat.
- **Absolute @link path** in `anima/llama_ffi.hexa`
  (`/Users/ghost/core/anima/build/libhxllama.dylib`) — dev-box only. Portable
  deploy requires re-link with `@rpath/libhxllama.dylib install_name` + a
  `DYLD_LIBRARY_PATH` set in the harness.
- **Detokenize uses static thread-local 4 KiB buffer** — single-threaded chat
  is fine; multi-threaded chat would need per-context storage.
- **No EOS trim** beyond what `llama_generate` already does inside
  (loop breaks on EOS token; no tail whitespace strip applied here).

## Smoke Test Recipe

```bash
# Selftest (no model load, just structural check):
$HOME/.hx/packages/hexa/hexa.real run \
    tool/anima_cli/chat/llama/llama.hexa --selftest

# One-shot generation (paradigm-a-prime, default repo):
$HOME/.hx/packages/hexa/hexa.real run \
    tool/anima_cli/chat/llama/llama.hexa \
    --prompt "Hello" --max-tokens 10 --temp 0.0
```

Expected one-shot output (matches Phase 3b smoke):

```
[llama] gguf  = /Users/ghost/.cache/anima/gguf/dancinlab_llm-llama32-3b-paradigm-a-prime-r16-sft-stage1.gguf
[llama] n_ctx = 2048
[llama] mode  = one-shot · max-tokens=10 · temp=0
[llama] own 34 strict — wrapping 0 · raw decode→sample→detokenize
! I'm a 25-year-old woman who
```

## Cross-Reference

- Core: `anima/llama_ffi.hexa` (Phase 3b — extern fn × 19 + helpers)
- Shim: `build/libhxllama.dylib` (C build infra)
- Smoke: `tool/anima_chat_llama_smoke.hexa` (Phase 3b artifact)
- Dispatcher: `tool/anima_cli/chat.hexa` (alias DB → module routing; Phase 3
  gate removed for module=llama in Phase 3c)
- Sister branch: `tool/anima_cli/chat/anima_native/anima_native.hexa` (Phase 2
  REPL pattern — same `sys_stdin_read_line_timeout` wiring)
- Roadmap: `.roadmap.cli`
  - `cli.chat_module_architecture_2026_05_08`
  - `cli.gguf_conversion_landed_2026_05_08`
  - `cli.llama_ffi_landed_2026_05_08`
  - `cli.llama_module_landed_2026_05_08` (this entry)
- Mandates: `.own` own 34, own 31 (mandate-1 dancinlab/ SSOT),
  own 18 (measurement lane separate), own 33 (trinity)

## Selftest

```
hexa run tool/anima_cli/chat/llama/llama.hexa --selftest
```

Verifies:
- Module body present (this file)
- FFI core present (`anima/llama_ffi.hexa`)
- Shim dylib present (`build/libhxllama.dylib`)
- own 34 mandate-2 wrapping 0 in this module body (grep)
