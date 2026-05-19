# Falsifier Set — F-HF-HUB-1..5 (Phase 1 PR draft, 2026-05-04)

> raw#71 falsifier-bound spec for `stdlib/hf_hub.hexa`. Each falsifier has a clear pass/fail predicate, a method (offline / live network), a current verdict, and reproduction steps.
>
> Selftest evidence: `selftest_log.txt` in this directory.

---

## F-HF-HUB-1 — `hf_whoami` validates token correctly

**Predicate**:
- (a) Valid `$HF_TOKEN` → `hf_whoami(token)["ok"] == true` AND `hf_whoami(token)["user"]["name"]` is non-empty string.
- (b) Invalid token (e.g. `"clearly_invalid_token_xxxxx"`) → `["ok"] == false` AND `["status"] == 401`.

**Method**: LIVE — requires `$HF_TOKEN` env + `$ANIMA_HF_HUB_LIVE=1` + network reachability to `https://huggingface.co`.

**Verdict**: **DEFERRED** — gated on live network access (intentional; CI/offline runs SKIP this falsifier). Selftest harness includes the assertions; running with the live gate will execute and PASS/FAIL.

**Reproduction**:
```sh
export HF_TOKEN=<HF_TOKEN_VALUE>     # opaque token from huggingface.co/settings/tokens
export ANIMA_HF_HUB_LIVE=1
cd /Users/ghost/core/hexa-lang && /Users/ghost/.hx/bin/hexa_real run stdlib/hf_hub.hexa | grep "F-HF-HUB-1"
# Expect: PASS F-HF-HUB-1 whoami ok
#         PASS F-HF-HUB-1 invalid token rejected
```

---

## F-HF-HUB-2 — `hf_repo_tree` returns canonical Llama-3.2-3B file list

**Predicate**: `hf_repo_tree("meta-llama/Llama-3.2-3B", "main", true, "")["files"]` contains an entry with `path == "config.json"`.

Optional stronger predicate (uncomment in selftest): also contains `tokenizer.json`, `tokenizer.model`, `model.safetensors`.

**Method**: LIVE — requires HF read access to `meta-llama/Llama-3.2-3B` (gated public model, requires accepted license + token).

**Verdict**: **DEFERRED** — gated on live network + license-accepted token. Selftest harness asserts presence of `config.json`.

**Reproduction**:
```sh
export HF_TOKEN=<HF_TOKEN_VALUE>     # license-accepted token
export ANIMA_HF_HUB_LIVE=1
cd /Users/ghost/core/hexa-lang && /Users/ghost/.hx/bin/hexa_real run stdlib/hf_hub.hexa | grep "F-HF-HUB-2"
# Expect: PASS F-HF-HUB-2 tree contains config.json
```

**Fallback if Llama license blocks**: substitute a public-no-license repo like `gpt2` or `bert-base-uncased`.

---

## F-HF-HUB-3 — `hf_download_file` round-trip with sha256 verify

**Predicate**: `hf_download_file("meta-llama/Llama-3.2-3B", "main", "config.json", "/tmp/_hf_hub_selftest_config.json", "")` returns:
- `ok == true`
- `bytes_written > 100` (real config.json is ~700 bytes)
- file exists on disk at returned `local_path`
- if file is LFS-tracked (which `config.json` is NOT), `sha256` matches `x_linked_etag`.

**Method**: LIVE — same gating as F-HF-HUB-2.

**Verdict**: **DEFERRED**. Selftest assertion present.

**Reproduction**: same `ANIMA_HF_HUB_LIVE=1` env + `grep "F-HF-HUB-3"`.

---

## F-HF-HUB-4 — `hf_resolve_lfs` returns `x-linked-etag` for LFS file

**Predicate**: `hf_resolve_lfs("meta-llama/Llama-3.2-3B", "main", "model.safetensors", "")` returns:
- `ok == true`
- `x_linked_etag` is non-empty AND either starts with `"sha256:"` (length 71) OR is a 64-character hex string (sha256 stripped of prefix).
- `content_length > 1_000_000_000` (real shard is ~6GB).

**Method**: LIVE — HEAD request only (no download), still requires license-accepted token for the gated repo.

**Verdict**: **DEFERRED**. Selftest assertion present (length / prefix check).

**Reproduction**: same gating, `grep "F-HF-HUB-4"`.

**Why this matters**: this is the keystone for safetensors numeric loading — without sha256 verify, a man-in-the-middle on the LFS S3 redirect could corrupt downloaded weights and the user would never know. F-HF-HUB-4 confirms our HEAD parse correctly extracts the canonical sha256 source-of-truth.

---

## F-HF-HUB-5 — Token never appears in stdout/stderr

**Predicate**: For any sample log line `L` containing `$HF_TOKEN` (≥8 chars), `hf_redact_token(L)` returns a string `R` such that:
- `R.index_of(HF_TOKEN) < 0` (token absent)
- `R.index_of("<HF_TOKEN>") >= 0` (placeholder present)

Stronger predicate (out of v0.1 scope, future Phase 1.5): no `println` / `exec` invocation inside `hf_hub.hexa` itself emits the raw token to stdout/stderr. Static lint required to prove this exhaustively.

**Method**: OFFLINE — no network required. Sample log line constructed in-memory.

**Verdict**: **PASS** (selftest_log.txt Run 2 with a synthetic placeholder token set):
```
PASS F-HF-HUB-5 token redacted
```

**Reproduction**:
```sh
HF_TOKEN=<HF_SYNTHETIC_LONG_PLACEHOLDER_VALUE> \
  /Users/ghost/.hx/bin/hexa_real run /Users/ghost/core/hexa-lang/stdlib/hf_hub.hexa | grep "F-HF-HUB-5"
# Expect: PASS F-HF-HUB-5 token redacted
```

The synthetic token need only satisfy `len(tok) >= 8`. Use any opaque string of ≥8 chars; a real token is NOT required for this falsifier (it is offline by design).

---

## Supporting offline checks (always run — non-numbered)

These are not full F-HF-HUB falsifiers but tight smoke assertions verifying the parsers work on synthetic inputs without network:

| Check | Predicate | Verdict |
|---|---|---|
| `_hf_parse_headers` content-length | `to_int(h["content-length"]) == 1234` for sample HTTP block | **PASS** |
| `_hf_parse_headers` etag strip | `_hf_strip_quotes(h["etag"]) == "abc"` | **PASS** |
| `_hf_repo_kind` models | `_hf_repo_kind("meta-llama/Llama-3.2-3B") == "models"` | **PASS** |
| `_hf_repo_kind` datasets | `_hf_repo_kind("datasets/wikitext") == "datasets"` | **PASS** |

All four PASS in `selftest_log.txt` Run 1 + Run 2.

---

## Verdict summary

| Falsifier | Type | Status |
|---|---|---|
| F-HF-HUB-1 | LIVE | DEFERRED (selftest authored, network-gated) |
| F-HF-HUB-2 | LIVE | DEFERRED |
| F-HF-HUB-3 | LIVE | DEFERRED |
| F-HF-HUB-4 | LIVE | DEFERRED |
| F-HF-HUB-5 | OFFLINE | **PASS** |
| supporting #1-4 | OFFLINE | **PASS** (4/4) |

**Offline pass rate**: 5/5 (4 supporting + F-HF-HUB-5). **Live pass rate**: pending operator-driven validation behind `ANIMA_HF_HUB_LIVE=1` gate; selftest harness contains the assertions and will surface PASS/FAIL on first live run.

**Acceptance for Phase 1 land**: offline 5/5 PASS is the bar. Live falsifiers are explicitly DEFERRED (raw#71 allows deferred falsifiers when network/auth-gated, with reproduction steps documented — both present here).
