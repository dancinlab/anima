# BG-π² cross-repo commit summary — .own mk1 cleanup 2026-05-04

**Cycle**: `own_mk1_cleanup_2026_05_04`
**User policy**: dual-SSOT EOL Option B (mk1_GRANDFATHER + UNKNOWN git rm; mk2_VERIFIED keep)
**Cross-link**: anima audit commit `39b83cb9` (BG-ζ .own mk2 verification)
**Push status**: PENDING (user authorizes separately — no remote push from this BG)

## 5 commits

| # | Repo | Branch | Commit | File removed | Class | Bytes |
|---|------|--------|--------|--------------|-------|-------|
| 1 | hexa-lang | `diag/orpheus-selftest-sigkill` ⚠ | `7569e423` | `.own` | mk1_GRANDFATHER | 3679 |
| 2 | nexus | `main` | `39acf0ec` | `.own` | mk1_GRANDFATHER | 37054 |
| 3 | orpheus | `main` | `6a1fc6c` | `.own` | mk1_GRANDFATHER POST_MK2_RECENT | 24296 |
| 4 | wraith-wallet | `main` | `5f09433` | `.own` | mk1_GRANDFATHER | 21321 |
| 5 | hexa-os | `main` | `5745a1b` | `.own-rules.json` | UNKNOWN | 1052 |

⚠ hexa-lang is NOT on main — user must decide merge or push-as-branch.

## launchctl coupling

- `dev.hexa-lang.atlas-absorb-sweeper` was loaded; **unloaded** before nexus rm.
- exit_code: 0; post-state: GONE.
- plist file untouched at `~/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist` (re-arm possible).

## Recommended push order

```bash
# 1. nexus (primary launchctl-coupled)
git -C /Users/ghost/core/nexus push origin main

# 2. hexa-lang (NON-MAIN — user verify intent FIRST)
#    Option A: merge to main, then push
#    Option B: push branch as-is
#    git -C /Users/ghost/core/hexa-lang push origin diag/orpheus-selftest-sigkill

# 3. hexa-os
git -C /Users/ghost/core/hexa-os push origin main

# 4. wraith-wallet
git -C /Users/ghost/core/wraith-wallet push origin main

# 5. orpheus
git -C /Users/ghost/core/orpheus push origin main
```

## Kept (mk2_VERIFIED — untouched, verified intact)

- `/Users/ghost/core/anima/.own` (63595 bytes, mk2 SSOT)
- `/Users/ghost/core/canon/.own.readme` (17682 bytes, mk2_VERIFIED)
- `/Users/ghost/core/canon/.own.group_p` (10283 bytes, mk2_VERIFIED)

## Non-overlap assertions

- did NOT touch hexa-lang/stdlib/ (BG-α³ territory)
- did NOT push any remote (user authorizes separately)
- did NOT modify launchctl plist file (only unloaded service)
- did NOT chflags
- selective `git commit -- <file>` in nexus + orpheus to avoid bundling unrelated dirty siblings
