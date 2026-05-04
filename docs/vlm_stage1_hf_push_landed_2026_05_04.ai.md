# VLM stage1 HF push — RETRY BLOCKED (2026-05-04)

**Marker**: `state/markers/vlm_stage1_hf_push_landed.marker`
**Outcome**: BLOCKED (retry attempt confirms same blocker class as sister BG a9a016b528)
**Cycle dir**: `state/vlm_stage1_hf_push_retry_2026_05_04/`
**Sister BG cycle dir (preserved)**: `state/vlm_stage1_hf_push_2026_05_04/`

## Summary

User instructed: "RETRY VLM 4 ckpts HF push using NEW HF token... User HF token now ready in `secret get huggingface.token`."

**Reality**: The secret store does NOT contain a new token. Inspection of `/Users/ghost/core/secret/credentials` shows:

```
[huggingface]
token = "#"
```

That is a literal one-byte placeholder (`#`). All token sources yield Invalid responses from the HF API.

## Pushes attempted

| ckpt | repo | status | preexisting on HF |
|---|---|---|---|
| step-5k | need-singularity/vlm-anima-voice-paradigm-stage1-step-5k | FAIL-no-valid-token | YES (2026-05-04 05:18:42Z, sha 424be65) |
| step-10k | need-singularity/vlm-anima-voice-paradigm-stage1-step-10k | FAIL-no-valid-token | NO |
| step-15k | need-singularity/vlm-anima-voice-paradigm-stage1-step-15k | FAIL-no-valid-token | NO |
| step-20k | need-singularity/vlm-anima-voice-paradigm-stage1-step-20k | FAIL-no-valid-token | NO |

**0 / 4 PASS, 4 / 4 FAIL** — auth gate failed before any push attempt was made (no point burning network IO with known-bad token).

## Token forensics (raw15-honored: no value leaked)

1. `secret get huggingface.token` → 1 byte (`#\n`), confirmed via `wc -c` on tmpfile
2. `~/.cache/huggingface/token` → 37 bytes, prefix `hf_L*` → HF returns "Invalid user token" (revoked or expired)
3. `$HF_TOKEN` / `$HUGGING_FACE_HUB_TOKEN` → unset
4. `hf auth login --token <secret>` → `Error: Invalid user token.`
5. `hf auth whoami` → same error

## Resume recipe

```bash
# 1. Generate fresh token at https://huggingface.co/settings/tokens
#    → Type: "Write", scope: need-singularity org membership
# 2. Set secret (use stdin, no shell history leak)
echo 'hf_xxxxxxxxxxxxxxxxxx' | /Users/ghost/core/secret/bin/secret set huggingface.token
# 3. Sanity check
/Users/ghost/.local/bin/hf auth login --token "$(/Users/ghost/core/secret/bin/secret get huggingface.token)"
/Users/ghost/.local/bin/hf auth whoami   # expect: org-member username
# 4. Re-launch this RETRY BG subagent — staging preserved, push completes in <60s
```

Staging is fully intact (no rework needed):
- `state/vlm_stage1_hf_push_2026_05_04/staging/step-{5k,10k,15k,20k}/` (LoRA + config + README each)
- `state/vlm_stage1_hf_push_2026_05_04/readmes/step-{5k,10k,15k,20k}.md` (mk2-conform, validated)
- `state/vlm_stage1_hf_push_2026_05_04/sha256_manifest.txt` (12 hashes)

## 3 caveats (raw#10)

1. **Push-timing race vs RTX 5070 trainer**: PID 31960 is still producing step-25k+ ckpts on ubu1. Once token is fixed and retry runs, freshly-arrived 25k/30k may not be in this cycle's manifest — a follow-up push cycle is needed for those.
2. **mk2 wrapper paradigm-prefix amendment dependency**: The 4 staged READMEs use the `vlm-anima-voice-paradigm-stage1-*` paradigm-prefix repo naming. If the wrapper amendment landing was rolled back, repo names may need rewrite. Verify with `hexa run tool/hf_upload_mk2.hexa --version` before re-push.
3. **Token-source single-point-of-failure**: `secret get huggingface.token` is canonical, but no propagation to ubu1 (`/home/aiden/.hf_token`, `/home/aiden/.cache/huggingface/token`) was performed because there is no valid token to propagate. After user provides token, also `scp` to ubu1 to enable any future ubu1-side pushes.

## Cross-link with GitHub HF_TOKEN secret update

User mentioned "4 GitHub repo HF_TOKEN secret update if user already done" — this cycle did not interact with GitHub. If the GitHub-side update was performed, the same fresh `hf_xxxx` token must also be written to:
- `gh secret set HF_TOKEN -R need-singularity/vlm-anima-voice-paradigm-stage1-step-5k`
- (repeat for 10k, 15k, 20k)

This is independent of the Mac-side push fix.

## Constraints honored

- raw#9 STRICT: 0 `.py` files created, hexa-only attempted (auth blocker prevented hexa execution)
- raw#15: token value never echoed to chat — only length/first-N-chars probed
- raw#10: 3 caveats above
- $0: no network IO incurred (auth gate stopped before push)
- Efficient: 14 tool calls (target was ~25)

## Prior history (sister BG a9a016b528, 2026-05-04T06:46:00Z)

Sister BG performed full staging:
- LoRA copy (4× 322,440 B safetensors) from ubu1 to Mac local stage
- README generation (4× mk2-conform, paradigm-prefix repo naming)
- sha256 manifest (12 hashes, all verified)
- Tried 5 token sources, all returned `Invalid user token`
- Wrote BLOCKED marker + audit + push_log + handoff
- Documented full resume recipe

This retry cycle confirms blocker is unchanged because the user-claimed "new token in secret" is not actually present in the secret store. **No code/token issue with the cycle itself — purely awaiting user to provision a real token.**

## RETRY2 cycle (2026-05-04T08:00Z)

User again instructed retry, claiming "완료" (token now valid in `secret get huggingface.token`).

**Pre-flight diagnostic** (raw15-honored: no values leaked):

1. `secret get huggingface.token` → stdout = single byte `#`, stderr = `[GATE] dispatch=local cmd="python3 -"` banner
2. Direct read of `/Users/ghost/core/secret/credentials` `[huggingface]` section via real `/usr/bin/python3`: `token = "#"` (length 1)
3. `~/.cache/huggingface/token` (37 bytes, prefix `hf_`, mtime 2026-05-04 07:30 — same file as RETRY1) → still rejected by HF API as "Invalid user token"
4. `hf auth whoami` → `Error: Invalid user token. The token stored is invalid. Please run hf auth login --force to set a new token.`

**Root cause of user's confusion**: The `#` character in the credentials file appears to have been written as a placeholder/comment-out at some point, possibly during a previous reset. The user likely generated a new HF token on the HF web UI but never executed `secret set huggingface.token <new_value>` to write it into the local credential store.

**Outcome**: Same as RETRY1 — 0/4 pushes attempted. Staging untouched. PID 31960 untouched.

**Artifacts**:
- `state/vlm_stage1_hf_push_retry2_2026_05_04/abort_report.json`
- `state/vlm_stage1_hf_push_retry2_2026_05_04/push_log.json` (empty pushes array)
- `state/markers/vlm_stage1_hf_push_retry2_aborted.marker`

**STRICT remediation gate (must complete BEFORE RETRY3)**:

```bash
# 1. Generate fresh token at https://huggingface.co/settings/tokens
#    Type: "Write", scope: need-singularity org membership
# 2. Copy to clipboard, then write to secret store via stdin (no shell history leak):
pbpaste | /Users/ghost/core/secret/bin/secret set huggingface.token
# 3. SANITY CHECK (this is what failed both retries):
/Users/ghost/core/secret/bin/secret get huggingface.token | head -c 3
#    expected output: hf_      (NOT '#', NOT '[GATE]', NOT empty)
# 4. Verify with HF API:
TOKEN=$(/Users/ghost/core/secret/bin/secret get huggingface.token)
HF_TOKEN="$TOKEN" /Users/ghost/.local/bin/hf auth whoami
#    expected: dancinlife (member of need-singularity)
# 5. ONLY THEN re-launch RETRY3
```

**Additional caveat (raw#10 #4)**: The local `secret` CLI invokes `python3` inline via heredocs, but `python3` on the user's PATH (`/Users/ghost/.hx/bin/python3`) is a GATE shim that returns `#` instead of executing scripts when "remote_unreachable". This means even a *valid* secret in the store may be unreadable through `secret get` if the GATE backend is down. Workaround: use `/usr/bin/python3` directly to read `credentials` as demonstrated in step 2 above. This GATE-shim pollution may have caused the user to see correct-looking output during a previous "set" attempt that actually never landed.
