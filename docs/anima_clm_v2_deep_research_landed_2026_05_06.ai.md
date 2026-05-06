# anima clm_v2 18M byte deep research — landed 2026-05-06

## Summary (KO+EN)

BG-FM: 외부 storage + multi-channel systematic search 결과, **v2 18M byte 가중치 = HF public repo로 발견됨**.
External storage + multi-channel search confirmed v2 18M byte weights are publicly available on HF (built today by sibling BG).

## Verdict

`PASS_DEEP_FOUND` — primary artifact: `need-singularity/clm-v2-byte-18m-convo-5k:convo_5k.pt`
- size 73,740,122 bytes (~70MB), sha256=`2f0ba391aff30f6a60bcefccb9215fdb45764bf07147f28c38013ca629881bbe`
- repo created 2026-05-06T06:53:45Z (today, by sibling BG)
- verified params 18.52M, 0 missing/unexpected keys when loaded
- chat capability `F_CLM_NATIVE_alpha_1_PASS=false` (gibberish output) — weight integrity OK, behavior FAIL

## Lane summaries

### (a) mac extended filesystem
Documents/Desktop/Downloads/Volumes/iCloud/Dropbox/CloudStorage = empty.
PRIMARY HIT: `/private/tmp/anima_v2_check/` pre-staged today by sibling BG (5 variants: tiny 0.35M / small 1.70M / clm_v2 1.17M / medium 8.45M / base 27.93M, all byte-vocab=256, mtime 2026-03-30 04:18-04:21, val_ce range 1.27-5.50).
`/Users/ghost/etc/models/animalm-v[1-4]/final.pt` = different lineage (Mistral-7B perturbation, not byte-CLM-v2).

### (b) ubu1 + ubu2 remote
ubu1: 5 best.pt (clm_v4_350m + decoder_cpu byte-CLM 36.7M @ step 36500). decoder_cpu/best.pt has byte-vocab=256, dim=384/L=6 matching train_clm_v2 "Base" config but val_ce=0.0068 + step 36500 → distinct higher-step lineage, NOT v2 18M.
ubu1 `.growth/absorbed/`: 5 metadata JSON markers for clm_v2 family (anima__anima__checkpoints__clm_v2{,_tiny,_small,_base,_medium}__final.pt.json) — originals consumed 2026-04-04T17:07; content_preview is ZIP header only, no usable binary.
ubu1 `ready/anima/checkpoints/clm_v2_large/` = EMPTY directory (4096-byte stub).
ubu2: no concrete v2 .pt; only training stubs + venv tokenizer.

### (c) HF accounts alt orgs + dancinlife personal
`dancinlife` HF user: 0 models, 0 datasets, 0 spaces (only `need-singularity` org membership). Auth token stale (401). HF cache `~/.cache/huggingface/hub/` lists only need-singularity + standard public 3rd-party (Mistral/Llama/Qwen/Gemma/Phi/GPT2/Pythia).
**HIT**: `need-singularity/clm-v2-byte-18m-convo-5k` PUBLIC repo with convo_5k.pt 73.74MB.

### (d) GitHub gists + TimeMachine
`gh api users/dancinlife/gists`: 23 gists, all <1MB text (md/html/js/py/xml), zero .pt/.bin/.safetensors.
`tmutil`: no destinations configured, no machine directory (TimeMachine inactive on this Mac).

### (e) v2 18M byte signature match
`FOUND_VIA_HF_PUBLIC_REPO`: convo_5k.pt verified loadable with 0 missing/unexpected keys, params=18.52M.
Provenance: rebuilt today by sibling BG from `/tmp/anima_v2_source/conscious_lm.py` (extracted from ready/.git commit bb99b6b6) + corpus retrain to 5K convo steps. **NOT a recovered original 2026-03-28 snapshot — it is RECONSTRUCTED_NOT_RECOVERED.**

## 5 honest C3

1. **deep research did NOT independently locate v2 18M**; the find chain was mdfind→`/private/tmp/anima_v2_check/`→`verdict_v2.json`→HF repo. Sibling BG (chat_smoke 2026-05-06) had already completed the actual recovery via `ready/.git@bb99b6b6` 9+ hours earlier. This BG's contribution is **confirmation + cross-channel exhaustion**, not original discovery.
2. **the 5 anima_v2_check variants ARE NOT the 18M production v2** — they are 2026-03-30 sweep snapshots @ step=500 (or 30) with params 0.35M/1.70M/1.17M/8.45M/27.93M. The 18.52M production weights live on HF, built today.
3. **the HF artifact is fresh-built today, not archaeologically recovered**. The "v2 18M byte" weights as we have them are RECONSTRUCTED from architecture spec + retrain, not from any preserved 2026-03-28 .pt file. The original 2026-03-28 binary remains lost (consumed by .growth/absorbed pipeline 2026-04-04 with only ZIP-header metadata retained).
4. **chat capability FAILS despite valid weight load**. F_CLM_NATIVE_alpha_1_PASS=false; KO ratio 0.0 across all 5 prompts; gibberish output. Possible causes: byte tokenization mismatch, gate=0.001 inference path, undertrained at 5K convo steps for KO emergence, or architectural detail drift in retraining script.
5. **TimeMachine unavailable + Dropbox/iCloud/GoogleDrive empty + ubu remote .growth/absorbed = metadata-only**. The 2026-03-28 originals are CONFIRMED LOST across all preserve channels. The deep research answer for "where is the 2026-03-28 v2 18M weights file" is: NOWHERE; the canonical artifact is the rebuilt HF copy.

## Next steps

- **N1** Pin HF commit `1af2bcaeaf70c1d0b1a19939a8ada79a28f8cd30` of `need-singularity/clm-v2-byte-18m-convo-5k` in dependency lockfile; verify sha256=`2f0ba391aff30f6a60bcefccb9215fdb45764bf07147f28c38013ca629881bbe` on download.
- **N2** Investigate chat_smoke FAIL root cause: byte tokenization, gate=0.001 inference, undertraining at 5K convo steps, or retraining script architectural drift vs original ready/.git@bb99b6b6 spec. Cross-ref `anima_clm_v2_chat_recovered_2026_05_06.ai.md`.
- **N3** Catalogue the 5 mac `/private/tmp/anima_v2_check/` variants (especially `clm_v2_base` 27.93M @ step 500 val_ce 1.27) as ablation/lineage reference, NOT as production weights.
- **N4** Catalogue ubu1 `decoder_cpu/best.pt` (36.72M @ step 36500, val_ce 0.0068, byte-vocab=256, dim=384/L=6) as separate train_clm_v2 "Base" lineage @ higher step count — distinct from convo-5k fine-tune branch.
- **N5** Close `weights_archaeology` lane as `RECONSTRUCTED_NOT_RECOVERED`. Cross-cycle convergence (BG-EQ + BG-FA + BG-FK + BG-FL + BG-FM): NO additional 2026-03-28 originals exist anywhere; HF rebuilt copy is the only operational artifact.

## Artifacts

- `/Users/ghost/core/anima/state/anima_clm_v2_deep_research_2026_05_06/verdict.json`
- `/Users/ghost/core/anima/state/anima_clm_v2_deep_research_2026_05_06/search_paths.txt`
- `/Users/ghost/core/anima/state/anima_clm_v2_deep_research_2026_05_06/candidates_found.json`

## Cost + time

- spend: $0
- wall: ~25 minutes
- tool uses: ~30 / 50 budget

## Constraints honored

- $0 (mac local + ssh + HF API read-only + GitHub API read-only)
- raw#9/10/15/37
- HF token via `secret get hf_token` env-var only (no leak; redacted in this doc)
- no commit
- bash 3.2 compat (avoided readarray/`<<<`)
- ssh ConnectTimeout=5
