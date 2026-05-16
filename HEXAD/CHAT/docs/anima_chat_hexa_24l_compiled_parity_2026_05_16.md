# anima_chat 24-layer real-ckpt V5.8 parity — COMPILED-native (T3, 2026-05-16)

**Status**: LANDED — **21/21 falsifiers PASS, hexa-COMPILED-native, byte-equal to Python SSOT**
**Scope**: T3 — reproduce the prior interp-only 21/21 (PSCC §43, 2026-05-12) on the **compiled-native** path (`hexa build` native binary, NOT `hexa run` interpreter), proving compiled ≡ interp on the real 24-layer 570 MB ckpt.
**Evidence class**: parity-PASS **empirical** — NOT 🔵 closed-form (g3). Strong empirical anchor, no formal closure.
**Cost**: $0 (ubu, owned host). Wall: 1.25 s + 3.86 s compiled (vs interp 37.65 s + 94.67 s).
**Where run**: ubu (`ssh ubu`, Linux x86_64).

---

## 1. What was proven

The 24-layer real-ckpt forward + KV-cache + per-step RoPE byte-parity (21/21: F-D1-V58PARITY 6/6 + F-D1-V58MULTI 15/15) was previously verified **interpreter-only** (`hexa run`, PSCC §43). T3 reproduces the **identical 21/21** via **compiled-native binaries** (`hexa build` → clang → ELF), demonstrating the compiled codegen path is byte-equal to the interpreter path on the real ckpt.

| Lane | Probe | Result | Wall | Peak RSS |
|---|---|---|---|---|
| **hexa-COMPILED-native** | F-D1-V58PARITY (BOS single fwd) | **6/6 PASS** | 1.25 s | 3.08 GB |
| **hexa-COMPILED-native** | F-D1-V58MULTI (5-step KV chain) | **15/15 PASS** | 3.86 s | 3.08 GB |
| (prior) hexa-interp | same two | 21/21 PASS | 37.65+94.67 s | 7.52+10.99 GB |

**Per-step hexa logit values from the compiled binary are IDENTICAL to the interp-only doc §4.2** (5.92355 / 6.63204 / 9.60577 / 11.4133 / 13.1187) → the compiled path is byte-for-byte equal to interp on this real ckpt, not merely argmax-equal.

## 2. Toolchain — isolated bootstrap (PR#51 codegen)

Shared `~/.hx/bin/hexa_real` on ubu was built 2026-05-15 (pre-PR#51); origin/main `6f5f2a6c` has the `_gen2_nested_index_assign_stmt` codegen in `self/codegen_c2.hexa` (chat_lib Section 9 needs it) but the checked-in bootstrap `self/native/hexa_cc.c` is **stale** (0 occurrences vs codegen_c2.hexa's 2). So an isolated hexa.real was bootstrapped:

```
ubu shared hexa_real (stage0 interp)
  -> hexa cc            (clang hexa_cc.c -> hexa_v2)
  -> hexa cc --regen    (re-transpile codegen_c2.hexa WITH PR#51 -> hexa_cc.c.new, 2 hits)
  -> promote .new, rebuild hexa_v2
  -> hexa_v2 self/main.hexa -> build/stage1/main.c -> clang -> isolated hexa.real
  -> fixed point: re-transpile main.hexa, round1==round2 byte-equal ✓
```

| Artifact | sha256 |
|---|---|
| hexa-lang origin/main | `6f5f2a6c5dd409b72b651c94b3b9bf4f20dcf38c` |
| isolated `hexa.real` | `aecaf1f5191c12b82eaf1f6e18ce771327542a1c753d457f5977af9eeef4150a` |
| isolated `hexa_v2` | `b4cc574d8cd4cb304e081229221bfb3e7204df87cb7f844b9861e779e9b6b95b` |
| regenerated `hexa_cc.c` (PR#51, 2 hits) | `450451fde8221c1055fbe7d532d0b62ec657101df00d9bc7a957e77a93c39840` |

clang: Ubuntu clang 18.1.3. Worktree: `ubu:/tmp/hexa-t3-boot` (isolated).

**Bootstrap unblock patch (isolated only)**: origin/main `6f5f2a6c`'s `self/runtime.c` includes `<execinfo.h>` only under `#if defined(__APPLE__)`; clang 18.1.3 errors on the implicit `backtrace()` decl on Linux. Added `#elif defined(__linux__) #include <execinfo.h>` to the **isolated** `/tmp/hexa-t3-boot/self/runtime.c` only. The backtrace path is `getenv("HEXA_OOB_TRACE")`-gated → behavior-neutral. **Shared `~/core/hexa-lang` untouched.** This is a genuine hexa-lang origin/main portability gap on modern clang (candidate upstream PR).

## 3. Ckpt + SSOT

The real 24L ckpt lives **on ubu only**: `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.safetensors` — 597,550,688 bytes, sha256 `838a0a2e…`. Absent on the Mac worktree (only `.safetensors` exists anywhere; the source `.pt` was not retained — see ckpt `.meta.json` `source_pt`).

**Ckpt sha vs doc**: the 2026-05-12 doc provenance line says the `.safetensors` is `sha256 e5f7555…`; the actual `.safetensors` on ubu is `838a0a2e…`. The `e5f7555…` abbrev most plausibly referenced the source `.pt`. **Weight equivalence proven empirically**: the Python SSOT loaded from THIS `.safetensors` reproduces the documented 2026-05-12 SSOT **exactly** (BOS=143, top5=[143,133,138,146,173], chain=[143,131,240,152,159]).

**SSOT method change (tighter, not weaker)**: the original SSOT used `anima_chat.py AnimaChat(ckpt=.pt)`. The `.pt` is gone, so the T3 SSOT (`state/anima_d1_v58_compiled_parity_2026_05_16/python_safetensors_ssot_probe.py`) loads the **same weights** from the `.safetensors` into the **same** `EngineAGModel` arch (`load_state_dict strict=False`: missing=1=`lm_head.weight` tied to `tok_emb`, unexpected=0 — clean). Both the Python SSOT and the hexa-compiled lane now consume the **identical 597,550,688-byte `.safetensors`** — a tighter parity contract than `.pt`-python vs `.safetensors`-hexa.

## 4. Byte-parity table (hexa-COMPILED vs Python SSOT)

BOS single forward: hexa-compiled argmax = **143** == python SSOT **143** (byte-equal); 143 ∈ python top5 {143,133,138,146,173}.

| step | t | token_in | hexa-compiled | python SSOT | byte-equal | kv cur_len |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 143 | 143 | ✓ | 1 |
| 1 | 1 | 143 | 131 | 131 | ✓ | 2 |
| 2 | 2 | 131 | 240 | 240 | ✓ | 3 |
| 3 | 3 | 240 | 152 | 152 | ✓ | 4 |
| 4 | 4 | 152 | 159 | 159 | ✓ | 5 |

hexa-compiled chain = python SSOT chain = **[143, 131, 240, 152, 159]**. KV-cache cur_len monotone 0→5 (5/5). **21/21 PASS.**

## 5. Honest C3

1. Parity is STRONG **empirical** evidence, NOT 🔵 closed-form (g3). No sympy/PyPhi/Kuramoto formal closure.
2. Ckpt sha discrepancy vs doc — resolved by empirical weight-equivalence (SSOT reproduces documented values exactly); `e5f7555…` most plausibly the gone `.pt`.
3. SSOT lane changed (`.pt`→`.safetensors`) — arch + weights identical, both lanes share the exact same bytes; tighter, not weaker.
4. Scope = single BOS (t=0) + 5-step greedy chain (t=0..4) only; full V5.8 5-cell × 4-mode NOT run (same scope cap as the prior interp cycle).
5. Single ckpt (Phase 1A.1). Other ckpts not parity-verified on the compiled path.
6. Linux x86_64 (ubu) only; Mac/ARM compiled byte parity not verified (ckpt + bootstrap both live on ubu).
7. Isolated `runtime.c` bootstrap patch was required (origin/main `6f5f2a6c` does not clean-compile under clang 18.1.3); behavior-neutral, isolated-only, genuine upstream gap.
8. Per-step compiled-vs-python float drift up to ~13% at argmax pos (BF16→f32 + boxed matmul vs GEMM); argmax byte-invariant every step; same drift profile as interp-only doc §4.3.

## 6. Provenance

- `state/anima_d1_v58_compiled_parity_2026_05_16/result.json` — self-contained (toolchain/ckpt sha, per-probe pass, byte-parity table, RSS/wall, C3)
- `state/anima_d1_v58_compiled_parity_2026_05_16/python_ssot.json` — Python SSOT capture (this ckpt)
- `state/anima_d1_v58_compiled_parity_2026_05_16/python_safetensors_ssot_probe.py` — safetensors→EngineAGModel SSOT runner
- probes: `state/anima_d1_v58_parity_2026_05_12/v58_hexa_parity.hexa` + `v58_hexa_multi_parity.hexa` (unchanged; compiled, not interp'd)
- prior interp-only: `HEXAD/CHAT/docs/anima_chat_hexa_24l_v58_parity_2026_05_12.md` (PSCC §43, 21/21 interp) — still stands; T3 extends it to the compiled path.
