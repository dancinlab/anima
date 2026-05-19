# hexa-lang Phase 1 follow-up fixes (2026-05-04)

**Cycle**: `hexa_lang_phase1_followup_fixes_2026_05_04`
**Owner**: BG-Φ²
**Files modified**:
- `/Users/ghost/core/hexa-lang/stdlib/http.hexa` (LoC 159 → 297, Δ +138)
- `/Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa` (LoC 821 → 1090, Δ +269)

**Cross-link**:
- BG-α³ baseline: `state/hexa_lang_phase1_hf_hub_2026_05_04/design.md` + `falsifier_set.md`
- Honest C3 source — `hf_hub.hexa` v0.1.0 module header §"Caveats" lines 57–74
  flagged: rate-limit not throttled, chunked LFS unsupported, HEAD primitive leak.
  This cycle closes all three.

---

## FIX-1 — `http_head` primitive in `stdlib/http`

### Why
`stdlib/hf_hub::_hf_curl_head` (BG-α³) shipped an inline curl wrapper because
`stdlib/http` exposed only GET. That is a Phase-1 prereq leak — the abstraction
belongs in `stdlib/http` so any caller (hf_hub, qmirror, GCS, REST clients) can
issue HEAD without re-deriving curl boilerplate or its quote/escape rules.

### API
```hexa
pub fn http_head(url: string, headers, timeout_sec: int) -> map
// returns {status: int, headers: map<lowercase>, body: "", ok: bool}
```
- `body` is always `""` (RFC 7230 §4.3.2 — HEAD has no entity body); kept as a
  field for shape-parity with `http_get_with_headers_status`.
- `headers` lowercased per RFC 7230 §3.2 case-insensitive convention via the
  newly-added `_http_ascii_lower` (private).
- Multi-block redirect dumps (curl `-I -L` emits one block per hop) collapse to
  the LAST block — final-resolved resource metadata is authoritative.

### Implementation sketch
- Reuses the existing `_http_shell_escape` and `_http_last_index_of` helpers.
- New private helpers: `_http_ascii_lower`, `_http_parse_head_block`.
- curl flags: `-sSIL --max-time T -H ... -w '\n%{http_code}'`.

### Honest C3 (FIX-1)
1. **HEAD ≠ GET headers on some upstreams**: S3 / CDN edges may strip
   Content-Length on HEAD (chunked streaming). Callers needing GET-equivalent
   headers must not rely on HEAD as a substitute.
2. **405 from buggy servers**: some endpoints respond 405 Method Not Allowed
   to HEAD. Status returned as-is for caller policy.
3. **ASCII-only header lowercasing**: HTTP token chars are ASCII per RFC; this
   is sufficient. Unicode header names (non-conformant) are passed through.
4. **No quote stripping on values**: callers (e.g. hf_hub LFS resolver) handle
   ETag quote conventions in their own layer.

### `_hf_curl_head` refactor
Now delegates to `http_head` via `_http_with_backoff_head` (FIX-2). Original
inline curl removed; downstream callers (`hf_resolve_lfs`) untouched.

---

## FIX-2 — Rate-limit retry with exponential backoff

### Why
HF Hub allows ~100 req/min unauth and ~1000 req/min auth. `hf_download_revision_pin`
of a 200-shard model trips 429 Too Many Requests — v0.1 returned the failure
to the caller without retry.

### Helper API (private)
```hexa
fn _http_with_backoff_get(url, headers, timeout) -> map      // wraps http_get_with_headers_status
fn _http_with_backoff_head(url, headers, timeout) -> map     // wraps http_head
fn _http_with_backoff_curl_status(cmd) -> map                // wraps direct curl exec (download/upload)
```
Schedule: `[1s, 2s, 4s, 8s, 16s]`, max 5 retries. `_http_with_backoff_head`
honors `Retry-After` header when numeric (HEAD response surfaces headers;
GET wrapper does not yet — see honest C3 #1).

### Refactored callers
- `hf_whoami` → `_http_with_backoff_get`
- `hf_repo_info` → `_http_with_backoff_get`
- `hf_repo_tree` → `_http_with_backoff_get`
- `_hf_curl_head` → `_http_with_backoff_head`
- `hf_download_file` (single-shot path) → `_http_with_backoff_curl_status`
- `hf_upload_file` → `_http_with_backoff_curl_status`

### Constants
```hexa
HF_HUB_RL_MAX_RETRIES   = 5
HF_HUB_RL_BACKOFF_{0..4} = 1, 2, 4, 8, 16
```

### Honest C3 (FIX-2)
1. **`http_get_with_headers_status` does NOT surface response headers**, so the
   GET retry path falls back to the local schedule even if the server emits
   `Retry-After`. HEAD path honors it. Closing this gap is a Phase-2 stdlib/http
   API extension (`http_get_with_response_headers`).
2. **Backoff caps at 16s × 5 attempts ≈ 31s**: pathological 5-min throttle
   periods still surface as a final 429 to the caller. User can retry the bulk
   op manually or extend `HF_HUB_RL_MAX_RETRIES` (compile-time constant — change
   not yet exposed via setter).
3. **Sleep capped at 60s per call**: prevents a malicious / misconfigured
   `Retry-After: 86400` from stalling a process indefinitely.
4. **No jitter**: synchronized clients produce thundering-herd retries against
   the same shard. HF rate-limiter is per-token so this is mostly self-curing,
   but documented for observability.

---

## FIX-3 — LFS chunked / range-resumable download

### Why
v0.1 single-shot curl on a 5GB safetensors shard ties up one TCP connection
for minutes; transient network drops force a full retry. Range-header chunked
download recovers from per-chunk failures and parallel-friendly when caller
threads the loop.

### Helper API
```hexa
fn _hf_download_chunked(url, output_path, total_size, headers, timeout_sec) -> map
// returns {ok, status, bytes_written, chunks}

pub fn hf_set_chunk_threshold(chunk_mb: int, threshold_mb: int)
// caller knob: chunk_mb=0 disables; threshold_mb<0 forces chunked for every download
```

### Constants
```hexa
HF_HUB_CHUNK_BYTES            = 64 MB  (mutable; see hf_set_chunk_threshold)
HF_HUB_CHUNK_THRESHOLD_BYTES  = 100 MB (mutable; below threshold = single-shot)
```

### Flow
1. `hf_download_file` resolves expected_size via `hf_resolve_lfs`.
2. If `expected_size > HF_HUB_CHUNK_THRESHOLD_BYTES` → `_hf_download_chunked`.
3. Per-chunk: `Range: bytes=offset-end`, expect HTTP 206 Partial Content.
4. Append each chunk to output (`>>`). Truncate at start of run (`: > path`).
5. Final size + sha256 verify by existing `hf_download_file` path (unchanged).
6. **416 Range Not Satisfiable** → fallback to single-shot path.
7. **200 mid-stream** → server ignored Range; treat as corrupt unless first chunk.

### Honest C3 (FIX-3)
1. **Per-chunk sha256 NOT performed**: HF Hub does not advertise per-chunk
   hashes. Final-file sha256 against `x-linked-etag` remains the SOLE source
   of truth.
2. **No incremental resume across process restarts**: each call truncates and
   re-downloads from offset 0. A `.partial` ledger is a Phase-3 enhancement.
3. **Sequential chunks only**: parallel chunk fetch is not implemented — the
   loop is straight line. For >5GB models, the speedup is from per-chunk 429
   isolation, not parallelism.
4. **Append via `>>` shell**: assumes filesystem support for atomic append. On
   network filesystems (NFS) without locking, concurrent writers to the same
   `output_path` would interleave. Single caller per path is required.

---

## Parse + selftest evidence

### Parse
```
$ /Users/ghost/.hx/bin/hexa parse /Users/ghost/core/hexa-lang/stdlib/http.hexa
RC=0  (PASS — no errors emitted)

$ /Users/ghost/.hx/bin/hexa parse /Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa
RC=0  (PASS — no errors emitted)
```

### Selftest (offline subset; live gated on `ANIMA_HF_HUB_LIVE=1`)
```
$ /Users/ghost/.hx/bin/hexa test /Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa
── stdlib/hf_hub selftest ──
  SKIP F-HF-HUB-5 (HF_TOKEN unset or too short)
  PASS offline header parse content-length
  PASS offline header parse etag stripped
  PASS repo kind models
  PASS repo kind datasets
  PASS F-FIX-2 backoff[0]==1
  PASS F-FIX-2 backoff[1]==2
  PASS F-FIX-2 backoff[4]==16
  PASS F-FIX-2 backoff[99]==16 (capped)
  PASS F-FIX-3 chunk knob 8MB
  PASS F-FIX-3 threshold knob 50MB
  SKIP live tests (set ANIMA_HF_HUB_LIVE=1 to enable)
── selftest summary: pass=10 fail=0 ──
1 pass, 0 fail, 0 skip
```

---

## Falsifier set

| ID | Statement | Evidence | Status |
|----|-----------|----------|--------|
| F-FIX-1 | `http_head` returns `{status, headers, body:"", ok}` shape with header parse | `parse PASS`; live HEAD round-trip deferred (network) | PARSE-PASS / LIVE-DEFERRED |
| F-FIX-2 | `_http_with_backoff_*` triggers retry on simulated 429 with exponential `[1,2,4,8,16]` schedule capped at 5 attempts | `_hf_backoff_floor` 4/4 PASS in selftest; live 429 mock deferred | OFFLINE-PASS / LIVE-DEFERRED |
| F-FIX-3 | `hf_set_chunk_threshold` knob writes back `HF_HUB_CHUNK_BYTES` + `HF_HUB_CHUNK_THRESHOLD_BYTES`; chunked download round-trip sha256 match for >100MB file | knob set/restore 2/2 PASS; live >100MB sha256 round-trip deferred | OFFLINE-PASS / LIVE-DEFERRED |

---

## Breaking risk

**Zero** — all three fixes are additive:
- `http.hexa` adds `http_head` (+ private helpers); no existing symbol touched.
- `hf_hub.hexa` adds private retry/chunk helpers + 1 new public knob
  (`hf_set_chunk_threshold`); existing public API surface unchanged.
- `_hf_curl_head` internals refactored to delegate to `http_head` — return
  shape `{status, headers, ok}` preserved (added pass-through `body:""` is a
  superset, callers that only key-read pre-existing fields are unaffected).

## Constraints honored

- raw#9 hexa-canonical: pure hexa, zero new C builtin, zero runtime.c change.
- raw#10 honest C3: 4 per fix, 12 total.
- raw#15 / raw#71: no token leakage; all retry helpers reuse the existing
  `_hf_auth_headers` map and `hf_redact_token` is unchanged.
- No git push, no chflags, no other stdlib files touched.
