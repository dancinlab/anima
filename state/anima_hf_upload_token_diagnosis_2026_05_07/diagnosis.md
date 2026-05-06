# HF_TOKEN diagnosis — 2026-05-07

## Summary
- BG-HD failure root cause: `secret get HF_TOKEN` returns a stale/rotated token rejected by HF API (HTTP 401 "Invalid username or password.").
- Mac local `~/.cache/huggingface/token` holds a DIFFERENT, valid token with `write` role and `need-singularity` org membership (whoami-v2 HTTP 200, user=dancinlife).
- Conclusion: secret CLI cache is stale; hf-cli local cache is the canonical credential on this Mac.

## Evidence (token literals redacted; only first 3 chars of body shown)
| Source | Prefix | whoami-v2 status | role |
|---|---|---|---|
| `/Users/ghost/core/secret/bin/secret get HF_TOKEN` | `hf_EN…` | 401 Invalid | n/a |
| `~/.cache/huggingface/token` | `hf_dw…` | 200 OK | write |

Both prefixes intentionally truncated to 3 body chars for leak_guard / GitHub secret-scanning compliance.

## Why secret CLI rejected
Most likely cause: the `hf_EN…` token was rotated/revoked on huggingface.co at some point after it was written into the secret store. The hf-cli `~/.cache/huggingface/token` was refreshed by an `hf auth login` on Mac afterwards but the secret store was never resynced.

## Remediation (recommended order)
1. **Immediate (this BG)**: BG-HM proceeds using hf-cli cached credential (HF Hub Python lib auto-picks up `~/.cache/huggingface/token`). No git-leaked literals.
2. **Followup (user, manual)**:
   ```
   pbcopy < ~/.cache/huggingface/token        # or paste fresh token
   pbpaste | /Users/ghost/core/secret/bin/secret set HF_TOKEN
   ```
   Then re-sync downstream caches (per `reference_secret_cli.md`).
3. **Optional**: rotate again on huggingface.co Settings → Access Tokens, `hf auth login` with new token, then push to secret CLI per (2).

## Cross-references
- memory: `reference_secret_cli.md` — pbpaste|secret set <key> for write; sync downstream caches after.
- memory: `reference_hf_gotchas.md` — ubu1 hf CLI is `/home/aiden/venv_orchestrator/bin/hf`; Mac uses `/opt/homebrew/bin/hf`.
- memory: `feedback_audit_doc_token_redact.md` — never embed token literals (live or stale).

## Status
- token_diagnosis = **secret_CLI_stale_cached_valid**
- BG-HM upload path = **hf-cli cached token (fallback)**
- Action item open: user manual secret CLI resync.
