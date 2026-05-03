# CLM-v4 Tokenizer F-TOK-1 / F-TOK-2 Status Report (BG-κ)

**Date (UTC):** 2026-05-04
**Scope:** Read-only verification of HF mirror push state and ubu1 hub cache state for the canonical 64K BPE tokenizer (`tokenizer_64k_multilingual.{model,vocab}`).
**Owner of write:** `state/clm_v4_tokenizer_ubu1_cache_status_2026_05_04/` only.
**Non-overlap:** does not touch BG-iota (`p9_path_a_llama_lora_*`) or BG-lambda (`clm_v4_tokenizer_caller_migration_spec_*`).

---

## 1. Executive verdicts

| Gate | Verdict | One-line evidence |
|------|---------|-------------------|
| F-TOK-1 (HF mirror sha256 match restoration sha256) | **PASS (audit-log basis)** | Upload audit `sha256_map` matches local sha256 byte-for-byte; live HEAD probe blocked by 401 (auth/token issue) so PASS is asserted via the recorded upload audit, not re-fetched via HTTP. |
| F-TOK-2 (ubu1 cache roundtrip identical bytes) | **UNMET** | ubu1 hub cache for repo `need-singularity/clm-v4-base-mirror` exists but contains ONLY `best.pt` (5.36 GB blob); no tokenizer model/vocab present. Cache prime not yet executed. |
| F-TOK-3 prep (vocab_size) | **PASS (vocab line count = 64000)** | `wc -l tokenizer_64k_multilingual.vocab` = 64000 matches `integrity_report.json` `spec.vocab_size = 64000`. |

**status_emit (single line, stdout-style):**

```
__CLM_V4_TOKENIZER_UBU1__ UNMET
```

(F-TOK-2 fails the AND-gate of {F-TOK-1, F-TOK-2} → overall sentinel = UNMET.)

---

## 2. Source artifact bit-exact re-verification (Mac)

```
shasum -a 256 state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.{model,vocab}
```

| File | Bytes (actual) | Bytes (integrity_report) | sha256 (actual) | sha256 (integrity_report) | match |
|------|----------------|--------------------------|-----------------|---------------------------|-------|
| `tokenizer_64k_multilingual.model` | 1306349 | 1306349 | `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` | `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` | YES |
| `tokenizer_64k_multilingual.vocab` | 989272 | 989272 | `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4` | `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4` | YES |

Source artifacts re-verified bit-exact against `integrity_report.json` recorded 2026-05-03T15:09:00Z. No drift on Mac side.

---

## 3. F-TOK-1: HF mirror sha256 (read-only)

### 3.1 Upload audit log (authoritative provenance)

`state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`:

```json
{
  "ts_utc": "2026-05-03T15:13:41Z",
  "mode": "upload",
  "repo": "need-singularity/clm-v4-base-mirror",
  "file_count": 4,
  "total_bytes": 2304683,
  "sha256_map": {
    "README.md": "f298bfba35a9c8ee7a4f2fe91e7c19f25bd8e1bdd7482588ab233d1018eed6ec",
    "integrity_report.json": "4632e4eb07b26b0d899bbb3cbac2f5dce2ecc0d0ec68483b94be82596a70726d",
    "tokenizer_64k_multilingual.model": "bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab",
    "tokenizer_64k_multilingual.vocab": "972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4"
  },
  "commit_url": "https://huggingface.co/need-singularity/clm-v4-base-mirror/commit/10ee03687db312c55bbec5858c814bef28e4d365",
  "outcome": "ok"
}
```

| File | Local sha256 | Audit-recorded HF push sha256 | match |
|------|--------------|-------------------------------|-------|
| `tokenizer_64k_multilingual.model` | `bb851d39…b710b8ab` | `bb851d39…b710b8ab` | YES |
| `tokenizer_64k_multilingual.vocab` | `972fc0ba…efa480a4` | `972fc0ba…efa480a4` | YES |

### 3.2 Live HEAD probe (best-effort)

Attempted unauth + auth HEAD on:
- `https://huggingface.co/need-singularity/clm-v4-base-mirror/resolve/main/tokenizer_64k_multilingual.model`
- `https://huggingface.co/need-singularity/clm-v4-base-mirror/resolve/main/tokenizer_64k_multilingual.vocab`
- `https://huggingface.co/need-singularity/clm-v4-base-mirror/resolve/main/tokenizer/tokenizer_64k_multilingual.model`

All returned `HTTP/2 401` (`Invalid username or password`). The repo is private and the locally-stored HF token at `/Users/ghost/.cache/huggingface/token` (37-byte `hf_E…`) is rejected by the API. Same on ubu1: `hf auth whoami` reports "Invalid user token. The token stored is invalid. Please run `hf auth login --force`."

So we cannot independently confirm via live HEAD that the bytes on HF still match the audit-log-recorded sha256. The audit log was emitted by the same upload pipeline that recorded `outcome=ok` and `commit_url=…/commit/10ee03687db312c55bbec5858c814bef28e4d365`, so under the assumption that no force-push has rewritten history (which the audit log gives no indication of), F-TOK-1 = PASS.

### 3.3 F-TOK-1 verdict

**PASS** with C3: depends on HF remote not having been force-pushed since 2026-05-03T15:13:41Z, and depends on the upload audit log being trustworthy. Live re-verification deferred until a valid HF token is restored.

---

## 4. F-TOK-2: ubu1 cache roundtrip

### 4.1 ubu1 SSH reachability

```
$ ssh ubu1 "uname -a && whoami"
Linux aiden-B650M-K 6.17.0-22-generic … x86_64 GNU/Linux
aiden
```

SSH OK.

### 4.2 ubu1 hub cache contents for `models--need-singularity--clm-v4-base-mirror`

```
$ ssh ubu1 "find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/ -type f"
~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/.no_exist/856278beb59c5b39f16485cc8f3a46dcdaf9d1e3/config.json
~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/refs/main
~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/blobs/22f180efc380aecb4a320191502afa13b81abcd077ec36c5f003dcfbe1d680b4
```

Snapshot dir:

```
~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/856278beb59c5b39f16485cc8f3a46dcdaf9d1e3/
  best.pt -> ../../blobs/22f180efc380aecb4a320191502afa13b81abcd077ec36c5f003dcfbe1d680b4 (5,365,727,261 bytes)
```

ubu1 hub cache contains exactly **one** materialized blob — the 5.36 GB checkpoint `best.pt`. There is **no** `tokenizer_64k_multilingual.model`, **no** `tokenizer_64k_multilingual.vocab`, **no** `README.md`, and **no** `integrity_report.json` from the 2026-05-03T15:13:41Z upload.

Note: `refs/main` points to `856278beb59c5b39f16485cc8f3a46dcdaf9d1e3`, which is **not** the tokenizer-upload commit `10ee03687db312c55bbec5858c814bef28e4d365`. The ubu1 cache is pinned to an older snapshot from a checkpoint-only download cycle and has not been refreshed since the tokenizer push.

### 4.3 F-TOK-2 verdict

**UNMET.** ubu1 cache has not been primed with the tokenizer artifacts. There is no path to do a sha256 roundtrip comparison without first executing a download.

---

## 5. F-TOK-3 prep: vocab_size

```
$ wc -l state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.vocab
   64000 …/tokenizer_64k_multilingual.vocab
```

Matches `integrity_report.json` `spec.vocab_size = 64000` exactly. (SentencePiece `.vocab` is one piece per line — no header — so 64000 lines = 64000 pieces.)

F-TOK-3 prep: PASS.

---

## 6. Decision matrix (next-cycle exec)

Current state: **F-TOK-1 PASS (audit-log basis) + F-TOK-2 UNMET**.

Per plan §4, this branch maps to: **prime ubu1 cache, then re-run roundtrip check before BG-lambda byte-fallback caller migration consumes the tokenizer**.

### 6.1 Required next actions (in order)

1. **Restore HF auth on ubu1** (token currently invalid):
   ```
   ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && hf auth login --token <NEW_HF_TOKEN>'
   ```
   Re-verify with `hf auth whoami`.

2. **Prime ubu1 cache for tokenizer-only files** (cheap; ~2.3 MB total, NOT the 5.36 GB checkpoint):
   ```
   ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && \
     hf download need-singularity/clm-v4-base-mirror \
       tokenizer_64k_multilingual.model tokenizer_64k_multilingual.vocab \
       --revision 10ee03687db312c55bbec5858c814bef28e4d365'
   ```
   (Pinning the revision to the tokenizer-upload commit avoids any later drift.)

3. **Roundtrip sha256 check on ubu1**:
   ```
   ssh ubu1 'find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/ \
     -name tokenizer_64k_multilingual.model -exec shasum -a 256 {} \;'
   ```
   Expected output (sha256 portion):
   ```
   bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab
   ```
   And for `.vocab`:
   ```
   972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4
   ```

4. **Live HEAD re-verify** (with restored token) for F-TOK-1 hardening:
   ```
   curl -sI -H "Authorization: Bearer ${HFTOKEN}" \
     'https://huggingface.co/need-singularity/clm-v4-base-mirror/resolve/10ee03687db312c55bbec5858c814bef28e4d365/tokenizer_64k_multilingual.model'
   ```
   Confirm `content-length: 1306349` and (if Xet) `x-linked-size: 1306349`.

### 6.2 Branch table

| F-TOK-1 | F-TOK-2 | Action |
|---------|---------|--------|
| PASS | PASS | Ready for BG-lambda byte-fallback caller migration to land. |
| PASS | UNMET (current) | Prime cache (step 2 above). Cost: ~2.3 MB download per ubu1 prime; trivial. |
| FAIL | * | Re-upload required. Cost: same ~2.3 MB push from Mac via the canonical pipeline (`tool/hf_upload_mk2.hexa`). The audit log makes a re-upload extremely unlikely to be needed unless HF lost the commit. |

---

## 7. Honest C3 caveats (raw#10)

1. **HF API rate-limit / ETag drift between probe time and exec time.** Live HEAD probes were 401-blocked by an invalid local token; even after token restoration, ETag/`x-linked-size` could change if anyone force-pushes the mirror branch. Re-verification at exec time is mandatory before `__CLM_V4_TOKENIZER_UBU1__ PASS` can be emitted.
2. **LFS pointer vs actual file ambiguity.** With Xet/LFS-backed repos, a `resolve/main/<path>` URL can return a JSON LFS-pointer (~150 bytes) instead of the actual file when the client lacks Xet support; sha256 over that pointer would not equal the real file's sha256. Any future programmatic verification must check `content-length` against the expected byte size (1306349 / 989272), not just check that *some* response was returned.
3. **ubu1 cache eviction policy.** Even if step 2 above primes the cache today, HF Hub cache eviction (or a manual `hf cache delete`) could evict the tokenizer blobs before the next training run. F-TOK-2 must be re-checked at the start of every training cycle that depends on the cached tokenizer, not assumed-stable from a previous prime.
4. **Token state divergence.** Both the Mac local token (`/Users/ghost/.cache/huggingface/token`, 37 B `hf_E…`) and the ubu1 token (`/home/aiden/.cache/huggingface/token`, 38 B `hf_E…`) are currently rejected by HF API. We cannot rule out that the upload audit log of 2026-05-03T15:13:41Z was emitted under a now-revoked token; the recorded sha256 still match local artifacts, so we trust the bytes were pushed, but live verification is genuinely deferred.
5. **`refs/main` points to the wrong commit on ubu1.** ubu1's hub cache `refs/main = 856278beb59c5b39f16485cc8f3a46dcdaf9d1e3` is older than the tokenizer-upload commit `10ee03687db312c55bbec5858c814bef28e4d365`. A naive `hf download <repo>` (without `--revision`) might or might not refresh `refs/main` depending on whether the cache resolver re-queries HF; we recommend pinning `--revision 10ee03687db312c55bbec5858c814bef28e4d365` to be safe.
6. **Read-only constraint honored, but partial verification is the cost.** This BG could not perform an actual download to bit-compare bytes, so F-TOK-2 must remain UNMET until a write-permitted cycle executes the prime. We do not fabricate PASS based on the upload-audit alone for F-TOK-2 because F-TOK-2's specific claim is "ubu1 cache load round-trips identical bytes" — and the cache currently has no tokenizer to load.

---

## 8. Status_emit sentinel (single-line, stdout-style)

```
__CLM_V4_TOKENIZER_UBU1__ UNMET
```

Reason: F-TOK-1 PASS (audit-log) AND F-TOK-2 UNMET → overall = UNMET (block on F-TOK-2 prime).

---

## 9. Files touched

- Created: `state/clm_v4_tokenizer_ubu1_cache_status_2026_05_04/status_report.md` (this file).
- Read-only references:
  - `state/clm_v4_tokenizer_restoration_2026_05_03/integrity_report.json`
  - `state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.{model,vocab}`
  - `state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`
  - ubu1 SSH probes (read-only; no `hf download`, no upload, no chflags, no git mutation).

No `.py` files created (raw#9). No git operations (per BG charter — parent serializes commits). No HF mutation. No SSH-side mutation.
