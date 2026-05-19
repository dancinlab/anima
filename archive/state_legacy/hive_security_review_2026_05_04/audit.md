# Hive Repo Security Review — Pre-Push Audit

- **cycle**: hive_security_review_2026_05_04
- **ts_utc**: 2026-05-04T11:30:43Z
- **scope**: read-only audit of `/Users/ghost/core/hive/scripts/leak_guard_pretool.bash` + `/Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json` ahead of GitHub `dancinlab/hive` push (currently untracked + uncommitted).
- **repo visibility**: **PUBLIC** (`gh repo view dancinlab/hive --json visibility` = `"PUBLIC"`).

---

## 1. Inventory snapshot

### 1.1 leak_guard_pretool.bash

- path: `/Users/ghost/core/hive/scripts/leak_guard_pretool.bash`
- mode: `-rwxr-xr-x` (executable, owner ghost:staff)
- size: 3266 bytes, 65 LoC
- mtime: May 4 19:16
- repo state: `?? scripts/leak_guard_pretool.bash` (untracked — not yet staged or committed)

### 1.2 settings.json

- path: `/Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json`
- mode: `-rw-r--r--`
- size: 1041 bytes, 24 LoC
- mtime: May 4 19:32
- repo state: `?? claude-config/` (entire dir untracked)

### 1.3 Hive repo working tree

```
M  spec/host_pool.spec.yaml      (pre-existing modification — not in scope)
?? claude-config/
?? scripts/leak_guard_pretool.bash
```

Recent commits (HEAD..HEAD~7):

```
54ebec933 feat(bin/cl): drop bash arrow loop — let cl.hexa run the picker
d19425765 fix(bin/cl): drop bash-side prompt — hexa already renders it
8a22df2b4 fix(bin/cl): Korean prompt + show target slot in cursor indicator
…
```

No prior `claude-config/` or `scripts/leak_guard_*` commits in HEAD~8. The two artifacts are first-introductions to the repo.

---

## 2. Token-regex exposure risk

### 2.1 Patterns published if pushed (lines 54-62 of hook)

| Label | Regex | Length min |
|---|---|---|
| GitHub_FineGrained | `github_pat_[A-Za-z0-9]{30,}` | 30 |
| GitHub_PAT        | `ghp_[A-Za-z0-9]{36}`         | 36 |
| GitHub_App        | `ghs_[A-Za-z0-9]{36}`         | 36 |
| GitHub_OAuth      | `gho_[A-Za-z0-9]{36}`         | 36 |
| Anthropic         | `sk-ant-[A-Za-z0-9_-]{30,}`   | 30 |
| HuggingFace       | `hf_[A-Za-z0-9]{30,}`         | 30 |
| RunPod            | `rpod_[A-Za-z0-9]{30,}`       | 30 |
| AWS_AccessKey     | `AKIA[A-Z0-9]{16}`            | 16 |
| Google_API        | `AIza[A-Za-z0-9_-]{35}`       | 35 |

### 2.2 Risk assessment

- **All 9 prefixes are industry-standard / publicly documented**:
  - GitHub: documented in `https://github.blog/2021-04-05-behind-githubs-new-authentication-token-formats/`.
  - Anthropic `sk-ant-`: documented in Anthropic API docs.
  - HuggingFace `hf_`: documented in HF security docs.
  - AWS `AKIA*`: appears in AWS official IAM policy examples.
  - Google `AIza*`: documented in Google Cloud API key spec.
  - RunPod `rpod_*`: documented in RunPod API docs.
- **Adversarial info gain ≈ 0**: anyone running a token-leak scanner (truffleHog, gitleaks, repo-secret-scan) already has these prefixes pre-baked. The hook is a *consumer* of public knowledge, not a *publisher*.
- **Length thresholds (`{30,}` / `{36}`)**: also derivable from token spec docs; trivially observable by generating a real token and counting characters.
- **Verdict**: **LOW** risk on regex exposure.

### 2.3 Stale token literals (lines 33-34)

```bash
STALE_HF_LYKZ='<HF_TOKEN_STALE_LYKZ_REDACTED>'
STALE_HF_RERB='<HF_TOKEN_STALE_RERB_REDACTED>'
```

- Both flagged "leaked AND rotated" (line 28-29 comment).
- Per anima MEMORY + state audit docs: these are the BG-Σ + cb3521bd2 leak tokens, since invalidated at HF.
- **Public exposure benign** — they cannot authenticate to HF anymore.
- **PR description note required**: must explicitly call out that these literals are **post-rotation evidence values**, not live secrets, so reviewers / scanners do not raise false alarms (gitleaks WILL fire on these patterns).

### 2.4 settings.json content review

- `command` field hard-codes user-local path `/Users/ghost/core/hive/scripts/leak_guard_pretool.bash`. Generic enough — other operators clone to a different prefix and adjust. Not a leak.
- `_bind_revert_cmd` field references `/Users/ghost/.hive/...bak.bind_activation_20260503_112759`. User home path leak (`ghost`) — already implicit from `/Users/ghost/core/hive` path; no incremental info gain.
- No tokens, no API keys, no env-var secret values. Schema reference points to public json-schema mirror.

### 2.5 Other secret scan

- `grep` for `secret`/`token`/`password`/`key` across both files: no hardcoded credential values. Single hit on hook's `permissionDecisionReason` string (deliberate, "leak guard:" message text). Clean.

---

## 3. GitHub repo state check

```
$ gh repo view dancinlab/hive --json visibility
{"name":"hive","url":"https://github.com/dancinlab/hive","visibility":"PUBLIC"}
```

**Visibility = PUBLIC**. Push will be visible to entire internet + indexed by GitHub Code Search + scraped by AI training crawlers.

Push impact summary:
- New files visible: `claude-config/hive-hook-bus/settings.json`, `scripts/leak_guard_pretool.bash`.
- Two stale-but-rotated HF tokens become permanently grep-able in repo history (cannot redact retroactively without force-push + history rewrite).
- Token-detection regex set becomes public — already public-domain knowledge per §2.2.
- Symlink chain `~/.hive/claude-config/hive-hook-bus/settings.json -> /Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json` continues to work post-push (file path unchanged).

---

## 4. Recommended push sequence

Default recommendation: **PR_NOTE_REQUIRED** — push OK with a PR/commit description that explicitly calls out the stale-token literals.

### 4.1 Recommended commit message template

```
feat(security): hive-hook-bus PreToolUse leak guard

- claude-config/hive-hook-bus/settings.json — Claude Code hook config
  (PreToolUse=Bash|Write|Edit|MultiEdit -> scripts/leak_guard_pretool.bash)
- scripts/leak_guard_pretool.bash — bash 3.2 compatible token-shape detector,
  9 regex patterns (industry-standard public token prefixes)

NOTE: lines 33-34 contain TWO stale HuggingFace token literals
(STALE_HF_LYKZ, STALE_HF_RERB) that were leaked + rotated on 2026-05-03.
These are intentional evidence values used to suppress audit-doc-cited
references during scan. Both are dead at HuggingFace; cannot authenticate.

Trigger context: 2026-05-04 BG-Σ leak prevention. Hook is anti-leak
detection layer, NOT secret material.
```

### 4.2 Push command (user runs)

```bash
cd /Users/ghost/core/hive
git add claude-config/hive-hook-bus/settings.json scripts/leak_guard_pretool.bash
git commit  # paste template above
git push origin main
```

### 4.3 Post-push verification

1. Confirm hook still active: trigger a tool call with a fake `hf_` token-shaped string in a sandbox; expect `permissionDecision":"deny"`.
2. Confirm symlink integrity: `readlink ~/.hive/claude-config/hive-hook-bus/settings.json` → `/Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json`.
3. Confirm gitleaks/truffleHog scan on the new commit: expect 2 stale-HF hits → mark as known-rotated in repo `.gitleaksignore` (optional follow-up).

### 4.4 Alternative: HOLD path

If the user prefers zero stale-token literals in public history:
- Replace lines 33-34 with hashes (e.g., `STALE_HF_LYKZ_SHA256='<hash>'`) and adjust line 38-39 stripper to compute SHA256 of `TOOL_INPUT` substrings.
- Cost: hook complexity ↑, bash 3.2 SHA256 portability ↓ (requires `shasum`).
- Benefit: zero raw token strings in public repo.
- Recommendation: **defer** — the rotated-token risk is benign per §2.3.

---

## 5. Honest C3 (≥4)

1. **Audit is read-only — push not executed**. The hive working tree shows `??` for both files (untracked). No commit, no push performed by this BG. User must execute §4.2 manually.
2. **Stale-token rotation status is asserted from anima MEMORY + commit-message hearsay, not from a live HF API verification**. This audit did NOT call HF whoami with these token literals to confirm 401 — that would itself be a token-handling event the leak guard would block. Recommend user confirm rotation independently before trusting "benign" classification.
3. **Public visibility lookup used `gh` CLI under user's auth context**. If `gh` is misconfigured / pointing at a different account, the visibility result could be wrong. Cross-check at https://github.com/dancinlab/hive recommended.
4. **The hook itself is a partial defense**, not complete leak prevention. It only catches token-SHAPED strings in `tool_input` JSON for Bash/Write/Edit/MultiEdit. Read tool, network egress (curl in unrelated tools), file content already on disk — all out of scope. Adversaries with novel token formats (no prefix match) bypass entirely.
5. **`_bind_revert_cmd` in settings.json references a `.bak.bind_activation_20260503_112759` file under `~/.hive/`**. That backup file is OUTSIDE the hive repo (still in dotfile-style location). If user's home dir is compromised, revert command depends on a file the repo cannot guarantee exists. Recommend documenting the backup file's expected SHA256 in settings.json comment.
6. **No diff against last-known-good baseline**. The hook + settings are first-introductions to the repo (no prior version to diff). Cannot verify "no regression." Reviewer must read all 65 + 24 LoC line-by-line; this audit covered the full file content.
