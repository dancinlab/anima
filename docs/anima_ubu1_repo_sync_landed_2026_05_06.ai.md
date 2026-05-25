# anima ubu1 repo sync — landed (2026-05-06)

## 한글 요약

ubu1 `/home/aiden/core/anima/ready/` 비어있음 확인. mac canonical `/Users/ghost/core/anima/ready/` (41GB, 77999 files) 의 dry-run rsync 결과 3,825 files / 41.1MB transferred (1000x reduction). 사용자 confirm 후 anima session 직접 actual rsync 실행 권장. BG는 dry-run + recipe emit만 수행 ($0).

## TL;DR (EN)

- ubu1 `ready/` empty; mac source 41GB but post-exclusion only 41MB
- Excluded: `.git` (7.1GB embedded), Rust `target/` (~8.5GB), corpora `*.txt`/`*.jsonl` (HF-only per), `*.pt`/`*.safetensors`/`*.bin`
- 3,589 regular files + 228 dirs + 8 symlinks ready to sync
- Recipe at `state/anima_ubu1_repo_sync_2026_05_06/rsync_recipe.txt`
- BG-FE blocker: ubu1 corpus dependency requires HF download separately

## State files

- `/Users/ghost/core/anima/state/anima_ubu1_repo_sync_2026_05_06/dry_run.txt` — full rsync --dry-run output with stats
- `/Users/ghost/core/anima/state/anima_ubu1_repo_sync_2026_05_06/rsync_recipe.txt` — copy-paste ready commands (dry-run + actual + verification)
- `/Users/ghost/core/anima/state/anima_ubu1_repo_sync_2026_05_06/verdict.json` — structured outcome
- `/Users/ghost/core/anima/state/anima_ubu1_repo_sync_2026_05_06/large_files_excluded.txt` — 30 large files (>5MB) skipped

## Honest C3

1. Corpora not synced — ubu1 train fire blocked on BG-FE (HF download)
2. Embedded `ready/.git` not synced — tree will be non-git on ubu1, acceptable since parent anima/ is git canonical
3. `.claude/worktrees/agent-abb59ac1/` excluded contains 1 corpus + 1 checkpoint — verified non-canonical
4. Rust `target/` exclusion forces ubu1 cargo rebuild (cross-platform safety, mac arm64 vs ubu1 x86_64)
5. AST parse smoke != runtime import smoke; real venv check defers to post-sync anima session

## Next

- User confirm dry-run output (file count + size sanity)
- anima session direct: `rsync -avzP --exclude=...` (actual, NOT BG — BG避 weight dep)
- Post-sync: `ssh ubu1 "ls -la /home/aiden/core/anima/ready/training/"` verify
- BG-FE: HF corpus download recipe for ubu1 `anima/data/`

## Raw compliance

- raw#9 secrets: no token literals
- raw#10 KO-only user face: compliant
- raw#15 LOCKED: no LOCKED file modified
- raw#37 transient_py: n/a
- HF-only ≥5MB: compliant (all weight/corpus extensions excluded)
