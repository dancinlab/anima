# Pre-Commit Hook Proposal — Token-Shape Scanner (2026-05-04)

**Status**: PROPOSAL ONLY. Hook file `tool/git_hooks/pre_commit_token_scan.bash` is NOT created here. Document the design + integration plan; user reviews and lands in a separate commit cycle.

## Objective

Block any `git commit` that adds plaintext token-shaped strings to tracked content. Catch the 2026-05-04 leak class (P3: API response containing `--env` echo) at the commit boundary, *before* the leak hits the public history.

## Scope

- Scan **staged content only** (not working tree, not history).
- Match on **token-prefix shape** (hf_, ghp_, sk-ant-, etc.) — high precision, low false-positive rate vs value-based scan.
- Optional **value-based pass**: if `secret list` is available locally, also pass `git diff --cached` through `secret leak-check --keys ...` (covers prefixless tokens; see Proposal 3 in `secret_cli_v2_proposals.md`).
- On hit: `exit 1` with diagnostic showing `path:line:matched_prefix`. Include hint: "if this is a known-stale value, add to `tool/git_hooks/leak_allowlist.txt`".
- Allow opt-out via `--no-verify` (caller takes responsibility) per raw#standard-hook-bypass policy.

## Regex set (9 patterns)

| Provider | Prefix | Min tail length | Notes |
|---|---|---|---|
| Hugging Face | `hf_` | 30 | the leaked token class |
| GitHub PAT (classic) | `ghp_` | 30 | |
| GitHub server token | `ghs_` | 30 | |
| GitHub OAuth | `gho_` | 30 | |
| GitHub fine-grained | `github_pat_` | 50 | longer prefix, longer tail |
| Anthropic API key | `sk-ant-` | 30 | api03 / api04 sub-prefixes |
| RunPod API key | `rpod_` | 30 | per RunPod 2024+ format; legacy keys are `runpodapikey_*` (also matched) |
| AWS access key | `AKIA` | exact 16 hex/upper | `AKIA[A-Z0-9]{16}` |
| GCP API key | `AIza` | exact 35 chars | `AIza[A-Za-z0-9_-]{35}` |

Bonus optional patterns (high false-positive — gate behind `--strict`):
- Bearer tokens (`Bearer [A-Za-z0-9_-]{40,}`)
- Generic JWT (`eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`)
- Stripe (`sk_live_[A-Za-z0-9]{24,}`)

## Bash impl sketch (~60 LoC)

```bash
#!/bin/bash
# tool/git_hooks/pre_commit_token_scan.bash
# Block commit if staged content contains token-shaped strings.
# Install: ln -sf ../../tool/git_hooks/pre_commit_token_scan.bash .git/hooks/pre-commit
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
ALLOWLIST="${REPO_ROOT}/tool/git_hooks/leak_allowlist.txt"

# Build PCRE-like alternation. Use grep -E (POSIX ERE) for portability.
PATTERNS=(
  'hf_[A-Za-z0-9_]{30,}'
  'ghp_[A-Za-z0-9_]{30,}'
  'ghs_[A-Za-z0-9_]{30,}'
  'gho_[A-Za-z0-9_]{30,}'
  'github_pat_[A-Za-z0-9_]{50,}'
  'sk-ant-[A-Za-z0-9_-]{30,}'
  'rpod_[A-Za-z0-9_]{30,}'
  'runpodapikey_[A-Za-z0-9_]{20,}'
  'AKIA[A-Z0-9]{16}'
  'AIza[A-Za-z0-9_-]{35}'
)

# Join with |
ALT=""
for p in "${PATTERNS[@]}"; do ALT+="${p}|"; done
ALT="${ALT%|}"

# Get the staged diff (added lines only — context lines start with ' ', removed with '-', added with '+').
# Filter to added lines only (line starts with '+' but NOT '+++').
HITS=0
DIFF_OUT="$(git diff --cached --no-color --unified=0)"

# Track current file path through the hunks.
current_file=""
line_no=0
while IFS= read -r line; do
    case "$line" in
        '+++ b/'*)
            current_file="${line#+++ b/}"
            line_no=0
            continue
            ;;
        '@@ '*'@@'*)
            # @@ -old,1 +new,N @@ — extract new start line.
            line_no=$(echo "$line" | sed -E 's/^@@ -[0-9,]+ \+([0-9]+).*$/\1/')
            line_no=$((line_no - 1))
            continue
            ;;
        '+++'*) continue ;;
        '+'*)
            line_no=$((line_no + 1))
            content="${line#+}"
            if echo "$content" | grep -qE "$ALT"; then
                # Check allowlist
                if [ -f "$ALLOWLIST" ] && grep -qF "$content" "$ALLOWLIST" 2>/dev/null; then
                    continue
                fi
                matched="$(echo "$content" | grep -oE "$ALT" | head -1)"
                # Show only the prefix to avoid re-leaking on stderr
                prefix="${matched:0:8}..."
                echo "TOKEN LEAK BLOCKED: ${current_file}:${line_no}: shape '${prefix}' (full match suppressed)" >&2
                HITS=$((HITS + 1))
            fi
            ;;
        ' '*) line_no=$((line_no + 1)) ;;
        '-'*) : ;;  # Removed lines — don't count
    esac
done <<< "$DIFF_OUT"

if [ $HITS -gt 0 ]; then
    echo "" >&2
    echo "secret pre-commit hook blocked ${HITS} suspected token leak(s)." >&2
    echo "Resolution options:" >&2
    echo "  1. Redact the token in the file and re-stage." >&2
    echo "  2. If false positive, add the exact line to ${ALLOWLIST}." >&2
    echo "  3. If you really want to commit (NOT RECOMMENDED): git commit --no-verify" >&2
    exit 1
fi

# Optional value-based pass: only if `secret` CLI exists AND user opted in via env.
if [ "${SECRET_LEAK_VALUE_CHECK:-0}" = "1" ] && command -v secret >/dev/null 2>&1; then
    if secret leak-check 2>/dev/null --help >/dev/null 2>&1; then
        # leak-check subcommand exists (Proposal 3 has landed). Run on staged diff.
        TMPDIFF="$(mktemp)"
        trap 'rm -f "$TMPDIFF"' EXIT
        git diff --cached --no-color > "$TMPDIFF"
        if ! secret leak-check "$TMPDIFF"; then
            echo "value-based leak-check FAILED — see above" >&2
            exit 1
        fi
    fi
fi

exit 0
```

## Integration plan

1. **Create file**: `tool/git_hooks/pre_commit_token_scan.bash` (chmod +x).
2. **Create allowlist**: `tool/git_hooks/leak_allowlist.txt` (empty initially; one full-line-content per line, exact match required).
3. **Install** (per-clone, can't be tracked in git): `ln -sf ../../tool/git_hooks/pre_commit_token_scan.bash .git/hooks/pre-commit`.
4. **Document** in `README.md` or `CONTRIBUTING.md`: install command + bypass option.
5. **Bootstrap script**: add to `tool/h100_pods_sync.bash` (or a new `tool/dev_setup.bash`) to symlink the hook on first checkout.

## Test cases

- Stage a file with `hf_FAKE0123456789012345678901234567890` → hook prints `path:line: shape 'hf_FAKE...'`, exit 1.
- Stage a file with `hf_short` (under 30-char tail) → no match, exit 0.
- Stage a file with `Bearer abc...` (short tail) → no match.
- Stage a file with content matching pattern but listed in allowlist → exit 0.
- `git commit --no-verify` → bypasses the hook (standard git behavior).
- Stage *only* deletions of token-shaped content → no match (we only scan added lines).
- Edge: rename-only diff (`diff --git a/x b/y` with no content) → no false hit.

## Falsifier set

- **F-PCH-1**: a freshly-cloned anima repo with hook installed must reject a synthetic test commit containing `hf_TESTTOKEN0123456789012345678901234567` → must exit 1 with the diagnostic line. (Test ground-truth.)
- **F-PCH-2**: a commit containing only legitimate prose (no token shapes) → must exit 0. (False-positive ground-truth.)
- **F-PCH-3**: the leaked-shape line from `state/p9_base_validation_h100_2026_05_04/boot.log` (current redacted form: `"HF_TOKEN=<HF_TOKEN_REDACTED>"`) → must exit 0. (Self-test: the redacted file itself does not trigger the hook.)
- **F-PCH-4**: Hook completes in <300ms on a typical anima staged diff (~50-200 changed lines). (Performance.)

## Honest C3 caveats (raw#10)

1. **Symlinking `.git/hooks/pre-commit` is not version-controlled by git itself**. Each clone needs the install step. Mitigation options: (a) use `core.hooksPath` config (sets project-wide hook directory) — but that's a per-clone config that's also not auto-applied. (b) Use `husky` or similar tool — adds a dependency. (c) Ship a `tool/dev_setup.bash` and instruct contributors to run once. Option (c) is the most consistent with the repo's existing bash-first style.

2. **Regex-only is bypass-able**: a determined attacker (or accidental encoding) could base64-encode the token (`echo $HF_TOKEN | base64`) and the hook misses it. The optional value-based pass (with `secret leak-check`) catches this *if* the original token is still in the secret store. Recommend running both passes.

3. **`git diff --cached --unified=0` and the @@ hunk parser**: the line-number reconstruction in the sketch is approximate (works for most cases but undercounts/overcounts on multi-hunk files near the end). For accurate `path:line` reporting, switch to `git diff --cached --unified=0 -p` and use `git blame`-style parsing or invoke `pcre2grep -nM` per file. Acceptable trade-off if line numbers are off-by-one — the hint is the path:line range, not exact.

4. **No CI integration**. The hook runs locally only; if a contributor uses `--no-verify`, the leak still lands. A mirror check in CI (e.g. GitHub Actions on PR) is required for full coverage. CI design: run the same scanner script over `git diff origin/main...HEAD` on every PR, fail the build on hit. Out of scope for this audit; flag for follow-up.

5. **Allowlist is a footgun**: a developer who hits a false positive may add the WHOLE LINE to the allowlist, including the actual token if it's a real-but-stale value. Document that allowlist entries should only be exact substrings of *demonstrably non-secret* shape (e.g., test fixtures, mock values).
