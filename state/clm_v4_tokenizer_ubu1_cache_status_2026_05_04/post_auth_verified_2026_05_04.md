# post-auth F-TOK-1 + F-TOK-2 verified 2026-05-04

## TL;DR

After HF token re-auth (user provided fresh token via `secret set huggingface.token` + `secret set hf.token`, sync'd via `pbpaste | secret set …` 2026-05-04), all gates blocked by "Invalid user token" in the prior cycle (commit `61fa77c2c`) are now PASS.

| Gate | Prior verdict (61fa77c2c) | This cycle | Method |
|---|---|---|---|
| F-TOK-1 (HF mirror sha256) | PASS (audit-log basis only — live HEAD blocked 401) | **PASS (live HEAD verified)** | curl HEAD with Bearer → `x-linked-etag` matches local sha256 byte-for-byte |
| F-TOK-2 (ubu1 cache roundtrip) | UNMET (cache miss; only stale `best.pt` 5.36GB present) | **PASS** | `hf download` at revision-pin `10ee03687…` succeeded; sha256 of cached files matches local source bit-exact |
| F-TOK-3 prep (vocab_size) | PASS | PASS (unchanged) | `wc -l .vocab = 64000` |

## Auth refresh flow

1. **User action**: generated fresh write-permission token at `https://huggingface.co/settings/tokens`; set into both `huggingface.token` and `hf.token` keys via `secret set` (interactive tty mode, no echo).
2. **sync chain (foreground)**: `secret get huggingface.token > .secrets/hf_token` → `cp .secrets/hf_token ~/.cache/huggingface/token` → `cat .secrets/hf_token | ssh ubu1 'cat > ~/.cache/huggingface/token'`. All 3 file locations + 1 ubu1 location now bit-exact (sha256 first-16 = `1e0a843263e1a2a8`).
3. **whoami verification**: `curl -H "Authorization: Bearer $TOKEN" https://huggingface.co/api/whoami-v2` returned user `dancinlife` / `Aiden Park` / id `69229786cde1fd9952da8cfa` on both Mac + ubu1.

Backups preserved at `~/.cache/huggingface/token.bak_2026_05_04` (Mac) and equivalent on ubu1 (older invalid tokens, not restorable as auth).

## F-TOK-1 evidence (Mac live HEAD, post-auth)

```
GET https://huggingface.co/need-singularity/clm-v4-base-mirror/resolve/10ee03687db312c55bbec5858c814bef28e4d365/tokenizer/tokenizer_64k_multilingual.model
→ content-length: 1397                # LFS pointer file size (not actual blob)
→ x-repo-commit: 10ee03687db312c55bbec5858c814bef28e4d365
→ x-linked-etag: "bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab"
```

`x-linked-etag` = LFS oid (sha256 of actual content) = our local source artifact sha256 byte-for-byte. F-TOK-1 → **PASS (live verified)**.

## F-TOK-2 evidence (ubu1 download + roundtrip sha256)

```
ssh ubu1 '/home/aiden/venv_orchestrator/bin/hf download need-singularity/clm-v4-base-mirror \
    tokenizer/tokenizer_64k_multilingual.model \
    tokenizer/tokenizer_64k_multilingual.vocab \
    tokenizer/integrity_report.json \
    --revision 10ee03687db312c55bbec5858c814bef28e4d365'

✓ Downloaded 3 files
path: /home/aiden/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/10ee03687db312c55bbec5858c814bef28e4d365

shasum -a 256 <snap>/tokenizer/tokenizer_64k_multilingual.{model,vocab}
bb851d39fbe3286d…  …/tokenizer_64k_multilingual.model
972fc0ba2f2633cf…  …/tokenizer_64k_multilingual.vocab
```

Both sha256 first-16 match local source artifact `state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.{model,vocab}` bit-exact. F-TOK-2 → **PASS**.

## status_emit (sentinel update)

Prior: `__CLM_V4_TOKENIZER_UBU1__ UNMET` (61fa77c2c)
This cycle: `__CLM_V4_TOKENIZER_UBU1__ PASS`

## Next-cycle unblocked

1. **byte-fallback caller migration** (per BG-λ spec, commit `68803d162`): F-TOK-1 + F-TOK-2 + F-TOK-3 all PASS → migration window confirmed open. F-MIG-1/2/3/4 falsifiers ready for execution. Recommended F-TOK-4 PR-ready target: full `.py` → `.hexa` replacement of `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py` (gitignored, line-only edit insufficient under raw#9 strict).

2. **F1_v3 base-validation BG cycle** (per `.roadmap.p9_sft cond.benchmark_a_prime_base_validation`): no longer blocked on HF auth. ubu1 BG cycle ~6-17h, $0. Llama-3.2-3B + CLM v4 base both already cached on ubu1.

3. **P9 path A LoRA HF push verification** (per BG-ι Path A complete, commit `e4d86fb2f`): Path A trained LoRA adapter at HF mirror — now live-checkable via `hf download` or `hf list` against the path A pod's recorded HF tag (need-singularity/clm-v4-sft-final or similar).

## Honest C3 (raw#10)

1. **Token longevity unverified**: HF tokens can be revoked / rotated / expire. Current verification is point-in-time (2026-05-04 Mac + ubu1 wallclock). Future cycles must re-verify before depending on auth state.
2. **3-location sync drift risk**: `.secrets/hf_token`, Mac `~/.cache/huggingface/token`, ubu1 `~/.cache/huggingface/token`, `secret get huggingface.token`, `secret get hf.token` are 5 storage points. Any partial update breaks consistency. The `secret` CLI is the natural SSOT — recommend documenting that and treating other locations as derived caches refreshed via the sync command.
3. **`hf` CLI path on ubu1 is venv-local**: `/home/aiden/venv_orchestrator/bin/hf` is required (not in default PATH). Any future BG/script must use the full path or activate the venv first; bare `hf` will fail with "command not found".
4. **F-TOK-1 LFS pointer vs blob ambiguity**: `content-length: 1397` returned by HEAD is the LFS pointer file size, NOT the 1.3MB actual content. The bit-exact match was made via `x-linked-etag` (LFS oid header). For files <50MB without LFS, `content-length` = blob size and the verification logic differs. Future verifiers must branch on LFS-vs-direct.
5. **Repo subpath assumption**: Initial `hf download` with files-at-root failed silently ("Fetching 0 files"). Correct path is under `tokenizer/` subdir per `https://huggingface.co/api/models/<repo>/tree/<rev>?recursive=true`. The audit log `sha256_map` keys are basenames only and were misleading. Future propagation tooling should normalize via the tree API, not the basename audit.

## Falsifier cross-link

- F-TOK-1 / F-TOK-2 / F-TOK-3 → all PASS this cycle
- F-TOK-4 → still UNMET (caller migration is the next gate; spec landed in `68803d162`)
- F-MIG-1/2/3/4 → unblocked, scheduled for next BG cycle

## raw invariants applied

- raw#9: hexa-on-Mac strict — only HTTP curl + scp + ssh used Mac-side; Python (`hf` CLI) only on ubu1 transient (raw#37 OK)
- raw#10: 5 honest C3 caveats (above)
- raw#15: repo-relative paths only (HF cache paths are absolute by HF design — noted but unavoidable)
- raw#37: transient-py-on-Linux explicit — `hf` CLI runs on ubu1 only
- raw#71: F-TOK-1/F-TOK-2 falsifier-bound, evidence captured byte-exact

## Pointer block

- prior status: `state/clm_v4_tokenizer_ubu1_cache_status_2026_05_04/status_report.md` (commit `61fa77c2c`)
- propagation plan: `state/clm_v4_tokenizer_propagation_plan_2026_05_04/plan.md` (commit `d373e67c7`)
- caller migration spec: `state/clm_v4_tokenizer_caller_migration_spec_2026_05_04/spec.md` (commit `68803d162`)
- restoration source: `state/clm_v4_tokenizer_restoration_2026_05_03/` (commit `90488dd3f`)
- HF audit log: `state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`
