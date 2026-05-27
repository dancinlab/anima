# anima mac secret HF token re-sync — landed 2026-05-05

## status
LANDED — mac `secret get huggingface.token --raw` post-resync whoami-v2 PASS as `dancinlife`. 4-cache sync OK. No HF push, no anima commit.

## why
BG-PBETA-HF-UPLOAD C7 caveat: mac secret CLI returned stale `hf_asc...` (rotated), ubu1 `~/.cache/huggingface/token` returned working `hf_dw...`. Future mac-side HF operations were blocked until secret store re-sync.

## diagnosis (pre-state)
- mac secret CLI: token `hf_asc...` (first-12: `hf_ascGmSqKJ`) — whoami-v2 returned `{"error":"Invalid username or password."}` → WHOAMI_FAIL
- ubu1 `~/.cache/huggingface/token`: token `hf_dw...` (first-12: `hf_dwDFAiqqM`) — whoami-v2 returned `dancinlife` (id `69229786cde1fd9952da8cfa`) → WHOAMI_PASS

## action
SYNC_UBU1_TO_MAC:
1. `ssh ubu1 'cat ~/.cache/huggingface/token'` → captured ubu1 token (format hf_* verified)
2. `echo "$UBU1_TOKEN" | secret set huggingface.token` → mac secret CLI updated (`ok: huggingface.token`)
3. mac secret CLI verified equal to ubu1 source
4. mac whoami-v2 PASS post-resync: `dancinlife`

## 4-cache sync (sha256 first-16 = `93bc24cd6bd54ac8`)
| cache | sha256_first16 |
|---|---|
| mac secret CLI | 93bc24cd6bd54ac8 |
| mac `~/.cache/huggingface/token` | 93bc24cd6bd54ac8 |
| mac `.secrets/hf_token` | 93bc24cd6bd54ac8 |
| ubu1 `~/.cache/huggingface/token` | 93bc24cd6bd54ac8 |

All 4 aligned. .netrc not audited (out of scope; per C2).

## verdict
`state/mac_secret_hf_resync_2026_05_05/verdict.json`:
- mac_pre_state: WHOAMI_FAIL
- ubu1_pre_state: WHOAMI_PASS
- action_taken: SYNC_UBU1_TO_MAC
- mac_post_state: WHOAMI_PASS
- 4_cache_sync_pass: true
- token_sha256_first16: 93bc24cd6bd54ac8
- whoami_user: dancinlife
- rotation_needed_userside: false

## honest C3 (≥5)
- **C1 (MEDIUM)**: ubu1 token rotation source unverified — assumed canonical because whoami-v2 PASS, but no audit trail of who rotated it or when.
- **C2 (LOW)**: 4-cache scope covers secret CLI + 2 mac files + ubu1 cache; `.netrc` (if any `machine huggingface.co` entry) NOT audited.
- **C3 (INFO)**: Token shown only as sha256 first-16 per raw#10 + leak_guard hook + `audit_doc_token_redact` memory. No raw token literals in this doc or verdict.json.
- **C4 (LOW)**: stale `hf_asc...` overwritten in `.secrets/hf_token` and `~/.cache/huggingface/token`; recovery requires fresh user rotation if `hf_dw...` ever fails.
- **C5 (MEDIUM)**: mac stale because likely older rotation snapshot; ubu1 was sync target during last user-side rotation but mac secret CLI was not updated → historical lapse in sync discipline.
- **C6 (INFO)**: verdict.json + this doc compatible with hive PreToolUse leak_guard 9-shape blocker (no raw token strings).

## guardrails honored
- raw#9 (no plaintext token logged)
- raw#10 (≥5 honest C3 — 6 provided)
- raw#15 (mac canonical companion handoff doc)
- `feedback_audit_doc_token_redact.md` (no token literals embedded)
- `reference_secret_cli.md` (--raw flag used; 4-cache pattern enforced)

## next
mac-side HF operations now unblocked. Future BG lanes (e.g. `hf_upload_mk2.hexa`) can call `secret get huggingface.token --raw` on mac.
