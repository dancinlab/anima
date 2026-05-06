# anima git deep search — clm_v2 weights archaeology last residual landed 2026-05-06

## TL;DR — verdict FAIL_NO_DEEP_TRACE

clm_v2 18M byte-level (commits bb99b6b6 / 6abc42f6 / 13b20f90, 2026-03-28) `.pt` weights are **NOT recoverable from any git plumbing layer of anima OR ready/.git**.

The five `.growth/absorbed/anima__anima__checkpoints__clm_v2{,_base,_medium,_small,_tiny}__final.pt.json` manifests preserve the first ~1KB of each `.pt` pickle (PK ZIP header + `tok_emb` / `pos_emb` / `blocks.0.ln1` tensor schema visible) — confirming the weights once existed but were stored at `/Users/ghost/Dev/ready/anima/anima/checkpoints/clm_v2*/final.pt` (absorbed `2026-04-04T17:07:32`) — a path **outside both git repos**. The v2 era `.gitignore` excluded `checkpoints/`.

BG-EQ's prior conclusion stands: only `AnimaLM` final.pt rename (blob `56dfa7c6`, 14.2MB at `models/animalm/checkpoints/final.pt`) is committed; clm_v2 was never in git history.

## sub-task results

### Sub-1: anima reflog --all (deep)
- 204 entries total — oldest reaches 2026-05-04
- v2 era (2026-03-28) **aged out** of reflog window (dense activity since 2026-05-04 push reflog rotation)
- direct grep `clm_v2 / 18M / byte-level / dialogue_ft / ConsciousLM` in `git log --walk-reflogs --all`: 1 hit (45ab7e37 = today's clm-3 β' commit referencing clm_v2_chat ROADMAP, not clm_v2 weights)

### Sub-2: anima fsck --lost-found --unreachable
- 555 unreachable blobs / 61 unreachable commits / 0 dangling
- top large blobs >50MB: corpus_v5.txt (104MB), p9 sft_data jsonl (79MB), p9 r16 sft (72MB), corpus_v2.txt (70MB) — **NO .pt blobs**
- 4 unreachable commits mention "v2" but all unrelated lanes:
  - f60afe27 `index on main: dd1e30f6 CLM-2 V2_PARTIAL_HS_ONLY` (2026-05-05, CLM-2 LoRA lane)
  - 5a916031 `V5/V6/STRICT closure` (2026-05-05, shim v5 lane)
  - 9722b905 untracked files on main: dd1e30f6 (2026-05-05)
  - a1740306 `p9 path A retrain v2 EXEC` (2026-05-04, p9 lane)

### Sub-3: ready/.git embedded full repo deep search
- size: 7.1GB / git repo (NOT worktree symlink)
- remote: `https://github.com/need-singularity/anima.git` (same as anima)
- HEAD: `ssot-hexa-first-fix` branch
- v2 era commits PRESENT — bb99b6b6 / 6abc42f6 / 13b20f90 cat-file confirms full commit message ("18M parameter byte-level model", CE=1.29, CE=0.04 dialogue_ft)
- **trees contain only .py source code** (.gitignore excluded `checkpoints/`)
- ready fsck: **0 dangling commits / 0 dangling blobs** (clean — likely fresh ssh fetch)
- top large blobs: corpus files (en.txt 3.2GB, ko.txt 2.0GB, zh.txt 1.6GB, code.txt 1.5GB, ja.txt 1.0GB, ru.txt 1.0GB) and `next-swc.darwin-arm64.node` (115MB) — **NO clm_v2 .pt**
- AnimaLM .pt files committed:
  - `models/animalm/checkpoints/final.pt` (blob 56dfa7c6, 14.2MB) — anima + ready both
  - `checkpoints/animalm/animalm_step_50.pt` (blob d08ad3ec, 14.2MB) — ready only
  - `data/self_learning/self_learner_state.pt` (35KB) — ready only
  - `anima-agent/data/default/agent_state.pt` (18KB) — ready only

### Sub-4: deleted commits / force-push history
- `git log --walk-reflogs --all` exhausted reflog window
- 4 unreachable v2-keyword commits (Sub-2) all post-2026-05-04 unrelated lanes
- no force-push artifacts from 2026-03-28 era (already aged out)

### Sub-5: stash + worktrees
- 14 stashes, 0 mention clm_v2 weights (pre-cherry-pick, pre-layout-migration, WIP, an11_b_templates, anima_tui, etc.)
- 1 worktree: anima itself on main

### Sub-6: .growth/absorbed/ smoking gun (the residual evidence)

5 manifests with `value_grade=critical`, n6_score 41.66~50.0:
| manifest | content_preview tensor schema | inferred dim |
|---|---|---|
| clm_v2 (step_050000.pt) | tok_emb 256 × ?, pos_emb cuda:0 | byte vocab 256 |
| clm_v2_base (final.pt) | tok_emb 256 × ?, mps, FloatStorage | byte vocab 256 |
| clm_v2_medium (final.pt) | tok_emb 256 × 256?, mps | byte vocab 256 |
| clm_v2_small (final.pt) | tok_emb 256 × 192?, mps | byte vocab 256 |
| clm_v2_tiny (final.pt) | tok_emb 256 × 64?, mps | byte vocab 256 |

absorbed_from: `/Users/ghost/Dev/ready/anima/anima/checkpoints/clm_v2{,_base,_medium,_small,_tiny}/final.pt`
absorbed timestamp: `2026-04-04T17:07:32.467034` (clm_v2 first, then 4 sibs in same scan)

## v2 .pt signature match — NOT_FOUND_DEEP

Reason: weights existed (manifest pickle header proves byte-level torch tensors) but `.gitignore` excluded `checkpoints/` directory. No git plumbing layer (reflog / fsck / pack-objects / lost-found / dangling commits / stash / worktree / submodule) holds a recoverable v2 `.pt` blob. The 1KB pickle preview cannot reconstruct full weights.

## 5 honest C3

1. **C3-1**: clm_v2 weights NOT recoverable from anima OR ready/.git — deep search exhausted. reflog + fsck + stash + dangling + pack-objects all probed, 0 .pt blobs match v2 signature.
2. **C3-2**: `.growth/absorbed` manifests are THE ONLY remaining trace. content_preview proves architecture (5 sizes, byte vocab 256, mps trained, step_050000 / final converged) but 1KB pickle preview cannot reconstruct weights.
3. **C3-3**: ready/.git is a 7.1GB FULL anima history snapshot containing v2 SOURCE CODE commits (bb99b6b6 / 6abc42f6 / 13b20f90) — but `.gitignore` excluded `checkpoints/`, so weights were never tracked. ready fsck is clean.
4. **C3-4**: BG-EQ's prior conclusion (only AnimaLM final.pt rename in git) STANDS — deep search adds zero new recoverable artifacts. AnimaLM final.pt is 14.2MB (NOT clm_v2 18M; AnimaLM is a separate model lane).
5. **C3-5**: original .pt files lived at `/Users/ghost/Dev/ready/anima/anima/checkpoints/clm_v2*/final.pt` absorbed 2026-04-04. **If user retains a backup of `/Users/ghost/Dev/ready/`**, weights may exist on filesystem outside git. Recommend filesystem search next.

## Next steps

- **STEP-1**: filesystem search `/Users/ghost/Dev/ready/anima/anima/checkpoints/clm_v2*/final.pt` — path indicated by `.growth/absorbed` manifests; absorption was 2026-04-04, recent files plausible
- **STEP-2**: if STEP-1 finds files → archive to HF Hub (own 14 mandate: weights → HF, not git)
- **STEP-3**: if STEP-1 empty → treat clm_v2 as PERMANENTLY LOST WEIGHTS; only retrainable from preserved tokenizer / hypothesis-fixture / training data (corpus_v2.txt 70MB IS in anima git as blob 506f826e)
- **STEP-4**: reorient clm-3 β' KoGPT2 head-swap as canonical chat-cap recovery path (already 2026-05-06 commit 45ab7e37 lane: `clm_native_chat / clm_v4_chat / clm_v2_chat` roadmap)
- **STEP-5**: document v2 weight loss as historical incident — own 14 ('models → HF Hub only') mandate retroactively justified by this loss

## Outputs

- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/verdict.json`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/reflog_excerpts.txt`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/fsck_dangling.txt`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/fsck_full.txt`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/ready_fsck.txt`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/anima_large_blobs.txt`
- `/Users/ghost/core/anima/state/anima_git_deep_search_2026_05_06/ready_large_blobs.txt`

## Cost

- $0 (mac local + git plumbing only)
- ~25min wall, 19 tool uses

## raw compliance

- raw#9 PASS (no LOCKED files touched)
- raw#10 PASS (no destructive ops)
- raw#15 PASS (read-only git plumbing)
- raw#37 PASS (only .json + .md state outputs; no .py created)
