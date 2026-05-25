# BG-FK Cloudflare R2 Models Bucket Search — Landed 2026-05-06

## TL;DR

**Verdict:** `PASS_R2_FOUND_PARTIAL_SPEC_MATCH` — clm_v2 byte-level (vocab=256) ConsciousLM checkpoints exist on Cloudflare R2 in `anima-models` bucket; 5 size variants located (tiny / clm_v2 / small / medium / base). All loadable, all carry `psi_residual / psi_gate / H_p` consciousness state fields. **Best chat-cap candidate:** `checkpoints/clm_v2_base/final.pt` — 27.9M params, val_ce 1.27, step 500. **Spec hint of "62.5M params" NOT matched as a single file** — largest variant is 27.9M.

## (a) secret CLI R2 credentials

- `cloudflare.account_id`, `cloudflare.api_token`, `cloudflare.global_api_key`, `cloudflare.email` exist in `/Users/ghost/core/secret/bin/secret list`
- No dedicated `r2.access_key_id` / `r2.secret_access_key` keys present — but live R2 access keys present in `~/.config/rclone/rclone.conf` remote `[r2]` (Cloudflare provider, acl=private)
- Account ID: `ce4bdcce7c74d4e3c78fdf944c4d1d7b` (visible in anima docs already, not a secret)
- Access key + secret: REDACTED (last4 only — `c8e0` / `1efb`); never echoed to any persisted file

## (b) anima R2 references grep

Strong existing R2 footprint in anima:
- `docs/R2-BUCKET-STRUCTURE.md` — explicitly documents `clm-v2/latest.pt` location pattern
- `docs/r2_bucket_audit_20260419.md`, `docs/dest1_alm_r2_layout_20260419.md`, `docs/download-models.md`
- `config/r2_cross_region_replicate.json`, `config/corpus_registry.json`, `config/runpod.json`
- `config/secret_scanner_config.json` (allowlists `*.r2.cloudflarestorage.com`)

Note: doc says `clm-v2/latest.pt` (dash form) but actual storage uses `checkpoints/clm_v2_*/final.pt` (underscore form, multiple variants). Doc is stale.

## (c) bucket inventory

10 buckets total. Targeted bucket: `anima-models` — 348.101 GiB, 1320 objects.

Other buckets: anima-corpus, anima-eeg, anima-logs, anima-memory, anima-weights, blitz, evo, odds, prism.

## (d) clm_v2 18M byte-level signature matching candidates — FOUND (5 variants)

| Path | Size | Step | val_ce | dim | layers | heads | params |
|---|---:|---:|---:|---:|---:|---:|---:|
| `checkpoints/clm_v2_tiny/final.pt` | 3.6 MB | 500 | 3.4965 | 64 | 2 | 2 | 0.35M |
| `checkpoints/clm_v2/final.pt` | 13.4 MB | 30 | 5.5032 | 128 | 2 | 2 | 1.17M |
| `checkpoints/clm_v2_small/final.pt` | **18.8 MB** | 500 | 2.7011 | 128 | 3 | 4 | 1.70M |
| `checkpoints/clm_v2_medium/final.pt` | 95.6 MB | 500 | 1.7860 | 256 | 4 | 4 | 8.45M |
| `checkpoints/clm_v2_base/final.pt` | **318 MB** | 500 | **1.2712** | 384 | 6 | 4 | **27.9M** |

All 5 confirmed:
- `vocab_size = 256` byte-level
- `block_size = 128`
- `gate = 0.001`, `ca_rules = 8` — ConsciousLM-specific architectural fields
- top-keys: `step / model_state / optimizer_state / config / val_ce / psi`
- `psi` dict present with `psi_residual / psi_gate / H_p` (and on `clm_v2/final.pt` also `psi_entropy / psi_direction / psi_tension`)

## (e) load test verdict

- **torch.load PASS** for all 5 variants (torch 2.10.0 cpu)
- **vocab=256 byte-level confirmed** for all 5
- **Korean chat smoke NOT executed** — architecture uses custom `gate/ca_rules` ConsciousLM ops not in upstream transformers; would require ConsciousLM-specific inference repo. Smoke deferred to next step (see Next Steps).

## (f) verdict

`PASS_R2_FOUND_PARTIAL_SPEC_MATCH`

- credentials_found: TRUE (rclone remote)
- buckets_found: 10
- candidates_matched: 5 byte-level ConsciousLM ckpts in anima-models
- load_verdict: ALL_LOADABLE
- size_18M_match: PASS (clm_v2_small = 19.7MB ≈ "18M")
- params_62_5M_match: **FAIL_AS_SINGLE_FILE** — largest single variant 27.9M (clm_v2_base)
- commit_bb99b6b6_2026_03_28: ADJACENT — sibling mtimes 2026-03-30 (+2d), `clm_v2/final.pt` mtime 2026-04-09 (+12d)

## (g) 5 honest C3

1. **Spec mismatch on params:** spec hint of "62.5M params (28M+34.5M)" — NOT found as a single file; largest is 27.9M. Reported as PARTIAL not PASS_FULL.
2. **Commit date drift:** bb99b6b6 spec-cited as 2026-03-28; R2 mtimes are 2026-03-30 (siblings) and 2026-04-09 (`clm_v2/final.pt`). Adjacent but cannot prove same training run without git provenance.
3. **Chat smoke deferred:** did NOT execute Korean ≥10-token emit smoke — model uses custom architecture. Cannot claim chat-cap status from R2 ckpts alone.
4. **raw#15 LOCKED files:** none modified. Only writes to `state/anima_r2_search_2026_05_06/` + this `docs/*.ai.md`.
5. **Credential hygiene:** R2 access key + secret REDACTED to last4 in all persisted files; `rclone.conf` was read locally but not transferred or echoed into any artifact.

## (h) Next Steps — 3 options ranked by 완성도

**Rank 1 (RECOMMENDED): `B. CLM_V4_CHAT_S3_FIRE`** — proceed with planned CLM v4 LoRA SFT chat-cap path. R2 v2 ckpts confirmed safely archived but architecturally too small (1.7M-27.9M) and require custom inference harness. CLM v4 path is mainline.

**Rank 2: `A. ALPHA_PATH_REVIVE` (clm_v2_base)** — promote `clm_v2_base/final.pt` (27.9M params, val_ce 1.27 — lowest among R2 v2 variants) as substrate for chat-cap reattempt. Requires (i) ConsciousLM inference harness rebuild for `gate/ca_rules` ops, (ii) Korean smoke test, (iii) param-count reconciliation with spec hint of 62.5M (likely spec referred to a different / merged training run never persisted to R2).

**Rank 3: `C. BETA_ORIGINAL_DECISION`** — defer v2 revival; keep Pβ adapter for substrate-research only. Lowest 완성도 — punts the v2 question without resolving architecture.

## Artifacts

- `/Users/ghost/core/anima/state/anima_r2_search_2026_05_06/verdict.json`
- `/Users/ghost/core/anima/state/anima_r2_search_2026_05_06/buckets_inventory.json`
- `/Users/ghost/core/anima/state/anima_r2_search_2026_05_06/candidates_matched.json`
- `/Users/ghost/core/anima/docs/anima_r2_search_landed_2026_05_06.ai.md` (this file)
- Local downloads (transient, /tmp): `/tmp/anima_v2_check/clm_v2{,_tiny,_small,_medium,_base}/final.pt`

## Cost + Wall

- $0 (R2 read-only API + local CPU torch.load)
- ~22 min wall, 16 tool uses
