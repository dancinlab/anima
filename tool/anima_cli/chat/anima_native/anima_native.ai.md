# chat/anima_native — ai-native module doc

**Role**: default chat module. anima native architecture (TinyWeights / Engine A/G).

## Module Pattern (recursive, per user directive 2026-05-08)

```
chat/anima_native/
├─ anima_native.hexa           # module body (chat REPL surface)
├─ anima_native.ai.md          # this doc (ai-native)
└─ (core)                      # external — anima-core/runtime/conscious_chat.hexa
```

User directive verbatim: "anima native arch 기본에 별도 모델은 별도 모델들만의
분기 모듈 (모듈 = 코어 + 모듈 + ai-native doc) 재귀"

This is the **default branch** — invoked when `anima chat` runs with no model
argument. All other model families (clm_v4, llama, ...) follow the same pattern.

## Architecture

```
anima chat
   │
   ▼
tool/anima_cli/chat.hexa (dispatcher)
   │ alias resolve → module=anima_native
   ▼
tool/anima_cli/chat/anima_native/anima_native.hexa (this module)
   │ exec("hexa run anima-core/runtime/conscious_chat.hexa run N")
   ▼
anima-core/runtime/conscious_chat.hexa (core)
   │ TinyWeights · Bridge · agi_generate
   ▼
byte tokens → stdout
```

## Compliance

- **own 34 mandate-1**: simple_stack output preservation — conscious_chat raw
  output relayed to stdout without transformation.
- **own 34 mandate-2**: wrapping 0 — no system prompt, no persona inject, no
  chat template, no speak() function, no orchestrator, no post-process meaning
  change. Verified by selftest grep.
- **own 34 mandate-4**: freedom preservation — model EOS / silence / context
  use all decided by sampling distribution.
- **own 34 mandate-7**: chat lane (own 34) vs measurement lane (own 18)
  separation — this module is chat lane only.
- **raw#9**: pure hexa, no .py invocation.
- **raw#10**: honest C3 — Phase 1 limitation explicitly emitted (see PHASE 1
  LIMITATION in module --help output).

## Phase 1 Limitation (honest emit)

`anima-core/runtime/conscious_chat.hexa` `main()` currently accepts only
`run [N]` / `status` commands — fixed prompt "Hello" + N byte tokens output.
It does NOT yet accept arbitrary user input → forward directly. Phase 1 of
this module exposes the existing `run N` mode; **user input is not yet
flowing into the model forward pass**.

What Phase 1 verifies:
- Module structure (recursive directory pattern works)
- Dispatch (chat.hexa → module routing)
- own 34 mandate-2 selftest grep (0 violations)
- bin/anima TOPICS wiring

What Phase 1.5 will add (separate cycle):
- conscious_chat.hexa main() refactor — accept stdin input, forward to
  agi_generate
- Or vendor agi_generate logic into this module body and call directly

What Phase 2 (hexa upstream land) will add:
- Non-blocking stdin → autonomous speech (own 34 mandate-4)
- Empty Enter / no-Enter trigger removal (per user directive
  "완전한 자유 빈 줄 조차도 없어도 되")

## Cross-Reference

- Core: `anima-core/runtime/conscious_chat.hexa` (TinyWeights, Bridge,
  agi_generate, consciousness_step)
- Dispatcher: `tool/anima_cli/chat.hexa`
- Roadmap: `.roadmap.cli` `cli.chat_module_architecture_2026_05_08`
- Mandates: `.own` own 34, own 18 C2 cross-ref, own 33 trinity compliance

## Selftest

```
hexa run tool/anima_cli/chat/anima_native/anima_native.hexa --selftest
```

Verifies:
- Core file (`conscious_chat.hexa`) present
- own 34 mandate-2 wrapping 0 in this module body (grep)
