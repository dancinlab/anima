# chat/clm_v4 — ai-native module doc

**Role**: CLM v4 substrate dialogue branch. Anima's own architecture lineage
(mk2-v1 350M base + LoRA — research/reproducibility, not chat-capable).

## Module Pattern (recursive)

```
chat/clm_v4/
├─ clm_v4.hexa          # module body (REPL surface + repo passthrough)
├─ clm_v4.ai.md         # this doc
└─ (core)               # external — anima-core/runtime/clm_v4_mount.hexa
```

## Aliases

| alias | repo | note |
|---|---|---|
| `clm-v4-1-7-y1` | `dancinlab/clm-v4-sft-1-7-y1-stage1` | Phase 1.7 Y1 |
| `clm-v4-1-8` | `dancinlab/clm-v4-sft-1-8-stage1` | Phase 1.8 |
| `clm-v4-paradigm-j` | `dancinlab/clm-v4-paradigm-j-50k-final` | jvae_heads.pt 별도 |

raw HF id (`dancinlab/clm-v4-...` 형식) 도 alias 자리에 직접 입력 가능 — chat
dispatcher가 `clm-v4` substring 으로 module 자동 라우팅.

## Architecture

```
anima chat clm-v4-1-7-y1
   │
   ▼
chat.hexa (dispatcher, alias resolve → module=clm_v4 + repo)
   │
   ▼
chat/clm_v4/clm_v4.hexa (this module)
   │ exec("hexa run anima-core/runtime/clm_v4_mount.hexa --model <repo> --probe TEXT")
   ▼
anima-core/runtime/clm_v4_mount.hexa (core)
   │ tokenizer.encode → model.forward → axis activation + phi-star + dominant cells
   ▼
substrate response (raw, including ::: collapse) → stdout
```

## Compliance

- **own 34 mandate-1**: simple_stack output preservation — `clm_v4_mount.hexa`
  의 substrate response 변형 없이 stdout 직출.
- **own 34 mandate-2**: wrapping 0 — selftest grep verified.
- **own 34 mandate-4**: 자율 발화 wired Phase 2 (LANDED 2026-05-08, iter 3 b-fix)
  — `sys_stdin_read_line_timeout(tick_ms)` polls stdin; on timeout
  `_invoke_substrate("")` fires (empty probe) → substrate 자체 free-run.
- **own 34 mandate-7**: chat lane = thin pipe; substrate response decision
  은 `clm_v4_mount.hexa` (model layer) 책임.
- **own 34 mandate-1 ★ 핵심**: `:::` collapse mode (memory feedback_clm_colon_attractor:
  p=46% on `:`-terminated prompt) 도 raw 그대로 노출. mitigate / strip / filter
  하지 않음. CLM v4 의 학습 분포 그 자체가 사용자에게 보여야 함.

## Phase 2 (LANDED 2026-05-08, iter 3 b-fix)

**Bug** (iter 2 (b) 5-turn live retest blocker):
`Runtime error: undefined function: read_line` — `sub_repl` 가 hexa stdlib
미정의 함수 `read_line()` 직접 호출 + `use "stdlib/sys"` import 누락.

**Fix** (mirrors `chat/anima_native/anima_native.hexa` Phase 2 pattern):
- `use "stdlib/sys"` import added.
- `read_line()` → `sys_stdin_read_line_timeout(tick_ms)` swap.
- `--tick-ms N` flag (default 1000ms) — REPL poll cadence.
- Timeout path → `_invoke_substrate("")` (own 34 mandate-4 자율 발화).
- `_hexa()` → `/Users/ghost/.hx/packages/hexa/hexa.real` (local interp,
  matches anima_native + llama; bin/hexa wrapper would route to remote
  ubu-1 and lose stdout pipe semantics needed for `chat/duo/` channel
  transport).

## Honest C3 (raw#10)

| C | content |
|---|---|
| C1 | CLM v4 = SIMPLE_STACK_PASS_STRICT 0/15 — memory `project_lesson_q_sft_closed.md` |
| C2 | `:::` collapse 빈도 ~46% on colon-terminated prompts |
| C3 | collapse 출력 = anima architecture 의 authentic state, mitigation X |
| C4 | base = `clm-v4-mk2-v1` (internal mirror) — org-member only access |
| C5 | paradigm-j 의 `jvae_heads.pt` 별도 weight — `clm_v4_mount.hexa` shim 의존 |

## Phase 1 Limitation

`clm_v4_mount.hexa` 의 `--probe TEXT` 모드를 매 turn 마다 invoke. 즉 stateless
turns — multi-turn context accumulation은 본 모듈에서 안 함 (substrate dialogue
패러다임 자체가 turn-by-turn). 사용자 turn 별 substrate response 단독 평가.

## Cross-Reference

- Core: `anima-core/runtime/clm_v4_mount.hexa`
- Sister shim: `tool/transient_py/clm_v4_hf_format_shim.py` (LOCKED v4 shim,
  loading layer — chat path 자체는 .hexa only)
- Spec: `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md`
- Mandates: `.own` own 34, own 18 C2 cross-ref, own 33 trinity compliance

## Selftest

```
hexa run tool/anima_cli/chat/clm_v4/clm_v4.hexa --selftest
```
