# Design — `stdlib/hf_hub.hexa` (Phase 1 PR draft, BG-α³, 2026-05-04)

> Phase 1 of the hexa-lang ML primitives upstream PR sequence. Closes the **HF Hub I/O MISSING** gap identified in `state/hexa_lang_gap_audit_2026_05_04/audit.md` §3 row 1 (priority P1, audit-estimated ~800 LoC). Lands as **`/Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa` (767 LoC)** — within the audit budget.

## 1. Goal

Provide pure-hexa primitives for HuggingFace Hub I/O so every model + dataset access path can land in hexa per:

- **raw#9 hexa-canonical-mandate** (no `.py` shims on Mac).
- **anima HF-only policy 2026-05-04** (memory `feedback_anima_models_datasets_hf_only.md`) — anima own models + datasets MUST flow through HF Hub, never GitHub. HF Hub I/O is therefore on the critical path of every artifact mutation.
- **mk2 hexa-only enforce-able target** at Phase 3 completion (per gap audit §10 roadmap proposal).

This is the **smallest, biggest-unlock first PR**: ~800 LoC enables "load any HF model in pure hexa" once paired with BG-β³ ieee754 + BG-γ³ sentencepiece.

## 2. API surface

| Function | Inputs | Returns | Purpose |
|---|---|---|---|
| `hf_whoami(token)` | string token (or "" → env) | `{ok, status, user}` | Verify token validity before bulk ops |
| `hf_repo_info(repo, revision, token)` | repo id, rev, token | `{ok, status, info}` | Get sha + siblings metadata |
| `hf_repo_tree(repo, revision, recursive, token)` | repo id, rev, bool, token | `{ok, status, files: []}` | Enumerate files for revision pin |
| `hf_download_file(repo, rev, path, out_local, token)` | 5 args | `{ok, status, sha256, bytes_written, local_path}` | Single-file download w/ verify |
| `hf_resolve_lfs(repo, rev, path, token)` | 4 args | `{ok, status, x_linked_etag, etag, content_length, url}` | HEAD probe → expected sha256 + size |
| `hf_upload_file(repo, rev, local, target, token, msg)` | 6 args | `{ok, status, commit_hash, target_path}` | Push local file via PUT |
| `hf_download_revision_pin(repo, rev, out_dir, token)` | 4 args | `{ok, status, files: [...], failures: [...]}` | Recursive sha256-verified download |
| `hf_redact_token(s)` | string | string | Defense vs leak in caller log lines |

All functions return a hexa map with `ok: bool` + `status: int` so callers chain via `if r["ok"] { ... }`. No exceptions. Error codes carried in `r["error"]` as a short slug ("http_404", "sha256_mismatch", "no_token", etc.).

## 3. HF Hub API mapping

| HF REST endpoint | hexa primitive | Method |
|---|---|---|
| `GET /api/whoami-v2` | `hf_whoami` | GET |
| `GET /api/models/<repo>/revision/<rev>` | `hf_repo_info` (models) | GET |
| `GET /api/datasets/<repo>/revision/<rev>` | `hf_repo_info` (datasets, prefix-detected) | GET |
| `GET /api/models/<repo>/tree/<rev>?recursive=true` | `hf_repo_tree` | GET |
| `HEAD /<repo>/resolve/<rev>/<path>` | `hf_resolve_lfs` | HEAD (curl `-I`) |
| `GET /<repo>/resolve/<rev>/<path>` | `hf_download_file` (curl `-o`) | GET, follow `-L` |
| `PUT /api/<kind>/<repo>/upload/<rev>/<target>` | `hf_upload_file` | PUT, `--data-binary @-` |

`hf_repo_kind()` heuristic: repo IDs prefixed with `datasets/` route to `/api/datasets/...`; everything else → `/api/models/...`. HF Spaces NOT supported v0.1 (out-of-scope for ML loading).

URL encoding: `_hf_url_encode_path` percent-encodes only the conflict-prone chars (`space`, `?`, `#`, `&`). HF repo IDs are restricted to `[a-zA-Z0-9._/-]` so the encoder is intentionally minimal — preserving `/` for org/name boundaries.

## 4. LFS handling

Per anima memory `reference_hf_gotchas.md`:

- **Non-LFS file**: `HEAD` returns 200 directly. Headers include `Content-Length` (real size) + `ETag` (md5 of file).
- **LFS file**: `HEAD` returns 302 → S3 redirect. After `curl -L`, final-hop headers include `X-Linked-Etag` (sha256 hash) + `X-Linked-Size` (real size). The `ETag` header on the LFS pointer is md5 of the *pointer file* (~200 bytes) and is NOT useful for blob verification.

`_hf_parse_headers` keeps **only the last hop** of a multi-block curl `-I -L` dump (search for last `HTTP/` line, parse following key:val pairs). All keys lowercased via `_hf_ascii_lower` for case-insensitive lookup per RFC 7230 §3.2.

`hf_download_file` uses `hf_resolve_lfs` first to fetch the expected sha256, then `curl -L` to download, then `shasum -a 256` to verify against `x_linked_etag` (stripping the `sha256:` prefix). Mismatch → `error="sha256_mismatch"`. Non-LFS files (no `x_linked_etag`) are size-checked against `content_length` only.

## 5. Auth flow

Token resolution order:
1. Caller-provided `token` arg, if non-empty.
2. `$HF_TOKEN` env var (per `huggingface_hub` Python convention).
3. Empty → anonymous (public read only; whoami / upload return `error="no_token"`).

Token is **always** injected via `Authorization: Bearer <tok>` header — never in the URL query string, body, or any field that could be logged by an HTTP intermediary or accidentally echoed by `set -x`.

`hf_redact_token(s)` is provided for callers that may print curl command echoes. Behavior: substring-replaces `$HF_TOKEN` (resolved from env, ≥8 chars) with the literal `<HF_TOKEN>` placeholder. Pure string transform, no I/O. Truncated/partial leaks are NOT scrubbed (those are bugs to fix at the source).

Defense vs `leak_guard` hook: callers wrapping any token-bearing log line MUST call `hf_redact_token` first. Module-internal `exec()` invocations route through `http_get_with_headers_status` (stdlib/http) which builds `-H 'Authorization: Bearer <tok>'` as a single shell-escaped flag — token never appears as a command-line argument visible in `ps`.

## 6. Error semantics

Per stdlib convention:
- Empty input args → `error: "empty_arg"` / `"empty_repo"` / `"empty_repo_or_path"`.
- HTTP non-2xx → `error: "http_<code>"`, `status: <code>`.
- Network failure (curl exits non-zero) → `status: 0`, `ok: false`.
- sha256 mismatch → `error: "sha256_mismatch"`.
- File size mismatch → `error: "size_mismatch"`.
- Missing local file (upload) → `error: "local_path_missing"`.
- Missing token (whoami/upload) → `error: "no_token"`.

`status: 0` is a special signal indicating curl-level failure (DNS, TLS, timeout, missing curl binary). Caller can retry or fall back.

## 7. Falsifier set

See `falsifier_set.md`. Five falsifiers F-HF-HUB-1..5 with selftest evidence captured in `selftest_log.txt`.

| ID | Type | Status |
|---|---|---|
| F-HF-HUB-1 (whoami valid+invalid) | LIVE network | DEFERRED — gated on `$ANIMA_HF_HUB_LIVE=1` + `$HF_TOKEN` |
| F-HF-HUB-2 (repo_tree contains config.json) | LIVE network | DEFERRED |
| F-HF-HUB-3 (download_file round-trip) | LIVE network | DEFERRED |
| F-HF-HUB-4 (resolve_lfs x-linked-etag) | LIVE network | DEFERRED |
| F-HF-HUB-5 (token redaction) | OFFLINE | PASS (selftest_log.txt Run 2) |

Plus 4 supporting offline checks (header parse content-length + etag-strip + repo-kind models/datasets) all PASS.

## 8. Cost

- Mac dev only. **$0** (no GPU, no RunPod, no paid API).
- Wallclock ~30 min implementation + 10 min selftest authoring.
- Destructive: 0 (additive new file, zero modifications to existing stdlib).
- Live falsifiers (F-HF-HUB-1..4) require ~$0 network bandwidth (config.json ~500 bytes + whoami JSON ~200 bytes + tree JSON ~5KB + LFS HEAD ~0 bytes body).

## 9. Honest C3 (≥4 per raw#10)

1. **HF Hub rate limits not enforced in this module.** Anonymous: ~100 req/min; authed: ~1000 req/min. `hf_download_revision_pin` of a multi-file repo can burst >100 requests in seconds and trip a 429. v0.1 does NOT throttle / retry / honor `Retry-After`. Phase 1.5 mitigation: caller adds `sleep_ms_between` arg analogous to `qrng_anu_chunked`. **Production risk: medium** — bulk pin of Llama-3.2-3B = ~10 files = under the limit, but a 70B repo (~30 shards) would 429.

2. **Token rotation NOT supported.** A token revoked mid-run will fail every subsequent call with `http_401` until process restart. Real HF Python SDK has token-refresh via OAuth2 device flow; v0.1 hexa version is static-token-only. **Production risk: low** for our use case (long-lived `HF_TOKEN` env tokens), but worth flagging as an honest C3.

3. **LFS chunked / resumable download NOT supported.** Single curl invocation per file. A 5GB safetensors shard at 1MB/s = 80 minutes — must complete in one TCP connection or fail. v0.1 has no `--continue-at` resume, no range-request multi-part. Phase 2 mitigation: add `range: [start, end]` arg. **Production risk: high** for slow/flaky networks; **low** on Mac dev with good connectivity.

4. **TLS verify status is system-dependent and silent.** curl uses SecureTransport (macOS) / OpenSSL (Linux) / Schannel (Windows). Self-signed corp-MITM certs fail with `status: 0` and no error message that distinguishes "TLS untrusted" from "DNS failure" or "timeout". Caller cannot today programmatically detect MITM scenarios. v0.1 does NOT expose `--insecure` (intentional — refuse to silently bypass cert validation), but also does NOT pass through stderr to surface the underlying curl error. **Production risk: low on Mac dev**, **medium on enterprise networks** with corporate proxies.

5. **stdlib/http does NOT today expose a HEAD primitive** — `_hf_curl_head` builds the curl command directly inside this module (matching the `stdlib/http` internals). This is a Phase 1 prereq leak: future stdlib/http.hexa enhancements that change the curl flag emission MUST be mirrored here. Mitigation considered + rejected: requesting a new public `http_head_with_headers` primitive in stdlib/http would block this PR on a separate review cycle. Pragmatic: keep the duplication for v0.1, file a follow-up issue for stdlib/http to upstream HEAD support.

6. **Multipart upload not supported** — `hf_upload_file` uses simple PUT-content. The Hub accepts up to ~5GB in this path; larger uploads must use the multi-stage commit API (init → upload-parts → finalize). Anima current artifact sizes (~3B parameter LoRA adapters ~500MB, full models <16GB) mostly fit, but a future 70B-class model upload would fail. Phase 2 mitigation.

## 10. Sequencing

- **Phase 1** (this PR): hf_hub.hexa (BG-α³) + ieee754.hexa (BG-β³) + sentencepiece.hexa (BG-γ³) — landing in parallel as separate files.
- **Phase 1 trio combined unlocks**: pure-hexa download + tokenize + parse-safetensors-numeric of any HF model. The `Llama-3.2-3B/main/config.json` falsifier is reachable.
- **Phase 2 dependencies**: bf16 tensor + production matmul/softmax/layernorm + Llama-3 block stack — not in scope for this PR.

## 11. Artifacts

```
/Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa                                    (NEW, 767 LoC, source)
/Users/ghost/core/anima/state/hexa_lang_phase1_hf_hub_2026_05_04/design.md        (this doc)
/Users/ghost/core/anima/state/hexa_lang_phase1_hf_hub_2026_05_04/falsifier_set.md (5 F-HF-HUB-* falsifiers)
/Users/ghost/core/anima/state/hexa_lang_phase1_hf_hub_2026_05_04/selftest_log.txt (selftest evidence)
```

References:
- Audit: `/Users/ghost/core/anima/state/hexa_lang_gap_audit_2026_05_04/audit.md` §3 row 1 + §4.1.
- Sister BGs: `stdlib/ieee754.hexa` (BG-β³), `stdlib/sentencepiece.hexa` (BG-γ³).
- Memory anchors: `reference_hf_gotchas.md`, `feedback_anima_models_datasets_hf_only.md`, `feedback_py_to_hexa_only.md`.
- Builds on: `stdlib/http.hexa`, `stdlib/json.hexa`, `stdlib/json_object.hexa`.
