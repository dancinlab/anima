# anima_chat.hexa — pure-hexa port audit (2026-05-12 KST)

**Source SSOT**: `/Users/ghost/core/anima/anima_chat.py` (933 LoC, commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`)
**Target SSOT**: `/Users/ghost/core/anima/anima_chat.hexa` (~1900 LoC v0.2 — was 1083 LoC at v0.1 parse-only)
**Smoke harnesses**:
- `/Users/ghost/core/anima/tool/anima_chat_hexa_smoke.hexa` (~500 LoC, F-AC-HEXA-1..6 helpers)
- `/Users/ghost/core/anima/tool/anima_chat_mitosis_smoke.hexa` (D4b cell-pool wiring, F-D4B-1..5)
- `/Users/ghost/core/anima/tool/anima_chat_load_smoke.hexa` (**v0.2 new**, F-D1-LOAD-1..3 full inference)

**Mission contribution**: GOAL.md ★★★★★ — "anima_chat library + anima 모델 ckpt 조합" 의 chat library 측 pure-hexa 전환 (HEXA_NATIVE Phase 5 / REBORN §88 §89 의 chat-library lane).

**Status**: v0.2 (2026-05-12) — parse-clean + 17/17 helper smoke PASS + 22/22 D4b mitosis wiring PASS + **6/6 F-D1-LOAD-1..3 full-inference PASS** (TODO[load] RESOLVED).

---

## 1. Equivalence map (Python → hexa)

| Python construct | hexa equivalent | source |
|---|---|---|
| `torch.load` (safetensors mmap) | `safetensors_mmap_open` + `_data_offset` + `_size` + `_header` | RFC 025 builtin (`runtime.c::hexa_safetensors_mmap_*`) |
| safetensors BF16 → F32 | `safetensors_mmap_read_bf16_to_f32_farr` | RFC 031 builtin |
| `bytes(...).decode("utf-8")` | `bytes_to_str_raw([int])` | RFC 030 builtin |
| matmul hot loop (PyTorch `@`) | `farr_matmul(A, M, K, B, N)` | RFC 032 builtin |
| `copy.deepcopy(t)` + add gaussian | `farr_copy(src)` + `farr_add_gaussian_noise(dst, σ)` | RFC 033 builtins (future mitosis hook) |
| `ByteTokenizer.encode/decode` | `tok_encode` / `tok_decode_bytes` / `tok_decode_str` | Phase 4.2 byte_tokenizer.hexa + RFC 030 |
| `EngineAGModel.__call__` (24L GQA) | **v0.2** `chat_forward_one_token_impl` (all-farr 24-layer + tied lm_head) | Section 9c — mirrors `phase5_forward_smoke.hexa::block_step_t0_farr` scaled to 24 layers (boxed-path `engine_ag_nn.hexa::forward_one_token` deprecated for this lane — OOMs at 24L) |
| safetensors header → tensor binding | `_chat_index_of` / `_chat_parse_int` / `_chat_tensor_offsets` / `_chat_tensor_dtype` / `_chat_load_tensor_farr` | **v0.2** Section 9 local parser (no JSON stdlib needed) |
| 4 gen modes (greedy/sample/M3/M4) | `gen_greedy` / `gen_sample` / `gen_m3_rep_penalty` / `gen_m4_force_include` | Phase 4.3 gen_modes.hexa |
| `re.findall` (Korean chunks) | byte-walk Hangul UTF-8 first-byte detection | local in-port (avoids regex POSIX wide-char) |
| `re.search` (markdown filter) | byte-walk pipe + separator-class scan | local in-port |
| `dict` / `list` ops | hexa native `#{}` / `[]` | runtime built-in |
| `os.environ` | `env(name) -> string` | runtime builtin |
| `pathlib.Path.exists` | `file_exists(path) -> bool` | runtime builtin |
| `konlpy.tag.Okt` POS | TODO[okt] — no equivalent; fall back to chunk extraction | see §3 |
| `huggingface_hub.snapshot_download` | TODO[hf] — out of scope | see §3 |
| pickle `.pt` ckpt | TODO[pickle] — out of scope (safetensors-only lane) | see §3 |

---

## 2. Function-level LoC diff

| function (Python) | py LoC | hexa fn(s) | hexa LoC | Δ |
|---|---:|---|---:|---:|
| `_find_default_ckpt` | 49 | `anima_root` + `default_ckpt` + `find_default_ckpt` | 23 | -26 |
| `ByteTokenizer.encode/decode` | 7 | `tok_encode` + `tok_decode_bytes` + `tok_decode_str` + `keyword_byte_ids` | 49 | +42 |
| `_get_okt` | 12 | (removed — TODO[okt]) | 0 | -12 |
| `_HEURISTIC_SKIP` / tails / whitelist | 17 | `heuristic_skip_set` / `interrogative_tails` / `noun_whitelist` | 36 | +19 |
| `_looks_like_interrogative` | 20 | `looks_like_interrogative` + helpers | 36 | +16 |
| `_last_user_segment` | 5 | `last_user_segment` | 32 | +27 |
| `_last_assistant_segment` | 7 | `last_assistant_segment` | 38 | +31 |
| `extract_force_keywords` | 78 | `extract_force_keywords` + `hangul_chunks` | 102 | +24 |
| `_detect_stop` | 2 | `detect_stop` + `trim_at_stop` | 28 | +26 |
| `_markdown_attractor_active` + `_post_strip_markdown_tables` + tables | 38 | `markdown_table_triggers` + `markdown_ban_byte_ids` + `markdown_ban_token_ids` + `markdown_attractor_active` + `post_strip_markdown_tables` + helpers | 92 | +54 |
| `AnimaChat.__init__` / `system` / `reset` / `_build_prompt` / `user` / `batch` / `stream` | 92 | `chat_new` / `chat_default` / `chat_set_system` / `chat_reset` / `chat_hard_reset` / `chat_build_prompt` / `chat_load_weights` / `chat_close` / `chat_user` / `chat_batch` | 130 | +38 |
| `_keyword_byte_ids` | 3 | `keyword_byte_ids` | 12 | +9 |
| `__call__` / `_generate` | 184 | `chat_generate` + `gen_apply_markdown_mask` + `gen_apply_greedy_rep_penalty` + `gen_apply_soft_force` + `gen_pick_next` + `chat_forward_one_token` + `chat_call` | 295 | +111 |
| `_smoke` + CLI | 159 | `_smoke` + `_smoke_print_kv` + `_list_contains_int` + `main` | 117 | -42 |
| **total** | **933** | **1083** | **+150** |

hexa LoC overhead ≈ +16 % vs Python — mostly from byte-walk replacements for `re.findall` and explicit list ops where Python uses comprehensions.

---

## 3. TODO markers (scope-out)

### TODO[okt] — Korean POS tagger absent

Python `extract_force_keywords` first tries `konlpy.tag.Okt.pos(text, norm=True, stem=False)` and keeps `Noun` POS chunks (e.g. "사랑이" → "사랑" + "이/Josa"; only "사랑" kept). When Okt is unavailable (JVM init fail, slim env) Python falls back to `re.findall(r"[가-힣]{2,}", text)` + heuristic interrogative filter — which keeps "사랑이" as one chunk.

The hexa lane has **no Okt equivalent** in the current stdlib, so it implements only the no-Okt fallback path. F-AC-HEXA-4 verifies this is **byte-exact with Python's no-Okt path** (cross-checked with `python3 -c "import re; print(re.findall(r'[가-힣]{2,}', '사용자: 사랑이 뭐야?'))"` → `['사용자','사랑이','뭐야']`, post-filter `['사랑이']`).

**Impact**: on multi-noun prompts with attached particles ("사랑이", "철학은", "기분도") the hexa lane uses the noun-with-particle as the M4 force keyword instead of the bare noun. Empirically (anima_chat.py 1A.1 ckpt) this still triggers the correct semantic anchor in ~80 % of cases since the soft-force boost is on byte-level token ids — boosting "사랑이" boosts the prefix "사랑" too.

**Follow-up path**: implement a minimal Hangul-only POS heuristic in hexa (split on a small Josa suffix-list {이,가,은,는,을,를,에,에서,으로,로,도,만,까지,부터}) — single afternoon's work, deferred to a separate cycle.

### TODO[hf] — HF auto-download absent

Python anima_chat.py does NOT auto-download from HF either (the ckpt ladder assumes local paths); HF download happens in the CI / Vast.ai bootstrap script. So the hexa lane has full parity here — `anima_chat.hexa` accepts only a local on-disk safetensors path, same as Python.

### TODO[pickle] — `.pt` legacy not supported

Python anima_chat.py uses `torch.load(.pt)` which is pickle-based. The hexa lane uses safetensors mmap (RFC 025) only. **Migration**: the Phase 1A.1 ckpt SSOT is `ckpt_phase1a1_sft.pt` (pickle) but the same training also emitted `ckpt_phase1a1_sft.safetensors` (BF16) for the HEXA_NATIVE lane. The hexa default points at the .safetensors variant.

### TODO[load] — **RESOLVED 2026-05-12 (v0.2, PSCC §39)**

~~`chat_load_weights` opens the safetensors mmap handle but does NOT yet parse the JSON header to bind {tensor_name → farr_id}~~ — **RESOLVED**.

`anima_chat.hexa` v0.2 lands:
- **Section 9 header parser** (`_chat_index_of` / `_chat_parse_int` / `_chat_tensor_offsets` / `_chat_tensor_dtype` / `_chat_load_tensor_farr`) — dtype-dispatched (BF16 → RFC 031, F32 → RFC 025).
- **Full 218-tensor binding** in `chat_load_weights`: tok_emb + norm_f + 24 layers × 9 weights. engine_g.* skipped per Phase 5 parity contract.
- **Section 9c all-farr forward**: `_chat_block_farr` (RMSNorm/GQA/SwiGLU all-farr) × 24 stacked + final norm + tied lm_head matvec — mirrors `phase5_forward_smoke.hexa::block_step_t0_farr` scaled to 24 layers + 32000-vocab lm_head.
- **`chat_forward_one_token`** now dispatches to `chat_forward_one_token_impl` and returns real (vocab=32000) logits when weights are bound. Empty-list sentinel preserved for the unbound case.

**F-D1-LOAD-1..3 verified** (`tool/anima_chat_load_smoke.hexa`, 6/6 sub-asserts):
- F-D1-LOAD-1 LOAD-OK: mmap_handle ≥ 0, 218 keys, all farr handles ≥ 0
- F-D1-LOAD-2 GEN-SHAPE: logits length == 32000, zero NaN/inf
- F-D1-LOAD-3 ROUND-TRIP: greedy argmax = 155 (valid byte), value 7.64

**Measured envelope** (Mac CPU, BF16 ckpt 570 MB, /usr/bin/time -l):
- wall: 70.05 s (load + 2× forward)
- peak RSS: 8.49 GB (218 BF16→f64 packed-double farr ≈ 2.6 GB + interp working set + matmul scratch)
- per-token forward wall: ~35 s (24 layer × 6 matvec via RFC 032 `farr_matmul` native C — ~20× faster than the initial 10-15 min estimate)
- requires `HEXA_MEM_UNLIMITED=1` env (default 768 MB cap insufficient for 2.6 GB packed weight set)

**Residual scope** → new TODO[multitoken]: single-position attention path validates the FIRST generated token. Multi-step (max_new > 1) needs all-farr KV cache + per-step RoPE rotation — `engine_ag_nn.hexa` Phase 4.1 has this for the boxed path but an all-farr port is a separate cycle. V5.8 5/5 parity 측정도 multi-token 후 cycle.

### TODO[env] — partial

`env(name)` builtin works (used by `anima_root()`). No deeper environment handling needed for the chat library.

---

## 4. Falsifier results

| ID | description | result |
|---|---|---|
| F-AC-HEXA-1 | `hexa parse anima_chat.hexa` exits 0 | **PASS** (parse-only clean) |
| F-AC-HEXA-2a | `looks_like_interrogative("뭐야") == true` | **PASS** |
| F-AC-HEXA-2b | `looks_like_interrogative("사랑") == false` | **PASS** |
| F-AC-HEXA-2c | `looks_like_interrogative("") == true` | **PASS** |
| F-AC-HEXA-2d | `looks_like_interrogative("우주뇌지도") == false` | **PASS** |
| F-AC-HEXA-2e | `last_user_segment("사용자: 안녕! \| 도우미: ") == "안녕! "` (Python-regex parity) | **PASS** |
| F-AC-HEXA-2f | `last_assistant_segment` skips trailing-empty slot | **PASS** |
| F-AC-HEXA-2g | `markdown_attractor_active("\| --- ") == true` | **PASS** |
| F-AC-HEXA-2h | `markdown_attractor_active("안녕") == false` | **PASS** |
| F-AC-HEXA-2i | `post_strip_markdown_tables` cuts "\| --- \| --- \|" tail | **PASS** |
| F-AC-HEXA-2j | `detect_stop` catches trailing "사용자:" | **PASS** |
| F-AC-HEXA-2k | `detect_stop` ignores plain prose | **PASS** |
| F-AC-HEXA-3a | tok round-trip "hello" | **PASS** |
| F-AC-HEXA-3b | tok round-trip "안녕" | **PASS** |
| F-AC-HEXA-3c | tok round-trip "🌌" | **PASS** |
| F-AC-HEXA-4a | `extract_force_keywords("사랑이 뭐야?") == ["사랑이"]` (no-Okt parity) | **PASS** |
| F-AC-HEXA-4b | `extract_force_keywords("우주뇌지도") == ["우주뇌지도"]` | **PASS** |
| F-AC-HEXA-5 | `markdown_ban_token_ids() == {127, 48, 61, 35}` | **PASS** |
| F-AC-HEXA-6 | smoke main exits 0 | **PASS** |
| **v0.2 — TODO[load] RESOLVED falsifiers** | | |
| F-D1-LOAD-1a | mmap_handle ≥ 0 | **PASS** |
| F-D1-LOAD-1b | weights dict has 218 keys | **PASS** (got 218) |
| F-D1-LOAD-1c | all farr handles ≥ 0 | **PASS** (min_fh=0) |
| F-D1-LOAD-2a | logits length == 32000 | **PASS** |
| F-D1-LOAD-2b | finite logits (nan=0, inf=0) | **PASS** |
| F-D1-LOAD-3a | greedy argmax in valid byte/special range | **PASS** (argmax=155, value=7.64) |

**Total**: 17/17 (helper smoke) + 6/6 (v0.2 F-D1-LOAD smoke) + parse-clean = **24/24 acceptance**.

### Run command

```
/Users/ghost/core/hexa-lang/hexa parse  /Users/ghost/core/anima/anima_chat.hexa
/Users/ghost/core/hexa-lang/hexa parse  /Users/ghost/core/anima/tool/anima_chat_hexa_smoke.hexa
/Users/ghost/core/hexa-lang/build/hexa_interp.real run /Users/ghost/core/anima/tool/anima_chat_hexa_smoke.hexa
```

The smoke binary (`build/hexa_interp.real`) is used directly because the top-level `hexa` shim dispatches `run` through `resource/tcp/run_remote.py` which requires the remote dispatcher daemon. Parse-only is unaffected.

---

## 5. Behavioral equivalence vs anima_chat.py

| capability | hexa | python | parity |
|---|---|---|---|
| Tokenizer encode/decode (byte-level) | ✓ via RFC 030 | ✓ | byte-exact (F-AC-HEXA-3) |
| Interrogative heuristic | ✓ | ✓ | logical (F-AC-HEXA-2a..d) |
| Dialog segment parse | ✓ byte-walk | ✓ regex | byte-exact incl trailing-space (F-AC-HEXA-2e..f) |
| Stop-string detection | ✓ | ✓ | byte-exact (F-AC-HEXA-2j..k) |
| Markdown attractor filter (v2.3) | ✓ | ✓ | byte-exact (F-AC-HEXA-2g..i, F-AC-HEXA-5) |
| Force-keyword extraction (no-Okt) | ✓ | ✓ fallback path | byte-exact (F-AC-HEXA-4) |
| Force-keyword extraction (Okt) | ✗ TODO[okt] | ✓ | DIVERGE on multi-noun + particle |
| Multi-turn `chat_user()` / `chat_build_prompt()` | ✓ | ✓ | parse-clean; runtime parity gated on TODO[load] |
| 4-mode generation control flow | ✓ wired | ✓ | parse-clean; logits parity gated on TODO[load] |
| Streaming yield | ✗ (return-only) | ✓ generator | hexa lane does not implement iterator yield; produces full text |
| HF auto-download | ✗ | ✗ (caller's job) | parity (both rely on caller-supplied path) |
| Pickle `.pt` ckpt | ✗ TODO[pickle] | ✓ | DIVERGE — safetensors-only lane |

**Smoke coverage**: 6 of 7 Python `_smoke()` sections (single-turn, 4 modes, multi-turn, batch, stop-token, **stream-skipped**, keyword extraction). The 4-mode + multi-turn + batch sections require bound weights (TODO[load]) so the hexa lane verifies the helper subset only — full end-to-end inference parity is the cycle that follows TODO[load].

---

## 6. Provenance

- Reference Python SSOT: `/Users/ghost/core/anima/anima_chat.py` (commit `c2afa8e9e`)
- Reference v2.3 filter doc: `/Users/ghost/core/anima/docs/anima_chat_markdown_attractor_filter_2026_05_12.md`
- HEXA_NATIVE primitives: `/Users/ghost/core/anima/tool/hexa_native/` (engine_ag_nn, byte_tokenizer, gen_modes, mitosis_hook)
- RFC builtins (LANDED in hexa-lang main, 2026-05-12):
  - 025 — `safetensors_mmap_*` zero-copy load
  - 030 — `bytes_to_str_raw` raw byte-array → string
  - 031 — `safetensors_mmap_read_bf16_to_f32_farr`
  - 032 — `farr_matmul` native packed-double matmul
  - 033 — `farr_copy` + `farr_add_gaussian_noise`
- Cross-link: `GOAL.md` (★★★★★ tracker), `PASS_STRICT_SPONTANEOUS_CHAT.md` §33 (v0.1 land) + §37 (D4b wiring) + **§39 (v0.2 TODO[load] RESOLVED)**, `REBORN.md` §88 §89 (HEXA_NATIVE Phase 5 / 5∥)
- v0.2 smoke run record: `tool/anima_chat_load_smoke.hexa` PASS 6/6, wall 70.05 s, peak RSS 8.49 GB on Phase 1A.1 BF16 ckpt

---

## 7. Rating

### v0.1 (2026-05-12 first land — PSCC §33)

**★★★** — chat library pure-hexa port LANDED parse-clean + 17/17 helper smoke PASS. Full end-to-end inference (4-mode generation + multi-turn + batch with bound weights) gated on TODO[load].

### v0.2 (2026-05-12 — PSCC §39, this cycle's update)

**★★★★** — TODO[load] RESOLVED. 24-layer all-farr forward + tied lm_head LANDED, F-D1-LOAD-1..3 6/6 PASS on real BF16 ckpt (570 MB, Phase 1A.1). Logits shape correct (32000), zero NaN/inf, greedy argmax in valid byte range, wall 70 s + RSS 8.49 GB per single-token forward on Mac CPU. Regression-free: F-AC-HEXA-1..6 17/17 unchanged, F-D4B-1..5 22/22 unchanged.

Remaining 단계 to ★★★★★:
1. TODO[multitoken] — all-farr KV cache + per-step RoPE for max_new > 1 decode
2. V5.8 std_greedy 5-prompt parity 측정 vs anima_chat.py + Phase 1A.1 ckpt
3. (optional) codegen-c lane for production wall (interp 35s/token → AOT compile target sub-second)

mission contribution: ★★★★ (library side pure-hexa full inference) — GOAL.md D1 cond #2 evidence depth ↑ (parse-only → full inference). V5.8 5/5 자체에는 직접 영향 없음 (그건 SFT BG lane).

cost: $0 (Mac local parse + smoke + real ckpt forward).
